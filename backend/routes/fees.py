from flask import Blueprint, request, jsonify, Response
from db import get_connection
import pandas as pd

fees_bp = Blueprint('fees', __name__)

@fees_bp.route('/fees', methods=['GET'])
def get_fees():
    month = request.args.get('month')
    year = request.args.get('year')

    conn = get_connection()
    cur = conn.cursor()

    query = """
        SELECT s.student_id, s.name, s.roll_number, s.batch_name,
               CASE 
                   WHEN f.fee_id IS NOT NULL THEN 'Paid'
                   ELSE 'Unpaid'
               END AS fee_status
        FROM students s
        LEFT JOIN fees f
        ON s.student_id = f.student_id 
        AND f.month = %s AND f.year = %s;
    """

    cur.execute(query, (month, year))
    rows = cur.fetchall()

    result = []
    for row in rows:
        result.append({
            "student_id": row[0],
            "name": row[1],
            "roll_number": row[2],
            "batch_name": row[3],
            "fee_status": row[4]
        })

    cur.close()
    conn.close()

    return jsonify(result)


@fees_bp.route('/upload-csv', methods=['POST'])
def upload_csv():
    file = request.files.get('file')

    if not file:
        return {"error": "No file uploaded"}, 400

    file.seek(0)

    try:
        df = pd.read_csv(file, encoding='utf-8-sig')
    except Exception:
        file.seek(0)
        df = pd.read_csv(file, encoding='latin1')

    # Normalize columns
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace('\ufeff', '', regex=False)
        .str.replace(r"[^\w]", "_", regex=True)
    )

    print("FINAL COLUMNS:", df.columns.tolist())
    print(df.head())

    # Validate columns
    required_cols = ['roll_number', 'month', 'year', 'amount_paid', 'payment_date']
    missing = [col for col in required_cols if col not in df.columns]
    if missing:
        print("Missing columns:", missing)
        return {"error": f"Missing columns: {missing}"}, 400

    # FIX 1: Parse dates and validate — NaT will cause silent DB failures
    df['payment_date'] = pd.to_datetime(df['payment_date'], errors='coerce')
    bad_dates = df[df['payment_date'].isna()]
    if not bad_dates.empty:
        print("Rows with invalid payment_date:", bad_dates['roll_number'].tolist())
        return {
            "error": f"Invalid or missing payment_date for roll numbers: {bad_dates['roll_number'].tolist()}"
        }, 400

    conn = get_connection()
    cur = conn.cursor()

    inserted = 0
    skipped = []

    try:
        for _, row in df.iterrows():
            roll_number = str(row['roll_number']).strip()

            # Cast DB column to text so int/varchar mismatch doesn't cause None
            cur.execute("""
                SELECT student_id FROM students WHERE roll_number::text = %s
            """, (roll_number,))
            student = cur.fetchone()

            # Debug: on first row, also print what rolls exist in DB
            if _ == 0:
                cur2 = conn.cursor()
                cur2.execute("SELECT roll_number, pg_typeof(roll_number) FROM students LIMIT 5")
                print("🗄️ DB roll_numbers sample:", cur2.fetchall())
                cur2.close()

            print("Checking roll:", roll_number, "→", student)

            if not student:
                print("Skipping, student not found:", roll_number)
                skipped.append(roll_number)
                continue

            student_id = student[0]

            # FIX 2: Also update payment_date on conflict
            cur.execute("""
                INSERT INTO fees (student_id, month, year, amount_paid, payment_date)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (student_id, month, year)
                DO UPDATE SET
                    amount_paid = EXCLUDED.amount_paid,
                    payment_date = EXCLUDED.payment_date;
            """, (
                student_id,
                int(row['month']),
                int(row['year']),
                float(row['amount_paid']),
                row['payment_date'].date()   # FIX 3: pass plain date, not Timestamp
            ))

            print("Inserted/Updated for roll:", roll_number)
            inserted += 1

        conn.commit()

    except Exception as e:
        # FIX 4: Catch DB errors, rollback, and return a real error response
        conn.rollback()
        print("DB error during upload:", e)
        return {"error": f"Database error: {str(e)}"}, 500

    finally:
        cur.close()
        conn.close()

    return {
        "message": "CSV uploaded successfully",
        "inserted_or_updated": inserted,
        "skipped_roll_numbers": skipped
    }, 200


@fees_bp.route('/export', methods=['GET'])
def export_data():
    month = request.args.get('month')
    year = request.args.get('year')

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT s.name, s.roll_number, s.batch_name,
               CASE 
                   WHEN f.fee_id IS NOT NULL THEN 'Paid'
                   ELSE 'Unpaid'
               END
        FROM students s
        LEFT JOIN fees f
        ON s.student_id = f.student_id 
        AND f.month = %s AND f.year = %s;
    """, (month, year))

    rows = cur.fetchall()

    def generate():
        yield "Name,Roll,Batch,Status\n"
        for row in rows:
            yield f"{row[0]},{row[1]},{row[2]},{row[3]}\n"

    return Response(generate(), mimetype="text/csv",
                    headers={"Content-Disposition": "attachment;filename=fees.csv"})
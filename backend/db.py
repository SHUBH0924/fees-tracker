import psycopg2

def get_connection():
    return psycopg2.connect(
        host="localhost",
        database="db_student",
        user="postgres",
        password="root"  # use your password
    )
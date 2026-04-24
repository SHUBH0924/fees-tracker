let allData = [];
window.onload = fetchData;

// Fetch data from backend based on selected month and year
async function fetchData() {
    const month = document.getElementById("month").value;
    const year = document.getElementById("year").value;

    document.getElementById("tableBody").innerHTML = "<tr><td colspan='4' style='text-align:center;'>Loading...</td></tr>";

    const res = await fetch(`http://127.0.0.1:5000/fees?month=${month}&year=${year}`);
    allData = await res.json();

    populateBatchFilter();
    applyFilters();
}

// Populate batch filter options based on fetched data
function populateBatchFilter() {
    const batchSet = new Set(allData.map(d => d.batch_name));
    const batchFilter = document.getElementById("batchFilter");

    // Remember current selection so it doesn't reset on refresh
    const current = batchFilter.value;
    batchFilter.innerHTML = '<option value="">All</option>';

    batchSet.forEach(batch => {
        const option = document.createElement("option");
        option.value = batch;
        option.textContent = batch;
        batchFilter.appendChild(option);
    });

    // Restore selection if it still exists
    if (current) batchFilter.value = current;
}

// Apply filters to the data and re-render the table
function applyFilters() {
    const batch = document.getElementById("batchFilter").value;
    const status = document.getElementById("statusFilter").value;

    let filtered = allData;

    if (batch) filtered = filtered.filter(d => d.batch_name === batch);
    if (status) filtered = filtered.filter(d => d.fee_status === status);

    renderTable(filtered);
}

// Clear all filters and re-fetch
function clearFilters() {
    const currentMonth = new Date().getMonth() + 1;
    document.getElementById("month").value = currentMonth;
    document.getElementById("year").value = "2026";
    document.getElementById("batchFilter").value = "";
    document.getElementById("statusFilter").value = "";
    fetchData();
}

// Handle CSV upload
async function uploadCSV() {
    const fileInput = document.getElementById("csvFile");
    const file = fileInput.files[0];

    if (!file) {
        alert("Please select a CSV file first.");
        return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
        const res = await fetch("http://127.0.0.1:5000/upload-csv", {
            method: "POST",
            body: formData
        });

        const result = await res.json();

        if (!res.ok) {
            alert("Upload failed: " + (result.error || "Unknown error"));
            return;
        }

        // Clear file input
        fileInput.value = "";

        alert(`Upload successful!\nInserted/Updated: ${result.inserted_or_updated}\nSkipped: ${result.skipped_roll_numbers?.join(", ") || "None"}`);

        // Auto-refresh table with current filters
        fetchData();

    } catch (err) {
        alert("Network error: " + err.message);
    }
}

// Render table rows based on filtered data
function renderTable(data) {
    const tbody = document.getElementById("tableBody");
    tbody.innerHTML = "";

    if (data.length === 0) {
        tbody.innerHTML = "<tr><td colspan='4' style='text-align:center;'>No data found</td></tr>";
        return;
    }

    data.forEach(student => {
        const row = document.createElement("tr");

        if (student.fee_status === "Unpaid") row.classList.add("unpaid");

        row.innerHTML = `
            <td>${student.name}</td>
            <td>${student.roll_number}</td>
            <td>${student.batch_name}</td>
            <td>${student.fee_status}</td>
        `;

        tbody.appendChild(row);
    });
}

// Populate month dropdown with all months
function populateMonths() {
    const months = [
        "January","February","March","April","May","June",
        "July","August","September","October","November","December"
    ];

    const select = document.getElementById("month");
    months.forEach((m, i) => {
        const opt = document.createElement("option");
        opt.value = i + 1;
        opt.textContent = m;
        select.appendChild(opt);
    });

    select.value = new Date().getMonth() + 1;
}

// Trigger CSV download based on selected month and year
function downloadData() {
    const month = document.getElementById("month").value;
    const year = document.getElementById("year").value;
    window.location.href = `http://127.0.0.1:5000/export?month=${month}&year=${year}`;
}

populateMonths();

document.getElementById("batchFilter").addEventListener("change", applyFilters);
document.getElementById("statusFilter").addEventListener("change", applyFilters);
document.getElementById("month").addEventListener("change", fetchData);
document.getElementById("year").addEventListener("change", fetchData);
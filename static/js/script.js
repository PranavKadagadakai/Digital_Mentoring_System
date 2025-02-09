document.addEventListener("DOMContentLoaded", function () {
    const chartElement = document.getElementById("sgpaChart");
    const errorMessage = document.getElementById("error-message");
    const loadingMessage = document.getElementById("loading-message");

    if (!chartElement) {
        console.error("Canvas element with id 'sgpaChart' not found!");
        return;
    }

    let sgpaChart = null; // Store chart instance to update instead of recreating

    function fetchData() {
        loadingMessage.style.display = "block";  // Show loading indicator
        errorMessage.style.display = "none";  // Hide error message

        fetch("/result-analysis")
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! Status: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                loadingMessage.style.display = "none"; // Hide loading message

                console.log("Fetched data:", data); // Debugging
                document.body.insertAdjacentHTML("beforeend", `<pre>${JSON.stringify(data, null, 2)}</pre>`); // Temporary Debugging

                if (data.error) {
                    showError(data.error);
                    return;
                }

                if (!Array.isArray(data.semesters) || !Array.isArray(data.sgpa) || data.semesters.length === 0) {
                    showError("No data available to display.");
                    return;
                }

                updateChart(data.semesters, data.sgpa);
            })
            .catch(error => {
                console.error("Error fetching data:", error);
                showError("Error loading data. Please try again.");
            });
    }

    function showError(message) {
        errorMessage.innerText = message;
        errorMessage.style.display = "block";
    }

    function updateChart(semesters, sgpa) {
        const ctx = chartElement.getContext("2d");

        // If a chart already exists, update it instead of creating a new one
        if (sgpaChart) {
            sgpaChart.data.labels = semesters.map(sem => `Semester ${sem}`);
            sgpaChart.data.datasets[0].data = sgpa;
            sgpaChart.update();
        } else {
            sgpaChart = new Chart(ctx, {
                type: "bar",
                data: {
                    labels: semesters.map(sem => `Semester ${sem}`),
                    datasets: [{
                        label: "SGPA",
                        data: sgpa,
                        backgroundColor: "rgba(54, 162, 235, 0.6)",
                        borderColor: "rgba(54, 162, 235, 1)",
                        borderWidth: 1,
                    }],
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        y: {
                            beginAtZero: true,
                            max: 10,
                        },
                    },
                    plugins: {
                        tooltip: {
                            callbacks: {
                                label: (tooltipItem) => `SGPA: ${tooltipItem.raw.toFixed(2)}`,
                            },
                        },
                    },
                },
            });
        }
    }

    fetchData(); // Fetch data when the page loads
});

document.addEventListener('DOMContentLoaded', () => {
    console.log("SGPA Chart script loaded successfully!");
    const errorMessage = document.getElementById("error-message");
    const loadingMessage = document.getElementById("loading-message");
    const chartElement = document.getElementById("sgpaChart");
    let sgpaChart = null; // Store chart instance to update instead of recreating

    async function fetchData() {
        console.log("Fetching data from /result-analysis/...");
    
        try {
            const response = await fetch('/result-analysis/');
            console.log("Response received:", response);
    
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
    
            const data = await response.json();
            console.log("Parsed data:", data);
    
            if (data.error) {
                showError(data.error);
                return;
            }
    
            if (!Array.isArray(data.semesters) || !Array.isArray(data.sgpa) || data.semesters.length === 0) {
                showError("No data available to display.");
                return;
            }
    
            updateChart(data.semesters, data.sgpa);
        } catch (error) {
            console.error("Error fetching data:", error);
            showError("Error loading data. Please try again.");
        }
    }    

    function showError(message) {
        errorMessage.innerText = message;
        errorMessage.style.display = "block";
        loadingMessage.style.display = "none"; // Hide loading if there's an error
    }

    function updateChart(semesters, sgpa) {
        const ctx = chartElement.getContext("2d");

        if (sgpaChart instanceof Chart) {
            sgpaChart.destroy(); // Destroy only if it's a valid Chart.js object
        }

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
                        title: {
                            display: true,
                            text: 'SGPA'
                        }
                    },
                },
                plugins: {
                    tooltip: {
                        callbacks: {
                            label: (tooltipItem) => `SGPA: ${tooltipItem.raw.toFixed(2)}`,
                        },
                    },
                    title: {
                        display: true,
                        text: 'Semester-wise Performance'
                    }
                },
            },
        });
    }

    fetchData(); // Fetch data when the page loads
});

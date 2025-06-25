// Gofry Dashboard JavaScript

// Global variables
let charts = {};

// Initialize application
document.addEventListener('DOMContentLoaded', function() {
    initializeTooltips();
    initializeCharts();
    setupFormValidation();
    setupTableFilters();
});

// Initialize Bootstrap tooltips
function initializeTooltips() {
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

// Initialize charts
function initializeCharts() {
    // Revenue chart
    const revenueCanvas = document.getElementById('revenueChart');
    if (revenueCanvas) {
        initRevenueChart(revenueCanvas);
    }

    // Products chart
    const productsCanvas = document.getElementById('productsChart');
    if (productsCanvas) {
        initProductsChart(productsCanvas);
    }
}

// Revenue chart initialization
function initRevenueChart(canvas) {
    const ctx = canvas.getContext('2d');
    charts.revenue = new Chart(ctx, {
        type: 'line',
        data: {
            labels: ['Pn', 'Wt', 'Śr', 'Cz', 'Pt', 'Sb', 'Nd'],
            datasets: [{
                label: 'Przychód (zł)',
                data: [320, 450, 380, 520, 680, 850, 720],
                borderColor: '#6f42c1',
                backgroundColor: 'rgba(111, 66, 193, 0.1)',
                borderWidth: 3,
                fill: true,
                tension: 0.4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    grid: {
                        color: 'rgba(0, 0, 0, 0.1)'
                    }
                },
                x: {
                    grid: {
                        display: false
                    }
                }
            }
        }
    });
}

// Products chart initialization
function initProductsChart(canvas) {
    const ctx = canvas.getContext('2d');
    charts.products = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Gofr podstawowy', 'Gofr z Nutellą', 'Gofr owocowy', 'Premium'],
            datasets: [{
                data: [35, 25, 25, 15],
                backgroundColor: [
                    '#6f42c1',
                    '#198754',
                    '#ffc107',
                    '#0dcaf0'
                ],
                borderWidth: 0
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        padding: 20,
                        usePointStyle: true
                    }
                }
            }
        }
    });
}

// Form validation setup
function setupFormValidation() {
    const forms = document.querySelectorAll('.needs-validation');

    Array.prototype.slice.call(forms).forEach(function(form) {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });
}

// Table filters setup
function setupTableFilters() {
    const searchInputs = document.querySelectorAll('.table-search');

    searchInputs.forEach(function(input) {
        input.addEventListener('input', function() {
            const table = this.closest('.card').querySelector('table');
            const rows = table.querySelectorAll('tbody tr');
            const searchTerm = this.value.toLowerCase();

            rows.forEach(function(row) {
                const text = row.textContent.toLowerCase();
                row.style.display = text.includes(searchTerm) ? '' : 'none';
            });
        });
    });
}

// Utility functions
function formatCurrency(amount) {
    return new Intl.NumberFormat('pl-PL', {
        style: 'currency',
        currency: 'PLN'
    }).format(amount);
}

function formatDate(date) {
    return new Intl.DateTimeFormat('pl-PL').format(new Date(date));
}

function showAlert(message, type = 'info') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;

    const container = document.querySelector('.container-fluid');
    container.insertBefore(alertDiv, container.firstChild);

    // Auto dismiss after 5 seconds
    setTimeout(function() {
        if (alertDiv.parentNode) {
            alertDiv.remove();
        }
    }, 5000);
}

// API helpers
async function apiRequest(url, options = {}) {
    try {
        const response = await fetch(url, {
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            },
            ...options
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        return await response.json();
    } catch (error) {
        console.error('API request failed:', error);
        showAlert('Wystąpił błąd podczas komunikacji z serwerem', 'danger');
        throw error;
    }
}

// Dashboard specific functions
function loadDashboardStats() {
    apiRequest('/api/dashboard_stats')
        .then(data => {
            updateStatsCards(data);
        })
        .catch(error => {
            console.error('Failed to load dashboard stats:', error);
        });
}

function updateStatsCards(data) {
    const statsContainer = document.getElementById('stats-cards');
    if (!statsContainer) return;

    statsContainer.innerHTML = `
        <div class="col-md-3 mb-3">
            <div class="card bg-primary text-white stats-card">
                <div class="card-body dashboard-metric">
                    <div class="d-flex justify-content-between align-items-center">
                        <div>
                            <h3>${data.total_products || 0}</h3>
                            <small>Produktów</small>
                        </div>
                        <i class="bi bi-box-seam fs-1"></i>
                    </div>
                </div>
            </div>
        </div>
        <div class="col-md-3 mb-3">
            <div class="card bg-success text-white stats-card">
                <div class="card-body dashboard-metric">
                    <div class="d-flex justify-content-between align-items-center">
                        <div>
                            <h3>${data.total_compositions || 0}</h3>
                            <small>Kompozycji</small>
                        </div>
                        <i class="bi bi-collection fs-1"></i>
                    </div>
                </div>
            </div>
        </div>
        <div class="col-md-3 mb-3">
            <div class="card bg-warning text-white stats-card">
                <div class="card-body dashboard-metric">
                    <div class="d-flex justify-content-between align-items-center">
                        <div>
                            <h3>${data.low_stock_products || 0}</h3>
                            <small>Niski stan</small>
                        </div>
                        <i class="bi bi-exclamation-triangle fs-1"></i>
                    </div>
                </div>
            </div>
        </div>
        <div class="col-md-3 mb-3">
            <div class="card bg-info text-white stats-card">
                <div class="card-body dashboard-metric">
                    <div class="d-flex justify-content-between align-items-center">
                        <div>
                            <h3>${formatCurrency(data.monthly_revenue || 0)}</h3>
                            <small>Przychód m-c</small>
                        </div>
                        <i class="bi bi-currency-exchange fs-1"></i>
                    </div>
                </div>
            </div>
        </div>
    `;

    // Add fade-in animation
    statsContainer.classList.add('fade-in');
}

// Export functions for global use
window.GofryDashboard = {
    loadDashboardStats,
    showAlert,
    formatCurrency,
    formatDate,
    apiRequest
};
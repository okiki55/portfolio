/**
 * ML/AI Portfolio - Main JavaScript
 * Handles animations, form submissions, and UI interactions
 */

document.addEventListener('DOMContentLoaded', function() {
    // Initialize all modules
    initNavbar();
    initScrollAnimations();
    initPredictionForm();
    initImageUpload();
    initRangeInputs();
});

/**
 * Navbar scroll effect
 */
function initNavbar() {
    const navbar = document.querySelector('.navbar');
    
    if (!navbar) return;
    
    window.addEventListener('scroll', function() {
        if (window.scrollY > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    });
}

/**
 * Scroll animations using Intersection Observer
 */
function initScrollAnimations() {
    const animatedElements = document.querySelectorAll('.fade-in, .slide-in-left, .slide-in-right');
    
    if (animatedElements.length === 0) return;
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
                observer.unobserve(entry.target);
            }
        });
    }, {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    });
    
    animatedElements.forEach(el => observer.observe(el));
}

/**
 * Prediction form handling
 */
function initPredictionForm() {
    const form = document.getElementById('prediction-form');
    
    if (!form) return;
    
    form.addEventListener('submit', handlePredictionSubmit);
}

async function handlePredictionSubmit(e) {
    e.preventDefault();
    
    const form = e.target;
    const submitBtn = form.querySelector('.predict-btn');
    const resultsSection = document.getElementById('results-section');
    const resultContent = document.getElementById('result-content');
    const chartContainer = document.getElementById('chart-container');
    const errorDisplay = document.getElementById('error-display');
    
    // Get project ID from form data attribute
    const projectId = form.dataset.projectId;
    
    if (!projectId) {
        showError('Project ID not found');
        return;
    }
    
    // Show loading state
    submitBtn.classList.add('loading');
    submitBtn.disabled = true;
    
    // Hide previous results
    if (resultsSection) resultsSection.classList.remove('show');
    if (errorDisplay) errorDisplay.style.display = 'none';
    
    try {
        // Collect form data
        const formData = new FormData(form);
        
        // Send prediction request
        const response = await fetch(`/api/predict/${projectId}`, {
            method: 'POST',
            body: formData
        });
        
        const result = await response.json();
        
        if (result.error) {
            showError(result.error);
        } else {
            displayResults(result);
        }
    } catch (error) {
        console.error('Prediction error:', error);
        showError('An error occurred while making the prediction. Please try again.');
    } finally {
        // Reset button state
        submitBtn.classList.remove('loading');
        submitBtn.disabled = false;
    }
}

/**
 * Display prediction results
 */
function displayResults(result) {
    const resultsSection = document.getElementById('results-section');
    const resultValue = document.getElementById('result-value');
    const resultDetails = document.getElementById('result-details');
    const chartContainer = document.getElementById('chart-container');
    
    if (!resultsSection) return;
    
    // Display main result
    if (resultValue) {
        let displayValue = result.result;
        
        // Format the result based on type
        if (typeof displayValue === 'number') {
            // Check if it's a large number (likely price or similar)
            if (Math.abs(displayValue) >= 1000) {
                displayValue = displayValue.toLocaleString('en-US', {
                    maximumFractionDigits: 2
                });
            } else {
                displayValue = displayValue.toFixed(4);
            }
        } else if (typeof displayValue === 'object') {
            // Handle classification results
            if (displayValue.class) {
                displayValue = displayValue.class;
            } else {
                displayValue = JSON.stringify(displayValue);
            }
        }
        
        // Add unit if provided
        const unit = result.unit || '';
        const prefix = result.prefix || '';
        
        resultValue.textContent = `${prefix}${displayValue}${unit}`;
    }
    
    // Display additional details
    if (resultDetails && result.details) {
        resultDetails.innerHTML = '';
        
        for (const [key, value] of Object.entries(result.details)) {
            const item = document.createElement('div');
            item.className = 'result-detail-item';
            item.innerHTML = `
                <div class="result-detail-label">${formatLabel(key)}</div>
                <div class="result-detail-value">${formatValue(value)}</div>
            `;
            resultDetails.appendChild(item);
        }
    }
    
    // Display confidence if available
    if (result.confidence !== undefined) {
        const confidenceDisplay = document.getElementById('confidence-display');
        if (confidenceDisplay) {
            const confidencePercent = (result.confidence * 100).toFixed(1);
            confidenceDisplay.innerHTML = `
                <div class="result-detail-label">Confidence</div>
                <div class="result-detail-value">${confidencePercent}%</div>
            `;
            confidenceDisplay.style.display = 'block';
        }
    }
    
    // Display chart if data provided
    if (chartContainer && result.chart_data) {
        chartContainer.style.display = 'block';
        renderChart(result.chart_data);
    } else if (chartContainer) {
        chartContainer.style.display = 'none';
    }
    
    // Show results section with animation
    resultsSection.classList.add('show');
    
    // Scroll to results
    resultsSection.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

/**
 * Render chart using Chart.js
 */
let chartInstance = null;

function renderChart(chartData) {
    const ctx = document.getElementById('result-chart');
    
    if (!ctx) return;
    
    // Destroy existing chart
    if (chartInstance) {
        chartInstance.destroy();
    }
    
    // Chart configuration
    const config = {
        type: chartData.type || 'bar',
        data: {
            labels: chartData.labels || [],
            datasets: [{
                label: chartData.label || 'Prediction',
                data: chartData.values || chartData.data || [],
                backgroundColor: chartData.type === 'pie' || chartData.type === 'doughnut' 
                    ? generateGradientColors(chartData.labels?.length || 5)
                    : 'rgba(0, 212, 255, 0.6)',
                borderColor: chartData.type === 'pie' || chartData.type === 'doughnut'
                    ? 'rgba(10, 10, 15, 1)'
                    : 'rgba(0, 212, 255, 1)',
                borderWidth: chartData.type === 'pie' || chartData.type === 'doughnut' ? 2 : 1,
                tension: 0.4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: chartData.type === 'pie' || chartData.type === 'doughnut',
                    position: 'bottom',
                    labels: {
                        color: '#a1a1aa',
                        padding: 20
                    }
                }
            },
            scales: chartData.type !== 'pie' && chartData.type !== 'doughnut' ? {
                y: {
                    beginAtZero: true,
                    grid: {
                        color: 'rgba(39, 39, 42, 0.5)'
                    },
                    ticks: {
                        color: '#a1a1aa'
                    }
                },
                x: {
                    grid: {
                        display: false
                    },
                    ticks: {
                        color: '#a1a1aa'
                    }
                }
            } : {}
        }
    };
    
    chartInstance = new Chart(ctx, config);
}

/**
 * Generate gradient colors for pie/doughnut charts
 */
function generateGradientColors(count) {
    const colors = [
        'rgba(0, 212, 255, 0.8)',    // Cyan
        'rgba(124, 58, 237, 0.8)',   // Purple
        'rgba(34, 211, 238, 0.8)',   // Light cyan
        'rgba(168, 85, 247, 0.8)',   // Light purple
        'rgba(6, 182, 212, 0.8)',    // Teal
        'rgba(139, 92, 246, 0.8)',   // Violet
        'rgba(14, 165, 233, 0.8)',   // Sky
        'rgba(192, 132, 252, 0.8)'   // Lavender
    ];
    
    return colors.slice(0, count);
}

/**
 * Show error message
 */
function showError(message) {
    const errorDisplay = document.getElementById('error-display');
    const resultsSection = document.getElementById('results-section');
    
    if (errorDisplay) {
        errorDisplay.textContent = message;
        errorDisplay.style.display = 'block';
    }
    
    if (resultsSection) {
        resultsSection.classList.remove('show');
    }
}

/**
 * Image upload handling
 */
function initImageUpload() {
    const uploadAreas = document.querySelectorAll('.image-upload-area');
    
    uploadAreas.forEach(area => {
        const input = area.querySelector('input[type="file"]');
        const preview = area.querySelector('.image-preview');
        
        if (!input) return;
        
        // Click to upload
        area.addEventListener('click', () => input.click());
        
        // Drag and drop
        area.addEventListener('dragover', (e) => {
            e.preventDefault();
            area.classList.add('dragover');
        });
        
        area.addEventListener('dragleave', () => {
            area.classList.remove('dragover');
        });
        
        area.addEventListener('drop', (e) => {
            e.preventDefault();
            area.classList.remove('dragover');
            
            const files = e.dataTransfer.files;
            if (files.length > 0) {
                input.files = files;
                handleImagePreview(files[0], preview, area);
            }
        });
        
        // File input change
        input.addEventListener('change', (e) => {
            if (e.target.files.length > 0) {
                handleImagePreview(e.target.files[0], preview, area);
            }
        });
    });
}

function handleImagePreview(file, preview, area) {
    if (!file.type.startsWith('image/')) {
        showError('Please upload an image file');
        return;
    }
    
    const reader = new FileReader();
    
    reader.onload = (e) => {
        if (preview) {
            preview.src = e.target.result;
            preview.style.display = 'block';
        }
        
        // Update upload area text
        const uploadText = area.querySelector('p');
        if (uploadText) {
            uploadText.textContent = file.name;
        }
        
        // Add visual feedback
        area.style.borderColor = 'var(--accent-primary)';
    };
    
    reader.readAsDataURL(file);
}

/**
 * Range input handling
 */
function initRangeInputs() {
    const rangeInputs = document.querySelectorAll('input[type="range"]');
    
    rangeInputs.forEach(input => {
        const valueDisplay = document.getElementById(`${input.name}-value`);
        
        if (valueDisplay) {
            // Set initial value
            valueDisplay.textContent = input.value;
            
            // Update on change
            input.addEventListener('input', () => {
                valueDisplay.textContent = input.value;
            });
        }
    });
}

/**
 * Utility functions
 */
function formatLabel(key) {
    return key
        .replace(/_/g, ' ')
        .replace(/([A-Z])/g, ' $1')
        .replace(/^./, str => str.toUpperCase())
        .trim();
}

function formatValue(value) {
    if (typeof value === 'number') {
        return value.toFixed(4);
    }
    if (typeof value === 'boolean') {
        return value ? 'Yes' : 'No';
    }
    return value;
}

/**
 * Smooth scroll for anchor links
 */
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
        const targetId = this.getAttribute('href');
        
        if (targetId === '#') return;
        
        const target = document.querySelector(targetId);
        
        if (target) {
            e.preventDefault();
            target.scrollIntoView({ behavior: 'smooth' });
        }
    });
});

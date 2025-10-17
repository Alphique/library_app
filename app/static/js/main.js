// app/static/js/main.js

// Global JavaScript functions
document.addEventListener('DOMContentLoaded', function() {
    initializeApplication();
});

function initializeApplication() {
    // Auto-dismiss alerts after 5 seconds
    autoDismissAlerts();
    
    // Initialize tooltips
    initializeTooltips();
    
    // Initialize file upload enhancements
    initializeFileUploads();
    
    // Initialize form validation enhancements
    initializeFormValidation();
    
    // Initialize cart functionality
    initializeCart();
    
    // Initialize admin features
    initializeAdminFeatures();
}

// Auto-dismiss alerts
function autoDismissAlerts() {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        if (!alert.classList.contains('alert-permanent')) {
            setTimeout(() => {
                const bsAlert = new bootstrap.Alert(alert);
                bsAlert.close();
            }, 5000);
        }
    });
}

// Initialize Bootstrap tooltips
function initializeTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    const tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

// File upload enhancements
function initializeFileUploads() {
    const fileInputs = document.querySelectorAll('input[type="file"]');
    
    fileInputs.forEach(input => {
        // Create custom file upload area if it doesn't exist
        if (!input.closest('.file-upload-area')) {
            const parent = input.parentElement;
            parent.classList.add('file-upload-area');
            
            // Add drag and drop functionality
            parent.addEventListener('dragover', function(e) {
                e.preventDefault();
                this.classList.add('dragover');
            });
            
            parent.addEventListener('dragleave', function(e) {
                e.preventDefault();
                this.classList.remove('dragover');
            });
            
            parent.addEventListener('drop', function(e) {
                e.preventDefault();
                this.classList.remove('dragover');
                input.files = e.dataTransfer.files;
                updateFileInputDisplay(input);
            });
            
            input.addEventListener('change', function() {
                updateFileInputDisplay(this);
            });
        }
    });
}

// Update file input display with selected file names
function updateFileInputDisplay(input) {
    const parent = input.parentElement;
    const fileList = parent.querySelector('.file-list') || createFileListElement(parent);
    
    if (input.files.length > 0) {
        fileList.innerHTML = '';
        Array.from(input.files).forEach(file => {
            const fileItem = document.createElement('div');
            fileItem.className = 'file-item small text-muted';
            fileItem.innerHTML = `
                <i class="fas fa-file me-1"></i>
                ${file.name} (${formatFileSize(file.size)})
            `;
            fileList.appendChild(fileItem);
        });
    } else {
        fileList.innerHTML = '<div class="text-muted">No files selected</div>';
    }
}

// Create file list element
function createFileListElement(parent) {
    const fileList = document.createElement('div');
    fileList.className = 'file-list mt-2';
    parent.appendChild(fileList);
    return fileList;
}

// Format file size
function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

// Form validation enhancements
function initializeFormValidation() {
    const forms = document.querySelectorAll('form');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const submitBtn = this.querySelector('button[type="submit"], input[type="submit"]');
            if (submitBtn) {
                submitBtn.disabled = true;
                submitBtn.innerHTML = '<span class="loading-spinner me-2"></span>Processing...';
            }
        });
    });
}

// Cart functionality
function initializeCart() {
    // Update cart item count in navbar
    updateCartCount();
    
    // Cart quantity controls
    const quantityInputs = document.querySelectorAll('.cart-quantity');
    quantityInputs.forEach(input => {
        input.addEventListener('change', function() {
            updateCartItem(this);
        });
    });
}

// Update cart count in navbar
function updateCartCount() {
    const cartCount = document.querySelector('.cart-count');
    if (cartCount) {
        // This would typically make an API call to get actual cart count
        // For now, we'll use a placeholder
        const count = getCartItemCount();
        cartCount.textContent = count;
        cartCount.style.display = count > 0 ? 'inline' : 'none';
    }
}

// Get cart item count (placeholder function)
function getCartItemCount() {
    // This would typically get the count from your backend or localStorage
    // For now, return 0 as we're using session-based cart
    return 0;
}

// Update cart item (placeholder function)
function updateCartItem(input) {
    const itemId = input.dataset.itemId;
    const quantity = input.value;
    
    // This would typically make an API call to update the cart
    console.log(`Updating item ${itemId} to quantity ${quantity}`);
}

// Admin features
function initializeAdminFeatures() {
    // Initialize data tables if they exist
    initializeDataTables();
    
    // Initialize chart functionality
    initializeCharts();
    
    // Initialize bulk actions
    initializeBulkActions();
}

// Initialize data tables (placeholder)
function initializeDataTables() {
    // This would initialize DataTables if the library is included
    const tables = document.querySelectorAll('.data-table');
    if (tables.length > 0 && typeof $.fn.DataTable !== 'undefined') {
        tables.forEach(table => {
            $(table).DataTable({
                responsive: true,
                pageLength: 25
            });
        });
    }
}

// Initialize charts (placeholder)
function initializeCharts() {
    // This would initialize charts if Chart.js is included
    const chartCanvases = document.querySelectorAll('.chart-canvas');
    if (chartCanvases.length > 0 && typeof Chart !== 'undefined') {
        chartCanvases.forEach(canvas => {
            // Initialize charts here
        });
    }
}

// Initialize bulk actions
function initializeBulkActions() {
    const bulkCheckboxes = document.querySelectorAll('.bulk-checkbox');
    const bulkActionBtn = document.querySelector('.bulk-action-btn');
    
    if (bulkCheckboxes.length > 0 && bulkActionBtn) {
        const selectAllCheckbox = document.querySelector('.select-all-checkbox');
        
        if (selectAllCheckbox) {
            selectAllCheckbox.addEventListener('change', function() {
                const isChecked = this.checked;
                bulkCheckboxes.forEach(checkbox => {
                    checkbox.checked = isChecked;
                });
                updateBulkActionButton();
            });
        }
        
        bulkCheckboxes.forEach(checkbox => {
            checkbox.addEventListener('change', updateBulkActionButton);
        });
    }
}

// Update bulk action button state
function updateBulkActionButton() {
    const bulkCheckboxes = document.querySelectorAll('.bulk-checkbox:checked');
    const bulkActionBtn = document.querySelector('.bulk-action-btn');
    
    if (bulkActionBtn) {
        if (bulkCheckboxes.length > 0) {
            bulkActionBtn.disabled = false;
            bulkActionBtn.textContent = `Apply to ${bulkCheckboxes.length} items`;
        } else {
            bulkActionBtn.disabled = true;
            bulkActionBtn.textContent = 'Bulk Actions';
        }
    }
}

// Utility function to show loading state
function showLoading(element) {
    element.disabled = true;
    const originalText = element.innerHTML;
    element.innerHTML = '<span class="loading-spinner me-2"></span>Loading...';
    return originalText;
}

// Utility function to hide loading state
function hideLoading(element, originalText) {
    element.disabled = false;
    element.innerHTML = originalText;
}

// AJAX helper function
function makeRequest(url, method = 'GET', data = null) {
    return fetch(url, {
        method: method,
        headers: {
            'Content-Type': 'application/json',
            'X-Requested-With': 'XMLHttpRequest'
        },
        body: data ? JSON.stringify(data) : null
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    });
}

// Toast notification system
function showToast(message, type = 'info') {
    const toastContainer = document.getElementById('toast-container') || createToastContainer();
    
    const toast = document.createElement('div');
    toast.className = `toast align-items-center text-bg-${type} border-0`;
    toast.setAttribute('role', 'alert');
    toast.innerHTML = `
        <div class="d-flex">
            <div class="toast-body">${message}</div>
            <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
        </div>
    `;
    
    toastContainer.appendChild(toast);
    const bsToast = new bootstrap.Toast(toast);
    bsToast.show();
    
    toast.addEventListener('hidden.bs.toast', function() {
        toast.remove();
    });
}

// Create toast container if it doesn't exist
function createToastContainer() {
    const container = document.createElement('div');
    container.id = 'toast-container';
    container.className = 'toast-container position-fixed top-0 end-0 p-3';
    container.style.zIndex = '9999';
    document.body.appendChild(container);
    return container;
}

// Price formatting utility
function formatPrice(amount) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
    }).format(amount);
}

// Date formatting utility
function formatDate(dateString) {
    return new Date(dateString).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    });
}

// Debounce function for search inputs
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Export functions for global use
window.LibraryApp = {
    showToast,
    formatPrice,
    formatDate,
    debounce,
    makeRequest,
    showLoading,
    hideLoading
};
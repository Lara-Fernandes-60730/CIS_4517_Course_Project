document.addEventListener('DOMContentLoaded', function() {
    // Show loading state during form submission
    const form = document.querySelector('.upload-form');
    if (form) {
        form.addEventListener('submit', function() {
            const submitBtn = this.querySelector('button[type="submit"]');
            submitBtn.disabled = true;
            submitBtn.textContent = 'Processing...';
        });
    }

    // Preview selected image before upload
    const fileInput = document.querySelector('.file-input');
    if (fileInput) {
        fileInput.addEventListener('change', function(e) {
            if (this.files && this.files[0]) {
                // You could add image preview logic here
                console.log('Selected file:', this.files[0].name);
            }
        });
    }
});
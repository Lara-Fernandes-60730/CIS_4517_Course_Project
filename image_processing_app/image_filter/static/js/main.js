document.addEventListener('DOMContentLoaded', function() {
    const uploadArea = document.getElementById('upload-area');
    const fileInput = document.querySelector('input[type="file"]');

    if(uploadArea && fileInput) {
        // Prevent default drag behaviors
        ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
            uploadArea.addEventListener(eventName, preventDefaults, false);
            document.body.addEventListener(eventName, preventDefaults, false);
        });

        // Highlight drop area when item is dragged over it
        ['dragenter', 'dragover'].forEach(eventName => {
            uploadArea.addEventListener(eventName, highlight, false);
        });

        ['dragleave', 'drop'].forEach(eventName => {
            uploadArea.addEventListener(eventName, unhighlight, false);
        });

        // Handle dropped files
        uploadArea.addEventListener('drop', handleDrop, false);

        // Handle file selection via input
        fileInput.addEventListener('change', handleFiles, false);
    }

    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }

    function highlight() {
        uploadArea.classList.add('highlight');
    }

    function unhighlight() {
        uploadArea.classList.remove('highlight');
    }

    function handleDrop(e) {
        const dt = e.dataTransfer;
        const files = dt.files;
        fileInput.files = files;
        handleFiles();
    }

    function handleFiles() {
        if(fileInput.files.length) {
            updateFileInfo(fileInput.files[0]);
            displayImagePreview(fileInput.files[0]);
        }
    }

    function displayImagePreview(file) {
        if (file.type.match('image.*')) {
            const reader = new FileReader();

            reader.onload = function(e) {
                // Remove any existing preview
                const existingPreview = document.querySelector('.image-preview');
                if (existingPreview) {
                    existingPreview.remove();
                }

                // Create new preview
                const preview = document.createElement('img');
                preview.src = e.target.result;
                preview.classList.add('image-preview');
                preview.style.maxWidth = '100%';
                preview.style.maxHeight = '200px';
                preview.style.marginTop = '15px';
                preview.style.borderRadius = '10px';

                // Add to upload area
                uploadArea.appendChild(preview);
            }

            reader.readAsDataURL(file);
        }
    }

    function updateFileInfo(file) {
        const uploadText = document.querySelector('.upload-text');
        if(uploadText) {
            uploadText.textContent = 'Selected: ' + file.name;
        }
    }
});

// Add active state to filter options for better UX
document.addEventListener('DOMContentLoaded', function() {
    const filterOptions = document.querySelectorAll('.filter-option');

    filterOptions.forEach(option => {
        const checkbox = option.querySelector('input[type="checkbox"]');
        const label = option.querySelector('label');

        if (checkbox && label) {
            // Initialize active state
            if(checkbox.checked) {
                label.classList.add('active');
            }

            // Update on change
            checkbox.addEventListener('change', function() {
                if(this.checked) {
                    label.classList.add('active');
                } else {
                    label.classList.remove('active');
                }
            });

            // Also make the label clickable
            label.addEventListener('click', function(e) {
                // Prevent double triggering
                e.stopPropagation();
            });
        }
    });
});
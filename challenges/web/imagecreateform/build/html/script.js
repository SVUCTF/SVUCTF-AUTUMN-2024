document.addEventListener('DOMContentLoaded', () => {
    const dropArea = document.getElementById('drop-area');
    const fileInput = document.getElementById('file-input');
    const preview = document.getElementById('preview');
    const uploadBtn = document.getElementById('upload-btn');
    const message = document.getElementById('message');
    const form = document.getElementById('upload-form');

    let selectedFile = null;

    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        dropArea.addEventListener(eventName, preventDefaults, false);
    });

    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }

    ['dragenter', 'dragover'].forEach(eventName => {
        dropArea.addEventListener(eventName, highlight, false);
    });

    ['dragleave', 'drop'].forEach(eventName => {
        dropArea.addEventListener(eventName, unhighlight, false);
    });

    function highlight() {
        dropArea.classList.add('highlight');
    }

    function unhighlight() {
        dropArea.classList.remove('highlight');
    }

    dropArea.addEventListener('drop', handleDrop, false);
    dropArea.addEventListener('click', () => fileInput.click());
    fileInput.addEventListener('change', () => handleFiles(fileInput.files));

    function handleDrop(e) {
        const dt = e.dataTransfer;
        const files = dt.files;
        handleFiles(files);
    }

    function handleFiles(files) {
        selectedFile = files[0];
        if (selectedFile && selectedFile.type === 'image/png') {
            const reader = new FileReader();
            reader.onload = function(e) {
                preview.src = e.target.result;
                preview.style.display = 'block';
                uploadBtn.style.display = 'inline-block';
            };
            reader.readAsDataURL(selectedFile);
        } else {
            preview.style.display = 'none';
            uploadBtn.style.display = 'none';
            message.textContent = 'Please upload a PNG image.';
        }
    }

    form.addEventListener('submit', function(e) {
        e.preventDefault();
        if (!selectedFile) {
            message.textContent = 'Please select an image before uploading.';
            return;
        }
        uploadFile(selectedFile);
    });

    function uploadFile(file) {
        const formData = new FormData();
        formData.append('image', file);

        fetch('index.php', {
            method: 'POST',
            body: formData
        })
            .then(response => response.json())
            .then(data => {
                const message = document.getElementById('message');
                message.style.display = 'block';
                message.textContent = data.message;

                if (data.filePath) {
                    message.textContent += ` File saved as: ${data.filePath}`;
                    message.classList.add('success');
                    message.classList.remove('error');
                } else {
                    message.classList.add('error');
                    message.classList.remove('success');
                }
            })
            .catch(error => {
                const message = document.getElementById('message');
                message.style.display = 'block';
                message.textContent = 'An error occurred during upload.';
                message.classList.add('error');
                message.classList.remove('success');
                console.error('Error:', error);
            });
    }
});

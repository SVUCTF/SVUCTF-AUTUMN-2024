<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Secure Image Upload</title>
    <style>
        :root {
            --primary-color: #8A2BE2;
            --secondary-color: #00FFFF;
            --accent-color: #FF1493;
            --bg-dark: #120458;
            --bg-light: #3F0071;
            --text-color: #E0E0E0;
        }

        body {
            font-family: 'Courier New', monospace;
            background: linear-gradient(135deg, var(--bg-dark), var(--bg-light));
            color: var(--text-color);
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            margin: 0;
            overflow: hidden;
        }

        .neon-sign {
            font-size: 2.5rem;
            font-weight: bold;
            text-transform: uppercase;
            margin-bottom: 2rem;
            position: relative;
            overflow: hidden;
        }

        .neon-sign span {
            position: relative;
            display: inline-block;
            padding: 0 10px;
        }

        .neon-sign span::before {
            content: attr(data-text);
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            color: var(--accent-color);
            filter: blur(15px);
            z-index: -1;
        }

        .neon-sign span:nth-child(1) {
            color: var(--secondary-color);
            animation: flicker 2s linear infinite;
        }

        .neon-sign span:nth-child(2) {
            color: var(--accent-color);
            animation: flicker 1.4s linear infinite;
        }

        .left-corner-text {
            position: absolute;
            top: 10px;
            left: 10px;
            font-size: 24px;
            color: white;
            font-family: 'Arial', sans-serif;
            font-weight: bold;
            writing-mode: vertical-rl;
            /* 竖排文字 */
            text-orientation: mixed;
            /* 确保字符正确显示 */
        }

        @keyframes flicker {

            0%,
            19.999%,
            22%,
            62.999%,
            64%,
            64.999%,
            70%,
            100% {
                opacity: 1;
            }

            20%,
            21.999%,
            63%,
            63.999%,
            65%,
            69.999% {
                opacity: 0.33;
            }
        }

        .container {
            background-color: rgba(18, 4, 88, 0.8);
            padding: 2rem;
            border-radius: 10px;
            box-shadow: 0 0 20px var(--primary-color), 0 0 40px var(--secondary-color);
            text-align: center;
            max-width: 400px;
            width: 100%;
        }

        h1 {
            color: var(--secondary-color);
            margin-bottom: 1rem;
            text-transform: uppercase;
            letter-spacing: 2px;
            text-shadow: 2px 2px var(--primary-color);
        }

        #drop-area {
            border: 2px dashed var(--secondary-color);
            border-radius: 10px;
            padding: 2rem;
            cursor: pointer;
            transition: all 0.3s ease;
            background-color: rgba(0, 255, 255, 0.1);
        }

        #drop-area:hover,
        #drop-area.highlight {
            background-color: rgba(0, 255, 255, 0.2);
            border-color: var(--accent-color);
            box-shadow: 0 0 10px var(--accent-color);
        }

        #file-input {
            display: none;
        }

        #preview-container {
            width: 100%;
            display: flex;
            justify-content: center;
            align-items: center;
            margin-top: 1rem;
            min-height: 200px;
        }

        #preview {
            max-width: 100%;
            max-height: 200px;
            display: none;
            border-radius: 5px;
            box-shadow: 0 0 10px var(--primary-color);
            object-fit: contain;
        }

        #upload-btn {
            background-color: var(--primary-color);
            color: var(--text-color);
            border: none;
            padding: 10px 20px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 16px;
            margin-top: 1rem;
            cursor: pointer;
            border-radius: 5px;
            transition: all 0.3s ease;
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        #upload-btn:hover {
            background-color: var(--accent-color);
            box-shadow: 0 0 15px var(--accent-color);
        }

        #message {
            margin-top: 1rem;
            font-weight: bold;
            color: var(--secondary-color);
            text-shadow: 1px 1px var(--primary-color);
        }

        @keyframes neon-glow {
            0% {
                text-shadow: 0 0 5px var(--secondary-color), 0 0 10px var(--secondary-color);
            }

            50% {
                text-shadow: 0 0 20px var(--secondary-color), 0 0 35px var(--secondary-color);
            }

            100% {
                text-shadow: 0 0 5px var(--secondary-color), 0 0 10px var(--secondary-color);
            }
        }

        h1,
        #upload-btn {
            animation: neon-glow 1.5s ease-in-out infinite alternate;
        }
    </style>
</head>

<body>
    <div class="neon-sign">
        <span data-text="Cyber">Cyber</span>
        <span data-text="Upload">Upload</span>
    </div>

    <div class="left-corner-text">
        那美好的仗，我已經打過了；
        該跑的路程，我已經跑盡了；
        當守的信仰，我已經持守了。
        此後，有那公義的冠冕為我存留，
        就是主——公義的審判者要在那一天回報給我的；
        也要給所有愛慕他顯現的人。
    </div>

    <div class="container">
        <h1>Secure Transfer</h1>
        <form id="upload-form" action="upload.php" method="post" enctype="multipart/form-data">
            <div id="drop-area">
                <p>请开始上传吧 嘿嘿</p>
                <input type="file" id="file-input" name="image" accept="image/jpeg">
            </div>
            <div id="preview-container">
                <img id="preview" src="#" alt="Image preview">
            </div>
            <button id="upload-btn" type="submit" style="display: none;">Upload Image</button>
        </form>
        <div id="message"></div>
    </div>

    <script>
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

        function handleDrop(e) {
            const dt = e.dataTransfer;
            const files = dt.files;
            handleFiles(files);
        }

        dropArea.addEventListener('click', () => fileInput.click());

        fileInput.addEventListener('change', function() {
            handleFiles(this.files);
        });

        function handleFiles(files) {
            selectedFile = files[0];
            if (selectedFile && selectedFile.type === 'image/jpeg') {
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
                message.textContent = 'Please upload a JPEG image.';
            }
        }

        form.addEventListener('submit', function(e) {
            if (!selectedFile) {
                e.preventDefault();
                message.textContent = 'Please select an image before uploading.';
            }
        });
    </script>
</body>

</html>

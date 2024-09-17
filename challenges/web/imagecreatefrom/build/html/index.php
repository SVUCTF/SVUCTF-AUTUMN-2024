<?php
$message = '';
$filePath = '';

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $target_dir = "images/";
    $filename = basename($_FILES["image"]["name"]);
    $target_file = $target_dir . $filename;

    $image = @imagecreatefrompng($_FILES["image"]["tmp_name"]);
    if (!$image) {
        $message = "File is not a valid PNG image.";
    } else {
        if (imagepng($image, $target_file)) {
            $message = "The file has been uploaded.";
            $filePath = $target_file;
        } else {
            $message = "Sorry, there was an error saving the image.";
        }
        imagedestroy($image);
    }

    if ($_FILES["image"]["size"] > 5000000) {
        $message = "Sorry, your file is too large.";
    }

    $response = [
        'message' => $message,
        'filePath' => $filePath
    ];

    header('Content-Type: application/json');
    echo json_encode($response);
    exit;
}
?>

<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Image Upload</title>
    <link rel="stylesheet" href="styles.css">
</head>

<body>
    <div class="left-corner-text">
        那美好的仗、
        我已經打過了。
        該跑的路程、
        我已經跑盡了。
        當守的信仰、
        我已經持守了。
        此後、
        有那公義的冠冕為我存留、
        就是主——
        公義的審判者要在那日賜給我的。
        不但賜給我、
        也賜給凡愛慕他顯現的人。
    </div>

    <div class="container">
        <h1>Image Upload</h1>
        <form id="upload-form" enctype="multipart/form-data">
            <div id="drop-area">
                <p>请开始上传吧 嘿嘿</p>
                <input type="file" id="file-input" name="image" accept="image/png">
            </div>
            <div id="preview-container">
                <img id="preview" src="#" alt="Image preview">
            </div>
            <button id="upload-btn" type="submit">Upload Image</button>
        </form>
        <div id="message"></div>
    </div>

    <script src="script.js"></script>
</body>

</html>

<?php
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $target_dir = "images/";
    $target_file = $target_dir . basename($_FILES["image"]["name"]);
    $imageFileType = strtolower(pathinfo($target_file, PATHINFO_EXTENSION));

    $blacklist = ['.user.ini', 'php1', 'php2', 'php3', 'php4', 'php5', 'html', 'asp', 'aspx', 'sh', 'py'];

    if (in_array($imageFileType, $blacklist)) {
        die("File type is not allowed !  ");
    }

    // Check if image file is a actual image or fake image
    if (isset($_POST["submit"])) {
        $check = getimagesize($_FILES["image"]["tmp_name"]);
        if ($check === false) {
            die("File is not an image.");
        }
    }

    // Try to create image from uploaded file
    $image = @imagecreatefromjpeg($_FILES["image"]["tmp_name"]);
    if (!$image) {
        die("Failed to create image.");
    }

    // If we've made it this far, try to move the uploaded file
    if (move_uploaded_file($_FILES["image"]["tmp_name"], $target_file)) {
        echo "The file " . basename($_FILES["image"]["name"]) . " has been uploaded.";
    } else {
        echo "Sorry, there was an error uploading your file.";
    }

    imagedestroy($image);
}

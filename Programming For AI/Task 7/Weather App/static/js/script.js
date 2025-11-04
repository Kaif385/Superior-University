document.addEventListener("DOMContentLoaded", () => {
    const img = document.querySelector(".apod-image");

    if (img) {
        img.addEventListener("click", () => {
            window.open(img.src, "_blank"); // Open HD image in new tab
        });
    }

    console.log("NASA APOD Page Loaded 🚀");
});

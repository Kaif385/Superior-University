
document.addEventListener("DOMContentLoaded", function() {
    const form = document.querySelector('form');
    const button = document.querySelector('button');
    const loadingDiv = document.getElementById('loading');

    if (form) {
        form.addEventListener('submit', function() {
            loadingDiv.style.display = 'block';
            
            button.innerText = 'Searching...';
            button.disabled = true;
            button.style.cursor = 'wait';
        });
    }
});
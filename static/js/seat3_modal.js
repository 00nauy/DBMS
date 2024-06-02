// modal.js

document.addEventListener('DOMContentLoaded', () => {
    const modal = document.getElementById('errorModal');
    const span = document.getElementsByClassName('close')[0];

    function showErrorModal(message) {
        const errorMessage = document.getElementById('errorMessage');
        errorMessage.textContent = message;
        modal.style.display = 'block';
    }

    span.onclick = function() {
        modal.style.display = 'none';
    }

    window.onclick = function(event) {
        if (event.target == modal) {
            modal.style.display = 'none';
        }
    }

    window.showErrorModal = showErrorModal;
});

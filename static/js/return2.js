// return2.js

document.addEventListener('DOMContentLoaded', () => {
    const modal = document.getElementById('resultModal');
    const modalContent = document.querySelector('.modal-content');
    const span = document.getElementsByClassName('close')[0];

    function showResultModal(message) {
        const resultMessage = document.getElementById('resultMessage');
        resultMessage.innerHTML = message; // Use innerHTML to handle HTML content
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

    const confirmButton = document.querySelector('.confirm-return');
    confirmButton.addEventListener('click', function(event) {
        event.preventDefault(); // 阻止默认链接行为

        fetch(this.href)
        .then(response => response.json())
        .then(data => {
            showResultModal(data.message);
        })
        .catch(error => console.error('Error:', error));
    });
});

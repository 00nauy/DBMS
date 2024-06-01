// add_book.js

document.addEventListener('DOMContentLoaded', () => {
    const modal = document.getElementById('successModal');
    const modalContent = document.querySelector('.modal-content');
    const span = document.getElementsByClassName('close')[0];

    function showSuccessModal(message) {
        const successMessage = document.getElementById('successMessage');
        successMessage.innerHTML = message; // Use innerHTML to handle HTML content
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

    document.getElementById('addBookForm').addEventListener('submit', function(event) {
        event.preventDefault(); // 阻止表单的默认提交

        const formData = new FormData(this);
        fetch(this.action, {
            method: 'POST',
            body: formData,
        })
        .then(response => response.text())
        .then(data => {
            showSuccessModal(data);
        })
        .catch(error => console.error('Error:', error));
    });
});

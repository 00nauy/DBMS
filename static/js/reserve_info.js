// reserve_info.js

document.addEventListener('DOMContentLoaded', () => {
    const modal = document.getElementById('resultModal');
    const modalContent = document.querySelector('.modal-content');
    const span = document.getElementsByClassName('close')[0];

    function showResultModal(message) {
        const resultMessage = document.getElementById('resultMessage');
        resultMessage.innerHTML = message; // 使用 innerHTML 以处理 HTML 内容
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

    const endButtons = document.querySelectorAll('.button');
    endButtons.forEach(button => {
        button.addEventListener('click', function(event) {
            event.preventDefault(); // 阻止默认链接行为

            fetch(this.href)
            .then(response => response.json().then(data => ({ status: response.status, body: data })))
            .then(response => {
                showResultModal(response.body.message);
            })
            .catch(error => console.error('Error:', error));
        });
    });
});

document.addEventListener('DOMContentLoaded', () => {
    const modal = document.getElementById('resultModal');
    const modalContent = document.querySelector('.modal-content');
    const span = document.getElementsByClassName('close')[0];

    function showResultModal(message) {
        const resultMessage = document.getElementById('resultMessage');
        resultMessage.innerHTML = message; 
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

    document.getElementById('returnForm').addEventListener('submit', function(event) {
        event.preventDefault(); // 阻止表单的默认提交

        const formData = new FormData(this);
        fetch(this.action, {
            method: 'POST',
            body: formData,
        })
        .then(response => response.text())
        .then(data => {
            if (data.startsWith('无借阅记录') || data.startsWith('请输入一个整数')) {
                showResultModal(data);
            } else {
                document.open();
                document.write(data);
                document.close();
            }
        })
        .catch(error => console.error('Error:', error));
    });

});

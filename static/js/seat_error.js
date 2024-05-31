document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('timeForm');
    form.addEventListener('submit', function(event) {
        event.preventDefault(); // 阻止表单的默认提交

        const formData = new FormData(form);
        fetch(form.action, {
            method: 'POST',
            body: formData,
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                showErrorModal(data.error);
            } else if (data.success) {
                document.open();
                document.write(data.html);
                document.close();
            }
        })
        .catch(error => console.error('Error:', error));
    });

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
});

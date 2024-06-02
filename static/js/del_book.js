
document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.del-book-form').forEach(form => {
        form.addEventListener('submit', function(event) {
            event.preventDefault(); // 阻止表单的默认提交

            const formData = new FormData(form);
            fetch(form.action + '?' + new URLSearchParams(formData), {
                method: 'GET',
            })
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    showErrorModal(data.error);
                } else if (data.success) {
                    showErrorModal(data.success); // 下架成功也显示弹窗提示
                }
            })
            .catch(error => console.error('Error:', error));
        });
    });
});

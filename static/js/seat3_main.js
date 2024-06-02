
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

    document.querySelectorAll('.reserve-form').forEach(reserveForm => {
        reserveForm.addEventListener('submit', function(event) {
            event.preventDefault(); // 阻止表单的默认提交

            const formData = new FormData(reserveForm);
            fetch(reserveForm.action + '?' + new URLSearchParams(formData), {
                method: 'GET',
            })
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    showErrorModal(data.error);
                } else if (data.success) {
                    showErrorModal(data.success); // 预约成功也显示弹窗提示
                }
            })
            .catch(error => console.error('Error:', error));
        });
    });
});

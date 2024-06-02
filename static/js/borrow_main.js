
document.addEventListener('DOMContentLoaded', () => {
    const select = document.getElementById('number');
    for (let i = 1; i <= 30; i++) {
        const option = document.createElement('option');
        option.value = i.toString();
        option.text = i.toString();
        select.appendChild(option);
    }

    const form = document.getElementById('numberForm');
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
                showErrorModal(data.success); // 预约成功也显示弹窗提示
            }
        })
        .catch(error => console.error('Error:', error));
    });
});

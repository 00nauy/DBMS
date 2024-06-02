document.addEventListener('DOMContentLoaded', () => {
    const hourSelects = [document.getElementById('hour'), document.getElementById('hour2')];
    hourSelects.forEach((select) => {
        for (let i = 8; i <= 21; i++) {
            const option = document.createElement('option');
            option.value = i.toString();
            option.text = i.toString();
            select.appendChild(option);
        }
    });

    const minuteSelects = [document.getElementById('minute'), document.getElementById('minute2')];
    minuteSelects.forEach((select) => {
        for (let i = 0; i <= 59; i++) {
            const option = document.createElement('option');
            option.value = i.toString();
            option.text = i.toString();
            select.appendChild(option);
        }
    });
});

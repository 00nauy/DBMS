

document.addEventListener('DOMContentLoaded', () => {
    const buttons = document.querySelectorAll('.button');

    buttons.forEach(button => {
        button.addEventListener('click', (event) => {
            event.preventDefault();
            button.classList.add('pop');
            setTimeout(() => {
                window.location.href = button.getAttribute('href');
            }, 400); // 等待动画完成后再跳转
        });
    });
});


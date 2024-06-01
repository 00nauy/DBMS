const images = [
    '../static/images/index_background/1.jpg',
    '../static/images/index_background/2.jpg',
    '../static/images/index_background/3.jpg',
    '../static/images/index_background/4.jpg',
    '../static/images/index_background/5.jpg',
    '../static/images/index_background/6.jpg',
    '../static/images/index_background/7.jpg',
    '../static/images/index_background/8.jpg',
    '../static/images/index_background/9.jpg',
    '../static/images/index_background/10.jpg',
];
let currentIndex = 0;

document.addEventListener('DOMContentLoaded', () => {
    const bg1 = document.querySelector('.bg1');
    const bg2 = document.querySelector('.bg2');

    const changeBackgroundImage = () => {
        currentIndex = (currentIndex + 1) % images.length;

        if (bg1.style.opacity == 1) {
            bg2.style.backgroundImage = `url('${images[currentIndex]}')`;
            bg2.style.opacity = 1;
            bg1.style.opacity = 0;
        } else {
            bg1.style.backgroundImage = `url('${images[currentIndex]}')`;
            bg1.style.opacity = 1;
            bg2.style.opacity = 0;
        }
    };

    // 初始化加载第一张背景图片
    bg1.style.backgroundImage = `url('${images[0]}')`;
    bg1.style.opacity = 1;
    setInterval(changeBackgroundImage, 5000); // 让每张图片停留5秒
});

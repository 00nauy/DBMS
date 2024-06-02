
document.addEventListener('DOMContentLoaded', () => {
    const modal = document.getElementById('errorModal');
    const modalContent = document.querySelector('.modal-content');
    const span = document.getElementsByClassName('close')[0];

    function showErrorModal(message) {
        const errorMessage = document.getElementById('errorMessage');
        errorMessage.innerHTML = message; 
        modal.style.display = 'block';
    }

    function showConfirmModal(message, onConfirm) {
        const errorMessage = document.getElementById('errorMessage');
        errorMessage.innerHTML = message;

        const confirmButton = document.createElement('button');
        confirmButton.textContent = '确定';
        confirmButton.style.marginRight = '10px';
        confirmButton.onclick = function() {
            modal.style.display = 'none';
            onConfirm();
        };

        const cancelButton = document.createElement('button');
        cancelButton.textContent = '取消';
        cancelButton.onclick = function() {
            modal.style.display = 'none';
        };

       
        errorMessage.innerHTML = message;
        errorMessage.appendChild(confirmButton);
        errorMessage.appendChild(cancelButton);

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

    document.querySelectorAll('.delete-announcement-form').forEach(form => {
        form.addEventListener('submit', function(event) {
            event.preventDefault(); // 阻止表单的默认提交

            showConfirmModal('确定要删除这条公告吗？', () => {
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
                        showErrorModal(`${data.success}<br>页面将在3秒后刷新。`);
                        setTimeout(() => {
                            location.reload();
                        }, 3000); // 3秒后刷新页面
                    }
                })
                .catch(error => console.error('Error:', error));
            });
        });
    });

    // 点击标题显示公告内容
    document.querySelectorAll('.announcement-title').forEach(title => {
        title.addEventListener('click', function(event) {
            event.preventDefault(); // 阻止默认点击行为

            const announcementModal = document.getElementById('announcementModal');
            const announcementTitle = document.getElementById('announcementTitle');
            const announcementContent = document.getElementById('announcementContent');
            const titleText = this.getAttribute('data-title');
            const contentText = this.getAttribute('data-content');

            announcementTitle.textContent = titleText;
            announcementContent.textContent = contentText;
            announcementModal.style.display = 'block';
        });
    });

    // 公告内容弹窗关闭逻辑
    const announcementModal = document.getElementById('announcementModal');
    const announcementSpan = announcementModal.getElementsByClassName('close')[0];

    announcementSpan.onclick = function() {
        announcementModal.style.display = 'none';
    }

    window.onclick = function(event) {
        if (event.target == announcementModal) {
            announcementModal.style.display = 'none';
        }
    }
});



// 点击标题显示公告内容
document.querySelectorAll('.announcement-title').forEach(title => {
    title.addEventListener('click', function(event) {
        event.preventDefault(); // 阻止默认点击行为

        const announcementModal = document.getElementById('announcementModal');
        const announcementTitle = document.getElementById('announcementTitle');
        const announcementContent = document.getElementById('announcementContent');
        const titleText = this.getAttribute('data-title');
        const contentText = this.getAttribute('data-content');

        announcementTitle.textContent = titleText;
        announcementContent.textContent = contentText;
        announcementModal.style.display = 'block';
    });
});


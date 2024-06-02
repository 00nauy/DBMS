document.addEventListener("DOMContentLoaded", function() {
    var modal = document.getElementById("announcementModal");

    var span = document.getElementById("announcementClose");

    span.onclick = function() {
        modal.style.display = "none";
    }

    // 获取所有公告链接并添加点击事件监听器
    var links = document.getElementsByClassName("announcement-link");
    for (var i = 0; i < links.length; i++) {
        links[i].onclick = function() {
            var title = this.getAttribute("data-title");
            var content = this.getAttribute("data-content");
            document.getElementById("modal-title").innerText = title;
            document.getElementById("modal-content").innerText = content;
            modal.style.display = "block";
        }
    }

    // 当用户点击窗口外部，关闭弹出窗口
    window.addEventListener("click", function(event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    });
});



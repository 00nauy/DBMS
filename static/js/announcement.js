// 获取弹出窗口
var modal = document.getElementById("announcementModal");

// 获取 <span> 元素，设置关闭按钮
var span = document.getElementsByClassName("close")[0];

// 当用户点击 <span> (x)，关闭弹出窗口
span.onclick = function() {
    modal.style.display = "none";
}

// 当用户点击窗口外部，关闭弹出窗口
window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
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

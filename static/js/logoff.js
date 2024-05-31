document.addEventListener("DOMContentLoaded", function() {
    // 获取模态窗口
    var logoffModal = document.getElementById("logoffModal");

    // 获取 <span> 元素，设置关闭按钮
    var span = document.getElementById("logoffClose");

    // 获取注销按钮
    var logoffButton = document.getElementById("btn2");

    // 获取确认和取消按钮
    var confirmLogoff = document.getElementById("confirmLogoff");
    var cancelLogoff = document.getElementById("cancelLogoff");

    // 当用户点击注销按钮时，打开模态窗口
    logoffButton.onclick = function(event) {
        event.preventDefault(); // 防止默认行为
        logoffModal.style.display = "block";
    }

    // 当用户点击 <span> (x)，关闭模态窗口
    span.onclick = function() {
        logoffModal.style.display = "none";
        logoffButton.classList.remove('pop');
        logoffButton.style.opacity = 1; // 确保按钮完全可见
    }

    // 当用户点击取消按钮，关闭模态窗口
    cancelLogoff.onclick = function() {
        logoffModal.style.display = "none";
        logoffButton.classList.remove('pop');
        logoffButton.style.opacity = 1; // 确保按钮完全可见
    }

    // 当用户点击确认按钮，执行注销操作
    confirmLogoff.onclick = function() {
        window.location.href = "/logoff"; // 执行注销操作
    }

    // 当用户点击窗口外部，关闭模态窗口
    window.addEventListener("click", function(event) {
        if (event.target == logoffModal) {
            logoffModal.style.display = "none";
            logoffButton.classList.remove('pop');
            logoffButton.style.opacity = 1; // 确保按钮完全可见
        }
    });
});

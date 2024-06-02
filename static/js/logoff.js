document.addEventListener("DOMContentLoaded", function() {
    var logoffModal = document.getElementById("logoffModal");

    var span = document.getElementById("logoffClose");

    var logoffButton = document.getElementById("btn2");

    var confirmLogoff = document.getElementById("confirmLogoff");
    var cancelLogoff = document.getElementById("cancelLogoff");

    logoffButton.onclick = function(event) {
        event.preventDefault(); 
        logoffModal.style.display = "block";
    }

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

    confirmLogoff.onclick = function() {
        window.location.href = "/logoff";
    }

    window.addEventListener("click", function(event) {
        if (event.target == logoffModal) {
            logoffModal.style.display = "none";
            logoffButton.classList.remove('pop');
            logoffButton.style.opacity = 1; // 确保按钮完全可见
        }
    });
});

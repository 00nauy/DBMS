// // sign.js

// document.addEventListener('DOMContentLoaded', () => {
//     const modal = document.getElementById('resultModal');
//     const modalContent = document.querySelector('.modal-content');
//     const span = document.getElementsByClassName('close')[0];

//     function showResultModal(message) {
//         const resultMessage = document.getElementById('resultMessage');
//         resultMessage.innerHTML = message; // Use innerHTML to handle HTML content
//         modal.style.display = 'block';
//     }

//     span.onclick = function() {
//         modal.style.display = 'none';
//     }

//     window.onclick = function(event) {
//         if (event.target == modal) {
//             modal.style.display = 'none';
//         }
//     }

//     document.getElementById('signForm').addEventListener('submit', function(event) {
//         event.preventDefault(); // 阻止表单的默认提交

//         const formData = new FormData(this);
//         fetch(this.action, {
//             method: 'POST',
//             body: formData,
//         })
//         .then(response => response.json().then(data => ({ status: response.status, body: data })))
//         .then(response => {
//             if (response.status === 200) {
//                 document.open();
//                 document.write(response.body);
//                 document.close();
//             } else {
//                 showResultModal(response.body.message);
//             }
//         })
//         .catch(error => console.error('Error:', error));
//     });
// });


document.addEventListener('DOMContentLoaded', () => {
    const modal = document.getElementById('resultModal');
    const modalContent = document.querySelector('.modal-content');
    const span = document.getElementsByClassName('close')[0];

    function showResultModal(message) {
        const resultMessage = document.getElementById('resultMessage');
        resultMessage.innerHTML = message; // Use innerHTML to handle HTML content
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

    document.getElementById('returnForm').addEventListener('submit', function(event) {
        event.preventDefault(); // 阻止表单的默认提交

        const formData = new FormData(this);
        fetch(this.action, {
            method: 'POST',
            body: formData,
        })
        .then(response => response.text())
        .then(data => {
            if (data.startsWith('无预约记录') || data.startsWith('请输入一个整数')) {
                showResultModal(data);
            } else {
                document.open();
                document.write(data);
                document.close();
            }
        })
        .catch(error => console.error('Error:', error));
    });

});


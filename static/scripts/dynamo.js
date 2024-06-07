document.addEventListener("DOMContentLoaded", function() {
    var chatWindow = document.getElementById('chatWindow');

    function checkOverflow() {
        if (chatWindow.scrollHeight > chatWindow.clientHeight) {
            chatWindow.classList.add('overflow');
        } else {
            chatWindow.classList.remove('overflow');
        }
    }

    checkOverflow();
    window.addEventListener('resize', checkOverflow);
});
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

$(document).ready(function () {
    $("#chat").on("submit", (event) =>  {
        event.preventDefault();
        $('#sendMessage').prop("disabled",true);
        $('#dynamoResponse').html('');
        $('#loading').prop("hidden",false);
        var msg = $("#userMessage").val();
        $.ajax({
            type: "POST",
            url: "/chat",
            data: {message: msg},
            dataType: "json",
            success: function (response) {
                document.getElementById('pingAudio').play();
                $("#dynamoResponse").html(response.talk);
                $("#userMessage").val('');
            },
            complete: function () {
                $('#sendMessage').prop("disabled",false);
                $('#loading').prop("hidden",true);
            }
        });
    })
});
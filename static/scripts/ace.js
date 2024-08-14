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
        $('#aceResponse').html('');
        $('#loading').prop("hidden",false);
        var msg = $("#userMessage").val();
        $.ajax({
            type: "POST",
            url: "/chat_ace",
            data: {message: msg},
            dataType: "json",
            success: function (response) {
                document.getElementById('pingAudio').play();
                $("#aceResponse").html(response.talk);
                $("#userMessage").val('');
            },
            complete: function () {
                $('#sendMessage').prop("disabled",false);
                $('#loading').prop("hidden",true);
            }
        });
    })

    $('#createTask').submit(function (e) {
        e.preventDefault();
        $('#createTaskButton').prop("disabled",true);
        task = $('#taskDesc').val();
        $.ajax({
            type: "POST",
            url: "/create_task",
            data: {taskDesc:task},
            dataType: "json",
            success: function (response) {
                $('#createTaskButton').prop("disabled",true);
                window.location.href = window.location.href;
            }
        });
    });

    $('#createProject').submit(function (e) {
        $('#createProjectButton').prop("disabled",true);
        $("#spinner").prop("hidden",false);
    });

    $('#projectInit').submit(function (e) { 
        $('#initProjectButton').prop("disabled",true);
        $("#initSpinner").prop("hidden",false);
    });

    $('#projectInitToggle').click(function (e) { 
        let toggle = document.getElementById("toggleIcon");
    
        if (toggle.classList.contains("fa-eye")) {
            toggle.classList.replace("fa-eye", "fa-eye-slash");
            $("#infoPane").prop("hidden",true);
            $("#projectInitToggle").attr("title","Show");
        } else if (toggle.classList.contains("fa-eye-slash")) {
            toggle.classList.replace("fa-eye-slash", "fa-eye");
            $("#infoPane").prop("hidden",false);
            $("#projectInitToggle").attr("title","Hide");
        }
    });    

    $('.discussions-container').on('submit', '.discussion-form', function(event) {
        event.preventDefault();
        var $form = $(this);
        var actionUrl = $form.attr('action');
        var formData = $form.serialize();
        var formId = $form.find('textarea').attr('id'); 
        var index = formId.split('-')[1];
    
        $('#talk-'+index).html('');
        $('#talkSpinner').removeAttr("hidden");
        $('#msg-'+index).prop("disabled", true);
        $("#askButton-"+index).prop("disabled", true);
        
        $.ajax({
            type: 'POST',
            url: actionUrl,
            data: formData,
            dataType: 'json',
            success: function(response) {
                console.log(response.talk);
                $('#catchup-' + index).hide();
                $('#talk-' + index).html(response.talk).show();
                $form.find('.message').val('');
                $('#msg-'+index).removeAttr("disabled"); 
                $("#askButton-"+index).removeAttr("disabled"); 
                $('#talkSpinner').prop("hidden","true");
                hljs.highlightAll();
            },
            error: function(xhr, status, error) {
                console.error("Error sending message: " + error);
                $('#talk-' + index).html('<div class="alert alert-danger">Failed to send message.</div>').show();
            }
        });
    });
    
    
});

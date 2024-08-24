document.addEventListener("DOMContentLoaded", function() {
    var toastElements = document.querySelectorAll('.toast');
    toastElements.forEach(function(toastElement) {
        var toast = new bootstrap.Toast(toastElement);
        toast.show();
    });

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

    $('#uploadFileModal').on('submit', 'form', function(event) {
        event.preventDefault();
        var $form = $(this);
        var actionUrl = $form.attr('action');
        var formData = new FormData($form[0]);
        var formId = $form.find('textarea').attr('id'); 
        var index = formId.split('-')[1];

        $('#talkSpinnerModal').removeAttr("hidden");
    
        $.ajax({
            type: 'POST',
            url: actionUrl,
            data: formData,
            contentType: false,
            processData: false,
            dataType: 'json',
            success: function(response) {
                console.log(response.talk);
                var modalIndex = $form.find('textarea').attr('id').split('-')[1];
                $('#talk-' + modalIndex).html(response.talk).show();
                $('#uploadFileModal').modal('hide');
                $('#talkSpinnerModal').prop("hidden","true");
                $('#attached-' + index).prop("hidden","false");
                hljs.highlightAll();
                if (response.file_link) {
                    $('#attached-' + index).attr("src", response.file_link);
                    $('#attached-' + index).removeAttr("hidden");
                    $('#attached-' + index).attr("width", "200");
                    $('#attached-' + index).attr("height", "200");
                    $('#attached-' + index).attr("draggable", "false");
                } else {
                    $('#attached-' + index).hide();
                }
            },
            error: function(xhr, status, error) {
                console.error("Error uploading file: " + error);
            }
        });
    });
    
    $('#uploadFileModalFree').on('submit', 'form', function(event) {
        event.preventDefault();
        $('#sendMessage').prop("disabled",true);
        $('#aceResponse').html('');
        $('#loading').prop("hidden",false);
        $('#talkSpinnerModal').removeAttr("hidden");
        var formData = new FormData(this);
    
        $.ajax({
            type: 'POST',
            url: "/chat_ace",
            data: formData,
            contentType: false,
            processData: false,
            dataType: 'json',
            success: function(response) {
                $('#talkSpinnerModal').attr("hidden", true);
                $("#aceResponse").html(response.talk);
    
                if (response.file_link) {
                    $('#attached').attr("src", response.file_link);
                    $('#attached').removeAttr("hidden");
                    $('#attached').attr("width", "200");
                    $('#attached').attr("height", "200");
                    $('#attached').attr("draggable", "false");
                } else {
                    $('#attached').hide();
                }
            },
            error: function(xhr, status, error) {
                $('#talkSpinnerModal').attr("hidden", true);
                console.error("Error uploading file: " + error);
                $("#aceResponse").html("An error occurred while uploading the file.");
            }
        });
    });

    $(".updateHabits").on('submit', '.updateHabit', function (e) {
        e.preventDefault();
        
        var $form = $(this);
        var url = $form.attr('action');
        var index = $form.attr('id').split('_')[1];
        
        $('#spinnerUpdate_' + index).removeAttr("hidden");
        $("#updateHabit_" + index + "_b").prop("disabled", true);
        
        $.ajax({
            type: "POST",
            data: {},
            dataType: "json",
            url: url,
            success: function (response) {
                console.log('AJAX response:', response);
            
                $('#spinnerUpdate_' + index).attr("hidden", true);
                $("#updateHabit_" + index + "_b").prop("disabled", true);
                
                if (response.success) {
                    $('#score_' + index).html(response.score);
                    var widthPercent = ((response.score / response.max_score) * 100).toFixed(2);
                    console.log('Progress Bar Width:', widthPercent);
                    $("#progressBar_" + index).css("width", widthPercent + "%").attr("aria-valuenow", response.score);
            
                    if (response.score == response.max_score) {
                        $("#status_" + index).html("Done");
                    }
                } else {
                    if (response.missed) {
                        $("#status_" + index).html("Failed");
                    }
                    console.error("Failed to update habit:", response.error);
                }
            },
            error: function (xhr, status, error) {
                console.error("AJAX request failed:", error);
                $('#spinnerUpdate_' + index).attr("hidden", true);
                $("#updateHabit_" + index + "_b").prop("disabled", false);
            }
        });
    });

    
    $(".updateHabits").on('submit', '.deleteHabit', function (e) {
        e.preventDefault();
        
        var $form = $(this);
        var url = $form.attr('action');
        var index = $form.attr('id').split('_')[1];
        $('#spinnerDelete_' + index).removeAttr("hidden");
        
        $.ajax({
            type: "POST",
            data: {},
            dataType: "json",
            url: url,
            success: function (response) {
                $('#spinnerDelete_' + index).attr("hidden", true);
                
                if (response.success) {
                    if ($("tbody tr").length === 1) {
                        location.reload();
                    } else {
                        $('#habitRow_' + index).remove();
                    }
                } else {
                    console.error("Failed to delete habit:", response.error);
                }
            },
            error: function (xhr, status, error) {
                console.error("AJAX request failed:", error);
                $('#spinnerDelete_' + index).attr("hidden", true);
            }
        });
    });    

    $('#createHabit').submit(function (e) { 
        $('#newHabit').prop("disabled","true");
    });
    
});

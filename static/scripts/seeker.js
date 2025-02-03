document.addEventListener("DOMContentLoaded", function() {
    var toastElements = document.querySelectorAll('.toast');
    toastElements.forEach(function(toastElement) {
        var toast = new bootstrap.Toast(toastElement);
        toast.show();
    });
});

$(document).ready(function () {
    $("#chat").on("submit", (event) =>  {
        event.preventDefault();
        $('#sendMessage').prop("disabled",true);
        $('#seekerResponse').html('');
        $('#loading').prop("hidden",false);
        var msg = $("#userMessage").val();
        $.ajax({
            type: "POST",
            url: "/chat_seeker",
            data: {message: msg},
            dataType: "json",
            success: function (response) {
                document.getElementById('pingAudio').play();
                $("#seekerResponse").html(response.talk);
                $("#userMessage").val('');
            },
            complete: function () {
                $('#sendMessage').prop("disabled",false);
                $('#loading').prop("hidden",true);
            }
        });
    })
});

$(document).ready(function () {
    $("#quickWikiChat").on("submit", function (event) {
        event.preventDefault();
        var msg = $("#userWikiMessageQuick").val();
        $("#userWikiMessageQuick").prop("disabled", true);
        $("#askButton").prop("disabled", true);
        $("#wikiResponseQuick").html('');
        $("#spinnerQuick").show();
        $.ajax({
            type: "POST",
            url: "/chat_wiki",
            data: { message: msg },
            dataType: "json",
            success: function (response) {
                $("#wikiResponseQuick").html(response.talk);
                $("#userWikiMessageQuick").val('');
                hljs.highlightAll();
            },
            complete: function () {
                $("#userWikiMessageQuick").prop("disabled", false);
                $("#askButton").prop("disabled", false);
                $("#spinnerQuick").hide();
            }
        });
    });
});


$(document).ready(function() {
    $('#wiki-form').on('submit', function(event) {
        event.preventDefault();

        const url = $('#wiki-url').val();
        const submitButton = $('#submit-btn');
        const spinner = $('#spinner');
        const buttonText = $('#button-text');
        const messageDiv = $('#message');
        const summaryParagraph = $('#summary');
        const summaryModalLabel = $('#summaryModalLabel');
        const discuss = $('#discuss');

        const wikiUrlPattern = /^https:\/\/en\.wikipedia\.org\/wiki\/.+/;
        if (!wikiUrlPattern.test(url)) {
            messageDiv.html('<div class="alert alert-danger">Please enter a valid Wikipedia URL.</div>');
            return;
        }

        messageDiv.html('');
        discuss.addClass('d-none');

        submitButton.prop('disabled', true);
        spinner.removeClass('d-none');

        $("#wikiResponseQuick").html('');
        
        $.ajax({
            url: '/condense_wiki',
            type: 'POST',
            data: JSON.stringify({ url: url }), 
            contentType: 'application/json',  
            success: function(response) {
                if (response.success != "False") {
                    messageDiv.html(`
                        <div id="processed" class="alert alert-success">
                            Content successfully processed! You can see the processed summary 
                            <a href="#" class="text-link" data-bs-toggle="modal" data-bs-target="#summaryModal">here</a>.
                        </div>
                    `
                    );
                    summaryParagraph.html(`${response.summary}`);
                    summaryModalLabel.html(`${response.title}`);
                    discuss.removeClass('d-none');
                }
                else {
                    messageDiv.html('<div class="alert alert-danger">Invalid URL!</div>');
                }
            },
            error: function(xhr) {
                messageDiv.html('<div class="alert alert-danger">An error occurred: ' + xhr.responseText + '</div>');
            },
            complete: function() {
                spinner.addClass('d-none');
                submitButton.prop('disabled', false);
            }
        });
    });
});

$(document).ready(function() {
$(".phil-init").click(function(e) {
    e.preventDefault();
    
    var token = $(this).attr("id").replace("init", "").toLowerCase();
    
    $.ajax({
    url: "/config_philosopher/" + token, 
    method: "POST",
    data: {},
    success: function(response) {
        if (response.success) {
        console.log(response.resp)
        console.log("Success!");
        } else {
        console.log("Error!");
        }
    },
    error: function(xhr, status, error) {
        console.log("AJAX error: " + error);
    }
    });
});
});

$(document).ready(function () {
    $("#chat").on("submit", (event) =>  {
        event.preventDefault();
        $('#sendMessage').prop("disabled",true);
        $('#seekerResponse').html('');
        $('#loading').prop("hidden",false);
        var msg = $("#userMessage").val();
        $.ajax({
            type: "POST",
            url: "/chat_seeker",
            data: {message: msg},
            dataType: "json",
            success: function (response) {
                document.getElementById('pingAudio').play();
                $("#seekerResponse").html(response.talk);
                $("#userMessage").val('');
            },
            complete: function () {
                $('#sendMessage').prop("disabled",false);
                $('#loading').prop("hidden",true);
            }
        });
    })
});

$(document).ready(function () {
    $(".message-form").on("submit", function (event) {
        event.preventDefault();
        
        var philosopher = $(this).attr("id").replace("pchat", "").toLowerCase();
        var sendButton = $(this).find('button');
        var messageInput = $(this).find(".message-input");
        var chatWindow = $("#chatWindow");
        var loadingIndicator = $(this).closest('.modal-content').find("#loading");
        var seekerResponse = $("#"+philosopher+"Response");

        sendButton.prop("disabled", true);
        seekerResponse.html('');
        loadingIndicator.prop("hidden", false);

        var msg = messageInput.val();

        $.ajax({
            type: "POST",
            url: "/chat_philosopher",
            data: { message: msg },
            dataType: "json",
            success: function (response) {
                document.getElementById('pingAudio').play();
                seekerResponse.html(response.resp);
                messageInput.val('');
            },
            complete: function () {
                sendButton.prop("disabled", false);
                loadingIndicator.prop("hidden", true);
            }
        });
    });
});

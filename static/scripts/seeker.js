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

$(document).ready(function() {
    const socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);
    $('#wiki-form').on('submit', function(event) {
        event.preventDefault();

        const url = $('#wiki-url').val();
        const submitButton = $('#submit-btn');
        const spinner = $('#spinner');
        const buttonText = $('#button-text');
        const messageDiv = $('#message');
        const topicsContainer = $('#topics-container');
        const modalsContainer = $('#modal-container');
        const table = $('#wiki-table');
        topicsContainer.empty();
        modalsContainer.empty();
        table.prop("hidden","true");
        

        const wikiUrlPattern = /^https:\/\/en\.wikipedia\.org\/wiki\/.+/;
        if (!wikiUrlPattern.test(url)) {
            messageDiv.html('<div class="alert alert-danger">Please enter a valid Wikipedia URL.</div>');
            return;
        }

        submitButton.prop('disabled', true);
        spinner.removeClass('d-none');

        $.ajax({
            url: '/condense_wiki',
            type: 'POST',
            data: JSON.stringify({ url: url }), 
            contentType: 'application/json',  
            success: function(response) {
                console.log(response)
                if (response.success != "False") {
                    console.log(response);
                    messageDiv.html('<div class="alert alert-success">Content successfully processed!</div>');
                    topicsContainer.empty();
                    modalsContainer.empty();
                    table.removeAttr("hidden");
                    
                    $.each(response.topics, function(topicTitle, topicContent) {
                        let topicTitleId = topicTitle.replace(/ /g,'_');
                        console.log(topicTitleId)
                        const topicElement = `
                            <tr>
                                <td><i class="fa-brands fa-wikipedia-w"></i>&nbsp;${topicTitle}</td>
                                <td><button type="button" class="btn btn-sm btn-dark" data-bs-toggle="modal" data-bs-target="#${topicTitleId}Modal">Read</button></td>
                            </tr>`;
                        const modalElement = `
                            <div class="modal fade" id="${topicTitleId}Modal" tabindex="-1">
                                <div class="modal-dialog">
                                    <div class="modal-content">
                                        <div class="modal-header border-none">
                                            <h1 class="modal-title fs-5 fw-bold"><i class="fa-brands fa-wikipedia-w"></i>&nbsp;${topicTitle}</h1>
                                        </div>
                                        <div class="modal-body">
                                            ${topicContent}
                                        </div>
                                        <div class="modal-footer border-none">
                                            <button type="button" class="btn dismiss" data-bs-dismiss="modal">Close</button>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        `;
                        topicsContainer.append(topicElement);
                        modalsContainer.append(modalElement);
                    });
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
    socket.on('processing_topic', function(data) {
        const topicMessage = `<div class="alert alert-info">Processing ${data.topic}...</div>`;
        $('#message').html(topicMessage);
    });
});
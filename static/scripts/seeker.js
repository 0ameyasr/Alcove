document.addEventListener("DOMContentLoaded", function() {
    var toastElements = document.querySelectorAll('.toast');
    toastElements.forEach(function(toastElement) {
        var toast = new bootstrap.Toast(toastElement);
        toast.show();
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
        const topicsContainer = $('#topics-container');

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
                console.log(response);
                messageDiv.html('<div class="alert alert-success">Content successfully processed!</div>');
                topicsContainer.empty();
                
                $.each(response.topics, function(topicTitle, topicContent) {
                    const topicElement = `
                        <div class="card my-3">
                            <div class="card-header">
                                <h5 class="card-title">${topicTitle}</h5>
                            </div>
                            <div class="card-body">
                                <p class="card-text">${topicContent}</p>
                            </div>
                        </div>`;
                    topicsContainer.append(topicElement);
                });
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

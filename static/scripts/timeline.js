$(document).ready(function () {
    $('#moodForm').submit(function (e) {
        e.preventDefault();
        let $submitButton = $('#postNote');
        let $spinner = $submitButton.find('.spinner-border');
        $submitButton.prop('disabled', true);
        $spinner.show();
        
        let noteCorpus = $('#noteArea').val();
        $.ajax({
            type: "POST",
            url: "/mood_timeline_update",
            data: {corpus: noteCorpus},
            dataType: "json",
            success: function (response) {
                window.location.href = window.location.href;
            },
            error: function () {
                $submitButton.prop('disabled', false);
                $spinner.hide();
            }
        });
    });
    $('.spinner-border').hide();
});
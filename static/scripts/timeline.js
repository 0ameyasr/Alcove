$(document).ready(function () {
    $('#moodForm').submit(function (e) { 
        e.preventDefault();
        let noteCorpus = $('#noteArea').val();
        $.ajax({
            type: "POST",
            url: "/mood_timeline_update",
            data: {corpus: noteCorpus},
            dataType: "json",
            success: function (response) {
                window.location.href=window.location.href;
                $('#status').html(response.flash);
                document.getElementById('postNote').disabled = true;
                document.getElementById('pingAudio').play();
            }
        });
    });
});
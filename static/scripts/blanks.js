window.onload = function () {
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl)
    })
}

$(document).ready(function () {
    $("#save").on("submit", (event) =>  {
        event.preventDefault();
        var journalText = $("#journalText").val();
        var token = $("#token").text();
        $.ajax({
            type: "POST",
            url: "/saves/"+token,
            data: {jtext: journalText},
            dataType: "json",
            success: function (response) {
                document.getElementById('pingAudio').play();
                $('#status').html(response.status);
            }
        });
    })
});
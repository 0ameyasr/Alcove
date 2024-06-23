window.onload = function () {
    document.getElementById("removePrompt").onclick = function () {
        document.getElementById("promptForJournal").hidden = true;
    }
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl)
    })
}

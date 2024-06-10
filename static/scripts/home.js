window.onload = function () {

    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl)
    })
    const toast = document.getElementById('liveToast')
    const toast_bs = bootstrap.Toast.getOrCreateInstance(toast)
    toast_bs.show()
}
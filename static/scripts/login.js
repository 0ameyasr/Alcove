const fontColor = "#31363f";
caption = document.getElementById("talk")
register_form = document.getElementsByClassName("details-body")[0]
login_form = document.getElementsByClassName("login-body")[0]
logo = document.getElementById("icon")

document.addEventListener('DOMContentLoaded', function() {
    var nicknameInput = document.getElementById('nickname-input');
    var safewordInput = document.getElementById('safeword-input');
    var recoveryInput = document.getElementById('recovery-input');
    var registerButton = document.getElementById('register-continue');
    var recaptchaContainer = document.getElementById('register-recaptcha');
    
    var nicknameRegex = /^[a-zA-Z0-9]{6,20}$/;
    var safewordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{6,32}$/;
    var emailRegex = /^[a-zA-Z0-9._%+-]+@gmail\.com$/;

    function validateForm() {
        var nickname = nicknameInput.value.trim();
        var safeword = safewordInput.value.trim();
        var recovery = recoveryInput.value.trim();

        var isNicknameValid = nicknameRegex.test(nickname);
        var isSafewordValid = safewordRegex.test(safeword);
        var isEmailValid = emailRegex.test(recovery);

        nicknameInput.classList.toggle('is-invalid', !isNicknameValid);
        safewordInput.classList.toggle('is-invalid', !isSafewordValid);
        recoveryInput.classList.toggle('is-invalid', !isEmailValid);

        var isValidForm = isNicknameValid && isSafewordValid && isEmailValid;

        if (isValidForm) {
            recaptchaContainer.hidden = false;
            document.getElementById('login-status').innerText = ""
        } else {
            recaptchaContainer.hidden = true;
            registerButton.disabled = true;
        }

        return isValidForm;
    }

    function onRecaptchaSubmitRegister() {
        registerButton.disabled = !validateForm();
    }

    nicknameInput.addEventListener('input', validateForm);
    safewordInput.addEventListener('input', validateForm);
    recoveryInput.addEventListener('input', validateForm);
});

window.onload = function () {

    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl)
    })

    const messages = [
        "Alcove"
    ];

    typewrite(messages[0], "talk", 1000, fontColor)
    setTimeout(() => { caption.hidden = true; login_form.hidden = false; logo.hidden = false;}, 2500)
}

function typewrite(message, id, timeout, color) {
    let counter = 0, string = "";
    let messageBar = document.getElementById(id);

    setTimeout(function () {
        let interval = setInterval(function () {
            if (counter < message.length) {
                string += message[counter] + "_";
                messageBar.innerText = string;
                setTimeout(function () { string = string.replace('_', ''); }, 100);
                messageBar.innerText = string;
                messageBar.style.color = fontColor;
                counter++;
            }
            if (counter == message.length) {
                let subinterval = setInterval(function () {
                    string = string.replace('_', '');
                    messageBar.innerText = string;
                    string += '_';
                }, 100);
                messageBar.style.color = color;
                clearInterval(interval);
                string = string.replace('_', '');
                messageBar.innerText = string;
                string += '_';
                clearInterval(subinterval);
            }
        }, 120);
    }, timeout);
}

function registerDirect() {
    login_form.hidden = true;
    register_form.hidden = false;
}

function loginDirect() {
    login_form.hidden = false;
    register_form.hidden = true;
}

function forgotPassword()
{
    login_form.hidden = true;
    register_form.hidden = true;
    document.getElementById("forgot").hidden = false;
    caption.hidden = false;
    caption.innerText="Alcove"
    logo.hidden = true;
}

function onRecaptchaSubmitRegister()
{
    var registerButton = document.getElementById('register-continue');
    registerButton.disabled = false;
}

function onRecaptchaSubmitLogin()
{
    document.getElementById("login-continue").disabled = false;
}
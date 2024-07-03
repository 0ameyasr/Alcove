window.onload = function () {
    const fontColor = '#31363f';
    const nickname = document.getElementById("nickname").innerText;
    const disclaimer = document.getElementById("disclaimer");
    const info = document.getElementById("info");
    const proceed = document.getElementById("proceed");

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

    function infoDisplay(message) {
        info.classList.remove("fade-in");
        void info.offsetWidth;
        info.classList.add("fade-in");
        info.innerText = message;
    }

    function delay(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }    

    async function introduction() {
        await delay(0);
        infoDisplay("Hello, "+nickname+"!");

        await delay(4000);
        infoDisplay("We're going to be scanning your mental landscape.");

        await delay(4000);
        infoDisplay("But for that, we need to know more about you.");

        await delay(4000);
        infoDisplay("Please cooperate with us. It will take a while, but it's worth it.");

        await delay(4000);
        disclaimer.classList.add("fade-in");
        await delay(500);
        disclaimer.hidden = false;
        info.hidden = true;

        await delay(1000);
        proceed.hidden = false;
    }

    introduction()
}

document.addEventListener("DOMContentLoaded", function() {
    const textarea = document.getElementById('radarResponse');
    const wordCountDisplay = document.getElementById('wordCount');
    const maxWords = 200;

    textarea.addEventListener('input', function() {
    const words = textarea.value.split(/\s+/).filter(word => word.length > 0);
    const remainingWords = maxWords - words.length;
    wordCountDisplay.textContent = `Remaining words: ${remainingWords}`;

    if (remainingWords < 0) {
        wordCountDisplay.classList.add('text-danger');
        wordCountDisplay.classList.remove('text-muted');
        textarea.value = words.slice(0, maxWords).join(' ');
    } else {
        wordCountDisplay.classList.remove('text-danger');
        wordCountDisplay.classList.add('text-muted');
    }
});
});

$('#radarForm').submit(function (e) {
    e.preventDefault();
    const resp = $('#radarResponse').val();
    const wordCountDisplay = document.getElementById("wordCount");
    console.log(resp);
    $.ajax({
        type: "POST",
        url: "/radar_response",
        data: {response: resp},
        dataType: "json",
        success: function (response) {
            document.getElementById("pingAudio").play();
            $('#radarResponse').val('');
            document.getElementById("question").innerText = response.question;
            wordCountDisplay.textContent = `Remaining words: 200`;
            wordCountDisplay.classList.add('text-muted');
            wordCountDisplay.classList.remove('text-danger');
        }
    });
});

$(document).ready(function() {
    $('#radarResponse').keydown(function(event) {
        if (event.keyCode === 13 && !event.shiftKey) {
            event.preventDefault();
            $('#radarForm').submit();
        }
    });
});

async function beginRadar(questions) {
    const nickname = document.getElementById("nickname").innerText;
    const disclaimer = document.getElementById("disclaimer");
    const info = document.getElementById("info");
    const proceed = document.getElementById("proceed");
    const interactPane = document.getElementById("interactPane");
    
    info.hidden = true;
    proceed.hidden = true;
    disclaimer.hidden = true;

    interactPane.classList.add("fade-in");
    interactPane.hidden = false;
}

$('#proceed').click(function (e) {
    e.preventDefault();
    beginRadar();
});
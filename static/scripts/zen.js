window.onload = function () {
    const fontColor = "#eeeeee";
    const talk = document.getElementById("talk");
    const info = document.getElementById("info");
    const begin = document.getElementById("begin");

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


    typewrite("bored.ai","talk",0,fontColor);
    typewrite("Zen Mode","talk",3000,fontColor);
    setTimeout(()=>{
        talk.hidden = true;
        info.hidden = false;
        infoDisplay("Soon, you are going to be performing a form of Zen meditation.");
    },6000);
    setTimeout(()=>{infoDisplay("It goes by the name, 'Zazen'.");},9000);
    setTimeout(()=>{infoDisplay("'Do not dwell in the past, do not dream of the future, concentrate the mind on the present moment.' – Buddha")},13000);
    setTimeout(()=>{infoDisplay("Before we begin, you must give your preference.")},20000);
    setTimeout(()=>{
        infoDisplay("Choose a form of meditation.")
        setInterval(()=>{},500);
        choices.hidden = false;
    },25000);
}

function infoDisplay(message) {
    info.classList.remove("fade-in");
    void info.offsetWidth;
    info.classList.add("fade-in");
    info.innerText = message;
}

function updateProgressBar(duration,persist=False) {
    const progressBar = document.getElementById('progressBar');
    const bar = document.getElementById("bar");

    bar.hidden = false; 
    let progress = 0;
    let intervalTime = duration / 100;

    let interval = setInterval(() => {
      progress++;
      progressBar.style.width = progress + '%';
      progressBar.setAttribute('aria-valuenow', progress);
      if (progress >= 100) {
        clearInterval(interval);
        if (!persist){
            setTimeout(() => {
                bar.hidden = true;
            }, 500);
        }
      }
    }, intervalTime);
}


function delay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}


async function beginSusokuKan()
{
    const content = document.getElementById("contentHolder");
    const talk = document.getElementById("talk");
    const info = document.getElementById("info");
    const begin = document.getElementById("beginSusokuKan");
    const bar = document.getElementById("bar");
    const details = document.getElementById("susokuKanDetails");

    content.style.background = 'transparent';

    const video = document.getElementById("gameVid");
    const source = document.getElementById("vidSrc");
    video.loop = true;
    video.playsinline = true;
    video.play();
    info.hidden = true;
    begin.hidden = true;
    talk.hidden = true;
    details.hidden = true;

    await delay(3000);
    info.hidden = false;
    infoDisplay("Before we begin, please ensure you have proper posture.");

    await delay(5000);
    infoDisplay("Make sure the screen is at comfortable eye level.");

    await delay(5000);
    infoDisplay("Focus your eyes on the dot. Close them half-way.");

    await delay(5000);
    infoDisplay("Inhale as the dot grows, and slowly exhale as it shrinks.");

    await delay(5000);
    infoDisplay("Count each exhalation from one to ten, and repeat.");

    await delay(5000);
    infoDisplay("You may close the window after you are satisfied.")

    await delay(3000);
    infoDisplay("");
    const dot = document.getElementById('dot');
    dot.classList.add("fade-in");
    const dotMode = document.getElementById('dotMode');
    dot.hidden = false;

    function breatheIn() {
        dot.style.animation = 'breathe-in 4s linear';
        dotMode.innerText = 'IN';
        setTimeout(breatheOut, 4000);
    }

    function breatheOut() {
        dot.style.animation = 'breathe-out 6s linear';
        dotMode.innerText = 'OUT';
        setTimeout(breatheIn, 6000);
    }

    breatheIn();
}

async function beginShikantaza()
{
    const content = document.getElementById("contentHolder");
    const talk = document.getElementById("talk");
    const info = document.getElementById("info");
    const begin = document.getElementById("beginShikantaza");
    const bar = document.getElementById("bar");
    const details = document.getElementById("shikantazaDetails")
    const focusDot = document.getElementById("focusDot")

    content.style.background = 'transparent';

    const video = document.getElementById("gameVid");
    const source = document.getElementById("vidSrc");
    video.loop = true;
    video.playsinline = true;
    video.play();
    info.hidden = true;
    begin.hidden = true;
    talk.hidden = true;
    details.hidden = true;

    await delay(5000);
    info.hidden = false;
    infoDisplay("Before we begin, ensure you have proper posture.");

    await delay(5000);
    infoDisplay("Close your eyes half-way, and focus on the center of the screen.");

    await delay(5000);
    infoDisplay("Do not focus on anything, let your mind wander.");

    await delay(5000);
    infoDisplay("Acknowledge your thoughts without judgement, and breathe normally.");

    await delay(5000);
    infoDisplay("Do not engage in your thoughts. Just let them pass by.");

    await delay(5000);
    infoDisplay("Lose yourself in a meditative trance.");

    await delay(5000);
    infoDisplay("When you are satisfied, you may close this window.");
    info.hidden = true;
    focusDot.classList.add("fade-in");
    focusDot.hidden = false;
}

async function susokuKan() {
    const details = document.getElementById("susokuKanDetails");
    const proceed = document.getElementById("beginSusokuKan");
    const postures = document.getElementById("postures");

    document.getElementById("taiko").play();
    infoDisplay("Susoku-Kan");
    
    await delay(5000);
    infoDisplay("Recommended Postures");
    postures.classList.add("fade-in");
    await delay(500);
    postures.hidden = false;

    await delay(5000);
    infoDisplay("")
    postures.hidden = true
    
    details.classList.add("fade-in");
    await delay(2000);
    details.hidden = false;

    await delay(1000);
    proceed.classList.add("fade-in");
    proceed.hidden = false;
}

async function shikantaza() {
    const details = document.getElementById("shikantazaDetails");
    const proceed = document.getElementById("beginShikantaza");
    const postures = document.getElementById("postures");

    document.getElementById("taiko").play();
    infoDisplay("Shikantaza");

    await delay(5000);
    infoDisplay("Recommended Postures");
    postures.classList.add("fade-in");
    await delay(500);
    postures.hidden = false;

    await delay(5000);
    infoDisplay("")
    postures.hidden = true

    details.classList.add("fade-in");
    await delay(2000);
    details.hidden = false;

    await delay(1000);
    proceed.classList.add("fade-in");
    proceed.hidden = false;
}


$(document).ready(function() {
    $('.btn-choice').click(function() {
        let choice = $(this).val();
        $.ajax({
            type: "POST",
            url: "/choose_zen",
            data: { zenChoice: choice },
            success: function(response) {
                document.getElementById("choices").hidden = true;
                infoDisplay("");
                if (response["choice"] == 'susokuKan') {
                    susokuKan();
                }
                else if (response["choice"] == 'shikantaza') {
                    shikantaza();
                }
                else {
                    console.log("Error: No choice furnished.")
                }
            },
            error: function(error) {
                console.error("Error: ", error);
            }
        });
    });
});

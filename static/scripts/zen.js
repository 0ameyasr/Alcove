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


function beginGame()
{
    const content = document.getElementById("contentHolder");
    const talk = document.getElementById("talk");
    const info = document.getElementById("info");
    const begin = document.getElementById("begin");
    const bar = document.getElementById("bar");

    content.style.background = 'transparent';

    const video = document.getElementById("gameVid");
    const source = document.getElementById("vidSrc");
    video.loop = true;
    video.playsinline = true;
    video.play();
    info.hidden = true;
    begin.hidden = true;
    talk.hidden = true;
    console.log("Zen Time")
}

async function susokuKan() {
    const details = document.getElementById("susokuKanDetails");
    const proceed = document.getElementById("begin");

    document.getElementById("taiko").play();
    infoDisplay("Susoku-Kan");
    
    await delay(5000);
    infoDisplay("");
    
    details.classList.add("fade-in");
    await delay(500);
    details.hidden = false;

    await delay(15000);
    proceed.classList.add("fade-in");
    proceed.hidden = false;
    details.hidden = true

}

async function shikantaza() {
    const details = document.getElementById("shikantazaDetails");
    const proceed = document.getElementById("begin");

    document.getElementById("taiko").play();
    infoDisplay("Shikantaza");

    await delay(5000);
    infoDisplay("");
    
    details.classList.add("fade-in");
    await delay(500);
    details.hidden = false;
    
    await delay(15000);
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
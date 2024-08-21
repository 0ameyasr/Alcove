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


    typewrite("Alcove","talk",0,fontColor);
    typewrite("Reflection Game","talk",3000,fontColor);
    setTimeout(()=>{
        talk.hidden = true;
        info.hidden = false;
        infoDisplay("To make this exercise as helpful as possible, be open to acknowledging your thoughts without judgement.");
    },6000);
    setTimeout(()=>{infoDisplay("This will only work as long as you are aware.");},9000);
    setTimeout(()=>{infoDisplay("You may speak to yourself or acknowledge your thoughts.");},14000);
    setTimeout(()=>{infoDisplay("'Knowing yourself is the beginning of all wisdom.' - Aristotle")},19000);
    setTimeout(()=>{infoDisplay("Arrange yourself, and focus.")},25000);
    setTimeout(()=>{
        infoDisplay("When you are ready, press 'Begin'")
        setInterval(()=>{},500);
        begin.hidden = false;
    },30000);
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

async function game() {
    const info = document.getElementById("info");
    const moodGrab = document.getElementById("question");
    const moodOptions = document.getElementById("questionOptions");

    info.hidden = false;
  
    infoDisplay("");

    await delay(1000);
    infoDisplay("Welcome.");
  
    await delay(6000);
    infoDisplay("To begin, take a deep breath in");
  
    await delay(500);
    updateProgressBar(4000, true);
  
    await delay(4500);
    infoDisplay("Now, hold your breath..");
  
    await delay(7500);
    infoDisplay("Slowly exhale.");
  
    await delay(500);
    updateProgressBar(8000, false);

    await delay(10000);
    infoDisplay("Repeat this exercise.");

    await delay(2000);
    infoDisplay("Again, inhale.");
  
    await delay(500);
    updateProgressBar(4000, true);
  
    await delay(4500);
    infoDisplay("Now, hold your breath..");
  
    await delay(7500);
    infoDisplay("And, slowly exhale.");
  
    await delay(500);
    updateProgressBar(8000, false);

    await delay(10000);
    infoDisplay("One last time.");

    await delay(2000);
    infoDisplay("Inhale.");
  
    await delay(500);
    updateProgressBar(4000, true);
  
    await delay(4500);
    infoDisplay("Hold your breath..");
  
    await delay(7500);
    infoDisplay("And... exhale.");
  
    await delay(500);
    updateProgressBar(8000, false);

    await delay(15000);
    infoDisplay("Make yourself comfortable.");

    await delay(5000);
    infoDisplay("Let's Begin.");

    await delay(3000);
    info.hidden = true;

    await delay(500);
    moodGrab.hidden = false;
    moodGrab.innerText="How are you feeling right now?"
    moodOptions.hidden = false;
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
    const now = new Date();
    const currentHour = now.getHours();

    const video = document.getElementById("gameVid");
    const source = document.getElementById("vidSrc");
    if (currentHour >= 18) {
        source.src = "/static/img/reflection_game.mp4";
        video.load();
        video.loop = true;
        video.playsinline = true;
        video.play();
    }
    video.loop = true;
    video.playsinline = true;
    video.play();
    info.hidden = true;
    begin.hidden = true;
    talk.hidden = true;
    game();
}

async function beginReflection(questionSet) {
    const info = document.getElementById("info");
    info.hidden = false;

    const slot = 120000;
    const q1 = questionSet[0];
    const q2 = questionSet[1];
    const q3 = questionSet[2];
    const q4 = questionSet[3];
    const q5 = questionSet[4];
    infoDisplay(q1)

    await delay(500);
    infoDisplay(q1);
    updateProgressBar(slot,false);

    await delay(slot+1000);
    infoDisplay(q2);
    updateProgressBar(slot,false);

    await delay(slot+1000);
    infoDisplay(q3);
    updateProgressBar(slot,false);

    await delay(slot+1000);
    infoDisplay(q4);
    updateProgressBar(slot,false);

    await delay(slot+1000);
    infoDisplay(q5);
    updateProgressBar(slot,false);

    await delay(slot+5000);
    infoDisplay("Now, collect your thoughts.");

    await delay(3000);
    infoDisplay("Observe the scene.");

    await delay(5000);
    infoDisplay("Leave whenever you want.");

    await delay(5000);
    info.hidden = true;
}

$(document).ready(function() {
    $('.mood-option').click(function() {
        let moodValue = $(this).val();
        const now = new Date();
        const currentHour = now.getHours();    
        let mode = "sun";
        if (currentHour >= 18) {
            mode = "moon";
        }
        $.ajax({
            type: "POST",
            url: "/influence_mood",
            data: { mood: moodValue, mode: mode},
            success: function(response) {
                document.getElementById('question').hidden = true;
                document.getElementById('questionOptions').hidden = true;
                beginReflection(response.questionSet)
            },
            error: function(error) {
                console.error("Error: ", error);
            }
        });
    });
});
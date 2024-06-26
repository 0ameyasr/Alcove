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


    // typewrite("bored.ai","talk",0,fontColor);
    // typewrite("Reflection Game","talk",3000,fontColor);
    // setTimeout(()=>{
    //     talk.hidden = true;
    //     info.hidden = false;
    //     infoDisplay("To make this exercise as helpful as possible, be open to acknowledging your thoughts without judgement.");
    // },6000);
    // setTimeout(()=>{infoDisplay("This will only work as long as you are aware.");},9000);
    // setTimeout(()=>{infoDisplay("You may speak to yourself or acknowledge your thoughts.");},14000);
    // setTimeout(()=>{infoDisplay("'Knowing yourself is the beginning of all wisdom.' - Aristotle")},19000);
    // setTimeout(()=>{infoDisplay("Arrange yourself, and focus.")},25000);
    setTimeout(()=>{
        infoDisplay("When you are ready, press 'Begin'")
        setInterval(()=>{},500);
        begin.hidden = false;
    },1000);
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

    await delay(10000);
    infoDisplay("Feeling better?");
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
    video.loop = true;
    video.play();
    info.hidden = true;
    begin.hidden = true;
    talk.hidden = true;
    game();
}

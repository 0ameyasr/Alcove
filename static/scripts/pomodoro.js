let worker;
let timeLeft = 25 * 60;
let isRunning = false;
let duration = 25;
let isBreak = false;
let breakDuration = 5;

const timerDisplay = document.getElementById('timerDisplay');
const startBtn = document.getElementById('startBtn');
const breakBtn = document.getElementById('breakBtn');
const resetBtn = document.getElementById('resetBtn');
const btn25 = document.getElementById('btn25');
const btn50 = document.getElementById('btn50');
const startAudio = document.getElementById('start');
const alarmAudio = document.getElementById('alarm');

function updateDisplay() {
    const minutes = Math.floor(timeLeft / 60);
    const seconds = timeLeft % 60;
    const timeString = `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
    timerDisplay.textContent = timeString;
    
    const status = isBreak ? 'Break' : 'Pomodoro';
    document.title = `${timeString} - ${status} | bored.ai`;
}

function startTimer() {
    if (!isRunning) {
        isRunning = true;
        startBtn.disabled = true;
        breakBtn.disabled = true;
        btn25.disabled = true;
        btn50.disabled = true;
        startAudio.play();

        if (typeof(Worker) !== "undefined") {
            if (typeof(worker) == "undefined") {
                worker = new Worker("static/scripts/pomodoroWorker.js");
            }
            worker.postMessage({
                action: 'start',
                duration: timeLeft,
                isBreak: isBreak
            });
            worker.onmessage = function(e) {
                timeLeft = e.data.timeLeft;
                updateDisplay();
                if (timeLeft === 0) {
                    timerEnded();
                }
            };
        } else {
            console.log("Web Workers are not supported in your browser.");
        }
    }
}

function timerEnded() {
    isRunning = false;
    startBtn.disabled = false;
    breakBtn.disabled = false;
    btn25.disabled = false;
    btn50.disabled = false;
    alarmAudio.play();
    if (isBreak) {
        resetTimer();
    } else {
        startBreak();
    }
}

function startBreak() {
    isBreak = true;
    breakDuration = duration === 25 ? 5 : 10;
    timeLeft = breakDuration * 60;
    updateDisplay();
    startBtn.innerHTML = '<i class="fa-solid fa-play"></i>';
    breakBtn.disabled = true;
    startTimer();
}

function resetTimer() {
    if (worker) {
        worker.postMessage({action: 'stop'});
    }
    isRunning = false;
    isBreak = false;
    timeLeft = duration * 60;
    updateDisplay();
    startBtn.innerHTML = '<i class="fa-solid fa-play"></i>';
    startBtn.disabled = false;
    breakBtn.disabled = true;
    btn25.disabled = false;
    btn50.disabled = false;
}

function setDuration(minutes) {
    if (!isRunning) {
        duration = minutes;
        resetTimer();
    }
}

startBtn.addEventListener('click', startTimer);
breakBtn.addEventListener('click', startBreak);
resetBtn.addEventListener('click', resetTimer);

btn25.addEventListener('change', function() {
    if (this.checked) {
        setDuration(25);
    }
});

btn50.addEventListener('change', function() {
    if (this.checked) {
        setDuration(50);
    }
});


var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
  return new bootstrap.Tooltip(tooltipTriggerEl)
})


updateDisplay();
breakBtn.disabled = true;

$(document).ready(function () {
    $("#quickChat").on("submit", function (event) {
        event.preventDefault();
        var msg = $("#userMessageQuick").val();
        $("#userMessageQuick").prop("disabled", true);
        $("#askButton").prop("disabled", true);
        $("#aceResponseQuick").html('');
        $("#spinner").show();
        $.ajax({
            type: "POST",
            url: "/chat_ace",
            data: { message: msg },
            dataType: "json",
            success: function (response) {
                $("#aceResponseQuick").html(response.talk);
                $("#userMessageQuick").val('');
                hljs.highlightAll();
            },
            complete: function () {
                $("#userMessageQuick").prop("disabled", false);
                $("#askButton").prop("disabled", false);
                $("#spinner").hide();
            }
        });
    });
});

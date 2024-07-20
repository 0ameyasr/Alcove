let timer;
let endTime;
let isBreak = false;
let duration;

self.onmessage = function(e) {
    if (e.data.action === 'start') {
        endTime = Date.now() + e.data.duration * 1000;
        duration = e.data.duration;
        isBreak = e.data.isBreak;
        clearInterval(timer);
        timer = setInterval(updateTimer, 100);
    } else if (e.data.action === 'stop') {
        clearInterval(timer);
    }
};

function updateTimer() {
    let timeLeft = Math.max(0, Math.floor((endTime - Date.now()) / 1000));
    self.postMessage({ timeLeft: timeLeft, isBreak: isBreak });
    
    if (timeLeft === 0) {
        clearInterval(timer);
    }
}
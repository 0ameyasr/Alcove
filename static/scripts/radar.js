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
    const maxWords = 50;

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

    const questionElement = document.getElementById("question");
    const progressBar = document.getElementById("progressBar");
    let changeCount = 0;

    const observer = new MutationObserver(function(mutations) {
        mutations.forEach(function(mutation) {
            if (mutation.type === "childList") {
                changeCount++;
                updateProgressBar();
            }
        });
    });

    observer.observe(questionElement, { childList: true });

    function updateProgressBar() {
        if (changeCount <= 16) {
            const progressPercentage = (changeCount / 16) * 100;
            progressBar.style.width = progressPercentage + "%";
            progressBar.setAttribute("aria-valuenow", changeCount);
        }
    }
});

function analyze(score, verdict, concerns) {
    const analysis = document.getElementById('analysis');
    const concernsDiv = document.getElementById('concernsDiv');
    const concernsPar = document.getElementById('concerns');

    const data = {}

    $.ajax({
        type: "POST",
        url: "/get_radar_analysis",
        contentType: "application/json",
        data: JSON.stringify(data),
        dataType: "json",
        success: function (response) {
            analysis.classList.add("fade-in");
            analysis.hidden = false;
            analysis.innerText = response.analysis;

            document.getElementById('title').innerText = response.title;
            document.getElementById('analysisContainer').hidden = false;

            concernsDiv.classList.add('fade-in');
            concernsPar.innerText = concerns;
            concernsDiv.hidden = false;

            const ctx = document.getElementById("combinedDoughnutChart");

            if (window.radarChartInstance) {
                window.radarChartInstance.destroy();
            }

            window.radarChartInstance = new Chart(ctx, {
                type: 'radar',
                data: {
                    labels: ["Sleep", "Depression", "Abnormal", "Anxiety"],
                    datasets: [{
                        label: "Your Mental Health Radar",
                        data: [
                            response.scores.pSleep,
                            response.scores.pDepression,
                            response.scores.pAbnormal,
                            response.scores.pAnxiety
                        ],
                        fill: true,
                        backgroundColor: "rgba(54, 162, 235, 0.2)",
                        borderColor: "rgba(54, 162, 235, 1)",
                        pointBackgroundColor: "rgba(54, 162, 235, 1)",
                        pointBorderColor: "#fff",
                        pointHoverBackgroundColor: "#fff",
                        pointHoverBorderColor: "rgba(54, 162, 235, 1)"
                    }]
                },
                options: {
                    responsive: true,
                    scales: {
                        r: {
                            suggestedMin: 0,
                            suggestedMax: 100,
                            angleLines: { color: "#aaa" },
                            grid: { color: "#ddd" },
                            pointLabels: { color: "#333", font: { size: 14 } }
                        }
                    }
                }
            });
        },
        error: function (error) {
            alert("Error occurred: " + error.responseText);
        }
    });
}


$('#radarForm').submit(function (e) {
    e.preventDefault();
    const resp = $('#radarResponse').val();
    const wordCountDisplay = document.getElementById("wordCount");
    $.ajax({
        type: "POST",
        url: "/radar_response",
        data: {response: resp},
        dataType: "json",
        success: function (response) {
            document.getElementById("pingAudio").play();
            $('#radarResponse').val('');
            if (response.status === 1) {
                console.log(response)
                document.getElementById('interactPane').hidden = true;
                analyze(response.score,response.verdict,response.concerns)
            }
            document.getElementById("question").innerText = response.question;
            wordCountDisplay.textContent = `Remaining words: 50`;
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
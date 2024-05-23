window.onload = function () {
    const fontColor = "#31363f";
    const questionList = document.getElementById("questions");
    const surveyForm = document.getElementById("surveyForm");
    const text = document.getElementById("talk");
    const introBody = document.getElementById("intro");

    const messages = [
        "Care for a quick survey?"
    ];

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
    
    typewrite(messages[0], "talk", 1000, fontColor)
    setTimeout(() => { introBody.hidden = true; text.hidden = true; questionList.hidden = false; surveyForm.hidden = false; }, 4500)
}

document.addEventListener("DOMContentLoaded", () => {
    const q1_list = document.getElementsByName("q1");
    const q2_list = document.getElementsByName("q2");
    const q3_list = document.getElementsByName("q3");
    const q4_list = document.getElementsByName("q4");
    const q5_list = document.getElementsByName("q5");

    const submit_button = document.getElementById("survey-submit-button");
    let values = [];
    let q1_c = false;
    let q2_c = false;
    let q3_c = false;
    let q4_c = false;
    let q5_c = false;

    const checkQuestions = () => {
        let survey_filled = q1_c && q2_c && q3_c && q4_c && q5_c;
        submit_button.disabled = !survey_filled;
    }

    const handleRadioChange = (questionList, index) => {
        for (let i = 0; i < questionList.length; i++) {
            if (questionList[i].checked) {
                values[index] = questionList[i].value;
                switch (index) {
                    case 0: q1_c = true; break;
                    case 1: q2_c = true; break;
                    case 2: q3_c = true; break;
                    case 3: q4_c = true; break;
                    case 4: q5_c = true; break;
                }
                break;
            }
        }
        checkQuestions();
    }

    q1_list.forEach(radio => radio.addEventListener('change', () => handleRadioChange(q1_list, 0)));
    q2_list.forEach(radio => radio.addEventListener('change', () => handleRadioChange(q2_list, 1)));
    q3_list.forEach(radio => radio.addEventListener('change', () => handleRadioChange(q3_list, 2)));
    q4_list.forEach(radio => radio.addEventListener('change', () => handleRadioChange(q4_list, 3)));
    q5_list.forEach(radio => radio.addEventListener('change', () => handleRadioChange(q5_list, 4)));
});
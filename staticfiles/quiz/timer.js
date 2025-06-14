document.addEventListener('DOMContentLoaded', function(){
    let timeLeft= parseInt(document.getElementById('timer').dataset.timeLimit); //Get time from data attributes
    const timerDisplay = document.getElementById('timer');
    const quizForm = document.querySelector('form');

    function updateTimer(){
        if (timeLeft <= 0){
            timerDisplay.textContent = "Time's up!";
            quizForm.submit();
        }else{
            const minutes = Math.floor(timeLeft/60);
            const seconds = timeLeft % 60;
            timerDisplay.textContent = `Time Left: ${minutes}:${seconds.toString().padStart(2,'0')}`;
            timeLeft--;
            setTimeout(updateTimer, 1000);
        }
    }
    updateTimer();
})
// ================================
// MARVEL × GFG EVENT WEBSITE
// JAVASCRIPT
// ================================


// COUNTDOWN TIMER
// Change this date when the actual event date is announced.

const eventDate = new Date("December 31, 2026 18:00:00").getTime();

const countdown = setInterval(function () {

    const now = new Date().getTime();

    const difference = eventDate - now;

    if (difference <= 0) {
        clearInterval(countdown);

        document.getElementById("days").innerText = "00";
        document.getElementById("hours").innerText = "00";
        document.getElementById("minutes").innerText = "00";
        document.getElementById("seconds").innerText = "00";

        return;
    }

    const days = Math.floor(
        difference / (1000 * 60 * 60 * 24)
    );

    const hours = Math.floor(
        (difference / (1000 * 60 * 60)) % 24
    );

    const minutes = Math.floor(
        (difference / (1000 * 60)) % 60
    );

    const seconds = Math.floor(
        (difference / 1000) % 60
    );


    document.getElementById("days").innerText =
        String(days).padStart(2, "0");

    document.getElementById("hours").innerText =
        String(hours).padStart(2, "0");

    document.getElementById("minutes").innerText =
        String(minutes).padStart(2, "0");

    document.getElementById("seconds").innerText =
        String(seconds).padStart(2, "0");

}, 1000);


// REGISTER BUTTON

function registerUser() {

    alert(
        "⚡ Mission accepted!\n\nRegistration details will be announced soon."
    );

}
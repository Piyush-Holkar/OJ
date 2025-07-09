const canvas = document.getElementById("starfield");
const ctx = canvas.getContext("2d");

canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

let stars = [];

for (let i = 0; i < 1000; i++) {
    stars.push({
        x: Math.random() * canvas.width,
        y: Math.random() * canvas.height,
        radius: Math.random() * 1.5,
        speed: Math.random() * 0.5 + 0.2
    });
}

function drawStars() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.fillStyle = "white";
    stars.forEach(star => {
        ctx.beginPath();
        ctx.arc(star.x, star.y, star.radius, 0, Math.PI * 2);
        ctx.fill();
    });
}

function moveStars() {
    stars.forEach(star => {
        star.y += star.speed;
        if (star.y > canvas.height) {
            star.y = 0;
            star.x = Math.random() * canvas.width;
        }
    });
}

function animate() {
    drawStars();
    moveStars();
    requestAnimationFrame(animate);
}

animate();

document.addEventListener("DOMContentLoaded", function () {
    new Typed("#typed-text", {
        strings: [
            "Debug the unknown.",
            "Conquer DSA with missions.",
            "Each mission, different situations.",
            "Let the Universe judge your code!",
            "Launch solutions beyond the stars.",
            "Compete on Cosmic Levels",
        ],
        typeSpeed: 50,
        backSpeed: 30,
        backDelay: 1000,
        loop: true
    });
});

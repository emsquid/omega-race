const canvas = document.getElementById("fond")
const ctx = canvas.getContext("2d")

const random = (min, max) => {
    return Math.random() * (max - min) + min
}

const createStar = (x, y, speed) => {
    return { x: x, y: y, speed: speed }
}

const updateStar = (star) => {
    star.y -= star.speed
    if (star.y < 0) {
        star.x = random(0, 100)
        star.y = 100
    }
}

const drawStar = (star) => {
    ctx.fillStyle = "white"
    ctx.fillRect(star.x * canvas.clientWidth / 100, star.y * canvas.clientHeight / 100, 1, 1)
}

const storeStars = (stars) => {
    const infos = []
    for (let i = 0; i < 128; i++) {
        infos.push({ x: stars[i].x, y: stars[i].y, speed: stars[i].speed })
    }
    sessionStorage.stars = JSON.stringify(infos)
}

const stars = []
var stored = sessionStorage.stars

if (stored === undefined) {
    for (let i = 0; i < 128; i++) {
        stars.push(createStar(random(0, 100), random(0, 100), random(0, 0.05)))
    }
} else {
    stored = JSON.parse(stored)
    for (let i = 0; i < 128; i++) {
        stars.push(stored[i])
    }
}


window.onbeforeunload = () => { storeStars(stars) }

setInterval(() => {
    canvas.width = window.innerWidth
    canvas.height = window.innerHeight
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    for (let i = 0; i < 128; i++) {
        drawStar(stars[i])
        updateStar(stars[i])
    }
}, 10)

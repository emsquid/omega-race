const random = (min, max) => {
    return Math.random() * (max - min) + min
}

const createStar = (x, y, speed) => {
    const star = document.createElement("div")
    document.body.appendChild(star)
    star.classList.add("star")
    star.style.zIndex = -1
    star.style.width = "1px"
    star.style.height = "1px"
    star.style.position = "fixed"
    star.style.backgroundColor = "white"
    return { div: star, x: x, y: y, speed: speed }
}

const updateStar = (star) => {
    star.y -= star.speed
    if (star.y < 0) {
        star.x = random(0, 100)
        star.y = 100
        star.speed = random(0, 0.05)
    }
    star.div.style.left = `${star.x}%`
    star.div.style.top = `${star.y}%`
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
        const x = stored[i].x
        const y = stored[i].y
        const speed = stored[i].speed
        stars.push(createStar(x, y, speed))
    }
}

window.onbeforeunload = () => { storeStars(stars) }

setInterval(() => {
    for (let i = 0; i < 128; i++) {
        updateStar(stars[i])
    }
}, 10)

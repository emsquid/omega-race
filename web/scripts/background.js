const random = (min, max) => {
    return Math.random() * (max - min) + min
}

const createStar = () => {
    const star = document.createElement("div")
    document.body.appendChild(star)
    star.classList.add("star")
    star.style.zIndex = -1
    star.style.width = "1px"
    star.style.height = "1px"
    star.style.position = "fixed"
    star.style.backgroundColor = "white"
    return { div: star, x: random(0, 100), y: random(0, 100), speed: random(0, 0.05) }
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

const stars = []

for (let i = 0; i < 128; i++) {
    stars.push(createStar())
}

setInterval(() => {
    for (let i = 0; i < 128; i++) {
        updateStar(stars[i])
    }
}, 10)

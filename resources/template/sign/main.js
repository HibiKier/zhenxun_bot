let wdDom = document.querySelector(".wd")

let wd = Math.floor(Math.random() * 40) + 1

wdDom.innerHTML = wd + "℃"

let weatherDom = document.querySelector(".weather-img")

let r = Math.floor(Math.random() * 12)

weatherDom.src = "res/img/weather/" + r + ".png"

let qianDom = document.querySelector(".qian")

let r1 = Math.floor(Math.random() * 6)

qianDom.src = "res/img/tag/" + r1 + ".png"

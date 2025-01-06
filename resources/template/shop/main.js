const leftElements = document.getElementsByClassName("shop-item-left")
const rightElements = document.getElementsByClassName("shop-item-right")

const defaultList = [
  "1.png",
  "2.png",
  "3.png",
  "4.png",
  "5.png",
  "qq.png",
  "xx1.png",
  "xx2.png",
]

const leftRightImgList = ["1.png", "2.png", "3.png", "4.png", "5.png"]

const leftRightImgList2 = ["qq.png", "xx1.png", "xx2.png"]

var leftRightImg = null
var leftRightImg2 = null

function randomImg() {
  const randomIndex = Math.floor(Math.random() * leftRightImgList.length)
  const randImg = leftRightImgList[randomIndex]
  if (leftRightImg == randImg) {
    return randomImg()
  }
  leftRightImg = randImg
  return randImg
}

function randomImg2() {
  const randomIndex = Math.floor(Math.random() * leftRightImgList2.length)
  const randImg = leftRightImgList2[randomIndex]
  if (leftRightImg == randImg) {
    return randomImg2()
  }
  leftRightImg2 = randImg
  return randImg
}

function getRandomInt(min, max) {
  const mathMin = Math.ceil(min)
  const mathMax = Math.floor(max)
  return Math.floor(Math.random() * (mathMax - mathMin + 1)) + mathMin
}

function createImgElement(is_qq, is_left, start_height, height) {
  const imgElement = document.createElement("img")
  const className = is_left ? "left-img" : "right-img"
  if (is_qq) {
    imgElement.className = "shop-item-left-qq " + className
    imgElement.src = "./res/img/left_right/" + randomImg2()
    imgElement.style.top = getRandomInt(start_height, height - 20) + "px"
    if (is_left) {
      imgElement.style.left = getRandomInt(10, 40) + "px"
    } else {
      imgElement.style.right = getRandomInt(10, 40) + "px"
    }
    imgElement.style.height = getRandomInt(80, 120) + "px"
    imgElement.style.transform = "rotate(" + getRandomInt(0, 45) + "deg)"
  } else {
    imgElement.className = "shop-item-right-zx " + className
    imgElement.src = "./res/img/left_right/" + randomImg()
    imgElement.style.top = getRandomInt(start_height, height - 20) + "px"
  }

  return imgElement
}

function getTop(dom) {
  return parseInt(dom.style.top.slice(0, -2))
}

const randomIndex = Math.floor(Math.random() * defaultList.length)
const leftImg = defaultList[randomIndex]

var start = true

if (["qq.png", "xx1.png", "xx2.png"].includes(leftImg)) {
  start = true
} else {
  start = false
}

for (let i = 0; i < leftElements.length; i++) {
  leftHeight = leftElements[i].offsetHeight

  if (leftHeight <= 1000) {
    // 长度不够，只增加一个
    if (start) {
      leftElements[i].appendChild(
        createImgElement(true, true, 20, leftHeight - 50)
      )
      rightElements[i].appendChild(createImgElement(false, false, 10, 60))
    } else {
      leftElements[i].appendChild(createImgElement(false, true, 10, 60))
      rightElements[i].appendChild(
        createImgElement(true, false, 20, leftHeight - 50)
      )
    }
  } else {
    // 先添加一个气球
    const firstDom = createImgElement(true, true, 20, 200)
    leftElements[i].appendChild(firstDom)
    let startHeight = 100 + getTop(firstDom)
    let endHeight = 300 + getTop(firstDom)
    let firstIsQq = false
    let inx = 0
    while (leftHeight - endHeight >= 200) {
      // 避免过多重复
      rand = Math.random()
      if (inx >= 2) {
        rand = 0.4
        inx = 0
      }
      if (inx <= -1) {
        rand = 0.6
        inx = 0
      }
      // 真寻和气球随机加
      if (rand > 0.5) {
        firstIsQq = true
        inx += 1
        const imgDom = createImgElement(true, true, startHeight, endHeight)
        leftElements[i].appendChild(imgDom)
        startHeight = getRandomInt(250, 350) + getTop(imgDom)
        endHeight = getRandomInt(450, 500) + getTop(imgDom)
      } else {
        if (leftHeight - startHeight < 700) {
          continue
        }
        inx -= 1
        const imgDom = createImgElement(false, true, startHeight, endHeight)
        leftElements[i].appendChild(imgDom)
        startHeight = getRandomInt(400, 700) + getTop(imgDom)
        endHeight = getRandomInt(600, 900) + getTop(imgDom)
        if (leftHeight - startHeight < 900) {
          break
        }
      }
    }
    startHeight = 10
    endHeight = 200
    inx = 0
    while (leftHeight - endHeight >= 200) {
      // 真寻和气球随机加
      rand = Math.random()
      if (rand > 0.5 && firstIsQq) {
        firstIsQq = false
        rand = 0.4
      }
      // 避免过多重复
      if (inx >= 2) {
        rand = 0.4
        inx = 0
      }
      if (inx <= -1) {
        rand = 0.6
        inx = 0
      }

      if (rand > 0.5) {
        inx += 1
        const imgDom = createImgElement(true, false, startHeight, endHeight)
        rightElements[i].appendChild(imgDom)
        startHeight = getRandomInt(250, 350) + getTop(imgDom)
        endHeight = getRandomInt(450, 500) + getTop(imgDom)
      } else {
        if (leftHeight - startHeight < 700) {
          continue
        }
        inx -= 1
        const imgDom = createImgElement(false, false, startHeight, endHeight)
        rightElements[i].appendChild(imgDom)
        startHeight = getRandomInt(400, 700) + getTop(imgDom)
        endHeight = getRandomInt(600, 900) + getTop(imgDom)
      }
    }
  }

  start = !start
}

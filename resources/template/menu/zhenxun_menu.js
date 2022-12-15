let color = {
    "color":[
        "#eea2a4",
        "#621d34",
        "#e0c8d1",
        "#8b2671",
        "#142334",
        "#2b73af",
        "#93b5cf",
        "#2474b5",
        "#baccd9",
        "#1781b5",
        "#5cb3cc",
        "#57c3c2",
        "#1ba784",
        "#92b3a5",
        "#2bae85",
        "#83cbac",
        "#41ae3c",
        "#d0deaa",
        "#d2b42c",
        "#d2b116",
        "#f8df72",
        "#645822",
        "#ddc871",
        "#f9d770",
        "#d9a40e",
        "#b78b26",
        "#5d3d21",
        "#f8b37f",
        "#945833",
        "#e8b49a",
        "#a6522c",
        "#8b614d",
        "#f68c60",
        "#f6cec1",
        "#eeaa9c",
        "#862617",
        "#f2b9b2",
        "#f1908c"
    ]
};

let colorlist = color.color;
let logoArr = Array.from(Array(24), (v,k) =>k+1);

let fatherDom = document.querySelector(".content");

let childDom = fatherDom.children;

//瀑布流列数统计
let columnCount = 0;
//首列为最长列的情况下，作为被除数
let firstColumnNum = childDom[0].childElementCount;



for(let i = 0 ;i < childDom.length ;i++){
    // 随机取颜色
    let index = Math.floor((Math.random()*colorlist.length));
    let themecolor = colorlist[index];
    colorlist.splice(index, 1);
    let colorStr = `--themebordercolor:${themecolor};--themebgcolor:${themecolor+'0a'};--pluginbgcolor:${themecolor+'5c'};`;
    childDom[i].setAttribute('style',colorStr);
    //固定图标
    let iconDom = childDom[i].querySelector("i");
    let plugin_type = childDom[i].querySelector("span").textContent;

    if(plugin_type == "功能")iconDom.classList.add("fa-cog");
    else if (plugin_type == "原神相关")iconDom.classList.add("fa-circle-o");
    else if (plugin_type == "联系管理员")iconDom.classList.add("fa-envelope-o");
    else if (plugin_type == "常规插件")iconDom.classList.add("fa-cubes");
    else if (plugin_type == "抽卡相关")iconDom.classList.add("fa-credit-card-alt");
    else if (plugin_type == "来点好康的")iconDom.classList.add("fa-picture-o");
    else if (plugin_type == "数据统计")iconDom.classList.add("fa-bar-chart");
    else if (plugin_type == "一些工具")iconDom.classList.add("fa-scissors");
    else if (plugin_type == "商店")iconDom.classList.add("fa-shopping-cart");
    else if (plugin_type == "其它")iconDom.classList.add("fa-tags");
    else if (plugin_type == "群内小游戏")iconDom.classList.add("fa-gamepad");
    else iconDom.classList.add("fa-pencil-square-o");

    //添加真寻元素
    let imgDom = childDom[i].querySelector("img");
    let logoIndex = Math.floor((Math.random()*logoArr.length));
    let logoUrl = `./res/logo/${logoArr[logoIndex]}.png`;
    logoArr.splice(logoIndex, 1);
    imgDom.src=logoUrl;

    //暂时把所有的插件数量写入到列数中
    columnCount += childDom[i].childElementCount
}

//计算瀑布流列数
columnCount = Math.ceil(columnCount / firstColumnNum) < 5 ? Math.ceil(columnCount / firstColumnNum) : 4;
//修改瀑布流列数
if(columnCount != 4){
    fatherDom.style.columnCount = columnCount;
}

// define default language to use
const defaultLang = 'english'

// load language files
let french = loadMap("/lang/french.json");
let english = loadMap("/lang/english.json");

// get current language
var curLang = getLang();
// manage handler nastily
var received = 0;

// build translation maps
const translations = new Map().set('english', english).set('french', french);
const flags = new Map().set('french', 'english.jpg').set('english', 'french.jpg');

// build sidenav on mobile
$(document).ready(function(){
    $('.sidenav').sidenav();
});

// manually closing the sidenav
function closeSidenav() {
    $('.sidenav').sidenav().style.width = '0px';
}

// used to automatically close sidenav on translate
function translateContentAndQuit() {
    translateContent();
    // it's not that "pretty"
    // closeSidenav();
}

// retrieve current languages from GET, or use default value
function getLang() {
    var tmp = getParameter('lang');
    if (tmp == null) {
        return defaultLang;
    } else {
        return tmp;
    }
}

// switch language
function changeLang(lang) {
    return (lang === 'english') ? 'french': 'english';
}

// translate the content of the actual page, using placeholders
function translateContent() {
    curLang = changeLang(curLang);
    translateAll(curLang);
}

function translateAll(newLang) {
    const elementsToTranslate = document.querySelectorAll('[data-translate]');
    for (const element of elementsToTranslate) {
        const myId = element.getAttribute('id')
        var translation = translations.get(newLang).get(myId);
        if (translation != null) element.innerText = translation;
    }
    translateLinks(newLang);
    translateImage(newLang);
}

function translateImage(newLang) {
    const flagsToTranslate = document.querySelectorAll('[img-translate]');
    for (const flag of flagsToTranslate) {
        flag.src = "images/" + flags.get(newLang);
    }
}

function translateLinks(newLang) {
    const elementsToTranslate = document.querySelectorAll('[data-translate]');
    const oldLang = changeLang(newLang)
    for (const element of elementsToTranslate) {
        if (element.href != null & element.href != "") {
            if (element.href.includes("?lang")) {
                element.href = element.href.replace("?lang=" + oldLang, "?lang=" + newLang)
            } else {
                element.href = element.href + "?lang=" + newLang
            }
        }
    }
}

// load a configuration map from a JSON file
// use a cb to reload page after file was loaded
function loadMap(file) {
    var map = new Map()
    $.getJSON(file, function(json) {
        $.each(json, function (key, value) {
            map.set(key, value)
        });
    }).done(onLoad);
    return map;
}

function onLoad() {
    translateAll(curLang);
}

// retrieve a GET parameter
function getParameter(key) {
    address = window.location.search
    parameterList = new URLSearchParams(address)
    return parameterList.get(key)
}

function setCollapse() {
    var btn = document
        .getElementsByClassName("collapse");

    for (let i = 0; i < btn.length; i++) {
        btn[i].addEventListener("click", function () {
            var content = this.nextSibling;
            do {
                if (!content) {
                    return;
                }
                content = content.nextSibling;
                if (!content) {
                    return;
                }
            } while (content.className != "toCollapse");
            this.classList.toggle("active");
            if (content.style.display === "block") {
                content.style.display = "none";
            } else {
                content.style.display = "block";
            }
        });
    }
}

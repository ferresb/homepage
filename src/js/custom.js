// load language files
let french = loadMap("/lang/french.json", loader);
let english = loadMap("/lang/english.json", loader);

// get current language
var curLang = getLang();
// manage handler nastily
var received = 0;

// build translation maps
const translations = new Map().set('english', english).set('french', french);
const flags = new Map().set('french', 'english.jpg').set('english', 'france.jpg');

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

// retrieve current languages from GET, or define it to english as it will be translated once on loading
function getLang() {
    var tmp = getParameter('lang');
    if (tmp == null) {
        return 'english';
    } else {
        return changeLang(tmp);
    }
}

// switch language
function changeLang(lang) {
    return (lang === 'english') ? 'french': 'english';
}

// translate the content of the actual page, using placeholders
function translateContent() {
    const flagsToTranslate = document.querySelectorAll('[img-translate]');
    const elementsToTranslate = document.querySelectorAll('[data-translate]');

    const oldLang = curLang;
    curLang = changeLang(curLang)

    for (const element of elementsToTranslate) {
        const myId = element.getAttribute('id')
        var translation = translations.get(curLang).get(myId);
        if (translation != null) element.innerText = translation
        if (element.href != null & element.href != "") {
            if (element.href.includes("?lang")) {
                element.href = element.href.replace("?lang=" + oldLang, "?lang=" + curLang)
            } else {
                element.href = element.href + "?lang=" + curLang
            }
        }
    }
    for (const flag of flagsToTranslate) {
        flag.src = "images/" + flags.get(curLang);
    }
}

// load a configuration map from a JSON file
// use a cb to reload page after file was loaded
function loadMap(file, cb) {
    var map = new Map()
    $.getJSON(file, function(json) {
        $.each(json, function (key, value) {
            map.set(key, value)
        });
    }).done(cb);
    return map;
}

// small wrapper to force reload on content loading
function loader() {
    received++;
    if (received >= 2) {
        translateContent()
    }
}

// retrieve a GET parameter
function getParameter(key) {
    address = window.location.search
    parameterList = new URLSearchParams(address)
    return parameterList.get(key)
}

let fr = loadMap("/lang/france.json", loader)
let en = loadMap("/lang/english.json", loader)

const translations = new Map().set('en', en).set('fr', fr);
const flags = new Map().set('fr', 'english.jpg').set('en', 'france.jpg');

function getLang() {
    var tmp = getParameter('lang');
    if (tmp == null) {
        return 'en';
    } else {
        return changeLang(tmp);
    }
}

var curLang = getLang()
var received = 0;

function changeLang(lang) {
    return (lang === 'en') ? 'fr': 'en';
}

function translate() {
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
                element.href = element.href.replace(oldLang, curLang)
            } else {
                element.href = element.href + "?lang=" + curLang
            }
        }
    }
    for (const flag of flagsToTranslate) {
        flag.src = "images/" + flags.get(curLang);
    }
}

function loadMap(file, cb) {
    var map = new Map()
    $.getJSON(file, function(json) {
        $.each(json, function (key, value) {
            map.set(key, value)
        });
    }).done(cb);
    return map;
}

function loader() {
    received++;
    if (received >= 2) {
        translate()
    }
}

function getParameter(key) {
    address = window.location.search
    parameterList = new URLSearchParams(address)
    return parameterList.get(key)
}

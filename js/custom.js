let fr = loadMap("/lang/france.json", loader)
let en = loadMap("/lang/english.json", loader)

const translations = new Map().set('en', en).set('fr', fr);
const flags = new Map().set('fr', 'english.jpg').set('en', 'france.jpg');

const languages = ['fr', 'en']; 
var curLang = 1;
var received = 0;

function translate() {
    const flagsToTranslate = document.querySelectorAll('[img-translate]');
    const elementsToTranslate = document.querySelectorAll('[data-translate]');

    curLang = (curLang === 0) ? 1: 0;

    for (const element of elementsToTranslate) {
        element.innerText = translations.get(languages[curLang]).get(element.getAttribute('id'));
    }
    for (const flag of flagsToTranslate) {
        flag.src = "images/" + flags.get(languages[curLang]);
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

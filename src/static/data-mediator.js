// Übersetzen von JS zu Python und umgekehrt via JSON
// noch nicht fertig!!!
// am besten die Quelle auschecken
// QUELLE: https://healeycodes.com/javascript/python/beginners/webdev/2019/04/11/talking-between-languages.html
// Beziehungen: BaseModel in models.py, /mediator in _init_.py

// GET is the default method, so we don't need to set it

fetch('/mediator')
    .then(function (response) {
      return response.json(); // But parse it as JSON this time
    })
    .then(function (json) {
      console.log('GET response as JSON:');
      console.log(json); // Here’s our JSON object
      const obj = JSON.parse(json)
      return obj
    })
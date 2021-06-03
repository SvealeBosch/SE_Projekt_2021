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
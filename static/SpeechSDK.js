  // status fields and start button in UI
  var phraseDiv;
  var startSpeakTextAsyncButton;

  // subscription key and region for speech services.
  var subscriptionKey, serviceRegion;
  var SpeechSDK;
  var synthesizer;

  document.addEventListener("DOMContentLoaded", function () {
    startSpeakTextAsyncButton = document.getElementById("startSpeakTextAsyncButton");
    // TTs Free
    subscriptionKey = '8ea4859aee134fc5b85f562dd62936ce';
    serviceRegion = 'westus';
    phraseDiv = document.getElementById("phraseDiv");
    
    startSpeakTextAsyncButton.addEventListener("click", function () {
      startSpeakTextAsyncButton.disabled = true;
      phraseDiv.innerHTML = "";
      
      var speechConfig = SpeechSDK.SpeechConfig.fromSubscription(subscriptionKey, serviceRegion);
      synthesizer = new SpeechSDK.SpeechSynthesizer(speechConfig);
    
      let inputText = phraseDiv.value;
      synthesizer.speakTextAsync(
        inputText,
      
        function (result) {
          startSpeakTextAsyncButton.disabled = false;
          window.console.log(result);
          synthesizer.close();
          synthesizer = undefined;
        },
        function (err) {
          startSpeakTextAsyncButton.disabled = false;
          window.console.log(err);
          //alert(serviceRegion);
          synthesizer.close();
          synthesizer = undefined;
      });
    });
  
    if (!!window.SpeechSDK) {
      SpeechSDK = window.SpeechSDK;
      startSpeakTextAsyncButton.disabled = false;
      // in case we have a function for getting an authorization token, call it.
      if (typeof RequestAuthorizationToken === "function") {
      }
    }
  });
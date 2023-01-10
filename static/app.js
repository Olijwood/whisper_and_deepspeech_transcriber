function uploadFile(form)
{
 
  const formData = new FormData(form);
 var oOutput = document.getElementById("static_file_response")
 var dOutput = document.getElementById("deepspeech_transcription")
 var oReq = new XMLHttpRequest();
     oReq.open("POST", "upload_static_file", true);
 oReq.onload = function(oEvent) {
     if (oReq.status == 200) {
       json = JSON.parse(oReq.response)
       oOutput.innerHTML = json.whisper_transcription;
       dOutput.innerHTML = json.deepspeech_transcription;
     } else {
       oOutput.innerHTML = "Error occurred when trying to upload your file.<br \/>";
     }
     };
 oOutput.innerHTML = "Transcribing file!";
 console.log("Sending file!")
 oReq.send(formData);

}
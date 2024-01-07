
const WebCamElement = document.getElementById("webCam");
const CanvasElement = document.getElementById("canvas");
const middleForm = document.querySelector('form');
let webcam;

try {
	webcam = new Webcam(WebCamElement, "user", CanvasElement);
	webcam.start().catch( (e) => console.log(e));

} catch (error) {
	console.log("Error when trying to use the webcam");
	console.log(error);
}


function startPictureProcess(){
	let message;
	try{
		message = webcam.snap(); // First take a picture
	} catch (error){
		console.log("Error when trying to take snapshot of webcam");
		console.log(error);
	}
	
	// Make POST request to server
	fetch(
		'/process', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
			},
			body: JSON.stringify({ message }),
		}
		)
		.then(
			response => {
				return response.text()
			}
		)
		.then(
			(my_json) => {
				document.getElementById("respuesta").style.animation= "animacionRespuesta 2s"
				document.getElementById("respuesta").style.display= "block"
				document.getElementById("respuesta-texto").innerText=JSON.parse(my_json).message
				/* Aqui toca cambiar el texto de la emoción predicha 
				Y hacer la animación solo si tenemos una emoción recibida.*/

			}
		)
		.catch(error => console.error('Error al enviar la imagen:', error));
		console.log('Finish')
	
}


/*
function takeAPicture() {
	let picture = webcam.snap()
	//console.log(picture)
	//document.getElementById("respuesta").style.animation= "animacionRespuesta 2s"
	//document.getElementById("respuesta").style.display= "block"
	var pictureBlob = dataURLtoBlob(picture)
	let micanvas = document.getElementById("canvas")
	var reader  = new FileReader();
	reader.onload = function(e)  {
        var image = document.createElement("img");
        // the result image data
        image.src = e.target.result;
        document.body.appendChild(image);
     }
     // you have to declare the file loading
     reader.readAsDataURL(pictureBlob);
	 return picture
}*/



function dataURLtoBlob(dataurl) {
    var arr = dataurl.split(','), mime = arr[0].match(/:(.*?);/)[1],
        bstr = atob(arr[1]), n = bstr.length, u8arr = new Uint8Array(n);
    while(n--){
        u8arr[n] = bstr.charCodeAt(n);
    }
    return new Blob([u8arr], {type:mime});
}


function cerrarRespuesta() {
	document.getElementById("respuesta").style.animation= "none"
	document.getElementById("respuesta").style.display= "none"
	document.getElementById("respuesta-texto").innerText=""
}
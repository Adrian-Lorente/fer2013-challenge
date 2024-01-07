const express = require('express');
const path = require('path')
const fs = require("fs")
const cp = require("child_process")
const app = express();


app.use(express.static('../frontend'))
app.use(express.json({ limit: '10mb' }));
app.get('/', (req, res) => {
	res.sendFile(path.join(__dirname, '../frontend/index.html'))
});

/* Message processing */

app.post(
	"/process",
	(req, res) => {
		let staticFilepathWrite = "./uploads/out.png";
		// Recibimos el body del mensaje
		const base64Data = req.body.message;
		// Eliminamos los metadatos
		var imageData = base64Data.replace(/^data:image\/png;base64,/, "");
		// Escribimos la imagen en un fichero para poder ser procesada
		fs.writeFileSync(staticFilepathWrite, imageData, 'base64', (err) => {
			if (err) 
				console.log(`Error encountered parsing camera: ${err}`); 
			else { 
				console.log("Output image file written successfully\n"); 
			}
		  });
		
		// If you use "python3" or "python" to run python scripts, change the "py" in the line below to the one you use.
		const face_process_model = cp.spawnSync('py', ['./app.py', '--img', './uploads/out.png']);
		let result = face_process_model.stdout?.toString()?.trim();
		let error = face_process_model.stderr?.toString()?.trim();
		console.log("Resultado es: " + result);
		console.log("Error es: " + error);
		
		if (error.length > 0) {
			result = "Indescifrable"
			res.status(500).json({ message: result });
		}
		else{
			res.status(200).json({ message: result });
		}
	});
module.exports = app;

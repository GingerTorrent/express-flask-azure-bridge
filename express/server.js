import express from "express";
import { dirname } from "path";
import { fileURLToPath } from "url";
import path from "path"; 
import multer from "multer";
// import axios from "axios";
// import FormData from 'form-data';
// import bodyParser from "body-parser"

const __dirname = dirname(fileURLToPath(import.meta.url));

const upload = multer();
const app = express();
const port = 3000;


app.get("/", (req, res) => {
  res.sendFile(path.join(__dirname, "..", "public", "index.html"));
});

app.post('/upload', upload.single('image'), async (req, res) => {
    console.log('File received in Express:', req.file ? true : false);
    console.log('Buffer length:', req.file.buffer.length);

  try {
    const fileBuffer = req.file.buffer;  
    // send to flask       e.g. http://localhost:5000
    const response = await fetch('  http://rnwwn-2a02-a31d-a193-3000-7532-25d7-f50-2d6d.a.free.pinggy.link/ocr', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/octet-stream'
      },
      body: fileBuffer
    });

    const data = await response.json();
    // output.textContent = JSON.stringify(data);
    res.json(data); // send to frontend
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
  
});

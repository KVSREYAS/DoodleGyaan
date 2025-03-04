const express = require('express');
const path = require('path');
const fs = require('fs');
const cors = require('cors');

const app = express();
const PORT = 5000;
const MAX_RETRIES = 30; // 60 seconds maximum wait time
const RETRY_INTERVAL = 2000; // 2 seconds

app.use(cors());

let isPDFGenerating = false;
let pdfError = null;

function checkFileExists(filePath, retries = 0) {
  return new Promise((resolve, reject) => {
    fs.access(filePath, fs.constants.F_OK, (err) => {
      if (!err) {
        resolve(true);
      } else if (retries >= MAX_RETRIES) {
        reject(new Error('Maximum retries reached'));
      } else {
        setTimeout(() => {
          checkFileExists(filePath, retries + 1)
            .then(resolve)
            .catch(reject);
        }, RETRY_INTERVAL);
      }
    });
  });
}

app.get('/', (req, res) => {
  res.send('Welcome to the PDF server. Use /get-pdf to download the PDF.');
});

app.get('/pdf-status', (req, res) => {
  if (pdfError) {
    res.json({ status: 'error', error: pdfError });
  } else {
    res.json({ 
      status: isPDFGenerating ? 'generating' : 'ready'
    });
  }
});

app.get('/get-pdf', async (req, res) => {
  const filePath = path.resolve(__dirname, './dummy.pdf');

  if (isPDFGenerating) {
    return res.status(202).json({ status: 'generating' });
  }

  try {
    isPDFGenerating = true;
    pdfError = null;

    await checkFileExists(filePath)
      .then(() => {
        isPDFGenerating = false;
        res.sendFile(filePath);
      })
      .catch((error) => {
        pdfError = 'PDF generation timeout';
        isPDFGenerating = false;
        res.status(404).send('File not found after maximum retries');
      });

  } catch (error) {
    isPDFGenerating = false;
    pdfError = error.message;
    res.status(500).send('PDF generation failed');
  }
});

app.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
});
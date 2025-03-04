
import React, { useState } from 'react';
import { fetchPDF } from './Api.jsx';
import './PDFViewer.css';

function PDFViewer() {
  const [pdfUrl, setPdfUrl] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleFetchPDF = async () => {
    setIsLoading(true);
    setError(null);
    try {
      const url = await fetchPDF();
      setPdfUrl(url);
    } catch (err) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div>
      <button className='fetchpdf' onClick={handleFetchPDF} disabled={isLoading}>
        {isLoading ? 'SUPERCHARGING...' : 'GET THE COMIC'}
      </button>
      {error && <p>Error: {error}</p>}
      {pdfUrl && (
        <iframe className='pdfviewer'
          src={pdfUrl}
          width="50%"
          height="1000px"
          title="PDF Viewer"
        ></iframe>
      )}
    </div>
  );
}

export default PDFViewer;
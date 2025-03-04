export async function fetchPDF() {
  const maxRetries = 150; // 60 seconds maximum wait time
  const retryInterval = 2000; // 2 seconds

  for (let i = 0; i < maxRetries; i++) {
    const response = await fetch('http://localhost:5000/get-pdf');
    
    if (response.status === 200) {
      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      return url;
    } else if (response.status === 202 || response.status === 404) {
      // PDF is still generating or not found, wait and retry
      await new Promise(resolve => setTimeout(resolve, retryInterval));
    } else {
      throw new Error('PDF generation failed');
    }
  }

  throw new Error('PDF generation timeout');
}
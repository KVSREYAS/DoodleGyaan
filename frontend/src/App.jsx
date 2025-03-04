import { useState } from 'react'
import Navbar from './Navbar.jsx'
import Home from './Home.jsx'
import HomeMiddle from './HomeMiddle.jsx'
import HomeBottom from './HomeBottom.jsx'
import Footer from './Footer.jsx'
import Carousel from './Carousel.jsx'
import PDFViewer from './PDFViewer.jsx'
import TextSender from './textSender.jsx'
import './App.css'

function App() {
  //const [count, setCount] = useState(0)

  return (
    <>
      <div className='app-parent'>
        <Navbar />
        <Home />
        <Carousel />
        <HomeMiddle />
        <HomeBottom />
        <TextSender />
        <PDFViewer />
        <Footer />
      </div>
    </>
  );
}

export default App;

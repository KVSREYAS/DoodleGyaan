

import { useState } from 'react'
import Navbar from './Navbar.jsx'
import Home from './Home.jsx'
import HomeMiddle from './HomeMiddle.jsx'
import HomeBottom from './HomeBottom.jsx'
import Footer from './Footer.jsx'
import './Landing.css'



function Landing() {
  //const [count, setCount] = useState(0)

  return (
    <>
      <div className='landing-parent'>
        <Home />
        <HomeMiddle />
        <HomeBottom />
      </div>
    </>
  );
}

export default Landing;

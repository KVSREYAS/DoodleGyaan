import { useState } from 'react'
import './Home.css'
import TopImage from './assets/side_panel_one.png'
import BottomImage from './assets/side_panel_two.png'

function Home() {
  const [count, setCount] = useState(0)

  return (
    <>
      <div className='home-parent'>
        <div className='header-text'>Education.<br></br>Panelized into<br></br>Comics.
        <p>Meet Doodle Gyan, your AI comic crafter.</p></div>
        <div className="side-panel">
          <img className='side-panel-top-image' width={400} height={300} src={TopImage} alt="" />
          <img className='side-panel-bottom-image' width={400} height={300} src={BottomImage} alt="" />
        </div>
      </div>
    </>
  );
}

export default Home;

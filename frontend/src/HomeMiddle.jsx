import { useState } from 'react'
import './HomeMiddle.css'
import TopImage from './assets/side_panel_one.png'
import BottomImage from './assets/side_panel_two.png'

function HomeMiddle() {
  const [count, setCount] = useState(0)

  return (
    <>
      <div className='home-middle-parent'>
        <div className='home-middle-header-text'>Unleash your creativity with our generative AI-powered comic generator that transforms any text prompt into stunning, vivid comic panels in seconds. Simply enter your topic, and watch as our advanced algorithms craft unique, engaging visual narratives that weave your topic in!  
        </div>
      </div>
    </>
  );
}

export default HomeMiddle;

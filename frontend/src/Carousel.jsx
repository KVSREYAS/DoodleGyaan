import React from "react"
import CarouselImage from './assets/carousel_image.png'
import "./Carousel.css"

function Carousel() {
  return (
    <>
      <div className="scroll-container">
          <div className="scroll-content">
            <img className="scroll-image" id="mainimg" src={CarouselImage} alt="Scrolling Banner"/>
            <img className="scroll-image" src={CarouselImage} alt="Scrolling Banner Duplicate"/>
        </div>
      </div>
    </>
  );
}

export default Carousel;

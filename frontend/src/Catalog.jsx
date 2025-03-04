import React from "react";
import './Catalog.css';
import first from './assets/firstCatalog.jpg';
import second from './assets/secondCatalog.jpg';
import third from './assets/thirdCatalog.jpg';
import fourth from './assets/fourthCatalog.jpg';
import fifth from './assets/fifthCatalog.jpg';
import sixth from './assets/sixthCatalog.jpg';
import seventh from './assets/seventhCatalog.jpg';
import eighth from './assets/eighthCatalog.jpg';
import ninth from './assets/ninthCatalog.jpg';
import tenth from './assets/tenthCatalog.jpg';
import eleventh from './assets/eleventhCatalog.jpg';
import twelfth from './assets/twelfthCatalog.jpg';


const imageUrls = [
    first,
    second,
    third,
    fourth,
    fifth,
    sixth,
    seventh,
    eighth,
    ninth,
    tenth,
    eleventh,
    twelfth
];

function Catalog() {
    return (
        <div className="catalog">
            <h1>The Comic Catalog</h1>
            <div className="catalog-grid">
                {imageUrls.map((url, index) => (
                    <div className="catalog-item" key={index}>
                        <img src={url} alt={`Item ${index + 1}`} />
                    </div>
                ))}
            </div>
        </div>
    );
}

export default Catalog;
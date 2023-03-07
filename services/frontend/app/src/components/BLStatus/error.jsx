import React from "react";

import { useLocation } from "react-router-dom";
import error from "../../img/error.png";
import "./bl.scss";

export default function Error() {
  const location = useLocation();
  const { identifier } = location.state;
  const { direction } = location.state;
  const { type } = location.state;
  
  return (
    <div className="bg-gradient-to-r from-white via-sky-100 to-sky-200 w-screen">
      <div className="grid grid-cols-2 gap-2">
        <div className="flex flex-col p-6 mt-10">
          <h1 className="text-3xl 2xl:text-5xl text-center">Sorry, we could not find your shipment</h1>
          <img className="w-10/12 h-10/12 ml-12" src={error} alt="" />
        </div>

        <div className="grid grid-cols-2 gap-y-10 place-content-center mt-20">
          <h1 className="font-bold text-lg">Here&apos;s what you entered:</h1>
          <p>BL/Container No: {identifier}</p>
          <p>Direction: {direction}</p>
          <p>Type: {type}</p>
        </div>

      </div>
      <svg xmlns="http://www.w3.org/2000/svg" className="block" viewBox="0 0 1440 320"><path fill="#a2d9ff" fillOpacity="0.8" d="M0,96L40,80C80,64,160,32,240,53.3C320,75,400,149,480,165.3C560,181,640,139,720,117.3C800,96,880,96,960,106.7C1040,117,1120,139,1200,133.3C1280,128,1360,96,1400,80L1440,64L1440,320L1400,320C1360,320,1280,320,1200,320C1120,320,1040,320,960,320C880,320,800,320,720,320C640,320,560,320,480,320C400,320,320,320,240,320C160,320,80,320,40,320L0,320Z" />
        <svg xmlns="http://www.w3.org/2000/svg" className="block" viewBox="0 0 1440 320"><path fill="#0099ff" fillOpacity="0.2" d="M0,96L80,122.7C160,149,320,203,480,202.7C640,203,800,149,960,128C1120,107,1280,117,1360,122.7L1440,128L1440,320L1360,320C1280,320,1120,320,960,320C800,320,640,320,480,320C320,320,160,320,80,320L0,320Z" />
          <svg xmlns="http://www.w3.org/2000/svg" className="block" viewBox="0 0 1440 320"><path fill="#0099ff" fillOpacity="1" d="M0,128L60,154.7C120,181,240,235,360,229.3C480,224,600,160,720,154.7C840,149,960,203,1080,213.3C1200,224,1320,192,1380,176L1440,160L1440,320L1380,320C1320,320,1200,320,1080,320C960,320,840,320,720,320C600,320,480,320,360,320C240,320,120,320,60,320L0,320Z" /></svg>
        </svg>
      </svg>
    </div>

  );
}


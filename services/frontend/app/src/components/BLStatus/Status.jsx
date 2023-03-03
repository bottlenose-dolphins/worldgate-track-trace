import React from "react";
import Card from "react-bootstrap/Card";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import "./bl.scss";
import { useLocation } from "react-router-dom";
import dateFormat, { masks } from "dateformat";



export default function Status() {
    const location=useLocation();
    const {arrival}=location.state;
    const {discharge}=location.state
    const {status}=location.state
    const {vessel}=location.state
    const {bl}=location.state
    const {shipline}=location.state
    const {loading}=location.state

    const eta=dateFormat("2023-01-02","d,mmm,yyyy");
    const arrsplit=eta.split(",");
    const day=arrsplit[0]
    const month=arrsplit[1]
    const year=arrsplit[2]


  return (
    <div>
    <div className="grid grid-cols-2 gap-2">
      <div className=" p-2 mt-10">

      <Card style={{ width: "40rem",backgroundColor:"#217BF4",borderRadius:"10px"}}>
      <Card.Body>
      <div className="grid grid-cols-2">
      <div className="  ">
        <Card.Title className=" font-sans text-white  text-5xl p-6">{day} {month}</Card.Title>
      
        <Card.Subtitle className=" text-white text-xl pl-6 pb-6">{year}</Card.Subtitle>
        </div>
        <div className="  ">
        <Card.Title className=" font-sans text-white  p-6">

        <svg xmlns="http://www.w3.org/2000/svg" className="h-10 ml-20" viewBox="0 0 576 512"><path fill="#FFFFFF" d="M224 0H352c17.7 0 32 14.3 32 32h75.1c20.6 0 31.6 24.3 18.1 39.8L456 96H120L98.8 71.8C85.3 56.3 96.3 32 116.9 32H192c0-17.7 14.3-32 32-32zM96 128H480c17.7 0 32 14.3 32 32V283.5c0 13.3-4.2 26.3-11.9 37.2l-51.4 71.9c-1.9 1.1-3.7 2.2-5.5 3.5c-15.5 10.7-34 18-51 19.9H375.6c-17.1-1.8-35-9-50.8-19.9c-22.1-15.5-51.6-15.5-73.7 0c-14.8 10.2-32.5 18-50.6 19.9H183.9c-17-1.8-35.6-9.2-51-19.9c-1.8-1.3-3.7-2.4-5.6-3.5L75.9 320.7C68.2 309.8 64 296.8 64 283.5V160c0-17.7 14.3-32 32-32zm32 64v96H448V192H128zM306.5 421.9C329 437.4 356.5 448 384 448c26.9 0 55.3-10.8 77.4-26.1l0 0c11.9-8.5 28.1-7.8 39.2 1.7c14.4 11.9 32.5 21 50.6 25.2c17.2 4 27.9 21.2 23.9 38.4s-21.2 27.9-38.4 23.9c-24.5-5.7-44.9-16.5-58.2-25C449.5 501.7 417 512 384 512c-31.9 0-60.6-9.9-80.4-18.9c-5.8-2.7-11.1-5.3-15.6-7.7c-4.5 2.4-9.7 5.1-15.6 7.7c-19.8 9-48.5 18.9-80.4 18.9c-33 0-65.5-10.3-94.5-25.8c-13.4 8.4-33.7 19.3-58.2 25c-17.2 4-34.4-6.7-38.4-23.9s6.7-34.4 23.9-38.4c18.1-4.2 36.2-13.3 50.6-25.2c11.1-9.4 27.3-10.1 39.2-1.7l0 0C136.7 437.2 165.1 448 192 448c27.5 0 55-10.6 77.5-26.1c11.1-7.9 25.9-7.9 37 0z"/></svg>
        <span className="ml-20">
       {discharge}
       </span>
       <span > , Vessel:{vessel}</span>
        </Card.Title>
        <Card.Subtitle className=" text-white text-xl pl-6 pb-6 ml-20">BL:{bl}</Card.Subtitle>
            </div>
    </div>
        
      </Card.Body>
    </Card>
      </div>
      <div className="  grid grid-cols-2 bg-gradient-to-r from-white via-sky-100 to-sky-200	 p-2 mt-10">
      <div className="">
        <h2 className="p-6 text-3xl ">Tracking Status</h2>
        <h2 className="p-6 text-xl font-bold">BL:{bl}</h2>
        <div >
        <ul className="step-progress">
    <li className="step-progress-item is-done"><strong>Shipment Origin</strong><br/><h2 className="text-xl">{loading}</h2></li>
    <li className="step-progress-item is-done"><strong>Shipment InProgress Via</strong><br/><h2 className="text-xl">{shipline}</h2></li>
    <li className="step-progress-item is-done"><strong>Shipment Disembarked</strong><br/><h2 className="text-xl">{discharge}</h2></li>
    <li className="step-progress-item current"><strong>Shipment Status</strong><br/><h2 className="text-xl">{status}</h2></li>

    <h1 className="ml-80">ETA:{arrival}</h1>
    
  </ul>
</div>

      </div>
      <div>
        {/* <h1 className="p-6 text-3xl font-bold text-[#217BF4]">On Time</h1> */}
      </div>
</div>


    </div>
    <svg xmlns="http://www.w3.org/2000/svg" className="block" viewBox="0 0 1440 320"><path fill="#a2d9ff" fillOpacity="0.8" d="M0,96L40,80C80,64,160,32,240,53.3C320,75,400,149,480,165.3C560,181,640,139,720,117.3C800,96,880,96,960,106.7C1040,117,1120,139,1200,133.3C1280,128,1360,96,1400,80L1440,64L1440,320L1400,320C1360,320,1280,320,1200,320C1120,320,1040,320,960,320C880,320,800,320,720,320C640,320,560,320,480,320C400,320,320,320,240,320C160,320,80,320,40,320L0,320Z"/>
  <svg xmlns="http://www.w3.org/2000/svg" className="block" viewBox="0 0 1440 320"><path fill="#0099ff" fillOpacity="0.2" d="M0,96L80,122.7C160,149,320,203,480,202.7C640,203,800,149,960,128C1120,107,1280,117,1360,122.7L1440,128L1440,320L1360,320C1280,320,1120,320,960,320C800,320,640,320,480,320C320,320,160,320,80,320L0,320Z"/>
  <svg xmlns="http://www.w3.org/2000/svg" className="block" viewBox="0 0 1440 320"><path fill="#0099ff" fillOpacity="1" d="M0,128L60,154.7C120,181,240,235,360,229.3C480,224,600,160,720,154.7C840,149,960,203,1080,213.3C1200,224,1320,192,1380,176L1440,160L1440,320L1380,320C1320,320,1200,320,1080,320C960,320,840,320,720,320C600,320,480,320,360,320C240,320,120,320,60,320L0,320Z"/></svg>
  </svg>
  </svg>
    </div>
    
  );
}


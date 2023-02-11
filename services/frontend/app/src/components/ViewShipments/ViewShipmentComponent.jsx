import React, { useState } from "react";
import refreshButton from "../../img/refreshButton.png"
import clock from "../../img/clock.png"
import warning from "../../img/warning.png"
import locationWhite from "../../img/locationWhite.png"
import locationBlack from "../../img/locationBlack.png"
import sortButton from "../../img/sortButton.png"

export default function ViewShipmentComponent(props){
  const [buttonText, setButtonText] = useState("closest to arrival");
  const [schedule, setSchedule] = useState(true);
  const [delayed, setDelayed] = useState(true);
  const [items, setItems] = useState([    { date: "2 Feb 2023", country: "USA", status: "On Schedule", lastUpdated: "01/02/23 06:00", blNumber: "MDC-034568" }, 
                                          { date: "3 Feb 2023", country: "UK", status: "Delayed", lastUpdated: "01/02/23 06:00", blNumber: "YMLU76438" },
                                          { date: "8 Feb 2023", country: "India", status: "On Schedule", lastUpdated: "01/02/23 06:00", blNumber: "MDA-6475" },
                                          { date: "12 Feb 2023", country: "UK", status: "Delayed", lastUpdated: "01/02/23 06:00", blNumber: "MDA-1234" }  ]);

//Change the items once linked with BE so can pull data accurately

  const toggleSchedule = () => {
    setSchedule(!schedule);
    //setDelayed(false);
  };

  const toggleDelayed = () => {
    setDelayed(!delayed);
    //setSchedule(false);
  };

  const handleClick = () => {
    if(buttonText==="closest to arrival"){
      setButtonText("furthest from arrival");
    }
    else{
      setButtonText("closest to arrival");
    }
  };

  return (
    <div className="p-10">
    <h1 className="text-2xl font-medium text-blue-700">{props.title}</h1>
    <div className="bg-light-blue-500 p-4 rounded-lg border border-blue-500 my-5 w-1/2">
    <h2 className="text-2xl font-medium text-blue-700">At a glance</h2>
      <div className="mt-6 flex">
        <button
          className={`flex-1 p-2 text-lg font-medium border border-gray-400 rounded-lg ${
            schedule ? "bg-blue-500 text-white" : "bg-gray-200"
          }`}
          onClick={toggleSchedule}
        >
            <img className="mx-auto" src={clock} alt=""/>
          On Schedule ({
            items.filter(item => item.status === "On Schedule").length
          })
        
        </button>
        <button
          className={`flex-1 p-2 text-lg font-medium border border-gray-400 rounded-lg ml-2 ${
            delayed ? "bg-yellow-500 text-black" : "bg-gray-200"
          }`}
          onClick={toggleDelayed}
        >
        <img className="mx-auto" src={warning} alt=""/>
          Delayed ({items.filter(item => item.status === "Delayed").length})
        </button>
        </div>
      </div>
      <div className="my-auto bg-light-blue-500 p-4 rounded-lg border border-blue-500 w-1/2">
      <h2 className="mt-6 text-lg font-medium text-blue-700 inline-block">List view</h2>
      <img className="ml-96 inline-block" src={sortButton}/> <button className="font-medium text-blue-700" onClick={handleClick}>{buttonText}</button>
      <div className="mt-6">
      {items.map((item, index) => {
    if (schedule && item.status === "On Schedule") {
      return (
        <div className="card m-4 bg-blue-500 p-4 rounded-lg border border-blue-500" style={{width: "36rem"}} key={index}>
          <div className="card-body text-white">
            <h5 className="card-title font-bold">{item.date}</h5>
            <h6 className="card-subtitle mb-2 text-muted">Last updated at: {item.lastUpdated} <button type="button"><img src={refreshButton} alt=""/></button></h6>
            <p className="card-text flex"><img src={locationWhite} alt=""/>{item.country}</p>
            <p className="card-text">B/L: {item.blNumber}</p>
          </div>
        </div>
      );
    } else if (delayed && item.status === "Delayed") {
      return (
        <div className="card m-4 bg-yellow-500 p-4 rounded-lg border border-yellow-500" style={{width: "36rem"}} key={index}>
          <div className="card-body">
            <h5 className="card-title font-bold">{item.date}</h5>
            <h6 className="card-subtitle mb-2 text-muted">Last updated at: {item.lastUpdated} <button type="button"><img src={refreshButton} alt=""/></button></h6>
            <p className="card-text flex"><img src={locationBlack} alt=""/>{item.country}</p>
            <p className="card-text">B/L: {item.blNumber}</p>
          </div>
        </div>
      );
    } else {
      return null;
    }
  })}</div>
  </div>
</div>
  )};
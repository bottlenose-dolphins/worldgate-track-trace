import React, { useEffect, useState } from "react";
import axios from "axios";
import { Card } from "react-bootstrap";
import { authenticate } from "../../api/config"
import locationWhite from "../../img/locationWhite.png"
import sortButton from "../../img/sortButton.png"

const getImportShipment = async() => {
  try {
    const authRes = await authenticate();
    // const {userId} = authRes.data;
    if(authRes.code === 200) {
      const res = await axios.post("http://127.0.0.1:5010/getImportContainerNum", {
            "wguser_id": "HMuAqcsAFtnJGfrM84VqL7"
      });
      if (res) {
        return res.data;
      }
    }
  }
  catch (error) {
    return error.response.data;
  }
  return "";
}

const getExportShipment = async() => {
  try {
    const authRes = await authenticate();
    // const {userId} = authRes.data;
    if(authRes.code === 200) {
      const res = await axios.post("http://127.0.0.1:5010/getExportContainerNum", {
            "wguser_id": "bk666dcoeZTH3dxZCuu4FR"
      });
      if (res) {
        return res.data;
      }
    }
  }
  catch (error) {
    return error.response.data;
  }
  return "";
}


export default function ViewShipmentComponent(props){
  
  const [buttonText, setButtonText] = useState("closest to arrival");
  const {title, type} = props;
  const [items, setItems] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      if (type === "Import") {
        const importShipments = await getImportShipment();
        setItems(importShipments);
      } else if (type === "Export") {
        const exportShipments = await getExportShipment();
        setItems(exportShipments);
      }
    };
    fetchData();
  }, [type]);

  console.log(items);

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
    <h1 className="text-2xl font-medium text-blue-700">{title}</h1>
      <div className="my-auto bg-light-blue-500 p-4 rounded-lg border border-blue-500 w-1/2">
      <h2 className="mt-6 text-lg font-medium text-blue-700 inline-block">List view</h2>
      <img className="ml-96 inline-block" src={sortButton} alt="sort"/> <button type="button" className="font-medium text-blue-700" onClick={handleClick}>{buttonText}</button>
      <div className="mt-6">
      {items.map((item, index) => {

        return (
          <div>
          <div className="grid grid-cols-2 gap-2">
            <div className=" p-2 mt-5">

            <Card style={{ width: "36rem",backgroundColor:"#217BF4",borderRadius:"10px"}} key={index}>
            <Card.Body>
            <div className="grid grid-cols-2">
            <div className="  ">
              <Card.Title className=" font-sans text-white  text-5xl p-6">{item.arrival_date ? item.arrival_date.slice(0,6) : item.delivery_date.slice(0,6)}</Card.Title>
              <Card.Subtitle className=" text-white text-xl pl-6 pb-6">{item.arrival_date ? item.arrival_date.slice(-4) : item.delivery_date.slice(-4)}</Card.Subtitle>
              </div>
              <div>
              <Card.Title className=" font-sans text-white  p-6" style={{ display: "flex", alignItems: "center"}}>
              <img className="h-10 ml-20" src={locationWhite} alt=""/>
              <span>{item.import_destination ? item.import_destination : item.export_destination}</span>
              </Card.Title>
              <Card.Subtitle className=" text-white text-xl pl-6 pb-6 ml-20">{item.container_numbers}</Card.Subtitle>
                  </div>
          </div>
              
            </Card.Body>
          </Card>
            </div>
            </div>
            </div>
        );
  })}</div>
  </div>
</div>
  )};
 // const [schedule, setSchedule] = useState(true);
  // const [delayed, setDelayed] = useState(true);
  
// Change the items once linked with BE so can pull data accurately

  // const toggleSchedule = () => {
  //   setSchedule(!schedule);
  //   // setDelayed(false);
  // };

  // const toggleDelayed = () => {
  //   setDelayed(!delayed);
  //   // setSchedule(false);
  // };

  /* <div className="bg-light-blue-500 p-4 rounded-lg border border-blue-500 my-5 w-1/2"/> 
    <h2 className="text-2xl font-medium text-blue-700">At a glance</h2>
      <div className="mt-6 flex">
        <button type="button"
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
        <button type="button"
          className={`flex-1 p-2 text-lg font-medium border border-gray-400 rounded-lg ml-2 ${
            delayed ? "bg-yellow-500 text-black" : "bg-gray-200"
          }`}
          onClick={toggleDelayed}
        >
        <img className="mx-auto" src={warning} alt=""/>
          Delayed ({items.filter(item => item.status === "Delayed").length})
        </button>
        </div> */
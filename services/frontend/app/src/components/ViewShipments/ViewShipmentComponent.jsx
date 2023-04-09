import React, { useState, useMemo, useEffect } from "react";
import { Card } from "react-bootstrap";
import { ChevronDownIcon } from "@heroicons/react/24/outline";
import { searchShipmentStatus ,addsubscription, deletesubscription} from "src/api/shipment";
import {authenticate} from "src/api/config"
import dateFormat from "dateformat";
import { useNavigate } from "react-router-dom";
import locationWhite from "../../img/locationWhite.png";


export default function ViewShipmentComponent({ title, data, setLoading }) {
  function ShipmentButton({item}) {
    const subscribe = async () => {
      const userid=user;
      const directionType = item.type.toLowerCase();
      const containerNumber = item.container_numbers[0];
      console.log(directionType);
      console.log(containerNumber);
      const searchType = "ctr";
      try {
      
        const response = await searchShipmentStatus(containerNumber, searchType, directionType);
        if (response.code !== 200) {
          throw new Error("No status found");
        }
        else if (response.code === 200) {
          const direction = title === "Incoming Shipments" ? "import" : "export";
          const result = response.data;
          const status=result.status;
          const response2 = await addsubscription(userid, containerNumber,status, direction);
          if (response2.code !== 200) {
            throw new Error("No status found");
        }
          else if (response2.code === 200) {
          const result = response2.data;
          console.log(result)
         
        }
        }
      }
      catch (err) {
        console.log(err);
      }  
    }
    const unsubscribe = async () => {
      const containerNumber = item.container_numbers[0];
      try {
          const response2 = await deletesubscription(containerNumber);
          if (response2.code !== 200) {
            throw new Error("No status found");
        }
          else if (response2.code === 200) {
          const result = response2.data;
          console.log(result)
        }
      }
      catch (err) {
        console.log(err);
      }
      

    }
  
    return(
      <div className="">
      <button onClick={subscribe} type="button" className="mt-2 ml-2 mb-2 inline-flex items-center px-5 py-2.5 text-xs  text-center text-white bg-blue-700 rounded-lg hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800"> 
          <svg
        xmlns="http://www.w3.org/2000/svg"
        viewBox="0 0 24 24"
        fill="currentColor"
        className="h-5 w-5">
        <path
          fillRule="evenodd"
          d="M5.25 9a6.75 6.75 0 0113.5 0v.75c0 2.123.8 4.057 2.118 5.52a.75.75 0 01-.297 1.206c-1.544.57-3.16.99-4.831 1.243a3.75 3.75 0 11-7.48 0 24.585 24.585 0 01-4.831-1.244.75.75 0 01-.298-1.205A8.217 8.217 0 005.25 9.75V9zm4.502 8.9a2.25 2.25 0 104.496 0 25.057 25.057 0 01-4.496 0z"
          clipRule="evenodd" />
      </svg>
      Subscribe
        </button>
        <br/>
        <button onClick={unsubscribe} type="button" className="mt-2 ml-2 mb-2 inline-flex items-center px-5 py-2.5 text-xs  text-center text-white bg-red-700 rounded-lg hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-red-300 dark:bg-red-600 dark:hover:bg-red-700 dark:focus:ring-red-800"> 
        <svg className="mr-2" fill="#FFFFFF" height="20px" width="20px" version="1.1" id="Capa_1" xmlns="http://www.w3.org/2000/svg" 
        xmlnsXlink="http://www.w3.org/1999/xlink" viewBox="0 0 283.194 283.194" 
        xmlSpace="preserve"><g id="SVGRepo_bgCarrier" strokeWidth="0"/><g id="SVGRepo_tracerCarrier" 
        strokeLinecap="round" strokeLinejoin="round"/><g id="SVGRepo_iconCarrier"> <g> 
          <path d="M141.597,32.222c-60.31,0-109.375,49.065-109.375,109.375s49.065,109.375,109.375,109.375s109.375-49.065,109.375-109.375 S201.907,32.222,141.597,32.222z M50.222,141.597c0-50.385,40.991-91.375,91.375-91.375c22.268,0,42.697,8.01,58.567,21.296 L71.517,200.164C58.232,184.293,50.222,163.865,50.222,141.597z M141.597,232.972c-21.648,0-41.558-7.572-57.232-20.2 L212.772,84.366c12.628,15.674,20.2,35.583,20.2,57.231C232.972,191.982,191.981,232.972,141.597,232.972z"/>
          <path d="M141.597,0C63.52,0,0,63.52,0,141.597s63.52,141.597,141.597,141.597s141.597-63.52,141.597-141.597S219.674,0,141.597,0z M141.597,265.194C73.445,265.194,18,209.749,18,141.597S73.445,18,141.597,18s123.597,55.445,123.597,123.597 S209.749,265.194,141.597,265.194z"/> </g> </g></svg>
       Unsubscribe
        </button>
        </div>
    )
    
  }
  const [user,setuser]=useState("")
useEffect(() => {
  const fetchData = async () => {
    const userdata = await authenticate();
    setuser(userdata.userId);
  
  };

  fetchData();
}, []);

console.log(user)

  useMemo(() => {
    data.sort((s1, s2) => {
      if (s1.arrival_date > s2.arrival_date) {
        return -1;
      }
      if (s1.arrival_date < s2.arrival_date) {
        return 1;
      }
      return 0;
    });
  }, [])

  const [isLatestOnTop, setIsLatestOnTop] = useState(true);
  const [items, setItems] = useState(data);

  const handleSortClick = () => {
    setIsLatestOnTop(!isLatestOnTop);
    setItems(items.reverse());
  };

  return (
    <div className="p-9 w-3/4">
      <h1 className="text-2xl font-medium text-blue-700 mb-1">{title}</h1>
      <div className="my-auto bg-blue-50 p-4 rounded-lg border border-blue-500">

        <div className="flex justify-between mt-3 mx-1">
          <div className="text-lg font-medium text-blue-700 w-1/2">List View</div>
          <button type="button" className="flex justify-end w-1/2 items-center" onClick={handleSortClick}>
            <ChevronDownIcon className={`w-6 h-6 text-blue-700 mr-1 ${!isLatestOnTop && "rotate-180"}`} />
            <div className="font-medium text-blue-700 hover:underline">{isLatestOnTop ? "closest to arrival" : "furthest from arrival"}</div>
          </button>
        </div>

        <div className="flex flex-col mt-5">
          {items.length === 0 && <div className="mx-1">No shipments found</div>}
          {items.length > 0 && items.map((item, index) => {
            return (
              <div className="inline-flex">
              <ShipmentCard key={index} item={item} index={index} setLoading={setLoading} />
              <ShipmentButton item={item}/>
              </div>
            );
          })}
        </div>

      </div>
    </div>
  )
  
};



function ShipmentCard({ item, index, setLoading }) {
  const navigate= useNavigate();

  const eta = item.arrival_date ? dateFormat(item.arrival_date, "d mmm yyyy") : dateFormat(item.delivery_date, "d mmm yyyy");

  const handleClick = async () => {
    setLoading(true);
    const directionType = item.type.toLowerCase();
    const containerNumber = item.container_numbers[0];
    const searchType = "ctr";
    try {
      const response = await searchShipmentStatus(containerNumber, searchType, directionType);
      if (response.code !== 200) {
        throw new Error("No status found");
      }
      else if (response.code === 200) {
        const result = response.data;
        navigate("/Status", {
          state: {
            blNo: containerNumber,
            type: searchType,
            eta: result.arrival_date,
            portOfDischarge: result.port_of_discharge,
            vesselName: result.vessel_name,
            status: result.delay_status,
            portOfLoading: result.port_of_loading,
            shippingLine: result.shipping_line
          }
        })
      }
    }
    catch (err) {
      navigate("/error", { state: { identifier: containerNumber, direction: directionType, type: searchType } })
    }
    setLoading(false);

  }


  return (
    <div role="button" className="mb-2" tabIndex={0}>
      <Card onClick={handleClick} onKeyDown={handleClick} className="mb-2 w-full" style={{ backgroundColor: "#217BF4", borderRadius: "10px" }} key={index}>
        <Card.Body>
          <div className="grid grid-cols-2 text-white p-4">
            <div className="flex flex-col justify-center">
              <Card.Title className="text-5xl justify-start mb-2">{eta.slice(0, 6)}</Card.Title>
              <Card.Subtitle className="text-xl justify-start">{eta.slice(-4)}</Card.Subtitle>
            </div>
            <div className="flex flex-col justify-center">
              <Card.Title className="flex justify-end mb-2" style={{ alignItems: "center" }}>
                <img className="h-10 mr-2" src={locationWhite} alt="shipping-icon" />
                <span>{item.import_destination ? item.import_destination : item.export_destination}</span>
              </Card.Title>
              <Card.Subtitle className="text-xl flex justify-end">{item.container_numbers[0]}</Card.Subtitle>
            </div>
          </div>
          
        </Card.Body>
      </Card>
      
    </div>
  )
}
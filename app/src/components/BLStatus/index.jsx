
import { useState } from "react";
import axios from "axios";
import TrackingHistoryTable from "./TrackingHistory";

export default function BLStatus() {

  const [selectedOption, setSelectedOption] = useState(null);
  const [secondSelectedOption, setSecondSelectedOption] = useState(null);
  const [selectedvalue, setSelectedValue] = useState(null);
  const [trackingHistory, setTrackingHistory] = useState([]);
  const [secondselectedvalue, setSecondSelectedValue] = useState(null);
  const [billOfLadingNumber, setBillOfLadingNumber] = useState("");
  const [displaytext, setDisplay] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const pattern = /^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d_-]*$/;
  const handleTrackShipment = async () => {
    setLoading(true);
    setError(null);
    
    try {
      const requestBody = {
        shipping_line: "Yang Ming",
        identifier: billOfLadingNumber,
        identifier_type: selectedvalue,
        direction: secondselectedvalue,
      };
      
      const response = await fetch('http://localhost:8081/scrape', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(requestBody)
      });
      
      if (response.status !== 200) {
        throw new Error('No status found');
      }
      
      const data = await response.json();
      setTrackingHistory([...trackingHistory, data]);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleBlur = () => {
    if (!billOfLadingNumber) {
      setError("The field cannot be empty");
    } else if (!pattern.test(billOfLadingNumber)) {
      setError("The value should be alphanumeric with exception of _ and -");
    }
  };

return(
<div>

  <div className="flex flex-col mt-20">
  <h1 className="text-6xl font-bold mb-20 ml-20">Track Your Shipment</h1>
  <div className="flex w-full mt-6">
    <div className="flex w-1/4 rounded-lg overflow-hidden ml-20 ">
      <button type="button"
        className={`w-1/2 py-2 text-center ${
          selectedOption === "Option 1"
            ? "bg-cyan-300 "
            : "bg-white text-black" 
        } border-2 border-blue-500/100 rounded-full`}
        onClick={() =>{setSelectedOption("Option 1");setSelectedValue("bl");setDisplay("Bill of Lading Number (BL)")}}
      >
        BL No.
      </button>
      
      <button type="button"
        className={`w-1/2 py-2 text-center ${
          selectedOption === "Option 2"
            ? "bg-cyan-300	 "
            : "bg-white text-black"
        } border-2 border-blue-500/100 rounded-full`}
        onClick={() => {setSelectedOption("Option 2");setSelectedValue("ctr");setDisplay("Container Number (CNo)")}}
        
      >
       
        Container No.
      </button>
     
    </div>
    <div className="flex justify-between w-1/4 rounded-lg overflow-hidden ml-40">
      <button type="button"
        className={`w-1/2 py-2 text-center ${
          secondSelectedOption === "Option 3"
            ? "bg-cyan-300 "
            : "bg-white text-black"
        } border-2 border-blue-500/100 rounded-full` }
        onClick={() => {setSecondSelectedOption("Option 3");setSecondSelectedValue("import");}}
      >
        Import
      </button>
      <button type="button"
        className={`w-1/2 py-2 text-center ${
          secondSelectedOption === "Option 4"
            ? "bg-cyan-300 "
            : "bg-white text-black"
        } border-2 border-blue-500/100 rounded-full`}
        onClick={() => {setSecondSelectedOption("Option 4");setSecondSelectedValue("export")}}
      >
        Export
      </button>
    </div>
  </div>
  <div className="flex flex-col w-80 mt-6 ml-20">
    <h4 className="text-stone-500"><i>{displaytext}</i></h4>
    <input
      type="text" id="blno" placeholder="Enter BL/Container No ..."
      className="mt-2 border border-gray-300 rounded-lg p-2"
      value={billOfLadingNumber} onBlur={handleBlur} 
      onChange={(e) => {setBillOfLadingNumber(e.target.value);setError("")}}
    />
 
  
 {error && <div className="text-red-500">{error}</div>}


        <button type="button"
          className="px-4 py-2 rounded mt-5 bg-blue-500 text-white"
          onClick={handleTrackShipment} 
        >
          Track Shipment
        </button>

  </div>
  </div>
  {loading && <p>Loading...</p>}
      {error && <p>Error: {error}</p>}
      {trackingHistory.length > 0 && (
        <div>
        <div className="font-medium text-lg italic p-5  text-center" >Tracking History</div>

      <div className="bg-black text-white rounded-lg overflow-hidden ml-4">

<table className="w-full text-left table-collapse">
<thead>
          <tr className="text-white">
            <th className="p-4 border-b-2 border-gray-800">Date</th>
            <th className="p-4 border-b-2 border-gray-800">Port of Discharge</th>
            <th className="p-4 border-b-2 border-gray-800">Date of Arrival</th>
            <th className="p-4 border-b-2 border-gray-800">Vessel Name</th>
            <th className="p-4 border-b-2 border-gray-800">Status</th>
          </tr>
        </thead>
          <tbody>
            {trackingHistory.map(item => (
              <tr>
                <td className="p-4 border-b border-gray-800"> {item.shipping_line}</td>
                <td className="p-4 border-b border-gray-800"> {item.shipping_line}</td>

                <td className="p-4 border-b border-gray-800"> {item.shipping_line}</td>

                <td className="p-4 border-b border-gray-800"> {item.shipping_line}</td>

                <td className="p-4 border-b border-gray-800"> {item.shipping_line}</td>

              </tr>
            ))}
          </tbody>
       </table>
       </div>
       </div>
       )}
        </div>
)
      }
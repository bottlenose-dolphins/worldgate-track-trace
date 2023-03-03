import { blStatus } from "src/api/user";
import { useState } from "react";

import { blStatus } from "src/api/user";

import { Alert, Navbar } from "react-bootstrap";
import { Bars } from "react-loading-icons";
import Modal from "react-modal";
import Button from "react-bootstrap/Button";

import { useNavigate } from "react-router-dom";

import ModalBody from "react-bootstrap/ModalBody";
import ModalHeader from "react-bootstrap/ModalHeader";
import ModalFooter from "react-bootstrap/ModalFooter";
import ModalTitle from "react-bootstrap/ModalTitle";
import Navigation from "../../layout/NavbarUser";

import ship from "../../img/ship3d.png";

import "./bl.scss";

export default function BLStatus() {
  const navigate=useNavigate();
  const [selectedOption, setSelectedOption] = useState(null);
  const [secondSelectedOption, setSecondSelectedOption] = useState("export");
  const [selectedvalue, setSelectedValue] = useState("bl");
  const [trackingHistory, setTrackingHistory] = useState([]);
  const [secondselectedvalue, setSecondSelectedValue] = useState(null);
  const [billOfLadingNumber, setBillOfLadingNumber] = useState("");
  const [displaytext, setDisplay] = useState("");
  const [error, setError] = useState("");
  const [error2, setError2] = useState("");
  const [loading, setLoading] = useState(false);
  const pattern = /^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d_-]*$/;
  const [show, setShow] = useState(false);
  const customStyles = {
    content: {
      top: "50%",
      left: "50%",
      right: "auto",
      bottom: "auto",
      marginRight: "-50%",
      transform: "translate(-50%, -50%)",
    },
  };
  const handleClose = () => setShow(false);
  const handleShow = () => setShow(true);



const handleTrackShipment = async () => {
  
    closeModal();
    setLoading(true);
    setError(null);
    
    try {
      const response = await blStatus("Yang Ming", billOfLadingNumber, selectedvalue, secondselectedvalue)
      
      if (response.status !== 200) {
        throw new Error("No status found");
      }
      
      const data = await response.json();
      setTrackingHistory([data]);
   
      navigate("/Status",{state:{arrival:trackingHistory[0].data.arrival_date,discharge:trackingHistory[0].data.port_of_discharge,vessel:trackingHistory[0].data.vessel_name,status:trackingHistory[0].data.status!=="undefined"?"No Status":trackingHistory[0].data.status,bl:billOfLadingNumber,loading:trackingHistory[0].data.port_of_loading,shipline:trackingHistory[0].data.shipping_line}})
    } catch (err) {
      navigate("/error",{state:{identifier:billOfLadingNumber,direction:secondselectedvalue,type:selectedvalue}})
      setError2(err.message);
    } finally {
      setError2("Connection Failed");
      setLoading(false);
    }
  };

  const handleBlur = () => {
    setError("")
    setError2("")
    if (!billOfLadingNumber) {
      setError("The field cannot be empty");
    } else if (!pattern.test(billOfLadingNumber)) {
      setError("The value should be alphanumeric with exception of _ and -");
    }
    else{
      openModal()
    }
  };

  Modal.setAppElement("body");
  let subtitle;
  const [modalIsOpen, setIsOpen] = useState(false);

  function openModal() {
    setIsOpen(true);
  }

  function afterOpenModal() {
    // references are now sync'd and can be accessed.
    subtitle.style.color = "#f00";
  }

  function closeModal() {
    setIsOpen(false);
  }
return(
 
<div id="fullpage " >


  <div className="flex flex-col mt-20 ">
 
  <h2 className="text-5xl text-left text-center font-bold  mt-20 ">Tracking Your Shipment has <br/> never been this easy!</h2>
  <Modal
        isOpen={modalIsOpen}
       
        style={customStyles}
        contentLabel="Example Modal"
      >
    
        <button type="button" className="font-bold mb-2" onClick={closeModal}>X</button>
        <span><h3 className="text-center italic mb-2">Choose Options</h3></span>
        <hr/>

        <div className="middle">
        <div className="wrapper">
 <input type="radio" name="select" id="option-1" onClick={() => {setSelectedValue("bl");}}/>
 <input type="radio" name="select" id="option-2" onClick={() => {setSelectedValue("ctr");}} defaultChecked/>
   <label htmlFor="option-1" className="option option-1">
     <div className="dot"/>
      <span>BL</span>
      </label>
   <label htmlFor="option-2" className="option option-2">
     <div className="dot"/>
      <span>Container</span>
   </label>
</div>
      
  {/* <label htmlFor="rad1">
  <input id="rad1" type="radio" name="radio"  onClick={() => {setSecondSelectedValue("import");}} />
  <div className="front-end box">
    <span>Import</span>
  </div>
</label>

  <label htmlFor="rad2">
  <input id="rad2" type="radio" name="radio" onClick={() => {setSecondSelectedValue("export");}} defaultChecked/>
  <div className="back-end box">
    <span>Export</span>
  </div>
</label> */}

</div>
<hr/>
<div className="middle mt-6">
  <hr/>
  <div className="wrapper">
 <input type="radio" name="select2" id="option-3" onClick={() => {setSecondSelectedValue("import");}}/>
 <input type="radio" name="select2" id="option-4" onClick={() => {setSecondSelectedValue("export");}} defaultChecked/>
   <label htmlFor="option-3" className="option option-3">
     <div className="dot"/>
      <span>Import</span>
      </label>
   <label htmlFor="option-4" className="option option-4">
     <div className="dot"/>
      <span>Export</span>
   </label>
</div>
  {/* <label htmlFor="rad3">
  <input id="rad3" type="radio" name="radio2"  onClick={() =>{setSelectedValue("bl")}} defaultChecked/>
  <div className="front-end box">
    <span>BL</span>
  </div>
</label>

  <label htmlFor="rad4">
  <input id="rad4" type="radio" name="radio2"  onClick={() =>{setSelectedValue("ctr")}}/>
  <div className="back-end box">
    <span>Container</span>
  </div>
</label> */}

</div>
<hr/>
      
<button type="button"  onClick={handleTrackShipment}  className=" mt-2 bg-[#217BF4]  hover:bg-blue-700 text-white font-bold py-2 px-4 ml-36 rounded-full">
 Confirm
</button>
      </Modal>
      
    
  
  {/* <div className="flex w-full mt-6"> */}
    {/* <div className="flex w-1/4 rounded-lg overflow-hidden ml-20 ">
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
     
    </div> */}
    {/* <div className="flex justify-between w-1/4 rounded-lg overflow-hidden ml-40">
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
  </div> */}
  
  <div className="  flex
                    items-center justify-center ">
                     
    {/* <h4 className="text-stone-500"><i>{displaytext}</i></h4> */}
    {/* <input
      type="text" id="blno" placeholder="Enter BL/Container No ..."
      className="text-sm text-gray-base w-80 mt-10 
      py-5 px-4 h-2 border 
      border-gray-200 rounded mb-2" 
      value={billOfLadingNumber} onBlur={handleBlur} 
      onChange={(e) => {setBillOfLadingNumber(e.target.value);setError("")}}
    />
 


        <button type="button"
          className="px-4 py-2  rounded  bg-blue-500 text-white"
          onClick={handleTrackShipment} 
        >
          Track Shipment
        </button> */}
         <img src={ship} alt="" className="lg:opacity-100 xs:opacity-25 absolute h-80 w-80 right-0 flex-col mr-20   "/>

    <div className="relative">
     
        <div className="absolute inset-y-0 left-0 flex  items-center pl-3 pointer-events-none">
            <svg aria-hidden="true" className="w-3 h-3  mt-10 text-gray-500 dark:text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/></svg>
        </div>

        <input type="text"   value={billOfLadingNumber} onChange={(e)=>{setBillOfLadingNumber(e.target.value)}}
     id="search" className=" w-96 p-4 mt-10  pl-10 text-sm text-gray-900 border border-gray-300 rounded-lg bg-gray-50 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500" placeholder="Search" required/>


        <button type="submit"   onClick={(e) => {setBillOfLadingNumber(billOfLadingNumber);setError("");handleBlur()}}  className="text-white absolute  right-2.5 bottom-2.5 bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm px-4 py-2 dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800" >Search</button>


    </div>


  </div>
  <h4 className="text-stone-500 text-center mt-2 "><i>Enter BL or Container Number</i></h4>

  {error &&
  <div className="bg-red-100 border border-red-400 mt-20 text-red-700 px-4 py-3 rounded relative" role="alert">
  <strong className="font-bold text-center">Error</strong>
  <br/>
  <span className="block sm:inline text-center">{error}</span>
 
</div>
}
{error2 &&
  <div className="bg-red-100 border border-red-400 mt-20 text-red-700 px-4 py-3 rounded relative" role="alert">
  <strong className="font-bold sm:text-center ">Error</strong>
  <br/>
  <span className="block sm:inline text-center">{error2}</span>
 
</div>
}
  {/* {loading && <p className="ml-40 text-3xl">Loading.... <Bars stroke="#00FF00" strokeOpacity={.500} /></p>} */}


  
<br/>
<br/>
<br/>
  <svg xmlns="http://www.w3.org/2000/svg" className="block" viewBox="0 0 1440 320"><path fill="#a2d9ff" fillOpacity="0.8" d="M0,96L40,80C80,64,160,32,240,53.3C320,75,400,149,480,165.3C560,181,640,139,720,117.3C800,96,880,96,960,106.7C1040,117,1120,139,1200,133.3C1280,128,1360,96,1400,80L1440,64L1440,320L1400,320C1360,320,1280,320,1200,320C1120,320,1040,320,960,320C880,320,800,320,720,320C640,320,560,320,480,320C400,320,320,320,240,320C160,320,80,320,40,320L0,320Z"/>
  <svg xmlns="http://www.w3.org/2000/svg" className="block" viewBox="0 0 1440 320"><path fill="#0099ff" fillOpacity="0.2" d="M0,96L80,122.7C160,149,320,203,480,202.7C640,203,800,149,960,128C1120,107,1280,117,1360,122.7L1440,128L1440,320L1360,320C1280,320,1120,320,960,320C800,320,640,320,480,320C320,320,160,320,80,320L0,320Z"/>
  <svg xmlns="http://www.w3.org/2000/svg" className="block" viewBox="0 0 1440 320"><path fill="#0099ff" fillOpacity="1" d="M0,128L60,154.7C120,181,240,235,360,229.3C480,224,600,160,720,154.7C840,149,960,203,1080,213.3C1200,224,1320,192,1380,176L1440,160L1440,320L1380,320C1320,320,1200,320,1080,320C960,320,840,320,720,320C600,320,480,320,360,320C240,320,120,320,60,320L0,320Z"/></svg>
  </svg>
  </svg>

  </div>
 
 {/* {loading && <p className="ml-40 text-3xl">Loading.... <Bars stroke="#00FF00" strokeOpacity={.500} /></p>}
      {error2 && <p className="ml-20 text-3xl">Error: {error2}</p>}
      {trackingHistory.length > 0 && (
        <div>
        <div className="font-medium text-lg italic p-5  text-center" >Tracking History</div>

      <div className="bg-black text-white rounded-lg overflow-hidden ml-4">

<table className="w-full text-left table-collapse">
<thead>
          <tr className="text-white">
            <th className="p-4 border-b-2 border-gray-800">Date of Arrival</th>
            <th className="p-4 border-b-2 border-gray-800">Port of Discharge</th>
            <th className="p-4 border-b-2 border-gray-800">Vessel Name</th>
            <th className="p-4 border-b-2 border-gray-800">Status</th>
          </tr>
        </thead>
          <tbody>
           
           
           
              <tr>
                <td className="p-4 border-b border-gray-800"> {trackingHistory[0].data.arrival_date}</td>
                <td className="p-4 border-b border-gray-800"> {trackingHistory[0].data.port_of_discharge}</td>

                <td className="p-4 border-b border-gray-800"> {trackingHistory[0].data.vessel_name}</td>

                <td className="p-4 border-b border-gray-800"> {trackingHistory[0].data.status!=="undefined"?"No Status":trackingHistory[0].data.status}</td>

              </tr>
         
          </tbody>
       </table>
       </div>
       </div>
       )} */}
        </div>
)
      }



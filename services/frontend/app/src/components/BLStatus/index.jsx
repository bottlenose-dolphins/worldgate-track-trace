import { useState } from "react";

import { blStatus } from "src/api/user";

import Modal from "react-modal";
import { MagnifyingGlassIcon } from "@heroicons/react/24/outline";
import Button from "react-bootstrap/Button";

import { useNavigate } from "react-router-dom";



import ship from "../../img/ship3d.png";

import "./bl.scss";

export default function BLStatus() {
  const navigate = useNavigate();
 
  const [searchType, setSearchType] = useState("ctr");
  const [trackingHistory, setTrackingHistory] = useState([]);
  const [directionType, setDirectionType] = useState("export");
  const [billOfLadingNumber, setBillOfLadingNumber] = useState("");
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
    console.log(billOfLadingNumber)


    try {
      const response = await blStatus("Yang Ming", billOfLadingNumber, searchType, directionType)

      if (response.status !== 200) {
        throw new Error("No status found");
      }
      else if (response.status === 200) {
        const data = await response.json();
        setTrackingHistory([data]);


        navigate("/Status", { state: { arrival: trackingHistory[0].data.arrival_date, discharge: trackingHistory[0].data.port_of_discharge, vessel: trackingHistory[0].data.vessel_name, status: trackingHistory[0].data.status !== "undefined" ? "No Status" : trackingHistory[0].data.status, bl: billOfLadingNumber, loading: trackingHistory[0].data.port_of_loading, shipline: trackingHistory[0].data.shipping_line } })
      }
    }
    catch (err) {
      navigate("/error", { state: { identifier: billOfLadingNumber, direction: directionType, type: searchType } })
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
    else {
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

  return (

    <div className="justify-center">
        <div className="flex flex-col items-center ml-40">
          <h2 className="text-4xl text-left text-center font-bold mt-20">Tracking your shipment has <br /> never been this easy!</h2>
          {/* Search Bar w/ Button */}
          <div className="relative">
            <span className="absolute inset-y-0 left-0 flex items-center pl-3 pointer-events-none"><MagnifyingGlassIcon className="w-6 h-6 mt-10" /></span>
            <input type="text" value={billOfLadingNumber} onChange={(e) => { setBillOfLadingNumber(e.target.value) }}
              id="search" className=" w-96 h-12 p-4 mt-10 pl-10 text-sm text-gray-900 border border-gray-300 rounded-lg bg-gray-50 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500" placeholder="Search" required />
            <button type="submit" onClick={(e) => { setBillOfLadingNumber(billOfLadingNumber); setError(""); handleBlur() }} className="ml-2 h-12 text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm px-4 py-2 dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800" >
              Search
            </button>
          </div>
          <h4 className="text-stone-500 text-center mt-2"><i>Enter B/L or Container Number</i></h4>
        </div>

        <Modal
          isOpen={modalIsOpen}

          style={customStyles}
          contentLabel="Example Modal"
        >
          <button type="button" className="font-bold mb-2" onClick={closeModal}>X</button>
          <span><h3 className="text-center italic mb-2">Choose Options</h3></span>
          <hr />

          <div className="middle">
            <div className="wrapper">
              <input type="radio" name="select" id="option-1" onClick={() => { setSearchType("bl"); }} />
              <input type="radio" name="select" id="option-2" onClick={() => { setSearchType("ctr"); }} defaultChecked />
              <label htmlFor="option-1" className="option option-1">
                <div className="dot" />
                <span>BL</span>
              </label>
              <label htmlFor="option-2" className="option option-2">
                <div className="dot" />
                <span>Container</span>
              </label>
            </div>
          </div>
          <hr />
          <div className="middle mt-6">
            <hr />
            <div className="wrapper">
              <input type="radio" name="select2" id="option-3" onClick={() => { setDirectionType("import"); }} />
              <input type="radio" name="select2" id="option-4" onClick={() => { setDirectionType("export"); }} defaultChecked />
              <label htmlFor="option-3" className="option option-3">
                <div className="dot" />
                <span>Import</span>
              </label>
              <label htmlFor="option-4" className="option option-4">
                <div className="dot" />
                <span>Export</span>
              </label>
            </div>
          </div>
          <hr />
          <button type="button" onClick={handleTrackShipment} className=" mt-2 bg-[#217BF4]  hover:bg-blue-700 text-white font-bold py-2 px-4 ml-36 rounded-full">
            Confirm
          </button>
        </Modal>

        {error &&
          <div className="bg-red-100 border border-red-400 mt-20 text-red-700 px-4 py-3 rounded relative" role="alert">
            <strong className="font-bold text-center">Error</strong>
            <br />
            <span className="block sm:inline text-center">{error}</span>

          </div>
        }
        {error2 &&
          <div className="bg-red-100 border border-red-400 mt-20 text-red-700 px-4 py-3 rounded relative" role="alert">
            <strong className="font-bold sm:text-center ">Error</strong>
            <br />
            <span className="block sm:inline text-center">{error2}</span>

          </div>
        }

      <img src={ship} alt="" className="hidden lg:block absolute h-72 w-72 2xl:h-1/2 2xl:w-1/4 right-20 top-40 2xl:right-1/5 2xl:top-1/3" />
      <svg xmlns="http://www.w3.org/2000/svg" className="absolute bottom-0 w-screen" viewBox="0 0 1440 250"><path fill="#a2d9ff" fillOpacity="0.8" d="M0,96L40,80C80,64,160,32,240,53.3C320,75,400,149,480,165.3C560,181,640,139,720,117.3C800,96,880,96,960,106.7C1040,117,1120,139,1200,133.3C1280,128,1360,96,1400,80L1440,64L1440,320L1400,320C1360,320,1280,320,1200,320C1120,320,1040,320,960,320C880,320,800,320,720,320C640,320,560,320,480,320C400,320,320,320,240,320C160,320,80,320,40,320L0,320Z" />
        <svg xmlns="http://www.w3.org/2000/svg" className="absolute bottom-0 w-screen" viewBox="0 0 1440 250"><path fill="#0099ff" fillOpacity="0.2" d="M0,96L80,122.7C160,149,320,203,480,202.7C640,203,800,149,960,128C1120,107,1280,117,1360,122.7L1440,128L1440,320L1360,320C1280,320,1120,320,960,320C800,320,640,320,480,320C320,320,160,320,80,320L0,320Z" />
          <svg xmlns="http://www.w3.org/2000/svg" className="absolute bottom-0 w-screen" viewBox="0 0 1440 250"><path fill="#0099ff" fillOpacity="1" d="M0,128L60,154.7C120,181,240,235,360,229.3C480,224,600,160,720,154.7C840,149,960,203,1080,213.3C1200,224,1320,192,1380,176L1440,160L1440,320L1380,320C1320,320,1200,320,1080,320C960,320,840,320,720,320C600,320,480,320,360,320C240,320,120,320,60,320L0,320Z" /></svg>
        </svg>
      </svg>
    </div>
  )
}



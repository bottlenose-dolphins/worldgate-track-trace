import React, { useEffect, useState } from "react";
import { downloadBL, getBLPreviewUrl } from "src/api/blDocument";
import FileSaver from "file-saver";
import Card from "react-bootstrap/Card";
import { DocumentArrowDownIcon, EyeIcon, EyeSlashIcon } from "@heroicons/react/24/outline";
import "./bl.scss";
import { useLocation } from "react-router-dom";
import dateFormat from "dateformat";
import { toast } from "react-toastify";
import locationWhite from "../../img/locationWhite.png";

export default function Status() {
  const location = useLocation();
  const { eta } = location.state;
  const { portOfDischarge } = location.state;
  const { vesselName } = location.state;
  const { blNo } = location.state;
  const { shippingLine } = location.state;
  const { portOfLoading } = location.state;

  const { isFcl } = location.state;
  const { containerReleaseDateTime } = location.state;
  const { deliveryTakenDateTime } = location.state;

  const { status } = location.state;
  const shipmentStatus = !status ? "UNKNOWN STATUS" : status.toUpperCase();

  const { type } = location.state;
  const { direction } = location.state;
  const etaFormatted = dateFormat(eta, "d mmm yyyy");
  function hasShipmentArrived() {
    const todayDateString = new Date().toLocaleDateString("en-ZA");
    const etaConverted = eta.replaceAll("-", "/");
    if (todayDateString > etaConverted) { // YYYY/MM/DD
      return true;
    }
    return false;
  }

  const shipmentStatusColours = {
    "UNKNOWN STATUS": "bg-gray-400",
    "EARLY": "bg-cyan-500",
    "ON TIME": "bg-green-600",
    "DELAYED": "bg-red-600"
  }

  const searchTypes = {
    "bl": "B/L NO",
    "ctr": "CTR NO"
  }

  return (
    <div className="bg-gradient-to-r from-white via-sky-100 to-sky-200 w-screen">
      <div className="grid grid-cols-2 gap-10 p-2">
        <div className="z-40">
          <ShipmentCard eta={etaFormatted} pod={portOfDischarge} vesselName={vesselName} blNo={blNo} />
          <ExpandableDocument identifier={blNo} identifierType={type} direction={direction} />
        </div>

        <div className="p-2 mt-2">
          <h2 className={`text-3xl font-bold text-white w-fit py-1 px-3 rounded-md ${shipmentStatusColours[shipmentStatus]}`}>{shipmentStatus}</h2>
          <div className="grid grid-cols-2 my-7 font-bold text-lg justify-start">
            <h2 className="">{searchTypes[type]}: {blNo}</h2>
            <h1 className="">ETA: {!eta ? "Unknown ETA" : eta}</h1>
          </div>

          <div>
            <ul className="step-progress">
              <li className="step-progress-item is-done">
                <strong>Shipment Departed</strong>
                <br />
                <h2 className="text-xl">{!portOfLoading ? "Unknown POL" : portOfLoading}</h2>
              </li>
              <li className={`step-progress-item ${hasShipmentArrived() ? "is-done" : "current"}`}>
                <strong>Shipment In Progress Via</strong>
                <br />
                <h2 className="text-xl">{!shippingLine ? "Unknown Shipping Line" : shippingLine}</h2>
              </li>
              <li className={`step-progress-item ${hasShipmentArrived() ? (containerReleaseDateTime ? "is-done" : "current") : ""}`}>
                <strong className={`${hasShipmentArrived() ? "" : "text-gray-400"}`}>Shipment Arrived</strong>
                <br />
                <h2 className={`text-xl ${hasShipmentArrived() ? "" : "text-gray-400"}`}>{!portOfDischarge ? "Unknown POD" : portOfDischarge}</h2>
              </li>

              {!isFcl ? "" :
                <>
                  <li className={`step-progress-item ${containerReleaseDateTime ? "current" : ""}`}>
                    <strong className={`${containerReleaseDateTime ? "" : "text-gray-400"}`}>Container Released</strong>
                    <br />
                    <h2 className={`text-xl ${containerReleaseDateTime ? "" : "text-gray-400"}`}>{containerReleaseDateTime || "-"}</h2>
                  </li>
                  <li className={`step-progress-item ${deliveryTakenDateTime ? "current" : ""}`}>
                    <strong className={`${deliveryTakenDateTime ? "" : "text-gray-400"}`}>Customer taken Delivery of Container</strong>
                    <br />
                    <h2 className={`text-xl ${deliveryTakenDateTime ? "" : "text-gray-400"}`}>{deliveryTakenDateTime || "-"}</h2>
                  </li>
                </>}
            </ul>
          </div>
        </div>

      </div>
      <svg xmlns="http://www.w3.org/2000/svg" className="z-0 block" viewBox="0 0 1440 320"><path fill="#a2d9ff" fillOpacity="0.8" d="M0,96L40,80C80,64,160,32,240,53.3C320,75,400,149,480,165.3C560,181,640,139,720,117.3C800,96,880,96,960,106.7C1040,117,1120,139,1200,133.3C1280,128,1360,96,1400,80L1440,64L1440,320L1400,320C1360,320,1280,320,1200,320C1120,320,1040,320,960,320C880,320,800,320,720,320C640,320,560,320,480,320C400,320,320,320,240,320C160,320,80,320,40,320L0,320Z" />
        <svg xmlns="http://www.w3.org/2000/svg" className="block" viewBox="0 0 1440 320"><path fill="#0099ff" fillOpacity="0.2" d="M0,96L80,122.7C160,149,320,203,480,202.7C640,203,800,149,960,128C1120,107,1280,117,1360,122.7L1440,128L1440,320L1360,320C1280,320,1120,320,960,320C800,320,640,320,480,320C320,320,160,320,80,320L0,320Z" />
          <svg xmlns="http://www.w3.org/2000/svg" className="block" viewBox="0 0 1440 320"><path fill="#0099ff" fillOpacity="1" d="M0,128L60,154.7C120,181,240,235,360,229.3C480,224,600,160,720,154.7C840,149,960,203,1080,213.3C1200,224,1320,192,1380,176L1440,160L1440,320L1380,320C1320,320,1200,320,1080,320C960,320,840,320,720,320C600,320,480,320,360,320C240,320,120,320,60,320L0,320Z" /></svg>
        </svg>
      </svg>
    </div>

  );
}

function ShipmentCard({ eta, pod, vesselName, blNo }) {
  return (
    <Card className="h-fit mt-7 2xl:w-5/6" style={{ backgroundColor: "#217BF4", borderRadius: "10px" }}>
      <Card.Body>
        <div className="grid grid-cols-2 text-white p-5">
          <div className="flex flex-col justify-center">
            <Card.Title className="text-4xl justify-start mb-4">{eta}</Card.Title>
            <Card.Subtitle className="text-xl justify-start">{blNo}</Card.Subtitle>
          </div>
          <div className="flex flex-col justify-center">
            <Card.Title className="flex justify-end mb-4" style={{ alignItems: "center" }}>
              <img className="h-10 mr-2" src={locationWhite} alt="shipping-icon" />
              <span>{pod}</span>
            </Card.Title>
            <Card.Subtitle className="text-xl flex justify-end items-end">
              <span className="text-base mr-1">Vessel: </span>
              {vesselName}
            </Card.Subtitle>
          </div>
        </div>
      </Card.Body>
    </Card>
  )
}

function ExpandableDocument({ identifier, identifierType, direction }) { // blNo, type, direction
  const [isPreviewVisible, setIsPreviewVisible] = useState(false);
  const [previewUrl, setPreviewUrl] = useState("");
  const [error, setError] = useState(null);

  useEffect(() => {
    getPreviewUrl();

    async function getPreviewUrl() {
      try {
        // TODO (Charmaine): remove dummy data
        const mockIdentifer = "YMLU3434431";
        const mockIdentifierType = "cont";
        const mockDirection = "export";
        // const res = await getBLPreviewUrl(mockIdentifer, mockIdentifierType, mockDirection);
        const res = await getBLPreviewUrl(identifier, identifierType, direction);

        console.log(res);
        setPreviewUrl(res);
      } catch (err) {
        setError("Error: Failed to retrieve House Bill of Lading document.");
      }
    }
  }, []);

  const handleToggle = () => {
    setIsPreviewVisible(!isPreviewVisible);
  }

  const downloadBLClick = async () => {
    try {
      // TODO (Charmaine): remove dummy data
      const mockIdentifer = "SMU-1234";
      const mockIdentifierType = "bl";
      const mockDirection = "import";
      // const response = await downloadBL(mockIdentifer, mockIdentifierType, mockDirection);
      const response = await downloadBL(identifier, identifierType, direction);

      const blob = new Blob([response], { type: "application/pdf" });
      FileSaver.saveAs(blob, "houseBL.pdf");
      return response;
    } catch (err) {
      console.log(err);
      toast.error(
        "Error: Failed to retrieve House Bill of Lading document.",
      );
      return err;
    }
  }

  return (
    <div className="w-full h-screen">
      <div className="flex items-end mt-6 ml-2">
        <span className="text-lg">House Bill of Lading</span>
        <DocumentArrowDownIcon className="ml-2 w-7 h-7 hover:cursor-pointer" onClick={downloadBLClick} />
        <button type="button" className="ml-1 w-7 h-7" onClick={handleToggle}>
          {isPreviewVisible ? <EyeSlashIcon className="ml-1 w-7 h-7" /> : <EyeIcon className="ml-1 w-7 h-7" />}
        </button>
      </div>
      {error !== null && isPreviewVisible && <div className="mt-4 ml-2 text-red-600">{error}</div>}
      {error == null && isPreviewVisible && <EmbeddedDocument documentUrl={previewUrl} />}
    </div>
  )
}

function EmbeddedDocument({ documentUrl }) {
  return (
    <iframe title="House BL" src={documentUrl} className="mt-3 ml-1 z-50 w-full h-full" />
  )
}


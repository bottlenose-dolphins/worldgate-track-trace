import React, { useState, useMemo } from "react";
import { Card } from "react-bootstrap";
import { ChevronDownIcon, EnvelopeIcon, EnvelopeOpenIcon, DocumentArrowDownIcon, DocumentIcon } from "@heroicons/react/24/outline";
import { searchShipmentStatus } from "src/api/shipment";
import dateFormat from "dateformat";
import { useNavigate } from "react-router-dom";
import FileSaver from "file-saver";
import { downloadBL } from "src/api/blDocument";
import { toast } from "react-toastify";
import locationWhite from "../../img/locationWhite.png";

export default function ViewShipmentComponent({ title, data, setLoading }) {

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
              <ShipmentCard key={index} item={item} index={index} setLoading={setLoading} />
            );
          })}
        </div>

      </div>
    </div>
  )
};

function ShipmentCard({ item, index, setLoading }) {
  const navigate = useNavigate();

  const [mailHovered, setMailHovered] = useState(false);
  const handleMouseEnterMail = () => {
    setMailHovered(true);
  }
  const handleMouseLeaveMail = () => {
    setMailHovered(false);
  }
  const handleMailClick = (e) => {
    e.stopPropagation();
    console.log("MAIL CLICKED");
    const emailSubject = "Enquiries Regarding Shipment Container No. " + item.container_numbers[0];
    const emailBody = `Dear Worldgate,\n\nI would like to enquire about the status of my shipment with container ${item.container_numbers[0]}.\n\n`;
    const emailTo = "wgate@singnet.com.sg";
    const mailToLink = `mailto:${emailTo}?subject=${encodeURIComponent(emailSubject)}&body=${encodeURIComponent(emailBody)}`;
    window.location.href = mailToLink;
  }

  const [bLHovered, setBLHovered] = useState(false);
  const handleMouseEnterBLHovered = () => {
    setBLHovered(true);
  }
  const handleMouseLeaveBLHovered = () => {
    setBLHovered(false);
  }
  const handleDownloadBLClick = async (e) => {
    e.stopPropagation();
    try {
      // TODO (Charmaine): remove dummy data
      const mockIdentifer = "SMU-1234";
      const mockIdentifierType = "bl";
      const mockDirection = "import";
      // const response = await downloadBL(mockIdentifer, mockIdentifierType, mockDirection);
      const response = await downloadBL(item.container_numbers[0], "ctr", item.type);

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

  const shipmentStatusColours = {
    "unknown": "bg-gray-400",
    "early": "bg-green-400",
    "on time": "bg-cyan-500",
    "delayed": "bg-red-400"
  }

  const eta = item.arrival_date ? dateFormat(item.arrival_date, "d mmm yyyy") : dateFormat(item.delivery_date, "d mmm yyyy");
  const status = item.delay_status;

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
            isFcl: result.is_fcl,
            containerReleaseDateTime: result.cont_released,
            deliveryTakenDateTime: result.del_taken,
            shippingLine: result.shipping_line,
            direction: directionType,
            originCords: result.cords,
            destinationCords: result.destination_cords, } })
      }
    }
    catch (err) {
      console.log(err);
      navigate("/error", { state: { identifier: containerNumber, direction: directionType, type: searchType } })
    }
    setLoading(false);

  }

  return (
    <div role="button" className="mb-2" onClick={handleClick} onKeyDown={handleClick} tabIndex={0}>
      <Card className={`mb-2 w-full 2xl:w-4/5 ${shipmentStatusColours[status]}`} style={{ borderRadius: "10px" }} key={index}>
        <Card.Body>
          <div className="grid grid-cols-2 text-white p-4">
            <div className="flex flex-col">
              <Card.Title className="text-4xl justify-start mb-2">{eta}</Card.Title>
              <Card.Subtitle className="text-xl justify-start">{item.container_numbers[0]}</Card.Subtitle>
            </div>
            <div className="flex flex-col">
              <Card.Title className="flex justify-end mb-2" style={{ alignItems: "center" }}>
                <img className="h-10 mr-2" src={locationWhite} alt="shipping-icon" />
                <span>{item.import_destination ? item.import_destination : item.export_destination}</span>
              </Card.Title>
              <Card.Subtitle className="flex justify-end">
                <div className="w-7 h-7 mr-2" onMouseEnter={handleMouseEnterBLHovered} onMouseLeave={handleMouseLeaveBLHovered}>
                  {bLHovered ? <DocumentArrowDownIcon className="w-7 h-7" onClick={handleDownloadBLClick} /> : <DocumentIcon className="w-7 h-7" onClick={handleDownloadBLClick} />}
                </div>
                <div className="w-7 h-7" onMouseEnter={handleMouseEnterMail} onMouseLeave={handleMouseLeaveMail}>
                  {mailHovered ? <EnvelopeOpenIcon className="w-7 h-7" onClick={handleMailClick} /> : <EnvelopeIcon className="w-7 h-7" onClick={handleMailClick} />}
                </div>
              </Card.Subtitle>
            </div>
          </div>
        </Card.Body>
      </Card>
    </div>
  )
}
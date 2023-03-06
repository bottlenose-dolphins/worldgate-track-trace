import React, { useEffect, useState } from "react";
import { Card } from "react-bootstrap";
import { getImportShipments, getExportShipments } from "src/api/shipment";
import { ChevronDownIcon } from "@heroicons/react/24/outline";
import locationWhite from "../../img/locationWhite.png";

export default function ViewShipmentComponent({ title, type }) {
  const [isLatestOnTop, setIsLatestOnTop] = useState(true);
  const [items, setItems] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      if (type === "Import") {
        const importShipments = await getImportShipments();
        setItems(importShipments.slice());
      } else if (type === "Export") {
        const exportShipments = await getExportShipments();
        setItems(exportShipments.slice());
      }
    };
    fetchData();
  }, [type]);

  const handleClick = () => {
    setIsLatestOnTop(!isLatestOnTop);
    setItems(items.slice().reverse());
  };

  return (
    <div className="p-9 w-3/4">
      <h1 className="text-2xl font-medium text-blue-700">{title}</h1>
      <div className="my-auto bg-blue-50 p-4 rounded-lg border border-blue-500">

        <div className="flex justify-between mt-3 mx-1">
          <div className="text-lg font-medium text-blue-700 w-1/2">List View</div>
          <button type="button" className="flex justify-end w-1/2 items-center" onClick={handleClick}>
            <ChevronDownIcon className={`w-6 h-6 text-blue-700 mr-1 ${!isLatestOnTop && "rotate-180"}`} />
            <div className="font-medium text-blue-700 hover:underline">{ isLatestOnTop ? "closest to arrival" : "furthest from arrival" }</div>
          </button>
        </div>

        <div className="flex flex-col mt-5">
          {items.map((item, index) => {
            return (
              <ShipmentCard item={item} index={index} />
            );
          })}
        </div>

      </div>
    </div>
  )
};

function ShipmentCard({ item, index }) {
  return (
    <Card className="mb-2 w-full 2xl:w-3/5" style={{ backgroundColor: "#217BF4", borderRadius: "10px" }} key={index}>
      <Card.Body>
        <div className="grid grid-cols-2 text-white p-4">
          <div className="flex flex-col justify-center">
            <Card.Title className="text-5xl justify-start mb-2">{item.arrival_date ? item.arrival_date.slice(0, 6) : item.delivery_date.slice(0, 6)}</Card.Title>
            <Card.Subtitle className="text-xl justify-start">{item.arrival_date ? item.arrival_date.slice(-4) : item.delivery_date.slice(-4)}</Card.Subtitle>
          </div>
          <div className="flex flex-col justify-center">
            <Card.Title className="flex justify-end mb-2" style={{ alignItems: "center" }}>
              <img className="h-10 mr-2" src={locationWhite} alt="shipping-icon" />
              <span>{item.import_destination ? item.import_destination : item.export_destination}</span>
            </Card.Title>
            <Card.Subtitle className="text-xl flex justify-end">{item.container_numbers}</Card.Subtitle>
          </div>
        </div>
      </Card.Body>
    </Card>
  )
}
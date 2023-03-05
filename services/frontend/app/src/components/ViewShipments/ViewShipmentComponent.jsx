import React, { useEffect, useState } from "react";
import { Card } from "react-bootstrap";
import { getImportShipments, getExportShipments } from "src/api/shipment";
import locationWhite from "../../img/locationWhite.png";
import sortButton from "../../img/sortButton.png";

export default function ViewShipmentComponent(props) {

  const [buttonText, setButtonText] = useState("closest to arrival");
  const { title, type } = props;
  const [items, setItems] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      if (type === "Import") {
        const importShipments = await getImportShipments();
        setItems(importShipments.slice().reverse());
      } else if (type === "Export") {
        const exportShipments = await getExportShipments();
        setItems(exportShipments.slice().reverse());
      }
    };
    fetchData();
  }, [type]);

  const handleClick = () => {
    if (buttonText === "closest to arrival") {
      setButtonText("furthest from arrival");
      setItems(items.slice().reverse());
    }
    else {
      setButtonText("closest to arrival");
      setItems(items.slice().reverse());
    }
  };

  return (
    <div className="p-10">
      <h1 className="text-2xl font-medium text-blue-700">{title}</h1>
      <div className="my-auto bg-light-blue-500 p-4 rounded-lg border border-blue-500 w-1/2">
        <h2 className="mt-6 text-lg font-medium text-blue-700 inline-block">List view</h2>
        <img className="ml-80 inline-block" src={sortButton} alt="sort" /> <button type="button" className="font-medium text-blue-700" onClick={handleClick}>{buttonText}</button>
        <div className="mt-6">
          {items.map((item, index) => {

            return (
              <div>
                <div className="grid grid-cols-2 gap-2">
                  <div className=" p-2 mt-5">

                    <Card style={{ width: "36rem", backgroundColor: "#217BF4", borderRadius: "10px" }} key={index}>
                      <Card.Body>
                        <div className="grid grid-cols-2">
                          <div className="  ">
                            <Card.Title className=" font-sans text-white  text-5xl p-6">{item.arrival_date ? item.arrival_date.slice(0, 6) : item.delivery_date.slice(0, 6)}</Card.Title>
                            <Card.Subtitle className=" text-white text-xl pl-6 pb-6">{item.arrival_date ? item.arrival_date.slice(-4) : item.delivery_date.slice(-4)}</Card.Subtitle>
                          </div>
                          <div>
                            <Card.Title className=" font-sans text-white  p-6" style={{ display: "flex", alignItems: "center" }}>
                              <img className="h-10 ml-20" src={locationWhite} alt="" />
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
  )
};
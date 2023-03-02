import React, { useState } from "react";
import ViewShipmentComponent from "./ViewShipmentComponent";

export default function ToggleTab(){
  const [activeTab, setActiveTab] = useState("Import");

  return (
    <div className="flex flex-col">
      <div className="tabs-header flex">
        <button type="button"
          className={`tab-header-item ${activeTab === "Import" ? "active" : ""} border-t-2 border-r-2 border-l-2 border-gray-400 text-sm font-medium p-4 hover:bg-gray-200 rounded-lg ml-4 mr-4`}
          onClick={() => setActiveTab("Import")}
        >
          Import
        </button>
        <button type="button"
          className={`tab-header-item ${activeTab === "Export" ? "active" : ""} text-sm font-medium p-4 hover:bg-gray-200 border-t-2 border-r-2 border-l-2 border-gray-400 rounded-lg mr-4`}
          onClick={() => setActiveTab("Export")}
        >
          Export
        </button>
        <button type="button"
          className={`tab-header-item ${activeTab === "Upcoming" ? "active" : ""} text-sm font-medium p-4 hover:bg-gray-200 border-t-2 border-r-2 border-l-2 border-gray-400 rounded-lg`}
          onClick={() => setActiveTab("Upcoming")}
        >
          Upcoming
        </button>
      </div>
      <div className="tab-content border border-black w-3/4 ml-4">
        {activeTab === "Import" && <div><ViewShipmentComponent title="Incoming Shipments" type="Import"/></div>}
        {activeTab === "Export" && <div><ViewShipmentComponent title="Outgoing Shipments" type="Export"/></div>}
        {activeTab === "Upcoming" && <div><ViewShipmentComponent title="Upcoming Shipments" type ="Import"/></div>}
      </div>
    </div>
  );
};
import React, { useState } from "react";
import ViewShipmentComponent from "./ViewShipmentComponent";

export default function ToggleTab() {
  const [activeTab, setActiveTab] = useState("Import");

  const tabs = ["Import", "Export", "Upcoming"];

  const renderTabs = tabs.map((tab) => (
    <button type="button"
      className={`${activeTab === `${tab}` ? "font-bold" : "opacity-25"} bg-white border-t border-r border-l border-gray-600 text-sm font-medium px-4 py-2 hover:bg-gray-200 rounded-tl-xl rounded-tr-xl mr-4`}
      onClick={() => setActiveTab(`${tab}`)}
    >
      {tab}
    </button>
  ))

  return (
    <div className="bg-blue-50 w-screen">
      <div className="flex flex-col ml-4 mt-4">
        <div className="tabs-header flex">
          {renderTabs}
        </div>

        <div className="border border-black w-3/4 bg-white">
          {activeTab === "Import" && <div><ViewShipmentComponent title="Incoming Shipments" type="Import" /></div>}
          {activeTab === "Export" && <div><ViewShipmentComponent title="Outgoing Shipments" type="Export" /></div>}
          {activeTab === "Upcoming" && <div><ViewShipmentComponent title="Upcoming Shipments" type="Import" /></div>}
        </div>
      </div>
    </div>
  );
};
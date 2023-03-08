import React, { useEffect, useState } from "react";
import { getExportShipments, getImportShipments } from "src/api/shipment";
import dateFormat from "dateformat";
import ClipLoader from "react-spinners/ClipLoader";
import ViewShipmentComponent from "./ViewShipmentComponent";

export default function ToggleTab() {
  const [activeTab, setActiveTab] = useState("Import");
  const [loading, setLoading] = useState(true);

  const tabs = ["Import", "Export", "Upcoming"];

  const renderTabs = tabs.map((tab, index) => (
    <button key={index} type="button"
      className={`${activeTab === `${tab}` ? "font-bold" : "opacity-25"} bg-white border-t border-r border-l border-gray-600 text-sm font-medium px-4 py-2 hover:bg-gray-200 rounded-tl-xl rounded-tr-xl mr-4`}
      onClick={() => setActiveTab(`${tab}`)}
    >
      {tab}
    </button>
  ))

  const [importShipments, setImportShipments] = useState([]);
  const [exportShipments, setExportShipments] = useState([]);
  const [upcomingShipments, setUpcomingShipments] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      const importShipments = await getImportShipments();
      setImportShipments(importShipments);
      const exportShipments = await getExportShipments();
      setExportShipments(exportShipments);

      const todayDateString = new Date().toLocaleDateString("en-ZA"); // YYYY/MM/DD
      console.log(todayDateString);
      const upcomingShipments = [];
      for (let i = 0; i < importShipments.length; i +=1 ) {
        if (dateFormat(importShipments[i].arrival_date, "yyyy/mm/dd") >= todayDateString) {
          upcomingShipments.push(importShipments[i]);
        } else {
          break;
        }
      }
      for (let i = 0; i < exportShipments.length; i +=1 ) {
        if (dateFormat(exportShipments[i].delivery_date, "yyyy/mm/dd") >= todayDateString) {
          upcomingShipments.push(exportShipments[i]);
        } else {
          break;
        }
      }
      setUpcomingShipments(upcomingShipments); // TODO (Charmaine): Sort by date 
      
      setLoading(false);
    };

    fetchData();
  }, []);

  return (
    <div className="bg-blue-50 w-screen">
      {loading ?
        <div className="flex justify-center items-center h-full">
          <ClipLoader
            color="#217BF4"
            size={60}
            aria-label="Loading Spinner"
            data-testid="loader"
          />
        </div>
        :
        <div className="flex flex-col ml-4 mt-4">
          <div className="tabs-header flex">
            {renderTabs}
          </div>

          <div className="border border-black w-3/4 bg-white">
            {activeTab === "Import" && <div><ViewShipmentComponent title="Incoming Shipments" data={importShipments} setLoading={setLoading} /></div>}
            {activeTab === "Export" && <div><ViewShipmentComponent title="Outgoing Shipments" data={exportShipments} setLoading={setLoading}/></div>}
            {activeTab === "Upcoming" && <div><ViewShipmentComponent title="Upcoming Shipments" data={upcomingShipments} setLoading={setLoading}/></div>}
          </div>
        </div>
      }
    </div>
  );
};
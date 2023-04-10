import React, { useEffect, useState } from "react";
import { getExportShipments, getImportShipments, getSubscriptions } from "src/api/shipment";
import ClipLoader from "react-spinners/ClipLoader";
import { authenticate } from "src/api/config";
import ViewShipmentComponent from "./ViewShipmentComponent";

export default function ToggleTab() {
  const [activeTab, setActiveTab] = useState("Import");
  const [loading, setLoading] = useState(true);

  const tabs = ["Upcoming", "Import", "Export"];

  const renderTabs = tabs.map((tab, index) => (
    <button key={index} type="button"
      className={`${activeTab === `${tab}` ? "font-bold" : "opacity-25"} bg-white border-t border-r border-l border-gray-600 text-sm font-medium px-4 py-2 hover:bg-gray-200 rounded-tl-xl rounded-tr-xl mr-4`}
      onClick={() => setActiveTab(`${tab}`)}
    >
      {tab}
    </button>
  ))

  const [userId, setUserId] = useState("");
  const [importShipments, setImportShipments] = useState([]);
  const [exportShipments, setExportShipments] = useState([]);
  const [upcomingShipments, setUpcomingShipments] = useState([]);
  const [subscriptions, setSubscriptions] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      const userData = await authenticate();
      setUserId(userData.userId);

      const importShipments = await getImportShipments();
      setImportShipments(importShipments);
      const exportShipments = await getExportShipments();
      setExportShipments(exportShipments);
      const subscriptions = await getSubscriptions();
      setSubscriptions(subscriptions.data);

      const todayDateString = new Date().toLocaleDateString("en-ZA"); // YYYY/MM/DD
      const upcomingShipments = [];
      for (let i = 0; i < importShipments.length; i += 1) {
        if (importShipments[i].arrival_date >= todayDateString) {
          upcomingShipments.push(importShipments[i]);
        }
      }
      for (let i = 0; i < exportShipments.length; i += 1) {
        if (exportShipments[i].arrival_date >= todayDateString) {
          upcomingShipments.push(exportShipments[i]);
        }
      }
      setUpcomingShipments(upcomingShipments);

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
            {activeTab === "Upcoming" && <div><ViewShipmentComponent title="Upcoming Shipments" userId={userId} data={upcomingShipments} subscriptions={subscriptions} setSubscriptions={setSubscriptions} setLoading={setLoading} /></div>}
            {activeTab === "Import" && <div><ViewShipmentComponent title="Incoming Shipments" userId={userId} data={importShipments} subscriptions={subscriptions} setSubscriptions={setSubscriptions} setLoading={setLoading} /></div>}
            {activeTab === "Export" && <div><ViewShipmentComponent title="Outgoing Shipments" userId={userId} data={exportShipments} subscriptions={subscriptions} setSubscriptions={setSubscriptions} setLoading={setLoading} /></div>}
          </div>
        </div>
      }
    </div>
  );
};
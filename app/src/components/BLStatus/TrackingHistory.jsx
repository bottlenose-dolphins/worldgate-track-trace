import React from "react";

function TrackingHistoryTable() {
  return (
    <div className="mt-5">
      <p className="ml-20">
        BL Number: <b/>
  
      </p>
    <div className="font-medium text-lg italic p-5  text-center" >Tracking History</div>

    <div className="bg-black text-white rounded-lg overflow-hidden ml-4">
      <table className="w-full text-left table-collapse">
        <thead>
          <tr className="text-white">
            <th className="p-4 border-b-2 border-gray-800">Date</th>
            <th className="p-4 border-b-2 border-gray-800">Port of Discharge</th>
            <th className="p-4 border-b-2 border-gray-800">Date of Arrival</th>
            <th className="p-4 border-b-2 border-gray-800">Vessel Name</th>
            <th className="p-4 border-b-2 border-gray-800">Status</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td className="p-4 border-b border-gray-800">Placeholder</td>
            <td className="p-4 border-b border-gray-800">Placeholder</td>
            <td className="p-4 border-b border-gray-800">Placeholder</td>
            <td className="p-4 border-b border-gray-800">Placeholder</td>
            <td className="p-4 border-b border-gray-800">Placeholder</td>
          </tr>
        </tbody>
      </table>
    </div>
    </div>
  );
}

export default TrackingHistoryTable;

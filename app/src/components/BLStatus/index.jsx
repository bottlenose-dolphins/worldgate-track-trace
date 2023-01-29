import { CCard, CCardBody, CCardImage, CCardText, CCardTitle } from "@coreui/react";
import ship from "../../img/ship.jpeg";
import lod from "../../img/lod.png";
import status from  "../../img/status.png";

export default function BLStatus() {

return(
   <div className="container">

    <form className=" flex items-center mt-20 ml-80" >   
<div className="relative w-80 ">
   
    <label htmlFor="simple-search" className="font-bold text-2xl" >
    Search BL/Container Status
<input type="text" id="simple-search" className=" bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-80 pl-10 p-2.5  dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500" placeholder="Search" required/>
</label></div>
<button type="submit" className=" p-2.5 ml-2 text-sm font-medium text-white bg-blue-700 rounded-lg border border-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800 mt-5">
    <svg className="w-8 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path  strokeLinejoin="round" strokeWidth="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/></svg><span>TRACK</span>
    <span className="sr-only">Search</span>
</button>
</form>
<br/>
  <hr/>
  
        <div className="grid grid-flow-row-dense grid-cols-3 grid-rows-3  ml-80 mt-40">

 
        <CCard style={{ width: "15rem" }}  className="border  " color="primary">
  <CCardImage orientation="top"  src={ship}  />
  <CCardTitle className="font-bold text-center">Vessel Name</CCardTitle>
  <CCardBody>
    <CCardText className="text-center"> Maersk </CCardText>
  </CCardBody>
</CCard>


        <CCard style={{ width: "15rem" }} className="border">
  <CCardImage orientation="top"  src={lod} />
  <CCardTitle className="font-bold text-center">Load of Discharge</CCardTitle>
  <CCardBody>
    <CCardText className="text-center"> India </CCardText>
  </CCardBody>
</CCard>



        <CCard style={{ width: "15rem" }} className="border">
  <CCardImage orientation="top"  src={status} />
  <CCardTitle className="font-bold text-center">Shipment Status</CCardTitle>
  <CCardBody>
    <CCardText className="text-center"> Delivered </CCardText>
    <CCardText className="text-center"><span className="font-bold bg-[#22c55e]"> Arrival Day: 22/11/2022</span> </CCardText>
  </CCardBody>
</CCard>

 
  

</div>

</div>
        
)


}
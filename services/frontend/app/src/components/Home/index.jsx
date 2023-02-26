import { Link, useNavigate } from "react-router-dom";
import React from "react";
import "../../index.css";

export default function Home() {
  const navigate = useNavigate();
  function handleClick() {
    navigate("/sign-up");
  }
  function handleClick2() {
    navigate("/about");
  }
  return (
    <div className="bg-image flex flex-col w-full h-full md:flex-row md:space-x-4 md:space-y-0 mt-5 bg-fixed">
      <div className=' md:w-1/2 lg:w-1/2 ml-40'>
        <h1 className=' sm:text-3xl md:text-8xl lg:text-8xl font-bold text-white mt-48 mb-2'>Keeping track of</h1>
        <h1 className=' sm:text-3xl md:text-8xl lg:text-8xl font-bold text-white mb-2'>your shipment</h1>
        <h1 className=' sm:text-3xl md:text-8xl lg:text-8xl font-bold text-white'>just got easier!</h1>
        <p className='text-2xl mt-10 mb-10 text-white'>Worldgate introduces <span className='font-bold'>Track&Trace</span>,<br /> for <span className='font-bold'>all</span> your shipment needs.</p>
        <div className='flex'>
          <Link to='/sign-up'>
            <button type="button" onClick={handleClick} className='signup-button mt-2 py-2 px-4'>Sign Up</button>
          </Link>
          <Link to='/about'>
            <button type="button" onClick={handleClick2} className='learn-button mx-10 mt-2 py-2 px-4'>Learn More</button>
          </Link>
        </div>
      </div>
    </div>
  );
};
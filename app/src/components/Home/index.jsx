import { Link, useNavigate } from "react-router-dom";
import React from "react";
import Container from "../../img/containers.png";
import Navigation from "../Navigation/Navigation";

export default function Home() {
  const navigate = useNavigate();
  function handleClick() {
      navigate("/sign-up");
  }
  function handleClick2(){
    navigate("/about");
  }
  return (
    <div>
         <Navigation />
   
    <div className='flex bg-white-to-light-blue gradient container mt-5'>
      <div className='w-1/2 mx-5'>
        <h1 className='text-8xl font-bold'>Keeping track of your shipment just got easier!</h1>
        <p className='text-lg mt-5'>Worldgate introduces <span className='font-bold'>Track and Trace</span>,<br/> for <span className='font-bold'>all</span> your shipment needs.</p>
        <div className='flex'>
          <Link to='/signup'>
            <button type="button" onClick={handleClick} className=' mx-5  mt-2 bg-blue-500 text-white py-2 px-4 rounded-md'>Sign Up</button>
          </Link>
          <Link to='/about'>
            <button type="button"  onClick={handleClick2} className=' mx-5 mt-2 text-blue-500 border border-blue-500 py-2 px-4 rounded-md'>Learn More</button>
          </Link>
        </div>
      </div>
      <div className='w-1/2'>
        <img src={Container} alt='' className="h-5/6" />
      </div>
    </div>
    </div>
  );
};



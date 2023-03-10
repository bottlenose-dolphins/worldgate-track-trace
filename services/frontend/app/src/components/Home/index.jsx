import { Link, Navigate, useNavigate } from "react-router-dom";
import "../../index.css";
import Navbar from "src/layout/Navbar";

export default function Home() {
  const username = localStorage.getItem("username");

  if (username !== "" && username !== null) {
    return <Navigate to="blStatus" replace />;
  }

  const navigate = useNavigate();
  function handleClick() {
    navigate("/sign-up");
  }
  function handleClick2() {
    navigate("/about");
  }
  return (
    <div className="bg-image flex flex-col w-full h-full md:space-x-4 md:space-y-0 bg-fixed">
      <Navbar />
      <div className='w-screen lg:w-7/12 2xl:w-1/2 pl-14 2xl:pl-24'>
        <h1 className='lg:leading-tight 2xl:leading-tight text-3xl md:text-6xl lg:text-7xl 2xl:text-8xl font-bold text-white lg:mt-10 2xl:mt-40 mb-2'>Keeping track of your shipments just got easier!</h1>
        <p className='text-2xl lg:my-6 2xl:my-10 text-white'>Worldgate introduces <span className='font-bold'>Track&Trace</span>,<br /> for <span className='font-bold'>all</span> your shipment needs.</p>
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
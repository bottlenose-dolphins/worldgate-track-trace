/* import { Link , useNavigate} from "react-router-dom";
import React from "react";

import Container from "react-bootstrap/Container";
import Nav from "react-bootstrap/Nav";
import Navbar from "react-bootstrap/Navbar";
import logo from "../../img/worldgate.png"; 
import "./navbar.css";

export default function Navigation() {
  const navigate = useNavigate();
    function handleClick() {
        navigate("/sign-up");
    }
  return (
<nav>
      <ul className="list">
        
      <li className="items"> <img src={logo} alt='' className="h-15 "/> </li>
      <li className=""> <span className='text-3xl font-bold -ml-60'>Track&<br/> Trace</span></li>

          <li className="items">Home</li>
          <li className="items">Services</li>
          <li className="items">Contact</li>
        </ul>
      <button type="button" className="btn">BTN</button>
    </nav> */
 /*    <nav className='bg-white flex justify-between items-center mt-2'>
            <img src={logo} alt=''/> 
            <span className='text-3xl font-bold -ml-60'>Track&<br/> Trace</span>
      <ul className='flex justify-end -mr-40'>
        <li className='mx-4 mt-2'><Link to="/" className='mr-4'>Home</Link></li>
        <li className='mx-4 mt-2'><Link to="/back">Back to Worldgate</Link></li>
        <li className='mx-4 mt-2'><Link to="/about">About</Link></li>
       <li > <button type="button" onClick={handleClick}  className='bg-blue-500 text-white py-2 px-4 rounded-md'>Sign Up</button></li>
      </ul>
      <hr />
    </nav> */
 /*  );
}; */
import { useState } from "react";
import { Link , useNavigate} from "react-router-dom";
import logo from "../../img/worldgate.png"; 

export default function NavBar() {
  const navigate = useNavigate();
  function handleClick() {
      navigate("/sign-up");
  }
    const [navbar, setNavbar] = useState(false);

    return (
        <nav className="w-full bg-light-300 shadow">
          
            <div className="justify-between px-4 mx-auto lg:max-w-7xl md:items-center md:flex md:px-8">
            <img src={logo} alt=''/> 
                    <h4 className='text-2xl font-bold inline-block mr-60'>Track & Trace</h4>
                <div>
                    <div className="flex items-center justify-between py-3 md:py-5 md:block">
                   

                        <div className="md:hidden">
                            <button type="button"
                                className="p-2 text-gray-700 rounded-md outline-none focus:border-gray-400 focus:border"
                                onClick={() => setNavbar(!navbar)}
                            >
                                {navbar ? (
                                    <svg
                                        xmlns="http://www.w3.org/2000/svg"
                                        className="w-6 h-6 text-black"
                                        viewBox="0 0 20 20"
                                        fill="currentColor"
                                    >
                                        <path
                                            fillRule="evenodd"
                                            d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z"
                                            clipRule="evenodd"
                                        />
                                    </svg>
                                ) : (
                                    <svg
                                        xmlns="http://www.w3.org/2000/svg"
                                        className="w-6 h-6 text-black"
                                        fill="none"
                                        viewBox="0 0 24 24"
                                        stroke="currentColor"
                                        strokeWidth={2}
                                    >
                                        <path
                                            strokeLinecap="round"
                                            strokeLinejoin="round"
                                            d="M4 6h16M4 12h16M4 18h16"
                                        />
                                    </svg>
                                )}
                            </button>
                        </div>
                    </div>
                </div>
                <div>
                    <div
                        className={`flex-1 justify-self-center pb-3 mt-2 md:block md:pb-0 md:mt-0 ${
                            navbar ? "block" : "hidden"
                        }`}
                    >
                        <ul className="items-center justify-center space-y-8 md:flex md:space-x-6 md:space-y-0">
                            <li className="text-black hover:text-indigo-200">
                            <Link to="/" className='mr-4'>Home</Link>
                            </li>
                            <li className="text-black hover:text-indigo-200">
                            <Link to="/back">Back to Worldgate</Link>                           </li>
                            <li className="text-black hover:text-indigo-200">
                            <Link to="/about">About</Link>                         </li>
                          
                        </ul>

                        <div className="mt-3 space-y-2 lg:hidden md:hidden">
                        <button type="button"  onClick={handleClick}  className='bg-blue-500 text-black py-2 px-4 rounded-md'>Sign Up</button>
                </div>
                    </div>
                </div>
                <div className="hidden space-x-2 md:inline-block">
                <button type="button"  onClick={handleClick} className='bg-blue-500 text-black py-2 px-4 rounded-md'>Sign Up</button>
                </div>
            </div>
        </nav>
    );
}



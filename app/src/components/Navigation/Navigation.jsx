import { Link , useNavigate} from "react-router-dom";
import React from "react";
import logo from "../../img/worldgate.png"; 
import "./navbar.css";

export default function Navigation() {
  const navigate = useNavigate();
    function handleClick() {
        navigate("/sign-up");
    }
  return (
    <nav className='bg-white flex justify-between items-center mt-2'>
            <img src={logo} alt=''/> 
            <span className='text-3xl font-bold -ml-60'>Track&<br/> Trace</span>
      <ul className='flex justify-end -mr-40'>
        <li className='mx-4 mt-2'><Link to="/" className='mr-4'>Home</Link></li>
        <li className='mx-4 mt-2'><Link to="/back">Back to Worldgate</Link></li>
        <li className='mx-4 mt-2'><Link to="/about">About</Link></li>
       <li > <button type="button" onClick={handleClick}  className='bg-blue-500 text-white py-2 px-4 rounded-md'>Sign Up</button></li>
      </ul>
      <hr />
    </nav>
  );
};




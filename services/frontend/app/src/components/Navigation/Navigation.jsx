import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import logo from "../../img/worldgate.png";
import TrackAndTrace from "../../img/TrackAndTrace.png";

export default function NavBar() {
    const navigate = useNavigate();
    function handleClick() {
        navigate("/sign-up");
    }
    const [navbar, setNavbar] = useState(false);

    return (
        <nav className="w-full bg-light-300 shadow">
            <div className="flex h-16 justify-between px-4 mx-auto max-w-7xl sm:px-6 lg:px-8">
                {/* <img width="70" height="70" src={logo} alt='Worldgate Logo' /> */}
                <img className='inline w-15 h-9 my-2' src={TrackAndTrace} alt='Track&Trace logo' />
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
                        className={`flex-1 justify-self-center pb-3 mt-2 md:block md:pb-0 md:mt-0 ${navbar ? "block" : "hidden"
                            }`}
                    >
                        <ul className="items-center justify-center space-y-8 md:flex md:space-x-6 md:space-y-0">
                            <li className="text-black hover:text-indigo-200">
                                <Link to="/" className='mr-4'>Home</Link>
                            </li>
                            <li className="text-black hover:text-indigo-200">
                                <Link to="/back">Back to Worldgate</Link>
                            </li>
                            <li className="text-black hover:text-indigo-200">
                                <Link to="/about">About</Link>
                            </li>
                        </ul>

                        <div className="mt-3 space-y-2 lg:hidden md:hidden">
                            <button type="button" onClick={handleClick} className='bg-blue-500 text-black py-2 px-4 rounded-md'>Sign Up</button>
                        </div>
                    </div>
                </div>
                <div className="hidden space-x-2 md:inline-block">
                    <button type="button" onClick={handleClick} className='bg-blue-500 text-black py-2 px-4 rounded-md'>Sign Up</button>
                </div>
            </div>
        </nav>
    );
}



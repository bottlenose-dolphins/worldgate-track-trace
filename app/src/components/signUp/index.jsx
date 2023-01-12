import { useState } from "react";
import { useNavigate } from 'react-router-dom';
import NameField from "./nameInput";
import EmailField from "./emailInput";
import UserNameField from "./usernameInput";
import PasswordField from "./passwordInput";
import PhoneNumberField from "./phoneInput";
import RegisterButton from "./registerButton";
import SignUpBackground from "../../img/SignUpBackground.png";
import TrackAndTrace from "../../img/TrackAndTrace.png";

export default function SignUp() {
    const navigate = useNavigate();
    function handleClick() {
        navigate('/sign-in');
      }

    return (
        <div className='flex flex-row-reverse bg-[center_left_4rem]' style={{
            backgroundImage: `url(${SignUpBackground})`, backgroundSize: 'contain', backgroundRepeat: 'no-repeat', width: '100vw',
            height: '100vh'
        }} >
            <div className='basis-full lg:basis-4/12 p-4 bg-white bg-opacity-50 sm:p-6 md:p-8 mr-40'>
                <div className='flex flex-row px-4'>
                        <h2 className='basis-1/2 font-medium text-lg mb-5'>
                            Welcome to <img className='inline w-13 h-8 ml-1' src={TrackAndTrace} alt='Track&Trace logo' />
                        </h2>
                        <h2 className='basis-1/2 text-gray-500'>
                        Have an Account? <a href='Sign Up' className='block font-semibold text-blue-400 hover:underline'></a>
                        <button onClick={handleClick}>Sign in</button>
                    </h2>
                </div>
                <h1 className='font-semibold text-4xl my-5 px-4'>Register an Account</h1>
                <div className="grid grid-cols-1 gap-4">
                    <NameField/>
                    <EmailField labelText="Email address" placeholderText="Enter your Email Address"/>
                    <div className="grid grid-cols-2 gap-4">
                        <UserNameField/>
                        <PhoneNumberField/>
                    </div>
                    <PasswordField />
                    <div className="flex justify-end">
                        <RegisterButton />
                    </div>
                    </div>

            </div>
        </div>
    )
}
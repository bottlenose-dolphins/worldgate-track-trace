import React, { useState } from 'react';

const PhoneNumberField = () => {
    const [phoneNumber, setPhoneNumber] = useState('');
    const [isValid, setIsValid] = useState(true);
  
    const singaporePhoneNumberRegex = /^[0-9]{8}$/;
  
    const handleChange = (event) => {
      const newPhoneNumber = event.target.value;
      setPhoneNumber(newPhoneNumber);
      setIsValid(singaporePhoneNumberRegex.test(newPhoneNumber));
    }
  
    return (
      <div>
        <label className='block mb-2 text-md font-medium text-black space-y-2'>Contact Number</label>
        <input 
          type="tel" 
          value={phoneNumber} 
          onChange={handleChange} 
          className='border border-blue-400 font-normal text-black text-sm rounded-lg focus:outline-blue-400 w-full p-2.5 px-4'
          placeholder="Enter your phone number" 
        />
        {!isValid && <div>Invalid Singapore phone number</div>} 
      </div>
    );
  }

export default PhoneNumberField;
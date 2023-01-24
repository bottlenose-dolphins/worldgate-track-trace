import React, { useState } from "react";

export default function PhoneInput({ phone, setPhone }) {

  return (
      <label
          htmlFor='phoneField'
          className='block mb-2 text-md font-medium text-black space-y-2'
      >
          Contact Number
          <input
              type='tel'
              id='phoneField'
              value={phone}
              onChange={(e) => setPhone(e.target.value)}
              className='border border-blue-400 font-normal text-black text-sm rounded-lg focus:outline-blue-400 block w-full p-2.5'
              placeholder='Contact Number'
          />
      </label>
  )
}

// singaporePhoneNumberRegex = /^[0-9]{8}$/;
// setIsValid(singaporePhoneNumberRegex.test(newPhoneNumber));
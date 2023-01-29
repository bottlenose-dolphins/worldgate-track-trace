import React, { useState } from "react";

export default function nameInput({ company, setCompany }) {

  return (
    <label htmlFor="nameField" className="block mb-2 text-md font-medium text-black space-y-2">
      Name
          <input
              type='text'
              id='nameField'
              value={company}
              onChange={(e) => setCompany(e.target.value)}
              className='border border-blue-400 font-normal text-black text-sm rounded-lg focus:outline-blue-400 block w-full p-2.5 px-4'
              placeholder='Enter your name/company name'
          />
      </label>
  )
}
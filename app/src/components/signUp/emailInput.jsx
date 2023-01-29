import React, { useState } from "react";

export default function EmailInput({ email, setEmail }) {

  return (
      <label
          htmlFor='emailField'
          className='block mb-2 text-md font-medium text-black space-y-2'
      >
        Email address
          <input
              type='text'
              id='emailField'
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className='border border-blue-400 font-normal text-black text-sm rounded-lg focus:outline-blue-400 block w-full p-2.5'
              placeholder='Enter your Email Address'
          />
      </label>
  )
}
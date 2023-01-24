import React, { useState } from "react";

export default function PasswordInput({ password, setPassword }) {

  return (
      <label
          htmlFor='password'
          className='block mb-2 text-md font-medium text-black space-y-2'
      >
          Enter your password
          <input
              type='password'
              id='passwordField'
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className='border border-blue-400 font-normal text-black text-sm rounded-lg focus:outline-blue-400 block w-full p-2.5'
              placeholder='Password'
          />
      </label>
  )
}
import React, { useState } from "react";

export default function UsernameInput({ username, setUsername }) {

  return (
      <label
          htmlFor='usernameField'
          className='block mb-2 text-md font-medium text-black space-y-2'
      >
          User name
          <input
              type='text'
              id='usernameField'
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              className='border border-blue-400 font-normal text-black text-sm rounded-lg focus:outline-blue-400 block w-full p-2.5'
              placeholder='Username'
          />
      </label>
  )
}
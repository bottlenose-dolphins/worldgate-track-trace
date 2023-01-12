import React, { useState } from 'react';

const PasswordField = () => {
  const [password, setPassword] = useState('');

  const handleChange = (event) => {
    setPassword(event.target.value);
  }

  return (
    <div>
      <label className='block mb-2 text-md font-medium text-black space-y-2'>Enter your Password</label>
      <input 
        type="password" 
        value={password} 
        onChange={handleChange} 
        className='border border-blue-400 font-normal text-black text-sm rounded-lg focus:outline-blue-400 block w-full p-2.5'
        placeholder="Enter your password" 
      />
    </div>
  );
}

export default PasswordField;
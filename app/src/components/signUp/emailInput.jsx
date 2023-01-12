import React, { useState } from "react";

const EmailField = (props) => {
  const [email, setEmail] = useState("");

  const handleChange = (event) => {
    setEmail(event.target.value);
  }

  return (
    <div>
      <label className='block mb-2 text-md font-medium text-black space-y-2'>{props.labelText}</label>
      <input 
        type="email" 
        value={email} 
        onChange={handleChange} 
        className='border border-blue-400 font-normal text-black text-sm rounded-lg focus:outline-blue-400 block w-full p-2.5'
        placeholder={props.placeholderText}
      />
    </div>
  );
}

export default EmailField;
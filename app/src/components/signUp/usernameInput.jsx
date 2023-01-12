import React, { useState } from "react";

function UsernameField() {
  const [username, setUsername] = useState("");

  const handleChange = (event) => {
    setUsername(event.target.value);
  }

  return (
    <label htmlFor="usernameField" className='block mb-2 text-md font-medium text-black space-y-2'>
      User name
      <input
        id="usernameField"
        type="text"
        value={username}
        onChange={handleChange}
        className='border border-blue-400 font-normal text-black text-sm rounded-lg focus:outline-blue-400 block w-full p-2.5 px-4'
        placeholder="Username"
      />
    </label>
  );
}

export default UsernameField;
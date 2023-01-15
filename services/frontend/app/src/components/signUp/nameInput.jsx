import React, { useState } from "react";

function NameField() {
  const [Name, setName] = useState("");

  const handleChange = (event) => {
    setName(event.target.value);
  }

  return (
    <label htmlFor="nameField" className="block mb-2 text-md font-medium text-black space-y-2">
      Name
      <input
        id="nameField"
        type="text"
        value={Name}
        onChange={handleChange}
        className="border border-blue-400 font-normal text-black text-sm rounded-lg focus:outline-blue-400 block w-full p-2.5 px-4"
        placeholder="Enter your name/company name"
      />
    </label>
  );
}

export default NameField;
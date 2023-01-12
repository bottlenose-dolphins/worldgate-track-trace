import React, { useState } from "react";

function EmailField({ labelText, placeholderText }) {
  const [email, setEmail] = useState("");

  const handleChange = (event) => {
    setEmail(event.target.value);
  }

  return (
      <label htmlFor="emailField" className="block mb-2 text-md font-medium text-black space-y-2">
        {labelText}
        <input
          id="emailField"
          type="email"
          value={email}
          onChange={handleChange}
          className="border border-blue-400 font-normal text-black text-sm rounded-lg focus:outline-blue-400 block w-full p-2.5"
          placeholder={placeholderText}
        />
      </label>
  );
}

export default EmailField;
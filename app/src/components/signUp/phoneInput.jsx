import React, { useState } from "react";

function PhoneNumberField() {
  const [phoneNumber, setPhoneNumber] = useState("");
  const [isValid, setIsValid] = useState(true);

  const singaporePhoneNumberRegex = /^[0-9]{8}$/;

  const handleChange = (event) => {
    const newPhoneNumber = event.target.value;
    setPhoneNumber(newPhoneNumber);
    setIsValid(singaporePhoneNumberRegex.test(newPhoneNumber));
  }

  return (
    <label htmlFor="phoneField" className="block mb-2 text-md font-medium text-black space-y-2">
      Contact Number
      <input
        id="phoneField"
        type="tel"
        value={phoneNumber}
        onChange={handleChange}
        className="border border-blue-400 font-normal text-black text-sm rounded-lg focus:outline-blue-400 w-full p-2.5 px-4"
        placeholder="Contact Number"
      />
      {!isValid && <div className="text-red-900">Invalid Singapore phone number</div>}
    </label>
  );
}

export default PhoneNumberField;
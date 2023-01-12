import React, { useState } from 'react';
import Modal from 'react-modal';

const RegisterButton = ({ handleClick }) => {
    const [modalIsOpen, setModalIsOpen] = useState(false);
  
    return (
    <>
    <button className="mt-5 place-self-end bg-green-600 hover:bg-green-500 text-white font-medium py-2 px-4 rounded-lg justify-end" onClick={() => setModalIsOpen(true)}>
    Sign Up
    </button>
    <Modal
      isOpen={modalIsOpen}
      onRequestClose={() => setModalIsOpen(false)}
      className="bg-white rounded-lg p-8"
      overlayClassName="fixed inset-3 z-50"
    >
      <h2 className="text-lg font-medium">Registration Successful!</h2>
      <p className="text-gray-700">Your account has been created in our system and you are able to use Track & Trace</p>
      <div className="flex justify-end mt-4">
        <button 
          className="bg-blue-500 hover:bg-blue-400 text-white font-medium py-2 px-4 rounded-full"
          onClick={() => setModalIsOpen(false)}
        >
          Confirm
        </button>
          </div>
          </Modal>
          </>
    );
}

export default RegisterButton;
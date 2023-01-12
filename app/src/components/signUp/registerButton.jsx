import React, { useState } from 'react';
import Modal from 'react-modal';

const RegisterButton = ({ handleClick }) => {
    const [modalIsOpen, setModalIsOpen] = useState(false);
  
    return (
    <>
    <button className="mt-5 place-self-end bg-blue-500 hover:bg-blue-400 text-white font-medium py-2 px-4 w-1/4 rounded-lg justify-end" onClick={() => setModalIsOpen(true)}>
    Register
    </button>
    <Modal
    isOpen={modalIsOpen}
    onRequestClose={() => setModalIsOpen(false)}
    >
    <h2>Confirm Registration</h2>
    <p>Are you sure you want to register?</p>
    <div>
    <button onClick={handleClick}>Confirm</button>
    <button onClick={() => setModalIsOpen(false)}>Cancel</button>
    </div>
    </Modal>
    </>
    );
}

export default RegisterButton;
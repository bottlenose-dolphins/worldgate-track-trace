import React, { useState } from 'react';
import MyModal from './registerModal';

const RegisterButton = () => {
  
    const [modalIsOpen, setModalIsOpen] = useState(false);

    const toggleModal = () => {
        setModalIsOpen(!modalIsOpen);
    }
    return (
    <>
    <button className="mt-5 place-self-end bg-blue-500 hover:bg-blue-400 text-white font-medium py-2 px-4 w-1/4 rounded-lg justify-end" onClick={toggleModal}>
    Register
    </button>

    <MyModal isOpen={modalIsOpen} toggleModal={toggleModal}></MyModal>
          </>
    );
}

export default RegisterButton;
import React, { useState } from "react";
import RegisterModal from "./registerModal";

function RegisterButton() {
  
    const [modalIsOpen, setModalIsOpen] = useState(false);

    const toggleModal = () => {
        setModalIsOpen(!modalIsOpen);
    }
    return (
    <>
    <button type="submit" className="mt-5 place-self-end bg-blue-500 hover:bg-blue-400 text-white font-medium py-2 px-4 w-1/4 rounded-lg justify-end" onClick={toggleModal}>
    Register
    </button>

    <RegisterModal isOpen={modalIsOpen} toggleModal={toggleModal} />
          </>
    );
}

export default RegisterButton;
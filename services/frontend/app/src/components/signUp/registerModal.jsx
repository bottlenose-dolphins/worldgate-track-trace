import React from "react";
import Modal from "react-modal";
import modalImg from "../../img/RegisterModalImg.png";

function RegisterModal({ isOpen, toggleModal, handleClick }) {

  return (
    <Modal
      isOpen={isOpen}
      onRequestClose={toggleModal}
      className="w-3/4 h-3/4 mx-auto my-auto flex flex-col items-center justify-center p-4 rounded-lg"
      overlayClassName="fixed inset-0 z-50 bg-white w-3/12 h-1/2 mx-auto my-auto"
      data-modal-backdrop="static"
    >
      {/* children details */}
      <img src={modalImg} alt="registerModal" className="w-24 h-24 rounded-full mt-auto" />
      <h2 className="text-lg font-medium mt-4">Registration Successful</h2>
      <div className="flex justify-center mt-4">
        <button
          type="button"
          className="bg-green-600 hover:bg-green-500 text-white font-medium px-8 py-2 rounded-lg"
          onClick={handleClick}
        >
          Continue to Sign in
        </button>
      </div>
    </Modal>
  );
}

export default RegisterModal;
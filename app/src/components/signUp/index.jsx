import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { signUp } from "src/api/user";
import NameField from "./nameInput";
import EmailField from "./emailInput";
import UsernameField from "./usernameInput";
import PasswordField from "./passwordInput";
import PhoneNumberField from "./phoneInput";
import RegisterButton from "./registerButton";
import RegisterModal from "./registerModal";
import SignUpBackground from "../../img/SignUpBackground.png";
import TrackAndTrace from "../../img/TrackAndTrace.png";

export default function SignUp() {
    const navigate = useNavigate();
    function handleClick() {
        navigate("/sign-in");
    }

    const [email, setEmail] = useState("");
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [phone, setPhone] = useState("");
    const [company, setCompany] = useState("");
    const [error, setError] = useState("");

    const [modalIsOpen, setModalIsOpen] = useState(false);

    const toggleModal = () => {
        setModalIsOpen(!modalIsOpen);
    }

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (company.trim() === "" || email.trim() === "" || username.trim() === "" || phone.trim()==="" || password === "") { //AC 1
            setError("Error: Empty fields detected");
            return;
        }
        const re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
        if (!re.test(String(email).toLowerCase())){ //AC 2
            setError("Error: Email not in the right format");
            return;
        }

        if (password.length < 8){ //AC 4
            setError("Error: Password length too short");
            return;
        }

        const res = await signUp(email, username, password, phone, company);
        if (res.code === 201) {
            toggleModal();
            setError("");
            console.log("success");
            // TODO: Redirect to home page/dashboard
        } else if (res.code !== 500) {
            setError("User already exists in the system");
        } else {
            setError(res.message); // if internal server error
        }
    }

    return (
        <div className='flex flex-row-reverse bg-[center_left_4rem]' style={{
            backgroundImage: `url(${SignUpBackground})`, backgroundSize: "contain", backgroundRepeat: "no-repeat", width: "100vw",
            height: "100vh"
        }} >
            <RegisterModal isOpen={modalIsOpen} toggleModal={toggleModal} />
            <div className='basis-full lg:basis-4/12 p-4 bg-white bg-opacity-50 sm:p-6 md:p-8 mr-40'>
                <div className='flex flex-row px-4'>
                    <h2 className='basis-1/2 font-medium text-lg mb-5'>
                        Welcome to <img className='inline w-13 h-8 ml-1' src={TrackAndTrace} alt='Track&Trace logo' />
                    </h2>
                    <h2 className='basis-1/2 text-gray-500'>
                        Have an Account?
                        <button type="button" onClick={handleClick} className='block font-semibold text-blue-400 hover:underline'>Sign In</button>
                    </h2>
                </div>
                <h1 className='font-semibold text-4xl my-5 px-4'>Register an Account</h1>
                <form onSubmit={handleSubmit}>
                <div className="grid grid-cols-1 gap-4">
                    <NameField company={company} setCompany={setCompany}/>
                    <EmailField email={email} setEmail={setEmail}/>
                    <div className="grid grid-cols-2 gap-4">
                        <UsernameField username={username} setUsername={setUsername}/>
                        <PhoneNumberField phone={phone} setPhone={setPhone}/>
                    </div>
                    <PasswordField password={password} setPassword={setPassword} />
                    <div className="flex justify-end">
                        <RegisterButton />
                    </div>
                </div>
                </form>
                <div className='pt-5 text-red-500'>{ error }</div>
            </div>
        </div>
    )
}
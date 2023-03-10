import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { signIn } from "src/api/user";
import PasswordInput from "./PasswordInput";
import UsernameInput from "./UsernameInput";
import SignInBackground from "../../img/SignInBackground.png";
import TrackAndTrace from "../../img/TrackAndTrace.png";

export default function SignIn() {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");

    const [error, setError] = useState("");
    const navigate = useNavigate();
    function handleClick() {
        navigate("/sign-up");
    }

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (username.trim() === "" || password === "") {
            setError("Error: Empty fields detected");
            return;
        }
        const res = await signIn(username, password);
        if (res.code === 200) {
            setError("");
            localStorage.setItem("username", res.username);
            navigate("/view-shipments");
        } else if (res.code !== 500) {
            setError("Incorrect username/email address or password");
        } else {
            setError(res.message); // if internal server error
        }
    }

    return (
        <div className='flex flex-row-reverse bg-[center_left_4rem]' style={{
            backgroundImage: `url(${SignInBackground})`, backgroundSize: "contain", backgroundRepeat: "no-repeat", width: "100vw",
            height: "100vh"
        }} >
            <div className='basis-full lg:basis-5/12 p-4 bg-white bg-opacity-50 sm:p-6 md:p-8'>
                <div className='flex flex-row px-4'>
                    <h2 className='basis-1/2 font-medium text-lg mb-5'>
                        Welcome to <img className='inline w-13 h-8 ml-1' src={TrackAndTrace} alt='Track&Trace logo' />
                    </h2>
                    <h2 className='basis-1/2 text-gray-500'>
                        No account?
                        <button type="button" onClick={handleClick} className='block font-semibold text-blue-400 hover:underline'>Sign Up</button>
                    </h2>
                </div>
                <h1 className='font-semibold text-4xl my-5 px-4'>Sign In</h1>
                <form onSubmit={handleSubmit} className='flex flex-col px-4 pt-10 w-full lg:w-3/4'>
                    <div className="mb-6">
                        <UsernameInput username={username} setUsername={setUsername} />
                    </div>
                    <div className="mb-6">
                        <PasswordInput password={password} setPassword={setPassword} />
                    </div>
                    <button
                        type='submit'
                        className='mt-4 text-white place-self-end bg-blue-500 hover:bg-blue-400 font-medium rounded-lg text-md w-full sm:w-auto px-8 py-2 text-center'
                    >
                        Sign In
                    </button>
                </form>
                <div className='pt-2 text-sm text-red-500'>{error}</div>
            </div>
        </div>
    )
}
export default function UsernameInput({ username, setUsername }) {

    return (
        <label
            htmlFor='username'
            className='block mb-2 text-md font-medium text-black space-y-2'
        >
            <p>Enter your username or email address</p>
            <input
                type='text'
                id='username'
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                className='border border-blue-400 font-normal text-black text-sm rounded-lg focus:outline-blue-400 block w-full p-2.5'
                placeholder='Username/Email Address'
            />
        </label>
    )
}

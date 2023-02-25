const { REACT_APP_API_BASE_ENDPOINT } = process.env;

// export const USER_ENDPOINT = `${REACT_APP_API_BASE_ENDPOINT}/user`;
export const USER_ENDPOINT = "http://127.0.0.1:5002/user"

// to extract csrf_access_token, which should then be put into request header ("X-CSRF-TOKEN")
export function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) {
        const cookie = parts.pop().split(";").shift();
        console.log(cookie);
        return cookie;
    }
    return null;
}
// USAGE EXAMPLE:
// const res = await axios.get("<ENDPOINT_URL>", {
//     withCredentials: true,
//     headers: {
//         "X-CSRF-TOKEN": getCookie("csrf_access_token")
//     }
// });
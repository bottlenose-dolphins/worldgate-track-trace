// local container solution does not work
export const { REACT_APP_USER_ENDPOINT } = process.env;
export const { REACT_APP_VIEW_ALL_SHIPMENT_ENDPOINT } = process.env;
export const { REACT_APP_COMPLEX_SCRAPER_ENDPOINT } = process.env;

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
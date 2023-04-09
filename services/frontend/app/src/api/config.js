import axios from "axios";

const { REACT_APP_API_ENDPOINT } = process.env;

export const USER_ENDPOINT = `http://${REACT_APP_API_ENDPOINT}:5002/user`;
export const COMPLEX_SCRAPER_ENDPOINT = `http://${REACT_APP_API_ENDPOINT}:5009`;
export const VIEW_ALL_SHIPMENTS_ENDPOINT = `http://${REACT_APP_API_ENDPOINT}:5010`;
export const NOTIFICATION_COMPLEX_ENDPOINT = `http://${REACT_APP_API_ENDPOINT}:5018`;
export const SHIPMENT_UNLOADING_STATUS_ENDPOINT = `http://${REACT_APP_API_ENDPOINT}:5013`;
export const BL_DOCUMENT_ENDPOINT = `http://${REACT_APP_API_ENDPOINT}:5014/bl_doc`;

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

export const authenticate = async() => {
    const res = await axios.get(`${USER_ENDPOINT}/verify`, {
        withCredentials: true,
        headers: {
            "X-CSRF-TOKEN": getCookie("csrf_access_token")
        }
    });
    return res.data;
}

// USAGE EXAMPLE:
// const res = await axios.get("<ENDPOINT_URL>", {
//     withCredentials: true,
//     headers: {
//         "X-CSRF-TOKEN": getCookie("csrf_access_token")
//     }
// });
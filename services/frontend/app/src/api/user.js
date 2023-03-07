import axios from "axios";
import { USER_ENDPOINT } from "./config";

const axiosUserInstance = axios.create({
    withCredentials: true,
    baseURL: USER_ENDPOINT,
    timeout: 5000,
});

export const signIn = async (username, password) => {
    try {
        const res = await axiosUserInstance.post("/signin", {
            "username": username,
            "password": password
        });
        if (res) {
            return res.data;
        }
        throw new Error("No data returned from backend");
    } catch (error) {
        return error.response.data;
    }
}

export const signOut = async () => {
    try {
        const res = await axiosUserInstance.post(`${USER_ENDPOINT}/signout`);
        if (res) {
            return res.data;
        }
        throw new Error("No data returned from backend");
    } catch (error) {
        return error.response.data;
    }
}

// original
// email: <str:email>, name: <str:name>, password: <str:password> , phone: <int:phone>, company: <str:company>
export const signUp = async (username, email, password, phone, company) => {
    try {
        const res = await axios.post(`${USER_ENDPOINT}/signup`, {
            "username": username,
            "email": email,
            "password": password,
            "phone": phone,
            "company": company
        });
        if (res) {
            return res.data;
        }
        throw new Error("No data returned from backend");
    } catch (error) {
        return error.response.data;
    }
}

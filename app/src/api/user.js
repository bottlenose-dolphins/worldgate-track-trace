import axios from "axios";
import { USER_ENDPOINT } from "./config";

export const signIn = async(username, password) => {
    try {
        const res = await axios.post(`${USER_ENDPOINT}/signin`, {
            "username": username,
            "password": password
        }, {
            withCredentials: true
        });
        if (res) {
            return res.data;
        }
        throw new Error("No data returned from backend");
    } catch (error) {
        return error.response.data;
    }
}
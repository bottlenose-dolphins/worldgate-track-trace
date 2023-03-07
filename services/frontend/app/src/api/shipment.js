import axios from "axios";
import { VIEW_ALL_SHIPMENTS_ENDPOINT, authenticate } from "./config";

export const getImportShipments = async () => {
    try {
        const authRes = await authenticate();
        if (authRes.code === 200) {
            const userId = authRes.userId;
            const res = await axios.post(`${VIEW_ALL_SHIPMENTS_ENDPOINT}/getImportContainerNum`, {
                "wguser_id": userId
            });
            if (res) {
                if (Array.isArray(res.data)) {
                    return res.data;
                }
                return []; // no shipments under this current user

            }
            throw new Error("No data returned from backend");
        }
        throw new Error("Request Unauthorised");
    }
    catch (error) {
        return error.response.data;
    }
}

export const getExportShipments = async () => {
    try {
        const authRes = await authenticate();
        if (authRes.code === 200) {
            const userId = authRes.userId;
            const res = await axios.post(`${VIEW_ALL_SHIPMENTS_ENDPOINT}/getExportContainerNum`, {
                "wguser_id": userId
            });
            if (res) {
                if (Array.isArray(res.data)) {
                    return res.data;
                }
                return []; // no shipments under this current user
            }
            throw new Error("No data returned from backend");
        }
        throw new Error("Request Unauthorised");
    }
    catch (error) {
        return error.response.data;
    }
}
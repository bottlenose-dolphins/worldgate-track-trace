import axios from "axios";
import { VIEW_ALL_SHIPMENTS_ENDPOINT, COMPLEX_SCRAPER_ENDPOINT,NOTIFICATION_COMPLEX_ENDPOINT, authenticate } from "./config";

const axiosShipmentsInstance = axios.create({
    baseURL: VIEW_ALL_SHIPMENTS_ENDPOINT,
    timeout: 10000,
});

const axiosComplexInstance = axios.create({
    baseURL: COMPLEX_SCRAPER_ENDPOINT,
    timeout: 20000,
});

const axiosNotificationInstance = axios.create({
    baseURL: NOTIFICATION_COMPLEX_ENDPOINT,
    timeout: 30000,
});

export const searchShipmentStatus = async(identifier, identifierType, direction) => {
    try {
        const authRes = await authenticate();
        if (authRes.code === 200) {
            const res = await axiosComplexInstance.post("/scrape", {
                "identifier": identifier,
                "identifier_type": identifierType,
                "direction": direction
            });
            if (res) {
                return res.data;
            }
            throw new Error("No data returned from backend");
        }
        throw new Error("Request Unauthorised");
    } catch (error) {
        console.log(error.response.data.message);
        return error.response.data;
    }
}
export const addsubscription = async(userid, containerid, status) => {
    try {
        const authRes = await authenticate();
        if (authRes.code === 200) {
            const res = await axiosNotificationInstance.post("/addsubscription", {
                "userid": userid,
                "containerid": containerid,
                "status": status
            });
            if (res) {
                return res.data;
            }
            throw new Error("No data returned from backend");
        }
        throw new Error("Request Unauthorised");
    } catch (error) {
        console.log(error.response.data.message);
        return error.response.data;
    }
}
export const deletesubscription = async( containerid) => {
    try {
        const authRes = await authenticate();
        if (authRes.code === 200) {
            const res = await axiosNotificationInstance.post("/deletesubscription", {
              
                "containerid": containerid
               
            });
            if (res) {
                return res.data;
            }
            throw new Error("No data returned from backend");
        }
        throw new Error("Request Unauthorised");
    } catch (error) {
        console.log(error.response.data.message);
        return error.response.data;
    }
}

export const getImportShipments = async() => {
    try {
        const authRes = await authenticate();
        if (authRes.code === 200) {
            const userId = authRes.userId;
            const res = await axiosShipmentsInstance.post("/getImportContainerNum", {
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
    } catch (error) {
        console.log(error.response.data);
        return [];
    }
}

export const getExportShipments = async() => {
    try {
        const authRes = await authenticate();
        if (authRes.code === 200) {
            const userId = authRes.userId;
            const res = await axiosShipmentsInstance.post("/getExportContainerNum", {
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
    } catch (error) {
        console.log(error.response.data);
        return [];
    }
}
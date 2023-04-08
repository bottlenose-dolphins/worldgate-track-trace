import axios from "axios";
import { VIEW_ALL_SHIPMENTS_ENDPOINT, COMPLEX_SCRAPER_ENDPOINT, SHIPMENT_UNLOADING_STATUS_ENDPOINT, authenticate } from "./config";

const axiosShipmentsInstance = axios.create({
    baseURL: VIEW_ALL_SHIPMENTS_ENDPOINT,
    timeout: 10000,
});

const axiosComplexInstance = axios.create({
    baseURL: COMPLEX_SCRAPER_ENDPOINT,
    timeout: 20000,
});

const axiosShipmentUnloadingInstance = axios.create({
    baseURL: SHIPMENT_UNLOADING_STATUS_ENDPOINT,
    timeout: 10000
})

export const searchShipmentStatus = async (identifier, identifierType, direction) => {
    try {
        const authRes = await authenticate();
        if (authRes.code === 200) {
            const res = await axiosComplexInstance.post("/scrape", {
                "identifier": identifier,
                "identifier_type": identifierType,
                "direction": direction
            });
            const unloadingStatus = await searchShipmentUnloadingStatus(identifier, identifierType, direction);
            if (res) {
                if (unloadingStatus) {
                    res.data.data.is_fcl = true
                    res.data.data.cont_released = unloadingStatus.cont_released
                    res.data.data.del_taken = unloadingStatus.del_taken
                } else {
                    res.data.data.is_fcl = false
                }
                console.log(res.data);
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

const searchShipmentUnloadingStatus = async (identifier, identifierType, direction) => {
    try {
        const res = await axiosShipmentUnloadingInstance.post("/unloading_status", {
            "identifier": identifier,
            "identifier_type": identifierType,
            "direction": direction
        });
        if (res.data.code === 200) {
            if (res.data.data) {
                return res.data.data;
            }
            return null; // if not FCL
        }
        throw new Error("No data returned from backend");
    } catch (error) {
        console.log(error.response.data.message);
        return error.response.data;
    }
}

export const getImportShipments = async () => {
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
    }
    catch (error) {
        console.log(error.response.data);
        return [];
    }
}

export const getExportShipments = async () => {
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
import axios from "axios";
import { COMPLEX_SCRAPER_ENDPOINT, authenticate } from "./config";

export const searchShipmentStatus = async(shippingLine, identifier, identifierType, direction) => {
    try {
        const authRes = await authenticate()

        if (authRes.code === 200) {
            const res = await axios.post(`${COMPLEX_SCRAPER_ENDPOINT}/scrape`, {
                "shipping_line": shippingLine,
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
        return error.response.data;
    }
}
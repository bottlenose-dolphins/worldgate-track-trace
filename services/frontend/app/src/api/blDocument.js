import axios from "axios";
import { BL_DOCUMENT_ENDPOINT } from "./config";

// {
//     "identifier": "SMU-1234",
//     "identifier_type": "bl",
//     "direction": "import"
// }
export const downloadBL = async (identifier, identifierType, direction) => {
    try {
        const res = await axios.post(`${BL_DOCUMENT_ENDPOINT}/download`, {
            "identifier": identifier,
            "identifier_type": identifierType,
            "direction": direction
        }, {
            responseType: "arraybuffer"
        });
        if (res) {
            return res.data;
        }
        throw new Error("No data returned from backend");
    } catch (error) {
        console.log(error.response.data.message);
        return error.response.data;
    }
}

// {
//     "identifier": "YMLU3434431",
//     "identifier_type": "cont",
//     "direction": "export"
// }
export const getBLPreviewUrl = async (identifier, identifierType, direction) => {
    try {
        const res = await axios.post(`${BL_DOCUMENT_ENDPOINT}/embed`, {
            "identifier": identifier,
            "identifier_type": identifierType,
            "direction": direction
        });
        if (res) {
            return res.data; // string
        }
        throw new Error("No data returned from backend");
    } catch (error) {
        return error.response.data;
    }
}

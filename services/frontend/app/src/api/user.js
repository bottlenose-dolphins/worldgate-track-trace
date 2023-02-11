import axios from "axios";
import { USER_ENDPOINT } from "./config";

// used for service discovery
// const { ServiceDiscovery } = require("@aws-sdk/client-servicediscovery")

// const  serviceDiscovery = new ServiceDiscovery({region:"ap-southeast-1"});

// original
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

// // with service discovery call, call can only be performed in VPC
// export const signIn = async(username, password) => {
//     const instances = await serviceDiscovery.discoverInstances({
//         HealthStatus: "HEALTHY", 
//         MaxResults: 10, 
//         NamespaceName: "tracktrace", 
//         ServiceName: "core_user_service"
//     })
//     try {
//         const res = await axios.post(`${instances.Instances[Math.floor(Math.random() * instances.Instances.length)].Attributes.AWS_INSTANCE_IPV4}/signin`,{
//             "username": username,
//             "password": password
//         }, {
//             withCredentials: true
//         });
//         if (res) {
//             return res.data;
//         }
//         throw new Error("No data returned from backend");
//     } catch (error) {
//         return error.response.data;
//     }
// }

// email: <str:email>, name: <str:name>, password: <str:password> , phone: <int:phone>, company: <str:company>
export const signUp = async(username, email, password, phone, company) => {
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
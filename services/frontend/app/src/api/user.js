import axios from "axios";
// import { USER_ENDPOINT } from "./config";

// used for service discovery
const { ServiceDiscovery } = require("@aws-sdk/client-servicediscovery")

const  serviceDiscovery = new ServiceDiscovery({region:"ap-southeast-1"});

// original 
export const signIn = async(username, password) => {
    try { 
        // const res = await axios.post(`${USER_ENDPOINT}/signin`, {
            const res = await axios.post("http://13.212.171.88/signin", {
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
//     // console.log("*** user attempted sign in")
//     // const instances = await serviceDiscovery.discoverInstances({
//     //     "HealthStatus": "HEALTHY", 
//     //     "MaxResults": 10, 
//     //     "NamespaceName": "tracktrace", 
//     //     "ServiceName": "core_user"
//     // })
//     // console.log("*** async call to obtain users made")
//     try {
//         // console.log("*** entered try loop")
//         // const res = await axios.post(`${instances.Instances[Math.floor(Math.random() * instances.Instances.length)].Attributes.AWS_INSTANCE_IPV4}/signin`,{
//             const res = await axios.post("http://172.31.32.115/signin",{
//         "username": username,
//             "password": password
//         }, {
//             withCredentials: true
//         });

//         // console.log("*** post request made with credentials")
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
    const instances = await serviceDiscovery.discoverInstances({
        "HealthStatus": "HEALTHY", 
        "MaxResults": 10, 
        "NamespaceName": "tracktrace", 
        "ServiceName": "core_user"
    })
    try {
        const res = await axios.post(`${instances.Instances[Math.floor(Math.random() * instances.Instances.length)].Attributes.AWS_INSTANCE_IPV4}/signup`, {
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
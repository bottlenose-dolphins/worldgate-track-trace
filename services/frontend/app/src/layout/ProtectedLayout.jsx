import { useEffect, useState } from "react";
import { Navigate, Outlet } from "react-router-dom";
import NavbarUser from "./NavbarUser";
import SideBar from "./SideBar";

export default function ProtectedLayout({ redirectPath = "/sign-in" }) {
    const [username, setUsername] = useState("");

    useEffect(() => { // TODO: refactor.
        const usernameValue = localStorage.getItem("username");
        if (typeof usernameValue !== "undefined" && usernameValue && usernameValue !== "") {
            setUsername(usernameValue);
        }
    })

    if (localStorage.getItem("username") === "" || localStorage.getItem("username") === null) {
        return <Navigate to={redirectPath} replace />;
    }

    return (
        <>
            <NavbarUser username={username} />
            <div className="flex">
                <SideBar />
                <Outlet />
            </div>
        </>
    );
}
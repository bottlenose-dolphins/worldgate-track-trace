import { Navigate, Outlet } from "react-router-dom";
import NavbarUser from "./NavbarUser";
import SideBar from "./SideBar";

export default function ProtectedLayout({ redirectPath = "/sign-in" }) {
    const username = localStorage.getItem("username");

    if (username === "" || username === null) {
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
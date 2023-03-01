import { Navigate, Outlet } from "react-router-dom";
import Navbar from "./Navbar";

export default function Layout({ redirectPath = "/blStatus" }) {
  const username = localStorage.getItem("username");

  if (username !== "" && username !== null) {
    return <Navigate to={redirectPath} replace />;
  }

  return (
    <>
      <Navbar />
      <Outlet />
    </>
  );
  
}
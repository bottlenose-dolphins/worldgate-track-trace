import { useState } from "react";
import { Link } from "react-router-dom";
import { ChevronDoubleLeftIcon } from "@heroicons/react/24/outline";

import search from "../img/search.png";
import vessel from "../img/vessel.png";

export default function SideBar() {
    const [open, setOpen] = useState(true);

    const [currentPage, setCurrentPage] = useState("");

    const pageNavigation = [
        {
            icon: vessel,
            name: "My Shipments",
            href: "/view-shipments"
        },
        {
            icon: search,
            name: "Track",
            href: "/blstatus" // TODO: Need Rohan to rename this path
        },
    ]

    const renderSideBarItems = pageNavigation.map((routingItem) => (
        <Link
            to={routingItem.href}
            key={routingItem.name}
            className={`flex items-center text-black text-lg ml-3 gap-x-2 px-2 py-4 hover:underline font-medium
            ${isCurrent(routingItem.href) ? "font-bold" : ""}`}
            aria-current={isCurrent(routingItem.href) ? "page" : undefined}
            onClick={() => setCurrentPage(routingItem.href)}
        >
            <img className={`h-5 w-5 ${open ? "" : "hover:scale-125 transform-gpu"}`} src={routingItem.icon} alt="" />
            <span className={`${!open && "hidden"} origin-left duration-100`}>{routingItem.name}</span>
        </Link>
    ));

    return (
        <aside className={`${open ? "w-48" : "w-16"} duration-200 h-screen bg-white border-r border-gray-300 relative`}>
            <div className="flex flex-col pt-5 justify-center">
                {renderSideBarItems}
            </div>
            <ChevronDoubleLeftIcon className={`absolute -right-3 bottom-20 bg-white cursor-pointer 
            rounded-full outline outline-1 outline-gray-400 p-1 h-7 w-7 ${!open && "rotate-180"}`}
                onClick={() => setOpen(!open)} />
        </aside>
    )
}

function isCurrent(href) {
    const currentUrl = document.location.toString().split("/");
    const page = `/${currentUrl[currentUrl.length - 1]}`;
    if (page === href) {
        return true;
    }
    return false;
}
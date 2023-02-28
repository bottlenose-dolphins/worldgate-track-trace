import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { toast } from "react-toastify";

import { Disclosure, Menu, Transition } from "@headlessui/react";
import { Bars3Icon, XMarkIcon, BellIcon } from "@heroicons/react/24/outline";

import { signOut } from "src/api/user";
import TrackAndTrace from "../img/TrackAndTrace.png";

export default function NavbarUser({ username }) {
    const [pageNavigation, setPageNavigation] = useState([
        { name: "Back to Worldgate", href: "https://www.worldgate.com.sg" },
    ]);

    const renderDisclosureNavbarItems = pageNavigation.map((item) => (
        <Disclosure.Button
            key={item.name}
            as='a'
            href={item.href}
            target={item.href.charAt(0) === "/" ? "_self" : "_blank"}
            className="text-gray-500 font-semibold hover:text-gray-700 block px-3 py-2 rounded-md text-base font-medium"
        >
            {item.name}
        </Disclosure.Button>
    ));

    return (
        <Disclosure as='nav' className='bg-white'>
            {({ open }) => (
                <>
                    <div className='flex h-16 justify-between mx-auto max-w-full px-6 sm:px-6 lg:px-8'>
                        <img className='inline w-15 h-9 my-3' src={TrackAndTrace} alt='Track&Trace logo' />
                        <div className='inline-flex items-center flex-row-reverse md:flex-row space-x-3 lg:space-x-5'>
                            <RoutingItems open={open} pageNavigation={pageNavigation} />
                            {/* <BellIcon className='text-gray-500 hover:text-gray-700 h-6 w-6' /> */}
                            <WelcomeUsername username={username} />
                            <BellIcon className='text-gray-500 hover:text-gray-700 block h-6 w-6' />
                            {/* <RoutingItems open={open} pageNavigation={pageNavigation} /> */}
                        </div>
                    </div>
                    <Disclosure.Panel className='md:hidden'>
                        <div className='space-y-1 px-2 pt-2 pb-3 sm:px-3'>{renderDisclosureNavbarItems}</div>
                    </Disclosure.Panel>
                </>
            )}
        </Disclosure>
    );
}

function RoutingItems({ open, pageNavigation }) {
    return (
        <>
            <MobileNavbarItems open={open} />
            <DesktopNavbarItems pageNavigation={pageNavigation} />
        </>
    );
}

function MobileNavbarItems({ open }) {
    useNavigate();
    return (
        <div className='flex'>
            <div className='mx-2 flex space-x-3 items-center md:hidden'>
                <Disclosure.Button className='inline-flex items-center justify-center rounded-md p-2 ml-2
                text-gray-500 hover:text-gray-700 outline outline-gray-400 focus:outline-none focus:ring-2 focus:ring-inset'>
                    <span className='sr-only'>Open main menu</span>
                    {open ? (
                        <XMarkIcon className='block h-6 w-6' aria-hidden='true' />
                    ) : (
                        <Bars3Icon className='block h-6 w-6' aria-hidden='true' />
                    )}
                </Disclosure.Button>
            </div>
        </div>
    );
}

function DesktopNavbarItems({ pageNavigation }) {
    const [currentPage, setCurrentPage] = useState("");

    useNavigate();
    const renderNavbarItems = pageNavigation.map((routingItem) => (
        routingItem.href.charAt(0) === "/" ?
            <Link
                to={routingItem.href}
                key={routingItem.name}
                className="text-gray-500 font-semibold hover:text-gray-700 drop-shadow-2xl shadow-gray-800 text-sm font-medium"
                onClick={() => setCurrentPage(routingItem.href)}
            >
                {routingItem.name}
            </Link> :
            <a
                href={routingItem.href}
                target="_blank"
                rel="noreferrer"
                className="text-gray-500 font-semibold hover:text-gray-700 drop-shadow-2xl shadow-gray-800 text-sm font-medium"

            >
                {routingItem.name}
            </a>
    ));

    return (
        <div className="hidden md:flex md:justify-between md:space-x-5">
            <div className='relative inline-flex items-center'>
                {renderNavbarItems}
            </div>
        </div>
    );
}

function WelcomeUsername({ username }) {
    const navigate = useNavigate();

    const handleSignOut = async (e) => {
        e.preventDefault();
        const res = await signOut();
        if (res.code === 200) {
            localStorage.removeItem("username");
            navigate("/");
            toast.success("Sign Out successful");
        } else {
            toast.error(
                "An unknown error occurred - please try again.",
            );
        }
    }

    return (
        <Menu as="div" className="relative">
            <Menu.Button className="hover:text-gray-500">
                <div className="text-sm">Welcome,</div>
                <div className="font-bold text-lg">{username}</div>
            </Menu.Button>
            <Menu.Items className="absolute right-0 mt-1 w-40 divide-y divide-gray-100 rounded-md bg-white shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none">
                <div className="px-1 py-1">
                    <Menu.Item>
                        <button type="button" onClick={handleSignOut} className="group flex w-full items-center rounded-md px-2 py-2 text-sm text-gray-500 hover:text-black">Sign Out</button>
                    </Menu.Item>
                </div>
            </Menu.Items>
        </Menu>
    )
}
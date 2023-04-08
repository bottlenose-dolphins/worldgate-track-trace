import { GoogleMap, LoadScript, MarkerF } from "@react-google-maps/api";
import shippingIcon from "../../img/freight.png";

const { REACT_APP_GMAPS_KEY } = process.env;

const containerStyle = {
  width: "800px",
  height: "600px"
};

const icon = {
  url: "../../img/freight.png", // url
};

// "https://cdn-icons-png.flaticon.com/128/1656/1656475.png"

const center = {
  lat: -3.745,
  lng: -38.523
};

function VesselView({ originCords, destinationCords }) {

  const originLat = originCords.length > 0 ? originCords[0] : null;
  const originLong = originCords.length > 0 ? originCords[1] : null;
  const destLat = destinationCords.length > 0 ? destinationCords[0] : null;
  const destLong = destinationCords.length > 0 ? destinationCords[1] : null;

  return (
    <LoadScript googleMapsApiKey={REACT_APP_GMAPS_KEY}>
      <GoogleMap
        mapContainerStyle={containerStyle}
        zoom={5}
        center={{ lat: originLat, lng: originLong }}
      >
        <MarkerF position={{ lat: originLat, lng: originLong }} 
        icon={shippingIcon}/> 
        <MarkerF position={{ lat: destLat, lng: destLong }} /> 
        { /* Child components, such as markers, info windows, etc. */}
      </GoogleMap>
    </LoadScript>
  )
}

export default VesselView
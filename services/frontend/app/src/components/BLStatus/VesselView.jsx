import { GoogleMap, LoadScript, Marker } from "@react-google-maps/api";

const { REACT_APP_GMAPS_KEY } = process.env;

const containerStyle = {
  width: "800px",
  height: "600px"
};

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
        // center={center}
        zoom={1}
        center={{ lat: originLat, lng: originLong }}
      >
        <Marker position={{ lat: originLat, lng: originLong }} />
        {/* <Marker position={center} /> */}
        {/* <Marker position={{ lat: destinationLat, lng: destinationLong }} />  */}
        { /* Child components, such as markers, info windows, etc. */}
      </GoogleMap>
    </LoadScript>
  )
}

export default VesselView
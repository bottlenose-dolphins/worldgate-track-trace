import { GoogleMap, MarkerF, useJsApiLoader, InfoWindowF } from "@react-google-maps/api";
import shippingIcon from "../../img/freight.png";

const { REACT_APP_GMAPS_KEY } = process.env;

const containerStyle = {
  width: "800px",
  height: "600px"
};

const onLoad = infoBox => {
  console.log("infoBox: ", infoBox)
};

const divStyle = {
  background: "white",
  // border: "1px solid #ccc",
  padding: 8
}

// "https://cdn-icons-png.flaticon.com/128/1656/1656475.png"


function VesselView({ originCords, destinationCords, portOfDischarge }) {

  const originLat = originCords.length > 0 ? originCords[0] : null;
  const originLong = originCords.length > 0 ? originCords[1] : null;
  const destLat = destinationCords.length > 0 ? destinationCords[0] : null;
  const destLong = destinationCords.length > 0 ? destinationCords[1] : null;

  const { isLoaded } = useJsApiLoader({
    id: "google-map-script",
    googleMapsApiKey: REACT_APP_GMAPS_KEY,
    libraries: ["geometry", "drawing"],
  });



  return (
      isLoaded && <GoogleMap
        mapContainerStyle={containerStyle}
        zoom={6}
        center={{ lat: originLat, lng: originLong }}
      >
        <MarkerF position={{ lat: originLat, lng: originLong }} 
        icon={shippingIcon}
      /> 
        <MarkerF position={{ lat: destLat, lng: destLong }}
        />
        <InfoWindowF
      onLoad={onLoad}
      position={{lat: destLat, lng: destLong }}>
      <div style={divStyle}>
        <h1>Destination Port: {portOfDischarge}</h1>
      </div>
    </InfoWindowF>
        { /* Child components, such as markers, info windows, etc. */}
      </GoogleMap>
  )
}

export default VesselView
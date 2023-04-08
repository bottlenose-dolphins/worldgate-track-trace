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

function VesselView({ cordsLat, cordsLong, destinationLat, destinationLong }) {

    // const [cordsLat, cordsLong] = cords;
    console.log(cordsLat);
    console.log(cordsLong);
    console.log(typeof cordsLat);
    console.log(typeof cordsLong);

    // const cordsLat = cords[0];
    // const cordsLong = cords[1];
    // const destinationLat = destinationCords[0];
    // const destinationLong = destinationCords[1];
    
    // console.log(cordsLat)
    // console.log(cordsLong)
    // const [destinationCordsLat, destinationCordsLong] = destinationCords;
    

    return (
    <LoadScript googleMapsApiKey={REACT_APP_GMAPS_KEY}>
        <GoogleMap
            mapContainerStyle={containerStyle}
            // center={center}
            zoom={1}
            center={{ lat: cordsLat, lng: cordsLong }}
        >
        <Marker position={{ lat: cordsLat, lng: cordsLong }} />
        {/* <Marker position={center} /> */}
        {/* <Marker position={{ lat: destinationLat, lng: destinationLong }} />  */}
        { /* Child components, such as markers, info windows, etc. */ }
      </GoogleMap>
    </LoadScript>
  )
}

export default VesselView
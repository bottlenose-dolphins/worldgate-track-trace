import { GoogleMap, LoadScript, Marker } from "@react-google-maps/api";

const { REACT_APP_GMAPS_KEY } = process.env;

const containerStyle = {
    width: "400px",
    height: "400px"
};

const center = {
    lat: -3.745,
    lng: -38.523
};

function VesselView(cords, destinationCords) {



    console.log(cords)
    const [cordsLat, cordsLong] = cords;
    
    console.log(cordsLat)
    console.log(cordsLong)
    // const [destinationCordsLat, destinationCordsLong] = destinationCords;
    

    return (
    <LoadScript googleMapsApiKey={REACT_APP_GMAPS_KEY}>
        <GoogleMap
            mapContainerStyle={containerStyle}
            center={center}
            zoom={7}
            // center={{ lat: cordsLat, lng: cordsLong }}
        >
        {/* <Marker position={{ lat: cordsLat, lng: cordsLong }} /> */}
        <Marker position={center} />
        {/* <Marker position={{ lat: destinationCordsLat, lng: destinationCordsLong }} />  */}
        { /* Child components, such as markers, info windows, etc. */ }
      </GoogleMap>
    </LoadScript>
  )
}

export default VesselView
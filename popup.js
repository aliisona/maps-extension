function initMap() {
    // Default location: center of the map if geolocation fails
    const defaultLocation = { lat: 37.7749, lng: -122.4194 }; // San Francisco
  
    // Create the map
    const map = new google.maps.Map(document.getElementById("map"), {
      zoom: 12,
      center: defaultLocation
    });
  
    // Try HTML5 geolocation to center the map on the user's location
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          const userLocation = {
            lat: position.coords.latitude,
            lng: position.coords.longitude
          };
          map.setCenter(userLocation);
        },
        () => {
          console.error("Geolocation failed.");
        }
      );
    } else {
      console.error("Browser doesn't support geolocation.");
    }
  }
  
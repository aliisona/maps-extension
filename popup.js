let map;
let directionsService;
let directionsRenderer;

document.addEventListener('DOMContentLoaded', function() {
  console.log("loaded....");

  const apiKey = config.GOOGLE_MAPS_API_KEY;

//load api
  const script = document.createElement('script');
  script.src = `https://maps.googleapis.com/maps/api/js?key=${apiKey}`;
  
  script.onload = initializeMap; 
  document.head.appendChild(script); // script to the document head
  console.log("map script added");

  function initializeMap() {
      if (typeof google !== 'undefined') {
          console.log("map initialized");
          directionsService = new google.maps.DirectionsService();
          directionsRenderer = new google.maps.DirectionsRenderer();
          const mapOptions = {
              zoom: 7,
              center: { lat: -35, lng: 150 } //random cords
          };
          const map = new google.maps.Map(document.getElementById('map'), mapOptions);
          directionsRenderer.setMap(map); // map for direction
      } else {
          console.error("Google Maps API not loaded properly.");
      }
  }
});

document.getElementById('show-route-button').addEventListener("click", function getCurrentRoute() {
  chrome.tabs.query({ active: true, currentWindow: true }, function(tabs) {
    const currentTab = tabs[0];
    console.log("pressed");
    if (currentTab.url.includes('google.com/maps/dir')) {
      const urlParams = new URLSearchParams(currentTab.url.split('?')[1]);
      const origin = urlParams.get('origin');
      const destination = urlParams.get('destination');

      if (origin && destination) {
        document.getElementById('origin').value = decodeURIComponent(origin);
        document.getElementById('destination').value = decodeURIComponent(destination);
      }
    } else {
      console.warn('Not a Google Maps direction URL');
    }
  });
})

document.getElementById('calculate-button').addEventListener("click",  function calculateRoute(event) {
  event.preventDefault(); //prevent default

  const origin = document.getElementById('origin').value;
  const destination = document.getElementById('destination').value;

  const request = {
    origin: origin,
    destination: destination,
    travelMode: google.maps.TravelMode.WALKING // make walk
  };

  directionsService.route(request, function(result, status) {
    if (status === google.maps.DirectionsStatus.OK) {
      directionsRenderer.setDirections(result);
    } else {
      console.error('Directions request failed due to ' + status);
    }
  });
})

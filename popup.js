// handle generating path from user input
document.getElementById('generate').addEventListener('click', () => {
  const start = document.getElementById('start').value;
  const end = document.getElementById('end').value;

  // clear previous status and results
  document.getElementById('status').innerText = '';
  document.getElementById('result').style.display = 'none';
  document.getElementById('error').innerText = '';

  if (start && end) {
    console.log('getting path from:', start, 'to:', end);
    document.getElementById('status').innerText = 'fetching path...';

    // send the request to flask
    fetch('http://127.0.0.1:5000/get-walking-path', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ start, end })
    })
    .then(response => response.json())
    .then(data => {
      document.getElementById('status').innerText = '';

      if (data.error) {
        document.getElementById('error').innerText = data.error;
        document.getElementById('result').style.display = 'block';
      } else {
        const walkingTime = data.duration;
        document.getElementById('walking-time').innerText = `walking time: ${walkingTime}`;
        document.getElementById('result').style.display = 'block';

        // Update Google Maps URL with new path
        updateGoogleMapsUrl(start, end);

        // inject info into google maps page
        injectInfoIntoGoogleMaps(`walking time: ${walkingTime}`);
      }
    })
    .catch(error => {
      console.error('fetch error:', error);
      document.getElementById('status').innerText = '';
      document.getElementById('error').innerText = 'error fetching data';
      document.getElementById('result').style.display = 'block';
    });
  } else {
    // display a message if start or end locations are missing
    document.getElementById('status').innerText = 'please enter both start and end locations';
  }
});

// function to update Google Maps URL with start and end points
function updateGoogleMapsUrl(start, end) {
  chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
    const currentTab = tabs[0];

    // Construct new Google Maps directions URL
    const googleMapsUrl = `https://www.google.com/maps/dir/${encodeURIComponent(start)}/${encodeURIComponent(end)}/`;

    // Update the current tab's URL to reflect the new start and end points
    chrome.tabs.update(currentTab.id, { url: googleMapsUrl }, function () {
      console.log('Google Maps URL updated to:', googleMapsUrl);
    });
  });
}
// handle using the current path from google maps url
document.getElementById('use-current').addEventListener('click', () => {
  chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
    const currentTab = tabs[0];
    const url = currentTab.url;

    // try to extract start and end from the google maps url
    const pathRegex = /\/dir\/([^\/]+)\/([^\/]+)\//;
    const match = url.match(pathRegex);

    if (match && match.length >= 3) {
      const start = decodeURIComponent(match[1].replace(/\+/g, ' '));
      const end = decodeURIComponent(match[2].replace(/\+/g, ' '));
      console.log('got start:', start, 'and end:', end);

      document.getElementById('status').innerText = 'using current path from url...';

      // send extracted start and end to backend
      fetch('http://127.0.0.1:5000/get-walking-path', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ start, end })
      })
      .then(response => response.json())
      .then(data => {
        document.getElementById('status').innerText = '';

        if (data.error) {
          document.getElementById('error').innerText = data.error;
          document.getElementById('result').style.display = 'block';
        } else {
          const walkingTime = data.duration;
          document.getElementById('walking-time').innerText = `current path time: ${walkingTime}`;
          document.getElementById('result').style.display = 'block';

          // inject info into google maps page
          injectInfoIntoGoogleMaps(`current path time: ${walkingTime}`);

        }
      })
      .catch(error => {
        console.error('fetch error:', error);
        document.getElementById('status').innerText = '';
        document.getElementById('error').innerText = 'error fetching data';
        document.getElementById('result').style.display = 'block';
      });
    } else {
      console.log('could not get start and end from the url');
      document.getElementById('status').innerText = 'no valid path found in url';
    }
  });

  // inject a simple "HELLO!" to the google maps page
});

//inject
function injectInfoIntoGoogleMaps(infoText) {
  chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
    chrome.scripting.executeScript({
      target: { tabId: tabs[0].id },
      func: (infoText) => {
        console.log('Injecting info into the side panel...');

        const sidePanel = document.querySelector('.ue5qRc');  
        if (sidePanel) {
          const injectedDiv = document.createElement('div');
          injectedDiv.setAttribute("id", "injectedDIV!!!");
          injectedDiv.style.color = 'blue';  
          injectedDiv.style.margin = '10px 0';
          injectedDiv.style.fontSize = '16px';
          injectedDiv.innerText = infoText;

          sidePanel.prepend(injectedDiv);

          console.log('Injected info into the side panel:', infoText);
        } else {
          console.error('Side panel not found on Google Maps page');
        }
      },
      args: [infoText]
    });
  });
}
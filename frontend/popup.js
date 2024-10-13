chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
  chrome.scripting.executeScript({
    target: { tabId: tabs[0].id },
    func: () => {
      const sidePanel = document.querySelector('.MlqQ3d.Hk4XGb');  
      const optionsButton = document.querySelector('.OcYctc');  // Query the "Options" button

      if (sidePanel && optionsButton) {
        // Make sure the parent container is using flexbox to align elements in a row
        sidePanel.style.display = 'flex';
        sidePanel.style.alignItems = 'center';  // Vertically center elements
        sidePanel.style.gap = '10px';  // Add spacing between elements

        // Create the toggle container
        const toggleContainer = document.createElement('div');
        toggleContainer.style.display = 'inline-block';
        toggleContainer.style.border = '1px solid #ccc';  // Light gray border
        toggleContainer.style.borderRadius = '4px';  // Smaller border radius
        toggleContainer.style.padding = '1px 4px';  // Reduce padding to make it more compact
        toggleContainer.style.marginLeft = '40px';  // Add space after "Options"
        toggleContainer.style.marginTop = '4px';
        toggleContainer.style.fontSize = '12px';
        toggleContainer.style.fontFamily = 'Roboto, Arial, sans-serif';  // Apply correct font-family
        toggleContainer.style.backgroundColor = '#ffffff'; // Light gray background
        toggleContainer.style.cursor = 'pointer';
        toggleContainer.style.display = 'flex';
        toggleContainer.style.alignItems = 'center';
        toggleContainer.style.width = '90px';  // Set fixed width to make it compact

        // Create the inner labels for Time and Safety
        toggleContainer.innerHTML = `
          <span id="time-label" style="color: gray; flex: 1; text-align: center;">Time</span>
          <span style="border-left: 1px solid #ccc; height: 12px; margin: 0 4px;"></span>
          <span id="safety-label" style="font-weight: bold; color: black;  flex: 1; text-align: center;">Safety</span>
        `;

        // Append the toggle to the side panel after the Options button
        optionsButton.parentNode.insertBefore(toggleContainer, optionsButton.nextSibling);

        // Add event listener to handle the toggle behavior
        toggleContainer.addEventListener('click', () => {
          const timeLabel = document.getElementById('time-label');
          const safetyLabel = document.getElementById('safety-label');

          if (timeLabel.style.fontWeight === 'bold') {
            timeLabel.style.fontWeight = 'normal';
            timeLabel.style.color = 'gray';
            safetyLabel.style.fontWeight = 'bold';
            safetyLabel.style.color = 'black';
          } else {
            timeLabel.style.fontWeight = 'bold';
            timeLabel.style.color = 'black';
            safetyLabel.style.fontWeight = 'normal';
            safetyLabel.style.color = 'gray';
          }
        });
      } else {
        console.error('Side panel or Options button not found on Google Maps page');
      }
    },
    args: []
  });
});

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
    fetch('http://127.0.0.1:5000/getsafetyroutes', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        origin: start,
        destination: end,
        mode: "walking" // update when we pull the mode from the FE
      })
    })
    .then(response => response.json())
    .then(data => {
      document.getElementById('status').innerText = '';

      if (data.error) {
        document.getElementById('error').innerText = data.error;
        document.getElementById('result').style.display = 'block';
      } else {
        // Update Google Maps URL with new path
        updateGoogleMapsUrl(start, end);

        // inject info into google maps page
        injectInfoIntoGoogleMaps(`Safety of route: ${data[0]}`);
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
      fetch('http://127.0.0.1:5000/getsafetyroutes', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          origin: start,
          destination: end,
          mode: "walking" // update when we pull the mode from the FE
        })
      })
      .then(response => response.json())
      .then(data => {
        document.getElementById('status').innerText = '';

        if (data.error) {
          document.getElementById('error').innerText = data.error;
          document.getElementById('result').style.display = 'block';
        } else {
          // inject info into google maps page
          injectInfoIntoGoogleMaps(`Safety of route: ${data[0]}`);

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
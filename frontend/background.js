chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.action === 'getRoute') {
        const origin = message.origin;
        const destination = message.destination;

        const requestUrl = `http://localhost:5000/directions?origin=${origin}&destination=${destination}`;

        fetch(requestUrl)
            .then(response => response.json())
            .then(data => {
                if (data.status === "OK") {
                    sendResponse({ status: 'success', directions: data });
                } else {
                    sendResponse({ status: 'error', message: 'Route request failed' });
                }
            })
            .catch(error => sendResponse({ status: 'error', message: error.message }));

        return true; 
    }
});

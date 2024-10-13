
function checkForWalkingPath() {
  const directions = document.querySelectorAll('.section-directions-trip-duration');
  return directions.length > 0;
}

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.message === 'checkForCurrentPath') {
    const pathExists = checkForWalkingPath();
    sendResponse({ pathExists: pathExists });
  }
});
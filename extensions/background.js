// Open side panel when the extension icon is clicked
chrome.sidePanel
  .setPanelBehavior({ openPanelOnActionClick: true })
  .catch((error) => console.error(error));

// Detect YouTube video changes
chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
  if (changeInfo.status === 'complete' && tab.url?.includes("youtube.com/watch")) {
    const videoId = new URL(tab.url).searchParams.get("v");
    // Send the new video ID to the side panel
    chrome.runtime.sendMessage({ type: "VIDEO_CHANGED", videoId: videoId });
  }
});
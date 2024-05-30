// Function to disable back button
function disableBack() {
    window.history.forward();
}

// Call disableBack function on load
window.onload = disableBack;
window.onpageshow = function(event) {
    if (event.persisted) {
        disableBack();
    }
};

// Use popstate event to prevent going back
window.addEventListener('popstate', function(event) {
    window.history.pushState(null, '', window.location.href);
});
// This block of code was taken from a tutorial at 
// https://medium.com/javascript-dots/creating-browser-notification-in-javascript-79e91bfb76c8
let permission = Notification.permission;
if(permission === "granted") {
   showNotification();
} else if(permission === "default"){
   requestAndShowPermission();
} else {
  alert("Use normal alert");
}
function showNotification() {
   var title = "Ask the Experts";
   icon = "image-url"
   var body = "Welcome back";
   var notification = new Notification('Ask the Experts', { body, icon });
   notification.onclick = () => { 
          notification.close();
          window.parent.focus();
   }
}
function requestAndShowPermission() {
   Notification.requestPermission(function (permission) {
      if (permission === "granted") {
            showNotification();
      }
   });
}
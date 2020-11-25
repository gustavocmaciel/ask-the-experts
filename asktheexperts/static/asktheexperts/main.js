document.querySelector('#report-user-form').onsubmit = reportUser;

function reportUser() {
  event.preventDefault();
  
  // Get reported user and reason from form
  const reportedUser = document.querySelector('#reported-user').value;
  const reason = document.querySelector('#reason').value;

  fetch('/send_report', {
    method: 'POST',
    headers: {'X-CSRFToken': csrftoken},
    mode: 'same-origin',
    body: JSON.stringify({
      reportedUser: reportedUser,
      reason: reason
    })
  })
  .then(response => response.json())
  .then(result => {
    if (result.message !== "Email sent successfully.") {
      console.log(result);
      alert(result.error);
      return false;
    } else {
      console.log(result);
      return false;
    }
  })
  .catch(error => {
    console.log('Error:', error);
  });
}

// Function to get cookie, from Django docs.
// https://docs.djangoproject.com/en/3.1/ref/csrf/#ajax
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
          const cookie = cookies[i].trim();
          // Does this cookie string begin with the name we want?
          if (cookie.substring(0, name.length + 1) === (name + '=')) {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              break;
          }
      }
  }
  return cookieValue;
}
const csrftoken = getCookie('csrftoken');
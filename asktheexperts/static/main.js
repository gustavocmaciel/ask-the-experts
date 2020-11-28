document.addEventListener('DOMContentLoaded', function() {
  document.querySelector('#report').addEventListener('click', reportForm);

  loadProfilePage();
});

function loadProfilePage(){

  // Show report-form-view and hide profile-view
  document.querySelector('#profile-view').style.display = 'block';
  document.querySelector('#report-form-view').style.display = 'none';
}

function reportForm() {

  // Show compose view and hide other views
  document.querySelector('#profile-view').style.display = 'none';
  document.querySelector('#report-form-view').style.display = 'block';

  // Clear reason field
  document.querySelector('#reason').value = '';

  // Send report
  document.querySelector('#report-user-form').onsubmit = reportUser;
}

function reportUser() {
  event.preventDefault();
  
  // Get reported user and reason from form
  const reportedUser = document.querySelector('#reported-user').value;
  const reason = document.querySelector('#reason').value;

  fetch('/report_user', {
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
    console.log(result);
    loadProfilePage();
    return false;
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

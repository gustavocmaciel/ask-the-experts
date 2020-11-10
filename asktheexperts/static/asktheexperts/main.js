document.addEventListener('DOMContentLoaded', function() {

    // Use buttons to toggle between views
  document.querySelector('#info').addEventListener('click', info_view);
  document.querySelector('#username').addEventListener('click', change_username);
  document.querySelector('#email').addEventListener('click', change_email);
  document.querySelector('#password').addEventListener('click', change_password);
  document.querySelector('#delete').addEventListener('click', delete_account);

  // By default, load the inbox
  info_view('username');
});
  
function info_view() {
  document.querySelector('#change-username-view').style.display = 'none';
  document.querySelector('#account-info-view').style.display = 'block';
  document.querySelector('#change-email-view').style.display = 'none';
  document.querySelector('#change-password-view').style.display = 'none';
  document.querySelector('#delete-account-view').style.display = 'none';


}

function change_username() {
  document.querySelector('#change-username-view').style.display = 'block';
  document.querySelector('#account-info-view').style.display = 'none';
  document.querySelector('#change-email-view').style.display = 'none';
  document.querySelector('#change-password-view').style.display = 'none';
  document.querySelector('#delete-account-view').style.display = 'none';


}

function change_email() {
  document.querySelector('#change-username-view').style.display = 'none';
  document.querySelector('#account-info-view').style.display = 'none';
  document.querySelector('#change-email-view').style.display = 'block';
  document.querySelector('#change-password-view').style.display = 'none';
  document.querySelector('#delete-account-view').style.display = 'none';


}

function change_password() {
  document.querySelector('#change-username-view').style.display = 'none';
  document.querySelector('#account-info-view').style.display = 'none';
  document.querySelector('#change-email-view').style.display = 'none';
  document.querySelector('#change-password-view').style.display = 'block';
  document.querySelector('#delete-account-view').style.display = 'none';


}

function delete_account() {
  document.querySelector('#change-username-view').style.display = 'none';
  document.querySelector('#account-info-view').style.display = 'none';
  document.querySelector('#change-email-view').style.display = 'none';
  document.querySelector('#change-password-view').style.display = 'none';
  document.querySelector('#delete-account-view').style.display = 'block';

}


function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#content-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';

  // Send mail
  document.querySelector('#compose-form').onsubmit = sendMail;
}
  


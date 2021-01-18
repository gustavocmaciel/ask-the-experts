# Ask the Experts

The final project is a web application called `Ask the Experts`.

**Ask the Experts** is a web application where users can ask questions about programming and also answer those questions. They can also search for questions in the search bar and additionally upvote or downvote each question and/or answer. There's a score system based on each action that happens on the website (users whose question gets more votes has a higher score, for example). 

When a user registers, he/she gets a default profile photo (that can be changed later on the **settings page**) and has a starting score of `1`.

On the **settings page**, any user (who is signed in) can change his/her username, email, password and, additionally, delete his/her account. When a user visits his own question page, he/she has the ability to **mark** any answer as **selected**, which means this answer was useful and then, the **selected answer** appears on the top of all the other answers.

The **score system** works like this:
- When a question is upvoted: the user who asked the question gets `+20` points.
- When a answer is upvoted: the user who wrote the answer gets `+20` points.
- When a answer is selected: the user who wrote the answer gets `+25` points, and the user who marked the answer as selected gets `+5` points.
- When a question is downvoted: the user who asked the question looses `-5` points.
- When a answer is downvoted: the user who wrote the answer looses `-5` points, and the user who voted down the answer looses `-2` points.

Any user on this website can report any other user if he/she notices any kind of bad conduct. This *report* can, later, be reviewed by the site administrator (via admin page). The administrator can then decide if the user who commited the 'infraction' should have his/her account removed.

## Files

The `capstone` project contains a single app called `asktheexperts`.

In `asktheexperts/models.py`, all the models are defined. There are `four` models: 

- The `User` model represents each user registered in the application. It also has four many-to-many fields related to the `Question` model and the `Answer` model to keep track of which user upvoted or downvoted which question or answer.
- The `Question` model represents each question asked, it also has a `vote` field with the default value of `0` to store the number of votes.
- The `Answer` model represents all the answers of those questions. It also has a field called `selected` which is a Boolean field that indicate if this answer was marked as *selected* or not (the default is `False`).
- The `Reported_User` model represents the users that have been reported. It also has field called `solved` which is a Boolean field that indicates if this report issue has been solved by the site administrator (the default is `False`).

In `asktheexperts/urls.py`, all the URL configuration of the app is defined.

In `asktheexperts/views.py`, all the views associated with each of the routes are defined. There are 24 views in total and the majority of them have the `@loginrequired` decorator to prevent a user who is not signed in from accessing any of those views. In this file there's also a form to change the profile photo called `ChangePhotoForm`.

In `asktheexperts/admin.py`, the models that can be accessed in the `admin` page are registerd. *All* the models are registered so the site administrator has total control of the database.

`asktheexperts/templates/asktheexperts/layout.html` is the HTML layout of this application. The `nav-bar` has a search field and also has links that redirects to the `Index` page, to the `Questions` page, to the `Log In` page, to the `Register` page, to the `Ask Question` page, to the signed in user's profile page, to the `Settings` page, and a link to `Log Out`. A few links are wrapped in a check for if `user.is_authenticated`.

`asktheexperts/templates/asktheexperts/register.html` is the file for the register page where a user can make his/her registration. It has a form with four fields: `username`, `email`, `password`, `confirm password` as long with the `submit button`.

`asktheexperts/templates/asktheexperts/login.html` is the file for the login page. It has a form with two fields: `username` and `password` as long with the `submit button`.

`asktheexperts/templates/asktheexperts/index.html` is the file for the index page that works as a landing page .It has two buttons: one redirects to the page with all the questions asked on the website and the other redirects to the page where a user can ask a question.

`asktheexperts/templates/asktheexperts/ask_question.html` is the file for the page where a user who is signed in can ask as question. It has a form with two fields: one for the `title` of the question and the other for the `content` of the question.

`asktheexperts/templates/asktheexperts/questions.html` is the file for the page that shows all the questions asked. It has a for loop `tag` for the questions that are passed from the function defined in the `asktheexperts/views.py` file. So for each question it shows the `title`, the `content` (truncated), the `profile photo` of the user who asked the question as well as his/her `username`, and a `timestamp`. And it also shows the number of answers this question already has and the number of votes it has. At the bottom of the file, there are the pagination links.

`asktheexperts/templates/asktheexperts/question.html` is the file for the page where a user can view more details about the question. It shows the question `title`, the `content`, the `username` of the user who asked the question as well as the `profile photo`, and the `timestamp`. There are also two `buttons`: one for `upvote` and other to `downvote`. Only a user who is signed in can vote a question. It also shows the number of votes the question has. Below the question, it has a for loop `tag` for the answers that are passed from the function defined in the `asktheexperts/views.py`. For each of the aswers it shows the `content` of the answer, the `username` of the user who wrote the answer, the `profile photo` of the user who wrote the answer and also the `timestamp`. For each of the answers it also has two `buttons` that behave the same as the question buttons: one for `upvote` (the answer this time) and the other to `downvote`. It also shows the number of votes the answer has received. If the user who is viewing this page is the one who asked the question, he/she gets presented with a `button` for each of the answers, where he/she can mark the answer as `selected`, or even **unselect** any answer that has been marked by him/her before. The `selected` answers appears on the top of the answers when the page gets rendered. Only users who are signed in can vote an answer. On this file there are also the pagination links. On the bottom of the page there is a `textarea` to answer the question. Only users who are signed in can answer a question.

`asktheexperts/templates/asktheexperts/search_results.html` is the file for the page that shows all the search results. It behaves just like the `asktheexperts/templates/asktheexperts/questions.html` but showing only the questions that meets the query from the search that the user has made.

`asktheexperts/templates/asktheexperts/profile.html` is the file for the profile page. Each user has its own profile page that shows all of his/her *info*. It shows the `profile photo`, the `username`, a `timestamp` indicating the date when the user made his/her registration and it also has the number of questions asked and the number of the questions answered. It has a button to *report a user*. When this button is clicked, a javascript function (defined in the `asktheexperts/static/asktheexperts/scripts.js` file) hides the `profile-div` and shows a form where a user can write the reason why this user is being reported. On the bottom it has some links to the questions that have been made by this user.

`asktheexperts/templates/asktheexperts/settings.html` is the file for the settings page that can only be visited if the user is signed in. There is a `block tag` that extends the page. There are also four `buttons` that redirects to pages where a user can change his username, password, or even delete the account.

`asktheexperts/templates/asktheexperts/account_info.html` is the file for the page that shows the main *info* of the user who is signed in, it shows the `profile photo`, the `username` and the `password` (hidden behind asterisks). It also has a button with a link that redirects to the page where a user can change the `profile photo`. Below this button there is another button to `remove` the current `profile photo`.

`asktheexperts/templates/asktheexperts/change_photo.html` is the file for the page where a user can change his/her `profile photo` by submmiting a form.

`asktheexperts/templates/asktheexperts/change_username.html` is the file for the page where a user can change his/her `username `. It has a form with two fields: one to enter the new username and the other to type the password.

`asktheexperts/templates/asktheexperts/change_email.html` is the file for the page where a user can change his/her `email`. It has a form with two fields: one to enter the new email and the other to type the password.

`asktheexperts/templates/asktheexperts/change_password.html` is the file for the page where a user can change his/her `password`. It has a form with three fields: `password` (the current one), `new password` and `confirm new password`.

`asktheexperts/templates/asktheexperts/delete_account` is the file for the page where a user can delete his/her account. It has a form where the user has to type his/her password and, by submmiting the form, the account gets deleted.

`asktheexperts/static/asktheexperts/styles.css` is the file that contains the `CSS` for the project.

`asktheexperts/static/asktheexperts/scripts.js` is the file that contains the `Javascript` functions for the project.

On the `asktheexperts/static/asktheexperts` folder, there are also two image files:
- `background.png` is the image file used as the **background image**. 
- `logo.png` is the image file used as the **website logo** and also as the **favicon**.

On the root directory, there is a `media/images` folder. This is the folder to store the profile photos from the users. In this folder there's also a image called `default_image.jpg`, this is the image used as the *default photo* when a user make his/her registration.

## Python packages

All the Python packages that need to be installed to run this web application are **included** in the [requirements.txt](requirements.txt) file.

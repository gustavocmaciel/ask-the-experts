# Capstone

## Ask the Experts

**Ask the experts** is a web application where users can make questions about programming and also answer those questions. They can also search for questions in the search bar and additionally upvote or downvote each question or answer. There's also a score sistem based on each action that happens on the website(e.g. users whose question gets more votes has a higher score). 

When a user registers, he/she gets a default profile photo that can be changed later on the `settings` page, and has a starting score of `1`. All the questions and answers can be written using markdown syntax, which gets converted when the question and answer gets rendered. 

On the `settings` page, any user(who is signed in) can also change his/her username, email, password and, additionally, delete his/her account. When a user visits his own question page, the user has the ability to **mark** any answer as **selected**, which means this answer was useful and then, the **selected answer** appears on the top of all the other answers.

The **score system** works like this:
- When a question is upvoted: the user who made the question gets `+10` points
- When a answer is upvoted: the user who wrote the answer gets `+10` points
- When a answer is selected: the user who wrote the answer gets `+15` points, and the user who marked the answer as selected gets `+2` points
- When a question is downvoted: the user who made the question looses `-2` points
- When a answer is downvoted: the user who wrote the answer looses `-2` points, and the user who voted down the answer looses `1` point

## Files

`asktheexperts/models.py` is where all the models are defined. There are `three` models: 

- The `User` model represents each user registered in the application. It also has four many-to-many fields related to the `Question` model and the `Answer` model to keep track of which user upvoted or downvoted which question or answer.
- The `Question` model represents each question that are made, it also has a `vote` field with the default value of `0` to store the number of votes.
- The `Answer` model represents all the answers of those question. It also has a field called `selected` which is a Boolean field that indicate if this answer was marked as selected or not (the default is `False`).

`asktheexperts/urls.py` is where all the URL configuration of the app is defined, which means all of the url paths *live* there.

`asktheexperts/views.py` is where all the views associated with each of the routes are defined. There 23 views in total and the majority of them have the `@loginrequired` decorator to prevent a user who is not signed in from accessing any of those views.

`asktheexperts/admin.py` is where the models that can be accessed in the `admin` page are registerd. All the models *are* registered so the administrator has total control of the database.

`asktheexperts/templates/asktheexperts/layout.html` is the HTML layout of this application. The `nav-bar` is in this file.

`asktheexperts/templates/asktheexperts/index.html` is the file for the index page that works more like an arrival page since it only has a *descriptive* message and two buttons: One that redirects to the page with all of the questions made on the website and the other redirects to the page where a user can ask a question.

`asktheexperts/templates/asktheexperts/ask_question.html` is the file for the page where a user who is signed in can ask as question. It has a form with two fields: one for the `title` of the question and the other for the `content` of the question that can be written using **markdown** syntax.

`asktheexperts/templates/asktheexperts/questions.html` is the file for the page that shows all of the questions asked. It has a for loop `tag` for the questions that are passed from the function defined in the `asktheexperts/views.py` file. So for each question it shows the `title`, the `content` (truncated), the `profile photo` of the user who made the question as well as his/her `username` and a `timestamp`. And also has a box with the number of answers this question already has and the number of votes it has.

`asktheexperts/templates/asktheexperts/question.html` is the file for the page where a user can view more details about the question. It shows the question `title`, the `content` (that was originally written in markdown but now is converted to html), the `username` of the user who made the question as well as the `profile photo`, and the `timestamp`. There's also a box with two `buttons`: one for `upvote` and the other to `downvote`. Only a user who is signed in can vote a question. In the same box, it also shows the number of votes the question has. Below the question, there are all the answers for this question. For each of the aswers it shows the `content` of the answer, the `username` of the user who wrote the answer, the `profile photo` of the user who wrote the answer and also the `timestamp`. For each of the answer it also has a box with two `buttons` that behave the same as the question buttons: one for `upvote` (the answer his time) and the other to `downvote`. It shows the number of votes the answer has received. If the user who is viewing this page is the one 'owner' of the question, he/she gets presented with a `button` for each of the answers where he/she can mark the answer as `selected`, or even **unselect** any answer that has been marked by him/her before. The `selected` answers shows on the top of the answers when the page gets rendered. Only users who is signed in can vote a answer. On the bottom of the page there is a `textarea` to answer the question. The answer can be written using **markdown** syntax. Only users who are signed in can answer those questions.

`asktheexperts/templates/asktheexperts/profile.html` is the file for the profile page. Each user has its own profile page that shows all of his/her *info*. It shows the `profile photo`, the `username`, a `timestamp` indicating the date when the user made his/her registration and it also has the number of questions asked and the number of the questions answered. On the bottom it has some links to the questions that have been made by this user.

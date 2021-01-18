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
## Screenshots

![image](https://user-images.githubusercontent.com/66797203/104955732-6abc4300-59a9-11eb-8d61-932f49c38b3f.png)

![image](https://user-images.githubusercontent.com/66797203/104955409-013c3480-59a9-11eb-99b4-787d4fd21f3a.png)

![image](https://user-images.githubusercontent.com/66797203/104955528-1b761280-59a9-11eb-9826-eb83c8269f2b.png)

![image](https://user-images.githubusercontent.com/66797203/104955649-3ba5d180-59a9-11eb-863f-1273bd5187fd.png)

![image](https://user-images.githubusercontent.com/66797203/104955676-4eb8a180-59a9-11eb-8a7f-f72477782f70.png)

## Python packages

All the Python packages that need to be installed to run this web application are **included** in the [requirements.txt](requirements.txt) file.

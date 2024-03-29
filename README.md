# Ask the Experts

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

![image](https://user-images.githubusercontent.com/66797203/104956063-1ebdce00-59aa-11eb-9a4f-bded722d3496.png)

![image](https://user-images.githubusercontent.com/66797203/104955874-b111a200-59a9-11eb-9c19-cbd0e3c0030b.png)

![image](https://user-images.githubusercontent.com/66797203/104955960-e4ecc780-59a9-11eb-949a-1d39f8b3a022.png)

![image](https://user-images.githubusercontent.com/66797203/104955937-d6061500-59a9-11eb-8b90-bd0a38cc50d0.png)

## Python packages

All the Python packages that need to be installed to run this web application are **included** in the [requirements.txt](requirements.txt) file.

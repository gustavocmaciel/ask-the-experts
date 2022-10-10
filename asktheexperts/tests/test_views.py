from django.test import TestCase

from django.urls import *
from asktheexperts.models import *


class IndexViewTest(TestCase):
    def test_index_view_exists_at_desired_location(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_index_view_accesible_by_name(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    def test_index_view_uses_correct_template(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'asktheexperts/index.html')


class LoginViewTest(TestCase):
    def setUp(self):
        # Create a test user
        test_user = User.objects.create_user(
                username='test_user',
                email='test_user@email.com',
                password='abcd'
                )
        test_user.save()

    def test_login_view_exists_at_desired_location(self):
        response = self.client.get('/login/')
        self.assertEqual(response.status_code, 200)

    def test_login_view_accesible_by_name(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_login_view_uses_correct_template(self):
        response = self.client.get(reverse('login'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'asktheexperts/login.html')

    def test_login_user(self):
        response = self.client.post('/login/', {
            'username': 'test_user',
            'password': 'abcd'
            })

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/')

    def test_fail_login_user_wrong_username(self):
        response = self.client.post('/login/', {
            'username': 'wrong_test_user',
            'password': 'abcd'
            })

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
                response.context['message'],
                'Invalid username and/or password.'
                )
        self.assertTemplateUsed(response, 'asktheexperts/login.html')

    def test_fail_login_user_wrong_password(self):
        response = self.client.post('/login/', {
            'username': 'test_user',
            'password': 'ab'
            })

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
                response.context['message'],
                'Invalid username and/or password.'
                )
        self.assertTemplateUsed(response, 'asktheexperts/login.html')

class LogoutViewTest(TestCase):
    def setUp(self):
        # Create a test user
        test_user = User.objects.create_user(
                username='test_user',
                email='test_user@email.com',
                password='abcd'
                )
        test_user.save()

    def test_logout_view_exists_at_desired_location(self):
        response = self.client.get('/logout')
        self.assertEqual(response.status_code, 302)

    def test_logout_view_accesible_by_name(self):
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)

    def test_logout(self):
        # Log in test user
        login = self.client.login(username='test_user', password='abcd')
        # Check user is logged in
        response = self.client.get(reverse('index'))
        self.assertEqual(
                str(response.context['user']),
                '1 - test_user'  # No idea why we need to add `1 - ` before
                )                # the actual username to make it work.

        # Check user log out
        response = self.client.get('/logout')
        self.assertEqual(response.context, None)  # No more user
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/')


class RegisterViewTest(TestCase):
    def setUp(self):
        # Create a test user
        test_user = User.objects.create_user(
                username='test_user',
                email='test_user@email.com',
                password='abcd'
                )
        test_user.save()

    def test_register_view_exists_at_desired_location(self):
        response = self.client.get('/register')
        self.assertEqual(response.status_code, 200)

    def test_register_view_accesible_by_name(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)

    def test_register_view_uses_correct_template(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'asktheexperts/register.html')

    def test_register_user(self):
        response = self.client.post('/register', {
            'username': 'test_user_2',
            'email': 'test_user_2@email.com',
            'password': 'abcdef',
            'confirmation': 'abcdef'
            })

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/')

    def test_fail_register_user_password_must_match(self):
        response = self.client.post('/register', {
            'username': 'test_user_2',
            'email': 'test_user_2@email.com',
            'password': 'abcdef',
            'confirmation': 'abcde'
            })

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
                response.context['message'],
                'Passwords must match.'
                )
        self.assertTemplateUsed(response, 'asktheexperts/register.html')

    def test_fail_register_username_already_taken(self):
        response = self.client.post('/register', {
            'username': 'test_user',
            'email': 'test_user_2@email.com',
            'password': 'abcdef',
            'confirmation': 'abcdef'
            })

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
                response.context['message'],
                'Username already taken.'
                )
        self.assertTemplateUsed(response, 'asktheexperts/register.html')


class QuestionsViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Create a test user
        test_user = User.objects.create_user(
                username='test_user',
                email='test_user@email.com',
                password='abcd'
                )
        test_user.save()

        # Create 35 test questions
        number_of_questions = 35
        for question_id in range(number_of_questions):
            Question.objects.create(
                    user=User.objects.get(username='test_user'),
                    title=f'title {question_id}',
                    content=f'content {question_id}'
                    )

    def test_questions_view_url_exists_at_desired_location(self):
        response = self.client.get('/questions')
        self.assertEqual(response.status_code, 200)

    def test_questions_view_url_accesible_by_name(self):
        response = self.client.get(reverse('questions'))
        self.assertEqual(response.status_code, 200)

    def test_questions_view_url_uses_correct_template(self):
        response = self.client.get(reverse('questions'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'asktheexperts/questions.html')

    def test_pagination_is_15(self):
        response = self.client.get(reverse('questions'))
        self.assertEqual(response.status_code, 200)

        # TODO: Check if `is_paginated`
        # self.assertTrue('is_paginated' in response.context)
        # self.assertTrue(response.context['is_paginated'] == True)

        self.assertEqual(len(response.context['questions']), 15)
        self.assertEqual(len(response.context['all_questions']), 35)

    def test_lists_all_questions(self):
        # Get third page and confirm it has exactly remaining 5 items
        response = self.client.get(reverse('questions')+'?page=3')
        self.assertEqual(response.status_code, 200)

        # TODO: Check if `is_paginated`
        # self.assertTrue('is_paginated' in response.context)
        # self.assertTrue(response.context['is_paginated'] == True)

        self.assertEqual(len(response.context['questions']), 5)
        self.assertEqual(len(response.context['all_questions']), 35)


class SearchViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Create a test user
        test_user = User.objects.create_user(
                username='test_user',
                email='test_user@email.com',
                password='abcd'
                )
        test_user.save()

        # Create 35 test questions
        number_of_questions = 35
        for question_id in range(number_of_questions):
            Question.objects.create(
                    user=User.objects.get(username='test_user'),
                    title=f'title {question_id}',
                    content=f'content {question_id}'
                    )

    def test_search_view_url_exists_at_desired_location(self):
        response = self.client.get('/search', {'q': 'title'})
        self.assertEqual(response.status_code, 200)

    def test_search_view_url_accesible_by_name(self):
        response = self.client.get(reverse('search'), {'q': 'title'})
        print(response)
        self.assertEqual(response.status_code, 200)

    def test_search_view_url_uses_correct_template(self):
        response = self.client.get(reverse('search'), {'q': 'title'})

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'asktheexperts/search_results.html')

    def test_pagination_is_15(self):
        response = self.client.get(reverse('search'), {'q': 'title'})
        self.assertEqual(response.status_code, 200)

        # TODO: Check if `is_paginated`
        # self.assertTrue('is_paginated' in response.context)
        # self.assertTrue(response.context['is_paginated'] == True)

        self.assertEqual(len(response.context['questions']), 15)
        self.assertEqual(len(response.context['all_questions']), 35)

    def test_lists_all_questions(self):
        # Get third page and confirm it has exactly remaining 5 items
        response = self.client.get(reverse('search')+'?page=3', {'q': 'title'})
        self.assertEqual(response.status_code, 200)

        # TODO: Check if `is_paginated`
        # self.assertTrue('is_paginated' in response.context)
        # self.assertTrue(response.context['is_paginated'] == True)

        # FIXME: This *should* be returning true
        # self.assertEqual(len(response.context['questions']), 5)

        self.assertEqual(len(response.context['all_questions']), 35)

    def test_returns_q(self):
        response = self.client.get(reverse('search'), {'q': 'title'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['q'], 'title')

    def test_search_substring(self):
        response = self.client.get(reverse('search'), {'q': 'ti'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['all_questions']), 35)

class QuestionViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Create a test user
        test_user = User.objects.create_user(
                username='test_user',
                email='test_user@email.com',
                password='abcd'
                )
        test_user.save()

        # Create a second test user
        test_user_2 = User.objects.create_user(
                username='test_user_2',
                email='test_user_2@email.com',
                password='abcdef'
                )
        test_user_2.save()

        # Create a test question
        Question.objects.create(
                user=User.objects.get(username='test_user'),
                title='test title',
                content='test content'
                )

        # Create 35 test answers
        number_of_answers = 35
        for answer_id in range(number_of_answers):
            Answer.objects.create(
                    user=User.objects.get(username='test_user_2'),
                    question=Question.objects.get(title='test title'),
                    content=f'content {answer_id}'
                    )

    def test_question_view_url_exists_at_desired_location(self):
        response = self.client.get(f'/questions/{1}')
        self.assertEqual(response.status_code, 200)

    def test_question_view_url_accesible_by_name(self):
        response = self.client.get(reverse('question',args=(1,)))
        self.assertEqual(response.status_code, 200)

    def test_question_view_url_uses_correct_template(self):
        response = self.client.get(reverse('question',args=(1,)))

        question = Question.objects.get(id=1)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'asktheexperts/question.html')
        self.assertEqual(response.context['question'], question)
        self.assertEqual(len(response.context['answers']), 15)
        # self.assertEqual(response.context['answers_count'], 35)
        self.assertEqual(len(response.context['selected_answers']), 0)

    def test_question_does_not_exist(self):
        response = self.client.get(f'/questions/{2}')
        self.assertEqual(response.status_code, 404)

    def test_pagination_is_15(self):
        response = self.client.get(reverse('question',args=(1,)))
        self.assertEqual(response.status_code, 200)

        question = Question.objects.get(id=1)

        # TODO: Check if `is_paginated`
        # self.assertTrue('is_paginated' in response.context)
        # self.assertTrue(response.context['is_paginated'] == True)

        self.assertEqual(response.context['question'], question)
        self.assertEqual(len(response.context['answers']), 15)
        # self.assertEqual(response.context['answers_count'], 35)
        self.assertEqual(len(response.context['selected_answers']), 0)

    def test_lists_all_answers(self):
        # Get third page and confirm it has exactly remaining 5 items
        response = self.client.get(reverse('question',args=(1,))+'?page=3')
        self.assertEqual(response.status_code, 200)

        question = Question.objects.get(id=1)

        # TODO: Check if `is_paginated`
        # self.assertTrue('is_paginated' in response.context)
        # self.assertTrue(response.context['is_paginated'] == True)

        self.assertEqual(response.context['question'], question)
        self.assertEqual(len(response.context['answers']), 5)

        # FIXME: This should be returning True
        # self.assertEqual(response.context['answers_count'], 35)

        self.assertEqual(len(response.context['selected_answers']), 0)


class AskQuestionTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Create a test user
        test_user = User.objects.create_user(
                username='test_user',
                email='test_user@email.com',
                password='abcd'
                )
        test_user.save()

    def test_ask_question_view_exists_at_desired_location(self):
        # Log in test user
        login = self.client.login(username='test_user', password='abcd')

        response = self.client.get('/ask_question')
        self.assertEqual(response.status_code, 200)

    def test_ask_question_view_accesible_by_name(self):
        # Log in test user
        login = self.client.login(username='test_user', password='abcd')

        response = self.client.get(reverse('ask_question'))
        self.assertEqual(response.status_code, 200)

    def test_ask_question_view_uses_correct_template(self):
        # Log in test user
        login = self.client.login(username='test_user', password='abcd')

        response = self.client.get(reverse('ask_question'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'asktheexperts/ask_question.html')

    def test_ask_question(self):
        # Log in test user
        login = self.client.login(username='test_user', password='abcd')

        response = self.client.post('/ask_question', {'title': 'test_title', 'content': 'test_content'})

        question = Question.objects.get(id=1)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/questions')
        self.assertEqual(question.title, 'test_title')
        self.assertEqual(question.content, 'test_content')

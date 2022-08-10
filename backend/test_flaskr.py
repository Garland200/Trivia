import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category

#from settings import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST




class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia"
        
        DB_HOST = 'localhost:5432'
        DB_PASSWORD = 'postgres'
        DB_USER = 'postgres'
        
        self.database_path = "postgresql://{}:{}@{}/{}".format(
    DB_USER, DB_PASSWORD, DB_HOST, self.database_name)

        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_get_paginated_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)
        
        self.assertTrue(data['total_questions'])   
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['questions']))
    
    def test_404_request_beyond_valid_page(self):
        """Tests question pagination failure 404"""

        # send request with bad page data, load response
        response = self.client().get('/questions?page=0')
        data = json.loads(response.data)

        # check status code and message
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Page not found')

        
    def test_delete_question(self): 
        question = Question(question="What is?",
                            answer='answer', 
                            category=1, 
                            difficulty=1)
        question.insert()
        q_id = question.id

        questions_before = Question.query.all()
        response = self.client().delete('/questions/{}'.format(q_id))
        data = json.loads(response.data)

        questions_after = Question.query.all()
        question = Question.query.filter(Question.id == 1).one_or_none()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], q_id)
    
        
    def test_create_questions(self):
        mock_question = {
            'question': 'ckjhgfdsdfghj',
            'answer': ';loiuygbnml;kjhg',
            'difficulty': 1,
            'category': 1,
        }
        res = self.client().post('/questions', json=mock_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        
    def test_if_question_does_not_exist(self):
        res = self.client().delete("/questions/1000")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data["message"], "Page not found")
       
        
    def test_search(self):
        search = {'searchTerm': '', }
        res = self.client().post('/search', json=search)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
      
    def test_if_search_questions_fails(self):
        res = self.client().post(
            '/search',
            json={'searchTerm': 'aaaaa'}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['questions']), 0)
        self.assertEqual(data['total_questions'], 0)
        self.assertEqual(data['current_category'], None)
    
    def test_get_questions_by_category(self):
        res = self.client().get('/categories/1/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['total_questions'])
        self.assertEqual(data['success'], True)
        
    def test_if_questions_by_category_fails(self):
        res = self.client().get('/categories/100/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Bad request')
        
    def test_quiz_questions(self):
        request_data = {'previous_questions': [], 'quiz_category': {'id': 3,  'type': 'Geography'}}
        res = self.client().post('/quizzes', json=request_data)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])

    def test_get_all_categories (self):
        """GET categories """
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])
        self.assertEqual(len(data['categories']), 6)
        self.assertIsInstance(data['categories'], dict)
    
    def test_422_if_question_creation_fails(self):
        mock_question = {
            'question': 'ckjhgfdsdfghj',
            'answer': ';loiuygbnml;kjhg',
            'difficulty':""
        }
        res = self.client().post('/questions', json=mock_question)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        
    def test_play_quiz_fails(self):
        response = self.client().post('/quizzes', json={})

        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)




# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
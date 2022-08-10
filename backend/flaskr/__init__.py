import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category


QUESTIONS_PER_PAGE = 10


def paginate_questions(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    questions = [question.format() for question in selection]
    current_questions = questions[start:end]
    return current_questions


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    
    CORS(app, resources={r"*": {"origins": "*"}})

   
    # Use the after_request decorator to set Access-Control-Allow
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,POST,DELETE')
        return response

    
    # Create an endpoint to handle GET requests
    @app.route('/categories')
    def get_all_categories():
        # get all categories
        categories = Category.query.all()
        # categories dict for holding the retrives categories
        categoriesDict = {}

        # adding all categories to the dict
        for category in categories:
            categoriesDict[category.id] = category.type

        return jsonify({
            'success': True,
            'categories': categoriesDict
        })

  
  
    #Create an endpoint to handle GET requests for questions,
    @app.route('/questions')
    def get_questions():
        try:
            # page
            page = request.args.get('page', 1, type=int)

            # questions
            questions = Question.query \
                .order_by(Question.id) \
                .paginate(page=page, per_page=QUESTIONS_PER_PAGE)

            questions_formatted = [
              question.format() for question in questions.items
            ]

            # categories
            categories = Category.query.order_by(Category.id).all()
            categories_formatted = {
              category.id: category.type for category in categories
            }

            if len(questions_formatted) == 0:
                abort(404)
            else:
                return jsonify({
                  'success': True,
                  'questions': questions_formatted,
                  'total_questions': questions.total,
                  'categories': categories_formatted,
                  'current_category': None,
                })
        except Exception as e:
            if '404' in str(e):
                abort(404)
            else:
                abort(422)


    
    # Create an endpoint to DELETE question using a question ID.
    @app.route('/questions/<int:id>', methods=['DELETE'])
    def delete_question(id):
  
        try:
            question = Question.query \
              .filter(Question.id == id) \
              .one_or_none()

            if question is None:
                abort(404)

            question.delete()

            return jsonify({
              'success': True,
              'deleted': id,
            })
        except Exception as e:
            if '404' in str(e):
                abort(404)
            else:
                abort(422)


#   Create an endpoint to POST a new question, 
#   which will require the question and answer text,
#   category, and difficulty score.
    @app.route("/questions", methods=['POST'])
    def add_question():
        body = request.get_json()
        try:
            new_question = body.get('question')
            new_answer = body.get('answer')
            new_difficulty = body.get('difficulty')
            new_category = body.get('category')
            question = Question(question=new_question, 
                                answer=new_answer,
                                difficulty=new_difficulty,
                                category=new_category)
            question.insert()
            selection = Question.query.order_by(Question.id).all()
            currentQuestions = paginate_questions(request, selection)

            return jsonify({
                'success': True,
                'created': question.id,
                'questions': currentQuestions,
                'total_questions': len(selection)
            })
        except Exception as e:
            print(e)
            abort(422)
    
   
#   Create a POST endpoint to get questions based on a search term.
#   It should return any questions for whom the search term
#   is a substring of the question. 
    @app.route('/search', methods=['POST'])
    def search_question():
    
            body = request.get_json()
            search = body.get('searchTerm', None)

            try:
                # Search the term
                questions = Question.query \
                .order_by(Question.id) \
                .filter(Question.question.ilike('%{}%'.format(search)))

                questions_formatted = [
                question.format() for question in questions
                ]

                return jsonify({
                'success': True,
                'questions': questions_formatted,
                'total_questions': len(questions.all()),
                'current_category': None,
                })
            except Exception:
                abort(422)
        # Create a GET endpoint to get questions based on category.
    @app.route("/categories/<int:id>/questions")
    def questions_by_category(id):
        category = Category.query.filter_by(id=id).one_or_none()

        if category:
            questions = Question.query.filter_by(category=category.id).all()

            paginated = paginate_questions(request, questions)

            return jsonify({
                'success': True,
                'questions': paginated,
                'total_questions': len(questions),
                'current_category': category.type
            })
        else:
            abort(400)

 

#   Create a POST endpoint to get questions to play the quiz.
#   This endpoint should take category and previous question parameters
#   and return a random questions within the given category,
#   if provided, and that is not one of the previous questions.
    @app.route('/quizzes', methods=['POST'])
    def quiz():
        body = request.get_json()
        quiz_category = body.get('quiz_category')
        previous_question = body.get('previous_questions')
        try:
            if (quiz_category['id'] == 0):
                questions_returned = Question.query.all()
            else:
                questions_returned = Question.query.filter_by(
                    category=quiz_category['id']).all()

            current_question = None
            if(len(questions_returned) > 0):
                index = random.randrange(0, len(questions_returned))
                current_question = questions_returned[index].format()
            return jsonify({
              'success': True,
              'question': current_question,
              'total_questions': len(questions_returned),
              })

        except Exception as e:
            print(e)
            abort(404)
    
 
# Create error handlers for all expected errors including 404 and 422.
    

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            'error': 400,
            "message": "Bad request"
        }), 400

    @app.errorhandler(404)
    def page_not_found(error):
        return jsonify({
            "success": False,
            'error': 404,
            "message": "Page not found"
        }), 404

    @app.errorhandler(422)
    def unprocessable_recource(error):
        return jsonify({
            "success": False,
            'error': 422,
            "message": "Unprocessable"
        }), 422

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            "success": False,
            'error': 500,
            "message": "Internal server error"
        }), 500
        
    return app
Trivia App
The Udacity team is invested in creating bonding experiences for its employees and students. A bunch of team members got the idea to hold trivia on a regular basis and created a webpage to manage the trivia app and play the game.

The trivia app was built so they can start holding trivia and see who the most knowledgeable of the bunch is. The application can:
1. Display questions - both all questions and by category. Questions should show the question, category, and difficulty rating by default and can show/hide the answer.
2. Delete questions.
3. Add questions and require that they include the question and answer text.
4. Search for questions based on a text query string.
6. Play the quiz game, randomizing either all questions or within a specific category.

## Getting Started 

### Pre-requisite installation:
- Python3 
- Pip 
- node 
    ### optional
    - It is recommended that you work in a virtual environment
        - cd to the backend folder and activate the virtualenv by running:: 
          'venv\scripts\activate'

### Backend Dependencies
    Once you have your virtual environment setup and running, install dependencies by navigating to the backend folder and running:
    pip install -r requirements.txt


## Frontend & Working in your Local Environment
    The frontend app was built using create-react-app and uses NPM to manage software dependencies. NPM Relies on the package.json file located in the frontend directory of this repository.

    Install Node and NPM This project requires on Nodejs and Node Package Manager (NPM). If you haven't already installed Node on your local machine
    
    Install project dependencies After confirming you have NPM installed, navigate to the frontend directory of the project and run:
    npm install
    tip: npm iis shorthand for npm install

    To start the app in development mode, run:

    npm start
    Open http://localhost:3000 to view it in the browser. The page will reload if you make edits.

### Error Handling

Errors are returned in the following json format:


{
    "success": False, 
    "error": 400,
    "message": "bad request"
}

The error codes currently returned are:

* 400 – bad request
* 404 – resource not found
* 422 – unprocessible
* 500 – internal server error

## Testing
To run the tests, Navigate to the project folder on your terminal and run:

dropdb trivia_test
createdb trivia_test (database can also be created directly from the pgAdmin application)
psql trivia_test < trivia.psql
python test_flaskr.py


### Expected endpoints and behaviors
1. GET '/categories'

Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
Request Arguments: None
Returns: An object with a single key, categories, that contains an object of id: category_string key:value pairs.
{
    'categories': { '1' : "Science",
    '2' : "Art",
    '3' : "Geography",
    '4' : "History",
    '5' : "Entertainment",
    '6' : "Sports" }
}
2. GET '/questions?page=${integer}'

Fetches a paginated set of questions, a total number of questions, all categories and current category string.
Request Arguments: page - integer
Returns: An object with 10 paginated questions, total questions, object including all categories, and current category string
{
    'questions': [
        {
            'id': 1,
            'question': 'This is a question',
            'answer': 'This is an answer',
            'difficulty': 5,
            'category': 2
        },
    ],
    'totalQuestions': 100,
    'categories': { '1' : "Science",
    '2' : "Art",
    '3' : "Geography",
    '4' : "History",
    '5' : "Entertainment",
    '6' : "Sports" },
    'currentCategory': 'History'
}
3. GET '/categories/${id}/questions'

Fetches questions for a cateogry specified by id request argument
Request Arguments: id - integer
Returns: An object with questions for the specified category, total questions, and current category string
{
    'questions': [
        {
            'id': 1,
            'question': 'This is a question',
            'answer': 'This is an answer',
            'difficulty': 5,
            'category': 4
        },
    ],
    'totalQuestions': 100,
    'currentCategory': 'History'
}
4. DELETE '/questions/${id}'

Deletes a specified question using the id of the question
Request Arguments: id - integer
Returns: Does not need to return anything besides the appropriate HTTP status code. Optionally can return the id of the question. If you are able to modify the frontend, you can have it remove the question using the id instead of refetching the questions.
POST '/quizzes'

Sends a post request in order to get the next question
Request Body:
{
    'previous_questions': [1, 4, 20, 15]
    quiz_category': 'current category'
 }
Returns: a single new question object
{
    'question': {
        'id': 1,
        'question': 'This is a question',
        'answer': 'This is an answer',
        'difficulty': 5,
        'category': 4
    }
}
5. POST '/questions'

Sends a post request in order to add a new question
Request Body:
{
    'question':  'Heres a new question string',
    'answer':  'Heres a new answer string',
    'difficulty': 1,
    'category': 3,
}
Returns: Does not return any new data
POST '/questions'

Sends a post request in order to search for a specific question by search term
Request Body:
{
    'searchTerm': 'this is the term the user is looking for'
}

Returns: any array of questions, a number of totalQuestions that met the search term and the current category string
{
    'questions': [
        {
            'id': 1,
            'question': 'This is a question',
            'answer': 'This is an answer',
            'difficulty': 5,
            'category': 5
        },
    ],
    'totalQuestions': 100,
    'currentCategory': 'Entertainment'
}
;

        `


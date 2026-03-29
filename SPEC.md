1 Project Description
    This project is a quiz application running in command line. The question relates on courses 36401 and 36402 at CMU, linear regression and modern advanced data analysis. Program will record users' historical information, statistical information and preference on questions and gives quesitons based on these. The program does not need any HTML, API, CSS, it completely run on a local engine.



2 Behavior Description:
    -1. User run the python quiz program (py quiz.py)
    -2. The program starts up and show welcome information "Welcome to use test"
    -3. User can choose: 
        - log in account
        - register a new account
    -4. Process of logging in account 
        - input User name and password
        - both thing are correct to enter the quiz
        - user can select "Forget user name/password"
    -5. Process of registering a new accout
        - input user name and password by user
        - re-input password function to check user remember the password
        - if user name has already existed, mention user and tell him use other names
        - privacy question provided, asking users birthday and last name
        - back to step 3
    -6. Process of "forget user name/password"
        - input user's birthday and the last name
        - user can change his user name and password
        - back to step 3
    -7. After logging in, users can choose the number of quesitions, categories (N/A means default, normal version), and difficulty they want
    -8. Select questions based on users' choice and weight questions weighted by their historical preferences (like/dislike) from question.json
    -9. For each question, 
        - show the question and options (if it has)
        - recevie user inputs
        - test user's answer, correct or wrong
        - show the result, whether user answers the answer correctly, and display the correct answer
        - after displaying result, user can choose like/dislike this question. (0 is dislike, 1 is like based no quesiton.json file)
    -10. Program stores user's grade and user's preference
    -11. After testing, show ending page, user can click "exit" to exit or "restart" to restart (back to step 7)



3 Data Format (question.json)
{
  "questions": [
    {
        "id": 1,
        "question": "Which regression is parametric regression?",
        "type": "multiple_choice",
        "options": ["Kernel Regression", "KNN Regression", "Linear Regression", "Spline Regression"],
        "answer": "Linear Regression",
        "category": "mixed",
        "difficulty": 1,
        "like": [0, 1]

    }, 
    {
        "id": 2,
        "question": "The MSE convergence speed of Kernel regression is O(__)? in 1 dimention"
        "type": "multiple_choice",
        "options": ["n^(-4/5)", "n^(-1)", "h^2 + n^p", "h^(4/5)"],
        "answer": "n^(-4/5)", 
        category: "Kernel regression",
        "difficulty": 3,
        "like": [0, 1]
    }, 
    {
        "id": 3,
        "question": "The bandwidth of kernel smoother decides whether the regression is straight or fluctuating.",
        "type": "true_false",
        "answer": "True",
        "category": "kernel regression",
        "difficulty": 1,
        "like": [0, 1]
    },
    {
        "id": 4,
        "question": "Kernel Smoother is linear smoother.",
        "type": "true_false",
        "answer": "True",
        "category": "kernel regression",
        "difficulty": 1,
        "like": [0, 1]
    },
    {
        "id": 5,
        "question": "In package 'mgcv' and 'gam', the function 's()' means smooth."
        "type": "true_false",
        "answer": "False",
        category: "additive regression",
        "difficulty": 3,
        "like": [0, 1]
    },
    {
        "id": 6,
        "question": "The following sudo code uses ___ ___ method.
        se_matrix <- replicate(100, {
            idx <- resample(1:len(dataset))
            new_dataset <- dataset[idx, ]
            fit <- regression(y ~ x, new_dataset)
            coefficient(fit)
        })
        required_se <- sd(se_matrix[, 1])
        ",
        "type": "short_answer",
        "answer": ["cases","bootstrap"] 
        "category": "bootstrap",
        "difficulty": 2,
        "like": [0, 1]
    },
    {
        "id": 7,
        "question": "In additive model, y = alpha + sum f(x_i), E[alpha] = ___?",
        "type": "short_answer",
        "answer": "0" 
        "category": "additive model",
        "difficulty": 1,
        "like": [0, 1]
    }
  ]
}



4 File Structure
15113-HW8-AGENTIC-BUILD
|
|-- app #folder
|   |-- quiz.py        # main program entrance, main file
|   |-- auth.py        # deal with: log in, register, forget password. (deal with users' user names and passwords)
|   |-- quiz_logic.py  # logic about question and scoring
|   |-- data_manage.py # data I/O (file operation)
|
|-- data #folder
|   |-- question.py    # question bank (readable)
|   |-- users.dat      # user data, user name + password(encryption)
|   |-- scores.dat     # score for each user(encryption)
|   |-- feedback.dat   # preference for each user (encryption)
|-- SPEC.md
|-- REVIEW.md
|-- REFLECTION.md



5 Error Handling
    -If JSON file is missed (not opend)
        - Output: "Error, question.json not opend/found"
    -If user input illegal answers
        - Let user input answer again, and show: "illegal answers". If user input illegal anwers over 3 times continuously, skip this question to the next one.
    -If user input the wrong user name + password in log-in page
        -hint user use "forget user name/password" function
    -If DAT file is missed (not opened)
        - Output: "Error, dat files are broken" and reset dat files
    -If question.json file has a wrong format
        - Output: "Error, JSON file is broken". And the exit the program.



6 Features
    - A local login system
        - user name + password
        - data(user name + password) stores as hashed method
        - be not allowed to store as human-readable file
    - Score history
        - users' scores and preference store as non-human-readable files
        - for each user, we store total question count, correct quesiton count, correct rate, preformance for each question.
    - Users' feedback
        - user can label like or dislike to each question
        - users' correctness will change the weight of each question
        - program will change the question weight based on users' like/dislike and their correctness
    - Question store
        - question should be put in "question.json" file. 
    - No HTML, CSS, IMAGE, API will be used. All thing will run locally.
    - User can select the category they want to test (the detailed categories seen "7 JSON file discription")
    - Score by difficulty
        - more difficult question (difficulty is 3) will earn extra credit if users answer correctly
        - easies quesition (difficulty is 1)will loss extra credit if users answer incorrectly
        - other cases will earn normal credit, which means wrong answer will not loss credit but correct answer will earn credit.
        - For example, medium question: correct -- add score, wrong -- no change; difficult question: correct-- add more score, wrong -- no change; easy question: correct -- add score, wrong -- loss score.



7 JSON file discription
    The question categority should include knowledge about kernel regression, knn regression, linear regression, spline regression, additive regression, bootstrap, additive regression, logistic regression, glm, gam, R code based above question, and mixed quesion. Question types are true_false, multiple choice, short answer. Difficulty includes 1 representing easy, 2 representing medium, 3 representing difficult. Like includes 0 representing dislike and 1 representing like.



8 Question weight
    When user gives a wrong answer, the question weight will increase; when user give a correct answer for question has bee increased by previous way, decrease the weight. When user gives dislike feedback, the question weight will decrease, but a like feedback will not increase the question weight, expect the question has been decreased weight. If question has been decreased weight due to dislike, like button will increase the weight. Question should be like a list. If users want to answer questions more than 10, there will be generated Question lists, each of which includes 10 questions. Once the current question list is done, based on user preference, generating the next 10 question list. For example, user input 12 question he wants to answer, their will be two question lists, L1 and L2, when L1 is finished, we give L2 based on his preference, and he answer 2 questions in L2, the program finishs and prepares to exit.  


9 Acceptance Criteria
    -The program can run by "py quiz.py" or "python quiz.py"
    -User can register and login successfully
    -User names and password are not readable by humans
    -Program will report Error and not crash when "question.json" or other DAT files are missed.
    -User can normally exit the program when test is finshed or Error is reported
    -Program can correctly show correctness and credit ( score)
    -Grade and user preferance can be recorded and updated, which can affect the following appearance of questions
    -Questions (professtional knowledge) should be correct
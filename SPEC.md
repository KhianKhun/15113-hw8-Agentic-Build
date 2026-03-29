1 Project Description


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
    -7. After logging in, users can choose the number of quesitions and difficulty they want
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


5 Error Handling


6 Features


7 Acceptance Criteria


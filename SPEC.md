1 Project Description


2 Behavior Description:


3 Data Format
{
  "questions": [
    {
        "id": 1,
        "question": "Which regression is parametric regression?",
        "type": "multiple_choice",
        "options": ["Kernel Regression", "KNN Regression", "Linear Regression", "Spline Regression"],
        "answer": "Linear Regression",
        "category": "mixed",
        "difficulty": 1

    }, 
    {
        "id": 2,
        "question": "The MSE convergence speed of Kernel regression is O(__)? in 1 dimention"
        "type": "multiple_choice",
        "options": ["n^(-4/5)", "n^(-1)", "h^2 + n^p", "h^(4/5)"],
        "answer": "n^(-4/5)", 
        category: "Kernel regression",
        "difficulty": 3
    }, 
    {
        "id": 3,
        "question": "The bandwidth of kernel smoother decides whether the regression is straight or fluctuating.",
        "type": "true_false",
        "answer": "True",
        "category": "kernel regression",
        "difficulty": 1
    },
    {
        "id": 4,
        "question": "Kernel Smoother is linear smoother.",
        "type": "true_false",
        "answer": "True",
        "category": "kernel regression",
        "difficulty": 1
    },
    {
        "id": 5,
        "question": "In package 'mgcv' and 'gam', the function 's()' means smooth."
        "type": "true_false",
        "answer": "False",
        category: "additive regression",
        "difficulty": 3
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
        "difficulty": 2
    },
    {
        "id": 7,
        "question": "In additive model, y = alpha + sum f(x_i), E[alpha] = ___?",
        "type": "short_answer",
        "answer": "0" 
        "category": "additive model",
        "difficulty": 1
    }
  ]
}


4 File Structure


5 Error Handling


6 Features


7 Acceptance Criteria


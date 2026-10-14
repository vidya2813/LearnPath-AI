
import os
import json
import joblib
import pandas as pd
import streamlit as st

# =====================================================
# 1. PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="LearnPath AI",
    page_icon="🎓",
    layout="wide"
)

MODEL_FILE = "learnpath_model.joblib"
PROGRESS_FILE = "learning_progress.json"

st.title("🎓 LearnPath AI")
st.subheader("Your Personalized Learning Path Generator")

st.write(
    "Learn new skills step by step. Get a personalized roadmap, "
    "study notes, quizzes, and recommendations about what to practise."
)

# =====================================================
# 2. LEARNING ROADMAPS
# =====================================================

roadmaps = {
    "Python Programming": [
        "Python variables and data types",
        "Operators and expressions",
        "Conditional statements",
        "Loops",
        "Lists, tuples, sets and dictionaries",
        "Functions",
        "File handling",
        "Mini Python project"
    ],

    "Programming Fundamentals": [
        "Introduction to programming",
        "Variables and data types",
        "Operators and expressions",
        "Conditional statements",
        "Loops",
        "Functions",
        "Basic problem-solving programs"
    ],

    "Data Structures": [
        "Introduction to data structures",
        "Arrays",
        "Searching algorithms",
        "Sorting algorithms",
        "Linked lists",
        "Stacks and queues",
        "Trees and graphs"
    ],

    "DBMS": [
        "Introduction to DBMS",
        "Relational model",
        "Keys and integrity constraints",
        "SQL queries",
        "Joins and subqueries",
        "Normalization: 1NF, 2NF and 3NF",
        "Transactions and concurrency"
    ],

    "Java Programming": [
        "Java basics and syntax",
        "Variables and data types",
        "Conditional statements and loops",
        "Classes and objects",
        "Inheritance and polymorphism",
        "Abstraction and interfaces",
        "Exception handling and collections"
    ],

    "Mathematics": [
        "Logic and propositions",
        "Sets and relations",
        "Functions",
        "Mathematical induction",
        "Number theory",
        "Combinatorics",
        "Probability"
    ],

    "Artificial Intelligence": [
        "Introduction to AI",
        "Intelligent agents",
        "Problem-solving and search",
        "Knowledge representation",
        "Reasoning",
        "Introduction to machine learning",
        "Build a beginner AI project"
    ],

    "Machine Learning": [
        "Introduction to machine learning",
        "Python and data handling",
        "NumPy and pandas",
        "Data visualization",
        "Supervised learning",
        "Unsupervised learning",
        "Model evaluation and a mini project"
    ],

    "DevOps": [
        "Introduction to DevOps",
        "Linux and command-line basics",
        "Git and GitHub",
        "Build tools",
        "CI/CD fundamentals",
        "Docker basics",
        "Deployment fundamentals"
    ],

    "GATE Preparation": [
        "Understand the GATE syllabus",
        "Engineering mathematics",
        "Discrete mathematics",
        "Data structures and algorithms",
        "Computer organization",
        "DBMS and operating systems",
        "Previous-year questions and mock tests"
    ]
}

# =====================================================
# 3. DETAILED STUDY NOTES
# =====================================================

notes = {
    "Python Programming": {
        "Python Variables and Data Types": '''
A variable stores a value.

Example:
name = "Ravi"
age = 18
marks = 85.5
is_student = True

Common data types:
- int: whole numbers
- float: decimal numbers
- str: text
- bool: True or False

Example output:
print(name)
print(age)
''',

        "Operators and Expressions": '''
Operators perform operations on values.

a = 10
b = 3

print(a + b)  # 13
print(a - b)  # 7
print(a * b)  # 30
print(a / b)  # 3.333...
print(a % b)  # 1
print(a ** b) # 1000

The % operator returns the remainder.
''',

        "Conditional Statements": '''
Conditions help a program make decisions.

marks = 75

if marks >= 40:
    print("Pass")
else:
    print("Fail")

Output:
Pass

Use elif to check additional conditions.
''',

        "Loops": '''
Loops repeat instructions.

for i in range(1, 4):
    print(i)

Output:
1
2
3

A while loop repeats while its condition is True.
''',

        "Lists, Tuples, Sets and Dictionaries": '''
List:
numbers = [10, 20, 30]
print(numbers[0])
Output: 10

Tuple:
values = (10, 20, 30)

Set:
unique_values = {1, 2, 2, 3}
A set stores unique values.

Dictionary:
student = {"name": "Ravi", "age": 18}
print(student["name"])
Output: Ravi
''',

        "Functions": '''
Functions are reusable blocks of code.

def add(a, b):
    return a + b

print(add(5, 3))

Output:
8

The def keyword defines a function.
The return statement sends a result back.
''',

        "File Handling": '''
Python can read and write files.

with open("notes.txt", "w") as file:
    file.write("Hello Python")

The w mode writes to a file and can replace
existing content. The with statement manages
closing the file when the block finishes.
''',

        "Mini Python Project": '''
Project: Simple Calculator

a = float(input("Enter first number: "))
b = float(input("Enter second number: "))

print("Sum:", a + b)
print("Difference:", a - b)
print("Product:", a * b)

This project practises variables, input,
type conversion and arithmetic operators.
'''
    },

    "Programming Fundamentals": {
        "Introduction to Programming": '''
Programming means writing instructions for a computer.

print("Hello, World!")

Output:
Hello, World!
''',

        "Variables and Data Types": '''
age = 18
price = 25.5
name = "Ravi"
is_ready = True

Common types include integers, floats,
strings and booleans.
''',

        "Operators and Expressions": '''
a = 10
b = 3

print(a + b)
print(a // b)
print(a % b)

Output:
13
3
1
''',

        "Conditional Statements": '''
number = 7

if number > 0:
    print("Positive")
elif number < 0:
    print("Negative")
else:
    print("Zero")
''',

        "Loops": '''
for i in range(1, 4):
    print(i)

Output:
1
2
3
''',

        "Functions": '''
def square(number):
    return number * number

print(square(4))

Output:
16
''',

        "Basic Problem Solving": '''
Steps:
1. Understand the problem.
2. Identify input and output.
3. Plan the logic.
4. Write the code.
5. Test your solution.
'''
    },

    "Data Structures": {
        "Introduction to Data Structures": '''
A data structure organizes data for efficient use.

Examples:
- Arrays
- Linked lists
- Stacks
- Queues
- Trees
- Graphs
''',

        "Arrays": '''
Arrays store elements accessed using indexes.

numbers = [10, 20, 30]

print(numbers[0])
print(numbers[2])

Output:
10
30

Python list indexes start at zero.
''',

        "Searching Algorithms": '''
Linear search checks elements one by one.

numbers = [10, 20, 30, 40]
key = 30

for i in range(len(numbers)):
    if numbers[i] == key:
        print("Found at index", i)
        break

Output:
Found at index 2

Binary search requires sorted data.
''',

        "Sorting Algorithms": '''
Sorting arranges elements in order.

numbers = [5, 2, 4, 1]
numbers.sort()
print(numbers)

Output:
[1, 2, 4, 5]

Common algorithms:
Bubble sort, selection sort,
insertion sort and quicksort.
''',

        "Linked Lists": '''
A linked list contains nodes.

Each node in a singly linked list stores:
- Data
- A reference to the next node

Nodes do not need to occupy consecutive
memory locations.
''',

        "Stacks and Queues": '''
Stack:
LIFO means Last In, First Out.
Push adds an element; pop removes the top.

Queue:
FIFO means First In, First Out.
Enqueue adds an element; dequeue removes
the front element.
''',

        "Trees and Graphs": '''
A tree organizes nodes hierarchically.

A graph contains vertices and edges.

Examples:
- Folder hierarchy: tree
- Road network: graph
'''
    },

    "DBMS": {
        "Introduction to DBMS": '''
A Database Management System helps store,
organize and retrieve data.

Examples: MySQL, Oracle Database,
and PostgreSQL.
''',

        "Relational Model": '''
A relational database organizes data into tables.

A row represents a record.
A column represents an attribute.

Example:
Student(Student_ID, Name, Marks)
''',

        "Keys and Integrity Constraints": '''
A primary key uniquely identifies a row.

A foreign key references a key in another table.

Common constraints:
PRIMARY KEY
FOREIGN KEY
UNIQUE
NOT NULL
CHECK
''',

        "SQL Queries": '''
Retrieve all records:

SELECT * FROM Student;

Retrieve selected records:

SELECT Name
FROM Student
WHERE Marks >= 40;

SQL is used to query and modify databases.
''',

        "Joins and Subqueries": '''
A JOIN combines related rows from tables.

SELECT Student.Name, Department.DeptName
FROM Student
JOIN Department
ON Student.DeptID = Department.DeptID;

A subquery is a query inside another query.
''',

        "Normalization": '''
Normalization helps reduce redundancy.

1NF: each cell contains a single value.

2NF: 1NF plus no partial dependency
of a non-prime attribute on a proper
subset of a candidate key.

3NF: 2NF plus no transitive dependency
of non-prime attributes on a candidate key.
''',

        "Transactions": '''
A transaction is a logical unit of database work.

ACID:
- Atomicity
- Consistency
- Isolation
- Durability
'''
    },

    "Java Programming": {
        "Java Basics": '''
public class Main {
    public static void main(String[] args) {
        System.out.println("Hello Java");
    }
}

Output:
Hello Java
''',

        "Variables and Data Types": '''
int age = 18;
double marks = 85.5;
char grade = 'A';
boolean passed = true;
String name = "Ravi";

Java is statically typed.
''',

        "Conditional Statements and Loops": '''
int marks = 75;

if (marks >= 40) {
    System.out.println("Pass");
} else {
    System.out.println("Fail");
}

for (int i = 1; i <= 3; i++) {
    System.out.println(i);
}
''',

        "Classes and Objects": '''
class Student {
    String name;

    Student(String name) {
        this.name = name;
    }
}

Student s = new Student("Ravi");

A class defines structure and behaviour.
An object is an instance of a class.
''',

        "Inheritance and Polymorphism": '''
Inheritance allows a class to extend another class.

class Animal {
    void sound() {
        System.out.println("Animal sound");
    }
}

class Dog extends Animal {
    void bark() {
        System.out.println("Bark");
    }
}

Polymorphism allows different behaviours
through a common interface.
''',

        "Abstraction and Interfaces": '''
Abstraction hides unnecessary implementation details.

An abstract class can contain abstract
and concrete methods.

An interface defines a contract for
implementing classes.
''',

        "Exception Handling": '''
try {
    int result = 10 / 0;
} catch (ArithmeticException e) {
    System.out.println("Cannot divide by zero");
} finally {
    System.out.println("Finished");
}

Exceptions help manage runtime problems.
'''
    },

    "Mathematics": {
        "Logic and Propositions": '''
A proposition is a statement that is either
true or false.

Example:
2 is an even number.

Logical operators include AND, OR and NOT.
''',

        "Sets and Relations": '''
A = {1, 2, 3}
B = {3, 4, 5}

A intersection B = {3}
A union B = {1, 2, 3, 4, 5}

A relation describes associations between elements.
''',

        "Functions": '''
A function maps each input in its domain
to exactly one output.

f(x) = 2x + 1

f(3) = 7
''',

        "Mathematical Induction": '''
Steps:
1. Prove the base case.
2. Assume the statement holds for n = k.
3. Prove it holds for n = k + 1.
4. State the conclusion.
''',

        "Number Theory": '''
Number theory studies integers and divisibility.

7 mod 3 = 1

The Euclidean algorithm finds the GCD
using repeated division.

A prime number has exactly two positive
divisors: 1 and itself.
''',

        "Combinatorics": '''
Permutations count ordered arrangements.

Combinations count selections where
order does not matter.

nCr = n! / (r! * (n-r)!)
''',

        "Probability": '''
For equally likely outcomes:

Probability =
favourable outcomes / total outcomes

Probability lies between 0 and 1.
'''
    },

    "Artificial Intelligence": {
        "Introduction to AI": '''
Artificial Intelligence develops systems
that perform tasks associated with intelligence.

Examples include language tools,
search systems and image recognition.
''',

        "Intelligent Agents": '''
An agent perceives its environment
and takes actions.

A robot may use sensors to navigate.
''',

        "Problem-Solving and Search": '''
Search algorithms explore possible states.

Breadth-first search explores level by level.
Depth-first search explores deeper paths first.
''',

        "Knowledge Representation": '''
Knowledge representation stores information
in a form that a system can use.

Examples include rules, logical statements
and semantic networks.
''',

        "Reasoning": '''
Reasoning uses known information
to derive conclusions.

Example:
If all humans are mortal and Ravi is human,
then Ravi is mortal.
''',

        "Introduction to Machine Learning": '''
Machine learning is a part of AI that
learns patterns from data.

Examples include classification,
prediction and clustering.
''',

        "Beginner AI Project": '''
Project idea: Rule-based study helper.

Input: a topic selected by a student.
Output: a matching note or study suggestion.

Start with simple rules before adding ML.
'''
    },

    "Machine Learning": {
        "Introduction to Machine Learning": '''
Machine learning builds models that
learn patterns from data.

A dataset contains examples and may
include target labels.
''',

        "Python and Data Handling": '''
pandas helps organize data in tables.

import pandas as pd
df = pd.read_csv("dataset.csv")
print(df.head())

head() displays the first rows.
''',

        "NumPy and pandas": '''
NumPy supports numerical arrays.

import numpy as np

numbers = np.array([1, 2, 3])
print(numbers.mean())

Output:
2.0
''',

        "Data Visualization": '''
Charts help reveal patterns.

Bar chart: compare categories.
Line chart: show changes over time.
Scatter plot: examine relationships.
''',

        "Supervised Learning": '''
Supervised learning uses labelled examples.

Classification predicts categories.
Regression predicts numerical values.
''',

        "Unsupervised Learning": '''
Unsupervised learning finds patterns
without provided target labels.

Clustering groups similar examples.
''',

        "Model Evaluation": '''
Evaluation measures model performance.

Classification metrics include accuracy,
precision, recall and F1 score.

Use data separate from training data
to estimate generalization.
'''
    },

    "DevOps": {
        "Introduction to DevOps": '''
DevOps connects software development
and IT operations to improve delivery.
''',

        "Linux and Command Line": '''
Useful commands:

pwd: show current directory
ls: list files on many Unix systems
cd: change directory
mkdir: create a directory
''',

        "Git and GitHub": '''
Git tracks changes to files.

git status
git add .
git commit -m "Update project"
git push

GitHub hosts repositories online.
''',

        "Build Tools": '''
Build tools compile code, manage dependencies
and package software.
''',

        "CI/CD": '''
Continuous Integration checks changes regularly.

Continuous Delivery or Deployment automates
steps in the release process.
''',

        "Docker Basics": '''
Docker packages applications and dependencies
into containers.

Containers help applications run consistently
across environments.
''',

        "Deployment": '''
Deployment makes an application available
to users.

Check configuration, dependencies,
secrets and logs before deployment.
'''
    },

    "GATE Preparation": {
        "Understand the GATE Syllabus": '''
Start with the official syllabus for
your specific GATE paper.

Break it into subjects and smaller topics.
''',

        "Engineering Mathematics": '''
Review the mathematics topics in your syllabus.

Practise definitions, formulas,
worked examples and previous questions.
''',

        "Discrete Mathematics": '''
Common areas include logic, sets,
relations, combinatorics and graph theory.
''',

        "Data Structures and Algorithms": '''
Study arrays, linked lists, stacks,
queues, trees, graphs, searching and sorting.

Practise tracing algorithms step by step.
''',

        "Computer Organization": '''
Study number representation, arithmetic,
digital logic, processors and memory
according to your syllabus.
''',

        "DBMS and Operating Systems": '''
DBMS: relational models, SQL, keys
and normalization.

Operating systems: processes, threads,
scheduling, synchronization and memory.
''',

        "Previous-Year Questions and Mock Tests": '''
Solve previous-year questions topic by topic.

Review incorrect answers and identify
concepts that need more practice.

Use mock tests to practise time management.
'''
    }
}

# =====================================================
# 4. QUIZ QUESTIONS
# =====================================================

quizzes = {
    "Python Programming": [
        {
            "topic": "Output and print function",
            "question": "Which function displays output in Python?",
            "options": ["input()", "print()", "display()", "show()"],
            "answer": 1
        },
        {
            "topic": "Variables and data types",
            "question": "Which data type stores True or False?",
            "options": ["int", "str", "bool", "float"],
            "answer": 2
        },
        {
            "topic": "Functions",
            "question": "Which keyword defines a function?",
            "options": ["function", "define", "fun", "def"],
            "answer": 3
        }
    ],

    "Programming Fundamentals": [
        {
            "topic": "Conditions",
            "question": "Which statement is used for a decision?",
            "options": ["if", "print", "input", "import"],
            "answer": 0
        },
        {
            "topic": "Loops",
            "question": "Which construct repeats instructions?",
            "options": ["Variable", "Loop", "Comment", "String"],
            "answer": 1
        },
        {
            "topic": "Functions",
            "question": "What is a function mainly used for?",
            "options": [
                "Storing only numbers",
                "Repeating code manually",
                "Reusing a block of code",
                "Deleting a program"
            ],
            "answer": 2
        }
    ],

    "Data Structures": [
        {
            "topic": "Stacks",
            "question": "Which data structure follows LIFO?",
            "options": ["Queue", "Stack", "Array", "Graph"],
            "answer": 1
        },
        {
            "topic": "Searching",
            "question": "Which search halves the search range in sorted data?",
            "options": ["Linear search", "Binary search", "Bubble sort", "DFS"],
            "answer": 1
        },
        {
            "topic": "Linked Lists",
            "question": "A singly linked-list node contains data and what?",
            "options": ["A next pointer", "A loop", "A database", "A compiler"],
            "answer": 0
        }
    ],

    "DBMS": [
        {
            "topic": "Introduction to DBMS",
            "question": "What does DBMS stand for?",
            "options": [
                "Data Backup Management Software",
                "Database Management System",
                "Digital Base Memory System",
                "Database Machine Setup"
            ],
            "answer": 1
        },
        {
            "topic": "Keys",
            "question": "Which key uniquely identifies a row?",
            "options": ["Foreign key", "Primary key", "Duplicate key", "Null key"],
            "answer": 1
        },
        {
            "topic": "SQL",
            "question": "Which SQL command retrieves records?",
            "options": ["SELECT", "DELETE", "DROP", "UPDATE"],
            "answer": 0
        }
    ],

    "Java Programming": [
        {
            "topic": "Objects",
            "question": "Which keyword creates an object?",
            "options": ["class", "new", "this", "void"],
            "answer": 1
        },
        {
            "topic": "Inheritance",
            "question": "Which keyword is used for class inheritance?",
            "options": ["implements", "inherits", "extends", "superclass"],
            "answer": 2
        },
        {
            "topic": "Exceptions",
            "question": "Which block handles an exception?",
            "options": ["try", "catch", "class", "package"],
            "answer": 1
        }
    ],

    "Mathematics": [
        {
            "topic": "Number Theory",
            "question": "What is 7 mod 3?",
            "options": ["0", "1", "2", "3"],
            "answer": 1
        },
        {
            "topic": "Number Theory",
            "question": "Which is a prime number?",
            "options": ["9", "15", "17", "21"],
            "answer": 2
        },
        {
            "topic": "Sets",
            "question": "What is a set with no elements called?",
            "options": ["Universal set", "Empty set", "Infinite set", "Subset"],
            "answer": 1
        }
    ],

    "Artificial Intelligence": [
        {
            "topic": "AI",
            "question": "What does AI stand for?",
            "options": [
                "Automated Internet",
                "Artificial Intelligence",
                "Advanced Information",
                "Applied Interface"
            ],
            "answer": 1
        },
        {
            "topic": "Search",
            "question": "Which is a common AI search algorithm?",
            "options": ["Breadth-first search", "Bubble sort", "Insertion sort", "Merge only"],
            "answer": 0
        },
        {
            "topic": "Agents",
            "question": "An intelligent agent interacts with what?",
            "options": ["Its environment", "Only a keyboard", "Only a database", "A compiler only"],
            "answer": 0
        }
    ],

    "Machine Learning": [
        {
            "topic": "Machine Learning",
            "question": "What does machine learning primarily do?",
            "options": [
                "Learns patterns from data",
                "Repairs hardware",
                "Creates electricity",
                "Only stores files"
            ],
            "answer": 0
        },
        {
            "topic": "Supervised Learning",
            "question": "Which is a supervised learning task?",
            "options": [
                "Clustering unlabeled data",
                "Classification using labeled data",
                "Random file sorting",
                "Deleting duplicate files"
            ],
            "answer": 1
        },
        {
            "topic": "Evaluation",
            "question": "Why evaluate a trained model?",
            "options": [
                "To measure performance",
                "To rename the computer",
                "To increase file size",
                "To remove the dataset"
            ],
            "answer": 0
        }
    ],

    "DevOps": [
        {
            "topic": "Git",
            "question": "What is Git mainly used for?",
            "options": ["Version control", "Image editing", "Video calls", "Database queries"],
            "answer": 0
        },
        {
            "topic": "CI/CD",
            "question": "What does CI/CD help automate?",
            "options": ["Software delivery", "Typing", "Computer cleaning", "Brightness"],
            "answer": 0
        },
        {
            "topic": "Docker",
            "question": "What is Docker commonly used for?",
            "options": ["Containers", "Spreadsheets", "Slide design", "Photo editing"],
            "answer": 0
        }
    ],

    "GATE Preparation": [
        {
            "topic": "Syllabus",
            "question": "What should you consult first to plan GATE study?",
            "options": ["Official syllabus", "Random videos only", "Social media", "No materials"],
            "answer": 0
        },
        {
            "topic": "Mock Tests",
            "question": "What helps identify weak topics?",
            "options": ["Mock tests", "Avoiding questions", "Skipping revision", "Reading titles only"],
            "answer": 0
        },
        {
            "topic": "Revision",
            "question": "What helps you understand GATE question patterns?",
            "options": ["Previous-year questions", "Ignoring syllabus", "Guessing only", "Skipping practice"],
            "answer": 0
        }
    ]
}

# =====================================================
# 5. PROGRESS STORAGE
# =====================================================

def load_progress():
    if os.path.exists(PROGRESS_FILE):
        try:
            with open(PROGRESS_FILE, "r", encoding="utf-8") as file:
                data = json.load(file)
                return data if isinstance(data, dict) else {}
        except (json.JSONDecodeError, OSError):
            return {}
    return {}


def save_progress(progress):
    try:
        with open(PROGRESS_FILE, "w", encoding="utf-8") as file:
            json.dump(progress, file, indent=4)
    except OSError:
        st.warning("Progress could not be saved to a local file.")


if "progress" not in st.session_state:
    st.session_state.progress = load_progress()

if "quiz_results" not in st.session_state:
    st.session_state.quiz_results = {}

if "show_study_notes" not in st.session_state:
    st.session_state.show_study_notes = True

# =====================================================
# 6. LEARNING PROFILE
# =====================================================

st.header("👤 1. Your Learning Profile")

branch = st.selectbox(
    "Choose your branch",
    ["CSE", "CSE (AI & ML)", "IT", "ECE", "Other"]
)

python_level = st.selectbox(
    "Your current programming level",
    ["Beginner", "Intermediate", "Advanced"]
)

quiz_score = st.slider(
    "Your current quiz score (%)",
    0, 100, 50
)

study_minutes = st.slider(
    "Daily study time (minutes)",
    15, 300, 60, step=15
)

goal = st.selectbox(
    "Your main learning goal",
    [
        "College exams",
        "GATE preparation",
        "Build projects",
        "Improve programming skills",
        "Career preparation"
    ]
)

# =====================================================
# 7. ML RECOMMENDATION
# =====================================================

st.header("🤖 2. Your ML Recommendation")

level_code_map = {
    "Beginner": 0,
    "Intermediate": 1,
    "Advanced": 2
}

goal_code_map = {
    "College exams": 0,
    "GATE preparation": 0,
    "Build projects": 2,
    "Improve programming skills": 0,
    "Career preparation": 1
}

branch_code_map = {
    "CSE": 0,
    "CSE (AI & ML)": 1,
    "IT": 2,
    "ECE": 3,
    "Other": 4
}

recommended_category = None

try:
    if not os.path.exists(MODEL_FILE):
        st.warning(
            "The trained model file was not found. "
            "Run train_model.py and ensure the model file is available."
        )
    else:
        saved_data = joblib.load(MODEL_FILE)

        if isinstance(saved_data, dict):
            model = saved_data["model"]
            feature_names = saved_data.get(
                "features",
                ["python_level", "quiz_score", "study_minutes", "goal"]
            )
            categories = saved_data.get("categories", [])
        else:
            model = saved_data
            feature_names = [
                "python_level", "quiz_score", "study_minutes", "goal"
            ]
            categories = []

        # Values available to match the model's training features.
        feature_values = {
            "python_level": level_code_map[python_level],
            "quiz_score": quiz_score,
            "study_minutes": study_minutes,
            "goal": goal_code_map[goal],
            "branch": branch_code_map[branch]
        }

        missing_features = [
            name for name in feature_names
            if name not in feature_values
        ]

        if missing_features:
            raise ValueError(
                "The model expects unsupported features: "
                + ", ".join(missing_features)
            )

        student_data = pd.DataFrame(
            [[feature_values[name] for name in feature_names]],
            columns=feature_names
        )

        prediction = model.predict(student_data)[0]

        # Decode an integer prediction if categories are encoded labels.
        if (
            categories
            and isinstance(prediction, (int,))
            and 0 <= prediction < len(categories)
        ):
            recommended_category = categories[prediction]
        else:
            recommended_category = prediction

        st.success(
            f"Recommended category: {recommended_category}"
        )

except Exception as error:
    st.warning("The ML recommendation is not available yet.")
    st.caption(f"Technical detail: {error}")

# =====================================================
# 8. SELECT LEARNING PATH
# =====================================================

category_to_subject = {
    "Programming Fundamentals": "Programming Fundamentals",
    "Python Programming": "Python Programming",
    "Data Structures": "Data Structures",
    "DBMS": "DBMS",
    "Java Programming": "Java Programming",
    "Mathematics": "Mathematics",
    "Artificial Intelligence": "Artificial Intelligence",
    "Machine Learning": "Machine Learning",
    "DevOps": "DevOps",
    "GATE Preparation": "GATE Preparation"
}

subjects = list(roadmaps.keys())

if recommended_category in category_to_subject:
    default_subject = category_to_subject[recommended_category]
else:
    default_subject = "Python Programming"

if "selected_subject" not in st.session_state:
    st.session_state.selected_subject = default_subject

st.header("🗺️ 3. Your Suggested Learning Roadmap")

st.write(
    "Complete each topic as you learn it. "
    "Your progress is saved locally in learning_progress.json."
)

selected_subject = st.selectbox(
    "Choose a subject to study",
    subjects,
    key="selected_subject"
)

# Keep notes and video subject selectors synchronized with the roadmap.
st.write(f"**Your selected learning path:** {selected_subject}")

# =====================================================
# 9. ROADMAP AND CHECKLIST
# =====================================================

topics = roadmaps[selected_subject]

for index, topic in enumerate(topics, start=1):
    progress_key = f"{selected_subject}::{topic}"

    st.checkbox(
        f"Step {index}: {topic}",
        value=bool(st.session_state.progress.get(progress_key, False)),
        key=f"roadmap_{selected_subject}_{index}",
        on_change=lambda key=progress_key, widget_key=(
            f"roadmap_{selected_subject}_{index}"
        ): (
            st.session_state.progress.update({
                key: st.session_state[widget_key]
            }),
            save_progress(st.session_state.progress)
        )
    )

completed_steps = sum(
    bool(st.session_state.progress.get(
        f"{selected_subject}::{topic}", False
    ))
    for topic in topics
)

total_steps = len(topics)
percentage = completed_steps / total_steps if total_steps else 0

st.progress(percentage)

st.write(
    f"**Progress: {completed_steps}/{total_steps} topics completed "
    f"({round(percentage * 100)}%)**"
)

if topics:
    next_topics = [
        topic for topic in topics
        if not st.session_state.progress.get(
            f"{selected_subject}::{topic}", False
        )
    ]

    if next_topics:
        st.info(f"Start with: {next_topics[0]}")
    else:
        st.success("Congratulations! You completed this roadmap.")

# =====================================================
# 10. STUDY NOTES AND VIDEO LESSONS
# =====================================================

st.header("📚 4. Study Notes and Video Lessons")

notes_subject = st.selectbox(
    "Choose a subject for study notes",
    list(notes.keys()),
    index=(
        list(notes.keys()).index(selected_subject)
        if selected_subject in notes
        else 0
    ),
    key="notes_subject"
)

open_col, hide_col = st.columns(2)

with open_col:
    if st.button("📖 Open study notes", use_container_width=True):
        st.session_state.show_study_notes = True

with hide_col:
    if st.button("🙈 Hide study notes", use_container_width=True):
        st.session_state.show_study_notes = False

if st.session_state.show_study_notes:
    for topic, explanation in notes[notes_subject].items():
        with st.expander(topic):
            st.markdown(explanation)

st.caption(
    "The YouTube button opens search results. "
    "Choose lessons that match your syllabus and current level."
)

st.write(f"**Suggested daily study time:** {study_minutes} minutes")

st.write(
    "Try learning one concept, practising questions, "
    "and reviewing mistakes."
)

video_topics = roadmaps.get(notes_subject, [])

if video_topics:
    video_topic = st.selectbox(
        "Choose a topic for video lessons",
        video_topics,
        key="video_topic"
    )

    from urllib.parse import quote_plus

    video_url = (
        "https://www.youtube.com/results?search_query="
        + quote_plus(notes_subject + " " + video_topic)
    )

    st.link_button("▶️ Search YouTube lessons", video_url)

# =====================================================
# 11. TOPIC-WISE QUIZ
# =====================================================

st.header("🧠 5. Test Your Knowledge")

st.write(
    "Answer the questions to find out which topics you may need "
    "to revise. Your report is based on this quiz attempt."
)

quiz_subject = st.selectbox(
    "Choose a quiz subject",
    list(quizzes.keys()),
    index=(
        list(quizzes.keys()).index(selected_subject)
        if selected_subject in quizzes
        else 0
    ),
    key="quiz_subject"
)

quiz_questions = quizzes[quiz_subject]

with st.form(key=f"quiz_form_{quiz_subject}"):
    submitted_answers = {}

    for index, question in enumerate(quiz_questions):
        st.markdown(f"📌 **Topic: {question['topic']}**")
        st.markdown(
            f"**Question {index + 1}: {question['question']}**"
        )

        submitted_answers[index] = st.radio(
            "Choose your answer:",
            question["options"],
            index=None,
            key=f"quiz_{quiz_subject}_{index}"
        )

    submitted = st.form_submit_button("Submit Quiz")

if submitted:
    correct_count = 0
    missed_topics = []

    for index, question in enumerate(quiz_questions):
        answer = submitted_answers[index]
        correct_answer = question["options"][question["answer"]]

        if answer == correct_answer:
            correct_count += 1
        else:
            missed_topics.append(question["topic"])

    score_percent = round(
        100 * correct_count / len(quiz_questions)
    )

    st.session_state.quiz_results[quiz_subject] = {
        "correct": correct_count,
        "total": len(quiz_questions),
        "percentage": score_percent,
        "missed_topics": missed_topics
    }

if quiz_subject in st.session_state.quiz_results:
    result = st.session_state.quiz_results[quiz_subject]

    st.subheader("📊 Your Quiz Report")

    st.metric(
        "Correct answers",
        f"{result['correct']}/{result['total']}"
    )

    st.write(f"**Score: {result['percentage']}%**")
    st.progress(result["percentage"] / 100)

    if result["percentage"] == 100:
        st.success("Excellent! You answered every question correctly.")
    elif result["percentage"] >= 50:
        st.info("Good work! Review the topics you missed.")
    else:
        st.info("Keep practising. Read the notes and try again.")

    if result["missed_topics"]:
        st.subheader("📌 Topics to Revise")

        for topic in sorted(set(result["missed_topics"])):
            st.write(f"- {topic}")
    else:
        st.success("No missed topics. Great work!")

    if st.button("🔄 Clear Quiz Report"):
        del st.session_state.quiz_results[quiz_subject]
        st.rerun()

# =====================================================
# 12. OVERALL LEARNING PROGRESS
# =====================================================

st.header("🏆 6. Your Learning Progress")

all_topics = [
    (subject, topic)
    for subject, topic_list in roadmaps.items()
    for topic in topic_list
]

total_all_steps = len(all_topics)

completed_all_steps = sum(
    bool(st.session_state.progress.get(
        f"{subject}::{topic}", False
    ))
    for subject, topic in all_topics
)

overall_percentage = (
    completed_all_steps / total_all_steps
    if total_all_steps else 0
)

st.metric(
    "Completed roadmap steps",
    f"{completed_all_steps}/{total_all_steps}"
)

st.progress(overall_percentage)

st.write(f"**Overall progress: {round(overall_percentage * 100)}%**")

st.divider()

st.write(
    "💡 **LearnPath AI** | Machine Learning Recommendations | "
    "Personalized Roadmaps | Topic-wise Quiz Feedback"
)

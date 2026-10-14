
import json
import os
from urllib.parse import quote_plus

import joblib
import pandas as pd
import streamlit as st


# ==================================================
# 1. PAGE CONFIGURATION
# ==================================================

st.set_page_config(
    page_title="LearnPath AI",
    page_icon="🎓",
    layout="wide"
)

st.title("🎓 LearnPath AI")
st.subheader("Your Personalized Learning Path Generator")

st.write(
    "Learn new skills step by step. Get a personalized roadmap, "
    "study notes, quizzes, and recommendations about what to practise."
)

st.divider()


# ==================================================
# 2. FILE PATHS
# ==================================================

MODEL_FILE = "learnpath_model.joblib"
PROGRESS_FILE = "learning_progress.json"


# ==================================================
# 3. LEARNING ROADMAPS
# ==================================================

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

    "Data Structures": [
        "Introduction to data structures",
        "Arrays and array operations",
        "Linear search and binary search",
        "Bubble sort and selection sort",
        "Linked lists",
        "Stacks",
        "Queues and circular queues",
        "Trees and heaps"
    ],

    "DBMS": [
        "Introduction to DBMS",
        "Relational model and tables",
        "Primary keys and foreign keys",
        "Integrity constraints",
        "SQL queries",
        "Relational algebra",
        "Functional dependencies",
        "Normalization: 1NF, 2NF and 3NF"
    ],

    "Java Programming": [
        "Java introduction and syntax",
        "Variables and data types",
        "Conditional statements and loops",
        "Classes and objects",
        "Constructors and the this keyword",
        "Inheritance and polymorphism",
        "Interfaces and abstract classes",
        "Exception handling"
    ],

    "Mathematics": [
        "Properties of integers",
        "Division theorem",
        "Greatest common divisor (GCD)",
        "Euclidean algorithm",
        "Least common multiple (LCM)",
        "Prime numbers",
        "Modular arithmetic",
        "Mathematical induction"
    ],

    "Artificial Intelligence": [
        "Introduction to Artificial Intelligence",
        "Intelligent agents",
        "Problem-solving and search",
        "Breadth-first search and depth-first search",
        "Knowledge representation",
        "Reasoning in AI",
        "Introduction to machine learning",
        "Build a simple AI project"
    ],

    "Machine Learning": [
        "Introduction to Machine Learning",
        "Supervised and unsupervised learning",
        "Features and labels",
        "Training and testing datasets",
        "Classification algorithms",
        "Regression algorithms",
        "Model evaluation",
        "Build a machine learning project"
    ],

    "DevOps": [
        "Introduction to DevOps",
        "Git and version control",
        "GitHub basics",
        "Linux command-line basics",
        "Continuous integration",
        "Continuous delivery and deployment",
        "Docker fundamentals",
        "Build a simple CI/CD workflow"
    ],

    "GATE Preparation": [
        "Understand the GATE syllabus",
        "Engineering mathematics",
        "General aptitude",
        "Data Structures and Algorithms",
        "Database Management Systems",
        "Operating Systems",
        "Computer Networks",
        "Previous-year questions and revision"
    ]
}


# ==================================================
# 4. STUDY NOTES
# ==================================================

notes = {
    "Python Programming": """
### Python Variables and Data Types

A variable stores a value.

```python
name = "Ravi"
age = 18
marks = 85.5
```

Common data types:
- int: whole numbers
- float: decimal numbers
- str: text
- bool: True or False

### Conditional Statements

```python
marks = 75

if marks >= 40:
    print("Pass")
else:
    print("Fail")
```

### Loops

Loops repeat a block of code.

```python
for i in range(1, 4):
    print(i)
```

Output: 1, 2, 3
""",

    "Data Structures": """
### What is a Data Structure?

A data structure organizes data so that it can be stored and processed efficiently.

### Stack

A stack follows LIFO: Last In, First Out.

Main operations:
- Push: insert an element
- Pop: remove the top element
- Peek: view the top element

### Queue

A queue follows FIFO: First In, First Out.

Main operations:
- Enqueue: insert an element
- Dequeue: remove an element

### Searching

Linear search checks elements one by one.

Binary search repeatedly divides a sorted search range into halves.
""",

    "DBMS": """
### What is DBMS?

A Database Management System helps users store, organize and retrieve data.

### Keys

- Primary key: uniquely identifies each row.
- Foreign key: refers to a key in another table.
- Candidate key: a minimal set of attributes that uniquely identifies a row.

### SQL Example

```sql
SELECT *
FROM Student
WHERE marks >= 80;
```

### Normalization

Normalization organizes tables to reduce unwanted data duplication and modification problems.

- 1NF: each field contains an atomic value.
- 2NF: 1NF plus no partial dependency of a non-key attribute on a candidate key.
- 3NF: 2NF plus no inappropriate transitive dependency of non-key attributes on a candidate key.
""",

    "Java Programming": """
### Classes and Objects

A class defines the structure and behaviour of objects.

```java
class Student {
    int marks;

    void display() {
        System.out.println(marks);
    }
}
```

Creating an object:

```java
Student s = new Student();
s.marks = 90;
s.display();
```

### Inheritance

Inheritance allows a class to acquire accessible features from another class.

### Polymorphism

Polymorphism allows the same interface or method name to have different behaviour.

### Exception Handling

Java uses try, catch and finally to manage exceptions.
""",

    "Mathematics": """
### Greatest Common Divisor (GCD)

The GCD is the greatest positive integer that divides two integers exactly.

Example:

GCD(12, 18) = 6

### Euclidean Algorithm

Repeatedly divide and replace the pair with the divisor and remainder until the remainder is zero.

Example:

18 = 12 × 1 + 6

12 = 6 × 2 + 0

Therefore, GCD(18, 12) = 6.

### Prime Numbers

A prime number is an integer greater than 1 with exactly two positive divisors: 1 and itself.
""",

    "Artificial Intelligence": """
### What is Artificial Intelligence?

AI involves building systems that perform tasks associated with abilities such as reasoning, learning and decision-making.

### Intelligent Agents

An intelligent agent observes its environment and takes actions.

### Search Algorithms

- BFS: explores a graph level by level.
- DFS: explores a path deeply before backtracking.

### Applications

AI is used in image recognition, language processing, recommendations and robotics.
""",

    "Machine Learning": """
### What is Machine Learning?

Machine Learning (ML) allows computer systems to learn patterns from data and use them to make predictions or decisions.

### Types of ML

- Supervised learning: learns from labelled examples.
- Unsupervised learning: finds patterns in unlabelled data.
- Reinforcement learning: learns through interaction and feedback.

### Classification

Classification predicts a category, such as spam or not spam.

### Model Evaluation

A test dataset helps evaluate how well a model performs on data it did not train on.
""",

    "DevOps": """
### What is DevOps?

DevOps combines development and operations practices to help teams deliver and maintain software reliably.

### Git

Git tracks changes to files and source code.

Common commands:

```bash
git init
git status
git add .
git commit -m "First commit"
```

### CI/CD

Continuous Integration (CI) helps integrate and test code changes frequently.

Continuous Delivery or Deployment (CD) automates later stages of delivering software.

### Docker

Docker packages an application and its dependencies into containers.
""",

    "GATE Preparation": """
### Starting GATE Preparation

1. Read the official syllabus for your paper.
2. Learn one concept at a time.
3. Solve topic-wise practice questions.
4. Review mistakes.
5. Practise previous-year questions.

### Useful Areas to Build

- Engineering mathematics
- General aptitude
- Data Structures and Algorithms
- DBMS
- Operating Systems
- Computer Networks

Check the official GATE syllabus for your examination year before finalizing your study plan.
"""
}


# ==================================================
# 5. QUIZ QUESTIONS
# Each question contains:
# (question, options, correct_option_index)
# ==================================================

quiz_questions = {
    "Python Programming": [
        (
            "Which function displays output in Python?",
            ["input()", "print()", "display()", "show()"],
            1
        ),
        (
            "Which data type stores True or False?",
            ["int", "str", "bool", "float"],
            2
        ),
        (
            "Which keyword is used to define a function?",
            ["function", "define", "fun", "def"],
            3
        )
    ],

    "Data Structures": [
        (
            "Which principle does a stack follow?",
            ["FIFO", "LIFO", "Random order", "Sorted order"],
            1
        ),
        (
            "Which principle does a normal queue follow?",
            ["LIFO", "Random order", "FIFO", "Reverse order"],
            2
        ),
        (
            "Which search algorithm requires sorted data?",
            ["Linear search", "Binary search", "Neither", "Both always"],
            1
        )
    ],

    "DBMS": [
        (
            "What is the main purpose of a DBMS?",
            [
                "Only to draw pictures",
                "To manage databases",
                "Only to compile Java",
                "To design web pages"
            ],
            1
        ),
        (
            "What does a primary key do?",
            [
                "Allows duplicate row identifiers",
                "Stores only images",
                "Uniquely identifies a row",
                "Deletes all records"
            ],
            2
        ),
        (
            "Which SQL command retrieves data?",
            ["INSERT", "UPDATE", "DELETE", "SELECT"],
            3
        )
    ],

    "Java Programming": [
        (
            "Which keyword is used to create a class in Java?",
            ["class", "define", "struct", "object"],
            0
        ),
        (
            "Which method is the usual entry point of a Java application?",
            [
                "start()",
                "main()",
                "runMain()",
                "execute()"
            ],
            1
        ),
        (
            "Which keyword creates an object in Java?",
            ["class", "this", "new", "static"],
            2
        )
    ],

    "Mathematics": [
        (
            "What is GCD(12, 18)?",
            ["2", "3", "6", "9"],
            2
        ),
        (
            "What is 2 to the power of 3?",
            ["5", "6", "8", "9"],
            2
        ),
        (
            "Which number is prime?",
            ["9", "15", "17", "21"],
            2
        )
    ],

    "Artificial Intelligence": [
        (
            "Which is an application of AI?",
            [
                "Image recognition",
                "A plain notebook",
                "An ordinary ruler",
                "An unpowered chair"
            ],
            0
        ),
        (
            "Which algorithm explores a graph level by level?",
            ["DFS", "BFS", "Binary search", "Selection sort"],
            1
        ),
        (
            "What does an intelligent agent do?",
            [
                "Only stores files",
                "Only displays text",
                "Observes its environment and acts",
                "Always performs sorting"
            ],
            2
        )
    ],

    "Machine Learning": [
        (
            "What is Machine Learning?",
            [
                "A type of computer hardware",
                "A way for systems to learn patterns from data",
                "A programming keyboard",
                "A database table"
            ],
            1
        ),
        (
            "Which task is a classification problem?",
            [
                "Predicting an exact temperature",
                "Adding two numbers",
                "Predicting spam or not spam",
                "Sorting a list alphabetically"
            ],
            2
        ),
        (
            "Why do we test a trained ML model?",
            [
                "To evaluate performance on unseen data",
                "To delete the training data",
                "To change the keyboard",
                "To remove every feature"
            ],
            0
        )
    ],

    "DevOps": [
        (
            "What is Git mainly used for?",
            [
                "Editing photographs",
                "Version control",
                "Playing music",
                "Creating hardware"
            ],
            1
        ),
        (
            "What does CI stand for in CI/CD?",
            [
                "Code Installation",
                "Computer Internet",
                "Continuous Integration",
                "Central Information"
            ],
            2
        ),
        (
            "What does Docker help create and run?",
            ["Documents", "Spreadsheets", "Slides", "Containers"],
            3
        )
    ],

    "GATE Preparation": [
        (
            "What should you consult to identify GATE topics?",
            [
                "A random timetable only",
                "The official syllabus",
                "Social media comments only",
                "An unrelated textbook"
            ],
            1
        ),
        (
            "Which data structure follows LIFO?",
            ["Queue", "Stack", "Graph", "Array only"],
            1
        ),
        (
            "What is a useful way to practise for GATE?",
            [
                "Avoid solving questions",
                "Read without revision",
                "Solve previous-year questions",
                "Study only on the exam day"
            ],
            2
        )
    ]
}


# ==================================================
# 6. TOPIC LABELS FOR QUIZ QUESTIONS
# Keep these in the same order as quiz_questions.
# ==================================================

quiz_topics = {
    "Python Programming": [
        "Output and print function",
        "Variables and data types",
        "Functions"
    ],

    "Data Structures": [
        "Stack and LIFO",
        "Queue and FIFO",
        "Searching algorithms"
    ],

    "DBMS": [
        "DBMS fundamentals",
        "Primary keys",
        "SQL queries"
    ],

    "Java Programming": [
        "Classes and objects",
        "Main method",
        "Object creation"
    ],

    "Mathematics": [
        "GCD",
        "Powers and exponents",
        "Prime numbers"
    ],

    "Artificial Intelligence": [
        "AI applications",
        "Search algorithms",
        "Intelligent agents"
    ],

    "Machine Learning": [
        "ML fundamentals",
        "Classification",
        "Model evaluation"
    ],

    "DevOps": [
        "Version control with Git",
        "CI/CD",
        "Docker containers"
    ],

    "GATE Preparation": [
        "GATE syllabus",
        "Stacks",
        "Previous-year questions"
    ]
}


# ==================================================
# 7. PROGRESS TRACKING FUNCTIONS
# ==================================================

def load_progress():
    """Load saved learning progress from a JSON file."""
    if os.path.exists(PROGRESS_FILE):
        try:
            with open(PROGRESS_FILE, "r", encoding="utf-8") as file:
                data = json.load(file)

            if isinstance(data, dict):
                return data

        except (json.JSONDecodeError, OSError):
            pass

    return {}


def save_progress():
    """Save learning progress to a JSON file."""
    try:
        with open(PROGRESS_FILE, "w", encoding="utf-8") as file:
            json.dump(
                st.session_state.progress_data,
                file,
                indent=4
            )
    except OSError:
        st.error("Unable to save progress. Check folder permissions.")


def update_topic_progress(subject, topic, widget_key):
    """Update progress when a topic checkbox changes."""
    completed = st.session_state.progress_data.get(subject, [])

    if st.session_state[widget_key]:
        if topic not in completed:
            completed.append(topic)
    else:
        if topic in completed:
            completed.remove(topic)

    st.session_state.progress_data[subject] = completed
    save_progress()


if "progress_data" not in st.session_state:
    st.session_state.progress_data = load_progress()


# ==================================================
# 8. STUDENT PROFILE AND ML RECOMMENDATION
# ==================================================

st.header("👤 1. Your Learning Profile")

col1, col2 = st.columns(2)

with col1:
    branch = st.selectbox(
        "Choose your branch",
        [
            "CSE",
            "CSE (AI & ML)",
            "IT",
            "ECE",
            "Other"
        ]
    )

    python_level = st.selectbox(
        "Your current programming level",
        ["Beginner", "Intermediate", "Advanced"]
    )

    quiz_score = st.slider(
        "Your current quiz score (%)",
        min_value=0,
        max_value=100,
        value=50,
        step=5
    )

with col2:
    study_minutes = st.slider(
        "Daily study time (minutes)",
        min_value=15,
        max_value=300,
        value=60,
        step=15
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

    selected_subject = st.selectbox(
        "Choose a subject to study",
        list(roadmaps.keys())
    )


# These numerical mappings must match the mappings used when
# training your model in train_model.py.
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

category_to_subject = {
    "Programming Fundamentals": "Python Programming",
    "AI Fundamentals": "Artificial Intelligence",
    "Machine Learning": "Machine Learning"
}

recommended_category = None
model_error = None

if os.path.exists(MODEL_FILE):
    try:
        model = joblib.load(MODEL_FILE)

        student_data = pd.DataFrame(
            [[
                level_code_map[python_level],
                quiz_score,
                study_minutes,
                goal_code_map[goal]
            ]],
            columns=[
                "python_level",
                "quiz_score",
                "study_minutes",
                "goal"
            ]
        )

        recommended_category = model.predict(student_data)[0]

    except Exception as error:
        model_error = str(error)

else:
    model_error = (
        "The trained model file was not found. "
        "Run train_model.py first."
    )


st.header("🤖 2. Your ML Recommendation")

if recommended_category is not None:
    st.success(
        f"Recommended learning category: **{recommended_category}**"
    )

    st.caption(
        "This is a recommendation from your trained model. "
        "Because the current dataset is small, treat it as a starting point."
    )
else:
    st.warning("The ML recommendation is not available yet.")
    st.caption(model_error)


# Select which roadmap to display.
if goal == "GATE preparation":
    roadmap_subject = "GATE Preparation"

elif goal == "Build projects":
    roadmap_subject = selected_subject

elif goal == "College exams":
    roadmap_subject = selected_subject

elif recommended_category in category_to_subject:
    roadmap_subject = category_to_subject[recommended_category]

else:
    roadmap_subject = selected_subject


st.info(f"Your selected learning path: **{roadmap_subject}**")


# ==================================================
# 9. PERSONALIZED ROADMAP AND PROGRESS
# ==================================================

st.divider()
st.header("🗺️ 3. Your Suggested Learning Roadmap")

st.write(
    "Complete each topic as you learn it. Your progress is saved "
    "locally in learning_progress.json."
)

topics = roadmaps[roadmap_subject]
completed_topics = st.session_state.progress_data.get(
    roadmap_subject, []
)

completed_count = sum(
    1 for topic in topics if topic in completed_topics
)

progress_percentage = completed_count / len(topics)

st.progress(progress_percentage)

st.write(
    f"**Progress: {completed_count}/{len(topics)} topics completed "
    f"({round(progress_percentage * 100)}%)**"
)

for index, topic in enumerate(topics):
    widget_key = f"progress_{roadmap_subject}_{index}"

    st.checkbox(
        f"Step {index + 1}: {topic}",
        value=topic in completed_topics,
        key=widget_key,
        on_change=update_topic_progress,
        args=(roadmap_subject, topic, widget_key)
    )

if completed_count == len(topics):
    st.success("🎉 Excellent! You have completed this roadmap.")

elif completed_count > 0:
    next_topic = next(
        topic for topic in topics if topic not in completed_topics
    )
    st.info(f"Your next topic: **{next_topic}**")

else:
    st.info(f"Start with: **{topics[0]}**")


# ==================================================
# 10. STUDY NOTES AND VIDEO LESSONS
# ==================================================

st.divider()
st.header("📚 4. Study Notes and Video Lessons")

notes_subject = st.selectbox(
    "Choose a subject for study notes",
    list(notes.keys()),
    key="notes_subject"
)

with st.expander("Open study notes", expanded=True):
    st.markdown(notes[notes_subject])

search_query = quote_plus(
    notes_subject + " tutorial for beginners"
)

youtube_url = (
    "https://www.youtube.com/results?search_query="
    + search_query
)

st.link_button(
    "▶️ Find video lessons on YouTube",
    youtube_url
)

st.caption(
    "The YouTube button opens search results. Choose lessons "
    "that match your syllabus and current level."
)

st.write(
    f"**Suggested daily study time:** {study_minutes} minutes"
)

if study_minutes < 30:
    st.write("Try a short lesson and solve two or three practice questions.")
elif study_minutes < 90:
    st.write("Try learning one concept, practising questions, and reviewing mistakes.")
else:
    st.write("Divide your session into learning, practice, and revision breaks.")


# ==================================================
# 11. QUIZ WITH TOPIC-WISE FEEDBACK
# ==================================================

st.divider()
st.header("🧠 5. Test Your Knowledge")

st.write(
    "Answer the questions to find out which topics you may need "
    "to revise. Your report is based on this quiz attempt."
)

quiz_subject = st.selectbox(
    "Choose a quiz subject",
    list(quiz_questions.keys()),
    key="quiz_subject"
)

questions = quiz_questions[quiz_subject]
quiz_topic_list = quiz_topics[quiz_subject]

with st.form("quiz_form"):
    answers = []

    for index, (question, options, correct_index) in enumerate(questions):
        st.caption(f"📌 Topic: {quiz_topic_list[index]}")

        answer = st.radio(
            f"Question {index + 1}: {question}",
            options,
            index=None,
            key=f"answer_{quiz_subject}_{index}"
        )

        answers.append(answer)

    submitted = st.form_submit_button("Submit Quiz")


if submitted:
    score = 0
    topic_results = {}

    for index, (question, options, correct_index) in enumerate(questions):
        topic = quiz_topic_list[index]
        correct_answer = options[correct_index]

        is_correct = answers[index] == correct_answer

        if topic not in topic_results:
            topic_results[topic] = {
                "correct": 0,
                "total": 0,
                "missed_questions": []
            }

        topic_results[topic]["total"] += 1

        if is_correct:
            score += 1
            topic_results[topic]["correct"] += 1

        else:
            topic_results[topic]["missed_questions"].append({
                "question": question,
                "correct_answer": correct_answer
            })

    total_questions = len(questions)
    percentage = round((score / total_questions) * 100)

    st.session_state["latest_quiz_report"] = {
        "subject": quiz_subject,
        "score": score,
        "total": total_questions,
        "percentage": percentage,
        "topic_results": topic_results
    }


# Show the latest report again on later reruns during this session.
if "latest_quiz_report" in st.session_state:
    report = st.session_state["latest_quiz_report"]

    st.divider()
    st.header("📊 6. Your Quiz Report")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Score",
        f"{report['score']}/{report['total']}"
    )

    col2.metric(
        "Percentage",
        f"{report['percentage']}%"
    )

    col3.metric(
        "Subject",
        report["subject"]
    )

    st.subheader("Topic-wise performance")

    weak_topics = []

    for topic, result in report["topic_results"].items():
        correct = result["correct"]
        total = result["total"]

        topic_percentage = round((correct / total) * 100)

        st.write(f"**{topic}: {correct}/{total} correct**")
        st.progress(topic_percentage / 100)

        if correct < total:
            weak_topics.append(topic)

    st.divider()
    st.header("🎯 7. What Should You Practise More?")

    if weak_topics:
        st.warning(
            "You missed questions from the topics below. "
            "Start your revision with these areas."
        )

        for topic in weak_topics:
            result = report["topic_results"][topic]

            st.markdown(f"### 📖 {topic}")

            for missed in result["missed_questions"]:
                st.write(f"**Question:** {missed['question']}")
                st.write(
                    f"**Correct answer:** {missed['correct_answer']}"
                )

            st.write(
                f"**Your next step:** Revise **{topic}**, practise "
                "similar questions, and then try another quiz."
            )

    else:
        st.success(
            "Excellent! You answered every question correctly. "
            "Try a more challenging quiz or move to the next topic."
        )

    st.caption(
        "Important: Each topic currently has one quiz question. "
        "A missed question is a useful revision clue, not a complete "
        "measurement of your knowledge. Adding more questions per topic "
        "will make the recommendations more reliable."
    )


# ==================================================
# 12. FOOTER
# ==================================================

st.divider()

st.caption(
    "LearnPath AI | Machine Learning Recommendations | "
    "Personalized Roadmaps | Topic-wise Quiz Feedback"
)
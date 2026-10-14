
import os
import json
import joblib
import pandas as pd
import streamlit as st

# ---------------- PAGE CONFIGURATION ----------------

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
    "Tell us about your current skills and learning goals. "
    "Our ML model will recommend a learning path for you."
)

# ---------------- LEARNING ROADMAPS ----------------

roadmaps = {
    "Python Programming": [
        "Python variables and data types",
        "Conditional statements",
        "Loops",
        "Functions",
        "Lists, tuples, sets and dictionaries",
        "File handling",
        "Mini project using Python"
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

# ---------------- STUDY NOTES ----------------

notes = {
    "Python Programming": {
        "Variables": "Variables store values. Example: age = 18",
        "Conditions": "Use if, elif and else to make decisions.",
        "Loops": "Use for and while loops to repeat instructions.",
        "Functions": "Functions are reusable blocks of code defined using def."
    },

    "Programming Fundamentals": {
        "Variables": "Variables store data used by a program.",
        "Conditions": "Conditional statements select which code to execute.",
        "Loops": "Loops repeat a block of instructions.",
        "Functions": "Functions divide a program into reusable parts."
    },

    "Data Structures": {
        "Arrays": "Arrays store elements that can be accessed using indexes.",
        "Searching": "Linear search checks elements one by one.",
        "Sorting": "Sorting arranges data in ascending or descending order.",
        "Linked Lists": "Linked lists contain nodes connected using pointers.",
        "Stacks": "Stacks follow LIFO: Last In, First Out.",
        "Queues": "Queues generally follow FIFO: First In, First Out."
    },

    "DBMS": {
        "Keys": "Keys help identify records and establish relationships.",
        "SQL": "SQL is used to define, query and manipulate relational data.",
        "Normalization": "Normalization organizes tables to reduce redundancy.",
        "Transactions": "Transactions are logical units of database work."
    },

    "Java Programming": {
        "Classes": "A class defines the data and behavior of objects.",
        "Objects": "An object is an instance of a class.",
        "Inheritance": "Inheritance lets a class reuse another class's features.",
        "Polymorphism": "Polymorphism allows one interface to have different behaviors.",
        "Exceptions": "Exception handling manages errors using try, catch and finally."
    },

    "Mathematics": {
        "Logic": "Propositional logic studies statements and their truth values.",
        "Sets": "A set is a collection of distinct elements.",
        "Induction": "Mathematical induction proves statements for integers.",
        "Number Theory": "Number theory studies integers, divisibility and primes."
    },

    "Artificial Intelligence": {
        "AI": "Artificial intelligence builds systems that perform intelligent tasks.",
        "Search": "Search algorithms explore possible states to find solutions.",
        "Agents": "An intelligent agent perceives its environment and takes actions."
    },

    "Machine Learning": {
        "ML": "Machine learning learns patterns from data.",
        "Supervised Learning": "Learns from labeled examples.",
        "Unsupervised Learning": "Finds patterns in data without target labels.",
        "Evaluation": "Metrics help measure model performance."
    },

    "DevOps": {
        "Git": "Git tracks changes to files and supports collaboration.",
        "CI/CD": "CI/CD automates integration, testing and delivery workflows.",
        "Docker": "Docker packages applications and their dependencies into containers."
    },

    "GATE Preparation": {
        "Syllabus": "Use the official syllabus to organize your preparation.",
        "Revision": "Revise concepts and solve previous-year questions regularly.",
        "Mock Tests": "Mock tests help identify topics needing more practice."
    }
}

# ---------------- QUIZ QUESTIONS ----------------

quizzes = {
    "Python Programming": [
        {
            "question": "Which keyword defines a function in Python?",
            "options": ["func", "def", "function", "define"],
            "answer": 1,
            "topic": "Functions"
        },
        {
            "question": "Which data type stores True or False?",
            "options": ["int", "str", "bool", "list"],
            "answer": 2,
            "topic": "Data types"
        },
        {
            "question": "Which loop iterates over a sequence?",
            "options": ["for", "switch", "case", "select"],
            "answer": 0,
            "topic": "Loops"
        }
    ],

    "Programming Fundamentals": [
        {
            "question": "Which statement is used for a decision?",
            "options": ["if", "print", "input", "import"],
            "answer": 0,
            "topic": "Conditions"
        },
        {
            "question": "Which construct repeats instructions?",
            "options": ["Variable", "Loop", "Comment", "String"],
            "answer": 1,
            "topic": "Loops"
        },
        {
            "question": "What is a function mainly used for?",
            "options": [
                "Storing only numbers",
                "Repeating code manually",
                "Reusing a block of code",
                "Deleting a program"
            ],
            "answer": 2,
            "topic": "Functions"
        }
    ],

    "Data Structures": [
        {
            "question": "Which data structure follows LIFO?",
            "options": ["Queue", "Stack", "Array", "Graph"],
            "answer": 1,
            "topic": "Stacks"
        },
        {
            "question": "Which search works on a sorted array by halving the search range?",
            "options": ["Linear search", "Binary search", "Bubble sort", "DFS"],
            "answer": 1,
            "topic": "Searching"
        },
        {
            "question": "A node in a basic singly linked list contains data and what?",
            "options": ["A pointer", "A loop", "A class only", "A database"],
            "answer": 0,
            "topic": "Linked Lists"
        }
    ],

    "DBMS": [
        {
            "question": "What does DBMS stand for?",
            "options": [
                "Data Backup Management Software",
                "Database Management System",
                "Digital Base Memory System",
                "Database Machine Setup"
            ],
            "answer": 1,
            "topic": "Introduction to DBMS"
        },
        {
            "question": "Which key uniquely identifies a row?",
            "options": ["Foreign key", "Primary key", "Duplicate key", "Null key"],
            "answer": 1,
            "topic": "Keys"
        },
        {
            "question": "Which SQL command retrieves records?",
            "options": ["SELECT", "DELETE", "DROP", "UPDATE"],
            "answer": 0,
            "topic": "SQL"
        }
    ],

    "Java Programming": [
        {
            "question": "Which keyword creates an object?",
            "options": ["class", "new", "this", "void"],
            "answer": 1,
            "topic": "Objects"
        },
        {
            "question": "Which keyword is used for inheritance between classes?",
            "options": ["implements", "inherits", "extends", "superclass"],
            "answer": 2,
            "topic": "Inheritance"
        },
        {
            "question": "Which block handles an exception?",
            "options": ["try", "catch", "class", "package"],
            "answer": 1,
            "topic": "Exceptions"
        }
    ],

    "Mathematics": [
        {
            "question": "What is the value of 7 mod 3?",
            "options": ["0", "1", "2", "3"],
            "answer": 1,
            "topic": "Number Theory"
        },
        {
            "question": "Which is a prime number?",
            "options": ["9", "15", "17", "21"],
            "answer": 2,
            "topic": "Number Theory"
        },
        {
            "question": "What is the set containing no elements called?",
            "options": ["Universal set", "Empty set", "Infinite set", "Subset"],
            "answer": 1,
            "topic": "Sets"
        }
    ],

    "Artificial Intelligence": [
        {
            "question": "What does AI stand for?",
            "options": [
                "Automated Internet",
                "Artificial Intelligence",
                "Advanced Information",
                "Applied Interface"
            ],
            "answer": 1,
            "topic": "AI"
        },
        {
            "question": "Which is a common AI search algorithm?",
            "options": ["Breadth-first search", "Bubble sort", "Insertion sort", "Merge only"],
            "answer": 0,
            "topic": "Search"
        },
        {
            "question": "An intelligent agent interacts with what?",
            "options": ["Its environment", "Only a keyboard", "Only a database", "A compiler only"],
            "answer": 0,
            "topic": "Agents"
        }
    ],

    "Machine Learning": [
        {
            "question": "What does machine learning primarily do?",
            "options": [
                "Learns patterns from data",
                "Repairs hardware",
                "Creates electricity",
                "Only stores files"
            ],
            "answer": 0,
            "topic": "ML"
        },
        {
            "question": "Which is a supervised learning task?",
            "options": [
                "Clustering unlabeled data",
                "Classification using labeled data",
                "Random file sorting",
                "Deleting duplicate files"
            ],
            "answer": 1,
            "topic": "Supervised Learning"
        },
        {
            "question": "Why evaluate a trained model?",
            "options": [
                "To measure performance",
                "To rename the computer",
                "To increase file size",
                "To remove the dataset"
            ],
            "answer": 0,
            "topic": "Evaluation"
        }
    ],

    "DevOps": [
        {
            "question": "What is Git mainly used for?",
            "options": ["Version control", "Image editing", "Video calls", "Database queries"],
            "answer": 0,
            "topic": "Git"
        },
        {
            "question": "What does CI/CD help automate?",
            "options": ["Software delivery workflows", "Typing", "Computer cleaning", "Screen brightness"],
            "answer": 0,
            "topic": "CI/CD"
        },
        {
            "question": "What is Docker commonly used for?",
            "options": ["Containers", "Spreadsheets", "Slide design", "Photo editing"],
            "answer": 0,
            "topic": "Docker"
        }
    ],

    "GATE Preparation": [
        {
            "question": "What should you consult first to plan GATE study?",
            "options": ["Official syllabus", "Random videos only", "Only social media", "No study material"],
            "answer": 0,
            "topic": "Syllabus"
        },
        {
            "question": "What helps identify weak topics?",
            "options": ["Mock tests", "Avoiding questions", "Skipping revision", "Only rereading titles"],
            "answer": 0,
            "topic": "Mock Tests"
        },
        {
            "question": "What is useful for understanding question patterns?",
            "options": ["Previous-year questions", "Ignoring the syllabus", "Guessing only", "Skipping practice"],
            "answer": 0,
            "topic": "Revision"
        }
    ]
}

# ---------------- PROGRESS STORAGE ----------------

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
        st.warning(
            "Progress could not be saved permanently in this environment."
        )


if "progress" not in st.session_state:
    st.session_state.progress = load_progress()

if "quiz_answers" not in st.session_state:
    st.session_state.quiz_answers = {}

if "quiz_submitted" not in st.session_state:
    st.session_state.quiz_submitted = False

# ---------------- SIDEBAR: PROFILE ----------------

st.sidebar.header("👤 Your Learning Profile")

age = st.sidebar.number_input(
    "Age",
    min_value=10,
    max_value=100,
    value=20
)

python_level = st.sidebar.selectbox(
    "Current programming level",
    ["Beginner", "Intermediate", "Advanced"]
)

goal = st.sidebar.selectbox(
    "Main learning goal",
    [
        "College exams",
        "GATE preparation",
        "Build projects",
        "Improve programming skills",
        "Career preparation"
    ]
)

quiz_score = st.sidebar.slider(
    "Current quiz score (%)",
    min_value=0,
    max_value=100,
    value=50
)

study_minutes = st.sidebar.slider(
    "Daily study time (minutes)",
    min_value=10,
    max_value=300,
    value=60,
    step=10
)

# ---------------- CATEGORY MAPPING ----------------

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

# ---------------- ML RECOMMENDATION ----------------

st.header("🤖 2. Your ML Recommendation")

recommended_category = None
model_error = None

if os.path.exists(MODEL_FILE):
    try:
        saved_data = joblib.load(MODEL_FILE)

        # FIX: The saved file is a dictionary, not the model itself.
        model = (
            saved_data["model"]
            if isinstance(saved_data, dict)
            else saved_data
        )

        if isinstance(saved_data, dict):
            feature_names = saved_data.get(
                "features",
                ["python_level", "quiz_score", "study_minutes", "goal"]
            )
        else:
            feature_names = [
                "python_level",
                "quiz_score",
                "study_minutes",
                "goal"
            ]

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

        # Ensure the input columns match the model's training order.
        student_data = student_data[feature_names]

        recommended_category = model.predict(student_data)[0]

        st.success(
            f"Recommended category: {recommended_category}"
        )

    except Exception as error:
        model_error = str(error)
        st.warning(
            "The ML recommendation could not be generated. "
            "Check the saved model and training features."
        )
        st.caption(f"Technical detail: {model_error}")

else:
    st.warning(
        "The trained model file was not found. "
        "Run train_model.py to create it."
    )

# ---------------- CHOOSE LEARNING PATH ----------------

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

if recommended_category in category_to_subject:
    default_subject = category_to_subject[recommended_category]
else:
    default_subject = "Python Programming"

st.header("📚 3. Your Learning Roadmap")

subjects = list(roadmaps.keys())

default_index = (
    subjects.index(default_subject)
    if default_subject in subjects
    else 0
)

selected_subject = st.selectbox(
    "Choose or change your learning path",
    subjects,
    index=default_index,
    key="selected_subject"
)

st.write(f"**Your selected learning path:** {selected_subject}")

st.caption(
    "The ML recommendation suggests a starting category. "
    "You can change your learning path whenever you want."
)

# ---------------- ROADMAP ----------------

st.subheader(f"🗺️ Roadmap: {selected_subject}")

for index, topic in enumerate(roadmaps[selected_subject], start=1):
    progress_key = f"{selected_subject}::{topic}"

    completed = st.checkbox(
        f"Step {index}: {topic}",
        value=bool(st.session_state.progress.get(progress_key, False)),
        key=f"roadmap_{selected_subject}_{index}"
    )

    if completed:
        st.session_state.progress[progress_key] = True
    else:
        st.session_state.progress.pop(progress_key, None)

save_progress(st.session_state.progress)

total_steps = len(roadmaps[selected_subject])
completed_steps = sum(
    1
    for topic in roadmaps[selected_subject]
    if st.session_state.progress.get(
        f"{selected_subject}::{topic}",
        False
    )
)

st.progress(
    completed_steps / total_steps if total_steps else 0
)

st.write(f"**Roadmap progress:** {completed_steps}/{total_steps} steps completed")

# ---------------- STUDY NOTES ----------------

st.header("📝 4. Study Notes")

subject_notes = notes.get(selected_subject, {})

if subject_notes:
    for topic, explanation in subject_notes.items():
        with st.expander(topic):
            st.write(explanation)
else:
    st.info("Study notes are not available for this subject yet.")

# ---------------- VIDEO SEARCH ----------------

st.header("🎥 5. Find Learning Videos")

video_topic = st.selectbox(
    "Select a topic for video lessons",
    roadmaps[selected_subject],
    key="video_topic"
)

video_query = (
    video_topic.replace(" ", "+")
    + "+"
    + selected_subject.replace(" ", "+")
)

video_url = (
    "https://www.youtube.com/results?search_query="
    + video_query
)

st.link_button(
    "▶️ Search YouTube lessons",
    video_url
)

# ---------------- QUIZ ----------------

st.header("🧠 6. Test Your Knowledge")

subject_quiz = quizzes.get(selected_subject, [])

if not subject_quiz:
    st.info("No quiz is available for this subject yet.")
else:
    with st.form(key=f"quiz_form_{selected_subject}"):
        current_answers = {}

        for index, question in enumerate(subject_quiz):
            st.markdown(
                f"**Question {index + 1}: {question['question']}**"
            )

            current_answers[index] = st.radio(
                "Choose an answer:",
                question["options"],
                index=None,
                key=f"answer_{selected_subject}_{index}"
            )

        submitted = st.form_submit_button("Submit Quiz")

    if submitted:
        st.session_state.quiz_answers[selected_subject] = {
            index: answer
            for index, answer in current_answers.items()
        }
        st.session_state.quiz_submitted = True

    if (
        st.session_state.quiz_submitted
        and selected_subject in st.session_state.quiz_answers
    ):
        answers = st.session_state.quiz_answers[selected_subject]

        correct_count = 0
        missed_topics = []

        for index, question in enumerate(subject_quiz):
            selected_answer = answers.get(index)
            correct_answer = question["options"][question["answer"]]

            if selected_answer == correct_answer:
                correct_count += 1
            else:
                missed_topics.append(question["topic"])

        score_percent = round(
            correct_count / len(subject_quiz) * 100
        )

        st.subheader("📊 Your Quiz Results")

        st.metric(
            "Score",
            f"{correct_count}/{len(subject_quiz)}"
        )

        st.progress(score_percent / 100)

        st.write(f"**Percentage:** {score_percent}%")

        if score_percent == 100:
            st.success("Excellent! You answered every question correctly.")
        elif score_percent >= 50:
            st.info("Good effort! Review the missed topics and try again.")
        else:
            st.info("Keep learning! Read the notes and retry the quiz.")

        if missed_topics:
            st.subheader("📌 Topics to Revise")

            for topic in sorted(set(missed_topics)):
                st.write(f"- {topic}")

        else:
            st.success("No missed topics. Great work!")

        if st.button("Try Quiz Again", key=f"retry_{selected_subject}"):
            st.session_state.quiz_submitted = False
            st.session_state.quiz_answers.pop(selected_subject, None)

            for index in range(len(subject_quiz)):
                answer_key = f"answer_{selected_subject}_{index}"
                if answer_key in st.session_state:
                    del st.session_state[answer_key]

            st.rerun()

# ---------------- OVERALL PROGRESS ----------------

st.header("🏆 7. Your Learning Progress")

all_topics = [
    (subject, topic)
    for subject, topic_list in roadmaps.items()
    for topic in topic_list
]

total_all_steps = len(all_topics)

completed_all_steps = sum(
    1
    for subject, topic in all_topics
    if st.session_state.progress.get(
        f"{subject}::{topic}",
        False
    )
)

st.metric(
    "Completed roadmap steps",
    f"{completed_all_steps}/{total_all_steps}"
)

st.progress(
    completed_all_steps / total_all_steps
    if total_all_steps
    else 0
)

st.caption(
    "Keep learning one step at a time. "
    "Your progress file is stored locally when the environment allows it."
)

st.divider()

st.write("💡 **LearnPath AI:** Learn at your own pace, one topic at a time.")

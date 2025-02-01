from flask import Flask, render_template, request, redirect, url_for, session
import json
import random

app = Flask(__name__)
app.secret_key = "your_secret_key"

# Path to the JSON file
json_file_path = r"D:\Nandini\projects\Online_Quiz_Platform\questions.json"

# Load questions from the JSON file
try:
    with open(json_file_path, "r") as file:
        questions_data = json.load(file)
except Exception as e:
    print(f"Error loading JSON file: {e}")
    exit(1)

# Initialize the leaderboard as an empty list
leaderboard = []

@app.route("/")
def index():
    session.clear()  # Clear session data when starting a new quiz
    return render_template("index.html", languages=questions_data.keys())

@app.route("/quiz/<language>", methods=["GET", "POST"])
def quiz(language):
    if "questions" not in session:
        # Randomly select 10 questions from the list
        session["questions"] = random.sample(questions_data[language], 10)
        session["score"] = 0
        session["current_question"] = 0
        session["language"] = language  # Store the selected language in the session

    if request.method == "POST":
        # Check if the user submitted an answer
        user_answer = request.form.get("answer")
        correct_answer = session["questions"][session["current_question"]]["answer"]
        if user_answer == correct_answer:
            session["score"] += 1

        # Move to the next question
        session["current_question"] += 1

        # If all questions are answered, redirect to the result page
        if session["current_question"] >= len(session["questions"]):
            return redirect(url_for("result"))

    # Get the current question and shuffle the options
    current_question = session["questions"][session["current_question"]]
    random.shuffle(current_question["options"])  # Shuffle options
    return render_template("quiz.html", language=language, question=current_question)

@app.route("/result")
def result():
    score = session.get("score", 0)
    total_questions = len(session.get("questions", []))
    language = session.get("language", "Unknown")

    # Add the current score to the leaderboard
    leaderboard.append({
        "language": language,
        "score": score,
        "total_questions": total_questions
    })

    # Sort the leaderboard by score (descending order)
    leaderboard.sort(key=lambda x: x["score"], reverse=True)

    return render_template("result.html", score=score, total_questions=total_questions, leaderboard=leaderboard)

if __name__ == "__main__":
    app.run(debug=True)
from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey


app = Flask(__name__)
app.config['SECRET_KEY'] = "secret"


debug = DebugToolbarExtension(app)


@app.route("/")
def show_survey_start():
    """Select a survey."""

    return render_template("survey_start.html", survey=survey)


@app.route("/begin", methods=["POST"])
def start_survey():

    session["responses"] = []

    return redirect("/questions/0")



@app.route("/questions/<int:qid>")
def show_question(qid):
    """Display current question."""
    responses = session.get("responses")
    
    if (responses is None):
        return redirect("/")

    if (len(responses) == len(survey.questions)):
        return redirect("/completion")

    if (len(responses) != qid):
        #Out of order question
        flash("Invalid question")
        return redirect(f"/questions/{len(responses)}")

    question = survey.questions[qid]

    return render_template(
        "question.html", question_num=qid, question=question)


@app.route("/answer", methods=["POST"])
def handle_question():
    """Save response and redirect to next question."""

# get the response choice
    choice = request.form['answer']

    # add this response to the session
    responses = session["responses"]
    responses.append(choice)
    session["responses"] = responses

    if (len(responses) == len(survey.questions)):
        return redirect("/completion")

    else:
        return redirect(f"/questions/{len(responses)}")

@app.route("/completion")
def complete():
    """Survey complete. Show completion page."""

    return render_template("completion.html")
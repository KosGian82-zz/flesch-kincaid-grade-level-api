from flask import Flask
from flask import render_template
from flask import request
from readability import Readability
from wtforms import Form
from wtforms import TextAreaField
from wtforms import validators


# Initialise a Flask instance
app = Flask(__name__)


# Create a TextReadabilityForm class to be rendered in text_readability.html
class TextReadabilityForm(Form):
    # TextAreaField checks whether the user entered any text or not
    # (Input must be at least 100 characters long, e.g. 100 one-letter words)
    textreadability = TextAreaField('',
                                    [validators.DataRequired(),
                                    validators.length(min=100)])


# Method that returns the F-K grade level, or ERROR message if text is < 100 words long
def get_fk_grade_level(text):
    # The text must contain at least 100 words
    if len(text.split()) < 100:
        result =  "ERROR: This piece of text is too short to get a Flesch Kincaid grade level."
    else:
        # Instantiate a Readability object
        r = Readability(text)
        # Get the F-K score metric
        fk = r.flesch_kincaid()
        # Get the F-K grade level
        result = fk.grade_level
    return result


# API's endpoint (URL)
@app.route('/')
def index():
    form = TextReadabilityForm(request.form)
    # Render text_readability.html file
    return render_template('text_readability.html', form=form)


# POST method for the API to enable requests to create new sources (F-K grade levels)
@app.route('/results', methods=['POST'])
def results():
    form = TextReadabilityForm(request.form)
    if request.method == 'POST' and form.validate():
        # Get user-defined text
        text = request.form['textreadability']
        # Get result (F-K grade level of error message)
        result = get_fk_grade_level(text)
        # Render input text and F-K grade level (or error) into a results.html page
        return render_template('results.html', content=text, result=result)
    return render_template('text_readability.html', form=form)


if __name__ == '__main__':
    app.run()

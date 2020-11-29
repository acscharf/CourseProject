from flask import Flask, request

import spacy

app = Flask(__name__)

@app.route('/')
def home():
    return """
        <html><body>
            <h2>Reflection analyzer</h2>
            <form action="/result">
                <p>
                Enter your reflection:<br>
                <textarea name='reflection' rows='10' cols='30'></textarea>
                </p>
                <!--
                <p>
                <input type='radio' name='language' value='ja'>
                <label for='ja'>日本語</label><br>
                <input type='radio' id='en' name='language' value='en'>
                <label for='en'>English</label><br>
                </p>
                -->
                <input type='submit' value='Submit'>
            </form>
        </body></html>
        """

@app.route('/result')
def result():
    reflection = request.args['reflection']
    #language = request.args['language']
    nlp = spacy.load("textdata")
    doc = nlp(reflection)

    if doc.cats["USEFUL"] > doc.cats["NOT USEFUL"]:
        msg = 'Your reflection was great!'
    else:
        msg = 'Hmm, try again?'

    return """
        <html><body>
            <h2>{0}</h2>
            <p><a href="/">Try again?</a><p>
        </body></html>
        """.format(msg)

if __name__ == "__main__":
    plac.call(main)

app.run(host="localhost", debug=True)
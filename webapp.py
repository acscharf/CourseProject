from flask import Flask, request
import plac
import spacy

app = Flask(__name__)

@app.route('/')
def home():
    return """
        <html>
        <head>
        <script src='https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js'></script>
        <script>
        $(document).ready(function(){
             $('#useful').click(function(){
                $('#reflection_area').val('Our company has products at each stage of the product lifecycle. As a manager, I will assign the right employees who can make the product succeed at each stage.');
            });
            $('#not_useful').click(function(){
                $('#reflection_area').val('Product lifecyle was interesting, I am looking forward to using it.');
            });
        });
       </script>
       </head>
        <body>
            <h1>Reflection analyzer</h2>
            
                <h2>Sample video: Product Lifecycle</h2>
                <p>
                <iframe src='https://player.vimeo.com/video/371068936' width='640' height='360' frameborder='0' allowfullscreen=''></iframe>
                </p>
                <p>
                <h2>Write Your Reflection</h2>
                <p>
                How can you apply the learning from this course to your job or daily life?
                </p>
                <p>

                <form action='/result'>
                <textarea id='reflection_area' name='reflection' rows='10' cols='40' placeholder='For example, reflect on any tasks or processes that might benefit from the knowledge you gained in this course.'></textarea>
                </p>

                <input type='submit' value='Submit'>

                              

            </form>
            <h3>Just want to give it a try?</h3>
            <p>
              <button id='useful'>Load Sample Useful Reflection</button>
              </p>
              <p>
              <button id='not_useful'>Load Sample Not Useful Reflection</button>
            </p>
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
        percent = doc.cats["USEFUL"] - doc.cats["NOT USEFUL"]
    else:
        msg = 'Your reflection could be improved.'
        percent = doc.cats["NOT USEFUL"] - doc.cats["USEFUL"]

    return """
        <html><body>
            <h2>{0}</h2>
            <p>(We're {1:.0%} percent sure of that)</p>
            <p>Useful reflections usually have the following:
            <li>Around 20 words</li>
            <li>Correct punctuation and capitalization</li>
            <li>Words like "apply" and "use" rather than "understand"
            </p>
            <p><a href="/">Enter another reflection?</a><p>
        </body></html>
        """.format(msg, percent)

if __name__ == "__main__":
    plac.call(main)

app.run(host="localhost", debug=True)

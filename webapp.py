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
    nlp = spacy.load("english_model")
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


@app.route('/ja')
def home_ja():
    return """
        <html>
        <head>
        <script src='https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js'></script>
        <script>
        $(document).ready(function(){
            $('#useful').click(function(){
                $('#reflection_area').val('企業が無駄な資産を抱え込まず効率的に売り上げ等を実現しているかを見る分析であることを学びました。ここで得た学びは、会計・財務システムの保守業務、顧客担当者とのコミュニケーションに活用します。');
            });
            $('#not_useful').click(function(){
                $('#reflection_area').val('理解しやすい内容でした。実践の場でも活用したい。');
            });
        });
       </script>
       </head>
        <body>
            <h1>振り返りアドバイザー</h2>
            
                <h2>サンプル動画：効率性分析</h2>
                <p>
                <a href='https://hodai.globis.co.jp/courses/71893843'>こちらからご覧ください</a>
                </p>
                <p>
                <h2>学んだ内容は業務や日常においてどう活用できそうですか？</h2>
                <p>
                具体的なシーンをイメージしながら書いてみましょう。
                </p>
                <p>

                <form action='/result_ja'>
                <textarea id='reflection_area' name='reflection' rows='10' cols='40' placeholder='例：業務で活用するためには、◯◯◯が大事だと感じます/◯◯◯なシーンにおいて、活用できるものだと思います'></textarea>
                </p>

                <input type='submit' value='Submit'>

                              

            </form>
            <h3>サンプルでやってみる？</h3>
            <p>
              <button id='useful'>役立ち振り返り</button>
              </p>
              <p>
              <button id='not_useful'>役に立たない振り返り</button>
            </p>
        </body></html>
        """

@app.route('/result_ja')
def result_ja():
    reflection = request.args['reflection']
    #language = request.args['language']
    nlp = spacy.load("japanese_model")
    doc = nlp(reflection)

    if doc.cats["USEFUL"] > doc.cats["NOT USEFUL"]:
        msg = '振り返りはとってもよかった！'
        percent = doc.cats["USEFUL"] - doc.cats["NOT USEFUL"]
    else:
        msg = '振り返りは改善の余地がある。'
        percent = doc.cats["NOT USEFUL"] - doc.cats["USEFUL"]

    return """
        <html><body>
            <h2>{0}</h2>
            <p>（自信度： {1:.0%}）</p>
            </p>
            <p><a href="/ja">もう一度振り返りを書いてみますか？</a><p>
        </body></html>
        """.format(msg, percent)

if __name__ == "__main__":
    plac.call(main)

app.run(host="localhost", debug=True)

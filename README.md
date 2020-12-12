# English and Japanese Course Reflection Analysis and Prediction

## About

After learners complete a video-based online business course, they are prompted to enter a "reflection" on how they can apply the knowledge from the course to their job or daily life. These reflections are shared with other learners so they can deepen their understanding, learning how others applied their learning.

This project aims to:
1.) to analyze "useful" and "not useful" reflections, finding syntactic elements that make up each
2.) gather user input for a user reflection and predict whether that reflection is "useful" or "not useful"

## Try It

A live version of the software is hosted below, complete with sample videos. Try a "useful" and "not useful" reflection and see if it matches your expectations. The sample reflections will give you an idea of what might be considered "useful" and "not useful."

### English
http://alexscharf.com/

### Japanese
http://alexscharf.com/ja

## train.py (Training Application)

### Overview
Reads labeled CSV for reflection data, analyzes reflections, trains a model, and saves that model to disk. Analysis looks at parts of speech (by percentage), common words, and average word counts for both "useful" and "not useful" reflections. 

### Implementation
The application has three key functions, explained below:
#### read_csv(filename, rows)
Opens a csv with the name of "filename" and reads the first number rows specified by "rows." The CSV should have two columns, the first with a label of '1' if the reflection is 'useful' or '0' if it is "not useful." Strips whitespace and returns a pandas DataFrame.

#### analyze_reflections(reflections, nlp, language)
Analyze reflections when provided with a pandas DataFrame, spaCy NLP object, a string to display for output. Iterates over each unigram for both useful and not useful reflections, counting parts of speech, common words, and average length while ignoring whitespace. Outputs the result using the print function.

Example output: 
#######################
English analysis
#######################

-----------------------
PARTS OF SPEECH
-----------------------

Useful:
INTJ 0.05%
PUNCT 7.52%
PRON 6.81%
AUX 3.22%
ADV 5.41%
ADJ 6.65%
CCONJ 3.46%
VERB 17.60%
ADP 9.22%
DET 11.59%
NOUN 20.87%
SCONJ 1.17%
PART 4.39%
PROPN 1.22%
NUM 0.09%
X 0.05%
SPACE 0.56%
SYM 0.11%

Not useful:
DET 3.30%
NOUN 7.01%
ADP 3.17%
PROPN 1.01%
AUX 1.24%
ADJ 3.10%
PUNCT 2.66%
CCONJ 0.86%
VERB 6.45%
ADV 1.74%
SCONJ 0.25%
PART 1.70%
PRON 2.61%
NUM 0.06%
X 0.05%
SPACE 0.18%
INTJ 0.09%
SYM 0.01%

-----------------------
COMMON WORDS
-----------------------

Useful:
[('structure', 82), ('pyramid', 72), ('use', 66), ('help', 54), ('apply', 52), ('thinking', 50), ('business', 41), ('course', 38), ('conclusion', 34), ('issue', 31)]

Not useful
[('use', 40), ('structure', 29), ('thinking', 26), ('daily', 20), ('apply', 20), ('work', 19), ('Pyramid', 17), ('pyramid', 16), ('business', 15), ('life', 15)]

-----------------------
AVERAGE LENGTH
-----------------------

Useful:
22.78342245989305

Not useful:
9.301538461538462


### data/english.csv
### data/japanese.csv
Labeled reflection data (700 entries labeled in English, 500 in Japanese)

### webapp.py
Flask-based web application that loads training model and gathers uset input to predict usefulness of reflection.

### waitress_server.py 
Waitress server to run the web app

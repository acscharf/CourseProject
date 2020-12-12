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

Example output: https://github.com/acscharf/CourseProject/blob/main/example_output.txt

#### train_reflections(reflections, nlp, n_iter, n_texts):
Trains model based upon label reflections data with a pandas DataFrame, spaCy NLP object, and the number of iterations and items in the reflection data. Holds 20% of the labeled data for evaluation, training off of the remaining 80%. Prints loss, recall, precision, and f-score for each training iteration. Currently build using the "simple_cnn" architecture provided by spaCy.

### Usage
The application requires the spaCy and pandas libaries as well as the "en_core_web_sm" and "ja_core_news_sm" spacy models. Additionally, the software needs the english.csv and japanese.csv labeled reflection datasets in a "data" subfolder. Examples can be found in this repository:

English: https://github.com/acscharf/CourseProject/blob/main/data/english.csv
Japanese: https://github.com/acscharf/CourseProject/blob/main/data/japanese.csv

After completion, the program saves a model to disk in the "english_model" and "japanese_model" subfolders.

## webapp.py (Training Application)

### Overview
Flask-based web application that loads training model and gathers uset input to predict usefulness of reflection. 


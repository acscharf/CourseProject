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



## Files

### Readme
This document

### Proposal.pdf
Project proposal

### Progress report.pdf
Mid-term progress report

### train.py

#### Overview
Reads labeled CSV for reflection data, analyzes reflections, trains a model, and saves that model to disk. Analysis looks at parts of speech (by percentage), common words, and average word counts for both "useful" and "not useful" reflections.



### data/english.csv
### data/japanese.csv
Labeled reflection data (700 entries labeled in English, 500 in Japanese)

### webapp.py
Flask-based web application that loads training model and gathers uset input to predict usefulness of reflection.

### waitress_server.py 
Waitress server to run the web app

import pandas as pd
import spacy
from collections import Counter
import random
import plac
from spacy.util import minibatch, compounding


def main():

    english_nlp = spacy.load("en_core_web_sm")
    japanese_nlp = spacy.load("ja_core_news_sm")

    english_reflections = read_csv("data/english.csv", 700)
    japanese_reflections = read_csv("data/japanese.csv", 500)

    analyze_reflections(english_reflections, english_nlp, "English")
    analyze_reflections(japanese_reflections, japanese_nlp, "Japanese")

    english_optimizer = train_reflections(english_reflections, english_nlp, 25, 700)
    japanese_optimizer = train_reflections(japanese_reflections, japanese_nlp, 25, 500)

    print("Not useful:")
    test_text="Video was good"
    doc=english_nlp(test_text)
    print(doc.cats)

    print("Useful:")
    test_text="I can take the learning from MECE and apply it to my current job by checking the sales charts."
    doc=english_nlp(test_text)
    print(doc.cats)

    with english_nlp.use_params(english_optimizer.averages):
        english_nlp.to_disk("english_model")
        print("Saved model")

    with japanese_nlp.use_params(japanese_optimizer.averages):
        japanese_nlp.to_disk("japanese_model")
        print("Saved model")

def train_reflections(reflections, nlp, n_iter, n_texts):
    textcat = nlp.create_pipe("textcat", config={"exclusive_classes": True, "architecture": "simple_cnn"})

    nlp.add_pipe(textcat, last=True)

    textcat.add_label("USEFUL")
    textcat.add_label("NOT USEFUL")

    reflections['tuples'] = reflections.apply(lambda row: (row['comment'], row['useful']), axis=1)

    train = reflections['tuples'].tolist()

    (train_texts, train_cats), (dev_texts, dev_cats) = load_data(train=train, limit=n_texts)
    train_texts = train_texts[:n_texts]
    train_cats = train_cats[:n_texts]
    print(
        "Using {} examples ({} training, {} evaluation)".format(
            n_texts, len(train_texts), len(dev_texts)
        )
    )

    train_data = list(zip(train_texts,[{'cats': cats} for cats in train_cats]))

    #training code taken from from https://github.com/explosion/spaCy/blob/master/examples/training/train_textcat.py
    pipe_exceptions = ["textcat", "trf_wordpiecer", "trf_tok2vec"]
    other_pipes = [pipe for pipe in nlp.pipe_names if pipe not in pipe_exceptions]
    with nlp.disable_pipes(*other_pipes):  # only train textcat
        optimizer = nlp.begin_training()
      
        print("Training the model...")
        print("{:^5}\t{:^5}\t{:^5}\t{:^5}".format("LOSS", "P", "R", "F"))

        batch_sizes = compounding(4.0, 32.0, 1.001)

        for i in range(n_iter):
            losses = {}

            random.shuffle(train_data)
            batches = minibatch(train_data, size=batch_sizes)

            for batch in batches:
                texts, annotations = zip(*batch)
                nlp.update(texts, annotations, sgd=optimizer, drop=0.2, losses=losses)
            
            with textcat.model.use_params(optimizer.averages):
                # evaluate on the dev data split off in load_data()
                scores = evaluate(nlp.tokenizer, textcat, dev_texts, dev_cats)
            print(
                "{0:.3f}\t{1:.3f}\t{2:.3f}\t{3:.3f}".format(  # print a simple table
                    losses["textcat"],
                    scores["textcat_p"],
                    scores["textcat_r"],
                    scores["textcat_f"],
                )
            )

    return optimizer
    

def read_csv(filename, rows):
    rows += 1
    reflections = pd.read_csv(filename, nrows=rows)
    reflections = reflections[['useful','comment']].dropna()
    reflections = reflections.replace('\n',' ', regex=True) 
    return reflections

def analyze_reflections(reflections, nlp, language):
    useful_len = 0
    useful_docs = 0
    useful_pos_c = Counter()
    useful_word_c = Counter()

    not_useful_len = 0
    not_useful_docs = 0
    not_useful_pos_c = Counter()
    not_useful_word_c = Counter()

    for index, row in reflections.iterrows():
        if reflections.at[index, 'useful'] == 0:
            not_useful_docs += 1
            doc = nlp(reflections.at[index, 'comment'])
            not_useful_len += len(doc)
            not_useful_pos_c += Counter(([token.pos_ for token in doc]))
            not_useful_word_c += Counter(([token.text for token in doc if token.is_stop != True and token.is_punct != True and token.text != ' ']))
        elif reflections.at[index, 'useful'] == 1:
            useful_docs += 1
            doc = nlp(reflections.at[index, 'comment'])
            useful_len += len(doc)
            useful_pos_c += Counter(([token.pos_ for token in doc]))
            useful_word_c += Counter(([token.text for token in doc if token.is_stop != True and token.is_punct != True and token.text != ' ']))

    sbase = sum(useful_pos_c.values())

    print("\n#######################")
    print(language + " analysis")
    print("#######################")


    print("\n-----------------------")
    print("PARTS OF SPEECH")
    print("-----------------------")
    print("\nUseful:")
    for label, cnt in useful_pos_c.items():
        print(label, '{0:2.2f}%'.format((100.0* cnt)/sbase))
    

    print("\nNot useful:")
    for label, cnt in not_useful_pos_c.items():
        print(label, '{0:2.2f}%'.format((100.0* cnt)/sbase))

    print("\n-----------------------")
    print("COMMON WORDS")
    print("-----------------------")
    print("\nUseful:")
    print(useful_word_c.most_common(10))

    print("\nNot useful")
    print(not_useful_word_c.most_common(10))

    print("\n-----------------------")
    print("AVERAGE LENGTH")
    print("-----------------------")
    print("\nUseful:")
    print(useful_len / useful_docs)

    print("\nNot useful:")
    print(not_useful_len / not_useful_docs)


def load_data(train, limit=0, split=0.8):
    train_data = train
    random.shuffle(train_data)
    texts, labels = zip(*train_data)
    cats = [{"USEFUL": bool(y), "NOT USEFUL": not bool(y)} for y in labels]
    split = int(len(train_data) * split)
    return (texts[:split], cats[:split]), (texts[split:], cats[split:])

#evalate taken from https://github.com/explosion/spaCy/blob/master/examples/training/train_textcat.py
def evaluate(tokenizer, textcat, texts, cats):
    docs = (tokenizer(text) for text in texts)
    tp = 0.0  # True positives
    fp = 1e-8  # False positives
    fn = 1e-8  # False negatives
    tn = 0.0  # True negatives
    for i, doc in enumerate(textcat.pipe(docs)):
        gold = cats[i]
        for label, score in doc.cats.items():
            if label not in gold:
                continue
            if label == "NOT USEFUL":
                continue
            if score >= 0.5 and gold[label] >= 0.5:
                tp += 1.0
            elif score >= 0.5 and gold[label] < 0.5:
                fp += 1.0
            elif score < 0.5 and gold[label] < 0.5:
                tn += 1
            elif score < 0.5 and gold[label] >= 0.5:
                fn += 1
    precision = tp / (tp + fp)
    recall = tp / (tp + fn)
    if (precision + recall) == 0:
        f_score = 0.0
    else:
        f_score = 2 * (precision * recall) / (precision + recall)
    return {"textcat_p": precision, "textcat_r": recall, "textcat_f": f_score}

if __name__ == "__main__":
    plac.call(main)
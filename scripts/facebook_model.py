import numpy as np
import pandas as pd
import spacy
import statsmodels.api as sm
from matplotlib import pyplot as plt

from patsy.highlevel import dmatrices
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from spacytextblob.spacytextblob import SpacyTextBlob


def get_reactions_prediction(text):
    best_post = get_best_post()
    df_for_text = get_mini_model_for_a_text_facebook(text, best_post)
    # print(df_for_text)

    df_facebook = pd.read_csv('data_facebook/facebook_data.csv')

    mask = np.random.rand(len(df_facebook)) < 0.85
    df_train = df_facebook[mask]
    df_test = df_facebook[~mask]
    # print('Training data set length='+str(len(df_train)))
    # print('Testing data set length='+str(len(df_test)))

    expr = """ALL_REACTIONS ~ POLARITY + SUBJECTIVITY + POSTS_LENGTH + SIMILARITY_TO_BEST + TWENTY_REACTS_BAYES + FIFTY_REACTS_BAYES + HUNDRED_REACTS_BAYES + TWO_HUNDRED_REACTS_BAYES"""

    y_train, X_train = dmatrices(expr, df_train, return_type='dataframe')
    y_test, X_test = dmatrices(expr, df_test, return_type='dataframe')
    # print(X_test)

    poisson_training_results = sm.GLM(y_train, X_train, family=sm.families.Poisson()).fit()

    poisson_predictions = poisson_training_results.get_prediction(df_for_text)
    #summary_frame() returns a pandas DataFrame
    predictions_summary_frame = poisson_predictions.summary_frame()
    #print(predictions_summary_frame)
    predicted_counts = predictions_summary_frame['mean']

    return int(predicted_counts[0])


def get_mini_model_for_a_text_facebook(text, best_post):
    nlp = spacy.load("pl_core_news_lg")
    nlp.add_pipe('spacytextblob')

    doc = nlp(text)
    best_post_doc = nlp(best_post)

    polarity = doc._.polarity
    subjectivity = doc._.subjectivity
    length = len(doc)
    similarity_to_best = doc.similarity(best_post_doc)
    more_than_20_reactions = get_bayes_index_for_n_reactions(text, 20)
    more_than_50_reactions = get_bayes_index_for_n_reactions(text, 50)
    more_than_100_reactions = get_bayes_index_for_n_reactions(text, 100)
    more_than_200_reactions = get_bayes_index_for_n_reactions(text, 200)

    data_dict = {
        'Intercept': [1.0],
        'POLARITY': [polarity],
        'SUBJECTIVITY': [subjectivity],
        'POSTS_LENGTH': [length],
        'SIMILARITY_TO_BEST': [similarity_to_best],
        'TWENTY_REACTS_BAYES': [more_than_20_reactions],
        'FIFTY_REACTS_BAYES': [more_than_50_reactions],
        'HUNDRED_REACTS_BAYES': [more_than_100_reactions],
        'TWO_HUNDRED_REACTS_BAYES': [more_than_200_reactions]
    }

    df = pd.DataFrame(data_dict)
    return df


def get_bayes_index_for_n_reactions(text, n_reactions):
    vec = CountVectorizer()
    df_facebook = pd.read_csv('facebook_data.csv')
    list_preprocessed_posts = df_facebook['PREPROCESSED_POSTS']
    list_all_reactions = df_facebook['ALL_REACTIONS']

    list_more_than_n_reacts = []
    for reacts in list_all_reactions:
        if reacts > n_reactions:
            list_more_than_n_reacts.append(1)
        else:
            list_more_than_n_reacts.append(0)

    x = list_preprocessed_posts
    y = list_more_than_n_reacts

    x, x_test, y, y_test = train_test_split(x, y, stratify=y, test_size=0.25, random_state=42)

    x = vec.fit_transform(x).toarray()
    x_test = vec.transform(x_test).toarray()

    model = MultinomialNB()
    model.fit(x, y)

    text_list = [text]

    prediction = model.predict(vec.transform(text_list))

    return prediction[0]


def get_best_post():
    df_facebook = pd.read_csv('data_facebook/facebook_data.csv')
    list_all_reactions = df_facebook['ALL_REACTIONS']
    list_posts = df_facebook['POSTS']

    max_reactions = 0
    best_index = 0
    for i in range(len(list_all_reactions)):
        if list_all_reactions[i] > max_reactions:
            max_reactions = list_all_reactions[i]
            best_index = i

    return list_posts[best_index]






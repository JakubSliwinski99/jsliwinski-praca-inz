import spacy
import pandas as pd
import numpy as np
import statsmodels.api as sm

from patsy.highlevel import dmatrices
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB


def get_index_prediction(text):
    best_post = get_best_post()
    df_for_text = get_mini_model_for_a_text_linkedin(text, best_post)
    # print(df_for_text)

    df_linkedin = pd.read_csv('data_facebook/facebook_data.csv')

    mask = np.random.rand(len(df_linkedin)) < 0.8
    df_train = df_linkedin[mask]
    df_test = df_linkedin[~mask]
    # print('Training data set length='+str(len(df_train)))
    # print('Testing data set length='+str(len(df_test)))

    expr = """INDEX ~ POLARITY + SUBJECTIVITY + POST_LENGTH + NUMBER_OF_ENTS + SIMILARITY_TO_BEST + INDEX_HIGHER_THAN_HALF_BAYES + INDEX_HIGHER_THAN_ONE_BAYES + INDEX_HIGHER_THAN_THREE_BAYES"""


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


def get_mini_model_for_a_text_linkedin(text, best_post):
    nlp = spacy.load("pl_core_news_lg")
    nlp.add_pipe('spacytextblob')

    doc = nlp(text)
    best_post_doc = nlp(best_post)

    polarity = doc._.polarity
    subjectivity = doc._.subjectivity
    length = len(doc)
    number_of_ents = len(doc.ents)
    similarity_to_best = doc.similarity(best_post_doc)
    index_higher_than_05 = get_bayes_index_for_x_index(text, 0.5)
    index_higher_than_1 = get_bayes_index_for_x_index(text, 1)
    index_higher_than_2 = get_bayes_index_for_x_index(text, 2)

    data_dict = {
        'Intercept': [1.0],
        'POLARITY': [polarity],
        'SUBJECTIVITY': [subjectivity],
        'POSTS_LENGTH': [length],
        'NUMBER_OF_ENTS': [number_of_ents],
        'SIMILARITY_TO_BEST': [similarity_to_best],
        'INDEX_HIGHER_THAN_HALF_BAYES': [index_higher_than_05],
        'INDEX_HIGHER_THAN_ONE_BAYES': [index_higher_than_1],
        'INDEX_HIGHER_THAN_THREE_BAYES': [index_higher_than_2]
    }

    df = pd.DataFrame(data_dict)
    return df


def get_bayes_index_for_x_index(text, x_index):
    vec = CountVectorizer()
    df_linkedin = pd.read_csv('data_linkedin/linkedin_data.csv')
    list_preprocessed_posts = df_linkedin['PREPROCESSED_POSTS']
    list_all_indexes = df_linkedin['INDEX']

    list_index_higher_than_x = []
    for index in list_all_indexes:
        if index > x_index:
            list_index_higher_than_x.append(1)
        else:
            list_index_higher_than_x.append(0)

    x = list_preprocessed_posts
    y = list_index_higher_than_x

    x, x_test, y, y_test = train_test_split(x, y, stratify=y, test_size=0.25, random_state=42)

    x = vec.fit_transform(x).toarray()
    x_test = vec.transform(x_test).toarray()

    model = MultinomialNB()
    model.fit(x, y)

    text_list = [text]

    prediction = model.predict(vec.transform(text_list))

    return prediction[0]


def get_best_post():
    df_facebook = pd.read_csv('data_linkedin/linkedin_data.csv')
    list_all_reactions = df_facebook['REACTIONS']
    list_posts = df_facebook['POSTS']

    max_reactions = 0
    best_index = 0
    for i in range(len(list_all_reactions)):
        if list_all_reactions[i] > max_reactions:
            max_reactions = list_all_reactions[i]
            best_index = i

    return list_posts[best_index]

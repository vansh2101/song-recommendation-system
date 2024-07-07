from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction.text import TfidfVectorizer
import textstat
import numpy as np


def extract_topics(lyrics, num_topics, num_words):
    try:
        vectorizer = CountVectorizer(input='content', strip_accents=None, stop_words='english')
        dtm = vectorizer.fit_transform(lyrics)
        lda = LatentDirichletAllocation(n_components=num_topics)
        lda.fit(dtm)

        topics = []
        for _, topic in enumerate(lda.components_):
            words = [vectorizer.get_feature_names_out()[i] for i in topic.argsort()[-num_words:]]
            topics.append(words)

        new_topics = set(tuple(topic) for topic in topics)
        new_topics = [list(new_topic) for new_topic in new_topics]
        return new_topics

    except:
        return []


def compute_tfidf(lyrics):
    try:
        vectorizer = TfidfVectorizer(stop_words='english')
        tfidf_matrix = vectorizer.fit_transform(lyrics)
        feature_names = vectorizer.get_feature_names_out()
        return tfidf_matrix, feature_names
    except:
        return [], np.array([])
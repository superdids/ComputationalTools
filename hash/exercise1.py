import json
import numpy as np
from sklearn.cross_validation import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction import DictVectorizer
from sklearn.feature_extraction.text import CountVectorizer

class ExerciseOne:

    __file_prefix = 'reuters-00'
    __file_postfix = '.json'

    def __construct_file_path(self, index):
        string = str(index) if index > 9 else '0' + str(index)
        return 'data-files/reuters-0' + string + '.json'

    def __should_exclude_article(self, article):
        return 'body' not in article or 'topics' not in article or len(article['topics']) < 1

    def load_files_construct_articles(self):
        articles = []
        article_topics = []
        for i in range(0, 22):
            with open(self.__construct_file_path(i)) as file:
                data = json.load(file)
                for article in data:
                    if not self.__should_exclude_article(article):
                        articles.append(article['body'].lower())
                        article_topics.append(article['topics'])
        return articles, article_topics

    def encode_bow(self, articles):

        distinct_words = dict()
        for article in articles:
            words_in_article = article.split()
            for word in words_in_article:
                if word not in distinct_words:
                    distinct_words[word] = 0

        bow_matrix = list()
        for index, article in enumerate(articles):
            bow_matrix.append(distinct_words)

            words_in_article = article.split()
            for word in words_in_article:
                bow_matrix[index][word] += 1

        return bow_matrix

    def forest_classifier(self, bow_matrix, topics):
        

        rfclf = RandomForestClassifier(n_estimators=50)
        #rfclf.fit(train)

        #rfclf.predict('earn')


    def load_files_construct_articles_2(self):
        '''
        Train a random forest classifier to predict if an article
        has the topic ‘earn’ or not from the body-text (encoded
        using bag-of-words). Use 80% of the data for training data
        and 20% for test data. Use 50 trees (n_estimators) in your
        classifier.
        '''
        #features = []
        #topics = []

        train = []

        for i in range(0, 22):
            with open(self.__construct_file_path(i)) as file:
                data = json.load(file)
                for article in data:
                    if not self.__should_exclude_article(article):
                        train.append(article)


        return train #features, topics

    def encode_bow_2(self, train):
        # vectorizer = CountVectorizer(min_df=1, lowercase=False)
        rfclf = RandomForestClassifier(n_estimators=50)
        rfclf.fit(train)


        rfclf.predict('earn')






'''instance = ExerciseOne()
#features, topics
train = instance.load_files_construct_articles_2()
#instance.encode_bow_2(features, topics)
instance.encode_bow_2(train)'''

instance = ExerciseOne()
articles, article_topics = instance.load_files_construct_articles()
bow_matrix = instance.encode_bow(articles)
print('(articles x features): (', len(bow_matrix), ' x ', len(bow_matrix[0]), ')')
instance.forest_classifier(bow_matrix, article_topics)

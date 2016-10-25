import json
import numpy as np
from sklearn.cross_validation import train_test_split
from sklearn.datasets import load_boston
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import RandomForestRegressor
from sklearn.feature_extraction import DictVectorizer
from sklearn.feature_extraction import FeatureHasher
from sklearn.feature_extraction.text import CountVectorizer, HashingVectorizer
import pandas as pd
from sklearn.preprocessing import MultiLabelBinarizer


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
                        articles.append(article['body'])
                        article_topics.append(article['topics'])
        return articles, article_topics

    def encode_bow(self, articles):
        distinct_words = dict()
        for article in articles:
            words_in_article = article.split()
            for word in words_in_article:
                if word not in distinct_words:
                    distinct_words[word] = len(distinct_words)

        bow_matrix = list()
        for index, article in enumerate(articles):
            bow_matrix.append([0] * len(distinct_words))
            words_in_article = article.split()
            for word in words_in_article:
                bow_matrix[index][distinct_words[word]] += 1

        return bow_matrix

    def encode_feature_hash_bow(self, articles):
        N = 1000
        bow_matrix = list()
        for index, article in enumerate(articles):
            bow_matrix.append([0] * N)
            words_in_article = article.split()
            for word in words_in_article:
                bow_matrix[index][self.__feature_hash(word)] += 1

        return bow_matrix

    def __feature_hash(self, item, buckets=1000):
        return hash(item) % buckets

    def forest_classifier(self, topics, articlos):

        #X_train, X_test, Y_train, Y_test = train_test_split(bow_matrix, topics, test_size=0.1)

        #clf = RandomForestClassifier(n_estimators=50)
        #clf.fit(X_train, Y_train)

        #clf.predict()

        vectorizer = CountVectorizer(analyzer=lambda x: x.split(), tokenizer=None, lowercase=True)

        X = vectorizer.fit_transform(articlos).toarray()
        print(X.shape)
        forest = RandomForestClassifier(n_estimators=50)
        Y = MultiLabelBinarizer().fit(topics)
        earn_index = np.array(Y.classes_).tolist().index('earn')
        Y = MultiLabelBinarizer().fit_transform(topics)
        X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2)
        #topics = pd.Series(topics)
        forest = forest.fit(X_train, Y_train)
        predict = forest.predict(X_test)
        score = forest.score(X_test, Y_test)

        print(score)



    def forest_classifier_feature_hashing(self, topics, articlos):
        #vectorizer = CountVectorizer(analyzer=lambda x: x.split(), tokenizer=None, lowercase=True)

        #X = vectorizer.fit_transform(articlos)
        #X = X.toarray()
        X = np.array(articlos)
        print(X.shape)


        forest = RandomForestClassifier(n_estimators=50)
        Y = MultiLabelBinarizer().fit(topics)
        earn_index = np.array(Y.classes_).tolist().index('earn')
        Y = MultiLabelBinarizer().fit_transform(topics)

        X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2)

        # topics = pd.Series(topics)
        forest = forest.fit(X_train, Y_train)
        #predict = forest.predict(X_test)
        predict = forest.predict_proba(X_test)
        
        #print(forest.score(X_test, Y_test))
        score = forest.score(X_test, Y_test)
        print(score)
        #print(score)







'''instance = ExerciseOne()
#features, topics
train = instance.load_files_construct_articles_2()
#instance.encode_bow_2(features, topics)
instance.encode_bow_2(train)'''

instance = ExerciseOne()
articles, article_topics = instance.load_files_construct_articles()
#bow_matrix = instance.encode_bow(articles)
#print('(articles x features): (', len(bow_matrix), ' x ', len(bow_matrix[0]), ')')


#distinct_topics = list(set([x for y in article_topics for x in y]))



# YEAH, works
#instance.forest_classifier(article_topics, articles)

bow_hash = instance.encode_feature_hash_bow(articles)
instance.forest_classifier_feature_hashing(article_topics, bow_hash)

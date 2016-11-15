import json
import numpy as np
import time
from sklearn.cross_validation import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import CountVectorizer


class ExerciseOne:
    # Creates a string that pertains to either of the given 22 files.
    def __construct_file_path(self, index):
        string = str(index) if index > 9 else '0' + str(index)
        return 'data-files/reuters-0' + string + '.json'

    # Determines whether an article should be included or not.
    def __should_exclude_article(self, article):
        return 'body' not in article or 'topics' not in article or len(article['topics']) < 1

    # Loads all the files, if a 'body' article is valid, it will be added along
    # with the expected result (whether 'earn' is contained in the 'topics' entry).
    def load_files_construct_articles(self):
        articles = []
        result_list = []
        for i in range(0, 22):
            with open(self.__construct_file_path(i)) as file:
                data = json.load(file)
                for article in data:
                    if not self.__should_exclude_article(article):
                        articles.append(article['body'].lower())
                        # If 'earn' is one of the values in the 'topics' entry,
                        # it will be added in the result list. However, if it is
                        # not contained, we add '0', which means that:
                        # This article does not contain the topic 'earn'.
                        if 'earn' in article['topics']:
                            result_list.append('earn')
                        else:
                            result_list.append('0')

        return articles, result_list

    # Creates a Bag of Words matrix given a list of articles. Each
    # word is associated to a specific feature given the result of
    # some feature hash function.
    def encode_feature_hash_bow(self, articles):
        N = 1000
        bow_matrix = list()
        for row, article in enumerate(articles):
            # Appends a row to the BOW matrix, the row will contain
            # 1000 cells with the value zero (representing 0 occurrences
            # of each feature).
            bow_matrix.append([0] * N)
            words_in_article = article.split()
            for word in words_in_article:
                # Increases the occurrence of a feature at a row, given
                # the result of the computed feature hash function.
                bow_matrix[row][self.__feature_hash(word, buckets=N)] += 1

        return bow_matrix

    # Hashes an item and returns an index within the boundary of
    # a given bucket size.
    def __feature_hash(self, item, buckets=1000):
        return hash(item) % buckets

    # Trains a Random Forest Classifier to predict whether articles has
    # the topic 'earn'.
    def forest_classifier_normal_bow(self, articles, earn_contained):

        # Prepare a vectorizer which will be used for BOW matrix generation.
        vectorizer = CountVectorizer(analyzer=lambda x: x.split())

        # Produce and encode a BOW matrix with (features x samples) dimensions,
        # each cell contains the occurrence of a given sample (column) in
        # a given article (row). Return a numpy array of the results
        # with the help of .toarray()
        X = vectorizer.fit_transform(articles).toarray()

        self.__forest_classifier(X, earn_contained)

    def forest_classifier_feature_hashing(self, articles, earn_contained):

        # As we produce the BOW matrix manually when hashing, we simply
        # convert the resulting list into a numpy array.
        X = np.array(articles)

        self.__forest_classifier(X, earn_contained)

    def __forest_classifier(self, X, earn_contained):

        print(X.shape)

        # Generate a vector that pertains to whether an article has the topic 'earn'.
        # As the resulting array becomes list of lists (with one element per list element),
        # we use the ravel function, which flattens the list to a one dimensional numpy array.
        Y = CountVectorizer(analyzer='word').fit_transform(earn_contained).toarray().ravel()

        # Initialize a forest classifier with 50 trees. n_jobs=-1 tells
        # the classifier to run with all cores available on the running
        # computer.
        forest = RandomForestClassifier(n_estimators=50, n_jobs=-1)

        # Split the data into 80% training data and 20% testing data.
        X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2)

        # Train the data using the RandomForestClassifier.
        forest = forest.fit(X_train, Y_train)

        # Compute the score / preciseness of the classifier.
        score = forest.score(X_test, Y_test)

        print(score)


instance = ExerciseOne()
articles, earn_list = instance.load_files_construct_articles()

start_time = time.time()
instance.forest_classifier_normal_bow(articles, earn_list)
print('Normal BOW execution time: ', (time.time() - start_time), ' seconds.')

start_time = time.time()
bow_hash = instance.encode_feature_hash_bow(articles)
instance.forest_classifier_feature_hashing(bow_hash, earn_list)
print('Feature hash bucketed BOW execution time: ', (time.time() - start_time), ' seconds.')

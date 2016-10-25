#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import random


class ExerciseOne:
    __file_prefix = 'reuters-00'
    __file_postfix = '.json'

    def __construct_file_path(self, index):
        # string = str(index) if index > 9 else '0' + str(index)
        # return 'data-files/reuters-0' + string + '.json'
        return 'data-files/reuters-100.json'

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

    """
    Create a matrix, with width = the number of distinct words from all articles, and is a hashed BOW, in the format
     that if a word is present in the article, we put 1 under the index of that word, for the current row of the matrix,
     where each row corresponds to an article.
    """

    def encode_bow(self, articles):
        distinct_words = dict()
        count = 0
        for article in articles:
            words_in_article = article.split()
            for word in words_in_article:
                # For each distinct word, as a key, put incremented integer, as a value
                if word not in distinct_words:
                    distinct_words[word] = count
                    count += 1

        bow_matrix = list()
        dist_words_count = len(distinct_words)
        for index, article in enumerate(articles):
            # Add a row of 0's for each new article, to the BOW matrix
            bow_matrix.append([0] * dist_words_count)

            words_in_article = article.split()
            # For each word in the article, get its value from the distinct words. That value is actually an index in
            # the current row of the BOW matrix. Put a 1 as a value to that index.
            for word in words_in_article:
                bow_matrix[index][distinct_words[word]] = 1

        return bow_matrix

    """
    Generate a list (permutation/hash function) of numbers from 0 to the length of the BOW matrix, shuffled randomly
    """

    def generate_permutation(self, bow_matrix):
        bow_matrix_len = len(bow_matrix)
        permutation = random.sample(xrange(0, bow_matrix_len), bow_matrix_len)
        return permutation

    """
    According to the permutation, generate a new matrix, from the BOW matrix
    """

    def permute_bow_matrix(self, bow_matrix, permutation):
        permuted_bow = list()
        for index, number in enumerate(permutation):
            permuted_bow.append(bow_matrix[permutation[index]])

        return permuted_bow


instance = ExerciseOne()
articles, article_topics = instance.load_files_construct_articles()
bow_matrix = instance.encode_bow(articles)
print 'articles x features => ' + str(len(bow_matrix)) + ' x ' + str(len(bow_matrix[0]))
# for bow_row in bow_matrix:
#     print(bow_row)

permutation_hash_1 = instance.generate_permutation(bow_matrix)
bow_permuted_1 = instance.permute_bow_matrix(bow_matrix, permutation_hash_1)

permutation_hash_2 = instance.generate_permutation(bow_matrix)
bow_permuted_2 = instance.permute_bow_matrix(bow_matrix, permutation_hash_2)

permutation_hash_3 = instance.generate_permutation(bow_matrix)
bow_permuted_3 = instance.permute_bow_matrix(bow_matrix, permutation_hash_3)

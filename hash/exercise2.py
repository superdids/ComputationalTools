#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import random

import re


class ExerciseOne:
    __file_prefix = 'reuters-00'
    __file_postfix = '.json'

    def __construct_file_path(self, index):
        string = str(index) if index > 9 else '0' + str(index)
        return 'data-files/reuters-0' + string + '.json'

    def __should_exclude_article(self, article):
        return 'body' not in article or 'topics' not in article or len(article['topics']) < 1

    # def load_files_construct_articles(self):
    #     articles = []
    #     article_topics = []
    #     format_string = lambda string: '' \
    #         .join(c for c in string if c not in '!"#%&/()=?\\1234567890+.,;:') \
    #         .lower()
    #
    #     for i in range(0, 22):
    #         with open(self.__construct_file_path(i)) as file:
    #             data = json.load(file)
    #             for article in data:
    #                 if not self.__should_exclude_article(article):
    #                     articles.append(format_string(article['body']))
    #                     article_topics.append(article['topics'])
    #     return articles, article_topics

    def load_files_construct_articles(self):
        articles = []
        article_topics = []
        format_string = lambda string: '' \
            .join(c for c in string if c not in '!"#%&/()=?\\1234567890+.,;:_') \
            .lower()

        with open('data-files/reuters-101.json') as file:
            data = json.load(file)
            for article in data:
                if not self.__should_exclude_article(article):
                    articles.append(format_string(article['body']))
                    article_topics.append(article['topics'])
        return articles, article_topics

    """
    Create a matrix, with width = the number of distinct words from all articles, and is a hashed BOW, in the format
     that if a word is present in the article, we put 1 under the index of that word, for the current row of the matrix,
     where each row corresponds to an article.
    """

    def encode_bow(self, articles, dist_words_list):
        distinct_words = dict()
        count = 0
        for article in articles:
            words_in_article = article.split()
            for word in words_in_article:
                # For each distinct word as key, put incremented integer as value
                if word not in distinct_words:
                    distinct_words[word] = count
                    dist_words_list.append(set())
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
    According to the permutation, generate a new matrix, from the BOW matrix.
    """

    def permute_bow_matrix(self, bow_matrix, permutation, dist_words_list):
        shuffled_bow = list()
        permuted_bow = dist_words_list

        # Shuffle and re-arrange the BOW according to the permutation. F.e. if the permutation is:
        # [6, 1, 7, 5, 4, 0, 3, 2, 8)], then the element on index 6 from the BOW will go on index 0 in the shuffled BOW,
        # the element on index 1 from the BOW will go index 1 in the shuffled, then el. on index 7 will go on index 2
        # in the shuffled BOW and so on.
        for index, number in enumerate(permutation):
            shuffled_bow.append(bow_matrix[permutation[index]])

        # TODO: change the algorithm here, so that it finds the first index of the main array at which it finds a 1
        # TODO ... for each letter, but not just where it finds 1 for first time and break
        for index, word_list in enumerate(shuffled_bow):
            for word_index, flag in enumerate(word_list):
                if flag == 1:
                    permuted_bow[word_index].add(index)
                    break

        return permuted_bow

# ----------------------------------------------------------------------------------------------------------------------
instance = ExerciseOne()
articles, article_topics = instance.load_files_construct_articles()
dist_words_list = list()
bow_matrix = instance.encode_bow(articles, dist_words_list)

permutation_hash_1 = instance.generate_permutation(bow_matrix)
bow_permuted_1 = instance.permute_bow_matrix(bow_matrix, permutation_hash_1, dist_words_list)
for index, row in enumerate(bow_permuted_1):
    if len(row) > 0:
        print (index, row)

print '-----------'

permutation_hash_2 = instance.generate_permutation(bow_matrix)
bow_permuted_2 = instance.permute_bow_matrix(bow_matrix, permutation_hash_2, dist_words_list)
for index, row in enumerate(bow_permuted_2):
    if len(row) > 0:
        print (index, row)

print '-----------'

permutation_hash_3 = instance.generate_permutation(bow_matrix)
bow_permuted_3 = instance.permute_bow_matrix(bow_matrix, permutation_hash_3, dist_words_list)
for index, row in enumerate(bow_permuted_3):
    if len(row) > 0:
        print (index, row)

print '-----------'

print 'articles x features => ' + str(len(bow_matrix)) + ' x ' + str(len(bow_matrix[0]))

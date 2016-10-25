#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json


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


instance = ExerciseOne()
articles, article_topics = instance.load_files_construct_articles()
bow_matrix = instance.encode_bow(articles)
print 'articles x features => ' + str(len(bow_matrix)) + ' x ' + str(len(bow_matrix[0]))

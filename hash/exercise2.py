#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import random

__file_prefix = 'reuters-00'
__file_postfix = '.json'


def __construct_file_path(file_index):
    string = str(file_index) if file_index > 9 else '0' + str(file_index)
    return 'data-files/reuters-0' + string + '.json'


def __should_exclude_article(article):
    return 'body' not in article or 'topics' not in article or len(article['topics']) < 1


def load_files_construct_articles():
    articles_list = []
    article_topics_list = []
    format_string = lambda string: '' \
        .join(c for c in string if c not in '!"#%&/()=?\\1234567890+.,;:') \
        .lower()

    for i in range(0, 22):
        with open(__construct_file_path(i)) as f:
            data = json.load(f)
            for article in data:
                if not __should_exclude_article(article):
                    articles_list.append(format_string(article['body']))
                    article_topics_list.append(article['topics'])
    return articles_list, article_topics_list


def load_files_construct_articles_test():
    articles_list = []
    article_topics_list = []
    format_string = lambda string: '' \
        .join(c for c in string if c not in '!"#%&/()=?\\1234567890+.,;:_') \
        .lower()

    with open('data-files/reuters-021.json') as f:
        data = json.load(f)
        for article in data:
            if not __should_exclude_article(article):
                articles_list.append(format_string(article['body']))
                article_topics_list.append(article['topics'])
    return articles_list, article_topics_list


"""
Create a matrix, with width = the number of distinct words from all articles, and is a hashed BOW, in the format
 that if a word is present in the article, we put 1 under the index of that word, for the current row of the matrix,
 where each row corresponds to an article.
"""


def encode_bow(articles_list):
    distinct_words = dict()
    dist_words = list()
    count = 0
    for article in articles_list:
        words_in_article = article.split()
        for word in words_in_article:
            # For each distinct word as key, put incremented integer as value
            if word not in distinct_words:
                distinct_words[word] = count
                dist_words.append(set())
                count += 1

    bow = list()
    dist_words_count = len(distinct_words)
    for i_article, article in enumerate(articles_list):
        # Add a row of 0's for each new article, to the BOW matrix
        bow.append([0] * dist_words_count)

        words_in_article = article.split()
        # For each word in the article, get its value from the distinct words. That value is actually an index in
        # the current row of the BOW matrix. Put a 1 as a value to that index.
        for word in words_in_article:
            bow[i_article][distinct_words[word]] = 1

    return bow, dist_words


"""
Generate a list (permutation/hash function) of numbers from 0 to the length of the BOW matrix, shuffled randomly
"""


def generate_permutation(bow):
    bow_matrix_len = len(bow)
    permutation = random.sample(xrange(0, bow_matrix_len), bow_matrix_len)
    return permutation


"""
According to the permutation, generate a new matrix, from the BOW matrix.
Then calculate the MinHash algorithm
"""


def permute_bow_matrix(bow, permutation, dist_words):
    shuffled_bow = list()
    # permuted_bow = copy.copy(dist_words)

    # Shuffle and re-arrange the BOW according to the permutation. F.e. if the permutation is:
    # [6, 1, 7, 5, 4, 0, 3, 2, 8)], then the element on index 6 from the BOW will go on index 0 in the shuffled BOW,
    # the element on index 1 from the BOW will go index 1 in the shuffled, then el. on index 7 will go on index 2
    # in the shuffled BOW and so on.
    for i_p, number in enumerate(permutation):
        shuffled_bow.append(bow[permutation[i_p]])

    # Loop through the `dist_words` (a list of indices of the words in the BOW, with value set()) - so, basically,
    # iterate for each distinct word, and then inner-iterate through the shuffled BOW matrix (permuted BOW), and
    # take the word of the current BOW by the current index of the `dist_words`, because each row of the BOW matrix
    # is identical to the `dist_words` list. Then check if the flag (the value) of the word in that row is 1.
    # If yes, add the index of that row from the BOW matrix, to the set of the current word in the `dist_words` and
    # break the loop (because we want to get the index of only the first occurrence of the word in the matrix).
    # If no, then go to the next row of the BOW matrix, and this way until we find a place where the flag is 1.
    for i_word, set_w in enumerate(dist_words):
        for i_word_list, word_list in enumerate(shuffled_bow):
            word_flag = word_list[i_word]
            if word_flag == 1:
                set_w.add(i_word_list)
                break

    return dist_words


def match_words_to_buckets(dist_words):
    buckets_list = list()
    checked_words = list()

    for outer_w_index, outer_words_set in enumerate(dist_words):
        # If this word has been compared already (which means it's already in a bucket), simply skip
        if outer_w_index in checked_words:
            continue

        match_set_found = False

        # Inner-loop through the list of "word-index: set()" and compare the current outer word-set to each inner
        # word-set until finding a match.
        for inner_w_index, inner_words_set in enumerate(dist_words):
            # If the outer index == the inner, then check if the word-set has already been placed in a bucket.
            # If not - place it there and continue with the next outer-iteration
            if outer_w_index == inner_w_index:
                if len(buckets_list) == 0:
                    bucket = set()
                    bucket.add(outer_w_index)
                    buckets_list.append(bucket)
                    checked_words.append(outer_w_index)  # add the current word index to the checked words
                    # The correct bucket is found, so don't iterate through the others
                    match_set_found = True
                    break
                else:
                    for bucket in buckets_list:
                        if outer_w_index in bucket:
                            bucket.add(outer_w_index)
                            checked_words.append(outer_w_index)  # add the current word index to the checked words
                            # The correct bucket is found, so don't iterate through the others
                            match_set_found = True
                            break
                    break

            # If there's a match of sets - loop through the already bucketed word indices and find the one where
            # the index of the outer-loop word index is present in. Then add this inner-loop index to that bucket
            if len(outer_words_set.symmetric_difference(inner_words_set)) == 0:
                bucket_found = False
                for bucket in buckets_list:
                    if inner_w_index in bucket:
                        bucket.add(outer_w_index)
                        checked_words.append(outer_w_index)  # add the current word index to the checked words
                        # The correct bucket is found, so don't iterate through the others
                        bucket_found = True
                        match_set_found = True
                        break

                if bucket_found is True:
                    break
                else:
                    # This word-set index hasn't been put in a dedicated bucket yet, so add both the inner- and outer-
                    # loop word-set indices to the same bucket.
                    bucket = set()
                    bucket.add(outer_w_index)
                    bucket.add(inner_w_index)
                    buckets_list.append(bucket)
                    checked_words.append(outer_w_index)  # add the outer-loop word index to the checked words
                    checked_words.append(inner_w_index)   # add the inner-loop word index to the checked words
                    match_set_found = True
                    break

        # No match set was found for the current outer-loop word-set index, so just create a new bucket and add this
        # index to it
        if match_set_found is False:
            bucket = set()
            bucket.add(outer_w_index)
            buckets_list.append(bucket)
            checked_words.append(outer_w_index)

    return buckets_list

# ----------------------------------------------------------------------------------------------------------------------
# articles, article_topics = load_files_construct_articles()
articles, article_topics = load_files_construct_articles_test()
bow_matrix, dist_words_list = encode_bow(articles)

permutation_hash_1 = generate_permutation(bow_matrix)
dist_words_list = permute_bow_matrix(bow_matrix, permutation_hash_1, dist_words_list)
print "Permutation 1 finished!"

permutation_hash_2 = generate_permutation(bow_matrix)
dist_words_list = permute_bow_matrix(bow_matrix, permutation_hash_2, dist_words_list)
print "Permutation 2 finished!"

permutation_hash_3 = generate_permutation(bow_matrix)
dist_words_list = permute_bow_matrix(bow_matrix, permutation_hash_3, dist_words_list)
print "Permutation 3 finished!"

for index, row in enumerate(dist_words_list):
    if len(row) > 0:
        print (index, row)

print '-----------'

buckets = match_words_to_buckets(dist_words_list)
for b in buckets:
    print b
print len(buckets)

print 'articles x features => ' + str(len(bow_matrix)) + ' x ' + str(len(bow_matrix[0]))

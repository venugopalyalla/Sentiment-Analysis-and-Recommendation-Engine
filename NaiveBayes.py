import csv
from nltk.tokenize import word_tokenize
import string
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
import nltk

import random

def findNaiveBayesAccuracy(filename, percentOfTrainingData):
    stopWords = set(
        [u'ive', u'all', u'just', u'being', u'over', u'both', u'through', u'yourselves', u'its', u'before', u'herself',
         u'had', u'should', u'to', u'only', u'under', u'ours', u'has', u'do', u'them', u'his', u'very', u'they',
         u'during',
         u'now', u'him', u'did', u'this', u'she', u'each', u'further', u'where', u'few', u'because', u'doing', u'some',
         u'are', u'our', u'ourselves', u'out', u'what', u'for', u'while', u're', u'does', u'above', u'between', u'be',
         u'we', u'who', u'were', u'here', u'hers', u'by', u'on', u'about', u'of', u'against', u'or', u'own', u'into',
         u'yourself', u'down', u'your', u'from', u'her', u'their', u'there', u'been', u'whom', u'too', u'themselves',
         u'was', u'until', u'more', u'himself', u'that', u'but', u'with', u'than', u'those', u'he', u'me', u'myself',
         u'ma',
         u'these', u'up', u'will', u'below', u'can', u'theirs', u'my', u'and', u'then', u'is', u'am', u'it', u'an',
         u'as',
         u'itself', u'at', u'have', u'in', u'any', u'if', u'again', u'when', u'same', u'how', u'other', u'which',
         u'you',
         u'after', u'most', u'such', u'why', u'a', u'off', u'i', u'm', u'yours', u'so', u'y', u'the', u'having',
         u'once'])
    neg_word = ["no", "not", "rather", "couldnt", "wasnt", "didnt", "wouldnt", "shouldnt", "werent", "dont", "doesnt",
                "havent", "hasnt", "wont", "hadnt", "never", "none", "nobody", "nothing", "neither", "nor", "nowhere",
                "isnt", "cant", "cannot", "mustnt", "mightnt", "shant", "without", "neednt"]
    f = open(filename, 'rb')
    fo = open('sample/nb.csv', 'wb')

    freader = csv.reader(f)
    fwriter = csv.writer(fo)

    # code to remove stop words from the review
    for l in freader:
        l[0] = l[0].translate(None, string.punctuation)
        reviewWords = word_tokenize(l[0].lower())
        # combine the negatino conjugates in string
        delIndex = []
        for t in range(len(reviewWords)):
            if reviewWords[t] in neg_word:
                if t + 1 < len(reviewWords):
                    temp = [reviewWords[t], reviewWords[t + 1]]
                    result = nltk.pos_tag(temp)
                    if result[1][1] == 'JJ' or result[1][1] == 'JJR' or result[1][1] == 'JJS':
                        tempStr = reviewWords[t] + '_' + reviewWords[t + 1]
                        reviewWords[t] = tempStr
                        delIndex.append(t + 1)
        for d in range(len(delIndex)):
            del reviewWords[delIndex[d]]
        # Remove stop words from the list
        words_filter = []
        for w in reviewWords:
            if w not in stopWords:
                words_filter.append(w)
        l[0] = ' '.join(word for word in words_filter)
        fwriter.writerow(l)

    f.close()
    fo.close()

    # collect reviews into lists, X -> reviews Y -> label(positive/negative)
    review_set = []
    label_set = []
    count_vector = CountVectorizer()
    freader = csv.reader(open('sample/nb.csv', 'rb'))

    completeData = []
    for f in freader:
        list1 = [f[0], f[1]]
        completeData.append(list1)

    random.shuffle(completeData)
    for c in completeData:
        review_set.append(c[0])
        label_set.append(c[1])

    # data - with review and label
    X = count_vector.fit_transform(review_set).toarray()
    Y = [int(l) for l in label_set]

    count_review = len(Y)
    count_train = int(count_review * percentOfTrainingData)
    count_test = count_review - count_train

    x_train = X[0:count_train]
    x_test = X[0: count_review]
    y_train = Y[0:count_train]
    y_test = Y[0: count_review]

    # count number of features(unique words) and number of reviews
    num_features = len(x_train[0])
    num_reviews = len(x_train)

    # divide the training data into two classed (0/1)
    review_class = [[rev for rev, lab in zip(x_train, y_train) if lab == c] for c in np.unique(y_train)]

    # calculate the class prior class = 0 and 1
    class_prior = [(float(len(i)) / float(num_reviews)) for i in review_class]

    # calcuate likelihood for each class
    # likelihood = word_count+1/number_features + (total word count in that class)

    # numerator of likelihood
    word_count = np.array([np.array(i).sum(axis=0) for i in review_class]) + 1
    # calculate denominator for each class separately
    num_zero = num_features
    num_one = num_features
    for i in range(num_features):
        num_zero = num_zero + word_count[0][i]
        num_one = num_one + word_count[1][i]

    likelihood = np.asarray(word_count, dtype=float)

    # calculate likelihood for each feature for each class and store it in likelihood array
    for i in range(num_features):
        likelihood[0][i] = float((word_count[0][i]) / float(num_zero))
        likelihood[1][i] = float(word_count[1][i]) / float(num_one)

    # calculate the accuracy for test data given test reviews and test labels
    y_label_cal = range(len(y_test))
    # print y_label_cal

    for i in range(len(y_test)):
        p0_test = class_prior[0]
        p1_test = class_prior[1]
        for j in range(num_features):
            if x_test[i][j] > 0:
                p0_test = float(p0_test * pow(likelihood[0][j], x_test[i][j]))
                p1_test = float(p1_test * pow(likelihood[1][j], x_test[i][j]))
        if p0_test > p1_test:
            y_label_cal[i] = 0
        else:
            y_label_cal[i] = 1
    return y_label_cal

import csv
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import string
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
import nltk
import random
from scipy.special import expit
import numpy as np
from sets import Set


def generate_Y_vector(training_set, training_class):
    no_reviews = len(training_set)
    Y = np.zeros(shape=no_reviews)
    for ii in range(0,no_reviews):
        Y[ii] = training_class[ii]
    return Y

def gradient_descent(X, Y_neg,theta,alpha, m,numIterations):
    for iter in range(0,numIterations):
        cost = cost_function(X, Y_neg, theta)
        delta = gradient(X, Y_neg, theta)
        theta -= alpha * delta
    return theta

def cost_function(X, Y, theta):
    no_examples = len(X)
    predicted_Y_values = hypothesis(X, theta)
    cost = (-1.0 / no_examples) * np.sum(Y * np.log(predicted_Y_values) + (1 - Y) * (np.log(1 - predicted_Y_values)))
    return cost

def gradient(X,Y, theta):
    no_examples = len(X)
    predicted_Y_values = hypothesis(X, theta)
    grad = (-1.0 / no_examples) * np.dot((Y - predicted_Y_values), X)
    return grad

def hypothesis(X, theta):
    return 1 / (1 + np.exp(-1.0 * np.dot(X,theta)))

def findMaxEntAccuracy(filename, percentOfTrainingData):
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
    fo = open('sample/maxent.csv', 'wb')

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

    review_set = []
    label_set = []
    count_vector = CountVectorizer()
    freader = csv.reader(open('sample/maxent.csv', 'rb'))

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

    x_train = X[0:count_train][:]
    y_train = Y[0:count_train]
    x_test = X[0:count_review][:]
    y_test = Y[0: count_review]

    # count number of features(unique words) and number of reviews
    num_features = len(x_train[0])
    num_reviews = len(x_train)

    # divide the training data into two classed (0/1)
    review_class = [[rev for rev, lab in zip(x_train, y_train) if lab == c] for c in np.unique(y_train)]
    word_count = np.array([np.array(i).sum(axis=0) for i in review_class]) + 1
    # calculate denominator for each class separately
    num_zero = num_features
    num_one = num_features

    m, n = np.shape(x_train)

    theta = np.ones(n)
    numIterations = 1000
    alpha = 0.99

    Y_neg = generate_Y_vector(X[0:count_train], Y[0:count_train])
    theta_neg = gradient_descent(x_train, Y_neg, theta, alpha, m, numIterations)

    y_label_cal = range(len(y_test))
    for i in range(len(y_test)):
        p = 0
        total_words_in_review = sum(x_test[i])
        for j in range(num_features):
            if x_test[i][j] > 0:
                p += (x_test[i][j] * theta_neg[j]) / total_words_in_review
        if p >= 0:
            y_label_cal[i] = 1
        else:
            y_label_cal[i] = 0
    return y_label_cal


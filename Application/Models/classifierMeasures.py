##############################################################################
# A collection of functions that generate measures out of a confusion matrix #
##############################################################################

"""Measures for multi-class classification"""

def avg_accuracy(confusion_matrix):
    """The average per-class effectiveness of a classifier"""
    result = 0
    for i in xrange(len(confusion_matrix)-2):
        denominator = (confusion_matrix[i, 7] + confusion_matrix[7, i] - confusion_matrix[i, i])
        if denominator != 0:
            result += confusion_matrix[7, i] / denominator
    return result / (len(confusion_matrix)-2)

def err_rate(confusion_matrix):
    """The average per-class classification error"""
    result = 0
    for i in xrange(len(confusion_matrix)-2):
        denominator = (confusion_matrix[i, 7] + confusion_matrix[7, i] - confusion_matrix[i, i])
        if denominator != 0:
            result += confusion_matrix[i, 7] / denominator
    return result / (len(confusion_matrix)-2)

def precision_mu(confusion_matrix):
    """Agreement of the data class labels with those
     of a classifiers if calculated from sums of per-text decisions"""
    numerator = 0.0
    denominator = 0.0
    for i in xrange(len(confusion_matrix)-2):
        numerator += confusion_matrix[i, i]
        denominator += confusion_matrix[i, 7]
    if denominator == 0:
        return 0
    return numerator / denominator

def recall_mu(confusion_matrix):
    """Effectiveness of a classifier to identify
    class labels if calculated from sums of per-text decisions"""
    numerator = 0.0
    denominator = 0.0
    for i in xrange(len(confusion_matrix)-2):
        numerator += confusion_matrix[i, i]
        denominator += confusion_matrix[7, i]
    if denominator == 0:
        return 0
    return numerator / denominator

def fscore_mu(confusion_matrix, beta):
    """Relations between data s positive labels and
     those given by a classifier based on sums of per-text decisions"""
    p = precision_mu(confusion_matrix)
    r = recall_mu(confusion_matrix)
    numerator = (beta*beta + 1) * p * r
    denominator = beta*beta * p + r
    if denominator == 0:
        return 0
    return numerator / denominator

def precision(confusion_matrix):
    """An average per-class agreement of the data class labels with those of a classifiers"""
    numerator = 0.0
    for i in xrange(len(confusion_matrix)-2):
        if confusion_matrix[i, 7] != 0:
            numerator += confusion_matrix[i, i] / confusion_matrix[i, 7]
    return numerator / (len(confusion_matrix)-2)

def recall(confusion_matrix):
    """An average per-class effectiveness of a classifier to identify class labels"""
    numerator = 0
    for i in xrange(len(confusion_matrix)-2):
        if confusion_matrix[7, i] != 0:
            numerator += confusion_matrix[i, i] / confusion_matrix[7, i]
    return numerator / (len(confusion_matrix)-2)

def fscore(confusion_matrix, beta):
    """Relations between data's positive labels and
    those given by a classifier based on a per-class average"""
    p = precision(confusion_matrix)
    r = recall(confusion_matrix)
    numerator = (beta*beta + 1) * p * r
    denominator = beta*beta * p + r
    if denominator == 0:
        return 0
    return numerator / denominator

""" This file is for reading in the graph and creating additional attributes.
"""
import snap

def simple_un_enron():
    return snap.LoadEdgeList(snap.PUNGraph, "data/snap/email-Enron.txt", 0, 1)

def dir_enron(start, end):
    """
    :param start: Start time to count emails.
    :param end: End time to count emails.
    :return: Simple direÅcted graph with each edge having number of emails sent from a to b, time of first email, time of last email.
    """
    pass

def additional_enron():
    pass
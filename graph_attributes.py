""" This file is for reading in the graph and creating additional attributes.
"""
import snap

def simple_un_enron():
    return snap.LoadEdgeList(snap.PUNGraph, "data/snap/email-Enron.txt", 0, 1)

def dir_enron(start, end):
    """
    :param start: Start time to count emails.
    :param end: End time to count emails.
    :return:
    """
    pass

def additional_entron():
    pass
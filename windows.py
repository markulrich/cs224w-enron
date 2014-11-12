""" This file is for performing the MLP
"""
from edges_by_timestamp import strtotime, edges_by_weight, TIME_FORMAT, getWindowDirName
from extract_features import write_features
import datetime
import time

MIN_TIME = '1998-10-30 07:43:00'
MAX_TIME = '2002-07-12 01:31:00'

def toDateTime(strtime):
    return datetime.datetime(*(strtotime(strtime)[0:6]))

def generate_window_networks(start_time=MIN_TIME, time_increment=datetime.timedelta(days = 30), final_end_time=MAX_TIME):
    start_time = toDateTime(start_time)
    final_end_time = toDateTime(final_end_time)
    while True:
        end_time = start_time + time_increment
        if end_time > final_end_time:
            break
        edges_by_weight(start_time.strftime(TIME_FORMAT), end_time.strftime(TIME_FORMAT))
        start_time = end_time

def generate_window_features(start_time=MIN_TIME, time_increment=datetime.timedelta(days = 30), final_end_time=MAX_TIME):
    start_time = toDateTime(start_time)
    final_end_time = toDateTime(final_end_time)
    while True:
        end_time = start_time + time_increment
        if end_time > final_end_time:
            break
        directory = getWindowDirName(start_time.strftime(TIME_FORMAT), end_time.strftime(TIME_FORMAT))
        write_features(directory + 'network.net', directory)
        start_time = end_time

if __name__ == '__main__':
    generate_window_networks()
    generate_window_features()
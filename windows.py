""" This file is for performing the MLP
"""
from edges_by_timestamp import strtotime, edges_by_weight, TIME_FORMAT, getWindowDirName
from extract_features import write_features
import datetime
import time

MIN_TIME = '1998-10-30 07:43:00'
MAX_TIME = '2002-07-12 01:31:00'

def getWindowDateTimes(start_time=MIN_TIME, time_increment=datetime.timedelta(days = 100), final_end_time=MAX_TIME):
    start_time = toDateTime(start_time)
    final_end_time = toDateTime(final_end_time)
    while True:
        end_time = start_time + time_increment
        if end_time > final_end_time:
            break
        yield (start_time, end_time)
        start_time = end_time

def getWindowEpochs(start_time=MIN_TIME, time_increment=datetime.timedelta(days = 100), final_end_time=MAX_TIME):
    return ((start.strftime(TIME_FORMAT), end.strftime(TIME_FORMAT)) for start, end in getWindowDateTimes(start_time, time_increment, final_end_time))

def getWindowNames(start_time=MIN_TIME, time_increment=datetime.timedelta(days = 100), final_end_time=MAX_TIME):
    return (getWindowDirName(start.strftime(TIME_FORMAT), end.strftime(TIME_FORMAT)) for start, end in getWindowDateTimes(start_time, time_increment, final_end_time))

def toDateTime(strtime):
    return datetime.datetime(*(strtotime(strtime)[0:6]))

def generate_window_networks(windows):
    for start_time, end_time in windows:
        edges_by_weight(start_time.strftime(TIME_FORMAT), end_time.strftime(TIME_FORMAT))

def generate_window_features(windows):
    for start_time, end_time in windows:
        directory = getWindowDirName(start_time.strftime(TIME_FORMAT), end_time.strftime(TIME_FORMAT))
        write_features(directory + 'network.txt', directory)

def generate_window_networks_and_features(windows):
    for start_time, end_time in windows:
        edges_by_weight(start_time.strftime(TIME_FORMAT), end_time.strftime(TIME_FORMAT))
        directory = getWindowDirName(start_time.strftime(TIME_FORMAT), end_time.strftime(TIME_FORMAT))
        write_features(directory + 'network.txt', directory)

if __name__ == '__main__':
    windows = getWindowDateTimes(time_increment=datetime.timedelta(days = 60))
    generate_window_networks_and_features(windows)
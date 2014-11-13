""" This file is for performing the MLP
"""
from edges_by_timestamp import strtotime, edges_by_weight, TIME_FORMAT, getWindowDirName
from extract_features import write_features, genLabelFile
from multiprocessing import Pool
import datetime
import time

MIN_TIME = '1999-06-01 00:00:00'
MAX_TIME = '2001-06-01 00:00:00'

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

def generate_window_networks_and_features(windows, windowName):
    for start_time, end_time, next_time in windows:
        directory = getWindowDirName(start_time.strftime(TIME_FORMAT), end_time.strftime(TIME_FORMAT), windowName)
        edges_by_weight(start_time.strftime(TIME_FORMAT), end_time.strftime(TIME_FORMAT), directory, 'network')
        write_features(directory + 'network.txt', directory)
        edges_by_weight(end_time.strftime(TIME_FORMAT), next_time.strftime(TIME_FORMAT), directory, 'future')
        genLabelFile(directory + 'future.txt', directory, 'Labels.txt')

if __name__ == '__main__':
    # windows = getWindowDateTimes(time_increment=datetime.timedelta(days = 60))
    # generate_window_networks_and_features(windows)
    base = toDateTime('2000-01-01 00:00:00')
    N_DELTAS = 9
    delta = [datetime.timedelta(days = 2**i) for i in range(N_DELTAS)]

    def call_gwnaf(data):
        i, j = data
        generate_window_networks_and_features([(base - delta[i], base, base + delta[j])], '{} {} (days past, days future)'.format(i, j))

    p = Pool(processes=3)
    for i in range(N_DELTAS):
        p.map(call_gwnaf, [(i, j) for j in range(N_DELTAS)])

""" This file is for performing the MLP
"""
from edges_by_timestamp import strtotime, edges_by_weight, TIME_FORMAT, getWindowDirName
from extract_features import write_features, genLabelFile
from multiprocessing import Pool
import datetime
import time
import sys
import os

MIN_TIME = '2000-01-01 00:00:00'
MAX_TIME = '2001-05-01 00:00:00'

def getWindowDateTimes(start_time=MIN_TIME, time_increment=datetime.timedelta(days = 100), final_end_time=MAX_TIME):
    start_time = toDateTime(start_time)
    final_end_time = toDateTime(final_end_time)
    while True:
        end_time = start_time + time_increment
        next_time = end_time + time_increment
        if next_time > final_end_time:
            break
        yield (start_time, end_time, next_time)
        start_time = end_time

def getWindowEpochs(start_time=MIN_TIME, time_increment=datetime.timedelta(days = 100), final_end_time=MAX_TIME):
    return ((start.strftime(TIME_FORMAT), end.strftime(TIME_FORMAT)) for start, end in getWindowDateTimes(start_time, time_increment, final_end_time))

def getWindowNames(start_time=MIN_TIME, time_increment=datetime.timedelta(days = 100), final_end_time=MAX_TIME):
    return (getWindowDirName(start.strftime(TIME_FORMAT), end.strftime(TIME_FORMAT)) for start, end in getWindowDateTimes(start_time, time_increment, final_end_time))

def toDateTime(strtime):
    return datetime.datetime(*(strtotime(strtime)[0:6]))

def generate_window_networks_and_features(windows, windowName):
    if os.path.isdir('windows/' + windowName):
        print 'ERROR {} already exists'.format(windowName)
        return
    for start_time, end_time, next_time in windows:
        directory = getWindowDirName(start_time.strftime(TIME_FORMAT), end_time.strftime(TIME_FORMAT), windowName)
        edges_by_weight(start_time.strftime(TIME_FORMAT), end_time.strftime(TIME_FORMAT), directory, 'network')
        write_features(directory + 'network.txt', directory, (start_time, end_time))
        edges_by_weight(end_time.strftime(TIME_FORMAT), next_time.strftime(TIME_FORMAT), directory, 'future')
        genLabelFile(directory + 'future.txt', directory, 'Labels.txt')

def gen_delta_windows():
    base = toDateTime(MIN_TIME)
    N_DELTAS = 9
    delta = [datetime.timedelta(days = 2**i) for i in range(N_DELTAS)]

    def call_gwnaf(data):
        i, j = data
        generate_window_networks_and_features([(base - delta[i], base, base + delta[j])], '{} {} (days past, days future)'.format(i, j))

    # p = Pool(processes=3)
    for i in range(N_DELTAS):
        [call_gwnaf((i, j)) for j in range(N_DELTAS)]
        # p.map(call_gwnaf, [(i, j) for j in range(N_DELTAS)])

def gen_linear_windows(days=60):
    windows = getWindowDateTimes(time_increment=datetime.timedelta(days=days))
    generate_window_networks_and_features(windows, 'attrdays' + str(days))

if __name__ == '__main__':
    if sys.argv[1] == 'delta':
        gen_delta_windows()
    elif sys.argv[1] == 'linear':
        gen_linear_windows()
    elif sys.argv[1] == 'simple':
        days = 4
        windows = getWindowDateTimes(start_time='2000-01-01 00:00:00', time_increment=datetime.timedelta(days = days), final_end_time='2000-01-09 00:00:00')
        generate_window_networks_and_features(windows, 'days{}'.format(days))
    else:
        print 'Option not available.'
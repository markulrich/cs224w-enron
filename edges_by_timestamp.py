import time
import re
import random
import os

TIME_FORMAT = "%Y-%m-%d %H:%M:%S"
VP_NAME = './vertex_prefix.txt'

def getWindowDirName(startTime, endTime):
    if type(startTime) is str:
        startTime = strtotime(startTime)
    if type(endTime) is str:
        endTime = strtotime(endTime)
    return './windows/time_%d_%d/' % (int(time.mktime(startTime)), int(time.mktime(endTime)))

def strtotime(strtime):
    return time.strptime(strtime, TIME_FORMAT)

# omits timestamp (since each edge can have multiple timestamps)
# start and end should be in format "YYYY-MM-DD HH:MM:SS"
def edges_by_weight(startTime, endTime, perc=1.0):
    directory = getWindowDirName(startTime, endTime)
    if type(startTime) is str:
        startTime = strtotime(startTime)
    if type(endTime) is str:
        endTime = strtotime(endTime)
    edgesf = open('./edges.txt', 'r')
    if not os.path.exists(directory):
        os.makedirs(directory)
    filename = directory + 'network.txt'
    file_by_weight = open(filename, 'w')
    edges = {}
    nodes = set()
    ex_to_in = {}
    for line in edgesf:
        if random.random() < perc:
            tokens = line.split(',')
            if strtotime(tokens[0]) >= startTime and strtotime(tokens[0]) <= endTime:
                src = int(tokens[1])
                dst = int(tokens[2])
                if (src, dst) in edges:
                    edges[(src, dst)] += 1
                else:
                    edges[(src, dst)] = 1
                    nodes.add(src)
                    nodes.add(dst)
    file_by_weight.write("*Vertices %d\n" % len(nodes))
    count = 0
    for node in nodes:
        file_by_weight.write("%d %d\n" % (count, node))
        ex_to_in[node] = count
        count += 1
    file_by_weight.write("*Edges %d\n" % (len(edges)))
    for edge in edges:
        file_by_weight.write("%d %d %d\n" % (ex_to_in[edge[0]], ex_to_in[edge[1]], edges[edge]))
    file_by_weight.close()
    edgesf.close()
        
# filters edges by time, all with weight 1
# start and end should be in format "YYYY-MM-DD HH:MM:SS"
def edges_by_timestamp(file, start, end):
    filename = "./edges_timestamp_%d_%d" % (int(time.mktime(strtotime(start))), int(time.mktime(strtotime(end))))
    file_by_timestamp = open(filename, 'w')
    for line in file:
        tokens = line.split(',')
        if strtotime(tokens[0]) >= strtotime(start) and strtotime(tokens[0]) <= strtotime(end):
            file_by_timestamp.write("%s,%d,%d,%f\n" % (tokens[0], int(tokens[1]), int(tokens[2]), 1.0))
    file_by_timestamp.close()

# returns a hash of id to email (from email.txt)
def get_emails(file):
    id_to_email = {}
    for i in file:
        tokens = re.split(',| ', i)
        id = int(tokens[0])
        email = tokens[1]
        id_to_email[id] = email
    return id_to_email

def write_vertices():
    emailsf = open('./email.txt', 'r')
    vertexf = open(VP_NAME, 'w')
    nodes = []
    for line in emailsf:
        nodes.append(int(line.split(',')[0]))
    vertexf.write("*Vertices %d\n" % len(nodes))
    count = 0
    for i in nodes:
        vertexf.write("%d %d\n" % (count, i))
        count += 1
    vertexf.close()
    emailsf.close()

if __name__ == '__main__':
    edges_by_weight("2000-09-01 00:00:00", "2000-09-30 23:59:59")
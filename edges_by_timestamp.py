import time
import re
import random

def strtotime(strtime):
    return time.strptime(strtime, "%Y-%m-%d %H:%M:%S")

# omits timestamp (since each edge can have multiple timestamps)
# start and end should be in format "YYYY-MM-DD HH:MM:SS"
def edges_by_weight(file, start, end, perc=1.0):
    filename = "./edges_weight_%d_%d.net" % (int(time.mktime(strtotime(start))), int(time.mktime(strtotime(end))))
    file_by_weight = open(filename, 'w')
    edges = {}
    for line in file:
        if random.random() < perc:
            tokens = line.split(',')
            if strtotime(tokens[0]) >= strtotime(start) and strtotime(tokens[0]) <= strtotime(end):
                src = int(tokens[1])
                dst = int(tokens[2])
                if (src, dst) in edges:
                    edges[(src, dst)] += 1
                else:
                    edges[(src, dst)] = 1
    vertex_file = open('./vertex_prefix.txt', 'r')
    for line in vertex_file:
        file_by_weight.write(line)
    file_by_weight.write("*Edges %d\n" % (len(edges)))
    for edge in edges:
        file_by_weight.write("%d %d %d\n" % (edge[0], edge[1], edges[edge]))
    file_by_weight.close()
        
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

def write_vertices(emailsf):
    vertexf = open('./vertex_prefix.txt', 'w')
    nodes = []
    for line in emailsf:
        nodes.append(int(line.split(',')[0]))
    vertexf.write("*Vertices %d\n" % len(nodes))
    count = 0
    for i in nodes:
        vertexf.write("%d %d\n" % (count, i))
        count += 1

emailsf = open('./email.txt', 'r')
edgesf = open('./edges.txt', 'r')
edges_by_weight(edgesf, "2000-09-01 00:00:00", "2000-09-30 23:59:59")
edgesf.close()
emailsf.close()
import time

def strtotime(strtime):
	return time.strptime(strtime, "%Y-%m-%d %H:%M:%S")

# omits timestamp (since each edge can have multiple timestamps)
# start and end should be in format "YYYY-MM-DD HH:MM:SS"
def edges_by_weight(file, start, end):
	file_by_weight = open('./edges_weight_' + time.mktime(start) + 
		'_' + time.mktime(end), 'w')
	edges = {}
	for line in file:
		tokens = line.split(',')
		if strtotime(tokens[0]) >= strtotime(start) and strtotime(tokens[0]) <= strtotime(end):
			if (tokens[1], tokens[2]) in edges:
				edges[(tokens[1], tokens[2])].append(tokens[0])
			else:
				edges[(tokens[1], tokens[2])] = [tokens[0]]
	for edge in edges:
		file_by_weight.write("%d,%d,%d\n" % (edge[0], edge[1], len(edges[edge])))
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
	
edgesf = open('./edges.txt', 'r')
edges_by_timestamp(edgesf, "2000-09-01 00:00:00", "2000-09-30 23:59:59")
edgesf.close()
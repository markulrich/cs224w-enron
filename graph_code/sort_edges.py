import snap

edges = open('./edges.txt', 'r')
lines = edges.readlines()
lines.sort()
edges_sorted = open('./edges_sorted.txt', 'w')
edges_sorted.writelines(lines)
edges_sorted.close()
edges.close()
FILENAME = 'message_class.labels'

label_freqs = [0] * 6

num_lines = 0

with open(FILENAME, 'r') as f:
    for line in f:
        num_lines += 1
        line = line.split()[1:]
        for i, item in enumerate(line):
            label_freqs[i] += int(item)

print label_freqs
print sum(label_freqs)
for label in label_freqs:
    print label / float(sum(label_freqs))
    print label / float(num_lines)
    print ' --- --- --- '

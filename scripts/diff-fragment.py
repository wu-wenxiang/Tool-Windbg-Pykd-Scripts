fragment_start = r'C:\local\tmp\fragment-start.txt'
fragment_end = r'C:\local\tmp\fragment-end.txt'

setStart = set(tuple(eval(line.strip())) for line in open(fragment_start) if line.startswith('['))
setEnd = set(tuple(eval(line.strip())) for line in open(fragment_end) if line.startswith('['))

diffFragment = setEnd - setStart

diffFile = open(r'C:\local\tmp\fragment-diff.txt', 'w')
for i in sorted(diffFragment, key=lambda x:int(x[0], 16)):
    diffFile.write('  '.join(i)+'\n')





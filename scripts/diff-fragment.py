fragment_start = r'C:\Users\wenw\Desktop\dump&TTT\fragment-start.txt'
fragment_end = r'C:\Users\wenw\Desktop\dump&TTT\fragment-end.txt'

setStart = set(tuple(eval(line.strip())) for line in open(fragment_start) if line)
setEnd = set(tuple(eval(line.strip())) for line in open(fragment_end) if line)

diffFragment = setEnd - setStart

diffFile = open(r'C:\Users\wenw\Desktop\dump&TTT\fragment-diff.txt', 'w')
for i in sorted(diffFragment, key=lambda x:int(x[0], 16)):
    diffFile.write('  '.join(i)+'\n')





file = open('drug_pre-suf.txt','r')
prefix = open('prefix.txt','w')
suffix = open('suffix.txt','w')
middle = open('middle.txt','w')
prefixes,suffixes,middles = set(),set(),set()
for line in file:
    word = line.strip()
    if '-' in word:
        if word[0] == '-': suffixes.add(word[1:].strip())
        else: prefixes.add(word[:-1].strip())
    else: middles.add(word)

def write_file(itr,file):
    for i in itr:
        file.write(i+'\n')
print('Prefix', list(prefixes))
print('Suffix', list(suffixes))
print('Middle', list(middles))
# write_file(prefixes,prefix)
# write_file(suffixes,suffix)
# write_file(middles,middle)
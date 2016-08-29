import csv
o = open('bg.csv', 'wb')
writer = csv.writer(o)
f = open('bg.txt')
data = f.readlines()

for line in data:
    print line.strip().split('\t')[0], '****', line.strip().split('\t')[-1]
##    data_split = line.strip().split('\t')
##    data_element = data_split[0]
##    description = data_split[-1]
##    while True:        
##        if data_element!='':
##            break
##        else:
##            description +=data_split[-1]
##    print data_element , description 
        

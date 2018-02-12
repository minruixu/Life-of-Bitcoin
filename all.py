import re
times = {}
sum = {}

for i in range(1,34):
    for line in open('trackbtc/%s.csv'%i,'r'):
        if re.search(r'[-]+',line):
            continue
        else:
            put = line.split(',')
            if put[0] not in times:
                times[put[0]] = 0
                sum[put[0]] = 0
                times[put[0]] += 1
                sum[put[0]] += float(put[1])
            else:
                times[put[0]] += 1
                sum[put[0]] += float(put[1])
fo = open('trackbtc/report.csv','a')
fo.write('address,times of input,sum of btc\n')
for key in times:
    fo.write(key + ',' +str(times[key]) + ',' + str(sum[key]) + '\n')
fo.close()
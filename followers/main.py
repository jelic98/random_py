import time
import requests

skip = 0

limit = int(input('How many profiles to scrape? '))
skip = int(input('How many profiles to skip? '))

start = '"edge_followed_by":{"count":'
end = '},"followed_by_viewer"'

fin = open('in.csv', 'r')
fout = open('out.csv', 'a')

i = -1

for line in fin:
    if i >= skip + limit:
        break

    i += 1
    
    if i <= skip or i == 0 or line is None:
        continue
    
    user = line.split(',')[1]
    url = 'https://www.instagram.com/' + user
    r = requests.get(url).text
    count = r[r.find(start)+len(start):r.rfind(end)]

    if '<head>' in count:
        count = 'UNDEFINED'

    print('#{} User {} has {} followers'.format(i, user, count))
    fout.write('{},{},{}\r\n'.format(i, url, count))
    time.sleep(1)

fin.close()
fout.close()

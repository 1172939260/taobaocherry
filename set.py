import codecs
import re
f=codecs.open('yingtao_url_new56.txt','r','utf-8')
f2=codecs.open('yingtao_url_new_all.txt','a','utf-8')
k=0
set1=set()
set2=set()
for line in f:
    k+=1
    print(line)
    line1=line.strip().split(',')
    http = re.search('https', str(line1[4]))
    # print(http)
    if (http):
          if(line1[4] not in set2):
              f2.write(line)
          set2.add(line1[4])
    else:
        id=re.findall('\d+',line1[4])[0]
        print(id)
        if(id not in set1):
              f2.write(line)
        set1.add(id)
print(len(set1)+len(set2))
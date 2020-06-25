stops = []
file_stop = open('stopwords.txt','r')
#print(file_stop.readlines())
for each in file_stop.readlines():
    if each.strip() != '':
        stops.append(each.strip())
file_stop.close()

print('原始長度', len(stops))
#print(stops)

# 加入可能誤判的ip數字 0~255
for i in range(256):
    stops.append(str(i))
print('加數字後長度', len(stops))

# 轉換成 set
stops = set(stops)
print('set長度', len(stops))

#print(stops)

# 轉回list來排序
stops = list(stops)
stops.sort()

file = open('stopwords_b.txt','w')
for each in stops:
    file.write(f'{each}\n')
file.close()
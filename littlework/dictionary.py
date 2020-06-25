import os
dic = {}
#檔案若不存在先建立空檔案
if not os.path.isfile('tmpdic'):
    print('檔案已建立')
    with open('tmpdic', 'w') as fw:
        fw.write('dictionary\n')

# 檔案內容初始化
def initdic():
    with open('tmpdic', 'w') as fw:
        fw.write('dictionary\n')

with open('tmpdic', 'r') as fr:
    # 若檔案的頭一行不是 dictionary 則重新建檔
    if fr.readline().strip() != 'dictionary':
        print('檔案毀損，已重新重檔')
        initdic()
    else:
        for line in fr.readlines():
            # 若是空行或找不到":"(就是待輸入) 則跳離for迴圈開始讓使用者輸入
            if line.find(':') == -1:
                break
            # 將存檔中所有資料讀入字典
            else:
                line = line.strip()
                aa = line.split(':')    # aa[0] = key, aa[1] = value
                if aa[0]=='' or aa[1] =='':
                    continue
                dic[aa[0]]= aa[1]

while True:
    a =input('請輸入鍵值 (結束存檔=end, 清空所有資料=clear 查看目前已存在鍵值=show 刪除已存在的鍵值=del) : ')
    if not a:
        continue
    if a == 'end':
        initdic()
        with open('tmpdic', 'a') as fw:
            for d in dic:
                fw.write(d+':'+dic[d]+'\n')
        print('結束並存檔。')
        break
    if a == 'clear':
        dic = {}
        initdic()
        print('字典已清除。')
        continue
    if a == 'show':
        if not dic:
            print('目前沒有資料！')
        else:
            for d in dic:
                print(d,':',dic[d])
        continue
    if a == 'del':
        b = input('請輸入想刪除的鍵值 ： ')
        if b in dic:
            del dic[b]
            print('該鍵值已刪除')
        else:
            print('該鍵值原本就不存在，請檢查輸入')
        continue
    if a in dic:
        print('！！已存在字典中, {} 的對應值為 ： {} '.format(a, dic[a]))
        b = input('要修改其值嗎？ (y/n)')
        if b == 'y':
            dic[a] = input('請輸入新的值 ： ')
            print('{} 的值已更新為 {}'.format(a, dic[a]))
    else:
        dic[a] = (input('不在字典中, 請輸入該鍵值來新增 : '))
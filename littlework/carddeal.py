import random

# 1~52 做樸克牌轉換
def tocard(m):
    # 用字典做轉換 要注意index +1 or -1
    trans = {i:i for i in range(1, 13)}
    trans.update({1: 'A', 11: 'J', 12: 'Q', 13: 'K'})
    suitscard = {0:'黑桃', 1:'紅心', 2:'方塊', 3:'梅花'}
    return suitscard[(m-1) // 13] + ' ' + str(trans[(m % 13)+1])

    # 不用字典只用if判斷式
    # def cardsymbol(n):
    #     if n>13: n = n%13
    #     if n == 1: return 'A'
    #     elif 1 < n < 11:return str(n)
    #     elif n == 11:return 'J'
    #     elif n == 12:return 'Q'
    #     else:return 'K'
    # if m <= 13: return '黑桃 ' + cardsymbol(m)
    # elif 13 < m <= 26: return '紅心 ' + cardsymbol(m)
    # elif 26 < m <= 39: return '方塊 ' + cardsymbol(m)
    # else: return '梅花 ' + cardsymbol(m)

# 用 random.shuffle 去把已存在的數列重排   和下面 randint 擇一
deck = list(range(1,53))        # 建一個 1~52 的list
random.shuffle(deck)            # 用 random.shuffle 去亂數排序

# 用 random.randint 去抽數字 有重覆就重抽
# deck = []
# n=0
# while n < 52:
#     x = random.randint(1, 52)
#     if x in deck:
#         continue
#     else:
#         deck.append(x)
#         n+=1

while True:         # 強迫症的讓使用者輸入不出錯
    num = input('請輸入有幾位同學 : ')
    if not num.isdigit() or int(num)>52 or int(num)<1 :
        continue
    else:
        break
num = int(num)      # 為了防呆，這裡才把 input 轉 int

everyhand_cardnums = 52 // num      # 初步每個人手上有幾張牌 不整除的下面會處理
leftcard = 52 % num         # 不整除後剩下幾張牌

last = 0        # last 變數是下面如果用切片的方法才需要
for i in range(num):
    # 切片記索引值的做法  和下面append做法擇一
    # eachhand = []
    # if leftcard > 0 :       # 如果還有餘牌
    #     eachhand = deck[last : last + everyhand_cardnums + 1]   # 第i+1位同學的手牌
    #     last = last + everyhand_cardnums + 1        # last設定至還未取用過的 deck 的 index
    #     leftcard -= 1       # 餘牌-1
    # else:                   # 如果沒有餘牌了
    #     eachhand = deck[last : last+everyhand_cardnums]     #第i+1位同學的手牌
    #     last = last + everyhand_cardnums        # last設定至還未取用過的 deck 的 index

    # 一個一個append 後, 用 pop 縮減 deck 的做法
    eachhand = []
    for j in range(everyhand_cardnums):         # 把每個人該有的手牌數給第 i+1 位同學
        eachhand.append(deck.pop(0))
    if leftcard >0:                             # 如果有餘牌 就先多給 i+1 位 一張
        eachhand.append(deck.pop(0))
        leftcard -= 1

    eachhand.sort()        # 強迫症的排序
    eachhand = list(map(tocard, eachhand))  # 用map函式把 eachhand 的每個int丟進上面定義的 tocard() 轉換成撲克牌表示
    print('第 {0:2} 位同學拿到的 {1:2} 張牌是 :  '.format(i+1, len(eachhand)), end ='')

    for card in eachhand:
        if card != eachhand[-1]:               # 如果 card 不是 eachhand 最後一個原素就不換行
            print('{:6} '.format(card),end='')
        else:                               # 是就換行
            print(card)
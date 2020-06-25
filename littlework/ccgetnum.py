#! -*- encoding:utf-8 -*-

import random
import time

# 利用 random 套件的亂數去取得不重覆的可能再進行排列
def factorial(x):       # 計算階乘
    result = 1
    while x > 0 :
        result *= x
        x -= 1
    return result

def ccgetnum(m,n):      # 算排列組合 C m 取 n
    a = factorial(m)
    b = factorial(m-n)
    c = factorial(n)
    return int(a/(b*c))

def printall(m, n):
    time.process_time()
    total_count = 0
    all_list = list(range(1,m+1))
    print('原本的數列為 {}'.format(all_list))
    sample_list = []
    x = 0
    while x < ccgetnum(m, n):
        string_sample = ''
        sample = random.sample(all_list,k=n)
        sample.sort()
        for ss in sample:
            string_sample += str(ss)
        if string_sample not in sample_list:
            sample_list.append(string_sample)
            x += 1
    sample_list.sort()
    print('可能的樣本組合(共 {} 種) : {} '.format(len(sample_list),sample_list))
    for ccc in sample_list:
        arrange_list = list(ccc)
        print('在 {} 的組合下 有 {} 種 可能 : '.format(arrange_list, factorial(len(arrange_list))))
        x = 0
        check = []
        while x < factorial(len(arrange_list)):
            random.shuffle(arrange_list)
            strings = ''
            for ss in arrange_list:
                strings+= str(ss)
            if strings not in check:
                check.append(strings)
                x += 1
        check.sort()
        for result in check:
            print('{}'.format(result), end =', ')
        total_count += len(check)
        print()

    tt = time.process_time()
    print('全部共有 {} 種可能的排列組合'.format(total_count))
    print(f'一共花了 {tt} 秒')

def main():
    m = int(input('總共有幾個數？ : '))
    n = int(input('取幾個數來排列組合？ : '))
    printall(m,n)
if __name__ == '__main__':
    main()
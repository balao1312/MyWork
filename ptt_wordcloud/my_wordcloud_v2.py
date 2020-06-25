from wordcloud import WordCloud
import jieba_fast as jieba
import numpy as np
from PIL import Image
import time

def my_wordcloud(filename):

    t1 = time.time()

    # 讀取停用字
    stopwords = [line.strip() for line in open('stopwords.txt').readlines()]
    print('停用字長度',len(stopwords))
    print('filename : ', filename)

    jieba.load_userdict('userdict.txt')

    words = []
    with open(filename, 'r') as fileread:
        for line in fileread.readlines():
            line = line.replace(' ', '')
            line = line.replace('7-11', '統一超商')
            line = line.replace('711', '統一超商')
            line = line.replace('SEVEN', '統一超商')
            line = line.replace('7-eleven', '統一超商')
            line = line.replace('小7', '統一超商')
            line = line.replace('7Eleven', '統一超商')
            line = line.replace('seven', '統一超商')
            line = line.replace('小七', '統一超商')
            cutted = jieba.cut(line,cut_all=False)
            for word in cutted:
                if word.lower() not in stopwords:
                    words.append(word.lower())
    t2 = time.time()
    print(f'分詞使用時間 {t2-t1:.4f} s')
    print(len(words))
    #words_in_string = ' '.join(words)

    word_appear_times = {}
    for i in words:
        if i not in word_appear_times:
            word_appear_times[i] = 1
        else:
            word_appear_times[i] += 1
    # print(word_appear_times)

    word_appear_times_ordered = sorted(word_appear_times.items(), key=lambda x: x[1], reverse=True)
    # top150 = word_appear_times_ordered[0:150]
    # print(top150)
    top150_word = ' '.join([x[0] for x in word_appear_times_ordered[0:150]])
    #print(top150_word)


    cloud_mask = np.array(Image.open("cloud_mask.png"))
    wc = WordCloud(repeat=False, include_numbers=False, max_words=150, min_word_length=2,
                   colormap='RdYlGn', mask=cloud_mask, background_color="black", scale=4,
                   font_path='/System/Library/Fonts/PingFang.ttc')
    wc.generate(top150_word)
    wc.to_file(f'{filename[:-4]}.jpg')

    t3 = time.time()
    print(f'畫圖使用時間 {t3-t2:.4f} s')

def main():
    my_wordcloud('cvs_100.txt')

if __name__ == '__main__':
    main()
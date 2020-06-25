from wordcloud import WordCloud
import jieba_fast as jieba
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import time

def my_wordcloud(filename):

    punct = str.maketrans("!.,:;-?※></()=，、。／[]《》", "                      ")
    plt.rcParams['font.sans-serif'] = 'PingFang TC'  # 設字型

    # 讀取停用字
    stop = [line.strip() for line in open('stopwords.txt').readlines()]

    print('停用字長度',len(stop))
    all_segs = []
    with open(filename) as file:
        for line in file:
            #print(line)
            line = line.translate(punct)
            segs = line.split(' ')
            for anyy in segs:
                if len(anyy.strip()) > 2:
                    all_segs.append(anyy.strip())
    #print(all_segs)
    print(len(all_segs))

    jieba.load_userdict('userdict.txt')

    word_appear_times = {}
    for i in all_segs:
        #print('-'*30)
        #print(i,':',list(jieba.cut(i,cut_all=False)))
        for anyy in list(jieba.cut(i,cut_all=True)):
            anyy = anyy.lower()
            if anyy not in stop and len(anyy.strip()) > 1:
                #print(anyy)
                if anyy not in word_appear_times:
                    word_appear_times[anyy] = 1
                else:
                    word_appear_times[anyy] += 1
            else:
                continue
        #print('-'*30,'\n')
        #time.sleep(3)
    #print(word_appear_times)

    word_appear_times_ordered = sorted(word_appear_times.items(), key=lambda x:x[1], reverse=True)
    top150 = word_appear_times_ordered[0:150]
    #print(top150)
    top150_word = ' '.join([x[0] for x in top150])
    print(top150_word)

    cloud_mask = np.array(Image.open("cloud_mask.png"))
    wc = WordCloud(colormap='RdYlGn', mask=cloud_mask, max_words=150, background_color="black",scale=4, font_path='/System/Library/Fonts/PingFang.ttc')  # 產生文字雲
    wc.generate(top150_word)
    wc.to_file(f'{filename[:-4]}.jpg')
    # plt.imshow(wc)  # 要繪製的圖像
    # plt.axis("off")  # 不顯示座標尺寸
    # plt.margins(0, 0)
    # plt.savefig("word_cloud.png",dpi=800)
    # plt.close()

def main():
    my_wordcloud('cvs_100.txt')

if __name__ == '__main__':
    main()
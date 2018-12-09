# -*- coding:utf-8 -*-
# @Time     :2018/12/8 15:06
import itchat
import matplotlib.pyplot as plt
import os
from wordcloud import WordCloud, ImageColorGenerator
import PIL.Image as Image
import jieba
import re
from collections import Counter
import numpy as np
signature = []
itchat.auto_login(hotReload=True)
friends = itchat.get_friends(update=True)
male = female = other = 0
print(friends[0])
for i in friends[1:]:
    name = i["NickName"]
    sex = i["Sex"]
    signature.append(i["Signature"])
    if sex == 1:
        male += 1
    elif sex == 2:
        female += 1
    else:
        other += 1
total_friends = len(friends)
print("男性朋友：%.2f%%" % (male / total_friends * 100), male)
print("女性朋友：%.2f%%" % (female / total_friends * 100), female)
print("其他朋友：%.2f%%" % (other / total_friends * 100), other)
plt.figure(figsize=(6, 6), dpi=100)
se = ["男性", '女性', '其他']
x = range(3)
y = [male, female, other]
# plt.bar(x,y,width=0.5,color=("b",'r','g'))
# plt.xticks(x,se)
# plt.grid(linestyle="--",alpha=0.5)
# plt.title("微信好友性别对比")
# plt.figure(figsize=(6, 6), dpi=100)
# plt.pie(y, labels=se, autopct="%1.2f%%", colors=('r', 'b', 'g'))
# plt.title("微信好友性别对比")
# plt.legend()
# plt.show()
jieba_str = []
for s in signature:
    s = re.sub("<span[\d\s].+?</span>", "", s.strip())
    jieba_str.append(s)
    # print(s)
    jieba.load_userdict("user_dict")

jieba_all = "".join(jieba_str)
word_list = jieba.cut(jieba_all)
# 结巴分词 cut后出来的词是生成器
# jieba_word = re.sub(' ','','，'.join(jieba.cut(s)))
# jieba_str.append(jieba_word)
my_word_list = " ".join(word_list)
d = os.path.dirname(__file__)
duolaameng = np.array(Image.open(os.path.join(d,"duolaameng.jpeg")))
# print(word_list)
my_wordcloud = WordCloud(
    background_color="white",
    max_words=200,
    mask=duolaameng,
    max_font_size=40,
    random_state=42,
    font_path='/Users/anbang/Library/Fonts/simhei.ttf'
).generate(my_word_list)

image_color = ImageColorGenerator(duolaameng)
plt.imshow(my_wordcloud.recolor(color_func=image_color))
plt.imshow(my_wordcloud)
plt.savefig("./temp.jpg",dpi=600)
plt.axis("off")
plt.show()
# most_word = Counter(word_list).most_common(100)
# print(most_word)

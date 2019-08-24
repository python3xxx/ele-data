

from random import randint
from matplotlib import pyplot as plt
from wordcloud import WordCloud

"""
菜品的词云分析
"""

def random_color(word=None, font_size=None, position=None,  orientation=None, font_path=None, random_state=None):

    """Random Color func"""
    r = randint(30, 255)
    g = randint(30, 180)
    b = int(100.0 * float(randint(60, 120)) / 255.0)
    return "rgb({:.0f}, {:.0f}, {:.0f})".format(r, g, b)


content = open('foods_name.txt', encoding='utf-8').read()


wordcloud = WordCloud(background_color="white",
               width=1000,
               height=600,
               max_font_size=50,
               font_path='/System/Library/Fonts/PingFang.ttc', # 需要根据实际操作系统更换路径
               color_func=random_color).generate(content)
plt.imshow(wordcloud)
plt.axis("off")
plt.savefig('ele_wordcloud.png', format='png', dpi=200)
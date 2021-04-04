import jieba
from wordcloud import WordCloud
from db.mi10_models import Comment
from conf.settings import FONT_DIR, IMAGE_DIR, DATA_ANALYZE_DIR


# 所有评论的词云
def get_all_comments_wordcloud():
    content = ''
    for comment in Comment.select():
        content += comment.content + '\n'
    stopwords = set()
    with open(DATA_ANALYZE_DIR + '/custom_cn_stopwords.txt', 'r', encoding='UTF-8') as f:
        for line in f.readlines():
            stopwords.add(line.replace('\n', ''))
    wordcloud: WordCloud = WordCloud(
        font_path=FONT_DIR + '/NotoSansCJKsc-Regular.otf',
        width=6000,
        height=2000,
        stopwords=stopwords,
        background_color='white',
        collocations=False
    )
    # 使用jieba分词的默认精确模式
    wordcloud.generate(' '.join(jieba.lcut(content)))
    wordcloud.to_file('mi10_all_comments_wordcloud.png')


if __name__ == '__main__':
    get_all_comments_wordcloud()

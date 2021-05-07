import jieba
from wordcloud import WordCloud
from db.mi10_models import Comment
from conf.settings import FONT_DIR, IMAGE_DIR
from data_analyze.utils import get_stopwords_set


# 所有评论的词云
def get_all_comments_wordcloud():
    content = ''
    for comment in Comment.select():
        content += comment.content + '\n'
    wordcloud = WordCloud(
        font_path=FONT_DIR + '/NotoSansCJKsc-Regular.otf',
        width=7200,
        height=2400,
        stopwords=get_stopwords_set(),
        background_color='white',
        collocations=False
    )
    # 使用jieba分词的默认精确模式
    wordcloud.generate(' '.join(jieba.lcut(content)))
    wordcloud.to_file(IMAGE_DIR + '/mi10_all_comments_wordcloud.png')


# 追评的词云
def get_after_comments_wordcloud():
    content = ''
    for comment in Comment.select().where(Comment.after_content.is_null(False)):
        content += comment.after_content + '\n'
    wordcloud = WordCloud(
        font_path=FONT_DIR + '/NotoSansCJKsc-Regular.otf',
        width=4000,
        height=2400,
        stopwords=get_stopwords_set(),
        background_color='white',
        collocations=False
    )
    # 使用jieba分词的默认精确模式
    wordcloud.generate(' '.join(jieba.lcut(content)))
    wordcloud.to_file(IMAGE_DIR + '/mi10_after_comments_wordcloud.png')


# iOS转化用户评论的词云
def get_ios_comments_wordcloud():
    content = ''
    for comment in Comment.select().where(Comment.user_device == 'iOS'):
        content += comment.content + '\n'
        if comment.after_content is not None:
            content += comment.after_content + '\n'
    wordcloud = WordCloud(
        font_path=FONT_DIR + '/NotoSansCJKsc-Regular.otf',
        width=4000,
        height=2400,
        stopwords=get_stopwords_set(),
        background_color='white',
        collocations=False
    )
    # 使用jieba分词的默认精确模式
    wordcloud.generate(' '.join(jieba.lcut(content)))
    wordcloud.to_file(IMAGE_DIR + '/mi10_ios_comments_wordcloud.png')


# 安卓留存用户评论词云
def get_android_comments_wordcloud():
    content = ''
    for comment in Comment.select().where(Comment.user_device == 'Android'):
        content += comment.content + '\n'
        if comment.after_content is not None:
            content += comment.after_content + '\n'
    wordcloud = WordCloud(
        font_path=FONT_DIR + '/NotoSansCJKsc-Regular.otf',
        width=4000,
        height=2400,
        stopwords=get_stopwords_set(),
        background_color='white',
        collocations=False
    )
    # 使用jieba分词的默认精确模式
    wordcloud.generate(' '.join(jieba.lcut(content)))
    wordcloud.to_file(IMAGE_DIR + '/mi10_android_comments_wordcloud.png')


# 提取评分五星以下评论的高频词
def get_non_five_star_comments_wordcloud():
    content = ''
    for comment in Comment.select().where((Comment.star.in_([1, 2, 3, 4]))):
        content += comment.content + '\n'
        if comment.after_content is not None:
            content += comment.after_content + '\n'
    wordcloud = WordCloud(
        font_path=FONT_DIR + '/NotoSansCJKsc-Regular.otf',
        width=4000,
        height=2400,
        stopwords=get_stopwords_set(),
        background_color='white',
        collocations=False
    )
    # 使用jieba分词的默认精确模式
    wordcloud.generate(' '.join(jieba.lcut(content)))
    wordcloud.to_file(IMAGE_DIR + '/mi10_non_five_star_comments_wordcloud.png')


if __name__ == '__main__':
    get_all_comments_wordcloud()
    get_after_comments_wordcloud()
    get_ios_comments_wordcloud()
    get_android_comments_wordcloud()
    get_non_five_star_comments_wordcloud()

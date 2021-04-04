from conf.settings import DATA_ANALYZE_DIR


def calculate_percentage(total: int, part: int) -> str:
    return format((part / total) * 100, '.1f')


def get_stopwords_set() -> set:
    stopwords = set()
    with open(DATA_ANALYZE_DIR + '/custom_cn_stopwords.txt', 'r', encoding='UTF-8') as f:
        for line in f.readlines():
            stopwords.add(line.replace('\n', ''))
    return stopwords

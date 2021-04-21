from conf.settings import DATA_ANALYZE_DIR


def get_stopwords_set() -> set:
    stopwords = set()
    with open(DATA_ANALYZE_DIR + '/custom_cn_stopwords.txt', 'r', encoding='UTF-8') as f:
        for line in f.readlines():
            stopwords.add(line.replace('\n', ''))
    return stopwords


# 计算百分比并返回保留一位小数的数值字符串
def calculate_percentage(total: int, part: int) -> str:
    return format((part / total) * 100, '.1f')


# 计算平均数
def calculate_average(data_list: list, output_str: bool = False):
    result = sum(data_list) / len(data_list)
    if output_str is False:
        return result
    else:
        return format(result, '.1f')


# 计算中位数
def calculate_median(data_list: list, output_str: bool = False):
    data_ls = sorted(data_list)
    if len(data_ls) % 2 == 1:
        result = data_ls[int((len(data_ls) - 1) / 2)]
    else:
        result = (data_ls[int(len(data_ls) / 2 - 1)] + data_ls[int(len(data_ls) / 2)]) / 2
    if output_str is False:
        return result
    else:
        return str(result)

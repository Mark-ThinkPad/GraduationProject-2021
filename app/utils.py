# 对较大的数据四舍五入到以万为单位的整数
def rounding_w(number: int) -> int:
    return int((number / 10000) + 0.5)

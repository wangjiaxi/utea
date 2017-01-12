
def parse_count(the_count):
    """
    :param the_count: such as 1.3万, 123213
    :type the_count: string
    :return: int
    """
    if "万" in the_count:
        return float(the_count.rsplit("万")[0]) * 10000
    return int(the_count)


def parse_datetime(datetime_sting):
    return
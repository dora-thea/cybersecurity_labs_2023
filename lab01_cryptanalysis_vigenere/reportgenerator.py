from matplotlib import pyplot as plt


def count_percent(keyword, found_keyword):
    length = len(keyword)
    found_len = len(found_keyword)
    count = [
        (i < found_len and found_keyword[i] == el)
        for i, el in enumerate(keyword)
    ].count(True)
    return int(100 * count / length)


class ReportGenerator:

    def __init__(self, report):
        self.report = report

    def print_table_head(self, title, columns):
        self.report.write(f'## {title}\n')
        self.print_table_row(*columns)
        self.print_table_row(*['---'] * len(columns))

    def print_table_row(self, *args):
        self.report.write('|' + '|'.join(map(str, args)) + '|\n')

    def print_test(self, text_len, keyword, found_keyword):
        percent = count_percent(keyword, found_keyword)
        self.print_table_row(text_len, keyword, len(keyword), found_keyword, len(found_keyword), '{}%'.format(percent))
        return percent

    def print_test_kasiski(self, text_len, keyword_lst, found_keyword_lst):
        row = []
        for i in range(len(keyword_lst)):
            if len(found_keyword_lst[i]) == len(keyword_lst[i]):
                row.append("**+**")
            else:
                row.append("")
        self.print_table_row(text_len, *row)

    def print_test_matching(self, text_len, keyword_lst, found_keyword_lst):
        percent = []
        for i in range(len(keyword_lst)):
            if found_keyword_lst[i] == "":
                percent.append("Fail")
            else:
                p = count_percent(keyword_lst[i], found_keyword_lst[i])
                if p >= 80:
                    percent.append(f"**{p}**")
                else:
                    percent.append(p)
        self.print_table_row(text_len, *percent)
        return percent

    def add_plot_to_report(self, x, y, title, x_label):
        plt.clf()
        plt.plot(x, y)
        plt.ylabel('Percents, %')
        plt.xlabel(f'{x_label} length, symbols')
        png_path = f'report/images/{title}.png'
        plt.savefig(png_path)
        self.report.write(f'\n![{title}](./images/{title}.png)\n')

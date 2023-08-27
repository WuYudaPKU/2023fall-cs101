import pandas as pd

df = pd.read_excel('studentListInCourse-20230827.xls')
df_schools = df['所属院系'].value_counts().reset_index()
df_schools.columns = ['所属院系', 'Count']
#print(df_schools)

fPlot = False
if fPlot:
    import itertools
    #print(*df_schools.loc[:, ['所属院系']].values)
    #print(*df_schools.loc[:, ['Count']].values)
    labels = list(itertools.chain(*df_schools.loc[:, ['所属院系']].values))
    sizes = list(itertools.chain(*df_schools.loc[:, ['Count']].values))

    import matplotlib.pyplot as plt
    plt.rcParams['font.family'] = ['Heiti TC']

    fig, ax = plt.subplots(figsize=(15, 15))
    ax.pie(sizes, labels=labels, autopct='%1.1f%%')

    plt.title(label="2023/8/24 选课院系分布",
              fontsize=20,
              loc="left",
              color="green")
    plt.show()
    import sys; sys.exit(0)

# 按照年级、院系和是否留学生排序
df.sort_values(['学号', '所属院系', '学生类别'], inplace=True)

# 初始化助教列表，这里以0到m-1的数字代表每位助教
TAs = ["张哲瑞", "张以宁", "彭亦男", "涂程颖", "陈威宇"]
m = len(TAs)
assistants = list(range(m))

# 为每个助教创建空字典，存储其管理的学生信息
assistant_students = {assistant: [] for assistant in assistants}

# 按排序后的顺序，将学生平均分配给助教
for i, student in enumerate(df.itertuples()):
    assistant_students[i%m].append((student.学号, student.姓名, student.所属院系, student.学生类别))

with pd.ExcelWriter("assistant_students.xlsx", engine='xlsxwriter') as writer:
    for assistant, students in assistant_students.items():
        #print(f'助教 {TAs[assistant]} 管理的学生：')
        #for student in students:
        #    print('\t {}，{}，{}，{}'.format(*student))

        df = pd.DataFrame(data=students, columns=['学号', '姓名', '所属院系', '学生类别'])
        df.to_excel(writer, sheet_name=TAs[assistant], index=False)

        # auto-adjust-excel-column-widths
        # ref: https://stackoverflow.com/questions/17326973/is-there-a-way-to-auto-adjust-excel-column-widths-with-pandas-excelwriter
        # If you get AttributeError: 'Worksheet' object has no attribute 'set_column', you may be missing XlsxWriter and
        # pandas is falling back on openpyxl. pip install XlsxWriter should solve it
        for idx, col in enumerate(df):  # loop through all columns
            series = df[col]
            max_len = max((
                series.astype(str).map(len).max(),  # len of largest item
                len(str(series.name))  # len of column name/header
                )) + 8  # adding a little extra space
            writer.sheets[TAs[assistant]].set_column(idx, idx, max_len)  # set column width


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# 为数据进行填充专业名称
def rebuild(df, name):
    cs = pd.DataFrame(df, columns=["政治理论", "外国语", "业务课1", "业务课2", "总分"])
    # cs.insert(2,'专业名称', pd.Series())
    # cs.fillna(name, inplace = True)
    cs = cs.reindex(columns=["专业名称", "政治理论", "外国语", "业务课1", "业务课2", "总分"], fill_value=name)
    return cs


# 画频率曲线图
def draw(name):
    plt.figure(figsize=(15, 6))
    plt.subplot(121).set_title('计算机科学与技术',size = 13)
    sns.kdeplot(cs_clear.loc[cs_clear["专业名称"] == "2018计算机科学与技术"][name].rename("2018" + name),
                color="b", shade=True)
    sns.kdeplot(cs_clear.loc[cs_clear["专业名称"] == "2019计算机科学与技术"][name].rename("2019" + name),
                color="g", shade=True)
    plt.subplot(122).set_title('计算机技术',size = 13)
    sns.kdeplot(cs_clear.loc[cs_clear["专业名称"] == "2018计算机技术"][name].rename("2018" + name),
                color="b", shade=True)
    sns.kdeplot(cs_clear.loc[cs_clear["专业名称"] == "2019计算机技术"][name].rename("2019" + name),
                color="g", shade=True)
    plt.tight_layout()
    plt.show()


# 进行数值计算，计算各成绩方差，标准差等信息
def statistics(name):
    df = cs_clear.loc[cs_clear["专业名称"] == name][["政治理论", "外国语", "业务课1", "业务课2","总分"]]
    sta = pd.DataFrame([df.std(),df.mean(), df.median(), df.max()])
    return sta.T.rename({0: name + "标准差", 1: name + "平均分", 2: name + "中位数", 3: name + "最高分"},
                         axis='columns')


# 统计过线的考生数
def over_line(name, line1, line2, line3):
    df = cs_clear[(cs_clear["专业名称"] == name)]
    num1 = len(df[df["政治理论"] >= line1])
    num2 = len(df[df["外国语"] >= line1])
    num3 = len(df[df["业务课1"] >= line2])
    num4 = len(df[df["业务课2"] >= line2])
    num_all = len(df[(df["政治理论"] >= line1) & (df["外国语"] >= line1) & (df["业务课1"] >= line2)
                     & (df["业务课2"] >= line2) & (df["总分"] >= line3)])
    num = np.array([num1, num2, num3, num4, num_all])
    num_rate = num / cs_count[name]
    over = pd.DataFrame([num,num_rate])
    over.rename({0: "政治理论", 1: "外国语", 2: "业务课1", 3: "业务课2", 4: "总分"}, axis='columns',inplace=True)
    over.rename({0: name+"过线人数", 1: name+"过线率"}, axis='index',inplace=True)
    return over.T


# 统计进复试和录取人数变化
def receive(name, line1, line2, line3, rec_num):
    df = cs_clear[(cs_clear["专业名称"] == name)]
    chu_num = len(df[(df["政治理论"] >= line1) & (df["外国语"] >= line1) & (df["业务课1"] >= line2)
                     & (df["业务课2"] >= line2) & (df["总分"] >= line3)])
    num_rate_chu = chu_num / cs_count[name]
    num_rate_fu =  rec_num / chu_num
    num_rate_bao = rec_num / cs_count[name]
    rec = pd.DataFrame([line3, chu_num, rec_num, cs_count[name], num_rate_chu, num_rate_fu, num_rate_bao])
    rec.rename({0: "录取分数线", 1: "复试人数", 2: "录取人数", 3: "报考人数", 4: "复录比", 5: "拟录比", 6: "报录比"}, axis='index',inplace=True)
    rec.rename({0: name}, axis='columns',inplace=True)
    return rec


# 读取近两年北京科技大学考研成绩表,以第一栏作为表头
data2019 = pd.read_excel("your path/20190215140202408200.xls", header=1)
data2018 = pd.read_excel("your path/20180203165211753910.xls", header=1)
# 删除考生编号和姓名等敏感信息
data2018.drop(['考生编号', '姓名'], axis=1, inplace=True)
data2019.drop(['考生编号', '姓名'], axis=1, inplace=True)
# 读取专硕成绩
data2018_jishu = data2018[(data2018["报考学院代码"] == 60) & (data2018["报考专业代码"] == "085211") &
                          (data2018['学习方式'] == "全日制") & (data2018['考试方式'] == "全国统考") &
                          (data2018['专项计划'] == "无")]

data2019_jishu = data2019[(data2019["学院代码"] == 60) & (data2019["学院名称"] == "计算机与通信工程学院") &
                          (data2019["专业代码"] == "085211") & (data2019["专业名称"] == "计算机技术") &
                          (data2019['学习方式'] == "全日制") & (data2019['考试方式'] == "全国统考") &
                          (data2019['专项计划'] == "无")]
# 读取学硕成绩
data2018_kexue = data2018[(data2018["报考学院代码"] == 60) & (data2018["报考专业代码"] == "081200") &
                          (data2018['学习方式'] == "全日制") & (data2018['考试方式'] == "全国统考") &
                          (data2018['专项计划'] == "无")]
data2019_kexue = data2019[(data2019["学院代码"] == 60) & (data2019["学院名称"] == "计算机与通信工程学院") &
                          (data2019["专业代码"] == "081200") & (data2019["专业名称"] == "计算机科学与技术") &
                          (data2019['学习方式'] == "全日制") & (data2019['考试方式'] == "全国统考") &
                          (data2019['专项计划'] == "无")]

# 将两年的计算机专硕和学硕成绩合在一起，并打标签
cs = pd.concat([rebuild(data2018_kexue, "2018计算机科学与技术"),rebuild(data2018_jishu, "2018计算机技术"),
                rebuild(data2019_kexue, "2019计算机科学与技术"), rebuild(data2019_jishu, "2019计算机技术"), ], axis=0)

# 重置索引，并把之前的索引删去
cs.reset_index(inplace=True,drop=True)

# 清洗数据，去除缺考，作弊的数据
cs_count = cs.groupby(['专业名称']).size()
cs_clear = cs[~(cs["外国语"] == "缺考") & ~(cs["政治理论"] == "缺考") & ~(cs["业务课1"] == "缺考") &
              ~(cs["业务课2"] == "缺考") & ~(cs["政治理论"] == "作弊")]
# 聚合两年学硕专硕考生人数
cs_clear_count = cs_clear.groupby(['专业名称']).size()
count_column = ["2018", "2019"]
count_columnL = ["总报考人数", "计算机科学与技术人数", "计算机技术人数", "计算机科学与技术缺考人数", "计算机技术缺考人数"]
dict_table = {"总报考人数": [len(data2018),len(data2019)],
              "计算机科学与技术报考人数": [cs_count["2018计算机科学与技术"], cs_count["2019计算机科学与技术"]],
              "计算机技术报考人数": [cs_count["2018计算机技术"], cs_count["2019计算机技术"]],
              "计算机科学与技术成绩有效人数": [cs_clear_count["2018计算机科学与技术"], cs_clear_count["2019计算机科学与技术"]],
              "计算机技术成绩有效人数": [cs_clear_count["2018计算机技术"], cs_clear_count["2019计算机技术"]]}

growth_count = pd.DataFrame.from_dict(dict_table, orient='index', columns=count_column)


growth_count = growth_count.loc[["总报考人数","计算机科学与技术报考人数", "计算机技术报考人数", "计算机科学与技术成绩有效人数",
                                "计算机技术成绩有效人数"]]

# 将增长率以百分比形式显示
growth_count["增长率"] = ((growth_count["2019"] - growth_count["2018"])/growth_count["2018"]).apply(lambda x: '%.2f%%' %
                                                                                                           (x*100))

# 画图出各科成绩频率分布图
'''
draw("外国语")
draw("业务课1")
draw("业务课2")
draw("总分")
'''

# 度成绩进行数值分析
'''
s1 = statistics("2018计算机科学与技术")
s1.columns = ['学硕标准差','学硕平均分','学硕中位数','学硕最高分']
s2 = statistics("2019计算机科学与技术")
s2.columns = ['学硕标准差','学硕平均分','学硕中位数','学硕最高分']
print(s2-s1)
'''

# 统计过线情况
'''
over_line_kexue = pd.concat([over_line("2018计算机科学与技术", 34, 51, 260),over_line("2019计算机科学与技术", 39, 59, 270)],axis=1)
over_line_jishu = pd.concat([over_line("2018计算机技术", 34, 51, 260),over_line("2019计算机技术", 39, 59, 270)],axis=1)    
over_line_kexue["过线率增长率"] =  ((over_line_kexue["2019计算机科学与技术"] - over_line_kexue["2018计算机科学与技术"])/over_line_kexue["2018计算机科学与技术"]).apply(lambda x: '%.2f%%' % (x*100))
over_line_jishu["过线率增长率"] =  ((over_line_jishu["2019计算机技术过线率"] - over_line_jishu["2018计算机技术过线率"])/over_line_jishu["2018计算机技术过线率"]).apply(lambda x: '%.2f%%' % (x*100))
'''

# 统计复录比，报录比等录取情况
'''
formater="{0:.02f}".format
rec = pd.concat([receive("2018计算机科学与技术", 34, 51, 318, 23),receive("2019计算机科学与技术", 39, 59, 340,29),
           receive("2018计算机技术", 34, 51, 314, 47),receive("2019计算机技术", 34, 51, 361,54)],axis=1)
rec["计算机科学与技术增长率"] = ((rec["2019计算机科学与技术"] - rec["2018计算机科学与技术"])/rec["2018计算机科学与技术"])
rec["计算机技术增长率"] = ((rec["2019计算机技术"] - rec["2018计算机技术"])/rec["2018计算机技术"])
rec.applymap(formater)
'''


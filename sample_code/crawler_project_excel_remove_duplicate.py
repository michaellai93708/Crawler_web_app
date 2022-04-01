import pandas as pd
import os
frame = pd.read_excel('/Users/michael/Downloads/output_smart_transit.xlsx')
data = pd.DataFrame(frame)
data.drop_duplicates(['原文地址', '信息标题', '招标编号'], keep='first', inplace=True)
# drop_duplicates用法：subset=‘需要去重复的列名’,keep=‘遇到重复的时保留第一个还是保留最后一个’,inplace=‘去除重复项，还是保留重复项的副本’
data.to_excel('out.xlsx')
print('合并完成')
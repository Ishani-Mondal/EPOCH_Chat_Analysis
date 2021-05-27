# Import libs
import pandas as pd
from scipy import stats

# Read the excel sheets
df1 = pd.read_excel("Group1_Annotated.xlsx")
df1['Group'] = '1'
df2 = pd.read_excel("Group2_Annotated.xlsx")
df2['Group'] = '2'
print(df1.shape, df2.shape)
df1

df = pd.concat([df1, df2])
print(df.shape)

# Combine same users together
df['User'] = df['User'].replace(to_replace="Vijana-SMART 1", value="Vijana-SMART")
df['User'] = df['User'].replace(to_replace="Vijana-SMART 2", value="Vijana-SMART")
df['User'] = df['User'].replace(to_replace="Vijana-SMART 2 ", value="Vijana-SMART")
df['User'] = df['User'].replace(to_replace="Vijana-SMART 2:", value="Vijana-SMART")
df['User'] = df['User'].replace(to_replace="Vijana-SMART 2: ", value="Vijana-SMART")
df['User'] = df['User'].replace(to_replace="Vijana-SMART 2: ", value="Vijana-SMART")
df['User'] = df['User'].replace(to_replace="PTXXXX: ", value="PTXXXX")
df['User'].value_counts()

# Removing rows with null values
df.dropna(subset = ["OriginalMessage", "Sentiment", "Language"], inplace=True)
df.reset_index(inplace = True)
import ast

user_lang_Eng={}
user_lang_Sw={}

for index, row in df.iterrows():
    try:
        if(len(eval(row['Language'])['English'])>0 and len(eval(row['Language'])['Swahili'])==0 and len(eval(row['Language'])['Sheng'])==0 and len(eval(row['Language'])['Code-mixed word'])==0 and len(eval(row['Language'])['Other'])==0):
            user_lang_Eng[row['User']]=[]
        if(len(eval(row['Language'])['English'])==0 and len(eval(row['Language'])['Swahili'])>0 and len(eval(row['Language'])['Sheng'])==0 and len(eval(row['Language'])['Code-mixed word'])==0 and len(eval(row['Language'])['Other'])==0):
            user_lang_Sw[row['User']]=[]
    except:
        pass


for index, row in df.iterrows():
    try:
        if(len(eval(row['Language'])['English'])>0 and len(eval(row['Language'])['Swahili'])==0 and len(eval(row['Language'])['Sheng'])==0 and len(eval(row['Language'])['Code-mixed word'])==0 and len(eval(row['Language'])['Other'])==0):
            user_lang_Eng[row['User']].append(row['Sentiment'])
        if(len(eval(row['Language'])['English'])==0 and len(eval(row['Language'])['Swahili'])>0 and len(eval(row['Language'])['Sheng'])==0 and len(eval(row['Language'])['Code-mixed word'])==0 and len(eval(row['Language'])['Other'])==0):
            user_lang_Sw[row['User']].append(row['Sentiment'])
    except:
        pass


active_users={}
for index, row in df.iterrows():
    active_users[row['User']]=[]

for index, row in df.iterrows():
    active_users[row['User']].append(row['OriginalMessage'])

total={}
for user, count in active_users.items():
    #print(user, len(count))
    total[user]=len(count)

import operator
sorted_d = dict( sorted(total.items(), key=operator.itemgetter(1),reverse=True))
print('Dictionary in descending order by value : ',sorted_d.keys())

sorted_active_users=list(sorted_d.keys())[0:10]

en=[]
sw=[]
f1=open('Frequency_user_Negative_sentiment.txt','w')
for key1, val in user_lang_Eng.items():
    for key2, val2 in user_lang_Sw.items():
        if(key1==key2):
            if(key1 in sorted_active_users):
                if(user_lang_Eng[key1].count("[('N',)]")/len(user_lang_Eng[key1])>0 or user_lang_Sw[key1].count("[('N',)]")/len(user_lang_Sw[key1])>0):
                    en.append(user_lang_Eng[key1].count("[('N',)]")/len(user_lang_Eng[key1]))
                    sw.append(user_lang_Sw[key1].count("[('N',)]")/len(user_lang_Sw[key1]))
                f1.write(str(key1)+"\t"+ str(user_lang_Eng[key1].count("[('N',)]")/len(user_lang_Eng[key1]))+"\t"+str(user_lang_Sw[key1].count("[('N',)]")/len(user_lang_Sw[key1]))+"\t"+str(len(active_users[key1]))+"\n")

from scipy import stats
print(stats.ttest_ind(en, sw))
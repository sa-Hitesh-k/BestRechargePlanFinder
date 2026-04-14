from FetchingResponse import loaded_json
import pandas as pd 
import numpy as np
from glom import glom, Flatten


def flatten(lst):
    result = []
    for item in lst:
        if isinstance(item, list):
            result.extend(flatten(item))
        else:
            result.append(item)
    return result

spec_rate='planCategories.*.subCategories.*.plans.*.amount'
unflat_rates=glom(loaded_json,spec_rate)
# print(unflat_rates)
# print(len(unflat_rates))
flattened_rates=[item for row in unflat_rates for item in row]
# print(flattened_rates)
# print(len(flattened_rates))

# all_price_data={"price":flattened_rates}
# df1=pd.DataFrame(data=all_price_data)
# print(df1)
spec_Cat='planCategories.*.type'
list_cat=glom(loaded_json,spec_Cat)
# print(list_cat)
all_price_data={"price":unflat_rates,"category":list_cat}
# print(all_price_data)
df1=pd.DataFrame(data=all_price_data)
# print('df1\n',df1)
df_exploded1=df1.explode("price")
df_prices=df_exploded1.explode("price",ignore_index=True)
df_prices.insert(0,"id",np.arange(0,len(df_prices)).tolist())
# print(df_prices)
ipcdict=df_prices.to_dict(orient='index')
# print('before')
# print(np.arange(0,191))
# print('after')
# print(df_prices)
# print(df1.explode("price",ignore_index=True))

# ->getting details :[ {header :" ", value;" "}]
#getting BENEFITS 
spec_benefits='planCategories.*.subCategories.*.plans.*.misc.details'
#we get dictionaries nested in list 4 times
total_req=glom(loaded_json,spec_benefits)
# print("total_req: \n")
# print(total_req,"\n",len(total_req))
one_list={}
count=0
spec_benefits='planCategories.*.subCategories.*.plans.*.misc.subscriptions.*.title'
ottlist=glom(loaded_json,spec_benefits)
# print("ottlist:\n",ottlist)
# flatott=Flatten(ottlist)
# for row in ottlist :
#     for item in row:
#         print(item)
# flatott=[item for row in ottlist for item in row if len(item)!=0]
# flatott=[item for row in flatott for item in row if  len(item)!=0]
# flatottfinal=[]
# for row in flatott:
#     for item in row:
#         if len(item)!=0:
#             print(item)
#             flatottfinal.append(item)
#     if len(row)==0:
#         print(row)
#         flatottfinal.append(row)
# print("\n",flatottfinal,"\n",len(flatottfinal))
flatott=[]
dict_one_list={}
for i in range(0,len(loaded_json['planCategories'])):
    for j in range(0,len(loaded_json['planCategories'][i]['subCategories'])):
        for k in range(0,len(loaded_json['planCategories'][i]['subCategories'][j]['plans'])):
            #we get a proper one list containing dictionaries numbered . It is in "header":"Benefit Name" , "value":"Benefit Value"
            if len(ottlist[i][j])==0:
                flatott.append(ottlist[i][j])
                total_req[i][j][k].append({'header':'Subscriptions','value':ottlist[i][j]})
            else:
                flatott.append(ottlist[i][j][k])
                total_req[i][j][k].append({'header':'Subscriptions','value':ottlist[i][j][k]})

            one_list[count]=total_req[i][j][k]
            count+=1

# print("one list=\n",one_list,"\n\n")
iterateing=0
one_pack=[]
final_dict={}
for i in one_list:
    one_pack.append(ipcdict[i])
    for j in range(len(one_list[i])):
        proper_one_list={}
        proper_one_list[one_list[i][j]['header']]=one_list[i][j]['value']
        one_pack.append(proper_one_list)
    #Here we get a dictionary containing lists(packs)
    final_dict[iterateing]=one_pack
    one_pack=[]
    iterateing+=1
# print("final dict=",final_dict)
# df_finaldict=pd.DataFrame(final_dict)
# print(df_finaldict)
Benefit_Name=[]
Benefit_Value=[]
for i in final_dict:
    mergeddict_i={}
    for j in final_dict[i]:
        mergeddict_i=mergeddict_i | j

    Benefit_Name.append(list(mergeddict_i.keys()))
    Benefit_Value.append(list(mergeddict_i.values()))

all_Benefits_data={"id":np.arange(0,len(Benefit_Name)).tolist(), "benefitname":Benefit_Name,"benefitvalue":Benefit_Value}
df2=pd.DataFrame(data=all_Benefits_data)
# print(df2)
df2=df2.explode(["benefitname","benefitvalue"],ignore_index=True)
dftest=df2.explode(["benefitvalue"],ignore_index=True)
# print(dftest.head(30))
# print(df2)
# print("\n",flatott,"\n",len(flatott))
dfott=pd.DataFrame({"sub_id":np.arange(0,len(flatott)).tolist(), "subval":flatott})
# print(dfott)
# dfott.insert(0,"subscription_id",np.arange(0,len(dfott)).tolist())
# print(dfott)
# print(df2.loc[df2['Plan Id']==183])
# print(len(df2))
#-> print(df2.columns)

df2.insert(0,"dfid",np.arange(0,len(df2)))
# print(df2)

# df2dict=df2.to_dict(orient="records")
# # print(df2dict)

uniqueottlist=pd.Series(flatten(flatott)).unique()
# print("uniqueottlist\n",list(uniqueottlist),len(list(uniqueottlist)))
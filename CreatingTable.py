# ---> THIS FILE EXTRACTS THE:
# 1. 'prices', 'unique id', 'price' and  'category' and puts them in a dataframe 'df_prices'
# 2. 'benefit name' and 'benefit value' and puts them in a dataframe 'df_benefits' then
#    inserts id(primary key) to connect to df_prices when putting in database
#    and dfid( dataframe id ) and uid( unique id )
# 3. unique ott list 'uuniqueottlist'

from FetchingResponse import loaded_json
import pandas as pd 
import numpy as np
from glom import glom
# imported all the required libraries

# a flattening function for nested list
def flatten(lst):
    result = []
    for item in lst:
        if isinstance(item, list):
            result.extend(flatten(item))
        else:
            result.append(item)
    return result

# using glom to extract amount of each plan
spec_rate='planCategories.*.subCategories.*.plans.*.amount'
unflat_rates=glom(loaded_json,spec_rate)

# flattening rates :
flattened_rates=[item for row in unflat_rates for item in row]

# extracting categories of plans
spec_Cat='planCategories.*.type'
list_cat=glom(loaded_json,spec_Cat)
# print(list_cat)

# creating dictionary of price and caetgory
all_price_data={"price":unflat_rates,"category":list_cat}
# print(all_price_data)
df_prices1=pd.DataFrame(data=all_price_data)
# print('df_prices1\n',df_prices1)

# exploding two times
df_prices2=df_prices1.explode("price")
df_prices=df_prices2.explode("price",ignore_index=True)
# print(df_prices)
df_prices.insert(0,"id",np.arange(0,len(df_prices)))
# print(df_prices)

# extracting unique ids
spec_listof_unique_ids='planCategories.*.subCategories.*.plans.*.id'
listof_unique_ids_unflat=glom(loaded_json,spec_listof_unique_ids)
listof_unique_ids=flatten(listof_unique_ids_unflat)
df_prices.insert(1,"uid",listof_unique_ids)

# getting a dictionary of id, uid, price and category
iduidpc_dict=df_prices.to_dict(orient='index')

# getting details :[ {header :" ", value;" "} ]
# getting BENEFITS 
spec_benefits='planCategories.*.subCategories.*.plans.*.misc.details'
# we get dictionaries nested in list 4 times
dict_benefits=glom(loaded_json,spec_benefits)
# print('dict_benefits=','\n',dict_benefits,"\n",len(dict_benefits))

# dictionary containing all the benefits of each pack ,an iterator for getting all the benefits
one_list={}
count=0 
# extracting the subscriptions( otts )
spec_otts='planCategories.*.subCategories.*.plans.*.misc.subscriptions.*.title'
ottlist=glom(loaded_json,spec_otts)

# list of all otts(but repeating)
flatott=[]

# appending otts to dict_benefits dictionary and putting them in one_list dictionary and otts to flatott. 
for i in range(0,len(loaded_json['planCategories'])):
    for j in range(0,len(loaded_json['planCategories'][i]['subCategories'])):
        for k in range(0,len(loaded_json['planCategories'][i]['subCategories'][j]['plans'])):
            # we get a proper one list containing dictionaries numbered . It is in "header":"Benefit Name" , "value":"Benefit Value"
            if len(ottlist[i][j])==0:
                flatott.append(ottlist[i][j])
                dict_benefits[i][j][k].append({'header':'Subscriptions','value':ottlist[i][j]})
            else:
                flatott.append(ottlist[i][j][k])
                dict_benefits[i][j][k].append({'header':'Subscriptions','value':ottlist[i][j][k]})

            one_list[count]=dict_benefits[i][j][k]
            count+=1

# print("one list=\n",one_list,"\n\n")
# putting all the benefits and uid, id ,price and category of each price in a list(one_pack)
iterateing=0
one_pack=[]
# dictionary with id, uid, price, category and all benefits( unnested)
final_dict_nested={}
for i in one_list:
    one_pack.append(iduidpc_dict[i])
    for j in range(len(one_list[i])):
        proper_one_list={}
        proper_one_list[one_list[i][j]['header']]=one_list[i][j]['value']
        one_pack.append(proper_one_list)
    #Here we get a dictionary containing lists(packs)
    final_dict_nested[iterateing]=one_pack
    one_pack=[]
    iterateing+=1

# uncomment print statement to see the dictionary. This dictionary contains the id, uid, price and category in one dict of pack lisit and benefits in other
# Example: {0: [{'id': 0, 'uid': '1018982', 'price': '349', 'category': 'Popular Plans'}, {'Pack validity': '28 Days'}, {'Total data': '56 GB'}, {'Data at high speed*': '2 GB/Day'}, {'Voice': 'Unlimited'}, {'SMS': '100 SMS/Day'}, {'Subscriptions': ['JioTV', 'JioAICloud']}]
# print("final dict nested=\n",final_dict_nested)

#getting the list of Benefit Name and Benefit Value from final_dict_nested
Benefit_Name=[]
Benefit_Value=[]
for i in final_dict_nested:
    mergeddict_i={}
    for j in final_dict_nested[i]:
        mergeddict_i=mergeddict_i | j

    Benefit_Name.append(list(mergeddict_i.keys()))
    Benefit_Value.append(list(mergeddict_i.values()))

#dictionary with Benefit Name and Benefit Value
all_Benefits_data={"id":np.arange(0,len(Benefit_Name)), "benefitname":Benefit_Name,"benefitvalue":Benefit_Value}

#Insertign the all_Benefits_data in a dataframe
df_benefits=pd.DataFrame(data=all_Benefits_data)

# inserting the unique ID for each plan
df_benefits.insert(1,"uid",listof_unique_ids)

# exploding the dataframe 
df_benefits=df_benefits.explode(["benefitname","benefitvalue"],ignore_index=True)

#inserting a dataframe id 
df_benefits.insert(0,"dfid",np.arange(0,len(df_benefits)))
# print(df_benefits)

#list of all the otts (non repeating)
uniqueottlist=pd.Series(flatten(flatott)).unique()

# getting a dataframe for otts
dfott=pd.DataFrame({"sub_id":np.arange(0,len(flatott)).tolist(), "subval":flatott})
# print(dfott)
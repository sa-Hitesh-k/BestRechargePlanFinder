import pandas as pd 
import numpy as np
from glom import glom
from FetchingResponse import fetch_jio_data

# --- HELPER FUNCTIONS ---

def flatten(lst):
    """A flattening function for nested list."""
    result = []
    for item in lst:
        if isinstance(item, list):
            result.extend(flatten(item))
        else:
            result.append(item)
    return result

# --- CORE PROCESSING FUNCTIONS ---

def get_price_dataframe(loaded_json):
    """Processes rates, categories, and unique IDs into df_prices."""
    # Extract rates
    spec_rate = 'planCategories.*.subCategories.*.plans.*.amount'
    unflat_rates = glom(loaded_json, spec_rate)
    
    # Extract categories
    spec_Cat = 'planCategories.*.type'
    list_cat = glom(loaded_json, spec_Cat)
    
    # Create and explode DataFrame
    all_price_data = {"price": unflat_rates, "category": list_cat}
    df_prices = pd.DataFrame(data=all_price_data)
    df_prices = df_prices.explode("price").explode("price", ignore_index=True)
    
    # Insert ID and UID
    df_prices.insert(0, "id", np.arange(0, len(df_prices)))
    spec_listof_unique_ids = 'planCategories.*.subCategories.*.plans.*.id'
    listof_unique_ids_unflat = glom(loaded_json, spec_listof_unique_ids)
    listof_unique_ids = flatten(listof_unique_ids_unflat)
    df_prices.insert(1, "uid", listof_unique_ids)
    
    return df_prices, listof_unique_ids

def get_benefit_logic(loaded_json, iduidpc_dict):
    """Handles the heavy nested iteration logic for benefits and subscriptions."""
    spec_benefits = 'planCategories.*.subCategories.*.plans.*.misc.details'
    dict_benefits = glom(loaded_json, spec_benefits)
    
    spec_otts = 'planCategories.*.subCategories.*.plans.*.misc.subscriptions.*.title'
    ottlist = glom(loaded_json, spec_otts)

    one_list = {}
    count = 0 
    flatott = []

    # PRESERVED ITERATION LOGIC
    for i in range(0, len(loaded_json['planCategories'])):
        for j in range(0, len(loaded_json['planCategories'][i]['subCategories'])):
            for k in range(0, len(loaded_json['planCategories'][i]['subCategories'][j]['plans'])):
                if len(ottlist[i][j]) == 0:
                    flatott.append(ottlist[i][j])
                    dict_benefits[i][j][k].append({'header': 'Subscriptions', 'value': ottlist[i][j]})
                else:
                    flatott.append(ottlist[i][j][k])
                    dict_benefits[i][j][k].append({'header': 'Subscriptions', 'value': ottlist[i][j][k]})

                one_list[count] = dict_benefits[i][j][k]
                count += 1

    # Formatting into final_dict_nested
    final_dict_nested = {}
    iterateing = 0
    for i in one_list:
        one_pack = [iduidpc_dict[i]]
        for j in range(len(one_list[i])):
            proper_one_list = {one_list[i][j]['header']: one_list[i][j]['value']}
            one_pack.append(proper_one_list)
        
        final_dict_nested[iterateing] = one_pack
        iterateing += 1
        
    return final_dict_nested, flatott

def get_benefit_dataframe(final_dict_nested, listof_unique_ids):
    """Creates the exploded df_benefits from the nested dictionary."""
    Benefit_Name = []
    Benefit_Value = []
    
    for i in final_dict_nested:
        mergeddict_i = {}
        for j in final_dict_nested[i]:
            mergeddict_i = mergeddict_i | j
        
        Benefit_Name.append(list(mergeddict_i.keys()))
        Benefit_Value.append(list(mergeddict_i.values()))

    all_Benefits_data = {
        "id": np.arange(0, len(Benefit_Name)), 
        "benefitname": Benefit_Name, 
        "benefitvalue": Benefit_Value
    }
    
    df_benefits = pd.DataFrame(data=all_Benefits_data)
    df_benefits.insert(1, "uid", listof_unique_ids)
    df_benefits = df_benefits.explode(["benefitname", "benefitvalue"], ignore_index=True)
    df_benefits.insert(0, "dfid", np.arange(0, len(df_benefits)))
    
    return df_benefits

def get_ott_list():
    spec_otts = 'planCategories.*.subCategories.*.plans.*.misc.subscriptions.*.title'
    loaded_json= fetch_jio_data()
    ottlist = glom(loaded_json, spec_otts)
    flatott = []

    for i in range(0, len(loaded_json['planCategories'])):
        for j in range(0, len(loaded_json['planCategories'][i]['subCategories'])):
            for k in range(0, len(loaded_json['planCategories'][i]['subCategories'][j]['plans'])):
                if len(ottlist[i][j]) == 0:
                    flatott.append(ottlist[i][j])
                else:
                    flatott.append(ottlist[i][j][k])

    #list of all the otts (non repeating)
    uniqueottseries=pd.Series(flatten(flatott)).unique().tolist()
    ids=np.arange(0,len(uniqueottseries)).tolist()
    datadict={'ottid':ids, 'otts':uniqueottseries}
    uniqueott_df=pd.DataFrame(datadict)
    # print(uniqueott_df)
    return uniqueott_df

# --- MASTER ORCHESTRATOR ---

def process_all_jio_data():
    """Orchestrates the full data pipeline from memory."""
    loaded_json = fetch_jio_data()
    if not loaded_json:
        return None, None, None

    # 1. Prices
    df_prices, listof_unique_ids = get_price_dataframe(loaded_json)
    iduidpc_dict = df_prices.to_dict(orient='index')

    # 2. Nested Benefits
    final_dict_nested, flatott = get_benefit_logic(loaded_json, iduidpc_dict)

    # 3. Benefit Dataframe
    df_benefits = get_benefit_dataframe(final_dict_nested, listof_unique_ids)

    # 4. OTT Dataframe
    dfott = pd.DataFrame({"sub_id": np.arange(0, len(flatott)).tolist(), "subval": flatott})
    # print("dfott =\n",dfott)
    return df_prices, df_benefits, dfott

# --- THE GUARDRAIL ---
if __name__ == "__main__":
    prices, benefits, otts = process_all_jio_data()
    uniqueotts=get_ott_list()
    if prices is not None:
        print(f"✅ Success! Processed {len(prices)} plans and {len(benefits)} individual benefits.")
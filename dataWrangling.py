import pandas as pd
import sqlalchemy as sql

dataset = "SampleSuperstore.csv"

def inspect(df):
    print(df.describe(include='all'))
    print(df.head())
    print(df.columns.to_list)


if __name__ == "__main__":
    df = pd.read_csv(dataset)
    # inspect(df)

    # country's unique val is just 'United States' and Region is not as useful as State
    # will drop country col and region col
    df1 = df.drop(['Country', 'Region'], axis=1)
    
    # inspect(df1)
    # no null values in dataset, as seen by running 'describe'

    # create calculated field retail price
    retail = []
    for saleamt, qty, dsct in zip(df1['Sales'], df1['Quantity'], df1['Discount']):
        if qty != 0:
            retailprice = (saleamt / qty) / (1 - dsct)
            retail.append(retailprice)
        else:
            retail.append(None)
    
    # concat retail with the df 
    df1['RetailPrice'] = retail

    # create high price flag column, prices in the top 20%
    threshold = df1['RetailPrice'].quantile(0.8)
    priceflag = []

    for price in df1['RetailPrice']:
        if price:
            if price > threshold:
                priceflag.append(True)
            else:
                priceflag.append(False)
        else:
            priceflag.append(False)

    # concat high priceflag with df
    df1['HighPriceFlag'] = priceflag

    # look at new df
    inspect(df1)

    # explore vals of things going to be put in sep tables: Category, subcat, segment
    # it is known that segment vals are: corporate, home office, consumer
    # category is: office supplies, technology
    # sub cat:
    print(df1['Sub-Category'].unique())
    # Subcat is: bookcases, chairs, labels, tables, storage, furnishings, art, phones, 
    # binders, appliances, paper, accessories, evelopes, fasteners, supplies, machines, copiers
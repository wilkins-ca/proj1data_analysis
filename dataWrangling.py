import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from dbClasses import cat, subcat, sales, segments, shippingmode, base

# get sql creds as env vars
load_dotenv()
rootuser = os.getenv("rootuser")
rootpw = os.getenv("rootpw")
host = os.getenv("host")
port = os.getenv("port")
db = os.getenv("db")

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

    x = 'Copiers' # subcat var used to figure out what category the subcat is 
    print(df1.loc[df1['Sub-Category'] == x, 'Category'])

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
    # inspect(df1)

    # explore vals of things going to be put in sep tables: Category, subcat, segment
    # it is known that segment vals are: corporate, home office, consumer
    # category is: office supplies, technology, furniture
    # sub cat:
    # print(df1['Sub-Category'].unique())
    # Subcat is: bookcases, chairs, labels, tables, storage, furnishings, art, phones, 
    # binders, appliances, paper, accessories, evelopes, fasteners, supplies, machines, copiers

    # map subcats to cats in dict to make preparation for cat foreign key in subcat table
    subcatToCat = {
        'Bookcases': 'Furniture',
        'Chairs': 'Furniture',
        'Labels': 'Office Supplies',
        'Tables': 'Furniture',
        'Storage': 'Office Supplies',
        'Furnishings': 'Furniture',
        'Art': 'Office Supplies',
        'Phones': 'Technology',
        'Binders': 'Office Supplies',
        'Appliances': 'Office Supplies', 
        'Paper': 'Office Supplies',
        'Accessories': 'Technology', 
        'Envelopes': 'Office Supplies',
        'Fasteners': 'Office Supplies',
        'Supplies': 'Office Supplies',
        'Machines': 'Technology',
        'Copiers': 'Technology'
    }

    # bring cat, subcat, seg, and shipping into separate entities so they can live in their own tables
    shippingmodes = df1['Ship Mode'].unique()
    segment = df1['Segment'].unique()
    categories = df1['Category'].unique()
    subcategories = df1['Sub-Category'].unique()

    # add row IDs
    ship_modes = pd.DataFrame({'id': range(1, len(shippingmodes) + 1), 'shippingModes': shippingmodes})
    seg = pd.DataFrame({'id': range(1, len(segment) + 1), 'segment': segment})
    cats = pd.DataFrame({'id': range(1, len(categories) + 1), 'category': categories})
    subcats = pd.DataFrame({'id': range(1, len(subcategories) + 1), 'sub-category': subcategories})
    # make cat col in subcats df
    subcats['category'] = subcats['sub-category'].map(subcatToCat)
    df1['id'] = df1.index + 1

    # replace string values in df1 with corresponding row IDs for cat, subcat, seg, and shipping
    cat_map = dict(zip(cats['category'], cats['id']))
    df1['Category'] = df1['Category'].map(cat_map)

    # add what will be foreign key to subcats df, drop the subcat df's column with cat names (as opposed to the cat ID)
    subcats['cat_id'] = subcats['category'].map(cat_map)
    subcats.drop(columns=['category'], inplace=True)
    
    subcats_map = dict(zip(subcats['sub-category'], subcats['id']))
    df1['Sub-Category'] = df1['Sub-Category'].map(subcats_map)

    seg_map = dict(zip(seg['segment'], seg['id']))
    df1['Segment'] = df1['Segment'].map(seg_map)

    ship_map = dict(zip(ship_modes['shippingModes'], ship_modes['id']))
    df1['Ship Mode'] = df1['Ship Mode'].map(ship_map)

    # print(df1)
    # create postgres engine
    engine = create_engine(f"postgresql://{rootuser}:{rootpw}@{host}:{port}/{db}")
    # create the tables
    # base.metadata.create_all(engine)


    # load the data into postgres
     
    Session = sessionmaker(bind = engine)
    session = Session()

    """ session.query(cat).delete()
    session.commit()
    for _, row in cats.iterrows():
        print(row)
        category = cat(
            id = row['id'],
            cat = row['category']
        )
        session.add(category)
    session.commit() """ 
    # ^committed successfully   

    """ for _, row in subcats.iterrows():
        subcategory = subcat(
            id = row['id'],
            subcat = row['sub-category'],
            cat = row['cat_id']
        )
        session.add(subcategory)
    session.commit() """
    # ^committed successfully    

    """ for _, row in ship_modes.iterrows():
        mode = shippingmode(
            id = row['id'],
            mode = row['shippingModes']
        )
        session.add(mode)
    session.commit() """
    # ^committed successfully

    """ for _, row in seg.iterrows():
        segment = segments(
            id = row['id'],
            seg = row['segment']
        )
        session.add(segment)
    session.commit()

    for _, row in df1.iterrows():
        salesRow = sales(
            rowID = row['id'],
            city = row['City'],
            state = row['State'],
            zipcode = str(row['Postal Code']),
            subcat = row['Sub-Category'],
            salesTotal = row['Sales'],
            profit = row['Profit'],
            retailprice = row['RetailPrice'],
            highPrice = row['HighPriceFlag'],
            qty = row['Quantity'],
            discount = row['Discount'],
            shipMode = row['Ship Mode'],
            cat = row['Category'],
            segment = row['Segment']
        ) 
        session.add(salesRow)
    session.commit() """
    # ^committed successfully
import pandas as pd


zips = pd.read_csv('data/new_zip_codes.csv')
addresses = pd.read_csv('data/new_property_info.csv')

address_out = []
for address in addresses.iterrows():
    add_data = list(address)
    a_latitude = add_data[1]['Latitude']
    a_longitude = add_data[1]['Longitude']

    best_index = 0
    best_diff = 999
    for zip_code in zips.iterrows():
        zip_data = list(zip_code)
        z_latitude = zip_data[1]['Latitude']
        z_longitude = zip_data[1]['Longitude']
        diff = abs(a_latitude - z_latitude) + abs(a_longitude - z_longitude)
        if diff < best_diff:
            best_index = zip_data[0]
            best_diff = diff
    address_out.append({'address': add_data[1]['PropertyAddress'], 'zip_code': zips.iloc[best_index]['Zip']})
pd.DataFrame(address_out).to_csv('data/address_zipped.csv', index=False)

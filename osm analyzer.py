

import osmnx as ox
import matplotlib.pyplot as plt

from pathlib import Path
import pandas as pd

AMENITY_QUERIES = [
    ("bank", {"amenity": "bank"}),
    ("bar", {"amenity": ["bar", "pub"]}),
    ("coffee shop", {"amenity": "cafe", "cuisine": "coffee_shop"}),
    (
        "greater victoria public library",
        {"operator": "Greater Victoria Public Library"},
    ),
    ("medical clinic", {"amenity": "clinic"}),
    ("school", {"amenity": "school"}),
    (
        "store",
        {
            "shop": ["supermarket", "greengrocer", "convenience"],
            "name": ["Walmart", "Wholesale Club"],
        },
    ),
]
COL_REGEX = r"^(name|brand|geometry|(addr:\w+))$"

if __name__ == "__main__":
    data_dir = Path("amenity data")
    data_dir.mkdir(exist_ok=True)

    for amenity, query in AMENITY_QUERIES:
        places = ox.geometries_from_place("Greater Victoria", query)
        places = places.filter(regex=COL_REGEX)

        #turn places into a pandas df with column Latitude and Longitude
        #to nad 83 utm 10n
        
        places = places.to_crs("EPSG:26910")
        places['geometry'] = places['geometry'].centroid
        places = places.to_crs("EPSG:4326")
        places["Latitude"] = places["geometry"].y
        places["Longitude"] = places["geometry"].x

        #drop geometry column
        places = places[['name', 'Latitude', 'Longitude']]

        places.to_csv(data_dir / f"{amenity}.csv", index=False)

    #create new empty df with 'amenity' and 'weight'
    weights = pd.DataFrame(columns=['amenity', 'weight'])
    weights.amenity = [amenity for amenity, _ in AMENITY_QUERIES]
    weights.weight = 1
    weights.to_csv('amenity weights.csv', index=False)
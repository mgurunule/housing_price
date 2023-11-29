DROP TABLE IF EXISTS predicted_data_table;
Create Table predicted_data_table
            ( longitude  int  not null,
            latitude  int  not null,
            housing_median_age  int  not null,
            total_rooms  int  not null,
            total_bedrooms  int  not null,
            population  int  not null,
            households  int  not null,
            median_income  int  not null,
            ocean_proximity_LESS_H_OCEAN  int  not null,
            ocean_proximity_INLAND  int  not null,
            ocean_proximity_ISLAND  int  not null,
            ocean_proximity_NEAR_BAY  int  not null,
            ocean_proximity_NEAR_OCEAN  int  not null,
            MEDIAN_HOUSE_PRICE  int  not null
            )

# query_homework.py
"""
Execute NYC Taxi Homework Queries
"""

import duckdb

# Connexion
con = duckdb.connect("nyc_taxi_pipeline.duckdb", read_only=True)

print("=" * 100)
print("NYC TAXI DATA ANALYSIS - HOMEWORK")
print("=" * 100)

# Voir les schémas
print("\n\t Schemas:")
schemas = con.execute("""
    SELECT schema_name 
    FROM information_schema.schemata
""").fetchdf()
print(schemas)

# Voir les tables
print("\n\t Tables:")
try:
    tables = con.execute("SHOW TABLES FROM nyc_taxi_data").fetchdf()
    print(tables)
except:
    tables = con.execute("SHOW TABLES").fetchdf()
    print(tables)

# Structure de la table
print("\n\t Structure de taxi_trips:")
structure = con.execute("""
    SELECT column_name, data_type
    FROM information_schema.columns
    WHERE table_name = 'taxi_trips'
    ORDER BY ordinal_position
""").fetchdf()
print(structure)

# Compter les lignes
print("\n\t Total lignes:")
count = con.execute("""
    SELECT COUNT(*) as total
    FROM nyc_taxi_data.taxi_trips
""").fetchdf()
print(count)


# Question 1
print("\n" + "=" * 100)
print("\n\t Q1: What is the start date and end date?")
print("=" * 100)
q1 = con.execute("""
    SELECT 
        MIN(trip_pickup_date_time) as start_date,
        MAX(trip_pickup_date_time) as end_date
    FROM nyc_taxi_data.taxi_trips
""").fetchdf()
print(q1.to_string(index=False))

# Question 2
print("\n" + "=" * 100)
print("\n\t Q2: Credit card proportion?")
print("=" * 100)
q2 = con.execute("""
    SELECT 
        COUNT(*) as total_trips,
        SUM(CASE WHEN payment_type = 'Credit' THEN 1 ELSE 0 END) as credit_card_trips,
        ROUND(SUM(CASE WHEN payment_type = 'Credit' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as credit_card_percentage
    FROM nyc_taxi_data.taxi_trips
""").fetchdf()
print(q2.to_string(index=False))

# Question 3
print("\n" + "=" * 100)
print("\n\t Q3: Total tips?")
print("=" * 100)
q3 = con.execute("""
    SELECT 
        ROUND(SUM(COALESCE(tip_amt, 0)), 2) as total_tips
    FROM nyc_taxi_data.taxi_trips
""").fetchdf()
print(q3.to_string(index=False))

print("\n\t Done!")

con.close()
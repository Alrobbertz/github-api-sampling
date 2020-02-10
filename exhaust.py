from sample import exhaust_range

# Set Query Bounds
id_low=200001
id_high=325000

# Set Granularity
granularity = 250

active_users = exhaust_range(id_low, id_high, granularity)

print(active_users)
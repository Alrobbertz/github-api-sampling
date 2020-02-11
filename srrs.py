import csv
import numpy as np
from sample import simple_random_range_sample

# Set the Upper Bound for known User Space
M=1000000

# Set the Budget (# of API call allocated)
B=50

# Set the number of Estimations to make
E=50

# Set the number of Queries to Exhaust a partition
alpha=1


# number of user IDs in each partition (assume 30 IDs from each query)
k=alpha*(30)

# number of partitions to divide G
n=int(M/k)

# number of partitions to randomly sample
m=int(B/(alpha*E))

print(f'Budget={B}    # Estimate={E}    Sample/Est={m}    Partition_Size={k}    # Partition={n}  Sample_Rate={m/n}')


# Yeet
estimations = simple_random_range_sample(M=M, B=B, E=E, alpha=alpha)
print(estimations)

# Print Stats
print(np.var([est['Users'] for est in estimations]))
print(np.std([est['Users'] for est in estimations]))
print([est['Users'] for est in estimations])


# Write results to a CSV
csv_columns = ['Users','Xt-Variance']
csv_file = "results.csv"
try:
    with open(csv_file, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
        writer.writeheader()
        for data in estimations:
            writer.writerow(data)
except IOError:
    print("I/O error")
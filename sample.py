import requests
import random
import numpy as np


# Setup the API Headers
headers={
    'Authorization': 'token d1bc0d9419dfe75e47f0156584675dea05690142',
}

def sample_id(id):
    response = requests.get('https://api.github.com/users?since='+str(id), headers=headers)
    return [user['id'] for user in response.json()]


def sample_range(id_low, id_high):
    active_in_range = 0
    _id = id_low
    _qr = True
    while _qr:
        active_ids = sample_id(_id)

        for user_id in active_ids:
            if user_id <= id_high:
                active_in_range += 1
            else:
                _qr = False
                break
        _id = active_ids[-1]

    return active_in_range


def simple_random_range_sample(M=60654216, B=1000, E=10, alpha=3):
    # Let k= number of user IDs in each partition 
    # # (assume 30 IDs from each query)
    k=alpha*(30)

    # let n= the number of partitions to divide G
    n=int(M/k)

    # let m= number of partitions to randomly sample
    m=int(B/(alpha*E))

    print(f'Budget={B}    # Estimate={E}    Sample/Est={m}    Partition_Size={k}    # Partition={n}  Sample_Rate={m/n}')

    # Run E - # of estimations
    estimations=[]
    for i in range(E):
        print(f'Making Estimation: {i}')        
        active=[]

        # Collect m - sample paratitions
        for t in range(m):
            # Chose a random partition
            start_id = random.randrange(0, M, k)
            end_id = start_id+k

            # Sample the Partition
            active_users = sample_range(start_id, end_id)
            active.append(active_users)
            print(f'Sampling: t:{t} range:{(start_id, end_id)} Foud:{active_users}')
        
        # Tabulation Stage
        n_hat = int(n/m) * sum(active)
        variance = np.var(active)

        # Save the results
        estimations.append({
            'Users': n_hat,
            'Xt-Variance': variance
        })
    return estimations


def sample_timebox(time_box):
    # Hot indexed (1 if id exists, 0 otherwise)
    samples=[]
    for sample in time_box['items']:
        _id = sample['id']
        response = requests.get('https://api.github.com/users?since='+str(_id), headers=headers)
        data = response.json()
        _exists = (data[0]['id'] == _id+1)
        if _exists:
            samples.append(1)
        else:
            samples.append(0)
    return samples


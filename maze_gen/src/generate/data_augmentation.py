import numpy as np
import pandas as pd
import random
import os
import datetime as dt

def load_data(dir):
    """Loads data to be augmented from csv file.

    Args:
        dir (): _description_

    Returns:
        _type_: _description_
    """
    file = input('Enter file name of data to be augmented:\n')
    data = pd.read_csv(f'{dir}/data/{file}')
    labels = data['labels']
    data = data.drop(['Unnamed: 0', 'labels'], axis=1)
    return data, labels

def compress(data):
    # print('COMPRESS')
    # print(data)
    factor = random.randint(2,4)
    insert_idx = round(150/factor)
    signal = data[::factor]
    noise = [x+random.randint(-1,1) for x in np.zeros(75)]
    new_data = np.insert(noise, insert_idx, signal)
    # print(len(new_data))
    return pd.Series(new_data)

def expand(data):
    # print('EXPAND')
    # print(data)
    factor = random.randint(15, 25)
    new_data = []
    data = data[factor:-factor]
    for i, d in enumerate(data):
        if i%2 != 0:
            continue

        if i == len(data)-1:
            new_data.extend([d, d])
            break
        mean = np.mean([d, data[i+1]])
        new_data.extend([d, mean, data[i+1]])

        
        # print('iter:', i)
        # print(len(new_data))
    # print(len(new_data))
    return pd.Series(new_data)

def shift_lr(data, direction):
    # print('SHIFT ', direction.upper())
    # print(data)
    new_data = []
    try:
        if direction == 'l':
            dist = random.randint(1,5)
        elif direction == 'r':
            dist = random.randint(-5,-1)
        else:
            raise ValueError
    except ValueError:
        print('Invalid direction input. String must be l or r.')
    
    for i in range(len(data)):
        # print(direction.upper())
        # print(i)
        if direction == 'l':
            check = i + dist <= len(data)-1
        else:
            check = i + dist >= 0
        if check:
            new_data.append(data[i+dist])
        else:
            new_data.append(random.randint(-1,1))
    # print(len(new_data))
    return pd.Series(new_data)

def main():
    dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    data, labels = load_data(dir)
    new_df = pd.DataFrame(columns=data.columns)
    # print(data)
    for i in range(1000):
        print(f'Iteration {i}')
        compressed = data.apply(compress, axis=1)
        expanded = data.apply(expand, axis=1)
        left_shift = data.apply(shift_lr, args=('l'), axis=1)
        right_shift = data.apply(shift_lr, args=('r'), axis=1)
        compressed.columns = data.columns
        expanded.columns = data.columns
        left_shift.columns = data.columns
        right_shift.columns = data.columns
        # print(compressed.columns)
        # print(expanded.columns)
        # print(left_shift.columns)
        # print(right_shift.columns)
        # print(data)
        new_df = pd.concat([new_df, compressed, expanded, left_shift, right_shift])
        # print(data)
    
    new_df['labels'] = labels
    new_df.to_csv(f'{dir}/data/augmented_{dt.datetime.now()}.csv')

if __name__ == '__main__':
    main()
    






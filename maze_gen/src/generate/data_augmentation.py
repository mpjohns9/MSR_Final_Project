import numpy as np
import pandas as pd
import random
import math
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

def center(data):
    noise = []
    signal = []
    check_noise = False
    for i, d in enumerate(data):
        if i < len(data)-3:
            if (abs(d) > 5) or (abs(data[i+3]) > 5):
                check_noise = False
            else:
                check_noise = True
        
        if check_noise:
            noise.append(d)
        else:
            signal.append(d)
    mid = round(len(noise)/2)
    p1 = noise[:mid].copy()
    p2 = noise[mid:].copy()
    centered = [*p1, *signal, *p2]
    return centered

def compress(data):
    # print('COMPRESS')
    # print(data)
    factor = random.randint(2,4)
    insert_idx = round(150/factor)
    signal = data[::factor]
    # print('Factor', factor)
    noise = [x+random.randint(-1,1) for x in np.zeros(150-insert_idx)]
    new_data = np.insert(noise, insert_idx, signal)
    # print(len(new_data))
    return pd.Series(new_data)

def expand(data):
    # print('EXPAND')
    # print(data)
    new_data = []
    data = data[25:-25]
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
    new_df = data.copy()
    # print(data)
    iters = 1
    for i in range(iters):
        print(f'Iteration {i}')
        # print(data.shape)
        # print(new_df.shape)
        for i, row in data.iterrows():
            print(len(row))
            print(row)
            while len(row) < 150:
                row.append(0)

            print(len(row))
            print(row)
            row = center(row)
            random_fn = random.randint(1, 4)
            if random_fn == 1:
                # print('COMPRESS')
                new_row = compress(row)
                new_row.index = new_df.columns
                new_row = new_row.to_frame().T
                new_df = pd.concat([new_df, new_row])
            elif random_fn == 2:
                # print('EXPAND')
                new_row = expand(row)
                new_row.index = new_df.columns
                new_row = new_row.to_frame().T
                new_df = pd.concat([new_df, new_row])
            elif random_fn == 3:
                # print('SHIFT L')
                new_row = shift_lr(row, 'l')
                new_row.index = new_df.columns
                new_row = new_row.to_frame().T
                new_df = pd.concat([new_df, new_row])
            elif random_fn == 4:
                # print('SHIFT R')
                new_row = shift_lr(row, 'r')
                new_row.index = new_df.columns
                new_row = new_row.to_frame().T
                new_df = pd.concat([new_df, new_row])
            # print(new_df)
        
        # print(compressed.columns)
        # print(expanded.columns)
        # print(left_shift.columns)
        # print(right_shift.columns)
        # print(data)
        # new_df = pd.concat([new_df, compressed, expanded, left_shift, right_shift])
        # print(data)
    
    new_df['labels'] = labels.tolist()*(iters+1)
    # print(new_df['labels'].value_counts())
    # return
    new_df.to_csv(f'{dir}/data/augmented_{dt.datetime.now()}.csv')

if __name__ == '__main__':
    main()
    






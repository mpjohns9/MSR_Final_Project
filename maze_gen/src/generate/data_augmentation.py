import numpy as np
import pandas as pd
import random
import math
import os
import datetime as dt

def load_data(dir):
    """Loads data to be augmented from csv file.

    Args:
        dir (str): Path to package root directory

    Returns:
        data (pd.DataFrame): Dataframe containing data loaded from csv
        labels (pd.Series): Labels extracted from column of dataframe
    """

    file = input('Enter file name of data to be augmented:\n')
    data = pd.read_csv(f'{dir}/data/{file}')
    labels = data['labels']
    data = data.drop(['Unnamed: 0', 'labels'], axis=1)
    return data, labels

def center(data):
    """Separates noise and signal and centers signal in time.

    Args:
        data (list): List of data to be centered (e.g., analog signal)

    Returns:
        centered (list): New list of same data with signal centered on noise
    """

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
    """Compresses signal and adds noise in its place.

    Takes every 2-4 data points (random) and fills the rest out
    around it with noise to reamin at length of 150.

    Args:
        data (list): List of data to be compressed 

    Returns:
        new_data (pd.Series): Compressed data
    """

    factor = random.randint(2,4)
    insert_idx = round(150/factor)
    signal = data[::factor]
    noise = [x+random.randint(-1,1) for x in np.zeros(150-insert_idx)]
    new_data = np.insert(noise, insert_idx, signal)
    return pd.Series(new_data)

def expand(data):
    """Expands signal by taking mean of consecutive data.

    Uses middle 100 data points and generates new data using 
    mean of consecutive data to maintain length of 150.

    Args:
        data (list): List of data to be expanded

    Returns:
        new_data (pd.Series): Expanded data
    """

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

    return pd.Series(new_data)

def shift_lr(data, direction):
    """Shifts signal toward front or back of list (earlier/later in time).

    Args:
        data (list): List of data to be shifted
        direction (str): 'l' for left shift (front) and 'r' for right shift (back)
    Raises:
        ValueError: Raises error if 'l' or 'r' isn't given as direction

    Returns:
        new_data (pd.Series): Data shifted left (forward) or right (backward) in list
    """

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
        if direction == 'l':
            check = i + dist <= len(data)-1
        else:
            check = i + dist >= 0
        if check:
            new_data.append(data[i+dist])
        else:
            new_data.append(random.randint(-1,1))

    return pd.Series(new_data)

def main():
    """Applies random transformation to existing data.
    
    Possible transformations include: compression, expansion, shift earlier/later in time.
    Transformed data is saved to csv (augmented_{current_time}.csv).
    """

    dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    data, labels = load_data(dir)
    new_df = data.copy()

    iters = 1
    for i in range(iters):
        print(f'Iteration {i}')
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
                new_row = compress(row)
                new_row.index = new_df.columns
                new_row = new_row.to_frame().T
                new_df = pd.concat([new_df, new_row])
            elif random_fn == 2:
                new_row = expand(row)
                new_row.index = new_df.columns
                new_row = new_row.to_frame().T
                new_df = pd.concat([new_df, new_row])
            elif random_fn == 3:
                new_row = shift_lr(row, 'l')
                new_row.index = new_df.columns
                new_row = new_row.to_frame().T
                new_df = pd.concat([new_df, new_row])
            elif random_fn == 4:
                new_row = shift_lr(row, 'r')
                new_row.index = new_df.columns
                new_row = new_row.to_frame().T
                new_df = pd.concat([new_df, new_row])
    
    new_df['labels'] = labels.tolist()*(iters+1)
    new_df.to_csv(f'{dir}/data/augmented_{dt.datetime.now()}.csv')

if __name__ == '__main__':
    main()
    






import numpy as np
import pandas as pd
import random
import os
import argparse
from inputs import get_gamepad
import time
import plotext as plt

from tensorflow.keras.models import load_model

class Synthetic:
    """Generate and test synthetic dataset."""

    def __init__(self):
        """Creates new synthetic object.

        Args:
            dir (str): Path to package root directory
            x (ndarray): 1D array containing 150 values spaced evenly from 0 to 2pi
            puff_sip (ndarray): Simulated puff then sip (sin(x))
            sip_puff (ndarray): Simulated sip then puff (-sin(x))
            double_puff (ndarray): Simulated double puff (absolute value of sin(x))
            double_sip (ndarray): Simulated double sip (neg. absolute value of sin(x))
            nothing (ndarray): Array of all zeros
            inputs (dict): Mapping class to simulated signal (input)
        """

        self.dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        
        self.x = np.linspace(0, np.pi*2, 150)

        self.puff_sip = np.sin(self.x)
        self.sip_puff = -self.puff_sip
        self.double_puff = np.abs(self.puff_sip)
        self.double_sip = -self.double_puff
        self.nothing = np.zeros(150)

        self.inputs = {
            0:self.double_sip,
            1:self.double_puff,
            2:self.puff_sip,
            3:self.sip_puff,
            4:self.nothing
        }

    def random_input(self):
        """Generates random input from inputs dict with random amplitude.

        Returns:
            ndarray: Random input with random amplitude
            event (int): Class corresponding to random input
        """

        amp = random.randint(75, 115)
        event = random.randint(0, len(self.inputs.keys())-1)
        return amp*self.inputs[event], event

    def simulate(self, num_events):
        """Generates specified number of randomized synthetic data points.

        Args:
            num_events (int): Number of data points to be generated

        Returns:
            events (list): List of random inputs
            labels (list): List of class labels corresponding to inputs
        """
        events = []
        labels = []
        for i in range(num_events):
            event, label = self.random_input()
            events.append(event)
            labels.append(label)

        return events, labels  

    def format_data(self, events, labels):
        """Creates dataframe from events and labels.

        Args:
            events (list): List of random inputs
            labels (list): List of class labels corresponding to inputs

        Returns:
            df (pd.DataFrame): Dataframe containing events and corresponding labels
        """

        df = pd.DataFrame(events)
        df['labels'] = labels
        return df   

    def load_model(self):
        """Loads trained model.

        Change directory to load different model.

        Returns:
            Sequential: Model loaded from directory
        """

        return load_model(f'{self.dir}/data/cnn_synthetic_augmented_user4.h5')

def main():
    """Generates synthetic data or tests trained model based on mode.

    generate: Generates synthetic dataset with 100000 data points
    test_keyboard: Tests trained model using keyboard number inputs to generate 
    inputs from inputs dictionary to make predictions
    test_sp: Tests trained model using live sip and puff data to make predictions
    """
    
    parser = argparse.ArgumentParser()
    parser.add_argument('mode', nargs='?', const='generate', default='generate', help='Selects whether data is generated or tested.')
    args = parser.parse_args()

    syn = Synthetic()

    if args.mode == 'generate':
        events, labels = syn.simulate(100000)
        data = syn.format_data(events, labels)

        data.to_csv(f'{syn.dir}/data/synthetic/synthetic_trial_data_range.csv')

    elif args.mode == 'test_keyboard':
        model = syn.load_model()[0]

        while True:
            print()
            num_pressed = int(input('Press a number 0-4. (Or 9 to exit.)\n'))

            if num_pressed == 9:
                break
            elif num_pressed > 4:
                print('Invalid number. Try again.')
                continue
            
            a = random.randint(1,115)
            data = a*syn.inputs[num_pressed]

            data = data.reshape(1, data.shape[0], 1)

            pred = model.predict(data)
            print('Prediction', pred)

    elif args.mode == 'test_sp':
        model = syn.load_model()
        
        
        exit = None
        accuracy_dict = {
            0:[0,0],
            1:[0,0],
            2:[0,0],
            3:[0,0],
            4:[0,0]
        }
        while exit != 'q':
            print()
            wait1 = input('Press a key to start data collection...\n')
            time.sleep(0.5)
            print()
            print('Collecting data...\n')
            print()

            counter = 0
            sensor_vals = []
            while len(sensor_vals) < 150:
                try:
                    events = get_gamepad()
                except:
                    print('*** No gamepad found. ***')
                    return
                for event in events:
                    if event.code == 'ABS_X':
                        sensor_vals.append(event.state)

            sensor_vals = np.array(sensor_vals)

            data = sensor_vals.reshape(1, sensor_vals.shape[0], 1)
            
            pred = np.argmax(model.predict(data), axis=1)

            plt.clear_figure()
            plt.plot(sensor_vals)
            plt.show()
            print(f'Sensor Values: {sensor_vals}\n')
            print(f'Prediction: {pred}\n')
            print()

            gt = int(input('Enter ground truth value: \n'))

            if pred[0] == gt:
                accuracy_dict[gt][1] += 1
            
            accuracy_dict[gt][0] += 1

            print()
            exit = input('Press Q to see results, or anything else to continue...\n')
            print()

        print('Accuracy by class:\n')
        for key in accuracy_dict.keys():
            correct = accuracy_dict[key][1]
            trials = accuracy_dict[key][0]

            if trials != 0:
                pct = round(correct/trials, 2)*100
                print(f'{key}: {correct}/{trials} ({pct}%)')
            else:
                print(f'{key}: {correct}/{trials}')

        

    else:
        print(f'{args.mode} is not a valid selection. Please try again.')

if __name__ == '__main__':
    main()


    
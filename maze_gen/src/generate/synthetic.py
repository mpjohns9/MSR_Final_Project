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

    def __init__(self):

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
        amp = random.randint(75, 115)
        event = random.randint(0, len(self.inputs.keys())-1)
        return amp*self.inputs[event], event

    def simulate(self, num_events):
        events = []
        labels = []
        for i in range(num_events):
            event, label = self.random_input()

            # # add noise to the nothing event
            # if label == 4:
            #     lower = random.randint(-5, 0)
            #     upper = random.randint(0, 5)
            #     event = np.array([e + random.randint(lower, upper) for e in event])

            # max = np.max(event)
            # min = np.min(event)
            # rng = max - min

            # event = np.concatenate((event, [max, min, rng]), axis=0)
            events.append(event)
            labels.append(label)

        return events, labels  

    def format_data(self, events, labels):
        df = pd.DataFrame(events)
        df['labels'] = labels
        return df   

    def load_model(self):
        return load_model(f'{self.dir}/data/cnn_synthetic_augmented_100000.h5')

def main():
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
            # max = np.max(data)
            # min = np.min(data)
            # rng = max - min
            # metrics = np.array([max, min, rng])

            # data = np.concatenate((data, [max, min, rng]), axis=0)
            data = data.reshape(1, data.shape[0], 1)
            # metrics = metrics.reshape(1, metrics.shape[0], 1)

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
            while len(sensor_vals) < 300:
                # print(counter)
            # while True:
                try:
                    events = get_gamepad()
                except:
                    print('*** No gamepad found. ***')
                    return
                for event in events:
                    if event.code == 'ABS_X':
                        sensor_vals.append(event.state)
                        # print(event.state)

                counter += 1
                # time.sleep(.005)

            # print(len(sensor_vals))
            sensor_vals = np.array(sensor_vals[::2])
            # max = np.max(sensor_vals)
            # min = np.min(sensor_vals)
            # rng = max - min
            # metrics = np.array([max, min, rng])

            # # sensor_vals = np.concatenate((sensor_vals, [max, min, rng]), axis=0)
            # metrics = metrics.reshape(1, metrics.shape[0], 1)
            data = sensor_vals.reshape(1, sensor_vals.shape[0], 1)
            
            # pred_metrics = model_metrics.predict(metrics)
            # pred_data = model_data.predict(data)
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


    
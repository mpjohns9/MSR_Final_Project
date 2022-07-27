import numpy as np
import pandas as pd
import random
import os
import argparse

from tensorflow.keras.models import load_model

class Synthetic:

    def __init__(self):
        
        self.x = np.linspace(0, np.pi*2, 150)

        self.puff_sip = np.sin(self.x)
        self.sip_puff = -self.puff_sip
        self.double_puff = np.abs(self.puff_sip)
        self.double_sip = -self.double_puff

        self.inputs = {
            0:self.double_sip,
            1:self.double_puff,
            2:self.puff_sip,
            3:self.sip_puff
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
            events.append(event)
            labels.append(label)
        return events, labels  

    def format_data(self, events, labels):
        df = pd.DataFrame(events)
        df['labels'] = labels
        return df      

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('mode', nargs='?', const='generate', default='generate', help='Selects whether data is generated or tested.')
    args = parser.parse_args()

    syn = Synthetic()
    dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    if args.mode == 'generate':
        events, labels = syn.simulate(10000)
        data = syn.format_data(events, labels)

        data.to_csv(f'{dir}/data/synthetic/synthetic_trial_data.csv')

    elif args.mode == 'test':
        model = load_model(f'{dir}/data/cnn_synthetic_v2.h5')

        while True:
            print()
            num_pressed = int(input('Press a number 0-3. (Or 9 to exit.)\n'))

            if num_pressed == 9:
                break
            elif num_pressed > 3:
                print('Invalid number. Try again.')
                continue
            
            a = random.randint(1,115)
            data = a*syn.inputs[num_pressed]
            data = data.reshape(1, data.shape[0], 1)

            pred = np.argmax(model.predict(data), axis=1)
            print('Prediction', pred)


    else:
        print(f'{args.mode} is not a valid selection. Please try again.')

if __name__ == '__main__':
    main()


    
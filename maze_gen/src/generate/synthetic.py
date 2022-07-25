import numpy as np
import pandas as pd
import random
import os
import argparse

class Synthetic:

    def __init__(self):
        
        self.x = np.linspace(0, np.pi*2, 150)
        self.amplitude = 100

        self.puff_sip = self.amplitude*np.sin(self.x)
        self.sip_puff = -self.puff_sip
        self.double_puff = self.amplitude*np.abs(self.puff_sip)
        self.double_sip = -self.double_puff

        self.inputs = {
            0:self.double_sip,
            1:self.double_puff,
            2:self.puff_sip,
            3:self.sip_puff
        }

    def random_input(self):
        event = random.randint(0, len(self.inputs.keys())-1)
        return self.inputs[event], event

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
    parser.add_argument('mode', help='Selects whether data is generated or tested.')
    args = parser.parse_args()

    syn = Synthetic()

    if args.mode == 'generate':
        events, labels = syn.simulate(1000)
        data = syn.format_data(events, labels)

        dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        data.to_csv(f'{dir}/data/synthetic/synthetic_trial_data.csv')

    elif args.mode == 'test':
        pass

    else:
        print('Invalid mode selected. Please try again.')

if __name__ == '__main__':
    main()


    
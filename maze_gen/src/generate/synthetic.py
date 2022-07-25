import numpy as np
import random

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
        event = random.randint(0, len(self.inputs.keys()))
        return self.inputs[event], event

    def simulate(self, num_events):
        events = []
        labels = []
        for i in range(num_events):
            event, label = self.random_input()
            events.append(event)
            labels.append(label)
        return events, labels        


    

def main():
    syn = Synthetic()
    events, labels = syn.simulate()

if __name__ == '__main__':
    main()


    
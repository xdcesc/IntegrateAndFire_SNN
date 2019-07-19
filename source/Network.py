from enum import Enum


class Network:

    def __init(self):
        self.number_of_neurons = 5
        self.number_of_inputs = 1
        self.neurons = Neuron[5]
        #for x in range(5):
        #    self.neurons[x] = Neuron(None, )


class NeuronType(Enum):
    Excitatory = 0
    Inhibitory = 1


class Neuron:

    def __init__(self, outputs, leak_rate, spike_threshold,
                 spike_voltage, refractory_period, neuron_type, resting_voltage):
        self.input_synapse = Synapse(0.0)
        self.outputs = outputs
        self.leak_rate = leak_rate
        self.spike_threshold = spike_threshold
        self.current_voltage = 0.0
        self.can_spike = True
        self.spike_voltage = spike_voltage
        self.cycles_waited = 0
        self.refractory_period = refractory_period
        self.neuron_type = neuron_type
        self.resting_voltage = resting_voltage

    def cycle(self):
        if not self.can_spike:
            self.cycles_waited += 1
            if self.cycles_waited >= self.refractory_period:
                self.can_spike = True
                self.cycles_waited = 0
        self.receive_voltage()
        self.leak()
        self.spike()

    def receive_voltage(self):
        self.current_voltage += self.input_synapse.get_voltage()

    def leak(self):
        self.current_voltage -= self.leak_rate
        if self.current_voltage < self.resting_voltage:
            self.current_voltage = self.resting_voltage

    def spike(self):
        if self.can_spike and self.current_voltage >= self.spike_threshold:
            for output in self.outputs:
                if self.neuron_type == NeuronType.Excitatory:
                    output.send_spike(Spike(self.spike_voltage))
                else:
                    output.send_spike(Spike(self.spike_voltage * (-1)))
            self.can_spike = False


class NeuronConnector:

    def __init__(self, weight, length, output, spikes):
        self.weight = weight
        self.length = length
        self.output = output
        self.spikes = spikes

    def cycle(self):
        for x in range(self.length - 1, -1, -1):
            if x == self.length - 1 and self.spikes[x] is not None:
                self.output.GiveSpike(self.spikes[x])
                self.spikes[x] = None
            elif self.spikes[x] is not None:
                self.spikes[x + 1] = self.spikes[x]
                self.spikes[x] = None

    def send_spike(self, spike):
        self.spikes[0] = spike


class Synapse:

    def __init__(self, current_voltage):
        self.current_voltage = current_voltage

    def give_spike(self, spike):
        self.current_voltage += spike.voltage

    def get_voltage(self):
        temp = self.current_voltage
        self.current_voltage = 0
        return temp


class Spike:

    def __init__(self, voltage):
        self.voltage = voltage


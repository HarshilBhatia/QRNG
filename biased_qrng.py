
from collections import defaultdict
import time
from dwave.system.samplers import DWaveSampler
import numpy as np
from matplotlib import pyplot as plt
import neal
import pandas as pd
from pyqubo import Array, Placeholder, solve_qubo, Constraint
from dwave.system.composites import EmbeddingComposite, FixedEmbeddingComposite
from dimod import AdjVectorBQM

isQPU = 1
Advantage = 1

for N in [4950]:
    if isQPU:
        print("QPU")
        if Advantage:
            print("Advantage")
            qpu = DWaveSampler(solver={'qpu': True, 'topology__type': 'pegasus'})
        else:
            print("Chimera")
            qpu = DWaveSampler(solver={'qpu': True, 'topology__type': 'chimera'})
        sampler = EmbeddingComposite(qpu)     
    else :
        print("SA")
        sampler = neal.SimulatedAnnealingSampler()

    l = {}

    x = Array.create("vector", N, "BINARY")
    for bias in [0.1,0.15,0.2]:        
        H = x[0] - x[0]
        for i in range(N):
            H += bias*(x[i])

        model = H.compile()
        qubo,offset = model.to_qubo()
        
        for itr in range(samples):
            response = sampler.sample_qubo(qubo, num_reads = 1,annealing_time = 1,auto_scale = False) 
            l = np.append(l,(np.array(response.to_pandas_dataframe().drop(columns = ['energy','num_occurrences']))).flatten())

        if Advantage == 1:
            pd.DataFrame(l).to_csv("pegasus_qubits={}_bias={}.csv".format(N,bias))

        else:
            pd.DataFrame(l).to_csv("chimera_qubits={}_bias={}.csv".format(N,bias))
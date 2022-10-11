
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
    mean = {}
    stderr = {}


    x = Array.create("vector", N, "BINARY")
    H = x[0] - x[0]

    for i in range(N):
        H +=(x[i]-x[i])

    model = H.compile()

    qubo,offset = model.to_qubo()

    response = sampler.sample_qubo(qubo, num_reads = 1, annealing_time = 1,       \
                                    return_embedding = True)
    embedding = response.info['embedding_context']['embedding']

    fixed_sampler = FixedEmbeddingComposite(qpu, embedding = embedding)

    for b in range(-100,101,2):
        H = x[0] - x[0]
        bias = b/100
        for i in range(N):
            H += bias*(x[i])

        if(b == 0):
            for i in range(N):
                H += (x[i]-x[i])

        model = H.compile()
        qubo,offset = model.to_qubo()
        response = fixed_sampler.sample_qubo(qubo, num_reads = 1000,annealing_time = 1,auto_scale = False)
        npx = np.array(response.to_pandas_dataframe().drop(columns = ['chain_break_fraction','energy']))
        y = np.zeros(N)
        for j in range(npx.shape[0]):
            for k in range(N):
                y[k] += npx[j,k]*npx[j,N]
        
        mean[bias] = [np.mean(y)]
        stderr[bias] = [np.std(y)]
        l[bias] = y

    pd.DataFrame(l).to_csv("1000_peg_all_bias_values.csv")
    pd.DataFrame(mean).to_csv("1000_peg_mean_values.csv")
    pd.DataFrame(stderr).to_csv("1000_peg_stderr_values.csv")

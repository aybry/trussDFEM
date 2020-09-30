import numpy as np

data1 = np.array([[-165.801e-06, -33.16e+06, -166.667e-06, -33.3333e+06],
[-166.473e-06, -33.295e+06, -166.667e-06, -33.3333e+06],
[-233.293e-06, -46.659e+06, -233.333e-06, -46.6667e+06],
[-231.966e-06, -46.393e+06, -233.333e-06, -46.6667e+06],
[208.963e-06, 41.793e+06, 208.319e-06, 41.6638e+06],
[266.885e-06, 53.377e+06, 266.667e-06, 53.3333e+06],
[266.746e-06, 53.349e+06, 266.667e-06, 53.3333e+06],
[292.541e-06, 58.508e+06, 291.687e-06, 58.3374e+06],
[-49.806e-06, -9.961e+06, -50.0000e-06, -10.0000e+06],
[0.001e-06, 0.0e+06, 2.44485e-12, 488.970e-03],
[-149.806e-06, -29.961e+06, -150.000e-06, -30.e+06],
[-124.839e-06, -24.968e+06, -125.009e-06, -25.0017e+06],
[-41.599e-06, -8.32e+06, -41.6638e-06, -8.33276e+06]])

data2 = np.array([[-83.841e-06, -16.768e+06, -83.8525e-06, -16.7705e+06],
[-83.352e-06, -16.67e+06, -83.8526e-06, -16.7705e+06],
[76.958e-06, 15.392e+06, 76.0345e-06, 15.2069e+06],
[0.173e-06, 0.035e+06, 2.12132e-12, 424.264e-03],
[0.062e-06, 0.012e+06, -905.307e-15, -181.061e-03],
[76.039e-06, 15.208e+06, 76.0345e-06, 15.2069e+06],
[76.14e-06, 15.228e+06, 76.0345e-06, 15.2069e+06],
[0.003e-06, 0.001e+06, -3.60138e-12, -720.277e-03]])

data3 = np.array([[18.822e-06, 3.764e+06, 18.7500e-06, 3.75000e+06],
[18.755e-06, 3.751e+06, 18.7500e-06, 3.75000e+06],
[20.968e-06, 4.194e+06, 20.9631e-06, 4.19263e+06],
[20.976e-06, 4.195e+06, 20.9631e-06, 4.19263e+06],
[20.976e-06, 4.195e+06, 20.9631e-06, 4.19263e+06],
[20.968e-06, 4.194e+06, 20.9631e-06, 4.19263e+06],
[18.755e-06, 3.751e+06, 18.7500e-06, 3.75000e+06],
[18.822e-06, 3.764e+06, 18.7500e-06, 3.75000e+06],
[-67.532e-06, -13.506e+06, -67.6041e-06, -13.5208e+06],
[-56.335e-06, -11.267e+06, -56.3367e-06, -11.2673e+06],
[-56.32e-06, -11.264e+06, -56.3367e-06, -11.2673e+06],
[-67.597e-06, -13.519e+06, -67.6041e-06, -13.5208e+06],
[0.009e-06, 0.002e+06, 1.88668e-12, 377.336e-03],
[-20.958e-06, -4.192e+06, -20.9631e-06, -4.19263e+06],
[0.002e-06, 0.0e+06, 5.61250e-12, 1.12250],
[0.002e-06, 0.0e+06, 6.66250e-12, 1.33250],
[-20.958e-06, -4.192e+06, -20.9631e-06, -4.19263e+06],
[0.009e-06, 0.002e+06, 1.88668e-12, 377.337e-03],
[-67.597e-06, -13.519e+06, -67.6041e-06, -13.5208e+06],
[-56.32e-06, -11.264e+06, -56.3367e-06, -11.2673e+06],
[-56.335e-06, -11.267e+06, -56.3367e-06, -11.2673e+06],
[-67.532e-06, -13.506e+06, -67.6041e-06, -13.5208e+06],
[0.029e-06, 0.006e+06, -1.88668e-12, -377.336e-03],
[0.001e-06, 0.0e+06, -7.19734e-12, -1.43947],
[0.001e-06, 0.0e+06, -7.19735e-12, -1.43947],
[0.029e-06, 0.006e+06, -1.88668e-12, -377.336e-03]])

data = data3
diffStrain = []
diffStress = []
errStrain = []
errStress = []
i = 0
while i <= np.shape(data)[0]-1:
    diffStrain.append(data[i,0] - data[i,2])
    diffStress.append(data[i,1] - data[i,3])
    errStrain.append(diffStrain[i]/data[i,2])
    errStress.append(diffStress[i]/data[i,3])
    print(i, errStrain[i])
    i+=1
# print (diff)
print (np.sort(np.abs(errStrain)))
print (np.sort(np.abs(errStress)))
print (np.max(np.abs(errStrain)))
print (np.max(np.abs(errStress)))
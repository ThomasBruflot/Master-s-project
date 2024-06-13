

timestep_40 = [  5.5306, -60.0498,  -2.2848,  18.9086,  -0.9030,  -9.4049,  15.9313,
          21.1650,  18.1411,  -1.0930,  13.9233,  37.7616,   4.3612,  32.6777,
          10.3959,  38.2457,   5.7137,  41.8462,  51.7613,  28.5787,   7.1693,
          -9.9465,  49.9978,   7.4585,  15.0919,  -0.1118,   0.6733,  24.1360,
          36.5450,  36.0498,  24.0423,  58.8811,  18.3943,  -3.9517,  34.4023,
           8.1575,  28.6699,  26.8916,  34.7755,  44.6397,  29.6046,  30.3362,
          44.2452,  24.6636,  33.1318,  14.4074,  38.4007,  59.2200,  -9.6108,
          -1.8266,   3.4970,   1.5648,  -9.8176,  10.8114,  41.4140,  28.9641,
          33.9094,  30.6709,  -2.9754,  24.1349,  67.6564,   9.8437,  19.7833,
          17.3406,   3.8108,  17.6116,  62.1320,  66.2487,  -8.0178,  24.4374,
          29.6979,  23.2112,  43.8866,  -2.2145,  -6.8453,  29.3880,  19.7454,
          16.5685,  29.3661,  19.8164,  43.3410,  48.4364,  31.4217,  53.8204,
          27.3427,  30.6640,  67.5072,   8.6647,  50.0333,  24.2016,  -3.5696,
          31.9390,  27.7022,  16.7246,   8.6594,  45.0373,  -8.2128,  -9.6437,
          32.0222,  16.5920]

timestep_41 = [-112.1456,  -60.0990, -121.0234,  -99.4201, -118.4848, -127.9948,
         -102.3381,  -96.2886,  -98.8941, -118.5937, -103.6297,  -79.9235,
         -113.9936,  -84.4693, -107.2870,  -78.7033, -112.5415,  -74.9271,
          -65.8404,  -89.7621, -111.4738, -128.0686,  -67.3382, -110.6168,
         -102.9178, -118.8474, -117.3031,  -93.9916,  -80.9113,  -81.1501,
          -93.5605,  -58.4594,  -99.2885, -121.6955,  -83.2791, -109.5677,
          -88.3272,  -89.9765,  -82.7898,  -72.1472,  -87.6901,  -86.6516,
          -72.4851,  -92.1289,  -84.4478, -102.8253,  -79.9012,  -58.3696,
         -127.9450, -120.0164, -114.9926, -116.8011, -128.0407, -107.3246,
          -75.8634,  -87.8768,  -83.6028,  -86.9395, -120.1937,  -93.2096,
          -48.9515, -108.7342,  -97.7644, -100.7949, -115.2673, -100.2672,
          -55.0596,  -51.2813, -127.7232,  -93.4169,  -87.4229,  -93.7128,
          -73.1549, -120.1022, -124.9714,  -88.2141,  -97.9064, -101.4889,
          -88.1088,  -97.3230,  -74.0975,  -68.5472,  -85.5413,  -63.7240,
          -90.7374,  -86.0699,  -49.5163, -108.9956,  -66.5941,  -93.4475,
         -122.2909,  -85.7539,  -90.2365, -100.6824, -109.8793,  -71.6382,
         -127.4034, -128.8207,  -85.5503, -100.7871]

for i in range(len(timestep_40)):
    #print("Neuron: ", i, "Voltage difference: ", timestep_41[i]-timestep_40[i])
    if (timestep_41[i]-timestep_40[i] > -100):
        print("Neuron: ", i, "Voltage difference: ", timestep_41[i]-timestep_40[i])

timestep_42 = [-109.1579,  -60.1478, -117.3111,  -96.0490, -115.4286, -125.7800,
          -98.1129,  -93.4224,  -95.2859, -115.2144, -101.1972,  -76.9857,
         -110.5479,  -79.8750, -103.2423,  -74.3706, -110.4015,  -70.9165,
          -62.4956,  -86.3064, -107.8917, -125.6946,  -62.1309, -107.0515,
          -98.7521, -115.0004, -114.6956,  -90.1283,  -76.7327,  -77.3229,
          -89.4209,  -53.8153,  -95.8853, -118.3332,  -78.0879, -106.7848,
          -84.5102,  -85.4069,  -77.8080,  -66.9675,  -83.4350,  -81.8865,
          -67.8699,  -87.8753,  -80.5794,  -98.8246,  -77.6381,  -55.2082,
         -125.8548, -117.7374, -111.4015, -113.2838, -125.8660, -103.6078,
          -72.2461,  -83.7872,  -80.6346,  -82.1801, -117.2435,  -90.0610,
          -43.1731, -105.1274,  -93.8245,  -96.5283, -113.0214,  -95.9725,
          -51.0390,  -47.1254, -126.3371,  -89.1565,  -83.5674,  -89.3726,
          -69.5425, -118.0536, -123.3464,  -85.4068,  -94.9517,  -99.2737,
          -84.8274,  -93.6086,  -70.4424,  -63.3236,  -81.5669,  -60.6621,
          -87.7693,  -81.9785,  -42.6659, -105.0696,  -61.8084,  -90.5675,
         -118.8018,  -82.0003,  -85.5173,  -96.2425, -105.9643,  -66.1427,
         -124.9598, -126.1253,  -82.0961,  -97.3439]
timestep_43 = [-106.8386,  -60.1961, -116.2653,  -93.8132, -112.9443, -122.9481,
          -96.4186,  -91.2888,  -93.1163, -112.9218,  -98.6271,  -74.2111,
         -108.8927,  -77.1529, -100.6859,  -72.1623, -107.9229,  -68.4550,
          -59.7343,  -84.3947, -106.3489, -123.2661,  -59.5924, -104.8141,
          -96.9017, -113.6827, -112.2839,  -87.7436,  -74.5036,  -74.8530,
          -86.6631,  -50.9394,  -93.4786, -116.1738,  -75.4986, -104.2445,
          -82.4494,  -82.7299,  -75.7229,  -64.2200,  -80.5778,  -79.2004,
          -65.3904,  -85.4304,  -78.4362,  -96.4556,  -74.7851,  -52.5916,
         -123.1470, -115.0112, -110.0429, -111.7406, -123.4902, -101.6486,
          -69.1651,  -81.8138,  -78.4564,  -80.0023, -114.5290,  -87.7035,
          -40.2060, -103.4288,  -91.6213,  -94.8153, -111.3284,  -93.4758,
          -48.8901,  -44.6103, -124.9367,  -86.9698,  -80.6947,  -86.8395,
          -67.3833, -115.2607, -120.9136,  -82.6810,  -92.7104,  -96.6553,
          -82.7569,  -91.6643,  -68.3463,  -60.7181,  -78.8309,  -58.6977,
          -84.9234,  -79.4072,  -40.2677, -103.3679,  -58.5489,  -87.9101,
         -117.7155,  -79.9753,  -83.4608,  -93.5636, -104.4964,  -63.9886,
         -123.5895, -124.8424,  -79.7530,  -94.9897]

timestep_44 = [-102.8629,  -60.2439, -113.5592,  -90.6316, -109.4172, -120.0657,
          -93.5790,  -87.3908,  -89.3478, -109.0663,  -94.0681,  -69.7099,
         -106.5962,  -73.4474,  -97.3150,  -67.5945, -104.0509,  -63.8618,
          -55.7506,  -80.0504, -103.7259, -120.2794,  -55.6459, -102.0870,
          -94.4789, -111.1078, -108.6361,  -85.1630,  -70.3075,  -70.9645,
          -82.5517,  -46.2401,  -89.6069, -112.8035,  -72.2144, -100.5389,
          -78.1084,  -78.8168,  -72.8369,  -59.9790,  -76.5832,  -75.1954,
          -60.7850,  -81.4436,  -74.5825,  -92.8227,  -70.7607,  -48.0811,
         -120.1375, -111.6677, -107.6924, -109.5870, -120.5383,  -99.3284,
          -65.0917,  -77.5224,  -74.4376,  -77.0742, -110.8778,  -84.0845,
          -35.4430, -100.8657,  -87.9328,  -92.3106, -108.6515,  -90.0629,
          -44.2752,  -40.1471, -122.4608,  -84.2638,  -76.3605,  -82.9256,
          -62.5755, -111.9358, -117.2709,  -78.7141,  -89.2031,  -92.2410,
          -78.3250,  -87.9248,  -64.2602,  -56.9876,  -73.7651,  -53.9441,
          -81.4496,  -75.1926,  -36.1209,  -99.4750,  -53.9625,  -83.9355,
         -114.6355,  -76.4560,  -80.3344,  -90.0943, -101.8316,  -58.8299,
         -121.1294, -122.3579,  -76.2558,  -91.3820]


print(timestep_41[1]-timestep_40[1])
print(timestep_42[1]-timestep_41[1])
print(timestep_43[1]-timestep_42[1])
print(timestep_44[1]-timestep_43[1])

print("The voltage levels for the neuron that spiked:")

print(timestep_40[1])
print(timestep_41[1])
print(timestep_42[1])
print(timestep_43[1])
print(timestep_44[1])

print("Let us look at some of the decay here.")
print("Timestep decay from formula: ", (timestep_40[1]+60)*0.99, " - Next voltage reading", timestep_41[1])
print(timestep_41[1]*0.99, " ", timestep_42[1])
print(timestep_42[1]*0.99, " ", timestep_43[1])
print(timestep_43[1]*0.99, " ", timestep_44[1])



import yaml
import numpy as np

pars_dict = {'Default': (10,0.2,0.2,[-0.3], [0], 0.15, 0), '5838.37': (10, 0.15, 0.15, [-0.3], [0], 0.15, 0), '7189.16': (10, 0.23, 0.1, [-0.3], [0], 0.15, 0),
                 '5712.13': (10, 0.5, 0.2, [-0.3, -0.3], [0, -0.2], 0.15, 0),
                 '5698.02': (10, 0.25, 0.7, [-0.3, -0.5], [0, 0.2], 0.15, 0),
                 '5284.1': (10, 1, 0.4, [-0.3, -0.7, -0.3], [0, -0.3, 0.2], 0.15, 0),
                 '5536.58': (10, 0.1, 0.2, [-0.3], [0], 0.15, 0),
                 '5325.56': (10, 0.4, 0.18, [-0.3, -0.1], [0, -0.25], 0.15, 0),
                 '5837.7': (10, 0.55, 0.45, [-0.3, -0.1, -0.2], [0, -0.37, 0.395], 0.15, 0),
                 '5577.03': (10, 0.18, 0.15, [-0.3], [0], 0.15, 0), '5807.78': (10, 0.15, 0.15, [-0.3], [0], 0.15, 0),
                 '6699.15': (10, 0.17, 0.17, [-0.3], [0], 0.15, 0),
                 '5636.7': (10, 0.15, 0.67, [-0.2, -0.3], [0, 0.4], 0.15, 0),
                 '5635.82': (10, 0.18, 0.6, [-0.3, -0.1], [0, 0.4], 0.15, 0),
                 '5691.50': (10, 0.2, 0.12, [-0.3], [0], 0.15, 0), '6481.87': (10, 0.2, 0.13, [-0.3], [0], 0.15, 0),
    '5052.167': (10, 0.3, 0.15, [-0.15,-0.5], [0,-0.1], 0.15, 0),
    '5380.337': (10, 0.3, 0.15, [-0.3], [0], 0.15, 0),
    '7111.47': (10, 0.3, 0.15, [-0.3], [0], 0.15, 0),
    '6300.311': (10, 0.3, 0.4, [-0.3,-0.3], [0,0.25], 0.15, 0),
    '5148.838': (10, 0.15, 0.35, [-0.3,-0.3], [0,0.25], 0.15, 0),
    '6696.018': (10, 0.3, 0.15, [-0.3], [0], 0.15, 0),
    '8773.896': (10, 0.15, 0.15, [-0.3], [0], 0.15, 0),
    '7835.309': (10, 0.15, 0.15, [-0.3], [0], 0.15, 0),
    '5645.611': (10, 0.3, 0.4, [-0.3,-0.1], [0,0.15], 0.15, 0),
    '6125.021': (10, 0.15, 0.15, [-0.3], [0], 0.15, 0),
    '6741.63': (10, 0.3, 0.35, [-0.3,-0.1], [0,0.15], 0.15, 0),
    '5512.98': (10, 0.15, 0.15, [-0.3], [0], 0.15, 0),
    '5590.114': (10, 0.15, 0.15, [-0.3], [0], 0.15, 0),
    '6439.08': (10, 0.15, 0.15, [-0.3], [0], 0.15, 0),
    '6169.042': (10, 0.15, 0.15, [-0.3], [0], 0.15, 0),
    '6499.65': (10, 0.15, 0.15, [-0.3], [0], 0.15, 0),
    '5260.387': (10, 0.15, 0.15, [-0.3], [0], 0.15, 0),
    '6493.78': (10, 0.3, 0.5, [-0.3,-0.3], [0,0.4], 0.15, 0),
    '6471.662': (10, 0.6, 0.3, [-0.3,-0.2], [0,-0.4], 0.15, 0),
    '5581.965': (10, 0.3, 0.6, [-0.3,-0.2], [0,0.3], 0.15, 0),
    '5671.821': (10, 0.6, 0.15, [-0.3,-0.2], [0,-0.4], 0.15, 0),
    '5081.57': (10, 0.7, 0.4, [-0.3,-0.2,-0.3], [0,-0.4,0.2], 0.15, 0),
    '5657.87': (10, 0.15, 0.15, [-0.3], [0], 0.15, 0),
    '6604.578': (10, 0.15, 0.15, [-0.3], [0], 0.15, 0),
    '6320.843': (10, 0.15, 0.15, [-0.3], [0], 0.15, 0),
    '6245.63': (10, 0.15, 0.15, [-0.3], [0], 0.15, 0),
    '5684.19': (10, 0.3, 0.6, [-0.3,-0.3], [0,0.3], 0.15, 0),
    '5526.82': (10, 0.3, 0.15, [-0.3], [0], 0.15, 0),
    '6279.76': (10, 0.15, 0.15, [-0.3], [0], 0.15, 0),
    '5295.774': (10, 0.15, 0.15, [-0.3], [0], 0.15, 0),
    '6258.104': (10, 0.15, 0.15, [-0.3], [0], 0.15, 0),
    '5866.452': (10, 0.5, 0.3, [-0.3,-0.1], [0,-0.3], 0.15, 0),
    '6554.22': (10, 0.6, 0.3, [-0.3,-0.1], [0,-0.3], 0.15, 0),
    '6556.06': (10, 0.2, 0.2, [-0.3], [0], 0.15, 0),
    '5219.7': (10, 0.3, 0.8, [-0.3,-0.3], [0,0.6], 0.15, 0),
    '6126.217': (10, 0.15, 0.15, [-0.3], [0], 0.15, 0),
    '5147.479': (10, 0.15, 0.15, [-0.3], [0], 0.15, 0),
    '5113.448': (10, 0.6, 0.3, [-0.3,-0.3], [0,-0.2], 0.15, 0),
    '5022.871': (10, 0.3, 0.9, [-0.3,-0.3,-0.3], [0,0.3,0.6], 0.15, 0),
    '4913.616': (10, 0.3, 0.6, [-0.3,-0.3], [0,0.3], 0.15, 0),
    '5490.15': (10, 0.5, 0.3, [-0.3,-0.3], [0,-0.3], 0.15, 0),
    '5739.464': (10, 0.6, 0.8, [-0.3,-0.3], [0,0.3], 0.15, 0),
    '5336.778': (10, 0.45, 0.3, [-0.3,-0.3], [0,-0.4], 0.15, 0),
    '5418.767': (10, 0.3, 0.7, [-0.3,-0.3], [0,0.4], 0.15, 0),
    '5381.015': (10, 0.5, 0.3, [-0.3,-0.3], [0,-0.4], 0.15, 0),
    '6606.97': (10, 0.3, 0.6, [-0.3,-0.3], [0,0.4], 0.15, 0),
    '5211.54': (10, 0.5, 0.4, [-0.3,-0.3,-0.1], [0,-0.4,0.4], 0.15, 0),
    '4911.193': (10, 0.3, 0.5, [-0.3,-0.3], [0,0.4], 0.15, 0),
    '4874.014': (10, 0.5, 0.5, [-0.3,-0.3,-0.3], [0,-0.4,0.4], 0.15, 0),
    '4865.611': (10, 0.15, 0.15, [-0.3], [0], 0.15, 0),
    '6251.82': (10, 0.15, 0.15, [-0.3], [0], 0.15, 0),
    '6357.292': (10, 0.15, 0.15, [-0.3], [0], 0.15, 0),
    '6531.415': (10, 0.6, 0.9, [-0.3,-0.1,-0.3], [0,-0.1,0.7], 0.15, 0),
    '6785.008': (10, 0.15, 0.15, [-0.3], [0], 0.15, 0),
    '6119.528': (10, 0.3, 0.4, [-0.3,-0.1], [0,0.2], 0.15, 0),
    '6199.2': (10, 0.3, 0.5, [-0.3,-0.1], [0,0.3], 0.15, 0),
    '6090.21': (10, 0.15, 0.15, [-0.3], [0], 0.15, 0),
    '6039.73': (10, 0.8, 0.5, [-0.3,-0.1,-0.3], [0,0.3,-0.4], 0.15, 0),
    '6081.44': (10, 0.15, 0.6, [-0.3,-0.1], [0,0.3], 0.15, 0),
    '4875.486': (10, 0.15, 0.6, [-0.3,-0.1], [0,0.3], 0.15, 0),
    '5670.85': (10, 0.6, 0.15, [-0.3,-0.1], [0,-0.4], 0.15, 0),
    '5727.046': (10, 0.15, 0.15, [-0.3], [0], 0.15, 0),
    '4936.335': (10, 0.15, 0.5, [-0.3,-0.3], [0,0.3], 0.15, 0),
    '5214.14': (10, 0.6, 0.2, [-0.3,-0.3], [0,-0.3], 0.15, 0),
    '6661.08': (10, 0.3, 0.4, [-0.3,-0.3], [0,0.2], 0.15, 0),
    '5238.964': (10, 0.6, 0.5, [-0.3,-0.1,-0.3], [0,0.3,-0.4], 0.15, 0),
    '5247.566': (10, 0.7, 0.6, [-0.3,-0.1,-0.3], [0,0.3,-0.4], 0.15, 0),
    '5272.007': (10, 0.2, 0.6, [-0.3,-0.1], [0,0.3], 0.15, 0),
    '5287.2': (10, 0.35, 0.7, [-0.3,-0.1], [0,0.3], 0.15, 0),
    '5296.691': (10, 0.15, 0.15, [-0.3], [0], 0.15, 0),
    '5348.312': (10, 0.15, 0.3, [-0.3], [0], 0.15, 0),
    '5300.744': (10, 0.3, 0.5, [-0.3,-0.1], [0,0.4], 0.15, 0),
    '5783.87': (10, 0.15, 0.3, [-0.3], [0], 0.15, 0),
    '5783.08': (10, 0.15, 0.3, [-0.3], [0], 0.15, 0),
    '5237.328': (10, 0.15, 0.15, [-0.3], [0], 0.15, 0),
    '5246.767': (10, 0.4, 0.5, [-0.3,-0.1], [-0.1,0.3], 0.15, 0),
    '5502.067': (10, 0.15, 0.15, [-0.3], [0], 0.15, 0),
    '5305.87': (10, 0.15, 0.15, [-0.3], [0], 0.15, 0),
    '5308.41': (10, 0.3, 0.4, [-0.3,-0.3], [0,0.3], 0.15, 0),
    '6016.64': (10, 0.3, 0.65, [-0.3,-0.3], [0,0.4], 0.15, 0),
    '6013.49': (10, 0.6, 0.65, [-0.3,-0.3,-0.3], [0,0.4,-0.3], 0.15, 0),
    '5004.891': (10, 0.3, 0.4, [-0.1,-0.2], [0,0.4], 0.15, 0),
    '5212.691': (10, 0.7, 0.5, [-0.3,-0.2,-0.3], [0,-0.5,0.3], 0.15, 0),
    '6814.942': (10, 0.15, 0.15, [-0.3], [0], 0.15, 0),
    '5247.911': (10, 0.55, 0.15, [-0.3,-0.3], [0,-0.4], 0.15, 0),
    '5301.039': (10, 0.5, 0.15, [-0.3,-0.3], [0,-0.4], 0.15, 0),
    '5483.352': (10, 0.5, 0.3, [-0.3,-0.3], [0,-0.4], 0.15, 0),
    '5530.774': (10, 0.5, 0.3, [-0.3,-0.3], [0,-0.4], 0.15, 0),
    '5342.695': (10, 0.3, 0.4, [-0.3,-0.3], [0,0.3], 0.15, 0),
    '6189.0': (10, 0.3, 0.5, [-0.3,-0.3], [0,0.3], 0.15, 0),
    '6223.984': (10, 0.3, 0.3, [-0.3], [0], 0.15, 0),
    '5176.56': (10, 0.3, 0.5, [-0.3,-0.3], [0,0.3], 0.15, 0),
    '6643.63': (10, 0.15, 0.15, [-0.3], [0], 0.15, 0),
    '6176.811': (10, 0.15, 0.15, [-0.3], [0], 0.15, 0),
    '5643.078': (10, 0.6, 0.5, [-0.3,-0.3,-0.3], [0,0.3,-0.5], 0.15, 0),
    '6130.135': (10, 0.8, 0.5, [-0.3,-0.3,-0.3], [0,0.3,-0.5], 0.15, 0),
    '6204.604': (10, 0.3, 0.8, [-0.3,-0.3], [0,0.6], 0.15, 0),
    '6586.33': (10, 0.3, 0.5, [-0.3,-0.1], [0,0.4], 0.15, 0),
    '6532.89': (10, 0.7, 0.3, [-0.3,-0.1], [0,-0.5], 0.15, 0),
    '7727.624': (10, 0.3, 0.8, [-0.3,-0.1], [0,0.6], 0.15, 0),
    '5589.358': (10, 0.2, 0.3, [-0.3], [0], 0.15, 0),
    '6086.282': (10, 0.15, 0.15, [-0.3], [0], 0.15, 0),
    '6772.315': (10, 0.3, 0.2, [-0.3], [0], 0.15, 0),
    '6378.25': (10, 0.3, 0.15, [-0.3], [0], 0.15, 0),
    '6108.116': (10, 0.15, 0.15, [-0.3], [0], 0.15, 0),
    '6327.6': (10, 0.3, 0.3, [-0.3], [0], 0.15, 0),
    '6767.772': (10, 0.3, 0.15, [-0.3], [0], 0.15, 0),
    '5010.938': (10, 0.3, 0.4, [-0.3,-0.1], [0,0.3], 0.15, 0),
    '6177.242': (10, 0.7, 0.5, [-0.3,-0.1,-0.3], [0,0.35,-0.5], 0.15, 0),
    '5220.066': (10, 0.7, 0.4, [-0.3,-0.3,-0.3], [0,0.2,-0.4], 0.15, 0),
    '5218.197': (10, 0.6, 0.4, [-0.3,-0.3,-0.3], [0,0.3,-0.2], 0.15, 0),
    '7933.13': (10, 0.4, 0.8, [-0.3,-0.3], [0,0.4], 0.15, 0),
    '5105.541': (10, 0.7, 0.3, [-0.3,-0.2], [0,-0.4], 0.15, 0),
    '6362.35': (10, 0.85, 0.85, [-0.3,-0.2,-0.3], [0,0.5,-0.4], 0.15, 0),
    '6435.004': (10, 0.6, 0.3, [-0.3,-0.2], [0,-0.4], 0.15, 0),
    '5087.42': (10, 0.6, 0.3, [-0.3,-0.2], [0,-0.4], 0.15, 0),
    '4900.11': (10, 0.9, 0.3, [-0.3,-0.2,-0.3], [0,-0.2,-0.7], 0.15, 0),
    '4883.685': (10, 0.5, 0.6, [-0.3,-0.2,-0.1], [0,0.4,-0.3], 0.15, 0),
    '5200.413': (10, 0.5, 0.3, [-0.3,-0.2], [0,-0.3], 0.15, 0),
    '6127.46': (10, 0.3, 0.15, [-0.3], [0], 0.15, 0),
    '6141.71': (10, 0.15, 0.15, [-0.3], [0], 0.15, 0),
    '6496.9': (10, 0.7, 0.15, [-0.3,-0.2], [0,-0.5], 0.15, 0),
    '5303.53': (10, 0.5, 0.15, [-0.3,-0.2], [0,-0.4], 0.15, 0),
    '6390.477': (10, 0.15, 0.15, [-0.3], [0], 0.15, 0),
    '5274.229': (10, 0.3, 0.5, [-0.3,-0.2], [0,0.2], 0.15, 0),
    '5319.81': (10, 0.3, 0.5, [-0.3,-0.2], [0,0.2], 0.15, 0),
    '5234.19': (10, 0.6, 0.2, [-0.3,-0.2], [0,-0.5], 0.15, 0),
    '5293.16': (10, 0.15, 0.5, [-0.3,-0.2], [0,0.2], 0.15, 0),
    '6645.1': (10, 0.3, 0.5, [-0.3,-0.2], [0,0.2], 0.15, 0),
    '6156.76': (10, 0.6, 0.3, [-0.1,-0.1,-0.3], [0,-0.2,-0.5], 0.15, 0)}

rounded_pars_dict = {}
for line in pars_dict:
    line_pars = pars_dict[line]
    if line != "Default":
        rounded_line = np.round(float(line),2)
        rounded_pars_dict[str(rounded_line)] = line_pars
    else:
        rounded_pars_dict[str(line)] = line_pars
    
with open('line_pars.yml', 'w') as outfile:
    yaml.dump(rounded_pars_dict, outfile, default_flow_style=False)
import pickle
import time
import tqdm

import numpy as np
import torch

from data import create_dataloader
from models import create_model
from IPython.display import display
from PIL import Image
import torchvision.transforms as transforms
from utils.util import save_image, tensor2im

#Get the dataloader for evaluation
with open('opts/opt_full.pkl', 'rb') as f:
    opt = pickle.load(f)
dataloader = create_dataloader(opt)

#Get the original full model
with open('opts/opt_full.pkl', 'rb') as f:
    opt = pickle.load(f)
model_full = create_model(opt, verbose=False)
model_full.setup(opt, verbose=False)

transform_list = [transforms.ToTensor(), transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))]
transform = transforms.Compose(transform_list)
print('             Input                        Original                        Ground-truth')
A_dir = 'imgs/maps/A'
B_dir = 'imgs/maps/B'

files = os.listdir(A_dir)
for file in files:
    if not file.endswith('.PNG'):
        continue
    base = file.split('.')[0]
    A_path = os.path.join(A_dir, file)
    B_path = os.path.join(B_dir, file)
    A_img = Image.open(A_path).convert('RGB')
    input = transform(A_img).to('cuda:0')
    input = input.reshape([1, 3, 256, 256])
    output_full = model_full.netG(input).cpu()
    B_full = tensor2im(output_full)
    save_image(B_full, 'output/full/%s.png' % base, create_dir=True)
    p1 = Image.open(A_path)
    p2 = Image.open('output/full/%s.png' % base)
    p3 = Image.open(os.path.join(B_path))
    all = Image.new('RGB', (256*3, 256))
    all.paste(p1, (0, 0))
    all.paste(p2, (256, 0))
    all.paste(p3, (256*2, 0))
    display(all)
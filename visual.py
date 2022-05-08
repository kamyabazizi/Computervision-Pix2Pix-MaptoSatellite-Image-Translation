from IPython.display import display
from PIL import Image
A_dir = 'imgs/maps/A'
B_dir = 'imgs/maps/B'
files = os.listdir(A_dir)
print('             Input                        Original                        Ground-truth')

for file in files:
    if not file.endswith('.PNG'):
        continue
    base = file.split('.')[0]
    A_path = os.path.join(A_dir, file)
    
    B_path = os.path.join(B_dir, file)
    
    p1 = Image.open(A_path)
    p2 = Image.open('output/full/%s.png' % base)
    p3 = Image.open(os.path.join(B_path))
    all = Image.new('RGB', (256*3, 256))
    all.paste(p1, (0, 0))
    all.paste(p2, (256, 0))
    all.paste(p3, (256*2, 0))
    display(all)

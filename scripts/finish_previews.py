import json
from pathlib import Path
from PIL import Image, ImageDraw
import imageio.v2 as imageio

root = Path(__file__).resolve().parent.parent
out = root / 'qa' / 'final-previews'
out.mkdir(parents=True, exist_ok=True)
atlas = Image.open(root / 'assets/spritesheet.png').convert('RGBA')
states = [('idle',6),('running-right',8),('running-left',8),('waving',4),('jumping',5),('failed',8),('waiting',6),('running',6),('review',6)]
def cell(r,c):
    return atlas.crop((c*192,r*208,(c+1)*192,(r+1)*208))
def display(im,label=''):
    bg=Image.new('RGB',(192,232),(238,240,242))
    bg.paste(im,(0,24),im)
    ImageDraw.Draw(bg).text((5,5),label,fill='black')
    return bg
def gif(name, frames, durations):
    frames[0].save(out / name,save_all=True,append_images=frames[1:],duration=durations,loop=0,disposal=2)
all_frames=[]
all_durations=[]
for r,(name,n) in enumerate(states):
    folder=out/'frames'/name
    folder.mkdir(parents=True,exist_ok=True)
    frames=[]
    for c in range(n):
        im=cell(r,c)
        im.save(folder/f'{c:02}.png')
        frames.append(display(im,name))
    durations=([280,110,110,140,140,320] if r==0 else [140]*(n-1)+[280])
    gif(name+'.gif',frames,durations)
    all_frames.extend(frames)
    all_durations.extend(durations)
gif('all-states.gif',all_frames,all_durations)
transition=[display(cell(0,c),'idle') for c in range(6)]+[display(cell(4,c),'jumping') for c in range(5)]+[display(cell(0,c),'idle') for c in range(6)]
gif('idle-jump-idle.gif',transition,[180]*len(transition))
look=[display(cell(r,c),'look') for r in (9,10) for c in range(8)]
gif('look-loop.gif',look,[160]*16)
with imageio.get_writer(out/'all-states.mp4',fps=25,macro_block_size=1) as writer:
    for frame,duration in zip(all_frames,all_durations):
        import numpy as np
        for _ in range(max(1,round(duration/40))): writer.append_data(np.array(frame))
stills=Image.new('RGB',(192*4,232),(238,240,242))
for i,(r,c,label) in enumerate([(0,0,'idle'),(3,1,'wave'),(4,2,'jump peak'),(7,2,'thinking')]):
    stills.paste(display(cell(r,c),label),(192*i,0))
stills.save(out/'four-stills.png')

labels=['000','022.5','045','067.5','090','112.5','135','157.5','180','202.5','225','247.5','270','292.5','315','337.5']
expected=['up']+['up-right']*3+['right']+['down-right']*3+['down']+['down-left']*3+['left']+['up-left']*3
evidence=[
 'Beak tip points straight above head center, eyes raised; planted torso.',
 'Beak projects above and right of face center, raised eyes track upper right.',
 'Head pitches upward and yaws right, beak tip high and right of face.',
 'Beak projects strongly right and slightly upward, eye/head angle remains raised.',
 'Head yaws right, beak projects horizontally toward screen right.',
 'Beak projects right with downward slope; head begins bowing.',
 'Beak descends right of face center, lowered eyes and bowed head.',
 'Head bows strongly, beak points down with small right displacement.',
 'Head bowed frontally, pupils low and beak points straight down.',
 'Head and beak slightly left while strongly bowed, eyes follow downward.',
 'Beak points diagonally down-left and head yaws left.',
 'Beak extends strongly screen-left with slight downward slope.',
 'Head yaws screen-left, beak projects horizontally left of face.',
 'Head raises and yaws left; beak extends left with a slight upward slope.',
 'Beak points diagonally up-left, raised head and eyes follow.',
 'Beak points strongly upward and slightly left, raised eyes continue arc to up.'
]
records={label:{'expected':exp,'observed':ev,'verdict':'warning' if label in ['067.5','157.5','202.5','292.5'] else 'pass','evidence':ev} for label,exp,ev in zip(labels,expected,evidence)}
(root/'qa/direction-semantics.json').write_text(json.dumps({'directions':records,'continuity_review':'Natural toe gaps account for bottom alpha warnings. Boundary changes preserve body anchoring and clockwise beak direction; no material body holes observed.'},indent=2))
print(out)

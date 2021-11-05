# This script `1_symbolic_method_1pha.py` makes it possible to
# produce a video showing the link between a sine wave
# and its associated phasor
#
# Author: Luca Giaccone (luca.giaccone@polito.it)
# Date: 5/11/2021 (initial release on GitHub)
# GitHub link: https://github.com/giaccone/pytool4teaching


# import libraries
# ----------------
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.animation as manimation

# define video properties
# -----------------------
tit = 'video1_single_phasor'
FFMpegWriter = manimation.writers['ffmpeg']
metadata = dict(title=tit, artist='', comment='')
writer = FFMpegWriter(fps=30, metadata=metadata)

# define waveform parameter
# -------------------------
f = 50
T = 1/f
TENDS = np.linspace(0, T, 300)
t0 = 0
M = 2
phi0 = np.pi / 4

# initialize figure (i.e. the frame of the video)
# -----------------------------------------------
hf = plt.figure(facecolor='w', figsize=(12, 5))

# begin recording
# ---------------
with writer.saving(hf, './video/' + tit + '.mp4',100):
    for tf in TENDS:
        t = np.linspace(t0,tf,50)
        y = M * np.sin(2*np.pi*f*t + phi0)

        # data phasor
        # -----------
        HL = M*10/100
        HW = 0.5*HL
        alpha = 2*np.pi*f*t[-1] + phi0

        RE = (M - HL) * np.cos(alpha)
        IM = (M - HL) * np.sin(alpha)
        XMIN = 0.5 + M * np.cos(alpha)/4.8
        
        # First subplot
        # -------------
        ax1 = hf.add_subplot(121)
        ax1.axis('square')
        ax1.set_xlim(-M*1.2,M*1.2)
        ax1.set_ylim(-M*1.2,M*1.2)
        ax1.grid()
        
        # plot phasor
        ax1.arrow(0, 0, RE,IM, linewidth=2,head_width=HW, head_length=HL, fc='C0', ec='C0')
        # plot line from arrow to right edge
        ax1.axhline(M * np.sin(alpha), xmin=XMIN,color='k',linewidth=1, linestyle='--')

        ax1.set_xticks([-M, 0, M])
        ax1.set_xticklabels(('-A','0','A'))
        ax1.set_yticks([-M, 0, M])
        ax1.set_yticklabels(('-A','0','A'))
        ax1.tick_params(labelsize=18)

        # Second subplot
        # -------------
        ax2 = hf.add_subplot(122)
        # plot waveform
        ax2.plot(t,y,'C0',linewidth=2)
        ax2.axhline(M * np.sin(alpha),xmax=t[-1]/T,color='k',linewidth=1, linestyle='--')
        ax2.axhline(M * np.sin(alpha),xmin=-0.26,xmax=0,linewidth=1,zorder=0, clip_on=False,color='k',linestyle='--')
        
    
        ax2.set_xlim(0,T)
        ax2.set_ylim(-M*1.2,M*1.2)
        ax2.grid()
        ax2.set_xticks([0,T/4,T/2,3/4*T,T])
        ax2.set_xticklabels(('0','T/4','T/2','3/4T','T'))
        ax2.set_yticks([-M, 0, M])
        ax2.set_yticklabels(('-A','0','A'))
        ax2.tick_params(labelsize=18)
        
        # grab frame and delete axis
        writer.grab_frame()
        hf.delaxes(ax1)
        hf.delaxes(ax2)

plt.close("all")


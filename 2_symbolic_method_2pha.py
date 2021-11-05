# This script `2_symbolic_method_2pha.py` makes it possible to
# produce a video showing two sine wave with either equal
# or different frequency
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

# select case:
#     * 'sync'  : same frequency
#     * 'async' : different frequency
# -----------------------------------
case_type = 'async'

# define video properties
# -----------------------
if case_type == 'sync':
    tit = 'video2_two_phasors_sync'
elif case_type == 'async':
    tit = 'video3_two_phasors_async'
FFMpegWriter = manimation.writers['ffmpeg']
metadata = dict(title=tit, artist='', comment='')
writer = FFMpegWriter(fps=30, metadata=metadata)


# waveform-1 parameter
f1 = 50
T = 1/f1
TENDS = np.linspace(0, T, 300)
t0 = 0
M1 = 2
phi0_1 = np.pi / 4

# waveform-2 parameter
if case_type == 'sync':
    f2 = 50
elif case_type == 'async':
    f2 = 150  # 3*f1
T2 = 1/f2
M2 = 1
phi0_2 = 0

# initialize figure (i.e. the frame of the video)
# -----------------------------------------------
hf = plt.figure(facecolor='w', figsize=(12, 5))

# begin recording
# ---------------
with writer.saving(hf, './video/' + tit + '.mp4',100):
    for tf in TENDS:
        t = np.linspace(t0,tf,50)
        y1 = M1 * np.sin(2*np.pi*f1*t + phi0_1)
        y2 = M2 * np.sin(2*np.pi*f2*t + phi0_2)

        # data phasor
        # -----------
        # first
        HL1 = M1 * 10 / 100
        HW1 = 0.5 * HL1
        alpha1 = 2 * np.pi * f1 * t[-1] + phi0_1

        RE1 = (M1 - HL1) * np.cos(alpha1)
        IM1 = (M1 - HL1) * np.sin(alpha1)
        XMIN1 = 0.5 + M1 * np.cos(alpha1) / 4.8

        # second
        HL2 = M2 * 10 / 100
        HW2 = 0.5 * HL2
        alpha2 = 2 * np.pi * f2 * t[-1] + phi0_2

        RE2 = (M2 - HL2) * np.cos(alpha2)
        IM2 = (M2 - HL2) * np.sin(alpha2)
        XMIN2 = 0.5 + M2 * np.cos(alpha2) / 4.8
        
        # First subplot
        # -------------
        ax1 = hf.add_subplot(121)
        ax1.axis('square')
        Mmax = max([M1, M2])
        ax1.set_xlim(-Mmax * 1.2, Mmax * 1.2)
        ax1.set_ylim(-Mmax * 1.2, Mmax * 1.2)
        ax1.grid()
        
        # plot phasor
        ax1.arrow(0, 0, RE1, IM1, linewidth=2,head_width=HW1, head_length=HL1, fc='C0', ec='C0')
        ax1.arrow(0, 0, RE2, IM2, linewidth=2,head_width=HW2, head_length=HL2, fc='C1', ec='C1')
        # plot line from arrow to right edge
        ax1.axhline(M1 * np.sin(alpha1), xmin=XMIN1,color='C0',linewidth=1, linestyle='--')
        ax1.axhline(M2 * np.sin(alpha2), xmin=XMIN2,color='C1',linewidth=1, linestyle='--')

        ax1.set_xticks([-Mmax, 0, Mmax])
        ax1.set_xticklabels(('-A','0','A'))
        ax1.set_yticks([-Mmax, 0, Mmax])
        ax1.set_yticklabels(('-A','0','A'))
        ax1.tick_params(labelsize=18)

        # Second subplot
        # -------------
        ax2 = hf.add_subplot(122)
        # plot waveform
        ax2.plot(t,y1,'C0',linewidth=2)
        ax2.axhline(M1 * np.sin(alpha1),xmax=t[-1]/T,color='C0',linewidth=1, linestyle='--')
        ax2.axhline(M1 * np.sin(alpha1),xmin=-0.26,xmax=0,linewidth=1,zorder=0, clip_on=False,color='C0',linestyle='--')

        ax2.plot(t,y2,'C1',linewidth=2)
        ax2.axhline(M2 * np.sin(alpha2),xmax=t[-1]/T,color='C1',linewidth=1, linestyle='--')
        ax2.axhline(M2 * np.sin(alpha2),xmin=-0.26,xmax=0,linewidth=1,zorder=0, clip_on=False,color='C1',linestyle='--')
        
    
        ax2.set_xlim(0, T)
        ax2.set_ylim(-Mmax * 1.2, Mmax * 1.2)
        ax2.grid()
        ax2.set_xticks([0,T/4,T/2,3/4*T,T])
        ax2.set_xticklabels(('0','T/4','T/2','3/4T','T'))
        ax2.set_yticks([-Mmax, 0, Mmax])
        ax2.set_yticklabels(('-A','0','A'))
        ax2.tick_params(labelsize=18)
        
        # grab frame and delete axis
        writer.grab_frame()
        hf.delaxes(ax1)
        hf.delaxes(ax2)

plt.close("all")


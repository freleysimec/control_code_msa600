
import numpy as np
import matplotlib.pyplot as plt

def DV_plot(D, V, filename):
    # butterfly
    plt.plot(V, D, color='blue', label='T0')
    #at vertical line at 0V
    plt.axvline(x=0, color='black', linestyle='--')
    plt.title('D-V plot')
    plt.xlabel('Voltage (V)')
    plt.ylabel('Distance (um)')
    plt.savefig(filename + ".png")
    plt.close()

def FR_plot(D, t, filename):
    plt.plot(t, D, color='blue', label='T0')
    plt.title('RF plot')
    plt.xlabel('frequency (Hz)')
    plt.ylabel('Distance (um)')
    plt.savefig(filename + ".png")
    plt.close()

def quick_plot(x):
    plt.plot(x,color='blue', label='T0')
    plt.show()

def quick_plot_2(x,y):
    plt.plot(x, y,color='blue', label='T0')
    plt.show()

def fft_plt(x,y, filename):
    plt.plot(x, y,color='blue', label='T0')
    plt.title('RF plot')
    plt.xlabel('frequency (Hz)')
    plt.ylabel('velocity (um)')
    plt.savefig(filename + ".png")
    plt.close()
    

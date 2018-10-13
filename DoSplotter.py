# -*- coding: utf-8 -*-
"""
Produce density of states plots

Created on Mon Jun 25 16:13:05 2018

@author: Cara Lynch

Input: name of file(s) to be graphed and, if >1, desired name to appear on graphs (either 1 or 3 files)
Desired name must follow filename, input as command line arguments.
Output: density of states graphs
"""

#import sys
import numpy as np
import os
import matplotlib.pyplot as plt
import sys

def readfile(filename):
	"""
	Reads DoS files
	
	:param filename: Name of file as string
	:return spin1occs, spin2occs: Spin occupation data as floats in 2 lists
	:return energies: energy data as floats in list
	"""
	spin1occs=[]
	spin2occs = []
	energies = []
	with open(filename) as infile:
		for line in infile:
			linetokens = line.split()
			spin1 = float(linetokens[0])
			spin1occs.append(-spin1) # negative so that appears on LHS of DoS plot
			spin2 = float(linetokens[1])
			spin2occs.append(spin2)
			energy = float(linetokens[2])
			energies.append(energy)
	return spin1occs, spin2occs, energies 

def plotDOS(infile):
	"""
	Make 1 density of states plot
	
	:param infile: name of file to read as string
	"""
	
	spin1occs, spin2occs, energies = readfile(infile)
	
	# Plot graph
	plt.plot(spin1occs,energies,"b", label='Spin 1')
	plt.plot(spin2occs, energies, "g", label = 'Spin 2')
	plt.legend()
	plt.title(infile)
	plt.ylabel('Energy')
	plt.box(on=None)
	plotaxes = plt.gca()
	plotaxes.axes.get_xaxis().set_visible(False)
	plt.savefig(infile + 'plot.jpg')
	plt.show()
	
def plot3DOS(infileA, nameA, infileB, nameB, infileC, nameC):
	"""
	Produce figure with 3 density of states graphs
	
	:param infileA, infileB, infileC: file names as strings
	:param nameA, nameB, nameC: desired names to appear in figure
	"""
	
	spin1occsA, spin2occsA, energiesA = readfile(infileA)
	spin1occsB, spin2occsB, energiesB = readfile(infileB)
	spin1occsC, spin2occsC, energiesC = readfile(infileC)
	
	
	spin1names = [spin1occsA, spin1occsB, spin1occsC]
	spin2names = [spin2occsA, spin2occsB, spin2occsC]
	energynames = [energiesA, energiesB, energiesC]
	names = [nameA, nameB, nameC]
	
	# Create figure
	fig, axs = plt.subplots(1,3,figsize=(18,12), facecolor='w', edgecolor='k')

	axs = axs.ravel()
	for i in range(0,3):
		axs[i].plot(spin1names[i], energynames[i], "b", label='Spin 1')
		axs[i].plot(spin2names[i], energynames[i], "g", label='Spin 2')
		
		axs[i].set_title(str(names[i]))
		axs[i].get_xaxis().set_visible(False)
	axs[0].set_ylabel('Energy')
	handles, labels = axs[0].get_legend_handles_labels()
	fig.legend(handles, labels)
	handles, labels = axs[0].get_legend_handles_labels()
	plt.savefig("DOSPLOTS")
	plt.show()
	


l = len(sys.argv)

if l==2:
	infile=str(sys.argv[1])
	plotDOS(infile)
elif l==7:
	infileA = str(sys.argv[1])
	nameA = str(sys.argv[2])
	infileB = str(sys.argv[3])
	nameB = str(sys.argv[4])
	infileC = str(sys.argv[5])
	nameC = str(sys.argv[6])
	plot3DOS(infileA, nameA, infileB, nameB, infileC, nameC)

# -*- coding: utf-8 -*-
"""
Compare data between data files produced by readOUTCAR

Created on Mon Jun 25 16:13:05 2018

@author: Cara Lynch

The names of files to be compared must be written in the command line followed by their respective desired legend name.
"""

#import sys
import numpy as np
import os
import matplotlib.pyplot as plt
import sys

def isfloat(value):
	"""
	Checks if a string, int or float is a float
	"""
	try:
		float(value)
		return True
	except ValueError:
		return False

def read_data(infile):
	"""
	Reads readOUTCAR.py output file and puts data into arrays

	:param infile: name of file to read
	:return array: table of all data from file
	:return varnames: name of variables in file
	"""
	with open(infile,"rt") as file:
		
		lines = file.readlines()
		varnames = lines[0].split(',')
		
		nvars = len(lines[1].split(',')) #Find number of variables in table
		varnames = varnames[:nvars] #Only include the relevant variable names
		dataarray = np.zeros([len(lines)-1,nvars]) #Create empty array to story data
		
		#Fill array
		for i in range(1,len(lines)):
			linetokens = lines[i].split(',')
			for n in range(0,len(linetokens)):
				if isfloat(linetokens[n]) == True:
					dataarray[i-1,n] = float(linetokens[n])
				else:
					dataarray[i-1,n] = 'NaN'
	return dataarray, varnames
    
def plotfile(infile, compoundname):
	"""
	Produce plots of data from file

	:param infile: name of input file as string
	:param compoundname: name of compound as string
	"""
	array, varnames = read_data(infile) # Get data array and variable names from file
	
	# find number of ions

	outdir = compoundname + 'plots' # name of output directory
	if not os.path.exists(outdir): #Create directory for plot data
		os.makedirs(outdir)
	else:
		compoundname = "new" + outdir
		os.makedirs(outdir)

	# Create plots for Enthalpy, Volume, Magtot
	for i in [1,2,5]:
		plt.subplot()
		plt.plot(array[:,[0]],array[:,[i]],"g", label=compoundname)
		plt.title(varnames[i])
		plt.xlabel(varnames[0])
		plt.ylabel(varnames[i])   
		plt.savefig(outdir + "/" + str(varnames[i]))
		plt.show()
		
	# Create plot for bandgaps
	plt.subplot()
	plt.plot(array[:,[0]],array[:,[3]],"g", label='Spin 1')
	plt.plot(array[:,[0]],array[:,[4]],"b", label='Spin 2')
	plt.legend()
	plt.title('Bandgap')
	plt.xlabel('Pressure (kbar)')
	plt.ylabel('Bandgap (eV)')   
	plt.savefig(outdir + "/Bandgap")
	plt.show()
	
	# Create plot for Mag ions
	numions = np.ma.size(array,1) - 6
	plt.subplot()
	for i in range(6, 6 + numions/2):
		plt.plot(array[:,[0]],array[:,[i]],"g", label=varnames[i])
	for i in range(6+numions/2, np.ma.size(array,1)-1):
		plt.plot(array[:,[0]],array[:,[i]],"b", label=varnames[i])
	plt.title('Ion Magnetization')
	plt.xlabel('Pressure (kbar)')
	plt.ylabel('Magnetization (Bohrs)')
	plt.legend()
	plt.savefig(outdir + "/IonMag")
	plt.show()

	# Create figure
	fig, axs = plt.subplots(2,3,figsize=(18,12), facecolor='w', edgecolor='k')
	fig.subplots_adjust(hspace = .5, wspace=.5)

	axs = axs.ravel()
	
	n=0 #plot counter
	# Create plots for Enthalpy, Volume, Magtot in fig
	for i in [1,2,5]:
		axs[n].plot(array[:,[0]],array[:,[i]],"g", label=compoundname)
		axs[n].set_title(varnames[i])
		axs[n].set_xlabel(varnames[0])
		axs[n].set_ylabel(varnames[i])
		n = n+1
	
	# Plot bandgaps in fig
	axs[n].plot(array[:,[0]],array[:,[3]],"g", label='Spin 1')
	axs[n].plot(array[:,[0]],array[:,[4]],"b", label='Spin 2')
	axs[n].set_title('Bandgap')
	axs[n].set_xlabel('Pressure (kbar)')
	axs[n].set_ylabel('Bandgap (eV)')
	n = n+1
	
	# Plot Magions in fig
	for i in range(6, 6 + numions/2):
		axs[n].plot(array[:,[0]],array[:,[i]],"g", label=varnames[i])
	for i in range(6+numions/2, np.ma.size(array,1)-1):
		axs[n].plot(array[:,[0]],array[:,[i]],"b", label=varnames[i])
	axs[n].set_title('Ion Magnetization')
	axs[n].set_xlabel('Pressure (kbar)')
	axs[n].set_ylabel('Magnetization (Bohrs)')
	
	handles, labels = axs[n-1].get_legend_handles_labels()
	axs[n-1].legend(handles, labels)
	plt.savefig(outdir + "/" + compoundname)      
	plt.show()	

def comparison_plots(infile1, name1, infile2, name2):
	"""
	Produce comparison plots of data from 2 files

	:params infile1, infile2: OUTCAR file names as strings
	:params name1, name2: names of compounds to use in legends etc
	"""
	#Get data arrays from files    
	array1, vars1 = read_data(infile1)
	array2, vars2 = read_data(infile2)   


	#Create file to put comparison plots
	datadir = name1 + "vs" + name2
	if not os.path.exists(datadir):
		os.makedirs(datadir)

	# Only want to compare Enthalpy, Volume, Bandgap1, Bandgap2, MagTot
	# so first 6 columns of data
	numcols = 6
	
	#unless some have less columns
	#if np.ma.size(array1,1) < numcols or np.ma.size(array2,1) < numcols:
		#if np.ma.size(array1,1) > np.ma.size(array2,1):
			#numcols = np.ma.size(array2,1)
		#else:
			#numcols = np.ma.size(array1,1)
	varnames = vars1[:numcols]

	while np.ma.size(array1,1) > numcols:
		array1 = np.delete(array1, numcols, 1) # delete irrelevant columns from array1
	while np.ma.size(array2,1) > numcols:
		array2 = np.delete(array2,numcols,1) # delete irrelevant columns from array2
	
	# if not enough columns, add extra NaN columns	
	while np.ma.size(array1,1) < numcols:
		np.insert(array1, np.ma.size(array1,1),np.nan,1)
	
	while np.ma.size(array2,1) < numcols:
		np.insert(array2, np.ma.size(array2,1),np.nan,1)

	# Check that all pressure points present, if not add them with NaN values
	p = 0.001
	if float(array1[0,0]) > p:
		array1 = np.insert(array1, 0, np.nan,0)
	if float(array2[0,0]) > p:
		array2 = np.insert(array2, 0, np.nan,0)			

	i = 1
	for p in range(2,11,2):
		print(p)
		print(i)
		if int(array1[i,0]) > p:
			array1 = np.insert(array1, i, np.nan,0)
		if int(array2[i,0]) > p:
			array2 = np.insert(array2, i, np.nan,0)		
		i = i+1

	for p in range(20,400,20):
		print(p)
		print(i)
		if int(array1[i,0]) > p:
			array1 = np.insert(array1, i, np.nan,0)
		if int(array2[i,0]) > p:
			array2 = np.insert(array2, i, np.nan,0)		
		i = i+1
		
		#for array in [array1, array2]:
	try:
		test = array1[i]
		if array1[i] == []:
			array1[i] = np.nan
	except:
		nanny = np.empty((1,6))
		nanny[:] = np.nan
		array1 = np.append(array1,nanny, axis=0)
		
	try:
		test = array2[i]
		if array2[i] == []:
			array2[i] = np.nan
	except:
		nanny = np.empty((1,6))
		nanny[:] = np.nan
		array2 = np.append(array2,nanny, axis=0)

	# Calculate relative differences between arrays
	differencearray2 = array2 - array1
	differencearray2[:,0] = array2[:,0] # set pressures back to right vals
	differencearray1 = array1 - array1
	differencearray1[:,0] = array1[:,0] # set pressures back to right vals


	# Create plots of relative enthalpies and volume
	for i in [1,2]:
		plt.subplot()
		plt.plot(differencearray1[:,[0]],differencearray1[:,[i]],"b", label=name1 + "(baseline)")
		plt.plot(differencearray2[:,[0]],differencearray2[:,[i]],"r", label=name2)
		plt.legend()
		plt.title("Relative " + varnames[i])
		plt.xlabel(varnames[0])
		plt.ylabel(varnames[i])   
		plt.savefig(datadir + "/Relative" + str(varnames[i]))
		plt.show()
	
	#Create plots of bandgap1, bandgap2 and total magnetization
	for i in range(3,6):
		plt.subplot()
		plt.plot(array1[:,[0]],array1[:,[i]],"g", label=name1)
		plt.plot(array2[:,[0]],array2[:,[i]],"r", label=name2)
		plt.legend()
		plt.title(varnames[i])
		plt.xlabel(varnames[0])
		plt.ylabel(varnames[i])   
		plt.savefig(datadir + "/" + str(varnames[i]))
		plt.show()

	# Create figure
	fig, axs = plt.subplots(2,3,figsize=(18,12), facecolor='w', edgecolor='k')
	fig.subplots_adjust(hspace = .5, wspace=.5)

	axs = axs.ravel()

	for i in [1,2]:
		axs[i-1].plot(differencearray1[:,[0]],differencearray1[:,[i]],"b", label=name1+"(baseline)")
		axs[i-1].plot(differencearray2[:,[0]],differencearray2[:,[i]],"r", label=name2)
		axs[i-1].set_title("Relative " + varnames[i])
		axs[i-1].set_xlabel(varnames[0])
		axs[i-1].set_ylabel(varnames[i])
	for i in range(3,6):
		axs[i-1].plot(array1[:,[0]],array1[:,[i]],"g", label=name1)
		axs[i-1].plot(array2[:,[0]],array2[:,[i]],"r", label=name2)
		axs[i-1].set_title(varnames[i])
		axs[i-1].set_xlabel(varnames[0])
		axs[i-1].set_ylabel(varnames[i])
	
	handles, labels = axs[0].get_legend_handles_labels()
	fig.legend(handles, labels, loc=10)
	plt.savefig(datadir + "/Variables Comparison")      
	plt.show()   

def comparison_plots3(infile1, name1, infile2, name2, infile3, name3):
	"""
	Produce comparison plots of data from 2 files

	:params infile1, infile2: OUTCAR file names as strings
	:params name1, name2: names of compounds to use in legends etc
	"""
	#Get data arrays from files    
	array1, vars1 = read_data(infile1)
	array2, vars2 = read_data(infile2)   
	array3, vars3 = read_data(infile3) 


	#Create file to put comparison plots
	datadir = name1 + "vs" + name2 + "vs" + name3
	if not os.path.exists(datadir):
		os.makedirs(datadir)

	# Only want to compare Enthalpy, Volume, Bandgap1, Bandgap2, MagTot
	# so first 6 columns of data
	numcols = 6
	
	#unless some have less columns
	#if np.ma.size(array1,1) < numcols or np.ma.size(array2,1) < numcols:
		#if np.ma.size(array1,1) > np.ma.size(array2,1):
			#numcols = np.ma.size(array2,1)
		#else:
			#numcols = np.ma.size(array1,1)
	varnames = vars1[:numcols]

	while np.ma.size(array1,1) > numcols:
		array1 = np.delete(array1, numcols, 1) # delete irrelevant columns from array1
	while np.ma.size(array2,1) > numcols:
		array2 = np.delete(array2,numcols,1) # delete irrelevant columns from array2
	while np.ma.size(array3,1) > numcols:
		array3 = np.delete(array3,numcols,1) # delete irrelevant columns from array3


	# if not enough columns, add extra NaN columns	
	while np.ma.size(array1,1) < numcols:
		np.insert(array1, np.ma.size(array1,1),np.nan,1)
	while np.ma.size(array2,1) < numcols:
		np.insert(array2, np.ma.size(array2,1),np.nan,1)
	while np.ma.size(array3,1) < numcols:
		np.insert(array3, np.ma.size(array3,1),np.nan,1)

	# Check that all pressure points present, if not add them with NaN values
	p = 0.001
	if float(array1[0,0]) > p:
		array1 = np.insert(array1, 0, np.nan,0)
	if float(array2[0,0]) > p:
		array2 = np.insert(array2, 0, np.nan,0)	
	if float(array3[0,0]) > p:
		array3 = np.insert(array3, 0, np.nan,0)			

	i = 1
	for p in range(2,11,2):
		if int(array1[i,0]) > p:
			array1 = np.insert(array1, i, np.nan,0)
		if int(array2[i,0]) > p:
			array2 = np.insert(array2, i, np.nan,0)
		if int(array3[i,0]) > p:
			array3 = np.insert(array3, i, np.nan,0)			
		i = i+1


	for p in range(20,400,20):
		if int(array1[i,0]) > p:
			array1 = np.insert(array1, i, np.nan,0)
		if int(array2[i,0]) > p:
			array2 = np.insert(array2, i, np.nan,0)
		if int(array3[i,0]) > p:
			array3 = np.insert(array3, i, np.nan,0)		
		i = i+1
		
	#for array in [array1, array2, array3]:
	try:
		test = array1[i]
		if array1[i] == []:
			array1[i] = np.nan
	except:
		nanny = np.empty((1,6))
		nanny[:] = np.nan
		array1 = np.append(array1,nanny, axis=0)
		
	try:
		test = array2[i]
		if array2[i] == []:
			array2[i] = np.nan
	except:
		nanny = np.empty((1,6))
		nanny[:] = np.nan
		array2 = np.append(array2,nanny, axis=0)

	try:
		test = array3[i]
		if array3[i] == []:
			array3[i] = np.nan
	except:
		nanny = np.empty((1,6))
		nanny[:] = np.nan
		array3 = np.append(array3,nanny, axis=0)

	
	# Calculate relative differences between arrays
	differencearray2 = array2 - array1
	differencearray2[:,0] = array2[:,0] # set pressures back to right vals
	differencearray1 = array1 - array1
	differencearray1[:,0] = array1[:,0] # set pressures back to right vals
	differencearray3 = array3 - array1
	differencearray3[:,0] = array3[:,0] # set pressures back to right vals


	#Create plots of relative differences between enthalpies and volumes wrt compound 1
	for i in [1,2]:
		plt.subplot()
		plt.plot(differencearray1[:,[0]],differencearray1[:,[i]],"g", label=name1 + "(baseline)")
		plt.plot(differencearray2[:,[0]],differencearray2[:,[i]],"r", label=name2)
		plt.plot(differencearray3[:,[0]],differencearray3[:,[i]],"b", label=name3)
		plt.legend()
		plt.title("Relative" + varnames[i])
		plt.xlabel(varnames[0])
		plt.ylabel(varnames[i])   
		plt.savefig(datadir + "/" + str("Relative" + varnames[i]))
		plt.show()
		
	#Create plots of bandgap1, bandgap2 and total magnetization
	for i in range(3,6):
		plt.subplot()
		plt.plot(array1[:,[0]],array1[:,[i]],"g", label=name1)
		plt.plot(array2[:,[0]],array2[:,[i]],"r", label=name2)
		plt.plot(array3[:,[0]],array3[:,[i]],"b", label=name3)
		plt.legend()
		plt.title(varnames[i])
		plt.xlabel(varnames[0])
		plt.ylabel(varnames[i])   
		plt.savefig(datadir + "/" + str(varnames[i]))
		plt.show()

	# Create figure
	fig, axs = plt.subplots(2,3,figsize=(18,12), facecolor='w', edgecolor='k')
	fig.subplots_adjust(hspace = .6, wspace=.5)

	axs = axs.ravel()

	for i in [1,2]:
		axs[i-1].plot(differencearray1[:,[0]],differencearray1[:,[i]],"g", label=name1+"(baseline)")
		axs[i-1].plot(differencearray2[:,[0]],differencearray2[:,[i]],"r", label=name2)
		axs[i-1].plot(differencearray3[:,[0]],differencearray3[:,[i]],"b", label=name3)
		axs[i-1].set_title("Relative " + varnames[i])
		axs[i-1].set_xlabel(varnames[0])
		axs[i-1].set_ylabel(varnames[i])
	for i in range(3,6):
		axs[i-1].plot(array1[:,[0]],array1[:,[i]],"g", label=name1)
		axs[i-1].plot(array2[:,[0]],array2[:,[i]],"r", label=name2)
		axs[i-1].plot(array3[:,[0]],array3[:,[i]],"b", label=name3)
		axs[i-1].set_title(varnames[i])
		axs[i-1].set_xlabel(varnames[0])
		axs[i-1].set_ylabel(varnames[i])
	
	handles, labels = axs[0].get_legend_handles_labels()
	fig.legend(handles, labels, loc=10)
	plt.savefig(datadir + "/Variables Comparison")      
	plt.show()   


l = len(sys.argv)

if l==3:
	infile=str(sys.argv[1])
	compoundname=str(sys.argv[2])
	plotfile(infile, compoundname)
elif l==5:
	infile1=str(sys.argv[1])
	name1=str(sys.argv[2])
	infile2=str(sys.argv[3])
	name2 = str(sys.argv[4])
	comparison_plots(infile1,name1, infile2, name2)
elif l==7:
	infile1=str(sys.argv[1])
	name1=str(sys.argv[2])
	infile2=str(sys.argv[3])
	name2 = str(sys.argv[4])
	infile3=str(sys.argv[5])
	name3 = str(sys.argv[6])
	comparison_plots3(infile1,name1, infile2, name2,infile3, name3)
else:
	print("Wrong number of arguments")
	print("You must input file names and compound names as arguments")

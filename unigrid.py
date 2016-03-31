#Creates a unigrid data cube of density, e:tc, of a specified length
#from an Enzo simulation, centered on the densest point. Exports the unigrid to a txt file located in the DD or RD directory
#Marco Surace and Carla Bernhardt
#Last updated: 22.02.2016
###################################################

import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
from matplotlib.colors import LogNorm
from yt.mods import *
import sys
from matplotlib import rc
rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})
rc('text', usetex=True)

for i in range(1,len(sys.argv)-1):

	#Reads in data files, overall box size,  unigrid box size, and sets up the dimensions of the unigrid
	ds = load(sys.argv[i])
	ds.print_stats()
	box_size_kpc = 100000
	sidelength = float(sys.argv[len(sys.argv)-1])
	val, loc = ds.find_max("density")
	field = 'density'
	ds.index
	#print ds.field_list
	units = ds.field_info['gas', field].get_units()
	print units

	left_edge = np.array(loc)-((0.5*sidelength)/box_size_kpc)
	print "side length of unigrid (kpc)= ", sidelength
	print "coords of left edge (code units) = ",left_edge
	dx = (ds.index.get_smallest_dx()).in_units('kpc')
	print "smallest dx = ", dx
	dimens = int(sidelength/float(dx))
	print "dimensions of unigrid = ", dimens
	dims = np.array([dimens, dimens, dimens])
	print "dimensions array = ", dims

	#Creates fixed resolution buffer with dimensions*2, the first number in parenthesis is resolution level data
	#is uniformly gridded at
	#dim is the number of cells along each axis of resulting covering_grid

	cg=ds.smoothed_covering_grid(1,left_edge, dims)
	data=cg[field]
	import numpy as np
	data = np.array(data)

	#Finds the minimum and maximum values of the field  within 2D x,y,z slices. Required to produce the colourbars below correctly
	x_min = data[dims[1]-1,:,:].min()
	x_max = data[dims[1]-1,:,:].max()
	y_min = data[:,dims[1]-1,:].min()
	y_max = data[:,dims[1]-1,:].max()
	z_min = data[:,:,dims[1]-1].min()
	z_max = data[:,:,dims[1]-1].max()

	#Plots the unigrid 2D slices
	plt.imshow(np.rot90(np.rot90(np.rot90(np.fliplr(np.flipud(data[dims[1]-1,:,:]))))),norm=LogNorm(vmin=x_min, vmax=x_max))
	#print "units = ", str(units)
	#plt.colorbar(pad=0.001).set_label(r"Density ($\frac{g}{cm^3}$)")
	plt.colorbar(pad=0.001).set_label(field+r" ($"+str(units)+"$)")
	plt.xlabel('y ('+str(dx)+' per unit)')
	plt.ylabel('z ('+str(dx)+' per unit)')
	plt.title('x Slice '+str(sidelength)+' kpc across ')
	print sys.argv[i],'_xSlice_',field,'_unigrid.png'
	plt.savefig(sys.argv[i]+'_xSlice_'+field+'_unigrid.png')
	plt.close()
	plt.imshow(np.rot90(np.rot90(np.fliplr(data[:,dims[1]-1,:]))), norm=LogNorm(vmin=y_min,vmax=y_max))
	#plt.colorbar(pad=0.001).set_label(r"Density ($\frac{g}{cm^3}$)")
	plt.colorbar(pad=0.001).set_label(field+r" ($"+str(units)+"$)")
	plt.xlabel('z ('+str(dx)+' per unit)')
	plt.ylabel('x ('+str(dx)+' per unit)')
	plt.title('y Slice '+str(sidelength)+' kpc across ')
	plt.savefig(sys.argv[i]+'_ySlice_'+field+'_unigrid.png')
	plt.close()
	plt.imshow(np.rot90(data[:,:,dims[1]-1]), norm=LogNorm(vmin=z_min, vmax=z_max))
	#plt.colorbar(pad=0.001).set_label(r"Density ($\frac{g}{cm^3}$)")
	plt.colorbar(pad=0.001).set_label(field+r" ($"+str(units)+"$)")
	plt.xlabel('x ('+str(dx)+' per unit)')
	plt.ylabel('y ('+str(dx)+' per unit)')
	plt.savefig(sys.argv[i]+'_zSlice_'+field+'_unigrid.png')
	
	#Writing the output into a file
	dat=data.flatten()
	#print dat
	for j in range(max(np.shape(dat))):
		data=open(sys.argv[i]+'_'+field+'.txt', 'a')
		data.write(str(dat[j]))
		data.write('\n')
	data.close()

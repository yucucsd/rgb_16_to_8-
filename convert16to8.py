#from PIL import Image
import numpy
import csv
#from osgeo import gdal, gdalnumeric, ogr, osr
#from gdalconst import * 
#from matplotlib import pyplot
#import struct
#import Image, ImageDraw
#import os, sys
import tifffile as tiff
import math
from multiprocessing import Pool
import itertools

def convert(band):
	mini = numpy.amin(band)
	maxi = numpy.amax(band)
	scale = maxi - mini
	contrast = 1
	brightness = 0
	for j in range(len(band)):
		for k in range(len(band[j])):
			band[j][k] = math.floor(float(band[j][k] - mini) / (contrast * scale) * 255)
		band[j][k] = min(255, band[j][k] + brightness)
	return band

file = open('grid_sizes.csv', 'rb')
readin = csv.reader(file, delimiter = ',')
i = 0
for row in readin:
	if len(row[0]) == 0:
		continue
	print row
	'''
	dataset = gdal.Open('three_band/' + row[0] + '.tif', GA_ReadOnly)
	#print datasetA.GetGeoTransform() 
	x_size = dataset.RasterXSize
	y_size = dataset.RasterYSize
	channel = dataset.RasterCount
	print x_size, y_size, channel
	pic = []
	for i in range(1, channel + 1):
		band = dataset.GetRasterBand(i)
		data = band.ReadAsArray(0, 0, band.XSize, band.YSize).astype(numpy.uint16)
		pic.append(data)
	print data[0]

	#print gdal.GetDataTypeName(band.DataType)
	#scanline = band.ReadRaster(0, 0, band.XSize, 1, band.XSize, 1, band.DataType) 
	#The ReadRaster() call has the arguments: 
	#def ReadRaster(self, xoff, yoff, xsize, ysize, buf_xsize = None, 
	#buf_ysize = None, buf_type = None, band_list = None ): 
	#The xoff, yoff, xsize, ysize parameter define the rectangle on the raster file to read. 
	#The buf_xsize, buf_ysize values are the size of the resulting buffer. 
	#So you might say "0,0,512,512,100,100" to read a 512x512 block at the top left of the image 
	#into a 100x100 buffer (downsampling the image).
	#print len(scanline)
	#value = data[3000, 3000]#struct.unpack('H' * band.XSize, scanline)
	#print value
	'''
	'''
	srcArray = gdalnumeric.LoadFile('three_band/' + row[0] + '.tif')
	gdalnumeric.SaveArray(srcArray, "OUTPUT.tif", format="GTiff")
	clip = srcArray.astype(gdalnumeric.uint8)
	print srcArray[0][0, 0]
	print clip[0][0, 0]
	gdalnumeric.SaveArray(clip, "OUTPUT.png", format = "PNG")
	'''
	img = tiff.imread('three_band/' + row[0] + '.tif')
	img = numpy.rollaxis(img, 0, 3)
	#print img.shape
	img = img.transpose(2,0,1)
	#print img.shape
	#print numpy.amax(img[0]), numpy.amin(img[0])
	#print numpy.amax(img[1]), numpy.amin(img[1])
	#print numpy.amax(img[2]), numpy.amin(img[2])
	pool = Pool(processes = len(img))
	img = pool.map(convert, img)
	img = numpy.array(img)
	img = img.astype('uint8')
	img = img.transpose(1,2,0)
	#print img.shape
	#print img[0][0][0]
	tiff.imsave('three_band_8bit/' + row[0] + '.tif', img)

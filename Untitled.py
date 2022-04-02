#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import rioxarray as rxr
from rasterio.enums import Resampling
import os
import re
#set up
city = 'Mexico-Mérida' #change this to streamlit input text
datadir = '../data/cache/{}/'.format(city)
#load ALL gisa files inside directory. 
#pythonic version
prefix = [filename for filename in os.listdir(datadir) if filename.startswith("gisa")]
prefix.sort()

years_prefix = []
#get get only the years in string
for i in range(len(prefix)):
    j = re.sub(r"\D", "", prefix[i])
    years_prefix.append(j)
    
#convert to integer
years_prefix = [int(i) for i in years_prefix]


#load the rasters into local variables and append to list
gisa_list = []
counter = 0
for i in years_prefix:
    locals()['gisa_'+str(years_prefix)] = rxr.open_rasterio(datadir + prefix[counter])                                             
    gisa_list.append(locals()['gisa_'+str(years_prefix)])
    counter += 1
    
#calcualate urbanized % per year
urbanized_area = []
for gisa_year in gisa_list:
    #get raster dimensions
    y = len(gisa_year.values[0][1])
    x = len(gisa_year.values[0])
    #urban area is represented by 1, non urban is represented by 0, this sums all 1 values in the raster.
    urban = gisa_year.values[0].sum()
    #total grids in raster 
    grid = x * y            
    percentage = (urban/grid) * 100
    urbanized_area.append(percentage)
    
#generate graph
import matplotlib.pyplot as plt
plt.style.use('ggplot')
plt.figure(figsize=(8, 6), dpi=80)

plt.bar(years_prefix,urbanized_area)
plt.title('Urbanized Area for {} (max range is 25% )'.format(city))
plt.ylim([0, 25])
plt.xlabel('year')
plt.ylabel('% urban area')
plt.show()


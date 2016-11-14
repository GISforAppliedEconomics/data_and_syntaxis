library(maptools)
library(RColorBrewer)

## set the working directory.
setwd("../Session_2/Polygons/")

## load the shapefile
africa<- readShapePoly("Africa_dvp_level0.shp") #add the median household incomes for each zipcode to the .shp file 

#select color palette and the number colors (levels of income) to represent on the map
colors <- brewer.pal(6, "YlOrRd") #set breaks for the 9 colors 
plot(zip, col=colors[(africa$REGION)], axes=F)

#add a title
title(paste ("Africa Regions"))

#add a legend
legend(x=6298809, y=2350000, legend=leglabs(round(brks)), fill=colors, bty="n",x.intersp = .5, y.intersp = .5)
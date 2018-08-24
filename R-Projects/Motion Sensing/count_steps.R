rm(list=ls())

require(quantmod)

motion_sensing <- read.csv("motion_sensing.csv")

acc_x <- motion_sensing$acc_x
acc_y <- motion_sensing$acc_y
acc_z <- motion_sensing$acc_z

peaks_x = findPeaks(acc_x,0.1)
peaks_y = findPeaks(acc_y,0.1)
peaks_z = findPeaks(acc_z,0.1)

valleys_x = findValleys(acc_x,0.1)
valleys_y = findValleys(acc_y,0.1)
valleys_z = findValleys(acc_z,0.1)

px = length(peaks_x)
py = length(peaks_y)
pz = length(peaks_z)

vx = length(valleys_x)
vy = length(valleys_y)
vz = length(valleys_z)

print((px+py+pz+vx+vy+vz)/6)
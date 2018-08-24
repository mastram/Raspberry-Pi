rm(list=ls())

require(ggplot2)

motion_sensing <- read.csv("motion_sensing.csv")

plot <- ggplot(data=motion_sensing,aes(x=capture_time)) + 
  geom_line(aes(y=acc_x, color="acc_x", group=1)) +
  geom_line(aes(y=acc_y, color="acc_y", group=1)) +
  geom_line(aes(y=acc_z, color="acc_z", group=1))

plot_x <- ggplot(data=motion_sensing,aes(x=capture_time)) + 
  geom_line(aes(y=acc_x, color="acc_x", group=1))

plot_y <- ggplot(data=motion_sensing,aes(x=capture_time)) + 
  geom_line(aes(y=acc_y, color="acc_y", group=1))

plot_z <- ggplot(data=motion_sensing,aes(x=capture_time)) + 
  geom_line(aes(y=acc_z, color="acc_z", group=1))

print(plot)
print(plot_x)
print(plot_y)
print(plot_z)
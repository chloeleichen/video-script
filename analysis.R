require(tidyverse)
require(dplyr)
output <- read.csv("~/Sites/video-script/output.csv")
ref <- read.csv("~/Sites/video-script/ref.csv")

output$id = as.factor(output$id)

output.subset = output%>%filter(id==7 | id == 8 | id == 9 | id == 5 | id == 4)
ref.subset = ref%>%filter(id=='trial7' | id == 'trial8' | id == 'trial9' | id == 'trial5' | id == 'trial4')

auto_plot = ggplot(output.subset, aes(x=id, y=value)) + geom_boxplot()
ref_plot = ggplot(ref.subset, aes(x=id, y=value)) + geom_boxplot()
ref_plot
auto_plot

auto_summary = output %>%group_by(id)%>%summarise(ave = mean(value),
                                                  var = var(value))

ref_summary = ref %>%group_by(id)%>%summarise(ave = mean(value),
                                                 var = var(value))

auto_summary
ref_summary


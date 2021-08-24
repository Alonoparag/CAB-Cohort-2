# Report for sales department, May 2021
### Created by: Alon Parag
# Problems
1. last week registered users complained about non-availabilty of bikes.
    * client segment is proffesional users (focus on work days seperately and holidays/weekends seperately)
    * problem: bikes are not available
2. contribution of weather in bike demands
3. Effects of traffic and pollution on sales (bike use)

## Questions:
1. What is the total number of bikes available in that area? according to CB, aprox. 1650 bikes (source: https://d21xlh2maitm24.cloudfront.net/wdc/cabi-2012surveyreport.pdf?mtime=20161206135939)
2. Considering the week discused is the week of Dec. 25 2012 to Dec. 31 2012
3. Source new data about traffic and pollution
   
# Recommendations:
## 1. Regarding bike availability
1. Request from DataOps to track the number of total available bikes
2. Allocate a budget to create live tracking of bikes around the city
3. Create a bike allocating service to move bikes to demand zones during peak demand:
   1. Either a service within Capitalbike
   2. A pay per gig system where users can get paid/receive benefits for moving bikes during peak demand.
## 2. Regarding effects of weather on bike use:
4. Coordinate special offers/membership sale on the fall months might increase sales since members will use bikes more when weather changes.
## 3. Regarding effects of pollution on bike use:
1. Increasing the amount of time included in a single trip from 30min to 60min during pollution time, both for casual users (single trip) and registered members might increase bike use and decrease pollution
## 4. Regarding effects of traffic on bike use:
1. At the moment there is no available data of traffic to analyse its effects on bike use. I recommend to allocate budget for a project on this matter
# 1. Availability of bikes between 24.04.2021 - 30.04.2021
In the above-mentioned week bike capacity for Capitalbike was approximately 4500 bikes.<br>
Here are graphs representing bike use per hour:
<img(plots/lastweek2.png)
Even in peak hours, bike use is barely 20% of total available bike. Therefore I think that the problem lays that there are areas of high demand in which available bikes become scarce in peak hours.
# 2. Effects of weather on bike demand:
* I Checked for the effects of felt temperature, month, and described weather situation on bike use for casual users and registered users
## 2.1 Effect of felt temperatures on bike demand
* For the sake of clarity, I grouped he measured temperatures to 5 groups, and plotted the effects of the daily average temperature on bike use for casual and registered users:
* The peak use for casual users if in the temperature range of $10^o-30^o$C
* The daily bike use for registered peaks from $10^o$C without a significant difference for higher temperatures.
  
<img(plots/use-temp.png)

## 2.2 Bike demand by month
* For casual users bike use peaks in the spring (March through May), gets moderately lower during the summer (June through Aug), increases during the fall (Sep, Oct) and sinks during the winter (Nov through Feb)
* For registered users bike use raises from march(March through Oct) and sinks during winter (Nov through Feb)
<img(plots/use-month.png)
## 2.3 Bike demand by weather situation
* Bike use for both casual users sinks during rainy days, though the decline in bike use for casual users is greater than the decline for registered users
* No data was available for days with heavy weather.
<img(plots/use-weathersit.png)
# 3. Effects of air quality/pollution on bike demand
* Pollution level as measured by AQI (Air quality index) do have impact on bike use.
* In casual users, there's a slight increase in bike use from no air pollution through pollution which is unhealthy for sensitive groups, then a sharp decrease for the higher pollution groups.
* In registered users theres a mild decline between Good to Unhealthy measured air quality, and a drop measured in the highest pollution level.
<img(plots/use-pollution.png)
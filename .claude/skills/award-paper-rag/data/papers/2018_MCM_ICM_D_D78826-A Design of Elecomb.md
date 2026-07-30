# D78826-A Design of Elecomb


## 第 1 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Forofficeuseonly TeamControlNumber Forofficeuseonly
T1 78826 F1
T2 F2
ProblemChosen
T3 F3
T4 D F4
2018
MCM/ICM
Summary Sheet
A Design of Elecomb
Summary
Thisarticle mainly analyzes theproblem of charging stationnetwork construction.
In the first question, we first predict the development mode of Tesla's charging station with the
help of the control system model and find thatTeslawill push the United States to all-electrification.
Consideringthecoverageofchargingstationsandotherfactors,thenonlinearprogrammingmodelis
established according to the idea of shortest path and minimum cost to get the network of charging
stationsin theUnited States. In total, 6.55million charging stationsneed to beestablished, ofwhich
1.28millioninrural, 3million in suburban, 2.23million in urban, 1.99millionfast charging stations,
and 5.56million destination charging stations.
In the second question, we chose Ireland. First, based on the model of the first question, a total of
87700 charging stations need to be established in the case of full coverage of electric vehicles. Then
establish a degree of urgency index according to the distribution of population density and so on,
which characterizes the establishment of the charging station of the degree of urgency mentioned
above and it varies with the charging stations. Withthe index we find that the dynamic development
modeofIrish chargingstation networkisamixofbothrural and urban. Finally,based onthelogistic
growth model, wefind that it takes Ireland about 18.1years torealizeall-electric.
In the third question, we first optimize the index of urgency in the light of the different cost of
buildingcharging stationsinurban and rural areas and thelevel ofscience and technology.And then
theindexesthataffecttheurgencylevelaredescribedbythemacroeconomicindicatorsofthecountry
such as the Gini coefficient, the urban house price, using a similar way to establish an urgent degree
of urban and rural areas within the country's priority AI. If AI< 0.2, built all rural chargers first, if
AI>0.65,built all urban chargers first, whilein other cases built both ofthem at thesametime.
In the fourth question, we analyzed theimpact ofsharing cars, self-driving cars etc. onthe
popularizationof electric vehicles and discovered that theirinfluences are focus ondifferent parts.
Besides, we foundthat withthe increaseinthecoverage rates ofrapid battery-swap stations inthe
cities, it’s effect onthereduction of theoverall numberofurban charging stationstends todecrease.
Finally,wewroteahandoutfortheleaders who areattending aninternational energy summit.And
pointout thekey factors they should consider to realizeall-electriccars andset adate tobangas.
KeyWords：ClassificationSystem LogisticGrowth Urgency Index Elecomb Nonlinear
ProgrammingModel


## 第 2 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team #78826 page 1of22
1.Introduction
1.1 Problem Background
Withaggravationofthegreenhouseeffect and theairpollutionproblem, allcountries are lookingfor
new energy sources to replace conventional fuel, such as original oil or diesel oil, to ease our
increasingly serious air problems. Since the launch of hybrid cars and gas-fueled vehicles, the
exploration of new clean cars is still going on continuously. At present, the electric vehicles led by
Tesla will break through the limitation of energy and economy to a greater extent and will balance
the relationship between rapidly growing automotive demand and the environment better. The
appropriate number of charging stations with the proper distance is of utmost importance for the
popularization of electric vehicles. Compared with petrol stations, electric vehicle charging stations
occupy less space, have higher safety factor and can be better distributed in the streets and
communities, allowing people to use it more conveniently and efficiently. However, the promotion
of electric vehicles is not accomplished in a single step. It is necessary to expand the coverage of
electric vehicles gradually, improve the network of electric vehicle charging stations continuously,
andfinallyfinishtheoperationofendinggasolineanddieselvehicles.In addition,differentcountries
have different economic and cultural conditions, therefore, it need to determine the promotion time
and promotionscope according totheirspecific conditions in order to achieve betterresults.
1.2 Restatement of the Problem
According to the requirements of the problem, the final network we need to solve for the charging
station includes the number of charging stations, the location, and the number of chargers for each
station and the different needs of cities, suburbs, rural areas. At the same time, taking into account
the development and evolution of charging station network, we consider the changes of charging
stationnetwork underthe conditionsof10%, 30%, 50%and 90%respectively.
For task 1, we are supposed to explore Tesla's network of charging stations and discuss whether
Tesla is on the track of the switch to all-electric vehicle in the United States. In the light of different
chargingstationsarechargeddifferently, weneed tofigureoutthedemandsofchargingstationshow
manychargingstationsarerequired,andifeveryoneintheUnitedStatesuses,whetherwouldelectric
vehicles be Completely popularized and how will they be distributed in urban, suburban, and rural
areas.
Fortask2,firstly, wearesupposedtochooseacountry, andthentodeterminetheoptimalnumber
ofits charging stationlayout, distributionand themain factors for a certaincountry which restrict
it from turning fuel cars into electric vehicles instantaneously. Secondly, we need to plan the entire
process of building its charging network start from scratch, including the first locations to build
charging stations and the factors that influence the design of charging station. Last, we will set a
developmentscheduleofelectriccarsforthatcountry,andtakingintoaccountitskeyimpactfactors.
For task 3, considering the difference between population densities and wealth distributions and
things like that among different countries, we are going to talk over whether our original network
plan isfeasibleand what thekey factors are which trigger different modes ofnetwork growth. Then


## 第 3 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team #78826 page 2of22
discussingthefeasibility ofestablishing aclassification system and thedifferent growth models they
shouldfollowamong countries.
For Task 4, analyze the impact of technological advances on the popularity of electric vehicles,
such as theemergence of vehiclesharing, flying cars and autonomous vehicles.
For Task 5, write a handout that covers the key elements needed to consider for different types of
countries, making it easy for the leaders to make a national plan and set a date to ban the use of
gasoline.
1.3 Overview of Our Work
The construction of electric vehicle charging station network is a key point for the popularization of
electricvehicles.Theconstructionofchargingstationnetwork willbeaffectedbymanyfactors,such
aspopulationdensity,scienceandtechnologylevel,economicconditionsandcosts.Atthesametime,
different countries have their own unique geographical features and national characteristics which
make the problem more complicated. In order to solve the problem of the construction of charging
stationnetwork, webuild and optimizethe entiremodel step bystep through thefollowingsteps.
● First explore the Tesla charging station network using a high-order control system model.
Combined with the idea of cell and pixel, a nonlinear programming model is set up to minimize the
cost and find out the shortest path so as to explore the distribution of different types of charging
stationsin theUS cities, suburbs and rural areas.
● First, determine the distribution of charging stations in Ireland if it’s under the full coverage of
electric vehicles according to the charging station service capabilities and charging station costs. An
urgency coefficient is defined for each charging station to indicate the urgency of building the
chargingstation.Theindexofurgencyismainlydeterminedbythefactorssuchaspopulationdensity,
wealth distribution and service capability. According to the index of urgency, we set out the process
ofbuildingan Irish charging station network from scratch and draw themodel it established. Finally,
weuseLogisticgrowth model to determine thedevelopment scheduleof electric vehicles inIreland.
● Optimize the index of urgency based on the land cost, construction cost and the technological
factors. In ordertocharacterizethenetwork growthmodel ofcharging stationsin different countries,
we use the macroeconomic indicators of each country to describe the above-mentioned indicators of
urgency, for example, use the Gini coefficient to represent the distribution of wealth, use education
yearstorepresentthelevelofscienceand technologyand soon.Theseindicatorsareusedtoindicate
the priority of cities and rural areas in the country so as to determine the charging station network
development model that different countries shouldfollow.
●Differentkindsofnewtechnologyvehiclesaffectdifferentaspects,andweseparatelyanalyzethem
and combine the model we established to judge their impact. We also studied the impact of rapid
battery-swap with different coverage ratios in thecity onthenumberof urban chargingstations.
2. General Assumption
●AssumptionI:Thedistancebetweenanyvehiclegatheringpointandchargingstationisthestraight
linedistance between twopoints.
● Assumption II: Electric vehicles in class j are evenly distributed, but different classes of areas


## 第 4 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team #78826 page 3of22
havedifferent densities ofdistribution.
Reason:From the national level, even though thedensity distribution ofvehicles in urban, suburban
and rural areas is different, theycan beregarded as uniform compared tothe entireland area
●AssumptionIII:Nomatterhowmanyelectricpilesaresetupinachargingstation,itwillnotaffect
thecharging of electric vehicle and theelectricity consumptionof thesurroundingresidents
3. Symbols and Definitions
In thesection, we usesomesymbols forconstructing themodel as follows:
P.S.Other symbols instructions willbegiven inthe text.
4. Model Design
4.1 Model I：Estimated the Charging Station Network of US
When considering the establishment of the charging station, Tesla has two charging methods:
superchargingand destinationcharging.Thesuperchargingstation issuitableforvehicles thatdonot
want to stay while the destination charging station is suitable for vehicles that can stay for a longer
period of time. Wethink destination charging stations are more distributed among cities in the state
to meet people's daily traffic needs, and supercharging stations are more to meet the needs of long-
distancetravelers.
WhenconsideringTesla'sgrowingnetworkofchargingstations,wefirstfitTesla’schargingstation
data from 2012 to 2017 and found that it is basically in line with the linear growth model, which
reminds us of the control Engineering high order system time-domain response (the specific process
shownin Figure 4.1).


## 第 5 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team #78826 page 4of22
Figure4.1ThecontrolEngineering highorder systemtime-domain response
Itisclearthatafterweextendthetime,Tesla'smodelfitsthefirstcase,soTeslaintendstopushthe
US to fully electrified. In the process of being fully electrified, as long as it continuously increases
thenumberofchargingstationstomeetthedemandofcharging,itmustbefullyelectrifiedintheend.
4.1.1 ‘ Elecomb ’, The Model of Charging Station Network within State
The construction of charging stations in the states is mainly to meet people's daily charging
demands among all cities. We designed a pixel-honeycomb model which we call ‘Elecomb’ to
represent the specific situation of each city in the state. Among each city, the density of vehicles in
urban, suburban and rural areas is different and we use the density of pixels to represent it. Then we
usedifferentsizesofhoneycombtocovertheentirecityinordertoreachthebestcoverage.Different
sized honeycomb represents different sizes of charging station coverage area for the same service
capability. The reason why choosing the honeycomb is that it can make the overlapping area reach
theminimum,sothatasinglechargingstationcanplayitsmaximumutilityandithasstrongeconomy,
besides it is self-adaptive[1]. What’s more, the charging station in the state includes two type:
supercharging stationsand destinationstations.


## 第 6 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team #78826 page 5of22
Figure4.2Thepixel andhoneycomb
 Vehicledensity in different cities in the state
Wefoundthepopulationdensityofurban,suburbsandruralareasindifferentcitiesindifferentstates
in the United States Census Bureau [2]. We calculated the vehicle density based on the
population density and average U.S. vehicle ownership which is 0.77, and the vehicle density heat
#$
map isshown inFigure 4.3.
Figure4.3Thevehicle density heat map
 Theminimum number ofdifferenttypes of chargingstations


## 第 7 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team #78826 page 6of22


## 第 8 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team #78826 page 7of22
Table4.1Thenumber of different charging stations instate
Charging station Destination stations Supercharging stations Total stations
Urban 1.86million 0.37million 2.23million
Suburban 2.50million 0.50million 3.00million
Rural areas 1.20million 0.04million 1.20million
Total stations 5.56million 0.91million 6.47million
Figure4.4Thelocation of charging stationswithinstate
4.1.2 The Model of Charging Station Network betweenStates
We follow the U.S. road map to arrange charging stations between states, and arrange fast charging
stations along important U.S. roads so that long-distance travelers can charge their Tesla. Because
there are few people living around the interstate roads and the long-distance travelers are in a hurry
tocharge theirTesla, so wedonot set destination charging stationsbetween states.
According to this problem we can refer to the setting of the roadside service area in the United
States. The distance between every service area is about 50 miles, which covers a gas station within
theircourage,sowecanarrangeTesla'sfastchargingstationintheserviceareawhichdoesnotexceed
Tesla'smaximum mileage if it filled with fully oil. What’smore, the setting of the service area is the
result of research and investigation by most experts and it might be a good choice for Teslato set up
asupercharging station.
At the Federal Highway Administration we found that the entire main roads cover 3951098 miles
[3].Ifwesetagasstationforevery50miles,wecangettheapproximatenumberofchargingstations
needed, and the number is shown in the Table 4.2, we also show the location of the stations in the
Figure4.5.
Table4.2Thenumber of differentcharging stationsbetween states
Charging station Destination stations Supercharging stations Total stations
Rural areas 0million 0.08million 0.08million
Total stations 0million 0.08million 0.08million


## 第 9 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team #78826 page 8of22
Figure4.5Thelocation of charging stationbetween states
Note that a point on the picture represents a charging station, in order to make it more obvious we
enlarge some points, the rest of the points remain their original size and therefore it is too small to
showin thefigure.
Taking all this into account, we can conclude that the number of charging stations in the cities,
suburbs and rural areas required by the United States to achieve full coverage of electric vehicles is
shownin theTable 4.3and thelocation in theFigure 4.6.
Table4.3Thenumber of different charging stations inthe US
Charging station Destination stations Supercharging stations Total stations
Urban 1.86million 0.37million 2.23million
Suburban 2.50million 0.50million 3.00million
Rural areas 1.20million 0.12million 1.28million
Total stations 5.56million 0.99million 6.55million
Figure4.6Thelocationof charging stationsintheUS


## 第 10 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team #78826 page 9of22
4.2 Model II：The Charging Station Network of Ireland
4.2.1 The Model of Charging Station Network ofIreland
Based on the original US model, we can calculate the number of charging stations, distribution and
otherinformationinIrelandwiththesamemethod[4].In thismodel,weonlydivideIreland intotwo
types, urban and rural. At the same time, because the Ireland is a country with a small land area, the
miles traveled inside the country are basically within 100 miles. Therefore, unlike the United States,
we do not consider separately the distribution of charging stations among the counties. Instead, we
build the map based on the design of the charging station in the country, and the results are shownin
thefollowingTable4.4and Figure4.7.
Table4.4Thenumber of different charging stationsin Ireland
Charging station Destination stations Supercharging stations Total stations
Urban 42.18thousand 8.44thousand 50.62thousand
Rural areas 30.90thousand 6.18thousand 37.08thousand
Total stations 73.08thousand 14.62thousand 87.70thousand
Figure4.7Thelocation of charging stationsinIreland
According to our designed charging station network model, we can see that the main factors that
affect usare populationdensity,economicconditions, theservice capabilities ofcharging station and
othergeographical conditions.
4.2.2 Charging Station Dynamic Programming Model
Inthepreviousquestion,wecalculatedthenumberofchargingstationsinIrelandunderfullcoverage,
which is the final state we are going to reach. Wecan also calculate the location of each charging
station so that the entire dynamic programming process can be viewed as a sequential problem of
selecting each specific charging station across the network of charging stations. In order to solve the
sequential problem better, we combine the three indicators of service capability, population density
and wealth distributioninto anew one: the urgency ofsettingup a charging station,the more urgent


## 第 11 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team #78826 page 10of22
thefaster weset upa charging station here. All thedata comes from the Irish Central Bureau of
Statisticsand Wikipedia.
 Servicecapacity indicators
In the first question, we set up a model of the shortest path and the minimum number of charging
stations,which is an indicatorof maximum service capability. Using the number ofvehicles that can
be serviced by the charging station per unit area as the indicators of maximum service capability, in
orderto unify theunits ofthethree indicators, we normalizeitas
All the factors are just as important to us. We sort all of the charging stations in ascending order
according to the urgency of setting up a charging station. In the process of construction, first of all,
it’sessentialtobuildamoreurgentchargingstation.Aftersatisfyingtheneedofmoreurgentcharging
stations, we are going to build a less urgent one until the charging stations completely cover Ireland.
Basedontheweight wecalculate,wecan findoutthatthecharging stationsinIreland arebuiltatthe
sametimeintheurbanandruralandthespecificorderoftheconstructionofurbanandruralcharging
stations in each county is shown in Appendix 3. We calculate the case when the charging station
coverageis 30%, 50%, 100%, andget thefollowingresults.
Table4.5Thenumber of charging stations inIreland
Charging station coverage 30% 50% 100%
Urban 25.77thousand 41.58thousand 50.62thousand
Rural areas 0.54thousand 2.27thousand 37.08thousand
Total stations 26.31thousand 43.85thousand 87.70thousand


## 第 12 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team #78826 page 11of22
Figure 4.8Thelocationof charging stationsof different coverage
We discussed Tesla's case in the United States in the first question. Tesla hopes to attract more
customersthrough theestablishmentofchargingstations,notinresponsetotheirexistingcustomers.
Also, the problem is focus on attracting more users. As a rational enterprise, Teslawill find ways to
make more money and all countries will support the development and promote the use of
environment-friendly products. What’s more, building more charging stations is also a way to keep
upwithtrend and make moreprofit.
4.2.3 The model of Irish electric vehicle developmenttimeline
Ireland is already a developed country, so we think its vehicle ownership will remain basically
unchanged.Withthe introduction of electricvehicles, it will replace theoriginal fuel vehicles until it
is fully electrified. From the above analysis we can see that the main factor affecting the popularity
ofelectricvehiclesisthechargingstation,whichisrelatedtoeconomicconditions,populationdensity
and other factors, so thewealth distribution and populationdensity indirectly affect the popularity of
electricvehicles. Wecan viewthis as amodel of finitegrowth whose final situation isknown, which
is a logistic growth model [5]. The condition of economy, population density and other factors will
affect itsgrowth, so weset upthefollowingmodel
Then, we fit the growth of electric vehicles inthe United States based on the 2005-2016 data. The
difference between Ireland and the United States lies in the coefficients . Wesearched for the date
onWikipediaand found that thepopulation densityin theUnited States is 0.5forIreland and theper
capita GDP for the United States is 0.93 for Ireland so that we can draw the Irish model of growth
from theUnited States model andplot itsspecific growth in Matla2016, justas shownin Figure4.9.


## 第 13 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team #78826 page 12of22
Figure4.9TheIrishelectric vehicle development timeline
In the figure, we can see the time needed to develop to different stages, and it takes about 18.1
years for Ireland to reach the fullcoverage of electric vehicles.
4.3 Model III：The Model of Classification System
First of all, in the above model, population density distribution and wealth distribution have been
taken into account. Therefore, population density distribution and wealth distribution have no effect
on the construction model of our charging station network. However, considering different
geographical issues, we think this indicator is used to determine qualitatively whether this countryis
suitableforestablishingachargingstationinthefirstplace.Ifappropriate,wecanstilluseouroriginal
model,ifnot, thereisnoneed to establishacharging stationin thisplace, suchasVenicewhereis no
need to build a car charging station there. Therefore, Australia, China, Indonesia, Saudi Arabia and
Singaporegivenintheproblemareallapply totheabovemodel except thatthegrowthpattern ofthe
charging station network ineach country isdifferent.
4.3.1 The Optimization Model of the Indicator ofUrgency
We consider the key factor triggering different growth networks to be the urgency of setting up
chargingstationsindifferent parts ofthecountry.In theabovemodel,wedid notdistinguish thecost
of establishing charging stations in rural and urban areas. However, in fact, the construction costs of
ruralandurbanareasaredifferentandithaveagreatinfluenceontheconstructionofchargingstation
network, sowe optimizetheindicatorin terms ofcost.
Total costs include construction costs, land costs. The cost of land is mainly related to the land
price in urban and rural areas, and the cost of construction is related to the country's technological
level. Therefore, we establish thefollowingcost factorformula:
+ + i i
 u= ∗u ∗  +  ∗ 


## 第 14 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team #78826 page 13of22
Then according to theindicatorof urgency after optimization,we can see that themain factors that
lead to the different growth networks are population density distribution, wealth distribution, service
capacityandcost.Inordertobetterexplaintheinfluenceofthesefactorsondifferentgrowthnetworks,
we take Ireland as an example to see how the changes in population density distribution and wealth
distributionaffect theoverall growth network, theresult is shownbelow:
Figure4.10Thechange ofthe charging stationnetworkconstruction
4.3.2 The model of classification system
Different countries have different growth modes, but we can classify their growth models into three
categories according to the macroeconomic indicators provided by each country. The specific steps
ofthemodel are as follows:
According to the main influencing factors of the index of urgency, we describe these factors to
different macroscopic indexes, the reason why we choose macroeconomic indexes is that they are
easier to obtain and each country is calculated in the same way, and indexes have greater


## 第 15 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team #78826 page 14of22
representation and economy.
Finding the corresponding index data in the global economic database and considering that there
is no gap between urban and rural areas, we can get an equilibrium point of AI = 0.4. Both sides are
of normal distribution, so we get the range of AI under different growth network, just as Figure 4.11
shows
Figure4.11Therange ofAI under different growthnetwork
Therefore,weestablishaclassificationsystem,eachcountryinputsitsownurbanpopulation,rural
population, urban area, rural area, Gini coefficient, average years of education to get the relative
superiority index, and thus come totheirown charging station growthnetwork.


## 第 16 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team #78826 page 15of22
5. The Impact of Different Technologies on the Popularization
of Electric Vehicles
With the development of technology, the emergence of new types of vehicles and the charging and
dischargingmethodswillhavedifferenteffectsonthepopularityofelectricvehicles.Inthisquestion,
wemainly consider theimpact ofsharing cars, self-driving cars, car quick-changers andflying cars.
First we consider the impact of shared cars. With the emergence of shared cars, the demand for
electric vehicles, fuel vehicles will decline, which to some extent hurts the popularity of electric
vehicles. However, as the number of cars decreases, the service capacity of individual charging
stations will increase, so it will be possible to accelerate the popularization of electric vehicles by
settingupfewerchargingstationstoreducethetimeforbuildingtheentirechargingstationnetwork.
Therefore, the emergence ofshared cars forthe popularity ofelectricvehicles have pros andcons
such itshould not begeneralized as awhole.
Second, we consider the impact of autonomous vehicles. We originally designed the charging
station network without considering the impact of human factors, and we think the vehicles are all
following the preset shortest path, but in reality it is not the case. Therefore, the model in the first
question can be improved by adding human factors. At the same time, autonomous vehicles are a
totallysystem-operatedvehiclethatmakescarssmarterandalleviatesmanytrafficproblems,thereby
accelerating thepopularityof electricvehicles.
Third, consider the impact of rapid battery-swap stations. Rapid battery-swap stations are mainly
to greatly reduce the charging time of electric vehicles, and the service capability of the whole city
has been improved. What’s more, we think that the rapid battery-swap stations can be regarded as a
collection of charging stations with a certain service capability and generally appears in urban areas
where the vehicle density is relatively high. Therefore, we consider the change in the number of
charging stations as a whole when the penetration of the rapid battery-swap stations are improved.
Then westudy thecase oftheUS and Ireland and plottheFigure 5.1.
Figure5.1Thechanges intotal number of stations
It can be seen from the figure that the emergence of rapid battery-swap stations will reduce the
number of the stations as a whole, and its rate of descent will be slower and slower as the degree of
coverage increases. The emergence of the substation makes the environmental benefits of electric
vehicles andthe rapid benefitsof rapid charging mutually reinforcing, improvingthe overall


## 第 17 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team #78826 page 16of22
effectiveness.
Finally, weconsider issues such as flying cars and Hyperloop. They certainly willhave an impact
onthepopularity ofelectric vehicles, butthe way theyaffect it isdifferent.
6.Strengths and Weaknesses
6.1 Strengths
● Datahas high security andreliability
●.The model takes full account ofthedifferences between urbanand rural areas in allaspects.
● PredictingtheTesladevelopment modelwith control engineeringcontent.
● The density of vehicles in different regions is represented by pixels, and the cell is used as the
charging station coverage model, thereby ensuring the coverage area while ensuring the minimum
overlap area.
6.2 Weaknesses
●Duetotimeanddataconstraints,themodelfailstoconsideratethedifferenceswithinurbanorrural
areas.
● In the process of calculation, the data that can not be found in some areas are replaced with the
previousdata.
● Rather than strictly considering the difference in the number of charging piles in charging stations
in different regions, the number of charging piles in the same type of charging station is considered
tobe thesame.
7. Future Improvements
● If we have more time, we will first consider the differences in the number of charging piles in the
same type of charging stations. Different charging piles represent different service capabilities, so
thatthe area that they can cover will change. Ourmodel will bemorerealistic.
● When designing model 1, taking into account the possible waiting time for the electric vehicles to
charge in the charging station. At the same time consider the impact of some human factors on the
model.
●Find more reliabledata to fit thefuture growth model ofelectricvehicles and reduceerrors.
8.Conclusion
●In the future, it is very likely that among the majority of countries, electric vehicles will be
completely popularized. Besides, the stagnation of the rest countries could be attributed to their own
geographical reasons, such as Indonesia, Veniceand other countries orregions.
●The main influencing factors which trigger different modes of network growth contain the density
of population, the distribution of wealth, the strength of science and technology and cost. Besides,
different factors may cause differenteffects.


## 第 18 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team #78826 page 17of22
● The Ginicoefficient has a great influence onthedevelopment ofthecharging station network,
whilethepopulationdensity has onlya slightimpact.


## 第 19 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team #78826 page 18of22
Handout
Distinguished leaders:
With the increasing prominence of resources and environmental issues, the new type of electric
vehiclescan largelyalleviatevariousproblemscausedbyautomobileexhaustemissions.Meanwhile,
with the advancement of science and technology, all kinds of technologies of electric vehicles have
becomeincreasingly sophisticated, which laid a good foundation for itspopularity.
Through our research, we can know that the most important factor influencing the popularization
of electric vehicles is the perfection of charging station network and the dynamic process of its
construction. Different countries have different economic and technological levels as well as their
uniquenationalcharacteristics.In viewofthissituation,wehavedevelopedasystem todetermineits
modeofdevelopment based onsuchnotablefeatures liketheGini index,urban population, and rural
population. All you need to do is to input Gini coefficient, rural population, urban population, urban
area, rural area, urban land price, rural land price and the average schooling years of your country
into our system. Our system will give you an indicator of in your country's relative priority between
urban and rural areas. And you can find the right growth pattern for your country based on the value
oftheindicator.
Regarding the date of the ban on gas, the total coverage of electric vehicles based on the world
average is about 163 years, but the degree varies with countries. All you need to do is to input the
population density, urbanization rate and GDP per capita into our Logistic Growth Model based on
your own situation to find the time it takes for the country to reach full coverage of electricvehicles,
which isthe timethat gasoline shouldbebanned.
Since each country has its specific situation, there will be some inevitable errors and uncertainties
in our model, but it can provide a general development forecast for different countries to better
achieve the full coverage of electric vehicles, I hope our model can benefit your country to some
extend, thank you for coming to thismeeting.


## 第 20 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team #78826 page 19of22
References
[1] Marzetta, T. L. (2010). Noncooperative cellular wireless with unlimited numbers ofbase station
antennas. IEEE TransactionsonWireless Communications,9(11),3590-3600.
[2]’theUnited States Census Bureau’https://www.census.gov/
[3] https://en.wikipedia.org/wiki/List_of_United_States_Numbered_Highways
[4]’Central Statistics Office’http://census.cso.ie/sapmap/
[5]Giordano, F.R.,Weir, M. D., & Fox,W.P.(2009). Afirst course in mathematicalmodeling
=.,15(4), 155-166.
[6] Brownley, C. W. (2016). Foundations for Analytics withPython: FromNon-Programmer to
Hacker.O'ReillyMedia, Inc.


## 第 21 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team #78826 page 20of22
Appendix 1
Thescatter plotof Tesla's sales data.


## 第 22 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team #78826 page 21of22
Appendix 2
Thelocation ofcharging stations inLubbock, US.


## 第 23 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team #78826 page 22of22
Appendix 3
Thespecific order oftheconstruction ofurban and rural charging stations in each county.
1 DublinCity urban_area 32 Roscommonurban_area'
2 Limerick City and Countyurban_area' 33 Waterford City andCountyrural_area'
3 Kildareurban_area' 34 Wicklowrural_area'
4 Cork Countyurban_area' 35 Monaghanurban_area'
5 Cork Cityurban_area' 36 Sligo urban_area'
6 DublinCity rural_area' 37 Carlowrural_area'
7 Waterford City andCountyurban_area' 38 Meath rural_area'
8 Wicklowurban_area' 39 Fingal urban_area'
9 'Carlowurban_area' 40 Offaly rural_area'
10 Meath urban_area' 41 Wexford rural_area'
11 Offaly urban_area' 42 Kilkenny rural_area'
12 Wexford urban_area' 43 Tipperary rural_area'
13 Kilkenny urban_area' 44 DunLaoghaire-Rathdown rural_area'
14 DunLaoghaire-Rathdown urban_area' 45 Galway City rural_area'
15 Tipperary urban_area' 46 Galway Countyrural_area'
16 Galway City urban_area' 47 SouthDublin rural_area'
17 SouthDublin urban_area' 48 Louth rural_area'
18 Galway Countyurban_area' 49 Leitrimrural_area'
19 Limerick City and Countyrural_area' 50 Westmeathrural_area'
20 Louth urban_area' 51 Laois rural_area'
21 Leitrimurban_area' 52 Donegal urban_area'
22 Westmeathurban_area' 53 Kerry rural_area'
23 Laois urban_area' 54 Clarerural_area'
24 Kerry urban_area' 55 Mayo rural_area'
25 Clareurban_area' 56 Cavan rural_area'
26 Mayo urban_area' 57 Longfordrural_area'
27 Cavan urban_area' 58 Roscommonrural_area'
28 Kildarerural_area' 59 Monaghanrural_area'
29 Cork Countyrural_area' 60 Sligo rural_area'
30 Cork Cityrural_area' 61 Fingal rural_area'
31 Longfordurban_area' 62 Donegal rural_area'

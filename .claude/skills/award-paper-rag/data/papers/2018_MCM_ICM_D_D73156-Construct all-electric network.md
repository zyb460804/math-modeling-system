# D73156-Construct all-electric network


## 第 1 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
TeamControlNumber
Forofficeuseonly Forofficeuseonly
73156
T1 F1
T2 F2
T3 F3
T4 ProblemChosen F4
D
2018
MCM/ICMSummarySheet
Construct all-electric network
The transformation from gas vehicles to electric vehicles becomes a hot topic all overthe
world. In order to get the schedule of the location of charging stations and predict the process
oftransformation tendency, weestablish several models to solvethequestions.
For question 1, we firstly establish a model based on queuing theory. Furthermore, we
construct a multi-objective programming model based on information of the current Tesla
charging network in the US. With the help of Matlab, we find that Tesla is on track to allow a
completeswitchtoall-electricintheUS.Weobtainthatthenumberofchargingstationsneeded
is about 1.7million when all gas vehicles transform to electric vehicles, and the distribution
proportions ofcharging stations inurban, suburban and rural areas are67:23:10.
For question 2, we establish the site selection models of charging station for urban,
suburban and rural areas of South Korea, separately. Combining with the programmingmodel
whichweestablishedinproblem1,weobtainthenumber,locationanddistributionofcharging
stations in Korea. We get the key factors that affect our plan are the building cost of chargers
and the government investment. By considering six indexes, we establish a logistic model.
Usingthismodel, we firstlygive thetimelineofthefull evolution toelectricvehicles. Wefind
that the key factor for this situation is policy orientation. Then we further predict the number
oftheelectricvehicles ofurban andrural areasinSouthKoreaseparately. Through thelogistic
model, we obtain that South Korea should give preference to build charging station in cities.
Similarly, we find that the two key factors which influent our model most are wealth
distributionand government investment. Additionally, weintroduceaconcept called lagindex
tomeasure therelationship between thecar and thechargingstation.
For question 3, we establish a classification system through Q-type clustering model.
According to different national conditions, we divide the countries into three categories.
Through some analysis of the Q-type clustering model, we find out that the key factors that
trigger the selection of different approaches to growing the network are policy orientation,
wealth distribution and government investment. According to these factors, a targeted electric
network development plan has beenproposed.
For question 4, to study the influence of various new technologies, we set several
indicatorstoestablish ourmodels, such as GDPand OPH. Byanalyzingourevaluation model,
we find that these technologies impact the growth rate of electric vehicles, which contributes
to the growing popularity of electric vehicles. Besides, the population of electric vehicles will
bedriven bythesetechnologies.
For question 5, we prepare a one-page handout for the leaders identifying the key factors
which they should consider as they return to their home country to develop a national plan to
migrate personal transportation towards all-electric cars and set a gas vehicle-ban date for
different countries.


## 第 2 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
数模乐园整理提供，更多数学建模资源请关注微信公众平台“数模乐园”或官方网站www.smlyor.com获取
Key words:siteselection model, logisticmodel, Q-typeclustering model, electricnetwork


## 第 3 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#73156 Page1of27
Content
1 Introduction....................................................................................................................2
1.1 Background..........................................................................................................2
1.2.Restatement oftheProblem................................................................................3
1.2 LiteratureReview................................................................................................3
1.3 OurWork.............................................................................................................4
2Assumptionsand Justifications......................................................................................4
3Distributethecharging stations intheUS......................................................................4
3.1 Concepts introduction..........................................................................................5
3.2 All-electricevaluation model..............................................................................6
3.2.1 Themodel construction............................................................................6
3.2.2 Model solutionand analysis.....................................................................7
3.3 Distributionoptimizationmodel..........................................................................8
3.3.1 Themodel construction............................................................................8
3.3.2 Model solutionand analysis.....................................................................9
4StudyonSouthKorea.....................................................................................................9
4.1 Urban charging stationlocation model..............................................................10
4.2 Suburban charging stationlocation model........................................................12
4.3 Rural charging stationlocation model...............................................................12
4.4 Logisticmodel...................................................................................................13
4.4.1 Index definition.......................................................................................13
4.4.2 Themodel construction..........................................................................13
4.4.3 Model solutionand analysis...................................................................14
4.5 Answers ofthe Questions..................................................................................14
5Create aclassification system.......................................................................................16
5.1 Themodel construction.....................................................................................17
5.2 Model solutionand analysis..............................................................................17
6Commentontheeffect ofnew technologies................................................................18
6.1 Themodel construction.....................................................................................18
6.2 Model analysis...................................................................................................18
7SensitivityAnalysis......................................................................................................19
8Conclusions..................................................................................................................20
8.1 Strengths............................................................................................................20
8.2 Weaknesses........................................................................................................20
8.3 Model extension................................................................................................20
9AHandout totheLeaders.............................................................................................20
10Reference....................................................................................................................21
11Appendix....................................................................................................................22


## 第 4 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#73156 Page2of27
1 Introduction
1.1 Background
Nowadays,fossilfuelandtheenvironmentprotectionhavebecomethehottestissues
intheworld[1].Themaintransportationsallovertheworldarebasedonfossiloil,which
has caused serious environmental pollutions. Since the resource of fossil fuels is limited
andit always leads to the pollution, thetransitionofit to more clean energyis inevitable.
In order to realize this aim, electric vehicles which are the representatives of new energy
vehicles, have been recognized as the main development direction of the transformation
in theautomotiveindustry in the21stcentury[2].
It is well established that electric vehicles are high efficiency, low noise and nearly
zeropollution[3].Theadvantagesofelectricvehiclesareobvious.Hence,theyhavebeen
widely used all over the world. To promote the large-scale development of electric
vehicles,itisnecessarytoimprovethecorrespondinginfrastructure. Asanimportantpart
of the construction of electric vehicle facilities, charging stations are crucial to the
development of the entire electric vehicle industry. Where and how many do we need to
construct the charging stations? Selecting the correct location and estimating the number
ofcharging stationsare veryimportant.
1.2. Restatement of the Problem
When we transform the gasoline and fossil fuel cars to electric vehicles, we need to
consider the network of charging stations and the growth of them over time. In order to
make a development schedule of the charging stations for a country, we are required to
answer thefollowing questions.
1.BuildamodeltojudgewhetherornotTeslacan switchtoall-electricall overUS.
Distributethecharging stations incase of fullelectric.
2.Select acountryto determine thenumberand location ofcharging stations. Make
atimelineforthe fullevolutionandfindoutthekeyfactorsthatmatteryour modelmost.
3.Considerwhetherthemodelissuitableforthecountrieswithdifferentgeographies,
population density distributions, and wealth distributions situations, and discuss the
feasibility ofcreating a classificationsystem.
4. Consider that how new technologies affect the analysis of the increasing use of
electricvehicles.
5. Write a one-page handout for the leaders to identify the key factors they should
consider and set agas vehicle-ban date.
1.2 Literature Review
Under the pressure of energy conservation and low carbon, the research on the
electric vehicles and the construction of charging station network have made great
progress.In the planning of charging facilities, some researchers point out that the layout
of charging stations are affected by the number of electric vehicles [4]. The construction
of power stations needs to meet the requirements of traffic density. Only in this way can
they develop in harmony. Taking California for example, we know that there are one
million new energy vehicles in existence [5].By combining thesupply anddemand of


## 第 5 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#73156 Page3of27
Californiaelectricity,theybuildlinearandnonlinearmodels,aimingatsavingenergyand
reducing emissions. Wang [6] proposed a new method for the layout of charging station.
In[6],theyconsideredseveralinfluentialfactorssuchastechnical level,holdingcapacity
and charging behavior of electric vehicles. However, the proposed load-shedding space
segment prediction method does not take into the driving features, using mode and
charging mode into account. The weight of the method is subjective and the prediction
error is large.
Forselectingthelocationofchargingstations,Holzman[7]aimedatminimizingthe
square distance of user-to-facilitylocations, and constructed the location selection model
based on network planning. Then he discussed and expanded the model with specific
conditions. Additionally, the authors [8] build the optimization model, whose algorithm
was based on game theory. Hakimi [9] conducted a systematic study of the selection of
facility location. He considers the location of one or more facilities within a network,
providing that the total distance or the maximum distance between the facility and the
point is minimized. The theory makes the selection of charging station furtherdeveloped
onthebasis of theoriginaltheory.
However,thedevelopmentofelectricvehiclesarestillattheinitialstage.Thelayout
planningtheoryof charging facilityis also under exploration and there are still verylittle
studies about the network of charging stations. Although some achievements have been
made, we still have lots of the uncertainties to study. In this paper, we propose a brand-
new model to imply the location of charging stations. Furthermore, we extend our
models tosuit different circumstances.
1.3 Our Work
Firstly, we establish a multi-objective programming model to calculate the number
of charging stations. Besides, we establish a site selection model to determine the
distribution in urban, suburban and rural areas. Then we choose six indexes which affect
thenumberoftheelectricvehicles.Accordingtheseindexes,weestablishalogisticmodel
topredict thenumberoftheelectricvehicles. Wecanfindoutthekeyfactors throughthe
predicted data. Furthermore, we can analyze the relationship among the different key
factors. Next, we expandourmodel. Weestablish aclassification system through Q-type
clustering model to analyze the electric network development plan for countries in
differentcategories.Wealsoconsidertheeffectofvariousnewtechnologies,andanalyze
the status of each technology and the trend of future development. Finally, we write a
handoutfortheleaderstoofferthemsomeeffectiveadviceonthedevelopmentofelectric
network.
2 Assumptions and Justifications
 The charging station which has been built cannot be removed. Since the
construction of charging station costs a lot of manpower and financial resources, the
demolitionofit will cause greaterlosses.
 The candidate points of charging station are obtained through reasonable
analysis and rigorous demonstration. Because if the charging station is built in an
areawith poor orunsafe conditions,it will lead tofewercars tobecharged.


## 第 6 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#73156 Page4of27
 Eachchargingstationwillnotbreakdownduringchargingprocess.Becausethe
charging stationnetwork will beregularlymaintained.
 Vehiclearrival obeysto Poisson distribution. Itis demonstrated in statistics.
3 Distribute the charging stations in the US
Task one requires us to determine whether Tesla isontrack to allow afull switch to
all-electric in the US, and give the distribution of charging stations based on all-electric
condition. Firstly, we searching the population density and car ownership per capita of
different states of America. According to population density, we divided the United
States into urban, suburban and rural areas. Secondly, the total amount of cars in each
area is determined by the amount of car ownership per capita. According to queuing
theory, we calculate the average waiting time for car charging. Then, we can get the
number of supercharging stations theoretically needed. We compare it with the actual
numberofchargingstations,determinewhetherornottheUScan go all-electric.Finally,
with the goal of minimum cost and minimum waiting time, we build a multi-objective
optimization model tocalculatethe numberofcharging stations required in eachregion.
3.1 Concepts introduction
 Populationdensity
Let ρ denote thepopulation density, i.e. the numberof peopleper square kilometer.
i
ThepopulationdistributionsintheUSareobtainedfromtheUSCensusBureau[10].We
dividetheUnited States intothree regions based ontheintensityof thepopulation.
When the population density is greater than 150, the area is the urban. Similarly,
when the population density is between 50 and 150, the area is suburban. Otherwise, the
areais therural. Thedividing results are as follows.
Figure1:ThepopulationdensitydistributionintheUS
 Carownership percapita
Let H denotethecar ownership per capita, which means theaverage number of
i
cars owned by each individual. According to the U.S. official statistic [11], the overall
carownership percapitais0.8.Wherein thecarownershippercapita in urban, suburban,
rural areas are 0.94,0.83,0.60respectively.
 Connectivity rate
The distance between two adjacent electric vehicle charging stations has a great
influence on the convenience of charging. The closer the charging station is, the higher
the charging convenience will be. In general, a supercharging station can provide up to
170 miles of power. If the distance between two charging stations is less than or equalto
thisvalue, then thecar can provide an endless stream ofelectricity. That is to say,the


## 第 7 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#73156 Page5of27
distributionofcharging station is reasonableto satisfy thecharging needs. Therefore, we
define theconnectivity rate toreflect therationality of charging stationdistribution.
number of adjacent stations < 170 miles away
connectivity rate =
number of all adjacent stations /2
Wefindthelocations ofall the chargingstations builtand to bebuilt from theTesla
website, and mark them on the US map. Then we connect all adjacent charging stations
whose distanceis less than 170miles.The road mapis shown asbelow.
Figure2:Connectivitydiagram
Asshowninfigure2,thecoverageofthechargingstationshasbasicallycoveredthe
entireUnited States, especiallyin areas with ahigh population density. After calculation,
we find that the connectivity rate has reached 71%. Therefore, we have initially judged
that Tesla is making the United States on an all-electric track. Next, we will analyze in
detail through modeling.
3.2 All-electric evaluation model
3.2.1 The model construction
1) Actual number ofelectric vehicles
The totalnumberof electric vehicles ina region will beaffected bymany factors.
The macroscopic parameter ofrangeis S which stands for theacreage of i area. The
i th
parameter P represents the percentage ofelectric vehicles in i area. Hence, wecan
i th
get theequation between thetotal numberof electric vehicles and thevarious factors.
n  S  H  P
i i i i i
2) Theoretical number of electric vehicles
When the number of electric vehicles reaches a certain level, there needs to be
enough charging stations to serve it. Because the supercharging station is much more
expensive than the destination charging station, we first consider the number of super
chargingstation.AccordingtothesurveydataofGeneralMotorsintheUnitedStates,the
utilization rate α of a public charging station is 35%. The electric vehicle can run T
miles when charging once at a supercharging station. According to the average annual
driving distance L of the car and the average number of driving days D , we can
calculate the number of times ( N ) a car is charged on the supercharging station every
sc
day.
αL
N =
sc DT
Throughmultiplyingthetotalnumberofelectricvehiclesineachareabytheaverage
number of charging times each day, we can get the total number of times all the vehicles
in the area needs to be recharged daily. For the charging stations, these are the number
N ofcharging vehicles they need toservice each day,
itotal


## 第 8 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#73156 Page6of27
N =N ×n .
itotal sc i
Vehicle arrival is a typicalPoisson distributionevent [12].Theaverageservicetime
of a supercharging station are t hours every day. There are λ vehicles arriving at
charging stationevery hour. Poissondistributionis expressed asfollows,
e-λt(λt)J
P (t)= (J = 0,1,2,...).
J J!
A supercharging station can be viewed as a single service desk model M/M/1. The
average service time per car is μ . When the vehicle arrives at the charging station at a
Poisson distribution, if at this time there are a number of vehicles are charging, then the
vehiclemust wait in line,
λ2
L =
q μ( μ-λ)
Iftheaveragenumberofarrivalsisgreaterthanacertaindegree,carsthatarrivelater
cannotbefullychargedintime.Undertheconditionofstablesystem,theaveragewaiting
timewillincrease first, and then close to astablevalue. That is theaverage waitingtime
L
= q.
T
qSC λ
Givenawaitingtime,we cancalculatethetotal numberofcars that asupercharging
stationcan servicen =λt.
sc
3.2.2 Model solution and analysis
In a charging station, waiting time is generated when more vehicles are queued for
charging. The longer the waiting time, the lower the quality of service. In order to make
electric vehicles more convenient to charge, we have to shorten the waiting time for the
car. Therefore, thenumber ofcharging stations need tobeincreased. Theconvenience
index CI isdefined to reflect theease ofcharging in each area.
i
N
CI = itotal
i n ×r
sc i
Where r denotes the actual number of supercharging stations.
i
When the actual number of vehicles needed to be charged is less than themaximum
numberofvehiclesthatthechargingstationcansupply,thechargingstationisconsidered
to beconvenient. It can beattributed to thefollowingformula.
convenient ,CI 1
type  i

inconvenient ,CI 1
i
All theconvenient areas are marked with dark blue, and shownas below.
Figure3:Convenientarea
From Figure 3, we can clearly see that the convenient area has a wide coverage and
basically covers the entire United States. Based on the previous connectivity map in the
United States and the connectivity rate of 71%, we have reason to believe that Tesla is
expected to achieve full electrification intheUnited States.


## 第 9 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#73156 Page7of27
3.3 Distribution optimization model
3.3.1 The model construction
The distribution of charging stations need to consider many aspects, while at the
same time it is subject to economy, time and other factors. In order to obtain the optimal
distributionprogram, weestablish a multi-objectivemodel withflexibleconstraints.
Goal of minimumcost:
On the basis of ensuring a rational distribution of charging stations, we should
minimizethecost ofour program. Sincethe prices of supercharging stations and
destinationchargingstations(C and C ) are different, weneed to consider thetotal
SC DC
buildingcost of them. Thenumberof them are r and r respectively. So, weget
SC DC
that
min Z   r  C   r C .
i DC DC SC SC
Goal of minimumwaiting time:
Thepurpose ofbuildinganumberofchargingstationsistoshorten the waitingtime
for the car to be charged, thereby improving service convenience. We consider the
average waiting time of the supercharging station and the destination charging station
simultaneously, and take their respective number as a weighting factor. The totalwaiting
timeobtained shouldbeas small as possible
minT  T qDC  r DC  T qSC  r SC ,i 1, 2,3 .
iq r r
DC SC
Constraintofdistance:
Whenthevehicletravels alongtrip, it needs enough power tosupport it. According
to the average annual driving distance L of the car and the average number of driving
days D,we can calculate thecharging miles thecar needs every day
L
A= .
D
Wherein α is theutilization rateof apubliccharging station
Hence, the total charging miles required in each area can be obtained from the
following formula
A A  n
itotal i i
When the distribution of charging stations is reasonable, the power provided by the
charging station should be greater than the power actually needed. Thus the vehicle can
travel along distancewithout consuming all theelectric. So,theconstraint is:
2
A  l n r k  DC,SC 
itotal k k k
k
Constraintofconvenience
Whenthe totalnumberofvehicles that thecharging stationcan serveis greater than
theactual number ofvehicles, thechargingstationcan satisfythe dailyneeds. According
to convenience index defined before, weshouldincreasethenumberof chargingstations
while reducing the waiting time at the same time. Therefore, the convenience index
should beless than orequal to1.
n
CI  i 1
i n r n r
DC DC SC SC


## 第 10 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#73156 Page8of27
Constraintofvehicles
The biggest difference between destination charging (DC) and supercharging (SC)
lies in the charging efficiency. The former costs a long time to charge, thus providing a
longtrip.Thelattercostsashorttimetocharge,butprovidingarelativelylongtrip.Hence,
thelatter onehas a higher charging efficiency. Nowwe assume that T represents the
DC
daily power supplytimeofDC, t denotes afully charged time,while l stands for
DC DC
thelength of triponecharge can provide. So, thecharging efficiency ratio between DC
andSC isas follows
EF
P  DC  T DC l DC T SC l SC .
efficiency EF t t
SC DC SC
Therefore, under thecondition ofthesame electricity supply, therelationship
between thenumber ofDC stationsand SCstations is r  r  P .
SC DC efficiency
In addition, therequired numberof charging stations should begreater than orequal
to theactual number ofcharging stations. So,the constraint is:
n
 i
r
SC
n
SC
To sumup,the wholeoptimization model isas follows
3.3.2 Model solution and analysis
According to data statistics, a charging station consists of 8.8 chargers in general.
By using MATBLA to solve the optimization model above, we obtain that the US needs
about 15 million chargers in all. Therefore, 1,704,500 charge stations are required. After
calculation, we get that urban area needs 1,142,015 charge stations, suburban area needs
392,035chargestations, rural area needs 170,450charge stations.
Table1:Distributionresults
Area Number ofcharging stations
Urban area 1,142,015
Suburban area 392,035
Rural area 170450
ThewholeUS 1,704,500


## 第 11 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#73156 Page9of27
4 Study on South Korea
South Korea is a typical developed country in Northeast of Asia. It has obvious
urban-suburban-rural divisions. The population density distribution is as follows.
Wherein thebluearea is thedensely populated area.
Figure4:ThepopulationdensitydistributioninSouthKorea
According to the difference in population density, we divide South Korea intothree
parts: urban area, suburban area, rural area. For different areas, we will build different
charging stationsiteselectionmodel.
4.1 Urban charging station location model
Since there are many electric cars in the city, it is necessary tobuild a large number
of charging stations. On the one hand, there are many restaurants, hotels and shopping
malls in the city, most of which have paring lots. Hence, the construction of charging
station can rely on the parking lots of these consumption places. On the other hand,
accordingtothelocation ofgasstation,thechargingstationscan alsobecentrallylocated
next to the main arterial roads with relatively large traffic volumes. We take Seoul as an
exampleto distributethechargingstations.
1) Total construction cost andaverage waitingtime
The followinganalysis is similartotask one,so we willnot elaboratein detail.
The totalelectricvehicles in Seoul is
n   S  H P .
seoul seoul seoul seoul
The numberofcharging times fora car every day is:
L
N= .
DY
The numberofvehicles needed to charge every day is:
N =N×n .
total seoul
The averagecharging miles ofpubliccharging station every dayis:
L
A= .
D
The totalcharging miles required every dayis:
A  A n .
total seoul
Accordingtothedriving dataofMinistry ofLand,Infrastructure andTransport of
Korea, South Korean residents mainly drive outfrom 9:00 to17:00. Hence, thecharging
timeofthepubliccharging station is T  8 hours. Besides, most drivers tend tochoose


## 第 12 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#73156 Page10of27
supercharging when going out.So,let thecharging timebet30minand the mileage
be Y  170 miles. Theaverage waiting timeofcharging is T .
qseoul
The totalcost of constructing charging stationsin Seoul is
Z  r C .
seoul seoul
2) Location ofcharging stations
Our goal is to select a plurality of consumption places or gas stations in a city to
install charging stations. A charging station should meet the charging needs of allnearby
vehicles. If we employthe traditional shortest path location model, the selected locations
areconcentratedinthecitycenter,whichwillheaventhetrafficpressure.Onthecontrary,
if the charging stations are located on the edge of the city, it will be time-consuming for
the vehicles to charge. Therefore, the location should take the distance, time and traffic
factors intoaccount.
Wedeterminethe city center based on the electronic map, and then constructa
nn weighted network map according to the size of the city. The innermost four
squares are thefirst level and theoutward twelvesquares are thesecond level. There are
n/2 levels in all. Thelength ofeach square, that is, the initial weight is 1.If the actual
positioncorresponding to thesidelength appears lakes, rivers, oceans and deserts, the

default valueofthe sidelength is .
In order to reduce the impact onthetraffic pressure, we introducecongestion index
 ofsidelength v v .Forthesidelengthatthe i level, weneed to updatetheweight
jk j k th
w of v v at thetimeofthe m calculation
jk j k th
n n
w 1(mi) ,i1 ,.m1
jk 2 2
Therefore, thesum ofshortest pathfrom onepoint to any otherpoint is:
 w  x
jk jk
x vv
The 0-1variable indicates whetheror not to choose ,
jk j k
1choose v v
x = j k
jk 0 not
Based ontheoptimizationmodel of task one, we add a newgoal of shortest path. It
will makethedistance to thecharging stationas short as possible.
So,the newaddedgoal is
min  w  x .
jk jk
The determination oftheshortest pathneeds to bewithin then n grid range. So,
thenew constraintis
 1 j  1
n n 
 x x  1 j  n
jk kj 
k1 k1  0 j  1, n
To sumup,the wholemodel is asfollows
minZ  r C,
seoul seoul
min T ,
q seoul
min  w x .
jk jk


## 第 13 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#73156 Page11of27
Chargers should be dispersed to the city first. Then, according to the characteristics
of urban construction, charging stations are formed. They are distributed near the
consumptionplaces and gas stations.
4.2 Suburban charging station location model
We consider that the area between cities are suburbs. Since the suburbs are mainly
located on both sides of the road with large traffic flow, we simplify the question to the
highway charging station selection question.
Themacroscopicparameter VF is the traffic volume in hhours at the i road.
ih th
The totalnumberof suburban electric vehiclesis:
n 24
n  P VF
sub ih
i1h1
The averagenumber ofvehicles needed tocharge everyday is
N =N×n .
total sub
The totalcharging miles required every dayis
A  A n .
total sub
Therefore, thetotal cost ofsuburban charging stationconstruction is
Z  r C.
sub sub
Thespecific location along thehighway does not affect theoptimizationobjectives
andconstraints. So,we can get theoptimizationmodel directly.
Sincethedistancebetweenadjacentchargingstationsdoesnotexceed170miles,we
can combine several chargers to form a charging station. The charging stations can be
builtalong theroad.
4.3 Rural charging station location model
Therural areas havelowdensityofpopulation,which resultsinlowchargingneeds.
Therefore, we can ignore the waiting time. Ifthe mileage of one charge is larger thanthe
distance between two adjacent charging stations, the charging network can be regarded
to cover theentire ruralarea.
We take the location of charging station as the center and the mileage Y as the
radius of service circle. The square of the circle is the range that the electric vehicles can
reach after charging. To achieve full coverage, there must be another charging station in
thecircle. From theviewof geometric point,that is to maketwo circles intersect. After


## 第 14 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#73156 Page12of27
simplification,thefulltriangularmeshmodelcanbeusedtoachievefullcoverageinrural
areas.
Generally, the charging station is built at the side of the road. Hence, the triangle
structure will be destroyed. We assume that the three sides of the triangle formed by the
adjacent three chargers are a, b,crespectively. According theHelen formula:
S  p(pa)(pb)(pc)
We can calculate the area of the triangle. In addition, the economic costs are
considered. Hence, the onlygoal isto minimizethetotal cost.
min Z  r C
urban urban
  S  S
urban

1
s.tp  (abc)
 2
 ac,ab,bc0

4.4 Logistic model
4.4.1 Index definition
1) Electric vehicleprice(EVP)
The price of electric cars has a great impact on the sales of electric vehicles. The
decrease in the car prices will result in more people buying cars. Hence, we define the
electriccar price as theaverage price of all theelectric cars soldonthe current market.
2) Density of population(DP)
There willbe moreelectriccars in places with largepopulation density. According
to thepopulation density, we dividetheUS intothree parts: urban, suburban andrural.
3) Wealth distribution(WD)
Atpresent,electriccarsarenewproducts,andtheirpricesarerelativelyhigh.Hence,
there are more electric cars in rich places. We use the GDP value of a certain area to
represent thewealth oftheregion.
4) Environmental awareness (EA)
Electric vehicles are environmental-friendly products. With the increasing
awareness of environmental protection, the sales of electric vehicles will becomehigher.
Wedefinethe environmental awarenessas:
EA=the numberof peoplebuying electric cars / thenumber ofpeople buying cars
5) Policy orientation (PO)
Policy orientation can guide thepurchasing direction ofpeople toa certain extent.
Wedefinethe amount ofsubsidies ofbuying an electriccar as policy orientation.
6) Government investment(GI)
The improvement of supporting services and facilities will largely affect the
enthusiasm of consumers purchasing electric cars. So we use the amount of investment
in supporting facilities to measure thisindex.
4.4.2 The model construction
Logisticregression is ageneralized linear regression analysis model, which is
commonly used inthefields ofdata miningand economicforecasting. Therefore, itis


## 第 15 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#73156 Page13of27
suitableforthequestion.Weselectthesixindicatorsdefinedaboveasinfluencingfactors,
andestablish theLogisticregression model to dotheprediction
4.4.3 Model solution and analysis
We use SAS to test the model, and the test results are shown in the appendix. After
analysis, we find that only WD, PO and GI pass the test. Therefore, we get the logistic
regression equation for thesethree indicators.
For cities, theregression equation is
p
ln  0.2176 1.7258WD  0.2987  PO 1.3291 GI .
1 p
For rural areas, theregression equation is
p
ln  0.1082  0.9652 WD 1.6549  PO  0.3472  GI .
1 p
For thewhole country, theregression equation is
p
ln  0.1110 1.7137 WD 1.5000 PO 1.614 GI .
1 p
4.5 Answers of the Questions
(a) After calculation, the optimal number of charging stations in South Korea is
about 270,000. The distribution is mainly concentrated in the Seoul Metropolitan Area
andtheBusan MetropolitanArea.Theremainingareasarerelativelysparselydistributed.
Theirgeneral location is shown as following figure.
Figure5:DistributionofchargingstationsinSouthKorea
The model we constructed above aims to minimize the total cost and the average
waitingtime. Whilethecost ofthechargers will havea direct impact onthetotal cost. In
addition, the number of chargers affect the total cost and average waiting time as well.
The number of chargers is affected by the investment. In conclusion, the key factors that
shape the development of our plan are the building cost of chargers and government
investment.


## 第 16 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#73156 Page14of27
(b) Itis well known that the number of chargers and the number of electric vehicles
interact and influence each other. In order to facilitate the study, we define a lag index
which is.
The macroscopic parameterisdefined as lag cardinality.Therefore, for the
function f (x) ,thelag index at pointx is
x  y
 .

Figure6:Lagindex
Now we have an exponential function:(x)ax x 20 0.05
x
Let (y)(x x) axx,wecan get thelag indexat pointx as
y  x
  .
x 
Since
(y)
can beobtained from thetranslation of
(x)
,we regard thislag as
synchronouslag.It has been observed that for thephenomenon ofsynchronous lag,the
larger x is, thesmaller is. That is   x .
x x
Based on the growth forecast of supercharging stations [13], we obtain the sales
growth forecast curve
(x)
ofTesla whilemeeting the service conditions.The curveis
exponential. Then, we let 20 and obtain a new Tesla sales growth forecast curve
when0.05(after one year). However, we find that forthe curves of
(x)
and
(x)
,
therelationship of   x is notestablished. As theyear grows, therelationship is
x
established.
Figure7:Changeoflagindex
Wecanregardthesalesgrowthforecastcurveasanexponentialcurve.Ifthenumber
ofchargershasnoeffectonthesalesvolumeofTesla,theoverallconstructionofchargers
will bedelayed byoneyear. The newsales growth forecast curve should appear
synchronizedlagphenomenonandtherelationshipof  x should beestablished all
x
thetime. However, there is nosynchronous lag inthe actual forecast situation,and the
relationship of   x even appears. It shows that theconstruction lag makes thesales
x
of Tesla decline. And the evaporation situation of sales will increase as year grows, thus
showing a vicious cycle. Similarly, we use Tesla sales growth to predict the growth of
chargers. Then, we put a whole lag into the sales growth curve and analyze the relevant
index.
Accordingtotheconclusion obtained, theinvestment distributionof chargers is
shown as follows.


## 第 17 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#73156 Page15of27
Figure8:Investmentdistributionofchargers
The wholeprocess isdivided into three stages: early, middleand latestage.
In the early stage, we need to increase investment in the construction of chargers to
ensure that the early owners can get the most basic charging service. Therefore, the
number ofpeoplebuying electriccars will increase.
In the middle stage, since the early construction of the chargers is sufficient to deal
withthegrowthofelectricvehicles,wecanusepartoftheinvestmentforsubsidies.Thus,
it canstimulatethenew energy automotiveindustry.
In the late stage, the number of vehicles close to a stable condition. So, we need to
constantly improvethecharging facilities services.
Tosumup,thecountryshouldbuildallcity-basedchargersfirst.Throughthecurves
ofurban and rural areas, we canfind that thegrowth rateofTeslain urban areais always
greater than that oftherural area.
Intheinitialstageofconstruction,weshouldbuildchargingstationsfirsttopromote
the purchase of cars. In the later stage of construction, the charging stations are built to
cope withthepurchase ofcars. In conclusion, chargersshouldbebuiltfirst.
From the test result of Logistic model, we can filter out the key factors. Hence, the
key factors that affect our proposed charging station plan are wealth distribution and
governmentinvestment.
(c) From the Logistic model established above, we have drawn a trend graph of
marketshareofelectricvehiclesandthecorrespondingtimeline.Theresultisasfollows.
Figure9:Trendofmarketshareofelectricvehicles
From the table below, we can clearly see the corresponding years of each degree of
full electrification. It is notable that when the market share of electric vehicles reaches 90%,
it close to a stable condition. At this time, the government needs to intervene to impose a
moratoriumontheuseofoilandgas, whichwilleventuallyleadtorealfullelectrification.
Table2:Timelineoffullevolutiontoelectricvehicles
Degree 10% 20% 30% 40% 50% 60% 70% 80% 90%~100%
Year 2024 2027 2031 2033 2035 2037 2040 2043 2069
In 2016, Tesla entered South Korea officially. Besides, there are fewer subsidies to
buyelectricvehiclesinSouthKorea. It showsthatthepolicyorientationhasanimportant
influence on the electrification conversion. Therefore, the key factor that shapes our
proposedgrowth plantimelineispolicyorientation.


## 第 18 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#73156 Page16of27
5 Create a classification system
Since countries with different geography, population and wealth distributions have
differentoverallpatterns ofgrowth, thenetworkofchargers weproposedearlierdoes not
apply to every country. To help a country determine the overall growth model that it
should follow, we establish a Q-based clustering model for each country. Therefore, it
can deploy its coverageplan of charging station networkbetter.
5.1 The model construction
To classify different types of countries, it is necessary to describe the similarities
between different countries quantitatively. While a country contains many indicators,we
can treat each country as a point in space, where p is the number of indicators contained
in each country. In order to classify countries more accurately, we selected five different
indicators: population density (DP), gross domestic product (GDP), country area (CA),
government investment (GI), electric vehicle price (EVP). Next, we characterize the
similaritiesbetween two countries.
In cluster analysis, theMinkowski distanceis themost commonlyused method.
However,whenusingtheMin-styledistance,theinformationwilloverlapduetothe
correlation between national indicators. It will emphasize the correlation between some
indicators unilaterally. Therefore, we consider to employ Mahilanobis distance to
measure thesimilarity.
d(x,y)  (x  y)T (x y) .
Mahalanobis distance of all linear transformation is invariable, so it is not affected
by the dimension. Since we have a measure of the similarity between countries, we then
measure thesimilaritybetween classes.
Under thiscircumstance, theNearest Neighbor orSingle LinkageMethod isadopted.
D(G ,G )  min{d(x ,y )} .
1 2 xi G1,xj G2 i j
Wecan simplyassume thatthis is theshortest distance between thenearest two
pointsin thetwo classes.
5.2 Model solution and analysis
In order tomake ourclassification morerepresentative, we have chosen eight
countries indifferent parts oftheworld. Theinformation is shown as below.
Table3:Eightcountries
Index 1 2 3 4
Country Australia Indonesia UnitedStates Singapore
Index 5 6 7 8
Country Korea SaudiArabia China Uruguay
Using theclassificationsystem we set upabove, wecan draw thefollowing cluster
map.


## 第 19 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#73156 Page17of27
Figure10:Clusterdiagram
According to this classification system, we can divide these countries into three
categories.
The first category is the developed countries led by the United States. They have
investedheavilyintheconstructionofchargingstationsandwillsoonenterthesaturation
period ofgrowth. The key factor for theirgrowth in thesecountries isinvestment.
The second category is the developing countries led by China. Charging stations in
these countries are at an early stage of construction. In the next few years, under the
influenceofinvestment,theywillusherin an explosionofgrowth. Thekeyfactors ofthe
growth of network are the investment and public awareness of environmental
protection.
The third category is underdeveloped countries led by Indonesia. These countries
have not yet built their charging networks and will grow slowly under the influence of
policiesandinvestmentsinthefuture. Therefore, thekeyfactors fortheirgrowth inthese
countries are policies andinvestments.
6 Comment on the effect of new technologies
Super-cycle trains use solar energy for rapid transit between cities, and electric
vehicles can improve the quality of the environment. But only aiming at protecting the
environment does not mean that electric vehicles can be truly universal. In this regard,
we establish an evaluation model to investigate whether these technologies can promote
thepopularity ofelectric vehicles.
6.1 The model construction
To investigate whether the electric vehicles are popular, we need to know their
growth rate, which is related to the country's GDP, URP and OPH. The general law of
things shows that the development of electric vehicles will close to a stable condition,so
weusethelogisticcurvetopredicttheimpactofdifferenttechnologiesonthegrowthrate
r and to determine whether it can contribute to thepopularity ofelectricvehicles.
First of all, in order to eliminate the dimensional effect of the above three variables
and make each variable have equal expressive force, we standardize the data of GDP,
URPand OPHindicators. The formulais as follows.


## 第 20 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#73156 Page18of27
Therefore, we can get the expression of the growth rate of electric vehicles. In
addition, we can also infer whether these technologies have a catalytic role to promote
thepopularity ofelectric vehicles
6.2 Model analysis
The popularity of electric vehicles results from the construction of the fast-
changingpowerstation. Atpresent, electricvehicles useliquidlithiumbatteries, butthe
biggestproblemwithliquidlithiumbatteries istheirshortlife. Thisisalsothekeyreason
that prevents electric vehicles from becoming mainstream. If drivers charge the car
regularly or each charging time is too long, it will affect the mind position in the public
about electric car. Fortunately, various countries in the world are stepping up the
construction of fast-changing electric vehicles. In particular, Tesla has invested heavily
intheconstructionofchargingstations(includingsuper-chargingstationsanddestination
charging stations),which lays thefoundation forthepopularity of electricvehicles.
The development of autopilot technology has increased the ownership of
electricvehicles.Nowadays,Artificial Intelligence(AI) hasmadebreakthroughprogress
in areas such as machine learning and computer vision fields, thus making autopilot
technology possible. Because the cost of maintaining the electric vehicles is lower. The
prospect of autonomous driving technology is very broad. On the one hand, most of the
two types of people are facing mobility restrictions from the aging and the disabled
market,andthedevelopmentofthistechnologymakestheirfreepassagepossible.Onthe
other hand, traffic congestion in cities is a problem that every metropolitan area faces.
Autonomous driving on-board sensors can be used in conjunction with intelligent
transportationsystemstooptimizetrafficflowatintersections.Thegreenorred-lighttime
intervalisdynamic.Accordingtothechangesofreal-timetraffic,wealleviatecongestion
byincreasingtheefficiencyoftrafficflow.Thisprovidesapowerfuldrivingforce forthe
popularity ofelectricvehicles.
Thedevelopmentofsuper-ring trains andflyingcars will alsocontributeto the
popularity of electric vehicles. Super Loop trains are solar-powered electric vehicles
that can reach 1,223 kilometers per hour at speeds of 340 meters per second. It is
apparently faster than any other commercial train traveling on Earth, in terms of future
intercitytraffic. Revolutionarybreakthrough and its construction costs willbe lowerthan
the cost of the general high-speed rail construction, under the premise of ignoring the
impactoftheweathermoresecure. Thedemand ofpublicistransferred fromflight tothe
electric vehicles, which improves the ownership of electric vehicles and provides a
potential driverfor thepopularity of electricvehicles.
Therefore, webelievethat thepopularityofelectricvehicles will continuetorise. In
thenear future, theoverall popularity ofelectricvehicles willsurely berealized.
7 Sensitivity Analysis
The number of chargers in each charging station has a direct impact on the waiting
time of driver. From the model above, we can see that our solution is obtained under the
condition that each charging station has 8.8 chargers. In addition, the average waiting
time is also affected by the daily charging time and fully charging time. Since the
population distribution and economic conditions vary from country to country, the
average supplying, there is a slight difference between the daily power supply time and
thenumberofchargersperchargingstation.Totesttherobustnessofthemodelandmake
the model more applicable, we will change the parameters that affect the latency and
conduct sensitivityanalysis.


## 第 21 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#73156 Page19of27
We still take the United States as an example. From an intuitive point of view, we
can see that when the waiting time for charging is reduced, all-electric charging requires
less charging stations on the original basis. The government can save money to invest in
other fields. Next, we mainly consider the number of average chargers (NAV) and the
daily supply time (AST). Through the model established before, we calculate the results
under different values.
Table4:Sensitivityanalysis
NAV 8.6 8.7 8.8 8.9 9.0
NCS 1708680 1707530 1704500 1703750 1701980
AST 6 7 8 9 10
NSC 1968320 1839860 1704500 1639670 1542390
Here NSC is thenumberofcharging stations.
Through the table above, we find that the change of these factors does affect the
waiting time, thus affecting the number of charging stations required for the full scale.
This shows that ourmodel has good stabilityand strong adaptability.
8 Conclusions
8.1 Strengths
1) The site-selection model takes the idea of clustering. And it splits the whole
network into smallcells. Not onlyeffectivelysolvethedistributionproblems ofcharging
stations, and simplify the complexityofdistribution.
2) The site-selection model has improved the traditional model. The shortest sumof
the traditional shortest path location model will make the site concentrated in the central
area. In our model, we introduce the concept of congestion index. After multiple
calculations, the weight of each side is updated every time. In the end, the scattered
distributionis achieved. Theresults obtained isconvicing.
3) We use the custom indicator "lag index" to analyze the relationship between
variables. Thisidea is veryinnovative
4) Sensitivityanalysis shows that ourmodel isrobust andreliable.
8.2 Weaknesses
1) Therearesomerestrictionsontheuseofthemodel.Thus,thismodelisabitrough.
If we want toimprovethe model, weshouldconsider moreaspects.
2) Wedonottake thetransition timeinto account, which weakens theaccuracy.
8.3 Model extension
The model can be extended to many industries, such as the courier industry, the
medical industry, theretail industry.
Take the courier industry as an example, we can compare a courier point to a
chargingstation.Courierservicerangecorrespondstothemileageoftheelectriccarafter
charging, while the average delivery time corresponds to the average waiting time for
electric car charging. Moreover, the demand for expressing delivery is very different in
cities,suburbsandvillages.Therefore,itiscompletelypossibletousethechargingstation
model to distributethecourierpoints.


## 第 22 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#73156 Page20of27
9 A Handout to the Leaders
To reduce the use of fossil fuels and look for cleaner energy sources, we examine
the current status of electric vehicle ownership in most countries, as well as the
distributionand sizeofthecorresponding charging stations.
First of all, we analyze the present Tesla charging station network. Currently, the
United States has 4,200 charging stations at all,550 of which are super charging stations,
making it the world's most advanced charging station construction country. In order to
explore whether Tesla can be fully galvanized in the United States, we divide the United
States into cities, suburbs and rural areas according to the density of population. For
different regions, the charging station location planning mode are different. Inparticular,
we collect the location of all existing charging stations in the United States and the
blueprintforbuildingchargingstationsinthefuture. Basedonthesedata,wemapoutthe
connectivity network for charging stations in the United States, which shows that the
connectivity network has basically achieved the coverage of the whole country. Only a
small part of the countryside has not been covered. In fact, this is similar to most of the
developed countries in the world, such as Britain, Germany and France. For developed
countries, thekey factorwhich shouldbe considered isinvestment.
Secondly, we analyze the construction of the charging station network in more
developed countries such as Korea and China. There are currently 131 charging stations
in Korea, 22 of which are super charging stations. Similar to the United States, South
Korea also has obvious divisions of the urban, suburban and rural areas, in which cities
with densely populated areas are mainly located in coastal areas. Popular cities such as
Seoul, for example, has basically covered the network of charging stations, while some
ordinary cities have not yet built relevant infrastructure and only a handful of rural
residents have charging stations. The car ownership per capita and coverage of electric
vehicles in South Korea are all obviously lower than that in United States and other
developedcountries.Forthosecountriesthathavejustbeguntodevelopelectricvehicles,
the key factors should be considered are investment and environmental awareness. The
charging station should be built first. Because city is the core of a country and it has
occupied the majority of the population in these countries. Besides, when employing the
strategyofencirclingtheruralareasfromthecities,weshouldnotforgetthedevelopment
ofenvironmental protection.
Finally, we have analyzed how underdeveloped countries such as Uruguay and
Indonesia build a charging stations network. Due to economic, policy or other reasons,
these countries have not yet carried out the construction of related infrastructure, or
related construction is extremely small to ignore. It is wise to make a plan to transform
personal transport to all-electric vehicles. For those countries that have not developed
electric vehicles yet, we suggest that the government should focus on policy and
investment. On the one hand, they should encourage citizens to buy electric vehicles and
give them considerable subsidies to increase the recognition of electric vehicles among
citizens.


## 第 23 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#73156 Page21of27
10 Reference
[1] Gao Jianping. Electric vehicle charging station network planning and optimization
[D]. Shandong University,2012.
[2] Etezadi-amoli M, Choma K, Stefani J. Rapid-charge Electric-vehicle Stations[J].
IEEE Trans onPower Delivery, 2010,25(3):1883-1887.
[3] Zhou Hongchao, Li Haifeng. Study on Location Optimization Model of Electric
Vehicle Charging Station Based on Game Theory [J]. Science and Technology,
2011,11(02): 51-54.
[4] XuFan, YuGuoqin,Gu Linfeng. Electricvehiclechargingstationlayoutplanning[J]
East ChinaElectric Power, 2009,17(10): 1678-1682.
[5]AhmedYousufSaber,GaneshKumarVenayagamoorthy.Onemillionplug-inelectric
vehicles on the road by2015[C]. IEEE Conference on Intelligent Transportation
Systems, St.Louis, MO, USA, 2009.
[6] Hengsong Wang, Qi Huang. A novel approach for the layout of electric vehicle
charging station[A].IEEE Conferences, 2010.
[7] Holzman. An Association Between Air Pollution and Mortality in six US Cities[M].
New England J. Med.1993,173-175.
[8] Zhou Hongchao, Li Haifeng. Research on Location Optimization of Electric Vehicle
Charging Station Based on Game Theory[J]. Science and Industry, 2011,11 (2): 51-
54.
[9] Hakimi.Newdirection ineconomical practice[M].EdwardElgarPublishingLimited,
1997.
[10] http://www.qiwen.org/renkou/shijierenkou/7769.html
[11]http://auto.163.com/18/0125/07/D8VRECD1000884MM.html
[12] ZhaoYing.Poissondistributionanditsapplication[J].JournalofLiaoningJiaotong
University, 2009.
[13] http://supercharge.info


## 第 24 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#73156 Page22of27
11 Appendix
Table 5: Test results oftheurban
DeviationsandPearsonGoodness-of-FitStatistics
Principle Value Degreeoffreedom Value/degreeoffreedom Pr>Chi
Deviation 1.9697 35 1.1991 0.0024
Pearson 38.1268 35 1.0893 0.4278
Maximumlikelihoodestimation
Parameter Degreeoffreedom Estimation Error Chi-Wald Pr>Chi
Intercept 1 0.2176 0.5357 0.0414 0.0150
EVP 1 -1.2326 0.7627 4.3827 0.8290
DP 1 2.3297 0.6576 4.8723 0.9802
WD 1 1.7258 0.4294 5.1284 0.0300
EA 1 -0.9624 0.5876 3.8527 0.7248
PO 1 0.2987 0.8423 4.7426 0.0186
GI 1 1.3291 0.2343 3.2973 0.0236
Table 6: Test resultsof therural
DeviationsandPearsonGoodness-of-FitStatistics
Principle Value Degreeoffreedom Value/degreeoffreedom Pr>Chi
Deviation 1.1837 35 1.1837 0.0013
Pearson 43.1245 35 1.8537 0.3867
Maximumlikelihoodestimation
Parameter Degreeoffreedom Estimation Error Chi-Wald Pr>Chi
Intercept 1 0.1082 0.2635 0.4826 0.0150
EVP 1 -1.9238 0.4264 5.3742 0.9868
DP 1 2.1924 0.6336 7.2742 0.6967
WD 1 0.9652 0.2743 4.7358 0.0283
EA 1 1.2731 0.8443 6.8648 0.7242
PO 1 1.6549 0.9535 5.8368 0.0320
GI 1 0.3472 0.4537 3.9586 0.0153


## 第 25 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#73156 Page23of27
Main Program
%%Initializationenvironment end
clc %%MapoftheTeslachargingstationinthe
clear UnitedStates
closeall [m,n]=size(pdata);
rest=zeros(m,n);
landcolor=[0.980.970.97];
lakescolor=[0.710.840.92]; fori=1:m
%%Readandprocesstesladata rest(i,3)=str2num(pdata{i,2});%Will
data=importdata('WebData.txt'); itopeninthefuture
data=data{1,1};%initialdata if~isempty(strfind(pdata{i,1},
'charge'))
flag1='type":["'; rest(i,4)=1;%Isitaneffective
flag2='"],"open'; chargingstation
flag3='soon":"'; end
flag4= '","la'; if~isempty(strfind(pdata{i,1},'super'))
flag5='latitude":"'; rest(i,5)=1;%Isitasuper
flag6='","long'; chargingstation
flag7='ngitude":"'; end
index1=strfind(data,flag1); rest(i,1)=str2num(pdata{i,
index2=strfind(data,flag2); 3});%latitude
index3=strfind(data,flag3); rest(i,2)=str2num(pdata{i,
index4=strfind(data,flag4); 4});%longitude
index5=strfind(data,flag5); end
index6=strfind(data,flag6);
index7=strfind(data,flag7); limit=[2648-130-60];
res=[];
fori=1:length(index1) fori=1:m
pdata{i,1}= ifrest(i,1)>limit(1)&&rest(i,1)<
data(index1(i)+length(flag1):index2(i)- limit(2)&&rest(i,2)>limit(3)&&rest(i,2)
1);%location_type <limit(4)&&rest(i,4)==1
pdata{i,2}= res=[res;rest(i,:)];
data(index3(i)+length(flag3):index4(i)- end
1);%open_soon end
pdata{i,3}=
data(index5(i)+length(flag5):index6(i)- mcolor=[249222239;255860;236165
1);%latitude 201;4770150];
pdata{i,4}=data(index7(i)+ mcolor=mcolor./255;
length(flag7):index7(i)+
length(flag7)+10);%longitude fori=1:size(res,1)


## 第 26 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#73156 Page24of27
curpoint(i).Geometry='Point'; scolor});%repmat(landcolor,
nextpoint(i).Geometry='Point'; numel(states),1)
ifres(i,3)==0 geoshow(ax,states,'DisplayType',
curpoint(i).Lon=res(i, 2); 'polygon',...
curpoint(i).Lat = res(i, 1); 'SymbolSpec',faceColors)
curpoint(i).Name=''; rivers=shaperead('worldrivers',
end 'UseGeoCoords',true);
ifres(i,3)==1 geoshow(rivers,'Color','blue')
nextpoint(i).Lon= res(i,2); geoshow(nextpoint,
nextpoint(i).Lat = res(i, 1); 'MarkerEdgeColor','r','Marker','.',
nextpoint(i).Name=''; 'MarkerSize',10)
end geoshow(curpoint,'MarkerEdgeColor','r',
end 'Marker','.','MarkerSize',10)
set(gcf,'Position',[100,100,800,400])
figure %%ReadingthedataofSuperfillingpilesin
ax=worldmap('World'); theUnitedStates
ax=worldmap([25,55],[230,300]); [~,~,data]=
land=shaperead('landareas','UseGeoCoords', xlsread('SuperChargeData.xlsx');
true); count=1;
geoshow(ax,land,'FaceColor',landcolor) fori=1:size(data,1)
lakes=shaperead('worldlakes', ifmod(i,13)==8
'UseGeoCoords',true); sdata=data{i,1};
geoshow(lakes,'FaceColor',lakescolor) index=strfind(sdata,',');
states=shaperead('usastatelo','UseGeoCoords', superCharge(count,1)=
true); str2num(sdata(1:index-1));
scolor=[]; superCharge(count,2)=
fori=1:size(states,1) str2num(sdata(index+2:end));
ifstates(i).PopDens2000>=150 superCharge(count,3)=data{i-1,
scolor=[scolor;mcolor(4,:)]; 1};
elseifstates(i).PopDens2000>=50 SuperChargeStatus{count,1}=
scolor=[scolor;mcolor(3,:)]; data{i+2,1};
else count=count+1;
scolor=[scolor;mcolor(1,:)]; end
end end
end %%DrawingthedataofSuper-fillingpiles
index=find(scolor(:,1)>=1); intheUnitedStates
fori=1:size(index,1) count=1;
scolor(index(i),:)=[100]; superpoint=[];
end chargeline=[];
faceColors=makesymbolspec('Polygon',... fori=1:size(res,1)
{'INDEX',[1numel(states)], ifres(i,3)==1&&res(i,5)==1
'FaceColor',...


## 第 27 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#73156 Page25of27
superpoint(count).Geometry='Point'; dis=calDis(superpoint(i).Lon,
superpoint(count).Lon=res(i,2); superpoint(i).Lat,superpoint(j).Lon,
superpoint(count).Lat=res(i,1); superpoint(j).Lat);
superpoint(count).Name=''; ifdis<=170*1.6
count=count+1; chargeline(count).Geometry=
end 'Line';
end chargeline(count).Lon=
fori=1:size(superCharge,1) [superpoint(i).Lonsuperpoint(j).LonNaN];
superpoint(count).Geometry='Point'; chargeline(count).Lat=
superpoint(count).Lon=superCharge(i,2); [superpoint(i).Latsuperpoint(j).LatNaN];
superpoint(count).Lat=superCharge(i,1); count=count+1;
superpoint(count).Name=''; count1=count1+1;
count=count+1; end
end ifdis<=220*1.6
count2=count2+1;
figure end
ax=worldmap('World'); end
ax=worldmap([25,55],[230,300]); ifcount2~=0
land=shaperead('landareas','UseGeoCoords', superrate(i)=count1/count2;
true); end
geoshow(ax,land,'FaceColor',landcolor) end
lakes=shaperead('worldlakes',
'UseGeoCoords',true); geoshow(chargeline,'Color','red',
geoshow(lakes,'FaceColor',lakescolor) 'LineWidth',1)
states=shaperead('usastatelo','UseGeoCoords', geoshow(superpoint,'Marker',
true); 'o','MarkerEdgeColor','green','MarkerSize',
faceColors=makesymbolspec('Polygon',... 10, 'MarkerFaceColor','green',
{'INDEX',[1numel(states)], 'LineWidth',1.5)
'FaceColor',... superratem=mean(superrate);
repmat(landcolor,numel(states),1)}); set(gcf,'Position',[100,100,800,400])
geoshow(ax,states,'DisplayType','polygon',... %%MappingthetrendofSuperQuick
'SymbolSpec',faceColors) fillingpilesintheUnitedStates
rivers=shaperead('worldrivers', figure
'UseGeoCoords',true); datax=2013:0.5:2018;
geoshow(rivers,'Color','blue') datay=[7,10,63,126,308,417,556,639,
767,873,1135];
count=1; x=2013:0.01:2018;
fori=1:length(superpoint) y=interp1(datax,datay,x,'v5cubic');
count1=0; holdon
count2=0; xr=2013+rand(1,400)*5;
yr=interp1(datax,datay,xr,'v5cubic');
forj=1:length(superpoint) xp=2018:0.01:2019;


## 第 28 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#73156 Page26of27
poly=polyfit(datax,datay,4); count=count+1;
yp=polyval(poly,xp); end
end
plot(xp,yp,'LineWidth',2,'LineStyle','--
','color','g'); count=1;
plot(x,y,'r'); cityline=[];
set(gca,'YGrid','on') fori=1:size(uscities,2)
set(gcf,'Position',[100,100,600,300]) temp=randperm(size(uscities,2));
set(gca,'xtick',2013:1:2019) temp=temp(1:3);
xlabel('Years')
ylabel('OpenSupercharges') forj=1:size(temp)
legend('FutureSupercharges','Current cityline(count).Geometry='Line';
Supercharges') cityline(count).Lon=
scatter(datax,datay,10,'filled', [uscities(i).Lonuscities(temp).LonNaN];
'MarkerFaceColor','r'); cityline(count).Lat=
scatter(xr,yr,10,'filled','MarkerFaceColor', [uscities(i).Latuscities(temp).LatNaN];
'r'); count=count+1;
%%MappingurbantrafficintheUnitedStates end
figure end
ax=worldmap('World'); cityline(1).Name='';
ax=worldmap([25,55],[230,300]);
land=shaperead('landareas','UseGeoCoords', geoshow(cityline,'Color','red',
true); 'LineWidth',1.5)
geoshow(ax,land,'FaceColor',landcolor) geoshow(uscities,'Marker','o',
states=shaperead('usastatelo','UseGeoCoords', 'MarkerEdgeColor','black','MarkerSize',10,
true); 'LineWidth',1.5,'MarkerFaceColor','red')
faceColors=makesymbolspec('Polygon',... set(gcf,'Position',[100,100,800,400])
{'INDEX',[1numel(states)], %%DrawingthepercentagechartofTeslain
'FaceColor',... theUnitedStates
repmat(landcolor,numel(states),1)}); endyear=2050;
geoshow(ax,states,'DisplayType','polygon',... x=2013:2017;
'SymbolSpec', faceColors) x=[x2017:0.01:endyear];
cities = shaperead('worldcities', y1=[17.129345587];
'UseGeoCoords',true); y2=[10.313.415.719.426.7];
poly1=polyfit(x(1:5),y1,6);
count=1; poly2=polyfit(x(1:5),y2,6);
fori=1:size(cities) yp1=polyval(poly1,x(6:end));
lat=cities(i).Lat; yp2=polyval(poly2,x(6:end));
lon=cities(i).Lon; y1=[y1yp1];
iflat>limit(1)&&lat<limit(2)&&lon> y2=[y2yp2];
limit(3)&&lon<limit(4) index=find(x>=2020);
uscities(count)=cities(i); fori=index(1):length(x)


## 第 29 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#73156 Page27of27
len=abs(x(i)-x(index(1))); loadindex1
y2(i)=y2(i)-len*len*1.6; loadindex2
y1(i)=y1(i)+len*len*1400; loadindexdouble
end color1=[94141193]./255;
t=[]; color2=[201221241]./255;
fori=index(1):length(x) ax=worldmap('World');
t(i)=2020+6*(x(i)-2020); ax=worldmap([25,55],[230,300]);
end
x(index(1):i)=t(index(1):i); land=shaperead('landareas',
index=find(x>=2053); 'UseGeoCoords',true);
[hAx,hLine1,hLine2]=plotyy(x(1:index(1)), geoshow(ax,land,'FaceColor',landcolor)
y1(1:index(1)),x(1:index(1)),y2(1:index(1))); states=shaperead('usastatelo',
hLine1.LineWidth=2; 'UseGeoCoords',true);
hLine2.LineWidth=2;
holdon fori=1:length(index22)
scolor(index22(i),:)=color2;
legend('U.S.teslaholdings','Teslamarket end
share') fori=1:length(index11)
set(gcf,'Position',[100,100,700,300]) scolor(index11(i),:)=color1;
set(gca,'YGrid','on') end
ylabel(hAx(1),'TenThousand')%lefty-axis faceColors=makesymbolspec('Polygon',...
ylabel(hAx(2),'percentage')%righty-axis {'INDEX',[1numel(states)],
'FaceColor',...
ylb=get(hAx(2),'YTickLabel'); scolor});
fori=1:size(ylb,1) geoshow(ax,states,'DisplayType',
ylb{i,1}=strcat(ylb{i,1},'%'); 'polygon',...
end 'SymbolSpec', faceColors)
set(hAx(2),'YTickLabel',ylb) cities = shaperead('worldcities',
set(gca,'xtick',2013:10:2053) 'UseGeoCoords',true);
%%Mappingtheconvenienceofthemajor set(gcf,'Position',[100,100,800,400])
states
figure
Logisticmodel
dataa;
inputx1-x7y@@;
cards;
...
;
proclogisticdescendingorder=data;
modely=x1-x7/scale=noneaggregate;
run;

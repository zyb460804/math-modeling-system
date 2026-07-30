# D82794-How to achieve the full adoption of all-electric vehicles


## 第 1 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
TeamControl Number
For office use only For office use only
82794
T1 F1
T2 F2
T3 Problem Chosen F3
T4 F4
D
2018 Mathematical Contest in Modeling (MCM/ICM) Summary Sheet
How to achieve the full adoption of all-electric vehicles
Summary
WeconstructtwomodelstofacilitatetheconstructionoftheTeslanetworkfromamacro
perspective,adouble-layercomplexnetworktomeasurethenetworktopologyandaSI epi-
demic model based on the evaluation index system(SI-EI)to identify the key factors in the
buildingprocess.
The double-layer complex network can be used to determine the number,location and
distribution of chargeing stations. People are divided into long-distance and short-distance
travelers. The number of charging stations are determined mainly by VehicleDensity,Daily
MileageandRangeAnxiety: (1)theouterlayeristostudythedemandsoflong-distancetrav-
elersforsuperchargestations,withintroducedWeightedBetweennesstomeasurewhethera
cityisatraffichub,whichisthereferencetoarrangethelocation;(2)theinnerlayeristostudy
the demands of the remaining three cases, and arrange location according to VehicleDensi-
ty.The distribution is based on thenumber of the abovefour cases. Weintroduce Reachable
Level,PermeabilityandLong-distancetraveldemandrateintoSI-EImodeltomeasuredaily
infectionrateλ,andapplythetraditionalSImodeltodeterminethekeyfactors.
Forproblem1,thereare8.08milliondestinationchargingstationsand2.16millionsuper-
chargestations inthefinalnetworkarchitecture. Ittakes108years toreachfullyautomobile
electrificationforconstructednetworkswhileittakes36yearstoconstructnetworks.
For problem 2, we choose Ireland. There are 78 thousand destination charging stations
and20.8thousandsuperchargestationsinthefinalnetworkarchitecture. Theoptimalinvest-
ment plan is to establish a 2: 1 ratio between the scale of the site and the present required
scale, andtoestablish chargingstationsby mixingtheratioof thecitytotherural area to3:
2. Theconclusion is mainly buildingdestination chargingstations when Permeability is less
than30%,andbuildingsuperchargestationsincitieswhenPermeabilityislessthan50%but
morethan30%,otherwisebuildingsuperchargestationsinroads.
Forproblem3,webuildaclassificationsystemtohaveaweaktrafficnetwork.
Forproblem4,technologythatwouldhinderEVs’spreadinclude:car-share,ride-share
servicesandhyperloop.WhiletechnologythatwouldboostEVs’spreadinclude:self-driving
cars,rapidbattery-swapstationsforelectriccars,andflyingcars


## 第 2 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Contents
1 Overview 1
1.1 Background..............................................................................................................................1
1.2 RestatementofProblem.........................................................................................................1
1.3 Illustration................................................................................................................................2
2 Notations 2
3 AssumptionsandJustification 2
4 Double-LayerComplexNetwork 3
4.1 ModelOverviewandAnalysis.............................................................................................3
4.2 InnerLayer:DistributionofChargingStationsoveraCounty........................................4
4.2.1 DistributionofDestinationChargingStationsoveraCounty.............................4
4.2.2 DistributionofSuperchargingStationsoveraCounty.........................................5
4.3 OuterLayer:DistributionofChargingStationsfromCountytoCounty.......................7
5 SIepidemicmodelbasedontheevaluationindexsystem 9
5.1 ModelOverviewandAnalysis.............................................................................................9
5.2 EstablishmentofEvaluationIndexSystem.........................................................................9
5.2.1 AnalysisofUser’sDemands.....................................................................................9
5.2.2 TheMeasureofIndex..............................................................................................10
5.3 SIEpidemicModel................................................................................................................11
6 ApplicationandAnalysis 12
6.1 Task1:ExplorethenetworkofTeslachargingstationsintheUnitedStates.................12
6.1.1 Thenumberanddistributionofchargingstations..............................................12
6.1.2 Prediction..................................................................................................................13
6.2 Task2:AnalysisthenetworkofTeslabuiltinIreland.....................................................14
6.2.1 2a:Thenumber,placementanddistributionofchargingstationsandkey
factors.........................................................................................................................14
6.2.2 2b:Ourproposedchargingstationplan...............................................................16


## 第 3 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
6.2.3 2c:Ourproposedgrowth plantimeline................................................................17
6.2.4 Analysisofkeyfactors.............................................................................................17
6.3 Task3:Aweaktrafficnetwork classificationsystem......................................................18
6.4 Task4:Theimpactoftechnologyon EVs’spread............................................................19
7 SensitivityAnalysis 19
8 CommentonHeavyTrucks 20
9 AnalysisoftheModel 20
9.1 Strengths.................................................................................................................................20
9.2 Weaknesses.............................................................................................................................20
10 Task5: Handout 21
Appendices 23


## 第 4 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#82794 Page1of24
1 Overview
1.1 Background
Theworldisfascinatedbyreducingtheuseoffossilfuels,includinggasolineforvehicles.
Whethermotivatedbytheenvironmentorbytheeconomics,consumersarestartingtomigrate
to electric vehicles. The migration from gasoline and diesel vehicles to electric vehicles is not
simpleandcan’thappenovernight.Thelocationandconvenienceofchargingstationsiscritical
as early adopters and eventually mainstream consumers volunteer to switch. When nations
planthistransition,theyneedtodo:
• Buildasufficientnumberofvehiclechargingstationsinalltherightplaces;
• Considerthefinalnetworkofchargingstations
• Considerthegrowthandevolutionofthenetworkofchargingstationsovertime.
Asnations seekto developpolicies thatpromotethemigrationtowards electric vehicles,
theywillneedtodesignaplanthatworksbestfortheirindividualcountry.
1.2 Restatement ofProblem
Weneed to determine the final architecture of the charging network to support the full
adoption of all-electric vehicles. And we will identify the key factors that will be important
as they plan their timeline for an eventual ban or dramatic reduction of gasoline and diesel
vehicles.
Ourspecifictasksarethefollowing:
• ExplorethecurrentandgrowingnetworkofTeslachargingstationsintheUnitedStates.
• Selectoneofthefollowingnations(SouthKorea,Ireland,orUruguay). Buildthenetwork
consideringthenumberanddistributionofchargingstations,determinethegrowthplan
and propose the timeline for the full evolution to electric vehicles in this country. And
identifythekeyfactors.
• Identifythekey factors thattrigger theselection of different approachesto growing the
network in different countries. Discuss the feasibility of creating a classification system
thatwouldhelpanationdeterminethegeneralgrowthmodel.
• Commentonhowothertransportationoptionsmightimpactouranalysesoftheincreas-
inguseofelectricvehicleswiththedevelopmentoftechnology.
• Prepareaone-pagehandoutwrittenfortheleadersofawiderangeofcountrieswhoare
attendinganinternationalenergysummit.


## 第 5 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#82794 Page2of24
1.3 Illustration
• Twotypesofchargingstations
Teslacurrentlyofferstwotypesofchargingstations:(1)destinationchargingand(2)su-
percharging. Supercharging stations are usually built along the main road. Supercharg-
ingcanquicklychargethevehiclewhilepeopletakeaquickbreak. Destinationcharging
stationsarebuiltatplaces,includingnearbycompany,shoppingcenterandparkinglots.
• Distributionofchargingstations
Themeaningofthedistributionofchargingstationsisthedifferencesinthedistribution
of rural areas, suburban areas, and urban areas. The differences include the number of
chargingstations,distributionoftwotypesofchargingstationsandsoon.
• Explanationsforcounty
Therearetwoexplanationsforcounty[6],oneisthatthecountyiscomposedofcity[7]and
countryside,theotheristhatthecountyiscomposedofurban,suburbanandruralareas.
• Achargingstationcontainsonlyonecharger
Becauseourmodelcalculatesthenumberofchargersneeded,whilethenumberofcharg-
ingstationsdepends on howmanychargers asitecontains. Thespecificnumberof dis-
tribution involves the use of power networks and land resources, which we won’t take
intoaccountstoomuchabout.
2 Notations
Herewelistthesymbolsandnotationsusedinthispaper,asshowninTable1.Someof
themwillbedefinedlaterinthefollowingsections.
Table1: Notations
Symbol Description
λ Thedailycontactrate
i Thecurrentnumber ofEVs
M ThetotalnumberoftraditionalvehiclesandEVs
sum
D Thetotalsatisfaction
3 Assumptions and Justification
• Focusonlyonpersonalpassengervehicles.


## 第 6 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#82794 Page3of24
• acompleteswitchtoall-electrichappens,thesystemisstableandneitherwillpeople
converttogasolinevehicleusersnorwillpeopleconverttoEVusers.
• Achargingstationcontainsonlyonecharger
4 Double-Layer Complex Network
4.1 ModelOverviewandAnalysis
Sincewearebuildinganetworkofchargingstationsforacountry,weshouldstandonthe
nation’spointtoconsiderthisproblem. Therearemanydifferencesbetweenthecountiesin
acountry,includingtopography,folkcustomsandsoon.Existingpapers[1−3]didresearch
onspecificcity,includingthenumberofchargingstationsperstreetandsoon.Suchmethod
ofresearchdoesnotapplytothisproblem. Weshouldgrasptheessenceoftheproblemand
abstracttheproblem,sowecomeupwithadouble-layeredcomplexnetwork,whichmeans
theglobalnetworkofchargingstationsandthenetworkofchargingstation’sdistribution.
TaketheUnitedStatesforexample,thestructureofourdouble-layercomplexnetworkis
showninFigure1:
Figure1:Adouble-layerNetwork
Wehave already discussed in the Illustration of the general location of the two charging
stations in thecity.This article does notintendtodiscuss thespecificlocation of thecharging
stationfromamicroscopicpointofview,buttodiscussthelocationfromamacroperspective
wherethelocationisunderstoodasthenumberofchargingstationsallocatedindifferentcities.


## 第 7 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#82794 Page4of24
4.2 Inner Layer:Distribution of ChargingStations over a County
Thedesignoftheinnerlayerismainlyforthepeoplewhosescopeofactivityisinacounty.
Theyarecharacterizedbyanarrowrangeofactivities,lesspowerconsumptionperday,soit’s
reasonabletobuilddestinationchargingstationsprimarily.
However,thereare still twokinds of people need superchargingstations. Oneis thatthe
peoplewhosescopeofactivityisinacounty,butalwaysforgetscharginghisvehicle. Theother
arethelong-distancetravelerswhopassthecounty.
Figure2isthesummaryofthetextbelow.
Figure2:Thestructureofthissubsubsection
4.2.1 DistributionofDestinationChargingStationsoveraCounty
1. Thenumberofdestinationchargingstations:
Wequantifythenumberofdestinationchargingstationsbyintroducingthetotalloadof
chargingformula[4]:
L(S i ,t,τ) = f(S i ,τ)×ϕ(S i)×N sum ×µ((P,t,τ)| Si ),i = 1,2,...,6 (1)
h∫l(Si)
ϕ(S i) = g(D i)dD i ,i= 1,2,...,6 (2)
ll(Si)
Σ
TL(t, τ ) = (L(S
i
, t,τ)) (3)
Si ttτ
∈
where


## 第 8 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#82794 Page5of24
• S istheithusergroup,andthesixusergroupsaredividedaccordingtothediffer-
i
enceofdailymileageofelectricvehicles(EVs).
• L(S i ,t, τ ) isthetotalnumber ofdestinationchargingstationsS i need intimetof
workdayτ.
• f(S
i
,τ)istheprobabilitydistributionoftheusersinusergroupS
i
inworkdaysand
isequaltotheratioofcharginguserstototalusersofusergroupS duringworkday
i
τ.
• N istheholdingnumberofEVsinourresearchingarea.
sum
• µ((P,t,τ) | si ) istheexpectedvalueforasingleuserinuserclassS i chargedduring
workdayτattimet.
• ϕ(S i) istheratioofthenumberofusersinusergroupS i toN sum .
• g(D i) istheprobabilitydensityfunctionthatdailydrivingdistanceofasingleuser
inusergroupS obeys.
i
• tt isthesetofusergroupthathavechargedduringtheworkdayτ.
τ
• TL(t, τ ) isthe totalnumber ofdestinationchargingstationsneededintime tof
workdayτ.
Σ
ThereisnodoubtthatweshoulduseDTL = max{ TL(t,τ)}astherequirednumber
ofdestinationchargingstations.
2. Thelocationofdestinationchargingstations:
Thenumberofdestinationchargingstationsassignedtoeachcountyisproportionalto
thevehicledensityinthecounty.
DTL×CD
i
DTL i = ΣCD (4)
i
where DTL is thenumber of chargingstations requiredfor theith city,DTL is thenum-
i
ber of charging stations required for the whole country, CD is the traffic density of the
i
ithcity.
3. Distributionbetweenurban,suburban,andruralareas:
Ourresearchonquantityandlocationisbasedonvehicledensity,andthemaindifference
betweenurban,suburban,andruralareasisvehicledensityaswell,soitisreasonableto
allocatethenumberofdestinationchargingstationsbasedonthevehicledensityratio.
4.2.2 DistributionofSuperchargingStationsoveraCounty
Forshort-distancetravelingpeoplewhoalwaysforgetcharging


## 第 9 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#82794 Page6of24
1. Thenumberofsuperchargingstations:
Suppose thatpeople with rate a always forget chargingat home, then they need super-
chargingstations.Rangeanxietyisdefinedasdrivers’concernswithbeingstrandedwith
adischargedEVbatteryandtheassociateddelaystotheirjourneysduetolongrecharg-
ingtimes[5]. Consideringthattherangeanxietyofdestinationchargingstationsshould
larger than that of fast-charge, so we introduce a Damage Factor rd, its meaning is the
maximumremainingcapacitywhenpeoplewanttousethesuperchargingstationsrela-
tive to that when they want to use the destination charging stations and the number of
superchargingstations.weneedcanberepresentedas:
STL = DTL ×a×rd (5)
2. Thelocationofsuperchargingstations:
It’s similar to the location of destination charging stations, so we will not repeat them
here.
3. Distributionbetweenurban,suburban,andruralareas:
It’ssimilartothedistributionofdestinationchargingstationsbetweenurban,suburban,
andruralareas,sowewillnotrepeatthemhere.
Forlong-distancetravelingpeople
Sincelong-distancetravelerstendtorestatthecenterofthecountiesalongtheway,itcan
bepredictedthatimportantcitiesshouldhavealargedemandforsuperchargingstations.Thus
weneedtosetupthestationsinsuchimportantcitiestofitthedemands.
TheimportanceofcitiescanbemeasuredbyBetweenness.
where, n jl(i) is the number of the shortest paths between v
j
and v
l
which also passes v
i
,
n isthenumberoftheshortestpathsbetweenv andv.
jl j l
Giventhatthenetworkwehaveconstructedisaweightedgraph,theattributeofanodeis
itsnumberofvehicles,andtheattributeofanedgeisthedistancebetweentwoadjacentcities.
NowweintroducetwocoefficientstoconstructWeightedBetweenness.Thus,wegetourfinal
WeightedBetweennessWB tomeasuretheimportanceofcities.
WB i= B i × η 1 ×η 2 (7)
whereη istheratioofthesumofthepopulationofthecitiesconnectedtothecitytothetotal
1
population, η is the ratio of the sum of the length of the edge between the city and all of its
2


## 第 10 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#82794 Page7of24
surroundingcitiestothetotallengthoftheedge.
1. Thenumberofsuperchargingstations:
Letusestimatethenumberofsuperchargingstationsneededforlong-distancetravelers.
Weassumethatlong-distancetravelerschargemainlyduringthetwelvehoursdaytime,
charging thirty minutes each time and traveling an average of L miles per day. ρ is a
factor used to preventtherush hourfrom being in short supply.TheRange Anxiety,E ,
r
is set at 130 miles, which means that travelers are expected to charge when they spend
130miles.
w×N ×L×ρ
sum
STL = (8)
24E
R
2. Thelocationofsuperchargingstations:
Thenwedividesuperchargingstationsintotwotypes,onearoundthecityandtheother
on the road between the two counties. Weshould try our best to put the supercharging
stationsinthecity,whichnotonlymeets therequirementsoflong-distancetravelersbut
also reduces the construction cost. Here we mainly consider the supercharging stations
around the city,and we will continue to discuss the supercharging station on the road
betweenthetwocountieslater.Wesettheratioofthesuperchargingstationsontheroad
totheoverallsuperchargingstationsasβ.
WB
i
STL ci = Σ
WB
×STL ×(1−β) (9)
i
3. Distributionbetweenurban,suburban,andruralareas:
Wehavediscussedabovethatthesuperchargingstationhereisbuiltintheurbanarea,as
forthesuperchargingstationsbuiltinthesuburbanandruralareas,theywillbediscussed
intheouternetwork.
4.3 Outer Layer: Distribution ofCharging Stations fromCounty to County
Themaintargetofthechargersbetweencountiesisthosewhotravellongdistances,whose
EV may out of battery before they arrive at their destinations. Thus they need the charging
stations. Howevertheywishtheycouldarriveinacertaintime,socomparedwithdestination
chargingstations,theyneedsuperchargingstationsmore.Fromthisweknow,stationsbetween
countiesshouldbesuperchargingstations.
Therearethree typesofroutesin theouterlayer,asisshowninFigure4:
• Thedirectroutebetweencitiesinthesamecounty.
• Thedirectroutebetweencitiesinneighboringcounties.


## 第 11 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#82794 Page8of24
Figure3:thenumberofchargingstations
• Theroutebetweencitiesthataren’tinadjacentcountiespassesthroughthebigcitieswho
locatedbetweenthesecities.
Itisworthmentioningthatdifferentcountrieshavedifferentstandardsfortheclassifica-
tionofcities.Wewillstudythenumberandlocationofsuperchargingstationsasfollows.
Figure4:theouter-layerNetwork
1. Thenumberofsuperchargingstations:
Thenetworkoftheouterlayerisacompletegraph.Wetestalltheedgesinthecomplete
graph. Thecalculation of the numberof supercharging stations between twocities is as
follows:
, ,
L N i + N j
K ij = × ×K sum ×β (10)
E R N sum
where,Listhedistancebetweentwocities;E
R
isRangeAnxiety;N i(i= 1,2,...) isthe


## 第 12 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#82794 Page9of24
number of EVs in the ith city; N is the number of EVs in all cities; K is the number
sum ij
of supercharging stations between the ith city and the jth city; K is the number of
sum
superchargingstationsinallcities;βisthescalefactor.
2. Thelocationofsuperchargingstations:
According to the experience of life, people will choose the shortest path to reach their
destination. And based on the interpretation and analysis of E , supercharging station
R
should be placed on the shortest path between the two cities and the distance to the
nearestsuperchargingstationis130miles.
5 SI epidemic model based on the evaluation index system
5.1 ModelOverviewandAnalysis
Inlife,peopledecidewhethertousetraditionalvehiclesorelectricvehiclesbasedontheir
satisfaction with electric vehicles which is mainly measured by the number and location of
chargingstations. Thusweestablishedaevaluationindexsystemtomeasurepeople’ssatisfac-
tion.
When a person is very satisfied with electric vehicles, he will tell his friends and family
aroundtheadvantagesofelectricvehicles,sothatpeoplearoundhimhaveacertainprobability
ofbeingconvincedbyhim,thatis,turningtotheuseofelectricvehicles.Accordingtotheabove
analysis,wehaveestablishedaSIepidemicmodelbasedontheevaluationindexsystem.
5.2 Establishment ofEvaluation IndexSystem
Beforeestablishingevaluationindexsystem,weneedtoanalysepeople’sspecificdemand-
s. Inthefollowing,wefirstclassifypeopleaccordingtothelengthoftheirjourneyandanalyse
thedemandsofdifferenttypesofpeople.Thenestablishtheevaluationindexsystemaccording
topeople’sdemands.
5.2.1 AnalysisofUser’sDemands
Basedonpeople’spreferences,peoplearedividedintotwotypes:thosewhopreferlong-
distancetravel(LT)andthosewhoprefershortexcursions(SE).
• Long trips often cross several counties and will definitely need supercharging station
during the travel, so it’s more important for LTthat the number and location of super-
chargingstationalongtheway.
• SE’sbasicnecessitiesoflifearemostlyintheirowncounty.SEisdividedintopeoplewho
won’tforgettocharge(NFC)andwhowillforgettocharge(FC).NFC’sdailylifedoesnot


## 第 13 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#82794 Page10of24
requiresuperchargingstation,theyonlyneedasufficientnumberofdestinationcharging
stations to meet the daily charging demands. FC may require superchargingstations in
thecityincaseforgottentochargeEVs intime,sothenumberofsuperchargingstations
inthecityismoreimportanttoFCsthanNFCs.
According to the analysis above, the metrics in evaluation index system should include: the
numberofdestinationchargingstations;thenumberofsuperchargingstationsinthecity;the
number of supercharging stations in the road; the location of supercharging stations in the
road.
Figure5:themetricsinevaluationindexsystem
5.2.2 TheMeasureofIndex
Themeasureofthelevelofsatisfactionwiththenumberofdestinationchargingstations
isthefollowing:
DTL
now
DNL = (11)
DTL × PT
where DNL is the satisfaction level with the number of destination charging stations, DTL
now
is the number of destination charging stations now, DTL is the total number of destination
charging stations when every gas vehicle has been replaced by an electric one and every gas
stationhasbeenreplacedwithachargingstation,PTisthepermeability.
Tomeasurethelevelofsatisfactionwiththenumberofsuperchargingstations,wehave
proposedthefollowingformula:
STL
SNL = c_now (12)
STL ×PT
c
where, SNL is the satisfaction level with the number of destination charging stations in city,
STL is the number of supercharging stations in city now, STL is the total number of
c_now c
destinationchargingstationswheneverygasvehiclehasbeenreplacedbyanelectriconeand
everygasstationhasbeenreplacedwithachargingstationincity,also,PT isthepermeability.


## 第 14 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#82794 Page11of24
PermeabilityisthecurrentproportionofEVstoallvehicleswhichcanbecalculatedas
follows:
i
PT = (13)
M
sum
where,iisthecurrentnumberofEVswhileM isthetotalnumberoftraditionalvehicles
sum
andEVs.
Satisfaction level with thelocation of asupercharging station on a longroad is indicated
by RL, which means reachable level, that is the reachable probability of multiple counties to
county B from county A route. If County A and County B are far apart and there are not
enoughsuperchargingstationsontheroadforcharging,theyarenotreachable,otherwisethey
arereachable.
Overallsatisfactioncanbemeasuredasfollows:
STL DTL
c_now now
D = w × PC + (1 − w) × (a × + ) (14)
STL ×PT DTL ×PT
c
Where,Disthetotalsatisfaction,wisthepercentageofthenumberofLT,aistheratioofthe
numberofFCtoSE,RListheReachableLevel.
5.3 SI EpidemicModel
In the SI epidemic model, people who use EVs are equivalent to those patients in the SI
model. People who use traditional vehicles are equivalent to healthy people in the SI model,
and those who are healthy will use EVs because of the encouragement of the people around
them,thatis,theywillbecomepatients.
AsisshowninFigure6,thedots whosecoloristhedeepest representpatientswhilethe
dotswhosecoloristhelightestrepresenthealthypeople.Thedepthofthedots’coloronbehalf
ofpeople’ssatisfactiontoEVs.TheratioofthenumberofLTtothatofoverallwandtheratio
Figure6:NetworkofSISEpidemicModel


## 第 15 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#82794 Page12of24
ofthenumberofCSEtothatofSEacanbecalculatedas:
w = PT ×x (15)
a = PT ×y (16)
wherePT isthepermeability,xisthenumberofLTtoallwheneverygasvehiclereplacedby
an electriconeandeverygas stationreplacedwithachargingstation,yis thenumberofCSE
tothatofSEwheneverygasvehiclereplacedbyanelectriconeandeverygasstationreplaced
withachargingstation.Thenputformula(15)andformula(16)into(14).
Inthisepidemicmodel,λisthenumberofpeoplewhoownvehiclesthatmakeefficient
useofEVs(enoughtoconvertpeoplefromatraditionalvehicleusertoanEVuser)everyday,
whichcanbereferredtoasthedailycontactrate.Theparameterλcanbecalculatedas:
(D − X)P
λ = (17)
D
whereXisathresholdvalue.WhenthetotalsatisfactionlevelD=X,peopleareneutral
aboutEVsandtraditionalvehicles;WhenD > X, peopletendtochooseEVs;WhenD < X,
peopletendtochooseatraditionalvehicle.Pisthetotalnumberofpeoplewithvehiclesthat
comeincontactwitheachpersonwhousestheEVseveryday.
di
=λi(1−i),i(0)=i (18)
dt 0
whereiisthecurrentnumberofEVs,λisthedailycontactrate,i istheinitialvalueof
0
EVs.
6 Application and Analysis
6.1 Task1:Explore the network ofTeslacharging stationsinthe UnitedStates
6.1.1 Thenumberanddistributionofchargingstations
1. Destinationchargingstations
• Thenumberofdestinationchargingstations
WeconsultedforinformationandlearnedthecurrenttotalpopulationoftheUnited
States is 323.1 million, the per capita consumption of vehicle is 0.766 and the daily
mileage expectation is 43.4. Weregard these data as the value of parameters in the
formula1,andgettheanswerDTL =8.08million.
• Thedistributionofdestinationchargingstations


## 第 16 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#82794 Page13of24
Based on the model name, the distribution of destination charging stations is the
same as the radio of urban, suburban, and rural areas. The result is as shown in
Table3.
2. Superchargingstations
• ThenumberofsuperchargingstationsThenumberofsuperchargingstationsis
showninTable2.
Table2:thenumberofchargingstations
type number(million)
destinationchargingstations 8.08
long-distancetravelingpeople 1.62
superchargingstations
short-distancetravelingpeople 0.54
• Thedistributionofsuperchargingstations
Accordingtotheformula9,whenß=0.3,wegetthedistributionasfollows:
Figure7:thecomparisonofdistributionbetweendestinationchargingstationsandsupercharg-
ingstations
Table3:thedistributionofsuperchargingstations
areas urbanareas suburbanareas ruralareas
destinationchargingstations 0.8 0.15 0.05
superchargingstations 0.725 0.1125 0.1625
6.1.2 Prediction
Wecanassumethatwhenacompleteswitchtoall-electrichappens,thesystemisstable
andneitherwillpeopleconverttogasolinevehicleusersnorwillpeopleconverttoEVusers.
AssumingthatthelevelofsatisfactionDisthethresholdatthistime,thisassumptionis
reasonablebecausevehiclecompanieswillsurelypursuetheirownmaximumprofitsunder


## 第 17 页

Team#82794 Page14of24
thepremiseofmaintainingsystemstabilitywhichwillkeepthesatisfactionatthelowestlevel
ofsatisfaction.
1
(36,1) (108,1)
thegrowingnetworkofTesla
thecurrentnetworkofTesla
0.8
0.6
0.4
0.2
0
0 50 100 150 200 250 300 350
t
Figure8:thecomparisonofthegrowingnetworkandthecurrentnetworkofTesla
Weset w = 0.7, a = 0.3, PT = 0.002, resulting in a threshold of 1.85. It can be seen
from the Figure 8 that under the premise of ensuring that each future state is the same as
today,thecurrentTeslanetworkcanmeettherequirementsofanall-electricvehiclebutrequires
36.ComparedwiththegrowingTeslanetwork,themainchangeistheadditionof496super-
chargingstations,whichcanreducetherealizationtimeto108.
6.2 Task2:Analysis the network ofTeslabuilt in Ireland
6.2.1 2a:Thenumber,placementanddistributionofchargingstationsandkeyfactors
Thedeterminationof thenumberanddistribution of chargingstations is consistent with
task1,andweapplythecollecteddataaboutIrelandtogettheresult:
Table4:thedistributionofdestinationchargingstations
areas urbanareas suburbanareas ruralareas
destinationchargingstations 0.7 0.2 0.1
superchargingstations 0.7 0.125 0.175
Table5:thenumberofchargingstations
type number(thousand)
destinationchargingstations 78.0
long-distancetravelingpeople 15.6
superchargingstations
short-distancetravelingpeople 5.2
Wewillfocusondeterminingthelocationbelow.
i
精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！


## 第 18 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#82794 Page15of24
Inordertosimplifytheproblem,wehaveselected27bigcitiesinIreland,withatotal
populationof80%ofthetotalpopulationofthecountry.
1. Thelocationofdestinationchargingstations
Applytheratioofvehiclepossessiontoequation4togetthenumberofdistributionfor
eachcity:
Figure9:thenumberofdistributionforeachcity
Figure10:thedistributionmapofchargers
Based on the assume that the demographic difference in small cities is not obvious be-
causeofthesmallpopulation,werandomlyallocatetheremainingdestinationchargers
tothemoreopenareasofthemap(theremainingsmallcitiesthatwedidnotconsider).
2. Thelocationofsuperchargestations
• Forshort-distancetravelers
Inequation5,leta=0.3,rd=0.25togetthenumberofdistributionforeachcity.
• Forlong-distancetravelers


## 第 19 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#82794 Page16of24
Weuse weighted mediators to measure the importance of nodes in the network,
accordingtotheimportance. Byequation9andequation10,wecangetthenumber
ofdistributionforeachcityandthenumberofdistributiononeachroadas:
Figure11:mixmap Figure12:distributionofsupercharging sta-
tions
ReasonablenessAnalysis:
Because the Teslanetwork in Ireland is in its infancy, it is difficult to verify the validity
of our results. Westudy the relatively more mature Tesla network in the United States. The
figure below is a mixture of thebetweenness, thevehicledensity andtheshortest pathbased
onthe309majormetropolitanareasintheUnitedStates.Thelighterplacesindicatethehigher
proportion of thedestination charging stations andthe superchargingstations. Wecan easily
identify the coastal cities of Boston, Los Angeles, New Yorkand Miami though not fortified
traffic but with a large population. Wecan speculate that the reason for their distribution is
primarily our study of vehicle density.While for Peoria, Las Cruces, Jackson, Little Rock and
othercitieswithrelativelysmallpopulationbutthetrafficfortressofthecity,theirdistribution
ismainlyduetoourstudyoftheweightedmediation.
Moreover,the main highlight in the picture is the best route to place super-charging sta-
tions for long-distance travelers. And we can observe that our highlight area distribution is
in good agreement with the current Teslanetwork density distribution in the United States,
provingthatourmodelworkswell.
6.2.2 2b:Ourproposedchargingstationplan
1. Chargersdistributionorderingtrade-off
BasedonthesecondModel,weconsiderthreecases:buildallcity-basedchargersfirst,
orallruralchargers,ormixofboth. Themaindifferenceamongthemisthatdifferent
locationsaffectλinE (18). WeconsiderλchangewiththegrowthofPTaccordingto
q
equation(17),andgetthechangeofPT withtimetindifferentsituations,asisshownin
Figure13.
Result Analysis: We can see that hybrid construction achieves the 100% permeability
ratethefastest,andevenfasterwhenthetwoareroughlyproportionalto3:2.Thisis


## 第 20 页

Team#82794 Page17of24
consistentwiththeideaofusingpopulationdensitymeasuresinourmodel.Thecollected
datashowthattheproportionofurbanizationinIrelandis63.2%,sothemodelresultsare
inlinewithreallife.
2. CarsfirstorStationsfirst
Theminimumnumberofchargingstationstobebuiltissuchthatλisexactlyequalto
thethreshold,otherwisepermeabilityoftheEV (PT)willcontinuetodecrease.Wehave
changedtheratioofthenumberofchargingstationsinthecaseofbuildingthechargers
firsttothatinthecaseofbuildchargersinresponsetovehiclepurchasesseveraltimes.
TheresultisshowninFigure14.
1 (47,1) 1(30,1)
(39,1) (54,1) 323,1 (41,1) 108,1
0.9 0.9
0.8 0.8
0.7 0.7
0.6 0.6
0.5 ruralareachangerfirst 0.5
city-basedchangerfirst
0.4 mixtheratioofthecitytoruralareato3:1 0.4
0.3 mixtheratioofthecitytoruralareato3:2 0.3 carsfirst
2:1ratiobetweenthescaleofthesiteandthepresentrequiredscale
0.2 0.2 3:1ratiobetweenthescaleofthesiteandthepresentrequiredscale
0.1 0.1
50 100 150 200 250 300 50 100 150 200 250 300
t t
Figure 13: Chargersdistributionordering Figure14:CarsfirstorStationsfirst
trade-off
ResultAnalysis: Themaindifferencebetweenthetwocasesistherateofreaching100%
permeabilityandtheup-frontcapitalwastedbybuildingsuperchargingstations.Wecan
simplyassumethatthesavingofcapitalislinearwiththePTspeed,soweconcludedthat
itiswisetobuildthechargersfirst,andthatitisoptimaltobuildasitesizethatis2: 1to
now.Therefore,wecandrawtheconclusionoftheoptimalinvestmentplan:toestablish
a 2: 1 ratio between the scale of the site and the present required scale, and to establish
chargingstationsbymixingtheratioofthecitytotheruralareato3:2.
6.2.3 2c:Ourproposedgrowthplantimeline
BasedontheanalysisoftheSI-EImodel,themaintaskofdifferentperiodsischanged,it
canbeseenintheFigure15.
6.2.4 Analysisofkeyfactors
Basedontheaboveanalysis,nowwestudythekeyfactors.
1. InTask2a,wemainexplorethefinalTeslanetworktopology.Thekeyfactorsthatshaped
thedevelopmentofourplanistheratioofthetotalnumberofchargingstationsoverthe
countrytothatineachcity.
i i
精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！


## 第 21 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#82794 Page18of24
Figure15:Themaintaskofdifferentperiods
2. InTask2b,wemainexploretheTeslanetworkestablishmentprocess.Thekeyfactorsthat
shapedourproposedchargingstationplanaretheratioofthesimultaneousconstruction
ofurbanandruralareas.
3. In Task2c, we mainly explore the different phases of the Teslanetwork establishment.
The key factors that shape your proposed growth plan timeline are the different main
influencingfactorsindifferentstagesofestablishment.
6.3 Task3:A weak traffic network classification system
Thisquestionrequiresus tocreateaclassificationsystemthatwouldhelpanationdeter-
minethegeneralgrowthmodel,weconsidertocreateaclassificationsystemwhichincludethe
countrywhohasaweaktrafficnetwork. Theunderdevelopmentmaybeduetothespecialge-
ographyorunderdevelopedeconomy,whichmakesitdifficulttoestablishanationwideroad
system.
This question requires us to determine the general growth model, so we don’t consid-
ercountry-specificdetails,andtheonlydifferencebetweenclassificationsystemwithothersis
thatthereislittleneedtoconsidertheneedtoestablishchargingstationsforlong-distancetrav-
elers. Buildingroadwaysbetweenneighboringcitiesisthekeyfactorthattriggertheselection
ofdifferentapproachestogrowingthenetwork.
Nowourproposedplanforgrowingandevolvingthenetworkofchargers doesn’twork.
Therefore,weshouldgreatlyreducetheweightofbetweennessindexinthefirstmodel,which
willsimplifytheproblemtomainlyrelyingontheproportionofthenumberofvehiclesinthe
regiontoallocatechargingstationso Consideringpeople’ssatisfactionwiththeEVs network,


## 第 22 页

Team#82794 Page19of24
thesatisfactionof long-haultravelersis relativelymore difficulttomeetpreviously.Now that
we don’t need to take them into consider, it is more simple and fast to migrate away from
gasolineanddieselvehiclestoallEVs.
6.4 Task4:The impact oftechnology onEVs’ spread
1. TechnologythatwouldhinderEVs’spread:vehicle-share,ride-shareservicesandhy-
perloop
As these three technologies evolve, the per-capita holding of vehicles will fall (that is,
someownersselltheirEVs),butasmorepeopleusenewtechnologies,somemayfindit
inconvenienttobuyavehicleagain. ThesequalitiesareinlinewiththeSISmodel,soour
SImodelbecomesaSISmodel.Thephenomenonwillleadtoadeclineinthepopularity
rate of EVs. Therefore, it is necessary to dynamically adjust the construction of the EVs
networkbasedonthedecreasingproportion.
2. TechnologythatwouldboostEVs’spread:self-drivingcars,rapidbattery-swapsta-
tionsforEVs,andflyingcars
ThesethreetechnologieswillincreasetheattractivenessofEVs. TheλinourSImodel
willincrease,aswellasthepenetrationandpopularityrateofEVs.Theycanalsoexpand
thedemandofchargingstationsandacceleratetheconversiontofullEVs.
7 Sensitivity Analysis
WehaveconductedasensitivityanalysisoftheSI-EImodel: settingi(0) = 0.01ands-
tudyingthechangeoftheproportionofiwhenλis0.3,0.27and0.33respectivelyovertime.
1
0.9 =0.3
=0.33
0.8 =0.27
0.7
0.6
0.5
0.4
0.3
0.2
0.1
0
0 5 10 15 20 25 30 35 40
t
Figure16:thechangeoftheproportionofiwhenλis0.3,0.27and0.33respectivelyovertime
We’vefoundthattheproportionofiislesssensitivetoλwhenthesystemisinitsearlyand
i
精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！


## 第 23 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#82794 Page20of24
latestageswhileitissensitiveinmid-termstage.Forexample,whent=15,theproportionof
thethreeofiisabout0.4,0.5and0.6.Thisdiscoveryisofpracticalsignificance,whichmeans
themid-termstageistherapidgrowthstageofpermeabilityinwhichwecantakestepsto
increasepeople’ssatisfactionlevelthusincreaseλandspeeduptherateofpenetration.
8 Comment on Heavy Trucks
Heavy trucks generally need to travel a long way,as well as their huge traction, which
resultinthattheirdemandforsuperchargingstationsisgreaterthanthatofpersonalvehicles
and they are not suitable for charging in cities. When a country’s road transport industry is
developed, attention should be given to improving the satisfaction of truck drivers and the
numberofsuperchargingstationsinruralareasandsuburbanareas.
9 Analysis of the Model
9.1 Strengths
1. Themodelofdouble-layercomplexnetworkappropriatesproblem’srequirements,Anal-
ysisnetworkconstructionfromamacroscopicperspectiveisdifferentfromagreatdealof
analysisonthepowerandstreetlayoutorothermicroperspectiveinthefieldandgreatly
simplifiestheproblem.
2. TheSI-EImodelcleverlyassimilatedtheideaofthetraditionalSImodelandcombined
withtheevaluationindexsystemtostudythepermeabilityfromanovelperspective.
3. TheselectionofWeightedBetweenessisveryappropriate,wellidentifiedamajortraffic
hubcity,sothatthechargingstationdistributionmorereasonable.
9.2 Weaknesses
The layout of the charging stations is only accurate to the amount allocated to the city
becauseofthelargedifferencesamongcitiesandthedifficultyincollectingthedata,andwith
moredetaileddatawecangetamoreaccuratedistribution.


## 第 24 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#82794 Page21of24
10 Task5: Handout
The world is fascinated by reducing the use of fossil fuels, including gasoline for cars.
Whethermotivatedbytheenvironmentorbytheeconomics,consumersarestartingtomigrate
toelectricvehicles. Weshouldconsiderthekeyfactorsthataffectourplaninordertobuildthis
networkfasterandbetter.
1. Fromtheperspectiveofthefinalnetworktopology
Weshouldhaveamoreaccuratepredictionofthetopologyofthefinalnetwork,which
mainly contains the consideration of the number, location and distribution of charging
stations.Thesemetricsarethemostimportantreferencetomeasurewhetherthenetwork
building process is better or not. A better prediction can boost the Permeability, save
morefundingofnetworkconstructionandgetthemostsocialbenefits.
2. Fromtheinvestmentperspectiveofnetworkestablishmentprocess
Weshould maintain the highest possible investment efficiency in the network con-
struction process. Todecide the optimal ratio, the current ratio of charging stations in
urban and rural areas should be taken into account, combined with their own national
urbanizationrate.Moreover,buildingultra-scalechargingstationsinadvanceisextreme-
lyhelpful inaccelerating thepenetrationof electric vehicles. Although itbrings a waste
ofpreviouscapital,butthelatterpartofthebenefitsofspeedisfargreaterthanthewaste
here.
3. Fromthestageperspectiveofnetworkestablishmentprocess
textbfWe shouldensurethattheestablishment of thechargingstation tobest meetpeo-
ple’s needs. The leading crowd who influence the overall satisfaction levels is different
in different stages. We initially speculated that in general destination charging stations
should be built in the initial construction stage; supercharge stations for short-distance
travelers should be built in the mid-term stage; supercharge stations for long-distance
travelersshouldbebuiltinthelatterstage.
The above is the overall consideration of the key factors of network construction.We think it
would be most reasonable to set a gas vehicle-ban date at 40 years later. The leaders of all
countries should, according to the particular circumstances of their own country, determine
the ways that are best for themselves, I wish all of you early realization of full automobile
electrification!


## 第 25 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#82794 Page22of24
References
[1] Wu,Lixia.ResearchontheLayoutPlanningofChargingStationforElectricVehicleinthe
City[D].ChongqingJiaotongUniVersity,Chongqing,China:WuLixia,2017.
[2] Wu,Lian.LocatingElectricVehiclesRefuelingStationsBasedOnTheGeneralizedCover-
age[D].HuazhongUniversityofScienceandTechnology:WuLian,2016.
[3] Fang, Lu. The location-sizing problem of electric vehicle charging station deployment
basedonqueuingtheory[D].BeijingJiaotongUniversity:FangLu,2015.
[4] Xu,Hao.StudiesonOptimalChargingStationPlacingandOrderlyChargingStrategyfor
Large-ScaleElectricVehiclesintoGrid[D].HuazhongUniversityofScienceandTechnolo-
gy:XuHao,2015.
[5] Fei,Wu,Ramteen,Sioshansi.A stochasticflow-capturingmodel tooptimizethelocation
offast-chargingstationswithuncertainelectricvehicleflows[J].TransportationResearch,
2017,(53): 354-376.
[6] County
https://en.wikipedia.org/wiki/County
[7] City
https://en.wikipedia.org/wiki/City


## 第 26 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#82794 Page23of24
Appendices
Herearesimulationprogrammesweusedinourmodelasfollow.
somemoretextInputC++source:
#define N 307
#define INF 1000000
typedef struct
{
int from;
int to;
char *fromCity;
char *toCity;
int value;
} Data;
int *getPath(int *path[], int i, int j)
{
int *ret = (int *)malloc(sizeof(int));
for (int i = 0; i < 20; i++)
{
ret[i] = -1;
}
if (i == j || path[i][j] == -1)
{
return ret;
}
int temp = i;
int k = 0;
while (temp != j)
{
ret[k++] = temp;
temp = path[temp][j];
}
ret[k++] = temp;
return ret;
}
void Floyd(Data *matrix[], int *path[])
{
for (int k = 0; k < N; k++)
{
for (int i = 0; i < N; i++)
{
for (int j = 0; j < N; j++)
{
if (
matrix[i][k].value != INF &&
matrix[k][j].value != INF &&


## 第 27 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#82794 Page24of24
matrix[i][j].value > matrix[i][k].value + matrix[k][j].value)
{
matrix[i][j].value = matrix[i][k].value + matrix[k][j].value;
matrix[i][j].fromCity = matrix[i][k].fromCity;
matrix[i][j].toCity = matrix[k][j].toCity;
path[i][j] = path[i][k];
}
}
}
}
}

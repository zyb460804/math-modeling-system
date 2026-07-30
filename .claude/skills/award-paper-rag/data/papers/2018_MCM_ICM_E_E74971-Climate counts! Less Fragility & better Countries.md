# E74971-Climate counts! Less Fragility & better Countries


## 第 1 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
TeamControlNumber
Forofficeuseonly Forofficeuseonly
74971
T1 F1
T2 F2
T3 F3
ProblemChosen
T4 F4
E
2018 MCM/ICM Summary Sheet
Climate counts! Less Fragility & better Countries
Abstract
Withthe rapid increase of the climate change influence, considerable attention has been attached to so-
called ‘fragile’ country. In order to measure the impact of climate change and propose reasonable state
interventions,weestablishtheFragile-ClimateChangeCouplingModelandothermodelsbasedonthetheory
ofcountryfragilityandclimatechange.
In task 1, for the sake of numeric measurement of the climate change’s influence, we introduce the
anomalyofmeteorologicalelementsandtheextremeweatherprobability,whichmakeuptheclimatechange
index(CCI).Furthermore,12indicatorscloselyrelatedtotheclimatechangefrom threeaspectsareselected
primarily,andthenentropyweightmethod(EWM)andcoefficientofvariationmethod(CVM)areappliedto
integrate the indexes into the fragility index based on the climate change(FCI). Moreover, fuzzy cluster
analysis(FCA)isemployedtoclarifycountriesintofour:impregnable,stable,vulnerable,andfragile.
Intask2,weselectSomalia asaresearchobjectandanalyzethe correlationbetweenits CCI andthe12
indexes in the fragile state index(FSI) to reveal the impact of climate change. The result indicates that the
economic fragility is sensitive to CCI. Meanwhile, the social fragility has less reaction to climate change,
andclimatechangehaspotentialeffectonpolitics.
In task 3, the Chi-square analysis and fitting method are employed to reflect the specific function
relationshipbetweenFCIandCCI,bywhichweestablishtheFragile-ClimateChangeCouplingModel.Thus,
itcomestousthatwiththeincreaseofclimatechange inMexico,thefragilityrisesupcorrespondingly. We
define the country tipping point in the light of the result of fuzzy cluster, and build up the climate change
prediction model by utilizing the second exponential smoothing method. The conclusion is that a country
reaches the tipping point when the CCI of the country drops down to 58.72, and it will probably fall into
fragilecountry.Whentheotherindexesreachtheirowncriticalpoints,itshouldalsobevigilant.
In task 4, on the basis of three perspectives of fragility,we propose some human interventions aimed at
the twelve fragility indicators. They are listed as follows: strengthen infrastructure construction, reuse of
resources,improvethecoveringrateofgardening,returnarablelandtothewaterandsoon.Thenweestablish
theInterventionCostPredictionModel,whichiscomposedofthecostofinterventionofeconomicrecession,
ecosystemsustainability,societyhabitability,andopportunitycost.
In task 5, we propose some modifications to apply our model into smaller or larger states. With the
appropriate alteration of indicators of fragility and climate change, our models have high stability and
extensiveapplicability..
KeyWords: Climatechange,Fragility,EWM,Fuzzyclustering


## 第 2 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Content
1.Introduction........................................................................................................................................1
1.1Background....................................................................................................................................1
1.2Ourwork........................................................................................................................................1
2.AssumptionsandJustification...........................................................................................................2
3.Notations..............................................................................................................................................2
4.TheFragilityMeasurementonClimateChange.............................................................................3
4.1Climatechangeindex(CCI)...........................................................................................................3
4.2Fragilityindexbasedonclimatechange........................................................................................6
4.3Fragilityidentification....................................................................................................................9
5.FragilityAnalysisofSomalia...........................................................................................................12
5.1Climatecharacteristics.................................................................................................................12
5.2CorrelationbetweenCCIandFSI................................................................................................13
6.Fragility-ClimateChangeCouplingModel....................................................................................14
6.1ClimatecharacteristicsofMexico................................................................................................14
6.2Fragility-climatechangecorrelation............................................................................................15
6.3Definitionoftippingpoint............................................................................................................16
7.HumanInterventionandCostPrediction......................................................................................17
8.Modificationsofourmodel..............................................................................................................18
8.1Smallerstates................................................................................................................................18
8.2Largerstates.................................................................................................................................19
9.SensitivityAnalysis...........................................................................................................................19
10.StrengthsandWeaknesses.............................................................................................................20
10.1Strengths.....................................................................................................................................20
10.2Weaknesses.................................................................................................................................20
References..............................................................................................................................................21


## 第 3 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#74971 Page 1of21
1. Introduction
1.1 Background
Whenitcomestoclimatechange,manystudiescanbereferredtosincepeoplethink
morehighlyoftheimpactsclimatechangeexertsonenvironment,economicandsociety.
According to the Fifth Assessment Report (AR5)[1]from the Intergovernmental Panel
on Climate Change (IPCC), climate change refers to the changes in climate state. The
reasons account for that may be natural internal processes or external forces, like
volcano eruption, or continuous human activities which result in the composition
changes ofatmosphere.
Moreover, the effects of climate change are likely to aggravate the breakdown of
social and governmental structures, leading to fragile states consequently. Fragility is
alsobedefinedinAR5,which involveswithvariousconceptsand factors includingthe
sensitivitytowards harm and the lack of responseoradaptability.
Asafragile country,it’s economic,societyand populationwillbemoresensitiveto
the climate shocks such as extreme meteorological disaster, rising sea level,increasing
global temperature and decreasing arable land. Correlating with poor governance and
social fragmentation, environmental instability will trigger violent conflict
undoubtedly[2].
1.2 Ourwork
In order tofind out thewaythat climatechange effects onregional fragility, weare
required to establish an evaluation index model which determines a country’sfragility.
By selecting appropriate evaluation indicators, we endow target weights and combine
those low indicators to realize some comprehensive indexes. Subsequently, the
established model will be applied to various countries to test its applicability and
modifications willbe proposed to improveit.
Wewillproceed as follows forthesake of tackling theseproblems:
 Stateassumptionsandmakenotations.Ignoringsomeinsignificantimpacts,we
will narrow the core of our approaches towards regional fragility and climate
change. Then we will list some notations which are important for us to clarify
ourmodel and determinetheir definitions.
 Establishanevaluationindexmodelwhichillustratesthefragilityandmeasures
theeffectsofclimatechangesimultaneously.Wewillapplythefuzzyclustering
method to expound a state’s fragility, like fragile, vulnerable, or stable. How
theclimatechange affect fragility is alsoneeded.
 Apply our model to one of the 10 most fragile states and another state not in
thatandinvestigatetheiractualinfluencefactors.Thenwewilldefineatipping
point tojudge when acountry reachesit.
 Introducethehumanintervention.Humanactivitiescandoafavortopreventa


## 第 4 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#74971 Page 2of21
countrybecomingmoredelicate,whichcanbepredictedfromtheresultsofour
model. Subsequently, we propose some modifications to apply our model to
somesmaller orlargerstates.
 Sensitivity analysis and model evaluation. Withthe evaluation criteria defined
before, we evaluate the reliability of our model and do the sensitivity analysis.
Then, wewill discussthestrengths andweaknesses about ourmodel.
Thewhole modelingprocess can beshown as follows:
Fig.1Technologyrouteforthecreationofourpaper.
2. Assumptions and Justification
Tosimplify the given problems and modify it more appropriate for simulatingreal-
life conditions, we make the following basic hypotheses, each of which is properly
justified.
 Weassume the country as an overall unit without considering the differences
of regions within the country. The assumption is a prerequisite for us to do
intensive study. For some countries with vast territory, the climatic conditions
vary in latitudeand development ofdifferent regions isimbalanced.
 We assume that all the countries react positively to climate change and take
human interventions to decrease the fragility of their country, neglecting the
passivecountries.
3. Notations
Welistthesymbols and notationsused inthis paper inTable1.
Table1Notations
Symbols Definition
ERI Economicrecessionindex


## 第 5 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#74971 Page 3of21
ESI Ecosystemsustainabilityindex
SHI Socialhabitabilityindex
FCI Fragilityindexbasedontheclimatechange
CCI Climatechangeindex
C Pearson’scontingencycoefficient
TC Totalcostofhumanintervention
4. The Fragility Measurement on Climate Change
The Organization for Economic Cooperation and Development (OECD) assumes
that if a country, armed with the weak ability of managing the basic state function like
population and territory, lacks of political ability or political will to develop a
constructive mutually reinforce relationship with the society, then the country is
considered as a fragile country[3].
The Country Policy and Institutional Assessment (CPIA) is one of the mostwidely
used evaluation systems, which is composed of four clusters: economic management,
structural policies, policies for social inclusion and equity, and public sector
management and institutions. These four clusters allow for further refinement and can
beexpanded to 20criteria (now has been decreased to12criteria)[4].
4.1 Climatechangeindex(CCI)
As the recent researches show[1], the core impact of the climate change mainly
focused on the warming in temperature, the anomaly of precipitation, the rise of sea
level, thenumber ofdays in extremeweather.
4.1.1Temperature,precipitation, sea level indicator
Thecharacteristicsofacountry’sclimateliketemperature,precipitationorsealevel
differ alot because of itslongitude, latitude, andaltitude. Therefore, we define annual
temperature anomaly d ,annual precipitation anomaly d ,and annual sea level
1 2
anomaly d ,annual standard deviation oftemperature ,precipitation  ,and sea
3 1 2
level to describe theclimatechange.
3
Recallingonthe basicknowledgeofmeteorology, thenarrow concept ofclimateis
the mean state of weather. The World Meteorological Organization (WMO) stipulates
30 years’ statistical mean and variability of climate factors can represent the basic
characteristics ofthenativeclimate.
Weassumethat thetemperature, precipitation, and sea level index obey segmented
distribution.When theannual anomaly d ofa country exceeds the30years’standard
i
deviation  ,climate ischanging and thescale depends ontheirdifference. Thus, we
i


## 第 6 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#74971 Page 4of21
Have
where , ,and represent those index oftemperatureT,precipitation P,
1 2 3
and sea level Lrespectively. Sincethefunction is continuous, thevalues of same
critical points are equivalent. Thus, we willgive theboundary conditions.
1
0.5
0.1
0 2 5
Fig.2 The curves of temperature, precipitation, or sea level index. The index model has
three subsections: exponential, linear, and logarithmic distribution, showing the effects
threeindicators’anomalieshaveonnativeclimatechange.
As theFig.3 shows, theannual anomaly d changing withina standard deviation
i
 ,itis reasonable and common because of themicro disturbance, thus thisfunction
i
obeys exponential distribution and tends to climatechange rapidly, settingthecritical
value =0.1.With theincreasing value ofannual anomaly, thespeed willslowdown
i
gradually, from thelinear shape, setting thecritical value =0.5 ,tologarithmic
i
distribution.Then we have
4.1.2 Extr
eme
weat
her
indi
cato
r
As isvividly shown in Fig.4,in thecontextof global warming, theextremeweather


## 第 7 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#74971 Page 5of21
disasters mainly embodies in high temperature and rainstorm[6]. Thus, combined with
the temperature and precipitation index, we can construct the extreme weather index
E.
frequency frequency
Hotweather
increase
Hotweather
Extremehot
weather
Extreme increase
hotweather
Fig.3 The schematic diagram of parameters of climate probability distribution. The right
partshows the increaseof average temperature andstandard deviation. The shade of light
redindicatesthehotweather,whiletheredshadeindicatestheextremehotweather.
Weassumethat thetemperature and precipitation during oneyear of acountry have
anormal distribution, which willbe confirmed later.Wecan derive that
Therefore, in order to simplify the model and simultaneously the effectiveness of
our model, we select the anomaly of temperature, precipitation, sea level and the days
of extreme disaster days as the points of focus for the sake of analyzing the influence
of climate change. Subsequently, we weight the indexes and integrate into one
comprehensivemetric, which isconsidered tobeableto represent the extentofclimate
change. It is difficult for ustomeasure theactual proportion ofthose factors, hence we
assumethat they are as crucial as eachother.
1
CCI  (T+P+L+E)100 (7)
m
where CCIisthe climatechange impact metric, T,P,L,Eare theevaluation


## 第 8 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#74971 Page 6of21
indexesof temperature, precipitation,sea level, and extremeweatherrespectively.
Considering thelandlocked countries withouttheeffects ofsea, weare required to
makea difference between landlocked and coastal states. Thus, we have
1,m 4 coastal or islandcountry
 (8)
  0,m3 landlocked country
4.2 Fragilityindex based on climatechange
4.2.1Primary indicatorsystem
Since the World Bank already has its evaluation system, the evaluation criteria he
haschosenarefromamacroscopicandcomprehensiveperspective. Inordertodevelop
astrong relationship between theimpact ofclimatechange and acountry’s fragility,on
the basis of a narrative explaining links between environmental stress and conflict[5],
wedefine fragility evaluation indexesfrom threelevels.
Biodiversity
Infection
Airpollution
Mortality Forestcoverage
Freshwater
Migration
resources
Society
Ecosystem
Available
landarea
Fragility
Economy
Floodloss Cerealyield
Energy
Droughtloss
consumption
Fig.4 Process flow for the establishment of the fragility evaluation criteria. From the
perspective of economic recession, ecosystem sustainability, and society habitability, the
model defines twelve indicators and incorporated them into the fragility index based on
climatechange.
(1)Economicrecession
 Energy shortage X (kwh per capita). When acountry suffers from aclimate
1


## 第 9 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#74971 Page 7of21
shock, armed with the weak infrastructure construction, the country will be more
sensitive to the climate change. Thus, we introduce the ratio of the total electricity to
thepopulation toreflect theenergy shortage.
 Cereal yield X (kg per hectare). Agriculture may be one of the mostsensitive
2
departments to climate change. We choose food production to represent the
agriculture’s reflection on climate change. The value of this indicator is inversely
proportional to thefragility.
 Economicloss in flood disaster X (%of GDP). Global warming may
3
strengthen the hydrologic cycle and average precipitation tends to increase. Flood
disasters will cause the mountain torrents rushing down, flooding farmland,
destructionsofinfrastructures, and casualties. Then weintroduce theratio ofeconomic
lossinflood disaster toGDP to represent thedisaster’simpacts.
 Economic loss in drought X (% of GDP). Although the precipitation may
4
increase in some regions, actual vaporization will rise simultaneously caused by the
rising average world temperature. We hence define the ratio of economic loss in
drought to GDP to symbolizedrought’sstress.
(2)Ecosystemsustainability
 Forest area X (% of land area). Forest productivity is one of the main factors
5
to judge the tree growth and ecosystem functioning. The influences climate change
exerts on forests major in temperature stress, etc. Thus, we introduce the ratio of the
forest area to grossing landarea to represent a country’sforest coverrate.
 Annual fresh water X (cubic meters per capita). Fresh water resource is one
6
ofthematerialbasisuponsurvivalofmankind.Climatechangemaycausegroundwater
levels to decline and rivers to dry up.Consequently, annual fresh water occupation per
capitais defined toillustrate theeffects of climatechange.
 Arable land X (hectares per person). With the average temperature rising
7
noticeably, glaciers melt undoubtedly, leading to the rises in sea levels. The
intuitionistic result is the reduction of arable land. We hence introduce the arable land
percapita to describe its reflection toclimateshock.
 Greenhouse gas emissions X (metric tons per capita). As we all know,
8
greenhousegasemissionsandclimatechangeareinteractedwitheachother. Therefore,
we determine greenhouse gas emissions per capita as one of the influence of climate
change.
 Native biodiversity X . Some species are in danger of extinction since they
9
fail to adapt to the new living environment. Thus, we introduce the native species
threatened as thebiodiversity reflectionto climatechange.
(3)Society habitability
 Net migration X .Duetotheincreasing severe burden ofnatural resources,
10
theimpacts ofclimatechange threaten theself-sufficient ability ofhuman beings. We
consequentlydefine net migration as an evaluation indicator.


## 第 10 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#74971 Page 8of21
 Cause of death, by natural disasters X (% of total). Extreme weather like EI
11
Niño, sand storm and hurricane will increase in frequency and intensity after climate
change.Wehence introducethe ratio ofdeath by natural disasters to totalnumber.
 Prevalenceof infection X .Peopleare at high risk ofdying from
12
communicablediseases through the transmissionofinsects. So,wechoose prevalence
ofinfection to represent thereflection ofhumanhealth toclimate change.
4.2.2Weightof indicators
a.Entropyweight method
With the evaluation indicators defined above, we further determine the weights of
these indicators, resulting in the combination of primary indicators. Recalling on the
Entropy WeightMethod (EWM), wewill carry out thestandardized treatment,making
theoptimaland worst value ofeach variables after alternation be1and 0,respectively.
The evaluation indexes are X ,X ,X ,...,X , where X

x ,x ,...,x

. Among
1 2 3 k i i1 i2 in
there, k and n are the number of defined evaluation indictors and sovereign
countries throughout theworld, where k=12 .
For the sake of the cost-type indicators, the fragility of a country is proportional to
the value of the indicator. However, in terms of the gain-type indicators, the higherthe
valueis,theless fragile thecountry willbe. Thus, wehave
 x  min(x)
y ij i
ij
 max(x )min(x )
 i i j 1,2,...,n (9)
 
max(x)x
y  i ij
 ij
 max(x ) min(x )
i i
where y is the standardizedvalue of each evaluation indicatorof each country,
ij
max(x ) and min(x ) arethe maximumand minimum valueofthe evaluation
i i
indicato X . max(x )max  x ,x ,...,x  , min(x )min  x ,x ,...,x  .
i i i1 i2 in i i1 i2 in
r
Afterstandardization, we succeed in substituting y for x to implicate the
ij ij
fragility ofa country. Then we introduce
py / n y (10)
ij ij j1 ij
According to theconcepts ofself-information and entropy inthe information theory,
wecan calculatetheinformation entropy E ofeach evaluation indicator, hence we
i
can obtain
n
E ln(n)1 p ln(p) (11)
i ij ij
j1
On thebasis oftheinformation entropy,we will further computetheweight of each
evaluation indicator wedefined before.
1E
w  i i 1,2,...,k (12)
i k  E
i i


## 第 11 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#74971 Page 9of21
Subsequently, we can derive the three comprehensive evaluation indicators:
economic recession index, ecosystem sustainability index, and social habitability.
Hereafter this paper will be abbreviated as ERI , ESI , and SHI respectively. On the
basis ofthosecalculated weights, we have
ERI  w y  w y w y w y
 j 1 1j 2 2j 3 3j 4 4j
ESI  w y  w y  w y  w y  w y (13)
j 5 5j 6 6j 7 7j 8 8j 9 9j

SHI  w y +w y +w y
 j 10 10j 11 11j 12 12j
b.Coefficient ofvariation method
Furthermore,weapplycoefficientofvariationmethodtoweight thesethreeindices
and merge them into a comprehensive metric. Therefore, we will introduce the
application ofcoefficient ofvariation methodbriefly.
Coefficient of variation method (CVM) utilizes the information from various
indexes and achieve the weight of each index through calculating, which shows to be
an objective approach to give weight.
Owing to the influence of different dimension, it is hard to compare the index
directly,so it needs the coefficient of variation of each index to measure the difference
extentofthem. The formula ofeach indexcan beexpressed as:

V i  z i i1,2,3 (14)
i
where V is thecoefficient of variation ofthe index i,which can also becalled as
i
standard deviation coefficient, and  means thestandard deviation oftheindex i.
i
And the z , z , z separately means ERI,ESI,and SHI.Then theweight of
1 2 3
eachindex comes tous:
V
W  i i 1,2,3 (15)
i n
V
i1i
Bythisway,weareabletoachievetheweightofeach index withoutanysubjective
impression. Finally, after getting the weight, we can derive the comprehensive metric-
fragility index based ontheclimatechange FCI
FCI (W ERIW ESIW SHI)100 (16)
1 2 3
4.2.3Fuzzy Cluster Analysis
Combined with the comprehensive fragility metric we established before, we will
importdataofvariouscountriesfromtheWorldBankandcalculatethevaluesof FCI .
Then accordingto theirrespectivevalues, weuse Mahalanobis distanceto clarifythese
countries as: impregnable, stable, vulnerable, and fragile. Thus, we can identify a
country’s fragility from their FCI . Since it is a conventional method, we neglect the
calculateprocess ofit.
4.3 Fragilityidentification
In theestablishment offragility-climate change coupling model, we assumethat n


## 第 12 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#74971 Page 10of21
isthenumberofsovereign countries throughouttheworld, which is too complicated to
implement. Thus, we select 20 countries varying in geographical locations, economy
degree, and climatefeatures throughout theworld, which will belistedlater.
Table2Weightvaluesofthetwelveevaluationindicatorsandthreecomprehensiveindexes.
Indicators Weights Indicators Weights
Energyshortage 0.2912
Cerealyield 0.1227
Economic
0.1145
recession Economiclossinflooddisaster 0.1648
Economiclossindrought 0.1971
Forestarea 0.2965
Fragility Annualfreshwater 0.2083
Ecosystem
0.6055 Arableland 0.1122
sustainability
Greenhousegasemissions 0.1954
Nativebiodiversity 0.1876
Netmigration 0.1986
Society
0.2800 Causeofdeath,bynaturaldisasters 0.5177
habitability
Prevalenceofinfection 0.2837
Since the specific value of those indicators have been given in Table 2, hence we
can calculate the FCI of our selected countries and apply fuzzy clustering method to
clarify these countries into four groups: impregnable, stable, vulnerable, and fragile.
The higher the value is, the more fragile the country is. The results of clustering are
shown as follows.
(a) (b)
(c) (d)
Fig.5Clusteringresultsofthefourindicators.(a)economicrecession;(b)society


## 第 13 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#74971 Page 11of21
sustainability;(c)ecosystemhabitability;(d)fragility.Thesequencenumberalongthe
abscissaaxisrepresentsthecountry:1Afghanistan;2Bangladesh;3Barbados;4Canada;
5Colombia;6Cuba;7Dominica;8Eritrea;9Finland;10France;11Georgia;12Iran; 13
Mali;14Mauritius;15Paraguay;16Senegal;17SouthSudan;18TrinidadandTobago;19
Tunisia;20UnitedStates.
According to Fig.5 , we can determine the classification standards of a country’s
fragility, once the value of ERI, ESI , SHI , and FCI is figured out. As is shown
in Fig.6, the classification standards of the three combined indicators and the
comprehensive metric varya little. Since theirfocus of attention: economy, ecosystem,
society,and combinationputtheemphasis onthevariousdevelopmentofacountry,the
ultimateranks offragility willbe differentsimultaneously.
The deeper the color is, the more fragile the country will be. According to
classification standards, the comprehensive metric-fragility rank indicates that stable
country is the overwhelming country, succeeding in striking a balance between
vectoring sustainable development.
21.27 47.24 63.29
comprehensivemetric
Comprehensivemetric
25.72 40.6 71.25
Economicrecession
26.92 33.0 8 62.15
Ecosystemsustainability
25.41 38.60 59.49
Societyhabitability
0 20 40 60 80 100
impregnable stable vulnerable fragile
Fig.6Classificationstandardsandtheirrespectivecriticalpointsofverifyingacountry’s
fragility,whichisclassifiedasimpregnable,stable,vulnerable,andfragile.
The original fragility ranks from Fragile States Index 2017 (FSI), as we can see in
Fig.7, match the fragile index based on climate change FCI we established well. We
choosesix countries as anexample.
Forexample, SouthSudan is actuallythemost fragile countryin theworld because
of its poverty, weak infrastructure, and relatively basic agriculture technologies.
Similarly, it is more sensitive to climate change, making itself the most fragile index.
When it comes to developed countries like United States, its global superpower, firm
infrastructure, and advanced technology determine that it will be easier to deal with
climatechange. Thus, it is clarified asimpregnable.


## 第 14 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#74971 Page 12of21
gfrraagdility
200
rank
160 impregnable
120 stable
80
vulnerable
40
Fragile
0
South Tunisia Finland France United Eritrea
Sudan States
Fig.7ComparisonoforiginalranksfromFSIandestimatedfragilityindexesfromFCI.
5. Fragility Analysis of Somalia
5.1 Climatecharacteristics
Second-placedSomalialocatesinSomalipeninsulaintheAfricanContinent,onthe
verge of the India Ocean. Itis one of the least developed nations throughout theworld,
with vulnerable industry, food shortage, and natural disasters. Most regions ofSomalia
belong to subtropical and tropical desert climate. The typical characteristics are high
temperaturethroughout theyear and dryorrainlessenvironments[7].
Temperatureanomaly
1
28
Annualmeantemperature
27.5
0.5
27
26.5 0
26
-0.5
25.5
25 -1
1991199319951997199920012003200520072009201120132015
Fig.8TheannualmeantemperatureandtemperatureanomalyofSomaliafrom1991to
2015.
AsisshowninFig.8,the24years’averagetemperatureofSomaliais26.5 C,which
illustrates its high temperature very well. The annual temperature fluctuates in a small
scale: from -0.5 C to 0.5 C . Then we conduct the normal distribution verification of
temperatureand precipitation asfollows.
According to Fig.9, thedaily average temperature and precipitation scatterplots fit


## 第 15 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#74971 Page 13of21
very well withthe curves of normal distribution.Thus, our assumptionused inthe
establishment ofCCIisreasonable andpractical.
(a) (b)
(c) (d)
Fig.9 Verification of normal distribution. (a) q-q plot of the temperature; (b) frequency
histogram of daily average temperature; (c) q-q plot of the precipitation; (b) frequency
histogramofdailyaverageprecipitation.
5.2 Correlation betweenCCI and FSI
To research more deeply on the effect of climate change, we study the relationship
among climate change and several indexes of FSI in Somalia for the last 30 years by
method ofPearson correlation analysis. Correlation coefficients are shown inTable3.
Table3CorrelationcoefficientsofclimatechangeandeachindexofFSI
Security Factionalized Group
Indictors Economy
apparatus elites grievance
Coefficients 0.1327 0.0028 0.4007 0.6528
Economic Humanflight State Public
Indicators
inequality andbraindrain legitimacy services
Coefficients 0.5431 0.3287 0.0028 0.2758
Human Demographic Refugeesand External
Indicators
rights pressures IDPs intervention
Coefficients 0.1279 0.5628 0.6526 0.0167


## 第 16 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#74971 Page 14of21
In Table 3, it comes to us clearly that CCI and FSI show great relevance. For
example, CCI has high coefficient with poverty and economic decline, economic
inequality, which represent that the aspect of economy is sensitive to the change of
climate. And the climate change directly and powerfully changes the economy of one
country. For example, the increase of mean temperature would come more droughts,
whichdecreasesthegrainyieldandinevitablyreducestheincome.However,therichest
crowd still take up most of the wealth in the country, so the economic inequality keeps
increase.
On the other side, the coefficients with Public services, Human flight and brain
drain, Human rights, which belong to the social aspect, are less than that of economy.
It is easily to understand. Because, though the influence of climate change on the side
of society is significant, the influence is slow and hidden. So the effect on the social
aspect needs timetoreveal.
Nevertheless, the coefficients with Factionalized elites, State legitimacy, which
stand forthe politics aspect, areverylittle.That means the connection between climate
change and politics is limited. The main reason is that politics is the result of human
subjective initiative, which has little relationship with weather. However, it doesn’t
mean thereis noeffect.Theclimatechange still has potential influenceonpolitics.For
example, the poverty resulting from famine, whose critical reason is drought, may
triggera politicalrevolution.
6. Fragility-Climate Change Coupling Model
6.1 Climatecharacteristics ofMexico
Because of the many plateau and mountainous areas, the climate of Mexico is
complexed and various. The vertical climate is characterized. In most areas, they can
beclarified as drought and rain seasons.
FCI CCI
60.0 70
58.0 60
56.0 50
54.0 40
FCI
52.0 30
CCI
50.0 20
48.0 10
200620072008200920102011201220132014201520162017
Fig.11ComparisonofMexicoFCIandCCI


## 第 17 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#74971 Page 15of21
As is illustrated in the Fig.11, the FCI of Kenya rise up rapidly between 2006 and
2008, and then it fluctuates at a high level. It is displayed by the linear trend line of
CCI that though the level of CCI doesn’t keep increasing, the overall trend is to rise
up,and theimpact of theCCIisto improvetheindex FCI .
6.2 Fragility-climatechangecorrelation
In order to confirm the correlation between climate change and fragility of the
country, we will conduct Chi-square analysis between FCI and CCI . According to
thevalues of FCI,CCI,we will have thebasis matrix M
m m
M  11 12 m  (17)
m m 1n

 m 
21 21 2n
Where m represents FCI , m represents CCI .Then, we can calculatechi-
1j j 2j j
square value
2:
 m2 
2  g n 2（ ij ）1 (18)
  j1 i1 g g  
2 n
Where g n 2 m , g 2 m , g n m .Then thePearson’s
j1 i1 ij 2 i1ij n j1 ij
contingency coefficient Ccomes to us
C  2 /(g2) (19)
The higher the value of C , the more closely the correlation between climate change
effects and fragility ofthecountry.
In order to measure theeffects ofclimatechange onfragility, weassumethat
without the influence of climate change, the country’s fragility is very small. When it
is shocked by climate change, the fragility will increase rapidly, with the exponential
formation, thus wehave
FCI r exp(l CCI  u) (20)
where r,l,uare theregression coefficients derived from thefittingcurve.
AsisshowninFig.10,byanalyzingtherelationshipbetweenclimatechangeimpact
index and the national vulnerability in the last thirty years in Somalia, we can see that
when climate change impact index grow, the national vulnerability approximately
presents positiveexponential function, which is estimatedas:
FCI 21.25exp(0.0636CCI 0.0014) (2)
The good-of-fit test of our coupling model is 0.5317. The result is not perfect,
because climate is random complexity, however, our fitting model still elaborate vital
phenomenon.That is when climate change is very intense, thecountry is rather fragile.
Without the effects of climate change, the value of CCI is 0 and FCI is a constant.
Thecountry’sfragilitywillbesosmallthatwecanidentifyitasstableorimpregnable.


## 第 18 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#74971 Page 16of21
Fig.10Thecurvefittingofourcouplingmodel.Thebluelineismadebythemethodof
cubicspline,andtheblackdottedlineisafittingcurve.
6.3 Definitionof tipping point
The climate change always exists and every country more or less is influenced by
it. But not all of the country will fall into the ‘fragile’ country under the pressure of
climate change. However, some of them inevitably change into fragile country, and
each of them has gone through the tipping point between ‘stable’ and ‘fragile’. In this
part we will discuss about the definition of tipping point based on the conclusion of
Fragility-ClimateChange Coupling Model.
Tobegin with, it’s hard to give a precise point of time when will the country fall
into fragile country, but we can learn the circumstance that the country will soon
become fragile country. What we need to do is that illustrate this critical point whichis
shownbythevalueofindexes.Andfromwhatwasdiscussedabove,wecanfairlyknow
that when one country’s FCI drop down to 63.29, it enters the fragile country rank.
However,acountry’scriticalpointisoughtnottobejustoneindex,forwhenoneaspect
shows to be hazardous for one country’s fragility, it may not be reflected in the
comprehensive index, but it really need to be noticed. Therefore, we list the tipping
pointfor each aspect inTable4.
Table4Tippingpointforeachaspect
Aspect ERI ESI SHI FCI
Value 71.25 62.15 59.49 63.29
Whenthevalueofabove parametersreach thelevel inthetable, thecountry should
keepvigilantagainsttheinfluenceofclimatechange,whichalreadygoestoahighlevel
and thecountry would slidto therank offragilecountry.
According to the research of IPCC, it comes to us clearly that the world is
Irreversiblywarminganddifferentweatherdisasterstakeplacemorefrequently.Based


## 第 19 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#74971 Page 17of21
on the conclusion of Fragility-Climate Change Coupling Model, we can easily get the
relationship between CCI and FCI . Substitute the value of tipping point into the
formula, we will derive that when the CCI comes to 58.72, the country experiences
thecritical point,which shouldbeattached closeattention to.
WeusethesecondexponentialsmoothingmethodtoestablishtheClimateChange
Prediction Model. Its formulacould beexpressed as:
(22)
Wherethe S(1) is thesmoothvalue oftheprimaryindex, S(2) isthesmooth valueof
t t
thesecondindex.Whenthetrendofparametershowstobestraightline,itcouldemploy
thestraight linemodel:
M  a bm m1,2 (23)
tm t t
a  2S (1) S(2)
 t t t
(24)
(1) (2)
b  (S  S )
 t 1 t t
where the M means thevalue ofCCI.Based onthis model, wecan predict the
tm
strength ofclimate change, and theresult reflects thatby2023,Mexico’sCCIwill
boomand exceed 58.72,which represents that it falls intofragile country.
Fig.12Thepracticalvalue(2006~2017)andpredictiedvalueofCCI(2017~2030).
7. Human Intervention and Cost Prediction
Our fragile-climate change coupling model presents the interaction of climate
change and national vulnerability. If a country is stable or impregnable, it raised the
resistance of the risk of climate change. This is a positive feedback system. Next, we
willpropose somestatedriven interventions which could improve theabilityto cope


## 第 20 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#74971 Page 18of21
withclimate change and mitigatetherisk ofclimate change.
On the basis of our established twelve fragility indicators, we propose some
interventions from the perspective of exposure, sensitivity, and adaptive capacity[6].
Exposureindicates thepressureof a countrysufferingfrom climatechange. Sensitivity
reflects theinternal system’s sensitivityto climate change.Adaptivecapacitydescribes
theinternal system’s response and adaptation to climatechange.
(1)Economicrecession
 Strengthen infrastructure construction. Infrastructure like dam or drainage
systemvaluesimportantfacedwithnaturaldisasterslikeflood,rainstorm.Thismeasure
willreduce economiclosses and casualtiesefficiently.
 Reuseofresources.Electricitygenerationconsumesenormous fuel,leadingto
greenhouse gas emissions. The reuse of resources will reduce air pollution and save
energy alot, which slows down theclimatechange.
(2)Ecosystemsustainability
 Improvethecoveringrateofgardening.Afforestationandprotectionofforests
can improve the ecosystem, curb erosion, and resist sandstorm damage. Implement of
itcan reducethe fragile sensitivity toclimatechange.
 Return arable land to the water. This measure is not only helpful to flood
control, but also protect theecosystem, thus increasethe country’s ecosystemstability.
(3)Society habitability
 Improvesocialsecuritybenefits.Ifthemajorityofpeoplehaveaccesstosocial
security benefits when shocked by climate disasters, the country will be more stable
and people get along certainly harmonious with eachother.
 Increase the service level for elementary medical institutions. When the
climate change shocks, the prevalence of infection will increase rapidly. With the
perfect medical treatment, we can minimizecasualties.
Thus, wecan develop theintervention cost prediction model:
TC  ERCESCSHCTC (25)
where TC is the total cost of human intervention, ERC , ESC , SHC are the cost
ofinterventionofeconomicrecession,ecosystemsustainability,andsocietyhabitability,
TC is the opportunity cost. Opportunity cost is the economy development we give up
inorder todecrease thecountry’s fragility.
8. Modifications of our model
Forthesakeofsmaller“states”(suchascities)orlarger“states”(suchascontinents),
ourcouplingmodelcanalsowork,whileprecisionofourpredictionwilldecrease.Thus,
wehave topropose somemodificationstoimprove ourmodel.
8.1 Smallerstates
 The majority of greenhouse gas emissions comes from cities result from the


## 第 21 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#74971 Page 19of21
consumptionoffossilfuel,whichusedinelectricitygeneration,transportation,lighting,
etc. Thus, the weights of our model must be adjusted to adapt to the practical situation
ofthecity.For example, theweight ofgreenhouse gas emissions shouldincrease.
 The infrastructure like drainage system of a city determine its fragility to a
great extent. Thus, the indicators of a city’s fragility must be more detailed, such as
infrastructure construction, renewable energy. Moreover, we should take the country’s
macro-control policies intoconsideration.
8.2 Largerstates
 Asforcontinents,itsvastlanddeterminesthattheclimatechangewillbemore
complicatedandchangeable.Ashigh-latitudeareas,meltingglaciersandfrozensoilare
expected to be considered. Meanwhile, large scale circulations between oceans like
Walker Circulation, Thermohaline Circulation, and El Niño Southern Oscillation
(ENSO)are themajorconcerns of climatechange.
 Thefragilityofthecontinentalsoneedsalteration.Massmigrationofrefugees
caused by disease breaks, famine, or military action, may exert great influences on the
fragility ofthecontinent. Theweights ofthoseindicators changeinevitably.
9. Sensitivity Analysis
In real life, statisticaldata areoften inaccurateand theremaybesomedeviationsin
the inputs of our model. These deviations may affect the results of our model. Totest
the robustness of our model, in this section, we will analyze the sensitivity of our
Climate Change Prediction Model in task 3. The results of the sensitivity analysis
explainthat ourmodel showa perfectstability.
Fig.13ThecurvefittingofCCIwithtime.Theblacklineisafittingcurveandtheblue
shadowpartistheconfidenceintervalforfutureprediction.


## 第 22 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#74971 Page 20of21
In task 3, we predict in 2023 Mexico’s CCI will exceed 58.72 in the method of
Second Exponential Smoothing, which indicate that it will fall into a fragile countryin
2023, if not take actions to cope with climate change. In the section, we forecast the
tippingpointinMexicobycurvefitting,thefittingresult showthatin theyearof2020,
the CCI excess 58.72 close to the previous result. Furthermore, by changing the
parametersofcurvefittingwith95%confidencebound,asisshownintheblueshadow
part, we discover our model is still stable and the tipping point range from the year of
2019 to 2021. Compared with the past results, the error is about 2-4years, which is
within acceptable limits. This shows the stability of our model, which can solve
practical problems in real life.
10. Strengths and Weaknesses
10.1 Strengths
 Thefragility-climate change coupling model established in ourpaper is based on
thefragility theory and research results ofIPCC, thusit isrelativelyrigorous.
 Theresultsoffragilityindexbasedonclimatechangematchestheranksofselected
countries from FSIwell, which indicates ourmodel is reasonable andeffective.
 Our evaluation indicators are determined from three perspectives: economic
recession, ecosystem sustainability, and society habitability. It is comprehensive
and objective todescribe thefragility ofacountry.
10.2 Weaknesses
 Ignoring the difference of climate distribution throughout the country, we use the
nationalaveragelevelstodescribethecountry’sclimatecharacteristics,whichmay
reducetheaccuracy ofourmodel.
 Weargue thatall thecountries react positively to climatechange, neglecting those
passivecountries, which may exert onourintervention cost predictionmodel.


## 第 23 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#74971 Page 21of21
References
[1]PachauriR K,Allen MR,BarrosVR,et al. Climatechange 2014: synthesis report.
Contribution of Working Groups I, II and III to the fifth assessment report of the
Intergovernmental Panel on ClimateChange. IPCC, 2014.
[2]Theisen,O.M.,Gleditsch,N.P.,andBuhaug,H.“Isclimatechangeadriverofarmed
conflict?”ClimateChange, April 2013,V117(3),613-625.
[3] Stewart F,Brown G. Fragile states. University of Oxford. Centre for research on
inequality, human security and ethnicity(CRISE),2009.
[4] Bandura R. A survey of composite indices measuring country performance: 2008
update. New York: United Nations Development Programme, Office of Development
Studies(UNDP/ODS WorkingPaper),2008.
[5]Krakowka,A.R., Heimel, N.,and Galgano, F.“ModelingEnvironmenal Securityin
Sub-Sharan Africa –ProQuest.”The Geographical Bulletin, 2012,53(1):21-38.
[6]LiuYang.Studyonthesocial and economic effects of global climatechange onthe
estuary and coastal areas of the Yangtze River Delta. East China Normal University,
2014.
[7]Somalia:https://en.wikipedia.org/wiki/Somalia
[8] Schwartz, P. and Randall, D. “An Abrupt Climate Change Scenario and Its
Implications forUnited States National Security”,October2003.
[9] FragileStates Index: http://fundforpeace.org/fsi/
[10]The WorldBank:http://www.worldbank.org/en/topic/fragilityconflictviolence/br
ief/harmonized-list-of-fragile-situations

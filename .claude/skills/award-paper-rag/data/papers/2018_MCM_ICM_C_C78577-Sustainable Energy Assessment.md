# C78577-Sustainable Energy Assessment


## 第 1 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team Control Number
For office use only For office use only
78577
T1 _ F1 _
T2 _ F2 _
T3 _ F3 _
Problem Chosen
T4 _ F4 _
C
2018
MCM/ICM
Summary Sheet
SustainableEnergy Assessment
Summary
Energyisoneofthefourpillarsofmodernsocialdevelopmentthemostbasicmaterialbasis,anda
prerequisiteforhumancivilization.InUnitedStates,manyaspectsofenergypolicyaredecentralizedtothe
statelevel.
Inthispaper,weareaskedbythesestatestoinformtheirdevelopmentofasetofgoalsfortheir
interstateenergycompact.
First,wepreprocessthedata,includingtheprocessingofmissingvaluesandthenormalizationof
thedata.Intheprocessofmissingvalueprocessing,wedealwiththeindicatorslackingasmallamountof
databyCubicSplineInterpolation,theindicatorslackinglessthanahalfofdatabycurvefitting,andthe
indicatorsmissingthevastmajorityofdatabyreplacingiswiththeaveragevaluesofothercities.
Afterthat,weusetheARIMAmodeltopredicteachstate'sindicators.Itisestimatedthatby2025,
theoverallscoreofeachstatewillreachCA:0.2578,AZ:0.1966,NM:0.2545,TX:0.1518.Andby2050,
eachstate’sscorewillreachCA:0.3481,AZ:0.3334,NM:0.3232,TX:0.3132.
Finally,wesetgoalsofthefourstatestoberaisingtheproportionofelectricgeneratedby
renewableenergysourceto34%by2025and59%by2050.Weusetheproportionofelectricgeneratedby
renewableenergysourcetoindicatetherenewableenergyusageanduseourmodeltopredictthe
proportion.Toachievesuchgoals,werecommendthefollowingthreeactionsforthefourstates:
integratingelectricmarket,establishingafundandapplytaxandsubsidypolicy.


## 第 2 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#78577 Page1 of 20
Contents
1 Introduction 1
1.1Background..................................................... 1
1.2OurWork...................................................... 1
1.3DetailedAssumptionsandNotations....................................... 1
1.3.1DetailAssumptions............................................ 1
1.3.2MathematicalNotations.......................................... 2
2 DataPreprocessing 2
2.1AddressingtheMissingValues.......................................... 2
2.2DataNormalization................................................ 3
3 EnergyProfile 3
3.1EnergyClassification................................................ 3
3.2EnergyIndices................................................... 4
3.3AnalysisofEnergyProfilesofFourStates.................................... 6
3.3.1EnergyStructure.............................................. 6
3.3.2UseofRenewableandCleanEnergy................................... 6
3.3.3GreenhouseGasEmissions........................................ 7
3.3.4InfluentialFactors............................................. 7
4 ModelforOverallScore 9
4.1OverviewoftheModel.............................................. 9
4.2UtilityFunction................................................... 10
4.3DeterminationofWeights............................................. 11
4.3.1SolvingforWeightsofSecondaryIndicesUsingPCA.......................... 11
4.3.2CombinationWeightingApproach.................................... 11
4.4DeterminationoftheBestProfile......................................... 12
5 PredictionofEnergyProfiles 13
5.1ModelofARIMA.................................................. 13
5.2SolutionandResultsofARIMA.......................................... 13
6 CooperationStrategiesofEnergyCompact 15
6.1FutureEnergyTargets............................................... 15
6.2ActionstoTake................................................... 16
6.2.1EstablishaFund.............................................. 16
6.2.2ElectricityMarketIntegration ....................................... 18
6.2.3EnactStrictLawsandRegulations.................................... 18
7 EvaluationofOurModel 18
7.1StrengthsofOurModel.............................................. 18
7.2WeaknessesofOurModel............................................. 19
References 19


## 第 3 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#78577 Pageof 20
Memo
To: GovernorsofCA, AZ,TX andNM
From: Team# 78577
Date:12February 2018
Subject: Usage ofCleaner,Renewable EnergySources
Purpose
We propose to summarize the state profiles of 2009 for you, and predict the
trend of energy usage in the absence of any policy changes, give my recom-
mended goalsand actions.
Summaryfor the Profile of 2009
CA (California) has the best energy profile of 0.1816 in 2009, followed by TX
(Texas) of 0.1743, NM (New Mexico) of 0.1209 and AZ (Arizona) of 0.1064. This
result is quite reasonable because California had the lowest emission of green-
house gases (per capita) and relatively high performance in use of renewable
energyin2009.
Prediction the Trend of EnergyUsage
If we ignore any policy changes, by 2025, the four states (AZ, CA, NM, TX)
willachieve anoverallscore of0.1966,0.2578,0.2545,0.1518.
By 2050, the four states (AZ, CA, NM, TX) will achieve an overall score of
0.3334, 0.3481, 0.3232, 0.3132, where CA always has the best score, and TX has
theminimal one.
Recommended Goals and Actions
Werecommendgoalsofthefour statestobe raisingtheproportionofelectric
generated by renewable energy source to 34% by 2025 and 59% by 2050. To
achievesuchgoals,werecommendthefollowingthreeactionsforthefourstates.
1. Integrating electricmarket;
2. Establishing afund.
The totalfund is208billion withthe share of: CA:89.8,AZ: 31.3,NM:30.6,
TX: 56.3.
3. Applyingtaxand subsidypolicies.


## 第 4 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#78577 Page1 of 20
1 Introduction
1.1 Background
Energy is an important part of people’s daily life, and the cornerstone of the
development of society. The formation of an industrial society brought fossil
fuelsintoourlives. However,withthedevelopmentofsociety,peoplehavebeen
gradually aware of the shortcomings of fossil fuels: high pollution and limited
quantity.People begantoseek tocreateaclean, renewable energystructure.
AlongtheU.S.borderwithMexico,fourstateshopetoformarealisticenergy
contract that focuses on cleaner, renewable energy. Weare asked to analyze the
compositionoftheenergystructureofthese states,and predictthetrendoftheir
development over the next 50 years. Wewill finally put forward some feasible
suggestionsforthecompact.
1.2 Our Work
Inthispaper,we breakour workinto sectionsasfollows.
1. Processthe primarydata (including missing value processing, data nor-
malization).
2. Establish thecomprehensive evaluationmodelofenergy(energyprofile),
andsolvefor the statewithbest energyprofile.
3. Establishthepredictionmodelofenergyprofile,andanalyzethechanging
trend ineachstate.
4. Set reasonabletargetsaccording toourmodel results, and providefeasible
suggestionsforthecompact.
1.3 Detailed Assumptions and Notations
1.3.1 DetailAssumptions
Inourmodel, we makethe following assumptions.
Weignoreany policy changes by eachgovernor’s office when predicting
• theenergyprofileofeach state, which hasbeenmentioned in the problem.
Weassumethattherelativeimportanceofvariousindicatorsdoesn’tchange
• overtime.


## 第 5 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#78577 Page2of 20
Each sector (transportation, commerce, etc.) is of the same importance to
• anenergytype,and isempoweredonlybytheamountofinformationcon-
tained. For example, the four sectors have the same realistic weight on
renewableenergy,andonlyconsider thenumberoffactorsinthe synthesis
process.
1.3.2 MathematicalNotations
Here arethe notationsand their meaningsin ourpaper:
Table1:MathematicalNotations
Notations MathematicalMeanings
S Overallscore ofenergyprofile
U Energyindex ofuse ofrenewableenergy
r
U Energyindex ofuse ofclean energy
c
GE Energyindex ofgreenhouse gasemissions
x Data oftheithindicator
i
u( ) Utility Function
i
· Proportionofconsumption
CA,CC ,CI ,CR
r r r r
ofrenewable energyinfour sectors
Proportionofconsumption
CA ,CC ,CI ,CR
c c c c
ofclean energy infour sectors
2 Data Preprocessing
The attached data file “ProblemCData.xlsx” provides us with 50 years (1960-
2009)ofdatain605variablesonenergyproductionandconsumptionalongwith
some demographic and economic information of the four states respectively.
Thisisahugeamountofdatawithlotsofredundantanduselessdata. Therefore,
we need to perform data preprocessing by cleaning, selecting and normalizing
thedata.
2.1 Addressing the Missing Values
There are lots of missing values in the data file, so we come up with the fol-
lowing methodstoaddressthis problem.


## 第 6 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#78577 Page3of 20
1. For some of the indicators (of some states), there are sometimes a small
number of values to be zero, which may result from statistical negligence.
In this case, we adopt cubic spline interpolation to fill in the missing val-
ues.
2. Data of some indicators were not collected in certain years (less than 25
years), which would lead to long lists of zeros. In this case, we fit the re-
maining data intoacurve andthus fillin themissingvalues.
3. For those indicators who have only 40 years (1970-2009) of data, we can
adoptthe same method mentioned in2.
4. For some of the indicators (of some states), most or all of the values are
zero. In this case, we have to refer to other data (e.g. data of other states of
the same indicator) and fill it with the help of the average of other highly
correlateddata.
Itisnoteworthythatnotallzerosarecausedbystatisticalnegligence. Someof
themmaybeduetotheabsenceofaccordingtechnologyorotherspecialreasons.
A typical example is “electricity produced from nuclear power by the electric power
sector”.
2.2 Data Normalization
Since we will use indicators with various units, we have to normalize all the
indicatorsandscaleallthevaluesintherange[0,1]. Formula(1)givesthegeneral
formofthe adoptednormalization.
x x
min
x = − , (1)
new
x max x min
−
where x and x arerespectivelythe maximum and minimum value ofthe
max min
indicatorsinthe same unit.
For most of the given indicators (e.g. consumption, production), the values
are proportional to the population or the area of the state. Therefore, when we
comparethestatesintermsofsuchindicators,weavoidtheinfluence ofpopula-
tionby dividing the variables by thepopulationofthe stateaccordingly.
3 Energy Profile
3.1 Energy Classification
To create an energy profile of each state, we categorize the energy into the
following groups:


## 第 7 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#78577 Page4of 20
Coal
•
Naturalgases
•
Petroleumproducts
•
Nuclearenergy
•
RenewableEnergy
•
Renewable energy here includes biomass energy, geothermal energy, Photo-
voltaicandsolarthermalenergy,hydroelectricityenergyandwind energy. Since
the reduction of greenhouse emissions is also crucial in determining the energy
structure, we will also consider clean energy,which is the aggregation ofrenew-
able energy,naturalgasesand nuclear energy.
3.2 Energy Indices
To demonstrate the overall performance of the use of energy of four states,
we adopt threeindices listed below.
Use of Renewable Energy
The use of renewable energy is one of the most important indices to illus-
trate the energy profile of each state. Thus, we create an energy index U, which
r
includesthe following aspects:
1. Totalproductionofrenewable energiespercapitaP
r
2. Proportionofrenewableenergyconsumptioninallenergyconsumptionin
transportationsector per capitaCA
r
3. Proportionofrenewableenergyconsumptioninallenergyconsumptionin
commercialsectorper capita CC
r
4. Proportionofrenewableenergyconsumptioninallenergyconsumptionin
industialsector percapita CI
r
5. Proportionofrenewableenergyconsumptioninallenergyconsumptionin
residentialsector percapitaCR
r
Totalproductionofrenewableenergypercapitacanreflecttheextenttowhich
renewableenergyisdeveloped. Since theenergystructureofthefoursectorsare
differentandchangesovertime,weshouldcalculatetheproportionofconsumed
renewable energyrespectively.


## 第 8 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#78577 Page5of 20
Use of CleanEnergy
Similartorenewableenergy,wecreateanenergyindexU toillustratetheuse
c
ofclean energy,which isdetermined by thefollowingindicators:
1. Totalproductionofcleanenergiesper capitaP
c
2. Proportionofcleanenergyconsumptioninallenergyconsumptionintrans-
portationsectorper capitaCA
c
3. Proportionofcleanenergyconsumptioninallenergyconsumptionincom-
mercialsectorper capita CC
c
4. Proportionofcleanenergyconsumptioninallenergyconsumptioninin-
dustialsector percapitaCI
c
5. Proportionofcleanenergyconsumptioninallenergyconsumptioninresi-
dentialsectorpercapitaCR
c
Greenhouse Gas Emissions
In the United States, most of the emissions of human-caused greenhouse
gases (GHG) come primarily from burning fossil fuels (coal, natural gas and
petroleum)forenergyuse. CarbonDioxideisthemaincomponentofgreenhouse
gases, so we use the emission of carbon dioxide to represent that of greenhouse
gases.
To analyze emissions across different fuels, we compare the amount of CO
2
emittedper unit ofenergyoutputusing the datainTable 2.[1]
Table2:CO EmissionRatioofDifferentFuels
2
Fuel CO EmissionRatio(Pound/MillionBtu)
2
Coal 214.3
Gasoline 157.2
Naturalgas 117.0
Therefore, we calculate the index of total greenhouse gas emissions GE as
the weighted sum of consumption of fossil fuels with CO emission ratios as
2
weights.


## 第 9 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#78577 Page6of 20
3.3 Analysis of Energy Profiles of Four States
3.3.1 EnergyStructure
To illustrate the energy profiles of the four states, we first need to observe
theirenergystructures.
In Figure 1, we present the consumption of five types of energy per capita
in the four states. This shows that energy consumption in both 1960 and 2009
comes mainly from non-renewable energy sources (coal, patroleum and natural
gas).
Figure1:EnergyConsumptionStructure
Figure 2 shows the production of five types of energy per capita. Wecan see
thatthelargedifferencesbetweenthestates: ArizonaandCalifornialacknatural
resources while New Mexico and Texasare rich in resources such as patroleum
and naturalgas.
Figure2:EnergyProductionStructure
3.3.2 Use of Renewable andCleanEnergy
Useofrenewableandcleanenergyisamaincomponentoftheenergyprofile.
Figure3illustratestheproportionofconsumptionofrenewableandcleanenergy


## 第 10 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#78577 Page7of 20
and theirchanging trendsover time.
From Figure 2, we find that California had the best performace in the twoin-
dicessince the1980s. The generaltrendofproportionofconsumed clean energy
had beendecreasing before1985and have beenslowly increasing sincethen.
Figure3:UseofRenewableandCleanEnergyFigure4:GreenhouseGasEmissionsPerCapita
3.3.3 Greenhouse GasEmissions
Anotherimportantfactorofthe energyprofile is greenhouse gasemissions.
Figure4illustratesthe emissions percapita and thechanging trendover time.
ArizonaandCaliforniahaveobviousadvantagesoverNewMexicoandTexas
inthisaspect. ThiscanbederivedfromFigure1,fortheproportionofconsumed
coal, patroleum and natural gases directly contribute to greenhouse gas emis-
sions. The general trend of greenhouse gas emissions has been decreasing since
theearly1980s.
3.3.4 InfluentialFactors
GeographyandClimate
Due to the unique geography of the four states, they have different levels of
richness inbothnon-renewable and renewable resources.[1]
Arizona has few fossil fuel resources and no significant natural gas reserves,
but it does have abundant solar and geothermal energy potential. Arizona also
hassomewindpotential,mainlyalongandjustnorthofthesteep-walledMogol-
lonRimthatcuts acrossthe centralpart ofthestate.
Californiahasanabundantsupplyofcrude oiland natrualgasbutlackscoal
reserves. It also leads the nation in electricity generation from solar,geothermal,
hydroelectricandbiomassresources.
NewMexicoisamongthetop10naturalgas-producingstates. Itsrichnessin
fossil fuels isaverage. New Mexico possesses substantialrenewable resources,


## 第 11 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#78577 Page8of 20
particularlyfromwindandsolar,butalsofromhydroelectric,biomass,andgeother-
malenergy.
Texas leads the nation in crude oil and natural gas reserves. It is rich in all
kindsofrenewable resources, especially wind energy,which accounts for nearly
allofthe electricitygenerated.
Thefourstatesareroughlyonthesamelatitudeandtheclimatethereismild.
Therefore, the per capita energy use in residential sector is relatively lower be-
cause there’slittle need forairconditioning or spaceheating.
Population
The four states have huge difference in population. Population of the four
statesis shown inFigure5.
Figure5:PopulationofFourStates
It can be seen that the population of California and Texas are much larger
thanthatofArizona and NewMexico.
Actually, California and Texasare the two most populated states in America
and they have the largest energy demand. The large populations of the states
maketheproductionoftherenewableandcleanenergypercapitalessoutstand-
ing, despite theirrichness innaturalresources.
Economyand Policy
California and Texashave two largesteconomyin USA.Therefore, theyhave
the ability to increase energy efficiency with the implementation of alternative
technologies. Arizona’sprimaryeconomicactivitiesarenotenergyintensive,the
state’s per capita energy consumption is among the lowest in the nation. New


## 第 12 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#78577 Page9of 20
Mexicohasrecognized aneconomicinterest inselling more electricity toother
states,particularly electricitygenerated fromitsrenewable resources.
All of the four states have regulated policies to increase the use ofrenewable
or clean energy and to reduce greenhouse gas emissions. This accounts for the
generaltrend illustrated inFigure3and 4since the early1980s.
4 Model for Overall Score
4.1 Overview of the Model
After selecting the energy indices, we then develop a model to characterize
how the energy profile of each of the four states has evolved from 1960 to 2009.
Figure6givesanintuitive representationofour model.
Figure6:OverviewoftheModel
Firstly,we use PCA (Principle Component Analysis) to calculate two energy
indices–U and U . WeadoptPCAtocompresstheprimarydataand determine
c r
their weights because the indicators (e.g. consumption proportion for different
sectors) are correlated, where AHP (Analytic Hierarchy Process) would lose ef-
fect.
During the procedure of weighted sum, we make use of Utility Functions,
whichwould helpdealwiththe problemoftoo large magnitude gap.
Afterthat,weadopttheCombinationWeightingApproachtogettheoverall
scoreS. Thedetailsoftheapproacheswillbediscussedinthefollowingsections.


## 第 13 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#78577 Page10of 20
4.2 Utility Function
Inourmodel,weareconfrontedwithproblemsoflargemagnitudeevenafter
normalization. In order not to omit influence of the indices with small magni-
tudes, we decide tomake use ofutilityfunctions.
Utility functions can be regarded as adjusters which tune the data values to
make thedata distributionmoreuniform.
Amongall formsofutilityfunctions, we choose theformasformula (2):
Generally, the region around the median of the data has the largest distribu-
tion density. As is shown in Figure 7, we effectively increase the distinction of
thedata by using utilityfunction.
Figure7:SketchMapofUtilityFunction
Substituting formula (3)(4) into formula (2), a = 0,b = 1 and k canbe
i i i


## 第 14 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#78577 Page11of 20
obtained withdata ofdifferent indices.
4.3 Determination of Weights
4.3.1 Solving forWeightsof SecondaryIndices UsingPCA
First,weprocessthesecondaryindicesofeachstateusingPCA.Weobtainthe
weights of secondary indices contributing to the first two principle components
asshown inTable3.
Table3:ResultsofPCA
Renewable CA CC CI CR P Cumulative
r r r r r
Comp.1 0.19347 -0.09019 0.11611 -0.16790 0.95538 0.83952
Comp.2 -0.21188 -0.24016 -0.93253 0.07815 0.14730 0.93164
Clean CA CC CI CR P Cumulative
c c c c c
Comp.1 -0.00036 -0.59869 -0.28644 -0.48698 -0.56777 0.93549
Comp.2 0.00229 0.80078 -0.22566 -0.37477 -0.40910 0.97887
Byusingthefirsttwoprinciplecomponents,wecangetacumulativepropor-
tionof0.93for cleanenergy,and 0.98forrenewableenergy.
4.3.2 Combination WeightingApproach
After determining the principle components for secondary indices, we cal-
culate the weights of 3 energy indices. Since we have to consider the correla-
tions between the indices and the realistic importance of them simultaneously,
we adopt the Combination Weighting Approach by combining AHP and PCA
together to get the weights and thus the overall score S for each state. The fo-
mula ofthisapproach isgivenby
whered isthefinalweightwegetfortheithindex,pisthenumberofweighting
i
methodsand mis the number ofindicators.
By calculation, we can get the weights using different weighting method as
shown in Table4. It’s also worth mentioning that, when processing AHP,we get
theconsistentindexCR = 0.033 < 0.1. SotheresultsofAHPpasstheconsistency
check.


## 第 15 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#78577 Page12of 20
To conclude, as is shown in Table 3, our criteria can be demonstrated as fol-
lows. We think that if a state has lower GE and higher U and U , then the state
r c
isbetterin use ofcleaner, renewable energy.
Andthenbyformula (2)(3)(4), wecanobtainthecoefficientsforutilityfunc-
tionsasshown inTable5.
Table4:WeightsofEnergyIndices Table5:CoefficientsforUtilityFunctions
Method U U GE Coefficient U U GE
r c r c
AHP 0.258 0.637 -0.105 a -0.115 -0.361 0
i
PCA 0.066 0.158 -0.776 b 0.074 -0.096 1
i
Combination 0.178 0.433 -0.389 k 1.431 0.782 0.821
i
4.4 Determination of the Best Profile
After determining the weights, we can get the energy indices and overall
scoresoffourstates. Theenergyindicesoffourstatesin2009areshowninFigure
8and the overallscoresoffour statesduring 50yearsare shownin Figure9.
Figure8:EnergyIndicesin2009 Figure9:OverallScores
From Figure 9, we know that CA (California) has the best energy profile in
2009, followed by TX (Texas), NM (New Mexico) and AZ (Arizona). This result
is quite reasonable because California had the lowest emission of greenhouse
gases(per capita)and relatively highperformance inuse ofrenewable energyin
2009.


## 第 16 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#78577 Page13of 20
5 Prediction of Energy Profiles
5.1 Model of ARIMA
ARIMA modelisawidely used time seriesanalysis method,which first put
forwardby Box and Jenkinsin 1970.[5]The basic approachesofARIMA are:
Firstly,smooththe originaltime serieswithdifferencemethod;
•
Secondly, determine the type of model, the order of model and undeter-
• mined parameters by analyzing the characteristics of ACF (Autocorrela-
tion Function) and PACF (Partial Autocorrelation Function) of stationary
sequence;
Thirdly,test the validityofthemodel;
•
Finally,analyze and predict the future timeseries.
•
ARIMA model can be known as ARIMA(p, q, d), where p is the autoregres-
sive order number and q is the sliding average order number.This model repre-
sents making differences on the non-stationary random sequence variable Y for
t
dtimes, and thenwe obtainthe stationaryseriesX.
t
5.2 Solution and Results of ARIMA
Formoreintuitive analysisofenergyindices and moreaccurate predictions,
we use ARIMAmodeltopredict each secondaryindex separately.
Inthispaper,we only pick one index, CA ofCalifornia, asanexample to
r
illustratein detail.
Tobegin with, by drawing a curve of the data series, we find that it isn’t a
stationary time series for it’s increasing. So we process once difference method
on the sequence. However,since p-value = 0.2607 > 0.05, we processdifference
on the sequence again. Then we get a p-value of 0.014 < 0.05, which means the
datapasses thetest.


## 第 17 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#78577 Page14of 20
We then plot the ACF and PACF graphs for this sequence to select the ap-
propriate p and q for the ARIMA(p, q, d) model. As is shown in Figure 10, the
autocorrelationvaluebasicallydoesnotexceedthe confidence intervalsafterthe
4-th order hysteresis. Although there exits a autocorrelation value that exceeds
the bounds, it may be caused by chance to exceed the 95% confidence intervals,
sowehavep = 4. Usingthesamemethod,accordingtoFigure11,wecanobtain
thatq= 4.
Figure10:AutocorrelationFunction Figure11:PartialAutocorrelationFunction
Throughtheaboveprocess,wehavedeterminedourmodelasARIMA(4,4,2).
And then by calculation, we can draw the prediction results as shown in Figure
12.
Figure12:PredictionofCA ofCalifornia
r
The parameters are shown in Table 6. Among them, σ2 = 1.439 10− 8, log-
likelihood=361.26, AIC=-704.52.These resultsshow the feasibility of×the model.


## 第 18 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#78577 Page15of 20
Table6:ResultsofParametersinARIMA
Parameter ϕ ϕ ϕ ϕ
1 2 3 4
Value 0.1779 0.2868 -0.0048 -0.1790
Parameter θ θ θ θ
1 2 3 4
Value -1.5161 0.1022 0.4157 0.0218
Afterwards,usingthemethodmentionedabove,wecanpredictthevaluesof
all secondary indices, and thus determine the energy indices and overall scores
ofthefourstates. OurpredictionofoverallscoreofeachstateisshowninFigure
13.
Figure13:PredictionofOverallScores
The overallscoresofthe fourstatesin 2025and 2050areshown in Table 7.
Table7:PredictionofOverallScoresin2025and2050
AZ CA NM TX
2025 0.1966 0.2578 0.2545 0.1518
2050 0.3334 0.3481 0.3232 0.3132
6 Cooperation Strategies of Energy Compact
6.1 Future Energy Targets
Whensettingtargetsforthecompact,wemainlyfocusontheincreaseinper-
formance ofuse ofrenewable energyU aftertheircombination.
r


## 第 19 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#78577 Page16of 20
Wehavealreadypredictedthechangeinenergyprofileinthefollowingyears.
Now, we are to aggregate the data of the four states together and predict its
changing trend as well. Wewill make use of the changing trend of U to set the
r
targets.
AsisshowninFigure14,wecanknowthatthepredictionvalueofU in2025
r
and 2050isrespectively 0.34and0.59.
Figure14:PredictionofOverallScores
In order to show the strength of cooperation, we set the target as 110% ofthe
predicted value. That is to say, the compact should reach the U score of 0.374
r
and 0.649in2025and 2050respectively.
6.2 Actions to Take
6.2.1 Establish aFund
The first action is to establish a fund. The fund will be used to invest com-
panies to build facilities relative to wind or solar energy. To achieve goals in
compact, the four states have to contribute a certain amount of money to the
fund.
Generally, the cooperation of the four states can create some extra profit. So
this approach can be understood as a problem of the distribution of profit in a
cooperation. Weuse the Shapley ValueRegression Model to determine the opti-
mized share ofthe funding fromeach state.
Shapley Value Regression Model
The Shapley value provides a priori evaluation of the position of each mem-
berinacooperativegame,basedonthecontributionthateachmembercanmake


## 第 20 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#78577 Page17of 20
tothe different coalitions.In thegame, some basic rulestoensure equity should
be followed:[8]
Efficiency: members should distribute the fullyield ofthegame.
•
Symmetry: twomemberswhohavethesamemarginalcontributiontoeach
• coalitionshould havethe samevalue.
Lawofaggregation: twoindependent games canbe combinedlinearly.
•
Nullmember property: members who contributenothing should getzero
• value.
In a cooperative game (N, v), for each member i N , the ideal profit of the
game is Φ(v). If the functions Φ( ) satisfy all the r∈ules mentioned above, the
i i
distributed profitofeachcan memb·er can be givenby formula (7) (8).
Share ofInvestment of EachState
Electric price and the proportion of RES are proportional relationship. Using
data of America from 2006 to 2014 in the paper, we estimate the rate of trans-
forming money into proportion of RES and get the result that 5.2 billion dollars
canimprove1% proportionofRES.[12]
The detailed informationofelectricity and itsprice is shownin Table 8.
Table8:ElectricityInformation
AZ CA NM TX
Electricity(Wind)(Btu) 288.3592 56996.98 15095.7 195454.8
Electricity(Solar)(Btu) 2.982 19.783 0.645 1.22
ElectricityPrice
50 40 35 30
(Wind) ($/MWh) (Solar)
ElectricityPrice
80 90 100 110
($/MWh)
Using the informationabove, we solveformula (7)(8) and getthe share and
theamount ofinvestment ofeachstate illustrated inTable 9.


## 第 21 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#78577 Page18of 20
Table9:ResultsofInvestment
AZ CA NM TX Total
Share (%) 0.150 0.431 0.147 0.27 1
Money (Billiondollars) 57.1 148.2 50.5 92.8 343.85
6.2.2 Electricity MarketIntegration
Asthecompactmainlyfocusesonrenewableandcleanenergy,wedon’tcon-
sider other kinds of energy. Renewable energy source has four major compo-
nents: biomass, hydropower, wind power and solar thermal. The four states
don’t have much differences in biomass and hydropower has already reached
its market saturation. However, the four states differ signifantly in wind power
and solar thermal for the reason of different altitude and geology. As a result,
the four states have different radiation intensity, wind speed and so on, which
meanstheyhavedifferentpotentialabilitywindandsolarenergy. Thus,weonly
payattentionto thecooperationonthe lasttwo typeofenergy.
After integration, states can buy energy from others with lower price while
stateswho provideenergyearnmoneywhen building moreplants.
6.2.3 Enact Strict Laws andRegulations
To increase the overall energy profile, we also suggest the compact to work
together to enact some strict laws and regulations. We can take the following
steps:
Carry out a certain degree of tax exemption on renewable energy power
• generation.
Developdifferentrenewableenergyprojectsaccordingtotheenergystruc-
• ture of states. For example, CA may focus on the construction and devel-
opmentofwind powerand hydroelectricpower.
Todrivetherapid developmentofrenewable energy,set up funds infour
• statesthataimtoselectrenewableenergyconstructiondemonstrationprojects.
7 Evaluation of Our Model
7.1 Strengths of Our Model
Based on the conditions of missing data of indicators, we take different
• measuresto maintainthe authenticityofthe data asmuch aspossible.


## 第 22 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#78577 Page19of 20
After a systematic consideration, we divide the indices into several cat-
• egories, and take PCA and combination weighting approach (AHP and
PCA)toobtainreasonable results.
Weuse ARIMA time seriesmodeltopredict. Comparedwith thetradi-
• tionalmethodoffittingprediction,themodelhasconsideredthedatachange
ofeach year,making itmorecredible.
Wemake adetailedanalysis when determining the goalsaswellas mea-
• sures.
Wehave splendid presentations ofour resultsthroughavariety ofcharts.
•
7.2 Weaknesses of Our Model
Wemaynotmakefulluseofallthedata. Weuseonly13indicatorstocalcu-
• latethe composite score, and some othersummaryindicatorsforanalysis.
The determinationofthe formofutility functionand thedetermination of
• pandqofthe ARIMAmodelmay be subjective.
References
[1] U.s. energyinformationadministration. .
https://www.eia.gov
[2] Omar Hafez and Kankar Bhattacharya. Optimal planning and design of a
renewable energy based supply system for microgrids. Renewable Energy,
45:7–15,2012.
[3] James Douglas Hamilton. Time series analysis, volume 2. Princeton univer-
sitypressPrinceton,1994.
[4] Andrew C Harvey and Andrew C Harvey. Time series models, volume 2.
HarvesterWheatsheaf NewYork,1993.
[5] Gareth Janacek. Timeseries analysis forecasting and control. Journal ofTime
SeriesAnalysis,31(4):303–303,2010.
[6] M. Kelly and M. C Thorne. An approach to multi-attribute utility analysis
underparametric uncertainty.Annals of Nuclear Energy,28(9):875–893,2001.
[7] Dawen Liang. Maximum likelihood estimator for variance is biased: Proof.
2012.
[8] TatianaNenova. The value of corporate voting rights and control: A cross-
countryanalysis. Journal of FinancialEconomics,68(3):325–351, 2003.


## 第 23 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#78577 Page20of 20
[9] Angel Nikolaev and Popi Konidari. Development and assessment of re-
newable energy policy scenarios by 2030 for bulgaria. Renewable Energy,
111:792–802,2017.
[10] Jyoti P Painuly. Barriers to renewable energy penetration; a framework for
analysis. Renewable energy,24(1):73–89,2001.
[11] YF Zhou and Fa-jie WU. Combination weighting approach in multiple at-
tribute decision making based on relative entropy. Operations research and
managementscience,5:009,2006.
[12] Tong Zhu. Comparison analysis on current energy transition in germany
and theunited states. International Petroleum Economics, 2016.

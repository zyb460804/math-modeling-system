# C80560-A New Keynesian Approach to Optimizing Energy Compact


## 第 1 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team ControlNumber
For officeuseonly For officeuseonly
80560
T1 F1
T2 F2
T3 ProblemChosen F3
T4 F4
C
2018
MCM/ICM
SummarySheet
Summary
A New Keynesian ApproachtoOptimizingEnergyCompact
In our paper, we construct an EROI evaluation system for the four states using data
scienceandsucceedin determiningoptimalgoals fortheinterstateenergycompact.
First, we operate on the data. Data are screened according to their integrity and
usefulness of the infomation. Then we select and merge different variables using Coin-
tegration and Multiple Dimensional Scaling(MDS) based on the independence and rep-
resentativeness of the attributes. For the reserved variables and statistics by year, we
use Mean Subtitution to conduct data imputation. Then, we classify the processed
database by usage, sources and sectors. Classification on the energy sources is
eventually made accordingtothecorresponding environmentalimpact.
Second, we construct a EROI evaluation system, which is an improvement of Re-
turn on Investment (ROI). We classify various kinds of energies into 10 distinct groups.
All variables of prices are adjusted in order to offset the influence by inflation and geo-
graphical differences. After that, we find that the external cost is related to the intensity
of pollution, so it is used to measure the influence on environment. Also, we take
sector influence and electric energy loss into consideration. Our data shows that
Californiahasthebest profilefor useof cleaner energysince1974.
Third, our predicting models feature both Mathematical and Economic models.
Since the data given are not stable in Time Series, we do not take ARMA or ARCH
model into consideration. A linear model is initially adopted to regress the data, but it
turns out to have limited accuracy and fails to fit short-term fluctuations or long-term
trends. As a result, we adopt a dynamic New Keynesian IS-LM model and include
forward-looking expectations in the model. We can therefore predict future energy
consumption and structure with better accuracy. What’s more, to simulate policy
effects, demand shocks and supply shocks are added to the enhanced model, so that
we areable toprovide governorswithquantitative predictionof policies.
Finally, sensitivity analysis is added to test and verify our models. The satisfying
results allow us to put models into real situations and to solve real problems. Wedeter-
mine the renewable energy usage targets that in 2025, California may reach 42% of
clean, renewable energy to the total consumption. Other states can reach 35%. And in
2050 All states may reach different from 38% to 51%. Four states’ government should
subsidize clean and renewable energy and impose pollution tax on others. Other kinds
ofdirect investment andlong-term policycan also beusedtomeettheenergygoals.
Keywords:New Keynesian; IS-LMModel; Linear Regression; TimeSeries; MDS


## 第 2 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#80560 Page1of24
Contents
1 Introduction 1
1.1 ProblemBackground. . . . .. . .. . . . . . . . . . . . .. . .. . . . . . . 1
1.2 Overview of OurWork. .. . . . . . . . . . . . .. . . . . . . . . . . . . .. 1
1.3 Assumptions.. . .. . . . . . . . . . . . .. . .. . . . . . . . . . . . .. . . 2
2 DataProcessing 2
2.1 DataScreening . . . .. . .. . . . . . . . . . . . .. . .. . . . . . . . . . .. 2
2.2 DataImputation . . . . . . .. .. . . . . . . . . . . . . .. .. . . . . . . . . 3
2.3 DataClassification .. . . . . . . . . . . . . .. .. . . . . . . . . . . . . .. 3
3 EnergyProfile 4
3.1 Overview Profileof theFour States. . . . . . . . . .. . .. . . . . . . . . . 4
3.2 Characterize theenergyprofile . .. . .. . . . . . . . . . . . .. . .. . . . 4
4 EROIEvaluation System 5
4.1 EROIDefinition . .. .. . . . . . . . . . .. . .. . . . . . . . . . . . .. . . 5
4.2 TheRevised EROIEvaluation System . . . . . . . . . .. .. . . . . . . . . 6
4.3 Resultsof EROIEvaluationSystem . .. .. . . . . . . . . . . . . .. .. . . 7
5 Predictive Modeling 9
5.1 Linear Regression Model . . . . . . .. . .. . . . . . . . . . . . .. . .. . . 9
5.2 DynamicNew Keynesian IS-LM Model . . . . . . . . . . . .. . .. . . . . 10
5.3 EnhancedNKIS-LMModel with Demandand SupplyShock . . . . .. . 12
5.4 ClimateChangeCompact inAction . . . . . . .. .. . . . . . . . . . . . . 16
6 SensitivityAnalysis 17
7 Strengthand Weakness 17
7.1 Weakness. . .. . .. . . . . . . . . . . . .. . .. . . . . . . . . . . . .. . . 18


## 第 3 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
8 Conclusions 18
9 Memo 21
Appendices 22
Team#80560 Page1of24
1 Introduction
1.1 Problem Background
Energy production lays a solid foundation for the development of the whole nation and
serves as the essential impetus for the function of the entire society. The utilization of
cleaner and green energy is a growing trend worldwide for purpose of the sustainable
development. There are masses of clean energy oriented contracts being signed all over
the world, while very few of those are carried out due largely part to their unrealistic and
far-fetched goals. Therefore, setting goals reasonable enough contributes a lot to the
optimalreconstruction ofthe energy structure regardingvarious countriesorstates.
The past years have witnessed unprecedented boom in the development of big
data. Data science has penetrated into every aspects of our life, and plays a significant
role in statistics, market intelligence, business analysis and so on. Moreover, data
science can be applied to offer a feasible solution and set a realistic goal and thus
facilitates the decision-making process. Therefore we give full play to the data science
inaddressingtheoptimalissue.
Now there are four states along the US border with Mexico, California (CA),
Arizona (AZ), New Mexico (NM), and Texas (TX) that wish to form a realistic and
practical new energy compact focused on increased usage of cleaner, renewable
energy sources. With 50 years of data in 605 variables on each of these four states’
energy production and con-sumption collected, we can perform data analysis and
modeling tofigureout a seriesof reasonable goalsfor theinterstateenergycompact.
1.2 Overview of Our Work
First,we find afewkeypointsin thisquestion:
Createanenergyprofilefor thefour statesrespectively.
Characterize theenergyprofilebasedon thetimeseriesmodel.
Develop an evaluation system tojudgethe level of the energyprofile.
How topredict theenergyprofileof thefourstates.
Determinefuturerenewable energyusage targetsand howtoachieve them.
Onthebasis ofabove discussion,to determinetheoptimal energygoals, we mayboil
down thetaskstothefollowing steps:


## 第 4 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
First, we do data screening according to the integrity and usefulness of the infor-
mation. For the retention of the dataset we use Cointegration and Multiple
Dimen-sionalScaling toperform dataimputation. And classifythedata.
Second, we use knowledge of finance to construct EROI evaluation system. And we
usethe EROIconcepttoevaluatethe energy profile evolved from1960–2009.


## 第 5 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#80560 Page2of24
Third, we initially adopt Linear Regression Model to predict the energy profile of
the four states in 2025 and 2050 while further use Dynamic New Keynesian IS-
LMModel toobtain morereliable projections.
Finally, we analyse different situation of the four states and accordingly propose
specificgoalsand actions.
1.3 Assumptions
The dataafter screeningand imputationarecorrectand robustfor furtheranalysis.
Natural resources in the four states are abundant and will not be exhausted
before2050.
All energy, no matter clean or not, are identical in total costs after 2009
( productioncost + possible environmentalcost).
Inflation (i.e. GDPdeflator) will not changeinfutureyears.
We mainly focus on the performance of macro-economy and energy structure,
in-cludingrenewable and cleanenergy.
2 Data Processing
2.1 Data Screening
Given that we have 50 years of data in 605 variables of the four states, the original
database is quite large. Therefore, we should do data screening according to the in-
tegrity and usefulness of the information.We first delete some variables manually, and
thenwe useCointegration andMDS tofurthernarrowdown thevariables.
Multiple DimensionalScaling
Multidimensional scaling (MDS) is a means of visualizing the level of similarity of
individualcases ofadataset.Itrefers toasetofrelated ordinationtechniques used


## 第 6 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#80560 Page3of24
in informationvisualization, inparticular todisplay theinformation containedin a
distancematrix.
Wethenutilize thismethodtofurthernarrow down thevariables.
2.2 Data Imputation
In statistics, missing data is quite common in the dataset and may cause certain bias
in the final conclusion. Therefore data imputation, which means replacing missing data
with substituted values, is of great necessity in eliminating such bias and obtaining
moreauthenticresults.
Through preliminary observation on the raw dataset, we discover that the statistics of
some variables remain zero for several years in a row. Some are missing data while under
some circumstances the true value is zero. Therefore, firstly we should distinguish the
abnormalstatistics from thedatabase andthen deal with themissing data.
By far there are several ways to do data imputation, including Listwise deletion,
Meansubstitution, Multiple Imputation andsoon. Herewe useMean substitution.
2.3 Data Classification
Weclassifytheenergyproductiondatabasebythree aspects– usage,sourceand
sector.Thespecific classification islisted asfollows.
Figure1: Energyproduction databaseclassification
Furtherwe makeaclassificationon differentkinds of energysourcesin termsof their
environmentalimpact:
Figure2:EnergySource Classification


## 第 7 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#80560 Page4of24
3 Energy Profile
3.1 Overview Profile of the Four States
Figure3: Overview Profileof theFour States
*Average price of fossil energy is important data because some states, such as Texas,
haveplenty of oil reserves. These states’ low price of fossil energy can’t reflect its advantage in
energy consumption. As long as we are learning about the energy consumption in various
states,theeffectofenergyexploitationshouldberemoved.
Figure4: Four statesenergyconsumptionbysector
3.2 Characterize the energy profile
Energy structure depends excessively on a state’s population, economy and industry. The table
belowbrieflysummarizesthedemographical,climaticandindustrialfeatureofthesefourstates:
Geographyplays animportant roleinthedistributionofenergyplantsacrossthefour states.
Due to similar geographical character, natural gas plants and petroleum plants locate sparsely
in their terrain. However, their difference outweighs similarities. While California and Texas
have various energy plants, such distributions in Arizona and New Mexico are relatively
monotonous. In addition, California is the only state to own geothermal plants. Coal power
plants, however, mainly locate in Arizona and Texas. While solar power are more abundant in
California and Ari-zona, Texas has more wind power plants. Finally, California and Texas have
thelargestnumberofhydroelectricpowerplants


## 第 8 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#80560 Page5of24
Figure5: populationdistribution
Figure6: geographydistribution
Figurefromhttps://www.eia.gov/state/maps.php
˘´
Energystructure dependsexcessively on a stateâAZs population, economy and industry.The table below briefly summarizes the
demographical,climaticandindustrialfeatureofthesefourstates:
4 EROI Evaluation System
4.1 EROI Definition
ReturnonInvestment(ROI),bydefinition,istheratiobetweenthenetprofitandcostofinvest-mentresultingfromaninvestmentofsome
resources,whichisusedtoevaluatetheefficiencyofaninvestmentortocomparetheefficienciesofseveraldifferentinvestments.
Wethencomeupwiththeideathatsimilarconceptcanbeintroducedtotheenergyproduc-tionfields.Afterfurtherresearch,we
discoverenergyreturnoninvestment(EROI),whichistheratiooftheamountofusableenergydeliveredfromaparticularenergyresource
totheamountofenergyusedtoobtainthatenergyresource.
ArithmeticallytheEROIcanbewrittenas:


## 第 9 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#80560 Page6of24
O l
WhereEi denotestheequivalentcaloricvalueofthetotalithenergyoutputandEi
denotestheequivalentcaloricvalueofthetotalithenergyinvestment.
Investment
We find that non-clean energy is more cost effective to produce while may
simultaneously generate huge amounts of environmental cost. By contrast, clean energy
can virtually do little damage to the environment while the production is more complex
andcancost alot regardingthe relevant researchand productionprocess. Therefore, we
should take both internal cost and external expenditure into consideration in order to
evaluate certain en-ergy comprehensively. The investment consists of two parts –
EnergyProductionInternalCost(EIC)andEnergyProductionExternalExpenditure(EEE).
Output
The net energy yield refers to the amount of energy that is gained from harvesting an en-
ergy source. This yield is the total amount of energy gained from harvesting the source
after deducting the amount of energy that was spent to harvest it. And here we take the
total EIC of all kinds of energy as the energy yields given that the two have positive
corre-lation.
4.2 The Revised EROI Evaluation System
DenotationandDefinition
Denotation Definition
i quality factor
EO theoutput energy
EI theinput energy
EIC energyproduction internalcost
EEE energyproductionexternal expenditure
PEE Percentageof totalenergyconsumedbyElectricpowerplant
I energyintensity
i Sectorinfluence rate
Table 1: DenotationandDefinition of theRevised EROI EvaluationSystem
EICrevision
1.ValueofUSdollaradjustment
Some parts of the energy investment can appear some statistics in the form of money rather
than caloric value. Therefore we need to find a conversion factor in order to measure such
monetary investment in the unit of BTU. Here we take energy intensity as the conversion
factor, which means that the energy costs per unit GDP. The relevant GDP statistics of the
fourstatescanbeobtained ontheofficialwebsitesandfurther weneedtotakeinflationfactor
into account. Theoretically, in order to eliminate the influence of inflation, we need to
accordinglyadjusttheGDPeachyearonthebasisoftheGDPinthefirstyear.
Althoughenergypriceshavebeenincreasinginthepast 50years, someoftheincrement
are not caused by the change of real price, but due to the depreciation of US dollar. In
ordertoremovethisinfluencingfactor,wedecidedtousethefollowingformula:
GDP(2005)
I= (3)
CurrentGDP
2.Regionaldifferenceadjustment


## 第 10 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#80560 Page7of24
Some states, such as Texas, are rich in fossil fuel reserves. These states’ low price of
petroleum products is partly because their easy access to plenty of oil. In order to ad-
dress the energy quality issue, many researchers have construct various index to add up
allkindsofenergy. Hereweadopttheearlistmeasurement:
α i=
Pi
(4)
P1
Where P1 denotes the national standard price of certain energy, while Pi denotes the
statepriceoftheithenergy.Theratioisthequalityfactorioftheithenergy.
EEECalculation
In economic terms, an externality is the cost or benefit that affects a party that does not
choosetoincurthatcostorbenefit.
Pollution is an essential part of negative externality. When consuming some kinds of en-
ergy that causes pollution, we do harm to the environment and this damage can be mea-
sured by currency. According to OECD(2005), EEA(2004) and Pew Research
Center(2009), we got the external cost of every kinds of energy. After changing unit and
exchange rate, as well as adjusting the number into dollars in 2005 just like EIC, we
computedthefollowingtable.
Figure7: Theexternal costof energy(dollar in 2005/million Bru)
SectorInfluenceRate
It’s quite obvious that pollution in residential area poses larger threat on environment
than that in industrial area. As a result, we set up an influence rate of different sectors to
balancetherealinfluenceofexternalcost.
Figure8: Theinfluence rateof every end-usesector
RevisedFormula
Based on the relevant revision stated above, we can obtain a new EROI calculaltion for-
mula:
P
4.3 Results of EROI Evaluation System
In the late 1970s, three states, except Arizona, had experienced great growths. After the peak from
1981 to 1982 was a long decline and it was not untill the new century, that all four states started
anotherincrement.However,thefinancialcrisisin20072008hadgreatimpactonthesituation.


## 第 11 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#80560 Page8of24
Figure9: Total EROIof four statesfrom1970 to2009
Figure10: Percentageof Using Clean andRenewable Energyin End-useSector
Thetotal EROI of four states has dropped significantly. Among these four states, California had
anobviousadvantageinEROI.
In end-use sectors, energy that is both clean and renewable only occupies a little part of total
consumption. In 2009, the figure was 3.5% in Arizona, 2% in California and only about 1% in other
two states. There had been nearly no consumption in all states before 1990, since clean energy,
suchasnuclearandhydraulicpower,canhardlybedirectlyusedbyend-usesectors.
Figure11: Percentage ofUsing Clean Energyin ElectricityPower Plant
However, the situation is different in electric power plant, where plenty of clean energies are
used.Totally,allfourstatesexperiencedlongandslowdecreasesinthe1970s,afterwhichtheyhad
experienced quite different situations. Since 1985, about 90% of energy sources of electricity
generation in California have been clean energy. Arizona also had a good performance, when
NuclearEnergyhasoccupied30-40%ofitselectricitygenerationsource.Inrecent20years,elec-tric
power plant in Texas had a stable energy consumption. Since 2005, usage of wind energy has
increasedgreatly.However,inNewMexico,cleanenergywasnotwidelyused.


## 第 12 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#80560 Page9of24
Figure12: Electricpower plant EROIof four statesfrom1970 to2009
The situation during the past 40 years is illustrated in the figure above. California had won
the highest EROI ever since 1974 as expected. According to the Total EROI in 2009, California
alsohadthebestprofileforuseofclean,renewableenergy.
Figure13: total EROIof Four statesin 2009
According to the total EROI, it can be clearly observed that California has the best profile,
followedbyTexas,ArizonaandNewMexico.
5 Predictive Modeling
Inthis section, we used various models to predict the futureof energy industry. Despite the fact
that we have data of various years, they are not technically Time Series. To be specific, many
factors do not pass ADF unit root test and, thus, traditional Time Series model such as ARMA
or GARCH(ARCH) model could not and should not be used in prediction. Wemainly developed
two models, one mathematically and one economically: linear regression model and New
KeynesianIS-LMmodel.
5.1 Linear Regression Model
This first model that come to our mind is the basic linear regression model. In this model, 43
Factors of different energy categories are used to perform the regression. We’ve listed some of
theresultsasfollows:
The graph shows that some factors are well fitted into regression, such as JFACB (Row1,
Col.2).Othersdonot andneglect somecurvesand fluctuations inshort termperiods,especially
factors like NGCBB (Row 2, Col. 5). Apart from that, many factors are co-integrated, which
meansthatitwillbearedundanttotakethemallintoconsideration.
LinearRegressionfailsformainlytworeasons:
First, despite the fact that long-term macro-economic performances often seem to have trends
tofollow, thesetrends are very likelytochangeduetopolicychanges andmacro-market dynam-ics.
Such factors are not included in a purely mathematics model(i.e.Linear Regression). Even if
polynomialalgorithmscanfitintohistoricaldata,itwillstillfacetheproblemofoverfittingand


## 第 13 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#80560 Page10of24


## 第 14 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#80560 Page11of24


## 第 15 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#80560 Page12of24
Theresultsoffourstatesareshowninthetable(billionBtu):
Energy California Arizona New Mexico Texas
2025 2050 2025 2050 2025 2050 2025 2050
Coal 36866.9 35683.5 16417.8 25531.1 2264.58 3528.00 49054.4 76271.9
Natural gas 2140457 3327307 152071.1 236390.8 240575 373975.3 2854761 4437663
Petroleum 5015969 7797268 768174.4 1194120 353683.6 549798.5 7751729 12049965
Solar 30205.5 46956.8 5396.95 8390.99 349.566 552.735 972.084 1517.60
Geothermal 2858.37 4453.88 437.865 680.018 629.529 988.719 2345.83 3656.23
Fuel ethanol 110091.4 171142.4 23910.05 37170.75 3770.696 5866.872 74755.37 116205.3
Wood and Waste 190232.2 295717.8 16613.63 25826.09 15323.07 23829.41 109979.4 170968.8
Hydroelectricity 289547.7 280278.1 89182.22 138641.7 3488.702 5431.955 14813.36 23032.46
Nuclear 464845.2 722602.1 406072.7 631221.7 nan nan 580634.3 902591.2
Wind 72724.7 113052.7 nan nan 19172.92 29813.04 194650 302556.1
Naninthetablearecausedbyinsufficientdata,sothatwecannotpredicttheirdevelopment.
Table 2: EnergyProfilePrediction oftheFour States
We’ve also visualized our findings in Figure 9-12. These figures shows the
energy consump-tion from 1970 to 2050, and the figure between 2009 to 2050
are predicted with New Keynesian IS-LM Model. The results show intuitively
but quantitatively that, without any inference of poli-cies, the economy tends to
use such energy that has a higher proportion before. In addition, those energy
with less prior usage slowly grow up, as to the effect of the expansion of
aggregated de-mand and supply. However, their percentage tends to drop and
graduallylosecompetitionwithenergieslikecoalsandpetroleum.
These findings are quite consistent with real world situation. Suppliers of coal
and petroleum tend to maximize their profit and expand their business, so they are
very likely to hinder new technology breakthrough, for fear of the shrinkage of their
own benefit. These phenomena slow the pace of renewable and clean energy
development and call for the inference of governmental policy to encourage and
promote the growth of green technology. In the next section, we’re going to
introduceanadaptedmodeltoanalyzeandpredicttheeffectofvariouspolicies.
5.3 Enhanced NK IS-LM Model with Demand and Supply Shock
Tobetterindicatetheeffectofpolicies,wethenintroducedthedemandand
supplyshocktoIS-LMmodel.Theenhancedmodeltakestheform:


## 第 16 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#80560 Page13of24
Figure15: Arizonaenergyprofileprediction Figure 16:Californiaenergyprofileprediction
Figure17: NewMexicoenergyprofilepredic-Figure18: Texasenergyprofilepredictiontion


## 第 17 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#80560 Page14of24
Theenhancedmodelprovidesuswithabetterwaytosimulatetheeffectofpolicies.Itinspiredustothinkquantitativelyandlogicallyon
thistopicandshedlightonthewaypoliciesworksothatwecouldcomeupwithbettersolutionstopromoterenewableenergies.
Wehaveconsideredvariouscompositionofpolicies.Herearesomeoftheresultswewouldliketosharewithgovernorsandpolicymakers.
1.DemandSidePolicies
Thefirstaspectofenergypolicyistoinsertdemandshocktothepublic.Thesepoliciesareintendedtoincreasethedemandofclean
energyanddecreasethatofuncleanenergy.Suchpoliciesinclude:
- Subsidiesforcleanenergyandextrataxesforuncleanenergy.
- Constructionofbetterfacilitiesandinfrastructuresforaccesstocleanenergy.
Figure19:
DemandShockPolicyonCaliforniaNaturalGasConsumptionfrom1970to2050
WhenweinsertademandshockonCalifornianaturalgasconsumptionin2009,theinstant
˘
effectissignificantâA¸Sconsumptionshootshighinthefirstyear.Itdecreasesalittlebitinthefollowingyear,andfluctuatesintwomore
years.Afterthat,theeffectofdemandshockdiesdown,andconsumptionstartstogrowatitspreviousrate.
2.SupplySidePolicies
Unlikedemandshock,wehavemathematicallytwowaystocontrolsupplyinIS-LMmodel.Thefirstonewouldbetoinsertasupply
shock,whichissimilartodemandside.AnothermethodwouldbetochangetheinterestrateandthustheROIratebycuttingcostfor
renewableenergyplants.Inrealsituations,governmentalpolicieshavelargereffectonsupplyratherthandemand,thusmakingsupply
sideveryimportant.Suchpoliciesinclude:
- Highertaxesonunrenewableenergysupplyandsubsidiesforrenewableenergy.
- Easieraccessandlowerinterestrateinrenewableenergyindustry,aslowerinterestratepromoteslargerinvestmentforinvestorsandallowsloanersto
fundtheirprogrameasier.
- Directgovernmentalinvestmentonrenewableenergyplants.
3.LongtermPolicyoutweighitsshortcounterpart
Politiciansarealwayslimitedtoestablishonlyshort-termpolicies.However,givingdemand


## 第 18 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#80560 Page15of24
Figure 20: Negative supply shock on Texas coalFigure 21: Effect of interest rate on Texas coal con-
consumptionfrom1970to2050sumptionfrom1970to2050
shockforlonger periods will lead toasignificant better outcomethan only giving demand shock
for one period. Intuitive as it may sound, it does have a quantitative support by using the en-
hancedmodel.
Figure22: Long-termandshort-termpolicyonCal-Figure23: totalconsumptionofthefourstatesfrom
iforniasolarconsumptionfrom1970to2050 2009to2050
In the case of California Solar Consumption. A 3-year demand shock and a 1-year demand
shock are simulated on 2009. In the successive year after 2009, two successive policies
increased the consumption. Despite a downward after each policy is implemented, the add-up
effect is way higher than only short-term policies. To our surprise, 3-year policies have a nearly
200% higher promotion in consumption of solar energy than that of 1-year policies! The result
showsthat apolicyinforcefortwomoreyearswillleadtonearlyhalf ofthebetterresults. Thus,
webelievethatlong-termpolicyoutweighitsshortcounterpart.
4.Cross-statecooperation


## 第 19 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#80560 Page16of24
Figure24: Predictionenergyproportionin 2025
Figure25: Predictionenergyproportionin 2050
So far, we have analyzed various energy policies and their effect under IS-LM Model, but
these policies are still limited within state. In order to have a knowledge for the state contract,
wedugdeeperintothecross-statecooperationforrenewableenergies.Suchpoliciesare:
-Extensionofenergytransmissionbetweenstates.
-Investmentoftechnology.
-Constructionofcrossboardernaturalgastube.
5.4 Climate Change Compact in Action
Basedonourmodels,localgovernmentsneedtoimplementmultipleactionsinordertoreach
ourgoals.Weconsiderfollowingactionsasnecessaryfordevelopmentofrenewableenergy.
WHEREAS,thereisconsensusamongstateleadersthatenergeticproblemisamongthe
mostsignificantproblemsfacingthefourstates;and
WHEREAS,collaborationofthefourstateswillleadtoabetterenergystructurewithless
pollutiontotheenvironmentandmoreefficientusageofenergy; and
WHEREAS,allpartiesrecognizethatcoordinatedandcollectiveactiononenergetic
problemwillbestservethecitizensoftheregion;
THEREFORE,EACHSTATESHALL:
Provide easy loans and low interest rates to investors in the field of renewable energy,
whilepromotingbanksandinstitutionsinvestonsuchprograms.
Governmental subsidies to renewable demanders and suppliers, with taxes to unrenew-
ableenergyusersandproducers.
Easy loan and low interest rate to investors at renewable technologies and plants.
Actionsacrosstheborder:
States with higher technological capabilities help other states build plants of high
efficiencyandlow environmentalcost.
Constructmoreenergypipelinesandtransmissioncablesacrossstates’border.


## 第 20 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#80560 Page17of24
Figure26: energypipelines and transmission cablessketchmap
6 Sensitivity Analysis
We have tested the max or min value of our IS-LM model, and the results are satisfying. Since
it’s the dynamic IS-LM model does not take natural resources and technological factors into
con-sideration,soitdoesnot always haveequilibrium.Most oftheparametershaveeconomical
meanings so that they are limited to a certain range. For example x is limited to [-1,1]. The
following graph is based on the sensitivity test of Arizona Natural Gas consumption, and the
resultsareshownasfollow:
Figure27: sensitivityanalysis
7 Strength and Weakness
subsectionStrength
Integrity. All the data in the given dataset have been screened and checked carefully, for
eithermissinginformationorincorrectinformation.
Fair evaluation system. Our evaluation criteria oriented from the return on earnings (ROI)
rate.Thus,ithasveryclearmeaningsonthecostandearningsofcertainenergy.
Mathematical and Economical Model: Our models and parameters have direct economic
meanings,whilesubjectingtomathematicslawsatthesametime.
Dynamic Models and Programing: sophisticated economical models and Time Series
pro-grammingisincludedastosimulatethegrowthofenergyconsumptionandprice.


## 第 21 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#80560 Page18of24
ScienceforPolicy.Wehaveaddedsupplyanddemandshocksinmodelsinordertosim-ulatetheeffectofpolicies.Thus,the
policymakerscanuseourmodelforquantitativeanalysisandclearlyobservemarketdynamics.
7.1 Weakness
SimplifyingAssumptions.Simplifiedassumptionsareadoptedforasolvablemodel,sotheresultmayslightlydigressfromthegroundtruth.
Lackofpossiblecost.Wedidnothavetimetotakeconstructioncostsofplantsintocon-siderationandnordidweaddintothe
modeltheconstraintsoftechnologyandnaturalresources.
Localmaximaorminima.Ourmodelhaveconsiderableamountofparameters.Althoughitfitsgoodtopredictthefuture,itis
inevitablethatlocalmaximaorminimaisreachedinpredictingsomefactors.
8 Conclusions
EnergyProfile
BasedonourenergyprofileandEROImodel,Californiahadboastedthebestprofileforuse
˘´
ofcleanandrenewableenergysince1974.Texasislistedthesecondin2009âAZsprofile.ByusingNKIS-LMmodels,wepredict
thatin2025,therankoffourstatesislikelytoremainthesameas2009,intheabsenceofanypolicychange.Furthermore,in
2050,Texasislikelytoloseitsleadingposition,plummetingtothefourth.California,aseveryonehasexpected,willstillbethe
beststateinoverallenergyuse.
Predictions&Goals
Ourmodelshavesettargetsforthefourstatesin2025and2050.Thesefiguresarelistedbelow,whichtakesintoconsiderationthe
situationduringthepastdecadesandcurrentpricefluctuations,thusdenotingthepercentageofcleanenergyconsumptionto
totalen-ergyconsumption.
WealsofitthetargetsintoourEROImodel,andcomputedtheTotalEROIin2025and2050asfollows:
IntuitionofmodelsforPoliticians
Asourmodelsaremostlybasedoneconomicmodels,ithasfurthereconomicmeaningsthatthefourstatesmighttakeintoconsiderationtomeettheirenergycompactgoals:
–Subsidiesforcleanandrenewableenergyandcollectpollutionfeeortaxfromun-cleanenergy.


## 第 22 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
–Easier accessandlower interestrateinrenewableenergyindustry, aslower interest
rate promotes larger investment for investors and allows loaners to fund their pro-
grameasier.
– Direct governmental investment on renewable energy plants, such as construction
ofbetterfacilitiesandinfrastructuresforaccesstocleanenergy.
–Longtermpolicyhasalargerimpactontheenergysituation.
What’smore,longtermpolicyhasalargerimpactontheenergysituation.


## 第 23 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
References
[1] YanHu,LianyongFeng, DongTian.(2011).Newapproachtoevaluatingenergyproduction
–EnergyReturnOnInvestment.Energy
[2] NewKeynesian;IS-LMModel; LinearRegression;TimeSeries;MDS
[3] Macroeconomics Mankiw 9th edition By N.Gregory Mankiw Macroeconomics (Ninth
Edition)(2015-06-06)
[4] C.Groth,LectureNotesinMacroeconomics,(Mimeo)2011
[5] University of Wyoming College of Business Department of Economics and Finance ECON
5110MacroeconomicsIILectureNote4,2014
[6] OECD,2005,EnvironmentallyHarmfulSubsidies:ChallengesforReform,Paris:OECD
[7] EuropeanEnvironmentAgency(EEA),2004,EnergySubsidiesintheEuropeanUnion:ABrief
Overview,Copenhagen:EEA
[8] ThePew Center onGlobal ClimateChallenge, 2009. Windand Solar Electricity: Challenge
andOpportunities.


## 第 24 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
9 Memo
Dear governors,
We are reaching out to you because we can offer you reasonable goals for the interstate
energy contract. And our definition of Energy Return on Investment is based on profit
maximization with both economic and ecologic benefits taken into consideration.
To begin with, we establish an energy profile for each of the four states and construct EROI
evaluation system to rate the energy profile. We can conclude that California has the best
profile, followed by Texas, Arizona and New Mexico in 2009.
Additionally, we adopt Dynamic New Keynesian IS-LM Model to predict the energy usage in
2025 and 2050. We determine the renewable energy usage targets that in 2025, California may
reach 42% of clean, renewable energy to the total consumption. Other states can reach 35%.
And in 2050 All states may reach different from 38% to 51%.
Last but not lease, we propose several realistic goals for the compact and feasible actions to
achieve them.
Goals
Governmental subsidies to renewable demanders and suppliers, with taxes to unrenew-
ableenergyusersandproducers.
loan and low interest rate to investors at renewable technologies and plants. Actions
acrosstheborder:
States with higher technological capabilities help other states build plants of high
efficiencyandlow environmentalcost.
Constructmoreenergypipelinesandtransmissioncablesacrossstates’border.
ClimateChangeCompactinAction
Work in close collaboration on construction of energy plants, including coal, natural gas,
all petroleum products, solar, geothermal, fuel ethanol, wood and waste, hydroelectricity,
nuclearandwindproduction.
Work in close collaboration on construction of infrastructures and energy transmission
system, including but not limited to underground pipelines, electric cables and energetic
productionmaterial.
Work in close collaboration on streamlining certification process across border and simpli-
fyingapprovalprocess,includinglandcertificate,operationcertificateandsafetychecks.
Use available fiscal and monetary policies, including providing reasonable subsidies to
re-newable demanders and suppliers in each state and levying taxes on unrenewable
energyusersandproducers.
Provide easy loans and low interest rates to investors in the field of renewable energy,
whilepromotingbanksandinstitutionsinvestonsuchprograms.
Wishourproposalcaninspireyouinpursuitofamoreenvironmentalfriendlysociety. Weare
lookingforwardtohearingfromyou.
Yourssincerely,
Ateamofmodelerswhoareenthusiasticaboutenvironmentalpreservation
2/12/2018


## 第 25 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Appendices
Hereareprogrammesweusedinourmodelasfollow.
calculationofEROIEvaluationSystemPythonsource:
’’’
ThisPythonfiledescribedourMajorModeltoestablishEnergyProfile
’’’
importnumpyasnp
importpandasaspd
importmatplotlib.pyplotasplt
####################LoadData####################
#totaldataset
data=pd.read_excel(’NewestData211.xlsx’,index_col=0)
#priceofenergy
p=pd.read_excel(’price_of_energy.xlsx’,index_col=0)
#priceofelectricity
pe=pd.read_excel(’price_of_electricity.xlsx’,index_col=0)
#outerelectricity
oe=pd.read_excel(’outer_electricity.xlsx’,index_col=0)
#outerenergy
o=pd.read_excel(’outer_energy.xlsx’,index_col=0)
#label
MSN=pd.read_excel(’new_label.xlsx’)
#TETCD
TETCD=pd.read_excel(’TETCD.xlsx’,index_col=0)
TETCD.index=pd.date_range(start=’1/1/1970’,end=’1/1/2009’,freq=’AS’)
#originalstate_state_
={
’AZ’:
pd.DataFrame(),’TX’:pd.Da
taFrame(),’NM’:pd.DataFra
me(),’CA’:pd.DataFrame()
}
state={
’AZ’:pd.DataFrame(columns=
MSN[’MSN’]),’TX’:pd.DataFrame(columns=
MSN[’MSN’]),’NM’:pd.DataFrame(columns=
MSN[’MSN’]),’CA’:pd.DataFrame(columns=
MSN[’MSN’])
}
for keyinstate_:one_state=
state_[key]
one_state=data[data[’StateCode’]==key].drop(’StateCode’,axis=1)foreach_MSNin
MSN[’MSN’]:
temp=one_state[one_state[’MSN’]==each_MSN]
state[key][each_MSN]=temp[’Data’]
state[key].index=pd.date_range(start=’1/1/1960’,end=’1/1/2009’,freq=’AS’)


## 第 26 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
####################MainFunction####################
defcoe(year,key,flag=True):
’’’
ThisFunctionReturnscostofunitenergyproduction(COE)
##Input##
Flag=True:with electricity;
=False:withoutelectricity;Year:any
datetime
key: statecode
’’’
#####################################DataPart#######################################
n=p.values.shape[0]#numberofenergym=
pe.shape[0]#nuberofelectricity
#nationaldata
avg_cost_us=TETCD.loc[year].values
#statedata
nominal_GDP=state[key].loc[year][’GDPRV’]real_GDP
=state[key].loc[year][’GDPRX’]pai=
nominal_GDP/real_GDP
avg_cost=state[key].loc[year][’TETCD’]
####################################EnergyPart######################################
# priceofenergy
price=[]
fortaginp.values.reshape(n,):
iftype(tag)isfloatortype(tag)isint:price.append(tag)
else:
price.append(float(state[key][tag].loc[year]))
price=(np.array(price)+o.values.reshape((n,)))/pai/avg_cost*avg_cost_us
# priceis(n,)
# consumptiondataofenergy
c_energy=[]
for each_MSNinnp.asarray(p.index):
c_energy.append(state[key].loc[year][each_MSN])
c_energy=np.asarray(c_energy)
#shapeis(n,)
##################################ElectricityPart####################################
# Priceofelectricity
price_e=[]
fortaginpe.values.reshape(m,):
if type(tag) is float or type(tag) is int:
price_e.append(tag)
else:
price_e.append(float(state[key][tag].loc[year]))
price_e=(np.asarray(price_e)+oe.values.reshape((m,)))/pai/avg_cost*avg_cost_us#shape=(m,)
# Consumptiondataofelectricity
c_electricity=[]
for each_MSNinnp.asarray(pe.index):
c_electricity.append(state[key].loc[year][each_MSN])


## 第 27 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
c_electricity=np.asarray(c_electricity)
#shape=(m,)
####################################ReturnPart######################################
#returncostofaverageenergycost_of_energy=
(np.dot(c_energy,price)
+flag*np.dot(c_electricity,price_e))/(np.sum(c_energy)+flag*np.sum(
#################UsingtheFunction###############
year=’2009-01-01’for
keyinstate:
print(key,"with:\t",coe(year,key,True))print
(key,"without:\t",coe(year,key,False))
c_electricity))
returncost_of_energy
calculationofweightbytheentropymethodmatlabsource:
function[s,w]=shang(x)
[n,m]=size(x);
[X,ps]=mapminmax(x’);
ps.ymin=0.002;-ps.ymax=0.996;
ps.yrange=ps.ymax-ps.ymin;
X=mapminmax(x’,ps);
X=X’;
fori=1:n
for j=1:mp(i,j)=X(i,j)/sum(X(:,j));
end
end
k=1/log(n);for
j=1:m
e(j)=-k*sum(p(:,j).*log(p(:,j)));
end
d=ones(1,m)-e;-
w=d./sum(d);

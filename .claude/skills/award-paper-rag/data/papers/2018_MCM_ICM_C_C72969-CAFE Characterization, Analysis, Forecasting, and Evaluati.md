# C72969-CAFE Characterization, Analysis, Forecasting, and Evaluation of Energy Profile


## 第 1 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
TeamControlNumber
Foroffice use only Foroffice use only
72969
T1 F1
T2 F2
T3 ProblemChosen F3
T4 C F4
2018
MathematicalContest in Modeling (MCM/ICM)Summary Sheet
CAFE: Characterization, Analysis, Forecasting, and
Evaluation of Energy Profile
Summary
As sustainability comes in the spotlight, renewable energy receives extensive study. One
fresh idea to it in U.S. is the Interstate Energy Compact, aiming at promoting collaboration
for energy use among states. In this paper,we formulate concrete objectives and actions on
theuse ofrenewable energyforsuch acompact amongCalifornia(CA), Arizona(AZ), New
Mexico(NM)and Texas(TX).
We first build CAFE, a novel framework for Characterization, Analysis, Forecast and
Evaluation on the energy profile (EP) of a state. Weconstitute EP with 20 items in a mul-
tifaceted manner selected and aggregated from the 605 variables in the provided data. We
utilize the Gaussian Process Regression (GPR) model to characterize the basic evolving
trends, strong fluctuations and random noise level of different EP time series in each state
from 1960 to 2009. Wecombine Gray Relational Analysis and Kendall Rank to measure
the similarity of EPs among states in value and tendency respectively, and use both Pear-
son Correlation Coefficient and Partial Relational Coefficient to unveil outer influential
factors on the similarity. Weconsider 7 criteria concerning renewable energy, endow them
with different importance by the Entropy WeightMethod, integrate them into an ultimate
scorebasedonTOPSISmethod,andfinallyjudgeCAhavingthe‘best’profile. Wepioneer-
ingly formulate an ARMA-GPR Hybrid model for EP prediction of 2025 and 2050, which
adaptively suits itself to short-term and long-term prediction. Wefurther propose a sliding
windowmechanismanda‘Look-Ahead’refinementapproachincorporatingmoreinforma-
tioninprediction.
Wethen determine goals and approaches for renewable energy usage in 2025 and 2050.
Wediscoverthepredominanceofrenewableenergyconsumption(RC)initsusage,andthus
modelthegoalsettingproblemasamulti-objectiveoptimizationoverRC.Resultsshowthat
RC targets for 2025/2050 are respectively CA: 988787/1227217, AZ: 148028/175154, NM:
30120/36359,TX:283871/371206(billionBtu). Wefurtherproposethreeactionstostimulate
RC in AZ, NM, and TX, and show that CA can export more renewable energy to help the
otherthree statesinenhancingRC.
Wefinally conductsensitivityanalysis, dissect prosandconsofourmodeland presenta
memo ofourworktothe stategovernors.
Keywords:CAFE;EnergyProfile;CorrelationAnalysis;ARMA-GPRModel;Multi-Objective


## 第 2 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！


## 第 3 页

Team#72969 Page0of22
精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Contents
1 Introduction 1
2 Assumptions 2
3 AbbreviationandDefinitions 3
4 CAFE:Characterization, Analysis, Forecasting, andEvaluation ofEnergyProfile 3
4.1 EnergyProfileFormulation ........................... . . 3
4.2 EnergyProfileCharacterizationandAnalysis ........... ...... . . 5
4.2.1 GPR model: EvolutionofEnergyProfile . . . . . . . . . . . . . . . . . . 5
4.2.2 SimilarityAnalysis ofEnergy Profile . . . . . . . . . . . . . . . . . .. . 8
4.3 InfluentialFactorsofSimilarities...................................................................................10
4.4 EnergyProfileEvaluation...............................................................................................11
4.5 EnergyProfilePrediction................................................................................................12
5 Targetsand Actions forInterstate EnergyCompact 14
5.1 Targets: TotalRenewable ConsumptionBased Optimization....................................15
5.2 Actions: MotivatingRenewable EnergyUse inNM, TX,and AZ.............................17
6 SensitivityAnalysis 19
7 StrengthsandWeaknesses 20
7.1 Strengths............................................................................................................................20
7.2 Weaknesses........................................................................................................................20
8 Conclusion 20


## 第 4 页

Team#72969 Page1of22
1 Introduction
Withthe mounting heterogeneityof energyinfrastructures and demands in different re-
gions, centralized regulation ofenergycan no longermeet the needs for economic develop-
ment in every state in U.S. Toconfront this, two well-known interstate compacts: Western
InterstateEnergyCompact(1970)andSouthStatesEnergyCompacts(1978),wereproposed
tomake forstate economicenhancement inadecentralized and cooperative manner[1].
In 21st century, as sustainability becomes under great concern, the same issue of decen-
tralization falls upon the renewable energy management. Currently, the state governors of
California, Arizona, New Mexico, and Texas are planning to formulate a renewable energy
interstate compact. Specifically, theyneed
anenergyprofile1for statestocharacterize andevaluatetheir renewable energyuse,
•
and make predictionsforit in2025and 2050;
alistofgoalswritteninthecompactforrenewableenergyusagein2025and2050,and
•
at least threeactionstoachieve thesegoals.
A slew of prior arts have shed light on the energy prediction: Cammarano et. al [3]
proposed Pro-Energy, a prediction model of future available energy for wireless sensor net-
works, Virote and Neves-Sirva [4] built an energy consumption model based on stochastic
Markov models to forecast energy saving. However, above works zoomed in on prediction
within days, far less than intervals of years as the compact requires. Moreover, no prior
works have ever raised any quantified goal or action for renewable energy in an interstate
energycompact.
In this work, we propose a novel framework, named CAFE (Characterization, Analysis,
Forecasting, and Evaluation of Energy Profile), to fill in the gap above. The framework of
CAFEis shownin Figure1.
Figure1:FrameworkofCAFE(Characterization, Analysis, Forecasting, and Evaluationof
EnergyProfile)
CAFEframeworkinFig. 1canbe summarized as thefollowing steps:
1Theenergyprofileprimarilyconsistsofenergyproduction,consumption,import,andexports[2].
Aggregate
Select
精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Given
Data Characterizationof Analysisof Evaluationof Forecastingof
Target
HistoricalEvolution Similarity EnergyProfile EnergyProfile and
GaussianProcess GrayRelational EntropyWeight Time- Sliding Action
Regression Analysis Method DecayingWindow
Weight
PearsonCorrelation
Energy ErrorAnalysis Analysis TOPSIS Auto-Regressive&
Profile MovingAverage
PartialCorrelation
Latitudinal
Analysis
Refinement
CAFE
InfluentialFactor
GaussianProcess
FRAMEWORK SimilarityMetrics Regression


## 第 5 页

Team#72969 Page2of22
精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Characterization: We create an energy profile for each state as an integration of 20
•
typicalitems,andbuildGaussianProcessRegression(GPR)modeltoshowtheevolution
ofenergyprofile.
Analysis: utilize Correlation Analysis to identify the similarities of energy profile
•
among stateswiththepotentialcausesincluding geography, climate, industry, etc.
Evaluation: We apply Technique for Order of Preference by Similarity to Ideal Solution
•
(TOPSIS)method toforman integratedcriterionbased onsevenrefined criteria.
Forecast: We novelly propose an ARMA-GPR model which adaptively suits well in
•
both short-term and long-term energy profile prediction. This model not only inte-
gratesGPRandARMAbyallocatingatime-decayingweight,butalsoincorporatesthe
similarity amongstates.
TargetsandActions: Weutilizemulti-objectiveprogrammingtodeterminequantified
•
targets for renewable energy consumption in four states in 2025 and 2050, and pro-
vide actions stimulating the renewable energy use in AZ, NM, and TX based on our
prediction.
2 Assumptions
First and foremost,we makesome basicassumptions and explaintheir rationales.
Assumption 1.Each state attaches greatimportance to renewable energyusage and sets ashared
goal to enhancethe managementand developmentof renewable energy.
This assumptionis thepremise ofour worksince onlywhen eachstate endeavorsto
increase the usage ofrenewable energy, ourproposed targetsand actions will makesense.
Assumption 2.There willbe nogreat technology revolution bringing revolutionary alternative
renewable energy.
There is nosignfor the emergence ofsome new and revolutionary alternativeenergyup
tonow, so this assumptioncan helptoeliminate the effectsofthe small probabilityevent.
Assumption3. Nodestructivecatastrophe(suchasgreatearthquake)andnohuman-madedisasters
(suchas war)will happen by2050.
Thesekindsofdisastershappenedrarelyinthehistoryrecord,soweneglecttheireffects
inourmodel.
Assumption 4.The provided data is realisticand accurate to acertain degree.
Despitetheincompletenessofthedataandsometoleranterrorinstatistics,wemakethis
assumptiontoguaranteeone validsolution.


## 第 6 页

Team#72969 Page3of22
精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Table 1:AbbreviationofRelevant Terms
Abbreviation FullName
RC RenewableConsumption
UC UnrenewableConsumption
RP RenewableProduction
UP Unrenewable Production
RI RenewableImport
RE RenewableExport
RED RenewableExpenditure
UED UnrenewableExpenditure
CPC ConsumptionPerCapita
EPC ExpenditurePerCapita
RPES Renewable ProductionEntropy bySource
UPES Unrenewable ProductionEntropy bySource
RCES Renewable ConsumptionEntropy bySource
UCES Unrenewable ProductionEntropy bySource
SRP Share ofRenewableProduction
SRC ShareofRenewable Consumption
RCPR Renewable Consumption-ProductionRatio
TCPR TotalConsumption-ProductionRatio
RCEES Renewable ConsumptionEntropy by End-use Sector
UCEES Unrenewable ConsumptionEntropyby End-useSector
3 Abbreviation and Definitions
Forcompactness, wedefineaseriesofabbreviationsforsomenotionsconcerningenergy
profilein Table1.
4 CAFE: Characterization, Analysis, Forecasting, and Evalu-
ation of Energy Profile
Inthissection, we firstlycreatetheenergyprofilebased onprovideddata. Thenwepro-
poseanovelmodel: CAFE,tocomprehensivelycharacterize,analyze,forecast,andevaluate
the energy profiles of CA, AZ, NM, and TX, based on the provided data set comprised of
605variables from1960to 2009[5].
4.1 Energy Profile Formulation
First of all, we formulate an energy profile for each state. The energy profile should
present a panoramic view of energy use. We macroscopically divide energy into renewable
(electricity, ethanol fuel, nuclear fuel, wood etc.) and unrenewable (oil/gasoline/petroleum,
coal, naturalgas)ones. We extractitems reflectingthe globalinformationabout different


## 第 7 页

Team#72969 Page4of22
aspectsofenergyinastate,mainlyintermsofimport,export,production,consumption,and
expenditure. Specifically, we select the following items which possess the global property:
RC, UC,RP,UP,RI,RE, RED, UED, CPC, EPC.
Unrenewable Renewable
Entropy
RenewableImport
Volume
UnrenewableProduction Ratio
RenewableProduction
VolumeperCapita
UnrenewableProduction
RenewableProduction
Entropy(Source)
Entropy(Source)
ShareofRenewable
Production
RenewableExport
UnrenewableConsumption
RenewableConsumption
UnrenewableExpenditure
RenewableExpenditure
UnrenewableConsumption RenewableConsumption
Entropy(Source) Entropy(Source)
UnrenewableConsumption RenewableConsumption
Entropy(End-UseSector) Entropy(End-UseSector)
ShareofRenewable
Consumption
Energy Profile
ConsumptionperCapita ExpenditureperCapita
Figure2:The EnergyProfileofaState
Toexplore the underneath information within these items, we make some aggregations
toformnewitemslistedinTable2. Inside,RPES/UPES/RCES/UCES(RPESasanepitome)
characterizesenergyusagedistributionoverdifferentkindsofsourceswhileRCEES/UCEES
(RCEES as an epitome) shows that over different sectors, serving as a supplement to items
withtotalityproperty;SRP/SRCrepresentsthepopularityofrenewableenergyuse;RCPR/
TCPR evinces the balance of energy use in a state. All these aggregated items enrich our
considerationin energyprofilecharacterization.
Table 2:AggregatedItemsinEnergyProfile
Item Definition
Σ
RPES/RCEES p log(1/p)3
j j j
SRP RP/(RP+UP)
SRC RC/(RC+UC)
RCPR RC/RP
TCPR (RC+UC)/(RP+UP)
3pj isthecorrespondingportionofj-th(un)renewableenergyinsources/sectors.
Supply
RenewableProduction/
RenewableConsumption
Renewable
Supply
Usage
TotalProduction/
TotalConsumption
Renewable
Unrenewable
Supply
Usage
Usage
精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！


## 第 8 页

Team#72969 Page5of22
Then combining the aggregated items with selected original items, we propose a tax-
onomy of items in energy profile as Figure 2, to help readers understand the relationship
among extracted items. In Figure 2, we group these items into four sub-classes based on
whether the energy is renewable and supply or usage of the energy.Moreover, these items
can be classified into four categories with different physical dimensions: entropy, volume,
ratio,andvolumepercapita. Itemsconcerningvolumeshowtheconcretevaluesofdifferent
energy aspects, while those in the relative dimension present the relationship between dif-
ferent aspects of energy.By this classification, we clarify the relationship of items in energy
profilein alogicaland hierarchicalway.
4.2 Energy Profile Characterization and Analysis
4.2.1 GPRmodel: Evolution ofEnergy Profile
Tohelp us understand the evolving pattern of the energy profile, we probe into a gen-
erative model to characterize the historical evolution. Wefirst make an observation on the
given data to form an intuitive understanding of the longitudinal data. Weselect four typi-
cal time series among extracted items, which present different shapes and trends, asshown
in Fig. 3. Specifically, renewable expenditure of Arizona (Fig. 3(a)) generally presents an
ascending trend with tiny fluctuations; renewable export of Arizona (Fig. 3(b)) has a sud-
denincreasewhilerenewableconsumptionentropybysource(Fig.3(c))appearstofluctuate
nearacertainvalue.
Based on the observations, we summarize the following challenges in characterization
ofthese time series:
• The fitting modelshould characterize the basic evolving trend oftimeseries;
• The strongfluctuationsofitemvaluesrequiresa modeltocapture theinstability;
• The model should accommodate the randomnoise existingintimeseries.
In view of these challenges, we adopt the Gaussian Process Regression (GPR), an non-
parametric probabilistic model, to fit the time series. The model of GPR can be generalized
asfollows. Assume thatnoisy data
y(x)=f(x)+s(x) (1)
8000 1400 0.75
7000 1200 0.7
0.65
6000 1000 0.6 5000
800 0.55
4000
0.5
600
3000 0.45
2000 400 0.4
1000 200 0.35
0 1960 1970 1980 1990 2000 2010 0 1960 1970 1980 1990 2000 2010 0. 1 3 960 1970 1980 1990 2000 2010
Time Time Time
(a) REDofArizona. (b) REofArizona. (c) RCESofArizona.
Figure 3:Threetypicaltime seriesoflongitudinalenergyprofiledata.
erutidnepxEelbaweneR tropxEelbaweneR
ecruoSybyportnEnoitpmusnoCelbaweneR
精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！


## 第 9 页

Team#72969 Page6of22
精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
GPR modelmakesaprobabilisticpredictionofoutputswithconfidence intervalsincon-
sideration of the stochastic errors. Furthermore, GPR renders higher correlation for tempo-
rally closer values, coinciding with the fact that closer information is of greater significance
inpredictionofenergyprofile.
Byadopting GPR, we fit the time seriesin Figure3as Figure4.
SinceGPRdoesnotoutputadeterministicvalue,weadditionallyshowthe95%-confident
intervals of each output. The gap surrounded by the upper and lower confident lines is
called confidence interval. As we can see, for RED of Arizona with a consistent increasing
trend, the confident interval is fairly small, showing the high stability and predicting reli-
ability of its evolution. By contrast, for RCES of Arizona with the greatest fluctuation, the


## 第 10 页

Team#72969 Page7of22
8000 1600 1.1
95%confidenceintervals 95%confidenceintervals 95%confidenceintervals
7000 historicaldata 1400 historicaldata 1 historicaldata
regressioncurve regressioncurve regressioncurve
6000 1200 0.9
5000 1000 0.8
800 0.7
4000
600
0.6
3000
400
0.5
2000 200
0.4
1000 0
0.3
0 -200
1960 1970 1980 1990 2000 2010 1960 1970 1980 1990 2000 2010 1960 1970 1980 1990 2000 2010
Time Time Time
(a)REDofArizona (b)REofArizona (c)RCESofArizona
Figure4:GPR curve ofthreetypicaltime series
confident intervalis large,whichindicates thatthe evolutionofrenewable expenditureis of
greatrandomness, lowpredictability, and highsensitivity to outer influential factors.
Wefurther apply our model into the remaining energy profile time series and present
theregressionparametersofAZin Table3and the corresponding regressioncurve inFig. 5
(the placing order is the same as Table3). As we can see, β reflects the general trend of the
evolution, α represents the temporal fluctuation of measurements while σ2 shows thenoise
error. Items (RC, UC, etc.) have α σ2, which means that fluctuation takes the predominant
partwhilerandomnoisecanbeneglected;Forthosewhereαisclosetoσ2 (UCES,SRC,etc.),
it isnotreasonable toomit the impact ofrandomnoises.
Table3: GPR regression results for energy profiles of Arizona (1960-2009) (The arrowdirec-
tionsrepresentthebasicevolvingtrendswhileLandSistheabbreviationoflargeandsmall
respectively)
98
980
Error Analysis: Table 3 also shows the Mean Absolute Percent Error (MAPE) between
regressionvaluesandground-truthvalues. ThelowMAPEscorroboratetheregressionpre-
cision ofGPR modelinfitting energyprofile timeseries.
erutidnepxEelbaweneR
tropxEelbaweneR
ecruoSybyportnEnoitpmusnoCelbaweneR
精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
RC UC RP UP RI RE RED UED CPC EPC
β 90679 782873 88454 298941 124 297 2657 3400 0.11 1328
Trend ↑ ↑ ↑ ↑ ↑ ↑ ↑ ↑ → ↑
α 10164 1.89 10161 3.33 190 82 52 4.8 5205
Fluctuation L S L S S S S S L S
σ2 0.13 0.03 0.13 0.02 0.06 0.05 0.02 0.06 0.22 0.09
Noise L S L S S S S S L S
MAPE 0.05 0.02 0.05 0.63 0.23 0.35 0.17 0.08 0.01 0.02
RPES UPES RCES UCES RCEES UCEES SRP SRC RCPR TCPR
β 0.56 -0.23 0.56 2.40 -0.42 -0.70 -0.98 0.32 1.60 2.11
Trend ↑ ↓ → ↑ ↓ ↓ ↓ ↑ ↑ ↓
α 2234 0.17 412 710 458 1290 0.01 0.04 231
Fluctuation L S L L L L S S L L
σ2 0.34 0.07 0.28 0.31 0.02 0.34 0.01 0.11 0.31 0.01
Noise L S L L S L S S L S
MAPE 0.02 0.25 0.04 0.01 0.07 0.05 0.01 0.08 0.01 0.01


## 第 11 页

Team#72969 Page8of22
精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Figure5:EvolutionofEnergyProfile forAZ (the placing orderisthe same asTable 3)
4.2.2 Similarity Analysis of EnergyProfile
We take a step further to study the similarity of energy profile evolution among four
states. Shown in Figure 4, the temporal fluctuation entangles accurate analysis of the re-
lationship among four states over each item, due to the uncertain time-variation of each
timeseriesand ourincomplete knowledgeofotherpotentialinfluentialfactors. Forsuchan
unclear situation, we adopt the Gray Relational Analysis (GRA) to unveil the relationship
among energy profile in four states. GRA performs reliably under systems with informa-
tion incompleteness and uncertainty, and with complicated multivariate interrelationships
[6, 7], by pursuing an appropriate result acceptable in real cases instead of persisting in an
optimum[8].
We conduct our GRA-based analysis as follows: For item e, suppose we consider the
values of it for T years, then we can obtain the time series y = (y(1), y(2), ..., y(T )) for
i i i i
state i. Then for two states i and j, we define ξ , which represents the relationship between
ij
comparability vector y and reference vector y.Specifically,
i j


## 第 12 页

Team#72969 Page9of22
精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
− | |
Thenwe canobtainthe integrated KRCC denotedasIKRCC in the same way.
ij
(a)GRC (b)KRCC
Figure6:Heat mapfor GRC and KRCC
4.3 Influential Factors of Similarities
To understand the profile similarities and differences much in depth, we then explore
the impacts of other possible influential factors including geography, climate, industry and
population. Note that geography and climate can be viewed as constants while industry
and population are evolving temporally. Therefore, for a constant factor G we use Absolute
Mean Error between twostatesi and j,denoted as


## 第 13 页

Team#72969 Page10of22
精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
To study the influential factors, our empirical intuition is: if two states with a similar
factor(likegeography)sharethesimilar energyprofile,thenwe treatthisfactorisrelatedto
theinterstatesimilarityofenergyprofile. InFigure7,weplotthefactorsimilarityv.s. IGRC
for 2C2 = 12 state pairs. As we can see, the scattered points appear to have a consistent
4
trend,which indicatesthatthe factor similarityis relatedtoIGRC.
Then we probe into the influential factors for IKRCC. We adopt Pearson Correlation
Coefficient (PCC) and Partial Relational Coefficient (PRC) to study the correlation. The ad-
vantageofPRCoverPCCisthatPRCtakestheinterdependenceamongdifferentinfluential
(a)Area (b)Temperature
(c)Population (d)GDP
Figure7:FactorSimilarityv.s. IGRC


## 第 14 页

Team#72969 Page11of22
精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
factors into considerations and capture the correlation excluding the impact from otherfac-
tors. Table4 shows the PCC and PRC between influential factors and IKRCC: PCC shows
thatallofthepotentialcriteriahaveanegativecorrelationwithinthetwostatesinvolved.
Table 4:PearsonCorrelation Coefficient and PartialRelationalCoefficient.
Area WaterPercentage Altitude Rainfall
PCC -0.45 -0.26 -0.39 -0.44
PRC -0.57 -0.14 0.27 0.34
Temperature Population GDP GDP Per Capita
PCC -0.61 -0.28 -0.21 -0.42
PRC -0.71 -0.72 0.80 -0.37
4.4 Energy Profile Evaluation
Following the energy profile characterization, we will analyze which state turns out to
have the best profile in terms of renewable energy usage. A good profile for renewable en-
ergyshouldbeintegratedlyjudgedandultimatelyindicateapositivetendencyforitsgreater
influence in society. In our work, we designate seven criteria based on different angles to
measure how good a profile is in regards to renewable energy use, list in detail in Table 5.
Newcriteriainclude: RCPC(RenewableConsumptionPerCapita),IRRC(IncreasingRateof
Renewable Consumption), and REGR (Renewable Expenditure-GDP Ratio). The proposed
criteria synthetizes popularity, diversity, and economic potentials, ensuring higher social
impact ofrenewable energyunder abetterenergyprofile forrenewable energyuse.
Table 5:Criteria forEvaluating EnergyProfile
Abbreviation SignificancetowardsRE Entropyweight
RCES ConsumptionVariety 0.183
RCEES ConsumptionVariety 0.191
RCPR EconomicBalance 0.105
SRC ConsumptionProportion 0.120
RCPC IndividualConsumption 0.189
IRRC ConsumptionTrend 0.107
REGR ExpenditureProportion 0.101
Judging the best profile requires reasonably melting the above seven criteria into a syn-
theticone. Here we againadoptEntropy WeightMethod toallocateweightsto eachcriterion.
In view of our objective to selecting the best profile, we utilize the TOPSIS2method, whose
core is to directly identify the best profile by minimizing the distance to the ‘virtual opti-
mum’ where all criteria reach the optimum. Toimplement the method, we first normalize
eachcriterionvalue toeliminate the problemofdifferent scales. Use Z todenotethe value
ij
ofthej-th criterionforstate i and itscorresponding normalized value Z0 can be calculated
ij
2TOPSIS:TechniqueforOrderPreferencebySimilaritytoanIdealSolution


## 第 15 页

Team#72969 Page12of22
精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
The evaluation results are presented in Table 6, whose first seven columns are the nor-
malized criteria,andthe last column isthe score foreachstate. Aswe can see, CA ranksthe
first in our final criterion, with TX following behind, while AZ ranks the third and NM isat
the bottom. This matches our sense that CA and TX are more developed, and they should
gofurtherin renewable energyuse compared with lessdevelopedAZ andNM.
Table 6:EvaluationResultsofRenewable EnergyUsage forFour States
RCES RCEES RCPR SRC RCPC IRRC REGR Score
AZ 0.16 0 0.95 0.69 0.16 0 1 0.434
CA 1 1 0.56 1 0 1 0 0.628
NM 0.32 0.21 0 0.38 0.29 0.52 0.64 0.417
TX 0 0.21 1 0 1 0.83 0.88 0.534
4.5 Energy Profile Prediction
Wenow make predictions on each energy profile of the four states. Following the GPR
model in profile characterization (Section 4.1), we first make prediction by GPR, results of
which are presented in Figure 8. Wecan observe that all items turn into a stable increase
after 10 years. This is because in long-term perspective, the prediction should reflect the
generaltrend,andbecomemore‘conservative’especiallyinpredictingpossiblefluctuations
since uncertainty increases. Therefore, for those showing a general increasing trend, like
RED and RE, the long-term prediction shows a stable uphill, while for those showing vi-
olent fluctuation like RCES, the prediction only turns a slight increase. This phenomenon
echosourcharacterizationofitemvalueevolution(Section4.1): thehigherpredictabilitythe
evolutionis, the less conservativethe long-termpredictionwillbe.


## 第 16 页

Team#72969 Page13of22
14000 2500 1
95%confidenceintervals 95%confidenceintervals 95%confidenceintervals
12000regression his c t u o r r v i e caldata 2000 r h e is g t r o e r s ic s a io l n da c t u a rve 0.9 r h e is g t r o e r s ic s a io l n da c t u a rve
predicteddata predicteddata 0.8 predicteddata
10000
1500 0.7
8000
0.6
6000 1000
0.5
4000 500 0.4
2000 0.3
0
0 0.2
1960197019801990200020102020203020402050 1960197019801990200020102020203020402050 1960197019801990200020102020203020402050
Time Time Time
(a) REDofArizona. (b) REofArizona. (c) RCESofArizona.
Figure8:GPR-Based EnergyProfile PredictionofArizona.
However, although GPR presents a global prediction, it fails to focus on the local in-
formation, thus making unreasonable short-term prediction. For example, for RE of Ari-
zona (Figure 8(b)), we can discover that within a short period after 2009, there is a counter-
intuitive decrease opposite to the sharp increase within several years before 2009. This is
because GPR synthesizes all the historical data, and thus drags down the sudden increase
after2009.
Torefine the short-term prediction, a local prediction model should be taken. Wedesign
twonoveltechniques torefine ourmodel.
Technique 1:Sliding Window Mechanism
The Autoregressive Moving Average Model (ARMA) model is an autoregressive predicting
method with priority in short-term prediction [9]. Its general representation is ARMA(p,q)
asfollows:
wheres(t)isthewhitenoiseattimet,whileφ andθ arebothweights. Theslidingwindow
i i
LTP:historydata
STP:historydata STP:futuredata LTP:futuredata
GPRWindow GPRPrediction(constant)
Topredict
Topredict
Topredict
ARMAPrediction(decayexponentially)
Topredict Topredict
ARMASlidingWindow ARMASlidingWindow
Short-TermPrediction(STP) Long-TermPrediction(LTP)
Figure9:ARMA-GPR Hybrid Modelinshort-termand long-termprediction
mechanism,whichrestrictsourconsiderationwithinasmalltemporalrangenearthecurrent
erutridnepxEelbaweneR
tropxEelbaweneR
ecruoSybyportnEnoitpmusnoCelbaweneR
GPRPrediction Topredict
Topredict
Topredict
noitciderPAMRA
精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！


## 第 17 页

Team#72969 Page14of22
精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
time, keeps away from the ‘outmoded’ data of less contribution and even bringingharmful
offset in short-termprediction. Specifically,we set the current time t and only consider time
interval [t k + 1, t], where k t. An intuitive example is illustrated in Figure 9. Moreover,
aswetargetatfollowingthetrendaroundcurrenttimeinshort-termpredictionwithhigher
accuracy, we need to precisely characterize how much the item value changes, that is to
apply ARMA modelonthe increments ofitemvalues,i.e.,
Weplot the prediction results of ARMA-GPR model in Fig. 10. Comparing with thepre-
dictionofGPR,thepredictedvaluegivenbyARMA-GPRmodelappearstobe‘higher’than
GPR predicted value. This is because the time series before 2009 present a ascending trend,
the sliding window of the ARMA model would capture this trend and ‘pull’ up the pre-
dicted value. Withthe time going by,the ARMA-GPR predicted value inclines to converge
tothe GPR predicted value, which resultsfromthe time-decayingweight.
5 Targets and Actions for Interstate Energy Compact
In this section, we put our CAFE model for energy profile into practical policies. Specif-
ically, we determine quantified goals for renewable energy use for 2025 and 2050, and pro-
pose specific measures for accomplishing suchgoalsby the fourstates.


## 第 18 页

Team#72969 Page15of22
14000 GPR95%confidenceintervals 2500 GPR95%confidenceintervals 1.2 GPR95%confidenceintervals
12000 G AR PR MA re -G gr P e R ss 9 io 5 n % c c u o rv n e fidenceintervals GPRre A g R re M s A s - io G n P c R ur 9 v 5 e %confidenceintervals G AR P M R A re -G gr P e R ss 9 io 5 n % cu c r o v n e fidenceintervals
A G R P M R A p - r G ed P i R cte p d re d d a ic ta tedcurve 2000 A G R P M R A p - r G ed P ic R te p d re d d a ic ta tedcurve 1 A G R P M R A p - r G ed P i R cte p d re d d a ic ta tedcurve 10000 A hi R st M or A ic - a G l P d R at p a redicteddata A hi R st M or A ic - a G l P d R at p a redicteddata A hi R st M or A ic - a G l P d R at p a redicteddata
8000 1500 0.8
6000 1000 0.6
4000
500 0.4
2000
0 0 0.2
1960197019801990200020102020203020402050 1960197019801990200020102020203020402050 1960197019801990200020102020203020402050
Time Time Time
(a) REDofArizona. (b) REofArizona. (c)RCESofArizona.
Figure10:ARMA-GPR-Based EnergyProfile PredictionofArizona.
5.1 Targets:TotalRenewable Consumption Based Optimization
Based on our observation on provided data, we identify that the renewable consumption
(RC) accounts for a dominant proportion of total renewable energy use. The predominance
of RC enlightens us to concentrate on consumption issues in drafting the targets while
puttingaside otherslike RP, RI,and RE.
Before we get down to setting targets for energy usage, we make some further assump-
tionsbased onthe generalonesinSection 2.
Assumption 5.The ultimate aim of the compactis to maximizethe global benefits over states.
Assumption 6.The governors of each state inclineto be ‘selfish’ and ,that isto say, they are un-
willing tosacrifice theirown benefits in the consideration of the compact.
Based on Assumption 5, the goal of the compact should be maximizing total renewable
consumption(TRP)amongthestates. However,solelyconsideringtheamountofconsump-
tioncoversthe renewable energyuse partially,asanalyzedinSection4.3. Therefore,amore
reasonable way to deciding goals should stem from our proposed criteria evaluating the
energy profile (Section 4.3). Hence the target setting problem can be formulated as a multi-
objective programming. Tointegrate the evaluation (i.e., objective function) of four states,
we define TotalRenewable ConsumptionProfile (TRCP)and
Moreover,there are two restrictions for the states during their chase for TRC maximiza-
tion:
erutidnepxEelbaweneR tropxEelbaweneR
ecruoSybyportnEnoitpmusnoCelbaweneR
精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！


## 第 19 页

Team#72969 Page16of22
精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Apparently, the problemis alinear programming, thuseasy tosolve. However, we ob-
servethat thereare two limitationsinthe originalTRCPmaximizationproblem:
Inhomogenity: The distribution of RC among states is heavily skewed. Most of the
•
RC enhancement isofferedto theNewMexico,while the otherthreestatesonlyenjoy
tinyincrease. ThisextremeinhomogeneityinhibitstheRCdevelopmentinstatesother
thanNM,deviatingfromthemutuality ofthecompact.
Infeasibility: ItispossiblethatnofeasiblesolutionexistsinmaximizingTRCP dueto
•
the hard constraints on RC. For example when RP is smaller than our predicted R˜C,
thenchancesare thatthe feasible regionis anemptyset.
To thisend, we modify theoriginal optimizationproblemintothe following renovated
version,
where λ is positive predefined parameters and d(i = 1, 2, 3, 4) are the expected benefit of
i
eachstate, whichcan be set by the governors.
Intuitively, there are two adjustments in the new optimization problem. The first is in-
troducing an additive RC requirement i.It tightens the restriction of RC enhancement,thus
.
ensuring an acceptable increment in each state, which dissolves the inhomogenity limita-
tion. The second is converting the RC Limitation constraint into a penalized term in the
objective function, where λ is the penalized factor. The penalized term restricts small dis-
crepancy between TRC and TRP which meets the balance requirement in practice. Mean-
while, itrelaxesthehard requirementsthatRC ≤ RP based ontheincompleteness ofthe


## 第 20 页

Team#72969 Page17of22
精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
provided data,and thepossible renewable energytransformationwith statesotherthanthe
four mentionedones, which dissolvesthe infeasibility limitation.
Thenweapplyourmodeltosettingoftargetsin2025and2050. Table7showstherenew-
able consumption targets as well as improvement percentage compared with the predicted
RC for 2025 and 2050.Here we consider d = 10% for 2025,d = 20% for 2050,i = 1, 2, 3, 4,
i i
and set = 0.015.Wewillfurther discuss the settingofinsensitivityanalysis.
Table 7:Renewable ConsumptionTargets for2025and2050(1014Btu)
Year AZ CA NM TX
2025 1.63(24%) 10.90(10%) 0.54(81%) 3.12(10%)
2050 2.10(58%) 14.73(20%) 0.77(113%) 4.45(20%)
Then we study the effects of our proposed targets on energy profiles. Specifically, we
comparethepredictedvaluesofRCPR,SRC,andRCPCwiththeproposedtargetsandthose
without targets. The results are shown in Figure 11. We notice that for all three items,
the predicted values with targets all outstrip those without targets in both 2025 and 2050,
showing the probable promotionbrought about bythetargets.
(a) RCPR (b) SRC (c) RCPC
Figure 11:The Effects ofProposed Policies in Energy ProfileEnhancement.
Moreover, we also calculate the evaluation criteria based on the RC targets and present
the results in Fig. 12. As we can see, SRC, RCPR, and, REGR for four states achieve signifi-
cant improvement under the RCtargets.
5.2 Actions: Motivating Renewable Energy Use in NM, TX, and AZ
Principles for Actions: (i) Since our goals are predicated on the renewable energy con-
sumption(RC), theactions should first contribute tothe achievement ofRCrequirements;
RCES RCES RCES RCES
REGR RCEES REGR RCEESREGR RCEESREGR RCEES
IRRC RCPRIRRC RCPRIRRC RCPRIRRC RCPR
RCPC SRC RCPC SRC RCPC SRC RCPC SRC
(a)AZ (b)CA (c)NM (d)TX
Figure12:Radar Map:EnergyProfile Evaluationand Target


## 第 21 页

Team#72969 Page18of22
精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
(ii)IfRCrequirementsarefulfilled,theactionsshouldalsobringaboutpositiveeffectsonre-
lateditems,forexampletheconsumptionentropyandtheshareofrenewableconsumption;
(iii) Actionsshould also be prediction-based toinhibit worsetendency in future intime.
Based on the above principles, we propose the following 3 actions and quantitatively
interprettheir promising effects.
Action 1:Stimulating RC and RPof NM andTX in shortterm
According to our prediction of 2025, we discover the following decrease in RC and RP
of NM and TX, listed in Table8. Weobserve that in short term, the renewable energy turns
a negative trend in NM and TX, which indicates that the governors of NM and TX should
stimulate thepromotionofrenewableenergyuse. Particularly NMshould focus onit,since
it is predicted that in 2025 the renewable energy import (RI) of NM still increases byalmost
(199 93)/93 = 114% compared with 2009. This shows the possible promotion of unrenew-
−
able energy use by NM governments, on which the interstate compact should exert more
notice.
Table 8:The decrease ofRCand RPofNM and TX in2025
NM TX
RP (35635−30119)/35635=15.5% (356635−283870)/356635=20.4%
RC (33785−26700)/33785=21.0% (303697−245937)/303697=19.0%
Action 2:Reducing Unrenewable Energy Production in AZ.
Certainly,all states should decrease their usage of unrenewable energy including motor
gasoline, natural gas and petroleum products. This problem is extremely serious in AZ,
as there is a steep decline of the share of renewable production (SRP): with a value of 30%
in 2025 and 87% in 2050. This sharp decrease echoes the historic evolution of unrenewable
energyproductionofAZ,withanalmost800timesgroundbreakingincreasefrom556(1960)
to 482422 (2009) billion Btu. Both strongly show that the wide industrial and social needof
unrenewable energy in AZ. Therefore the to realize the goal of AZ, AZ should limit the
production of unrenewable energy, especially natural gas and gasoline accounting for the
principal portions(20.2% and 28.9%currently).
Action 3:PromotingDiverse Usage ofMore Kindsof Renewable Energyin NM,TX
Wenote from our prediction that NM and TX may both have a decrease in RCES, i.e.
the variety of different kinds of renewable energy consumption. The predicted decrease
is shown in Table 9, which may be a consistent downhill in future. Toinhibit such worse
tendency,NMand TX cantryotherpossible renewableenergyand expanditsconsumption
variety. Currently solar and geothermalenergyisofthe lowest utilizationrate inrenewable
energy,whichaccountforonly1.3%and4.4%. Therefore,motivatingtheuseoftheseenergy
hasgreatpotentials inenhancing renewable energyusage.
In all, according to our current profile assessment and prediction, CA performs the best
and can develop as its current trend without exerting more additional actions. Therefore,
the compact can make CA and other three states cooperate with each other.Specifically,for
example, CA can provide more renewable export to AZ to stimulate the renewable energy
consumption there, and to NM and TX to impede the declining trend of their renewable
consumption.


## 第 22 页

Team#72969 Page19of22
GPRregressioncurve
ARMA-GPRpredictedcurve historicaldata
ecruoSybyportnEnoitpmusnoCelbaweneR
Table 9:The decrease ofRCESofNM andTX in 2025and2050
NM TX
2025 (0.746−0.55)/0.746=26.3% (0.614−0.38)/0.614=38.1%
2050 (0.746−0.43)/0.746=42.3% (0.614−0.25)/0.614=59.3%
6 Sensitivity Analysis
Weprobe into the sensitivity of some parameters in our ARMA-GPR models. As shown
inFig.13(a),whenwechangebfrom0.1to0.9,thepredictedcurvemovesupward. Thepre-
diction of 2025 varies much while the prediction of 2050 remains unchanged. Thisindicates
that the short-term prediction is sensitive to b and the long-term prediction is insensitive.
The reason is that the ARMA prediction counts little in long-term prediction. Moreover,
Fig. 13(b) shows the variation when we change c from 0.1 to 0.9. As we can see, with
0
c increasing, the ARMA-GPR prediction curve approaches GPR prediction curve. This is
0
because larger c generates faster decaying of the effects by ARMA and makes the curve
0
converge toGPR predictionmorequickly.
1 1
GPRregressioncurve
0.9 0.9 ARMA-GPRpredictedcurve historicaldata
0.8 0.8
0.7 0.7
0.6 0.6
0.5 0.5
0.4 0.4
0.3 0.3
1960197019801990200020102020203020402050 1960197019801990200020102020203020402050
Time Time
(a)sensitivityofb (b)sensitivityofc
0
Figure13:SensitivityAnalysis ofParametersin ARMA-GPR model
Then we probeinto the sensitivityofouroptimizationmodelinSection5.1.Setting dif-
ferent,we obtainthe optimized value oftheobjective function, shownin Table 10.The
Table 10:Sensitivity AnalysisofParameterinOptimizationModel
λ 0.011 0.012 0.013 0.014 0.015 0.016 0.017 0.018 0.019
TRCPj 3.11 4.25 6.45 7.43 9.23 11.25 14.50 16.34 18.33
results in the table show that different bring about much variation of the optimized value.
In fact, represents the weight of difference between total renewable consumption and pro-
duction. If this weight is small, then the target RC given by the optimization will increase
much. This provides more flexibility to the governors. Specifically, if the governors desire
toset ahighand challenging target,can be set asarelatively smallvalue. To achieve this
ecruoSybyportnEnoitpmusnoCelbaweneR
精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！


## 第 23 页

Team#72969 Page20of22
精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
target,eachstate must take moreactionsand enhance cooperation.Hence, onecan set a
propertoadjust the difficulty ofthe compact target.
7 Strengths and Weaknesses
7.1 Strengths
Low Feature and Evaluation Complexity: We refine 20 out of total 605 features, and
•
furthergeneralize7 criteria integratedinto 1 in evaluation;
HighGeneralizability: WeapplyGPR tocharacterizeallitemsinenergyprofileswith
•
different trends due toitsnon-parameticproperty;
BilateralSimilarityAnalysis: Weseminallydissectsimilarityofenergyprofilesamong
•
different states by the combination of GRA and KRCC, with concentration on value
and tendency similarityrespectively;
Temporally Adaptive Prediction: We are avant-couriers proposing the ARMA-GPR
•
Hybrid model suitable in both short-term and long-term prediction, by adaptively al-
teringtheweights oflocaland globalinformation;
QuantifiedandRationalGoals: Wesetquantifiedgoalsstrictlybasedonoptimization
•
theory.
7.2 Weaknesses
• No VerificationofRaw Data: Wehaveno guaranteeoftheaccuracy ofgivendata[5].
No Involvement of Other States: We do not consider states other than CA, AZ, NM,
•
and TX,due to thelack ofrelevant data.
NoConsiderationofStateSelf-Interest: Wesetourtargetsbasedonmaximizingtotal
•
renewable energy consumption, but in fact each state may care more about its own
developmentwhile regardlessofothers, thus notfollowing our mutualtargets.
8 Conclusion
In this paper, we first create a energy profile by selecting and aggregating the variables
in the provided data. Then we propose a framework called CAFE (Characterization, Anal-
ysis, Forecasting, and Evaluation of Energy Profile) to characterize the evolution of energy
profile time series, analyze the similarity of energy profile among four states, evaluate the
renewable energy usage, and forecast the future evolution of energy profile. Based on the
results of CAFE, we adopt multi-objective programming to set up renewable energy usage
targets for CA, AZ, NMïijNˇ and TX. Moreover, we propose a series of concrete actions for
eachstatetomeetthetargets. Finally,weconduct sensitivityanalysisofsomeparametersin
ourmodeland discussthe strengths and weakness ofourwork.


## 第 24 页

Team#72969 Page21of22
精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
MEMORANDUM
To:GovernorsofCA, AZ,NM, andTX
From:Team #72969
Date: Feb12th,2018
Subject: EnergyProfilesCharacterization, Predictionand Future Goals
Honorable GovernorsofCA, AZ, NM,andTX,
Currently the four states intend to enact an energy compact, with emphasis on policies
of renewable energy usage. As the person in charge, our team has made a comprehensive
study on renewable energy use based on historical data from 1960 to 2009, including char-
acterizingthe energyprofile offourstates in thisperiod, predicting energy use to2050,and
settingfuture goalsandactions.
Energy Profiles: In 2009, both the renewable energy production and consumption in all
states increase at least 100% and 200% compared with 1960 respectively. Main difference
exists in unrenewable energy production: CA and TX decreases by 16.5% and 3.4%, while
NM and AZ increases by 52% and 800 times. It renders CA and TX an increasing share of
renewableenergyproduction,whileAZadecreaseby85%. Generally,CAisjudgedtohave
thebest energy profile in2009.
Predictions: Wemakepredictionsofenergyprofilesin2025and2050. Fortherenewable
energy production and consumption, both NM and TX first decrease before 2025 while in-
crease around 2050, while CA and AZ consistently increase. Other factors are ofreasonable
future trends expect: (i) the share of renewable energy production, where AZ is predicted
to have a decrease of 30%/87% in 2025/2050 compared with that in 2009; (ii) the varietyof
renewableenergyconsumption,whereNMandTXcontinuestodecreaseby37%/49%and
38%/59%.
Goals: Renewable energy consumption (RC) takes the dominant role of all renewable
energy use, acting as the linchpin of renewable energy promotion. Therefore the states
shouldstimulateRCinfuture. Basedonourprediction,thegoalsofRCarerespectivelyCA:
988787/1227217,AZ: 148028/175154,NM: 30120/36359, TX: 283871/371206 (billionBtw)in
theyear of2025/2050.
Actions: Our main proposed actions, ranked by significance, are: (i) Stimulating RC
and RPofNM andTX inshort term; (ii) Reducing Unrenewable EnergyProductionin AZ;
(iii) Promoting Diverse Usage of More Kinds of Renewable Energy in NM and TX. All are
based on profiles as of 2009 and our predictions. Meanwhile, CA can perform positively
without any extra action, so CA can export more renewable energy to the other three states
tostimulate their RCs.
The above is the summary of our study.Wesincerely hope that it will provide you with
usefulinformation.
Thanks!


## 第 25 页

Team#72969 Page22of22
精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
References
[1] J. F. Zimmerman, Interstate cooperation: Compacts and administrative agreements. SUNY
Press, 2012.
[2] “Explanationofenergyprofiles.”http://libguides.gatech.edu/c.php?g=54047p=349537.
[3] A. Cammarano, C. Petrioli, and D. Spenza, “Pro-energy: A novel energy prediction
model for solar and wind energy-harvesting wireless sensor networks,” in IEEE 9th In-
ternational Conference on Mobile Adhoc and Sensor Systems(MASS),pp.75–83,2012.
[4] J.ViroteandR.Neves-Silva,“Stochasticmodelsforbuildingenergypredictionbased on
occupant behaviorassessment,”Energy and Buildings,vol.53,pp. 183–193,2012.
[5] “Dataset source.” https://catalog.data.gov/dataset/state-energy-data-system-seds-
complete-dataset-through-2009sec-dates.
[6] U. Çaydas¸and A. Hasçalık, “Use of the grey relational analysis to determine optimum
lasercuttingparameterswithmulti-performance characteristics,” Optics&LaserTechnol-
ogy,vol.40,no. 7,pp. 987–994,2008.
[7] Y.Kuo, T.Yang, and G.-W. Huang, “The use of grey relational analysis in solving mul-
tiple attribute decision-making problems,” Computers & industrial engineering, vol. 55,
no. 1,pp.80–93,2008.
[8] “Greyrelationalanalysis.”https://en.wikipedia.org/wiki/Grey-relational-analysis.
[9] S. Akhtar and S. Rozi, “An autoregressive integrated moving average model for short-
termpredictionofhepatitiscvirusseropositivityamongmalevolunteerblooddonorsin
karachi,pakistan,”WorldJournalofGastroenterology(WJG),vol.15,no.13,pp.1607–1612,
2009.


## 第 26 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Appendix A:Similarity calculation MATLAB code
1 factor = [423970 295243 315198 696241;
2 4.70 0.35 0.20 2.50;
3 880 1250 1740 520;
4 563 323 350 734 ;
5 17 24 15 .521;
6 92.6 22 6.62 40.6;
7 2424 295 91 1648;
8 61925 43269 43551 59995];
9
10F= 8;
11 factorrelation = zeros(N,N,F);
12
13 factort = [];
14 similarity1t = [];
15 forf= 1:F
16
17f i g u r e ;
18 x = [ ] ;
19y= [];
20 for n1 =1:N
21 for n2 =1:N
22ifn1~=n2
23factorrelation(n1,n2,f)= abs(factor(f,n1)−factor(f,n2))/ factor(f,n1);
24plot(factorrelation(n1,n2,f),similarity1(n1,n2),’bo’);
25x= [xfactorrelation(n1,n2,f)];
26y = [ysimilarity1(n1,n2)];
27holdon;
28 end
29 end
30 end
31factort= [factort;x];
32similarity1t= [similarity1t;y];
33[w, s]= polyfit(x,y,1);
34x= 0:0.01:100;
35y= w(1)*x+w(2);
36plot(x,y);
37a=0;b1= 1.2*max(max(factorrelation(:,:,f)));b2= 1.2*max(max(similarity1));
38%xlim([ab1]);
39%ylim([0.8*min(min(similarity1))b2]);
40axis([ab1ab2]);
41end
42
43 forf= 1:F
44tmp= factorrelation(:,:,f);
45 factorkendallc(f) = corr(similarity2(:) ,tmp(:) ,’type ’,’pearson ’);


## 第 27 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
46 end
47 tmp1= [];
48 forf= 1:F
49 tmp= [];
50 forn1 = 1:N
51 tmp = [tmp ; factorrelation(n1,: ,f) ’];
52 end
53 tmp1= [tmp1tmp];
54 end
55 facto rkendallp= partialcorr([tmp1,similarity2(:)]);
Appendix B:GPR regression MATLAB code
1 N= 4;
2 K = 20;
3 T= 50;
4
5 weight = zeros(N,K);
6 bi as = zeros(N,K) ;
7 Sigma = zeros (N,K) ;
8 deviation = zeros(N,K);
9
10 x= 1960:2009;
11 x= x’;
12 testx = 2010:2050;
13 te stx = testx ’ ;
14 fork=1:20
15
16 datafit = datanew(6*k−4:6*k−1,2:T+1);
17 datafit(isnan(datafit))= 0;
18
19 y= datafit(1,:);
20 gprMdl1 = fitrgp(x,y, ’Basis ’,’linear ’ ,...
21 ’FitMethod ’,’exact ’,’PredictMethod ’,’exact ’,’Kernel Function ’,’squaredexponential ’,’
Standardize ’ ,1,’Regularization ’ ,0.2);
22
23 y= datafit(2,:);
24 gprMdl2 = fitrgp(x,y, ’Basis ’,’linear ’ ,...
25 ’FitMethod ’,’exact ’,’PredictMethod ’,’exact ’,’Kernel Function ’,’squaredexponential ’,’
Standardize ’ ,1,’Regularization ’ ,0.2);
26 beta2= gprMdl2.Beta(1);
27
28 y= datafit(3,:);
29 gprMdl3 = fitrgp(x,y, ’Basis ’,’linear ’ ,...
30 ’FitMethod ’,’exact ’,’PredictMethod ’,’exact ’,’Kernel Function ’,’squaredexponential ’,’
Standardize ’ ,1,’Regularization ’ ,0.2);
31 beta3= gprMdl3.Beta(1);
32


## 第 28 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
33 y = datafit(4,:);
34 gprMdl4 = fitrgp(x,y, ’Basis ’,’linear ’ ,...
35 ’FitMethod ’,’exact ’,’PredictMethod ’,’exact ’,’Kernel Function ’,’squaredexponential ’,’
Standardize ’ ,1,’Regularization ’ ,0.2);
36 beta4 = gprMdl4 .Beta (1);
37
38 testx = 1960:2009;
39 [ygr1 ,bi1 ,ci1] = predict(gprMdl1,testx ’);
40 [ygr2 ,bi2 ,ci2] = predict(gprMdl2,testx ’);
41 [ygr3 ,bi3 ,ci3] = predict(gprMdl3,testx ’);
42 [ygr4 ,bi4 ,ci4] = predict(gprMdl4,testx ’);
43
44 error(k)= mean(abs(ygr1 ’ − datafit(1,:))./(datafit(1,:)));
45
46 weight(1,k)= gprMdl1.Beta(1);
47 bias (1,k) = gprMdl1.Beta(2);
48 Sigma(1,k)= gprMdl1.Sigma;
49 deviation(1,k)= mean((bi1(1:50)))/mean(datafit(1,:));
50 weight(2,k)= gprMdl2.Beta(1);
51 bias (2,k) = gprMdl2.Beta(2);
52 Sigma(2,k)= gprMdl2.Sigma;
53 deviation(2,k)= mean((bi2(1:50)))/mean(datafit(2,:));
54 weight(3,k)= gprMdl3.Beta(1);
55 bias (3,k) = gprMdl3.Beta(2);
56 Sigma(3,k)= gprMdl3.Sigma;
57 deviation(3,k)= mean((bi3(1:50)))/mean(datafit(3,:));
58 weight(4,k)= gprMdl4.Beta(1);
59 bias (4,k) = gprMdl4.Beta(2);
60 Sigma(4,k)= gprMdl4.Sigma;
61 deviation(4,k)= mean((bi4(1:50)))/mean(datafit(4,:));
62
63 subplot (2,10,k)
64 plot(testx ,ygr1 , ’b’,’LineWidth ’ ,1,’Color ’,’r’);
65 set(gca , ’xtick ’ ,[] , ’xticklabel ’ ,[]) ;
66 set(gca, ’ytick ’ ,[] , ’yticklabel ’ ,[]) ;
67 xlim([1960 2009]);
68 hold on
69 end
Appendix C:ARMA-GPR regression MATLAB code
1 N= 4;
2 K= 20;
3 T= 50;
4
5 x= 1960:2009;
6 x= x’;
7 te stx = 2010 :2050 ;


## 第 29 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
8 te stx = testx ’;
9%fork=1:K;
10 k=13;
11 datafit = datanew(6*k−4:6*k−1,2:T+1);
12 datafit(isnan(datafit)) = 0;
13
14 y = datafit(1,:);
15 y0 = [ diff(datafit(1,:))’;repmat(y(1,49) ,41,1)];
16 z= iddata (y0);
17%z.y= cumsum(z.y);%integrateddata
18m= armax(z(1:49),[33],’IntegrateNoise’,true);
19yma1= predict(m,z,41);
20yma1= yma1.outputdata(50:90);
21 gprMdl1 = fitrgp(x,y, ’Basis ’,’linear ’ ,...
22 ’FitMethod ’,’exact ’,’PredictMethod ’,’exact ’,’Kernel Function ’,’squaredexponential ’,’
Standardize ’ ,1,’Regularization ’ ,0.2);
23 beta1 = gprMdl1 .Beta (1);
24
25 y = datafit(2,:);
26 y0 = [ diff(datafit(2,:))’;repmat(y(1,49) ,41,1)];
27 z= iddata (y0);
28%z.y= cumsum(z.y);%integrateddata
29m= armax(z(1:49),[33],’IntegrateNoise’,true);
30yma2= predict(m,z,41);
31yma2= yma2.outputdata(50:90);
32 gprMdl2 = fitrgp(x,y, ’Basis ’,’linear ’ ,...
33 ’FitMethod ’,’exact ’,’PredictMethod ’,’exact ’,’Kernel Function ’,’squaredexponential ’,’
Standardize ’ ,1,’Regularization ’ ,0.2);
34 beta2 = gprMdl2 .Beta (1);
35
36 y = datafit(3,:);
37 y0 = [ diff(datafit(3,:))’;repmat(y(1,49) ,41,1)];
38 z= iddata (y0);
39%z.y= cumsum(z.y);%integrateddata
40m= armax(z(1:49),[33],’IntegrateNoise’,true);
41yma3= predict(m,z,41);
42yma3= yma3.outputdata(50:90);
43 gprMdl3 = fitrgp(x,y, ’Basis ’,’linear ’ ,...
44 ’FitMethod ’,’exact ’,’PredictMethod ’,’exact ’,’Kernel Function ’,’squaredexponential ’,’
Standardize ’ ,1,’Regularization ’ ,0.2);
45 beta3 = gprMdl3 .Beta (1);
46
47 y = datafit(4,:);
48 y0 = [ diff(datafit(4,:))’;repmat(y(1,49) ,41,1)];
49 z= iddata (y0);
50%z.y= cumsum(z.y);%integrateddata
51m= armax(z(1:49),[33],’IntegrateNoise’,true);


## 第 30 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
52yma4= predict(m,z,41);
53yma4= yma4.outputdata(50:90);
54 gprMdl4 = fitrgp(x,y, ’Basis ’,’linear ’ ,...
55 ’FitMethod ’,’exact ’,’PredictMethod ’,’exact ’,’Kernel Function ’,’squaredexponential ’,’
Standardize ’ ,1,’Regularization ’ ,0.2);
56 beta4 = gprMdl4 .Beta (1);
57
58 alpha = 0.8;
59 ysp1 = alpha*cumsum(yma1) + (1−alpha)*(prelation(1,2,k)*cumsum(yma2)+prelation(1,3,
k)*cumsum(yma3)+prelation(1,4,k)*cumsum(yma4))/sqrt(prelation(1,2,k)^2+prelation
(1,3,k)^2+prelation(1,4,k)^2) ;
60 ysp2 = alpha*cumsum(yma2) + (1−alpha)*(prelation(2,1,k)*cumsum(yma1)+prelation(2,3,
k)*cumsum(yma3)+prelation(2,4,k)*cumsum(yma4))/sqrt(prelation(2,1,k)^2+prelation
(2,3,k)^2+prelation(2,4,k)^2) ;
61 ysp3 = alpha*cumsum(yma3) + (1−alpha)*(prelation(3,1,k)*cumsum(yma1)+prelation(3,2,
k)*cumsum(yma2)+prelation(3,4,k)*cumsum(yma4))/sqrt(prelation(3,1,k)^2+prelation
(3,2,k)^2+prelation(3,4,k)^2) ;
62 ysp4 = alpha*cumsum(yma4) + (1−alpha)*(prelation(4,1,k)*cumsum(yma1)+prelation(4,2,
k)*cumsum(yma2)+prelation(4,3,k)*cumsum(yma3))/sqrt(prelation(4,1,k)^2+prelation
(4,2,k)^2+prelation(4,3,k)^2) ;
63
64 [ygr1 ,bi1 ,ci1] = predict(gprMdl1,testx);
65 [ygr2 ,bi2 ,ci2] = predict(gprMdl2,testx);
66 [ygr3 ,bi3 ,ci3] = predict(gprMdl3,testx);
67 [ygr4 ,bi4 ,ci4] = predict(gprMdl4,testx);
68
69 a1 = 0.4;a2 = 0.5;decay = −0.6;
70%ypred1= ((1−a1.*exp(decay.*(testx−2010))).*ygr1+ a1.*exp(decay.*(testx−2010)).*
ysp1);
71 ypred1 = (1−a1.*exp(decay.*(testx −2010))).*ygr1 + a1.*exp(decay.*(testx −2010)).*
(datafit(1,50)+ysp1);
72 ypred2 = (1−a1.*exp(decay.*(testx −2010))).*ygr2 + a1.*exp(decay.*(testx −2010)).*
(datafit(1,50)+ysp2);
73 ypred3 = (1−a1.*exp(decay.*(testx −2010))).*ygr3 + a1.*exp(decay.*(testx −2010)).*
(datafit(1,50)+ysp3);
74 ypred4 = (1−a1.*exp(decay.*(testx −2010))).*ygr4 + a1.*exp(decay.*(testx −2010)).*
(datafit(1,50)+ysp4);
75 end

# E88902-A Probabilistic Model of the Relationships between Countries and Climate Change


## 第 1 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
TeamControlNumber
Forofficeuseonly Forofficeuseonly
88902
T1 F1
T2 F2
T3 ProblemChosen F3
T4 E F4
2018 MCM/ICM Summary Sheet
A Probabilistic Model of the Relationships between Countries and
Climate Change
Summary
Background Under the effects of climate change, a series of economic, environmental and social problem have
emerged from region to region, especially in fragile states. It becomes more and more imperative to develop a
sophisticated but easy-to-understand model of the relationships between a country’s fragility and the impact of
climate change over it as a guide for the decision and policy makers.
Objective The objective of this paper is to propose a probability and machine learning based model called
2THN(2-Time-slice Hybrid Network), as well as two newmetrics to measure the fragility(WFSI(Weighted Frag-
ile State Index)) and climate change’s impact of the country(CCIC(Climate Change Index by Country)). The
whole paper can be divided into five main parts: data collection and pre-process; model representation; param-
eter estimation; model analysis; case study and problem solution.
Firstly, we identify all the data we would like to use in an ideal situation. But since we cannot get access
to some subset of the ideal data, we have to construct our model using a different dataset other than the ex-
pected one. Incomplete as it is, it’s sufficient for the purpose of illustrating the main points of our model. Data
augmentation, classification, and several normalization methods are also introduced in thispart.
Secondly, trying to make the paper easy to read and understand, we then concentrate only on the representa-
tions and semantics of our models, leaving out the esoteric mathematical details. We first define our firstmetric
- Climate Change Index(CCI), which is a global metric to quantize the degree of climate change. Later on, Cli-
mate change vulnerability(CCV) is introduced, which is a state-level metric. We then define the Climate Change
Index by Country(CCIC) using CCI and CCV as our second metric. Then Weighted Fragile State Index(WFSI),
a revised version of FSI utilizing Analytical Hierarchy Process(AHP) and Entropy Method(EM) is defined, after
which we introduce the novel 2-Time-slice Hybrid Network(2THN) to connect the two dots(CCIC and WFSI)
and establish an easy-to-understand relationship, where the rationales of our choice of a probabilistic model, as
well as other concerns are thoroughly discussed.
Thirdly, the details of how the parameters are derived are introduced, including the details of Entropy
Method(EM) and the learning and inference of 2THN. Meanwhile, the reasons for our choice to learn both the
structure and parameters are discussed.
Fourthly, we analyze the properties and characteristics of our model using Mean Value Analysis,
correlation analysis, information-theoretical analysis and other analysis to better understand the trained
model, where we make our hypothesis of the dynamics of the Climate-Fragility system and justify them by
reasoning through the evidence. Furthermore, the notion of Warning Zone(WZ) is introduced, indicating that
the latent effects of climate change are invisible to people outside a specific range.
Eventually, we come back to the 5 tasks assigned to us in the first place and tackle them using our model one by
one. We use K-Means to define the standard line of one country’s fragility state. We take Sudan and Greece


## 第 2 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
as examples to apply our model in practice, after which we identify some possible strategies taking Sudan’s
example again. Finally,we scale our model to the level of continents and discuss the feasibility of scaling it to
evencities.
Conclusion In general, the models of WFSI-CCIC and 2THN fit well to reality and therefore pragmatic.
The fact that the parameters are calculated by analyzing the data instead of fixed gives our model enormous
flexibility,makingiteasytobeappliedwidely.Butmeanwhile,itsstrongdependenceondatamakesituseless
whenfacingextremesituationssuchascountriesinlargescalewars.


## 第 3 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Contents
1Introduction············································································································ 1
1.1Background······································································································1
1.2OurMethods····································································································1
2AssumptionandAcronyms·························································································2
2.1Assumption······································································································2
2.2Acronyms········································································································2
3Data·······················································································································2
3.1DataCollectionandAugmentation········································································2
3.2DataClassification·····························································································3
3.3DataNormalization····························································································3
3.4DataDiscretization·····························································································3
4Model···················································································································· 3
4.1ClimateChangeIndexbyCountry(CCIC)······························································· 3
4.1.1ClimateChangeIndex(CCI)·········································································4
4.1.2ClimateChangeVulnerability(CCV)······························································4
4.2WeightedFragileStateIndex(WFSI)·······································································5
4.32-Time-SliceHybridNetwork···············································································5
4.3.1Overview·································································································5
4.3.2Assumptions···························································································· 6
4.3.3Precautions······························································································ 7
4.3.4InnerStructure-MarkovNetwork································································ 7
4.3.5IntraStructure-BayesianNetwork································································8
5ParameterEstimation································································································ 9
5.1WeightCalculation·····························································································9
5.1.1FormationOfindicatoreigenvaluematrixC······································································9
5.1.2Calculatingtheentorpyofindicators······························································9
5.1.3Thecoefficientofvariationofindicators························································10
5.1.4Calculatingtheweightofentropy································································10
5.1.5Normalizationofindicatoreigenvaluematrix·················································10
5.1.6FuzzyComprehensiveEntropyWeightMedol················································10
5.2Parametersof2THN·························································································10
5.2.1Learning································································································ 11
5.2.2Inference································································································12
6Analysis················································································································12
6.1Intuition·········································································································12
6.2PosteriorMeanValueAnalysis············································································12
6.3OtherAnalysis·································································································13
7Task1:Modelsand StandardLines··············································································13
7.1DeterminethestandardlinebyK-MeansClusteringAlgorithm··································13
7.2IdentifyingtheImpactofClimateChange······························································14
8Task2:CaseStudy -Sudan························································································14
9Task3:CaseStudy -Greece······················································································· 15
9.1WFSIandCCICforGreece·················································································15
9.2PredictionforGreece·························································································16
10Task4: PossibleStrategies························································································17
11Task5: ScalabilityAnalysis·······················································································17
12Strengthsandweaknesses························································································19
12.1Strengths·······································································································19
12.2Weaknesses··································································································· 19
Reference·················································································································20
Appendices··············································································································23


## 第 4 页

Team#88902 Page1of24
精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
1 Introduction
1.1 Background
In 2007, the Intergovernmental Panel on Climate Change (IPCC) first associated the fragile state
with climate change. They state that developing countries are particularly vulnerable to the socio-
economicimpactsofclimatechangefortheirdependenceonagricultureandhighpopulationgrowth
as well as weakinfrastructure. Theclose to 80 percent of theworld population thatlives in the de-
veloping world faces 90 percent of the disasters[1]. Efforts to help fragile states move onto a path
toward stability and sustainability continue to face enormous challenges. Climate change is one
of these challenges[2]. There is a growing consensus among researchers and policy-makers that cli-
mate change represents a real threat to peace and security.Dabelko stated in Climate Change and
FragileStatesWorkshop[3] thatclimatechangecanactasa"threatmultiplier"andastressoronstate
capacities,oncommunitiesandonexistingconflictdynamics.
In order to solve this problem, we have to construct a model with high enough fidelity of the
dynamicsregardingthewholesystem.However,wehavetwomainchallengesbeforeus:
1. Itiswithinthesefragilecountriesthatclimateinformationisoftentheweakestifitexistsat
all[4].
Attemptingtosolvethisproblem,wemakeeffectiveuseofthedatabycombiningmultipledata
source,conductingsophisticateddatapreprocessingandaugmentation,addingweightcontrol
aswellasutilizingtheexpertknowledge. Butstill,wearesufferingfromthelackofdata.
2. Theimpactsofclimatechangecouldbeobscuredwhilepassingthroughthefuzzyphysical
channelsforitsinterconnectednesswithdevelopment,resourceuse,health,livelihoods,and
economies[3],makingitextremelyhardtogetdeepinsightofthesystem.
Tobetter model the interconnected and uncertain nature of the system, we propose a proba-
bilisticmodelcalled2THN(2-Time-sliceHybridNetwork),combinedwiththeinformationand
probabilistictheoryaswellasthemostadvancedmachinelearningapproach.
1.2 OurMethods
Theoverallobjectivesofourmodelislistedasfollows:
1. Designacomprehensibleandpragmaticmetricaswellaclearlydefinedstandardforthemea-
surementsofthefragilityofandclimatechangeimpactoveronecountry.
2. Establishaprobabilisticnetworkwithreasonablyfidelitytoanalyzethesimultaneousandtem-
poralrelationships ofthefivemostcrucialelements andthereforeprovidereferentialsugges-
tionsfordecisionandpolicymakers.
SOCIAL COHESION
x(1-CCV)
CCI CCIC WFSI
POLITICAL ECONOMIC
Figure1:Thestructureofourmodel.


## 第 5 页

Team#88902 Page2of24
精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Figure 1 shows the structure of our model. First, we define Climate Change Index(CCI) as
a quantified measurement of the global climate change. Second, we manipulate it with Climate
Change Vulnerability(CCV) to narrow the global effect of climate change down to a single coun-
try,resultinginanewindexcalledClimateChangeIndexbyCountry(CCIC).Third,weestablisha
probabilisticnetworkbetweenCCICandWeightedFragileStateIndex(WFSI),disassemblingCCIC
intofourdimensionalsub-indicators,combinedwithsophisticatedweightingmethods.
2 Assumption and Acronyms
2.1 Assumption
1. Thedatasourceisreliable.
2. Thedomesticpoliticalsituationisrelativelystableandlarge-scalewardoesnotbreakoutinthe
countrywhileapplyingourmodel.
3. Themainproductiveforcesandsocialstructurewon’tchangeinrecentyears.
2.2 Acronyms
Abbreviation FullName Abbreviation FullName
CI CohesionIndex C1 SecurityApparatus
EI EconomicIndex C2 FactionalizedElites
PI PolicyIndex C3 GroupGrievance
SI SocialIndex E1 Economy
CCI ClimateChangeIndex E2 EconomicInequality
CCIC ClimateChangeIdnexofCountry E3 HumanFlightandBrainDrain
WFSI WeightedFragileStateIndex P1 StateLegitimacy
2THN 2-Time-slicHybirdNetwork P2 PublicServices
P3 HumanRights S1 DemographicPressures
WZ Warningzone CCV ClimateChangeVulnerability
S2 RefugeesandIDPs X1 ExternalIntervention
FI FactorIndicator RI ResultIndicator
EPI EnvironmentalPerformanceIndex KA K-meansClusteringAlgorithm
3 Data
3.1 Data Collection andAugmentation
Todetermineastate’sfragility,weuse12indicators(C1,C2,C3,E1,E2,E3,P1,P2,P3,S1,S2,X1)
providedbyTHEFUNDFORPEACE[30].
Annual Average Temperature[31]and Precipitation[32], CO Emissions[33],Arable Land[34],Envi-
2
romentPerformanceIndex[35]areusedtocalculateClimateChangeIndexofastate.
For the first 12 indicators, we download data of 12 years(2006-2017) on 178 countries. Toget
sufficientdataforcalculationofCCI,wecanonlyfinddataof13years(2000-2012)on111countries.
Luckily,the 111 countries are all included in the former 178 countries. So, we finally get data of 7
years(2006-2012)on111countries.
Wedidn’tmanagetofindEPIdataofyear2011,so,forthesakeofcontinuityandauthenticityof
thedata, weuse the mean value of the year of 2010and 2012to fill theblank because the indicator
valuesarecomparativelysmooth.


## 第 6 页

Team#88902 Page3of24
精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
3.2 Data Classification
SameasTHEFUNDFORPEACE[30],wedividethese12indicatorsintofourcategories(Cohesion
Index, Economic Index, Political Index, Social Index) as shown in Figure 3. The reasons to adopt
suchahierarchicalstructurearelistedasfollows:
1. Thereisasignificantknowledgegapamongkeydecisionandpolicymakersaroundtheclimate
changeandenvironmentalrisksinfragilestatesandtheirimpactonthesecurityenvironment[26].
Toprovidethedecisionmakerswithmoreacceptableinstructions,wehavetomakeourmodel
easytounderstand.
2. Toavoidtheextensivecomputationalcostwhenimplementingthealgorithms,whichwillbe
introducedlater.
3.3 Data Normalization
Accountingforthedifferentscalesoftheindicators,allourdatahasbeennormalizedbeforeused
inourmodels.
All the 17 indicators can be classified into three types: positive indicators to which the bigger
thebetter,negativeindicatorstowhichthesmallerthebetter,andspecialindicatorsofwhichthebest
valueisafixedvalue.Supposethereareevaluatingindicatorscountedm,evaluatingobjectscounted
n.Inthefollowingequations,c representstheoriginalvalueofindicatoriforsamplestatej,where
ij
i = 1, 2, . . . , n andj = 1, 2, . . . , m. r isthenormalizedvalueofx .
ij ij
Forthepositiveindicators,thereare
c
r = ij (1)
ij
max c
j { ij }
Forthenegativeindicators,thereare
min c
ij
j { }
r = (2)
ij
c
ij
For the special indicator, we must choose a best-fixed value. In our model, PRI, TASIand ALI
belongtothiskind. Wecalculatetheaveragevalueofeachcountryasthebestvalueforthatcountry
duetodifferentnationalconditions.Thenormalizationequationis:
c A
ij ij
r = 1 − (3)
ij . .
−.max c A .
j {| ij − ij |}
where,A isthebestvalueforthejthindicatorontheithcountry.Ifr equalsto0,wereassignitto
ij ij
0.0001.
3.4 Data Discretization
Inordertoutilizethecomputertosimulateourmodelandtomakeourmodelmorecomprehen-
sive,wediscretizeourresultsinto10intervalsusingtheK-meansalgorithm.
4 Model
4.1 Climate Change Index byCountry(CCIC)


## 第 7 页

Team#88902 Page4of24
精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
To establish the network between climate
change and fragility of a country, we first de-
sign a metric to quantize the impact of climate
change on different countries. There are two
stepsasfollows:
1. DefineCCI(ClimateChangeIndex).
2. MultiplyCCIwithCCV(ClimateChange
Vulnerability)togetCCIC.
4.1.1 ClimateChangeIndex(CCI)
According to the IPCC(Intergovernmental
PanelonClimateChange),climatechangerefers
to "a change in the state of the climate that can
beidentified... bychangesinthemeanand/or
the variability of its properties, and that per-
Figure2:ClimateChangeIndex(CCI)
sists for an extended period, typically decades
orlonger"[5].
Therearemanyrelatedprofessionalindexes
used to measure climate change, but most of
themincludehighweightsofunnatural indica-
tors(e.g.,CCPI(ClimateChangePerformanceIndex)weightsclimatepolicyas20%[7]),whicharenot
desiredinourcaseforthepresenceofCCV(ClimateChangeVulnerability).Therefore,weestablisha
newmetricourselvesbycombiningtwocategoriesconsistingofonlynaturalindicatorsandweight
them:factorindicatorandresultindicatorasshowninFigure2.
Factorindicators(FI)arevariableswhichdirectlyinfluencetheclimate,suchastemperature,solar
radiation intensity, precipitation and carbon emission. Result indicator(RI) is on the opposite, which is
the natural phenomenon, which indicates the degree of climate change reversely. It includes biodi-
versity, arable land, sea level change, natural disasters and so on. Here, we only gained the access to
complete historical metadata for three FI and one RI by country due to the access right and time
limitation. Hence,weturnedtoaprocesseddataindexwhichisso-calledEnvironmentalPerformance
Index(EPI). According to the YaleCenter for Environmental Law & Policy (2018), EPI consists of many
RIslikeforest(5%),biodiversity(12.5%),waterresource(12.5%)andsoon.
CCI =WT Index
norm
×
whereWT meanstheweightvectorandIndex isthenormalizedvaluevectorofacountry.
norm
The equation above is processed to grade the degree of climate change, which we will discuss
in detail later in Parameter Estimation Section. That is, if a country gets a high score, which is
approaching1,thiscountrydoesn’tsuffermuchfromclimatechange.
4.1.2 ClimateChangeVulnerability(CCV)
Due to geographical location or socio-economic condition, some countries are more vulnerable
to the impacts of climate change than others. ND-GAIN[6] assesses the vulnerability of a country
by considering six life-supporting sectors: food, water, health, ecosystem services, human habitat and
infrastructure,whichcanbequantizedrespectivelybyareal numberbetween 0to1.Thehigherthe
number,themorelikelythecountrywillsufferfromtheimpactofclimatechange.Wetakethismetric
asclimatechangevulnerability(CCV),andmultipliedtheprocessedCCItogetCCIC:
CCIC = CCI (1 CCV )
× −
wheretheCCICwillbecomefairlylargewhenCCIisapproaches1orCCVisapproaches0.


## 第 8 页

Team#88902 Page5of24
精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
4.2 WeightedFragile State Index(WFSI)
Weightingmodelisessentialtoevaluatethedifferentcontributionoftheindicators,especiallyin
our case. Here, we assume that the four categories (cohesion, economic, political and social) have
the same importance for the time being. However, if expert knowledge is accessible, we can use
AHP(AnalyticalHierarchyProcess)togiveamoresophisticatedoverallweightingstrategywhilewe
useEM(EntropyMethod)(detailswillbediscussedlaterinParameterEstimationSection)toweight
the12sub-factorsbasedonthehistoricaldata.
Figure3:WeightedFragileStateIndex(WFSI)
We respectively apply EM to the four indicators, each of which consists of another three sub-
factors,whichisshowninFigure3.
OncewegettheresultfromEM,wethenmultiplyitbytheFSIwealreadyhave,whoseresultis
exactlywhatweneed.
4.3 2-Time-Slice HybridNetwork
4.3.1 Overview
Wenow havethenormalizedmeasurements of thefourmost crucial indicators weobtained by
utilizing EM. To better study the interactions between these four indicators, we then formulate its
inner structure and the temporal effects across them into a 2-Time-slice Hybrid Network(2THN).
Specifically, we combine the undirected Markov Network(MN) model with the directed Bayesian
Network(BN)model,whichcanbeillustratedbyfigure4.
Butwhyprobabilisticmodels?Althoughdeterminismisindeedaveryvaluablepropertyinmod-
eling,takingthemassiveuncertaintyandnoisesintoconsideration,forevenamodestproblem,giv-
inganexactanswerisofteninfeasible[14],leavealonesuchacomplicatedone. Furthermore,accord-
ingtoDan SmithandJanani Vivekananda[15],thereisatleastthreedimensions’ uncertaintyunder
thecontextofclimatechange’seffects:
1. Theprecisephysicaleffectsareuncertain,includingtheirscaleandgeography.
2. Theknock-onsocialconsequencesareuncertain.


## 第 9 页

Team#88902 Page6of24
精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
3. Thethirddimensionuncertaintyliesinthelackofclearandtestedpolicyprescriptionstoguide
theresponse.
Probabilisticnetworks(PNs),alsoknownasBayesiannetworks(BNs),arealreadywellestablished
as representations of domains involving such uncertain relations among a group of random vari-
ables[10],thereforebecomesaneligiblecandidate.Anotherreasonisthatthedataisseldomcomplete
inreallife,whichisalsowellsupportedbyprobabilisticmodelsbothintheoryandinpractice. More-
over,theseparationof knowledgeandreasoning[12]inprobabilisticmodelsdecouplesthesystem’s
overallcomplexity.
Figure4:Overviewofthe2THNmodel.
During our research, we found most of the models are either pure Bayesian networks or pure
Markovnetworksbutrarelyboth.Sowefeelitnecessarytodefendourchoiceofsuchahybridsys-
tem.Wehave knownthattheimpactbetweentheindicators aremutual andintricateandtheinner
structure can evenbecyclic.Hence, theimpactoneindicator imposes on theothers will eventually
and inevitably affect itself, which makes this problem problematic. Neither Bayesian networks nor
Markovnetworksalonecanmodelthepairwiserelationshipsandthetemporaldynamicssimultane-
ously,whichleadstoourhybridsystem-2THN.
In our model of 2THN, the dashed-lined area represents the template part, whose structure
will be replicated to other adjacent time slices. The original inspiration is the so-called 2-time-slice
bayesiannetwork(2TBN),whereallthelinksaredirectedandacyclic. Inordertocapturemoretraits
oftheinterconnectednatureofsuchafuzzysystem,wecombineitwithanotherprobabilisticgraph-
ical model, Markov network, which is undirected. The whole model can be taken into two parts -
inner-time-slice model and intra-time-slice model. The inner-time-slice model is used to analyze
theinstanteffectsandthesimultaneousrelationshipswithinourfour-indicatorfragilitymodelwhile
theintra-time-slicemodelisusedtoanalyzethetemporaleffectamongthefourdifferentindicators.
4.3.2 Assumptions
Tosimplifyourmodel,wemakethefollowingtwoassumptionsforthedirectedintra-time-slice
model:
1. MarkovAssumption
Because we decide to use a template model to make the model more general, we assume
the conditional probability distribution of future states of the process depends only upon the
presentstate,notonthesequenceofeventsthatprecededit[13].Thatis tosay,onceyouknow
the current state, you don’t care about the past anymore, therefore you forget about the past.
Specifically,thefragilityofthenextyearonlydependsontheenvironmentsofthecurrentyear
insteadof a trajectoryof thepastyears.This assumptioncanbe expressedprecisely usingthe
followingmathematicalexpressions:
Given:
(X(t+1) X(0:t−1) X(t))
⊥ |


## 第 10 页

Team#88902 Page7of24
精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Then:
whereXt istherandomvariables(nodes)intimeslicet.
2. TimeInvariance
Wefurtherassumethedynamicsofthesystemdon’tdependonthetimeinourmodel,which
istosay,forallgivent,wehave:
j
P(X(t+1) X(t)) = P(X X)
| |
j
where X denotes the next time slice and X denotes the current time slice, therefore we can
replicatethesamemodeltoeverytransitioninsteadofcreatingoneforeachofthem.
4.3.3 Precautions
An important parameter of our model is the time granularity ∆T . Weset it to one year for the
timebeinginordertomakeiteasiertogetvaliddata. Butthisintervalcanberesettoasmallervalue
ifenoughdatabecomesavailableinthefuture.
Anotherveryimportantpointworthcautionisthattheinner-time-slicemodelandtheintra-time-
slicemodelshouldneverbemixedupremissly.Thesetwopiecesaredesignedfordifferentdynamics
and different purposes. All models are wrong, but some are useful [9]. If you are mixing them up,
youareriskingconfusingthemapwiththeterritory.AsLeestatesinPlatoandtheNerd:
Modelsarehumanconstructions.Modelingparadigmsarealsohumanconstructions.
Therefore,botharesubjecttocreativity.Theyareinventednotdiscovered[8].
Therefore, models arealsosubjecttothecontextof theconcreteproblem.Hence, wewouldlike
torestatethesubtletyherealthoughmentionedpreviously:
1. InnerStructure-MarkovNetwork
In our model, it captures the intricate pairwise and simultaneous relationships between the
four indicators. It can be used to analyze the integrative node-node interactions without the
notionoftime,thereforetobetterunderstandthewholesystem.
2. IntraStructure-DynamicBayesianNetwork
Inourmodel,itmodelsthedynamicsofthesystemoveratimeseries. Itenablesustomonitor
and update the overall system as time proceeds, and make future predictions, which is the
centralmodelofthefollowingdiscussion.
4.3.4 InnerStructure-MarkovNetwork
We learned the following Markov network from data, representing the pairwise relationships
between the five indicators. The lines between the nodes denote the mutual interactions of these
indicators.
Foreachedgebetweentwoof thefiveindicators(Economic E, Cohesion C, Political P ,Social S
and CCIC CCIC) X, Y , there is an associated factor(aka. affinity function, compatibility function,
soft constraints) φ (X, Y ), which is a replacement of the conditional probability in a Bayesian net-
ij
work.Thefactor representsthelocal happiness of thevariable[12]X andY totakeaparticularjoint
assignment. Wecangetsuchfactorsthroughsomeparticularalgorithmswhichwillbeintroducedin
parameterestimation.
˜
Havingallthefactorsinourmodel,weareabletocalculatetheproductoffactorsP :
Φ


## 第 11 页

Team#88902 Page8of24
精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Figure5:Theinnerstructureof2THN.
(4)
whereωisthecoefficient,fisthefeaturefunctionandD isthejthfactor,e.g.(C,P),(S,E).Then
i
wecannormalizeitusing:
1
P(E,C,P,S,CCIC) = P ˜ (E,C,P,S,CCIC) (5)
Z Φ
whereZ iscalledthepartitionfunction:
Σ
Z = P˜ (E,C,P,S,CCIC) (6)
Φ
A relativelysubtlepointof theMarkov networkmodel isthatthereisn’t anatural mappingbe-
tweentheprobabilitydistributionandthefactors.Thismeans wehaveto explicitlyspecifythefac-
torizations. Here,weclaimthisnetworktobeapairwisenetworkinordertodoso. Notefurther,the
pairwisefactoriscommutativeinourmodel,sothereare7factorsintotalinthis network,listedas
follows:
(P, C); (C, S); (S, E); (E, CCI).
4.3.5 IntraStructure-BayesianNetwork
Tovisualizetheconditionaldependenciesacrosstimeslice,weusethedirectedacyclicgraph(DAG),
shownasFigure6:
Figure6:Theintrastructureof2THN.
ForeachnodeintheDAG,thereexistsaprobabilitydistributionfunction(pdf),whosedimension
anddefinition depends on theedges leading to that node. In our example,thedashed line denotes


## 第 12 页

Team#88902 Page9of24
精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
so-called "persistence link", which links the same node from t to t + 1(the unprimed node to the
primednode).Thesolidlinkdenotestheotherdependenciesbetweendifferentnodes.Thisstructure
is replicated for all the given time t to t + 1 while in this graph we only show 2 steps. So for a
i i
trajectoryover 0, 1, ..., T ,wecanthenunroll thetemplatenetworktoaflattenedgroundnetwork.
That is to say,we can, therefore, make predictions over an arbitrarily long time series using some
inferencealgorithms,whichenables us to getinsights of thedeep causal relationshipsamongthe5
elements.
ThejointprobabilitydistributionscanthenbecalculatedusingthechainruleaccordingtoEqua-
tion7.
j
whereX isthesetofrandomvariablesinthenexttimeslice,X istherandomvariablesinthe
j
currenttimeslice,andPa Xj isalltheparentsofX .
i
i
5 Parameter Estimation
Inthissection,howtodeterminetheweightofthe12fragilityindicatorsaswellashowthe
structureandparametersof2THNmodelaredeterminedareintroduced.
5.1 WeightCalculation
5.1.1 FormationOfindicatoreigenvaluematrixC
Supposethereareevaluatingindicatorscountedm,evaluatingobjectscountedn,thenformsthe
indicatoreigenvaluematrixC= (c )
ij m×n
wherec isthedataofthejthevaluatingobjectontheithindicator
ij
5.1.2 Calculatingtheentorpyofindicators
Informationentropyisthemeasurementofthedisorderdegreeofasystem[28].Whenthediffer-
ence of the value among the evaluating objects on the same indicator is high, while the entropy is
small, it illustrates that this indicator provides more useful information. On the other hand, if the
differenceissmallerandtheentropyishigher,theindicatorprovideslessusefulinformation.[29]
(9)
Inwhich,
wheree istheentropyoftheithindicator,e>0.
i i


## 第 13 页

Team#88902 Page10of24
精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
5.1.3 Thecoefficientofvariationofindicators
g =1 e
i i
−
whereg iscoefficientofvariation.Thelargertheg is,themoresignificanttheithindicatoristothe
i i
model.
5.1.4 Calculatingtheweightofentropy
(10)
wherew istheweightoftheithindicator.
i
If each evaluating object on theith evaluation indicator is exactly the same, the entropy reaches
the maximum value of 1 and the corresponding weight is 0, which means this indicator provides
nothingusefulforthedecisionmaker,thatistosay,itcanbeignored.Incontrast,ifeachevaluating
object varies on one indicator, then the entropy of the indicator is small and the weight is high,
indicatingthattheindicatorprovidesmoreusefulinformationandshouldbefocusedon.
5.1.5 Normalizationofindicatoreigenvaluematrix
Accordingtoaforementionedthreemethodsofdatanormalization,normalizeequation(8)toget
equation(11)
wherer isthedataofthejthevaluatingobjectontheithindicator,andr [0, 1].
ij ij
∈
5.1.6 FuzzyComprehensiveEntropyWeightMedol
Accordingtothedefinitionofmembershipmatrix,therelativeoptimalmembershipdegreevec-
torsofinferiorandsuperioronesarerespectively:
b = (0 0 0 0)T
···
h = (1 1 1 1)T
···
Theoptimalmembershipdegreeoftheevaluatingobjectis:
(12)
5.2 Parameters of2THN
Recallthatpreviouslywehaveintroducedtherepresentationofthe2THNmodel.butwehaven’t
divedintothedetailsofhowtoapplysuchmodelyet. Oneessentialworkofconstructingprobability


## 第 14 页

Team#88902 Page11of24
精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
networksistolearnitsparameters,includingitsstructureandconditionalprobabilitydistributions,
after which we can then conduct inference on the unknown data or updating the existing model.
Here we will briefly introduce the mechanisms of such process using the intra-time-slice Bayesian
network(figure6)asanexample,leavingouttheMarkovnetworktoavoidduplicates.


## 第 15 页

Team#88902 Page12of24
精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
5.2.1 Learning
Althoughextensiveresearcheshavebeendoneupontherelationshipsamongthefourindicators
andtheimpactofclimatechange[17,18,19,20],noneofthemconsideredallofthefiveasawhole.Fur-
thermore,accordingtothereportoftheClimateChangeandFragileStatesWorkshopheldonSeptember
28and29,2011[3],perfectknowledgeisnotavailable,especiallyincontextsoffragilityandit’sessen-
tialtostepbackfromourunderstandingsandassumptionsandthinkopenlyandholistically.
Learning the structure of the Bayesian network model that represents a domain can reveal in-
sights intoits underlyingcausal structure[21]whilelearningtheparameters canreveal thedetails of
howthenodesareconnected,whichexactlyembodiestheconceptsaddressedabove-tothinkopenly
andholistically.Anotherbenefitwecangetfromutilizingthisstrategyisthatcontinuouslyupdating
boththestructureandtheparametersbecomeseasy,makingitpossibleforthemodeltoevolveover
time with more and more data fed in. Hence, both the structure and parameters of our model are
learnedfromdata,concretely,weusethepgmpypythonlibrary[23]fortheimplementation.
StructureLearning Tosummarize,theoverallstrategyistouseascorefunctiontorateeachnet-
workandchoosetheonewiththebestscore.Giventhedataset ,thestructure ’sscoreis:
D G
P ( )P ( )
Score( , )=P ( )= D|G G
D G G|D
P( )
D
which is the posterior probability of given data . Note that the denominator is fixed for a
G D
givendataset,soourtaskreducestomaximizethenumeratorP( )P( ). Tofurthersimplifythe
problem,weassumeauniformpriordistributionoverP( )(seeHe D ck | e G rma G n[22]forotherdiscussions),
G
thereforeP( ) istheonlyoneleft:
D|G
wherepistheweightbytheposteriorprobabilityofallthepossibleparameters. Formultinomial
PDFs[16]:
whereα and N arethe hyperparameters, which counts for theprobability distribution func-
ijk ijk
tionofX forparentconfigurationj.
i
Thisprocesscanbecomplicatedfortwomainreasons:
(1) Difficultiesininferringcausality.
(2) Theexponentialnumberofdirectededgesthatarepossibleforagivendataset.
Totackle these problems, we choose to use Greedy Hill Climbing algorithm with a reduced
factorset(keeponly5elements). Butwhilewegainedbetterperformancethroughthisapproach,we
arealsofacedwiththeriskofgettingstuckinalocaloptimum,whichcanbewellsolvedbyapplying
randomrestarts.
Parameter Learning Parameter learning is relatively less problematic than structure learning, it is
similartomanycommonparametertrainingalgorithmsinthefieldofmachinelearning. Weusethe
normalizeddataasinput,thentrainthepreviouslyconstructednetworkusingMaximumLikelihood
Estimation(MLE[24])togettheconditionalprobabilitydistributionsofeveryrandomvariable.


## 第 16 页

Team#88902 Page13of24
精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
5.2.2 Inference
Ingeneral,acomputationofaprobabilityofinterestgivenamodelisknownasprobabilisticinfer-
ence[22]. Having thejoint distribution of X, in principle, we can compute any probability of interest
about X. Typically,we will be in a situation where some evidence is observed so that we can infer
something else about other variables. Generally, the queries can be expressed using the following
question: "What is the whole probability distribution over variable X given evidence e, P (X e)?[25]" Con-
cretely,giventhequeryvariablesX, observedevidenceE =e andunobservedvariable|sY:
which means to simply sum over all the variables not involved in the query. For other more
sophisticatedinferencemethods,seeButz,etal[27].
6 Analysis
6.1 Intuition
WecaneasilydrawthefollowingintuitiveconclusionsfrombothFigure5andFigure6:
1. CCICcanaffecteconomicdirectlysincetheyareconnecteddirectlyinbothgraph.
2. CCICcanaffectalltheotherthreeelementsindirectlythroughtheflowofinfluence.
These conclusions are rather intuitive, hence easy to understand. Wewill then try to justify the
aboveintuitionsusingsomeformalmethodsandgainfurtherunderstandingofthedynamicsofthis
system.
6.2 Posterior MeanValueAnalysis
Themostdirectwaytounderstandhowoneelementmayaffecttheotheristovisualizeit. Since
wealreadyconsideredthecountry’svulnerabilityinCCIC,wecanthensynthesizeallthe111coun-
tries’datatoconducttheposteriormeananalysis.
Theresultsofthefourindicatorsarerather
similar(Figure8).Fromthefourwiredcurves
causedbyCCIC,wecanseethatCCICisnotal- CCICMean
0.240 Variables
ways linearly correlated with the other four in- •Economic
0.230 •Social
dicators(recallthatCCICisconsideredtobethe •Political
•Cohesion
0.220
largerthebetter).Weinterpretthisphenomenon
0.210
bythefollowinghypothesis:
0.200
(1) Withina reasonable range, concretely(0, 0.190
0.2) in our model(we call it the Warn-ing 0.180
Zone(WZ)), CCIC can effectively pro- 0.170
moteordiminishalltheotherfourindica- 0.160
tors, whose impact can be approximately 0.150
consideredaspositivelylinear. 0.140
0.130-+----,------.------.---r----,------.----,---� ----------,
0.100.200.300.400.500.600.700.800.901.00
(2) After WZ, CCIC’s impact gradually re- VariableMeans
cedes,ultimatelyexercisesnoorevenneg-
ative impacts on the other four dimen-
Figure7:PosteriormeananalysisforCCIC.
sions’performance.


## 第 17 页

Team#88902 Page14of24
精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Wefurtherpostulatethatwhenglobalcli-
matechangedeterioratestoacertainextent,its
influencewillgraduallyemerge.Untilthen,theimpactisinvisibletopeople.Hence,wemustbe
aware of its presence and get ready to properly handle it. Another interesting point(the red outlier
line)liesinFigure7,wheretheredline(economic)becomesanoutlier.Itsslopeisslightlyhigherthan
theothers,whichcanbeexplainedbythedirectconnectionbetweenCCICandeconomic.
CohesionMean EconomicMean
0.80 0.80
0.75 • • S P o o c li i t a ic l al 0.75 • • C Po C l I i C tical
0.70 • •C Ec C o IC nomic 0.70 • • C So o c h i e a s l ion
0.65
0.65
0.60
0.60
0.55
0.50 0.55
0.45 0.50
0.40 0.45
0.35
0.40
0.30
0.35
0.25
0.30
0.20
0.15 0.25
0.104---�----��-�--�--�----r--- ---------, 0.20 -4------..----�-�--�--�----.----,----..------,
0.000.100.200.300.400.500.600.700.800.901.00 0.00 0.10 0.20 0.30 0.40 0.50 0.60 0.70 0.80 0.90 1.00
VariableMeans VariableMeans
PoliticalMean SocialMean
0.90 0.70
•Economic •Cohesion
•Cohesion 0.65 • • C Po C l I i C tical
0.80 •CCIC •Economic
•Social 0.60
0.70 0.55
0.50
0.60
0.45
0.50
0.40
0.40 0.35
0.30
0.30
0.25
0.20
0.20
0.104---�----��-�--�--�----r--- ---------, 0.15
-+---�--�-��-�--�--�--�--�--�-�
0.00 0.10 0.20 0.30 0.40 0.50 0.60 0.70 0.80 0.90 1.00 0.000.100.200.300.400.500.600.700.800.901.00
VariableMeans VariableMeans
Figure8:Posteriormeananalysisforthe4indicators.
6.3 Other Analysis
Wealso conducted other analysis to our model, including both statistical methods(correlation,
etc.) and information-theoretical methods(mutual information, Entropy,etc.), shown in Table1, Ta-
ble2,fromwhichwecanseethatthebondbetweenCCICandeconomic is weakerthantheothers.
This is reasonable to some extent. But it may also indicate that not enough evidences are provided
toconvinceourselvesthatclimatechangecanactuallyhaveagreatimpactonacountry’seconomic
system. With more data, the actual bond may gradually emerge, and presumably become strong
thanthecurrentone. Moreover,otherbondsotherthanthecurrentsetarealsopossibletoemergein
thefuture.
7 Task1: Models and Standard Lines
7.1 Determine the standard line byK-Means ClusteringAlgorithm
After all the four indicators of WFSI for a country have been calculated, we still don’t have a
qualitative concept about the country’s current state. Fragile? Vulnerable? Or stable? Therefore, K-
Meansclusteringalgorithm[36]isadoptedtosetastandard.


## 第 18 页

Team#88902 Page15of24
精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
KL Mutual Consistency
Divergence information Estimate
Sum 3.3175 3.3175 3.3175
Mean 0.8294 0.8294 0.8294
Standard Deviation 0.3377 0.3377 0.3377
Table1:Overallmetrics.
Symmetric Symmetric
Parent Child
Dive
K
rg
L
ence
R
W
e
e
la
ig
ti
h
v
t
e
Co
O
nt
v
r
e
ib
r
u
a
t
ll
ion inf
M
or
u
m
tu
a
a
ti
l
on
No
M
rm
ut
a
u
li
a
z
l
ed R
M
e
u
la
tu
ti
a
v
l
e GKL-test G
(D
-
a
te
ta
s
)
t
C
P
o
e
r
a
r
r
e
s
la
o
t
n
io
's
n
Information Information
Political Cohesion 1.1556 1.0000 34.8327% 1.1556 34.7862% 40.9864% 983.6067 983.6067 0.9053
Economic Political 0.9829 0.8506 29.6288% 0.9829 29.5893% 34.3695% 836.6590 836.6590 0.8754
Cohesion Social 0.9143 0.7912 27.5612% 0.9143 27.5244% 31.2598% 778.2728 778.2728 0.8142
CCIC Economic 0.2646 0.2290 7.9774% 0.2646 7.9667% 9.0010% 225.2653 225.2653 0.2602
Table2:Metricsfornode-noderelationship.
One drawback[37] to the algorithm occurs when it is applied to datasets with m data points in
n 10 dimensional real space Rn and the number of desired clusters is k 20. In this situation, theK-
M≥eans algorithm often converges with one or more clusters which are ei≥ther empty or summarize
very few data points (i.e. one data point). However, our model has only four dimensions and K,
whichdenotesthenumberofclusters,is3inourmodel.So,KAissuitableforourmodel.
GivenadatasetsD ofm pointsinRn andclustercentersC1,t, C2,t, . . . , Ck,t atiterationt,compute
C1,t+1, C2,t+1, . . . , Ck,t+1 atiterationt +1inthefollowing2steps:
1. ClusterAssignment. Foreachdata record xi D, assign xi to cluster h(i) such that center
Ch(i),t isnearesttoxi inthe 2-norm. ∈
2. ClusterUpdate.ComputeCh,t+1 asthemeanofallpointsassignedtoclusterh.
StopwhenCh,t+1 =Ch,t, h =1, . . . , k,elseincrementtby1andgotostep1.
AftertrainingaK-Meansmodelusingthedatawehave,wefinditperformswellasisshownin
Figure9.
Becausewehavefourdimensions,whichcan’tbeshowninonlyonefigure. Hence,wedraweach
threeofthemforonetimeinafigure,afterwhichwegetthesefourfigures.
7.2 Identifying the Impact of ClimateChange
Pleasesee6.1and6.2.
8 Task2: Case Study - Sudan
Amongall of thetop 10most fragilestates,wecanonlygetthedataof IraqueandSudan.Con-
sideringtheextensivechaosandwarsinIraque,wefinallychoseSudan.
Conductingcausalityinferenceinprobabilisticmodelsarerathereasy.Accordingtoourdata,we
provideourmodelwithanewpieceofevidence:
P (0.067 CCIC 0.091)=1
≤ ≤
Wethen calculate the probability of other variables accordingly,the original and post-evidence
results are shown in the same graph(Figure 10) for the purpose of comparison. It is obvious that
CCIC can result in a high probability of low score in all the other four variables without other ex-
ternalintervention,especiallyeconomic. Hence,wecanconcludethatclimatechangecanmakethe


## 第 19 页

Team#88902 Page16of24
精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Figure9:K-MeansModelResults
badsituationevenworse,throughdirectlyweakenonecountry’seconomicsystemandindirectly
influencealltheothervariables.
Therefore,ifweconverselysetCCICtobegreaterthan0.38,itwouldresultinahigherprobability
of high score in all the other variables, therefore leading to a less fragile state. For more concrete
strategiesinordertoeasethefragilityofSudan,seesection10.
Figure10:ImpactofCCIC.
9 Task3: Case Study - Greece
9.1 WFSI and CCIC forGreece
Greece is chosen to be evaluated by our model. Firstly, we get the WFSI and CCIC scores for
Greecefrom2008to2012asshownbelowinFigure11.NotethateachscoreofGreeceisbelow0.35


## 第 20 页

Team#88902 Page17of24
精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
andthechangesbetweenyearsaresmall,sowesettheradarchartboundaryto0.35tobettershow
thetrendofthechanges.
Figure11:WFSIandCCICforGreecefrom2008to2012
Thedetails for each year is shown in Table3. In these fiveyears, Greece stays in thevulnerable
state.
Year CI EI PI SI CCIC Category
2008 0.34311201 0.30068317 0.32482785 0.33128552 0.110295 vulnerable
2009 0.33108916 0.28565486 0.3052545 0.28280523 0.119507 vulnerable
2010 0.3177221 0.31542998 0.27146437 0.30181049 0.081737 vulnerable
2011 0.32430351 0.3477323 0.27657189 0.26598385 0.086050 vulnerable
2012 0.30322494 0.29910825 0.29347285 0.32876026 0.095530 vulnerable
Table3:WFSIandCCICforGreecefrom2008to2012.
Thedataabovesuggeststhat,althoughthecurrentstatusofGreeceisacceptable,theFSIscoresof
itisgraduallyreducing. Especially,thecohesionindexandpolicyindexdeclineobviously.Althoughin
2008theGreekeconomywasregardedasthe27thlargesteconomy[38]oftheworldbynominalGross
Domestic Product (GDP) with 32,100 USD GDP per capita[39], as a corollary of the international fi-
nancialcrisisandthelocalunrelentingspending,Greekcitizensstartedfacingserioussocioeconomic
turmoil. In 2009, the economic crisis impinged on a greater proportion of the population, whereas
in 2010 a Memorandum of Economic and Financial Policies was signed in order to avert Greece’s
default.Thesameyear,nationalestimatesshowedthatGDPdroppedto-3.5%,whileunemployment
rates reached as high as 14.2%, with 180,000 people losing their jobs[40]. In 2011, the profile of the
Greekeconomyappearsthegloomiestofthedecade: GDPfurtherdeclinedto-6.1%,whereasunem-
ploymentrates increasedfrom6.6%in May2008to16.6%in May2011.Concomitantly,throughout
the same period, the debt has grown from 105.4% in 2007 to 160.9% of GDP in 2011 (239.4 billion
eurosto328.6billioneuros)[41].
9.2 Prediction forGreece
Using the model 2THN, we predict the future status of Greece, shown in Figure 12. The detail
predictingdatafrom2013to2017isshowninTable4.
Year CI EI PI SI Category
2013 0.32372539 0.27658597 0.30632332 0.34520463 vulnerable
2014 0.27213682 0.23103887 0.25672303 0.38824761 vulnerable
2015 0.27160032 0.26766136 0.25412672 0.46719683 vulnerable
2016 0.24880141 0.24614655 0.2126675 0.444723410 fragile
2017 0.27053746 0.26077977 0.18593567 0.24906261 fragile
Table4:WFSICforGreecefrom2013to2017.


## 第 21 页

Team#88902 Page18of24
精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Figure12:WFSIforGreecefrom2008to2017
Franklyspeaking,thewiredpeakinourpredictionresultsarenotveryeasytointerpret.Presum-
ably,thereasonsmaylieinsidethecomplexblackboximplementationofourmodel,whichformsa
weakpointofourmodel.
Despite the absence of the full understand of the result, in order to get the tipping point, we
retrievethecenterofthethreeclustercalculatedbyKA(seesection7.1formoreinformation),which
respectivelyare:
[0.7146366, 1.48168573, 2.62917114]
Then we calculate the mean of the two smaller values as the tipping point. Wecan then draw
the conclusion from Table 4 that Greece may turn to fragile state in 2016. Among the four index,
the policy index and social index fluctuate wildly while the social index even plays a decisive role of
Greece’sturningbacktofragilestate.
10 Task4: Possible Strategies
Climatechangeisa globalissue(fixedCCI),whichis hardtobeadjustedbyonlyonecountry’s
efforts. However, we can find a breakout according to our model - CCV can differ from country
to country, which makes it possible to mitigate the risk of climate change by launching particular
policiesonastatelevel. BasedontheindicatorsthatformCCV,wecanreduceCCVfromsixequally
weighteddimensionsaccordingtoNG-GAIN:food,water,health,ecosystemservices,humanhabitat
andinfrastructure.
WeagaintakeSudanasanexample,theproposedstatedriveninterventionsinTable5mayhelp
to increaseits resilience to climatechange, therefore help to preventit frombecoming aeven more
fragilestateunderthesevereclimatechange.
NotethatitisimpossibleforustodiminishCCVdowntozero. Soinordertosetarealisticgoal,
we roughly recommend some percentages based on thecurrent speed of development[43]. And the
estimated costs of the interventions are given by consulting the Expenditure Review of Sudan[42],
combinedwiththegoalsofinterventionsaspercentages.
11 Task 5: ScalabilityAnalysis
Ourmodelsareoriginallybasedonnationallevel,whicharerelativelyindependententities.We
find that continents are more similar to countries than cities from the perspective of independence
level.Sowepostulatethatourmodelcanbescaledtocontinentsundersomeadjustmentsbutprob-
ablynotcities.
To simplify the problem, we simply average the WFCIs for all countries on a single (modi-
fied)continentdirectlytogetthenewWFCIs(WeightedFragileContinentIndex)andthenvisualize
them,asshowninFigure13(Thegrayareameansthatwehavenodataofit).


## 第 22 页

Team#88902 Page19of24
精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
SubIndicators Value Interventions EstimatedCost
ProvidefarmerswithsupportonFertilizer,Irrigation,Pesticide,
Food $8million/year
0.739 Tractorusetoincreaseyieldby10 everythreeyear.
Introducetechnologytobuilddamoramplifydamcapacity.
Water 0.691 $3million/year
Increasecleanwaterstorageby6everythreeyear.
Spendmorebudgetonmedicalstaffstoreducethedeathsfrom
Health 0.709 $2million/year
climatechangeinduceddiseasesby8everythreeyear.
Enactmorestrictpoliciestoprotectbiomesandreducethe
Ecosystem 0.661 $80,000/year
vulnerabilityscoreintermsofecosystemby1everyyear.
Improvethequalityoftradeandtransportespeciallypaved
Habitat 0.547 $500,000/year
roadstoreducethehabitatindexby2everythreeyear.
Putmoreeffortintodisasterpreparednesstoreducethe
Infrastructure 0.337 $600,000/year
damageofdisasterby1everythreeyear.
AllinterventionsabovetrytoreduceCCVtoimprovethe
CCV 0.620 $14.18million/year
climatechangeresilienceofSDN(CCIC=(1-CCV)*CCI)
Table5:ProposedsolutionstoSudan’scase.
(a) ClimateChangeIndexbyCountry. (b)WeightedFragileContinentIndex.
Figure13:Resultswithcontinents.
Notethatwedidn’tusethegeographical"continent"asdefinedinWikipedia.Instead,wemade
someadjustmentstothe"structureoftheworld",notablyweputtheareainthesouthoftheU.S.as
awhole(LatinAmerica).Thisisbecausethattheeconomicandsocialenvironmentofthesecountries
differtoomuchfromtheU.S.andCanadadespitethefactthattheyareinthesamecontinent.Fora
counterexample,pleasefindAustraliainbothgraphsandmakeacomparison. Themodelingresult
isnotveryidealsinceAustraliashouldhavehadaveryhealthyscore.Theproblemliesintheweak
clusterstrategy,whichcouldbesolvedbysplittingcountrieslikePapuaNewGuineatotheSoutheast
Asia.Afterfurtherresearch,weeventuallydrawthefollowingconclusions:
1. Our model can be applied to continents if proper adjustments(such as re-clustering) over the
definition of the term "continent" are made. Concretely, the adjustments should take the eco-
nomic,socialandpoliticaldifferenceamongtheclusteredcountriesintoconsideration.
2. Theprobabilityofourmodel’sapplicationoncitiesisremoteunlesswesubstitutethe5major
indicatorswithsomere-designedindicatorsandre-weightthemaccordingly.Thereasonsliein
theshrinkofthe"granularity"oftheproblem,makingithardertopredicttheoverallsystem’s
performance.Asaresult,moresophisticatedmodelsarerequiredinsteadofasimple5-element
network.


## 第 23 页

Team#88902 Page20of24
精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
12 Strengths and weaknesses
Generallyspeaking,ourmodelisdesignedforaveragecountries.Onecountrycanusethismodel
toguideitsdirectionofdevelopmentbyconductinginferenceonthetrainednetwork.
12.1 Strengths
1. Robustnessandflexibility.
Thefundamentalstrengthofourmodelcomesfromitsenormousflexibility,wherenoneofthe
parameters in our model is fixed, even the structure of the network. And since that all the
parametersarelearnedfromdata,ourmodelisveryeasytobecustomized,thereforecouldbe
appliedwidely.Ourmodelalsoincorporatestheideaofbigdata. Thatistosay,withmoreand
moredata(evidence),ourmodelcangivemoreandmoreprecisepredictions.Furthermore,our
modelhasthenotionoftime,whichisomittedinmostmathematicalmodels.
2. Combinationofdataandexpertknowledge.
Besideseffectivelyutilizingthedata,ourmodelalsotakesadvantageoftheexpertknowledge
when determining the weights(AHP) and constructing the network. This gives our model a
seconddimension’sinsight.
3. Easytounderstand.
Adoptingahierarchicalstructure,ourmodelcanbeeasilyunderstoodwithasinglegraphand
several lines of explanation, see Figure 1. Hence, our model is more likely to be understood
by the decision and policy makers with the presence of their knowledge gap in the complex
interconnectedsystem.
12.2 Weaknesses
1. Potentialvulnerabilityduetothelackofdata.
Thefundamental weakness of our model also comes from data. Since our model is so depen-
dentondata,itislikelytobeuselesswhenconsideringcountriesinabnormalsituations,such
aslarge-scalewarsandnaturaldisasters.
2. Potentialinvalidassumptions.
Anotherobstaclethatmayholdbackourmodel’sperformanceisthattheassumptionsmadeto
simplifythe model may be invalid, therefore leading to a less useful model. For example, the
fragilityof onecountrymay depend on otherfactors otherthanthe4 factors identifiedbyus.
Ourmodelmayalsofailtogivereasonableresultswhenencounteringsomeabnormalcases.
3. Potentialabnormalphenomenons.
Duetotheinternalcomplexityoftheinherentstructureof2THN,someoutcomesofourmodel
may be hard to interpret(see section 9.2), which is also the drawback of many other machine
learningapproachessuchasneuralnetworks. (Notethattheinternalcomplexitydoesn’tneces-
sarilyconflictwithitscomprehensibilityforthatitcanbetreatedasablackbox.)


## 第 24 页

Team#88902 Page21of24
精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
References
[1] Wijeyaratne,S.(2009).Fragileenvironment,fragilestate:Conflict,crisisandclimatechange.
[2] Crawford, A., DazÃl’, A., Hammill, A., Parry, J., & Zamudio, N. (2015). Promoting climate-
resilientpeacebuildinginfragilestates.Geneva:InternationalInstituteforSustainableDevelop-
ment(IISD).
[3] Climate Change and Fragile States Workshop report. (n.d) Retrieved Feb 10, 2018,
from
https://reliefweb.int/sites/reliefweb.int/files/resources/Climate_
Change_and_Fragile_States_Workshop_Report.pdf
[4] Mason, S., Kruczkiewicz, A., Ceccato, P.,& Crawford, A. (2015). Accessing and using climate
data and information in fragile, data-poor states. International Institute for Sustainable Devel-
opment:Winnipeg,MB, Canada.
[5] Edenhofer,O.,&Seyboth,K.(2013).Intergovernmentalpanelonclimatechange(IPCC).
[6] Chen, C., Noble, I., Hellmann, J., Coffee, J., Murillo, M., & Chawla, N. (2015). University of
NotreDameGlobalAdaptationIndexCountryIndexTechnicalReport.ND-GAIN:SouthBend,
IN,USA.
[7] Burck,J.,Bals,C.,&Ackermann,S.(2009).Theclimatechangeperformanceindex:background
andmethodology.Germanwatch.
[8] Lee,E.A.(2017).Platoandthenerd:thecreativepartnershipofhumansandtechnology.
[9] Box,GeorgeE.P.;NormanR.Draper(1987).EmpiricalModel-BuildingandResponseSurfaces,
p.424,Wiley.ISBN0471810339.
[10] Mihajlovic,V.,&Petkovic,M.(2001).Dynamicbayesiannetworks:astateoftheart.Epl.
[11] Simon.(2011).Probabilistic graphical models:principles and techniques bydaphne koller and
nir friedman, mit press, 1231 pp. $95.00, isbn 0-262-01319-3. Knowledge Engineering Review,
26(2),237-238.
[12] Koller,D.,&Friedman,N.(2009).Probabilisticgraphicalmodels.ProbabilisticGraphicalMod-
els.SpringerInternationalPublishing.
[13] Markovproperty.(n.d.)InWikipedia.RetrievedFeb10,2018,from
https://en.wikipedia.
org/wiki/Markov_property
[14] Jaimovich,A.(2010).UnderstandingProtein-proteinInteractionNetworks(Doctoraldisserta-
tion,HebrewUniversity).
[15] Dan,S.,&Vivekananda,J.(2009).Climatechange,conflictandfragility.
[16] Cooper,G.F.,&Herskovits,E.(1992).Abayesianmethodfortheinductionofprobabilistic
networksfromdata.MachineLearning,9(4),309-347.
[17] Woolcock,M., & Ritzen, J. (2010). Social cohesion, public policy and economic, growth: impli-
cations for countries. The Contribution of Human and Social Capital to Sustained Economic
Growth and Well-being: International Symposium Report, Human Resources Development
CanadaandOECD.
[18] Carvajal,L.(2007).Impactsofclimatechangeonhumandevelopment.(49).
[19] Gelsdorf,&Kirsten.(2010).Globalchallengesandtheirimpactoninternationalhumanitarian
action.


## 第 25 页

Team#88902 Page22of24
精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
[20] Dziembala,Malgorzata.(2016).Someconsiderationsontherelationshipbetweeneconomicand
social cohesion and implementation of the cohesion policy. Perspectives on Federalism, 8(1),
53-80.
[21] Margaritis, D. (2003). Learning bayesian network model structure from data /. Learning
BayesianNetworkModelStructurefromData.
[22] Heckerman, D. (1995). A tutorial on learning with bayesian networks. Learning in Graphical
Models,25(4),33-82.
[23] Ankan, A., & Panda, A. (2015). Mastering Probabilistic Graphical Models using Python. Packt
Publishing.
[24] Edgeworth, Francis Y.(Sep 1908). "On the probable errors of frequency-constants". Journal of
theRoyalStatisticalSociety.71(3):499-512.doi:10.2307/2339293.JSTOR2339293.
[25] Inference in Bayesian Networks. (n.d.) Retrieved Feb 10, 2018, from
https:
//ocw.mit.edu/courses/electrical-engineering-and-computer-science/ 6-
825-techniques-in-artificial-intelligence-sma-5504-fall-2002/
lecture-notes/Lecture16FinalPart1.pdf
[26] Climate change, fragility and conflict. (n.d.) Retrieved Feb 10, 201, from
http://www.
.
international-alert.org/projects/13624
[27] Butz,C.J.,Oliveira,J.D.S.,&Madsen,A.L.(2014).BayesianNetworkInferenceUsingMarginal
Trees.ProbabilisticGraphicalModels.SpringerInternationalPublishing.
[28] MengQS,1989.Informationtheory[M].Xi’An:Xi’AnJiaotongUniversityPress.19-36.
[29] Zou,Z.H.,Yi,Y.,&Sun,J.N.(2006).Entropymethodfordeterminationofweightofevaluating
indicatorsinfuzzysyntheticevaluationforwaterqualityassessment.JournalofEnvironmental
Sciences,18(5),1020-1023.
[30] GlobalData|FragileStatesIndex.RetrievedFeb9,2018,form
http://fundforpeace.org/
fsi/data/
[31] WorldBank,2018.RetrievedFeb9,2018,form
http://climatedataapi.worldbank.org/
climateweb/rest/v1/country/cru/tas/year/ISO3.csv
[32] WorldBank,2018.RetrievedFeb9,2018,form
http://climatedataapi.worldbank.org/
climateweb/rest/v1/country/cru/pr/year/ISO3.csv
[33] World Development Indicators, 2018. CO emissions (metric tons per capita)
2
(EN.ATM.CO2E.PC). Retrieved Feb 9, 2018, form
http://databank.worldbank.org/
data/reports.aspx?source=world-development-indicators&preview=on
[34] World Development Indicators, 2018. Arable land (% of land area)(AG.LND.ARBL.ZS). Re-
trieved Feb 9, 2018, form
http://databank.worldbank.org/data/reports.aspx?
source=world-development-indicators&preview=on
[35] Enviroment Performance Index, 2018. Retrieved Feb 9, 2018, form
http://archive.epi.
yale.edu/downloads
[36] Duda, R. O.,Hart, P.E., & Stork, D. G.(1995). Pattern classification and sceneanalysis 2nded.
ed:WileyInterscience.
[37] Bradley, P.S., Bennett, K. P.,& Demiriz, A. (2000). Constrained k-means clustering. Microsoft
Research,Redmond,1-8.


## 第 26 页

Team#88902 Page23of24
精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
[38] Economou, M., Madianos, M., Peppou, L. E., Patelakis, A., & Stefanis, C. N. (2013). Major de-
pression in the era of economic crisis: a replication of a cross-sectional study across Greece.
Journalofaffectivedisorders,145(3),308-314.
[39] Eurostat,2010.ReportoftherevisionoftheGreekGovernmentdeficitanddebtfigures.
http:
.
//epp.eurostat.e.c.europa.eu/cache/ITY
[40] BankofGreece,2010.AnnualReports.B.G.PrintingOffice,Athens.
[41] Eurostat,2011.EuroAreaandEU27GovernmentDeficitat6.0%and6.4%ofGDP,reespec-
tively.Eurostat,Luxembourg.
[42] SUDAN State-level Public Expenditure Review, (May 2014), Retrived Feb 11, from
https://openknowledge.worldbank.org/bitstream/handle/10986/23505/
Synthesis0repo0ary0for0policymakers.pdf?sequence=1&isAllowed=y
[43] Sudan:TheLandandthePeople,(n.d.),RetrivedFeb11,from
http://www.sd.undp.org/
content/sudan/en/home/countryinfo.html#Human


## 第 27 页

Team#88902 Page24of24
精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Appendices
import numpy as np
import pandas as pd
class Data:
def init (self, data_filepath, from_year=2006, to_year=2012,
reassign_value=0.0001):
self.data_filepath = data_filepath
self.from_year = from_year
self.to_year = to_year
self.reassign_value = reassign_value
@staticmethod
def _entropy_method(C):
P = C / np.sum(C, axis=0)
e_i = - (1.0 / np.log(C.shape[0])) * np.sum(P * np.log(P), axis=0)
g_i = 1 - e_i
w_i = g_i / np.sum(g_i)
R_i = np.min(C, axis=0) / C
return np.sum(w_i * R_i, axis=1)
def _CCI_entropy_method(self, C): C[:,
0] = np.min(C[:, 0]) / C[:, 0]
C[:, -1] = C[:, -1] / np.max(C[:, -1])
# reassign zero value to reassign_value
for k in range(C.shape[0]):
for j in range(C.shape[1]):
if C[k, j] == 0:
C[k, j] = self.reassign_value
P = C / np.sum(C, axis=0)
e_i = - (1.0 / np.log(C.shape[0])) * np.sum(P * np.log(P), axis=0)
g_i = 1 - e_i
w_i = g_i / np.sum(g_i)
return np.sum(w_i * C, axis=1)
def get_data(self, norm=False):
country_data = {}
data = []
fsi_file_path = self.data_filepath + "fsi-{}.xlsx"
df = pd.read_excel(fsi_file_path.format(2017))
countries = set(df["Country"])
for i in range(6, 13):
year = 2000 + i
file_path = fsi_file_path.format(year)
df = pd.read_excel(file_path, index_col=0)
before_keys = list(df.keys())
temp = np.array(df.iloc[:, 3:])
cohesion_index = self._entropy_method(temp[:, 0:3])
economic_index = self._entropy_method(temp[:, 3:6])
political_index = self._entropy_method(temp[:, 6:9])
social_index = self._entropy_method(temp[:, 9:12])
df["cohesion_index"] = cohesion_index
df["economic_index"] = economic_index
df["political_index"] = political_index
df["social_index"] = social_index
df = df.drop(before_keys, axis=1)
data.append(df)


## 第 28 页

Team#88902 Page25of24
精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
for country in countries:
country_data[country] = []
for year_data in data:
if country in year_data.index:
country_data[country].append(list(year_data.ix[country]))
country_data[country] = np.array(country_data[country])
df = None
for i in range(6, 13):
year = 2000 + i
file_path = self.data_filepath + "CCI-" + str(year) + "-normalized.csv"
if df is None:
df = pd.read_csv(file_path)
else:
df = df.append(pd.read_csv(file_path), ignore_index=True)
temp = np.array(df.iloc[:, 1:])
CCI = self._CCI_entropy_method(temp)
CCI_country_name = set(df.iloc[:, 0])
df["CCI"] = CCI
df = df[["Country", "CCI"]]
df_vulnerability = pd.read_csv(self.data_filepath + "vulnerability.csv",
index_col=1)
result = []
for country, C in country_data.items():
if country in CCI_country_name:
N = np.array(df_vulnerability.loc[country])[-11:-4]
M = np.array(df[df["Country"] == country].iloc[:, -1])
# compute CCIC
M = M * (1 - N)
for j in range(0, C.shape[0] - 1):
before_year = list(C[j, :])
now_year = list(C[j + 1, :])
before_year.append(M[j])
before_year.extend(now_year)
before_year.append(M[j + 1])
result.append(before_year)
# data discretization
result = np.array(result) * 20
X = np.array(result, dtype=np.int)
if norm:
return X / np.max(X, axis=0)
else:
return X

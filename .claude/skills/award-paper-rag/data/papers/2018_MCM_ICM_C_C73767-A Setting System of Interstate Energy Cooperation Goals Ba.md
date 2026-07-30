# C73767-A Setting System of Interstate Energy Cooperation Goals Based on Data Insight


## 第 1 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team Control Number
Forofficeuseonly Forofficeuseonly
73767
T1 F1
T2 F2
T3 ProblemChosen F3
T4 C F4
2018
MCM/ICM
SummarySheet
A Setting System of Interstate Energy Cooperation
Goals Based on Data Insight
Summary
Afterperformingdataanalysisandmodeling,wefinallydetermineasetofdevelop-
mentgoalsforthenewfour-stateenergycompact.
First,wepreprocessthedataprovided,whichincludesdefaultvalueprocessing,ab-
normalvalueprocessanddataclassification. Forthesakeofanalysis,wedividevarious
energy into two broad categories. One is cleaner renewable energy (CRE), the other is
traditionalfossilenergy(TFE).Afterthat,weselect11importantvariablesfromthegiven
data to create the energy profile for each of the four states. Wecall the 11 variables the
basicvariables
Next, we apply the decoupling theory to characterize the dynamic relationship be-
tweeneconomicdevelopmentandenergyutilization,whichcanreflecttheevolutionof
energy profile. Wefind that the four states differ in production and usage of various
energysignificantly.Todeterminetheunderlyingfactorsthatleadtothedifferences,we
constructthesimultaneousequationsmodel. Combiningnaturalenvironmentinforma-
tionfurther,wefindoutthefactorsandknowtherespectivestrengthsofthefourstates
inCRE.
Then, we establish a multi-dimensional evaluation system to identify the state that
has the“best”energy profile on the whole. We introduce the index, comprehensive
utilization performance (CUP) to measure the energy profile. The CUP is composed of
threeparts,energyperformance,economicperformanceandenvironmentperformance.
Andeachofthethreepartsincludesthreeindexesrespectively,allofwhicharesynthe-
sized by thebasic variables. Weuse the PCA method to integrate thenine indexes into
anoverallindex,namelytheCUP.RankingCUP,wefindthatCaliforniaisthe“best”.
Finally, we construct BP neural network to predict the energy profile. Analogous
to Cobb-Douglas Production Function in economics, we define the CUP in a new way
for predicting. Through setting various development scenarios, we get the predictions
successfully. After that, we regard the four states as a whole to determine renewable
energy usage targets for 2025 and2050. In this process, we use theBP neutral network
andpreviousmodelsagain.Wecollectrealdatafrom2010to2015tocalculatethevalues
ofCUP.Comparethemtothepredictedvalue,wetestourpredictingsystem. Theresult
showsthatourpredictingsystemworkswell.


## 第 2 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#73767 Page1of28
Contents
MEMO 3
1 Introduction 4
1.1 ProblemStatement......................................................................................................4
1.2 OurGoals......................................................................................................................4
1.3 OurThinking................................................................................................................4
2 AssumptionsandNotations 5
2.1 Assumptions.................................................................................................................5
2.2 Notations.......................................................................................................................6
3 DataPreprocessing 6
3.1 DefaultValueProcessing............................................................................................6
3.2 AbnormalValueProcessing.......................................................................................6
3.3 DataSynthesisandClassification.............................................................................7
4 EnergyProfile 7
5 ModelConstruction 10
5.1 DecouplingAnalysis.................................................................................................10
5.2 TheSimultaneousEquationsModel.......................................................................10
5.3 TheMulti-dimensionalEvaluationSystem...........................................................12
5.3.1 ConstructionofIndexes...............................................................................12
5.3.2 PrincipleComponentAnalysis...................................................................13
5.4 EnergyProfilePredictingSystem............................................................................14
5.4.1 DeterminingthePredictors.........................................................................14
5.4.2 ConstructingBPNeuralNetwork..............................................................15
5.4.3 AnalyzingtheError......................................................................................17
5.4.4 PredictingtheTargetValues........................................................................17
6 TestingOurModel 19
6.1 PredictingReliabilityTest.........................................................................................19
6.2 SensitivityAnalysis...................................................................................................19
7 DeterminingGoalsfortheEnergyCompact 20
7.1 Ideaone: Don’tcooperate........................................................................................20
7.2 Ideatwo: Cooperate..................................................................................................20
7.3 GoalsandActions......................................................................................................20


## 第 3 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#73767 Page2of28
8 Conclusions 21
9 StrengthsandWeaknesses 21
9.1 Strengths.....................................................................................................................21
9.2 Weaknesses.................................................................................................................22
References 22
Appendices 23
AppendixA ProfilesofArizona 23
AppendixB Profileof NewMexico 25
AppendixC ProfilesofTexas 25


## 第 4 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#73767 Page3of28
MEMO
From:Team73767,MCM2018
To:ThegroupofGovernors
Date:February13,2018
Subject:Goalsfortheinterstateenergycompact
Dear governors, we are honored to inform you our achievement after performing
dataanalysisandmodeling.
First,weintroducetheenergyprofilesofyourstatesin2009. Weusecomprehensive
utilization performance (CUP) to reflect the energy profile on the whole. Ranking the
CUP of your four states, California appears to be the best. In terms of the usage of
cleaner renewable energy, California, Arizona, Texas and New Mexico has the largest
consumption successively in the water power, nuclear power, wind power and solar
power.Itis decidedby thenatural environment of your four states,such as geography
andclimate.
Then,weprovideyouthegoalsfortheinterstateenergycompact.Throughpredict-
ing,yourfourstates’averageCUPwillincreaseto16.98by2025andto26.05by2050,if
yourfourstatescancooperateadequately.Basedonthepredictions,wesetthedevelop-
mentgoalsasfollows:
• Buildingacommunityofenergyutilizationandeconomicdevelopment,soasto
realizemanualbenefitandwin-winresult.
• Promotingtheproductionandusageofnewenergysourcesandreducingthede-
pendenceontraditionalfossilfuels.
• Increasing the whole economy’s comprehensive utilization performance to 16.98
by2025andto26.05by2050,andachievingtheharmonyofeconomy,energyand
environmentultimately.
According to thegoals above and the characteristics of each of your four states, we
offeryouthefollowingsuggestionstomeetthegoals.
• Buildinganenergyinvestmentbanktointegratemoneyfordevelopingtheclear
renewableenergy.
• Enhancingresiduals’environmentalprotectionconsciousness.
• Adjustingtheindustrialstructureproperly.
Wesincerelyhopethatyoucanachievethegoalsabove!
Pleasecontactusifyouhaveanyproblems.


## 第 5 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#73767 Page4of28
1 Introduction
1.1 ProblemStatement
Energyisthemainmaterialbaseanddrivingforceforhuman’sdailyproductionand
life.Theproper utilizationof allkindsof energyarecloselylinkto thesustainabilityof
economic development. The excessive consumption of traditional fossil fuels not only
restrictstheeconomicdevelopment,butalsocausesaseriesofenvironmentalproblems,
such as global warming. Therefore, in America, many states have been trying to im-
provetheproductionandusageofenergy.Asuccessfulpracticeisthatsomestateswith
different strengths and weaknesses unite to form an interstate compact, for promoting
the usage of cleaner,renewable energy sources, through cooperation and adherence to
specificpolicies.
In the southwest of the U.S., there are four states – California (CA), Arizona (AZ),
New Mexico(NM), andTexas (TX) –thathopeto forma realistic new energycompact
aswell.Askedbythefourgovernorsofthesesates,wedetermineasetofdevelopment
goalsfortheenergycompact.
1.2 OurGoals
Basedonourunderstandingoftheproblem,wesetthefollowinggoals:
• Usethegivendatatofoundanenergyprofileforeachstate.
• Develop a model system to show the dynamic relationships between various en-
ergy consumption and economic development of each of the four states, and ex-
ploretheunderlyingfactorsthatleadtotheserelationships.
• Definethe“best”profileforuseofcleaner,renewableenergy,thensetupasystem
ofevaluationtodeterminethestatethathasthe“best”profilein2009.
• According to the analysis above, develop a model and set different scenarios to
predicttheenergyprofileofeachstatefor2025and2050.
• Basedontheestablishedmodels,decidetheusagetargetsofcleanerandrenewable
energyfor2025and2050. Thenprovidethreeactionsforthefourstatestoachieve
thegoals.
1.3 OurThinking
Thisisatypicalbigdataproblem,sowesolveitfromthepointofviewofstatistical
analysis.Hereisourthinking.
First,wepreprocessthedataprovided,whichincludesdefaultvalueprocessing,ab-
normalvalueprocessinganddatasynthesisandclassification. Basedonourdefinitions,
weselect some major energy sources for analysis and divide them into two categories.
Oneiscalledcleanerrenewableenergy(CRE),theotheriscalledtraditionalfossilen-
ergy(TFE).Thespecificdefinitionswillbegivenlater.


## 第 6 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#73767 Page5of28
Second, we select some important data from the dataset provided to construct the
energy profile. Through statistical charts, we visualize them. In this way,we found an
energyprofileforeachstate.Comparingtheenergyfiles ofthefourstates,wefinddif-
ferencesintheirutilizationofthetwokindsofenergysources. Tofurtherclarifythedif-
ferences,welearnfromthedecouplingtheoryandusecoefficientsofelasticitytoshow
the dynamic relationships between various energy consumption and economic devel-
opment of each state. Then we use the simultaneous equations model to respectively
analyze the four states’ economy systems, in which way,we find out the reasons why
thedifferencesexist.
Third,weintroducetheconceptofthecomprehensiveutilizationperformance(CUP)
toevaluatewhichofthefourstatesappearedtohavethe“best”profile.Sincedifferent
stateshavetheirowncharacteristics,therefore,weestablishamulti-dimensionalevalua-
tionsystemtomeasurethecomprehensiveutilizationperformanceincaseofbias.Then
weuseprinciplecomponentanalysis(PCA)tointegrateeachevaluationindexintoan
overallindex,namelythecomprehensiveutilizationperformance.
Finally, we build the BP neural network to predict the energy profile of each state.
By setting various change trajectory of independent variables, we get the predictions
successfully. After that, we regard the four states as a whole to determine renewable
energyusagetargetsfor2025and2050.
2 Assumptions and Notations
2.1 Assumptions
Duetolackofnecessarydataandlimitationofourknowledge,wemakethefollow-
ing assumptions to help us perform modeling. These assumptions are the premise for
oursubsequentanalysis.
• Forthefourstates,allkindsofenergytheyproduceareconsumedbythemselves
eachyear.Thus wecanreplaceenergyoutput with energyconsumptionin calcu-
lation.
• Thepolicyofeachstatewillnotchangeinthefuture. Thisassumptionmaybenot
realistic, but it is essential for us when predicting the energy profile in 2025 and
2050.
• The natural environment of the each states will not change. So we can see it as
constant. This assumption simplify our analysis, and it is reasonable, since the
naturalenvironmentisusuallystable.
• Onceforminganinterstateenergycompact,thefourstatescandevelopandutilize
resourcestogether. Thustheycanrealizemanualbenefitandwin-winresult.


## 第 7 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#73767 Page6of28
2.2 Notations
Herearethenotationsandtheirmeaningsinourpaper:
Notation Meaning
Epd Electricityproduction
Tpd Totalenergyproduction
Rce Renewableenergyexpenditure
ttdp GDP
Cpd Renewableenergyproduction
Pri Priceenergy
Ind Secondaryindustryconsumption
Pop Population
Wcs Woodconsumption
Tcs TFEconsumption
Enc Totalenergyconsumption
Cep Carbonemissionpercapita
K EnergyexpendituresasshareofGDP
Table1:notation
3 Data Preprocessing
Fordata-analysisproblem,thereareusuallysomeincompleteandabnormaldatain
thelargeamountofrawdata,whichmayseriouslyaffecttheefficiencyofmodelingand
theaccuracyofconclusions.Soitisquiteimportanttopreprocessthedata.
3.1 DefaultValueProcessing
Weusedifferentmethodsto process variables with various degrees of dataloss.(1)
For variables with large amount of data missing, we just delete it. Because small data
cannot provide enough and valuable information for our modeling. (2) For variables
with a small amount of data missing, we use interpolation method to compensate the
data. More specifically, we first use existing data points to establish an appropriate in-
terpolationfunction,andthenreplacethemissingvaluewiththefunctionvaluef(x)at
i
thecorrespondingpointx.
i
3.2 AbnormalValueProcessing
Ifavalueinasetofdataismorethantwicethestandarddeviationoftheaverage,we
call it the abnormal value. Statistically we can use a box-plot to identify the abnormal
values. For the abnormal value, we fix it with the average value of its two adjacent
observations.


## 第 8 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#73767 Page7of28
3.3 Data Synthesis andClassification
There are 605 variables in the dataset provided. Not all of them are used in our
model.Thus,wesortthedataweneedintoanewdataset. Besides,wedividetheenergy
sourcesintotwocategoriesforthefurtheranalysis,Oneiscalledcleanerrenewableen-
ergy,whichincludesthehydroenergy,thewindenergy,thegeothermalenergy,thesolar
energy and the ethanol; the other is called traditional fossil energy,which includes the
coal,thepetroleum,thenaturalgasandotherfuels.
Definition:
• Cleanerrenewableenergyistheenergythatproduceslittlepollutionandcanbe
useddirectlyintheproductionandlife.
• Traditionalfossilenergyisnon−renewableenergyandwillcauseairpollution
afterburning.
Inourmodel,somesynthesizedvariablesareused,forexample,theaveragepriceof
cleaner renewable energy.It can be calculated according to formula (1). Other synthe-
sizedvariableswillbeexplainedlater.
Σ
4 Energy Profile
Afterdatapreprocessing,wechoose11importantvariablestocreatetheenergypro-
file.wecallthemthebasicvariables
Notation Abbreviation intheoriginaldataset
GDP GDPRX
Totalpopulation TPOPP
TFEconsumption FFTCB
Totalconsumption TETCB
Woodconsumption WWTCB
Electricityproduction ESTCB
Totalenergyproduction TEPRB
Priceofrenewableenergy AVACD
Renewableenergyproduction REPRB
Renewableenergyexpenditure RFEIV
Secondaryindustryconsumption TEICB
Table2:basicvariable
Descriptivestatistics is usuallythefirst stepin statistical analysis, whichcan shows
the important features of the data visually through graphs and tables. In view of this,
weadoptthedescriptivestatisticsmethodtoshowtheenergyprofileofeachstate.Here
istheenergyprofileofCalifornia,thoseofotherstatesareattachedtotheappendix.


## 第 9 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#73767 Page8of28
Figure1:changetrendofpriceandenergyconsumptioninCalifornia
Figure2:energyconsumptionofdifferentitemsinCalifornia


## 第 10 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#73767 Page9of28
Figure2:
Pic1 TrendgraphofTFEanditsprice
Pic2 TrendgraphofCREanditsprice
Pic3 Trendgraphoftotalconsumption(TC)
anditsprice
Pic4 TrendgraphoftheratioofTFEtoTC
andCREtoTC
Figure3:
F Fuelenthanol C Coal
HY Hydroelectricity PE Petroleum
products
GE Geothermalenergy NG Natural
gas
WE Windenergy OT Other
PH&SO Photovoltaicandso-
larthermalenergy
(Onlytheunitof"F"isThausandBarrels)
Table3:thecutlineinFigure2andFigure3
Figure3:constitutionoftotalenergyconsumptioninCaliforniain2009
Variable QuantitativeChange RateofChange
Energytotalproduction 510310.93(BillionBtu) 156.56%
Renewableenergytotalproduction 28262.33(BillionBtu) 383.32%
Fossilfuels,totalproduction 482048.60(BillionBtu) 151.32%
Electricityproduction 16995.11(BillionBtu) 2279.84%
Woodconsumption 4244.64(BillionBtu) 64.04%
Secondaryindustryconsumption 414753.42(BillionBtu) 199.64%
Renewableenergytotalend-useexpenditures 750.17(Milliondollars) 873.31%
GDP 59090(Milliondollars) 593.15%
Table4:quantitativechangeandrateofchangeoftypicalvariablesfrom1960to2009


## 第 11 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#73767 Page10of28
By comparing the energy profiles of the four states, we preliminarily reached the
followingconclusions:
• Overall,thefourstatesdifferintheirutilizationandconsumptionofthetwotypes
ofenergy(CRE&TFE).
• Each of thefour states has a growing share of CRE consumption, whiletheshare
ofTFEisstillhigh.
• California ranks the first in terms of the amount of CRE consumption; Arizona
ranks the firstin terms of theshare of CRE consumption. However, New Mexico
lagsbehindintheusageandconsumptionofCRE.
5 Model Construction
5.1 Decoupling Analysis
Sincehavinghadageneralideaoftheenergyprofilesofthefourstates,wenowin-
tendtocalculatethecoefficientsofelasticitytodeeplyanalyzethedependencybetween
economic development and the various energy consumption of each state. According
tothedecouplingtheory,thehighertheabsolutevalueoftheelasticity,thestrongerthe
[1]
dependency. Theformulaofcoefficientofelasticityisasfollow.
The calculation results are shown in figure 4. From the figure, we can intuitively
know that generally the dependency between economic development and CRE con-
sumptionisontheriseforeachstate,buttheintensityofthedependencydiffersamong
thefourstates.
Figure4:elasticitycoefficientofFTE(left)andCRE(right)
5.2 TheSimultaneous EquationsModel
Toexploretheunderlyingfactors thatleadstothedifferencesofenergyfilesamong
thefourstates,wedevelopasimultaneousequationsmodel,asshownbelow.Different
syste
m
from single equation regression, simultaneous
more
equations model can explain the complex economic
comp


## 第 12 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
T re e h a e m n # si 7 v 3 e 7 ly 67 and accurately. We introduce three Page11of2(38)
equations into the model, since there are
interactionsbetweeneachtwoofthethreeelements,
eco- nomic development, energy consumption, and
[2]
environmentalpollution.
whereXisasetofcontrollingvariablesonthenaturalenvironment
Lack of variable data on the natural environment, we neglect the set of controlling
variables X to solve the model. The regression results of equation ln(Enc) are shown
in the following table. The regression coefficients reflect the influence of explanatory
variablesondependentvariables,fromwhichwecandeterminetheimpactofdifferent
factorsontheenergyvariable.
TFE CRE
Equation1
AZ CA NM TX AZ CA NM TX
ln(ttdp) 0.2189*** 0.5122** 0.4896** 1.2368*** 0.1904*** 0.4915** 0.2167* 0.4532**
ln(Cep) 0.0012 0.0104** 0.1326** 0.1725** 0.0031 0.0113* 0.0682** 0.1651***
ln(K) 0.2169** 0.3481** 0.2018* 0.3018** 0.2267** 0.4162** 0.2481*** 0.3156*
ln(Pop) 0.0104 0.0341 0.0361* -0.2214 0.0133 0.0265 0.0421* -0.2153
ln(Pri) 0.1152* 0.1421 0.1102** 0.2451 0.1842* 0.1821* 0.2012** 0.2201
ln(Ind) 0.1421* 0.4142*** 0.2269* 0.2684** 0.1723* 0.3841*** 0.2362* 0.2758*
Constant 17.6421* 19.2364* 13.2631* 50.3641* 16.6372* 37.6298* 13.2156* 61.2571*
Table5:theregressionresultsofEquation1
*，**，***respectivelyrepresenttheconfidenceof10%,5%,1%
FromtheTable5,wecanseethatpopulationhasnosignificantinfluenceontheen-
ergy consumption. While the the economic development and the share of secondary
industyhavesignificantinfluenceontheenergyconsumption.
To determinetheinfluence of geographyandclimate, wecollectinformation about
the natural environment of the four states, which is shown in Figure 5. It shows the
resourcedistributionofsolarpower,windpowerandhydroelectricpower.
FromFigure5,weknowthatthefourstatesdifferinthepotentialofCREproduction.
Thedifferencesarecausedbythevariousnaturalenvironmentofthefourstates,suchas
climateandgeography.


## 第 13 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#73767 Page12of28
Figure5:resourcedistributionofCRE
5.3 TheMulti-dimensionalEvaluationSystem
Inthispart,wewilldeterminewhichofthefourstateshasthe“best”energyprofile
in 2009. Through the above analysis, we know that the four states differ in strengths
andweaknessescongenitally. Thus,foravoidingbias,weestablishamulti-dimensional
evaluationsystemtomeasuretheirenergyprofile.
5.3.1 ConstructionofIndexes
Thecoreindexesofourevaluationsystemiscalledcomprehensiveutilizationperfor-
mance(CUP),whichreflects thedevelopment andutilization level of CRE. TheCUPis
composedofthreeparts,energyperformance, economicperformanceandenvironment
performance.Andeachofthethreeparts includes threeindexesas well.Theseindexes
andtheirformulasaredetailedintheTable6.
Figure6:evaluationindexsysterm


## 第 14 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#73767 Page13of28
NameofIndex Meaning Formula
ReflectsthestatusoftheCRE Cpd
Development
developmentandutilizationin
De=
Efficiency(De) Epd
theelectricityindustry.
Energy Development Ref C le R c E ts d th ev e e s l u o s p t m ai e n n a t b a il n it d yof Dp = (Cpdt−Cpdt−1)
performance Potential(Dp)
utilization.
Cpdt−1
(Ep)
Reflectsthecontributionof
Development Cpd
CREdevelopmentand Dpa=
Achievements
utilizationtothestateenergy Tpd
(Dpa)
structure.
Reflectthestate’ssupportfor Rce
Economic renewableenergyatthe Es =
support(Es) ttdp
investmentlevel
Economic Rateofreturnon
pr
R
of
e
i
f
t
l
a
e
b
c
i
t
li
t
t
h
y
e
o
e
f
ff
in
ic
v
ie
e
n
st
c
m
y
e
a
n
n
t
d
on
Roi= Cpd
proformance investment(Roi) Rce
renewableenergy
(Epf)
Equilibriumof
Reflectsupply’ssatisfaction 1
supplyand Esd=
withdemand Pc
demand(Esd)
Secondary Reflectsthedependenceon Scs
industry pollutingindustriesineach
Sip=
Tocs
proportion(Sip) state.
Reflectisthesituationofthe Tcs
Environment Carbonemission Cep =
greenhousegasemissionper
performance percapita(Cep) Tpo
capita.
(Enp)
Consumption of Reflectsthesituationofnatural Wcs
Cnr =
natural resources resourcesconsumptionper
Tpo
percapita(Csr) capita.
Table6:indexesandtheirformulas
5.3.2 PrincipleComponentAnalysis
We use the PCA method to integrate each evaluation index into an overall index,
namely the comprehensive utilization performance. Then through the comparison of
theCUPvaluesofthefourstates,wedeterminethe“best”state.
First, we use the given data and the formulas in Table6 to calculate the evaluation
indexes.Andthen,weusetheequationbelowtostandardizethevaluesoftheseindexes.


## 第 15 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#73767 Page14of28
TheresultsofPCAisshowedintable7.fromthetable,wecanseethatCalifornia
hasthe“best”energyprofilein2009.
Rank State PCAScore
1 California 0.9433
2 Texas 0.5561
3 Arizona 0.2466
4 NewMexico -1.7459
Table7:PCAscores
5.4 EnergyProfile PredictingSystem
5.4.1 DeterminingthePredictors
Inpart5.3,wemeasuredtheenergyfileinthreedimensions,energyperformance,
economicperformanceandenvironmentperformance.Forthefollowinganalysis,we


## 第 16 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#73767 Page15of28
selectanindexfromeachofthemtocalculatethecomprehensiveutilizationperformance
(CUP)inadifferentway.
TheindexesweselectareDpa,RoiandCep.AnalogoustoCobb-DouglasProduction
Functionineconomics,wederivethefollowingformula.
CUP = A ·(Dpa)α ·(Roi)β ·Cepγ (9)
where:
Aisunitcorrectionfactor;
α,β,γareweightcoefficientsofvariables;
α+β+γ=1.
In the previous analysis, we pointed out that, there is an interaction between each
[3]
tow of the three elements, economy, energy and environment. Therefore, we choose
ttDPpercapital(ttdp),Secondaryindustryproportion(Sip)andcarbonemissionper
capita(Cep)astheindependentvariablesinprediction.Thenwecandrivethefollowing
equation.
CUP =θ +θ ttdp+θ Sip+θ Cep+ε (10)
0 1 2 3
5.4.2 ConstructingBPNeuralNetwork
Sincewehavetopredicttheenergyprofilesofthefourstatesrespectively,itisaheavy
task.Thus,weutilizetheintelligentalgorithm(BPneuralnetwork)withhighprediction
efficiency to finish this work. It has been proved theoretically that BP neural network
canapproachanynonlinearfunctionwithhigherprecision. Theflowchartbelowshows
theprincipleofBPneuralnetwork.
Figure7:theprincipleofBPneuralnetwork
There are two steps in the process of constructing BP neural network. First, we
shouldsetthenetworkparameterkthatrepresentsthenumbersofneurons. Herewelet


## 第 17 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
k = 9. Second, we use existing data of input and output to train the network. Wenow
Team#73767 Page16of28
drivethecoreformulasoftheBPNetwork.


## 第 18 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#73767 Page17of28
5.4.3 PredictingtheTargetValues
Topredictthedependentvariable,wehavetoknowtheindependentvariablesfirst.
Unfortunately,welackthevaluesofttdp,SipandCepfor2025and2050.Sowecanonly
predictthedependentvariablebysettingthechangetrajectoryofthethreeindependent
[4]
variablesinadvance.Wesettwoscenariosin total.


## 第 19 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#73767 Page18of28
Figure8:thefittingresults
Figure9:Scenarioone Figure10:Scenario two
• Scenarioone:Lineartrend
Asisshowninfigure9,ifthechangeofthethreeindependentvariablesfollows
thelineartrend.Wecanusetheformula15tocharacterizetheirtrajectory.
x = x +a (20)
t t−1
• Scenariotwo:Smoothfluctuation
Asisshowninfigure10,ifthechangeofthethreeindependentvariablesfollowthe
smoothfluctuation.Wecanuseautoregressivemovingaveragemodel,ARMA(p,q)
[5]
tocharacterizetheirtrajectory.


## 第 20 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#73767 Page19of28
x =φ +φ x +φ x +φ x +ε −θ ε +θ ε −θ ε +µ (21)
t 0 1 t−1 2 t−2 p t−p t 1 t−1 2 t−2 q t−q
Once determining the change trajectory of independent variables, we can estimate
theirvalues.EnteringthemtotheBPnetworks,wegetthepredictedvaluesoftheCUP
ofeachstates.Theresultsareshownintable9.
Scenario1 Scenario2
Year DPA ROI CEC CUP DPA ROI CEC CUP
2025 0.06 25.16 170.97 23.92 0.05 22.15 190.26 23.49
AZ
2050 0.07 50.45 100.45 40.19 0.06 50.15 120.15 35.22
2025 0.08 30.04 138.63 28.39 0.10 29.36 145.26 26.14
CA
2050 0.09 57.87 89.14 45.15 0.12 55.86 108.15 39.15
2025 0.07 50.14 350.45 8.20 0.07 41.26 351.22 7.89
NM
2050 0.08 59.85 282.43 15.16 0.09 57.12 301.86 14.12
2025 0.05 20.60 348.15 7.84 0.05 19.26 369.15 6.95
TX
2050 0.08 48.29 321.53 14.50 0.08 44.12 348.85 12.19
Table9:thepredictingresults
6 TestingOur Model
6.1 PredictingReliabilityTest
Totest the predicting reliability of the BP network, we collect relevant data of each
statefrom2010to2015,andusethemtopredicttheCUP.Thenweuseformula15again
tocomputetheaverageerrorbetweenthepredictedvaluesandtheactualones.Hereare
theresults.
Thepredictingerror
State California Arizona NewMexico Texas
Error 5.89% 6.24% 7.98% 10.07%
Table10:thepredictingerror
6.2 SensitivityAnalysis
IntheprocessofconstructingBPnetwork,weletthenetworkparameterk =9. How
doesthechangeofkinfluencethepredictingresults?Weanalyzetheaveragedeviation
ofCUPcausedbychangingkslightly.
State k-2 k-1 k+1 k+2
AZ 11.08% 4.43% 3.54% 8.51%
CA 8.19% 3.15% 4.66% 10.80%
NM 9.78% 5.39% 4.66% 12.28%
TX 6.66% 2.19% 2.28% 12.33%
Mean 8.93% 3.79% 3.79% 10.98%
Table11:theinfluencebychangingk
Fromtable11,wecanfindthattheinfluenceofk isnotbig,whichwecanbear.


## 第 21 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#73767 Page20of28
7 Determining Goals for the Energy Compact
7.1 Idea one:Don’t cooperate
Ifthefourstatesdon’tcooperate,whichmeanstheydevelopindependently,theycan
onlyutilizetheirownresourcestoenhancethelevelofrenewableenergyusage.Inthis
condition,wecanjustusethepredictedvaluesinpart5.4astheirrespectivetargets.
Forthetwoscenariosinpart5.4,wethinkthatscenariotwoismorereasonableand
realistic. Because the evolution of the macro-economy is usually stable, especially for
[6]
advancedeconomiesliketheUnitedStates. Sowejusttakescenariotwointoconsider-
ation.
Inscenariotwo,theaveragecomprehensiveutilizationperformancecanincreaseto
16.12and25.17successivelyin2025and2050.
7.2 Idea two: Cooperate
Giventhatthefour-stateenergycompactisaninterstatecompact,itisnecessaryfor
the tour states to cooperate. Wepresume that they can develop and utilize resources
together. In this case, we regard the four states as a whole economy.Then we use pre-
vious method and models to predict the whole economy’s comprehensive utilization
performancefor2025and2050.
Year 2025 2050
Thewhole 16.98 26.05
economy’sCUP
Table12:predictionsofthewholeeconomy
Theresultsshowsthatthewholeeconomy’scomprehensiveutilizationperformance
canincreaseto16.98and26.05successivelyin2025and2050,andeachofthemishigher
thanthatinideaone. Maybeitisbecausecooperationenablesthefourstatestogivefull
play to their own advantages and promote the development and utilization of cleaner
[7]
renewableenergy.
7.3 GoalsandActions
Basedontheresultsinideatwoandthepreviousanalysis,wesetthefollowinggoals
forthefour-stateenergycompact.
• Building a community of energy utilization and economic development, so as to
realizemanualbenefitandwin-winresult.
• Promoting the production and usage of new energy sources and reducing then
dependenceontraditionalfossilfuels.
• Increasing the whole economy’s comprehensive utilization performance to 16.98
by2025andto26.05by2050,andachievingtheharmonyofeconomy,energyand
environmentultimately.
According to the goals above and the characteristics of each state, we propose the
actionsandmeasuresforthefourstates.


## 第 22 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#73767 Page21of28
• Focusondevelopingtheirownadvantageous energyresourceandsharetheiren-
ergyandachievementswithothers.
• Make more investment in scientific research to make better use of renewable en-
ergytoimprovethelowutilizationefficiencyofnewenergysources.
• Introduceaproper subsidypolicytoawardtheenterpriseswhodevelopnewen-
ergysource.
• Makecertain quantitative index and do statistic periodically to make sure the di-
rectionofenergydevelopmentisgoingwell.
8 Conclusions
Weareaskedbythegovernorsofthefourstatestosetsomegoalsfortheirinterstate
energy compact. After performing data analysis and modeling, we have finished the
tasksuccessfully. First,Usingdecouplingtheoryandsimultaneousequationsmodel,we
characterizetheevolutionofenergyprofileofeachstatefrom1960–2009,andfindout
theinfluentialfactors. Wehaveknownthatitisthedifferencesofeconomiclevel,indus-
trial structure and natural environment that leadto the distinct energy profiles of each
state. In terms the production and usage of cleaner renewable energy,each of the four
stateshasagrowingshareofCREconsumption,whiletheshareofTFEconsumptionis
stillhigh.
Second,weconstructamulti-dimensionalEvaluationSystemandintroducethecore
concept in this paper,named comprehensive utilization performance (CUP), which re-
flects the development and utilization level of CRE. Through the PCA method, we de-
terminethatCaliforniahasthe“best”energyprofile.
Finally,based on the previous analysis, we build BP neural network for predicting
the energy profile of each state. By setting various change trajectory of independent
variables, we get the target values successfully. After that, we regard the four states as
awholetodeterminerenewableenergyusagetargetsfor2025and2050. Inthisprocess,
weuseBPneutralnetworkagain.
9 Strengths and Weaknesses
9.1 Strengths
• Datapreprocessing.Whenfacedwithbigdataproblem,thedataprocessingisvery
important.Throughthis step,wegreatlyimprovethequalityofthedata.Thus,it
ismoreefficientandconvenientforustosolvetheproblem.
• Accuracyandstability.WeuseBPneutralnetworktomakepredictions. Itisapow-
erful algorithm with great nonlinear approximation ability. The error test shows
thatourpredictingresultsaremoreaccurate.Besides,whenchangingthenetwork
parameterk,itsinfluenceisnotlarge.SotheBPnetworkismorestable.
• Goodexpansibility and flexibility.Thereare threeparameters α, β and γ in our
CUPequation,whichcanbeusedtoreflecttheimportanceofcorrespondingindi-
cators.Indifferentsituations,wecanadjustthemflexibly.


## 第 23 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#73767 Page22of28
9.2 Weaknesses
• Subjectivity.Thecalculationofsomesynthesizedvariablesissubjective.Itcan
causeextraerrorofourmodels.
• Lacknecessarydata.Lackofdataonenergyproduction,wecanonlyusedataon
energyconsumptiontoreplacethem.
• Simplifyingassumption.Forconvenienceofmodeling,weneglecttheelements
aboutimportandexport,whichplayimportrolesineconomy.
References
[1] CarleyS.Staterenewableenergyelectricitypolicies:AnempiricalevaluationofEf-
fectiveness[J].EnergyPolicy,2009,37(8):3071–3081.
[2] VerbruggenA,FischedickM,MoomawW,etal.Renewableenergycosts,potentials,
Barriers:Conceptualissues[J].EnergyPolicy2010,38(2):850–861.
[3] Vries B J M D, Vuuren D P V,Hoogwijk M M. Renewable energy sources: Their
globalpotentialforthefirst-halfofthe21stcenturyatagloballevel:Anintegrated
Approach [J]. Energy Policy, 2007, 35(4):2590-2610. [36] Sliz-Szkliniarz B. Assess-
ment of the renewable energy-mix and land use trade-off at a regional level: A
case stud for the Kujawsko–Pomorskie Voivodship [J]. Land Use Policy,2013, 35:
257–270.
[4] Al-BadiAH,MalikA,GastliA.Assessmentofrenewableenergyresourcespoten-
tial in Oman and identification of barrier to their significant utilization[J]. Renew-
ableandSustainableEnergyReviews,2009,13(9):2734–2739.
[5] AkellaAK,SainiRP,SharmaMP.Social,economicandenvironmentalimpactsof
renewableenergysystems[J].RenewableEnergy,2009,34(2):390–396
[6] KaygusuzK.Environmentalimpactsofthesolarenergysystems[J].EnergySources
PartA:RecoveryUtilizationandEnvironmentalEffects,2009,31:1366-1376.
[7] WeeH M, YangW H, Chou C W,et al. Renewable energy supply chains, perfor-
mance,applicationbarriers,andstrategiesforfurtherdevelopment[J].Renewable
andSustainableEnergyReviews,2012,16(8):5451–5465.


## 第 24 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#73767 Page23of28
Appendices
Appendix A Profiles of Arizona
Figure11:EnergyprofileofArizona
Figure12:MeansofenergyconsumptioninArizona


## 第 25 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#73767 Page24of28
Figure12:
Pic1 TrendgraphofTFEanditsprice
Pic2 TrendgraphofCREanditsprice
Pic3 Trendgraphoftotalconsumption(TC)
anditsprice
Pic4 TrendgraphoftheratioofTFEtoTC
andCREtoTC
Figure13:
F Fuelenthanol C Coal
HY Hydroelectricity PE Petroleum
products
GE Geothermalenergy NG Natural
gas
WE Windenergy OT Other
PH&SO Photovoltaicandso-
larthermalenergy
(Onlytheunitof"F"isThausandBarrels)
Table13:thecutlineinFigure2andFigure3
Figure13:TheconstituteoftotalenergyconsumptioninArizonain2009
Datafrom1960to2009
Variable QuantitativeChange RateofChange
Energytotalproduction 1116104.735(BillionBtu) 374.35%
Renewableenergytotalproduction 67311.832(BillionBtu) 186.04%
FossilfuelS,totalproduction 1048792.903(BillionBtu) 400.36%
Electricityproduction 672434.71972(BillionBtu) 2090.35%
Woodconsumption 6547.67591(BillionBtu) 171.44%
Secondaryindustryconsumption 1127324.01293(BillionBtu) 816.29%
Renewableenergytotalend-useexpenditures 4885.009(Milliondollars) 4728.95%
GDP 201016(Milliondollars) 6.736912662
Table14:Thequantitativechangeandtherateofchangeoftypicalvariables


## 第 26 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#73767 Page25of28
Appendix B Profile of New Mexico
Figure14:energyprofileofNewMexico
Figure15:meansofenergyconsumptioninNewMexico
Appendix C Profiles of Texas


## 第 27 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#73767 Page26of28
Figure15:
Pic1 TrendgraphofTFEanditsprice
Pic2 TrendgraphofCREanditsprice
Pic3 Trendgraphoftotalconsumption(TC)
anditsprice
Pic4 TrendgraphoftheratioofTFEtoTC
andCREtoTC
Figure16:
F Fuelenthanol C Coal
HY Hydroelectricity PE Petroleum
products
GE Geothermalenergy NG Natural
gas
WE Windenergy OT Other
PH&SO Photovoltaicandso-
larthermalenergy
(Onlytheunitof"F"isThausandBarrels)
Table15:thecutlineinFigure2andFigure3
Figure16:theconstituteoftotalenergyconsumptioninNewMexicoin2009
Table16:Thequantitativechangeandtherateofchangeoftypicalvariables
Datafrom1960to2009
Variables QuantitativeChange RateofChange
Energytotalproduction 510310.930(BillionBtu) 156.56%
Renewableenergytotalproduction 28262.327(BillionBtu) 383.32%
FossilfuelS,totalproduction 482048.602(BillionBtu) 151.32%
Electricityproduction 16995.11376(BillionBtu) 2279.84%
Woodconsumption 4244.64258(BillionBtu) 64.04%
Secondaryindustryconsumption 414753.41587(BillionBtu) 199.64%
Renewableenergytotalend-useexpenditures 750.173(Milliondollars) 873.31%
GDP 59090(Milliondollars) 593.15%


## 第 28 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#73767 Page27of28
Figure17:EnergyprofileofTexas
Figure18:MeansofenergyconsumptioninTexas


## 第 29 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#73767 Page28of28
Figure18:
Pic1 TrendgraphofTFEanditsprice
Pic2 TrendgraphofCREanditsprice
Pic3 Trendgraphoftotalconsumption(TC)
anditsprice
Pic4 TrendgraphoftheratioofTFEtoTC
andCREtoTC
Figure19:
F Fuelenthanol C Coal
HY Hydroelectricity PE Petroleum
products
GE Geothermalenergy NG Natural
gas
WE Windenergy OT Other
PH&SO Photovoltaicandso-
larthermalenergy
(Onlytheunitof"F"isThausandBarrels)
Table17:thecutlineinFigure2andFigure3
Figure19:TheconstituteoftotalenergyconsumptioninTexasin2009
Variable QuantitativeChange RateofChange
Energytotalproduction 6319816.106(BillionBtu) 142.26%
Renewableenergytotalproduction 306479.838(BillionBtu) 611.07%
FossilfuelS,totalproduction 6013336.268(BillionBtu) 136.90%
Electricityproduction 1061765.94759(BillionBtu) 8953.51%
Woodconsumption 23236.12241(BillionBtu) 60.67%
Secondaryindustryconsumption 5556015.3619(BillionBtu) 158.61%
Renewableenergytotalend-useexpenditures 24323.858(Milliondollars) 5688.46%
GDP 876004(Milliondollars) 460.01%
Table18:Thequantitativechangeandtherateofchangeoftypicalvariables

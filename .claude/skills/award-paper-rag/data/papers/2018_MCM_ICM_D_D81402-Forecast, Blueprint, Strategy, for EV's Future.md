# D81402-Forecast, Blueprint, Strategy, for EV's Future


## 第 1 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
TeamControlNumber
Forofficeuseonly Forofficeuseonly
81402
T1 F1
T2 F2
ProblemChosen
T3 F3
D
T4 F4
2018
MCM/ICM
SummarySheet
(Yourteam'ssummaryshouldbeincludedasthefirstpageofyourelectronicsubmission.)
Typeasummaryofyourresultsonthispage.Donotincludethenameofyourschool,advisor,orteammembersonthispage.
Forecast, Blueprint, Strategy, for EV's Future
Since 21th century, electric vehicles(EV) has grown from a sprout in vehicles industries as
for its environmental benefits. Many people wonder that if one day electric vehicles could
replace fuel vehicles completely. Considering the inconvenience of charging, a critical
problem of electric vehicles is about the charging system construction.
To maximize profit and minimize cost, the EV industries are overcoming three facets:
1) the mapping distribution of a specific area; 2) a time-domain evolution model for market
prediction/forecast; 3) A standard classification of worldwide marketing. To reduce the
Carbon Dioxide pollution, the government also concerns about the policy design for EV
market.
In this essay, we will start from an approach tothecharger location and
allocationproblem, and then dig deep into theforecast of EV marketin different
countries. To solve 5 tasks, we proposed several models in the cross-science of Network
Science, Operations Research, Economics, Statistics, Environmental Science, Graph
Theory, Cybernetics and Game Theory.
For task 1), we first took a data pre-processing, transforming address/zip code to
Geodetic Coordinate System. We aim to make an approach to the maximum coverage
problem. We defined 892 supercharger locations, 3,048 charger locations and 492 urban
cities/clusters as “nodes”. For the simplicity, an undirectedgraph model representing the
whole charging network was established, in which every node denotes a potential position
for building chargers. After the graph was connected, we applied SPFA algorithm to
calculate the Shortest Path among each nodes pairs. We also developed a Demand
EstimationModel to generalize Average Miles Driven data and Urbanization data, and
proposed the demand of each node respectively. To obtain a best charger allocation
scheme, we constructed a Linear Programming model, which could be not solved in
affordable time. To reduce the computational complexity, we converted it into an equivalent
MinimumCost Max-flow Networkmodel. We showed our location and allocation results
in maps, graphs, contours and major city lists, respectively for U.S. and South Korea. For
task 2b), we applied a Most Profit model based on Nash Equilibrium, to find the optimal
strategy in a “chicken or the egg causality dilemma”: chargers lead vehicles market, or
vehicles market lead chargers? For the former situation, we introduced a systematic
dynamic model to demonstrate the process by cybernetics concepts; For the latter
situation, we introduced a Market Evolution Model based on Bass DiffusionModel, to
achieve a better understanding of high technology products’ adoption in economics. For
task 2c), We proposed Bass Diffusion Model based on data analysis, predicted the market
adopted timeline from a blank market. For task 3), we discussed the feasibility of our
previous model, and proposed a Linear Regression Model to calculate the weight of each
factors contributed to future EV industry evolution, i.e. GDP per Capita, PPI, Oil price, etc.
For task 4), we proposed our perspective for high technology adoption in the future. For
task 5), we proposed our hand out to decision makers in governments, briefly stating our
results in EV market promotion.
Our work has many strengths and weaknesses. Our strengths were performed in
interdisciplinary views, coding and mathematic skills, economics views and social
responsibilities; our weakness were performed in the lack of sensitivity modification, and


## 第 2 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
the quantitative derivation of system dynamic model in investments.


## 第 3 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Contents
1 Introduction 2
2 Modeling 2
2.1 Outline...........................................................................................................................2
2.2 Assumptions.................................................................................................................3
2.3 Location&AllocationOptimizationModel............................................................3
2.4 DemandEstimationModel........................................................................................5
2.5 ShortestPathModel....................................................................................................6
2.6 BestProfitStrategyModel..........................................................................................7
2.7 MarketEvolutionModel............................................................................................8
2.8 ClassificationofPromotingEVs................................................................................9
3 Dataset&Toolkit 10
4 ResultsandAnalysis 10
4.1 Task1...........................................................................................................................10
4.2 Task2...........................................................................................................................12
4.2.1 Task2a............................................................................................................12
4.2.2 Task2b............................................................................................................15
4.2.3 Task2c.............................................................................................................16
4.3 Task3...........................................................................................................................17
4.4 Task4...........................................................................................................................18
4.5 Handout......................................................................................................................20
Appendices 22
AppendixA Code 22
1


## 第 4 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#81402 Page2of27
1 Introduction
Havingseentheenvironmentalsituation(greenhouseeffect,etc.),analternativeenergy
to replace fossil fuels in vehicles industry is now becoming a hot issue. Withthe rapid
technologydevelopmentofelectricvehiclesandtheencouragementofpoliciescoopera-
tiononinternationalnegotiations,electricvehicles(EV)isnowafashioninbothlabora-
toryandcommerce.
Since2012,TeslaCorporationisstandingoutasaleadingpeerinelectricvehiclesin-
dustries. TeslaimprovesitsR&Dinvestment,resultinginasolidfoundationofelectric
vehicleengineandenergystoragetechnology.Itresultsintheexcellentperformanceof
salesinmanyproducts,suchasModelSandModelX.
Thepowersupplyandchargingnetworksareessentialinfrastructuresinelectricve-
hicles industry. Problem D in ICM 2018 provided a chance to see the insight of these
infrastructures. By analyzing and predicting its consuming trend and the location of
chargingpiles,itmaybeagoodperspectiveforustounderstandtheexpectingfuture.
2 Modeling
2.1 Outline
Tomaximizeprofitandminimizecost,theEVindustriesareovercomingthreefacets:1)
themappingdistributionofaspecificarea;2)atime-domainevolutionmodelformarket
prediction/forecast;3)Astandardclassificationofworldwidemarketing.
Forthemappingchargersdesign,itincludes:1a)thecalculationofdemandchargers
in numbers, according to Population, Urbanization, Household travel willingness, etc;
1b)theoptimizationofchargersdesign:sizingandplacing.
1b) is a critical problem. The location of EV chargers should be both easily accessi-
bleandwidelyspread.Hence,EVscanbechargedeasilyin"neighborhood"forregular
business/school/church, etc., and also able to cruise around a larger area upon being
re-chargedforlongdistancetrips.(Lamet. al,2014)[9]Theultimategoaltomaximizethe
efficiencyofchargersandthecoverageofchargingsystem.
Green energy industries like Tesla Corp. has been scheduling a long-term market-
ing and planning blueprint to switch U.S./the world to an all electric vehicles society.
Thisblueprintrequiresasystematicdynamicmodeltoforecastthemarketevolutionin
the following decades. To expand Tesla Corp.’s global market, decision makers would
run into a “chicken or the egg causality dilemma": 2a) Let chargers stimulate vehicles
sales,or2b),vehiclessalespromotethechargersystemconstruction?Thisgametheory
problemwouldintroducetwodifferentmarketingpredictionandstrategies.
TosolvetasksstatedinICM2018ProblemD,weapplymultiplemathematicalmodel-
ingmethodsinthecross-scienceofOperationResearches,NetworkSciences,Economics,
GameTheory,Geography,GraphTheory,etc.
For facet 1), the mapping distribution of a specific area, the bottleneck is how to opti-
mize the distribution under a certain charging demand. It indicates a famous prob-
leminappliedmathematics, Maximum CoverageProblem(or,Maximum CoverageLo-
cation Problem, Church & Revelle, 1974)[3]. We established a Linear Programming
Model(MLP Model, Hiller, 2012)[8] to solve this problem. Toreduce the computational
complexity,weconverteditintoanequivalentMinimumCostMax-flowNetworkmodel.


## 第 5 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#81402 Page3of27
In our MLP model, two parameters needed to be modified: i) the shortest path
between two nodes; ii) the charging demand of each node. Tofind parameter i), we
developed a Shortest Path Model(Dijkstra, 1959)[5]. All the address/zip codes data
from Tesla.comwere extracted, and transformed into Geodetic Coordinate Format. Af-
ter pre-processing, we applied all the location data of existing chargers, superchargers,
andlargest497cities/clusters(definitionofUrban,U.S.CensusBureau,2010)[18][19]in
U.S. to draw a graph. Weidentified that the current construction of Teslachargers and
superchargersisabletolink497cities/clusters.Tomodifyparameterii),weintroduced
a Demand Estimation Model in a macro scope via statistics from geography,i.e. pop-
ulation, urbanization, highway miles, etc. Wecalculate the demand per node(city) (d
i
below) by AverageMiles Driven per year by state (AMD)[17] and Urbanization Statis-
tics,inurban,suburbanandruralareasrespectively.
Forfacet2),thetime-domainmarketevolutionmodel,weneedtoclarifythedifficultyof
makinga decision on which is theleadingfactor - between constructing chargingpiles
and constructing EVs. For decision makers, we introduce a game theory model Best
ProfitStrategyModel-tofindtheoptimalstrategy.
Forthecase2a),weintroducedaSystematicDynamicmodel,butnotaquantitative
one.wedidn’tincludethispartinourModelingsection,onlyinthetasks.
For the case 2b), we proposed a Market Prediction Model - Bass diffusion model
(Norton & Bass, 1987)[11] to estimate the future occupancy of future EV market. Bass
diffusion model demonstrate how a high technology product run into the market and
ultimatelyreplacetheoldgenerationofproducts.ApplyingTeslasalesdataandKorea
EVsalesdata,BassDiffusionModelperformswellinourdatafitting.
For facet 3),the standard classification of worldwide marketing, we promote a classifica-
tionsamplebyLinearRegression.
2.2 Assumptions
Inthismodel,thefollowingitemsareoutofourworkscope:1a)altitudeofeachcities/n-
odesincalculatingdistancesinshortestpathmodel;1b)trafficjams;1c)chargingblueprint
ofAlaskaandHawaii,andPuertoRico;1d)thegrowthofthedemand,intask1;1e)home
charging.
For the simplicity, we also simplify the following items in our modeling: 2a) We
define geographical design of "urban" and "suburban" as a circle zone. Their area are
extracted fromLandAreain Urban areas of theUnited States of America (U.S.Census
Bureau, 2010)[18][19].; 2b) The earth radius was set by 6,378 kilometers; 2c) Weuse su-
perchargersconstructiontoreplacechargersinourblueprint(assuperchargersaremore
efficient).
Otherassumptionsmentioninasingletask/modelarealsovalid.
2.3 Location &Allocation OptimizationModel
TosolvetheMaximalCoverageProblem,wedevelopedaLinearProgrammingmodelto
findthe maximal coveragesolution in station location problem.Wedidn’tconsider the
capacity difference between a charger and a supercharger primarily; for an optimized
blueprintin alarge scale, wefirst regard themas "nodes",which means that weattach
moreimportancetothelocation.
ObjectiveFunction:


## 第 6 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#81402 Page4of27
∑∑
min
yij,ci
, y
ij
d(i,j) (1)
i Vj V
subjectedto ∈ ∈
i V, j V,y 0 (2)
ij
∀ ∈ ∀ ∈
∑
i V, y ⩾d (3)
ij i
∀ ∈
j V
∑ ⩾
∈
i V, y ij αd i (4)
∀ ∈
j V dist i,j minD
⩾
∈ ∧i V(,c)⩾i 0 (5)
∀ ∈
∑
j V, y⩾ c (6)
ij j
∀ ∈
i V
⩽
j V,c∈ maxC (7)
i
∀ ∈
⩽
α: A Dimensionless Coefficient of long distance traveling. For example, αd means
i
Charging multiple alternatively. It demonstrate the charging demand of node i which
has to be contributed by the "distant" nodes. The neighborhood nodes is defined by
a distance radius min D. Weimplement this to cases where people have long distance
traveldemands,theyneedtochargeinanothercity.
maxC: Aparameter. TheMaximumchargercapacityofasinglenode,dependingon
thechargetechnique.
Nevertheless, since there are more than V variables in the above linear program-
mingmodel,itis difficulttosolvethis large|-|sc2aleLP model usingstandard algorithms
like Simplex. Thus, the LP model is converted into an equivalent minimum cost max-
flowmodelasfollows.
• Assumethatthesourceandsinkofthenetworkflowmodelis,respectively,Sand
T;


## 第 7 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#81402 Page5of27
2.4 Demand EstimationModel
Thechargingdemand is also acomplicatedissue to besolved.Everyday,people travel
backandforth,contributingthedemandofeachcharger. Previousresearcheshavepro-
posed the(daytime, nighttime) demand of each communityin acity byLinear Regres-
sion,wherevarious factors havebeentakenintoconsideration:neighborhood, popula-
tion, community social structure, household traveling willingness, employment, daily
activities,etc.(Chenetal.,2013;Fradeetal.,2011)[2][7]Suchestimationsarefeasibleina
relative small scale, like Lisbon and Seattle in the literature. For such a large scale of
UnitedStates, it would occur a large computational complexity if we divide the whole
country into communities and apply linear regression to calculate the weight of each
factors. Hence we only consider the impact factors in a macro scope, i.e. population
andlandareaofcities(alsocalled,urbanization),AverageMilesDrivenperyearbystate
(AMD)[17].
Weprepared a parsimonious estimation with the following model setting: a) Wedi-
vide AMD data to urban, suburban and rural respectively.A vague definition of "sub-
urban"wereintroduced. b) Weregard acity (among 497cities/clusters) as a node. The
urbandemandwascontributedbyitsownpopulationanditsshareofAMD.Theurban
share of AMD corresponds to inter-city traveling (employment, school, church, etc.) c)
The demand of rural area was shared by the remained AMD per area. Considered the
subnationaltravel,wedistributethisdemandequallytostates.d)Adefinitionofurban,
suburbanandruralshouldbeclarified.UrbanareasoftheUnitedStatesofAmerica(U.S.


## 第 8 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#81402 Page6of27
CensusBureau,2010)[18][19]onlydefined“urban"inabroadsense:Urbanincludedall
populationinurbanized areas andurban clusters (each with theirownpopulation size
and density thresholds). This definition includes both urban and suburban. It has al-
ways been an issue to clarify the geographic definition of urban suburban areas, in a
narrow sense, we define urban as a node on the map and suburban as the cities’ large
landareaproposedinUrbanareasoftheUnitedStatesofAmericadata. Forpopulation
distribution,wedistribute26%inurban,53%insuburban,and21%inrural.[22]e)We
onlyconsideredthecurrentpopulation,demand,etc. Theultimategoalistochangethe
wholevehiclesindustrytoanall-electricone.Theaimofreplacingfuelenergyvehicles
weights more than calculate the growth of vehicles. Wedidn’t propose a dynamic sys-
tem,fortask1.
The notations reads i: node; j: state; R: rural area; SU :suburban area; U : urban
area;d:demandpernode;D :demandexcepturbanarea;P :populationofacity;P :
i R c s
populationofastate;m :AMDwherethecitylocates;S:landareaofU.S.;ϵ:aparameter
j
toadjustdemandweightbythenodesdensityinanarea; center(i): i SU,center(i) is
thecentercitythatsuburbannodei belongsto; size(i): i U, the num∈berofsuburban
citiesbelongingtocityi;. ∈
2.5 ShortestPathModel
Torun the Linear Programming model, the shortest path d(i, j) need to be calculated.
Wecouldsimplytackle theproblem employingaiterativealgorithm(Dijkstra, 1959)[5].
Thisproblemsetsreadsthetreeofminimumtotallengthbetweennnodes,andthepath
ofminimumtotallengthbetweentwogivennodesPandQ(Dijkstra,1959)[5].
Ourmodelsettingaimstoconstructagraphconnectingallnodes.Primarynodeswere
setbyallthecurrentsuperchargersinU.S.(892nodes),chargersinU.S.(3,048nodes)and
497cities/clusters mentionedabove.Intotal,weset4,295nodescovering48statesand
WashingtonD.C.inU.S.(Alaska,HawaiiandPuertoRicoareexceptions.)
Adatapre-processingwasappliedasalltherawlocationdatawereperformedinad-
dress/zip code format. In order to calculate the path, we applied a Google Geocode
API[20]totransformtherawdataintoGeodeticCoordinateSystem(latitude,longitude).
Hence,theshortestpathcouldbecalculatedviadistancecalculationonasphericalsur-
face. The earth radius was set by 6,378 kilometers for thesimplicity.Weherepropose a
generalnodesmapofappliednodes(figure1)
Toreducethecalculationcomplexity,weapplytheSPFAAlgorithm(Duan,1994)[6]
tooptimizeshortestpathcalculationbasedonqueue.


## 第 9 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#81402 Page7of27
Figure1:Allnodes(superchargers,chargersandcitiesinclueded)
Figure2:NodesaroundSalt-LakeCity
2.6 BestProfitStrategyModel
MarketingstrategiesshouldchangedynamicallyregardingthedevelopmentofEVtech-
nology,theabilityofchargingpiles(thechargeofpilesandhowlongcanitaddcharge)
and the instant international trade accumulating the acceleration of EV and charging
piles.
We need to do is find the best profit between two situations : more EV and more
charging piles. Between thetwo classifications, there are a bestexpectation that would
happen so that we can get the most profit. We introduce a Best Profit Strategy Model
basedaNashEquilibrium(Nash,1951)[10]inGameTheory.
A plan needed to be drew,to predict a pattern in order to decide what we should
weightmorebetweenconstructingEVandconstructingchargingpiles.Notationsneeds
tobeemphasizedbelow:
P:theratioofchargingpilestoEV;


## 第 10 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#81402 Page8of27
P :thestandardratioofchargingpilestoEV;
P :theratioofchargingpilestostandardchargingpiles;
0c
P :theratioofEVtostandardEV;
e
Hencewecanwritethefollowingagametheorymodel,seetable1and2. EX and
EX holdthesameformulation,withdifferentnotationsforprobabilities. 1
This is a simple game theory model describing the optimal strategy.The meaning
10
oftheoptimalstrategyinwhichwechooseistherepresentationoftherelativedegreeof
data. What we needto do is find a formal formula to correctly describethe data of the
standardchargersandP ;
Inorder tomaximizetheinterests,oneshouldbeina positiveor negativesituation
0
whenourearningsareequal(orinthisgame,eachothercanchangeboththefrontand
theprobabilitythatourexpectedrevenue),sothatweknowthat:
EX EX
P = −
(17)
e
40 20
EX EX EX + EX
− −
Hence,thefuturestrategywou1l0dmad2e0based3o0nthis40model.
2.7 MarketEvolutionModel
To see the marketing performance of "chargers in response to car purchases", a fore-
casting model is required to explain systematic dynamic market evolution of Electric
Vehicles.
Table1:NashEquilibriumModelforchargers
P < P P >P
P < 1 ChargersEX1 EVEX3
c 0 0
P > 1 EV EX2 ChargersEX4
c
Table2:NashEquilibriumModelforEVs
P < P P >P
P < 1 Chargers EX EVEX
e 0 0
P > 1 EV EX ChargersEX 0
e 10 30
20 4


## 第 11 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#81402 Page9of27
Weintuitivelynoticethedevelopmentofhightechnologyproductsasasimplepos-
itive feedback process. Such an explosive trend is unfeasible in fitting a linear model.
Particularly, in United States, the growth economics index(e.g.GDP per capita, house-
hold income) and population tend to be moderate. Thus, a linear regression cannot
explaintheboostortheexpectedboostinElectricVehiclesindustry.However,anexpo-
nentialincreaseinthepositivefeedbackisexplosive.Comparingwiththeanalogywith
speciesreproductioninecology,anexponentialmodelignoresthelimitedantecedentsof
theenvironmentalresourceswelivein.Wealsonoticethatalthoughitisnotcompletely
identical,insomesituationsthemodeldoesreflectwellatsomepointintime.
Although the initial assumption says that exponential growth is occurring in the
same period, we can adjust the model by modifying the multiple of the exponential
growthtoavoidtheblowup.Byshowingthatgrowthmultiplesareaffectedbycertain
factors,suchfactorsbecomethecoreofthismodel.
WehereapplyBassdiffusionmodel(Norton&Bass,1987)[11]toestimatethefuture
occupancy of the charging pile through the number of tesla electric cars. This model
tends to form an s-shaped curve in the transition from positive feedback to negative
feedback.
When considering the impact of multivariate factors on the problem, the logistic
modelreflectsitskeysignificance,whichisalsousedbyusinpredictingthefuturetrend
ofelectricvehiclesandtheaddingnumberofchargingpiles.
BassDiffusionModelsaysthat,
f(t)/[1 F(t)]=p+qF(t). (18)
−
It explains the if f (t) is defined as the probability of adoption at time t, (neglecting
thehazardfunction),F(t) isthefractionoftheultimatepotentialhasadoptedbytimet.
p and q are parameters, respectively,the coefficient of innovation and thecoefficient of
imitation.
Tosolvethisdifferentialequation,aninitialconditioncouldbeaddedasazeroth
point,F(0)=0.ThuswewillgetthesolutionofF(t)andf(t):
F(t) = [1 exp( bt)]/[1+aexp( bt)] (19)
− − −
f(t) = (b /p)exp( bt)/[1+aexp( bt)] (20)
− −
2 2
wherea = q/p andb = p + q. The peakof f(t) occursatt = (1/b)ln(a).
Thisdifferentialequationcouldbesolvednumerically. Inth∗isessay,wewillpropose
themarketevolutionofAmericaandSouthKoreabyfittingtheexistingsalesdatainto
Bassdiffusionmodel.
2.8 Classification ofPromotingEVs
When talking about the classification system, we need to think about such a question:
howthesefactorsaffecttheselectionofdifferentapproachestogrowingthenetworkand
how much?Maybe different countries havedifferent situations and therefore selecting
thefactorsseemsimportant.
TherearesomanycountriessuchasAmerica,UnitedKingdom,China,Japan,South
Koreaandother countries and thereare manyfactors, forinstance, GDP,Engels coeffi-
cient,degreeofindustrializationandagriculture,thedegreeoftrafficnetworkdevelop-
ment,andsoon.


## 第 12 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#81402 Page10of27
Among these factors, some are possibly interacted and associated. What we might
think most is find a master-slave relationship among these factors. However, in this
model setting, we need to notice some important factors that we cannot ignore as there
are some essential small factors such as the degree of electricity, industrialization and
transportation. These may be a branch of some data such as GDP or PPI, but they are
thesameimportant.
Now we can set a function to mainly describesome necessary index. The Multiple
LinearRegressionformulareads:
ttDP PPI ttI RN VPC OP UB
a +a +a +a +a +a +a = 1 (21)
ttDP PPI ttI RN VPC OP UB
1 2 3 4 5 6 7
Ournota0tionreads:0ttDP:Gr0ossDome0sticProduc0tperCapi0ta;PPI: P0roducerPrice
Index;ttI:GiniCoefficients;RN:Roadnetworktotalmiles;VPC:VehiclesperCapita(1000
people);OP :OilPrice; UB:Urbanization.
TheEVweightwerereplacedbyVPCandOPinourmodelasmanycountries
haven’tpromoteEV.
3 Dataset & Toolkit
Wehaveappliedthefollowingdatasetandtoolkit:
• Fororiginal Teslachargers andsuperchargers,weappliedaddress/zipcodefrom
officialwebsite[4][14].
• ForShortestPathModel,wetransformedaddress/zipcodetoGeodeticCoordinate
System, and appliedGoogle GeocodeAPI[20]. Wealsoused the Korea cities data
togetlatitudesandlongitudesofKoreacities.[25]
• ForDemandEstimationModel,weappliedAverageMilesDrivenperyearbystate
(AMD)[17],UrbanareasoftheUnitedStatesofAmerica(U.S.CensusBureau,2010)
[18][19].
• ForLocation&AllocationOptimizationModel,weappliedGoogleCostflowToolkit
tooptimizeLinearProgrammingcalculation[21].
• For Market Evolution Model/Bass Diffusion Model, we referred the Tesla sales
data[15][12] in America and EV sales data in South Korea[13][16] to predict the
dynamicevolutionofTeslamarket.
• Forclassificationbetweencountries,weappliedglobaldataofGDP[27],PPI[29],
GI[23],RoadNetwork[24],Urbanization[30],OilPrice[26]andVehiclesperCapita[28].
4 Results and Analysis
4.1 Task1
OurSimulationincluding4,297nodeshaveproposedapossibleblueprintforTesla’s
chargerconstruction.Wesupposethatthesuperchargerswouldreplacethechargers


## 第 13 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#81402 Page11of27
due to theadvantages in charging power. For our distribution,allocation and capacity
blueprintweonlyconsiderthesuperchargers.
OurShortestPathModeldemonstratethatallthechargers,superchargersandcities
arefullyconnected.Parametermind=170(miles)accordingtothechargingcapacityof
30minutesinTeslasupercharger.Indeed,Teslaisontracktoallowacompleteswitch
toall-electricintheUS.Itmighttakeafewdecadestoaccomplishacompleteswitch,
butTeslaistryingtodrawtheblueprint.
OurDemandEstimationModelprovidesademand(inmilesunit)foreachnode.We
classifiedthedemandofurbanareas,suburbanareasandruralareasrespectively,and
derivedparameterα=0.25whichcouldbefittedintheweightofdistantmultiplealter-
nativecharging. Wesettheparametersmaxc=50000(theupperlimitsuperchargersfor
anode).
OurLocation&AllocationOptimizationModelprovidesaforecastofanall-electric
U.S.Itwouldrequire873,869tocoveranall-electricU.S.Thechargerconnectionscanbe
seen in Figure 4. An interesting thing occurred in our simulation: the current super-
chargernodeswouldremainactive,butmostofthechargernodesareeliminatedforthe
performance.
FortheAllocationofchargers,thedistributionmapcanbeseeninFigure3.Wealso
printthesuperchargersdesignof12Cities/Clusters withlargestpopulation,inTable3.
AcontourfigureareshowninFigure5
Weproposetheurban,suburbanandruraldistributionofsuperchargersinTable4.
Figure3:ChargerDistributioninU.S.


## 第 14 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#81402 Page12of27
Figure4:ChargerConnectionsinU.S.
Figure5:ChargersDistributionContourFigureinU.S.
4.2 Task2
4.2.1 Task2a
Basedon themodelsappliedintask1,wedrew agraph of 135Korea’s maincities[25].
ThenwecreatedalocationandallocationblueprintifwereplaceKorea’scurrentvehicles
toEVs.
Duetothelackofdata,wecalculatedthedemandofeachnodebythefollowing
estimation:
vehicles per capita of South Korea
(22)
d =d inU.S.
i i
× vehicles per capita of U.S.


## 第 15 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#81402 Page13of27
Table3:Superchargersdesignof12MainCities/Clusters
Location Numbers Location Numbers
NewYork-Newark 11667 Philadelphia 3634
LosAngeles-LongBeach-Anaheim 8289 Huston 9609
Chicago 5730 Atalanta 9680
Miami 6823 Detroit 3991
Dallas-FortWorth-Arlington 3798 Boston 2893
WashingtonD.C. 2715 Phoenix-Mesa 2342
Table4:ChargerDistributionPlanninginUrban,SuburbanandRural
Geography Urban Suburban Rural
Proportion 40.25% 25.38% 34.36%
Our calculations showed that 56,953 superchargers required to be constructed in
South Korea.Figure 6 shows thepredictedsuperchargers locationin South Korea.Fig-
ure 7 shows the predicted superchargers distribution in South Korea. Similar to U.S.,
South Korea has well-constructed road, vehicles culture, high household income, and
urbanizationdegree.Theirdifferencemainlyincludesgeography(landarea,cities’net-
work,population, etc.) Based on our model,key factors that shaped thedevelopment
couldbe:geographiccities/roadnetwork,populationandurbanization. Fromthis per-
spective,SouthKoreacouldbeconsideredasalargelandareaofU.S.,likeNortheast.
Figure6:ChargerConnectionsinSouthKorea


## 第 16 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#81402 Page14of27
Figure7:ChargerDistributioninSouthKorea
Figure8:ChargersDistributionContourFigureinSouthKorea


## 第 17 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#81402 Page15of27
Location Seoul Pusan Taegu Inch’on Taejon
Numbers 11153 3777 2597 2479 1774
Location Kwangju Sungnam Puch’n Suwon Ulsan
Numbers 1602 1264 1147 1112 918
Table5:NumberofChargersin10MajorSouthKoreanCities
4.2.2 Task2b
Speakingofinvestmenttoablankmarket,wewillproposeseveralinvestmentstrategy.
It always runs into a dilemma. Weneed chargers to make people who purchased EV
moreconvenient; buttheoriginalmarketlawsbasedonthetechnologypromotionand
leverprinciplearealsoimportant. Orwecansay,bothofthemcannotbeneglected,es-
peciallyintheexpansionperiod.
OurMostProfitmodelingametheoryhasprovidedafutureplanningofprobabili-
ties in the two situations: chargers first, or market first? Tofind a general "behaviour",
ourgametheorymodelappliedEVandchargingpilesgenerations,tofindanoptimized
solution(Table6).
Bylinearregression,wecangenerallyobservethatwhenP isstableinthestandard
e
Year 2012 2013 2014 2015 2016 2017
EVPurchase 52607 97507 122438 116099 158614 199826
Chargers 11042 20198 25684 31674 44028 59167
P 0.11 0.20 0.26 0.31 0.44 0.59
e
P 0.21 0.21 0.21 0.27 0.28 0.30
0
Table6:BestProfitModelDerivation
valueof0.375,thevalueofP shouldbestableat0.275.Thegametheoryvalidtestin
U.S.correspondsourcalculationsofSouthKorea.Sucha"behavior"couldbeconsidered
0
as"thechoiceofcustomersandproducers".WeapplytheparameterP =0.275forour
gametheorycase.
0
Thus,ourproposaltalksaboutthebalanceofconstructingtheratioofchargingpiles
andEVBuildachargingsystemandelectricvehiclesproportionallyinascalebasedon
thestandardratioof0.275.Theinvestmentproportionofthetwoprojectsiscarriedout
according to the price of the charging system divided by the price of the chargers di-
vided by the price of the electric vehicle, and the fluctuation limit is no more than 10
million. According to the game theory model, when the pile ratio is less than 0.275, it
tends topilethepile,andviceversa.Theimportantfactoristheratioofpiletocarand
the saturation limit of pile and car.From the perspective of urban and rural areas, the
mixedconstructionshouldbetaken.
For the first situation, the chargers’ leading one, we can take a qualitative system
dynamicapproach.Whenweplacedtheangleofviewintheprocessofattentiontothe
improvementoftheelectricsystem,wefinditexistsasasystemflowandithasaposi-
tivefeedback,whichmakesusabletousesystemdynamicsmodeltosolvetheproblem.
Intheanalysisofthemutualpromotionmechanismbetweenchargingpilesandelectric
vehicles,wecanrealizethatthereisaconsiderablepositivefeedbackincentivebetween
thetwosituations. Wecandrawabriefsystemdynamicsprocess(Figure9)basedonthe
existing positive feedback and system flow.Through the analysis of system dynamics
model,wecangetapreliminaryanswerthatistosay,ifyoudon’tappearunderthemu-


## 第 18 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#81402 Page16of27
tualpromotionmechanismofoverproduction,willbethetrendofpositivefeedbackon
thewhole,inotherwords,thatistobuildonearbitrarywillpromoteanotherproduction
andconstruction.
Forthesecondsituation,wewillletthemarketdrive.
Figure9:SystemDynamicProcess
4.2.3 Task2c
As the taskrequires a "blank" market,our investment wouldfirstly "build" chargers to
stimulate the first 6 years of an EV market corresponding to the graph in task 1) and
chargers’ growth in task 2b). For the simplicity, we adjusted our placing with current
salesdataofKoreaEVmarket,andre-calculatethetimescale. Thenweputthemarket
evolutionmodelinourtasksolution.
ThekeyfactorofourMarketPredictionModelisgenerallyshapedbytherelationship
ofhigh-technologyproductionandtheoldgenerationsoftheproduction.Thisrelation-
ship has it’s own parameters in p(innovations) and q(imitations). In South Korea case,
the p and q were generally modified by it’s market evolution. Actually,South Korea is
actuallyaleadingpeerinworldwideEVmarket. DomesticcompanieslikeHyundaialso
promotedit’sownEVproducts. StatisticsshowsthatKoreaistheonlycountrythatup-
gradeditstargetin2016,from200000to250000electriccarsby2020,aspertheSpecial
PlanforFineDustManagement,releasedinJune2016[16].
WeappliedBassDiffusionModelasourMarketPredictionModel. WeappliedEV
sales data of South Korea(since 2012), the competition in EV industry were neglected.
Weapplied Bass Diffusion Model because it performs well in South Korea’s previous
data,revealingasituationthatSouthKoreaisonthetrackofBassPrediction.
Our simulation shows the EV market evolution in South Korea in Figure10 (Adop-
tionattimet)andFigure11(UltimatePotentialadoptedbytime).
Theultimateadoptionpercentageisshownintable7.
Table7:UltimateAdoptionPercentage(zerothpointfrom2018)
Percentage 10% 30% 50% 99.9%
Year 2026 2028 2029 2036


## 第 19 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#81402 Page17of27
Figure10:Adoptionattime t
Figure11:UltimatePotentialadoptedbytime
4.3 Task3
Wedon’thavemuchconfidenceinthemodel’sfeasibilityofpromotingEVintothefive
countries.Asmentionedabove,bothU.S.andSouth Koreahavewell-constructedroad,
vehicles culture, high household income, and urbanization degree. We suppose that
insomeotherdevelopedcountries,likeAustralia,withwell-constructedroadnetwork,
thismightbefeasible. IncitycountrieslikeSingapore,wemightfacethehazardestima-
tionofdemand. Thedemandofacitymustbecarefullyestimated,asmentionedabove.
Inotherdevelopingcountries,likeChina,IndiaorIndonesia, themainproblemwould
be the household income, urbanization. Thanks to the government’s policy in China,
China’sEVmarketisnowbecomingaleadingmarketworldwide.
Afterapplyingdatainsevenaspects,wegettheresultsofLinearRegressionModel
plottedinFigure12.
By comparing these index, we can know which is more important in this country.
The network in Saudi Arabia and Australia might be a problem, as the large occupa-
tion of desert area. As for Singapore, over-promotion in Vehiclesindustry would leave
a negative effect on it’s traffic. China needs to improve its urbanization. In Indonesia,
it needs to improve its GDP per Capita, its gas price and urbanization. Toexpand the


## 第 20 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#81402 Page18of27
vehiclesindustries,SaudiArabiaandU.S.needstoreduceit’sGiniCoefficients-make
morepeopleaffordvehicles.
However,thereare manyaspects influencing acountry’s market. A simple classifi-
cation as we proposed above, might not gave an accurate, quantitative answer on the
key factors that trigger the selection of different approaches. The following factors can
betakenintoconsideration:
• GDPperCapita(weighted,canbereplacedbyhouseholdincomeorconsumption
data)
• PPI(weighted,canbereplacedbydomesticEVindustriesdata)
• GiniIntex(weighted,orEngel’scoefficients)
• Roadnetworktotalmiles(weighted,butit’sconstrainedbythegeographyland
scaleofacountry)
• VehiclesperCapitaandOilPrice(weighted,butthisoneshouldbetheEVadoption
weightinthefuture)
• Urbanization(weighted)
• PublicPolicy(supportfromgovernment)
• VehiclesCultureandPublictransportation
Tosummarize,EVmarketwouldhavedifferentevolutionindifferentcountries.Geog-
raphy,economics,policy,culture...allofthemcanaffectamarket’sdomesticevolution.
Figure12:TheWeightof7aspectsin6countries
4.4 Task4
Wearedriftingsuchatechnologicalworldthatwewouldneverknowwhatwillhappen
inthenextdecade.Whatwehaventdreamedup,likesmartphonesandArtificialIntel-
ligence,havecometrue. Relyingonourlimitedknowledgeaboutforecastingthefuture


## 第 21 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#81402 Page19of27
world,whatweneedtodeeplythinkisthatwhetherornotitreallyhasaprofoundim-
pactontheenergystructure.
Considering the energy structure nowadays, it is mainly dependent on fossil fuels
suchascoal,oilandnaturalgas. Otherkindsofenergylikewind,hydrogenandnuclear
are not common in our daily life. Using the heat directly like the internal combustion
enginefordrivingthecarisconstantlyseenthanothers.Astherearenotenoughtechnic
forkeepingthecarmotivatedandfullofcharge, interms ofvehicleperformance, there
aresomedeficienciesinelectriccars.Besides,thecostofelectricvehiclesistoohighand
therearelackofenoughassistantfrompolicyandcountry,leadingtoitsslowdevelop-
menttoday.
Thedevelopmentof electricvehicles is mainlyfromclimateinternational changein
the world. As countries around the world have a great deal of concern about environ-
mentalissues,climatechangeandsoon,newenergyhasbecomethefocusoftheworlds
attention. A larger scale in developing the new energy such as wind and hydrogen to
power generation seems mainstream. Electric vehicles are a fundamental basic in the
development of using new energy.What we are concerned about is how chargers can
supplyenoughimpetusandreserveenoughenergyforalongdistance.
In a continuous period, we may think about a better way to supply enough impe-
tus andreserveenoughenergy,forinstance, developingnewenergyandmakingafor-
mation of an alternative to electric vehicles. If the new technology cannot get enough
improvement on doing so, I think that such an innovation cannot be revolutionary on
todays power demand. Such a barrier cannot hold a big truck for lifting a heavy stone
and delivering a high speed in todays fast life for a quick speed such as airplane and
thehigh-speedrail.Imagingthatthereis achangethatcangreatlyinspire theproperty
of high-speedand enough powerreservation in a modality of electricity, I think that it
mustleadstoahugedeclineaboutthecostofelectricvehiclesunlessthereissomething
necessaryforsupplyingthatistooexpensivetocoverthecostsuchasapressurizedgas
tank for storing liquefied hydrogen gas. Maybe in a few decades we can see a spec-
tacularsituationthataroundtheworldtherearecountlesselectricvehiclescrossingthe
road safely than beforeas thereis noopen flamefor explosion. It must accumulatethe
developmentofelectricvehiclesinapositivefeedbackandthusgraduallyimprovesthe
number of holding EV and charging piles. In a few years it can replace fossil fuel cars
aroundtheworld.
In another perspective, if the technological level has a great impact and even there
existsahugechangesothatitcanreplaceelectricvehiclessuchasnuclearenergywhich
isportableandsafeenoughfornotleaking. Maybesuchtechnichassuchaprofoundef-
fectonelectricvehiclesthatisparticularlyexciting.Althoughelectriccarshaveenough
room to grow and update, a more efficient approach to energy use would make such
progressnegligible.Soinsuchintenseenergystructureintheprocessoftransformation,
thevigorousdevelopmentofelectricvehicles,maybeoveraperiodoftime,willbemuch
moreefficientbecauseofthenewenergydevelopmentandgradualreductionofitssize,
eventuallyleadingtothemostefficientmeansofenergyuse,suchas nuclearenergyor
hydrogen,finallysustainedapplicationabovetoourwayoftransportation.
Inaword,thedevelopmentofenergydependsonthenewestenergystructure.We
hopefullyseesuchabettertransportationincar-shareandride-shareservices,self-driving
cars,rapidbattery-swapstationsforelectriccars,andevenflyingcarsandHyperloop.


## 第 22 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#81402 Page20of27
4.5 Handout
Asaninternationalenergysummit,weareverypleasanttobeherewithallofyouinthe
diplomaticfield. Duringthesedaysofconferences,wewillmainlydiscussthedevelop-
ment of energy structure and policy blueprint. Weunderstand that different countries
havedifferentenergypolicies andenergytechnologydevelopmentplans.Wehopethat
aforward-lookingenergystructurewillbemoresuitableforalong-termplanning,con-
tributingtothefutureofourplanetfromeverypart.
Themeetingtodiscussthemaincontenthasthefollowingaspects,alsohopingthat
leaderscanagreeonagreement,foreachnationalenergypolicyfocusontargetedpolicy.
• Futureuseofnewenergy
• Structuralcontradictionsinnewenergydevelopment
• Developmentprospectsandplansfornewenergyapplications.
Our meeting attaches much importance to the specific implementation of the protocol
after the end of the conference in domestic laws. Electric cars contributes a lot on the
reductionofpollution.Intheconcreteofnewenergydevelopmentandpopularizationof
electriccars,weproposeseveralfactorswhichcouldinfluencethepoliciesforpromoting
electricvehicles.
Thesefactorsarelistingasfollows:
• Thestateofeconomicdevelopment
• Thedevelopmentofelectricvehicles
• Statepowersupplysituation
• Thedevelopmentofelectricvehicles
• Statepowersupplysituation
• Nationalroadtrafficdistributionplanning
• Trasportationnetwork
• Urbanization
• Engelscoefficient
• Thestatefinancestaxonrelatedareas
• Internationalcooperationandtrade
• Transformationoftechnologicalachievements
• Internationalcooperationinthefieldoftechnology
Weawarethatthefactorsabovedonotfullycoverallfieldsofacountry’sblueprint.Our
hopeistoinitiateatrendwithgreen,electricvehicles.Wehopethatstaytouchedinthe
summitofthedifferencesandcontradictions,participateinnegotiations oftheinterna-
tional framework, being committed to global governance and development, jointly set
upabroaderplatformforthedevelopmentofnewenergytechnologies.


## 第 23 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#81402 Page21of27
References
[1] Becker,T.A.,Sidhu,I.,&Tenderich,B.(2009).ElectricvehiclesintheUnitedStates:
a new model with forecasts to 2030. Center for Entrepreneurship and Technology,
UniversityofCalifornia,Berkeley,24.
[2] Chen, T. D., Kockelman, K. M., & Khan, M. (2013, January). The electric vehicle
chargingstationlocationproblem: aparking-basedassignmentmethodforSeattle.
InTransportationResearchBoard92ndAnnualMeeting(Vol.340,pp.13-1254).
[3] Church, R., & ReVelle, C. (1974, December). The maximal covering location prob-
lem. In Papers of the Regional Science Association (Vol. 32, No. 1, pp. 101-118).
Springer-Verlag.
[4] Destination Charging| Tesla.(2018).Tesla.com. Retrieved10 February2018,from
https://www.tesla.com/destination-charging
[5] Dijkstra, Edsger W. "A note on two problems in connexion with graphs." Nu-
merischemathematik1.1(1959): 269-271.
[6] Fanding,D.(1994).AFasterAlgorithmforShortest-PtathSPFA[J].JournalofSouth-
westJiaotongUniversity,2.
[7] Frade, I., Ribeiro, A., Gonçalves, G., & Antunes, A. (2011). Optimal location of
chargingstationsforelectricvehiclesinaneighborhoodinLisbon,Portugal.Trans-
portation research record: journal of the transportation research board, (2252), 91-
98.
[8] Hillier,F.S. (2012). Introduction to operations research. TataMcGraw-Hill Educa-
tion.
[9] Lam, A. Y.,Leung, Y.W.,& Chu, X. (2014). Electric vehicle charging station place-
ment: Formulation, complexity, and solutions. IEEE Transactions on Smart Grid,
5(6),2846-2856.
[10] Nash,J.(1951).Non-cooperativegames.Annalsofmathematics,286-295.
[11] Norton, J. A., & Bass, F.M. (1987). A diffusion theory model of adoption and sub-
stitutionforsuccessivegenerationsof high-technologyproducts.Managementsci-
ence,33(9),1069-1086.
[12] Monthly Plug-In Sales Scorecard. (2018). Insideevs.com. Retrieved 10 February
2018,fromhttps://insideevs.com/monthly-plug-in-sales-scorecard/
[13] Organization for Economic Co-operation and Development, Retail
Trade Sales: Passenger Car Registrations for the Republic of Korea
[SLRTCR03KRQ180S], retrieved from FRED, Federal Reserve Bank of St. Louis;
https://fred.stlouisfed.org/series/SLRTCR03KRQ180S,February10,2018.
[14] Supercharger | Tesla. (2018). Tesla.com. Retrieved 10 February 2018, from
https://www.tesla.com/supercharger
[15] U.S.vehiclesales1977-2017|Statistic.(2018).Statista.Retrieved10February2018,
fromhttps://www.statista.com/statistics/199983/us-vehicle-sales-since-1951/


## 第 24 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#81402 Page22of27
[16] https://www.iea.org/publications/freepublications/publication/GlobalEVOutlook2017.pdf
[17] https://www.carinsurance.com/Articles/average-miles-driven-per-year-by-
state.aspx
[18] https://en.wikipedia.org/wiki/List_of_United_States_urban_areas#cite_note-1
[19] https://www.census.gov/geo/reference/ua/urban-rural-2010.html
[20] https://developers.google.com/maps/documentation/geocoding/intro
[21] https://developers.google.com/optimization/flow/mincostflow
[22] https://fivethirtyeight.com/features/how-suburban-are-big-american-cities/
[23] https://en.wikipedia.org/wiki/List_of_countries_by_income_equality
[24] https://en.wikipedia.org/wiki/List_of_countries_by_road_network_size
[25] http://www.tageo.com/index-e-ks-cities-KR.htm
[26] https://www.bloomberg.com/graphics/gas-prices/#20173:Australia:USD:g
[27] https://en.wikipedia.org/wiki/List_of_countries_by_GDP_(nominal)_per_capita
[28] https://en.wikipedia.org/wiki/List_of_countries_by_vehicles_per_capita
[29] https://tradingeconomics.com/indonesia/producer-prices
[30] https://en.wikipedia.org/wiki/Urbanization_by_country
Appendices
Appendix A Code
Herearecodesweusedinourmodelasfollows.
BuildGraph
import csv
import json
import sys
import matplotlib.pyplot as plt
from utils import distance, calculate_shortest_path, is_connected,
calculate_shortest_path_dijkstra
import math
import numpy as np
vertex = []
print "processing data..."
# plot the major cities
cnt = 0
with open("./data/urban_data_with_state.json", "r") as f:


## 第 25 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#81402 Page23of27
cities = json.load(f)
city_x = []
city_y = []
city_no = []
for city in cities:
cnt += 1
if city["longtitude"] < -140:
continue
if city["latitude"] < 20:
continue
city_x.append(city["longtitude"])
city_y.append(city["latitude"])
city_no.append(cnt - 1)
point = {}
point["x"] = city["longtitude"]
point["y"] = city["latitude"]
point["type"] = "city"
point["no"] = cnt - 1
point["state"] = city["state"]
point["area"] = city["land_area"]
point["name"] = city["name"]
if len(point["state"]) > 2:
print "****** ERROR *********"
point["population"] = city["population"]
vertex.append(point)
print "major cities: ", len(city_x), "/", len(cities)
# plot the super chargers
schargers_x = []
schargers_y = []
schargers_no = []
cnt = 0
tot = 0
with open("./data/superchargers.csv", "r") as f:
lines = csv.reader(f)
flag = True
for line in lines:
if flag:
flag = False
continue
tot += 1
if float(line[2]) < -140 or float(line[2]) > -40:
continue
schargers_x.append(float(line[2]))
schargers_y.append(float(line[1]))
schargers_no.append(tot - 1)
point = {}
point["x"] = float(line[2])
point["y"] = float(line[1])
point["type"] = "super_charger"
point["no"] = tot - 1
vertex.append(point)
print "super chargers: ", len(schargers_x), "/", tot
# plot the destination chargers
chargers_x = []
chargers_y = []
chargers_no = []
cnt = 0
with open("./data/destinations.csv", "r") as f:


## 第 26 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#81402 Page24of27
lines = csv.reader(f)
flag = True
for line in lines:
if flag:
flag = False
continue
cnt += 1
if float(line[2]) < -140 or float(line[2]) > -40:
continue
x = float(line[2])
y = float(line[1])
if y < 20:
continue
chargers_x.append(x)
chargers_y.append(y)
chargers_no.append(cnt - 1)
point = {}
point["x"] = x
point["y"] = y
point["type"] = "destination_charger"
vertex.append(point)
print "destination chargers: ", len(chargers_x), "/", cnt
print ""
for i in range(len(vertex)):
sys.stdout.write("\033[F") #back to previous line
sys.stdout.write("\033[K") #clear line
print "classifying vertex into urban/suburban/rural: %.2f" % (float(i) /
float(len(vertex)) * 100.) + "%"
if vertex[i]["type"] == "city":
vertex[i]["position"] = "urban"
else:
is_suburban = False
for j in range(len(vertex)):
if vertex[j]["type"] == "city":
if distance(vertex[i]["y"], vertex[i]["x"], vertex[j]["y"],
vertex[j]["x"]) < math.sqrt(vertex[j]["area"] / 2 / math.
pi):
vertex[i]["position"] = "suburban"
is_suburban = True
break
if is_suburban == False:
vertex[i]["position"] = "rural"
with open("./data/vertex.json", "w") as f:
json.dump(vertex, f, indent = 4, sort_keys = True)
a = plt.scatter(city_x, city_y, c = 'r', marker = 'o')
b = plt.scatter(chargers_x, chargers_y, c = 'g', marker = '+')
c = plt.scatter(schargers_x, schargers_y, c = 'b', marker = '+')
plt.legend((a, b, c), ("major cities", "destination chargers", "super chargers
"))
plt.xlabel("longtitude")
plt.ylabel("latitude")
MaxD = 170 * 1.609344
x = city_x + schargers_x + chargers_x
y = city_y + schargers_y + chargers_y
edges = []
edge_table = []


## 第 27 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#81402 Page25of27
sz = len(x)
for i in range(sz):
edge_table.append([])
print "size of V: ", sz
print ""
for i in range(sz):
sys.stdout.write("\033[F") #back to previous line
sys.stdout.write("\033[K") #clear line
print "building graph: %.2f" % (float(i) / float(sz) * 100.) + "%"
for j in range(i + 1, sz):
d = distance(x[i], y[i], x[j], y[j])
if d <= MaxD:
edges.append([i, j, d])
edge_table[i].append([j, d])
edge_table[j].append([i, d])
print "size of E: ", len(edges)
print "is connected: ", is_connected(sz, edge_table)
print ""
total_dist = []
with open("data/spp.csv", "w") as f:
for i in range(sz):
sys.stdout.write("\033[F") #back to previous line
sys.stdout.write("\033[K") #clear line
print "calculating shortest path: %.2f" % (float(i + 1) / float(sz) *
100.) + "%"
dist = calculate_shortest_path(i, sz, edge_table)
total_dist = total_dist + dist
for j in range(len(dist)):
if j > 0:
f.write(",")
f.write(str(dist[j]))
f.write("\n")
print "MinD = %s" % np.mean(np.asarray(total_dist))
LinearProgramming
import networkx as nx
import random
import sys
from ortools.graph import pywrapgraph
import timeit
import csv
import re
import json
start = timeit.default_timer()
alpha = 0.25
minD = 500
min_cost_flow = pywrapgraph.SimpleMinCostFlow()
maxC = 50000
base = 365 * 24 * 340 * 1.609344
ssp = []
sz = 0
print ""
total = 0.
with open("./data/ssp_new_1.csv", "r") as f:
while True:


## 第 28 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#81402 Page26of27
line = f.readline()
if line == None or len(line) == 0:
break
sz += 1
sys.stdout.write("\033[F") #back to previous line
sys.stdout.write("\033[K") #clear line
print "retreiving ssp data: %.2f" % (float(sz) / 4295. * 100) + "%"
line = re.sub(r"\n", '', line)
line = line.split(r",")
for i in range(len(line)):
line[i] = float(line[i])
ssp.append(line)
with open("./data/demand.json", "r") as f:
demand = json.load(f)
min_cost_flow = pywrapgraph.SimpleMinCostFlow()
inf = 0x7fffffff
total_flow = 0
print ""
for i in range(1, sz + 1):
sys.stdout.write("\033[F") #back to previous line
sys.stdout.write("\033[K") #clear line
print "building network: %.2f" % (float(i) / float(sz) * 100.0) + "%"
total_flow += int(demand[i - 1] / base + 2)
min_cost_flow.SetNodeSupply(i, int((1. - alpha) * demand[i - 1] / base +
1))
min_cost_flow.SetNodeSupply(sz + i, int(alpha * demand[i - 1] / base + 1))
min_cost_flow.SetNodeSupply(2 * sz + i, - maxC)
for j in range(1, sz + 1):
min_cost_flow.AddArcWithCapacityAndUnitCost(i, 2 * sz + j, inf,
int( ssp[i - 1][j - 1]))
if ssp[i - 1][j - 1] >= minD:
min_cost_flow.AddArcWithCapacityAndUnitCost(sz + i, 2 * sz + j,
inf, int(ssp[i - 1][j - 1]))
print "sz: %s" % sz
print "total_flow: %s" % total_flow
print "calculating..."
min_cost_flow.SolveMaxFlowWithMinCost()
print "min-cost: ", min_cost_flow.OptimalCost()
solution = []
num_of_arcs = min_cost_flow.NumArcs()
max_flow = 0
flow = [0] * sz
print ""
for i in range(num_of_arcs):
sys.stdout.write("\033[F") #back to previous line
sys.stdout.write("\033[K") #clear line
print "retreiving optimal flow: %.2f" % (float(i + 1) / float(num_of_arcs)
* 100.0) + "%"
flow[min_cost_flow.Head(i) - 2 * sz - 1] += min_cost_flow.Flow(i)
max_flow += min_cost_flow.Flow(i)
print "max-flow: ", max_flow
with open("./data/assignments.json", "w") as f:
json.dump(flow, f, indent = 4)
stop = timeit.default_timer()


## 第 29 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#81402 Page27of27
print "time consumed: %s s" % (stop - start)

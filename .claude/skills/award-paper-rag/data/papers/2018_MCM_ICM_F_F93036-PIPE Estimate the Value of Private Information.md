# F93036-PIPE Estimate the Value of Private Information


## 第 1 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
TeamControlNumber
Foroffice use only Foroffice use only
93036
T1 F1
T2 F2
T3 ProblemChosen F3
F
T4 F4
2018
MCM/ICM
Summary Sheet
PIPE: Estimate the Value of Private Information
Summary
Contrary to the pervasive belief that human society has entered the information age,
the massive data produced by human individuals are not fully exploited yet. Private data
nowadays are under poor,isolated management by individual enterprises, where thevalue
of data cannot be fully extracted to benefit either its provider or owner. To address this
problem,awell-establishedmarketsystemisrequiredthatnotonlypricesandrewardsdata
sharing, but also regulates and protectsprivateinformation.
To satisfy the requirement, our paper provides a detailed analysis based on a dataset
PI-DATA,based onwhichwe proposeasophisticated andgeneralizedmodel,PrivateInfor-
mation Price Estimation (PIPE), which is able to estimate the price of private information
(PI)regarding different data domainsofPI and socialsubgroups.
Task 1: We abstractly extract feature vectors from individuals and query requests to dis-
tinctlycharacterize theirtraitsin different data categories..
Task2: Weestimatethecorrelationmatrixofdatacategoriesanddevelopanamendment
formula toaccuratelycompute data value considering internaland externalfactors.
Task3: WeestablishaSupplyand DemandModeltoestimatethevalueofPIasacommod-
ityonthe levelofindividuals, groupsandnations.
Task 4: We surveyed the existing government act (e.g. Privacy Act, GDPR, APPI, etc.)
and price regulations related to the private information around the world. Also, we intro-
duce adynamic variationtoillustrate thechange ofhuman decision-making overtime.
Task 5: We introduce a risk-to-benefit factor and show how generational differences
change ourmodel. We alsocompare PI withPP and IP.
Task 6: To clarify the connection between different subgroups of people, the multi-
dimensional clustering algorithm for friends (mCAF) is applied to the dataset PIDATA. By
conducting experiments on the data from different groups as well as from the same group,
we find thatthe relationship betweendata and value isnot linear, but log-likelihood.
Task 7: We simulate the effect of massive data breach and predict the effect of PI loss
andcascade eventusing ourmodel. Based onourpricing system,we think agenciesshould
compensate toindividuals directly fordatabreaches.
Inthe end, we make sensitivityanalysis and discuss thestrengths as wellas weaknesses
of our model. Moreover, a policy memo is presented to the decision maker on the utility,
resultsand recommendationsbased onourPIPE policymodel.
Keywords:Private Information; Pricing Strategy;Dynamic System; NetworkEffect


## 第 2 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
MEMORANDUM
To:DecisionMakeraboutPrivacy
From:MCM2018Team
Subject: PrivateInformation: The Emergence ofaNewAsset
Date: Monday,February12,2018
1 Introduction
In the era of ”anywhere, anytime”, people now produce more data than ever before.
Thevarietyandvolumeofdigitalrecordsthatcanbecreated,processedandanalyzed
will continue to increase dramatically. By 2020, International Data Corporation (IDC)
estimatesthattheglobalamountofdigitalrecordswillincreasemorethan40-fold.
The problem is to quantify the cost of privacy.That is, to establish a metric to eval-
uate the monetary value of keeping PI protected and the fees it would cost for others
to possess or utilize PI. Weconsider private information (PI) as record of ”everything
a person makes and does”. Tomake the problem clearer, several concepts need to be
explained.
Domain of Private Information. An initial list of types of private information in-
cludes: Digital identity (e.g., names, addresses, phone numbers, demographic infor-
mation, social network profile information, etc.); Relationships to other people and
organization (social media, contact list and profiles); Communication data and logs
(emails, SMS, phone calls, IM and social network posts); Media produced, consumed
and shared (in-text, audio, photo, video and other forms of media); Financial data (fi-
nancialtransactions,accounts,creditscores,physicalassetsandvirtualgoods);Health
data (health/medical records, medical history,medical device logs, prescriptions and
health insurance coverage); Institutional data (government, academic and employ-
mentdata).
Subgroup of Individuals. E.g. citizenship, professional profiles, age, education
level,occupation, etc.
Risks. The risks involve loss of safety,money,valuable items, intellectual property
(IP), theperson’selectronicidentity,professionalembarrassment ,lossofapositionor
job,socialloss (friendships), social stigmatization, ormarginalization.
2 Solutions and Conclusions
Private information will continue to increase dramatically in both quality and diver-
sity, and has the potential to unlock significant economic and societal value. To some
extend,PrivateInformation(PI) is similar topersonalproperty(PP) and intellectual
1


## 第 3 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
18
18
16 16
14
12
14
10
5
4 12
3
0
1 2
2
3 1
4 5 0 10
Figure1:Demand Surface: the influence ofdatavolumnand informationentropy
property (IP). However, there are also discrepancies among them. PI differs from PP
andIPinthatitcanbesoldorgiventootherswhothenhavetherighttouseitwithout
ownership, and it needs to be regulated by government. These information and pri-
vacy issues should be protected not only by the individuals but also by the agencies.
Based on our model, the private data should not be trackable by the government for
nationalsecurityconcerns.
Building a harmonious ecosystem around personal data will require significant
commitment from all stakeholders. Our model proposes four critical solutions todeal
withtheproblem:
Anexpandedroleforgovernment,suchthatgovernmentscanusetheirpurchas-
•
ing power to help shape commercially available products and solutions that the
privatesector canthenleverage;
Mechanisms for enhancing trust among all parts in private informationtransac-
•
tion;
Integrate principles surrounding and user trust and data protection into the de-
•
velopment ofnewservicesand platforms;
Policymakersandagenciesshouldlaunchaninternationaldialog,whichshould
•
encompass governments, international bodies such as the World Trade Organi-
zation, end user privacy rights groups and representation from the private sec-
tor.It should include not only US and European Union members, but interested
partiesfromthe Asia-Pacific regionand emergingcountries;


## 第 4 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
2


## 第 5 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#93036
PIPE: Estimate the Value of Private Information
Contents
1 Introduction 1
1.1 ProblemBackground . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 1
1.2 OurWork. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 1
2 Assumptions&Nomenclature 2
2.1 Assumptions. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 2
2.2 Nomenclature . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 2
3 PIPE: MathematicalModelfor Private InformationPriceEstimation 2
3.1 Vector-basedRepresentationfor Individualsand Queries . . . . . . . . . . . . 4
3.1.1 IndividualFeature Vectors. . . . . . . . . . . . . . . . . . . . . . . . . . 4
3.1.2 QueryFeature Vector& CorrelationMatrix . . . . . . . . . . . . . . . . 6
3.2 Dynamic MarketSystem& Pricing Strategy . . . . . . . . . . . . . . . . . .. . 7
3.2.1 PIDemand Model . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 7
3.2.2 Buyer-Seller RelationshipInfluence toPrice . . . . . . . . . . . . . . . . 8
3.3 mCAF:aMulti-dimensional ClusteringAlgorithmforFriends of Social Net-
workServices . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 9
4 ExperimentalResults 12
4.1 Task1:Price Point forProtecting One’s Privacyand PI inVariousApplications 12
4.2 Task2:Pricing Structure ofPI.........................................................................................14
4.3 Task3:Supply andDemand...........................................................................................15
4.4 Task4:Assumptionsand Constraints- Political/CulturalIssues.............................15
4.4.1 ExplanationofTerminology...............................................................................15
4.4.2 PoliticalIssues andCulturalIssues...................................................................16
4.4.3 PriceRegulations.................................................................................................17
4.5 Task5: GenerationDifference.........................................................................................17
4.6 Task6:mCAF:aMulti-dimensional ClusteringAlgorithmfor FriendsofSocial
NetworkServices..............................................................................................................18
4.7 Task7:Data BreachEffect...............................................................................................18


## 第 6 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#93036
5 SensitivityAnalysis 19
5.1 DemandModel.................................................................................................................19
5.2 mCAFModel......................................................................................................................20
6 ConclusionsandFutureWork 20
A Implementation of Function σ(·) 22
A.1 Demographics...................................................................................................................22
A.2 Family& Health................................................................................................................24
A.3 Property.............................................................................................................................24
A.4 Activities............................................................................................................................25
A.5 Consumer...........................................................................................................................26
B PrivacyAct 26


## 第 7 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#93036 Page 1of27
1 Introduction
1.1 Problem Background
Weare moving towards a “Webof the world” in which mobile communications, social
technologies and sensors are connecting people, the Internet and the physical world into
oneinterconnectednetwork[1]. Vastquantitiesofdatarecordsareincreasinglygatheredby
cheap and numerous information-sensing devices on personal information (PI) including
but not limited to tweets, purchasing histories and health records. In 2016, roughly 16.1
zettabytes (1021 bytes) of data are being generated each day, and it is estimated that the
figurewill increase to 163zettabytesby the year2025[2].
Mining and analyzing such data enables researchers to study,understand and evenpre-
dict human behaviors on the individual, group and global level. Advanced data analytics
methods that extract value from data have been in widespread use in insurance, marketing
and many other industries [3]. For instance, methods combining big data with deep learn-
ingmethodshaveshownsuperiorperformanceinpredictingtrafficflows[4]andmanaging
high-risk patients[5].
However, the massive collection, sharing and distribution of personal data are prone
to certain risks concerning information privacy. As participation in social networking sites
has dramatically increased in recent years, services such as Wechat, Twitter,and Facebook al-
low millions of individuals to create online profiles and share personal information with
vast networks of friends-and, often, unknown numbers of strangers [6]. Data breaches also
pose considerable threats to sensitive private information that involves personal health in-
formation (PHI), personally identifiable information (PII), trade secrets of corporations or
intellectualproperties[7].
It has been acknowledged that data providers can possibly be classified into subgroups
according to their data’s value distribution over multiple domains (e.g. finance, health).On
theotherhand, personalorcommunityrisksrelatedtodataprivacyoftenarousesignificant
differences inpeoples’ privacychoices acrosssuch domainsas well[8].
Moreandmoreintensivesharingaretakingplacenowadays,whilethemanagementand
tradingofprivatedataareunderloosecontrolofthegovernmentandcompanies. Currently,
millionsofpeoplearetrickedintoofferingtheirdatainexchangeforlittlereward. However,
theuseoftheirdataisfarfromefficientduetodataisolationbetweenenterprises. Moreover,
some of these data are not even kept safe, and stolen data can possibly encourage illegal
activities,such asfraud.
1.2 Our Work
Toaddress this situation, we model private information that can be classified into sev-
eral categories as a range of digital commodities that are constantly produced throughout
a person’s life, the value of which is determined by a joint strategy that takes into consid-
eration potential losses caused by disclosure of personal information as well as social and
commercial benefits to be exploited from that data. The actual price of such data fluctuates
around its real value under the influence of supply and demand, the cumulative effect and
many otherfactors.
In this paper, we introduce three feasible techniques. Firstly,we propose a vector-based
representationfor bothdata providersand data queryrequeststhat abstractlyand quanti-


## 第 8 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#93036 Page 2of27
tativelydescribesfeaturesofprivatedata,alongwithancorrespondingvaluepredictorthat
approximates the value function via correlation matrices. Secondly, with the introduction
of a dynamic market system, we are able to further investigate the fluctuation in the real
price influenced by both inner factors (e.g. supply and demand) and external causes (e.g. a
sudden data bleach). Lastly, we develop an social network model to especially investigate
the network effects of data sharing and the impact of social connection on data correlations
withthe multi-dimensional clustering algorithmmCAF.
Themajorcontributionofthisworkisthatwepresentareliablepricemodelforpervasive
collection,sharingandtradingofprivateinformation. Inourexperiments,weapplyandtest
ourmodelunderdiverseconditions,whereitgivesinterestingandreasonableresultswhich
convinces us that the currency of private information should be kept under strict control
under laws andregulationsin orderto maintainahealthy dataeconomy.
2 Assumptions & Nomenclature
2.1 Assumptions
Tobetterquantifytheproblem,ourprivateinformationpricingmodelisbasedonseveral
assumptions that hold true in most cases or is indisputably satisfiable under government
regulation.
Assumption 1. All kinds of private information canbe classified intoafixednumber of distinct
datacategories (e.g. demographics, family& health, etc.), the number is denoted by m.
Assumption2. Personaldatabringsbenefitstothesocietybycontributingtoresearchesthatintends
to study the social and financial behaviors. Profits made from fraud or harassment are not takeninto
consideration.
Assumption 3. For information security and many other concerns, all the gathered data are man-
aged by a trusted third-party organization, which protects uses’ data and helps sell them under
owner’s permission.
Assumption 1 ensures that the number of parameters required to model private data is
limited, thus it makes sense to represent PI with matrices. Assumption 2 guarantees that
an universal understanding of data value exists, which forms the basis of our model. By
assumption3large-scale management and regulationofdata aremadepossible.
2.2 Nomenclature
In this paper we use the nomenclature in Table 1 to describe our model. Other symbols
thatare used onlyonce willbe described later.
3 PIPE: Mathematical Model for Private Information Price
Estimation
In this section, we will discuss all details about our model, which is capable of estab-
lishinganaccuratepricing systemofpersonaldatawiththeapplicationof1)avector-based
representationthat distributesbothbenefitsand risksofdatafromacertainsubgroupover


## 第 9 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#93036 Page 3of27
m data categories; 2) a dynamic pricing strategy that determines the intrinsic value as well
as market price of data; 3) a social network model that further improves the predicting ac-
curacy by takingdata correlationoriginated fromsocialconnections intoaccount.
Table1: Nomenclature
Symbol Definition
m Totalnumber ofdata categories
c The ith category
i
I Individual that producesdata
X Individualfeaturevector
σ(·) Individualfeatureextractor
q PI queryrequest
Y Queryfeaturevector
ϕ(·) Queryfeature extractor
C Correlationmatrix
v Rawvalue ofaperson’sdata under acertainquery
T Sequence lengthofpersonaldata
t Freshness of privatedata
N Quantityofdatarecords
ω Cumulative factorofdatasequence
τ Decay factorofhistorydata
µ Scale factor
vj Amended value ofaperson’sdata under acertainquery
d Data size from personi
i
Totalinformationcontained fromthePI
I
Γ Neighborhood
R Region
Q Typesof Agencies
P Price concerning differentagencies
agency
G Interactionvaluebetweenpersoniandj ofsocialcircle
ij
O Organizations
T Tiestrength
i
Wk Weightsummary ofonemeasurement toonenode
i
Sim Similarity between twovertices
i,j
N ThresholdNeighbor
M Metric that evaluates the sensitivity ofmCAF
Eq(·) Functionthat judges equality
l Grouplabel ofvertexi
i
Our idea is that the intrinsic value of personal data comes from two aspects: the poten-
tialriskfrominformationdisclosure, and thesocialbenefits broughtabout bydataanalytic.
Such benefits and threats posed by personal data varies not only among different data cat-
egories, but also between diverse social subgroups. Another unnegligible factor that affects
the value of data is the data quality demanded by corporations or institutes. For instance, a
commercialdatasetthatrequestsdetailedfinancialinformationshoulddefinitelybecharged
higherthan aroughportrait onlyinvolving the overallincome and tax bills ofthesame so-


## 第 10 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#93036 Page 4of27
cialgroup. Thereisnothingambiguousthatavarietyofadditionalfactorsalsohaveimpacts
on data value, including freshness, quantity and consistency, which are taken into account
inour modelaswell.
Based on such assumptions we model private data as a commodity in continuous pro-
duction,whichisthenfitintoamarketmodelwheredataownerscanchoosetopayforvar-
ious levels of privacy protection, or to put their data on sale via a trusted third-party data
manager. The overall supply is mainly determined by people’s willing to share their data
based on its benefit-risk ratio , while the market demand follows a gaussian distribution
and can be affected by incidents such as data breaches. We further classify data agencies
into three types based on their purchasing power, and develop a pricing strategy for the
third-partydatamanager.
Sincehumandataishighlylinkedand individualbehaviorscanbe quitecorrelatedwith
those whom they are socially, professionally, economically or demographically connected,
wefurtherconsider thenaturalsocialnetworkasagraphandclustersimilar individualson
multiple dimensionsbased onbothnetworkstructure and profile information. Onthe basis
ofsuchsocialclusters,weespeciallypolishourpricingpolicyinconsiderationofsimilarities
withinclustersand distinctions betweenthem.
The overview of our entire pricing framework and three major components of it are il-
lustratedin Fig. 1.
Figure1:The schematicillustrationofthe entiremodel
3.1 Vector-basedRepresentation for Individuals and Queries
3.1.1 Individual FeatureVectors
Based on the assumption in Sec. 2.1 that private data can be classified into m distinct
categories, an individual’s private data can thus be considered to consist of data records in
multiplecategories. Inourmodel,weassumem = 5andthecategoriesincludedemographics,
family& health,property, activities and consumerdata.
The value of a person’s entire data can then be split into m independent category values,
the sum of which is equal to the original data value. Therefore, it makes sense to represent
privateinformationofindividuals withanm× 1 matrix, which isactually avector:
where I is a data provider,element X i(1 ≤ i ≤ m) in vector X indicates the value of I’s
data in the ith category, and function σ(·) extracts such category values based on life events


## 第 11 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#93036 Page 5of27
andindividualattributes.WedefinevectorXaspersonI’sfeaturevectormainlybecauseits
elementsrevealstheessentialvalueofI’sdatathatisdistributedovermcategories.
The core part of Eqn. (1) is the function σ(·) that maps a person to the corresponding
feature vector. The process is accomplished based on an analysis on the most influential
factorsofdatavalueconductedbyFinancialTimes [9]. Thereportpointsoutthatcontraryto
popular belief, the value of private information does not increase linearly with its amount.
Infact,generalinformationaboutaperson,suchastheirage,genderandlocationiswortha
mere $0.0005 per person, or $0.50 per 1,000 people. It is certain milestones in a person’s life
that prompt major changes in data values, such as becoming a new parent, moving homes,
getting engaged, buying acar,or going throughadivorce.
As is mentioned above, the value of data limited to a certain category is defined as the
sum of potential risks and benefits incurred by it. On the basis of the Financial Times re-
port, we develop a sophisticated model that implements the function σ(·). Here we briefly
introduce itsmechanism, the complete implementationcanbe referredto inAppx. A
Apersoncanpossessanumberofattributesatthesametime,suchasbeingengaged,own-
ing a home and current job, and some values of these attributes can possibly incur risks or
benefitsifknownbyadata company,forexample, beingengaged =trueand currentjob=gov-
ernment officer. Our model includes a databases that stores the economical value vectors of
certainattribute-valuepairs,asisshowninTable2,factorsregardingtopersonalproperties,
health conditions and activities are considered more important and attached higher values
thanothers.
Table 2:Some ofthemost significant value vectorsinour
Attributecondition Value vector /$
Beingamillionaire [0.116 0 0 0 0]
Havinga heartdisease [0 0.260 0 0 0]
Registeredat arealestate agency [0 0 0.105 0 0]
Interestedinforeigntravel [0 0 0 0.135 0]
Holdingastoreloyaltycard [0 0 0 0 0.136]
Bysignificancewemeanthemagnitudeofvectorscalculatedbynorm X .Notethatall
|| ||
ourvectorsconcentratevaluesinonedimension(onedatacategory),bywhichweintendto
reducedatacorrelationsbetweencategories,whichwillbereconsideredinSec.3.1.2.
Algorithm 1:Feature vector extractor
Input :Anindividual I, informationvalue database .
S
Output: The feature vector X = σ(P ).
Σ Σ
1X ← 0 0 ...0 ;
2for attr ∈ {P’s attributes} do
3 if (attr,P[attr]) ∈ S.values then
4 X ← X +S[(attr,P[attr])];
5return X;
Asis shown inAlg.1,our algorithmfirst setsthe initialfeaturevector asanall-zero
vectorand thenchecksall theattributes ofthatpersontodetermine ifsome attribute-value


## 第 12 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#93036 Page 6of27
pairscanbefoundinourdatabase. Ifamatchisfound,whichmeansacertainvalue-creating
conditionismet,thevaluevectorcorrespondingtothatattribute-valuepairwillbeaddedto
the person’s feature vector.In other words, a person’s feature vector is the sum of all value
vectorsofthe conditionssatisfied by hispersonalattributes.
BasedonAlg.1,weareabletodeterminethetypicalindividualfeaturevectorsofvarious
socialsubgroups, whichwill be discussed inSec.4.1.
3.1.2 Query Feature Vector&Correlation Matrix
Similar to individual feature vectors defined in Sec. 3.1.1, we define an m ×1 query feature
vector Y = ϕ(q)that represents the query request q with m scalars, each stands for the inten-
sity of private data requested in an data category.The intensity is measured by the amount
as well as accuracy of requested data. For instance, if full information of a person’s demo-
graphiccharacteristics and purchasing historyisrequested,the query featurevectorshould
Σ Σ
be 1 0 0 0 1 .
However,withmerelyqueryvectorswearestillnotabletoaccuratelycalculatethevalue
of private information, as data correlations tend to occur between different categories of
data. Toaddressthisphenomenon,weintroduceacorrelationmatrixC thattakesconnections
betweenvariouscategoriesofdataintoconsideration,anddefinethatthevalueofapieceof
datarecord fromindividual Iqueried withfeature vectorY as
v = σ(P)CY T (2)
.Σ ΣΣ
Ideally, with no data correlations the correlation matrix C = E = diag 1 1 . . . 1 .
In order to estimate the intensity of data correlations, we fill the correlation matrix C in
following manners:
C i,j = |cov(c i ,c j)| (3)
where c and c are the ith and jth data category value. Our final correlation matrix C is
i j
computedbasedonfeaturevectorsextractedfromtypicalpopulationsubgroups,whichwill
be discussed indetailinSec. 4.1and demonstrated inFig.6.
1.0000 0.6463 0.8443 0.8231 0.2793
0.6463 1.0000 0.6767 0.2197 0.2226
C = 0.8443 0.6767 1.0000 0.5403 0.1649 (4)
0.8231 0.2197 0.5403 1.0000 0.6916
0.2793 0.2226 0.1649 0.6916 1.0000
whichsuggeststhat the most magnificent data correlationsexistsbetween data categoriesof
• Demographics&Property
• Demographics&Activities
• Activities&Consumer
On the basis of Eqn. (2) and Eqn. (4), we are able to calculate the raw value of a spe-
cific data record and its query requests. However, there remain external factors that have
strongly affect the real value of private data, among which the most significant one is time.
Itiswidelyacknowledgedthatdatavaluedecayswithtime. Ontheotherhand,aconsistent


## 第 13 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#93036 Page 7of27
datarecordsequencecollectedthroughoutalongtimeperiodshouldbeattachedadditional
value. Similarly, data scale affects the value of private data nonlinearly. Thus, an amend-
ment ismade with Eqn. (2) by introducingvariations:
vj = eωT − τtNµv (5)
where the dynamic element T denotes the sequence length (/days) of data, t stands for the
freshness of private data (days since the data is generated), and N represents the numberof
data records. Parameters ω,τ and µ affects the real value in exponential and multinomial
manners. Inourestimationbased oninformationrules[10], ω = 1.28 10−3,τ = 9.50
× ×
10−4 and µ= 1.05.
3.2 Dynamic Market System & Pricing Strategy
3.2.1 PI DemandModel
s
benefit
λ = ,λ ∈[0,1] (6)
j s + s j
benefit risk
Table 3:Calculationofrisk score(1,2,3,4,5 stand forlevelofrisk)
Criterion 1 2 3 4 5
Financial Risk 0.05 0.062 0.074 0.09 0.128
HealthRisk 0.06 0.09 0.11 0.14 0.24
Family Risk 0.05 0.062 0.088 0.15 0.22
Social Risk 0.03 0.062 0.1 0.13 0.17
Thus, the demanding of an individual j ∈ J+is
Σ dM
D(j)= λ
j
P
j
−r
j
Σ i i,j , (7)
M
i ω J+ i,ω
∈


## 第 14 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#93036 Page 8of27
AsymmetricInformation. Thispartillustratesthatpurchaserspossessasubstantialamount
ofinformationabout data providers. These facts suggest thatthe restrictionssuchas policy
and culture - which make itdifficult for data providerstoadjust prices whenthey provide
privateinformationtopurchasers overtime - havedifferent price effects acrossdifferent
sellersand buyersdepending ontheir privatelyrevealed types, culturalandpoliticalissues.
Incorporatingsuchfactorsinour modelthereforebecome important inanticipationofus-
ing themodel tostudy thePI problem. Formally,we estimatethese effectsin the following
equation8,
Σ5
Default i,t = α j(i) +α t + β n1ψi,t=n +s it (8)
n=1
Here the dependent variable is an indicator for any instance of default by purchaser i af-
ter period t, and the key coefficients β capture differences in default rate across different
n
private information, which denoted by ψ. Meanwhile the fixed effects for purchaser i and
timethelpensurethattheseriskcomparisonsaremadewithinotherwiseobservablysimilar
purchasers.
Model Exposition This section presents the PI model. The backbone of the demand model
isafinite mixtureofagencytypes, each ofwhomhas demand over PI providers.
Our model denotes type by θ. We specify several parameters to be estimated for each
type. First, each type enjoys a flow utility d from buying from person j and a time utility
jθ
n from transacting with person j; meanwhile the utility is normalized to zero. Addition-
jθ
ally, in order to capture the adjustment cost, each type pays a agency cost s for refer to
jθ
potential related PI with person j. The parameters d ,n ,s are the key demand
{ jθ jθ jθ} (θ,j) Θ J
parameterstobeestimatedinthemodel,alongwithaprobabilitydis∈tr×ibutionµ overtypes.
θ
Integrating over taste shocks s for each choice yields the standard Bellman equation for
continuationvaluesV,whichis shownin Eqn. (9).
. Σ
Σ
V(θ,j,k) = log exp(v(jj,kj|j,k,θ)) , (9)
j ,k
j j
wherethelower-case v termdenotestotalexpectedpayoffs. Thevalueofv dependsondata
buyers’ past-period and current-period choices. The expectation E can be decomposed as
θ
Eqn.(10),
E θ[V(θj,j,b)]=(1−δ(θ))T
θθ
(θ)V(θj,j,b)+δ(θ)T
θθ
(θ)V(θjj,0,0). (10)
j j
With the establishment of Eqn. (5), our model further takes time variations and scale
effects as dynamic elements into consideration to estimate the worth of personal data over
time.
3.2.2 Buyer-Seller Relationship Influence toPrice
AsFig.2shows, internetadvertising revenuehasgrownstronglyoverthe lasttenyears.
In2013ithit$42.8billionintheUS. Internetgiantssuch asGoogleandFacebookhavebusi-
ness models underlined by the use of personal data, but most people would have trouble
knowingwhoexactlyhasaccesstothedatatrailtheyaregeneratingacrosstheinternet[11].
ArecentstudybyJPMorganChase[12]foundthateachuniqueuserisworthapproximately
$4toFacebookand $24to Google.


## 第 15 页

Team#93036 Page 9of27
Besides commercialcorpo-
AdvertisingRevenue
40
rations, there arealso other
agencieswho purchase PI.
35
Mozilla collect data about
usersto better personalize 30
theirexperienceswith their
25
opensource products such as
Firefox, Thunderbird. The
20
informationtheygatherthrough
analyticscan be used tomake 15
theirproduct easier touse.
10
They also use cookies(small
2004 2006 2008 2010 2012
datafiles placed in browsers) Year
to remember language pref- Figure2:USInternet AdvertisingRevenue by Year,the
erences. Center for Dis- shadowrepresents statisticaluncertaintyand variance.
ease Controlutilizesthe data
shared totracethe spread ofdisease inordertoprevent furtheroutbreak.
There are 3 types of agencies in our model and their purchasing power is shown as Ta-
ble 4. The price estimationsystemconcerning withdifferent agencieswhopurchased the PI
isillustrated as Eqn.(11).
ΣM
P agency = τ jQi , (11)
j=1
where τ is the control level of individual j to sell his/her own data, there are totally M
j
individuals in a group/nation, can be , or which represents the purchasing
Qi Q1 Q2 3Q
power of different types of agencies.
3.3 mCAF: a Multi-dimensional Clustering Algorithm for Friends of So-
cial Network Services
The multi-dimensional clustering algorithm for friends (mCAF) is adopted by us to per-
form multi-dimensional clustering. Multi-dimensional clustering algorithms on social net-
works are progressively gaining popularity due to the information and insights produced
using large-scale social data. [13] describes the user’s opinions, comments, and likes in so-
cialmediahavesignificantrelationshipswiththepopularityofthatpost. Multi-dimensional
cluster analysis is a strategy for identifying different Facebook users’ fan groups and pro-
videsinsightstopromptfurtherresearchanalytics[14]. Bothnetworkstructuresandprofile
information should be taken into consideration while analyzing a user’s clusters on social
networks[6,15].
Table4:Purchasing powerofthreetypesofagencies
Denotation Typesof Agencies
Q Commercial Corporation, e.g. Google, Facebook, Microsoft, etc.
1
Q Non-Profit Organization (NPO), e.g. Mozilla, GNU, WWF, etc.
2
Q Government Department,e.g. NSA, Department ofEnergy, etc.
3
)nb$(
ecirP
精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！


## 第 16 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#93036 Page 10of27
Inthisstudy,weusedtheFacebookGraphAPItoretrieveinformationof600users. First,
we define the measurementsofclustering.
SocialCircles. Asocialcircleisagroupofpeoplewhohavethesameinterestsorjointhe
sameactivity.WedefineM asthenumberofmutualfriendsofuseriandjandG asthe
ij ij
interactionvalue.Wequantifythesubject’sinteractionswithinthecommunitytoobtainS
ij
withEqn.(12)andthennormalizetheresultasEqn.(13)
MG
ij
=M ij+G
ij
,MG={MG
xy
|x,y ∈1,2,3,...,n} (12)
MG
ij
S ij = max(MG) ,S = {S xy | x,y ∈ 1,2,3,...,n} (13)
Regions. Wedeterminetheregionoftheusersandthencalculatethe distancesbetween
themandstorethemasadatasetdescribedby D ,D ,D ,D . Takethecalculationofdis-
{ 1 2 3 4}
tancebetweenAandBasanexample,D representsthedistancebetweenthehometowns
1
ofA and B; D represents the distance between the current residence of A and B; D rep-
2 3
resentsthe distancebetweenA’shometownandB’s currentresidence; D representsthe
4
distancebetweenA’scurrentresidenceandB’shometown.ThecalculationofR isshown
ij
as Eqn.(14).
R ij = α×D 1 +β ×D 2 +γ×D 3 +δ×D 4 (14)
Organizations. If two individuals attended the same school or worked in the same com-
pany,the organizationsmeasurement O issetequalto1since theyhaveaconnection. Ifno
ij
connectionispresent, the O isset equal to0.
ij
Tie strength. We retrieve related information and use the method described in [16] to cal-
culate the tie strength as T, which indicates the tie strength between a user and his jth
j
friend.
mCAFmaps auser’s friendsintoun-directed, weighted graphs. Wedefine the entire
graphasG = {V, E},inwhich Visthe set ofverticesandE isthe setofedges, defined as
. Σ
E i,j(ek
i,j
) ,whichrepresents aconnectionifavalue ek
i,j
isgreaterthanzerobetween nodes
iandjundermeasurementk.
Definition of vertex structure. Let vertex i V ,where the structureofi isdefined byits
∈
neighborhood denotedby Γ (i)inEqn. (15)
Γ(i) = {j |j ∈V ∧E i,j ∈E} (15)
Definitionoftheweightsummaryofonemeasurementtoonenode Eqn. (16) definesthe
summaryvaluesofmeasurements fromvertexj, whichis connected toi:
jΣ=V
| |
W k = (ek ), wherej ∈ Γ(i) (16)
i i,j
j=1


## 第 17 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#93036 Page 11of27
Definition of the weight summary of one measurement to two nodes Let vertex m V,
∈
andletedgesfrom(i,m)and(j,m)exist.Eqn.(17)definesthesummaryvaluesofmeasure-
mentsfromvertexm,whichisconnectedtoiandj:
Definition ofstructuresimilarity Shestructuresimilarityoftwoverticesiandjisdefined
as Eqn.(18):
1 2 3
. Σ {T ,T ,T }
Sim = S1 ,S2 ,S3 = . i,j i,j i,j (18)
i,j i,j i,j i,j
W
i
1 ·W
j
1 +W
i
2 ·W
j
2 +W3
i
·W
j
3
Definition of the threshold neighbor If two nodes can be clustered together based on
measurementk,theirstructuresimilarityvalueSk mustbegreaterthanthepresetthreshold
i,j
sk tofilterout noise. Eqn(19) defines neighborswith qualified similarity structurevalues.
The parametersk could be estimated viatraining.


## 第 18 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#93036 Page 12of27
. Σ
N sk(i) = j|j ∈ Γ(i)∧Sk
i,j
≤ sk where k = 1 to 3 (19)
The complete mCAFalgorithmis described in Algorithm2.
The clustering result of mCAF is shown in Fig. 3. The social network of several individ-
uals are clustered into 8 subgroups. The visualization of network shows the correlations
betweendifferent people.
2.0
2.0
1.5 1.5
I
1.0
0.5
1.0
5
4
0 3 0.5
1 2
2
3 1
4 5 0
Figure3: mCAFClustering Result ofSocial Figure4:Relationship betweendata size d
i
Network and information I
To better evaluate the network effects of data sharing, we investigate the relationship
between two individuals who are highly linked and discover the relationship between the
datasizefromonepersonandtheinformationitcanprovide. Defined isthedatasizefrom
i
person i and I= f(d) [∈0,1] represents the information the data on one person can provide.
There are totally M individuals. Eqn. (20) represents the function between d and and Fig. 4
I
illustratesthefunctionin thecircumstance ofi = 2.
ΣM
I= log(1+ d i) (20)
i=1
4 Experimental Results
4.1 Task1: Price Point for Protecting One’s Privacy and PI in Various
Applications
Inordertoaccuratelymodelrisktoaccount forboth1)characteristicsoftheindividuals,
and 2) characteristics of the specific domain of information, we introduce the concept of
individualand queryfeaturevectorsdiscussed inSec.3.1.
Aftersurveyingonseveraldatasets[17,18,19]andrecentmethods,wecollectourdataset
PIDATAwithanAPIprovidedbyFacebook[20]. TheusageofthisdatasetobservesthePlat-
formPolicies,DataUsePolicy,StatementofRightsandResponsibilities. Correspondingstatistical
informationisillustratedasFig.5. Fig5(a)isagedistribution. Fig5(b)isgenderdistribution.
Fig 5(d) is education distribution. Fig 5(c) is occupation distribution. Fig 5(e) is education
occupationdistribution. Fig 5(f)is friend distribution.


## 第 19 页

Team#93036 Page 13of27
0.016
0.20
0.014 50
0.012 0.15
40
0.010
0.10 0.008 30
0.006 0.05
20
0.004
0.00
0.002 10
0.000
0
0 20 40 60 80 100 Female Male Occupation
Age Gender
(a) AgeDistribution (b) GenderDistribution (c) OccupationDistribution
0.4 0.0200
0.0175
0.3
0.0150
0.0125
0.2
0.0100
0.1 0.0075
0.0050
0.0
0.0025
0.0000
0 50 100 150
EducationLevel EducationLevel NumberofFriends
(d) EducationDistribution (e) Education-OccupationJoint (f) Numberoffriends
Distribution
Figure5:Statistic informationofPIDATA
Fig. 6 shows the distribution of private data over different data categories (feature vec-
tors) of 6 selected subgroups. It is clear that the value of person’s data is partially related
hisageandsocialstatus. AnotherinterestingobservationfromFig.6isthathighcovariance
existsbetweencertaindata categories,which will be dealtwith inSec.3.1.2.
Figure 6:Individualfeaturevectorsofsome typicalsubgroups.
Todevelop a price point for PI protection, we exam the true value of a person’s fulldata
and its components. Fig. 7 shows how different categories of private data contributes tothe
value ofaperson’sPI.
oitaR
oitaR
noitapuccO
rebmuN
oitaR
oitaR
精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！


## 第 20 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#93036 Page 14of27
Figure7:Value componentsofdifferent subgroups’sPI.
Based on the computed value of personal information, we are able to establish a price
point for protecting it by treating data protection as an special insurance. Although the
trade value of data can is just a few dollars, cost for each stolen data record can be as high
as $141 - roughly 70-fold of its trade value, and the likelihood of a recurring material data
breach over the next two years is estimated as 27.7%, according to a data breach study by
IBM [21]. Therefore, to firmly protect a certain data record for 1 year, one must invest 10
times of its trade value calculated from Eqn. (5), which leads to the deduction that it might
be bettertoshare personaldata and make profitsfromit ifthe risk islow.
4.2 Task2: Pricing Structure of PI
Withthe introductionoffeature vectors, correlationmatrixand the amendment formula
(Eqn. (5)), we can simply determine how much a person’s information is worth given a
queryonaspecificdomain. Basedonathoroughsurveyon77adults,weareabletoestimate
the corresponding query feature vector of several query domains. The results are listed in
Table5.
Based on query feature vectors in Table 5 and Eqn. (2), values of private information
queried by differentdomains are illustratedin Fig. 8.
From results shown in Fig. 8, we can establish a pricing structure correspondingly. The
price is explicitly calculated in view of different basic elements of data via individual fea-
turevectorsdefined inSec. 3.1.1.Asforcost ofprivacyacross variousdomains, itcan be
Table5:Comparisonbetweenquery featurevectorsfromvariousdomains
Domain Averagequeryfeaturevector
Social media [0.93 0.68 0.13 0.96 0.37]
Financialtransactions [0.82 0.53 0.94 0.24 0.98]
Health/ media records [0.26 0.99 0.08 0.11 0.10]
Searchhistories [0.66 0.58 0.13 0.74 0.84]
Locationinfo [0.24 0.05 0.05 0.35 0.12]


## 第 21 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#93036 Page 15of27
Figure8:Informationvalue invarious domainsofsome typical subgroups.
calculatedinsimilarmannersasSec.??,whereprotectingcostandtradevalueofdataarein
direct proportion. If the risk of data disclosure is negligible, spending considerable money
ondataprotectionwouldbeanunnecessarycost,andpeoplemightprefertohavetheirdata
unprotectedinordertosavebudgets.
4.3 Task3: Supply and Demand
PeoplebecomemoreclearaboutwhichagencieshadpurchasedtheirPI,howmuchtheir
PI was worthand howPI wasbeingused.
Based on the above model, we evaluate the influence of the control level to the price of
PI. Withdata becoming acommodity, we find that:
It is appropriate to consider forces of supply and demand for PI. Commercial Corpo-
•
rations have higher demand for PI, which makes it possible for them to provide
Q1
higher offercompared withthe othertwo typesofagencies.
Ifpeoplehavecontroltoselltotheirdata,whichmeansτ varieswithdifferentindi-
• j
viduals, the price P increases with the τ.
agency j
4.4 Task4: Assumptions and Constraints - Political/Cultural Issues
The assumptions and constraints of our model, which is also the political and cultural
issues of the United States, European Union and other countries is listed as below.Suppose
our model is proposed under the circumstance which is in compliance with local govern-
mentregulationsandculturalissues. Firstly,weexplaintheterminologyusedinthemodel.
4.4.1 Explanation ofTerminology
Agency: anycorporations, organizations,Executivedepartment,militarydepartment,
•
Government corporation, Government controlled corporation, or other establishment
inthe executivebranch oftheFederalGovernment.
Individual: a citizen of the United States or an alien lawfully admitted for permanent
•
residence.


## 第 22 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#93036 Page 16of27
Private Information: any item, collection, or grouping of information about an indi-
•
vidual that is maintained by an agency, including, but not limited to, his education,
financial transactions, medical history, and criminal or employment history and that
contains his name, or the identifying number, symbol, or other identifying particular
assigned tothe individual, suchas afingerorvoice print oraphotograph.
4.4.2 Political Issues and Cultural Issues
TheUnited States: PrivacyAct [22]
The Overview of the Privacy Act of 1974, 2015 Edition is prepared by the Department of
Justice’s Office of Privacy and Civil Liberties (OPCL). Tracking the provisions of the Act
itself, the Overview provides reference to and legal analysis of court decisions interpreting
theAct’sprovisions.
The purpose ofthe Privacy Actistobalance the government’sneed tomaintaininforma-
tion about individuals with the rights of individuals to be protected against unwarranted
invasions of their privacy stemming from federal agencies’ collection, maintenance, use,
and disclosure ofpersonalinformationabout them. Moredetailsare inthe Appx.B.
EuropeanUnion: GeneralDataProtection Regulation(GDPR)[23]
The GDPR aims primarily to give control back to citizens and residents over their per-
sonaldataandtosimplifytheregulatoryenvironmentforinternationalbusinessbyunifying
the regulation within the EU. The regulation was adopted on 27 April 2016. It becomesen-
forceable from25 May2018after atwo-yeartransitionperiod.
Data breaches. Under the GDPR, the Data Controller will be under a legal obligation to
notify the Supervisory Authority (SA) without undue delay.The reporting of a data breach
isnotsubjecttoanyde minimisstandardandmust bereportedtotheSupervisoryAuthority
within72 hoursafter havingbecome awareofthe databreach.
CitizenControlofPersonalData.UndertheGDPR,organizationsareencouragedtogive
back controlofpersonaldata tothe individual, orcitizen.
Canada:PersonalInformationProtection andElectronicDocumentsAct
The Personal Information Protection and Electronic Documents Act (PIPEDA or the
PIPEDAct)isaCanadianlawrelatingtodataprivacy. Itgovernshowprivatesectororgani-
zations collect, use and disclose personal information in the course of commercialbusiness.
Inaddition,theActcontainsvariousprovisionstofacilitatetheuseofelectronicdocuments.
The lawgivesindividuals the right to
• knowwhy anorganizationcollects, uses ordiscloses theirpersonalinformation;
• knowwhointheorganizationisresponsibleforprotectingtheirpersonalinformation;
expect an organization to protect their personal information by taking appropriatese-
•
curitymeasures;
• obtainaccess to theirpersonalinformationand ask for correctionsifnecessary;and
Japan: Act onProtection ofPersonalInformation(APPI)


## 第 23 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#93036 Page 17of27
APPI reflectsthe Japanese socio-cultural characteristicsforpersonalinformationprotec-
tion.Personalinformationleakagecases andsocial responsesin Japanreflect threeJapanese
socio-culturalcharacteristics: Uchi/Sotoawareness,insularcollectivismandHon’ne/Tatemae
tradition. Aneffectivelaw protecting personalinformationinJapan’sculturalenvironment
cannot be made simply by copyingthe privacyprotectionlaws inwesternnations. Instead,
legalprotectionofpersonalinformationshould be drafted thatreflectsand takesinto ac-
count these socio-cultural characteristics[24].
4.4.3 Price Regulations
Generally, the data value of people varies from different regions. It’s common to see
quitealotofvariationbylocation. Fig.9isthestatisticalresult,whichisacomparisonofthe
totalnumber ofaperson’sdata value forcountriesaround the world (oneswithout enough
dataare left gray)[25]:
Based on the model and the political/cultural issues, we can draw the conclusion that
information privacy should be made a basic human right when thinking about policy rec-
ommendations.
4.5 Task5: Generation Difference
In the perspective of risk-to-benefit ratio of PI and data privacy, there are generational
differences. Forexample,therisk-to-benefitratioisdifferentbetweenoldpeopleandyoung
people when their health record is leaked. For old people, it is usually much higher than
thatofyoungpeople.
As generation changes, the input individual attributes change and data value depends
on the generation correspondingly. As for the risk-to-benefit factor we defined in Eqn. (6),
it describes the risk-to-benefit ratio of PI. The factor will change since the benefit score and
risk score will change. Considering all the effects that generation change have, our final
data price will be affected in the process above. PI (private information) is different from
PP (private personal property) and IP (intellectual property). PI is an abstract concept. It
isnon-entity.HoweverPPoftenreferstothepropertyofpeople. It physically exists. IP is
Figure9:Data Value bylocations: comparisons ofthetotal number ofaperson’s datavalue
forcountriesaround the world(ones withoutenoughdata areleft gray)


## 第 24 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#93036 Page 18of27
Figure10:CostofData Breach inDifferent Industries
thepropertyofhuman intellect including copyrightsand patents. PI isonly knownby the
ownerbut IPisnot onlyknownby the owner.People all knowthe owner ofthe IP.
PI is also similar with PP and IP to some extent. PI and PP are both private while PI and
PPare bothabstract.
4.6 Task6: mCAF: a Multi-dimensional Clustering Algorithm for Friends
of Social Network Services
Based onthe mCAF modelwe proposed previously, we have the following conclusions:
Networkeffectsofdatasharingsharingdoeffectthepricesystemforindividuals,sub-
•
groups, andentirecommunitiesandnations.
Itis theresponsibility ofthe communitiesto protectcitizen’s PI ifcommunitieshave
•
shared privacyrisks.
4.7 Task7: Data Breach Effect
Data breach, especially massive data breachwhere millionsof prople’sPI arestolenwill
affecttheprivacyalot. TakingTJXdatabreachasexample,itinvolvesmorethan100million
records and causes 118 million dollars loss to cover the loss and potential liabilities. That
doesnotincludethelossinreputationofbrandandotherindirectcost. Fromtheresearchof
IBM [21], we get cost of data breach for different industries (Fig. 10) and countries (Fig.11).
Wecan see thatdata breachwidely existsand PI lossis afactorthatwe should notneglect.
ThePIlossandcascadeeventcausedbymassivedatabreachwillimpactthepricepoint.
Inourmodel,wehaveconsideredsucheffect. Eqn.(7)showsthetradeoffbetweentheprice
and data breach effect. When massive data breach happens, the trade off factor λ will be
j
smaller and thus λ p will be smaller. r depends on the level of data breach. For massive
j j j
data breach and the corresponding cascade event, it would be higher. Wecan see that the


## 第 25 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#93036 Page 19of27
Figure11:Cost ofData BreachinDifferentRegions
price will be lower. It is reasonable since data breach will violate the assumption that all
the gathered data are managed by a trusted third-party organization, which protects users’
data and helps sell them under owner’s permission. People’s data will be sold without
permissionorevenbeused asransom. SomePIbuyerswillbuythebreachdatainanillegal
way instead of buying data from people or trusted third-party organization. Demand will
decrease and the price willbelower.
Agencies that breach the data should be responsible for the data breach and pay the
individuals directly. As shown above, price of data will be much lower after massive data
breachhappens. Theagenciesshouldberesponsible forthePIlosseveniftheydon’tintend
tobreach thedata.
5 Sensitivity Analysis
In this part we will do sensitivity analysis on our model. The sensitivity analysis show
that our model is generalized and performs stably under different conditions, by which we
areconvinced thatourmodelis able tosolve theproblemsuccessfully.
5.1 Demand Model
This part shows the PI purchasers are sensitive to price and illustrates how it ispossible
to identify heterogeneous price sensitivities in the data. This heterogeneity will play a key
role when we later use the model to study the equilibrium effects of the PI’s price restric-
tions, because this heterogeneity affects which types of purchasers change theirpurchasing
behaviorinresponse todifferent relative pricechanges.
The event-time-specific estimatesis shown asEqn. (21):
logQ jt = α j +α t +β j t+α A,t +s jt , (21)
whereQ denotesretentionratesamongexistingbuyersfordataproviderjattimet. The
jt
first two α terms in this equation implement a standard difference-in-difference design,
while the α terms capture differences between data provider A and other.For sakeof
A,t


## 第 26 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#93036 Page 20of27
presentation, theβ termisincluded toaccount fordifferenttimetrendsamongtheincluded
data providers. When estimating the demand side of the model, we use price variation to
estimateheterogeneous price sensitivitiesacross different purchasertypes.
5.2 mCAF Model
We adopt the multi-dimensional clustering algorithm for friends (mCAF) to perform
identify social clusters. mCAF algorithm randomizes the center points initially. We run
mCAF severaltimesonourdataset PIDATA and analyze theresult.
We propose a metric to evaluate the sensitivity of mCAF in Eqn. (22), where Eq(·) is
defined in Eqn. (23)
Table6 shows the results from 8 experiments, from which we can conclude that the δ is
very small in all experiments. It proofs that mCAF model perfoms well and is robust under
different situations.
Table 6:Result ofSensitivityAnalysisonmCAF
ExpNo 1 2 3 4 5 6 7 8
δ 0.025 0.013 0.025 0.013 0.051 0.013 0.013 0.025
6 Conclusions and Future Work
We develop a complete pricing system that accurately estimates the intrinsic value as
well as market price of a certain individual’s data under a specific query request. Out
method consists of three core components: a value calculator that maps a query and an
individual to value of that data, a dynamic market system to further compute its market
price, and a social cluster model to estimate the network effect on data price. In the envi-
ronments and sensitivity analysis of our model, we find that it is accurate and generalized
enoughtobe adopted inawide range ofdomains.
One limitation of our current approach is that our model requires a large dataset topre-
cisely estimate the correlation matrix as well as many other parameters used in its mecha-
nism. A promising future direction is to combine out methods with better estimation algo-
rithms,e.g. AnalyticHierarchyProcess(AHP),toreducethevariancecausedbyinsufficient
data.
In future work, our goal is to introduce non-linear data value predictors, e.g. neural
networks, to characterize a more complicated relationship between individuals and data.
Additionally,weplantoextendthecurrentdatasetinbothscaleandcoveragetocatertothe
needsofdeeplearningalgorithms.


## 第 27 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#93036 Page 21of27
References
[1] M. Davis, R. Martinez, and C. Kalaboukis, “Rethinking personal information - work-
shoppre-read.”InventionArts and WorldEconomicForum,2010.
[2] R. David, G. John, and R. John, “Data age 2025: The evolution of data to life-critical,”
seagate.com. Framingham, MA, US: International Data Corporation, Tech. Rep., 04
2017.
[3] “Bigdata,”Wikipedia. [Online]. Available:https://en.wikipedia.org/wiki/Big_data
[4] Y.Lv,Y.Duan, W.Kang, Z. Li, and F.-Y.Wang,“Trafficflow prediction with big data: a
deeplearningapproach,”IEEE TransactionsonIntelligentTransportationSystems,vol.16,
no. 2,pp.865–873,2015.
[5] D. W.Bates, S. Saria, L. Ohno-Machado, A. Shah, and G. Escobar, “Big data in health
care: using analytics to identify and manage high-risk and high-cost patients,” Health
Affairs,vol. 33,no.7,pp. 1123–1131,2014.
[6] R. Gross and A. Acquisti, “Information revelation and privacy in online social net-
works,”in ACMWorkshop on Privacy in the ElectronicSociety,2005,pp.71–80.
[7] “Data breach,” Wikipedia. [Online]. Available: https://en.wikipedia.org/wiki/Data_
breach
[8] B. Debatin, J. P.Lovejoy,A.-K. Horn, and B. N. Hughes, “Facebook and onlineprivacy:
Attitudes, behaviors, and unintended consequences,” Journal of Computer-Mediated
Communication,vol. 15,no. 1,pp.83–108,2009.
[9] E.Steel,C.Locke,E.Cadman,andB.Freese,“Howmuchisyourpersonaldataworth?”
https://ig.ft.com/how-much-is-your-personal-data-worth, Financial Times, 2013.
[10] C.ShapiroandH.R.Varian,InformationRules: AStrategicGuidetotheNetworkEconomy.
Harvard BusinessPress,1998.
[11] J. Detemple and M. Rindisbacher, The Private Information Price of Risk. Palgrave
Macmillan UK,2016.
[12] J. Brustein, “Start-ups seek to help users put a price on their personal data,” The New
YorkTimes,vol.12,no. 3, 2012.
[13] H. Khobzi and B. Teimourpour,“How significant are users’ opinions in socialmedia?”
InternationalJournal ofAccounting &Information Management,vol. 22,no.4,pp.254–272,
2014.
[14] E. Wallace, I. Buil, L. de Chernatony, and M. Hogan, “Who “likes” you and why? a
typology of facebook fans: From “fan”-atics and self-expressives to utilitarians and
authentics,” Journal of AdvertisingResearch,vol. 54,no. 1,pp.92–109,2014.
[15] J. Mcauleyand J.Leskovec, “Discoveringsocial circlesinegonetworks,” ACMTransac-
tions on KnowledgeDiscovery fromData (TKDD),vol.8,no. 1,pp. 1–28,2014.
[16] T. T-H, C. H-T, C. Y-J, H. Y-H, L. D-H, K. C-C, and Y. T-Y, “TreeIt: an application to
create, maintain, and enhance online social connections,” in Networking and Electronic
CommerceConference(NAEC).NAEC2014,2014.


## 第 28 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#93036 Page 22of27
[17] A. L. Traud,E. D. Kelsic, P.J. Mucha, and M. A. Porter,“Comparing community struc-
tureto characteristics in online collegiate social networks,” SIAM Review, vol. 53,no. 3,
pp.526–543,2011.
[18] H. A.Schwartz,J. C.Eichstaedt, M.L.Kern, L. Dziurzynski, S. M. Ramones,
M. Agrawal, A. Shah, M. Kosinski, D. Stillwell, M. E. Seligman et al., “Personality,gen-
der, and age in the language of social media: The open-vocabulary approach,” PloS
One,vol. 8,no.9,p.e73791, 2013.
[19] A. Pak and P.Paroubek, “Twitter as a corpus for sentiment analysis and opinion min-
ing,” in International Conference on Language Resources and Evaluation, Lrec 2010, 17-23
May 2010,Valletta, Malta,2010.
[20] W.Graham, Facebook APIdevelopersguide. Infobase Publishing,2008.
[21] P. Allor, “Cost of data breach study,” https://www.ibm.com/security/data-breach,
2017.
[22] J. T.O’Reilly,“The privacyact of1974.”Censorship,vol.61,no.2,p.7,1975.
[23] G. D. P.Regulation, “Regulation (eu) 2016/679 of the european parliament and of the
councilof27april2016ontheprotectionofnaturalpersonswithregardtotheprocess-
ing of personal data and on the free movement of such data, and repealing directive
95/46,” Official Journal of the EuropeanUnion (OJ),vol. 59,pp.1–88,2016.
[24] Y. Orito and K. Murata, “Socio-cultural analysis of personal information leakage in
japan,” Journal of Information, Communication and Ethics in Society, vol. 6, no. 2, pp. 161–
171,2008.
[25] V.Gkatzelis,C.Aperjis,andB.A.Huberman,“Pricingprivatedata,”ElectronicMarkets,
vol.25,no. 2,pp.109–123,2015.
A Implementation of Function σ(·)
Weformatour attribute, value database inthe formofareader-friendly questionnaire
( )
consistingoffiveparts,eachcorrespondingtoadatacategoryasvaluevectorsinourdatabase
concentratevaluesin onedimension. The five scoresgenerated by the following question-
naire makeup forthe five elementsinthe individualfeature vectorofthetester.
A.1 Demographics
Hasthe following informationbeenleaked? Value
Age $0.0005
Gender $0.0005
ZIPCode $0.0005
Ethnicity $0.005
Educationlevel $0.0005


## 第 29 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#93036 Page 23of27
Are youamillionaire? Value
Yes $0.116
No $0
Are youengagedto be married?Ifso,how long? Value
Yes,one monthorless $0.12
Yes,one tothreemonths $0.115
Yes,more thanthreemonths $0.10
No $0
Are you? Value
Recentlymarried? $0.01
Recentlydivorced? $0.01
Emptynester? $0.01
Whatis your job? Value
Accountant $0.072
Altorney $0.08
Bankingand finance executive $0.08
Chairman $0.076
Chiefexecutive $0.086
Chieffinancialofficer $0.086
Chiefinformationofficer $0.086
Chiefoperatingofficer $0.086
Chieftechnologyofficer $0.086
Companyowner $0.086
Cosmetologist+Beauty $0.072
Entrepreneur $0.10
Healthprofessional $0.072
Humanresourcesexecutive $0.08
Homeimprovement contractor $0.072
Insurance agent $0.072
Licensed professional $0.072
Manufacturing& Engineering $0.072
Non-profit $0.072
Pilot $0.072
Pharmaceutical industry exec $0.076
President $0.086
Realestate agentorbroker $0.072
Vice chairman $0.086
Other $0


## 第 30 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#93036 Page 24of27
A.2 Family & Health
Do youhave children? Value
Yes $0.005
No $0
Areyouexpecting ababy?Ifso, will thisbe yourfirst Value
childand which trimesterareyouin?
YesYesFirst $0.095
YesYesSecond $0.115
YesYesThird $0.115
YesNo First $0.08
YesNo Second $0.10
YesNo Third $0.10
No $0
Areyouanewparent?Ifso, is your newbaby aboy or Value
girl?
YesBoy $0.035
YesGirl $0.035
No $0
Do youhave any ofthe following conditions? Value
Acid reflux $0.26
ADHD $0.26
Allergies $0.26
Arthritis $0.26
Asthma $0.26
Back pain $0.26
Clinical depression $0.26
Diabetes $0.26
Frequentheartburn $0.26
Headaches/migraines $0.26
A.3 Property
Do youown ahome? Value
Yes $0.085
No $0


## 第 31 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#93036 Page 25of27
Ifyouownahome, itis likelythat datacompanies already Value
knowthisinformationabout youfrompublic databases:
The size ofyourhome $0.005
The size ofyourmortgage $0.005
Howmany bathrooms the propertyhas $0.005
Howmany bedrooms the property has $0.005
Ifyouownahome, Hasthe following informationbeen Value
releasedonpublic databases?
Yes $0.085
No $0
Isthereafireplace inyour home? Value
Yes $0
No $0
A.4 Activities
Doyouhave anyofthesehobbies? Value
Areyouacruiseenthusiast? $0.03
Areyouafitness andexcercisebuff? $0.03
Areyouinterestedinforeigntravel? $0.03
Doyouownanaircraft? Value
Yes $0.085
No $0
Doyouownaboat? Value
Yes $0.076
No $0
Doyouexercise orparticipatein otheractivitiestolose Value
weight?
Yes $0.105
No $0


## 第 32 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#93036 Page 26of27
A.5 Consumer
Have yousearched online orvisited websitesrecently on Value
anyofthese topics? (please select asmany as appropriate)
Auto $0.0021
Financial information $0.001
Retail $0.001
Travel $0.001
Gossip $0.0013
Gaming $0.0013
Food $0.0013
Education $0.0013
Cooking topics $0.0008
Movie information $0.003
Political and govermentaltopics $0.0019
Telecom and televisionpurchase research $0.0015
Do youhold anystoreloyaltycards, at agrocerystoreor Value
pharmacy, forinstance?
Yes $0.001
No $0
Areyoulooking tobuy anyofthese products? (Select as Value
many asappropriate)
Car(s) $0.0018
Consumer packaged goodssuch assoap, shampoo, toilet $0.001
paperetc
Education $0.0013
Financial products orservices $0.001
Othervehicles $0.0011
Clothes $0.0008
Travel $0.0011
Areyoulooking tobuy amobile phone? Value
Yes $0.0125
No $0
B Privacy Act
In 1974, Congress was concerned with curbing the illegal surveillance and investigation
of individuals by federal agencies that had been exposed during the Watergate scandal. It
wasalso concerned withpotentialabuses presentedby the government’sincreasing use of


## 第 33 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#93036 Page 27of27
computerstostoreandretrievepersonaldatabymeansofauniversalidentifier-suchasan
individual’ssocial security number.The Act focuses onfour basicpolicyobjectives:
• Torestrict disclosure ofpersonallyidentifiable recordsmaintained byagencies.
Tograntindividuals increased rightsofaccess to agencyrecordsmaintained onthem-
•
selves.
To grant individuals the right to seek amendment of agency records maintained on
•
themselvesuponashowing thatthe recordsarenotaccurate,relevant,timely,orcom-
plete.
Toestablishacodeof"fairinformationpractices"thatrequiresagenciestocomplywith
•
statutorynormsfor collection,maintenance, and disseminationofrecords.

# F83744-Private Information Pricing System Based on Game Theory and Graph Theory


## 第 1 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
TeamControlNumber
Forofficeuseonly Forofficeuseonly
83744
T1 F1
T2 F2
ProblemChosen
T3 F3
F
T4 F4
2018
MCM/ICM
SummarySheet
Private Information Pricing System Based on Game Theory and
Graph Theory
To study the issues regarding private information (PI), build a pricing system and offer
recommendationsto government, we build our primary model based ongame theory and extend itby
referring to graph theory. We assume there are three components of the society: individuals,
organizationsandgovernments.IndividualsdecidewhethertosellanddisclosePItoorganizationsand
they both make every efforts to maximize their own benefits. The government, as a social planner, can
adoptsomemeasurestomaximizesocialutility,includingbothindividualsandorganizations.Weseta
dynamic perfect-information two-stage sequential game to predict the behavior of individuals and
organizations,wheresimultaneously,wetrytoexplorethepolicyimplicationsforgovernment.
First,tomodelriskofdatadisclosureforindividuals,wedividetheriskintothreeprimaryandpossible
categories. Each sub-risk is affected by different characteristics of the individuals and specific kind of
information.Toprovideaninsightofhowtoquantifytheserisks,weprovidesomeroughestimationof
each sub-risk on the most influential factor. Considering the weights of these sub-risks may be
distinctive in different PI domains such as social media, financial transaction and health records, we
employAHP to quantify the weights given that there are few data available in this field. Then, we use
the amount of information as an essential factor influencing the value of data disclosure for both
individuals and organizations. We create a method to quantify the amount of PI with the category of
basic and profitable information. Naturally, we assume the benefit of individuals and organizations
increaseswithlargeramountofPI.
Next, we enter the main part of our analysis to solve the game. By discussing the equilibrium and
constraints in the game, we predict every market outcome with different parameter settings. The
equilibriumallowsustoaddintheroleofgovernmentswheretheycanuseanelaboratepricingsystem
to offer recommended price of different PI and strengthening market surveillance to make the market
moreeffective.
The following parts will show several applications of our model under different circumstances. We
discuss whether PI should be made a basic human right from economics perspective, introduce
dynamic time influence on data value, consider how generational risk perception difference will affect
themodelandprovidesuggestionsforpolicy-makingduringamassivedatabreach.
Lastly, to extend our model on network effect of PI, we employ a network simulation based on graph
theory with consideration of information externality. We find that the social utility will be greatly
miscalculated if we ignore the network effect, leading to the failure of pricing system. Nevertheless,
withPigovianTaxation,orsubsidy,oninformationdisclosurewithstrongexternality,governmentscan
erasetheexternalityeffectandincreasethetotalsocialutility.


## 第 2 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team83744 PIPricingSystemBasedonGameTheoryandGraphTheory
MEMORANDUM
To:PresidentofGovernment
From:Team83744
Subject:PolicyRecommendationonPrivateInformation
Date:February12,2018
Thismemoispresentedtoprovideyouwithanoverviewofourmodelsonprivacy,corresponding
results and policy recommendations. Our team has investigated various issues and aspects about
privateinformation(PI)andbasedonourinvestigation,weintroducedsomeusefulparametersand
buildtwoprimemodelsutilizinggametheoryandgraphtheoryrespectively.
In our first model based on game theory, four key exogenous parameters are introduced and e-
laborately discussed: r , the risk of data disclosure on individuals (e.g. identity theft, spam and
1
price discrimination); w, the benefit of data sharing for individuals (e.g. service personalization
and health condition analysis report); b, the benefit of data sharing for organizations owning the
information (e.g. targeted advertisement and reasonable price setting); p , the probability of data
s
beingstolen,orillegallyusedwithoutindividual’sconsentbyorganizations(e.g.datahacking).We
adopt assorted measures to account for some major impacts for each parameter. Then we use the
frameworkofgametheorytopredicthowtheseparameters’changeswillresultinthevariationof
marketoutcomes.Next,toexplorehowgovernmentcanplayapositiveroleinthisfieldandenlarge
the total social utility,we further introduce P (price suggested by government on PI transactions)
andr (theriskoforganizations’beingpunishedbygovernmentforillegallycapturingindividuals’
2
data).
After calculation by game theory,the larger value of w, b and the smaller value of r can lead to
1
greaterpossibilityofNashEquilibriumofmarketdisclosureortransaction,whichmeansthosemar-
kettransactiondataaremorelikelytobesharedbyindividuals tocompanies becauseindividuals
canreceivethebenefitoftargetedoffers(w)andcompaniescanuseittolocatepotentialcustomers
(b). The effect of p is more complex. Weuse the method of Shapley Valueto derive a fair pricing
s
systemforindividualsandorganizations,whichcanalsoleadtoefficientmarketequilibrium.
However, one of the largest concerns of PI sharing is externality, indicating that others sharing
of their data may result in the benefit or cost on others, especially in the Information Age when
people are widely connected. A positive example is individuals epidemic disease data for Center
of Disease Control (CDC) will be extremely helpful to control terrifying diseases. In contrast, my
Instagramposttagcanexposemyfriendslocationorotherprivateinformationtothepublic,leading
to unexpected risk. Todelineate this phenomenon, we employ graph theory to build a network
modelandpredictsocialutilityunderdifferentcircumstances.
Theresultshowsthattotalsocialutilitywillbegreatlymiscalculatedifweignoretheexternalityand
this effectgrows biggerwithincreasingexternality(both positiveandnegative).Withtheinspira-
tionofeconomictheory,weintroducesPigovianTaxtoeraseexternality.Thesimulationrevealsthat
proper amountof taxation(or subsidy) on individuals or organizations will greatlyincrease social
utility.
1


## 第 3 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team83744 PIPricingSystemBasedonGameTheoryandGraphTheory
Basedonourmodelsandresults,weofferthefollowingvaluableandviablerecommendationsto
yourgovernmentandhopefortheadoption:
Governmentshouldnotconfineprivacyasakindofuntradeable(non-waiver)humanrightfromeconomic
perspectivewhichwillresultinlossinefficiency.
•
GovernmentcanprovidesuggestedoptimalpricefordifferenttypesPI.ForPIwithhighervalueforfirmsor
NGO,andPIwithhigherdisclosureriskforindividuals,thetransactionpriceshouldbothbehigher.Specific
e•xamplescanbefinancialtransactiondatageneratinggreatvalueforfirmsandprivateidentityinformation
withmuchriskofidentitytheftandmisuse.
Governmentshouldconductsupervisionandincreasethepunishmentforillegallydata-capturingbehavior
for organizations to a certaindegree to deter misbehavior, especiallyfor those information withlowbenefits
t•ofirmssuchasdepreciatedpersonalhistorydata.However,overexpenditureonsupervisionwillalsocause
inefficiencyforgovernment.
Consideringgenerationaldifference,inreality,theelderlymaybelesswillingtoacceptthepricesuggested
by government. But government should not address this issue if they believe that they accurately estimate
o•bjectiveriskandotherparameters.
Government should take quick actions in preventing another PI theft accident after massive data breach
becauseofincreasedleakagerisk,andthusthenegativeeffectcanbeerasedasmuchaspossible. Thetotalloss
i•nthisprocessdependsonthespeedofgovernmentreactionandtherequiredlevelofmanagement.
Alawshouldbeenactedbycountry,forcingdata-holderagenciestotakeresponsibilityandofferreimburse-
menttoindividualsformisuseorlossofdata. Themeasurewillcreateincentivefororganizationstocarefully
k•eepprivateinformationandincreasesocialwelfare.
Regarding the externality of PI, we strongly recommend government levy tax on data sharing behavior
withnegative externality(e.g. phone apps thatrequire friendsonline privacy)andprovide subsidyonthose
w•ithpositiveexternality(e.g.personaldiseasedata).Andtheamountoftaxationshouldbeinproportionto
theextentofexternality.
2


## 第 4 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team83744 PIPricing SystemBasedon Game Theory andGraph Theory
Contents
1 Introduction 1
1.1 Background.................................................................................................................................................1
1.2 Statementof the problem...........................................................................................................................1
2 Base model analysis 3
2.1 Assumptions................................................................................................................................................3
2.2 Notation of parameters...............................................................................................................................3
2.3 Modelling risk.............................................................................................................................................3
2.4 Costandbenefitanalysis of privacy........................................................................................................6
2.5 A game theory model for pricing private information...........................................................................8
2.6 Thetransferof pricing power...................................................................................................................9
3 Application ofour model 11
3.1 Privacyasa human right..................................................................................................................11
3.2 Timelinessof private information..........................................................................................................12
3.3 Generationaldifferencein PI system...............................................................................................13
3.4 MassivePI breach concern......................................................................................................................14
4 Extensiononnetworkeffect of PI 16
4.1 Modelling network effect.........................................................................................................................16
4.1.1 Generatinga scale-free network.................................................................................................16
4.1.2 Simulation process.......................................................................................................................17
4.1.3 Simulation results........................................................................................................................17
4.2 Corresponding policy suggestions..........................................................................................................17
5 Conclusion 19
5.1 Strengths and weaknesses........................................................................................................................19
5.1.1 Strengths.......................................................................................................................................19
5.1.2 Weaknesses....................................................................................................................................19
5.2 Conclusion..................................................................................................................................................19
A Appendix 23
A.1 Examplesofcalculatingtheamount of PI............................................................................................23
I


## 第 5 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team83744 PIPricing SystemBasedon Game Theory andGraph Theory
List of Figures
1 DecisionTree oftheBaselineGame Theory Model..............................................................................8
2 Supply And Demand Curve For PI As Commodities.........................................................................10
3 Willingness Versus Age............................................................................................................................14
4 BANetworkOf 10,000 Nodes................................................................................................................16
5 e=-0.05.......................................................................................................................................................18
6 e=0.01........................................................................................................................................................18
7 U vs e....................................................................................................................................................18
max
8 d vs e.......................................................................................................................................................18
m
II


## 第 6 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team83744 PIPricing SystemBasedon Game Theory andGraph Theory
1 Introduction
1.1 Background
The value of private information has always been in the center of discussion both academically and mun-
danely, especially in an era where information explodes exponentially and big data becomes popular.
Private information can bring profits to both individual and organizations who obtain private information.
But the use of private information to gain profit may bring harm to the information owner. Determining
the exact value of private information will facilitate policy making of government to balance privacy pro-
tectionand publicdata sharing.
With the development of information technology,personal information can be obtained more easily than
ever. Tonsofinformationconcerningpersonalpreferencesandtastesareautomaticallyexposedaftercon-
sumers shopping online. Individual information including phone number and home address have to be
providedinmyriadsofscenariosandmaybeleakedforadvertisinguse. Consideringthebenefitsofprivate
information, if no protection is provided, individuals will find it almost impossible to keep privacy and
maysufferfrom tele marketingharassment,property loss,and social embarrassment.
Private information, on the other hand, will bring benefits to individuals only if it’s known to others in
somecases. Marketersarebetterabletoservecustomersthroughcustomizationandpromotionifpersonal
dataareprovided[2]. Individualhealthprofilescanbeusedbyhospitaltocontrolthespreadofepidemics.
Thus, it’s inappropriate to rush to the conclusion that privacy must be kept only to the individual.
Scholarshaveexploredqualitativesolutionstotheconflictsofprivacyprotectionandinformationsharing.
Forexample, fair information practices (FIPs), are a set of standards governing the collection and use
ofpersonalinformation,incorporatingfivecoreprinciples:notice,choice,access,securityandenforcemen-
t[3]. However,lackinquantitativemodelsofprivateinformationvaluegreatlyharmstheefficacyofsuch
methods.Theambiguity makesithard toevaluatetheprocessofprotection and dissemination.
It’s rather interesting to compare private information (PI) with private personal property (PP), as well
aswith intellectual property(IP).An assumption inourmodel depicts anessentialsimilarityofthose three:
they are both tradable items on corresponding markets, where we can also put price tags on them. However,
compared to normal PP and IP, PI transaction is more like leasing instead of selling. Individuals still have
property to their private information but they cannot resell their PP or IP under common cases. As for
organizations, based on our assumptions, they cannot sell or give PI to other agencies even after they
lawfullyobtain it.
1.2 Statement ofthe problem
Problem F in ICM requires us to act as a policy analysis team and provide a pricing system of private
information. To begin with, we have to give private information a clear definition. Privacy has many
meanings under different circumstances, and some of them may even cause contradiction [4]. Referring to
thedefinitioninliterature,weintroduce thefollowing definition.
Private information is a kind of differentiation power related to an individual [5].
Private information is owned by individuals, which cannot be legally obtained by any other people
•
withoutpermissionortransaction [6].
•
We then adopt analytical hierarchy process to model the risk brought by PI leakage of people with dif-
ferent characteristics and specific information domain. Then, we set an economic scenario where private
information can be traded between individuals and organizations. By using the model of game theory, we
1


## 第 7 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team83744 PIPricing SystemBasedon Game Theory andGraph Theory
analyze the cost and benefits of government privacy protection and therefore give a pricing structure of
private information. By assigning the pricing power to different entities, we reach the equilibrium natu-
rally generating the appropriate price for individuals, organizations and the entire nation. Generational
difference, interaction influence and massive leakage are then explored through parametric manipulation.
Additionally, we extend our model to the social network level based on graph theory. Finally, we come up
withthememo ofpolicy recommendations.
The essay is structured as below. The following chapter introduces our model for risk and baseline game
theory model for pricing, with the cost-benefit analysis for privacy protection. Part three assigns pricing
power and introduces generational difference and studies the case of massive information leakage. Part
four presents a simulation on an undirected scale-free graph to provides suggestions for policy-making.
Partfive concludes.
2


## 第 8 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team83744 PIPricing SystemBasedon Game Theory andGraph Theory
2 Base model analysis
2.1 Assumptions
Asdiscussed above,wemakeseveralassumptionsinourmodel.Inlatterpartoftheessay,wemayrelax
some of these assumptions to deal with different issues.
There are three components of the society: Individuals, organizations and governments.
Individualsandorganizationsaremarketparticipants.Theyonlycareabouttheirown benefits.
•
Private information sold to organizations cannot be sold bythe organization to other entities.
•
Everyparticipantin thegame hasperfect information.
•
Government acts as a social planner whose aim is to maximize social utility.
•
Governmentsetsthepriceforprivate information.
•
Thetransactionof privateinformation takesthefollowingform: Organizationsdevisethebundleof
•
private information they wantto obtain, individuals then decide whether to sell given a price.
•
The first four assumptions are in accordance with the basic economic theories. The sixth assumption is
to assure that the value of private information rises when more information is included, discarding some
valuelesscombinationsof information.
2.2 Notation ofparameters
Westarttheanalysisby givingalistofparametersinvolved inthemodelasshown inTable1.
2.3 Modelling risk
In our model, r1 represents the risk of private information leakage. More specifically, being the major
disutility in privacy issues, it is the expected loss once your PI is disclosed by yourself and shared with
organizations. We want to categorize these risks to accurately model risk to account for different individ-
ual characteristics and specific domain of information. After reviewing related literatures, we divide r1
into three sub-risks, the risk of exposure to targeted marketing harass like sales call r11 [10], the risk of
property loss r12(including but not limit to telecom fraud, Internet fraud) and the risk of discrimination
r13(including but not limit to employment discrimination, insurance discrimination and sexual discrimina-
tion). Also, we treat total risk as the weighted summation of these three sub-risks. Different information
type in various domains have different weights here, as their likelihood in corresponding risks differs.
r1 = a (r)T, r =(r11,r12,r13); (1)
→− −→ −→
a is the weight vector. Obviously, sub-ris·ks here are influenced by numerous factors. To simplify the
−→modelandquantify theserisks,wejustconsiderthemost essentialindividualcharacteristics ineachsub-
risk.
Firstly, people with high time value suffers most from sales call since the time they spend on listening the
boring call is more valuable. According to traditional labor economics theory [11], on equilibrium, the time
value of leisure is equal to the amount of income. So r11equals the time length of sales call multiplied by
wage.Forexample,ifweassume time lengthofasalescallequalsto30seconds andsomeones daywage
equalsto200,then r =0.5(200 )=0.21.
11
8 3600
·
1Supposepeoplework8hours·perdayandthereare3600secondsperhour.
3


## 第 9 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team83744 PIPricing SystemBasedon Game Theory andGraph Theory
Parameter Description
P PriceofcommercializedPI
r1 Expectedlossfrom PI leakage
r Riskoftargetedmarketing harass
11
r Riskofpropertyloss
12
r Riskofdiscrimination
13
a Weightvectorofr1
−→r Vectorofriskcomponents
−→θ Socialrankofindividualwealth
IS Vectorofsensitivecharacteristics
−V→ ValueofindividualPItreatment
A−→ Reciprocalmatricesfordifferentdomainofinformation
i
b Valueofprivateinformationfororganizations
w Mutualbenefitsofdatadisclosure forindividuals
x Theamountofinformation
PI Basicprivateinformation
b
PI Profitableprivate information
p
n Numberofpiecesofbasicprivateinformation
C Completenessofbasicprivateinformation
p Probabilityof organization’ssuccessfulPItheft
s
r2 Lossoforganizations from theriskofunsuccessfultheft
N Thenumberofchanges happeninagiventime period
t Time
µ Subjectiveriskperceptionindex
r 1′ Subjectiveexpectedrisk
p Scoreofwillingness totakerisks
v Degree ofnodes
i
d Taxorsubsidyofferedbygovernmentoninformationdisclosure
e Externalityeffects
U Maximum ofsocialwelfare
max
Table1:ListofParametersand Notations
Secondly, telecom insurance price is a persuasive measure of how much people are willing to fully avoid
fraud risks. Based on the insurance products designed by Alipay and ZhongTong Company, the insurance
price is 9.9 CNY(1.57 USD). On the other hand, people who are less wealthy have fewer fraud risk since
they have less property to be defrauded. As a result, they are less willing to pay such a price. Weintroduce
discount parameter θ to indicate the wealth level: θ equals to the rank of his/her wealth in the society. So
r12=insurance price θ2.
As for discrimination risk, it varies from different PI and discrimination such as driving records for car
·
insurancediscrimination,medicalrecordsforhealthinsurance discrimination,politicalleaning andmar-
2Insurancepriceisdifferentforeveryindividual.Itisnotthefocusofourmodel,sowejustputithere
4


## 第 10 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team83744 PIPricing SystemBasedon Game Theory andGraph Theory
italstatus of female for employment discrimination and sexual minority for social discrimination. So we
think the key factor here is the occurrence of these sensitive information and peoples characteristics. For
example,politicalextremistswillsufferfrom employment discriminationwhile thosemoderateswillnot
face the risk when they share their political views. From these complex cases, we model r13 = IS V . IS
isavectordenotingaseriesofsensitivecharacteristicsandpeoplewithoneofthesecharacteri−s→tics→−wil−l→be
·
marked as 1, otherwise 0, in corresponding elements. V denotes the benefits of protecting characteristics
from companies. The value of V needs further resear−→ch and exploration. The setting here explains why
some political dissenters or sex−→ual minorities havehigher leakage risks and therefore avoidsharing their
PI.
Tounderstand how different domains of information will influence the risk, weneed to determine the weights
a of different sub-risk .Referring to Analytic Hierarchy Process (AHP) developed by Thomas L.Saaty in
→−the 1970s [12], we develop a method on estimating the weights in different domains. The main step in AHP
tries to estimate the weights of different criteria to the goal just based on the importance compar- ison
between each two criteria. The comparison result is stored in a reciprocal matrix and then calculate the
eigenvector. Similarly, we try to estimates the weights of different sub-risks to the total risk based on the
likelihood comparison. For example, If the likelihood of r11 is bigger than r12, then the first row, second
column element A(1, 2) will range from 1 to 9, where the bigger number indicates the bigger likelihood,
and correspondingly, the second row, first column element A(2, 1) will range from 1 to 1/9, which is the
reciprocal value of A(1, 2). Likewise, the same rule still holds if the likelihood of r12 is bigger than r11
when we have A(1, 2) < 1 and A(2, 1) > 1. The following matrices indicate a kind of reasonable likelihood
comparison under social media A , financial transaction A and health/medical records A , devised by us.
1 2 3
Basedonthesecomparisonmatrices,wederiveddifferentweightsofsub-riskinthethreedomains.
a1 = (0.45,0.1,0.45)
a→−2 =(0.57,0.34,0.08)
→−a3 =(0.20,0.31,0.49)
→−
5


## 第 11 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team83744 PIPricing SystemBasedon Game Theory andGraph Theory
Basically, the weights here are in accordance with our intuition. Forinstance, people tend to have more
worries about fraud in financial transaction domain than in social media domain and they also tend to
havemoreworriesaboutdiscrimination(byhealthinsurancecompany)inhealth/medicalrecordsdomain.
Weprovideanexampletoexplainourmodelmoreclearly.Imaginesomeonewhoreceives100dailywage
andranks50%ofhiswealthinthesocietywithnosensitivecharacteristics. Thenwecancalculateoutthe
6


## 第 12 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team83744 PIPricing SystemBasedon Game Theory andGraph Theory
risk r1 of his PI in financial transaction domain using (1) and a2.
−→
r1 =a2 (r)T
100
−→ →−
=(0.5·7, 0.34, 0.08) (0.5 ( ), 1.57 0.5, 0]
8 60
=0.326. · · · (2)
·
So the risk of privacy information being known by others is modelled accurately. Protecting privacy help
individual avoid the risk. Thus, it is reasonable to view the price point for protecting PI as the amount of
expectation loss from the risk, i.e., r1in this section. Forevery individual and every domain of information,
the price point can be calculated as (2). The related values depend on the property of the individual and
the information.
2.4 Cost and benefit analysis of privacy
In this section, we refer to the work of Acquisti A.(2010) [14], framing the analysis by presenting the
disclosure of PI and protecting PI as two sides of a coin, wherein protected PI may carry benefits and
costs which are, adversely, the opportunity cost and benefits of PI disclosure. For disclosed data, we refer
to states in which individuals knowingly and or unknowingly share PI with data holding organizations 3.
For protecting PI, we similarly refer to the situations above (data disclosure) have not taken place. While
Disclosure of PI can result in economic value for both organizations and individuals, this behavior may
also bring risk to individuals. So three key parameters are introduced to model the tradeoffs between costs
andbenefitsofkeepingPI private.
We use r1 to indicate the risk of data disclosure, or the value of keeping data privacy. Recently, many
economicsstudieshaveassumedthatprivacydemandsandprivacyvalueareexistingin,orhighlysensitive
to the indirect negative consequences of information transmission [13].The consequences include but not
limit to identity theft, price discrimination, stigma or other psychological costs [15]. The structure of r1
has been fully explored in the previous section.
Then, we use b to model the benefit of PI disclosure for organizations. As a kind of valuable resource in
informationage,privatedatapossessioncanleadtoincreasedrevenuesforcompaniesthroughconsumertargeting,
disease tracking for Center for Disease Control (CDC)and research output for universities. The most
prominent exampleof how consumer information canbe leveragedfor higher profit is online ad- vertising. E-
commerce and online advertising now amount to 300 billion per year in the US, providing employment to 3.1
million Americans [16]. Organizations also benefit indirectly from consumer data by selling it to other firms.
Simultaneously, PI disclosure may also benefit individuals, which we use w tostand for. By providing
data to companies or organizations, people might be able to install the App,
receivecorrespondingconveniences 4, have targetedoffers, personalizationanddataanalysisreport. Some
individualsmayevenreceivemonetarycompensationforrevealingherown personaldata.
Wethen explore the determinants of b and w. Apparently,innumerable factors will affect b and w in reality,
such as characteristics of individual, different organizations for different uses and types of PI. To simplify
the model and account for a consensus that a name with the persons picture attached is of higher value
3Forexample,company,NGOandresearchinstitution.
4Forinstance,FacebookConnectenablesseamlessauthenticationonthird-partyWebsites,reducingtheuserscostof
signingupacrossdifferentplatforms
7


## 第 13 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team83744 PIPricing SystemBasedon Game Theory andGraph Theory
than a name alone, we adopt one of the most essential factors, the amount of information, which we use x
todenote. We decidethatx isthesoledeterminantofb andw inourbasemodel5 andconsidertheexact effect.
Certainly,ThelargeramountofsharingPI,themorevaluableitwillbe forbothorganizationsandindividuals.For
example, advertising companies with more PI are able to target potential consumers more accurately. Likewise,
individual will receive bettertargeted offers and personalized product with sharing largeramount ofdata.So
it is apparent that both variables are positively related. However, the accurate relationship between b,w and x
depends greatly upon the purposes of organizations and services provided to individuals. So we do not
provide a detailed function of b(x) and w(x) here.
But we have to find a way to quantify the amount of personal information an individual provided so as
to compare their value. The value of a phone number alone seems to be smaller compared with the value
of a phone number with the persons recent photo attached. Initially we referred to Shannons information
theory [17], viewing each personal information as a random variable. However, as is pointed out by Daniel
Moody & Peter Walsh [18], information theory has not proved to be a useful method in practice except in
engineering, for it focuses purely on the amount of information transmitted and ignores the context of the
information. The information entropy of the phone number of a tycoon and that of a common person may
be the same, but the prior seems to have much greater value than the latter for luxury goods companies.
Here we divide personal information into two categories: basic personal information and profitable per-
sonalinformation.Basicpersonalinformation, denotedbyPI isdefined asthe information used toidentify,
b
contact and locate a single person, or to identify an individual in context. Specifically, it refers to
personal information an individual provided when applying for a US VISA 6. Considering the rapid de-
velopmentofonlineshoppingandsocialnetwork,weinclude IPaddress.Thereare15typeofPI intotal.
b
PI = fullname, photo, gender, marital status, date ofbirth,
b
{ place ofbirth, national identification number, social security number,
homeaddress,ZIP code,primary phone number,secondary phonenumber,
work phone number, email address, IP address
Profitable personal information, denoted by PI , is defined as inform}ation that are profitable when com-
p
bined with basic personal information, such as income, job, shopping preference, political leaning, health
condition and travel experience. Weassume that PI does not have any value without PI . This is easy
p b
to understand. For example, shopping preference of an individual is of little use for an advertiser when the
name or contact information are not provided. Now we can naturally define the amount of information as:
x =C ln(n+1), (3)
number of pieces of PI provided
b
C = · . (4)
15
Here we introduce n as the number of pieces of PI included, and select logarithmic function to measure
p
the profitability referring to the utility function widely used in microeconomics [19]. C measures the
completeness of basic personal information provided, referring to a method to measure the completeness
of pharmacological information in Wikipedia articles [20]. In this way, our definition above can be used
to compare the amount of personal information in a specific context. We have two examples devised in
5Furtherdiscussiononvaluesandamountofinformationwillbepresentedinsection3.2.
6Therearedifferenttypesofdefinition,differingslightly.
8


## 第 14 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team83744 PIPricing SystemBasedon Game Theory andGraph Theory
appendix for further discussion. Briefly, a name with a person’s photo attached is more valuable than a
name alone because it contains more information 7.
In this section, we perceive the benefit of keeping privacy as r1 in previous section. The tradeoffs are
the benefits brought to both sides through information sharing. With the definition of x, we successfully
quantify b and w for comparison. The price structure of PI should take both sides into consideration
because keeping them can lead to potential opportunity cost. All of these will be involved in our pricing
systeminnextsection.
2.5 A game theorymodel for pricing privateinformation
Suppose now that private information is commercialized and can be traded freely. We devise a game theory
model to characterize the appropriate price for each transaction. The transaction is a two-period game,
and information of the game is perfect for both sides. Given the price, individual chooses to sell or not to
sell their private information. In the second period, the organization will decide on whether to obtain the
private information through illegal channels, i.e., PI theft. If the organization chooses not to steal and the
individual decides to sell, then the transaction is executed at the price, or both sides will receive nothing.
In the model, we have analyzed r1, b and w in the previous sections. Given the bundle of information on
Figure1:DecisionTreeoftheBaselineGameTheory Model
sale, the three parameters are constants in the model. Wenow introduce r2and p
s
. p
s
is the probability
of organizations’stealing PI successfully,which is influenced bythe precautions of individuals. r2refers
tothelossoforganizationifstealingisunsuccessful. Specifically,hereweassignr2 asthepunishmentof
governmentif theft behaviors are exposed.The organizational cost of stealing is trivial in the setting.So
thebenefits ofPItheftistheexpectationofrewards,i.e.,p
s
b (1 p
s
) r2.
Wecalculate the sub-game perfect Nash equilibrium of the game. In the second period, the organization
· − − ·
will choose to steal if the expectation is larger than zero. This depends on the value of the information
bundle on sale, the probability of successful theft and the punishment. Toconsider the nontrivial part,
weassume that p
s
b (1 p
s
) r2 >0. This is reasonable since now government has not attached much
importancetopreventingPItheft. Thisassumptionwillberelaxedinlaterpolicyanalysis. Nowwereturn
· − − ·
7DetailedexplanationisintheappendixA.1.
8


## 第 15 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team83744 PIPricing SystemBasedon Game Theory andGraph Theory
tothefirstperiod.
The choice of the individual depends on P . If P is larger than (1 p
s
) r1 w, meaning that the price
individualreceivedcancompensateforthepossiblerisklosslesstheprofitfromsharingthedata,thenthe
− · −
individual will sell their PI at that price. And for the organization, P has to satisfy P < b so that the
organizationwillbe willingto participate inthis game.
As policy advisors, we first assume that the price is set by the government. What the government aims to
achieve is that once commercialized, individual and organization can successfully trade at the given price,
making both sides better off. Thus, we have to make (sell, not steal) the equilibrium. Such price will only
existonlyifthefollowingconditionstands:
(1 p
s
) (b + r2) (1 p
s
) r1 w;
Iftheaboveconditionisdisobeyed,th−ennop·ricewillb≥eapp−ropri·ate.−Lowpricewilldiscourageindividuals
tosell,whileahighpricewillmotivatetheorganizationtostealgivenapositivestealingexpectationprofit.
The equilibrium price can be any points in [(1 p
s
) r1 w,(1 p
s
) (b+r2)]. As a social planner, the
governmentshould then consider the equality of the distribution of the surplus in social welfarebetween
− · − − ·
the two sides. Wedraw lessons from the method by L.S. Shapley on equal distribution of the bonus [7]
and reach the conclusion that the bonus should be distributed equally to both sides. Thus, the pricing
system foragovernment is:
1
P = [(1 p
s
) b+(1+p
s
) r1]. (5)
2
subjectto: − · ·
(1 p
s
) (b+r2) (1 p
s
) r1 w, (6)
p
s−
b (
·
1 p
s
) r ≥2>0
−
;
· −
(7)
Tomakeitclear,thepricegivenbyth·eg−over−nmen·thasachievedtwogoals: leadingtoanefficientmarket
equilibrium where both participants are better off, and assure the equality in the distribution of trading
surplus. r1is the benefit of keeping privacy, modelled as risk in 2.3. b and w are value of information
discussedin2.4,makinguseofthepricingstructure. p isinfluencedbypersonalability,andgovernment
s
exerts great impact on both r2and p
s
. The five parameters are allrelated to properties of the information
sold,includingdistinctdomains andpersonalcharacteristics.
2.6 The transfer of pricing power
In this section we modify our model by assigning pricing power, i.e., the ability to set the price, to different
entities.Throughthealterationofthisability,we obtaindifferentpredictionsoftheprice.
First we consider a market with no market power and no government pricing. Recalled that in previous
section,price willbe apoint in [(1 p
s
) r1 w,(1 p
s
) (b+r2)]. However,now it’shard to detect the
actualpriceinsingletransaction,becauseithighlydependsonthenegotiationabilityofbothparticipants.
− · − − ·
Market fluctuation will affect the exact price of this perfectly competitive market. Weuse the forces of
supplyanddemandtodepictthissituation. Wesimplyconsiderinformationashomogeneouscommodities,
and there are numerous individuals and organizations in the market. The deduction of the supply and
demandcurvecomesfromthecostandbenefitanalysisqualitatively8. Fromtheperspectiveofindividuals,
8Hereweconsiderthesimplestformofsupplyanddemand.Theheterogeneityofinformationfordifferentpeopleand
different domain of information certainly will affect the discussion, but this can be explored similarly as the corresponding
9


## 第 16 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team83744 PIPricing SystemBasedon Game Theory andGraph Theory
the marginal cost equals the loss from the risk they are exposed to less the mutual benefits they obtain
from the data transaction. If more information is sold, the loss from the risk will grow larger since the risk
is increasing. The mutual benefit, existing in some certain kinds of information9, grows slower than the
loss, so the marginal cost will rise, in accordance with the traditional supplier marginal cost. The demand
curve of the organizations represent their willingness to pay. So the final price can be determined in the
supply and demand system in Figure 2.
Notethat inFigure2,thedemandcurvestarts from thepoint(0,(1 p
s
) (b +r2)),andthesupplycurve
− ·
Figure2:SupplyAnd DemandCurve ForPIAsCommodities
starts from the point (0,(1 p
s
) r1 w), corresponding to the equilibrium. Instead of focusing on the
price point, wedepict market fluctuation through comparative statics. Weconsider an exogenous impact
− · −
that increases the demand of the organizations at given price, which makes the demand curve shift right
andincreases the price.This can be quantitatively explained as the increase in b,and the intercept of the
demand curve gets larger10. Then if technology advances and PI theft is more likely to happen, the risk
gets bigger,increasing the supply curve’s intercept. In this way,the supply curve turns left,and the price
rises11.
Next we assume that individuals have control to sell of their PI, that is, they can determine the price
of their private information. In this scenario, the decision tree in our basic model remains, but a totally
different explanation is given. The goal individual wants to achieve is utility maximization. And the
largest possible payoff for him is P + w r1. And P cannot be larger than (1 p
s
) (b + r2). So the
best payoff for him is (1 p
s
) (b + r2) +
−
w r1. As a result, if (sell, not steal)
−
could
·
be an equilibrium,
individual will choose the price with the largest payoff, leaving the organization indifferent between buying
− · −
and stealing. However, if this price is smaller then (1 p
s
) r1 w, then the individual will decide to quit
thetransaction.Theresultisconcluded as below.
− · −
{
(1 p
s
) (b+r2) ,(1 p
s
) (b+r2) (1 p
s
) r1 w
P = (8)
0(Q
−
uit)
·
,(1
−
p
s
)
·
(b+r2)
≥
<(1
−
p
s
)
·
r1− w
− · − · −
economictheory. Theanalysisinourmodelistoshowthatforacertaintypeofprivateinformation, theforcesofsupply
anddemandcanstillbeappliedifPIiscommercialize.
9Notethatnotallinformationhasthisbenefit.Someinformationexposurewillnotbringaboutbenefits,asdiscussedin
section2.4.
10ThisisshowninFigure2.
11Herewegivetwo simpleexamplestoexplainthatthesupplyanddemandtheoryfitswellwithourgametheorymodel.
Other exogenous impacts can be decomposed into impacts on the parameters and predict the price accordingly.
10


## 第 17 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team83744 PIPricing SystemBasedon Game Theory andGraph Theory
3 Application of our model
3.1 Privacyas a human right
Should privacy be regarded as a basic human right? From our model, we find out that the answer to
the question varies according to the properties of certain type of private information. As described in
ourassumptions,wegivethisquestionanentirelyrationalandutilitymaximizationsolution,ignoringthe
potentialculturalorpolitical influence.
Wereviewedliteraturesonthedefinitionofbasichumanrights. Humanrightsaremoralprinciplesornorms
thatdescribecertainstandardsofhumanbehaviour,andareregularlyprotectedaslegalrightsinmunicipal
andinternationallaw[21]. Tomakemattersclearer,wegivemorespecificmeaningsofbasichumanrights
inourmodel,whichhastwolevels. Thefirstoneisthatprivateinformationshouldbecompletelyprotected
from market and cannot be sold. The second is that individuals have the rights to decide on whether to
sell their PI, and any efforts other than personal consent that entities take to obtain an individual’s PI
mustberegardedasillegal,andbepunishedseverely. Turningtoourmodelandrecallingtheequilibrium
result,wefound that an ideal market equilibrium willonly exist if(1 p
s
) (b+r2) (1 p
s
) r1 w. If
wedo notconsidergovernmentmonitoring and thecondition willturn − to (1 · p s ) b ≥ (1 − p s· ) r − 1 w.
Qualitatively,ifatypeofprivateinformationwillbringaboutmanylossestoindividualsonceleaked,and
− · ≥ − · −
the mutual benefits of information sharing is small 12, then most likely the market fails to generate an
ideal equilibrium, which may lead to another outcome of the game: evil capture of PI without consent.
As a result, government should ban the transaction of this level of information and keep it entirely to
the individuals, as in our first type of human rights definition. Now individuals are better off through
protection. And for information with a large b, a small r1 and a large w 13, the best choice is to let it be
traded freely.
Next,weconsiderthepolicyparameterinourmodel,i.e.,r2. Thebasicideaistoenhancer2soastosatisfy
the condition.Here weextend the discussion to apreviously made assumption,p
s
b (1 p
s
) r2> 0.
No PI theft will occur if r2 is high enough such that:
· − − ·
p
s
r2 > b; (9)
1 p
s
·
Asaresult,organizationshave noinclinationstosteal−inthesecondstage.Thus,theequilibrium price
changes14:
1
P= (b+ r1 w). (10)
2
−
subjectto:
b r1 w; (11)
≥ −
Itiscleartoseethatnow individualsbenefitmoresincetheorganizationshavenothreatsofillegally
obtainingPInow.Sopsb canbeviewedasanupperbound ofsupervisionforatypeofinformation,
whichdepends ontwoe
1
l−em
ps
ents.IfindividualshavetheabilitytoprotecttheirPI,whichmeansasmall
·
12Forexample,informationofpersonalbankaccount,orthepasswordofpersonalcomputer.
13Consumerpreferencesforcustomization,forinstance.
14Theequilibriumissolvedsimilarlyasinsection2.5.Governmentsetstheprice.
11


## 第 18 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team83744 PIPricing SystemBasedon Game Theory andGraph Theory
p , this will help the government reduce the cost of supervision. So here, for any type of information,
s
the government can simply set the supervision level to the upper bound, and by appealing to individuals
protecting their PI carefully, can successfully decrease the cost of supervision.
Combined with the discussion on the first meaning of human rights we defined, we find that it is more
appropriate for government to adopt the second method. Privacy should be considered as human rights,
and it can be also traded under the willingness of individuals. To sum up, the best protection strategy
ofgovernmentactsasbelow: If a type of information is highlyvaluedby buyers, which meansthe b is
large, then it is likely that the transaction will be executed smoothly, so the government does not need to
take many efforts on supervising. And if the information has a low perceived value b, then the government
should set its protection level generating an approximately ps b effect. This policy is optimal because
1
−
ps
individualsreceivebenefitsandhavecontroltotheirPI,organizationsobtainusefulPIin alegalway,and
·
thecostofgovernmentismuchlessthanotherforbiddenoroverallsupervisionpolicies.
3.2 Timeliness of private information
In this section we introduce a dynamic element to our model that incorporates the consideration into chang-
ing personal beliefs about the worth of their private information. Specifically, we consider the change of
the amount of information with time passing.
As is mentioned by Daniel Moody & Peter Walsh [22], information is perishable and its value depreciates
overtime. Weview this decline as a result of the gradual loss of x (the amount of information we defined
in section 2.4). For example, the phone number of an individual is personal information, but once the
individual uses a new number, the old number is of no importance and contains no value.Information
becomes invalid due to the changing nature of the world. The speed at which personal information loses
thevaluedependsonits type.
Forbasic personal information(PI ), weview the probability of change remains the same overtime. Let
b
N be a random variable representing the number of changes happens in time t and wedivide t intosmall
fragments∆t,sothere willbe N0 = t fragments. Letλ ∆t be theprobabilityof achange during time
∆t
∆t.Weassume that during∆t theprobability oftwochangesis0.Thatisto say anindividualis unlikely
·
to change his or her basic information frequently during a short time (the probability of changing ones
name twice in an hour is 0).We also assume that the changes are mutually independent. The probability
distributionandexpectation ofNcanbe calculatedas below15.
P (N = k)= C
N
k
0
(λ ∆t)k (1 λ ∆t)N0− k, (12)
E(N )=N0 λ ·∆t =λ· t;− · (13)
Thatistosaythenumberofchangesisproporti
·
ona
·
ltotime
·
. Hencethedeclineofxcanbemodeledas16:
x(t) = x0 λ t; (14)
Forprofitable personal information(PI ), weview the−cha·nge mainly as a result of the drifts of personal
p
interest. Forexample,thetransactiondataofLGcellphonetenyearsagoisoflittleusesincetheindivid-
ualmaylikeiPhonenow. Theexponentialfunctioniswidelyusedtomeasuredriftstograduallydiscount
15It’sabinomialdistribution.
16x0 istheinitialamountofinformation,λreflectsthedecayingrate.
12


## 第 19 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team83744 PIPricing SystemBasedon Game Theory andGraph Theory
thehistoryofpastbehaviour[23][24],basedonwhichwemodelthechange ofPI
p
17:
ln2·t
x(t) = x0 e−
h
(15)
Specific examples could be transaction data and socia·lmedia data. The former directly reflects shopping
preference while the latter can be analyzed to catch to mine customer sentiment in order to support mar-
keting and customer service activities [25]. Shopping preference and customer sentiment are considered
hereaspersonalinterests. Nowthatwehaveincorporatedthedynamicelementintherelationshipbetween
x and t,wecanreturn toourbasicmodeland analyzethepricewithtime passing.Recallthatin section
2.4 we define b and w as functions of x. P is a function of b and r1, so P is directly influenced by x, and
the existence of equilibrium is also affected by x.
Givena bundle of information, the amount of information x contained decreases year after year, and as
a result, b and w also decreases. The decrease of b has two impacts on the equilibrium. The equilibrium
pricegetslower 18, andthe condition 18intends to fail. On theotherhand, w alsodecreases, leading the
right side of condition 18 becomes larger. So the model predicts the dynamic change of the equilibrium as
describedbelow:
Thevalueofprivateinformationtendstodeclineastime passes,due tothedecayintheamountofinfor-
mation it contain. This leads to the market price of PI falls(linearly correlated with the decrease in value
of PI to buyers). Further, the market transaction will not be an equilibrium anymore. Government ought
tointerfereandprotecttheindividualsfromPI theft.
3.3 Generational difference in PI system
In this section we consider the variation of risk perception by age and how this would affect our pricing
system. Wedefine risk-to-benefit ratio of PI and data privacy as r1. Because the issue of how age difference
w
will influence risk perception is hotly discussed, we will mainly focus on the generation effect on r1instead
of the benefit w. So the risk-to-benefit ratio is only affected by the change of risk.
We emphasize the meaning of r1 here and provide further explanations. r1, the risk of data disclosure,
is the expected loss derived by objective, rational and detailed calculation. So we assume the value of r1
here is independent of peoples subjective perception. Todescribe the perception by various groups of indi-
viduals, we introduce an index, µ, to stand for the degree of subjective and psychological risk perception.
The total subjective risk value of individuals become r
1′
=µ r1.
The higher value of µ indicates the larger risk perception. When µ = 1, it indicates that the individual
·
canaccuratelyperceivetheexpectationlossofPIdisclosureandcorrespondingly,µ>1indicatesthatthe
individualovervaluesthe risk.
ThedatafromaresearchbasedonSOEPdatabasecanprovideuswithanusefulinsightoftherelationship
betweenriskperception[26]. Theresearchfocusesonriskattitudesandindividualcharacteristics,where
age is included. Clearly,people with higher willingness to take risk should havelowerperception of risk
andthosewithlowerwillingnesstotakeriskshouldhavehighermentalvalueofrisk. Wetakethemedian
willingnessscorepofeachagegroupfromSOEPandfittherelationshipbetweenthem,usingpolynomial
curvefitting.Thefittingcurve is:
17x0istheinitialamountofinformation,hreflectsthehalflifeofinformationdecay.
18Inaccordancewiththebasemodel,westillequipgovernmentwiththepricingpower
13


## 第 20 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team83744 PIPricing SystemBasedon Game Theory andGraph Theory
f(x)=2.738 10−7 x4+( 8.182) 10−5 x3+7.357 10−3 x2+ 0.2799 x+9.7. (16)
As is shown in Figure ·3, gene·rally, a−s people·age, t·hey are less·willing· to ta−ke risk an∗d therefore, possess
Figure3: WillingnessVersus Age
higherriskperception,µ.Toquantifyµ specifically,weendeavortoform abijection betweenwillingness
scorep andµ.Wedescribe ourassumptions andconstraintsconcerning thisrelationship:
Thelargervalueofp shouldcorrespondtothelowervalueofµ.Asismentionedabove,risk-loving
peoplewillhavelessperceivedlossofPI disclosure.
•
µ shouldbe strictlylargerthan0.Whenp isthemeanvalue,thecorresponding µ shouldbe 1sincewe
assumesthe average people canaccuratelymeasuretheobjective expectationof loss.
•
Accordingtoourassumption,weusethebijectionfrom p toµ as below.Thepoweritem indicateshow
muchstandard deviationexistsbetweenp andthemean value5.1.
p−5.1
µ= e− 1.1 (17)
Sowecanderivethat,forexample,someone aged 30willhavescore p = 5.94, and thus willhaveµ = 0.4678
andunderratetheexpected loss.
Now we discuss how the modelling of generational difference influence the game between individuals and
organizations in our base model. Forthose who age and have higher µ, only when either they have higher
w, mutual benefit from sharing PI, or higher price P in the market equilibrium, will they be willing to
have their PI sold. This is because the equilibrium price is determined by their actual risk r1, but their
ownperceptionisevenhigher.SoahigherP isrequired.
3.4 Massive PI breach concern
In this section, we apply our model to analyze massive data breach. We first discuss the kind of information
beingleaked,followedbyageneralanalysisinPImarket.
The immediate outcome of the breach is explicit. For the type of private information being exposed, the
value b for organizations decreases, and the probability of successful theft p rises because small flaws in
s
protectioncan lead to larger one. Moreover, we suppose that the information being exposed typically has
a small w. This is reasonable because individuals are willing to share PI with large w, and it is meaningless
14


## 第 21 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team83744 PIPricing SystemBasedon Game Theory andGraph Theory
to talk about massive breach. r1 will get larger because information of the same type is more likely to be
leakedanddoharm toindividuals.
Wereconsiderthetwoconditionsintheequilibrium insection2.519. Thefirstconditiontendstobe
disobeyed given r2 does not change accordingly. Thus, the market equilibrium is likely to fail and more
vicious thefts will occur. If the government does not do anything, then the second condition will also be
disobeyed. So this type of information will finally degrade into a point where no transactions and no thefts
happen.
Now we consider that the government will take actions by increasing r2. The change of the model will be
similar to that to section 3.1. With r2increasing, the first condition will be satisfied again, with the second
condition being dissatisfied quicker, reducing the incentive for theft. Thus, the transaction equilibrium
recovers with a different price. Since no more theft occurs, b will increase again and r1 will decrease.
Finally the corresponding parameter return to the original state, and government can go back to normal.
The implication from the model is obvious: government can take quick actions in preventing PI theft after
a massive data breach and the negative effect can be erased. The total loss in this process depends on the
speed of government reaction and the required level of management.
In reality, US court rulings have not awarded damages for breaches of PI up to 2009. The reason lies
on the plaintiffs’ inability to show actual damages - as required by negligence tort claims- or to show
a clear linkage of causation between the breach and the ensuing damage [27]. Moreover, data-keeping
organizations may hold the view that individuals should bear the risks, or expectation losses, of data
breach which are included in r1, when they carry out their decision of disclosure. However, according to
Acquisti [28], the setting will definitely lead to moral hazard of data holders: they have few incentives to
keep PI safety because they have not internalized such privacy costs in their utility function. So we think
a helpful law regarding PI should be enacted by country, forcing data-holder agencies’ responsibility and
reimbursement to individuals for misuse or loss of data.
Next we consider the effect of a massive data breach on the overall PI market. According to the research by
Romanosky and Acquisti [27], individuals availed themselves of the free credit protection and monitoring
tools after data breach of Choicepoint company. We regard it as steps of individual protection of data,
and thus the parameter p will decrease after massive data cascade and organizations which wish to obtain
s
private information illegally will face more difficulties in stealing or capturing without clear consent. So
p will fall in general. This will also change the outcome of our game theory model.
s
Asp falls,thecondition 19isdisobeyedandthereisnointentionofstealingPIduetothelowprobability.
s
Thefirstcondition 18willturnintob r1 w. Thesocialwelfarebecomesbettersinceitissurethattheft
will not happen. This can be explained as the positive externality brought by the massive data breach.
≥ −
Governmentandindividuals’senseofinformationprotectionwillriseandthecircumstancewillbebetter.
19
(1−ps)·(b+r2)≥(1−ps)·r1−w, (18)
ps·b−(1−ps)·r2>0; (19)
15


## 第 22 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team83744 PIPricing SystemBasedon Game Theory andGraph Theory
4 Extension on network effect of PI
Inprevious sectionswefocus ontheeffectofPIdisclosure onindividuals.Thateffect,including risksand
benefits,wouldbe greatlyreducedifindividualchooses tokeephisPIprotected.However,inreality,the
disclosureofothers privacymightaffectaPI-keepersincethedataofonepersoncanprovideinformation
aboutotherswhen theyaresocially,professionally,economically,ordemographicallyconnected[29].This
phenomenon, causingthecostorbenefitthataffectsapartywhodidnotchoose toincurthatcostor
benefit,isatypicalexampleofexternalityineconomics.Akindofclassicandusefulpolicytosolve
externalityproblem isPigovianTax/Subsidy:taxingonthose who producetheexternality.Basedonthe
theoryoftaxneutrality, itsindifferentbetweentaxingonindividualsanddata-demanded organizations.
Inthefollowingsectionweextendourmodeltotakenetworkeffectintoconsiderationandconsiderthe
effect of Pigovian Tax based on the simulation on an undirected scale-free graph 20.
4.1 Modelling networkeffect
4.1.1 Generatingascale-free network
Previousstudiessuggestthatsocialnetworksitesandotherhuman-formednetworksexhibitpropertiesof
scale-freenetworks[30].Henceweconductoursimulationsonanundirectedscale-freegraph,assumingthe
relationshipbetweenpeoplearebidirectional. WeuseBA(Barabsi-Albert)modeltorandomlygeneratea
scale-freenetwork,sinceBAmodelfollowstherulethatthemorenodesaparticularnodeconnectsto,the
morelikelythenodewillattractnewconnections[31],whichisagoodapproximationofsocialnetwork21.
In BA model, certain number of nodes are first randomly connected. The remaining unconnected nodes
are then added to the graph according to the principle that the probability of connecting to an existing
node is proportional to the degree of that node [31]. The graph with 10,000 nodes we generate via BA
modelisshown inFigure 4.
Figure4:BANetwork Of10,000Nodes
20AllcodingisimplementedonPython2.7andMatlabR2016b
21Forexample,attractivegirlenchantsmoreboys
16


## 第 23 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team83744 PIPricing SystemBasedon Game Theory andGraph Theory
4.1.2 Simulationprocess
Each node represents an individual who can decide whether to disclose his/her PI. The decision is made
accordingtothepayofffunction below:
Payoff =w (1 p ) r d. (20)
i s i
Herethe footnotei refers to the ithindividual and−varia−ble d·ref−ers to theidenticaltax bygovernment to
solveexternalityproblemresultingfromthedatadisclosure.w,r1andp
s
areasdefinedpreviously,varying
from person to person. The simulation is carried out for each individual to make decision on disclosing
his/her PI if and only if the payoffis positive. Tomodel the PI disclosure effect on the whole society,we
define the utility function of the whole society as following:
∑
U = [b+w (1 p )r +e v d]+ I d. (21)
i s i i
i I
∈ − − · − | |·
Herev isthedegreeoftheithnodeandvariableereflectstheithnodesdisclosureeffectonothersthrough
i
acertainedge. ecanbeeitherpositive(e.g. diseaseinformationforepidemiccontrol)ornegative(e.g. other
peoplesprivacyonmyFacebookpost). Weassumethatedgeisidenticalandthemagnitudeofexternality
depends solely on the degree. The set I is defined as the set of people choosing to disclose his/her PI in
thenetwork and I isthenumberof elementsinI. Benefitb isheld thesameforeverybody.
Asforparametersvaluein themodel,w and r arerandomlyinitialized followingauniform distribution
| | i i
on [0,1]. Other parameters in this simulation is setas: b =0.1, p =0.05. Regarding the heterogeneity of
s
information,wetest e from -0.2 to 0.2 with astep length of 0.01.Foreach e,wetest d from -1 to 1 with
asteplengthof0.01,calculatethecorrespondingU anddeterminethedvalueofthemaximumU,which
we name d that reflects the best taxation rate for government, given e.
m
4.1.3 Simulation results
Figure 5 shows a U d plot for e = 0.05 and Figure 6 shows a U d plot for e = 0.01. From the plot we
can clearly see the maximum d lies in the middle with given externality magnitude and the peak shifted
− − −
leftwardswhene grows.
U is plotted against e in Figure 7, showing a steady growth of U with increasing e. The figure
max max
shows the effect of externality on optimal social utility. It is interesting to find that government can do
little to obtain better social utility when externality is negative. When externality grows from negativeto
positive, the rising of social utility speeds up, meaning that the government can do more to improve the
overall welfare.
InFigure8d (besttaxationrate)increaseswhenedeclines,whichreallymakessenseinthatwhenthe
m
negative externality grows bigger, Pigovian Taxshould also be heavier to address it. In addition, when
something has lots of positive externality such as epidemic disease record registration, a negative tax,
which means subsidy,can be given to individuals to maximize social utility.
4.2Corresponding policy suggestions
According to the simulation results above, ignoring externality of PI will certainly misvalue the effect of
data disclosure. Also, market force itself fails to erase externality and government have the responsibility
17


## 第 24 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team83744 PIPricing SystemBasedon Game Theory andGraph Theory
Figure 5: e=-0.05 Figure 6: e=0.01
Figure 7: U vs e Figure8: d vs e
max m
to intervene by adopting Pigovian Tax, especially for those PI with strong externality. For PI with strong
negative externality, such as those applications requiring your friends privacy, government can levy tax
either on individuals or organizations; for PI with strong positive externality, such as diseases data for
CDC or other health research institutions, government can offer subsidy for either part.
A commonly asked question could be if it is the community’s responsibility to protect citizens’ PI to
reduce shared risks. According to our simulation, community needn’t take that responsibility because
government’s tax has already compensated most of the shared risks, which has been taken into consideration
inthepayofffunctionforevery individual.
18


## 第 25 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team83744 PIPricing SystemBasedon Game Theory andGraph Theory
5 Conclusion
5.1 Strengthsandweaknesses
5.1.1 Strengths
We use a traditional sequential game theory model to depict the market equilibrium. It is concise and
powerful. By adding several parameters to the base framework, we can apply the model to many realistic
•
settings.
Scientific methods are adopted in deciding the actual form of parameters. Wecombine AHP, graph
theory,psychologicaltheoryandfittingmethodswithoureconomicmodel,andachievesatisfactoryresult.
•
Weuse undirected scale-free network to creatively simulate the process of private information disclosure
and quantify the effects of externality. This is quite new in related fields.
•
We give direct and viable policy implications to government from comparative statics in our model,
whichareconvincing andscientific.
•
5.1.2 Weaknesses
Wedo not discussthe situation of imperfect information. In reality,the parameters are hard to be fully
obtainedby participants.
•
Wedo not check the robustness and the sensitivity of our model due to the lack in data in reality.
The forms of parameters are subjective. We only give a rough quantitative form of r1, b, etc., without
•
exploring the most suitable form. Future research could look into these parameters more carefully.
•
Our model only consider the transaction between one individual and one organization. More complex
game settings, like many individuals involved in a trade with one organization, can be explored further.
•
Wedo not consider the cost of protecting PI such as purchase of data protection software and time
spent on taking precautions, both of which will affect our equilibrium result.
•
Due to our assumption, individuals still possess the ownership of PI even after they reach a trade with
one agency. This means that they can trade with other organizations. But we do not consider the effect
•
of this due to shortage of time.
5.2 Conclusion
In this paper we devise a pricing system for commercialized PI based on game theory. We fully discuss
the potential costs and benefits of privacy and incorporate corresponding parameters in the payoff repre-
sentationofthe game.
By solving the equilibrium, we conclude that under certain circumstances, selling PI as commodities will
bring benefits to individuals and organizations with government setting the price. We then extend our
analysis by discussing the parameters. We find that government can set privacy as basic human rights.
PI can be sold if the individual agrees and government have an efficient way of supervision and regulation
throughthecontrolofone parameter.
Wealso take into account the timeliness of information and concludes that government should pay extra
attention to those information which are not sold for years because they are more likely to be stolen.
The generational difference of risk attitude suggests that as people grow older, they are more unwilling
to sell their PI. Then we use our model to explain massive data breach and find that by quick reactions,
governmentcanbring theequilibriumbackto normal.Andtheoverallawarenessof dataprotectionwill
19


## 第 26 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team83744 PIPricing SystemBasedon Game Theory andGraph Theory
be strengthened. Finally,weaccountfor the network effects of PI bygenerating ascale-free network and
simulatetheprocessofPIdisclosure. Theimplicationisthatgovernmentcandolittlewhenthedisclosure
has negative externality, but can greatly improve social welfare byencouraging disclosure with positive
externality.
Private information pricing will become a hotter topic in the future. With more data accumulated, it is
very likely that what we propose in this paper be verified by empirical evidence. Though some discus-
sionsareroughandincomplete,webelievethatourresultsprovidesomebeneficialpolicyimplicationsfor
reference.Ifpossible,wehopethat wecould digdeeperintothis field.
20


## 第 27 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team83744 PIPricing SystemBasedon Game Theory andGraph Theory
References
[1] LeeDJ,Ahn JH,BangY.Managingconsumerprivacyconcerns inpersonalization:a strategic
analysisofprivacyprotection[J].MisQuarterly,2011: 423-444.
[2] PhelpsJ,NowakG,FerrellE.Privacyconcerns andconsumerwillingness toprovidepersonalinfor-
mation[J]. Journal of Public Policy & Marketing, 2000, 19(1): 27-41.
[3] Rotenberg M.FairInformationPracticesandtheArchitectureofPrivacy(WhatLarryDoesn’tGet)[J].
Stan.Tech.L.Rev.,2001: 1.
[4] ShostackA,Syverson P.Whatpriceprivacy?[M].EconomicsofInformationSecurity.Springer,Boston,
MA,2004: 129-142.
[5] JentzschN,Preibusch S,HarasserA.Studyonmonetisingprivacy:Aneconomicmodelforpricing
personalinformation[J].ENISA,Feb,2012.
[6] Stevens G M. Data security breach notification laws[J]. 2012.
[7] ShapleyLS.Avalueforn-persongames[J].TheShapleyvalue, 1988:31-40.
[8] VarianHR.Economic aspectsofpersonalprivacy[M]//Internetpolicyandeconomics.Springer,
Boston,MA,2009: 101-109.
[9] Laudon K C. Markets and privacy[J]. Communications of the ACM, 1996, 39(9): 92-104.
[10] Hann IH,HuiKL,LeeTS,etal.Consumerprivacyand marketingavoidance[J].Unpublished
manuscript, Department of Information Systems, National University of Singapore, 2005.
[11] Cahuc P,Carcillo S, Zylberberg A. Labor economics[M]. MIT press, 2014.
[12] Saaty TL.Decisionmakingwiththeanalytichierarchyprocess[J].Internationaljournalof services
sciences,2008,1(1): 83-98.
[13] Wathieu L, Friedman A. An empirical approach to understanding privacy valuation[J]. 2007.
[14] Acquisti A. The economics of personal data and the economics of privacy[J]. 2010.
[15] StoneEF,StoneDL.Privacyinorganizations:Theoreticalissues,researchfindings,and protection
mechanisms[J]. Research in personnel and human resources management, 1990, 8(3): 349-411.
[16] Deighton,J.andJ.Quelch(2009).EconomicValueoftheAdvertising-SupportedInternetEcosystem.
IAB Report.
[17] Shannon,C.andWeaver,W.The Mathematical TheoryofCommunication,University of Illinois Press,
Urbana,Illinois, 1949.
[18] MoodyDL,WalshP.MeasuringtheValueOfInformation-AnAssetValuationApproach[C]//ECIS.
1999: 496-512.
[19] VarianHR.Microeconomics:amodern perspective[J].GezhiPress,TheJointPublishing Company,
PolityPress,Shanghai,2011,282: 1176.
21


## 第 28 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team83744 PIPricing SystemBasedon Game Theory andGraph Theory
[20] KraenbringJ,PenzaTM,GutmannJ,etal.Accuracyandcompleteness ofdruginformationin
Wikipedia:acomparisonwithstandard textbooks ofpharmacology[J].PloSone,2014,9(9): e106930.
[21] NickelJ.withassistance from ThomasPogge,MBE Smith,andLeifWenar(Dec13,2013)Stanford
EncyclopediaofPhilosophy[J].Human Rights.
[22] MoodyDL,WalshP.MeasuringtheValueOfInformation-AnAssetValuationApproach[C]//ECIS.
1999: 496-512.
[23] ZhengN,LiQ.Arecommendersystem basedontagand timeinformationforsocialtaggingsystems[J].
ExpertSystems withApplications,2011,38(4): 4575-4587.
[24] ChengY,QiuG,BuJ,etal.Modelbloggers’interestsbasedonforgettingmechanism[C]//Proceedings
of the 17thinternationalconferenceon WorldWide Web.ACM,2008: 1129-1130.
[25] Khan GF.Sevenlayersofsocialmediaanalytics:Mining businessinsightsfrom socialmediatext,
actions, networks, hyperlinks, apps, search engine, and location data[M]. CreateSpace, 2015.
[26] Dohmen TJ,FalkA,Huffman D,etal.Individualriskattitudes:New evidencefrom alarge,repre-
sentative,experimentally-validatedsurvey[J]. 2005.
[27] RomanoskyS,AcquistiA.Privacycostsandpersonaldataprotection:Economicand legalperspec-
tives[J].BerkeleyTechnologyLawJournal,2009,24(3): 1061-1101.
[28] Acquisti A. The economics of personal data and the economics of privacy[J]. 2010.
[29] Wathieu L, Friedman A. An empirical approach to understanding privacy valuation[J]. 2007.
[30] Ahn YY,Han S,Kwak H,etal.Analysis oftopologicalcharacteristics ofhuge online socialnetworking
services[C]//Proceedings of the 16th international conference on World Wide Web. ACM, 2007: 835-
844.
[31] BarabsiAL,AlbertR.Emergenceofscalinginrandomnetworks[J].science,1999,286(5439): 509-512.
22


## 第 29 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team83744 PIPricing SystemBasedon Game Theory andGraph Theory
A Appendix
A.1 Examples of calculating the amount of PI
ConsiderabundleofinformationofAlice22:
Information Contents Type
Name Alice PI
b
Gender Female PI
b
Phonenumber 123456 PI
b
Emailaddress Alice@yahoo.com PI
b
Politicalleaning Democrat PI
p
Livingcondition Inahouse PI
p
Annualincome $100,000 PI
p
Table2:PrivateInformationofAlice
HereC =4andn =3.X(A)=4 ln3=0.29.
15 15
ThenweconsiderabundleofinformationofBob:
·
Information Contents Type
Name Bob PI
b
Gender Male PI
b
Phonenumber 654321 PI
b
Annualincome $100,000 PI
p
Thesizeofthehouse 200m2 PI
p
Livingcondition In ahouse PI
p
Thesizeofthemortgage $500,000 PI
p
Bathroom number 2 PI
p
Bedroom number 5 PI
p
Has agarden Yes PI
p
Table3:PrivateInformationofBob
HereC =3andn =6.SoX(B)=3 ln7=0.39.
15 15
In this case Bob’s private information is more valuable than that of Alice for X(B) > X(A). This is
·
because Bob provides more valuable private information. The calculation of private information is done
similarly.
22Thecategoryofprivateinformationandthecalculationmethodarepresentedinsection2.4,referringequation4
23

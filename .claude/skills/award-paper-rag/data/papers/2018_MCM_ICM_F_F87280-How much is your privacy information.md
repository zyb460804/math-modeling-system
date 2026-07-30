# F87280-How much is your privacy information


## 第 1 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team Control Number
For office use only For office use only
87280
T1 F1
T2 F2
T3 F3
Problem Chosen
T4 F4
F
2018ICM
How much is your privacy information?
Summary Sheet
For ensuring thestabilityof thesociety, we establish asystem ofprivacy pricing.
Task1, according to the personal characteristics and information field, we choose 26
indexes to measure privacy price, and divide them into 5 categories according to the degree
ofcorrelation.
Task2, we price the privacy. The present value method is used to quantify the value of
privacy. We use the Analytic Hierarchy Process and Gradient Boosting Decision Tree,
throughthePythonlanguagetocalculatethecoefficientsoftheparameters.Thenweestablish
Gauss mixture model to evaluate the information related value. Finally, the simulation of500
people's privacy information is selected to verify thefeasibility of themodel.
Task3, we give the pricing method, introduce the demand elasticity coefficient, and
analyze that the privacy information is more flexible. Then the life cycle changes in a long
timerange are predicted.
Task4, with the development of the times, the risk factor will be changed. We add
dynamicfactors and use Matlab to fit thechange function of therisk coefficient.
Task5,thevalueofprivacywill increasewithage and thenstabilizeat acertain level. We
find out the relationship between PI, IP and PP in the privacy market through a number of
literaturesearches.
Task6, we use small world model and dynamic game theory to do simulation and
prediction, and find that the privacy of individuals and groups will be largely leaked with the
development of market.
Task7, the impact of data leakage is long tail. The agency can use the actuarial model to
calculatethetotal amount ofcompensation tothe individual.
Task8, we put forward somesuggestions to thegovernment onthebasis of themodel.
Finally, we perform asensitivitytest to verify thestabilityofthemodel.


## 第 2 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#87280 Page1of20
I Introduction
Withthedevelopment ofsocial informatization,thecommercialization ofprivacybecomes
an important issue. Therefore, we need to establish a privacy pricing system to maintain the
stableand healthy development of theinformation sales market. Ourtasks are asfollows:
Task 1: considering the level of risk can pass personal information and data fields
classifying model, considering the different characteristics of category information, find the
best balance of classification accuracy and simplicity.
Task 2: the question to think about the integrity of personal information, uniqueness,
scarcity, according to the value of different factors, finally comprehensive assessment of the
valueof personal information.
Task 3: consider the information value, risk value, and the impact of information integrity
onthefinal information pricing.
Task 4: consider the assumptions and constraints of the pricing model, judge the
relationship between information privacy and human rights, and adjust the model to make it
universal in thedynamic environment.
Task5: consider the influence of age factors on the risk-benefit ratio of the population,and
consider thesimilarities and differences between PIand PPandIP.
Task6: make sure each individual data sharing information leakage caused by the network
effect, and to consider whether the information network effect will affect the value of the
personal information system, and to have the same privacy risks related to personnel, thesale
oftheirpersonal information should berestricted.
Task 7: consider the impact of large-scale PI leakage on data vendors, acquirers, and
informationvaluesystems.Andconsiderwhethertheresponsibilityfordatadisclosureshould
beresponsible forinformationdisclosure.
Task 8: organizetheabove questions intoproposals.
II Categorize individuals into sub-groups (Task 1)
2.1 A brief introduction to personal privacy pricing
Personal privacy is a basic resource, if it is used reasonably, it will help to promote the
information social development. Culnan[1] find that, if private used by business are not
known to individuals, they will increase their concerns about privacy disclosure. Hagel and
others’ [2] research shows, some people tend to pay more attention to privacy, the reason is
that they want to get compensation for information leakage. Adjei[3]thinks that, people will
be willing to provide personal information to get paid if their personal profits outweigh the
risks.
Thus, it can be seen that, on the premise of the sound pricing system of personal privacy
most people are willing to obtain certain compensation or compensation through the sale of
personal privacy. So theappropriate pricing system should be set up.


## 第 3 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#87280 Page2of20
2.1.1Theestablishmentand evaluationof personalprivacy information archives
The classification of personal privacy information can help research and excavate the real
value contained in information, and the value of information can be further evaluated by
studying the correlation degree. Therefore, we chose 26 indicators based on the principle of
personalinformationclassificationandtheactualsituationofthissubject. Itincludespersonal
attributes, financial transactions, social networks, personal assets and health care. This paper
classifies personal privacy intotwo aspects: individualcharacteristics and informationfield.
Theindicators and theirclassification are shownin Figure 2-1.
Figure2-1:Classification
The reasons for the selection of personal privacy information in five aspects are analyzed
as follows:
 Citizenship:They belong tothe range ofattributeinformation and are objective
information that can beusedto identify specificindividuals.
 Social Contact: Because oftheuniquesocial attributes ofhuman beings, it has an
important research valuein thefield of information, which is generated inthe process of
lifewith theotherspider webinformation.
 Finance: Itreflects thesituationofindividual financial trade and has great value for
information mining.
 Health/Medical: It has certain significance to thestudyofsocial medical treat- ment
service system, and reflects the various situationsofthe individualbody.
 Personal Assets：It reflects thepersonal economicstatus, which is valuable forpublic
interest, such as national economic analysis, andcorporate profits, and it can create
economicbenefits.


## 第 4 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#87280 Page3of20
III Privacy Cost Model（Task2）
3.1 Brief Introduction
Thecost of privacy isacomprehensive pricing ofthe valueof privacy, and weconsider
three components.
The first is the expected value of income, and we divide five two - level parameters into
two categories.
Difficulttoquantify:Ascitizenship,weempowereachparameterbyanalytichierarchy
process[4].
Quantify: Theother16parameters can bequantified byusingthepresent valuemethod
of income in accounting. Then the coefficient of each parameter is calculated by themachine
learning method of theGradient Boosting DecisionTree(GBDT)[5].
Thesecond aspect is therisk valueof privacy. Because thevalueof risk isnot easy to
measure, we useprobability theory to estimatetheaverage deviation degree ofexpected
revenueand get theexpected risk reward[6].
Thethirdaspectis informationrelated value. Thecostofprivacydepends notonlyonthe
integrity of information, but also on the relevance. For example, the value of only the name
should be lower compared with the value of the name attached to the person. We set up a
Gauss mixed model to study the relationship between the correlation value and the relevant
valueofinformation[7].
3.2 Model Building
3.2.1Expected ValueofIncome
Theexpected value ofincome is ：
26
I 
C
j j
j1
Where：
I ：Expectedtotalincomevalue
：Thevaluecoefficientofthejth parameter, 
j j j
C ：Theexpectedreturnvalueofthejth parameter
j
Step1:Theempowerment ofcivil identityinformation byAHP
The related factors of citizenship quantification are decomposed into objectives,
guidelines, programs and so on. Based on this, qualitative and quantitative analysis is carried
out.The analytic hierarchy process is likeFigure3–1：


## 第 5 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#87280 Page4of20
Figure3–1:TheStructureofAHP
 Construct acomparison matrix
Byconsultingrelevantinformation and combiningwiththe realityoflife, weanalyze the
relationship and importance of 10 indicators in citizenship, and build pair wise comparison
matrix.
 Hierarchical singleorder
The elements of each column of the judgement matrix are normalized, and the general
terms oftheelements are:
n
A =A

A
ij ij ij
i,j=1
Using sumand product method are used tocalculate andadd the judgement matrix of
eachcolumn after thenormalization. TheW is obtained.
i
n

W = B
i ij
i,j=1
The element of the W is the sort weight value of the relative importance of the same
i
level factor to a certain factor of the upper level factor. For W (W,W ,...,W )T,In the
1 2 n
process ofnormalization,theapproximatesolutionof theeigenvector isobtained. Calculating
themaximumeigenvalue of thejudgmentmatrix 
max
n (AW)
  i
max nW
i1 i
After that, wecan makesure that therank ordering is consistent withthe consistency
check.Theso-called consistency check is theallowable range ofA.
 Pairwisecomparison matrix consistencytest
Theconsistency index ofthe pairwisecomparison matrix isConsistency Index (C.I.),
  n
CI  max
n1
To measure thesizeofCI, arandom consistency index RIisintroduced. Themethod is:
construct 500pairwise comparison matrices randomly, andget theconsistency index
CI  CI  ... CI
RI 1 2 500
500
Theratio ofthe consistency index CI. to thesame order mean random consistency index
R.I. is called therandom consistency ratioConsistency Ratio(CR)。
CI
CR 
RI


## 第 6 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#87280 Page5of20
TheCR<0.1 is obtained through thelevel analysis software, and theconsistencycheck is
passed.
 Determiningtheweightfactor
Theeigenvectors are obtained bycalculation,which is theweight of the10indexes.
 =W=(0.056,0.019,0.155,0.025,0.075,0.134,0.053,0.095,0.186,0.20)
j[1,10]
Step2：Earningspresent valuemethod quantifies other information
Privacy information seems to be difficult to quantify, but as long as the method is
appropriate, we can quantify it to a certain extent. We regard privacy information as an
intangible asset, a lot of international ways of quantifying intangible assets. Here we use the
present valuemethod[8].
The present value method of income is a kind of asset evaluation method to estimate the
value of the assets evaluated by estimating the future expected revenue of the assessed assets
and turning them into the present value. We determine the value of privacy information by
calculating the future revenue of the privacy value. For example, Table 3-1 shows that the
future earnings of businesses refer to the profits gained by merchants' knowledge of private
information, ortheexpenditure reduced bygovernment agencies and publicorganizations.
Table3–1:Informationvaluequantizationtable
Step3：GBDT calculation ofexpected valuecoefficient
Gradient Boosting Decision Tree isacombination algorithm for machine learning[9],By
iterating forward distribution algorithm, continuewith thenewweights, each roundof
iteration to get astrong learner and loss function, thenextiteration ofthegoal is tofind isa
weak learning regression treemodel, make thenextroundto minimizetheloss, itis to find a
decision tree, let sampleloss to becomesmaller. Thisis themost significant algorithm in
machinelearning at present. Figure 3- 2shows theprincipleofits calculation[10].
Thelast formula oftheabove steps is theinformation gain after thedivision ofthe
decisiontreeiscreated,andthebestsplittingpointisthepositionwiththehighestinformation
gain. In order to find themaximum gain positionofthefeature, we need totraverse all the
characteristics, find thehighest gain forevery feature, calculateall the features gain,the
specific process islikeFigure 3–3,and then usegreedy algorithm to repeat theprocess.


## 第 7 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#87280 Page6of20
Figure3–2:GBDTPrinciple
WeusePython toprogram according to theabove principles, then we can increase the
accuracy and findthemost appropriatecoefficient by adjusting thesteps, iterations, the
maximumdepth of decision tree, theminimumsamplesizeandso on.Finally, we can get the
expected value ofeachparameter value coefficient:
G
 j
j H 
j
3.2.4Venture Value
Step1. Thestandard deviationis calculated.
Generally, we can use standard deviation to measure the degree of general response risk,
but we have multidimensional index. In order to facilitate comparison with other parameters,
itis moreideal to usestandard deviation rate.


## 第 8 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#87280 Page7of20

Cof
E
Where
Cof：coefficient ofvariation, E ：expected value,：Standard deviation
Figure3–3:Informationgaintraversal
Step2. Determinethe riskfactor.
By theanalytichierarchy process described above, theweight ofeach parameter is
considered as a risk factor, indicating therisk ofprivacy exposure.
Theriskcoefficientisdeterminedbytheanalytichierarchyprocess.Afterintroducingthe
risk factor, we cancalculate theexpected rate ofreturn ontherisk ofprivacy:
26

R  rCof
j j
j1
Where
R ：The rate ofrisk reward forthe jth parameter
j
r ：The risk coefficient of the jth parameter
j
Step3.Calculating theamount oftherisk of privacy, that is thevalue oftherisk.
Where
K ：Valueofprivacy risk, jth parameter
I ：Expected return valueof the
j


## 第 9 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#87280 Page8of20
3.2.4Information related value
For the personal privacy information provided, the value of the data should be further
excavated. According to practical experience, the more sensitive information is, the more
sensitive rules can be mined, so the value of information is bigger,so we define "information
related value" to measure thedegree ofinformation correlation.
According to the study, the relationship between the two is "S" positive correlation, so the
Gauss mixed model is established[11], the Gauss probability density function is used to
quantify accurately.
The relationship between information related value and information correlation is consistent
withthe following Gauss function curve trend such as figure Figure3–4.
()2

D()ae 22
The  and  are the parameters, and the maximum likelihood method can be
used[12]toestimate theparameters
Figure3–4:Relationdiagramofinformationrelatedvalueandcorrelation
The MATLAB program is used to program the correlation value of the information
provided bytheindividual, and the information related value can becalculated. Personal data
providedthatthetwoperson,theexpectedvalueandriskreturnvalueisthesame,privacycost
pricing is not representative of the two men is the same, it is necessary to study the degree of
correlation according to specific content provided by the two data, estimate the value of the
relevant information, soas to calculate thefinal cost ofprivacypricing.
Theinformation related valueiscalculated onthebasis oftheexpected valueof income, and
theconcretesteps are as follows:
()2

D  ae 22
Where：
D ：Information related value, I ：Expected value ofincome,：Correlation


## 第 10 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#87280 Page9of20
3.2.4Totalvalueofthecost ofprivacy
Where：
3.3 Model solution
3.3.1 Data compilation
Based ontheparameters that are quantified, we have collected datafor 1997-2016 years
inChina's census and consumption.
Data source:National Bureau of Statistics ofChina（http://data.stats.gov.cn/）
3.3.2 Data processing
After asimplearrangement ofthedata, furtherprocessing of thedatais needed.
Data cleaning: checkwhether thedata is correct. The outliers are modified byfuzzy matching
tofill themissingvalues.
Data standardization:using theZ-score methodto standardize thedata, theresearch shows
that themethod has thehighest compatibility inmany criteriastandardization[13].
3.3.3 Calculationcoefficient
Through the above method, we get the risk coefficient, value coefficient and correlation
degree of each dimension through the analytic hierarchy process and GBDT by Python
programming. The specificvalues are Table 3–2.
3.3.4 Privacy cost pricing
Theexpected value ofearnings is based onthedataofChina's nearly five years (2011-
2016)and is further calculated bytheabovecoefficients.
Table3–2Valuecoefficientandriskfactor


## 第 11 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#87280 Page10of20
Table3-3Privacycostprice
l
1ofthemrepresentthisprivacyinformation,and0arenotprovided.
Then, we simulated thetransactionsof 500people's personal privacy data, such as Table 3
–3,and calculated theprivacy costpricing basedonthese data, and madea brief analysis.
We calculate each individual's expected return value, risk value and relative value, have
been found according to the total privacy, personal privacy information provided $600-3000
between thefloating in.
Ifapersonprovidesallhisprivacyinformationisall1,thenwecalculatethetotalprivacy
for$5578(per year).


## 第 12 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#87280 Page11of20
IV Pricing system & Supply and demand relationship （Task3）
When we sell personal privacy information as commodities, we are bound to be affected
by market fluctuations, including micro supply and demand, macro policy adjustment and
economicbalance.
4.1 Pricing system
Individuals can earn certain profits by selling their own privacy information. Businesses
orgovernmentagencieswanttopurchasetheseinformation,andtheywillpaypersonalmoney,
plus someprofits besides privacycosts.
B  CP  S
Where:
B ：Pricing ofprivacyinformation CP ：Thetotal price ofprivacy
S：Personal sale ofhiddenprofits
Accordingtothecurrentmarketprofits,inadditiontoluxuryaccessoriesandprofiteering,
theprofitmarginofacommodityisroughly10%-30%.Asaperson'sprivateseller,howmuch
profit can bemade forits own price, butthe profit margin can not exceed30%.
Theprofit margin
is
0.3

，we canget thefollowing:

4.2 Demand elasticity of privacy value
When privacy information becomes a commodityinthemarket, itwill receivethe
influence ofmarket fluctuations caused byvarious factors.This kind ofinfluence will cause
thechange ofdemand and price ofprivacy information. In order to respond to thedegree and
relationship ofchange,we introducethe concept ofdemand price elasticity in economics to
explainthedemand elasticity ofprivacy value[14].
Q B
E  
d B Q
Where：
E ：Elasticity coefficient of demand，Q：Quantity demanded，
d
B ：Pricing ofprivacy information
In general, the elasticcoefficient is negative, and in order to besimple, wesee it as apositive
number. It is also divided into fivecases of Table4-1.
Table4–1Elasticitycoefficientofdemand


## 第 13 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#87280 Page12of20
According to theconcept oflifecycle, we dividethemarket ofthis kindofinformation
intothree stages, as shown byFigure 4–1
Figure4–1LifeCycle
Development period: In this period, the relationship between the value of privacy and the
amount of demand is more flexible. When the price of privacy rises, most people will be
willingto sell, and when theprice falls, people willchoose tokeep theirprivacy.
Mature period: With the deepening of the concept of privacy information becoming a
commodity, institutions or organizations have fixed demand for privacy information, and the
coefficient ofelasticity willbe smaller, oreven afixedprice.
Decline period:When most ofthe people's privacy is sold for years, themarket forprivacy
information is closeto saturation, and there may be aprice - freephenomenon.
V Assumptions and Dynamic improvement（Task 4）
5.1Assumptions and constraints of personal information pricingmodel
1. It is assumed that people with the same conditions have the same willingness to protect
privacy. In the real world, due to the particularity of each person, the degree of importance
attached to personal information is different. Its distribution is roughly normal distribution.
We assume that each person's attention to their personal information is only related to the
individualcharacteristics and information related fields.
2. We don't consider the personal information of people in a special field. Special areas
includepolitical areas, military areas, and soon.Insomespecial areas, thedisclosure of


## 第 14 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#87280 Page13of20
personal information willresult in greater consequences and can’t bequantified according to
general standards.
3. We only consider the data of model system above. In order to quantify the value of
personal data, we only select the characteristic factors that have a great impact on the value
of personal information and evaluate the value of personal information according to the
characteristicfactors.
5.2 Whether information privacy should be regarded as humanrights
In ourview, information privacy should notbe protected fullyas human rights.
On the one hand, a part of personal information is closely related to the dignity of the
person and reflects the personality factors of the individual. From the phenomenon of the
commercialization of personal information, we can find that personal information reflects
both personality and property interests[15].Therefore, it is reasonable to protect the property
right.
Tosum up, we think that the personal information should be divided into two aspects,that
is, the personality elements of personal information and the property elements of personal
information. In the collection and utilization of personal information, we should pay
attention to the desensitization of personal information and make use of the information data
withoutdamaging thelegitimate rights and interests oftheinformationowners.
5.3 Dynamic analysis of cost of privacy
5.3.1Thechangeofpersonal values withtime
With the development of time, the spread of privacy protection ideas is expanding. People
are increasingly familiar with the consequences of privacy disclosure and pay more attention
to privacy. Therefore, people's expectations for the return of privacy are getting higher and
higher. According to the analysis of the privacy cost model, the risk value is changed due to
thechange ofpeople's thought.
5.3.2Thedynamicanalysisofthemodel
With the change of time，he value of risk increases gradually, we add dynamic factors on
the basis of the original model. The risk factors of 26 indicators ( r ) are changed from
j
constants to functions ,which are changing bytime(t ).
Taking thetotal asset as an example, itstrend ofchange is shownin Figure 5-1.
The data is fitted by the MATLAB fitting toolbox. Weget a higher fitting degree R-square,
which is 0.9779. The fitting effect is very good. So, the function relationship between the
risk coefficient (r )and thetime(t)ofthe18th indexes is as follows:
18
r  0.6404e(0.07066t0.6887)
18
By fitting the risk coefficients of the other 25 indexes in the same way, we can calculate the
function relation of the risk coefficients of each index. Combined with the formula of risk
value:


## 第 15 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#87280 Page14of20
We will add the functional relationship between the dynamic factors ( r )and the time ( t )
j
into the upper formula, then it can calculate the change of risk value over time to realize the
dynamicevaluation ofthemodel.
Figure5-1:Thechangetrendoftotalassets
VI Generational differences and conceptual comparisons（Task5）
6.1 Generational Differences
Withthe different ideas of the times and the growth of age, there are more or less differences
in the cognition of the risk and income of privacy information. In this regard, we collect
relevant data, and doan analysis.
Data sources:
(1) Data report onChina's Internet consumption ecology in 2015- 2017.
http://doc.mbalib.com/view/e720ad8eb4ebac9f83d56ec790a6dd1c.html
(2) Census ofChina's national bureauof statistics.
http://www.stats.gov.cn/tjsj/pcsj/
(3) Chinesedata Yearbook
http://data.stats.gov.cn/easyquery.htm?cn=C01
Weget theconsumption data ofall ages in personal assets, social networking, financial
transactions,health care, and then analyze and regress to get Figure 6-1,from 19to 63years
old,theaverage growth ofpeople's activitiesand consumptionexpenditureand 19years old.
According to theanalysis ofthe second problem, consumption expenditurecan be
regarded as expected value, so ourmodel needs tomake somechanges.
If pertinence is stronger, or we want to accurately calculate the value of privacy information,
we can increase the value of each kind of privacy value according to the growth of every
dimension.


## 第 16 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#87280 Page15of20
If only for theoverall calculation, and withoutcareful consideration of theincreasein the
situation,theaverage growth value can beused.
Figure6–1GenerationalDifferencesofconsumptionlevel
6.2 Compare with PI，PP andIP
·Private information[16] ： Non - public information ,Commercialization is not entirely
beneficial to individuals, and the sale of personal information will bring a series of
immeasurable risks, which may beinvisibleandlong-term.
 PP：Personal property is divided intotangibleand intangible assets[17].
Thesale ofPPbychanging thecommodity itselftoa certain valueis not determined bythe
relationship with theowner.
 IP：Rights generated bycreative activities based onintelligence[18].
Thesale ofIP willnot cause therisk of disclosureofprivacy information.
Theconceptual relationships ofPI, PP,and IP are shown in Figure 6- 2.
Figure6–2TheconceptualrelationshipsofPI,PP,andIP
VII Network effects of data sharing（Task 6）
We use Matlab to build a small world model for information leakage, and find that
individuals who do not sell privacy are increasingly implicated with the development of
privacy trading market. Then through the dynamic game theory, it is predicted that the
information of the group will be leaked seriously because of the individual behavior, and if it
is properly constrained, theinterests ofthegroup can bemaximized.


## 第 17 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#87280 Page16of20
7.1 The analysis and hypothesis of the problem.
1.Usingthe"economicman"hypothesisineconomics,itisassumedthatalltheresidentsin
thecommunity are economic man, that is,each stepshould only consider theirown interests.
2.Using amodified small-world model to simulategroup information leaks,members who
selltheinformationleakpersonalinformationaboutmembersofhisorherneighborhoodand
p
have a chanceto reveal information about othermembers.
3.Assumingthat any member's saleof personal information is immediatelyknown toother
members, this isa reasonable assumptioninsmallgroups.
4.Supposeeach member has thesame impact oninformationdisclosure.
5.Supposethat theinformation breakers leak information to themselves and to the
associated members have thesame impact.
6. Information disclosure does not consider human rights constraints.
7.2 Model
7.2.1Asmall worldmodel ofpersonal privacydisclosure.
Establishasmallworldmodeltodescribethedegreeofprivacydisclosureinagroup,Inthe
model, the proportion of people willing to sell personal information for profit is n ，The
proportion of people who are unwilling to sell personal information in return for benefits is
1n，individualswhoselltheirprivacywilllosetheprivacyoftwo adjacentindividualsinthe
model, the probability of having n causes loss of privacy of non-adjacent individuals. Use
Matlab software tosimulate.
Figure7–1:Simulationofsmallworldmodel.


## 第 18 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#87280 Page17of20
Assuming that the group has a population of 40, adjust the range of n and p ,and simulate
thelossof privacy.
The individuals who are connected by the attachment are individuals who are at risk of
privacy disclosure. According to the Matlab simulation analysis, it is obvious that with the
increasing of the parameters P and N, the privacy disclosure in the group becomes more and
moreserious.
7.2.2Analysisofprisoner's dilemma based on dynamicgametheory.
In a group, some people are willing to sell their own privacy, others think that privacy is
more important, we assume that the sale of privacy is an open, in groups, there are four
kinds ofcondition.
Table7-1Thegameofinterestwithinthegroup
According to "economic man" hypothesis, each group member only consider their
interests and action, is willing to sell a member of the privacy will sell their privacy, under
this precondition, even if other members do not want to sell privacy, their privacy will be
violated, as a result, even if part of the members are reluctant to sell privacy for interests, in
seeking tostop thecases, willsell the privacy in order to get morebenefits.
Based on the above simulation analysis, we get the conclusion. In the outside world
without intervention, a group with the same privacy risks into sub-game refining Nash
equilibrium, cannot get benefit optimization, in order to jump out of the prisoner's dilemma,
to maximize the interests of groups and groups to limit the privacy of personal selling
behavior isnecessary.
VIII Impact of data disclosure on the value of privacy(Task 7)
When information security issues arise in the organizations that purchase personal
privacy information, there will be a large amount of privacy information leakage. If the
privacy isstolen bycriminals, it can poseathreat to personal safety and social stability.
8.1 The impact of data leakage on the value of privacy
Wediscussthe impact ofdata leakage based onthecomponents ofprivacy value.
1. When a large number of data is leaked, personal privacy information is improperly
distributed in the market, then the bussiniess’ willingness to purchase personal information
willbe reduced, and the expected return valueof theindividual willalsodecline.
2.Because of people's awareness of the risk of personal information leakage is increased,
and theirwillingness to sell information willdecline.
3.Therelevant value willdecrease withthedecrease of expected returnvalue.


## 第 19 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#87280 Page18of20
In general, as Figure 8-1 shows, data leakage can cause the decline of personal privacy
value, and the willingness of people to sell their privacy value will also decline, which will
lead to theeconomic crisis of privacy trading market.
Figure8–1：Theimpactofdataleakageonthevalueofprivacy
8.2 Time effect of data leakage
As time goes on, the impact of data leaks can change, too. We consider the influence of two
trends, one is the long tail effect [19], the other is the bullwhip effect[20]. As shown in
Figure 8-2.
Figure8–2:LongTailandBullwhipEffect
 Long tail effect：If the public opinion of the leak is guided by the demand side of
personal information, such as intermediary companies and government agencies, then
there willbe along taileffect.
 Bullwhip effect：If the message of the leaked data is spread rapidly across the network,
the overall public opinion is not controlled by any organization, then there will be the
bullwhipeffect.
Figure8–3:Theimpactofdataleakagechangesovertime


## 第 20 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#87280 Page19of20
Although these two cases will appear, the bullwhip effect can be controlled by the
other.With impact events increasing, effects of data leakage has become smaller. Therefore,
the overall impact of data leakage, such as Figure 8-3. It will rise first, then drop, and there
willbe fluctuations in it.
8.3Agency compensation model
When the data leakage occurs, the agency needs to compensate everyone for a certain loss.
In addition to the value of the data itself, the agency also needs to compensate for other
losses caused by data lost. We use the actuarial model of the insurance[21] industry to
calculate the amount of compensation. The establishment method of actuarial model is
generally parametric modeling, and its process isshown inFigure8-4.
Figure8–4:Flowchartofparameterconstructionofactuarialmodel
Finally, theamount of compensation wehave calculated isas follows:
U  I  
Where：
U:The amount ofthefinal compensation tothe individual
I :The valueof theinformation itself,and it is also theoriginal expected value.
：Other losses should becompensated for bytheactuarial model.
IX Sensitivity analysis
In order to test the stability of the model, we consider that different people pay different
attention to personal privacy information and have different attitudes and tolerance to risk
disclosure. Therefore, the weight assignment of value coefficient and risk coefficient is
different from person to person. In order to test the universality of the coefficients
determined by the gradient lifting tree and the analytic hierarchy process, we have designed
a questionnaire on personal privacy information attitude (see Appendix II). In this paper, 50
people of different ages were selected as the respondents, we investigated their weighting of
26 indicators and obtained new value coefficients and risk factors. Through the analysis of
the data, 3 groups of invalid data were excluded, and 47 new value coefficients and risk
factors were obtained. We put these coefficients into the model and repriced the privacy
costs of the 500 people generated by the simulation. The new pricing situation is shown in
Figure 9-1.(Because ofthelarge amount ofdata, only partial dataisdisplayed.)


## 第 21 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#87280 Page20of20
Figure9-1:Localdiagramofnew pricingresults
The average value of the new pricing (Average) is not significantly different from the
original model (Original). Weuse SPSS software to carry out the independent-samples T-test
onthesetwo sets of data, and get thetestresults such as Figure 9-2.
Figure9-2:Theresultofindependent-samplesT-test
Itcanbeseenfromthetestresultsthat, in the test of homogeneityof variance, p=0.775>0.05,
we can accept the original hypothesis, it can be considered that the variance is equal, the
independent-samples T-testshould beused.
The results of independent-samples T-testshows, p=0.910<0.05, we can’t accept the original
hypothesis. Therefore, there is no significant difference between the above two sets of data,
so thestabilityofthe modelis good.
X Analysis of the advantages and weaknesses of the model
 Advantages：
1. Weconsider many basicand derived parameters and establish a personal information
pricing model that reflects theimpact ofallaspects.
2. Theimpact of theemergency pricingmodel isconsidered.
3. Model is asimplebut flexibleand reliable. When a certain factor changes greatly,the
model canbe universally adjusted bysimpleadjustment.
4. The method used in thepricing model is novel, R-squared is high, and theerror rate is
small.
 Weaknesses:
1. Someparameters need tobeadjusted according tothe actual situation.
2. Itis impossiblefor all peoplecan accept thecommercialization ofprivacy.
3.Theareas involvedare notexhaustive.


## 第 22 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Privacy Pricing Policy Recommendations
Dear decision maker:
In the information society, the analysis and processing of information has brought
great social and economic value. Information becomes moreand moreimportant.
At present, the personal information of citizens has been circulated in the market, but
personal information is an important part of information cluster. The laws, policies
and pricing strategies related to the commercialization of personal information still
exist in a large gap in related fields, resulting in huge risks. In order to standardize the
market order of information, reduce the risk of citizen information leakage brought by
information commercialization. Through the comprehensive consideration of various
factors, we have set up a pricing system for the commercialization of personal
information.
Our team considers the value of information from both the information owner and the
information user. We obtain cost measurement through information, assess the risk
and value of information sharing, and predict the value of information. Furthermore,
we consider the influence of dynamic factors and sudden events on information value
and establish theinformation commercializationpricingsystem.
Privacy information pricing
Weconsiderthe followingfactors toprice themodel.
prospective earnings ： Consider privacy as an intangible asset, quantifying the
value of personal information through the quantitative method of intangible assets. It
can also be understood that when individuals sell their privacy as a commodity, they
can makea bigprofit fortheirprivacy buyers.
Risk assessment value：Whenpeople sell their privacy, the privacy they sell brings
certain risks. As compensation, the information buyer should compensate the seller
for risk. Because each person's information and information value is different, the risk
valueisdifferent.
Relevance value：In fact, the privacy value of the system is often higher than that
of individual privacy prices. Other things being equal,if privacy is a system, the value
ofprivacy is higher.
Other factors：Inaddition to the above three factors, we also consider other factors
todynamically compensate themodel.
Generational differences：Agedifferences lead to different ideas. This leads to
greatercognitive differences inthe valueofprivacy.
 Age difference ： The younger age differences can also be reflected in the
concept, and the information value of the individual will change as the age changes.
Individuals' perceptions ofrisk and benefits also change withage.
 Unpredictable risk：Some risks are latent and cannot be predicted in today's


## 第 23 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
circumstances.
Effect of pricing
Applicablefields：Wemake pricing proposals forPIin three areas
socialmedia
financialtransactions
health/medical records
Model effect：
According to the online survey and simulation, the same crowd divided on the
value of information cognition has a little different, but the overall value of the float is
less than $10,thepricing model of basiccan meet theexpected valueofpeople.
And more than 50% of people are willing to sell their privacy information at this
price, but only if the information can be reasonably used, and it will not pose a threat
topersonal safety.
National macro-control
In order to avoid unexpected privacy information market conditions, lead to data
leakage or other social instability happens, the government must want to undertake
certain macroeconomic regulation and control, limit privacy price within a certain
range.
 Promulgates thelaws andregulations ofeconomic regulation and
regulation:establish a perfect system to adapt tothedevelopment ofmarket economy,
and calm the relationship between supplyand demand.
 Disciplinary punishment forillegalbehaviors:avoid usingotherpeople's
privacy information forillegal activities.
 Restricted trading of special information: information of certain special
groups, such as government personnel, should be restricted according to
circumstances.
Accident prevention
If something unexpected happens, for example, a large amount of privacy is leaking,
weneed todevelop acompletesolution.
 Agency compensation: onthebasis ofpersonal information value, make
certain increment compensation.
Guide public opinion: the government and media guide public opinion without
infringing on individual rights and interests, and prevent riots or panic, causing social
instability.
 Control themarket:try toavoid leaking datainto themarket to prevent
economicrecession orimbalance.
 Deal with itas soon as possible: timely and properly handle theunexpected
situation.
Sincerely
Team 87280


## 第 24 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
References:
[1] Culnan M J.’How didthey get my name’:an exploratory investigation ofconsumer
attitudes toward secondary information use[J].MISQuarterly,1993,17(3):341-363.
[2] Hagel J III,Rayport J F.Thecoming battlefor customerinformation[J]. Harvard Business
Review,1997,75(1):53-65
[3] Adjei J K． Monetizationof personal identity information: technological and regulatory
framework[C].India: International Conference onInformation Science&Security,2015
[4] Al-Harbi AS. Application ofthe AHP inproject management[J].International Journalof
Project Management, 2001,19(1):19-27.
[5] Dai yixin, sun rongling. Realizationand quantification ofintangible asset value[J].
Chinesesoftscience,2000(07):74-77.
[6] Zhu guo. Application of EXCEL in financial management -- calculationof investment
risk value[J]. Journal of chifeng college (natural edition), 2009,25(4):130-131.
[7] SunGuangling, TangXianglong. Hierarchical semi supervised learning algorithm based
onGauss mixturemodel [J]. Computerresearch anddevelopment,2004(01):159-164.
[8] LiHongxun.Asset evaluation andmanagement: ChinaForestry Publishing House,2000
[9] FriedmanJH.StochasticGradientBoosting[J].ComputationalStatistics&DataAnalysis,
2002,38(4):367-378.
[10] Introduction to Boosted Trees, Tianqi Chen,2014
From http://homes.cs.washington.edu/~tqchen/pdf/BoostedTree.pdf]
[11] SunGuangling,TangXianglong.Researchanddevelopmentofsemisupervisedlearning
algorithm [J].layered computer based onGauss mixturemodel,2004(01):159-164
[12] Zhang Rongquan, Du Yuming, Yang Jianyu. A LFM signal maximum likelihood
estimation model and a fast algorithm for parameter estimation [J]. Journal of radio wave
science,2005 Journal of radio wave science (05):101-105.
[13] Xu Yunhui,Li Zhongfei. Dynamic portfolio selection based on income sequence related
dynamicmeanvariancemodel[J].Theoryandpracticeofsystemengineering, 2008(08): 125-
[14]Diego S.Price elasticity ofdemand[J].Betascript Publishing, 2009,3(4):1717-1718.
[15] PengYun.Research on property property of personal information from theangle of
Anglo American Property Law.Legal system and society:ten-day periodical, 2011(11):249
[16] A. Beimel and Y.Stahl,Robust information-theoretic privateinformation retrieval, in
Proceedings ofthe3rd International Conference onSecurity in Communication Networks
(SCN'02), pp.326–341,2003.Citeis from DGH2012,op.cit.
[17] Personal property". SirRobert Harry Inglis Palgrave. Dictionary of political economy,
Volume3.1908.p.96
[18] Personal property". Sir Robert Harry Inglis Palgrave. Dictionary of political economy,
Volume3.1908.p.96
[19] TangHaijun. Theory of longtail theory of economics[J]. Modern management science.
2009(1):62-64.
[20] TangHaijun. Theory of longtail theory of economics[J]. Modern management science.
2009(1):62-64.
[21] Xiao Yan.Actuarial model [M]. RenminUniversity of Chinapress,2013.


## 第 25 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Appendix I
Python
#####################################GBDT################################
import numpy as np
from sklearn.ensemble import GradientBoostingRegressor
gbdt=GradientBoostingRegressor(loss='ls', learning_rate=0.1,
n_estimators=100,
subsample=1, min_samples_split=2, min_samples_leaf=1, max_depth=3
, init=None, random_state=None, max_features=None, alpha=0.9, verbose=0,
max_leaf_nodes=None, warm_start=False
)
train_feat=np.genfromtxt("f_train.txt",dtype=np.float32)
train_id=np.genfromtxt("f.txt",dtype=np.float32)
test_feat=np.genfromtxt("f_test.txt",dtype=np.float32)
test_id=np.genfromtxt("ff.txt",dtype=np.float32)
gbdt.fit(train_feat,train_id)
pred=gbdt.predict(test_feat)
print(gbdt.feature_importances_)
total_err=0
for i in range(test_feat.shape[0]):
print(pred[i],test_id[i])
err=(pred[i]-test_id[i])/test_id[i]
total_err+=err*err
print(total_err/pred.shape[0])
##Result##
'''
====================== RESTART: F:\math\gbdt\usegbdt.py
======================
[0.05769512 0.00610115 0.05629678 0.01203783 0.02682956 0.08157958
0.03342411 0.09468546 0.03692312 0.05884569 0.03874673 0.06441484
0.05666908 0.01886848 0.04130826 0.08557419]
2.0430143820015707 2.04364
1.7260317333863573 1.72623
1.4539094183773056 1.45404
1.187036709759271 1.18706
0.936417771272397 0.93639
2.324334324614137e-08
'''


## 第 26 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Matlab
%%%%%%%%%%%%%%%%%%%%%%%%Small world model%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
function matrix = SW()
tic
a=1:1:40;
c=randperm(numel(a));
N=a(c(1:20));m=2;
p=0.1;
matrix=sparse([],[],[],40,40,0);
for i=m+1:N(1:20)-m
for j=i-m:i+m
matrix(i,j)=1;
end
end
for i=1:m
for j=1:i+m
matrix(i,j)=1;
end
end
for i=N(1:20)-m+1:N(1:20)
for j=i-m:N(1:10)
matrix(i,j)=1;
end
end
for i=1:m
for j=N(1:20)-m+i:N(1:20)
matrix(i,j)=1;matrix(j,i)=1;
end
end
for i=1:N(1:20)-m-1
for j=i+1:i+m
r=rand(1);
if r<=p
unconect=find(matrix(i,:)==0);
M=length(unconect);
r1=ceil(M*rand(1));
matrix(i,unconect(r1))=1;
matrix(unconect(r1),i)=1;
end
end
end
for i=N(1:10)-m+1:N(1:10)-1


## 第 27 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
for j=[i+1:N(1:20) 1:i- N(1:20)+m]
r=rand(1);
if r<=p
unconect=find(matrix(i,:)==0);
r1=ceil(length(unconect)*rand(1));
matrix(i,unconect(r1))=1;
matrix(unconect(r1),i)=1;
end
end
end
for i=N(1:20)
for j=1:m
r=rand(1);
if r<=p
unconect=find(matrix(i,:)==0);
r1=ceil(length(unconect)*rand(1));
matrix(i,unconect(r1))=1;
matrix(unconect(r1),i)=1;
matrix(i,j)=0;matrix(j,i)=0;
end
end
end
for m=1:N(1:20)
matrix(m,m)=0;
end
toc
end
function tu_plot(rel,control)
r_size=size(rel);
if nargin<2
control=0;
end
if r_size(1)~=r_size(2)
disp('Wrong Input! The input must be a square matrix!');
return;
end
len=r_size(1);
rho=50;
r=2/1.05^len;
theta=0:(2*pi/len):2*pi*(1-1/len);
[pointx,pointy]=pol2cart(theta',rho);
theta=0:pi/36:2*pi;


## 第 28 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
[tempx,tempy]=pol2cart(theta',r);
point=[pointx,pointy];
hold on
for i=1:len
temp=[tempx,tempy]+[point(i,1)*ones(length(tempx),1),point(i,2)*ones(lengt
h(tempx),1)];
plot(temp(:,1),temp(:,2),'r');
text(point(i,1)-0.3,point(i,2),num2str(i));
end
for i=1:len
for j=1:len
if rel(i,j)
link_plot(point(i,:),point(j,:),r,control);
end
end
end
set(gca,'XLim',[-rho-r,rho+r],'YLim',[-rho-r,rho+r]);
axis off
function link_plot(point1,point2,r,control)
temp=point2-point1;
if (~temp(1))&&(~temp(2))
return;
end
theta=cart2pol(temp(1),temp(2));
[point1_x,point1_y]=pol2cart(theta,r);
point_1=[point1_x,point1_y]+point1;
[point2_x,point2_y]=pol2cart(theta+(2*(theta<pi)-1)*pi,r);
point_2=[point2_x,point2_y]+point2;
if control
arrow(point_1,point_2);
else
plot([point_1(1),point_2(1)],[point_1(2),point_2(2)]);
end
%%%%%%%%%%%%%%%%%%%%%%%%%%%% Risk factor%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
x=0:60;
y=0.71*log(x)/log(60)
figure('color',[1 1 1]);
plot(x,y)
hold on;


## 第 29 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
plot([28,28],[0,0.581],'g--')
hold on;
plot([0,28],[0.581,0.581],'g--')
xlabel('Year')
ylabel('Risk factor')
hold on;
gl=[0:3:60]
Y=interp1(x,y,gl);
dian=[0
0.182,0.356,0.351,0.420,0.437,0.501,0.535,0.571,0.581,0.599,0.601,0.630,0.
656,0.640,0.668,0.665,0.651,0.683,0.710,0.712];
scatter(gl,dian,'k')
%%%%%%%%%%%%%%%%%%%%%%%%%%%% The correlation %%%%%%%%%%%%%%%%%%%%%%%%%%%
clc,clear
a=xlsread('data.xlsx','Sheet1','A4:Z504'); %The data is in Appendix II
name=xlsread('data.xlsx','Sheet1','A4:A504');
CitizenshipNumber=xlsread('data.xlsx','Sheet1','C4:C504');
Address=xlsread('data.xlsx','Sheet1','F4:F504');
ContactWay=xlsread('data.xlsx','Sheet1','G4:G504');
if(name==0&Citizenship==0&Number==0&Address==0&ContactWay==0)
Y=0;
else
gl=xlsread('data.xlsx','Sheet1','AA4:AA504');
x=0:0.00001:5;
y=300*gaussmf(x,[1.8 5]);
figure('color',[1 1 1]);
plot(x,y)
Y=interp1(x,y,gl)
end
xlabel('Information correlation')
ylabel('Price(£¤)')


## 第 30 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Appendix II
An Investigation Into Attitudes To Personal Privacy.
1. Yourgender：
A. Male
B. Female
2. Yourage：
A．≤11years
B.12 years—18years
C.19 years—35years
D. 36years—65 years
E.≥65 years
3. Yourcareer：
A. Government officials
B Technical personnel
C. Juniorofficers
D. Business services
E. Business and servicepersonnel.
F.Production, transportation equipment operators and related personnel.
G.solder
4. Youattach great importance topersonal privacy information.：
A. attach great importance to
B. attach importanceto
C. generalemphasis
D. donot takethe
E. it doesn't matter
5. Pleasefill inthe followingtablewith thefollowing information youthink:
Forexample, ifyouthinkthe home address information isthree times as important as
thename information, please fillin the"3"inthe correspondingform; Ifyouthinkthe
importance ofgenderinformation is 1/8 times thatofinterest andhobbies, pleasefill in
"1/8"inthecorresponding form.


## 第 31 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
xl x2 x3 x4 xS x6 x7 x8 x9 xlO I xll x12 x13 x14 I x15 x16 xl 71 x18 I x19 I x20 I x21 I x22 x23 x24 x25 x26
N皿阳CxlJ I 1
Gender(x2)
C,h zensh,p Number (x3)
Age( x4)
Educahonal Background( x5)
Address( x6)
。
c ntact曹ay(x7)
Fait h(x8)
Portrait (x9)
H。bby(xlO)
Total Assets(xll)
Income (x12)
Expenditure( x13)
Intellectual Pr。perty(x14)
s。cialiay(x15)
Fnends (x16)
Social Signal (xl 7)
Financial Credit (x18)
Trading Info，回tion(x19)
。 。
Transactioo nAmunt(x20)
Debt(x21)
Physical Heal th Status( x22)
ledical Insurance( x23)
ledical Hist。ry(x24)
ledical Expense(x25)
Genetic Ian (x26}

# E78511-How Will Climate Change A ect Fragility


## 第 1 页

精品数模资料，各类F比o赛r o优c秀e论u文se、o学nly习教程、写作模板Te与a经m验C技on巧tro、lmNautmlabbe程r序代码资料等，Fo尽r在o淘ce宝u店se铺o：nl闵y大荒工科男的杂货铺！
T1 T1
78511
T2 T2
ProblemChosen
T3 T3
E
T4 T4
2018
MCM/ICM
How Will Climate Change A ect Fragility?
People living in fragile states are more vulnerable to potential shocks. With the
climate change exacerbating fragility, people gradually begin to focus on the
importance of measuring and dealing with the fragility. In order to solve these
problems, we rst establish an evaluation model to measure the fragility under climate
change. Then it is applied to Afghanistan and Egypt to show their fragility situation. At
last, a set of optimal interventions are given and the model is modi ed in order to
apply to smaller and bigger states.
To begin with, 37 inferior factors are considered into our model and we gure out
the normalization method and measurement for each inferior factor. After that, eight
superior indicators are summarized from inferior factors include food, water, shelter,
security, stability, economics, governance and demography. The analytic hier-archy
process method is used to weigh these indicators. At last, the impacts of climate
change are characterized by precipitation, arable land, temperature and natural
disasters.
Next, the evaluation model is applied to Afghanistan and Egypt. Afghanistan is in the
top ten fragile states list and Egypt is not in the top ten list. Fragility indicator is used to
measure the fragility. It is a bene t-type indicator normalized to the range of [0,1]. Using
the collected data, we nd that with the climate change, the fragility indicator is 0.280 for
Afghanistan and 0.407 for Egypt. Without the climate change, it is
0.310 for Afghanistan and 0.428 for Egypt. The percentage change is 10.7% and
5.2%, respectively. Among the eight superior indicators, economics is mostly a ected.
At last, we use the K-Means Clustering Algorithm to determine the tipping point and
stable point. Results show the tipping point is 0.428 and the stable point is 0.711.
In order to help Afghanistan and Egypt escape from the fragility, an optimization
model is developed to maximize the fragility indicator under the limitation of the
budget. To prevent fragility, Afghanistan needs to spend 285% of its GDP (57.2
billion dollars) and Egypt 1% (3.32 billion dollars). We gure out the optimal
distribution of money using our optimization model. Results show that money for food
and water should account for 30% and 25%, respectively. Sensitivity analysis is
made at the end. Our model is a little more sensitive to precipitation.
At last, our model is modi ed to t for smaller and bigger states. For smaller states,
the factors and weights are reconsidered and the cost of intervention is lower
because of the synergy e ect; for bigger states, the sphere of in uence is restrained,
and the cost is higher because of the di culty in managing the bigger states. Still
using the data of Afghanistan and Egypt, we nd that other things equal, smaller
states can develop more quickly while bigger states develop much more slowly.


## 第 2 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Contents
1 Introduction 1
2 Assumptions 2
3 Measurement of Fragility and Climate Change 2
3.1 Establishment of the Fragility Model . . . . . . . . . . . . . . . . . . . . . 2
3.1.1 Discussion of the Superior and Inferior Indicators . . . . . . . . . . 3
3.1.2 Normalization of Inferior Indicators . . . . . . . . . . . . . . . . . . 4
3.1.3 Determination of the Weights for Indicators . . . . . . . . . . . . . 6
3.2 Modeling the Climate Change Impacts . . . . . . . . . . . . . . . . . . . . 6
3.2.1 Characterizing the Climate Change . . . . . . . . . . . . . . . . . . 6
3.2.2 Water and Food Scarcity Impacts . . . . . . . . . . . . . . . . . . . 7
3.2.3 Potential Insecurity and Instability Impacts . . . . . . . . . . . . . 8
3.2.4 Extreme Weather and Disasters Impacts . . . . . . . . . . . . . . . 9
4 Analysis of Fragility in Afghanistan and Egypt 10
4.1 Fragility Situation in Afghanistan and Egypt . . . . . . . . . . . . . . . . . 10
4.2 Sensitivity analysis . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 12
4.3 Determination of Tipping Point . . . . . . . . . . . . . . . . . . . . . . . . 12
5 Designation of Intervention Plan 13
5.1 Establishment of the Optimization Model . . . . . . . . . . . . . . . . . . . 13
5.2 Formulation of a Intervention Project . . . . . . . . . . . . . . . . . . . . . 14
5.3 Impacts of the Intervention Project . . . . . . . . . . . . . . . . . . . . . . 16
5.4 Sensitivity Analysis . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 16
5.5 Suggestions . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 17
6 Modi cation of Fragility Model 17
6.1 Modi cation for Smaller States . . . . . . . . . . . . . . . . . . . . . . . . 17
6.2 Modi cation for Bigger States . . . . . . . . . . . . . . . . . . . . . . . . . 18
6.3 Application to Afghanistan and Egypt . . . . . . . . . . . . . . . . . . . . 19
7 Conclusions 20
8 Strengths and Weaknesses 20
Reference 21
Team # 78511 Page1 of21
1 Introduction
Backgroud
People used to think that climate change just a ects the environment business. How-
ever, Frank Walter, the foreign minister in Germany, claimed that climate change is a
growing threat to peace and stability[1] . It will aggravate the fragility of countries.
When the climate change is combined with the poverty and resource scarcity, the
state might be more fragile because of the violent con icts caused by the combination.
We have to study on the relationship between climate change and fragility of
countries, in order to halt the exacerbation of fragility and o er the reasonable
intervention plans to the fragile states.


## 第 3 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Literature Review
States can be divided into fragile states and resilient states. Fragility and resilience
are de ned in the report of New Climate for Peace. Fragility is the inability (whether
whole or partial) of a state to ful l its responsibilities as a sovereign entity, including a
lack of legitimacy, authority, and capacity to provide basic services and protect its
citizens[2] . Resilience is the opposite. Climate change alone cannot make signi cant e
ects on the state, but it can so when it interacts other pressures. There are seven risks
that will emerge: local resource competition, livelihood insecurity and migration, extreme
weather events and disasters, volatile food prices and provision, transboundary water
management, sea-level rise and coastal degradation, and unintended e ects of climate
policies. These possible consequence o ers the base of thinking for our study.
The essay of Department for International Development indicated that, the
governance e ciency, state function and international support need to be improved, in
order to relieve the fragility problem[3] . In another essay, the writer pointed out that the
rebuilding of Afghanistan includes the economic, politics, security and society area[4] .
These facets should be included in our fragility model to make it more comprehensive.
The previous researches have contributed a lot to the solution of fragility
problems, but there are still some limitations of their work for solving our problem. For
instance, the factors of the physiological need are ignored in the rank of fragility, and
the cost of the intervention has not been considered. Furthermore, they provide little
statistics and models to measure the fragility, which are taken into account in our
study, these factors are involved to build a more complete and useful model.
Our Work
Because of the weaknesses of the previous work, we should further study this
issue in detail. The mind map of our study is shown in Figure 1 in detail. Firstly, a
new evaluation model should be established considering more factors. Climate
change impacts should also be taken into account. In our study, the climate change
is regarded as an in uential factor added into the fragility evaluation model. After that,
Afghanistan and Egypt are analyzed and the fragility situations are discussed.
Afghanistan is in the top ten fragile states list while Egypt is not.
In order to ght against fragility, interventions are needed. Optimization model is
used to gure out the best intervention plan under the limitation of budget. The main
purpose is to maximize the fragility indicator. At last, modi cation is made to smaller
and bigger states according to their natural features. The factors and costs of
intervention for smaller and bigger states are reconsidered.


## 第 4 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team # 78511 Page2 of21
Figure 1: Flowchart of our study
2 Assumptions
The fragile states are not able to adapt to the climate change in the short run.
{ If a state can adapt to that change well, climate change can even bene t that
state[5] . Considering that most fragile states are developing states, we
assume that they are not able to adapt to the climate change in the short run.
The long run impacts of natural disasters are neglected.
{ The impacts of natural disasters are always direct, like economic loss. In
the long run, the disasters will be solved and their impact will not last as
long as other climate changes like temperature increase.
The marginal cost of intervention increases linearly.
{ This is a reasonable simpli cation of increasing marginal cost[6] . In reality,
the increase of marginal cost depends on the speci c situation.
The physiological need is the most important need of human.
{ Physiological need is the most basic need. It should be given more attention.
3 Measurement of Fragility and Climate Change
The fragility model includes two parts: the indicators used to describe fragility and
the impacts of climate change on indicators. The fragility of a state is actually
measured by the indicators and the impacts of climate change is built into the
indicators. Therefore, We will rst establish an indicator system to evaluate the fragility.
Climate change is regarded as in uential factors to the indicators.
3.1 Establishment of the Fragility Model
According to the problem, a fragile state is one where the state government is not
able to, or chooses not to provide the basic essentials to its people. This implies that the
theory of needs can be applied to measure the fragility. The most popular theory of
needs is Maslow's hierarchy of needs. From the most basic needs to the most superior,
the needs are physiology, safety, society, self-esteem and self-actualization[7] .
We only take into account the three most basic needs, considering that fragile states
are often characterized by low income and weak government[8] . The framework of the


## 第 5 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team # 78511 Page3 of21
fragility model is shown in Figure 2. Several speci c factors are considered under each
type of need in Figure 2. The physiology is consisted with food, water and shelter. The
safety is consisted with security and stability. The society is consisted with economics,
governance and demography. We set an indicator for each detailed need, so we get
eight superior indicators describing the fragility. A speci c assemblage I is given for them:
I = fF D; W A; SH; SC; ST; EC; GN; DMg
where F D, W A, SH, SC, ST , EC, GN, DM represent food, water, shelter, security,
stability, economics, governance and demography, respectively.
There are many inferior indicators under each superior indicator. As shown in Figure
2, 37 inferior indicators are considered in our fragility model. The superior indicators are
determined by the linear combination of these inferior indicators. The determination of
the weights will be discussed later. Those eight superior indicators measure the fragility
of a state. Weset the fragility indicator F as the linear combination of them:
X
F = !ii (1)
i2I
where !i is the weight of each superior indicator.
Figure 2: Framework of fragility model
We are going to introduce the inferior indicators and normalize each of them into
the same pattern. After that, the weights of each superior and inferior indicator will be
determined using the Analytic Hierarchy Process (AHP).
3.1.1 Discussion of the Superior and Inferior Indicators
The fragility indicator is calculated by eight superior indicators and the superior
indi-cators are determined by the inferior indicators. We are going to discuss about
them in detail.
Physiology
Food is a basic precondition for living, so it is also a critical factor related to the
fragility. When a country is lack of food, citizens will not satisfy and they may rob
others or even attack the government. Therefore, the more food people can get, the
less fragile the country is. The food indicator (F D) is based on the following inferior
indicators: food production per capita, average food price and food import quantity.


## 第 6 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team # 78511 Page4 of21
Similarly, people need usable water to maintain their subsistence. A state may
become less fragile because of the insu cient usable water. Therefore, the water
indicator (W A) is also used to re ect the fragility. The speci c inferior indicators are:
water quantity per capita, sewage discharge rate, improved water rate and total water
reservoir.
Shelter is an important factor a ecting fragility. In the fragile countries, people
gener-ally do not have a stable shelter, especially when the violent con icts exist.
This situation can exacerbate the fragility[9] . The inferior indicators for shelter
indicator (SH) are: housing area per capita, slum population portion and house price.
Safety
The security indicator (SC) is important for the safety. the speci c inferior indi-
cators for the factors listed in Figure 2 are: crime rate, external intervention level,
number of terrorist attacks, army power and police density.
The stability indicator (ST ) refers to the stability of the migration of population, so
it is a ected by the population mobility. In some states, refugee is a serious problem.
Their migration and mobility can disturb the society severely. The society is also su
ered from the violent con icts. The inferior indicator for these factors are refugee
index, number of violent con icts and migration rate.
Society
The economic indicator (EC) is rather important. It is in uenced by many aspects,
like GDP, in ation, etc. The inferior indicators are chosen as: GDP per capita, in-ation
rate, unemployment rate, the Gini coe cient, debt to GDP ratio and interest rate.
The governance indicator (GN) mainly refers to the ability to manage the society.
It measures whether the government can manage the state well. The inferior
indicators for it are law system completeness, management e ciency, corruption rate,
public service quality, party relationship and the government support rate.
Demography indicator (DM) describes the features related to people, like pop-
ulation and age structure. Similarly, the inferior indicators are: population density,
amount of the ethnics, literacy rate over 15 years old, epidemic rate, sex ratio,
average age and equity level.
3.1.2 Normalization of Inferior Indicators
The inferior indicators need to be normalized into the range of [0,1]. Meanwhile,
the inferior indicators need to be transformed to the bene t-type indicators which
means that the larger the better. We use di erent normalization method to normalize
di erent kinds of indicators according to their characteristics. These methods include
the logistic function, the maximum normalization method, the moderate normalization
method, the minimum normalization method and the subordinate function of fuzzy
mathematics. We are going to show the applications of each method we use.
Logistic function
This normalization method is applied to indicators which do not have a speci c upper
limitation, such as the food production per capita. There are some rules of normalization for
this kind of indicators. When the original indicator is close to 0, the normalized indicator
should be 0; when the original indicator approaches in nity, the normalized indicator should
be close to 1. Meanwhile, the normalized indicators should rise sharply when it is close to 0.
For thesereasons,we chooselogisticfunction tobethenormalization


## 第 7 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team # 78511 Page 5 of 21
function:
1
x 0 = 1 +e b(x x ) (2)
0
0
where x is the normalized indicator; x is the original indicator; x0 is the minimum
stan-dard of the indicator; b is a parameter to control the climbing speed of the
normalization function. The value of b will be determined in the solution of model.
Maximum normalization method
This method is used to normalize the bene t-type indicators, like the improved water
rate. The greater the indicator is, the better the situation is. The way to normalize the
indicators is
x
x 0 = x (3)
max
wherexmaxisthe maximum ofthe indicator.
Minimum normalization method
This method is similar to the maximum normalization method. It is used to normalize
the cost-type indicators, such as the crime rate. The way to normalize the indicators is
x
= 1
x 0 xmax (4)
Moderate normalization method
This method is used to normalize the moderate-type indicators. When the
indicator is close to the optimal value, the state can have better resilience. The
example of this kind of indicators includes the in ation rate. The way to normalize is
jx xopj
0
x = (5)
maxfjxmax xopj; jxmin xopjg
wherexopis the optimalvalue ofthe indicator.
Subordinate function
This method is used to normalize the discrete indicators. These indicators can be
divided into several intervals with a discrete grade, like GDP per capita. According to
the theory of fuzzy mathematics, we choose the correspondence of the value set and
the comment set as:
fAwf ul; Bad; N ormal; Good; Excellentg = f1; 2; 3; 4; 5g (6)
The partial large Cauchy distribution membership function is determined as:
We set that when the grade value is 1, the membership grade should be 0.01; when
the grade value is 3, the membership grade should be 0.8; when the grade value is 5,
the membership grade should be 1. Hence, the parameters of the partial large Cauchy
distribution membership function can be determined as:
(
c=0:3915; d = 0:3699 (8)
a = 1:1086; b = 0:8942
Using these normalization method, all the inferior indicators can be normalized.
Here we omit the detailed methods for each inferior indicator.


## 第 8 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team # 78511 Page6 of21
3.1.3 Determination of the Weights for Indicators
The Analytic Hierarchy Process (AHP) is a well-developed method which is used
to analyze the weights. The hierarchy structure of the indicators need to be
determined. It consists eight superior indicators and 37 inferior indicators.
The weights of normalized superior and inferior indicators is calculated using AHP
method. Speci cally, the superior indicators are divided into three groups based on
the three kinds of need. The weight of the superior indicators in the same group is
regarded as the same. The results are listed in Table 1.
Table 1: Theweightsof indicators
Physiologicalneed
Food18% Water 18% Shelter 18%
Price 26%, Import 10% Stress46%,Sanitation26% Houseprice14%,Slums24%
Production 64% Pollution14%, Reservoir14% Housingarea62%
Safetyneed
Security 15% Stability15%
Externalintervention11% Refugee29%, Violentconict 62%
Military6%, Public order21% Population mobility 9%
Terroristattack42%, Crimes20%
Societyneed
Economics5.33% Governance5.33% Demography5.33%
GDP 40%, National debt 6% Law 5%, Corruption 18% Population47%
Ination16%, Interest5% Management34% Education6%, Health10%
Unemployment10% Party22% Genderdistribution 10%
Unevendevelopment23% Public support 9% Equality4%, Ethnic18%
Public services 12% Age structure 5%
We assume the physiology is the most important factor. Therefore, the food, water
and shelter indicator occupy the largest weights. Among the inferior indicators, the food
production, the water stress and the housing area indicators are most important. As for
safety and society, the management, GDP, terrorism and violent con ict seem to be more
signi cant. These indicators do have huge impact on the fragility of a country in reality.
3.2 Modeling the Climate Change Impacts
Next, we will measure the impacts of climate change. The climate change
includes many kinds of forms, such as shrinking glaciers and unpredictable weather.
We should describe them using typical parameters so that it can be made clear.
3.2.1 Characterizing the Climate Change
We extract three important factors as they run through nearly all of the climate
changes. These three factors are: percentage change of the precipitation, arable land
and temperature. Besides, another category called natural disaster is also set to
include those climate changes which are not re ected by the three factors.
We will de ne the direct and indirect impacts of climate change. The direct impacts of
climate change are de ned as impacts which are simply caused by climate change and
do not necessarily relate to other factors. They are always the impacts to food, water and
shelter. The indirect impacts of climate change are impacts which are caused


## 第 9 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team # 78511 Page7 of21
by climate change combined with other factors. They are always the impacts to
factors under safety and society in Figure 2.
The climate impacts report has analyzed the impacts in detail. They gave out sev-
en ways in which climate change may exacerbate the fragility[2] . We list them out as
follows: 1. local resource competition; 2. livelihood insecurity and migration; 3.
extreme weather events and disasters; 4. volatile food prices and provision; 5.
transboundary water management; 6. sea-level rise and coastal degradation; 7.
unintended e ects of climate policies.
We can categorize them into some groups according to the their general features.
These seven impacts can be concluded into three general features: water and food
scarcity (W F S), potential insecurity and instability (P II)and extreme weather and
disasters (EW D). Local resource competition, volatile food prices and provision and
transboundary water management are categorized into W F S. They are all impacts
related to water and food. Livelihood insecurity and migration, sea-level rise and
coastal degradation and unintended e ects of climate policies belong to P II. As for
the natural disasters, it will be discussed in EW D.
Up to now, we summarize the climate change impacts into three categories, which is
shown in Figure 3. The impacts caused by the change of climate factors except disasters
have long run impacts. EW D refers to the sudden impacts because of disasters. Wecan
express the superior indicators after taking each kind of impacts into account as
ic = fi i i; i 2 I (9)
where ic is the indicator after the impacts of climate change; fi is the in uential coe -
cients of di erent indicators, which characterize the long run impacts; i is the sudden
impacts caused by the natural disasters.
Figure 3: Categories of Climate Change Impacts
The four climate factors we re ned can describe most of the impacts. We will next
determine thein uential coecientsandthesuddenimpacts basedon thethree categories.
3.2.2 Water and Food Scarcity Impacts
Water and food scarcity (W F S) includes water scarcity and food scarcity.
Climate change can make both direct and indirect impacts related with W F S, as de
ned before. We will discuss these two types of impacts, respectively.
Direct impacts
The direct impacts of W F S are the water scarcity and food scarcity caused by
pre-cipitation decrease, arable land decrease and temperature increase. Speci cally,
water scarcity is only related to the precipitation, and food scarcity is related to
precipitation, temperature and arable land.


## 第 10 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team # 78511 Page8 of21
Food may be a ected by all of the climate factors. We assume that food will
change proportionally with each climate factor, so the in uential coe cient of food can
be ob-tained as:
fFD = (1 pr)(1 te)(1 ar) (10)
where pr; te; ar are the percentage change of precipitation, temperature and arable
land, respectively.
Water is mainly relevant to the precipitation. The same proportional assumption is
made so that the in uential coe cient of water fWA is
fWA = 1 pr (11)
Indirect impacts
The indirect impacts mainly refer to impacts on security and some social factors
(Figure 2). They are caused by the combination of climate change and W F S. This is
in line with the fact that resources scarcity and poor governance can combine to a ect
fragility, as illustrated in the reference [2].
First we concern the indirect impacts on security. Poor governance can further
exacer-bate the side e ects like violent con icts according to the report of G7 in
2015[2] . This can worsen the security of a state. Thus, the in uential coe cient fSC;1
for security indicator is de ned as
where GN is the governance indicator; ; ; re ect the importance of governance to
cope with climate change. As we can see from Equation 12, it involves both the
climate change and governance. The greater the climate change factors i are, the
smaller the in uential coe cient for security indicator is.
Now we are going to talk about the impacts on economics. Food scarcity will cause
volatile food prices. The increase of food price will inevitably cause the price level to rise,
because food is a kind of necessity for subsistence. This is known as in ation. Therefore,
climate change will have indirect impacts on economics. Furthermore, this will cause the
whole economy to be a ected more signi cantly than the initial impact because of the
multiplier e ect[10] . The multiplier e ect is the reality that people have their marginal
propensity to consume (M P C) and will not spend all the money. Therefore, the whole
economy would lose more from an economic perspective than the initial impact. Based
on the above analysis, the in uential coe cient fEC is
3.2.3
Potential Insecurity and Instability Impacts
Climate change makes impacts related with potential insecurity and instability (P II).
For direct impacts, climate change can signi cantly a ect the environment. Once the
environment is not suitable to live, people will have to migrate to other places. This might
increase the risks of insecurity and instability. What's more, temperature increase will
also a ect human health and further exacerbate the demographical situation. For indirect
impacts, the security, stability and governance should be taken into account.
Direct impacts


## 第 11 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
The direct impacts on P II mainly refers to the impacts on the shelter and demography.
Shelter is mainly a ected by the sea-level rise and coastal degradation. Sea-level rise is
caused by the melting of glaciers, so we can assume that the rate of sea-level rise is


## 第 12 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team # 78511 Page9 of21
proportional to the temperature increase[11] . We can get the rate of sea-level rise is
dH
=a (t)T (14)
dt te 0 where a is proportionality
constant; te(t)T0 is the temperature increase. Besides, the lower the elevation of a region
is, the more susceptible the region is to the sea-level rise. Thus, we use the ratio of the
elevation and sea-level rise rate to measure the impact of sea-level rise to the shelter.
Considering that people may also migrate to other places because of the lack of
precipitation and arable land, we take the in uential coe cient of shelter indicator as
E
where E is the elevator; dH=dt is the rate of sea-level rise. According to Equation 15,
if the elevation is relatively high, the shelter indicator will almost not be in uenced.
Demography would be a ected by temperature because of health. Germs may be-
comemore active in high-temperature areas. For simplicity, we approximately take the
in uential coe cient of demography as
Indirect impacts
Large amount of people might surge into the city or other regions because of the
climate change. This is a threat to the security and stability of a region. Besides, the
public services in the region may be insu cient if there are too many people.
Therefore, the security, stability and the governance quality will be a ected.
The threat to the security mainly comes from migration and disease, and the sound
quality of governance can alleviate it to some extent. If migration is banned or limited, this
kind of security threat will decrease. Therefore, the in uential coe cient of security should
takemigration, disease andgovernanceindicator intoconsideration. Itis determinedas
+ +
fSC;2 = fSH fDM GN
SC;2 pr SC;2 ar SC;2 te
(17)
where ; ; re ect the importance of law to cope with climate change. Combine t-wo in
uential coe cients of security indicator, and we can get the complete in uential coe
cient for security fSC as
f =f f
SC SC;1 SC;2 (18)
The stability only relates to the migration of people and completeness of the law,
which is similar to what we have discussed for the security. Therefore, the in uential
coe cient of stability indicator is
+ +
fST=fSHGN ST pr ST ar ST te (19)
On the contrary, governance quality can also deteriorate because of the migration,
such as public service and management. Governance quality can be in uenced by
the de-mographic indicators, like population and education. Therefore, the in uential
coe cient of governance indicator fGN is
+ +
fGN=fSHDM GN pr GN ar GN te (20)
3.2.4 Extreme Weather and Disasters Impacts
Extreme weather and disasters (EW D) is a special form of climate change impacts
which is di erent from (W F S) and (P II). W F S and P II are caused by the change of
precipitation, arable land and temperature, which belong to the long-run impacts. On


## 第 13 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team # 78511 Page10 of 21
the contrary, EW D does not have signi cant long-run indirect impacts, but it does
great harm directly in the short run. For example, droughts, ood or hurricane will not
maintain for a long time, but they will cause destroyable damage to assets and
lives[12] . Therefore, we only focus on the direct impacts of EW D in this part.
Natural disasters are somewhat random. Therefore, we use the random simulation to
simulate natural disasters and measure its possible in uence. The Poisson distribution is
often used to measure the frequency of natural disasters in a given period[13] , so we
suggest that the number of disasters in a year follows the Poisson distribution:
where is the parameter of Poisson distribution, also known as the mean value of N.
describes whether the natural disasters occur frequently or not in this region and it
can be determined by the history data.
The natural disaster will a ect our fragility indicators when it occurs. The general
signi cance of its impacts is measured by the exponential distribution. We assume
the general signi cance is 0.001 each time in average, so we get
( 1000e 1000x ; x > 0
Sig f(x) = 0; x 0 (22)
The mean value is chosen as the general signi cance Sig. The decrease in each
fragility indicator is still simulated using exponential distribution, based on the general
signi cance of the disaster. Therefore, the impacts of the disasters are expressed as:
:
Up to now, the in uential coe cients fi and sudden impacts i are determined. The
superior indicators after taking into account the climate change ic is calculated using
Equation 9.
4 Analysis of Fragility in Afghanistan and Egypt
We choose Afghanistan and Egypt as our study objects. Afghanistan is in the top
ten fragile states list, while Egypt is not. Afghanistan is fragile with dry climate and
water scarcity. Egypt is a state whose fragility level is at the boundary of fragility. We
will calculate the fragility with and without impacts of climate change for Afghanistan
and Egypt. Meanwhile, the di erences between the two states will be compared.
4.1 Fragility Situation in Afghanistan and Egypt
The original fragility of Afghanistan and Egypt can be obtained based on our
model and the data of inferior indicators. Other parameters will be set according to
references and reality. At last, we will do sensitivity analysis of the critical variables:
the percentage change of precipitation, arable land and temperature.
In order to calculate the fragility indicator, the weights and data of each inferior
and superior indicators must be obtained. In subsection 3.1, the weights have been


## 第 14 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
determined using AHP. In this part, some parameters and data will be decided and
collected. In order to calculate the fragility indicator after climate change, the
parameters in subsection 3.2 should be determined.


## 第 15 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team # 78511 Page11 of 21
We can get some information about precipitation, arable land and temperature
change from references [14] and [15]. The climate change is estimated as 0.1% for
temperature increase, 0.2% for precipitation decrease and 2.7% for arable land decrease.
The param-eters of the importance of governance to cope with climate change ; ; are set
to 1 for simplicity. According to economic textbook[16] , the marginal propensity to
consume M P C is estimated as 0.6 in average. The proportionality constant a in the
expression of sea-level rise rate is determined by the relative research as 0.34mm/year
per centigrade[11] . which measures the average number of disasters is set as 10. The
average temperature is estimated as 20 C for Afghanistan and 25 C for Egypt.
Table 2: Superior indicatorsbeforeandafter climatechange
Afghanistan Egypt
Without Withclimate Without Withclimate
Indicators
climatechange change climatechange change
F D 0.271 0.307 0.409 0.429
WA 0.336 0.363 0.547 0.557
SH 0.324 0.341 0.520 0.543
SC 0.070 0.105 0.161 0.183
ST 0.149 0.174 0.215 0.240
EC 0.305 0.379 0.538 0.596
GN 0.437 0.471 0.429 0.454
DM 0.729 0.749 0.598 0.602
F 0.280 0.310 0.428 0.407
The values of superior indicators and fragility indicator (F ) of Afghanistan and
Egypt without and with climate change are listed in Table 2. The fragility indicators
are cal-culated using Equation 1. From Table 2, the fragility of Afghanistan increases
from 0.28 to 0.31 without the impacts of climate change. The percentage change is
10.7%. This is a relatively signi cant change for Afghanistan. As for Egypt, the
fragility indicator decreases from 0.428 to 0.407 after the impact of climate change.
The percentage change is 4.9%. This is a smaller change but is still signi cant.
Compare Afghanistan and Egypt and we nd Afghanistan is more vulnerable. This
indicates that states with lower fragility indicator will be more vulnerable.
(a) (b)
Figure 4: Superior indicators with and without climate change:
(a) Afghanistan; (b) Egypt.


## 第 16 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team # 78511 Page12 of 21
The signi cance of climate change impacts can be demonstrated more intuitively
by the radar graph shown in Figure 4. From Figure 4(a), the economic indicator,
shelter indicator and governance indicator are more vulnerable. The demography
indicator is the least vulnerable in Afghanistan. The similar impacts also t for Egypt,
as shown in Figure 4(b). Speci cally, the economic indicator is very vulnerable in
Egypt. This is a result of the huge population in Egypt and that each person has a
marginal propensity to spend money.
4.2 Sensitivity analysis
Next, we will do the sensibility analysis for the important variables: percentage
change of precipitation, arable land and temperature. We will discuss the in uence of
these three parameters on the fragility indicator. The initial value of these three
parameters are set as 0.2%, 2.7% and 0.1%, respectively. When discussing one of
them, the other two parameters are set as the initial values.
We change the three parameters from 0.05% to 5% with the footstep of 0.05%.
The variation of the fragility indicator of Afghanistan and Egypt is shown in Figure 5.
From Figure 5, we can conclude that the fragility indicator keeps a decreasing trend
with the rise of the three parameters. It is obvious that the in uence of the percentage
change of precipitation decrease pr is more signi cant than the other two parameters.
The in uence of the percentage change of temperature increase te performs di erently
in di erent countries. For Afghanistan (Figure 5(a)), the in uence caused by
temperature increase seems to be not signi cant. For Egypt (Figure 5(b)), the in
uence is more obvious, so Egypt is more sensitive to temperature increase. Besides,
the in uence of the natural disasters is shown by the uctuation of the fragility
indicators. The drastic uctuation shows that the in uence of natural disasters is very
crucial to the fragility indicator. In conclusion, the decrease in precipitation and the
natural disasters are the two main reasons which make the two states more fragile.
(a) (b)
Figure 5: Sensitivity analysis of the percentage change of climate factors:
(a) Afghanistan; (b) Egypt.
4.3 Determination of Tipping Point
There are 193 countries all over the world and about 35 to 50 of them are listed
as fragile states[8] . This means that about a quarter of countries in the world are
fragile states. Our tipping point should be determined as the boundary between these
fragile states and other states. What's more, we will additionally de ne a stable point
which divide the vulnerable country and stable country.
We classify the countries in the world into four categories according to the fragility
indicator. The boundary of the most fragile states is the tipping point and the boundary


## 第 17 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team # 78511 Page13 of 21
of the stablest group is the stable point. The method we use is the K-means Cluster-
ing Algorithm. K-means Clustering Algorithm aims to partition n observations into k
clusters[17] . Its purpose is to minimize the sum of the distances from the sort center
D( k)
th
where xi is an observation in the k cluster Ck.
However, it is so di cult to calculate the fragility indicator of each country in the
world so that the K-means Clustering Algorithm is hard to apply. Therefore, we will rst
use FSI (Fragile States Index) to nd the tipping point based on the o cial indexes.
Then we will nd the country whose FSI is the closest to the tipping point. At last, we
calculate the fragility indicator of that country using our model and set it as our tipping
point.
The tipping point is calculated as 91.3 and the stable point is 47.4 based on FSI,
as shown in Figure 6(a). The FSI of Egypt is 89.8, which is close to the FSI tipping
point. The FSI of Argentina is 48.2, which is the closest to the FSI stable point. We
approxi-mately use the fragility indicator of Egypt as the tipping point and that of
Argentina as the stable point.
The fragility indicator of Egypt and Argentina are 0.428 and 0.711, respectively.
Therefore, the tipping point is determined as 0.428 and the stable point is 0.711. As
shown in Figure 6(b), when the fragility indicator is lower than 0.428, the state is fragile;
when the fragility indicator is greater than 0.711, the state is stable, otherwise the state
is vulnerable.
(a) (b)
Figure 6: Tipping point and stable point in di erent calculation systems:
(a) FSI; (b) fragility indicator.
5 Designation of Intervention Plan
Intervention plans for Afghanistan and Egypt are necessary. Fragility is harmful
for a state to develop. We will establish an optimization model under the budget limit
for ghting against fragility. Then we move on to decide the values of related
parameters. After solving the model, a set of intervention plans and its impacts will be
given. At last, we will analyze the sensitivity of the climate change factors.
5.1 Establishment of the Optimization Model
Our optimization model is a single objective model. The objective of the
optimization model is maximizing the fragility indicator. The main constraint is the
total budget for improving fragility indicator. That means we should maximize the
fragility indicator with a certain amount of budge.
Better management of budgets can bene t the fragility to the best extent. This
decides that the constraints of the model mainly come from the budget B. Therefore,
total cost of the interventions should not exceed the total budget:


## 第 18 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！


## 第 19 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team # 78511 Page14 of 21
where Bi is the money spending on each superior indicator.
When an indicator increases by 0.01, the certain amount of money is needed. We call
0
the amount of money as Bk . According to the economic law of increasing marginal
cost[6] , themarginal moneyBk 0 neededfortheadditional improvement increasesprogres-
sively. For simpli cation, we approximately take it as
where i is the linear coe cient; i0 is the original value of indicators before taking into
account the impacts of climate change. In this way, the budget used to improve a
certain fragility indicator can be written as
Taking into account the relationships between those superior indicators
established in subsection 3.1, and we can nally obtain the optimization model:
There are also other constraints which relate the indicators together. These
constraints include Equation 9-13, 15-20 and 23.
5.2 Formulation of a Intervention Project
In order to re ect the amount of money needed intuitively, the proportion of budget
in GDP r is used to describe the money needed, so the budget for fragility dealing is
B = rGDP (29)
The GDP of Afghanistan and Egypt in 2016 are 21.06 and 332.3 billion dollars,
respec-tively. We assume that the percentage of precipitation decrease, arable land
decrease and temperature increase are 0.2%, 2.7% and 0.1%, respectively, which is
in accordance with the former part. Further analysis of the percentage changes will
be shown in the sensitivity analysis.
Figure 7 shows the relationship between fragility indicator and the budget. For both
Afghanistan and Egypt, intervention plans are e ective. However, Figure 7(a) illustrates
that 285% of Afghanistan GDP is needed to prevent Afghanistan from being a fragile
country. That is, the total cost of intervention is about 57.2 billion dollars. It is hard for
Afghanistan to escape from fragility without the external help. As for Egypt, its fragility
indicator is 0.428 without the impacts of climate change, which is set as our tipping point.


## 第 20 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
After taking into account the climate change impacts, the fragility indicator of Egypt
decreases to about 0.38, which means that Egypt becomes a fragile state. Egypt must
spend 1% of its GDP (about 3.32 billion dollars) to deal with fragility problems in order to
prevent itself from turning into a fragile state. The scal pressure for Egypt


## 第 21 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team # 78511 Page15 of 21
is much lower than that of Afghanistan. There are two reasons account for this result.
On the one hand, Egypt is not far away from the tipping point at the very beginning
while Afghanistan is in the top ten fragile states list. On the other hand, the GDP of
Afghanistan is much lower than Egypt. This means Afghanistan must spend a larger
portion of its GDP.
(a) (b)
Figure 7: Fragility situation with/without climate change and intervention:
(a) Afghanistan; (b) Egypt.
We will give the optimal intervention plan under the budget of each country. As
analyzed above, the total cost for Afghanistan to escape from fragility is 57.2 billion
dollars and for Egypt, 3.32 billion dollars, so we discuss the intervention plan under
these budgets. We get the optimal plan from the optimization model and show it in
Figure 8. As we can see from Figure 8, the allocation of the budget is similar for
Afghanistan and Egypt. What's more, the indicators of the physiological need should
be invested more because they are given more weights in our fragility model. They
are the most basic factors to prevent fragility.
Based on these results, we suggest that both Afghanistan and Egypt should spend
about one-third of their budget on the facet of food. Following that, nearly one-fourth of
the budget should be spent to improve water situation, such as water pollution, water
sanitation and water stress. Food and water are two basic requirements of people. Shel-
ter and security should be regarded as equally important according to the optimization
results, where Afghanistan and Egypt should spend about 6.5 billion and 0.4 billion re-
spectively. As for facets of other superior indicators:stability, economics, governance and
demography, Afghanistan should spend 4.51, 2.62, 1.61 and 2.23 billion dollars and
Egypt 0.27, 0.15, 0.09 and 0.13 billion dollars.
(a) (b)
Figure 8: Optimal allocation of budget: (a) Afghanistan; (b) Egypt.


## 第 22 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team # 78511 Page16 of 21
5.3 Impacts of the Intervention Project
We compare the superior indicators before and after intervention in order to know the
impacts of the intervention. The impact of interventions on superior indicators can be
obtained according to the third constraint in the optimization model. Figure 9 shows the
radar graphs of the eight superior indicators before and after the intervention. As shown
in Figure 9, the food and water situation are improved signi cantly after intervention both
in Afghanistan and Egypt. The improvement of food indicator is about 0.183 in
Afghanistan which is especially signi cant. These are excellent achievements because
physiological needs account for the most part of the fragility. At the same time, other
superior indicators like shelter, security and stability also improve a lot in Afghanistan
and Egypt. These will help them deal with the fragility.
(a) (b)
Figure 9: Superior indicators before and after the intervention: (a) Afghanistan;
(b) Egypt.
After these interventions, the fragility indicator of Afghanistan is 0.385, and its fragility
indicator before intervention is 0.288. The fragility indicator increases by 33.7%, but it is
still smaller than the tipping point. Afghanistan is still a fragile country after the
intervention. This is may be caused by the random natural disasters. Natural disasters
would do signi cant harm to the region at many facets. Besides, the total cost of this
improvement is about 57.2 billion dollars, which is three times of Afghanistan GDP. This
is a big challenge for the state. As for Egypt, our intervention can e ectively prevent
Egypt from becoming a fragile state with only 1% of its GDP. The fragility indicator of
Egypt increases from 0.397 to 0.42. This is very close to the tipping point.
5.4 Sensitivity Analysis
Next, we will analyze the sensitivity of the climate change factors: percentage
change of precipitation, arable land and temperature. The initial values of them are
0.2%, 2.7% and 0.1%. We change the value of each factor from 0.005 to 0.2 with the
step of 0.005. When one of the parameters is changing, other two parameters are still
set as the initial value. The proportion of budget in GDP is set as 57.2 billion dollars
for Afghanistan and 3.32 for Egypt.
Figure 10 shows the trend of optimal fragility indicator of Afghanistan and Egypt. The
trends are similar in the two states. We can see that fragility decreases mostly rapidly with
the change of precipitation. This means that our optimization model is most sensitive to
precipitation. Theuctuationof theline representstherandomnatural disasters.


## 第 23 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team # 78511 Page 17 of 21
(a) (b)
Figure 10: Sensitivity analysis of percentage change of climate factor
using the optimization model: (a)Afghanistan; (b) Egypt.
5.5 Suggestions
From the results of our optimization model, we conclude that Afghanistan should
spend 285% of its GDP to prevent fragility and Egypt 1%. The di erence is signi cant. For
Afghanistan, it is almost impossible to prevent fragility in the short run. Therefore, we
suggest the related organizations should help those countries whose fragility indicator is
far lower than the tipping point, like Afghanistan. Otherwise they can hardly escape from
fragility. Speci cally, fragile states should use about one-third of the budget to deal with
food issues and about one-fourth to deal with water issues. As for other aspects, the
speci c investment can be obtained through our optimization model. This model can give
out the optimal intervention to eliminate fragility within a limited budget.
6 Modi cation of Fragility Model
It is worth noted that our model aims to solve the fragility in small or middle countries
like Afghanistan and Egypt. That is because when we consider the possible factors, we
regard the country as a whole and provide factors for sovereign states. However, some
factors need to be modi ed when our model is applied to smaller region like cities or
bigger state like continents. Speci cally, there are three problems for smaller states:
Factors like parties and ethnic is not suitable to smaller states.
Factors like city environment and development indicator should be
considered. The cost of interventions will be lower because of synergy[18] .
Similarly, there are two problems for bigger states like continents:
Climate change impacts will not a ect the state as a whole;
The cost of interventions should be related to the scale of intervention it
implements to;
We will modify our model based on these problems in this section in order to make
our model available to smaller and bigger states.
6.1 Modi cation for Smaller States
Modi cation for smaller states includes two general aspects: factor
reconsideration and cost modi cation.
For superior indicators of physiological need, most of the original factors are still suit-able
except food import. Food import is a general factor for a sovereign state, so it should be
deleted. For superior indicators of safety need, the external intervention and military factors
shouldbe deleted,becausetheyarenot meaningful forcities. Meanwhile, sustain-


## 第 24 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team # 78511 Page18 of 21
ability and exibility should be added to measure smaller states. For superior
indicators of society need, ethnic, uneven development, national debt and party
relationship should be deleted. Economic structure, economic e ciency, subsidy
and public green space should be taken into account. We still use the AHP method
and get weights of the factors for smaller state, which are shown in Table 3.
From Table 3 we can see that the main body of our model is unchanged. The
weights are still similar to Table 1. This guarantees that our model is consistent for
smaller states and normal states.
Table 3: Theweightsof indicators
Physiologicalneed
Food18% Water 18% Shelter 18%
Price26%,Production74% Stress46%,Sanitation26% Houseprice14%,Slums24%
Pollution14%, Reservoir14% Housingarea62%
Safetyneed
Security 15% Stability15%
Refugee25%, Violentconict 48%
Publicorder 11% Population mobility 9%
Terroristattack58%, Crimes31% Sustainalibity13%, exibility6%
Societyneed
Economics5.33% Governance5.33% Demography 5.33%
GDP40%,Unemployment11% Law 5%, Corruption 18% Publicgreenspace17%
Ination 20%,Interest5% Management 34% Education6%, Health10%
Economicstructure17% Subsidy 21% Genderdistribution 10%
Unevendevelopment11% Public support9% Equality 5%, Population 47%
Economice ciency 7% Public services 12% Agestructure5%
The cost of intervention in smaller states such as cities will be smaller because
of the synergy e ect. High population density can improve communication ability
and knowledge sharing so that the cost of intervention will decrease. We use to
measure the synergy e ect and the linear coe cient for smaller states in intervention
cost s can be rewritten as
6.2 Modi cation for Bigger States
The impact area of climate change and the complexity of governance should be
con-sidered for bigger states.
As for the impact of climate change, we mainly focus on natural disasters
because it always occurs to a limited range. Other climate changes like greenhouse
e ect and sea-level rise are global climate change. Therefore, even bigger states
like continents will su er from it as a whole.
We de ne an in uential range index to measure how signi cantly the climate
change impacts this bigger state. Most natural disasters will not too serious and
extreme disaster only occurs accidentally, so we assume the probability function of
the in uential range index f (x) as


## 第 25 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team # 78511 Page19 of 21
In this way, the possibility of serious natural disasters is much lower. The impacts of
disasters for bigger states is determined as
where is the impacts of natural disasters in normal states.
The cost of interventions has nothing to do with the proportion of budget in GDP in
the former model. However, it is impossible for the government to cope with the fragility
of the whole state at a time in bigger states. The e ciency of large-scale investment
coping with fragility will inevitably decrease because of the ability limitation. This is
equivalent of increasing the unit cost of intervention. Generally, the higher the proportion
of budget in GDP is, the bigger the scale of intervention is, and the higher the unit cost of
intervention is. Therefore, the linear coe cient for bigger states in intervention cost b
is determined as
where r is the proportion of budget in GDP.
6.3 Application to Afghanistan and Egypt
We still use the example of Afghanistan and Egypt to apply the modi ed model in
order to compare the model before and after the modi cation. Figure 11 illustrates the
di erences of our three models. The horizontal axis represents the proportion of
budget in GDP, and the vertical axis represents the best fragility level it can reach
under the limitation of current budget.
(a) (b)
Figure 11: Comparison between the original fragility model and the modi ed one:
(a) Afghanistan; (b) Egypt.
We can know from Figure 11 that the general trend of the fragility of smaller states
increases more rapidly than bigger states because of the synergy e ect. The fragility of
bigger states increases very slowly when the budget increases. This is because
continent is too large to manage in the short run. Therefore, trying to improve the fragility
of bigger states in one time is impossible. Figure 11(a) shows that Afghanistan is more
similar to a smaller state. This is in accordance to the reality. Afghanistan is a relatively
small country with about twenty million people. This population is similar to that of Beijing.


## 第 26 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
As for Egypt, it is a relatively large country with ninety million people. Therefore, it is
more similar to the bigger state, as shown in Figure 11(b).
We suggest that the scale of the state should be considered when using our fragility
model. For smaller state, the modi cation of factors and cost should be applied; for
bigger state, the modi cation of the in uential area and cost should be applied.


## 第 27 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team # 78511 Page20 of 21
7 Conclusions
To sum up, we rst establish an evaluation model to measure fragility, and then we
take into account the climate change impacts. The optimization model is used to nd
the intervention to reach the fragile point. Besides, the modi cation of the evaluation
model gures out suitable models for smaller and bigger states. Afghanistan is in the
top ten fragile states list and Egypt is not fragile but vulnerable. They are analyzed
using our model to decide the impacts of climate change on fragility.
The results of our model show that the fragility indicator with climate change is 0.280
for Afghanistan and 0.407 for Egypt. Without the climate change, the fragility indicator
changes to 0.310 for Afghanistan and 0.428 for Egypt. Among the eight superior
indicators, economics indicator will be mostly a ected whose average percentage change
is 14.6%. The tipping point and stable point are determined as 0.428 and 0.711, which
divides the states into three kinds: fragile, vulnerable and stable.
According to the result of optimization, Afghanistan needs to spend 285% of its
GDP and Egypt 1% to avoid fragility. The cost is mainly used to prove the food and
water indicators. After intervention, both states will be less fragile. However, it is hard
for Afghanistan to escape from fragility in the short run.
We reconsider the factors and weights for smaller states and lower the cost of
intervention for them because of the synergy e ect. For bigger states, the in uence
range is considered and the cost is higher because of the di culty in managing. We
nd that smaller states can develop more quickly than bigger states.
8 Strengths and Weaknesses
Strengths
Five di erent normalization methods are used to normalize the inferior indicators.
According to the di erent features of di erent type of indicators, we choose the most
suitable normalization method. This will improve the availability of our models.
The in uence of the natural disaster is generated by the random distribution. We
use Poisson distribution to simulate it. This is a suitable method to measure the
disasters. Compared with others who neglect the disasters, our model can be
more useful.
In the optimization model, the costs of the intervention are set as an increasing
cost. This is more realistic. Because actually the marginal cost of everything is
increasing, our model is more practicable.
In the modi cation of the model, we apply our modi ed model to Afghanistan and
Egypt to test its availability. Results show Afghanistan is similar to a smaller state
and Egypt is similar to a bigger state. This can validate our modi ed model.
Weaknesses
In the K-means Clustering Algorithm, the data from the FSI website is used to
help us nd the tipping point. This may cause some deviations, but this method
can simply our calculation process and bring convenience.
Some of the value of parameters are estimated such as the cost of unit intervention.
This may cause the actual e ect of the budget deviates from the reality, but more speci
c statisticscan becollectedwhen usingour model tosolve thisproblem.
For bigger states, it is better to divide the states into di erent part according to
their geological characteristics. In this way our model can be more accurate.
The further work can be done to improve this aspect.


## 第 28 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team # 78511 Page21 of 21
References
[1] Wikipedia. Frank walter steinmeier. https://en.wikipedia.org/wiki/Frank-/
Walter_Steinmeier.
[2] Stang G Rttinger L, Smith D. A New Climate for Peace: Taking Action on Climate
and Fragility Risks: an Independent Report Commissioned by the G7 Members,
2015.
[3] Vaillant C Chapman N. Synthesis of country programme evaluation conducted in
fragile states. ITAD, 2010.
[4] Mustafa M Q. The responsibility to protect a fragile state: a case study of postin-
tervention afghanistan. Accessed February 12, 2018.
[5] Richard S J Tol. Estimates of the damage costs of climate change. part 1: Benchmark
estimates. Environmentaland ResourceEconomics, 21(1):47{73,Jan 2002.
[6] Richard D S Philip A L. Has australia surpassed its optimal macroeconomic
scale? nding out with the aid of `bene t' and `cost' accounts and a sustainable
net bene t index. Ecological Economics, 28(2):213 { 229, 1999.
[7] McLeod S. Maslow's hierarchy of needs. Simply Psychology, 1, 2007.
[8] Wikipedia. Fragile state. https://en.wikipedia.org/wiki/Fragile_state.
[9] Wikipedia. Shanty town. https://en.wikipedia.org/wiki/Shanty_town.
[10] Toh R S Khan H, Phang S. The multiplier e ect: Singapore's hospitality industry.
Cornell Hotel and Restaurant Administration Quarterly, 36(1):64{69, 1995.
[11] Stefan Rahmstorf. A semi-empirical approach to projecting future sea-level rise.
Science, 315(5810):368{370, 2007.
[12] David G L Carol T W. Modeling the regional impact of natural disaster and
recovery: A general framework and an application to hurricane andrew.
International Regional Science Review, 17(2):121{150, 1994.
[13] Wikipedia. Poisson distribution. https://en.wikipedia.org/wiki/Poisson_ distribution.
[14] National aeronautics and space administration. Global temperatures. https://
earthobservatory.nasa.gov/Features/WorldOfChange/decadaltemp.php.
[15] The gardian. Earth has lost a third of arable land in past 40
years, scientists say. https://www.theguardian.com/environment/2015/dec/02/
arable-land-soil-food-security-shortage#img-1.
[16] Krugman P. Economics. Worth publishers, 2013.
[17] Wikipedia. K-means clustering. https://en.wikipedia.org/wiki/K-means_ clustering.
[18] Wood J. Synergy city; planning for a high density, super-symbiotic society. Land-
scape and Urban Planning, 83(1):77 { 83, 2007.

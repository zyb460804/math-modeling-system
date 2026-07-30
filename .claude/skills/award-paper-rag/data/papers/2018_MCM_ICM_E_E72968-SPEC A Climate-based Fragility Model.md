# E72968-SPEC A Climate-based Fragility Model


## 第 1 页

精品数模资料，各类比赛优秀论文、学习教程、写作模T板ea与m经C验o技n巧tro、l mNautlmabb程er序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
For office use only For office use only
72968
T1 F1
T2 F2
T3 Problem Chosen F3
E
T4 F4
2018
MCM/ICM
Summary Sheet
SPEC: A Climate-based Fragility Model
Summary
Effects of Climate Change have aroused growing attention worldwide. The potential
damages of Climate Change threaten most regions in the world, especially those fragile
states. A fragile state cannot meet its people’s demands, and is quite vulnerable to those
climate shocks. As a result, how to measure the fragility of countries counts.
Our SPEC Model provides a quantitative analysis of fragility degree for most countries
in the world. It considers multiple aspects, including security, politics, economics and Cli-
mate Change.
We use 20 individual indicators to measure each aspects. Considering the impact of
time, we apply Latest-determine Method and Weighted Average Method to do data weight-
ing for different indicators. Moreover, in Weighted Average Method, we use the
exponential weighting pattern to have realistic time-relating weights to better measure the
indicators in a long period.
We divide effects of Climate Change into two parts: General impacts and Extreme im-
pacts. The general part refers to those indirect effects of Climate Change. We use four
indi-cators to represent the influences of rising sea level, decreasing arable lands,
deteriorating ecological environment and restrained water source.
The extreme part of Climate Change illustrates the potential damage of extreme weath-
ers resulting from Climate Change. We apply Self-regulatory Factor to predict countries’
ability to maintain their current condition facing extreme weathers. We use three indicators
to further measure the self-regulatory factor. Moreover, self-regulatory factor also relates
to the Tipping Point of a country, and we put forward the Tipping Model.
We apply Analytic Hierarchy Process (AHP) to determine the weights of indicators. We
refer to different databases such as Worldbank. We simulate our model to 178 countries in
the world, and we work out the self-regulatory factor and SPEC index of each country.
We apply the SPEC model to Yemen, one of the most fragile country and India, a
country with ordinary fragility. We predict the total cost of state driven intervention of India.
In order to make our model more applicable, we use Re-weighting Method to modify
our model. In this way, we find SPEC works well in "smaller" or "larger" states.
Finally, we do sensitivity analysis to the SPEC Model and discuss strengths and weak-
nesses.
Keywords: SPEC Model; Self-regulatory Factor; Weighed Average Method; data mining;
climate impacts; Analytic Hierarchy Process;


## 第 2 页

Team # 72968
精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
SPEC: A Climate-based Fragility Model
February 12, 2018
Contents
1 Introduction 1
1.1 Problem Background . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 1
1.2 Our Efforts . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 1
2 Assumptions 2
3 Nomencalture 2
4 Statement of Our Model 3
4.1 Security . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 3
4.2 Politics . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 4
4.3 Economics . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 4
4.4 Data Weighting Methods for Individual Indicators . . . . . . . . . . . . . . . . 5
4.4.1 Latest-determine Method . . . . . . . . . . . . . . . . . . . . . . . . . . 5
4.4.2 Weighted Average Method . . . . . . . . . . . . . . . . . . . . . . . . . 5
4.5 Climate . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 6
4.5.1 General Climate Impact . . . . . . . . . . . . . . . . . . . . . . . . . . . 6
4.5.2 Extreme Weather Events . . . . . . . . . . . . . . . . . . . . . . . . . . . 8
4.5.3 Self-regulatory factor R . . . . . . . . . . . . . . . . . . . . . . . . . . . 9
4.6 Calculation . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 9
5 Answers to Tasks 11
5.1 Task 1 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 11
5.2 Task 2 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 12
5.3 Task 3 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 13
5.3.1 Tipping Model Based on Self-regulatory Factor . . . . . . . . . . . . . . 13
5.3.2 Application of Our Model to India . . . . . . . . . . . . . . . . . . . . . 14
5.4 Task 4 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 15


## 第 3 页

Team # 72968
精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
5.4.1 Predict the total cost of intervention . . . . . . . . . . . . . . . . . . . . 16
5.5 Task 5 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 16
5.5.1 Larger "states" . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 17
5.5.2 Ex-State model . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 17
5.5.3 Dealing with missing data . . . . . . . . . . . . . . . . . . . . . . . . . . 17
5.5.4 Smaller "states" . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 18
5.5.5 Re-weighting for SPEC index . . . . . . . . . . . . . . . . . . . . . . . . 18
5.5.6 Examples: Guangzhou and Cape Town . . . . . . . . . . . . . . . . . . 18
6 Model Analysis 19
6.1 Sensitivity Analysis . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 19
6.1.1 Impact of Mediate Constant a in Weighted Average Method . . . . . . 19
6.1.2 Impact of Universal Extreme Weather Probability p% . . . . . . . . . . 20
6.2 Strengths & Weaknesses . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 20
6.2.1 Strengths . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 20
6.2.2 Weaknesses . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 20
7 Conclusion 20
Appendices 22
Appendix A SPEC Indexes Results 22
Appendix B Analytic Hierarchy Process 23
Appendix C SPEC Model Data Mining Algorithm 24
Appendix D SPEC Model Final Calculation Algorithm 30
Team #72968 Page1 of 20
1 Introduction
1.1 Problem Background
It is always an interesting experience in winter seeing passengers taking off their
sweaters and heavy coats on the plane flying from north to south. Obviously, climate
influence our life-style. Moreover, nowadays it significantly impact the stability, or saying
conversely, the fragility of a country.


## 第 4 页

精品数模资料，各A类 f比ra赛g优ile秀 s论ta文t、e 学is习 a教 l程ow、-i写nc作o模m板e 与co经u验nt技ry巧 c、hmaartalcatbe程ri序ze代d码 b资y 料w等ea，k尽 s在ta淘te宝 c店a铺pa：c闵ity大 a荒n工d/科or男 的杂货铺！
weak state legitimacy leaving citizens vulnerable to a range of shocks [1]. A state’s fragility
interplays with its social conditions and they can easily fall into a viscous cycle once one of
the indexes becomes severe. Therefore, people often examine fragility to view as a
compre-hensive reflection of a country’s conditions.
There are multiple ways to measure the fragility of a country. The existing fragility lists
such as Fragile States Index [2] of Fund for Peace [3] put more focus on social indicators
re-garding politics, safety, economy, etc.. However, they almost neglect natural indicators
such as climate shocks and global climate changes, whose influences have become
remarkable today. Here we use "almost" to assume their weighting systems, considering
climate to have minor impacts on fragility by indirectly affect the core indexes including
security political, economical indicators.
1.2 Our Efforts
To specify the climate impacts on fragility, we build a climate-based fragility model
called the SPEC Model, which is able to analyse the impact of climate both directly and
indirectly. In the model, we also quantify other important indicators concerning security,
politics and economics.
In Section (2), we state the basic assumptions of the SPEC Model. In Section (4), we
give detailed explanation and calculation for each indicator used in the model. Section (6)
provides thorough analysis of the SPEC Model including sensitivity analysis and strengths
& weaknesses review.
We also solve tasks listed as follows,
1. Build a model to determine the fragility of a country and analyse the influence of cli-
mate.
2. Apply our model on one of the top 10 most fragile states and quantify the impact of
climate on fragility.
3. Apply our model on another state outside the top 10 most fragile list. Find distinct
indicators and tipping point of its fragility trend.
4. Use our model to predict positive interventions to reduce negative impact of climate
and avoid a fragile state.
5. Generalize our model on states of different sizes, small as cities, large as continents.


## 第 5 页

精品数模资料T，ea各m类#比7赛29优6秀8论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，P尽ag在e淘2宝of店2铺0：闵大荒工科男的杂货铺！
2 Assumptions
We make the following assumptions for the SPEC Model:
1. States can exchange resources and communicate with neighbouring states.
2. Within a country, resources can be dispatched quickly from rich places to poor areas,
especial when some parts of the country are suffering natural catastrophe.
3. The stability and strength of a country is largely depend on the political environment,
economical conditions, social security, military power, national resources, etc..
4. The richness of national resources can be reflected by national territorial area.
5. Risk of extreme weather events increases with global climate change [4].
3 Nomencalture
The name for our climate-based fragility model SPEC is the combination of four first
letters of Security, Politics, Economics , Climate. These four parts are our focus in the
fragility measurement model.
We use the notation in Table 1 to present the indicators in equations of our SPEC Model.
Notations used only once is not included in Table (1), they are introduced in certain sections.
Table 1: Notation
Symbol Definition
Security SyntheticSecurityIndicator
S
Social conflicts
conf
S Political stability & Absence of violence
abs
S Incidence of coups
coups
S Gross human rights abuses
abuse
S Refuge & Territory
ref
P olitics Synthetic Political Indicator
P
Government effectiveness
gov
P Rule of law
law
P Control of corruption
corpt
P Voice & Accountability
acc
Economics Synthetic Economical Indicator
E
Gross national income (GNI) per capita
GNI
E Growth of domestic product (GDP)
GDP
E Inflation
inf
E Income inequality
ineq
E Regulatory quality
reg
Climategen Climate indicator for general global climate change
C Population living in areas where elevation is below 5 meters
elv
C Forest area
frst
C Arable land
ara
C People using basic drinking water service
drk
Climateext Climate indicator for extreme weather events
R Self-regulatory factor
SPEC
the intergrated SPEC Model score
score
Team #72968 Page3 of 20


## 第 6 页

精品数模资料4， 各类S比t赛at优e秀m论e文n、t学 o习教f 程O、u写r作 M模o板与d经e验l 技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
In assessment of the fragility of a country, a state, or a city, we refer to multiple factors.
We classify the factors into four main fields: politics, economics, security and climate.
Factors in distinct fields contribute to fragility in different ways. We introduce the
quantification of impact from various factors field-by-field.
Figure 1: SPEC Index
4.1 Security
We use five security indicators in security fields. These five indicators measure the
pres-ence of different types of political violence in a country, from civil war to gross human
rights violations on a scale of 0 (smallest) to 10 (greatest).
Social conflicts is an indication of the state’s ability to maintain peace within its bor-
ders and provide basic physical and human security. We refer to the data set Major
Episodes of Political Violence 1946-2016 that comprises a comprehensive
accounting of all forms of major armed conflicts in the world.
Political stability and absence of violence measures the perceptions of the likeli-
hood that the government will be destabilized or overthrown by separatism or violent
means, including terrorism.
Incidence of coups. States that have experienced violent overthrow are by definition
highly unstable, and likely to lack the political mechanisms that ensure peaceful tran-
sition of power. For this indicator, a country score 0 if there have been any coups in
the last fifteen years and score 10 if else. We acquire the data from List-of-coups on
Wikipedia.
Gross human rights abuses. States that rely on widespread oppression to maintain
control will be susceptible to internal discontent and instability. We assign a score for
this indicator based on Political Terror Scale 2015.
Refugee & Terrorism is the best available indicator for a state’s ability to carry out its
sovereignty and maintain a monopoly on the use of armed force across the entirety


## 第 7 页

精品数模资料T，ea各m类 #比 7赛29优6秀8 论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，P尽ag在e淘 4 宝of店 2铺0：闵大荒工科男的杂货铺！
of its territory. Large numbers of refugees emerge in those countries which can not
quell the revolutionary and ethnic wars started by challengers seeking major changes
in their status.The database is provided by Political Instability Task Force, 2017.
The mathematical expression for security indicators in the SPEC Model equation has a
form of
We will later assign weights 1, 2, 3, 4, 5 totheseindicatorsinSection(4.6).
4.2 Politics
We used four political indicators to quantify the impact of politics on fragility of a
state. We define the four indicators to reflect the political appearance of a state to the
same large extent and ignore other minor factors. We treat the four political indicators
equally by grad-ing the them from 0 (smallest) to 10 (greatest) in the fragility function.
Government effectiveness directly shows the states’ govern capability, including
the public and civil service quality and policy executive ability. Facing with social
crisis, a government’s coping ability impacts the results greatly.
Rule of law measures the confidence and efficiency of a government to build a legiti-
mate country using strong regulations, and relate tightly to the long-term stability of a
state.
Control of corruption prevents the state from irrational resource distribution and in-
stitution erosion, which is a strong indicators to predict a state’s public trust.
Voice & Accountability measures the extent of citizens get involved in the construc-
tion of a government. It is the reflection of civil freedom and influence the stability of a
government in the long-term.
In assessment of political indicators, We refer to the data set Governance Matters VI, 2007
on the World Bank. The mathematical expression for political indicators in the SPEC
Model equation has a form of
where 1, 2, 3, 4 are given in Section (4.6).
4.3 Economics
There are five economical indicators. These widely used indicators allow us to capture
key aspects of national economic performance.


## 第 8 页

精品数模资料，各类G比ro赛s优s 秀Na论ti文on、a学l I习nc教o程m、e (写G作NI模) p板e与r 经Ca验p技ita巧 . 、 W m e a b tl e a li b e 程 ve 序 l 代 ow 码 p 资 er 料 c 等 ap ， it 尽 a i 在 nc 淘 om 宝 e 店 i 铺 s a ： p 闵 ro 大 x 荒 -im 工 a 科 te 男 的杂货铺！
effect of state weakness, circumscribing a country’s capacity to achieve essential
government functions. The database is provided by World Development Indicators, 2007.


## 第 9 页

Team # 72968 Page 5 of 20
精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Growth of Gross Domestic Product (GDP). Like GNI per capita, average economical
growth can be both a resulting effect and proximate cause of state weakness. Coun-tries
that manage to sustain economical growth generally exhibit relatively stable and secure
societies. The same data set is available at The World Bank.
Inflation may indicate an economy’s susceptibility to external shocks or
unsustainable fiscal policy. We use the absolute value of the annual change in
consumer prices, al-lowing us to treat cases of deflation and inflation in the same
manner. World Economic Outlook Database, 2017 provides the data required.
Income Inequality. High income inequality has been linked to the likelihood of re-
bellion and other forms of political violence. We determine the score of each country
based on its Gini coefficient which represents the wealth distribution of a country’s
residents.
Regulatory Quality. Poor Regulatory Quality indicates a state’s inability to foster an
environment conducive to private-sector growth, which is essential to increasing na-
tional income. Governance Matters VI, 2007 provides the data required.
The mathematical expression for political indicators in the SPEC Model equation has a
form of
We will later assign weights 1, 2, 3, 4, 5 to these indicators in Section (4.6).
4.4 Data Weighting Methods for Individual Indicators
We search for the data of the indicators in security, political and economical fields and
operate the mass data with two fundamental methods: weighted average methods and
latest-determine methods, and then we apply the operated indicators into the equation of
fragility.
4.4.1 Latest-determine Method
Indicators acts differently to the fragility of a country, some of them has abrupt and sudden
impact, while others has on-going influence. We apply the latest-determine method
on indicators that has sudden and short impact, and only use the latest data to
represent the indicator.
Among all 14 indicators introduced in the previous three fields, we use this latest-
determine method on 9 of them, regarding them as instantaneous and transient factors. For
only 5 in-dicators mentioned in the next part, we use the weighted average method to
measure their relatively long-standing impact.
4.4.2 Weighted Average Method
We apply an exponential weighing pattern, showing the impact of a indicator decreases
T
with time. We define the relative weight (1 a) , where T is the time number in the time


## 第 10 页

精品数模资料p，e各rio类d比fa赛ll优in秀g论be文tw、e学e习n教th程e、in写te作g模er板s与fr经om验技1巧to、m5atolrab1程序to代1码5,资a料n等d，a尽is在淘a宝m店ed铺ia：te闵大po荒si工tiv科e男的杂货铺！
constant that falls in the interval [0; 1].


## 第 11 页

Team # 72968 Page 6 of 20
精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
A mediate constant a = 0:15 implies the weight decreases by 15 percent when we
move back in time each year. Though the mediate constant a in the equation of
relative weight can be a arbitrary constant in [0; 1], the value of a = 0:15 is rational to
quantify the impact variation with time goes by.
Time range of 5 years or 15 years are reasonable enough for the impact of indicators,
when T with 15 year range measures long and continuous impact and 5 year range
measures relatively small and continuous impact.
Then we scale the relative weight to make the sum equals to 1 and get the result of
absolute weight that used in our method of averaging.
where we define a = 0:15 and T = 5; 10.
Parameter Scheme for Indicators: We use the weighted average method to process the
data of 5 indicators. Three indicators belong to security category: social conflicts, incidence
of coups, human rights abuse. Two indicators belong to economy category: Growth of
Gross Domestic Product (GDP), Inflation.
We assign 15 year time span for social conflicts, incidence of coups; 5 year time
span for human rights abuse, GDP and inflation. A country suffering social conflicts
and incidence of coups need a relatively longer time to recover from the mighty and
widespread social destruction. Under this condition, there are still repercussions with
decreasing impact to make a country fragile. We assign 5 year time span for human rights
abuse since it is a more flexible indicator, which can be easily changed by policy or other
instant law. GDP and inflation measures the economic appearance of a country. Since
economic event happen frequently in modern world and their effects do not vanish
instantly, we assume the latest 5 year data forecast the present economy.
4.5 Climate
We consider two aspects of climate impact on fragility of a state. General climate im-
pact indicator measures the impact under global climate trend such as global warming
and glacier melting. The general impact are largely determined by the state’s dependence
on agriculture, water source and its location (risk of being submerged by rising sea level),
etc. Extreme weather condition indicator measures the possibility of a country to
become frag-ile faced with natural catastrophe. It relates tightly with the state’s possibility
of suffering a natural disaster and resistance of destruction.
4.5.1 General Climate Impact
From 1990s, people become more clear about the negative trend of climate and put
more efforts on researches and control of the global climate change. Results of climate
change including increased droughts, shrinking glaciers and other ecological problems,
are blocking the development of many countries.


## 第 12 页

精品数模资料T，ea各m类 #比 7赛29优6秀8 论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，P尽ag在e淘 7 宝of店 2铺0：闵大荒工科男的杂货铺！
In this section, we employ four indicators to quantify the general climate impact on a
country caused by the current global climate trend.
We process the raw data and normalize the values of four indicators to fall in a range
from 0 to 5, and then give them different weights in the SPEC Model equation.
Population living in areas where elevation is below 5 meters (% of total population)
Population living in areas where elevation is below 5 meters (% of total population)
shows the risk of a country to become fragile faced with global warming and glacier
melting. Once the sea level rises, and if a country has a large population living in the
place with elevation lower than 5 meters, the residential condition in the country will
meet with crisis. We calculate the indicator result as Equation (2), showing that more
population living in areas where elevation is below 5 meters, smaller the value of the
indicator is, and more fragile the country is.
where
– Celv is the normalized result of the indicator ranging from 0 5.
– Delvis thepopulation percentagein thesourcewhich rangingfrom 0 56:18.
Forest area (% of land area)
Forest area reflects the animal and plant ranges and is a measurement of species
rich-ness. A larger forest area build a more stable and adaptable ecological
environment when a state faced with climate change. We calculate the forest area
indicator value in SPEC model using Equation (3), showing faster the growth of forest
land, higher the indicator value is, and less fragile the country is.
– Cfrst is the normalized result of the forest area indicator ranging from 0 5.
– Dt;frst is theforest areapercentagein thelatest year sourcerangingfrom 0 73:1.
– DT;frst is theforest areapercentagein thereferenceyear.
Arable land (% of land area)
Frequent draughts and floods nowadays are the result of climate change and they
diminish the area of arable land. Observing the change of arable land we can predict
a country’s resistance towards climate change. Equation (4) calculate the arable land
indicator value in the SPEC model, showing lower the decreasing speed of arable
land area, higher the arable land indicator value is, and less fragile the state is.
– Cara is the normalized result of the forest area indicator ranging from 0 5.
– Dt;ara is thearableland areapercentagein thelatestyear sourceranging from


## 第 13 页

精品数模资料，各类比赛优0秀5论6文:1、75学.习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
– DT;ara is thearableland areapercentagein thereferenceyear.


## 第 14 页

Team # 72968 Page 8 of 20
精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
People using basic drinking water service (% of population)
Global climate change give rise to the possibility of floods and droughts. Draughts
especially, threaten the daily water supply for residence. Water resource is also one
of the core inducement of region conflicts. Change of the population using basic
drinking water service measures the state’s dependence on water. We use Equation
(5) to calcu-late the drinking water indicator in the SPEC Model. If the population
using drinking water service rises with time, the state depends less on water
resource and thus less on climate, and appears less fragile.
– Cdrk is thenormalized result of thedrinkingwater indicator rangingfrom 0 5.
– Dt;drk is the drinking water service population in the latest year source ranging
from 0 100.
– DT;drk is thedrinking water service populationin thereferenceyear.
On the basis of accessible data, we use different ways to process the data and let the
indexes fall in the value interval [0; 5]. Then we weigh the indexes '1, '2, '3, '4 and get the
value of general climate impact indicator as Equation (6).
4.5.2 Extreme Weather Events
There is little doubt that the Earth’s climate is changing and weather is becoming more
extreme. Future warming will bring more dangerous condition, even if the world manages
to keep temperature rises within a 2 C limit to which governments have committed. The
state’s ability to cope with extreme weather has shown an increasing role in safeguarding
economic and social stability. The full formula for country scoring in extreme condition is
given by
where
– p% is the universal probability of extreme weather. At current time, it’s
reasonable to set the value of p to 5%.
– CO2t is national CO2 emissions(kt) that year.
– CO2T is national CO2 emissions(kt) in year 1990.
– R refers to self-regulation factor. It is originally a measure of the stability of the
ecosystem and here it indicates country’s ability to effectively carry out disaster
relief and disaster prevention work. This factor is synthesized from three parts
which we discuss later.
Extreme weather events is of small probability, but can be catastrophic. In the process of
increasing overall national strength, the state’s response capability to extreme weather con-
ditions is also on the rise. However extreme heatwaves and heavy rain storms are already
happening with increasing regularity worldwide because of man-made climate change.
There-fore a proportional item CO2t/CO2T is of necessity in the formula to indicate the
increasing difficulty of disaster relief and the increase of probability.


## 第 15 页

Team # 72968 Page 9 of 20
精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
4.5.3 Self-regulatory factor R
Self-regulatory factor R is synthesized from three parts: national land area, per capita
income, security. The self-regulatory factor r is determined by Equation (8).
where s(n) is national land area, s(USA) is the land area of America. For Russia and
Canada, whose land area is bigger than America, we set its r1 to 1 to avoid inaccuracy.
i(n) is per capita income, and i(L) is the per capita income of Luxembourg. According to
World Bank, Luxembourg’s per capita income ranks first in the world. Security score is
already obtained, we divide it by 50 to have the value fall in the range of zero to one.
Security factors is the basic guarantee for dealing with extreme weather events. Rela-
tively large land area enhance disaster prevention capabilities to some extent for its rich
resources and manpower. Per capita income is the embodiment of the current economic
strength that support disaster prevention and relief work.
4.6 Calculation
The score of the SPEC Model measures the fragility of a state. Higher scores show less
fragility while lower scores show more fragility. The SP ECscore has the equation form as
Equation (9) shows the relation between the SPEC score and indicators of four core fields
regarding fragility: security, politics, economics and climate, where climate consists of gen-
eral climate change and extreme weather condition. The five security indicators, the four
political indicators, the five economical indicators and four general climate indicators have
positive correlation with the SPEC score. Bigger the value of the indicators, bigger the
value of the SPEC score and less fragility of a state.
We only put the indicators considering extreme weather condition in the denominator,
showing the negative correlation with the SPEC score. Bigger the value of extreme
weather indicator, smaller the value of the SPEC score and more fragile of a state.
Wespan the item of Climateext referring to Equation (8), since its calculation differs from
the other four items in the numerator of Equation (9).


## 第 16 页

精品数模资料w，h各er类e 比th赛e优 s秀el论f-r文eg、u学la习to教ry程 fa、c写to作r 模R 板h与as经 t验he技 d巧e、tamilaetdla bfo程rm序 代o码f E资q料ua等ti，on尽 (在1淘1)宝 w店it铺h ：co闵e大ffi荒cie工n科ts男 的杂货铺！
determined by AHP. The analytic hierarchy process (AHP) is a structured technique for
organizing and analyzing complex decisions, based on mathematics and psychology [5].
Team #72968 Page10 of 20
We prioritize the indicators and employ AHP to get the coefficients for every indicator. Re-
sults are listed in Table (2).
Table 2: The weight of indicators
Indicators weight (%)
Social conflicts 20.69
Political stability and absense of violence 17.24
Incidence of coups 27.59
Gross human rights abuses 10.34
Refugee 24.14
Governmenteffectiveness 25.00
Rule of law 25.00
Control of corruption 25.00
Voice & Accountability 25.00
GrossNationalIncome(GNI)perCapita 25.93
Growth of Gross Domestic Product (GDPïijL’ 29.63
Inflation 11.11
Income Inequality 18.51
Regulatory Quality 14.86
Populationlivinginareaswhereelevationisbelow5meters 11.31
Forest area 35.43
Arable land 22.61
People using basic drinking water service 30.65
Then, We have precise Equations (12) to calculations each indicator, and plug them in
Equation (9) to get the SPEC score. We conclude the results in Figure (2).
Security =(20:69%)Sconf + (20:69%)Sabv + (20:69%)Scoups + (20:69%)Sabuse +
(24:14%)Sref P olitics =(25:00%)Pgov + (25:00%)Plaw + (25:00%)Pcorpt + (25:00%)Pacc
Economics =(25:93%)EGNI + (29:63%)EGDP + (11:11%)Einf + (18:51%)Eineq + (14:86%)Ereg
Climategen =(11:31%)Celv + (35:43%)Cfrst + (22:61%)Cara + (30:65%)Cdrk
(12)


## 第 17 页

Team # 72968 Page 11 of 20
精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Figure 2: World map for SPEC score. Higher score means means a state less fragile, and
lower score means a state more fragile.
5 Answers to Tasks
5.1 Task 1
We use the SPEC Model to determine the fragility of a state. Fragility classification de-
pends on the value of the SPEC score. SPEC score falls between 0 to 27 belongs to
fragile category; SPEC score falls between 27 to 50 belongs to vulnerable category; SPEC
score falls between 50 to 70 belongs to stable category.
Table 3: Fragility classification.
SPEC score Fragility
[0; 27) Fragile
[27; 50) Vulnerable
[50; 70) Stable
To measure the climate impact on fragility, we evaluate the values of Climateext to
see direct impacts and Climategen to analyse indirect impacts.
Climateext measures the intensity of direct extreme climate impacts. According to
statical data generated by the SPEC Model, Climateext larger than 2:70, indicating a
state’s extreme weather conditions impacts the fragility to a great extent. Climateext
between 2:00 and 3:70 is normal. Climateext below 2:00 means the state has little impact
from extreme weather conditions.


## 第 18 页

精品数模资料T，ea各m类 #比 7赛29优6秀8 论文、学习教程、写作模板与经验技巧、matlab程序代码资料等P，a尽ge在 1淘2 宝of店 2铺0：闵大荒工科男的杂货铺！
Climateext is influence by two main factors: i) self-regulatory factor R: R below 0:60 means
a country is not capable of fighting extreme climate impacts and existence of extreme weather
lead to more fragility; 0:60 to 0:75 is the normal range; R above 0:75 means a country is very
powerful to cope with extreme weather, and acts less sensitive to destruction of ex-
tremeclimate.ii)probabilityofextremeweatherevents lnCO
2t
p,whichisinfluenceby
CO2T
the emission of the greenhouse gases. CO2 emission index larger than 0.80 is a serious
phe-nomenon saying that a country is having too much CO2 emission to promote the
possibility of having extreme weather and thus increase its fragility.
Climategen measures the indirect impacts of climate. According to SPEC Model statistical
data, Climategen above 5:00 is having large indirect impact of climate by affecting other in-
dicators in security, political, economical fields. Climategen between 3:00 and 5:00 is normal.
Climategen below 3:00 appear to have little indirect impact from climate change.
5.2 Task 2
We choose Yemen to discuss its fragility causes. Yemen ranks seven in our SPEC
fragility list, which agrees well with its rank in the fsi list.
Figure 3: yemen
The direct climate indicator Climateext = 2:83 is larger than 2:70, which means the fragility
of the country is greatly influenced by the extreme climate events. The reason be-hind is that
Yemen has a low self-regulatory factor R = 0:60, indicating its poor resistance before natural
catastrophe. R made up of an item r3 = security=50, and since there are so-cial conflicts and
coups inside the country, Yemen owns a poor ability to recover itself once encounter climate
shocks. Extreme climate conditions can easily drive Yemen to be fragile.
The indirect climate indicator Climategen = 3:67 is a normal value for according to
SPEC’s statistical data. Therefore, it contributes little to Yemen’s fragility.
How to be less fragile
Improve political conditions and stop coups.
Improve security conditions by stopping social conflicts.
Live in harmony with the neighbouring countries to help when faced with climate
problems.


## 第 19 页

Team # 72968 Page 13 of 20
精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Increase self-regulatory factor to promote the state’s capability to cope with extreme
climate events.
5.3 Task 3
As is shown above, Climate Change effects a country’s fragility from two aspects, in-
cluding general part and extreme part. As we have mentioned, the general part refers to
the indirect impacts of Climate Change. According to available sources, we find indirect
impacts only has slight influence on the fragility of a country in a short period.
Therefore, we conclude that the general part effects the fragility in a long period. That
period will be at least twenty-year-scaled. In this case, we mainly consider the impacts of
the extreme part when measuring the fragility of a country.
5.3.1 Tipping Model Based on Self-regulatory Factor
From the above conclusion, we find that Climate Change pushes a country to become
more fragile mostly via its extreme part. According to what is discussed in the Model Sec-
tion, we come to determine the definitive indicators.
Figure 4: Definitive indicators of impacts of Climate Change.
Since the situation of CO2 emissions of a country is limited to its current technology
and has close relation to its future development, it might be steady in a long term. So our
major work is to discuss the self-regulatory factor.
Moreover, we use our SPEC data calculated above to see the relation between SPEC
index and the self-regulatory factor.
Figure 5: Relation of SPEC Index


## 第 20 页

精品数模资料T，ea各m类 #比 7赛29优6秀8 论文、学习教程、写作模板与经验技巧、matlab程序代码资料等P，a尽ge在 1淘4 宝of店 2铺0：闵大荒工科男的杂货铺！
From the Figure (7), we find that SPEC index and the self-regulatory factor has a
beautiful linear relation. When the self-regulatory factor increases, the relevant SPEC also
increases. This relation confirms our assumption and discussion above.
Since the self-regulatory factor measures the ability of countries to maintain their
current condition facing extreme situations, it is valid for us to put forward a Tipping
Model based on Self-regulatory Factor.
From the relation between SPEC index and self-regulatory factor, we have the
following definition:
Tipping Point: The Tipping Point of a country is the time when its self-regulatory factor
decrease to reach the very value 0:6, and becomes lower.
Due to the indicators self-regulatory factor use, it well illustrates slight changes of secu-
rity, political, economical conditions of a country under Climate Change. When the value of
self-regulatory factor is smaller than 0:6, it is impossible for those countries to keep them
safe from extreme climate shocks. Also, from the results of our model above, we find that
such countries with small self-regulatory factor mostly are fragile, and some vulnerable.
This shows our definition of Tipping Point is quite reasonable.
5.3.2 Application of Our Model to India
Figure 6: India
From Figure (7) , we have the following conclusions:
India is a vulnerable country.
Politics in India is stable, but not strong.
India exists gross human rights abuses, especially to females.
Due to the geographical position of India, large amount of population of India living in
areas where elevation is below 5 meters face the severe threaten of rising sea level.
The yearly rising CO2 emissions put India at higher risk of extreme weathers.
Although India has self-regulatory factor 0:735, it is at quite high risk facing extreme
weathers as a result of Tropical Monsoon Climate.
Therefore, India is becoming more vulnerable to extreme weathers. If India do not take
effective measures to solve gross human rights abuses, India may face more social conflicts,


## 第 21 页

Team # 72968 Page 15 of 20
精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
which negatively affect economics and security of India. This adverse trend will bring down
the self-regulatory factor of India, and India might reach the Tipping Point in a short period.
5.4 Task 4
According to SPEC Index, climate change has direct and indirect effects on states’
stabil-ity. Initiatives is needed to deal with these two aspects respectively.
Our eight proposed state driven interventions for India is in appliance with the climate
indicators in SPEC Index.
For general climate impact:
Set strict control over the rezoning of cultivated land during urbanization.
Promote agricultural transformation and upgrading, increase water use efficiency and
equity.
Develop desalination technology.
Carry out old town renovation and reasonably increase the urban density. Urban
plan-ning has to focus on tall buildings.
Increase the income of the forestry sector, focus on the renewal and reforestation of
natural forests and reduce artificial forests of single tree species.
For extreme weather events:
Promote accurate poverty alleviation and attach more importance to the consistency
of poverty alleviation policies.
Strengthen infrastructure construction in rural areas and promote housing safety for
lower-class residents.
Add medical expenses to local health insurance plan and focus on reducing under-5
deaths rate.
These initiatives closely respond to the impact of general climate factors as follows.
1. According to the World Bank collection of development indicators, arable land in India
was reported at 156463000 ha in 2015,about 500,000 hectares less than year 2004. To
deal with dwindling arable land, India must set strict control over the rezoning of
cultivated land. Land other than agricultural use needs to be more efficiently utilized.
2. Faced with increasing population, density in residential neighbourhoods has to be in-
creased by decreasing lot sizes and replacing old houses with town-houses.
3. Report[6] claimed that India’s population is growing faster than its ability to produce
rice and wheat. To feed its growing population, India should raise its farm productiv-
ity by reducing food staple spoilage and improving its infrastructure.


## 第 22 页

Team # 72968 Page 16 of 20
精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
4. Affected by the southwest monsoon, grain output fluctuates every few years. From
1999 to 2005, the minimum grain output reached 1.74 billion tons, the highest at 213
million tons, a difference of 390 million tons [7]. Thus, under the influence of
continued climate change, the pressure on food security in India is likely to increase.
5. India has already carried out Forest regeneration program, but many are single-
species plantations. Large-scale afforestation in degraded forest areas, including
monoculture, can not create the ecosystems and biodiversity needed for abundant
animal and plant ranges [8].
6. In 2015, implementation of a universal health care system was delayed due to bud-
getary concerns. Penetration of health insurance in India is low by international stan-
dards and most healthcare expenses are paid out of pocket by patients and their
fam-ilies, rather than through insurance [9]. The add to the vulnerability of low-class
resi-dents facing extreme weather events.
5.4.1 Predict the total cost of intervention
It’s quite diffcult to accurately predict the expenses these measures for India required. We
first determine the field to these measures belong and refer to The Expenditure of Government
of India 2016-2017 to get access to the government’s total spending in this area.
Then we compare and estimate the ratio of expenditures on this measure to major
items in this area. The estimated expenditure of our 8 proposed intervention is listed below.
(Unit: hundred million dollars)
Table 4: Estimated expenditure of each intervention
Intervention Expenditure
Control of rezoning 18.7
Agricultral upgrading 77.9
Desalination 50
Rural renovation 1558
Forestry sector 20
Poverty alleviation 468
Housing safety 1000
Healthcare 100
5.5 Task 5
We notice that only a few countries cover extra large land areas equivalent of
continents. If measured by population, countries that own 20 million to 50 million people is
equivalent to the scale of a medium-sized city and only 25 countries is under that size.
When coming to smaller states and larger states, to be more mathematically precise, we
have to adjust the coefficient of our SPEC Model.
What’s noteworthy is that it’s never merely the change in land area, indicators in
security, politic and economic fields are all affected.


## 第 23 页

Team # 72968 Page 17 of 20
精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
5.5.1 Larger "states"
To obtain a modification of SPEC Model, a ex-State model is required. The following
facts need special consideration.
Big countries have more human and energy resources and can be fully deployed dur-
ing times of emergency.
As a combination of countries, continents have inherent advantages in developing re-
silient and flexible policy-making. All regions have a higher degree of coordination
and complementarity of policies when faced with unrest.
Policy silos are more impossible to exist, it is essential rearrange evaluation system in a
broader context of education, healthcare, good governance, and societal resilience.
5.5.2 Ex-State model
As noted above, we already have each country’s score on fragility and now we need to
weight each of them. The scoring formula is
where
– Fcop is the fragility of the hole continent.
– Fi is the fragility of the hole continent.
– Ri is the earlier determined self-regulation factor of each country.
Notice that countries rank high in SPEC fragility index has high likelihood of future political
and economic instability. In broader view, these countries take on more responsibility in
face of difficulties. Therefore we determine the expression of continent’s fragility by a
weighted average expression. This approach is concise and effective.
5.5.3 Dealing with missing data
Though our SPEC indicators have relatively good data coverage worldwide, there are
missing data points. In this ex-State model where multiple area needs to be included, we
don’t filling these data gaps with imputed estimates.
Instead we calculate with available country data using the formula above. Our rationale
is that neither the accuracy of the overall continent weakness score, nor the credibility, are
significantly affected by the missing data. Furthermore, most countries have data for all
SPEC indicators.There is a risk that imputed data would amount to an implausible
estimate of a country’s performance on certain indicators.


## 第 24 页

Team # 72968 Page 18 of 20
精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
5.5.4 Smaller "states"
Cities have less industrial diversity and abundance of resources compared with states.
here we explain how to rearrange the weight of each SPEC fields.
The following facts need special consideration.
With globalization providing a net benefit to nations around the world, regions are
linked closer with each other.
The city’s basic climatic conditions can be obtained from the country’s data.
Each city has its own major industry which reflect the city’s overall strength and sig-
nificantly affect its vulnerability to economic fluctuations and climate events.
5.5.5 Re-weighting for SPEC index
Here are the principles for re-weighting.
1. Four general climatic indicators apply to both cities and states, therefore, scoring for-
mula for general climte conditions doesn’t change.
2. As explained earlier, scoring formula for extreme climate condition consist of extreme
weather events(EWE) probability, CO2 emission and self-regulatory factor(R). EWE
probability doesn’t change with land area size. R is determined by the same formula
expressed earlier and CO2 emission is available in data set.
3. The weight for security(S),politic(P) and economic(E) fields is rearranged using Ana-
lytic Hierarchy Process based on city’s major industry.
5.5.6 Examples: Guangzhou and Cape Town
We take Guangzhou and Cape Town as examples to reweight its SPEC index in
compli-ance with principles above.
Guangzhou is the capital and most populous city of the province of Guangdong in
southern China. Its urban development characteristics is embodied in following areas.
– main manufacturing hub of one of mainland China’s leading commercial and
manufacturing regions
– rivers and streams improve the landscape and keep the ecological environment
of the city stable
– top ten container ports in the world
Cape Town is the legislative capital of South Africa. Its urban development
character-istics is embodied in following areas.
– noted for its architectural heritage and natural setting, once named the best
place in the world to visit
– serves as the regional manufacturing centre


## 第 25 页

Team # 72968 Page 19 of 20
精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
– Encountering freshwater crisis, affecting sustainable development
With careful consideration of each field, the new SPEC coefficient is determined
through AHP method.
Figure 7: Rearranged weight for small "states"
6 Model Analysis
6.1 Sensitivity Analysis
The SPEC model contains several constant parameters. We referred to on-line
database and various accessible literature when deciding on the parameters. In this
section, we test and sensitivity of the SPEC Model by changing the values of the
parameters to show its reliability.
6.1.1 Impact of Mediate Constant a in Weighted Average Method
Figure 8: Weight variation with time span for different a.
We set a to be 0:15 and never changed again in when using weighted average method to
give weight of every indicator. We choose constant 0:15 based on the same calculations in
Index of State Weakness In the Developing World [10]. In Figure (8), we have value of a to
vary from 0:10 to 0:20 by 0:25. Every curve representing a certain value of a shows the same
trend. Therefore, the SPEC Model is not sensitive to the value of mediate constant a.


## 第 26 页

Team # 72968 Page 20 of 20
精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
6.1.2 Impact of Universal Extreme Weather Probability p%
6.2 Strengths & Weaknesses
6.2.1 Strengths
The SPEC Model uses accurate and latest databases to guarantee the reliability of re-
sults. The results have high reference value and can be applied in real life immediately.
We employ 19 indicators of 4 fields in the SPEC Model to measure the fragility of a
state. In this way the SPEC Model is able to avoid abrupt influence of a single
indicator, and the results are more integrated.
We apply two kinds of data weighting methods (Latest-determine Method and
Weighted Average Method), according to the characteristic of the indicator, making the
SPEC Model more scientific.
We explore the climate indicators and divide the impacts into indirect ones and direct
ones. Calculations on items of climate indicators is straightforward quantifications of
their impacts on fragility.
6.2.2 Weaknesses
We neglect some indicators such as terrorism because we lack the accurate
database, which may result in large fragility errors of some country.
Some indicators of a states are missing. To get the SPEC score, it requires extra weight-
ing of the indicators, which means the SPEC Model can be complex sometimes.
7 Conclusion
We build the SPEC model to analyse countries’ fragility, considering the aspects of se-
curity, politics, economics and climate. We employ different data weighting methods do
quantify individual indicators. Analytic Hierarchy Process is applied to determine weight
numbers. We propose the Self-regulatory Factor to better measure the Tipping Point of dif-
ferent countries. Also, we modify our model to ensure it applicable to "larger" or "smaller"
states. Then we refer to databases such as Worldbank, and we work out detailed and
quan-tified SPEC indicators of 178 countries and regions in the world. Our final SPEC
Score corresponds to the Fragile States Index. Finally, we do sensitivity analysis, discuss
strengths and weaknesses and prove the credibility of our SPEC model.


## 第 27 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
References
[1] “Fragile state,” Wikipedia. [Online]. Available: https://en.wikipedia.org/wiki/
Fragile_state
[2] “Fragile states index,” Fund for Peace (FFP). [Online]. Available: http://fundforpeace.
org/fsi/
[3] “Fund for peace,” Wikipedia. [Online]. Available: https://en.wikipedia.org/wiki/
Fund_for_Peace
[4] M. M. Q. Mirza, “Climate change and extreme weather events: can developing coun-
tries adapt?” Climate policy, vol. 3, no. 3, pp. 233–248, 2003.
[5] “Analytic hierarchy process,” Wikipedia. [Online]. Available: https://en.wikipedia.
org/wiki/Analytic_hierarchy_process
[6] S. Sengupta, “The food chain in fertile india, growth outstrips agriculture,” New York
Times. http://www. nytimes. com/2008/06/22/business/22indiafood. html, 2008.
[7] C. P. Ilbert, The Government of India. BiblioBazaar, LLC, 2008.
[8] K. Chakraborty, S. Sudhakar, K. Sarma, P. Raju, and A. K. Das, “Recognizing the
rapid expansion of rubber plantation–a threat to native forest in parts of northeast
india,” CURRENT SCIENCE, vol. 114, no. 1, pp. 207–213, 2018.
[9] P. Berman, R. Ahuja, and L. Bhandari, “The impoverishing effect of healthcare pay-
ments in india: new methodology and findings,” Economic and Political Weekly, pp.
65– 71, 2010.
[10] S. E. Rice and S. Patrick, Index of state weakness in the developing world. Brookings
Institution Washington, DC, 2008.


## 第 28 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Appendices
Appendix A SPEC Indexes Results


## 第 29 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Appendix B Analytic Hierarchy Process
clca=[1,3,1/6,5;1/3,1,1/7,4;6,7,1,9;1/7,1/4,1/9,1];n=length(a);
[x,y]=eig(a);eigenvalue=diag(y);lamda=eigenvalue(1);ci1=(lamda-4)/3;
RI=[0,0,0.58,0.9,1.12,1.24,1.32,1.41,1.45,1.49,1.51];RI(n)
CR=ci1/RI(n)
w1=x(:,1)/sum(x(:,1))
b=[1,3,1/4,1/4;1/3,1,1/6,1/6;4,6,1,3;4,6,1/3,1];m=length(b);
[p,q]=eig(b);eigenvalue2=diag(q);lamda2=eigenvalue2(1);


## 第 30 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
ci2=(lamda2-4)/3;
CR2=ci2/RI(n)
w2=p(:,1)/sum(p(:,1))
Appendix C SPEC Model Data Mining Algorithm
Part I
importnumpyasnp
importpandasaspd
importmath
ref=pd.read_csv(’/Users/Administration/Desktop/fsi-2017.csv’)
govind=pd.read_csv(’/Users/Administration/Desktop/worldwide_governance_indicators.csv’)confli=
pd.read_csv(’/Users/Administration/Desktop/conflict_intensity.csv’)
abu=pd.read_csv(’/Users/Administration/Desktop/gross_humanrights_abuses.csv’)elevation=
pd.read_csv(’/Users/Administration/Desktop/elevation.csv’)
CO=pd.read_csv(’/Users/Administration/Desktop/CO2.csv’)
forest=pd.read_csv(’/Users/Administration/Desktop/forestarea.csv’)arable=
pd.read_csv(’/Users/xufeng/Desktop/arableland.csv’)
gdp_growth=pd.read_csv(’/Users/Administration/Desktop/gdp_growth.csv’)gni_per=
pd.read_csv(’/Users/Administration/Desktop/gni_per_capita.csv’)landarea=
pd.read_csv(’/Users/Administration/Desktop/country_land_area.csv’)inflation=
pd.read_csv(’/Users/Administration/Desktop/inflation.csv’)drinking_water=
pd.read_csv(’/Users/Administration/Desktop/drinking_water.csv’)refugee=
pd.read_csv(’/Users/xufeng/Administration/refugee.csv’)
gini=pd.read_csv(’/Users/xufeng/Administration/gini.csv’)
ref_=ref.fillna(0)govind_=
govind.fillna(0)confli_=
confli.fillna(0)abu_=abu.fillna(0)
elevation_=elevation.fillna(0)CO_=
CO.fillna(0)
forest_=forest.fillna(0)arable_=
arable.fillna(0)gdp_growth_=
gdp_growth.fillna(0)gni_per_=
gni_per.fillna(0)landarea_=landarea.fillna(0)
inflation_=inflation.fillna(0)
drinking_water_=drinking_water.fillna(0)refugee_=
refugee.fillna(0)
gini_=gini.fillna(0)
country=[]gov
=[]law=[]corpt
=[]acc=[]
conflict=[]abv=
[]coups=[]
abuse=[]refu=
[]gni=[]
gdp=[]inf =
[]ineq=[]
reg=[]ele=
[]fore=[]
ara=[]water
=[]co=[]
land=[]
gni_p=[]
foriinrange(178):
country.append(ref_[’Country’][i]) forjin
range(7704):
if(country[i]==govind_[’CountryName’][j]andgovind_[’IndicatorCode’][j]==’forainrange(2016,2003,-1):
a=str(a)
ifgovind_[a][j]!=0:
s=govind_[a][j]/10.0
abv.append(s)
break
a=int(a)


## 第 31 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
if(a<=2004andgovind_[’2004’][j]==0):
abv.append(’null’)
break
if(j>=7703andcountry[i]!=govind_[’CountryName’][7703]):print(i,
country[i],’abv’,6)
abv.append(’null’)#a=
int(a)#ifa<=2004:
#abv.append(’null’)forj
inrange(7704):
if(country[i]==govind_[’CountryName’][j]andgovind_[’IndicatorCode’][j]==’forainrange(2016,2003,-1):
a=str(a)
ifgovind_[a][j]!=0:
s=govind_[a][j]/10.0
corpt.append(s)
break
a=int(a)
if(a<=2004andgovind_[’2004’][j]==0):corpt.append(’null’)
break
if(j>=7703andcountry[i]!=govind_[’CountryName’][7703]):print(i,
country[i],’corpt’,3)
corpt.append(’null’)
forjinrange(7704):
if(country[i]==govind_[’CountryName’][j]andgovind_[’IndicatorCode’][j]==’forainrange(2016,2003,-1):
a=str(a)
ifgovind_[a][j]!=0:
s=govind_[a][j]/10.0
gov.append(s)
break
a=int(a)
if(a<=2004andgovind_[’2004’][j]==0):gov.append(’null’)
break
if(j>=7703andcountry[i]!=govind_[’CountryName’][7703]):print(i,
country[i],’gov’,1)
gov.append(’null’)
forjinrange(7704):
if(country[i]==govind_[’CountryName’][j]andgovind_[’IndicatorCode’][j]==’forainrange(2016,2003,-1):
a=str(a)
ifgovind_[a][j]!=0:
s=govind_[a][j]/10.0
reg.append(s)
break
a=int(a)
if(a<=2004andgovind_[’2004’][j]==0):reg.append(’null’)
break
if(j>=7703andcountry[i]!=govind_[’CountryName’][7703]):print(i,
country[i],’reg’,14)
reg.append(’null’)
forjinrange(7704):
if(country[i]==govind_[’CountryName’][j]andgovind_[’IndicatorCode’][j]==’forainrange(2016,2003,-1):
a=str(a)
ifgovind_[a][j]!=0:
s=govind_[a][j]/10.0
law.append(s)
break
a=int(a)
if(a<=2004andgovind_[’2004’][j]==0):law.append(’null’)
break
if(j>=7703andcountry[i]!=govind_[’CountryName’][7703]):print(i,
country[i],’law’,2)
law.append(’null’)
forjinrange(7704):
if(country[i]==govind_[’CountryName’][j]andgovind_[’IndicatorCode’][j]==’forainrange(2016,2003,-1):
a=str(a)
ifgovind_[a][j]!=0:
s=govind_[a][j]/10.0
acc.append(s)
break
a=int(a)
if(a<=2004andgovind_[’2004’][j]==0):acc.append(’null’)


## 第 32 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
break
if(j>=7703andcountry[i]!=govind_[’CountryName’][7703]):print(i,
country[i],’acc’,4)
acc.append(’null’)
conflictt=0
forkinrange(2012,1997,-1):forjin
range(9046):
if(country[i]==confli_[’COUNTRY’][j]andconfli_[’YEAR’][j]==k):x=10-confli_[’ACTOTAL’][j]
ifx<=0:x=
0
conflictt=conflictt+x*(0.85**(2013-k))/5.171659conflict.append(conflictt)
abusee=0
forkinrange(2016,2011,-1):forjin
range(8606):
if(country[i]==abu_[’Country’][j]andabu_[’Year’][j]==k):a=abu_[’PTS_A’][j]
b=abu_[’PTS_H’][j]c=
abu_[’PTS_S’][j]
if(a!=’NA’andb!=’NA’andc!=’NA’):x=(a+b+c)/3
elif(a!=’NA’andb!=’NA’andc==’NA’):x=(a+b)/2
elif(a!=’NA’andb==’NA’andc!=’NA’):x=(a+c)/2
elif(a==’NA’andb!=’NA’andc!=’NA’):x=(b+c)/2
elif(a!=’NA’andb==’NA’andc==’NA’):x=a
elif(a==’NA’andb!=’NA’andc==’NA’):x=b
elif(a==’NA’andb==’NA’andc!=’NA’):x=c
else:
x=2
x=(5-x)*2.0
abusee+=x*(0.85**(2017-k))/3.152337abuse.append(abusee)
forjinrange(264):
if(elevation_[’CountryName’][j]==country[i] andelevation_[’2010’][j]!=0):y=elevation_[’2010’][j]
s=(100-y) /20
ele.append(s)break
if(j>=263andelevation_[’2010’][263]==0):ele.append(’null’)
forjinrange(264):
if(CO_[’CountryName’][j]==country[i]andCO_[’2001’][j]!=0andCO_[’2014’][jx=CO_[’2001’][j]
y=CO_[’2014’][j]
s=math.log(y)/math.log(x)co.append(s)
break
if(j>=263andCO_[’2001’][263]==0):co.append(’null’)
elif(j>=263andCO_[’CountryName’][263]!=country[i]):print(i,
country[i],’co’,21)
co.append(’null’)
forjinrange(264):
if(country[i]==arable_[’CountryName’][j]andarable_[’1992’][j]!=0andarablx=arable_[’1992’][j]
y=arable_[’2015’][j]s=
math.exp(y/x)ara.append(s)
break
if(j>=263andarable_[’1992’][263]==0):ara.append(’null’)
elif(j>=263andarable_[’CountryName’][263] !=country[i]):print(i,country[i], ’ara’,
17)
ara.append(’null’)
forjinrange(264):
if(country[i]==forest_[’CountryName’][j]andforest_[’2000’][j]!=0andforesx=forest_[’2000’][j]
y=forest_[’2015’][j]s=
math.exp(y/x)fore.append(s)
break
if(j>=263andforest_[’2000’][263]==0):


## 第 33 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
fore.append(’null’)
elif(j>=263andforest_[’CountryName’][263] !=country[i]): print(i, country[i],’fore’,
16)
fore.append(’null’)
forjinrange(264):
if(country[i]==drinking_water_[’CountryName’][j]anddrinking_water_[’2000’][jx=drinking_water_[’2000’][j]
y=drinking_water_[’2015’][j]s=
math.exp(y/x)water.append(s)
break
if(j>=263anddrinking_water_[’2000’][263]==0):water.append(’null’)
elif(j>=263and drinking_water_[’CountryName’][263] !=country[i]):print(i, country[i],’water’,
18)
water.append(’null’)
s=0cnt
=0
forkinrange(2015,2000,-1):k=str(k)
p=int(k)
forjinrange(264):
if(country[i]==inflation_[’CountryName’][j]andinflation[k][j]!=0andccnt+=1
x=(100-abs(inflation_[k][j]))/10.0s+=x*(0.85**(2016-p))/
3.152337
ifcnt>=5:inf.append(s)
else:inf.append(’null’)
s=0cnt
=0
forkinrange(2015,2000,-1):k=str(k)
p=int(k)
forjinrange(264):
if(country[i]==gdp_growth_[’CountryName’][j]andgdp_growth[k][j]!=0andcnt+=1
x=gdp_growth_[k][j]
s+=x*(0.85**(2016-p))/3.152337
q=s+3ifq
>=10:
q=10
elifq<0:
q=0
ifcnt>=5:
gdp.append(q)
else:gdp.append(’null’)
forjinrange(264):
if(country[i]==landarea_[’CountryName’][j]andlandarea_[’2017’][j]!=0):x=landarea_[’2017’][j]
y=landarea_[’2017’][249]
s=math.log(x)/math.log(y)ifs>1:
s=1
land.append(s)
break
if(j>=263andlandarea_[’2017’][263]==0):land.append(’null’)
elif(j>=263andlandarea_[’CountryName’][263]!=country[i]):print(i,
country[i],’land’,19)
land.append(’null’)
forjinrange(264):
if(country[i]==gni_per_[’CountryName’][j]andgni_per_[’2016’][j]!=0):x=gni_per_[’2016’][j]
y=gni_per_[’2016’][142]
s=math.log(x)/math.log(y)ifs>1:
s=1
gni_p.append(s)r=
s*10gni.append(r)
break
if(j>=263andgni_per_[’2016’][263]==0):gni_p.append(’null’)
gni.append(’null’)
elif(j>=263andgni_per_[’CountryName’][263]!=country[i]):print(i,country[i],’gni,
gni_p’,10,20)


## 第 34 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
gni_p.append(’null’)
gni.append(’null’)
forjinrange(264):
ifcountry[i]==refugee_[’CountryName’][j]:if
refugee_[’2016’][j]!=0:
x=refugee_[’2016’][j]/1000000.0*10.0x=10.0-x
ifx<=0:x=
0
refu.append(x)
break
elif(refugee_[’2016’][j]==0andrefugee_[’2015’][j]!=0):x=refugee_[’2015’][j]/1000000.0*10.0
x=10.0-xifx
<=0:
x=0
refu.append(x)
break
elif(refugee_[’2016’][j]==0andrefugee_[’2015’][j]==0andrefugee_[’2014x=refugee_[’2014’][j]/1000000.0*10.0
x=10.0-xifx
<=0:
x=0
refu.append(x)
break
elif(refugee_[’2016’][j]==0andrefugee_[’2015’][j]==0andrefugee_[’2014x=refugee_[’2013’][j]/1000000.0*10.0
x=10.0-xifx
<=0:
x=0
refu.append(x)
break
elif(refugee_[’2016’][j]==0andrefugee_[’2015’][j]==0andrefugee_[’2014x=refugee_[’2012’][j]/1000000.0*10.0
x=10.0-xifx
<=0:
x=0
refu.append(x)
break
break
if(j>=263andrefugee_[’2016’][j]==0andrefugee_[’2015’][j]==0andrefugee_[’2refu.append(’null’)
elif(j>=263andrefugee_[’CountryName’][263]!=country[i]):print(i,
country[i],’refu’,9)
refu.append(’null’)
guo=[’Fiji’,’Ecuador’,’Burundi’,’CentralAfricanRepublic’,’Venezuela’,’Philippforjinrange(38):
ifguo[j]==country[i]:s=0
coups.append(s)break
if(j>=37andguo[37]!=country[i]):s=10
coups.append(s)
forjinrange(264):
ifcountry[i]==gini_[’CountryName’][j]:forkin
range(2015,1979,-1):
k=str(k)
ifgini_[k][j]!=0:
s=(100-gini_[k][j])/10ineq.append(s)
break
k=int(k)
if(k<=1980andgini_[’1980’][j]==0):ineq.append(’null’)
break
if(j>=263andgini_[’CountryName’][263]!=country[i]):print(i,
country[i],’ineq’,13)
ineq.append(’null’)
spec=[country,gov,law,corpt,acc,conflict,abv,coups,abuse,refu,gni,gdp,inf,iSPEC=pd.DataFrame(spec)
SPEC=SPEC.TSPEC.to_csv(’/Users/Administration/Desktop/SPEC_data.csv’,mode=’a+’)
print(’Successfullydone!’)
Part II


## 第 35 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
importpandasaspd
importmath
arable=pd.read_csv(’/Users/Administration/Desktop/arableland.csv’)gdp_growth=
pd.read_csv(’/Users/Administration/Desktop/gdp_growth.csv’)gni_per=
pd.read_csv(’/Users/Administration/Desktop/gni_per_capita.csv’)landarea=
pd.read_csv(’/Users/Administration/Desktop/country_land_area.csv’)inflation=
pd.read_csv(’/Users/Administration/Desktop/inflation.csv’)drinking_water=
pd.read_csv(’/Users/Administration/Desktop/drinking_water.csv’)refugee=
pd.read_csv(’/Users/Administration/Desktop/refugee.csv’)
gini=pd.read_csv(’/Users/Administration/Desktop/gini.csv’)
arable_=arable.fillna(0)gdp_growth_=
gdp_growth.fillna(0)gni_per_=
gni_per.fillna(0)landarea_=landarea.fillna(0)
inflation_=inflation.fillna(0)
drinking_water_=drinking_water.fillna(0)refugee_=
refugee.fillna(0)
gini_=gini.fillna(0)
df=pd.read_csv(’/Users/Administration/Desktop/SPEC_data.csv’)
foriin[3,5,6,15,28,29,35,36,48,57,58,66,69,79,105,111,133,153]:forjinrange(264):
if(df[’22’][i]==gni_per_[’CountryCode’][j]andgni_per_[’2016’][j]!=0):x=gni_per_[’2016’][j]
y=gni_per_[’2016’][142]
s=math.log(x)/math.log(y)ifs>1:
s=1df[’20’][i]
=s
r=s*10df[’10’][i]=r
break
forjinrange(264):
ifdf[’22’][i]==refugee_[’CountryCode’][j]:if
refugee_[’2016’][j]!=0:
x=refugee_[’2016’][j]/1000000.0*10.0x=10.0-x
ifx<=0:x=
0
df[’9’][i] =xbreak
elif(refugee_[’2016’][j]==0andrefugee_[’2015’][j]!=0):x=refugee_[’2015’][j]/1000000.0*10.0
x=10.0-xifx
<=0:
x=0df[’9’][i]
=xbreak
elif(refugee_[’2016’][j]==0andrefugee_[’2015’][j]==0andrefugee_[’2014x=refugee_[’2014’][j]/1000000.0*10.0
x=10.0-xifx
<=0:
x=0df[’9’][i]
=xbreak
elif(refugee_[’2016’][j]==0andrefugee_[’2015’][j]==0andrefugee_[’2014x=refugee_[’2013’][j]/1000000.0*10.0
x=10.0-xifx
<=0:
x=0df[’9’][i]
=xbreak
elif(refugee_[’2016’][j]==0andrefugee_[’2015’][j]==0andrefugee_[’2014x=refugee_[’2012’][j]/1000000.0*10.0
x=10.0-xifx
<=0:
x=0df[’9’][i]
=xbreak
break
s=0cnt
=0
forkinrange(2015,2000,-1):k=str(k)
p=int(k)
forjinrange(264):
if(df[’22’][i]==gdp_growth_[’CountryCode’][j]andgdp_growth[k][j]!=0ancnt+=1


## 第 36 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
x=gdp_growth_[k][j]
s+=x*(0.85**(2016-p))/3.152337
q=s+3ifq
<=0:
q=0elifq
>=10:
q=10if
cnt>=5:
df[’11’][i]=q
s=0cnt
=0
forkinrange(2015,2000,-1):k=str(k)
p=int(k)
forjinrange(264):
if(df[’22’][i]==inflation_[’CountryCode’][j]andinflation[k][j]!=0andcnt+=1
x=(100-abs(inflation_[k][j]))/10.0s+=x*(0.85**(2016-p))/
3.152337
ifcnt>=5:df[’12’][i]=s
forjinrange(264):
if(df[’22’][i]==landarea_[’CountryCode’][j]andlandarea_[’2017’][j]!=0):x=landarea_[’2017’][j]
y=landarea_[’2017’][249]
s=math.log(x)/math.log(y)ifs>1:
s=1df[’19’][i]
=sbreak
forjinrange(264):
if(df[’22’][i]==drinking_water_[’CountryCode’][j]anddrinking_water_[’2000’][x=drinking_water_[’2000’][j]
y=drinking_water_[’2015’][j]s=
math.exp(y/x)
df[’18’][i]=sbreak
forjinrange(264):
if(df[’22’][i]==arable_[’CountryCode’][j]andarable_[’1992’][j]!=0andarabx=arable_[’1992’][j]
y=arable_[’2015’][j]s=
math.exp(y/x)df[’17’][i]=s
break
forjinrange(264):
ifdf[’22’][i]==gini_[’CountryCode’][j]:forkin
range(2015,1979,-1):
k=str(k)
ifgini_[k][j]!=0:
s=(100-gini_[k][j])/10df[’13’][i]=s
break
break
df=df.fillna(0)df.to_csv(’/Users/Administration/Desktop/SPEC_Data.csv’,mode=’a+’)print
(’Successfullydone!’)
Appendix D SPEC Model Final Calculation Algorithm
importpandasaspd
importmath
R=[]spec=[]
country=[]gov
=[]law=[]
corpt=[]acc=
[]
conflict=[]abv=
[]coups=[]
abuse=[]refu=
[]


## 第 37 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
gni=[]gdp=
[]inf=[]ineq
=[]reg=[]
ele=[]fore=
[]ara=[]
water=[]co
=[]land=[]
gni_p=[]
extre=[]
df=pd.read_csv(’/Users/Administration/Desktop/SPEC_Data.csv’)df=df.fillna(0)
foriinrange(178):
country.append(df[’0’][i])
gov.append(df[’1’][i])
law.append(df[’2’][i])
corpt.append(df[’3’][i])
acc.append(df[’4’][i])
conflict.append(df[’5’][i])
abv.append(df[’6’][i])
coups.append(df[’7’][i])
abuse.append(df[’8’][i])
refu.append(df[’9’][i])
gni.append(df[’10’][i])
gdp.append(df[’11’][i])
inf.append(df[’12’][i])
ineq.append(df[’13’][i])
reg.append(df[’14’][i])
ele.append(df[’15’][i])
fore.append(df[’16’][i])
ara.append(df[’17’][i])
water.append(df[’18’][i])
land.append(df[’19’][i])
gni_p.append(df[’20’][i])
co.append(df[’21’][i])
pol=df[’1’][i]+df[’2’][i]+df[’3’][i]+df[’4’][i]
sec=0.2069*df[’5’][i]+0.1724*df[’6’][i]+0.2759*df[’7’][i]+0.1034*df[’8sec=sec*5
eco=0.2593*df[’10’][i] +0.2963 *df[’11’][i]+0.1111*df[’12’][i] +0.1851*dfeco=eco*5
gen=0.1131*df[’15’][i]+0.3543*df[’16’][i]+0.2261*df[’17’][i]+0.3065*dfalpha=0.3189*df[’19’][i]+0.2211*df[’20’][i]+0.46*sec/50
extreme=math.exp(-alpha)*df[’21’][i]*5extre.append(extreme)
R.append(alpha)
index=(pol+sec+eco+gen)/extreme
spec.append(index)
final=[country, gov,law,corpt,acc,conflict,abv,coups,abuse,refu,gni,gdp,inf,SPEC=pd.DataFrame(final)
SPEC=SPEC.TSPEC.to_csv(’/Users/Administration/Desktop/SPEC_INDEX.csv’,mode=’a+’)
print(’Successfullydone!’)
[13]

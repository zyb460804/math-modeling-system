# E89499-An Evaluation Model of State Fragility related to Climate Change Based on the PSR Model and Entropy Weight Method


## 第 1 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#89499 Page1of21
TeamControlNumber
Forofficeuseonly 89499 Forofficeuseonly
T1 F1
T2 F2
ProblemChosen
T3 F3
E
T4 F4
2018
MCM/ICM
SummarySheet
(Yourteam'ssummaryshouldbeincludedasthefirstpageofyourelectronicsubmission.)
Typeasummaryofyourresultsonthispage.Donotincludethenameofyourschool,advisor,orteammembersonthispage.
AnEvaluationModel of StateFragility related to Climate Change
Basedon thePSRModel andEntropy WeightMethod
Climate change is likely to influence the fragile situation of a state. Thereby, we propose
an evaluation model in order to derive a quantitative expression of state fragility as well as
therelationship between it and climate change.
First, theP-S-R (Pressure-State-Response) Model is applied in our model to offer a
distinct framework of the relationship between fragility and related indicators. The model
follows a domain-theme-feature structure. Climate change is involved through direct
indicators and indirect impact on social and economic environment. Thereafter, we derive the
equation of fragility by Entropy Weight Method. Furthermore, we apply the Discriminant
Analysis to obtain the value range of fragile, vulnerable and stable states. The corresponding
results are0.4991-1, 0.2196-0.4991, and 0-0.2196.
Second, we determine the fragility in Sudan from 2012 to 2016, which shows a
fluctuation in the limited fragile range. Meanwhile, it is observed that climate change mainly
influences on the food security in Sudan through Gray Relational Analysis. Then by
establishing a new framework without climatic indicators directly, we acquire the fragility
withoutclimate change, and theresult isthat thefragility declines.
Third, for Egypt, our model shows that the fragile situation isgenerally deteriorating
from 2012 to 2016 but still regarded as vulnerable. We obtain that climate change mainly
impacts on health condition in Egypt. Then the tipping point of fragility is determined as
0.4991 (value of fragility) in this section. By Line Regression Method, we then predict that
Egypt would become afragile statein2028.
Fourth, we propose a series of interventions based on the model, focusing on climate
control and improving the coping capability of a country respectively. The total cost of
interventions is calculated as 1,120,070,0000 dollars, and the results show that the fragile
situationofEgypt would be 8.92%better after implementinginterventions.
Lastly, we illustrate the comprehensive modifications of model for better applicable to
different sizesof state, mostlyconcentrated ontheindicators we choose.
key words: PSR Model, Entropy WeightMethod, DiscriminantAnalysis


## 第 2 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team # 89499
1Introduction.......................................................................................................................................2
1.1Background.............................................................................................................................2
1.2Restatementoftheproblem.................................................................................................2
2AssumptionsandNotations..........................................................................................................3
2.1Assumptions...........................................................................................................................3
2.2Notations.................................................................................................................................3
3TheModelofFragility....................................................................................................................3
3.1P-S-RModel............................................................................................................................3
3.2P-S-RFrameworkforstatefragility....................................................................................4
3.2.1P-S-RFramework........................................................................................................4
3.2.2AnalysisofImpactofClimate...................................................................................6
3.3EvaluatetheStateFragility...................................................................................................7
3.3.1Entropyweightmethod.............................................................................................7
3.3.2EquationofStateFragility.........................................................................................8
3.5ModelTest...............................................................................................................................8
3.5.1ModelTeston30countries........................................................................................8
3.5.2ClassificationofFragile,vulnerableandstablestates..........................................9
4FragilityandClimateChangeinSudan......................................................................................9
4.1FragileSituationandClimaticImpact..............................................................................10
4.1.1CurrentFragilityinSudan.......................................................................................10
4.1.2 HowClimatechangeimpactsonfragileSudan...................................................11
4.2ALessFragileSudanwithoutinfluenceofClimate.......................................................11
5FragilityandClimateChangeinEgypt.....................................................................................12
5.1FragileSituationandClimaticImpact..............................................................................12
5.1.1 CurrentFragility.......................................................................................................12
5.1.2 HowClimatechangeimpactsonfragileSudan...................................................13
5.2Thetippingpointoffragility..............................................................................................14
6InterventionPlanforBetterStability........................................................................................14
6.1Interventions.........................................................................................................................15
6.1.1 Planaboutclimatecontrol.......................................................................................15
6.1.2 Planaboutcopingability.........................................................................................15
6.2CostbasedonEgypt.............................................................................................................16
6.3Effectsofinterventions........................................................................................................16
7Modificationsforregionsofdifferentsizes.............................................................................17
7.1Inapplicabilityofmodelforsmallerorlargerstates......................................................17
7.2Modificationsforregionsofdifferentsize.......................................................................17
8StrengthsandWeaknesses...........................................................................................................18
8.1Strengths................................................................................................................................18
8.2Weaknesses............................................................................................................................18
9Futurework.....................................................................................................................................19
References...........................................................................................................................................21


## 第 3 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#89499 Page2of21
1 Introduction
1.1 Background
Climate-fragility risks pose threats to the stability of states and societies. In other
words, climate change has already had observable effects on environment [1] and
further on the state fragility. In this paper, we define the problem of climate change as
the impact of superimposition of natural change cycle and human activities, rather than
attributionofhuman activities orattribution ofnatural phenomena purely. [2]
States are classified as fragile if they lack the capacity to discharge their normal
functions and drive forward development [3]. In fragile regions where inequality
persists and the government is unable to respond to stresses, it has been found that the
impacts of climate change on water, food and land will augment existing pressures. That
is to say that dynamics of state fragility may be exacerbated by climate change impacts
and that the consequence of this is reduced adaptation capacity [4]. Vice versa, the
downward trend of state stability will also exacerbate the climate change. Terrible
natural and political environment further enables resources shortage, migration, weak
governance andeven violent conflict.
1.2 Restatement of the problem
According to the problem, we are required to develop an appropriate model which
contribute to the identification of a country’s fragility and the impact of climate change
at the same time. After that, model instantiation should be implemented on concrete
countries. Meanwhile, propose a series of interventions to mitigate the risk of climate
change and further modifications for regions of different sizes.
Research work about fragile state has sprung up recent years around the world,
especially for the west. 11 kinds of current indices for fragility are listed in [5],
including Country Indicators for Foreign Policy Fragility Index (CIFP), Harvard
Kennedy School Index of African Governance (IAG), Fragile States Index (FSI), etc.
All these diverse evaluation indices are based on the Buckets effect and derived
quantificationally. Nevertheless, scarcely do current indices take climate change into
account, which becomes moreand more non-negligible.
Thereby, on the foundation of the related work above, we establish a
comprehensive evaluation model based on Entropy Analysis Method, so as to represent
the extent of fragility as well as how climate change contributes to it. Next, we complete
evaluation on both fragile Sudan and relatively not so fragile Egypt based on our model,
deriving a tipping pointas the boundary value. Meanwhile, we acquire both the fragility
quantificationally and the level of fragility. Furthermore, interventions of climatic
controlling and better coping capabilityare proposed with the cost. Finally, we put
forward modifications in order to exacerbate the capability of ourmodel on smaller and
lagerstates.


## 第 4 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#89499 Page3of21
2 Assumptions and Notations
2.1 Assumptions
(1) The indicators of a country's fragility are mainly socio-economic, ecological and
climate. Based on that we establishour evaluation model, where the choice of indicators
is comparatively comprehensive, since it offers convenience for a more integrated
considerationof state fragility.
(2) The political situation in Egypt is stable during intervening. Although Egypt is
politically unstable in reality, this assumption is beneficial for calculating the total cost
ofour interventions.
(3) Egypt will follow the trends in massive countries based on indicators like GDP,
population and Industry. These trends are generally true. Thus, if Egypt follow them,
we are able to derive quantitative relationship between a number of indicators so as to
predict theeconomic growth inEgypt, based oncurrent values ofindicators.
2.2 Notations
3 The Model of Fragility
Our model for the evaluation of state fragility is based on the P-S-R model and
the Entropy Weight Method. Initially, we apply the former to determine and collect
indicators that influence the fragility of a state, especially the indicators related to
climate change. Then our model adopts the latter as the way of deriving an equation
about these selected indicators, which enables the representation and calculation of state
fragility quantificationally. After that, we determine the range of three criteria of
fragility, namely fragile, vulnerable and stable, byDiscriminationAnalysis.
3.1 P-S-R Model
P-S-R(Pressure-State-Response)is an evaluation modelcommonly used in sub-
disciplinesof ecosystem health assessment in thefield ofenvironmental quality


## 第 5 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#89499 Page4of21
assessment. Through the thinking logic"reason-effect-response", the PSR model reflects
the interaction between humans and the environment [6]. Mankind acquire the resources
necessary for its survival and development from the natural environment and meanwhile,
dischargethe waste to the nature. In this way, the reserves of natural resources and the
quality of the environment are changed. And in return, variation in the state of nature
and the environment impacts onsocio-economic activities and welfare of human beings.
Furthermore, the society responds to these changes by means of environmental,
economic and sectoral policies, as well as changes in consciousness and behavior. This
cycle of reciprocation constitutes a pressure-state-response relationship between humans
and the environment.
The PSR model answers the three basic questions of sustainable development, that
is, "what happened, why it happened, how we do it." To represent and solve these more
concretely, three categories of indicators are defined in the PSR model, namely
exposure, sensitivity and adaptive capability. More specifically, the exposure
characterizes howmortalsocio-economic activities impact on the environment, such as
the environmental damage and disturbance due to resource acquisition, material
consumption and emissions caused by various industries. Meanwhile, the sensitivity
characterizes the environmental status and the change of environment itself during a
specific period of time, including the current status of ecosystems and the natural
environment, the quality of life and health of human beings. Finally, the adaptive
capacity refers to how societies and individuals act so as to mitigate, deter, recover and
prevent the negative effects of climate and economic factors, as well as remedial
measures for the existing change in ecological environment that is not conducive to
human existence.
3.2 P-S-R Framework for state fragility
3.2.1 P-S-R Framework
The mutual effect between state fragility and environment (both political and
natural) mentioned above accords with the basic background of PSR model, which
means that it is reasonable to interpret the relationship between state fragility and
environment as a pressure-state-response relationship.
Figure1
TheDomainLayer
For fragility, theoriginal three categories ofindicators correspond to stress


## 第 6 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#89499 Page5of21
indicators, status indicators and response indicators respectively as shown in Figure1.
More exactly, the stress indicators refer to the catastrophic condition of a state, the
status indicators own relatively indirect relationship with fragility, and the response
indicators represent the capability of coping with negative influence ofa state. Note that
no clear differentiation exists between the stress indicators and the status indicators.
These threecategories constitutethedomain layer.
Then the theme layer further refines the domain layer. First, we define the themes
of stress indicators as climate change and socio-economic. The concrete indicators and
thestructure are shownin Figure 2.
Figure2
Second, the themes of status indicators are defined as water resources, eco-system,
TheThemeLayerandFeatureLayerofStressIndicators
social and economic development, the development of population, health andIndustrial
energy consumption efficiency. The structure of both theme layer and feature layer is
shown in Figure 3.
Figure3
Finally, thethemes ofresponse indicators are defined as economic capability,
TheThemeLayerandFeatureLayerofStatusIndicators


## 第 7 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#89499 Page6of21
human resources and social security, infrastructure and technical security. Thestructure
ofboth themelayer and feature layer is shownin Figure 4.
Figure4
While selecting the indicators, we give consideration to both scientificity and
TheThemeLayerandFeatureLayerofResponseIndicators
effectiveness, since it is kind of difficult to acquire correlative date for some special
regions whose fragility are comparatively high. Moreover, we take the influence of
government on fragility into account and regard it as an independent part, which
contributes greatly to the more concrete analysis of state fragility as well as the
interventions to mitigate fragility. Similarly, we take climate change as an individual
theme including several indicators, which enables and augments the representation and
interpretationof howclimatechange impacts onfragility.
3.2.2 Analysis of Impact of Climate
Figure5
In addition to the 23 indicators which involving direct climatic indicators, we
TheCouplingSystem
select above in section 3.2.1, we further present the indirect part of climate change as a
more specific and effective explanation. Given that climate, ecological environment and
social-economic environment constitute a coupling system [7] as shown in Figure 5, it
is undoubtedly massively difficult to determine a certain quantitative relation. As a
result, theindirect impart here is not equal to quantitativeimpact butworks as guidance


## 第 8 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#89499 Page7of21
forproceeding interventions instead.
Weapply the Gray Relational Analysis(GRA) to obtain climate variables with the
largest impact on some social indicators, namely the most relevant indicators, in order
to draw effective instructions for proposing interventions. Gray Relational Analysis use
gray relational degree as one metrics of the relational degree between the target and
other related factors. In the process of system development, if the tendency of the
change of two factors is consistent, that is, the degree of synchronization changes is high,
the correlation between the two is higher; on the contrary, it is lower. That is to say,
through GRA we can get the relationship between factors and the target in a numerical
way,which simplifies further work.
Based on the indicators provided in the Fifth Assessment Report of IPCC, we
select some with dramatic change and obvious impacts on society and economy. The
final selected alternative variables are respectively CO2, temperature, land cover rate,
etc.
3.3 Evaluate the State Fragility
3.3.1 Entropy weight method
With the main factors related to the capability of a region to offer clean water, the
second step in our evaluation model is to determine the weight of each factor so that the
equationofstate fragility can be determined.
In this section we adopt the Entropy Weight Method as the means of delivering
each factor's weight. The basic idea of the Entropy Weight Method is that entropy is a
measure of the degree of disorder of the system. If the information entropy of an
indicator is smaller, the greater the amount of information provided by the indicator, the
greater the role played by the indicator in comprehensive evaluation, and the higher the
weight should be. In other words, the size of the indicator variability determines the
objectiveweight. It consists ofseveral steps.
1) Above all, assuming that state fragility has been observed for m years and the number
of indicators is n, we regard as the value of the jth
indicator in the ith year. Thereby, constitutes the
"#
  (  = 1,2, … ,  ;   = 1,2, … ,  )
matrixX.
"#
  (  = 1,2, … ,  ;   = 1,2, … ,  )
2) Standardization. The value of each indicators should be standardized so as to
proceed the following steps, which is actually the homogenization of
heterogeneousindicators. We define the standardized data corresponding to
indicators as
separately.
"# "#
  (  = 1,2, … ,  ;   = 1,2, … ,  )   (  = 1,2, … ,  ;   = 1,2, … ,  )
wherei=1,2,…,m; j=1,2,…,n.
3) Calculatetheproportion ofthejthindicator inthe ithyear ofthat indicator.
"#
"


## 第 9 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#89499 Page8of21
wherei=1,2,…,m; j=1,2,…,n.
4) Next, derive the information entropy of each factor. According to the
definition ofinformation entropy,it isexpressed as follows.
>
E
5)Calculate the coefficient of variation of the jth indicator. For each indicator, the
larger the difference, the more important it accounts for the evaluation, the smaller the
information entropy.The variation coefficient isdefined asfollows.
#
6) Given the information entropy , , ,..., the weight of each indicator can
bederived as thefollowing equation.
< P Q >
E E E W
wherei=1,2,…,m; j=1,2,…,n.
3.3.2 Equation of State Fragility
At last, we determine the equation of state fragility can be determined as the sum
ofmultiplication oftheweight and valueofeachindicator as follows.
wherei=1,2,…,m; j=1,2,…,n; is thestatefragility in theithyear.
3.5 Model Test "
 
3.5.1 Model Test on 30 countries
Given that our evaluation model is a generalized model whose parameters cannot
be determined until the target state is chosen, we test it on 30 countries respectively so
as to certify its robustness and validity. And the 30 countries are SouthSudan, Yemen,
Syria, Chad, Iraq, Ethiopia, Niger, Libya, Myanmar, NorthKorea, Nepal, Mozambique,
BurkinaFaso, Cambodia, Madagascar, Laos, Turkey, Russia, Azerbaijan, Gabon,
Paraguay, Samoa, Botswana, Montenegro, Argentina, Poland, United States, Belgium,
Canada, and Norway.


## 第 10 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#89499 Page9of21
Comparison of the Rank Based on Our Model and
FSI
140 0.7
120 0.6
0.5
100
0.4
80
0.3
60
0.2
40 0.1
20 0
OurModel FSI
Figure6
From Figure 6 above, it can be interpreted that the rank of states of fragility
ComparisonofTheRankBasedonOurModelAndFSI
according to the evaluation from our model differs from that according to the Fragile
State Index, but in a reasonable range. The tendency of the two lines is similar. It is
understandable for several reasons, especially for that our model takes indicators about
climate change into account. In this way, countries with relatively small size and
impressionable to climate change are prone to show an increase in fragility. Forexample,
the fragility of Samoa increases compared with that in Fragile State Index, for it is
located in Pacific isles suffered from extreme fluctuant climate throughout the year.
Similarly, Laos that often encounters natural disasters like typhoons also shows a
relativeincrease when compared with FragileState Index.
3.5.2 Classification of Fragile, vulnerable and stable states
Based on the outcome of 30 countries in section 3.5.1, we then work on obtaining a
relatively accurate range of three levels of fragility, namely fragile, vulnerable and
stable. Here, we adopt the Discriminant Analysis, a statistical analysis to predict a
categorical dependent variable (called a grouping variable) by one or more continuous
or binary independent variables (called predictor variables). More specifically, in this
section, weselect certain countries in the relatively top, middle and back part in the rank
of Fragile State Indexas samples for classification. In the meantime, we take other
countries as input for Discriminant Analysis and regard the fragility of countries in the
junction between two categories as the boundary value. The results are shown below in
Table2.
Table2
Level Range
Rangeofthreelevels
Fragile 0.4991-1
Vulnerable 0.2196-0.4991
Stable 0-0.2196
4 Fragility and Climate Change in Sudan
In thissection, weimplement ourevaluation model onSudan, determining its


## 第 11 页

Team#89499 Page10of21
fragility and analyze the influence of climate change on it objectively. Furthermore, we
instantiate our model in another condition where the effect of climate change is not
taken into account through removing climatic indicators, which indicates that the state
would beless fragile in thisway.
4.1 Fragile Situation and Climatic Impact
4.1.1Current Fragility in Sudan
Applying our model to Sudan withthe collected data from theWorld Bank, we
determinethe fragility ofSudan and thelevel from 2012to2016 as follows.
FragilityofSudan
0.8
0.6
0.4
0.2
0
2012 2013 2014 2015 2016
Year
StressIndicator StatusIndicator
ResponseIndicator Fragility
Figure7
It can be obtained from the Figure 7 that during the five years, Sudan is still in
FragilityofSudan
severe fragile condition though its fragility fluctuated in a relatively small range like
“W”, and on the whole it declined, which meets the reality. More specifically, the stress
indicators, the status indicators, the response indicators are shown in Figure 8. It can be
concluded that from 2012 to 2015, the change of fragility mainly comes from the
change of response indicators as 57.39%, while from 2015 to 2016, the increase in
fragility mainlycomes from the increase in stress indicators as78.1%.
VarianceofStress,StatusandResponseIndicators
0.3
0.25
0.2
0.15
0.1
0.05
0
2012 2013 2014 2015 2016 Year
StressIndicators StatusIndicators ResponseIndicators
Figure8
 Stress Indicators
VarianceofStress,StatusandResponseIndicatorsinSudan
eulaV
eulaV
精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！


## 第 12 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#89499 Page11of21
For the stress indicators including climate change and socio-economic, the
variance of precipitation in dry and wet season both showed almost the same fluctuation
from 2012 to2016. Therefore, we can conclude that during the 5 years, it still received a
greater threat and impact from the global climate, and the imbalance of eco-system has
not yet been fundamentally alleviated. Moreover, the population of refugee by country
or refuge area kept increasing dramatically, which directly compounded the pressure on
the government and reflected the poor efficiency of government's measures and action
at thesame time.
 StatusIndicators
For the status indicators including natural environment and social-economic, GNI
per capita showed an upward trend especially between 2014 and 2015 when it almost
doubled, meanwhile, both arable land per capita and forest area kept declining during
the five years. Tosum up, indicators pertaining to the status indicators showed a benign
development condition onthe whole.
 ResponseIndicators
For the response indicators including economic capability, human resources and
social security, infrastructure and technical security, government expenditure on
education totally (% of GDP) showed a positive tendency though the change is slow and,
as well as health expenditure (% of GDP), while Net ODA received per capita
maintained decreasing year by year significantly. All of the change indicates that
adaptability ofSudan to external environment improved.
4.1.2 How Climate change impacts on fragile Sudan
Applying the Gray Relational Analysis to Sudan, we determine the relationship
between climaticindicators and somesocial-economicindicators as shown in Table3.
Table3
Per capita renewable Cereal Prevalence of
RelationshipIndexbetweenclimaticindicatorsandsocial-economicindicators
inland freshwater production undernourishment
resources
CO2 0.0171 0.1367 0.0942
Temperature 0.0324 0.0942 0.1023
Precipitation 0.0514 0.1023 0.0786
Landcoverage 0.0223 0.0786 0.0622
Extreme Weather 0.0308 0.0522 0.1367
From the table above, we can conclude that climatic indicators mostly impact the
cereal production, namely the food security of Sudan, since the degree of relationship
between them is relatively high on the whole. Therefore, in Sudan, climate change
mainlyinfluences the fragility through food security.
4.2 A Less Fragile Sudan without influence of Climate
In order to get the how the fragility of Sudan would change without the influences
of climate change, we directly remove the indicators related to climate in our model and
run it again. The results of 10 countries including Sudan are shown below in Table 4 in
theform oforiginal andsubsequent rank.


## 第 13 页

Team#89499 Page12of21
Table4
Country Rank with Rankwithout Changeof
Ranksofcountries'fragilitywithandwithoutclimateimpact
climaticimpact climaticimpact Rank
SouthSudan 2 1 -1
Somalia 1 2 +1
CentralAfricanRepublic 4 4 0
Yemen 3 3 0
Sudan 6 7 +1
Syria 5 5 0
CongoDemocraticRepublic 7 6 -1
Chad 8 9 1
Afghanistan 9 10 +1
Iraq 10 8 -2
It can be inferred from the table that the fragile situation of Sudan is relatively
dampened sinceits rank goes down, neglecting theimpact of climatechange.
5 Fragility and Climate Change in Egypt
In this part, we complete another case study onEgypt about fragility based on our
evaluation model, which is out of the top 10 fragile states. Through calculation of the
model, we measure the fragility of Egypt, as well as how and when climate change may
increase that. Based on the work above, we further determine the tipping point that a
country become fragile and makerelevant predictions.
5.1 Fragile Situation and Climatic Impact
5.1.1 Current Fragility
Applying our model to Egypt with the collected data from the World Bank, we
determinethe fragility ofSudan and thelevel from 2012to2016 as follows.
FragilityofEgypt
0.6
0.5
0.4
0.3
0.2
0.1
0
2012 2013 2014 2015 2016 Year
StressIndicators StatusIndicators ResponseIndicators Fragility
Figure9
It can be inferred from theFigure 9that thefragile situationof Egypt showed a
FragilityofEgypt
eulaV
精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！


## 第 14 页

Team#89499 Page13of21
eulaV
精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
generally deteriorate trend from 2012 to 2016 as its fragility fluctuated.More
specifically, the stress indicators, the status indicators, the response indicatorsare shown
in Figure 10.It can be concluded that from 2012 to 2013, the change of fragility mainly
comes from the change of response indicators and status indicators as 77.87%, while
from 2013 to 2016, the increase in fragility mainly comes from the increase in response
indicators as 83.4%.
VarianceofStress,StatusandResponseIndicators
0.25
0.2
0.15
0.1
0.05
0
2012 2013 2014 2015 2016 Year
StressIndicators StatusIndicators ResponseIndicators
Figure10
 Stress Indicators
VarianceofStress,StatusandResponseIndicatorsinEgypt
For stress indicators, the variance of precipitation in dry season is relatively steady
while that in wet season decreaseddramatically. The temperature in both wet and dry
season also showed an apparent change. Therefore, we can conclude that during the 5
years, itsuffered from more severe threat and impact from the global climate than Sudan,
and the imbalance of eco-system has not yet been fundamentally alleviated as well.
Moreover, increase in other indicators like Present value of external debt (% of GNI)
and the population of refugee by country or refuge area reflected the poor efficiency of
government's measures.
 StatusIndicators
The status indicators, except for the slight rise from 2012 to 2013, retained a
relatively stable tendency during the 5 years. What resulted in this is that most concrete
indicators involved change quite gently like forest coverage, dense of population and so
on. However, though slight, the variance still showed the rough living environment in
Egypt.
 ResponseIndicators
As shown inthefigure, theresponse indicators first experienced a comparatively
reduction inEgypt from 2012to 2013,which mainlyonaccount ofthehalving of Net
ODAreceived per capita. Withoutenough aid, itmay be muchmoredifficult for
Egyptian governments todeal withtroubles. Thereby, though contributed less compared
withother two kindsof indicators, theresponse indicators still account greatly when
evaluating thestate fragility.
5.1.2 How Climate change impacts on fragile Sudan


## 第 15 页

Team#89499 Page14of21
Applying the Gray Relational Analysis to Egypt, we determine the relationship
between climaticindicators and somesocial-economicindicators as shown in Table5.
Table5
Percapita renewable inland Cereal Prevalence of
RelationshipIndexbetweenclimaticindicatorsandsocial-economicindicators
freshwater resources production undernourishment
CO2 0.0223 0.1076 0.1431
Temperature 0.04545 0.0998 0.0879
Precipitation 0.0583 0.11415 0.11006
Land coverage 0.0282 0.08925 0.0622
ExtremeWeather 0.0368 0.0677 0.1367
From the table above, we can conclude that climatic indicators mostly impact the
prevalence of undernourishment, namely the medical condition of Egypt, since the
degree of relationship between them is relatively high on the whole. Thus, in Egypt,
climatechange mainly influences thefragility through medical condition.
5.2 The tipping point of fragility
As what illustrated in classification of fragility, the tipping point is actually the
boundary value between fragile and vulnerable. Thereby, we define the tipping point as
0.4991(valueof fragility), arriving at which means thiscountry is fragile.
After that, we adopt Multi Factor Line Regression Method to predict when Egypt
would become a fragile country as defined, by forecasting indicators including the
population of refugee by country, precipitation, density of population, health condition,
etc. The outcomeis shown in Figure11 as follows.
PredictionofFragilityinEgypt
0.6
0.5
0.4
0.3
0.2
0.1
0
201720182019202020212022202320242025202620272028Year
StressIndicators StatusIndicators ResponseIndicators Fragility
Figure11
As indicated in the figure, we can conclude that Egypt would arrive at a truly
PredictionofFragilityinEgypt
fragile situation in2028, after struggling for 11 years since 2017. Without additional
interventions, thistendency is unpreventablein away.
6 Intervention Plan for Better Stability
Based on our evaluation model accompanied with the cases of Egypt, we come up
with a series of interventions of two kinds, the one is to control climate change and the
otheris tostrengthen thecoping capability starting from response indicators. How these
eulaV
精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！


## 第 16 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#89499 Page15of21
interventions work has been shown through ourmodel, at thesametime, we listthe
totalcost clearly.
6.1 Interventions
6.1.1 Plan about climate control
1) Droughts, floods,extremetemperatures
Undertaking water conservancy projects is an excellent solution for droughts and
floods, since water conservancy can play a role of regulating and replenishing the water
of the river. More specifically, it is able to shut down some of the water during floods
and release the water from reservoirs to ease the drought. Additionally, returning
farmland to forestry or grassland is also recommendable, since trees and grass can
conserve part of water.Thereafter, reducing carbon emissions and slowing the warming
oftheearth may be effectiveways tomitigate extremeweather.
2)Totalgreenhousegas emissions (ktofCO2 equivalent)
The CO2-concentration is one of the most decisive indicators of global warming,
thus reducing it is also capable of dampening the environmental degradation. Multiple
means can be effective for that, like modifying technology, improving energy efficiency,
energy saving, adjusting industrial structure, the development of energy-saving and
environment-protecting industry.
6.1.2 Plan about coping ability
1) Economic capability
 Optimizationandupgrading ofindustrial structure
For the purpose of improving economic capability, industrial structure is in need of
optimizing and upgrading. Governments should better speed up transformation and
upgrading of traditional industries, deepen the integration of informatization and
industrialization, strive to foster strategic emerging industries, and actively cultivate
new formats and new business models and build a new system for the development of
modern industry. In the final analysis, the competition of comprehensive national
strengthis a competition of innovation. Thereby, it is necessary to further implement the
innovation-driven development strategy and promote scientific and technological
innovationof all kinds.
 Develop advantageouslocal industries
Starting from local reality, it is of great help and significance to take market as
guideline and develop economy with special characteristics through suitable measures
with local conditions. In this way, the local conditions for readjusting production
structure, increasing income and enhancing product competitiveness can be benefited
[5].Multiple countermeasures include combining local advantageous with market
requirement and develop industry and product withspecial characters.
2) Forhuman resourcesand socialsecurity
 Promote catastropheinsurance
In allusionto Insurance andfinancial services (% ofservice imports, BoP), ithelps if
catastrophe insurance can bepromoted and applied widely in a country. Catastrophe isa


## 第 17 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#89499 Page16of21
less frequent but destructive risk. Government and insurance industry should strengthen
catastrophe risk prediction and early warning, as well as catastrophe risk management,
building effective catastrophe prevention system and catastrophe compensation
mechanism as soon as possible[8].
3) Infrastructureandtechnicalsecurity
 Augmentrailroadingand peacekeeping
The contradiction between the shortage of energy resources and the deterioration
of the environment has forced many countries to re-understand the importance of
accelerating the development of the railway [9]. Moreover, for war zones, peacekeepers
work as an important source ofsecurity safeguard.
6.2 Costbased on Egypt
Take Egypt as example, we analyze and estimate the total cost of above
interventions, listed inTable6below.Somecalculation formulas are listed as follows.
Table6
Measure Cost
Interventionsandthecost
CatastropheInsurance 50,000,000dollars
Peacekeepers 70,000dollars
Education 40,000,000dollars
Railroading 460,000,000dollars
Medical treatment 50,000,000dollars
EconomicTransition 500,000,000dollars
Climaticimprovement 20,000,000dollars
TotalCost
1,120,070,000dollars
The cost of education is derived by increasing the expenditure on education of
Egypt from 375 million to 400 million, similarly, the cost of medical treatment is
derived by increasing the health expenditure (% of GDP) from 5.64 to 5.8. And for
railroading, we obtain the cost through increasing the mileage by 3%. These changes are
reasonablewith related theoretical support.
Furthermore, the total cost makes up for almost 3.365% of the GDP in Egypt, in a
rational range. Therefore, our interventions are feasible without too much financial
burden.
6.3 Effects of interventions
Simulating the implement of interventions on Egypt through our evaluation model,
weobtain theeffects ofinterventions as shownbelowin Figure 12.


## 第 18 页

Team#89499 Page17of21
FragilityinEgyptBeforeandAfterInterventions
0.6
0.55
0.5
0.45 Before
0.4
After
0.35
0.3
Figure12
It can be included that our interventions enable the declination of fragility by
FragilityinEgyptBeforeandAfterIntervention
almost8.93% on average, which further testifies that the impact of climate change is
mitigated and thecoping capabilityof Egypt.
7 Modifications for regions of different sizes
7.1 Inapplicability of model for smaller or larger states
1) Forsmaller regions likecities
It is not so suitable to apply our model to evaluate the fragility of such a small
region like a city. First, some indicators in the existing model may be unavailable. For
example, indicators such as long-term foreign debt and CPIA are utilized to evaluate the
condition of a country, which may be less meaningful for a city. Second, we regard a
country as a politically and economically independent entity, whereas cities are not of
this nature. A city is influenced by national policies and other factors and then the
fragility increases or decreases. For example, some countriestend to call various
resources to maintain the stability ofitseconomic and political center, which leads to a
less fragile area.
2) Forlarger regions likecontinents
In terms of stress indicators, situation of a continent is more complicated than a
country. For example, Asia stretches across the tropical climate, the temperate zone and
the frigid zone, which means that directly measuring the climatic indicators of a
continent is too rough to measure the risk of becoming fragile.In terms of status
indicators, the situation of ethnic groups and religions in a continent is more complex
than a country as well. Diversity of national system and strong independence among
countries exist. For some indicators we use in the model like per capita arable land, the
differences of countries are not taken into account if arable land is directly averaged. In
terms of response indicators, when it comes to economic capability, countries with
steady economic base may be very sound, boosting the economic ability of the entire
continent todeal with thefragile factors deviating from reality.
7.2Modifications for regions of different size
ytiligarF
精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！


## 第 19 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#89499 Page18of21
1) Forsmaller regions likecities
When specific to a city, the overall framework of our model can maintain, that is,
the categories of indicators including stress, status and response indicators and
weighting to get the fragility of the region. For some national-level indicators, use the
corresponding indicators at the regional level instead. When considering the response
indicators, it is not feasible to consider the indicators of the city only, but such
indicators as the country's ability to respond to the policies of the region and the country
should be included.
2) Forlarger regions likecontinents
A continent is composed of various countries. Therefore, existing models can be
used to count the degree of fragility of each country within a continent. Then based on a
country's population, territorial area and other indicators, the analytic hierarchy process
can be applied to determine the weight of each country. Finally, we can obtain the
fragility of a continent through the sum of themultiplication of fragility and the weight
ofeach country.
8 Strengths and Weaknesses
8.1 Strengths
1) Comprehensiveandmostly objective indicators aboutfragility.
While searching for and selecting indicators about agility for its equation, we
consider as comprehensively and meticulously as possible. Both indicators relevant with
climate change and other irrelevant indicators like GDP are considered. Moreover, most
of the indicators are selected as per what Fragile State Index takes into account, which
means that ourmodel is onavalid, significative basis.
2) Comparatively correct results ofthemodel.
With restricted number of indicators and data, the fragility rank of our model is still
similar to that of Fragility State Index proposed by the Fund for Peace. Particularly, the
impact ofclimatechange is highlighted inthe results, which is novel and valid.
3)Extensiveevaluation indexsystem.
In our model of fragility, according to the "stress-state-response" framework,
indicators are selected from three aspects including risk degree, sensitivity and
vulnerability .The comprehensive evaluation index system is designed this way,
reflecting the fragility of the country, the sensitivity of the state to risks and the
capabilityto deal with therisk.
8.2 Weaknesses
1)Subjectivity and Limitation in theProcess ofSelecting theIndicators.
Although referring to other related literature as well as the factors involved in
Fragile State Index, we still select the indicators with kind of subjective concept. This is
unavoidablewithout enough literature.
2) Imprecise Classificationof Fragility.
Our classification of fragility, namely the range of fragile, vulnerable and stable, is
based ontheoutcome of30selected countries in section3.5.1. Thelimited numberof


## 第 20 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#89499 Page19of21
countries restricts theaccuracy of theclassification, even ifwe apply theDiscrimination
Analysis forbetter classification.
3) NotAll-inclusive Analysis ofSudan andEgypt.
In the analysis of Sudan and Egypt, we only assess the fragile condition for 5 years
from 2012 to 2016, the date for which is rather restricted. In that way, our results of the
analysis are not comprehensive and precise enough to represent the fragility of the two
states.
9 Future work
As discussed in the weaknesses of the models, multiple possibilities exist for the
development of a more precise form of our model. Therefore, in the future, a more
comprehensiveand definitivemodel would be developed in thefollowing ways:
1) More precise andcomprehensive data
Our model is built and analyzed based on the assumption that all of our collected
data is all reliable due to the limited time, which is relatively inconsistent with the real
world. Therefore, more dependable and realistic data corresponding to the real world is
ought tobeacquired bymorecareful researching.
2) Considerspecialcountries
In particular countries where an indicator may so extreme that leads to the collapse
of the entire country,failing to guarantee the basic livelihood ofpopulation. For instance,
the extreme lack of water resources may have a significant impact on the country's
fragility, while in the future work we may not include the country in the list of fragile
regions. We can define a normalized value of each indicator as a critical point that
seriously limits people's livelihood security. If this value is reached, the basic living
conditions of population in the country would be severely restricted and the fragility
would begreatlyenhanced.
3)Consider thecoupling relationshipbetween climate andsocio-economicactivities
The mutual influence is bound to exist due to the coupling relationship between
climate and socio-economic activities. Our model, with climate runs through the model
as the starting point, only takes into account a series of indirect and direct impacts of
climatethat onlystarting from climate. Therefore, it isnecessary to consider the
couplingrelationship between climateand socio-economic activities inthe future.
10 Conclusion
To conclude, we first establish a comprehensive evaluation model based on the
PSR model and Entropy Weight Method, so as to represent the fragility
quantificationally. Furthermore, we apply Discriminant Analysis to determine the range
of fragility for fragile, vulnerable and stable states respectively. Test of 30 countries
shows that ourmodel isrobust and correct.
Thereafter, we implement model instantiations on Sudan, an extremely fragile state,
and Egypt, a relatively not so fragile state. It can be illustrated from the results that the
climate changemainly influences fragility through food security in Sudan and through
medical condition in Egypt. Without the impact change the fragility of Sudan would be
alleviated. After that, we define thetippingpoint as 0.4991(value offragility) and


## 第 21 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#89499 Page20of21
completepredictions, deriving that Egypt would become afragile country.
Then we put forward a series of interventions about mitigating climate change and
improving coping ability,as well as the cost based on our model. Our interventions are
able to mitigate the influence of climate change and further contributes to the stability of
a state. At last, we modify our model to be applicable to smaller cities and larger
continents better through substituting some original indicators while maintaining the
framework.


## 第 22 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#89499 Page21of21
References
[1] Team N A S. Climate change impacts on the United States: the potential
consequences of climatevariability and change.[J]. 2001, 336(6077):10-.
[2] Liu Yang.Study on the socio-economic impact of global climate change on the
estuary ofthe Yangtzeriver delta[D]. East Chinanormaluniversity.2014.
[3] David Marsden. Deconstructing Development Discourse: Buzzwords and
Fuzzwords[J].Development in Practice, 2007, 17(4-5):471-484.
[4] Rüttinger L, Stang G, Dan S, et al. A New Climate for Peace – Taking Action on
Climate and Fragility Risks. Executive Summary[J]. British Heart Journal, 2015,
38(8):877-877.
[5] Mata J F, Ziaja S. Users’ guide on measuring fragility[J]. Country Indicators for
Foreign Policy, 2009.
[6] Feng Shan and Xu Changle.Summary of Development of Global Climate Change
and Its Effects on Social Economy[J]. China Population Resources &
Environment, 2014. v.24;No.165(s2):6-10.
[7] Ai Yunhang.To Give Full Play to The Advantages of Resources In Mountainous
Areas, To Vigorously Develop Economy with Special Characteristic[J].Chinese
Journal ofAgricultural Resources and Regional Planning.2005,26(2):38-42.
[8] Wang He. Reflections on the Establishment of Catastrophe Insurance System in
China[J].ChinaFinance. 2005(7):50-52.
[9] Liu Zhijun. Recognizing the current situation and pushing forward the
harmonious development of railway construction to achieve the sound and rapid
development ofrailways[J].Railway Economics Research.2007 (1):18-33.

# B79002-How many languages


## 第 1 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
TeamControlNumber
Forofficeuseonly Forofficeuseonly
T1 79002 F1
T2 F2
ProblemChosen
T3 F3
B
T4 F4
2018
MCM/ICM
Howmanylanguages?
To predict the number of the one language, we assume that native speakers are related to natural growth rate of its native
speaker and number of the its second speakers. Based on the data we collected, we use time series languages speakers
difference equation model to describe the dynamic change of both native and second language speakers, considering the
influenceofforeignlanguagetaughtinschool,socialmedia,economics,culturalcommunicationandsoon.
Thedifferenceequationmodelcanapplyourcollectedindicatorstothepredictionofchangeoflanguagedistributionover
time.50yearslater,top10languagesinorderoftotalspeakerschangefrom[Mandarin,English,Hindustani,Spanish,Arabic,
Malay,Russian,Bengali,PortugueseFrench]to[Mandarin,English,Spanish,Hindustani,Arabic,Bengali,Portuguese,Malay,
Russian,French];therankoftop10nativelanguagesspeakerschangesfrom[Mandarin,Spanish,English,Hindustani,Arabic,
Bengali,Portuguese,Russian,Punjabi,Japanese]to[Mandarin,Spanish,English,Hindustani,Arabic,Bengali,Portuguese,
Punjabi,RussianandHausa].Byanalyzingthesechanges,wefindsomereasonableexplanations,suchastherapidnatural
growthrateofsomedevelopingcountriesandsomelanguages’increasingspeaking-power.
Given the global population growth and migration pattern, we establish geographical distribution of difference equation
model,topredictthegeographicaldistributionofdifferentlanguages.Throughtheestablishmentofthedifferenceequation,
weconsidertherelationshipbetweenthedistributionoflanguagesondifferentcontinentsandmainmigrationroutes.Weuse
MATLAB to calculate language proportion changes on each continent over the next 50 years, finding some reasonable
predictions. For example, Mandarinwill become the No.2 native language inNorthAmerica andAustralia. The proportion
ofMandarinandArabicspeakersinEuropewillincreasesignificantly.
InPartII,basedontherequirementandthefeatureofservicecompany,wechoosesixsuitablecitiesbasedonourprediction
oflanguage speakers. Also,we findthat thecities are differentdependingonwhether the companyis long-termoriented(6
suggestedcities:Shanghai,NewYork,Calcutta,Madrid,Dubai,andRiodeJaneiro)orshort-termoriented(6cities:Shanghai,
NewYork,Calcutta,Madrid,Dubai,andSingapore).
Moreover, we build the cost-benefit analysis model to calculate the suitable number of offices that this company should
build.Giventhelevelof company’s profitabilityandcost,we seta newparameter, cost-profitabilityratio.If thevalue ofc-
pratioislessthan281,wethink6officesshouldbebuilt.Ifthevalueofthisratioisbetween281and422,wethink5offices
shouldbebuilt.Ifthevalueisbetween422-527,4officesarebest;ifitisbetween527and544,3officeshouldbebuilt;if>
544,weshouldonlymaintaintwooffices.
Finally,weanalyzetheperformanceofourmodelandthesensitivityofourmodel,provingthatourmodelisrelativelystable
fordifferentparameters.
Key words:Language distribution,TimeSeries Difference Equation Model, Dynamic simulation,siteselection
Cost-profitanalysis


## 第 2 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#79002 Page1of29
CONTENT
1 Introduction.................................................................................................................................................2
1.1 ProblemBackground....................................................................................................................2
1.2 Ourwork.......................................................................................................................................2
2 AssumptionsandSymbols..........................................................................................................................2
2.1 Assumptionsoftheinitialdata.....................................................................................................2
2.2 Symbols and definitions...............................................................................................................3
3 PartIModelsandResults...........................................................................................................................4
3.1 Model I:Various Languages Speakers Difference Equation Model............................................4
3.1.1 Theincreaseofthenativespeakers................................................................................................4
3.1.2 Theincreaseofthesecondlanguagespeakers...............................................................................5
3.1.3 ThetotaldifferenceequationofmodelI........................................................................................8
3.2 Model IResults&Analysis.........................................................................................................8
3.2.1 Initialrankandparametersetting...................................................................................................8
3.2.2 Results&Analysis.........................................................................................................................9
3.3 Model II:Geographical Distribution Difference Model............................................................10
3.4 Populationgrowth fitting andcurrent migration pattern............................................................11
3.5 Theincrease speakers ofeach languageoneach continent........................................................12
3.6 Resultand Analysis....................................................................................................................13
4 PartIIModels&Results..........................................................................................................................15
4.1 Assumptionsabout theservice company...................................................................................15
4.2 Explanation aboutour choices...................................................................................................15
5 SensitivityAnalysis....................................................................................................................................17
5.1 sensitivityanalysis ofModel I....................................................................................................17
5.2 sensitivityanalysis ofmodel II...................................................................................................19
6 StrengthandWeakness.............................................................................................................................20
7 Memo..........................................................................................................................................................21
8 Appendix....................................................................................................................................................22
8.1 data.............................................................................................................................................22
8.2 program......................................................................................................................................24


## 第 3 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#79002 Page2of29
1 Introduction
1.1 ProblemBackground
In the world of globalization, number of native speakers and L2 speakers of a certain language increase or
decreaseovertime.Therearemanyfactors thataffecttheincreaseordecreaseofacertainlanguage,including
theforeignlanguage taught inschool,culturalcommunicationandassimilation,EconomicFactor,technology,
socialmediaandsoon.
Our first task is to establish a model of the distribution of various language speakers over time, in which we
shouldconsiderthefactorlistedabove.
Besides,oursecondtaskistheestablishamodeltopredictthegeographicdistributionsoftheselanguagesover
timebasedonthegivenglobepopulationandhumanmigrationpatternsforthenext50years.
In the partII, alarge multinationalservice company hire ourteam togive locationoptionsfor newoffices. So
ourthirdtaskistoconsiderwhereweshouldlocatetheseofficesandifopeninglessthansixofficesbetter.
1.2 Ourwork
Languageissuchanimportanttopicduetoitsroleinculturalcommunication,internationalbusiness,migration
issue and so on. Under the circumstance that we are consulted to give out 6 most suitable sites to build new
officebyaservicecompany,ourmainworkisasfollows:
Firstly, based on the data we collected, we use time series languages speakers difference equation model to
describethedynamicchangeofbothnativeandsecondlanguagespeakers,consideringtheinfluenceofforeign
languagetaughtinschool,socialmedia,economics,culturalcommunicationandsoon.
Secondly, considering the global population growth model and migration patterns, we establish geographical
distribution difference model, presenting the change of languages’ distribution in 6 main continents over 50
years.
Thirdly, we choose the sixsuitable cities based on our prediction of language speakers. Also, we find that the
citiesaredifferentdependingonwhetherthecompanyislong-termorientedorshort-termoriented.
Moreover,webuildthecost-benefitanalysismodeltocalculatethesuitablenumberofofficesthatthiscompany
shouldbuild.
Finally,weanalyzetheperformanceofourmodelandthesensitivityofourmodel.
2 Assumptions and Symbols
2.1 Assumptionsoftheinitialdata
1. Those languages whose current total speakers are less than 100 million won’t become the top 10
languages. Thus, according to the list of languages by total number of speakers, we only use the data of
top16languages,sincetheyaretheonlylanguagesthatareusedbymorethan100millionpeople.[1]
Reason: The French ranked 10th in 2017 with a total number of 228million speakers. According to common
sense,total number ofLanguage speakershave asmall possibilitytodecrease.So,those languages withfewer
than100millionspeakersarelesslikelytobecomeTop10in50years.Atthesametime,wealsodothistoreduce
ourcomputationalloadandtoreduceourprogrammingdifficulty.
2.ForsomeLanguagesL2speakersnumber‘?’inthe[1],weassumeitiszero.


## 第 4 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#79002 Page3of29
Reason:Wespeculatetheremaybetworeasonsforthecomingof ‘?’.Oneisbecausethedataistoosmall,not
good statistics. The other reason is that it is controversial to define who can be the second foreign language
speakers.Forbothreasons,wecanallassumethenumberiszero.
3.Wethink native speaker's growth is only related to its own natural growth rate and second language
population
Reason:Accordingtoourcommonsense,thegrowthofnativespeakersisoftenassociatedwithchangesinthe
localpopulation.Localpopulationgrow,native speakers alsowillgrow.Foreigners migrate in,andtheforeign
languagenativespeakersincrease.Therefore,nativespeakerchangesandpopulationchangesareveryrelevant.
And in order to simply our model, we think native speaker's growth is only related to its own natural growth
rateandsecondlanguagepopulation.[2]
4.We think L2 speaker’s growth is only affected by its own feature (the languages learned in school,
cultural communication) and the global situation (economics, development of technology, media use).
Andtherelationshipbetweenthemisdirectlyproportional.
Reason:Accordingtocommonsense,thesefactorspositivelyaffectstheL2speaker’sgrowth.Althoughweare
notquitesurewhethertherelationshipbetweenthemislinearornot,inordertosimplifytheproblem,wemay
thinkthattherelationshipbetweenthemislinear,andtherefore,proportional.
2.2 Symbols anddefinitions
i 1 2 3 4 5 6 7 8
Table2codesfortop16languages
Languages Mandarin English Hindustani Spanish Arabic Malay Russian Bengali
i 9 10 11 12 13 14 15 16
Languages Portuguese French Hausa Punjabi German Japanese Persian Swahili


## 第 5 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#79002 Page4of29
3 Part I Models and Results
3.1 ModelI: VariousLanguages Speakers DifferenceEquationModel
Howtoquantifytherelationshipbetweenlanguagegrowthandthevariousfactorsisadifficultproblem?There
are a variety of time series models we could use. If we have enough data, we can regress the functional
relationshipbetweenthenumberoflanguagesonvariousfactors.Butthetruthis,wecan’tfindenoughcredible
data online. There are two reasons for this. One is because it is vague to judge whether a person has a second
foreign language ability.For this reason, different data sources may not come from the same criterion. So the
data betweenthe two will be very different. In addition,the twodata whose sources are the same, while years
aredifferentarestillnot credible.Thisis because the datesof the censuses varyfromcountrytocountry. This
makesalotofdatadoesnothavetimecontinuity.Forthesetworeasons,wecan’tandwillnotusethosemethods
offittingforecasts.
Differenceequationmodelcanconsidertheimpactofdifferentfactorsonthesizeoftheindependentvariables.
Moreover, the difference equation model only requires the initial data on it. These two characteristics fit very
wellwithourproblem.Thetimestepinwhichwesetinthedifferenceequationisoneyear.Wedenotethatthe
numberofnativespeakersoflanguageiinnextperioddependsonthecurrentnumberofitsnativespeakersand
the current number of its 2ndlanguage speakers. Therefore, we can construct a difference equation model to
describethechangeof2typesspeakersforthe16languages.
3.1.1 Theincreaseof thenativespeakers
According to our common sense, the growth of native speakers is often associated with changes in the local
population. Local population grow,and native speakers also will grow.Foreigners migrate in, and the foreign
languagenativespeakersincrease.Therefore,nativespeakerchangesandpopulationchangesareveryrelevant.
So, we assume that native speaker's growth is only related to its natural growth and the number of second
languagespeakers.Wechoosetheweightedaverageofnaturalgrowthrateofcountrieswhoseofficiallanguage
isthelanguageiastheincreaseofthenativespeakersoflanguagei.
However, the world population growth pattern varies from countries. The most significant difference is the
differencebetweenthepopulationgrowthpatternsindevelopinganddevelopedcountries.Therefore,wedivide
these languages into two group. One type is mainly spoken in developed countries, and the other is mainly
spokeninthedevelopingcountries. Developedcountriesusuallyhave lownaturalpopulationgrowthrates and
highimmigrationrate while developingcountries usuallyhave higher naturalpopulationgrowthrates.Totake
this difference into consideration, we divide all 16 languages into 2 types, according to their main speakers’
types—developedordeveloping.
Table3 typesoflanguages
types languages
TypeI:mostspokenindevelopedcountries English,Spanish,French,German,Japanese,
Mandarin
TypeII:mostspokenindevelopingcountries Hindustani,Arabic,Malay,Portuguese,Hausa,
Punjabi,Persian,Swahili
TypeIlanguages’speakers’growthmodel:Malthusiangrowthmodel
TypeIlanguagesaremainlyspokenindevelopedcountries,whosepopulationusuallyhaveaverylownatural


## 第 6 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#79002 Page5of29
growth rate, such as 0.5%, or even a negative value. Its population growth rate mainly depends on the
immigration, while the next generation of those immigrants usually have to learn the local language as their
mothertongue.
Forthistypecountries,wecanconsideritasaconstantrate,r,overthenext50years.SoweusetheMalthusian
growth model to measure the number of native speakers[4]. According to Malthusian growth model, the
populationgrowthrate,r,doesnotchangeovertime.Therefore,thepopulationinyeart+1couldbewrittenas:
（1）
denotes the number of native speakers of language i in year t; denotes the natural speaker growth rate
  ( +1)−  ( )=  ( )   +  ∙  ( )
x
oif
(
l
t
a
)
nguagei;Rdenotesacoefficientthatexplainstheproportionof2
ri
ndspeakersofthislanguageinyeartthat
turnsintonativespeakerinyeart+1.Later,wewilldosensitivityanalysisforthiscoefficientR.
TypeIIlanguages’speakers’growthmodel:LogisticGrowthModel
TypeIIlanguagesaremainlyspokenindevelopingcountries,whosepopulationusuallyhavearelativelyhigher
natural growth rate, such as 2%. Nevertheless, we cannot use this number for the next 50 years, since their
populationcannotmaintaingrowingsofast.Tomake amorerealisticanalysis,weuseLogisticGrowthModel.
LogisticGrowthModelisaslightmodificationofMalthus’smodel.Itpointsthatthepopulationgrowthrateis
not constant—there is a limited carrying capacity of the environment, resulting in a stable population over
time[5].
AccordingtoLogisticGrowthModel,thepopulationinyeart+1couldbewrittenas:
3.1.2 Theincreaseof thesecond languagespeakers
When discussing the change of 2ndlanguage speakers, we believe it is mainly affected by two major factors.
Firstly, it is affected by its own feature, such as region, difficulty, promotion by the government, cultural
communication, etc. Secondly, it is affected by the global situation, such as economics, development of
technology,etc.
3.1.2.1 Effectofthelanguageownfeatures
 theforeignlanguagetaughtinschool[3]
Weassume that the language promoted by the government is the foreign language taught in school. For
example,Englishistaughtinmanycountriesasstudents’mainforeignlanguagebecauseofEnglish’swide
spread and use in the world. Although statistics are incomplete in some developing countries, we only
found data of some developed countries. However, we think this promotion of language in education is
related to the power of the language itself, which means the number of L2 speakers. Therefore, we use
availabledatatomakeupforthemissingdata.


## 第 7 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#79002 Page6of29
For example, when i refers toFrench and j refers to English, is the percentage of French taught in
school as a foreign language in English-speaking countries. is the coefficient to measure how much
langTij
thisfactor(thelanguagetaughtinschool)willinfluencetheincreaseof2ndlanguagespeakersoflanguage
k1
i.Laterwewilldosensitivityanalysisfor
k1.
Figure1Theforeignlanguagestudiedinschool,takingU.S.forexample
 Culturalcommunication&assimilation [6]
Manyreports state that cultural communication and assimilation play a significant role in the increase of
2nd language learners. However, how to quantify cultural exchange is a very difficult issue. In order to
solve this problem, we propose two factors that will affect cultural communication. The following are
two effects:
NeighborhoodEffect:Ifthespeakersoftwolanguageliveneartoeachother,itismorelikelyforthemto
haveculturalcommunication.Andtherefore,theywouldbecomemorelikelytolearnneighbors’language
astheir2ndlanguage.
Figure2Theneighborhoodeffectamongthetop16languages
(thetwolanguagehavingalinelinkedmeanstherewillbeNeighborhoodeffectbetweenthem)
Policy-led Effect: When the home country of language speakers is strongly promoting the country's
relations with some special countries, the likelihood of those languages learning from each other's
languages will also increase, such as China's the Belt and Road Policy making it more motivated for the
peoplealongthepolicytolearnChinese.Forexample,PakistanusesChineseasitssecondlanguage.


## 第 8 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#79002 Page7of29
The power of these two effect is positively related to the population of language speakers, ,
andtheculturalcommunicationbetweentwolanguages.Wegetthefollowingequation:
xi( ) ∙   ( )
16
Δi,cult=k2∙∑ 퐶ｸ⎋  , ∙  ( )∙  ( )
describes the extent of cultural exchangje=b1etween language i and language j; is the coefficient
tomeasurehowmuchthisfactor(theextentofculturalcommunicationandassimilation)willinfluencethe
culti,j k2
increaseof2ndlanguagespeakersoflanguagei.Laterwewilldosensitivityanalysisfor .
3.1.2.2 Effectoftheglobalsituation k2
 EconomicFactor
Differentlanguages havedifferentspeakingpowerintheglobalbusiness environment. Themorepowerit
has,themorepersonschoosetolearnit.ThroughtheGDPcontributedbydifferentlanguages[SeeFigure
3],wegivedifferentweighttothetop16language.
Eco is the economic power of language i. describes how much the economic factor motivates people
Δi,Eco =푘3 ∙퐸th 
tolearnlanguageiastheir2ndlanguage.Laterwewilldosensitivityanalysisfor .
i k3
k3
Figure4GDPcontributedbylanguage
 theupdateoftranslationsoftwaretechnology
[7]
Thedevelopmentoftechnologywillmakeiteasierandfastertotranslatedifferentlanguages.Weassume
thevelocityoftranslationsoftware’supdaterateisconstant.Therefore,itwillhaveanegativeimpacton
thenumberof2ndlanguagelearners.ThisfactorwillinfluencetheincreaseofL2speakersoflanguageias:
Cisthevelocityoftechnologydevelopment. describesthechangeof2ndlanguagelearnerinfluenced
Δi,Tech = k4c (c>0, k4 < 0)
bythedevelopmentoftranslationsoftware.Laterwewilldosensitivityanalysisfor .
k4
 thepushofnetworkandsocialmedia
k4
Thoughtherearethousandsoflanguagesallovertheworld,only5%ofthemareusedwidelyintheinternet.
54.5%ofallwebcontentisstillinEnglishdespitehugegrowthinusersthatdonotunderstandEnglishor
who prefer to access content in their native languages. Due to analysis of the most popular 10 million
websites by W3techs, after English, the most common languages are Russian (5.9%), German (5.7%),
Japanese(5.0%),andSpanish(4.7%).[8]
Dataalsoshowusthatthenumberoflanguagesusedbymainstreamsocialmedias,suchasFacebook,
TwitterandLinkedInislimitedtofewlanguages.


## 第 9 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#79002 Page8of29
Figure5languagesintheinternet(left) &thepressureofmainstreamwebsite(right)
Wecanexpressthepoweroflanguageinthenetworkasfollows:
[9] [8]
describesthepoweroflanguageiintheinternet. describesthechangeof2ndlanguagelearner
Δi,Net=푘5∙푁‸  
influencedbythepushofinternetandsocialmedia.Laterwewilldosensitivityanalysisfor .
k5
k5
3.1.3 Thetotal difference equation ofmodel I
3.2 ModelI Results &Analysis
3.2.1 Initialrank andparametersetting
Inthesectionabove,we builda differenceequationmodel,whichcouldpredictthenumberofnative speakers
and second language speakers in the following years. We get the initial rank by total language speaker[1]. It
represents the numbers of native speakers and second language speakers of different languages in 2017. And
hereistheinitialdata:
Rank Language L1speakers L1Rank L2speakers L2Rank Total
Table4Theinitialrankbylanguagesize[1]
1 Mandarin 897 1 193 4 1090
2 English 371 3 611 1 982


## 第 10 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#79002 Page9of29
3 Hindustani 329 4 215 2 544
4 Spanish 436 2 91 8 527
5 Arabic 290 5 132 6 422
6 Malay 77 15 204 3 281
7 Russian 153 8 113 7 267
8 Bengali 242 6 19 13 261
9 Portuguese 218 7 11 15 229
10 French 76 17 153 5 229
11 Hausa 85 11 65 10 150
12 Punjabi 148 9 ? ? 148
13 German 76 18 52 12 129
14 Japanese 128 10 1 19 129
15 Persian 60 25 61 11 121
16 Swahili 16 26 91 8 107
Accordingtothedatawecollectedin[1,4-7,9],wecansetindicesintheformula(4)andformula(5).The
indicesaregivenasfollows:
Index
Table5Indicessetting
value k1 k2 k3 -k0.43 0k.52
1 1
Lang0u.2age’s Language’s
L23le0a0rner C9u0l0tu0r0al Technology
Explanation powerin powerin
condition communication factor
business internet
Theseparametersinourvariouslanguagesspeakersdifferenceequationmodelaregivenbyourestimate.We
willdosensitivityanalysisforthemtojudgeifthechangeofL2speakerswillbesensitivetotheseindices.
3.2.2 Results &Analysis
AfterinputtingtheinitialvalueandindicesinMATLAB,wegotthenewrank:
rank Languages L1speakers L1rank L2speakers L2rank Total
Table6Thepredictedrankbylanguagesizeafter50years,Unit:million
1 Mandarin 1119.9556 1 397.2715 2 1517.227
2 English 625.07569 3 752.60658 1 1377.682
3 Spanish 714.54914 2 232.09149 7 946.6406
4 Hindustani 437.73828 4 322.65571 3 760.394
5 Arabic 410.4004 5 235.69087 5 646.0913
6 Bengali 337.48877 6 112.72084 13 450.2096
7 Portuguese 306.72269 7 101.83735 14 408.56
8 Malay 121.75222 11 269.89281 4 391.645
9 Russian 159.65859 9 187.58738 8 347.246
10 French 109.24506 13 234.28833 6 343.5334


## 第 11 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#79002 Page10of29
11 Punjabi 226.42109 8 78.858666 15 305.2798
12 Hausa 133.98132 10 132.39229 10 266.3736
13 Persian 87.30792 14 122.95997 12 210.2679
14 German 81.926176 15 125.04862 11 206.9748
15 Japanese 121.48183 12 71.268763 16 192.7506
16 Swahili 26.054248 16 145.23578 9 171.29
ThetoptenoftotalspeakersvaryfromMandarin、English、Hindustani、Spanish、Arabic、Malay、Russian、
Bengali、Portuguese、FrenchtoMandarin、English、Spanish、Hindustani、Arabic、Bengali、Portuguese、
Malay、Russian、French.
ThetoptenofnativespeakersvaryfromMandarin、Spanish、English、Hindustani、Arabic、Bengali、Portuguese、
Russian、Punjabi、JapanesetoMandarin、Spanish、English、Hindustani、Arabic、Bengali、Portuguese、
Punjabi、Russian、Hausa.
Comparingthetworankings,wecandraw5mainconclusions:
ThefastincreaseofMandarinL2speakers:AstheofficiallanguageofChina,atypicalrepresentative ofthe
fast-growingcountries,Mandarinhasattractedmanypeopletochooseitastheirsecondlanguage.Atthesame
time,Chinahasalsoadoptedaseriesofexchangepolicieswithothercountries,suchastheaidtoAfricaandthe
BeltandRoadPolicy,whichhasalsoenhancedtheattractivenessofChinese.
Russiantotal rankdeclines:due tothe verylownaturalgrowth rateinRussia,Russiannative speakers’ rank
declines,directlyleadingthedeclineinRussian’stotalrank.
Bengalitotalrankincrease:Bangladeshhasalarge nationalpopulationbaseandahighnaturalincreaserate,
resultinginarapidincreaseinBengalinativespeakersanditsrank.
Thelistoftop10languagesonlyhaveanintra-groupchange:Becausethereisahugegapbetweenthe10th
language(French,totalspeakers:229million)andthe11thlanguage(Hausa,totalspeaker:150million).Thegap
doesn’t disappear completely over time. But we can see from Table 7 that the top 16 list changes during 50
years.
Native speaker of Japanese decline from the top10 list: This is mainly because Japan's natural growth rate
has been negative recently. In addition, Hausa in Africa has become the 10th largest native language speaker
duetoitsrapidrateofnaturalincrease
3.3 ModelII: GeographicalDistribution DifferenceModel
As the model above established, we have established a model to measure the speakers’ numbers of different
languages over time. The model above quantifies the relationship between the trend of native speakers and
secondlanguagespeakersandSchool,migrationofculturalgroup,economics,theuseoftranslationtechnology
andsocial media. But obviously, we didnot consider the impact of geographical distribution on the language.
Thefollowingmodelspecificallyaddressesthisissue.
However, howtoputthegeographical distributionintoourmodel isa huge challenge. Wedidnot know atthe
outsetwhatamountoflanguageshouldbeusedtomeasurethegeographicdistributionoflanguages.Butaswe
looked up the data, we found that the language distribution across all continents varied greatly. Below is the
languagedistributionin2017:


## 第 12 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#79002 Page11of29
Therefore, we divide Earth language data into six continents, and each different continent has a different
Figure6Languagedistributionin2017
languagedistribution. Then,basedonthe modelingideasoftheabove model,we considerthenaturalincrease
of population on all continents on the one hand, and population migration across the other continents on the
otherhand. Thenwe create adifference equationforeachlanguage of eachcontinentover time.Thisequation
canconsidertheimpactoftheannualimmigrantpopulationonthelocallanguageandthelocallanguage'sown
internalgrowth,whichiswhatwewant.
Thefollowingsectionconsidersassumptionsabouttheworld'spopulationgrowthandthepatternofmigration.
3.4 Populationgrowthfitting and current migrationpattern
Inthefollowingsection,wewillfittheworld'spopulationdataandfindthemainmigrationpathoftheworld's
population.
AlthoughwecaneasilyfindtheworlddemographicdatafromtheWorldBank[10]from1960to2016,howto
fitthe56-yeardatatomaketheirerrorssmallerisstillaproblem.Wetriedexponentialfitting,polynomialfitting,
logisticequationfittingandsoon,andfinallyfoundthatGaussianfunctionfittingthebest.Belowisourfitting
effectandfunctionexpression.
Figure7Theregressionontheworlddemographicdata
( −2069)⁄ 2
11 ( 97.67)
N(t)denotestheworldpopulationintyears.
N(t)=1.058∗10 ∗‸
Currentglobalmigrationmodelisverycomplicated.Ifwefocusonthepopulationtransferdatainvarious


## 第 13 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#79002 Page12of29
countries, we can easily fall into too many data and can’t get the result. So, in order to simplify the world
migrationpattern,wemaywishtoconsideronlymajormigrationroutesinthecurrentworld.Thenwelookfor
themainmigrationpatterns,andtheimagebelowshowssomeoftherouteswefound.
Based on the current global migration patterns, we propose to assume the following seven major migration
Figure8Somemainroutesofglobalmigration[11]
routes. These seven migration routes are the most promising migration path we believe will be in the next 50
years. Based on the average annual data and our understanding of these routes, we make the following
assumptionsastotheproportionofthesesevenroutesinalltheroutes.
route details proportion
Table8 7mainmigrationroutes
1 ChinatoUSandCanada 20%
2 ChinatoEU 15%
3 IndiatoEU 15%
4 WestAsiatoEU 15%
5 northAfricatoEU 15%
6 LatinAmericatoUSandCanada 15%
7 ChinatoAustralia 5%
3.5 Theincrease speakersofeach language oneachcontinent
Besides, the population of immigrants will have the next generation in the destination country. Because it is


## 第 14 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#79002 Page13of29
difficult tomeasure the impact of this factor on the number of native speakers inthat country, we assume that
the annual growth of native speakers in local languages because of migrationis proportional tothe number of
immigrants,andwesettheindexis .
Thus,wehavethefollowingdifferenceequation:
k6
3.6 Resultand Analysis
Weuse MATLAB to calculate that difference equations. And the chart below is our result. In order to easily
differentiatedatachangesonallcontinents,wespecializedinconvertingdataofdifferentcontinentstopiecharts.
Figure9Thedistributionoflanguagesin6maincontinentsin2017.


## 第 15 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#79002 Page14of29
Figure10Thedistributionoflanguagesin6maincontinentsin2037
Accordingtotheabovechangesshow,wecouldfind:
Figure11Thedistributionoflanguagesin6maincontinentsin2067
1. Thedistributionof languages inAfrica,Australia, AsiaandLatinAmericadidnot change much.This
is because the linguistic changes in these two continents are mainly determined by the natural
population growth. The mode of population migration has little effect on these two continents.
(Although Africa is one of the immigrants’ exit points and Australia is one of the destinations for
immigrants).
2. The proportion of Mandarin and Spanish in the United States and Canada is on the rise. Portuguese
native speakers appear and account for a certain percentage. This is because Route 1 brings a large
number ofMandarinspeakers totheUnitedStatesandCanada, andRoute6brings alarge number of


## 第 16 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#79002 Page15of29
SpanishandPortuguesespeakers.
3. Native speakersof Arabic,Mandarin,Hindi appearinEuropeandcontinue toincrease. However,due
tothe small number of immigrants, the proportionisstill low.The language ofEurope still contains a
lotofvarieties.
4 Part II Models & Results
4.1 Assumptionsabout theservicecompany
Aservicecompanyisabusinessthatgeneratesincomebyprovidingservicesinsteadofsellingphysicalproducts.
Agoodexampleofaservicecompanyisapublicaccountingfirm.Theyearnrevenuesbypreparingincometax
returns,performingauditandassetservices,andevendoingbookkeepingwork.[12]
Basedonourunderstandingoftheservicecompany,wemakethefollowingassumptionsaboutthelocationof
thenewinternationaloffices.
1. The service company's profit is in direct proportion to the total number of languages it serves. The
morelanguagesitserves,thehighertheprofititearns.Thisisalsothemainprofitpatternofthisservice
company.
2. TheofficesshouldbelocatedintheplaceswhereEnglishiswidelyused,inconsiderationofthecrucial
roleEnglishplaysinthecommunicationbetweendifferentbranchoffices.
3. The offices tend tobe locatedina denselypopulated andeasilyaccessible metropolitan area.That is,
iftherearetwocitiesinthesamelanguagearea,weprefertochooseacitywithalargepopulationand
convenienttraffic.
4.2 Explanationabout ourchoices
Therewillnotbemajorchangesinlanguagepopulationintheshortterm.So,werefertothenumberoflanguage
speakers in 2017 when considering the short-term site selection. The top-six used languages are Mandarin,
English, Hindustani, Spanish, Arabic and Malay.The six locations are correspondingly Shanghai, New York,
Calcutta,Madrid,Dubai,Singapore.Thepopulationdensitymapandthelocationsofofficesareshownbelow:
However,whenweconsiderthesiteselectioninthelongterm,werefertotheresultsofourmodelI.Atthis
Figure12populationdensitymapandlocationsof6officesbasedondatain2017
point,thetop-sixusedlanguageshavechanged.TheyareMandarin,English,Spanish,Hindustani,Arabidand


## 第 17 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#79002 Page16of29
Bengali. However, due to its large population but underdeveloped economy in Bangladesh, the company's
service projects lack local consumer groups. So, we consider the seventh language in the projected languages
rankings–Portuguese.Therefore,wechooseShanghai,NewYork,Madrid,Calcutta,Dubai,andRiodeJaneiro
tolocatetheseoffices,arrangedinorder.
As we can see in Figure 14, Singapore is replaced by Rio de Janeiro since the rapid growth of Portuguese
Figure13populationdensitymapandlocationsof6officesbasedondatain2067
speakers.
BasedonourmodelfromPartI,hereareourresults:
Intheshortterm,wechooseShanghai,NewYork,Calcutta,Madrid,DubaiandSingaporetolocatethese
international offices.The top-six usedlanguages-- Mandarin,English, Hindustani, Spanish, Arabic andMalay
wouldbespokencorrespondinglyintheseoffices.
Inthelongterm,wechooseShanghai,NewYork,Madrid,Calcutta,Dubai,andRiodeJaneiro.Mandarin,
English, Spanish,Hindustani, Arabid andPortuguese wouldbe spoken correspondinglyinthese offices. Cost-
BenefitAnalysisModel
Wheneverestablishinganewofficeinanewlocation,thecompanywillhaveawiderrangeofconsumergroups,
andthusmorerevenue.Butatthesametime,buildinganewofficealsocostsalot.Accordingtothegeneral
equation,weneedtoclarifythesourceofcompany’srevenueRandcostC.
Since English is a necessary language, we used the number of the most popular language speakers except
Benefit= Revenue−Cost
English in that region, to judge the company's profitability when we set up our Cost-Benefit Analysis model.
HerewegivesomeAssumptionsasfollows:
 R(TotalRevenue)ispositivelyrelatedtothecompany’sprofitability,whichisαC(TotalCost)isafix
numberineachplace.WeassumethecostofbuildinganewofficeisaconstantC.
So,wehavetheequation:
Pop( ) is the number of speakers of top10 languages except English in . Because we use pop( to
Profit (cityi)=α∙pop(cityi)−퐶
describethepowerandpopularityoflanguagei,wecouldletthenumberoftotalspeakerstoroughlyrepresent
cityi cityi cityi)
it.
Wehavecalculatedthemostsuitablecitiesin4.1.TherankisinTable9
Rank 1 2 3 4 5 6
Table10Themostsuitablecities
City Shanghai NewYork Madrid Calcutta Dubai Singapore
Note:1.ShanghaiandNewYorkisthetwoofficewealreadyhave.
2.Weusethedatacollectedin2017ratherthanthepredictedvaluefor50yearslater,becausethecompany
willconstructthe6newofficenowbutnot50yearslater.


## 第 18 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#79002 Page17of29
Tocalculatetheprofit-maximizeofficeamount,weneedtoasksomeadditionalinformationfromourclient
company,whichistheexactvalueof andC,fromthecompanytomeasureitsprofitability.
For wehaveajudgementtodeterminewhetherweshouldsetupanofficehere:
α
cityi,
C/ measuresthecompany’sabilitytoturnthecostintoprofit,wecallitcost-profitabilityratio,orc-pratio
inshort.
α
GivendifferentvalueofC/ ,wecangivethefollowingsuggestions:
α
C-pratio(unit:million) TabNleu1m1bHeorwofmoafnfiycoesfficesshouldthecompanysetuCp?ity
[544.982) 2 Shanghai,NewYork
[527,544) 3 Shanghai,NewYork,Madrid,
[422,527) 4 Shanghai,NewYork,Madrid,Calcutta
[281,422) 5 Shanghai,NewYork,Madrid,Calcutta,Dubai
Shanghai,NewYork,Madrid,Calcutta,Dubai,
[0,281) 6
Singapore
Therefore,giventheadditionalinformationof andC,wecanhelpthecompanytodecidehowmanyoffices
theyshouldbuild.
α
5 Sensitivity Analysis
5.1 sensitivityanalysisofModelI
The purpose of our Model I was to get the change of Top10 language of the most native speakers and total
speakersforthenext50years.Butifyouuserankingsasthedependentvariableforoursensitivityanalysis,we
think the result we got must be insensitive, and the rank remain the same, because the Independent variables
changelittle,andtherankisadiscretedata.SowewanttochooseoneofthemodelI’sresultdata asourother
dependent variable. For example, we choose the number of Mandarin second language speakers in 50 years
laterasourobservedvariables.Thefollowinganalysisistoconsiderthesensitivityofthisvariableundersmall
changesinbelowparameters.
1.natural increaserate
WeenterdifferentnaturalgrowthratesofMandarinintotheprogram,andwegetdifferentMandarinL2speakers
number.Hereistheresult:
naturalincreaserateofMandarin 0.34 0.44 0.54
Table12Sensitivityanalysisonnaturalincreaserate
thenumberofMandarinL2speakers 386.34 397.27 403.18
sensitivity 0.093256475


## 第 19 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#79002 Page18of29
The Sensitivity Index shownabove means that whenthe natural increase rate increased by 1%,the number of
MandarinL2speakerswillinturnincreaseby0.09%.Sothevariationofthisindexhasminorinfluenceonthe
results.
2.
istheproportionalcoefficientofthesecondlanguagegrowthrateandschoollearningrate.Weenterdifferent
1
k
intotheprogram,andwegetdifferentMandarinL2speakersnumber.Hereistheresult:
k1
k1
0.0025 10.003333 0.005
Table13Sensitivityanalysisonk
thenumberofMandarinL2speakers 383.14 397.27 410.5
k1
sensitivity 0.104437788
TheSensitivityIndexshownabovemeansthatwhenthek increasedby1%,thenumberofMandarinL2
speakerswillinturnincreaseby0.10%.Sothevariationofthisindexhasminorinfluenceontheresults.
1
3.
ist2heproportionalcoefficientofthesecondlanguagegrowthrateandculturalcommunication.weenter
k
different intotheprogram,andwegetdifferentMandarinL2speakersnumber.Hereistheresult:
k2
k2
k 0.00001 02.0000111 0.0000125
2 Table14Sensitivityanalysisonk
thenumberofMandarinL2speakers 393.11 397.27 401.38
sensitivity 0.093739774
TheSensitivityIndexshownabovemeansthatwhenthe increasedby1%,thenumberofMandarinL2
speakerswillinturnincreaseby0.09%.Sothevariationofthisindexhasminorinfluenceontheresults.
k2
4.
is3theproportionalcoefficientofthesecondlanguagegrowthrateandeconomics.weenterdifferent
k
intotheprogram,andwegetdifferentMandarinL2speakersnumber.Hereistheresult:
k3 k3
k 0.2 3 0.3 0.4
3 Table15Sensitivityanalysisonk
thenumberofMandarinL2speakers 387.12 397.27 408.2
sensitivity 0.079593224
TheSensitivityIndexshownabovemeansthatwhenthe increasedby1%,thenumberofMandarinL2
speakerswillinturnincreaseby0.079%.Sothevariationofthisindexhasminorinfluenceontheresults.
k3
5.
is4theproportionalcoefficientofthesecondlanguagegrowthrateandtechnology.weenterdifferent
k
intotheprogram,andwegetdifferentMandarinL2speakersnumber.Hereistheresult:
k4 k4
0.1 4 0.2 0.3
Table16Sensitivityanalysisonk
thenumberofMan4darinL2speakers 391.82 397.27 403.1
k
sensitivity 0.028393788
TheSensitivityIndexshownabovemeansthatwhenthe increasedby1%,thenumberofMandarinL2
speakerswillinturnincreaseby0.028%.So,thevariationofthisindexhasminorinfluenceontheresults.
k4
6.
5
k


## 第 20 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#79002 Page19of29
istheproportionalcoefficientofthesecondlanguagegrowthrateandmedia.weenterdifferent intothe
program,andwegetdifferentMandarinL2speakersnumber.Hereistheresult:
k5 k5
k 0.1 5 0.2 0.3
5 Table17Sensitivityanalysisonk
thenumberofMandarinL2speakers 394.88 397.27 400.12
sensitivity 0.013190022
TheSensitivityIndexshownabovemeansthatwhenthe increasedby1%,thenumberofMandarinL2
speakerswillinturnincreaseby0.013%.So,thevariationofthisindexhasminorinfluenceontheresults.
k5
5.2 sensitivityanalysisofmodelII
ThepurposeofModelIIistoshowtherelationshipbetweenthechangeinthegeographicaldistributionof
languageandtheimmigrantsovertime.Theman-madeparametersinmodelIIarethenaturalincreaseratesand
.Belowwewillconductasensitivityanalysisofthesetwoparameters.Wewillusedifferentresulttomeasure
thechangeofthetwoindices.
k6
7.Naturalgrowthrate
InourmodelII,wesetaverylargenumber ofnaturalgrowthrates.Almost everycontinenthasitsownnatural
rateofgrowthineverylanguage.Butwecan’tanalysiseveryparameter.Therefore,weonlychangethenatural
growthrateofHindiinAsiatoseewhatchangesitwillbring.
Figure15Sensitivityanalysisonthenaturalgrowthrate
Asthepiechartshows,subtlechangesintherateofnaturalincreasedonotchangethedistributioninAsia.
thegivenHindigrowthrateis0.8%(right)and1.2%(left)
Therefore,wesaythattheselectionofournaturalgrowthrateisinsensitivetotheresult.
8.
is 6the proportional coefficient of migration to the growth of native language speakers. If we change the
k
numberof , allresultsmaychange.The we setfirstis0.5%.Thenweslightlylowerthisvalueto0.3%to
6
k
seewhatchangesitwillproduce.
6 6
k k


## 第 21 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#79002 Page20of29
Wenow have a slight diff
F
e
i
r
g
e
u
n
r
c
e
e
1
b
6
e
T
tw
he
ee
s
n
en
t
s
h
i
i
t
s
iv
r
i
e
ty
su
a
l
n
t
a
a
ly
n
s
d
is
in
on
F
m
ig
i
u
g
r
r
e
at
1
io
7
n
th
co
e
e
o
ff
r
i
i
c
g
ie
in
n
a
t
l r6esult in Figure 18. English
andFrenchspeakersintheU.S.andCanadadroppedslightly.Besides,AustralianEnglishusersdroppedslightly.
Wecanseethatthesechangesareverysmallanddonotaffecttheoverallsituation.So,wethinkthechangeof
thisparameterhaslittleeffectontheresult.
6 Strength and Weakness
Strengths:
(1) Wedoplentyofresearch,andcollectplentyofdatawhichmakeourmodelclosetoreality.
(2) Weconsidervariousfactorsintermsofsecondlanguageincrease,suchasschoolteaching,cultural
migrationandassimilation,theuseoftechnology,socialmediaandeconomics.
(3) Wedoafullsensitivityanalysis.
Weakness:
(1) Wedonotincludeallinfluencetothetotalnumberofspeakersofalanguage,suchastheuseofelectronic
communicationforlackofdata.
(2) Weassume the secondlanguage speakers is indirect proportion toits influences. But the fact may be not.
For example, we assume the second language speakers is in direct proportion to school teaching, but the
factmaybeexponentialrelationshiporpaternityrelationship.
(3) OurmodelIIdoesnotconsiderageandsexratio.
(4) Wedonotconsiderthesecondlanguageinrespectofgeographicdistributionsoftheselanguages.Because
wedonotfindefficientdatatoanalyzethis.


## 第 22 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#79002 Page21of29
7 Memo
MEMORANDUM
TO: ChiefOperating Officer
FROM: Team#79002
Abouthalftheworld’s totalpopulationaresayingthat oneofthetop10languages(inorderof mostspeakers)
as their mother tongue. In addition, many people learn a language as their second language because of
government promotion, schooling, neighborhood effect, social media trends, international business and
immigration. Therefore, the number of native speakers and 2nd language speakers in each language is
dynamicallychangingovertime.
Predictionoftop10languagesover50years:
BasedonthevariousdatacollectedfromEthnologue,WorldBankandmanyotherresources,ourteamhastaken
intoaccountthefactorsmentionedaboveandhasbuiltamodelofthenumberofspeakersofeachlanguageover
timetopredictthechangeinlanguagerankoverthe50-yearperiod.
Wefoundthetop10languages’rankschangefromMandarin、English、Hindustani、Spanish、Arabic、Malay、
Russian、Bengali、Portuguese、Frenchin2017toMandarin、English、Spanish、Hindustani、Arabic、Bengali、
Portuguese、Malay、Russian、Frenchin2067.
As a service company, when choosing whether to set up local branches, your company should focus on how
many potential local clients, and then to conduct a wide range of professional service, to achieve higher
profitability.
Inthemeantime,alargepercentageofthesecitiesareeithernativeorsecondforeignlanguages,andemployees
ofmorethantwolanguagesareeasilyadmittedtothecompany'sbranchoffice.
Sixofficesites:
Our recommendations are different in the short term versus the long term because the rapid growth in both
populationandeconomicofPortuguesespeaker.
In the short term, the six office sites recommended are: Shanghai, New York, Calcutta, Madrid, Dubai, and
Singapore.Whileinthelongterm,thesixofficessitesrecommendedare:Shanghai,NewYork,Calcutta,Madrid,
Dubai,andRiodeJaneiro.
Aswecansee,theMalayspeakers’growthisslightlyslowerthanthegrowthofPortuguesespeakers.
Thebestnumberofoffices:
Todeterminethebestnumber of offices,we setupa cost-benefitanalysismodel,andwhenyour companyhas
providedus with your profitability and office-building costs, we can figure out the suitable company number.
Whenthecompany'sprofitabilityandcostlevelsaredifferent,thenumberofplantsbestsuitedforconstruction
isdifferent.
If thevalue ofc-pratioislessthan281,we think6officesshouldbe built.Ifthevalueof thisratioisbetween
281 and 422, we think 5 offices should be built. If the value is between 422-527, 4 offices are best; if it is
between527and544,3officeshouldbebuilt;if>544,weshouldonlymaintaintwooriginaloffices.


## 第 23 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#79002 Page22of29
Thankyouforyourconsultation.
Best,
Team#79002
References:
[1].https://en.wikipedia.org/wiki/List_of_languages_by_total_number_of_speakers.
[2].Languagesforthefuture.2013:BritishCouncil.
[3].SarahElaineEaton,P.D.,globaltrendsinlanguagelearningin21stcentury.2010.
[4].https://en.wikipedia.org/wiki/Malthusian_growth_model.
[5].http://www.stolaf.edu/people/mckelvey/envision.dir/logistic.html.
[6].https://en.wikipedia.org/wiki/List_of_most_commonly_learned_foreign_languages_in_the_United_States.
[7].http://unicode.org/notes/tn13/.
[8].https://www.weforum.org/agenda/2015/10/is-the-internet-killing-off-the-worlds-languages/.
[9].http://www.internetworldstats.com/stats7.html.
[10].https://data.worldbank.org.cn/indicator/SP.POP.TOTL.
[11].https://faculty.washington.edu/sis/.
[12].https://www.myaccountingcourse.com/accounting-dictionary/service-company.
[13].https://en.wikipedia.org/wiki/List_of_most_commonly_learned_foreign_languages_in_the_United_States.
8 Appendix
8.1 data
(1) languagedistributionofvariouscontinents:
Source:
https://www.worldatlas.com/articles/the-most-spoken-languages-in-america.html
https://en.wikipedia.org/wiki/Teaching_English_as_a_second_or_foreign_language#Asia
https://en.wikipedia.org/wiki/List_of_countries_by_natural_increase


## 第 24 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#79002 Page23of29
http://www.myeses.com/news/view.asp?id=3457
https://www.douban.com/note/635706471/
https://en.wikipedia.org/wiki/List_of_countries_by_population_growth_rate
https://en.wikipedia.org/wiki/List_of_countries_and_dependencies_by_population
(2) languagesOntheInternet[9]
(3) GDP
[7]
(4) foreighlanguagetaughtinschool:[13]
Source:
https://en.wikipedia.org/wiki/List_of_most_commonly_learned_foreign_languages_in_the_United_States
http://ec.europa.eu/eurostat/statistics-
explained/index.php/File:Foreign_languages_learnt_per_pupil_in_upper_secondary_education_(general),_20
10_and_2015_(%25)_ET2017.png


## 第 25 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#79002 Page24of29
(5)naturalgrowthrate:
Source:
https://en.wikipedia.org/wiki/List_of_countries_by_natural_increase
8.2 program
1.moduleI
%r1averagenaturalpopurlationofpeople
z=xlsread('data.xlsx');
x0=z(:,1);
y0=z(:,2);
r1=z(:,3);
c=[1;1;0;1;0;0;1;0;0;1;0;0;1;1;0;0];%developedornot
n=length(x0);
x=zeros(n,60);
y=zeros(n,60);
x(:,1)=x0;
y(:,1)=y0;
r2=0.0005;%increasecontributedbythesecondlanguagespeakers
k1=1/300;%schoolfactor
k2=1/90000;%culturalcommunication
k3=0.3;%internationalbussiness


## 第 26 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#79002 Page25of29
k4=0.2;%theuseoftranslationtechnology
k5=0.3;%sociamedia
a=xlsread('a.xlsx');%differentlanguageusepercentageinschoolofdifferentregion
b=xlsread('b.xlsx');%comunacationpercentage
q=xlsread('q.xlsx');%GDPcommunicatedbylanguages
p=xlsread('p.xlsx');%languageusedininternet
fori=2:60
%thenextyearnativespeakers
x(:,i)=x(:,i-1)+native1(x(:,i-1).*c,y(:,i-1).*c,r1,r2)+native2(x(:,i-1).*(c==0),r1,2*x0);
%theincreaseofsecondlanguagespeakersbecauseofschooluse
delta1=school(x(:,i-1),a,k1);
%theincreaseofsecondlanguagespeakersbecauseofculturalcommunication
delta2=culturecom(x(:,i-1),b,k2);
%theincreasebecauseofinternationalbussiness
delta3=interbussiness(q,k3);
%thedecreasebecauseoftheuseoftranslationtechnology
delta4=technology(k4);
%theincreasebecauseofsociamedia
delta5=media(p,k5);
y(:,i)=y(:,i-1)+delta1+delta2+delta3+delta4+delta5;
end
xlswrite('answer.xlsx',[x(:,50),y(:,50)]);
functionz=native1(x,y,r1,r2)
%theincreaseofnativespeakerindevelopedcountries
z=r1.*x/100+r2.*y;
end
functionz=native2(x,r,s)
%theincreaseofnativespeakerindevelopingcountries
z=r/100.*(1-x./s).*x;
end
functionz=school(x,a,k)
%theincreaseofsecondlanguagespeakersbecauseofschooluse
%kisaproperationindex
n=length(x);z=zeros(n,1);
fori=1:n
z(i)=k*a(i,:)*x;


## 第 27 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#79002 Page26of29
end
end
functionz=technology(k)
%theincreasebecauseoftheuseoftranslationtechnology
z=-k;
end
functionz=media(p,k)
z=k*p;
end
functionz=culturecom(x,b,k)
%theincreaseofsecondlanguagespeakersbecauseofculturalcommunication
n=length(x);
z=zeros(n,1);
fori=1:n
z(i)=k*x(i)*b(i,:)*x;
end
end
2. moduleII
#include<stdio.h>
#include<math.h>
#include<cstring>
#include<iostream>
#include<algorithm>
usingnamespacestd;
floatr[50][50],sum[50];
floatx[50][50],y[50],ry[50],p[50][50];
structnode{
floatpeople;
intlanguage;
}aa[50];
boolcmp(nodea,node
b){return
a.people>b.people;
}
intT=50;
floatk=0.003;


## 第 28 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#79002 Page27of29
intmain()
{
//x[i][j]第 i洲说 j语言人数
//r[i][j]表示第i洲说语言j的自然增长率
//y[i]第 i洲 others的人数
//ry[i]第i洲others 的自然增长率
//p[i][j]第 i洲说 j语言的比例
x[1][1]=150,x[1][2]=56,x[1][3]=34,x[1][4]=28,x[1][5]=26;y[1]=289.25692;
x[2][6]=897,x[2][7]=550,x[2][8]=301.625412,x[2][9]=260,x[2][10]=240,x[2][1]=230,x[2][11]=230,x[2][12]=
120;
y[2]=1377.734272;
x[3][8]=18.175,x[3][6]=0.625,x[3][1]=0.35,y[3]=5.85;
x[4][9]=106,x[4][13]=97,x[4][14]=66,x[4][15]=65,x[4][8]=60,x[4][16]=38.5,x[4][17]=38,y[4]=304.382487;
x[5][17]=383.4,x[5][18]=217.26,y[5]=38.34;
x[6][8]=43.240855,x[6][17]=4.508850,x[6][6]=0.932035,x[6][18]=0.601385,x[6][19]=0.30643,x[6][1]=0.539
895,x[6][14]=7.2867;
y[6]=9.9511;
r[1][1]=0.015;r[1][3]=0.02;for(inti=1;i<=19;i++)if(r[1][i]==0)r[1][i]=0.016;
r[2][6]=0.005;r[2][7]=0.012;r[2][8]=0.009;r[2][9]=0.002;for(inti=1;i<=19;i++)if(r[2][i]==0)r[2][i]=0.01;
for(inti=1;i<=19;i++)r[5][i]=0.01,r[6][i]=0.004,r[3][i]=0.008;
ry[1]=0.016;ry[2]=0.001;ry[3]=0.008;ry[5]=0.001;ry[6]=0.004;
printf("time continent language people(million) others(million)\n");
for(intt=1;t<=T;t++){
for(int
i=1;i<=6;i++){sum[
i]=0;
for(intj=1;j<=19;j++)
sum[i]=sum[i]+x[i][j];
sum[i]+=y[i];
for(intj=1;j<=19;j++)
p[i][j]=x[i][j]/sum[i];
}
for(int
i=1;i<=6;i++){for(int
j=1;j<=19;j++)
x[i][j]=x[i][j]*(1+r[i][j]);
y[i]=y[i]*(1+ry[i]);
}


## 第 29 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#79002 Page28of29
x[4][6]+=0.36+0.36*k*p[4][6];x[4][1]+=0.72*(1+k*p[4][1]);
x[4][7]+=0.18*(1+k*p[4][7]);x[4][8]+=0.18*(1+k*p[4][8]);
x[6][6]+=0.48*(1+k*p[6][6]);x[6][17]+=0.24*(1+k*p[6][17]);
x[6][18]+=0.12*(1+k*p[6][18]);x[3][6]+=0.12*(1+k*p[3][6]);
// x[2][6]-=8.4;x[2][1]-=3.6;
// x[2][7]-=1.8;x[2][8]-=1.8;
// x[5][17]-=2.4;x[5][18]-=1.2;
// x[1][1]-=4.8;
for(int
i=1;i<=6;i++){for(int
j=1;j<=19;j++){
aa[j].people=x[i][j];aa[j].language=j;
}
sort(aa+1,aa+20,cmp);
if(t==20||t==50){
for(intj=1;j<=19;j++)
printf("%d %d %d %lf %lf\n",t,i,aa[j].language,aa[j].peopl
e,y[i]);
printf("\n");
}
}
}
return0;
}

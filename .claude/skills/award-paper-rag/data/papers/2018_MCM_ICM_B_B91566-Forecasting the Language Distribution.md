# B91566-Forecasting the Language Distribution


## 第 1 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team Control Number
For officeuseonly For officeuseonly
91566
T1 F1
T2 F2
T3 ProblemChosen F3
B
T4 F4
2018
MCM/ICM
SummarySheet
Forecasting the Language Distribution
Summary
Language shift is a common and complicated phenomenon since ancient times, which
has far-reaching influence on the development of the human civilization. The language
shift is influenced by many factors. We study the geographically distributed language
shift model and provide solutions based on language shift and economic benefits to
thelocations ofnew international officesfor aservice company.
To get the geographical language transformation model, we start off by creating a
simplemodel, and thenmakeit more sophisticated.
The Worldwide Language Shift Model reflects the situation when two or more
languages communicate. The model takes into account factors such as government
support,tourism,internationalbusinessrelations and technological progress.
The Domestic Language Shift Model is the application of the worldwide
language shift model in country. We adjust some parameters to make this model
fit thedomesticsituation better.
The Geographical Language Shift Model is based on the domestic language
shiftmodel. Thismodel containstheimpact of migrationon languageshift.
We collect rich and effective data, fit the unknown parameters and get the
geographical distribution of various languages in the future. Through the sensitivity
analysis, we prove the stability and error tolerance of the model. By the model
implementation, we found that the geographical language distribution remains
basicallystablein thenext 50 years.
To address the locations of international offices, we take into account the predicted ge-
ographical language distribution and the economic need. In our opinion, choosing the
location of an international office should make the company more profitable. To this
end, we establish a model of the impact of geographical language distribution on the
company’s effectiveness. We identify the six cities most suitable for hosting interna-
tional offices in both short and long terms are: Paris, Tokyo, Milan, Toronto, Bombay,
Brussels. Wealsoput forward ourown ideas aboutthecompany’slong-term plan.
In a word, we predict the language development for the next 50 years according to the
geographical distribution language shift model, and provide effective reference for the
locationsof internationaloffices.


## 第 2 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#91566 Page1of26
Contents
1Introduction. . . . . . .. .. . . . . . . . . . . . . .. .. . . . . . . . . . .. . .. . . 4
1.1 Background . .. .. . . . . . . . . . . . . .. .. . . . . . . . . . .. . .. . 4
1.2 Restatementof theproblem . . . . . . . .. .. . . . . . . . . . . . . .. .. 4
1.3 RelatedWork . . . . . . . .. . .. . . . . . . . . . . . .. . .. . . . . . . . 4
2Assumptionsand Notations. . . . . . . . .. . .. . . . . . . . . . . . .. . .. . . . 5
2.1 Assumptions. . . .. . .. . . . . . . . . . .. .. . . . . . . . . . . . . .. . 5
2.2 Notations. . . . . . . . .. . . . . . . . . . . . .. . .. . . . . . . . . . . . . 6
3Model Construction. . . . . . . . . . . .. .. . . . . . . . . . . . . .. .. . . . . . . 6
3.1 Worldwide LanguageShift Model . .. . . . . . . . . . . . .. . . . . . . . 6
3.1.1 Factors .. . . . . . . . . . . . .. . .. . . . . . . . . . . . .. . .. . 6
3.1.2 DataPre-processing . . .. . . . . . . . . . . . .. . .. . . . . . . . 7
3.1.3 Worldwide Language Shift Model Construction . . . . . . . .. . . 8
3.2 DomesticLanguageShift Model .. . .. . . . . . . . . . . . .. . .. . . . 11
3.2.1 DomesticLanguage Shift Model Construction . .. . . . . . . . . . 11
3.3 MigrationModel . . . . . . . . . . . . . .. .. . . . . . . . . . . . . .. .. 12
3.3.1 DataPre-processing . . .. . . . . . . . . . . . .. . .. . . . . . . . 12
3.3.2 MigrationModel Construction . . . . . . . . .. . .. . . . . . . . . 12
3.4 GeographicLanguageShift Model . . .. .. . . . . . . . . . . . . .. .. . 13
3.4.1 Factors. . . . . . . . .. . .. . . . . . . . . . . . .. . .. . . . . . . 13
3.4.2 Geographic LanguageShift Model Construction. . . . . . . .. . . 13
4Model Implementation andResults. . . .. . .. . . . . . . . . . . . .. . .. . . . . 14
4.1 PartI Problem A .. . . . . . . . . . .. .. . . . . . . . . . . . . .. .. . . . 14
4.2 PartI Problem B .. . . . . . . . . . .. .. . . . . . . . . . . . . .. .. . . . 15
4.3 PartI Problem C .. . . . . . . . . . . . .. . .. . . . . . . . . . . . .. . .. 15
4.4 PartIIProblem A . . . . . . . . . . .. . .. . . . . . . . . . . . .. . .. . . 17
4.5 PartIIProblem B . . . . . . . . . . .. . .. . . . . . . . . . . . .. . .. . . 18
5SensitivityAnalysis . . .. . .. . . . . . . . . . . . .. . .. . . . . . . . . . . . .. . 18
5.1 Sensitivity Analysisfor Ki . . . . . . .. .. . . . . . . . . . . . . .. .. . . 18
5.2 Sensitivity Analysisfor domesticlanguagedistribution. . .. . . . . . . . 18
5.3 Sensitivity Analysisfor FittingParameters. . . . . . . .. .. . . . . . . . . 19


## 第 3 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#91566 Page2of26
6Strengthsandweaknesses. . . . . . .. .. . . . . . . . . . . . . .. .. . . . . . . . 19
6.1 Strengths. . . . . . . . .. . .. . . . . . . . . . . . .. . .. . . . . . . . . . 19
6.2 Weaknesses . . . . . . . . . . . . .. .. . . . . . . . . . . . . .. .. . . . . 20
6.3 Further work. . . .. . .. . . . . . . . . . . . .. . .. . . . . . . . . . . . . 20
7 Conclusions. . . . . . . . . . . .. .. . . . . . . . . . . . . .. .. . . . . . . . . . . . 20
Appendices. . . . . . . .. .. . . . . . . . . . . . . .. .. . . . . . . . . . .. . .. . . 22
Team#91566 Page3of26
To:Chief Operating Officer
From:InvestigationTeam
Date:12February, 2018
Subject:SuggestionsforNew OfficeLocations
Wehave completed an analysis of the locations of your company’s international offices
aswell as thetrendsof global languages.
First, we set up a model of global language competition and summed up the rules of global
language shift by collecting considerable and reliable data. We analyzed and pre-dicted
the geographical distribution of global languages in the next 50 years. Second, based on
the changes of languages, the recruitment cost and the development level of the city
where the office is located in, we provided 6 suitable office locations. Finally, we combined
scientific and technological development factors, and gave reasonable sugges-tions to the
long-termplan ofsetting upnew officesinthe future.
Basedonour analysis, herearesomesuggestions:
It is advisable to set up offices in the following six cities. The languages
correspondtoeachofficeareas follows:
City Country Correspondinglanguage
Paris France France,Spanish, English
Tokyo Japan Japanese,English
Milan Italy Italian, France,English
Toronto Canada English, French
Bombay India English, Hindustani, Bengali
Brussels Belgium France,Dutch,English
We do not recommend frequent replacements of office sites, because there is a
cer-tain stability of the distribution of the world’s languages, no major changes
would occur within a short time. At the same time, replacing an office is costly,
andad-versely affectingthecompany’sprofits.
Profits brought by language advantages will be reduced due to the rapid
expansion of global communications. While the cost of employing may increase,
the amount of existing offices may no longer be optimal. If you can provide more
specific data, we will be able to give more reasonable advice on the long-term
plans forthenewoffices.


## 第 4 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Our modeling analysis report contains moredetailed theoreticalinformation.Please
contactus promptly if thereareany questions.


## 第 5 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#91566 Page4of26
1 Introduction
1.1 Background
It is generally taken for granted that language, as a concomitant of culture, can spread.
With the trend of globalization and the world’s cultural exchange, language transfer
and integration are also more common. Nowadays more and more people can speak
two or even morelanguages.
The shift and spread of language can be seen through the amount of speakers, includ-
ing native speakers plus second or third, etc. language speakers. However, the total
number of speakers of a language fluctuates under the influence of various
complicated factors. These factors involve political, economic, diplomatic, social
relations and other aspects, such as government-mandated official languages, tourism
among nations, mi-gration and population movements, the promotion of new social
media (facebook,Twit-ter, etc.)and soon.
1.2 Restatement of the problem
Weare required to predict the spread and development of languages all over the world
under the influence of several factors and help a large multinational service company
todetermine thelocations ofnew offices.
Theproblem canbeanalyzed intothreeparts:
Develop a model of the distribution of various language speakers over time
based on impact factors and predict what will happen to the number of speakers
of eachlanguageinthenext 50 years.
Use the model to predict the geographic distributions of languages in the next 50
years.
Determine the locations of new international offices and the languages used in
thenew officesbasedonthemodeling results.
1.3 Related Work
Mcmahon(1994) and Mufwene(2001) proposed that the languages change of a region
is caused by a mechanism named language shift. Language shift is a process that
takes place in the region where obsess more than one language. The members of the
region abandon their initial language in favor of another. So, despite the migration.
Accord-ing to Abrams and Strogatz(2003), Anna and Roman(2010), Katharina and
Gero(2017), language shift is modeled as a competition between two communities
who use differ-ent languages, and the motivation of the language shift is to chase to
better opportunity provided by another language. Abrams-Strogatz (A-S) Model is the
most widely math-ematic model of describing the changes in the patterns of language
shift between two language communities. The A-S Model shows the temporal
populationshift ofbothlanguages,which resultsin


## 第 6 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#91566 Page5of26
where nA andnB representtheproportionof each language(languageA andlanguageB)
ofthetotal population. PB!A(nA; sA) is thepossibilitythat anindividual from lan-guageB’s
communityshiftstolanguageB’s communityshifts, in other words, PB!A(nA; sA) is the
shiftratefrom B toA. Thecalculation methodof PB!A(nA;sA) is definedas
where c is the maximum shift rate, a quantifies the resistance level of language B speak-
a
ers to change their language to A. So, n A is a factor that measures the consistency of the
attractiveness and language community size of A. sA is the language status, which
represents the social and economic opportunities afforded to the speakers of language A
relative to language B. The higher the proportion of a language, the higher shift rate and its
status and the lower the resistance, the higher its attractiveness and therefore speak-ers of
other languagesare more likely tousethis languagein thefuture.
Inthesameway, PB!A(nA; sA) is definedas
AssAand sB aretwoopposite factors, wehave sA + sB= 1.
Pinasco and Pomanelli(2006) developed an expanded model of A-S Model which
takes the natural reproduction of language communities into account, and the natural
repro-ductionof languageAis
where rA is the maximum natural growth rate and KA is carrying capacity of language
Ain thisregion.
2 Assumptions and Notations
2.1 Assumptions
Tosimplifyour problems, wemakethefollowing basicassumptions, eachof which is
properlyjustified.
Use 26 languages on behalf of all languages. Because this 26 languages
have 50 million or more total speakers and have a large impact all over the world.
Thelanguagesarelistedin theappendix.
Use 36countrieson behalf of all countries.Theupdatetimeof languagedata from
Ethnologue is usually slow. We can not collect data about all countries all languages
by time. We have access to data series over time in major languages of the world
(26) and cross-section data updated in 2016 for countries in various countries in the
world.Considering the company as aservicecompany, inthe selection ofthe


## 第 7 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#91566 Page6of26
international office location, the population and economic level of a country also have
some requirements. Therefore, we mainly study the top 30 countries in the world in
terms of population ranking or the top 30 countries in the world in terms of GDP. We
think these countries are the major influencers of linguistic changes and linguistic
exchanges and major players in global economy. In addition, we remove countries
lacking of relevant data (for example, the Democratic People’s Republic of Korea).
Thecountriesthat meetthe requirements are listed inthe appendix.
2.2 Notations
3 Model Construction
3.1 Worldwide Language Shift Model
Weconsidertheinfluence of several factorsandestablish alanguageshiftmodel to
reveal thedevelopment principle of everylanguage.
3.1.1 Factors
Government Support
Government support has a far-reaching impact on the development of language.
The language established by the government as the official language can be
used more widely, for example as an educational language among school
teachers and students. Official languages tend to be more competitive and less
likelytobeelim-inatedthanothernon-official languages.


## 第 8 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#91566 Page7of26
Tourism
With the improvement of people’s living standards, the international tourism in-dustry
has also become increasingly prosperous. Tourism promotes the exchange of
people of different languages. When tourists are traveling or living abroad for a short
period of time, they will have an impact on the local language and culture, thus
facilitatingexchanges andcollisionsamong differentlanguages.
International BusinessRelations
With the development of globalization, international business trade is becoming
more and more common. The economic exchanges between countries have led
to the exchange of personnel and material resources, thus promoting the
exchangeandintegration of differentlanguages.
Technology
The progress of global science and technology, especially the development of
on-line social media and the advancement of translation tools, have made
communica-tion and exchange between languages more frequent and more
convenient. People can easily access various languages through the Internet to
learn and exchange. As the translation software is more intelligent, people in
different languagesin differ-ent countriescan understandeachother.
3.1.2 DataPre-processing
Quantityof languagespeakers
We have collected the worldwide number of language speakers of the selected 26
languages.Each of these languages has the number of native speakers and second
or third language users, respectively. Due to limited data sources, we can only
collect the data for the four years from 2014 to 2017 and use it as a basis for
analysis and solution.We observe the changes of the number of native speakers and
the totalnumber of speakers,soas toobserve the law oflanguage development.
Rateof being theofficial language
We count the number of countries where each language is the official language and
its ratio to the total number of countries in the world is the ratio of the language as
the official language in 2017. In this way, we can measure the extent to which the
language is supported by the government.In view of the fact that the official
languages in each countries vary very little, here the proportion of each language as
the official language is not subject to change over time. The proportion of countries
with languagelas their officiallanguage canbe calculatedas:
N
R = o
l,t N (6)
No is the number of countries with language l as its official language, N is the
totalnumber of countries. N= 197.
Tourism Index
We have compiled statistics on the number of departing population from each
countryin2014-2017. Webelieve thattheproportionof languageusersineach


## 第 9 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#91566 Page8of26
country’s departing population is consistent with the overall rate of language
speak-ers in the whole country, so that the number of languages spoken and
outgoingbyeachcountry canbecalculated. Thecalculation methodis:
Social Media
When measuring the impact of social media on language shifting, we select the
in-fluential global social media Facebook as the data source. With the "group"
lookup feature on Facebook, we look up the number of groups whose keywords
are a lan-guage study group and count the number of users who participated in
the group. For example, we enter the keyword "English study" in the group query
interface, then we find out that there are 99 groups that contain this keyword, and
the total number of participants in this kind of group is 65,109. Counting the
number of language learning groups per language measures the contribution of
social media (Facebook) tothatlanguage.
3.1.3 WorldwideLanguage Shift ModelConstruction
We expand the language competition model to a global scale, join multiple languages
(not just a bilingual situation), and use the number of speakers of the language as a
mea-sure of language development. By exploring the influence of those factors
mentioned above on the number of language speakers, we can predict the future
development of language.Thisis Worldwide LanguageShift Model:


## 第 10 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#91566 Page9of26
Figure1: Globallanguageshiftschematicdiagram
ShiftPossibility
Theshiftpossibilitycan beexpressedas:


## 第 11 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#91566 Page10of26
sl,t is the language status, which indicates the social and economic opportunity
and convenience of the language l. Being official language increases the social
andeconomicopportunitiesand thusimproves thelanguagestatus.
ResistanceLevel
Theresistancelevel canbe expressedas:
Tourism, international business relationship with other countries (which can be indi-
catedbytotal theimportand export volume) reducestheresistance.
Technological advances also make linguistic transitions more convenient. It lowers the
difficulty of translation and facilitate online communication. Thus, over time, the resis-
tancehas anintrinsicdecreasingtrend.
The number of participants of the topic of a language in the online social network
shows the popularity of this language, which shows the willingness and decreases the
resis-tance.
The technology also reduce the language resistance as it lowers the difficulty of
transla-tion and facilitate online communication. Thus, over time, the resistance has an
intrinsicdecreasing trend.
LanguageStatus
LanguageStatuscanbe expressedas:


## 第 12 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#91566 Page11of26
3.2 Domestic Language Shift Model
Based on the established worldwide language shift model, we can extend the model to
the domestic language competition. The principles and influencing factors are
consistent withtheglobal situation.
3.2.1 DomesticLanguageShiftModelConstruction
For eachcountry, we canalsocalculatethe changeofnumber ofspeakers over timeas:


## 第 13 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#91566 Page12of26
3.3 Migration Model
Migrationisan importantmeansof population mobilityamongnations.Studying the
global migrationtrendis very importanttosolve theproblem of languageshift.
3.3.1 DataPre-processing
Wegetthemigrationdata from1991 to2017with aninterval of 5years from United
Nations(2017).The migrationratecan becalculatedas:


## 第 14 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#91566 Page13of26


## 第 15 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#91566 Page14of26
Figure2: Geographical languageshiftschematicdiagram
4 Model Implementation and Results
4.1 Part I Problem A
Wemodel thedistribution of various languagespeakersover timeastheWorldwide
LanguageShiftModel.
For unknown parametersin themodel, thegradient decent methodis usedtoperform
thefitting withprogramming tools.
Algorithm 1: Parameter Fitting
Step1: Calculate theactualamountof changein thenumberof usersforeach
languageform 2014to2017
Step2: Use theannual datain themodelformula tocalculate thepredictedvalue of
thechangein thenumber ofusersforeach languagefrom 2014 to2017
Step3: The cost functionis constructedasthesum of squaresforerror of theactual
variationand thepredictedquantity
Step4: Solve thecost functiontoreachtheminimumvalue of theparameters,that is,
theresult of thefitting
Theresult ofparameter fittingis:


## 第 16 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#91566 Page15of26
4.2 Part I Problem B
Use the Worldwide Language Shift Model to predict the future of speakers quantity
inthenext 50years. Weuse thepattern:
as the low of population growth. In fact, the choice of population growth mode has no
essential effect on the result of our result. If the pattern of population growth changes,
thenwe cancalculatethedevelopment of thelanguageunder thenew growthpattern.
Respectively, Use data of native speakers quantities of various languages and data of to-
tal speakers quantities of various languages in the model and solve the result for 50 years
later. The changes of two indicators can be observed. Figure 3 and figure 4 indicates the
numberchangesand Figure5andfigure 6indicatesthe proportion changes.
Figure3:NativeSpeakers Quantities in2068 Figure4: TotalSpeakers Quantitiesin 2068
To see how rank of the top 10 languages changes, we plot the top 15 rank of
languages according to native speakers quantities and total speakers quantities in 50
years. (Figure 7 and figure 8) Among the top10 languages native speakers languages,
only Punjabi (10th th) is replaced by Wu Chinese. Similarly, among the top ten total
speakers lan-guages, only French (10th) is replaced by Wu Chinese. This can be
roughly attributed to the large number of tourists and foreign trade scale of people who
speak Wu language. In addition, there are several internal adjustments in the order of
thetoptenin bothrankings.
4.3 Part I Problem C
Use the Geographic Language Shift Model to predict the numbers of speakers of
each language in each country for the next 50 years. In order to observe whether the
geo-graphicaldistribution of languagehaschanged, one-way ANOVAwasused.


## 第 17 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#91566 Page16of26
Figure 5: Native Speakers Proportions inFigure 6: Total Speakers Proportions in 2068
2068
Figure7: Native SpeakersRankin 50yearsFigure8: TotalSpeakersRank in 50years
Use ANOVA to test the number of users for each language in 2018 and the predicted
number of users for each language in 2068. The result of ANOVA is listed in the ap-
pendix. According to the one-way ANOVA test, all languages pass the test except
Malay. (This situation is because Malay is a union of several languages and its data is
not very accurate.) In this way, we can say that other 25 languages geographical
distributionwill not changealot inthenext 50 years.
Use ANOVA to test the number of users for each country in 2018 and 2068 and the
conclusions are that the geographical distribution in each country will not change
duringthenext 50 years. Theresult of ANOVAis listedin theappendix.
Wecanobserve the geographicaldistribution ofEnglishstraightly fromFigure9 and 10.


## 第 18 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#91566 Page17of26
Figure9: Distributionof Englishin 2018 Figure10:Distribution ofEnglish in2068
4.4 Part II Problem A
We assume that each employee can speak multiple languages. The company needs
topay higher salaries to multilingual employees and such employees areharder to hire.
We suppose that the company will pay C when each employee learn a new language.
The benefit company can get by learning a new language l in one year is Qi;l;t=Pi;t F .
Qi;l;t=Pi;t indicates the business opportunity brought by learning a new language in one
year and F indicates the business benefit one can get by earning one unit of business
opportunity.
To get the maximum benefit, when recruiting staff, the company will give priority to
employees who can speak both English and the language with the highest proportion
inthelocal area.Thenet benefitseachemployee canbring tothecompanyare:
Wecanget thebest employees numbern
We assume that C=F = 10% and calculate n for each country. If n < 2 or English is not
includedin thetopnlanguages,recruiting in thatcountrywill beuneconomical.
Except for uneconomical countries, we rankthecitiesin othercountries bytherankof
City classification for 2016 powered by Globalization and World Cities Research
Networktochoosethelocationof new offices. Theresult is:
We do not recommend recruiting employees with different language policies in the
short term versus the long term. Because from the previous analysis, we know that the
lan-guagedistributionof thesecities will not changealot in thenext 50 years.


## 第 19 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#91566 Page18of26
Table 2: OfficeLocations
City Country n* Correspondinglanguage
Paris France 3 France,Spanish, English
Tokyo Japan 2 Japanese,English
Milan Italy 3 Italian, France,English
Toronto Canada 2 English, French
Bombay India 3 English, Hindustani, Bengali
Brussels Belgium 2 France,Dutch,English
4.5 Part II Problem B
As technology advances over time, cross-lingual communication becomes more and
more convenient. This will reduce the advantages of being a particular language
speaker and thus reduce the business opportunities and business benefits. On the
other hand, the increase in the cost of employment will lead to an increase in C, so it
will increase the ratio C=F over time. Based on previous studies, the proportion of the
population for a language is basically constant. So n may decrease over time, thus
failing to meet the company’s requirements and rendering the office uneconomical. So
inthelong run,it maynot be economical tohave some officeswhose n= 2.
In order to study this issue, we need exact C and F data, especially the salary data for
employees who can speak different languages and the benefit data they bring to the
company. In addition, there is a need for data that measures the level of technology,
business communication efficiency and communication costs. Through these data, we
can analyze change of cost C and return F under the influence of time and
communica-tion efficiency. In this way, we can get n to help the company make better
decisionsin thelongrun.
5 Sensitivity Analysis
5.1 Sensitivity Analysis for Ki
Wehave mentioned above that Ki is assumed as the 1.5 times of present population of
nation i. In this part, we change the value of Ki to see whether it will significantly affect
the global distribution of the population in all languages 50 years from now. Let the
times q = 1:25; 1:75; 2 and do the ANOVA analysis on the result in 2068. The results
arelistedin theappendix.
According to the ANOVA analysis, both the number and the proportion of speakers are
notsensitive tothechangeof Ki.
5.2 Sensitivity Analysis for domestic language distribution
Due to the error when collecting the data about Malay, we can not get the correct pre-
diction result about Malay. As a result, we artificially add errors to the initial data to test the
stabilityof the model.Using arandom number generator,randomlyselectacountry


## 第 20 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#91566 Page19of26
i to change the initial language distribution of the country. Specifically, swap the num-
th th
ber of users in the i language of the country with the number of users in the L i
language. Due to limited computational power of the computer, 20 tests are conducted.
Do the ANOVA analysis on the results of experiments. The ANOVA results are listed in
theappendix.
The results show that there is no significant difference in the results of the model after
all the data in one country are disrupted. That is to say, the distribution of each
language is not affected by a single country. Data errors in Malay will not affect the
resultsof thewhole model.
5.3 Sensitivity Analysis for Fitting Parameters
^ ^
isthebasedresistancelevel. isthebasedlanguagestatus.isthemaximumshiftasc^
rate. These three parameters impact the whole model during prediction and are very
important. Use Austrilia as an example to explore the impact on the language distri-
bution brought by the change of these three parameters. The results are showed in the
Figure11.
Figure11: Sensitivity Analysis forFittingParameters
From the analysis, we can know that except for the positive increasing of c, the model
is not sensitive to the change of a; s and the minus change of c. The model is very
sensitive to the positive increasing of c. When the c gets lower, the main language will
keep increasing because of its large base number. However, this enhanced trend will
alsobegin todecline after along enoughperiodof time.
6 Strengths and weaknesses
6.1 Strengths
Wepioneer andformulatethe multi-language competition modeland combine itwith the
globalmigrationmodel,whichis more practical thanthe bilingual competitionmodel.


## 第 21 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#91566 Page20of26
This composite model has a good interpretability and applies to language shifts both in
theworld andin anation.
This model runs spontaneously after it is established and can predict the number of
users of any language in any country at any one time. This model can smooth the
impactof dataerrorscaused byroughstatistics.
We also set up another model that measures the economic marginal benefits from the
perspectiveofthe costand profitabilityformthe use oflanguage,whichisan innovation.
6.2 Weaknesses
At this stage, as there is limited access to linguistic data, we have simplified the model
to some extent, for example, assuming the same maximum transfer speed between
lan-guages.
Before using the gradient descent method to find the optimal combination of parame-
ters, a large amount of manual derivations and calculations are required. Moreover,
thismodel hasmanyparameters tofit,sothemodel’sfitting timeis long.
6.3 Further work
Since there still exists some weaknesses in our current work, we will continue to
improve andoptimize themodeland solving process.
Firstly, we will look for more linguistic data and earlier data for each country to support
thefit of themodeland restorethesimplified partof themodel.
Secondly, we will discuss whether the parameters can be reduced with the assurance
of accuracy. This can enhance the practical value of the model and reduce the data
require-ments.
Thirdly, we will use the statistical data to evaluate the forecasting results and improve
themodel oncethestatisticsarereleasednext time.
7 Conclusions
For Part I, we establish a language transfer model that integrates language competi-
tion and migration. We look for language distributions across countries and around the
world for model fitting. After getting the fitted parameters, we predict the linguistic dis-
tribution of any group in the future, whether the group is the entire global, a country or
a community. After inserting the initial distribution of each country’s languages into the
model, the model can automatically give the number of speakers each year, each
country and each language through the method of Cellular Automata. After that, we
predict that in the next 50 years, the distribution of various languages in the world will
bebasically stable.
For Part II, we set up another model, which gets the most economical hiring strategy
based on the country’s linguistic distribution. Then, we use this model to evaluate
whether theworld’s majorcities aresuitableforthecompanytosetup offices, andrec-


## 第 22 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#91566 Page21of26
ommendsixlocationoptions. Wegiveadvice basedon themodel, as communication
becomesmoreconvenient in thefuture,lessthan 6officesshould beestablished.
Wealsoperformsomefurtherstudies. Weprovethestabilityand error toleranceof our
model attheend of our discussion.
References
[1] Daniel M Abrams and Steven H Strogatz. Linguistics: Modelling the dynamics of
languagedeath. Nature,424(6951):900, 2003.
[2] Lester Russell Brown and Hal Kane. Full house: Reassessing the earth’s
populationcarrying capacity. Earthscan,1995.
[3] Gretchen C Daily and Paul R Ehrlich. Population, sustainability, and earth’s carry-
ingcapacity. InEcosystem Management,pages435–450. Springer,1994.
[4] Gretchen C Daily and Paul R Ehrlich. Socioeconomic equity, sustainability, and
earth’scarrying capacity. EcologicalApplications, 6(4):991–1001, 1996.
[5] Courtenay Honeycutt and Daniel Cunliffe. The use of the welsh language on face-
book: An initial investigation. Information, Communication & Society, 13(2):226–
248,2010.
[6] Anne Kandler, Roman Unger, and James Steele. Language shift, bilingualism and
the future of britain’s celtic languages. Philosophical Transactions of the Royal
SocietyB: BiologicalSciences, 365(1559):3855–3864,2010.
[7] April MS McMahon. Understanding language change. Cambridge University
Press, 1994.
[8] Salikoko S Mufwene. The ecology of language evolution. Cambridge University
Press, 2001.
[9] Katharina Prochazka and Gero Vogl. Quantifying the driving factors for lan-guage
shift in a bilingual region. Proceedings of the National Academy of Sciences,
114(17):4365–4369,2017.
[10] Department of Economic United Nations and Population Division (2017)
Social Affairs. Trends in international migrant stock: The 2017 revi-
sion (united nations database, pop/db/mig/stock/rev.2017). http:
//www.un.org/en/development/desa/population/migration/data/
estimates2/estimates17.shtml.
[11] Ethnologuehttps://www.ethnologue.com/statistics/size
[12] Wikipediahttps://en.wikipedia.org/wiki/Main_Page
[13] TheWorldBankhttps://data.worldbank.org


## 第 23 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#91566 Page22of26
Appendices
Table A1:CountryList
China Egypt Netherlands Tanzania
Argentina France Nigeria Thailand
Australia Germany Pakistan Turkey
Bangladesh India Philippines United Kingdom
Belgium Indonesia Poland United States
Brazil Iran Russian Federation Viet Nam
Myanmar Italy Saudi Arabia
Canada Japan SouthKorea
Colombia Kenya Spain
Congo Mexico Switzerland
TableA2: LanguageList
MandarinChinese Hausa Tamil
English Punjabi Marathi
Hindustani German YueChinese
Spanish Japanese Turkish
Arabic Persian Vietnamese
Malay Swahili Italian
Russian Telugu
Bengali Javanese
Portuguese WuChinese
French Korean
Team#91566 Page23of26
Table A3: LanguageANOVA
Language F-value P-value
Arabic 0.126460763 0.723199651
Bengali 0.01946812 0.889433442
Mandarin 1.57292E-06 0.999002891
German 0.081672152 0.775888019
English 0.009311393 0.923402739
Persian 0.075428564 0.784399768
French 0.055489296 0.814460637
Hausa 0.225852825 0.636095674
Hindustani 0.000111288 0.991613026
Italian 0.060315915 0.806715958
Javanese 0.054260691 0.816488366
Japanese 0.015521312 0.901209534
Korean 0.17026054 0.681141448
Marathi 0.088763071 0.76663808


## 第 24 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Malay 7.660217524 0.007217351
Punjabi 0.044877544 0.832844964
Portuguese 0.008953098 0.924886351
Russian 0.02091572 0.885424378
Spanish 0.03310032 0.856159619
Swahili 0.610550371 0.437215462
Tamil 0.103668634 0.748430346
Telugu 0.081301552 0.776383223
Turkish 0.02908759 0.865068954
Vietnamese 0.08705579 0.768827363
WuChinese 0.114672547 0.735899623
Yue Chinese 0.142967776 0.706492498
Team#91566 Page24of26
Table A4:CountryANOVA
Country F-value P-value
Argentina 0.007180598 0.932807751
Australia 0.010279037 0.919649862
Bangladesh 0.005194494 0.942831475
Belgium 0.036227065 0.849818022
Brazil 0.007068465 0.933333186
Canada 0.01255359 0.91123807
China 0.009238495 0.923811796
Colombia 0.00719267 0.932751431
Congo 0.008827832 0.925519183
Egypt 0.005450956 0.941439765
France 0.02490977 0.875227783
Germany 0.006832509 0.934452725
India 0.030554174 0.861944636
Indonesia 0.00934412 0.923378874
Iran 0.007673707 0.930544745
Italy 0.009250409 0.923762838
Japan 0.007241333 0.932524882
Kenya 0.009448448 0.922953684
Mexico 0.007516689 0.931257174
Myanmar 0.133593491 0.716276655
Netherlands 0.369745359 0.545895404
Nigeria 0.01762093 0.894928753
Pakistan 0.016767358 0.897490374
Philippines 0.01076275 0.917787779
Poland 0.000817746 0.977300434
RussianFederation 0.005671598 0.940268571
SaudiArabia 0.000110737 0.991645751
SouthKorea 0.012061057 0.912989485
Spain 0.007454537 0.931541246
Switzerland 0.00700541 0.933630498
Tanzania 0.013530812 0.907863293
Thailand 0.009630563 0.922217114
Turkey 0.063482105 0.802107443
UnitedKingdom 0.00751444 0.931267433


## 第 25 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
UnitedStates 0.01171465 0.914243064
Viet Nam 0.00867058 0.926183563
Team#91566 Page25of26
TableA5: ANOVA after Distribution Modified
No. F-value P-value
1 0.012109461 0.912690158
2 2.09116E-06 0.998850306
3 0.054184749 0.816614494
4 0.005367356 0.941806384
5 0.051066312 0.821876616
6 0.03653546 0.848967267
7 4.8344E-05 0.994472145
8 0.040907493 0.840303268
9 0.03702232 0.847976735
10 0.010132928 0.920106186
11 0.059291545 0.808331394
12 0.029920096 0.863170845
13 0.005664064 0.940222538
14 0.013522629 0.907758193
15 0.020080842 0.887718584
16 0.069403299 0.792981514
17 0.054251554 0.816503536
18 0.019573792 0.889135748
19 0.06004562 0.807140792
20 0.075328546 0.784539154
TableA6: ANOVA Analysisof theLanguagePopulations in 2068
q F-value F-crit
1.25 0.6184 4.0343
1.75 0.7477 4.0343
2 0.9201 4.0343
Table A7: ANOVAAnalysis of theLanguagePopulation Proportionsin 2068
q F-value F-crit
5
1.25 8:8131 10 4.0343
1.75 0.0177 4.0343
2 0.2402 4.0343
Team#91566 Page26of26
TableA8: CityClassification for2016
1 London(UK) 11 Frankfurt(Germany)
2 Singapore 12 Madrid(Spain)


## 第 26 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
3 Paris(France) 13 Warsaw(Johannesburg)
4 Tokyo (Japan) 14 Toronto(Canada)
5 Dubai (UAE) 15 Bombay(India)
6 Brussels(Belgium) 16 Seoul(Korea)
7 Milan(Italy) 17 Istanbul(Indonesia)
8 Chicago(Chicago) 18 Amsterdam(Netherlands)
9 Mexico City(Mexico) 19 Brussels(Belgium)
10 Moscow(Russia)

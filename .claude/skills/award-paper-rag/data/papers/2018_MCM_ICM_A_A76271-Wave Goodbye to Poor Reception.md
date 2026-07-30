# A76271-Wave Goodbye to Poor Reception


## 第 1 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
TeamControlNumber
Forofficeuseonly Forofficeuseonly
76271
T1 F1
T2 F2
T3 ProblemChosen F3
T4 A F4
.
Wave Goodbye to Poor Reception
ThediscoveryofHighFrequencyskywavesinthe1920’sallowedamateurradioenthusiasts,
eventhosewithlowpoweredtransmitters,toconnectoverlongdistances.Nowincommonuse,
skywavesallowcommunicationacrosstheturbulentoceantoshipsatseaordistantcontinentsby
bouncingwavesbetweentheionosphereandthesurfaceoftheEarth.Wecreateamodeltotacklethe
challengeofreliablecommunication,simulatingtheunpredictabilityofskywavecommunication,
includingunevenionospheredensityandwildreflectionoffofnon-uniformsurfaces.
Inourmodel,atransmitterataninitiallatitudeandlongitudeonasphericalEarthbeamsaHF
signalwithabearingandelevationangle.
 WeuseNASA’sInternationalReferenceIonospheredatasettodeterminethecurved
trajectoryresultingfromrefractionofthesignalintheionosphere.
 Wegeneratesmallpatchesofterrainusingeitherawavesimulatororgeologicalelevation
data,whichgivethesignalanewheadingasitbounces.
Thismulti-stepprocessallowsourmodeltocreatethecompletepathofaskywavesignal.
Next,we cancalculate howthe atmosphere andterraininterfere withskywaves, or prevent
themfromreflectingatall.Wemodelsignalstrengthusingthedominantsourcesofsignalgainand
loss,andstoppropagationwhenthesignalfallsbelowthe10dBminimum.
 Thetransmitterpower,receiversensitivity,andantennagainprovide170dBofmargin.
 Thesignalweakensalongitstrajectorybecauseofthefreespacepathloss.
 Thesignalattenuatesduetoionosphericabsorptionanddiffusesurfacereflection.
Werunhigh-throughputsimulationsofskywavepathsthatbounceoncalmandturbulent
water,aswellassmoothandmountainousland.Werandomlyvarytransmitterlocations,andtest
pathsfromcoastalcitiestodeterminethemaximumeffectivetransmissiondistance.Toexploreour
model’ssensitivity,wealterthewaveconditionsfromcalmtosuper-turbulent,increasethe
transmissionpower,andchangeionosphericdensity.Lastly,weco-varythefrequencyandelevation
angle,whichwedeterminetobethemostsensitiveparameters.
Weinspecttheaveragenumberofhops,distancetravelledovertheEarth,andpowerlostafter
bouncestocompareourresults.Forourdefaultfrequencyandangleof3MHzand30degrees,
respectively,wefindamaximumoftwohops.Thepowerafterafirstbounceis0.72dBlessfor
turbulentseascomparedtocalm,and0.26dBlessformountainouslandcomparedtosmooth.The
signalsoverturbulentoceanreach1622kmfromtheshore.Wefindthatdependingonlocation,angle,
andfrequency,manysignalspassthroughtheionospherecompletelyorareabsorbedbeforetheycan
bounce.Mappingbouncelocationsoverionosphericdensity,wefindthatskywave
propagationismosteffectiveonthe“greyline”betweennightandday,whenabsorptionislessened
buttheionospherecanstillreflectsignals.


## 第 2 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#76271 1of30
Table ofContents
I Introduction 2
A Problem Summary........................................................................................................2
B OurStartingPoint: Existing Models.........................................................................2
C Our Model.......................................................................................................................3
II Background 3
A Transmitter and Receiver............................................................................................3
B Radio Propagationand Loss.......................................................................................4
C Skywave Channel Interaction......................................................................................4
D Performance Evaluation...............................................................................................5
IIIAssumptions 6
A Model Assumptions......................................................................................................6
IV Model Development 8
A Model Construction......................................................................................................8
B Model Validation.........................................................................................................13
V Model Application 13
A Part I..............................................................................................................................13
B Part II............................................................................................................................14
C Part III...........................................................................................................................14
VI Results 14
A Validation......................................................................................................................14
B Part I..............................................................................................................................14
C Part II............................................................................................................................15
D Sensitivity Results.......................................................................................................16
E Part III...........................................................................................................................16
VIISensitivity Analysis 17
A Explore Parameter Space...........................................................................................17
VIII Conclusion 19
A Our Conclusion............................................................................................................19
B Strengths.......................................................................................................................20
C Weaknessesand Limiting Assumptions.................................................................20
D Future Work.................................................................................................................20
IX Letter 21
X Appendix 24


## 第 3 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#76271 2of30
I. Introduction
Innovatorssincethedawnofhumankindhavesoughtamoreinterconnectedsocietyby
enhancingourabilitytocommunicateoverlongdistances. Thehistoryoftelecommunica-
tionbeganin1800BC,whereChinesesoldiersusedsmokesignalstowarntheircomrades
up to 500 miles away of an attack.1 In 1876, Alexander Graham Bell achieved the first
telephone call.1 While the telephone was a vast improvement over other technologies at
thetime,itrequiredanenormousinfrastructureinvestmentandcouldonlybe usedwith
static stations. A few decades later, the inventionof the radio allowed mobile vehicles to
communicateovervastdistances. In1914, the International Conventionforthe Safetyof
LifeatSearequiredshipboardradiostationstobemanned24hoursaday.2Long-distance
communicationviaHFradiowavesremainsthemoststablemeansofcommunicationonthe
openoceantothisday.3 Ifavesselisnotwithinline-of-sightofacoastalradiostation,the
coastalradiostationusesskywavepropagationtoreflectradiowavesoffoftheionosphere
andbacktoEarth.4 Astheradiowaveskipsbetweenthesurfaceandtheionosphere,ital-
lowsthestationtocommunicatebeyondthehorizon.Despitetheunpredictabilityofradio
overlongdistances,ruggedterrain,andvolatileseas,itremainsanintegralcomponentof
communicationtechnologies that allow mankind to stay connected.
A. Problem Summary
• HighFrequency(HF)radiowaves,from3-30MHz,can“hop”betweentheionosphere
andthesurfaceoftheEarth,travellingagreaterdistancethantheycouldalongthe
ground. When sufficient signal strength is maintained (>10 dB), this enables long
distance communication.
• If the signal reflects off the ocean surface, it maybe affected bychanging electrical
andmagneticpropertiesofthewaves,aswellassize,shape,frequency,anddirection.
• If the signal reflects off the land, it may be affected byterrain variations.
• Followingthelossofamulti-hopsignalnecessitatesthemodelingofthetransmitter,
propagationbetweenbounces,interactionwiththeionosphere,interaction
with the Earth’s surface, and ftnally the receiver.
B. OurStartingPoint:Existing Models
Studiesofskywavecommunicationhavebeenperformedbothempiricallyandtheoret-
ically byradio operators and electrical engineers in the decades since its creation. These
existingmodelshavebeenrefinedovertimebyourincreasingunderstandingofcomplex
physicalphenomenon,improvedmeasuringtools,andthecapabilitiesofmoderncomput-
ers.
Beforedevelopingourownmodel,weexploredtheliteraturetogainathoroughunder-
standingofexistingmodels,andwhichcomplexitiestheyconsider.Afewarehighlighted
here:
• Analyticalandgeometricmodelsareeasytoimplementbutmakesimplificationsthat
degradeaccuracy.Examplesinclude:


## 第 4 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#76271 3of30
– Assuming that the Earth and ionosphere are flat
– Treatingradiowavesassingleordouble rays
– Formula-basedsurfacesfor terrain
• Numericalmodelscanachievehighaccuracyandtakeintoaccountdynamiccondi-
tions,buttheyrequirelargedatasetsandcomputationalpower. Examplesinclude:
– Using real ionospheric conditions as a function of time
– Statisticalfadingofsignalsduring propagation
– Real terrain from geological or oceanic data sources
C. Our Model
Our modeling approach is rooted in our conclusion that while this prompt focuses
on surface hops, a full model of the signal propagation is necessary. The losses in the
ionosphere,forinstance,directlydeterminetheremainingsignalstrengthforhops. Thus,
our model will focus on implementing complexity where detail is most necessary, and
simplicitywheredetailisnotnecessary,asdeterminedbyourresearch. Wehopetoobtain
anaccuratetrajectorythroughtheionosphere,aswellasaccurateinteractions
withterrain,butsimplifyfreespace propagation.
Thecomplexityofthepropagationofradiowavesrequiresustoevaluatethetrade-offs
betweenrealismandcomputationtime.Thisimpactsourterrainandionospheremodeling,
thetypesoflossweconsiderduringpropagation,andradiohardware.Inthefollowingsec-
tions,wewilldeterminewhichterrainandionospheremodelstousebyconsideringthose
withavailabledataandsufficientresolution.5 Wewilldetermineapropagationmodelthat
includeslosseswithasignificantmagnitudecomparedtothecomplexityofthenecessary
calculations. Finally,wewillchoosegeneraldetailsaboutourtransmitter,receiverandthe
systemantennaeinordertodetermineoursignalstrength.Byprogrammingdifferentsce-
nariosintothemodeltolinkbouncestogether,wecantracktheresultsforthecomplete
pathofeach signal.
II. Background
A. TransmitterandReceiver
The ending of each signal’s path can be determined by the point that the remaining
signal power falls below the 10 decibel threshold. This threshold is called the “link
margin,”andistheminimumpowerrequiredtohaveareliableconnection.6
The100Wtransmitpowercanbeconvertedtodecibelswiththeequation:
dBm=10log (P∗1000/1)=50 (1)
10
The decibel is a relative calculation, which in this case is taken as a ratio of power to
onemilliwatt.Indecibelform,thepowerP ,positiveantennagaintt,andnegativelossL
canbeadded. Thecombinationofthesefactorsisknownasthelinkbudget,andwilltell
usthereceivedpower.6


## 第 5 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#76271 4of30
P = P +tt + L+tt (2)
Rx Tx Tx Rx
Comparing this result to the receiver sensitivity yields the link margin. Because the
characteristicsofthe receiverand the receivingantenna arepartof theequation,wewill
treattheendofthesignalpathasthetheoreticallocationwherethereceivercannolonger
detectthe signal, meaning the budget does not meet the required link margin.
Wedeterminetheantennagainandreceiversensitivityfromsourcesaboutradioequip-
ment. A common range of receiver sensitivity is -90 to -120 dBm.6 We will use the
highestsensitivityof-120dBm,becausewedonothaveanyrequirementsforthebit
errorrateofthesystem,orhowsuccessfullyitsendsdata.
Asimpletypeofantennaisa1.25wavelengthdipole,whichhasagainof5.03dBi.7
Thisisrelativetoanisotropicradiator,whichradiatesequallyinalldirections. Thegain
is dueto the antenna signal being focused in certain directions, instead of equal. While
thephysicallengthmightmakeitimpracticaltouse,mathematicallyitrepresentsabasic
antennacase.Wewillusethesamefigureforboththetransmittingandreceivingantennas.
Lastly, the loss will be determined from the propagation of the radio waves. Once all
theseparametersarecalculated,wecandeterminehowfarthesignalcantravel.
B. RadioPropagationand Loss
Evenwithoutanybounces,thereceivedsignalpowerwillbelessthanthetransmitted
power. Thisisduetothespreadingofthesignalasitpropagatesthroughspace. Insteadof
travellinginatightbeam,thewavefrontexpandsoutward,losingpower.Thisphenomenon
iscalledfreespaceloss,andincreaseswith distance.8
The free space loss only includes the effects of distance, and not any obstacles or
interferencethesignalmightencounter.Duringpropagation,thesignalalsoexperiences
lossfromabsorptionintheatmosphere,multipathfading,andshadowing.9Moleculesin
theatmosphere,likewatervapororgaseousoxygen,canattenuatethesignalasitpasses
through. Whenthesignalinteractswithobjects,itcansplitintodifferentpathsthatarrive
atdifferenttimeswithdifferentphases,causinginterference.Thisiscalledshadowingwhen
it occurs with large objects, and fading when it occurs with small ones.
C. SkywaveChannelInteraction
Skywaveradiofollowsa“channel”asitbouncesbetweentheionosphereandtheEarth.
Bothtypesofinteractionscanintroducelosses.
1. Ionosphere interaction
Inthe ionosphere, radiationfromthe sunbreaks downmolecules intoions and elec-
trons.Thesechargedparticlesformlayers.Thevaryingelectrondensitycausestheindex
ofrefractiontodecreasewithaltitude,bendingthesignalsastheytravel.Thedifferent
layersabsorbandrefractthesignal,untilitisattenuated,reflected,orpasses
throughintospace.10 Thechargedparticlesintheionospherevarywiththe sunlight,


## 第 6 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#76271 5of30
changing between day and nighttime, different seasons, and periods of high and low so-
lar activity.11 The ionosphere also interacts magnetically with radio waves, due to their
electromagneticnature,butthisinfluenceisoftenneglectedinmodels.5
Inrelationtoskywaves,thechanginglayersoftheionospherecausesignalstobehave
differently over time, even hour to hour.10 During the day, the D-layer from 60 to 90
km is generated by Lyman radiation and x-rays. This region contributes the most to
absorptionlossofthesignals,especiallythosewithlowerfrequency,andcanpreventthem
frompenetratingfurther. Atnight, however,the D region dissipates, leaving the
reflectiveE andF regions from100to400km.Athigheraltitudes,thelowerdensity
gastakeslongerforionsandelectronstorecombine,allowingtheseregionstopersistwhen
thesunisnotilluminatingthem.Thesignalscantravelhigherwithoutbeingattenuated,
andbecomerefractedmoreandmore,untiltheyreachthepointwheretheyarereflected
back.Thebalancebetweenabsorptionandreflectionmeansthattheday/nightterminator
isanexcellentlocationforskywavestopropagate.Theheightofthelayerthatthesignals
reachdetermines howfar theycan hop, with a2500 kmmaximumfortheE-layer and a
5000kmmaximumfortheF-layer.Duetothesignificantroleoftheionosphereinskywave
communication, we plan to incorporate its variations withheight and location, although
todosointimewouldbetoocomputationallyexpensive.10
2. Surface interaction
On the surface of the Earth, the signal can be reflected, diffracted, or scattered de-
pending on the terrain.9 The ground or water can impact the polarity of the signal, and
multipathinterferenceiscommonassignalsinteractwiththegroundandwitheachother.
Formodelingpurposes,theterraincanbemathematicallyconstructedsurfaces,oractual
geographicaldata,whichisonlyavailableforland models.12
Diffractionmostlyoccurson“knifeedge”surfacesoraroundtheedgesofobjects like
buildings, so reflection and scattering are the most dominant for terrain reflection.5 The
surfaceoftheEarthhasacomplexreflectivitycoefficient,whichdependsonthe conduc-
tivity and permittivity of the medium, and effects the amplitude of the resulting signal
duetophaseinterference.Dependingontheroughnessofthesurface,thereflectionwillbe
specular,havingacoherentmainsignal, ordiffuse,and spreadoutinalldirections.The
comparison of the specular component versus scattering determines the signal
lossdueto reflection.
D. Performance Evaluation
Atthecompletionofthe signal’s path,weneed todeterminehowit behaved. Wefirst
needtofindthenumberofhops,whichcansimplybecalculatedbycountingthenumber
ofsurfaceinteractionsbeforethesignalislost. Wewillalsocalculatethearclengthacross
the Earth’s surface, which tells us the overall distancethe signaltravelled.
Whileitisbeneficialtoknowhowmanyhopswereaccomplished,wewouldalsoliketo
predictwherethesignalendsupontheglobe. Usingthedistancesandthedirectionsthat
thesignalsarereflected,wecandeterminethelatitudeandlongitudeofthefinalbounces.
The density of the signals on the Earth allows us to determine which locations are
likelytoreceiveastrongskywavesignal.


## 第 7 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#76271 6of30
III. Assumptions
A. Model Assumptions
• Thesignalisnotattenuatedbyrain,fog,andinteractionswithmoleculesinthelower
atmosphere.Theselossesareonlysignificantforfrequenciesabove1 GHz.8
• GroundinterferenceisnotasignificantbecausethesignalishighabovetheEarth’s
surface for most of its path and the interference from the ground is viewed as a
minimalimpairmentuntil reflection.5
• Thesignalisnotpolarizedandthefrequencyremainsthesameduringtravel. These
factorsarenotasusefulforlong-distanceradiomodelscomparedtofreespaceloss.5
• Theionospherereachesfrom80kmto2000kmasasphericalshellaboveaspherical
Earth for increased accuracy compared to flat models.13 The signal only begins to
be refracted from bottom of the ionosphere.
• The ionosphere follows the Reference Standard Ionosphere data from NASA at a
givenepoch,sotheglobaldataprovidesinformationaboutbothnightand day.13
• When modeling the behavior of a radio wavebouncing off of water or land, every
bounce will occur on that specified terrain. The coordinates that we use are
onlytodeterminetheionospheredatalocationandthedistancetravelled
ontheEarth.
• The ocean surface is stationary compared to the speed of light. The signal reflects
offoffixedwave shapes.
• Acalmoceanhaswaveheightsoflessthan1m,whilearoughoceancanhaveswells
from 1 to 10 m. A super-turbulent ocean can have a peak swell of 15 m, based on
NationalWeatherServicewaveforecastsforafully-developed sea.14
• Thelandconsistsoftopographicalfeatureswithoutanysurfacecoverings,tosimplify
computations.
• A flat land surface is entirely smooth, while a mountainous region may havesharp
altitude deviations in the tens of meters.
• The transmitting and receiving antennae are dipole 11 wavelengthantennaewith
4
gainsof5.03dBieach.6 Thereceiverhasasensitivityof-120dBm.6
• Thevelocitiesofthetransmittingandreceivingantennas,ifinmotion,arenegligible
comparedto thespeedoflight.
• All the signal loss occurs between the two antennae, with no loss due to cabling,
filters,orothernoiseatthetransmitterandreceiver.Thesevaluesareusuallysmall
comparedtopathloss,andrequiredefiningpreciseequipmenttodetermine.6


## 第 8 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#76271 7of30
• Thecommunicationslinkonlyneedstobe completeinonedirection,meaningthat
the transmitting station only transmits,and the receiving stationonly receives. We
do not need to determine how successfully information is transmitted, only if the
connectionismade.4
Nomenclature
∆A Amplitudechangefactor
∆h Standarddeviationofsurfaceheight [m]
∆ Initialangleofsignalprojection [rad]
A Path length from starting point to bottom of the ionosphere[km]
s Permittivity of free space [8.8541∗10−12F ∗m1] i
0
ˆ Localincidenceunit vector
nˆ Local normal unit vector
rˆ Local reflection unit vector
λ Signalwavelength[m]
µ(z) The refractive index at a given altitude
ω Angularwavefrequency[rad/s]
φ TheangleofincidenceatpointP [rad]
0 in
ψ Phase [rad]
ρ Complexreflectivitycoefficient
Θj Theanglesweptoutfromthewaveenteringtheionospheretoitspeakaltitude
[rad]
θ Incidence angle between ray and surface [rad]
i
˙r Total reflection unit vector
B Totalpathlength [m]
brg Initialbearingofa signal[rad]
c Velocityoflight[2.99792x108m/s]
e Charge on the electron [−1.602∗10−19C]
f Frequencyofthesignalwave [hertz]
tt Antennagain[dBi]
h DistancefromsurfaceoftheEarthtothelowestpointoftheionosphere[80km]
0
h Distance from surface of the Earth to the highest point the ray reaches [km]
r √
j Complexvariable[−1]
k Non-deviativeabsorptionloss [dB]
L Loss [dB]
m Massoftheelectron[9.109∗1031kg]
N Electrondensity[electrons]
m3
P Power[W]
P /P Thepointsofentry/exitinto/leavingthe ionosphere
in out
R RadiusoftheEarth [km]
S Pathlengththe ionosphere[km]
v Electron-neutralcollisionfrequency [Hz]
z DistancebetweentherayandthesurfaceoftheEarthatanygivenpointin
itstrajectory[km]


## 第 9 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#76271 8of30
IV. Model Development
A. Model Construction
Themodelisconstructedinordertoaccuratelycreatethepathofthebouncingsignal.
This path provides the loss due to free space and ionospheric absorption, which
aredetermined perdistance. Thegroundmodel determines theloss from the terrain
interactionaswellasthenewincidenceangleforpropagationofthenextbounce.
1. Propagationand Ionosphere Interaction
Thefirst portionof themodel consistsof thesignaltravelling fromthegroundtothe
ionosphere,refracting,andtravellingfromtheionospherebacktotheground.Overthis
entiresection,wedeterminethepathaboveandbelowtheionosphereseparately.The
belowequationsarederivedfromseveralsources.515
Theequationsinthissectionarebasedonacurvedradiowavetrajectory,asshownin
ourdiagram,Figure1.
Figure1.DiagramofSkywaveInteractionwithIonosphere


## 第 10 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#76271 9of30
Thedistancefromthetransmittertotheionosphereisdeterminedfromthelawofsines
usingtheequation
By Snell’s law, the angle of incidence is equal to the angle of reflection,5 therefore
thelengthofthetransmitter-ionospherepathisthesameasthelengthoftheionosphere-
receiverpath.
Oncethewaveenterstheionosphere,itbeginsonatrajectorytowardspointP . Due
proj
tothevariabilityoftherefractiveindexbetweenthefirst80kmofEarth’satmosphereand
theionosphere,theraybeginstobendalongpathSuntilitreachesthereflectionpoint,at
which it bends back towards the Earth’s surface. Wecalculate the length of path S with
the equation
TheaboveequationsconvertfrompolarcoordinatestoaCartesiangridwiththeorigin
on the earth’s surface directly below the radio wave’s virtual maximum. The value of Θj
isfoundwith5
Wemodeled the electron density of the ionosphere using valuesprovided bya NASA
database.13 Our model has a sample for every 10° latitude by 20° longitude by 10km
sectionoftheionosphere. ThesevaluesaretakenfromJanuary1,2001at1:30AMGMT
toprovideaconsistentdatasetwithbothdayandnightregions,butitdoesnotinclude
variationintheionospherefromseason,solarcycle,andotherfactors.Forcomputational
speed,intermediateelectrondensityisfoundwithlinearinterpolation. SeeFigure5inthe
Appendixforanexampleofatrajectorycalculatedbyourmodel.Thistrajectorymatches
Figure1well.


## 第 11 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#76271 10of30
2. Ground Interaction
Whentheradiowavecomesincontactwiththeearth,weemployadifferentmodelto
predictitsnewdirectionandloss. Thismodelisgeneralizedtoallowfordifferenttypesof
landandwaterterrains.
Forfixedterrainsuchasland masses,geologicalsurveydataexiststhatwecanuseto
createrealisticshapes.TheUnitedStatesGeologicalSurveywebsitecontainsdownloadable
data sets for elevation, such as the Space Shuttle Radar Topography Mission data that
coversthe globe with onearcsecond resolution.12 We arbitrarilyselect one such dataset,
containinghillsandgulliesfromtheborderofGuineaandMaliinwesternAfrica.
For unfixed terrain such as water, no permanent data sets exist. Because we only
needtocapturethemotionofthewateratafixedmomentintime,wedecidetogenerate
instantaneous wave shapes. Such simulations are plentiful in MATLAB, and we adapt
one provided byStackExchange user “Hoki”.17 This simulation models random wavesof
set height based on wind patterns, using the Phillips spectrum of waveamplitude for a


## 第 12 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#76271 11of30
fully-developedsea.Figure2(andFigure7intheAppendix)areexamplesofturbulent
andcalmrandomwaves,respectively.
Figure2.IncidentandReflectedRaysOffRandomTurbulentWaves
Wecreatetheterrainforeachtypeofsurfaceasfollows:
• Smooth land: We generate a perfectly flat 10 by 10 meter surface in MATLAB,
representingaplains environment.
• Mountainous land: Our model randomly selects a 50 by50point subsection of the
Guinea/Malidatasettoprovidetheterrainshape. Thesizeisscaleddowntoa10by
10metersquare,withsmoothedelevationchangesof10metersorless. Thisterrain
canveryfromgentleslopestosteepmountainsides,butdoesnotinclude cliffs.
• Calmseas: Wegeneratea10by10metersquareofgentlewaves,withamplitudeless
thanonemeter.
• Roughseas: Weprovideacrosswindtogeneratelargeswells,withamplitudefrom1
to 10 meters for rough ocean and up to 15 meters for super-turbulent.
Thesizeofeach patchisdetermined byourneed forasmallmeshinordertoreduce
computationtime,whichmeanstheareamustalsobesmallinordertopreservedetail.
Thenextstepistodeterminethesignallossexperiencedoneachtypeofterrain,using
equations for reflection and scattering on rough surfaces.5 Wequantify the roughness of
asurfaceusingthestandarddeviationoftheheight∆h overtheentiremeshsurface. We
canthenapplytheRayleighroughnesscriteriontoapproximatehowmuchthe signal


## 第 13 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#76271 12of30
willreflectorscatter.Thechangeinphasecausedbytheheightdifference,asdifferent
raystakedifferentlengthpaths,canbecalculatedusingincidenceangleθ andwavelength
i
λ:
∆ψ=4π∆hsin(θ)/λ (16)
i
Thedifferentphasescausemultipathinterferenceinthewave,whichreducestheam-
plitudeofthecoherentspecularlyreflectedcomponent.Thisamplitudereduction
canbecalculated:5
∆A = exp(−∆ψ2) (17)
The reflection capability of the terrain depends on its reflection coefficient ρ, deter-
minedbytherelativepermittivitys andconductivityσ.Weusetheequationfor
r
perpendicularpolarization,althoughwehavenotassignedapolarizationtooursignal:
whereχ =18e9σ/f ,σ =5S/m,σ =0.002S/m,s =81,ands =13
water land rwater rland
formountainousterrain.18
Theresultingloss,basedonthepowerofthespecularcomponent,is:5
L = 10log (ρ(∆A)2) (19)
reflection 10
Lastly,weuseraytracingmethodstodeterminethedirectionthatthespecularcom-
ponentwillreflect,providingthenewincidenceangleforthe nextionosphere
bounce.19
Using the terrain surface mesh, we find the local normal vector nˆ at each mesh-point
usingtheMATLABfunctionsurfnorm.Weusetheincidenceanglebetweentheincoming
signal and the horizontal to find a local incidence vector ˆi, which is constant for each
mesh-point.UsingthesetwovectorswiththeLawofReflection,wecandeterminethe
localreflectedvectorsrˆ.19
rˆ=ˆi+2cos(θ )nˆ (20)
local
whereθ isthelocalangleofincidencebetweenthelocalnormalandlocalincidence
local
vector,determinedby:
cos(θ local ) = −ˆi·nˆ (21)
Oncewefind thelocalreflectionvectors,wecantakethe meanofeachcomponent in
ordertofindthetotalreflectionvector.Weremovethelocalvectorswherethez-component
isnegativefromthecalculation,becausethisrepresentscaseswheretheterrainisshadowed
from the incident signal. With the total reflection direction, we extract the azimuth and
elevationusingMATLAB’scart2sphconvertertoprovideforthenext bounce.
The example terrain plots, including Figure 2 and Figure 7 and 6 in the Appendix,
displaythesurfaceswithlocalvectorsshown,aswellasthemeanincidenceandreflected
vectors.


## 第 14 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#76271 13of30
3. Loss
To tie our model together, we return to the overall link budget, updated with new
losses:
P = P +G +L +L +L +G (22)
Rx Tx Tx free absorption reflection Rx
Aftereachionosphereandsurfacebounce,ourmodelreevaluatesthisequationtodeter-
mineifthelinkmarginismet. Ifitismet,thesignalcontinuesforanotherbounce. Ifnot,
we determine that signal to be lost, and record its last known surface location. Overall,
wehave180dBinthebudget,of whichwecanloseupto170dBtoremainover10dB.
B. Model Validation
Wewill first validate our model qualitatively byfollowing individual rays along their
path until they are absorbed, fly into space, or fall below the minimum signal strength.
Givenaccountsofskywaveradiooperators,weexpectthatthiswilldependonthetimeof
dayandelectrondensityatthebouncelocation.10 Weexpectthesignaltofollowastraight
pathfromtheorigintothebottomoftheionosphere,followedbyacurvedpointthatpeaks
at the calculated point of refraction, followed by a straight path from the bottom of the
ionosphere back to the surface. While we don’t have a quantitative expectation of the
signal’s behavior after bouncing off of the surface; however, wedo expect that the more
surface variation, the more variation wewill see in subsequent bounces. Weexpect that
thelosswillincreasewithdistancetravelled,andincreasewitheachsurfaceandionosphere
interaction.
Quantitatively,wefindthatarangeforthemaximumdistanceofahopisbetween2500
and5000km,dependingontheheight.20 Wewilllikelyseeourmaximumdistanceonour
first bounce because of our ability to control the input frequency and angle.
V. Model Application
In order to recreate the desired scenarios, we set the model conditions for each test,
includinginputvariables,outputvariables,andnumberoftrials.
A. Part I
The first application of our model focuses on reflection of the signal off of the ocean.
Using the January 1, 2000 ionosphere data obtained from NASA,13 we will uniformly
randomlyselectalatitude,longitude,andbearingastheoriginofthesignal. Thislocation
determinesonlythelocalionosphericconditions,becauseweassumethatthesignalwill
bounceoffofwaterforthisproblem,nomatterwhereitgoes.
Wesendthissignalinitiallyatanelevationangleof30°,afrequencyof3MHz,apower
of100W,anantennagainof5.03dBi,andareceiverantennasensitivityof-120dBm. We
willdetermineamean,median,andstandarddeviationofsignalstrengthafter
asinglebounceandthemaxnumberofbounces(wherebounce2andonwardare
overcalmwater)giventheaboveinitialconditions.Wewillsimulate10000signalsfor a


## 第 15 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#76271 14of30
firstbounceoncalmseaswith<1 mwaves(becausethisisourbasecase)and1000
forafirstbounceonroughseaswith< 10mwaves.
B. Part II
Wewillreusetheinitialconditionsfromabove,butinsteadassumethateverybounce
willtakeplaceofflandwithsmooth (perfectlyflat)or mountainous(up to10m
deviations). Our results will be in the same format as Part I, and will show the effects
ofdifferentterrainsonthenumberofreflectionsofthesignal,aswellasthepowerlostfor
1000 trials.
C. Part III
Usingthesameelevationangleandfrequency,weremovetherandomstartinglocation,
ftxing a transmitter location and bearing near the edge of the water. By running
1000trialswithdifferentelevationangles,andoutputtingthelocationofeachbounce,we
canfindtheregion where a ship would be able to receive the signal.
VI. Results
A. Validation
As wediscussed in the Background, weexpect that the peak of radio wavereflection
to occur in the region of the day/night terminator. This occurs because of a balance of
theweakreflectionofthenightandthestrongabsorptionoftheday.Ourmodelmatches
theseresults,asshowninFigures8and9intheAppendix.Theformerplotsthelatitude
andlongitudeofmodeledoceanicbounces,superimposedoveracolormapofthemaximum
ionosphere electron density that day. The bounces occur between the bright and dark
regions,showingaclearpreferencefortheday/nightterminator.Thelatterplotshowsthe
probabilityofradiowavesburstingthroughtheionosphereasafunctionofpeakelectron
density.This probability is near unity the highest and lowestdensities, but decreases for
intermediate densities, as would be expected near the day/night terminator. Thus, our
modelmatcheswellwithqualitative predictions.
B. Part I
Werunourmodeltocomparetheperformanceofthesignaloncalmoceanandturbulent
oceanmeasuredbythepowerofthesignalafterthefirstbounce. ForPartIandPartII,we
willusea2samplet-testbecausetheobserveddataarefromrandomsamplesofaskewed
normaldistributions.Forouranalysis,wesaythatournullhypothesisisthatthetwosets
ofdataarethe same.
Table1.PowerAfterFirstBouncebyVaryingTurbulenceofOcean
Mean(dB) StdPower(dB)
Calm 25.54 4.13
Turbulent 24.82 4.28


## 第 16 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#76271 15of30
The distribution of signal strength after the first bounceis shown in Figure 10 in the
Appendix and the numerical values are shown in 1. Running our t-test, we get a p-value
of0.0291,whichmeansthedifferenceinpowerfromcalmtoturbulentissignificantata
5%level.
Table2.DistanceofSignalbyVaryingTurbulenceofWater
AvDistance(km) StdDistance(km) AvBounces StdBounces
Calm 1444.67 474.26 1.53 0.50
Turbulent 1006.71 231.72 1.10 0.33
As we extend our analysis to include multiple bounces, we find that the maximum
number of bounces with an initial angle of 30° and a frequency of 3 MHz is 2
bounces,forbothinitialcalmandinitialturbulentcases.Usingthesamet-teston
the average signal distance, we geta p-value of 3.87∗10−32, and a p-value of 7.84∗10−28 for
thenumberofbounces.Thismeansthatalthoughbothhavethesamemaximumnumber
ofbounces,wecanconcludethatoveralltheturbulentoceancausesareductioninboth
distanceandbounce number.
C. Part II
We run our model to compare the performance of the signal on smooth terrain and
ruggedterrainmeasuredbythepowerofthesignalafterthefirstbounce.
Table3.PowerAfterFirstBouncebyVaryingRuggednessofTerrain
Mean(dB) StdPower(dB)
Smooth 24.84 4.07
Rugged 24.58 3.97
The distribution of signal strength after the first bounce is shown in Figure 11 in the
Appendix and the numerical values are shown in 1. Running our t-test on the two data
sets,wegetap-valueof0.39andcannotprovethatthepowerdatafromthesmoothand
ruggedterrainsimulationsaredifferent.
Table4.DistanceofSignalbyVaryingRuggednessofTerrain
AvDistance(km) StdDistance(km) Av Bounces StdBounces
Smooth 1360.45 453.67 1.47 0.50
Rugged 997.47 316.37 1.25 0.44
AsweextendouranalysistoincludeallsignalsthatdonotfallbelowtheSNRthreshold
of10dB,wefindthat the maximumnumber ofbouncesthat weobserve withan initial
angleof30°anda frequency of3MHzoversmooth andmountainousterrain
is2bounces.Usingthesamet-testontheaveragesignaldistanceovertheEarth, we
get a p-value of 2.74 ∗ 10−44 and reject the null hypothesis because the p-value is well


## 第 17 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#76271 16of30
belowanyreasonablestatisticalmeasure.Therefore,wecansaythatthedistancedata
fromthesmoothandruggedterrainsimulationsaredifferent.Thep-valueforbouncesis
3.74∗10−10, which is similarly significant.
D. Sensitivity Results
BeforeproceedingtoPartIII,wemustfirstdeterminethebestinitialangleandthebest
initialfrequencyforourtransmittingstationandourboatreceiver. Insteadofthenumber
ofhops,wewillusethehighestaverageEarthdistanceofanangle-frequencycombination.
Withanidealangle30°andfrequency3MHz,wewillsamplethreepotentiallocations
andshiptraveldirectionsinordertodeterminethemaximumdistancethattheship can
travelawayfromthestationwhilestillreceivingcommunication.
E. Part III
Toensure that our sample size has enough successful bounces to compare the three
locations,wechoosetosamplefromlocationsanddirectionsthatshowedahighpercent-
age of reflection from PartsI and II. Our tworealistic locations are Monjaras, Honduras
(13°09’07.6”N 87°23’07.2”W) and Los Angeles, California (32°41’19.9”N 117°13’14.7”W),
andwewillaimourtransmitterWestandSouthwest,respectively.21 Afterrunningthese
threesimulations,wewilldeterminetheaverageperformanceofourradiosystem.
Figure3.HondurasTrajectory
Figure4.L.A.Trajectory
Inthissimulation,wevarytheinitialangle∆from0°to60°inincrementsof0.1°in
ordertogetarepresentationofatransmitterdispersingasignal.
Table5.DistanceforSignalsAimedataShipinTurbulentSeas(Measuredinkm)
B1MinDist B1MaxDist B2MinDist B2MaxDist
Honduras(W) 651.77 1085.87 187.67 1622.24
L.A.(SW) 676.42 810.67 - -
Ourmodeltrackstheminimumandmaximumdistance(km)foreachbouncethatwe
observeofindividualrays.FromHonduras,weseethataboatonturbulentoceanscould


## 第 18 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#76271 17of30
maintainasignalwiththetransmittingstationfrom187.67kmto1622.24kminastraight
linefromtheshore.AsshowinFigure18intheAppendix,thelocationofthefirstpoints
areconcentratedbetween651.77kmand1085.87kmfromtheshore. Thesecondbounces
arescatteredbytheturbulent wavesand wouldnotprovideaconsistent signalforaboat
outsideofthefirstbounce concentration.
FromL.A.,oursignalonlybouncesasingletimeandcoversthedistancestretchofocean
from 676.42km to 810.42km in a straight line from the shore. Similar to the Honduras
simulation,the first bouncepoints areconcentratedalong the initialtrajectory.
VII. Sensitivity Analysis
A. ExploreParameterSpace
Inordertoensurethatourmodelisrobust,weneedtounderstandhowourassumptions
and inputs effect the results. Todo this, we select several key inputs and data sets, and
varythem with 1000 trials to see how the model responds.
1. Frequencyand Elevation Angle
TheHFbandcontainsfrequenciesfrom3-30MHz,butwechoose3MHzasourdefault,
launchedatan angleof30degrees.This selectionisarbitrary,so wedecidetoperforma
studyonthemodel’ssensitivitytocombinationsofelevationangleandsignalfrequency.
Ourmetricsarethedistance,bounces,andlossduetoionosphericabsorption. Weselect
elevation angles of 0, 2, 5, 10, 15, 20, 30, 40, and 50 degrees for this sweep,
accompanyingthechangesinsignalfrom3to21MHzbymultiplesof3MHz.
Weexpectthat some typesof losspenalize highfrequencies,whilesomepenalizelow,so
thereisatrade-off. Additionally,theelevationangleeffectstheoverallpathlength,which
effects loss.
Theresultsof thisanalysis showthat functionalangle/frequency pairs exist ona line
traversingthroughtheparameterspace.Deviationfromthislinecausesthesignaltoeither
travel unabated throughtheionosphereor be totally deteriorated byloss. Pairs withlow
frequenciesandhighanglestendtobouncemore,buttravelashorteroveralldistance,asis
seeninFigures12and13intheAppendix. Highfrequency/lowanglepairsaremuchmore
likelytobe consumedbylossthanlowfrequency,highanglepairs.Thiscanbe observed
in Figure 14 in the Appendix.
2. Wave Turbulence
Forthe waveturbulence, wewish to determine the limits of the extent to which tur-
bulent water can effect the overall distance. Wedo this by adding an additional metric
forsuper-turbulent swellswith a maxheight of <15 m, representativeofextreme
storm conditions, as well as running trials that bounce off of the same type of wa-
ter for all bounces instead of calm water for bounces after the first. Weexpect that
super-turbulent water willhavethemost effecton decreasing distance, but changing the
subsequent bounces will also decrease the distance.
Table6containstheresultingvaluesfromthesimulationastheturbulenceisvaried.We
performat-testtodeterminewherethesedifferencesaresignificant.Wetestthehypotheses


## 第 19 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#76271 18of30
thateachpairofobservationshavethesamemeanandfindp-valuesofessentially0forthe
Calm/Turbulentand Calm/SuperTurbulentpairings.Thefinalpairing,Turbulent/Super
Turbulent,hasaninsignificantp-valueof0.64.Thus,weconcludethatturbulentand
superturbulentoceanstenddecreasethemeandistancetraveledbytheradio
signal. A box-plot of these data are found in Figure 15 in the Appendix.
Table 6. EffectsofOceanTurbulenceonDistance Traveled
DistanceTraveled Calm Turbulent Super
Turbulent
Mean(km) 1445 1007 995
StandardDerivation 474 232 253
(km)
3. Transmit Power
The power of the transmitter determines the initial signal strength, so we want to
examineifincreasingthisparameterallowsthesignaltobounceagreaterdistanceacross
theEarth.Thetransmitterpowerisincreasedinorderofmagnitudestepsof100W,1000
W, and 100,000 W, whichcorrespond to 50, 60, and 80 dBm. Including the antenna
andreceiversensitivity,thevaluesare180,190,and210dBmtotalsignalcomparedtothe
10dBcutoff.
Plugging these values into the simulation, wefind statistics presented in Table7. We
comparethesesimulationswitha2-samplet-test,findingthedifferencesbetweenallthree
pairs to be statistically significant. The lowest p-value, 4E-5, corresponds to the null
hypothesis that the 190 and 210 dBm signals have the same average distance travelled.
Thisismuchlowerthananycommonsignificancelevel. Theotherp-valuesareessentially
0.Weconcludethatthemorepowerfulthetransmitter,thegreatertheoverall
distancetravelled.AboxplotofthisdatacanbefoundinFigure16inthe Appendix.
Table7.EffectsofTransmitterPoweronDistanceTraveled
DistanceTraveled 180dBm 190dBm 210dBm
Mean(km) 1445 1737 2105
StandardDerivation 474 672 1168
(km)
4. Ionosphere Density
Our sample used NASA’s ionosphere data for January 1, 2000. This year recorded
nearly140sunspots,11 arelativelyhighamountofsolaractivitycomparedtoneighboring
years. Totesttheeffectofthenumberofsunspotsonourmodel,weuseNASAdatafor
theyears2003and2009,with70sunspotsand10sunspots11, respectively.


## 第 20 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#76271 19of30
These represent a moderate and low case of solar activity. The solar activity influences
theelectrondensityoftheionosphere,whichshouldincreasetherefractiveindex,making
it more difficult for signals to reflect instead of refract.
Asinthepreviouscases,wepluggedtheseparametersintothesimulationandrecorded
the resultant total distances, with overall statistics displayed in Table 8. Weperform a
two-sample t-test on each of these pairs, and find an insignificant p-value of 0.6 for the
2009/2003pair.Thus,wecannotconcludethatthesetwodatasetsaredifferent.However,
the2009/2000and2003/2000pairshavep-valuesof0.03and0.003respectively,whichare
bothsignificantatthecommon5%standard. Thus,wecanconcludethathighsolar
activityhasastatisticallysigniftcantnegativeeffectondistancetravelled. See
Figure 17 in the Appendix for a box-plot of these data.
Table8.EffectsofSolarActivityonDistanceTraveled
DistanceTraveled 2009Data 2003Data 2000Data
(Low) (Medium) (High)
Mean(km) 1587 1551 1445
StandardDerivation 520 430 474
(km)
VIII. Conclusion
A. Our Conclusion
Usinghigh-throughputsimulationofradiowavetravel,weexploretheparametersthat
moststronglyaffectradiocommunications.Wefindthattheinteractionbetweentheradio
wavesandtheionosphereisthestrongestdeterminantofpropagationbehavior.Thetypical
lossasignalexperiencesintheionosphereisaround15-20dB,whereastypicallossfrom
ground interaction is less than one dB.
Thesensitivitytotheionospheremanifestsitselfwhenconsideringthefrequencyand
angle of elevation of skywave. Too much interaction with the ionosphere will sap the
signal’s strength, while too little interaction will not alter its upwardtrajectory, allowing
ittoescapetospace.Theseasonalanddailychangesintheionospherealsohavemarked
effectsonsignalpropagation,increasinganddecreasingtheelectrondensityasmoreorless
solar radiation is incident on the atmosphere.
Also important to radio wave propagation is interaction with the Earth. We consider
multipleterrains inthis model, and find that rough oceans ormountainousland slightly
reducesignalstrengthwhilescatteringitstrajectory.
Through our consideration of all relevant signal attributes, we qualitatively match
knownradiowavebehavior.Thus,weholdthismodeltobe ausefultoolforradioenthu-
siastsandprofessionals alike.


## 第 21 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#76271 20of30
B. Strengths
• Themodelconsidersthecomplexityofthelayersoftheionosphere,usingrealglobal
data for day and night that varies with altitude. This allows more accurate cal-
culations of ionospheric trajectory and absorption loss, as well as when signals are
reflectedortransmitted,matchingrealworldexpectationsfortheday/nighttermi-
nator.
• Themodelconsidersacurvedionosphereand curvedEarth,findingmoreaccurate
distances as arc lengths overthe surface than a flat approximation.
• The model uses realistic terrain shapes for land and water, to aid in determining
correctreflectionlossandbounce direction.
• The model is computationally efficient, allowing 1000 trials to run in just a few
minutesonapersonal laptop.
C. WeaknessesandLimiting Assumptions
• The model ignores many potential sources of loss, including multipath loss due to
polarization in areas other than the ground bounce, as well as Doppler shift and
magneticeffectsinthe ionosphere.
• Themodelonlyconsidersasmallpatchofground,wheninrealitythesignalwould
bounceoffamuchlargerarea.Italsoneglectssurface coverings.
• The model does not consider the ways that the ionosphere changes with time on
scaleslargerthanoneday-nightcycle,unlessacompletelynewdatasetisprovided.
• The model does not take into account the use of real radio equipment with cables,
noise, and the need to transmit information with a low bit error rate.
D. Future Work
Our simulation could be extended and improved byincreasing the complexity of the
data used, and reducing assumptions. If wegained access to or created a model of iono-
spheric conditions with time, wecould make the time an input to our model. With a full
globallanddataset,wecouldtiethelatitudeandlongitudetoterrainaswellastheiono-
sphere,andmaketheterraindeterministicforagivenlocation.Inaddition,withmoretime
wecouldincludebiggerlandandwaterpatches,solargerfeatureswoulddominateinstead
ofverylocalones. Lossaccuracycouldbeincreasedbyaccountingforthesignalphaseand
interferencethroughoutthepropagation,aswellasconsideringrealradioequipment.
Furthermore,wecouldgaingreaterunderstandingoftheaccuracyofourmodelcom-
pared to real skywave signals by finding an empirical data. For instance, if we found
recordedinformationabouttheequipmentused,transmitandreceivelocations,andexact
dateandtime,wecoulduseanionospheredatasetforthatdaytosimulatetherealcontact.
WecouldseewherethesignalsbouncedontheEarth,andwhatpowerweexpectthemto
arrive with, to see if our model is accurately recreating trajectory and loss.


## 第 22 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#76271 21of30
IX. Letter
Skywavecommunicationremainstheonlynon-line-of-sightmethodofradiocommu-
nication over vast, turbulent oceans and disruptive terrain. While bouncing the signal
betweentheionosphereandthesurfaceoftheEarthallowssignaltransmissionoverlong
distances,itintroducestheunpredictabilityoftheionosphericdensity,thenon-uniformity
of reflection surfaces, and signal deterioration overthe path of the signal.
Our model simulates a transmitter at an initial latitude and longitude on a spherical
EarthbeamingaHF(between3MHzand30MHz)signalwithaninitialbearingandeleva-
tionangle. Foroursimulation,weassumea100-Watttransmitterwitha100-meterdipole
antenna. The model of the ionosphere wasadapted from a gradient set of data collected
by NASA (see NASA’s International Reference Ionosphere data set). Using the variable
density,wecandeterminetherefractionofthesignalateachlayerofthe ionosphere.
Oncethesignalexitsthebottomoftheionosphere,itcontinuesonitstrajectorytowards
asimulatedpatchofterrainusingeitherawavesimulatororgeologicalelevationdata.From
thisbouncewedeterminetheimpactlossandthenewtrajectoryofthesignal.Weiterate
this process until the signal falls below the sensitivity of the radio receiver.
Withthepathdetermined,wecalculatethelossalongthepathofthesignalconsidering
freespacepathlossduetospreadingalongdistance,ionosphericabsorptionloss,andreflec-
tionlossfromscattering. Whileothersourcesoflossexistinrealsystems,wedetermined
thatthesethreelossesconstitutemostofthelossincurredduring transmission.
Due to the unpredictability of the ocean and of terrain, we test skywave paths that
bounceoncalmandturbulentwater,aswellassmoothandmountainousland. Wedothis
byrandomlyvaryingtransmitterlocations,andtestpathsfromcoastalcitiestodetermine
themaximumeffectivetransmissiondistance.
Weobservethelargestdifferenceinourresultswhenvaryingfrequencyandelevation
angle. Todeterminetheirrelationtoone-another,weco-varythefrequencyandelevation
angle. Fromthis analysis, wefind an effective angle and transmission frequency around
10°and20MHz. Lowerfrequencyandhigheranglepairs,suchas30°and3MHztendsto
bouncemore,buttravelalowerdistance.Theeffectivenessoftheradiowavesrangingabove
50°and15MHzquicklydissipates,asthesewavesareeitherabsorbedintheionosphereor
launchedintospace.
Wealso explore our models sensitivity by altering the waveconditions from calm to
super-turbulent,increasingthetransmissionpower,andchangingionosphericdensity.Of
these factors, the ruggedness of the terrain has the largest influence of the dispersion of
thesignal, whiletheionosphericdensity(heavilyinfluencedbysunspotnumber)causes
ourwavesto be absorbedorlostinspace.
Inourmostrealisticsimulation,wesendasignalfromHondurasdirectlysouthwestat3
MHzandavaryingelevationangle. Wefindthatthesignaldistancerangesfrom187.67km
to 1622.24km in a straight line from the shore. The signal as it first bounces is fairly
concentrated,whilethesecondarybouncesshowsanear-chaoticdispersionofthesignal
fromtheroughnessofthewaves.This600raysimulationdemonstratestheunpredictability
ofthespreadofHFradiowavesonroughterrain. Theseresultsdemonstratethecausefor
dead-zonesofskywavesignals,especiallyontheopen ocean.
Insummary,ourmodelconsidersthemostsignificantfactorsinmodelingthebehavior
ofHFradiowaves.Throughtheseconsiderationsandoursensitivityanalysis,wequalita-


## 第 23 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#76271 22of30
tivelymatchknownradiowavebehavioraswellasapproximaterangesexpectedfromthe
transmission systems described above. Thus, wehold this model to be a useful tool for
radioenthusiastsandprofessionals alike.


## 第 24 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#76271 23of30
References
1“The History of Communication Technology,” https://www.conferencecallsunlimited.com/
history-of-communication-technology.Accessed:2018-02-10.
2“ReportandMinutesofProceedings,”Tech.rep.,InternationalConferenceonSafetyofLifeatSea
CommitteeonLifeSavingAppliances,1914.
3“What Marine Communication Systems Are Used in the Maritime Industry?” https://www.
marineinsight.com/marine-navigation/marine-communication-systems-used-in-the-maritime-industry. Ac-
cessed:2018-02-10.
4MCM2018:ProblemA,MathematicalContestinModeling,COMAP,Web,2018.
5Barclay,L.andofElectricalEngineers,I.,PropagationofRadiowaves,ElectromagneticWaves,In-
stitutionofEngineeringandTechnology,2003.
6Scientific,C.,“LinkBudgetandFadeMargin,”https://s.campbellsci.com/documents/us/technical-
papers/link-budget.pdf,2016.
7Wescom,G.,“JustaDipole,”,2007.
8ModelingthePropagationofSignals,MATLABDocumentationCenter,Accessed:2018-02-10.
9Farahmand, F., “Channel Modeling and Characteristics,” https://web.sonoma.edu/users/f/
farahman/sonoma/courses/cet543/lectures/2011Lectures/ChannelModelsF13.pdf,SonomaStateUniver-
sity,2014.
10ElectronicsNotes,“IonosphericLayers:D,E,F,F1,andF2Regions,”https://www.electronics-notes.
com/articles/antennas-propagation/ionospheric/ionospheric-layers-regions-d-e-f1-f2.php,Accessed:2018-
02-10.
11Gannon,M.,“Sun’s2013SolarActivityPeakIsWeakestin100Years,”https://www.space.com/
21937-sun-solar-weather-peak-is-weak.html,Accessed:2018-02-11.
12Survey,U.S.G.,“ShuttleRadarTopographyMission(SRTM)1Arc-SecondGlobal,”https://lta.
cr.usgs.gov/SRTM1Arc,Accessed:2018-02-11.
13“InternationalReferenceIonosphere,”https://iri.gsfc.nasa.gov/.Accessed:2018-02-10.
14“SeaStates,”https://manoa.hawaii.edu/exploringourfluidearth/physical/waves/sea-states,Univer-
sityofHawaii, 2018.
15Davies,K.andofElectricalEngineers,I.,IonosphericRadio,ElectromagneticsandRadarSeries,
Peregrinus,1990.
16“Calculatedistance,bearingandmorebetweenLatitude/Longitudepoints,”http://www.
movable-type.co.uk/scripts/latlong.html,Accessed:2018-02-11.
17Hoki,“MATLAB/CUDA:oceanwavesimulation,”https://stackoverflow.com/questions/28279337/
matlab-cuda-ocean-wave-simulation,Accessed:2018-02-11.
18Stroobandt,S.,“WorldAtlasofGroundConductivity,”http://hamwaves.com/ground/en/index.
html,Accessed:2018-02-10.
19deGreve,B.,“ReflectionsandRefractionsinRayTracing,”https://graphics.stanford.edu/courses/
cs148-10-summer/docs/2006--degreve--reflectionrefraction.pdf,StanfordUniversity,2006.
20ElectronicsNotes,“IonosphericLayers:D,E,F,F1,andF2Regions,”https://www.electronics-notes.
com/articles/antennas-propagation/ionospheric/skywaves-skip-distance-zone.php,Accessed:2018-02-11.
21“GoogleMaps,”https://www.google.com/maps/,Accessed:2018-02-12.


## 第 25 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#76271 24of30
X. Appendix
Diagram of Calculated Ionosphere Trajectory
Thisplotprovidesanexampleofourionospheremodel,illustratingthebendingofthe
signalbeforeitis reflected.
Figure5.ExampleIonosphereSignalTrajectory
Example Terrain with Vectors
Theseplotsdemonstratetheterraingenerationandvectorreflectioncalculations. The
axes describe the x and y locations, as well as height, in meters. The local vectors are
positioned at every mesh-point to illustrate the local calculations. The mean vectors are
shown tothe side inred and yellow. Land is shown ingreyand water inblue. The water
plotisformattedidenticallytoland,exceptthelocalnormalvectorsareomittedforclarity.
Figure6.Incident,Normal,andReflectedRaysOffRandomMountainousTerrain


## 第 26 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#76271 25of30
Figure7.IncidentandReflectedRaysOffRandomCalmWaves
ModelValidation:Comparing Absorbed and Escaped Signals to Modeled Electron Density
Figure8.OceanicBounceLocationsPlottedOverIonosphereElectronDensity


## 第 27 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#76271 26of30
Figure9.ProbabilityofEscapingtoSpaceVersusIonosphereElectronDensity
Signal Remaining After First Bounce for Water (PartI) and Land (PartI)
Figure10.AveragePowerDirectlyAfterFirstBounceforCalmandTurbulentWater


## 第 28 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#76271 27of30
Figure11.AveragePowerDirectlyAfterFirstBounceforSmoothandRuggedTerrain
Results ofFrequency and Elevation Angle Sweep Sensitivity Analysis
Figure12.AverageNumberofBounces


## 第 29 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#76271 28of30
Figure 13. Net Arc Length on the Earth fromthe StartingPointa.k.a. TotalDistance in km
Figure14. PercentageofSignalsthatareAbsorbedbyLossasOpposedtoEscapingtoSpace


## 第 30 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#76271 29of30
Results ofOcean Turbulence Sensitivity Analysis
Figure15.TotalDistanceTravelledRelatedtoOceanTurbulence.Calmdistancesaresta-
tisticallydifferentthanbothturbulentoceans.
Results ofTransmit Power Sensitivity Analysis
Figure16.TotalDistanceTravelledRelatedtoInitialPowerofSignal


## 第 31 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#76271 30of30
Results ofIonosphere Electron Density Sensitivity Analysis
Figure17.TotalDistanceTravelledDependingonSolarActivity
Results from Geographic Locationsin Part III
Figure18.DispersionofRadioSignalOriginatingfromHonduras

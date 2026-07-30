# A86103-Simulation Analysis of Multi-hop HF Radio


## 第 1 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
TeamControlNumber
Forofficeuseonly Forofficeuseonly
86103
T1 F1
T2 F2
T3 ProblemChosen F3
T4 A F4
2018
MCM/ICM
SummarySheet
Simulation Analysis of Multi-hop HF Radio
Summary
HFradiopropagation plays anextremely importantrole incommunication at seaand
mountains. It may be influenced by various factors, resulting in great loss of signal
transmission. In this paper we focus on transmission and reflection loss of HF radio
propagationinreflectingsurfacechanges.
First, according to the PMwave spectrum and randomwave theory,we establish a
three-dimensional random wave model to simulate the motion of waves. On this ba-
sis,weanalyze the reflection of electromagnetic waves on theseasurface. Weconsider
theinfluenceofwaveheightcausedbydifferentwindlevelsonthereflectioncoefficient
and obtain the reflection loss of electromagnetic wave under different conditions suc-
cessfully.ThenwegetthesumofthelossinthetransmissionandtheThefirstreflection
intensityoftheturbulentoceanandthecalmone.Atlastweanalyzethesignalelectric-
fieldandatmosphericnoiseelectricfieldofthereceivingpoint,gettherelationbetween
SNR, transmission distance and hops, and the maximum number of hops should be 6
whenSNRattenuatesto10dB.
Second,weanalyzethetransmissiononthegroundonthebasisofthewavemodel.
Wesimulate the topography with the wave fluctuation. Because the electromagnetic
characteristicsoftheeartharedifferentfromtheseasurface,wecorrecttherelativedi-
electricconstantandconductivity.Sincetherearemoreobstaclesonthegroundthanon
thesea,sowealsoanalyzethediffractionphenomenonofelectromagneticwaveprop-
agationontheground.Wecalculateandcomparethefirstreflectionintensitybetween
mountainousorruggedterrainandsmoothterrain.Surprisingly,theeffectivedistance
ofsky-wavetransmissionisshorterthanthatof seasurfacereflection.Underthesame
conditions,themaximumnumberofhopsofHFradiopropagationis4.
Finally,weconsiderthewindandwavesthattheshipmayencounterontheseasur-
face,andcalculatethelongestdistancethatthereceivedsignalcanpropagateatagiven
wind level (i.e., SNR not less than 10 dB). Because ships usually travel longer,we also
analyzetheperiodicvariationoftheionospherewithtime,andobtaintheinfluenceof
the periodic variation of the ionosphere on the propagation of sky wave. On the basis
ofthis,wegettheoptimalradiofrequencyunderdifferentconditions.Aftertakingthe
ship speed into account, we amend the original model and obtain the maximum time
fortheshiptomaintainthesamemulti-hoppath.


## 第 2 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Simulation Analysis of Multi-hop HF Radio
Abstract Transmission loss analysis
HF radio is widely used in long-distance In the process of transmission, SNR of
propagation in a lot of countries because of its the signal may be reduced due to various
advantages of long propagation distance, low factors. For a fixed reception point, the loss of
transmission loss and no external influence on the signal is related to the angle of the signal
the quality of propagation, especially maritime emission, the transmission distance, the
propagation. Because it is capable of ionospheric absorption intensity, sea situation
reflections off the ionosphere and the earth, and so on. We have a simple classification of
"jumping" to its destination. Besides, the the loss of the signal: free space transmission
characteristics of the reflected surface loss, ionospheric absorption loss, additional
determine the intensity of the reflected waves lossandseasurfacereflectionloss.
and the extent to which the signal eventually Then, we lay special stress on the
travels. In this paper, we simulate different relationship between sea surface reflection
environments of the ocean and ground, and loss and various factors. By simulating the
obtain the degree of signal loss and the reflection path, we study the relationship
propagationdistancefinally. between reflection path and reflection
coefficient, and draw the conclusion that when
Ocean wave model
the hop count is 1, the relationship between
According to the wave spectrum and the first reflection intensity and the wind
random wave theory, we take the actual wave scaleisasfollows:
as the superposition result of sinusoidal wave
with different frequency, different propagation
direction, different wave height and different
initial phase. Then we establish the Longuet-
Higgins long peak wave model. On this basis,
we analyze the possible superposition of
waves, and get the three-dimensional
simulation diagram of the waves, and simulate
it.
Figure2Therelationshipbetweenthewindscale
andthefirstreflectionintensity
Inlong-distancepropagation,thenumberof
multi-hopisoftengreaterthan1sothatthe
wavecantravelenoughdistance.Butthe
integrityofthesignalalsoattenuatesgradually
withthepropagation.Bycalculation,weknow
thatthemaximumnumberofhops at calm
seais6whenthepoweris100wandthe
frequencyis15 MHz.
Figure1Thewavesituation
whenthewindscaleis6


## 第 3 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Compare with the Modification based on
model on the ground navigation
Based on the three-dimensional wave model, In the actual navigation, the receiving point is
we simulate the relief of the terrain with the motional. Thus, it cannot be regarded as a
wave fluctuation. Considering diffraction may fixed point and to be calculated. So we
occur during the ground propagation, and the modify the model to calculate the emission
variation of the conductivity and relative angle, frequency, power and so on as variables.
dielectric constant caused by the complex Based on these, we obtain the maximum
ground. We modify the existing models, distance and the time to maintain the same
calculate the first reflection intensity and the multi-hop path before the SNR attenuates to
maximum number of hops on different 10 dB. We also conclude that the absorption
groundforms. loss will increase due to the periodic variation
of the ionosphere. So the launch frequency
needstobeadjustedatdifferenttimes.


## 第 4 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#86103 Page1of25
Contents
1 Introduction 3
1.1 Background.................................................................................................................3
1.2 Restatementoftheproblem......................................................................................3
2 Assumptions 3
3 Notation 4
4 Radio propagation on seasurface model 4
4.1 IntroductiontoHFpropagation...............................................................................4
4.1.1 WayofHFpropagation.................................................................................4
4.1.2 Structureofionosphere.................................................................................5
4.1.3 Bestusablefrequency....................................................................................5
4.2 Wavemodel.................................................................................................................6
4.2.1 Longuet-Higginswavemodel...................................................................6
4.2.2 Threedimensionalwavemodel...................................................................6
4.2.3 Modelsimulation...........................................................................................7
4.3 TransmissionlossofHFradiowavesL b.................................................................7
4.3.1 FreespacetransmissionlossL bf...................................................................8
4.3.2 IonosphericabsorptionlossL a......................................................................8
4.3.3 SeasurfacereflectionlossL g.........................................................................9
4.3.4 AdditionallossY P.........................................................................................12
4.4 Firstreflectionintensity...........................................................................................12
4.5 CalculationofSNR...................................................................................................13
[10]......................................................................................................................................
4.5.1 HFsky-wavefieldintensity 13
4.5.2 Fieldintensityofatmosphericnoise.........................................................14
4.5.3 Maximumnumberofhops.........................................................................14
5 Comparisonbetweenseasurfacemodelandgroundsurfacemodel 15
6 Motion analysis ofships using HF radio propagation on turbulent ocean 16


## 第 5 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#86103 Page2of25
6.1 Maximumtime(t )usingthesamemulti-hoppath.........................................16
max
6.2 Suggestionsonfrequencyselectionoftransmitter..............................................18
7 Strengthsandweaknesses 18
7.1 Strengths....................................................................................................................18
7.2 Weaknesses................................................................................................................18
Appendices 21
Appendix A Firstappendix 21


## 第 6 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#86103 Page3of25
1 Introduction
1.1 Background
It is universally acknowledged that a ship sailing in the boundless sea will encounter
a variety of danger at any time. Withthe increasing number of ships in theworld and
thetrendtowardlarge-scaleandhigh-speedoceanshipping,theworld’swaterwaysare
becoming more and more crowded and crisis may occur at any time. In this case, HF
radiopropagationhasplayedasignificant role.HFradiopropagationcanattractusto
transmitting messages, thats mainly because that HF communication can be achieved
onlybyappropriatetransmittingpowerandmoderateequipmentcostevenfarapart.
1.2 Restatement of theproblem
Asrequiredbythequestion,wearesupposedtodeterminethestrengthofthefirstre-
flectionoffaturbulentoceanandcompareitwiththestrengthoffacalmocean.Mean-
while,wewillalsodeterminethemaximumnumberofhopsthesignalcantakebefore
its strengthfalls below ausableSNR. Afterthat, wewill comparethefindings with hf
reflections off different topography. Moreover, we are going to change our model to
accommodateashipboardreceivermovingonaturbulentocean.
Therearetwoformsofshortwavepropagation.Oneisgroundwave,whichconsists
ofsurfacewave,directwaveandreflectedwave;andanotherisskywavethatreaches
the ground reception point being reflected by the ionospheric. In this article, we only
modelthereflectionofskywaves.
2 Assumptions
Weconsiderthetransmissionofskywavesasthemainway.
Reason: Energy is lost with the propagation of ground wave, and the higher the
•
frequency(that is, the shorter the wave length), the greater the loss. However,
sky-wave communication has the advantages of long propagation distance, low
transmissionlossandnotbeingaffectedbythegeologicaltypesofbothsides.So
weconsiderthetransmissionofskywavesasthemainway.
The reflection of sky-waves in the ionosphere is mainly considered in the F 2
layer.
•
Reason:(1)It’sexistall day.(2)It’sheightcanaccommodatethelongestpath.(3)
MUF(maximumusablefrequency)isthebiggest.
Themainfactoraffectingwaveheightiswindspeed.
•
Weregard the relative permittivity and conductivity of seawater as fixed values.
Reason:Thechangesofrelativedielectricconstantandconductivityaremainly
•


## 第 7 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#86103 Page4of25
causedbythechangeof saltcontentandtemperature,andthewaveandseawa-
termotionhavelittleeffectonthem,sowethinkthattheyarealmostunchanged,
andregardthemasfixedvalues.
Weconsider ships movement on the sea asa uniformmotion.
•
3 Notation
Notation Definition
L Transmissionloss
b
L bf Freespacetransmissionloss
L Ionosphericabsorptionloss
a
L Groundreflectionloss
g
ε Electricmediumconstant
σ Conductivity
Y Additionalloss
P
r Propagationdistance
D Maximumpropagationdistance
∆ Elevationangleoftransmission
n Numberofhops
f Workingfrequency
P
0
Powerofthetransmitter
P Firstreflectionintensity
1
R Reflectioncoefficient
θ Incidenceangleofelectromagneticwave
P.s.Othersymbolsinstructionwillbegiveninthetext.
4 Radio propagation on sea surfacemodel
4.1 Introduction to HFpropagation
4.1.1 Wayof HFpropagation
HFpropagationistheradiopropagationofradiowavesintherangeof3to30MHz(corre-
sponding wave length 100 to 10m). HF communication has the advantages of long
communication distance, strong persistence and simple equipment,meanwhile, it has
the disadvantages of channel congestion, time-varying, dispersion characteristics, and
soon. Moreover,itiseasytobeinfluencedbyotherexternalfactorsandisunstable. HF
propagationcanpropagatealongthegroundastheground-wave,anditcanalsoprop-
agatethroughreflectionsofftheionosphericasthesky-wave. Thepropagationdiagram
isasfollows:


## 第 8 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#86103 Page5of25
Figure1HFpropagationdiagram
4.1.2 Structure ofionosphere
Ionosphereisaionizationregionoftheearthsatmosphere.Itisionizedbyhighenergy
radiation from the sun and cosmic rays. For the existence of a huge number of free
electrons and ions, radio waves can change the speed of propagation ,and refraction,
reflection and scattering occurred. The ionosphere can be divided into layer D, E, F
[1]
andsoon,andthelayerFcanbedividedintoF andF .Theheightofeachlayer
1 2
changesovertime,andsomelayersevendisappearatnight.
Figure2Innerlayersofionosphere
4.1.3 Best usablefrequency
Accordingtothetheoryofionosphericpropagation,shortwavewithahigherfrequency
canonlyreturntothegroundfromthereflectionoffionospherewithahigherelectron
densitydistribution.Thereisamaximumfrequencyofradiowavesthatcanbereflected
backtotheground,whichwecallMUF(maximumusablefrequency).thefrequencyof
propagation should be as high as possible to reduce absorption, but generally only at
thefrequencyof 0.85MUF.Because if we use MUF,as long as the ionosphere changes
slightly,theradio waves would go through theionospherewithout goingback. So we
[2]
callthefrequencyof0.85MUF thebestusablefrequency.


## 第 9 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#86103 Page6of25
4.2 Wavemodel
4.2.1 Longuet - Higginswavemodel
Thewavephenomenonisverycomplex,anditsspeculativeandnonlinear.Therefore,it
is very difficult to establish an accurate wave model. According to the wave spectrum
andrandomwavetheory,wecanregardtheactualwaveastheresultofsinusoidalwave
superpositionwithdifferentfrequency,differentpropagationdirections,differentwave
[3]
heights and different initial phases. The Longuet-Higgins model describes the waves
of long-peak waves by the superposition of countless random cosine waves, and the
amplitudeisexpressedasfollows:
Whereξ referstotheamplitudeoftheicosinewave,ω referstothefrequencyof
ai i
theicosinewave,andε referstothephaseoftheicosinewave.
i
Inpracticalapplications,theLonguet-Higginsmodelisoftenexpressedbythewave
spectrum:
In the formula, S ∆ωis the wave spectrum. At present, there are several widely
ζ
used ocean spectrum,such as Pierson-Moscowitz spectrum(PM spectrum), Neumann
spectrum(N spectrum), ITTC spectrum and so on, among which PM spectrum is the
mostwidelyused.Itcanwellrepresentthefullydevelopedrandomwaves.Therefore,
weusethePMspectrum.AndtheexpressionofPMspectrumisasfollows:
Wherevisthewindspeedwithaheightof19.5mabovethesealevel.
4.2.2 Three dimensional wavemodel
In the above model, we consider only one direction. But in the actual wave, the wave
notonlychangesinheightandfrequency,butalsospreadinmorethanonedirection. So
wedefinethewaveswhicharesuperimposedoneachotheranddiffusedrandomly to
π/2inthemainwaveasthreedimensionalirregularshortpeakrandomwavemodel.
Weoverlaytheabovemodelinmanydirections,andfinallywegetthefollowing
±
expression:
Where ζ , ω , k , µ and ε are the amplitude, the angular frequency, the wave
aij i i j ij
number,thedirectionangleandtherandominitialphaseofthecomponentharmonics,
ε is randomnumber between 0 and π/2, (ξ, η)is the coordinates of a certain point on a
ij
wavesurface.


## 第 10 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#86103 Page7of25
4.2.3 Modelsimulation
WesimulatedthemodelinMATLAB,andtheresultsareasfollows:
Figure3Wavesituationof5 8winds
∼
4.3 TransmissionlossofHF radio waves L
b
Duringthetransmissionofradiowaves,therearemanyfactorsthatcanaffectthetrans-
mission loss. Wedivide the basic transmission loss(L ) during the whole propagation
b
processintofourparts:freespacetransmissionlossL ,ionosphericabsorptionlossL
bf a
,groundreflectionlossL ,andadditionallossY .Ifalllossesareexpressedindeci-
g P
bel(dB),thebasictransmissionlossofsky-wavepropagationisasfollows:
L = L +L +L +Y (5)
b bf i g P
Figure4Partsoftransmissionloss


## 第 11 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#86103 Page8of25
4.3.1 Free space transmission lossL
bf
Thefreespacetransmissionlossisthelossofenergycausedbygeometricfactorsafter
[4]
radiowavedetachingantenna.TheequalityofL isasfollows :
bf
L =32.44+20lgf +20lgr (6)
bf
Wheref isthe workingfrequencyin MHz andristhe effectivepath ofHFradio
propagationinkm.
Thecurvatureoftheearthandtheheightoftheionospherelimittheone-timemaxi-
[5]
:
mumjumpdistanceofthereflectionofftheionosphericD
max
Intheequation,∆ is theminimumelevationangle of theantenna, andweknow
min
that the general elevation angle of the antenna is greater than 3◦. The R is the radius
e
of the earth, and we value it as 6371km. The h is the reflection virtual height of the
ionosphere. The height of each layer is shown in the diagram. For F reflection, the
2
maximumpropagationdistanceD is4000km.
max
4.3.2 Ionospheric absorptionlossL a
In HF radio propagation, the loss caused by ionospheric absorption mainly occurs in
layer D, because there are more neutral molecules in layer D and the collision loss is
[6]
larger . TheconcentrationofelectronsinlayerDdecreasesatnight,andtheabsorption
loss decreases. The loss is mainly non-offset absorption. The emission absorption in
[7]
layer 4 E or F mainly refers to offset absorption . Weignore it in calculation for its
verysmall( 1dB).
≤
Whereϕistheincidentangleataheightof100km,f(MHz)istheworkingfrequency
andf (MHz)isthegyromagneticfrequency,Iistheabsorptionindexandnisnumber
H
ofhopsinthepath.
TheabsorptionindexIis:
I = (1 +0.037R)(cos0.881χ)1.3 (9)
Where R is the number of sunspots and χ is the zenith angle of two 100 km high
absorbs.
For theionospheric absorption loss is relatedto transmitter,issue timeandteh pa-
rametersofreceivingspots,andthatthecalculationistoocomplex,wetakeitas4dBto
makethecalculationeasy.


## 第 12 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#86103 Page9of25
4.3.3 Sea surface reflection lossL
g
(1)Calm seareflection
Formulti-hopseasurfacereflectionlosssupposeincidentwaveismessypolariza-tionThe
energyoftheradiowavesisevenlydistributedonthehorizontalandverticalpolarizations,so
thattheformulaforcalculatingtheenergyis
(10)
WhereRHandRVarethereflectioncoefficientsofhorizontalandverticalpolarizedwaves,
respectively,asfollows:
Whereθistheincidentangle,isthecomplexpermittivityoftheseasurface,εisthe
permittivityofseawater,λisthewavelengthoftheincidentwaveandσisthecon-ductivity.
Accordingtothisformula,therelationshipbetweenR ，R andtheangleofincidence.
H v
Figure5TherelationshipbetweenRH,RVandincidenceangle
Accordingtothefigure,itisnotdifficulttofindthatforthehorizontalpolarizedwave,the
reflectioncoefficientdecreasesgraduallyfrom1,whiletheamplitudeisverysmall.Forthe
verticalpolarizedwave,withthereflectioncoefficientincreaseswiththeincreaseoftheincident
angle,thereflectioncoefficientincreasesto1graduallyafterde-creasingrapidlyatfirst.The
comparisonshowsthatthechangeofreflectioncoefficient


## 第 13 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#86103 Page10of25
ofthehorizontalpolarizationwaveismuchmoresensitivetotheincidentangle.
(2)Ocean WaveModel algorithm for turbulentocean
Forthethreedimensionalirregularshort-peakrandomwavemodelmentionedabove,
werandomlyselectawavecrosssectiontoanalyze.Whentheelectromagneticwave
shinesonthewave,mostoftheavailableelectromagneticwavesareemittedintheform
ofreflectionandscattering,andreflectionisthemainone.
Figure6Diagramofelectromagneticwavereflectiononturbulentocean
Forthewavefunctionξ(x)ofthiscrosssectionatacertaintime,wetakethederiva-
tive of it and obtain the tangent equation of the section irradiated by electromagnetic
wave.
y = ξ′(x)(x x )+y (14)
0 0
Where(x ,y )isthe coordinateofsurfaceelementα.
0 0 −
According to Sneel’s law, we assume that the grazing angle of electromagnetic wave
incidentto planeαis θ,andthen weobtainthepropagationpathequation of reflected
waveasshownbelow:
y = tan(∆ + arctan ξ′(x))(x x )+y (15)
0 0
−
Because the water surface has a certain dip angle, the full incident wave cant be
reflectedinthepositivedirection. Therefore,wedifferentiatethewavesurface,analyze
eachmicro-elementplane,andfindoutthetotalnumberofreflectedwavesreflectedin
theforwarddirection,andgetthecorrectioncoefficientfinally:
m
ρ = (16)
M
Wheremisthetotalnumberofpositiveandnegativereflectionelectromagnetic
wavesandMisthetotalnumberofincidentelectromagneticwaves.


## 第 14 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#86103 Page11of25
Figure7Diagramofwaveshadow
Asshowninthefigure,theactualwaveswillhaveupsanddowns. Especiallywhen
thewindandwavesarehigh,someoftheseasurfacewillbecoveredbythewaves.At
thispoint,wehavecorrectedtheoccludedpart,ignoringthereflectedlightinthatpart.
Thecorrectionmethodisasfollows:
Weobtainthesecondderivativeforwavefunctionξ(x)andobtainthetangentequa-
tion of extreme value point corresponding to its extreme point. Then the second inter-
sectionpointofelectromagneticwaveandwaveistheintersectionpointoftheequation
andwavefunction,andtheshadingistheshadedarea.
S s
ρ′ =ρ (17)
S
−
∗
WhereSisthesurfaceareaofawaveandsistheshadedarea.
Figure8Diagramsofcorrectioncoefficients


## 第 15 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#86103 Page12of25
Inthefigureabove,theleftimageshowsthecorrectioncoefficientsatdifferentwind
speeds when the grazing angle is 1◦/5◦/15◦, and the right image shows the correction
coefficientsatdifferentwindspeedswhenthefrequencyis10MHz/20MHz/30MHz.
Wecangetthefollowingcurve,whichisthefinalreflectioncoefficientbymultiply-
ingitwiththereflectioncoefficientwhenitisstationary:
Figure9Relationcurveofreflectioncoefficientunderdifferentwindspeed
Thenwecangetthelossofturbulentocean:
L′ = L 10lg(ρ′) (18)
g g
−
4.3.4 Additional lossY P
Additionallossisthelosscausedbyotherfactorsinadditiontothemainreasonsmen-
tioned above. The detailed calculation is too complicated, but we conclude that it is
[9]
mainlyrelatedtolocaltime,whichisassumedtobeabout15dBhere .
4.4 First reflectionintensity
Combinedwiththelossanalysisabove,forasinglejumpsignalsource,wecangetthe
followingformula:
10lg(P )=10lg(P ) L L L Y (19)
1 0 bf a g P
− − − −
Amongthem,P (w)istheelectromagneticwavepowerofthetransmittingpoint
1
and P (w) is the first reflection intensity. For the electromagnetic wave propagation
0


## 第 16 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#86103 Page13of25
routewhichhasbeendeterminedinbothtimeandspace,onlyL isalterablebecauseof
g
thedifferentseaconditions,wegetthefollowingchartbycalculation:
Figure10ThestrengthofthefirstreflectionP
1
Table1RelatedParameters
Parameter Referencevalue Unit
L 4 dB
a
Y 15 dB
P
f 100 MHz
P 100 w
0
θ 3 ◦
As is shown in the figure, its the first reflection intensity of a signal with different
frequencies under different wind speeds. We can get the curve of reflection intensity
changing with sea condition by fitting. From the diagram, we can know that the first
reflection intensity decreases with the increase of frequency and the increase of wind
speed. Thus, we must consider the influence of weather in the process of maritime
communication.
4.5 Calculation ofSNR
[10]
4.5.1 HF sky-wave fieldintensity
Thefieldstrengthofthereceivingpointcanbecalculatedbythefollowingformula:
E =137.2+20lgf+10lgP +G L (20)
t 0 t b
−
Intheformula,E(dB)isthesignalintensityofthereceivingpointduringtheprop-
t
agationofskywave,f(MHz)istheworkingfrequency,P(kw)isthepowerofthetrans-
mitter,tt(dB) is the normal gain of the transmitter antenna radiation, and L (dB) is the
b
transmissionlossofsky-wave.


## 第 17 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#86103 Page14of25
4.5.2 Field intensity of atmosphericnoise
[11]
Atmospheric noise is mainlycaused bylightning . It is the main noise source of ma-
rineHFradiopropagationatpresent. Theformulaforcalculatingtheeffectivevalueof
atmosphericnoisefieldintensityisasfollows:
E = F + 10 lg B + 20 lg f 96.8 (21)
n a
In the formula, E (dB) is the field intensity of atm−ospheric noise, F (dB) is the ef-
n a
fectivenoisecoefficientofatmosphericradio,B(dB)istheeffectivenoisebandwidthof
receiver,F(MHz)isworkingfrequency.
AtmosphericnoiseisusuallyestimatedbythenoisedataprovidedintheCCIR322nd
report.Acompletesetofatmosphericnoisedatacontains72charts.Thecalculationpro-
cessisverycomplicatedandtheaccuracyisnothighenough.Thusweusethemethod
ofestablishingadatabasetomakeasimpleestimate.Thefollowingfigureshowsthe
[12]
atmosphericnoisetableatdifferenttimesinacertainareainsummer .
Table2Atmosphericnoiseatdifferenttimesinacertainareainsummer
4.5.3 Maximum number ofhops
AccordingtotheformulaforcalculatingtheelectricfieldintensityofHFsky-waveand
the formula for calculating the effective value of atmospheric noise field intensity, we
obtaintheformulaforcalculatingsignal-to-noiseratioofshortwavesky-wavecommu-
nicationundernaturalconditions.
SNR =201.56+10lgP 20lgf 20lgr 10lgB L L Y F (22)
0 a g P a
− − − − − − −
Intheformula,afternjumps,wefoundthat
r=nD (23)
max
L′ = (n 1) L (24)
g g
L′
a
= n− L×a (25)
Withreferencetothefollowingtablefore×achparameter,wecangetn=6byusing
thefsolvefunctionofMATLAB.


## 第 18 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#86103 Page15of25
5 Comparison between sea surface model and ground surface
model
Becausethegroundenvironmentismorecomplicatedthantheseasurfaceandiscom-
posedofvariousmaterials,wetaketherelativepermittivityof3to8asthebasicvalue
andthegeodeticequivalentconductivityastheelectricalconductivityinthecalculation.
Byusingtheproposedmodelandthealgorithmproposedabove,wetaketheundu-
lationofthemountainasthemotionofthewaveandcalculateitapproximately.Because
there are many obstacles on the ground, the electromagnetic wave will be diffracted
whenitmeetstheobstacle.However,becausetheshortwavewavelengthisnotenough
toavoidobstacles,mostofthemwillbeblockedbyvariousobstacles,sothepropagation
abilityofshortwaveonthegroundisveryweak.Accordingtotheanalysis,wesubsti-
tutetheelectromagneticparametersofgroundintotheformulaandgetthesolutionas
[13]
follows :
Figure11Reflectioncoefficientrelationshipcurvesunderdifferentgroundconditions
Therelatedparametersareshowninthetable.
Table3ε,σindifferentenvironments
Variation Average
Groundform
ε(F/m) σ(S/m) ε(F/m) σ(S/m)
Seawater 80 1 4.3 80 4
Freshwater 80 10−3 2.4 10−2 80 10−3
Wetsoil 10 30 3 10−3 ∼ 2.4 10−2 10 10−2
Drysoil 3 4 1.1 10− ∼ 5 2 × 10−2 4 10−3
∼ × ∼ ×
Thefirstreflectionintensi∼tyinhilly×areasi∼sas×showninthediagram,especially
whentheterrainissmooth,thereliefdegreeis0.


## 第 19 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#86103 Page16of25
Figure12Strengthofthefirstreflection
WetakeL as6.53dBwhenthegroundisflatandwegetthatn=4.Comparedwith
g
the sea surface, the propagation distance of the HF radio through the ground is much
shorterthanthatoftheseasurface.
6 Motion analysis of ships using HF radio propagation on tur-
bulent ocean
6.1 Maximumtime(t )using the same multi-hop path
max
In the above model, we only consider the condition that the reception point is fixed.
This model is applicable to the communication between two fixed points , or the case
wherethepositionchangeofthereceivingpointisnegligible. Theshipintheturbulent
ocean has a long moving distance, so we can not only calculate the effective propaga-
[14]
tiondistancer asafixedvalue . Atthispoint, thepropagationdistancer is related
to the emission angle ∆, and L , L is related to n(the number of hops of sky-wave),
a g
meanwhile,L isalsorelatedtotheemissionangle∆. Toensurethatthereceivedsignal
g
isclearenough,weconcludethattheSNRshouldbegreaterthanorequalto10,thatis:
SNR = 201.56+10 lg P 20 lg f 20 lg r 10 lg B nL (n 1)L Y F 10 (24)
0 a g p a
− − − − − − − − ≥
Throughanalysis,weknowthatsinceL isrelatedto∆,thelongertheroutedistance
g
is, the higher the power transmitter and the increase antenna are needed to assist the
shipintheseacourse. Ortheradiofrequencycanbeadjustedtoavoidoverattenuating
tomaketheSNRtoolowanddifficulttodistinguish.


## 第 20 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#86103 Page17of25
Figure13Relationshipsamongdistance,frequencyandSNR
Asshowninthefigure,SNRof100wsignalisobtainedatthereceivingpointswith
differentfrequenciesanddistances,withthenumberofhopsn=1 6,thewind scale
is5,andthereceivingpointsatdifferentfrequenciesanddistances.
∼
Table4Maximumpropagationdistanc rwhenf=15Hz,P =100w
Numberofhopsn Maximumpropagatioendistancer(km) SNR(dB)
1 3225 54.0977
2 6449 23.2859
3 9674 16.9728
4 10125 10
5 <10125 10
6 <10125 10
Wecanknowfromthefigurethatwhennisfixed,thepropagationdistanceisinsuf-
ficientorthesignal-to-noiseratioistoolowwithincreasingdistance.
Byanalyzingthedataabove,wedrawaconclusionthatwhenthenumberofhopsis
toohigh,fortheshiptravelingontheturbulentseasurface,thesignalreflectstoomany
timesbetweentheseasurfaceandtheionosphere,andthelossofthepropagationpath
is too large, which results in the decrease of the maximum propagation distance. It is
notenoughtospreadthesignalfarenough. Therefore,inthiscase,weneedtoincrease
thetransmissionpowerorsignalfrequencytoincreasethesignal-to-noiseratioandthe
maximumpropagationdistance.
Insummary,themaximumtimeforshipstomaintainmulti-hoppathsinturbulent
oceanis:
t max = v r (27)
Wherevisthespeedoftheshipmovingatsea. Inthecaseofthetableabove,the


## 第 21 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#86103 Page18of25
multi-hop path must be changed for every 3000km movement. In the case of 100W
and15MHz,thesignalpowerandfrequencymustbeincreasedwhenthetransmission
distanceisover10000km.
6.2 Suggestions on frequency selection oftransmitter
Because not only the periodic variation of the ionosphere,but also the influence of the
dayandnight,theseason,thesolaractivityandsoon canaffectthevalueof theiono-
sphericpropagationlossL . Inorderforshipstohavebettercommunicationatsea,the
a
emittermustchoosedifferentfrequencyatdifferenttimetoachievebetterpropagation.
The following table shows the range of radio broadcasts commonly used to take into
accountionosphericeffects:
Table5Recommendedemissionfrequency
2 4MHz Tropicalfrequency,smallnumberofsunspotsandtransmissionisgood.
Somecountriesneartheequatorcanuseitasdomesticbroadcasting
∼
6 7MHz Moresuitableusinginautumnandwinterornightforclose-rangebroa-
dcasting
∼
9 11MHz Moderateandsuitableforall-daybroadcastingbothinsideandoutside
13MHz Effectwouldbebetteratdaytimeandissuitableforlongdistancebroa-
∼
dcasting
15 17MHz Betterinspringandsummer
∼
7 Strengths and weaknesses
7.1 Strengths
Weclassifyandanalyzethepropagationpath,whichmakesourcalculationmore
accurate.
•
Wehaveestablishedathree-dimensionalwavemodel,whichismoreintuitive.
• Weadoptthecorrectionmethodofreflectioncoefficient,whichisdifferentfrom
thepreviousempiricalformula,andcananalyzethereflectioncoefficientunder
•
differentseaconditionsquantitatively.
Wetaketheeffectsofperiodicionosphericvariationsintoaccount,whichare
sensitiveandcanbeusedinvarioussituations.
•
7.2 Weaknesses
WeonlyconsidertheHFsky-wavetransmissionmodel,buttheground-wave
transmissionalsohascertaininfluence.
•
Inreallife,theionosphericlossiscomplicatedandvariesgreatlywithlatitude,
longitude,seasonsandsoon.However,weonlycalculatethereasonable values
•


## 第 22 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#86103 Page19of25
accordingtotheliterature.
Weonlyfocusonthecharacteristicsofshortwavepropagationatsealevelandthe
effectofreflectionwithoutconsideringtheeffectofrefractiondiffraction.
•
The dielectric constant and conductivity of the reflected surface change with the
frequency, but we only use the fixed value to calculate. When the salinity and
•
temperatureofseawaterchangesharply,thereliabilityofthedatawilldecrease.


## 第 23 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#86103 Page20of25
References
[1] LIWei.InfluenceofIonosphericCharacteristicsonShortwaveTransmission[J].In-
nerMongoliaRadio& TVBroadcast Engineering,2016,33(06):68-71. Mathematical
SocietyandAddison-WesleyPublishingCompany,1984-1986.
[2] SHIXiang-tong,WANGLei,HUBo.FrequencySelectionofShortwaveCommuni-
cationRadio[J].ShipElectronicEngineering,2013,33(10):39-41.
[3] QI Ning,XIA Tian,LI Wen-yan,ZHAOLi-guang. Simulationof theMathematical
Model of 3-D Irregular Wave Based on MATLAB[J]. Computer Knowledge and
Technology,2013,9(25):5737-5739.
[4] PENG Feng-hua, ZHOU Xue-jun. Propagation of Maritime Short-wave Telecom-
municationLink[J].ShipElectronicEngineering,2011,31(12):125-127.
[5] ZHAO Yu-cai. Research and Realization on Radio Propagation Prediction and
Interference Analyzing Technology[D]. National University of Defense Technol-
ogy,2009.
[6] YUANXiao-bo.ShortwaveSkyWavePropagationLoss PredictionandPrediction
ofFieldStrength[J].Information&Communications,2013(05):11-12.
[7] LI Xue-hongLI FazhongHAN LongCHEN Lijun. Method and Models of Field
Strength Calculation in HF Sky Wave Communication[J]. Communications
Technology,2016,49(04):418-422.
[8] WANGYing, GU Jian. Research and simulation analysis of radio reflection char-
acteristic over the ocean[J]. International Electronic Elements, 2016, 24(05):113-
115+119.
[9] LUO Jia, ZHANG Wen-ming, WANG Xue-song. Modeling and Simulation of
HFSkywaveTransmissionLossinCommunicationCountermeasure[J].Computer
Simulation,2007(08):28-31+35.
[10] DONG HangXUChiYI TaoHANDong.HFCommunicationAid DecisionMaking
Model basedon SNR Evaluation[J]. CommunicationsTechnology,2014,47(11):1313-
1317.
[11] Qu Gui-cheng, Wang Rui. Research on the Feasibility of Shortwave Commu-
nication at Sea under the Condition of Atmosphere Yawp.[J]. Ship Electronic
Engineering,2009,29(01):92-95.
[12] ZHANGHai-yong.EvaluationofSNRandSIRBasedonHFField-StrengthPredic-
tion[A].ThirteenChineseConferenceSSTA:2011:5.
[13] ZHUANGQian-boSUNFang-gang.InfluenceofDifferentGroundFormsonShort-
waveCommunication[J].ChinaNewTelecommunications,2014,16(09):92+97.
[14] HUANG Fang. Research on Characteristics of Maritime Wireless Radio Propaga-
tionandChannelModeling[D].HainanUniversity,2016,49(04):418-422.


## 第 24 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#86103 Page21of25
Appendices
Appendix A First appendix
Herearesimulationprogrammesweusedinourmodelasfollow.
%Wave situaion
fengji=8;
pinpushu=1000;
jiaodushu=5;
wavewmin = [2.438306 1.462983 1.044989 0.812770 0.664988 0.562683 0.487659 0.430288];
wavewmax = [16.444115 9.866469 7.047480 5.481373 4.484760 3.794799 3.288826 2.90190];
wavewp=[4.053570 2.432142 1.737244 1.351190 1.105519 0.935439 0.810714 0.715336];
%-----------------------------------------------------
u=[3,5,7,9,11,13,15,17];
%---------------------------------------------------
if fengji>8
fengji=8;
end
if fengji<1
fengji=1;
end
fi=fengji;
wmin=wavewmin(fi);
wmax=wavewmax(fi);
wp=wavewp(fi);
ui=u(fi);
M=pinpushu;
N=jiaodushu;
wavewn=(wmax-wmin)/M;
thetawn=pi/N;
dx=1;
dy=1;
x=[0:dx:500];
y=[0:dy:300];
[x,y]=meshgrid(x,y);
z=zeros(size(x));
for wi=1:M
for ki=1:N
theta=-pi/2+(ki-1)*thetawn;
epsin=rand*2*pi;
w=wmin+(wi-1)*wavewn+wavewn/2;
swi=0.81*exp(-7400/(w*ui+eps).^4)*2*(cos(theta)).^2/(pi*(w.^5+eps));
an=sqrt(2*swi*wavewn*theta);
z1=w*w*x*cos(theta)/9.8+w*w*y*sin(theta)/9.8+epsin;
z=an*cos(z1)+z;
end
end
surfl(x,y,abs(z));
shading flat;
colormap ;


## 第 25 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#86103 Page22of25
lightangle(-45,30);
set(findobj(gca,’type’,’surface’),’FaceLighting’,’phong’,’AmbientStrength’,.3,’DiffuseStrength ’Sp
ecularStrength’,.9,’SpecularExponent’,200)
set(gca,’ztick’,[0,5]);
%Figure 5:calculate the relationship between Rh,Rv and incidence angle
thetas=(0:1:90);
theta=thetas./180.*pi;
niu=10;
lambda=1./niu;
epsilon=80-1i.*60.*lambda.*50;
RH1=sin(theta)-sqrt(epsilon-cos(theta).^2);
RH2=sin(theta)+sqrt(epsilon-cos(theta).^2);
RHh=abs(RH1./RH2);
subplot(1,2,1);
plot(thetas,RHh,’LineWidth’,1.5);axis([0 90 0.2 1]);hold;
xlabel(’incident angle(a˛)’)
ylabel(’reflection coefficient’)
RH1=epsilon.*sin(theta)-sqrt(epsilon-cos(theta).^2);
RH2=epsilon.*sin(theta)+sqrt(epsilon-cos(theta).^2);
RHv=abs(RH1./RH2);
subplot(1,2,2);
plot(thetas,RHv,’LineWidth’,1.5);axis([0 90 0.2 1]);hold;
xlabel(’incident angle(a˛)’)
ylabel(’reflection coefficient’)
niu=20;
lambda=1./niu;
epsilon=80-1i.*60.*lambda.*50;
RH1=sin(theta)-sqrt(epsilon-cos(theta).^2);
RH2=sin(theta)+sqrt(epsilon-cos(theta).^2);
RHh=abs(RH1./RH2);
subplot(1,2,1);
plot(thetas,RHh,’r’,’LineWidth’,1.5);axis([0 90 0.2 1]);hold;
set(get(gca,’YLabel’),’Fontsize’,12)
set(get(gca,’XLabel’),’Fontsize’,12)
RH1=epsilon.*sin(theta)-sqrt(epsilon-cos(theta).^2);
RH2=epsilon.*sin(theta)+sqrt(epsilon-cos(theta).^2);
RHv=abs(RH1./RH2);
subplot(1,2,2);
plot(thetas,RHv,’r’,’LineWidth’,1.5);axis([0 90 0.2 1]);hold;
set(get(gca,’YLabel’),’Fontsize’,12)
set(get(gca,’XLabel’),’Fontsize’,12)
%Figure 8:Diagrams of correction coefficients
clc;clear;
niu1=30*10^6;c=3*10^8;niu2=20*10^6;niu3=10*10^6;
theta=1/180*pi;
omega=[0:20];
h=0.0051.*omega.^2;
g1=0.5*(4.*pi.*h.*niu1.*sin(theta)./c);
g2=0.5*(4.*pi.*h.*niu2.*sin(theta)./c);
g3=0.5*(4.*pi.*h.*niu3.*sin(theta)./c);
rou1=1./(sqrt(3.2.*g1-2+sqrt((3.2.*g1).^2-7.*g1+9)));
rou2=1./(sqrt(3.2.*g2-2+sqrt((3.2.*g2).^2-7.*g2+9)));
rou3=1./(sqrt(3.2.*g3-2+sqrt((3.2.*g3).^2-7.*g3+9)));
subplot(1,2,1);
plot(omega,rou1,’r’,omega,rou2,’b’,omega,rou3,’g’,’LineWidth’,1.5);axis([0 20 0.97 1]);hold on


## 第 26 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#86103 Page23of25
legend(’10MHz’,’20MHz’,’30MHz’)
xlabel(’wind speed(m/s)’)
ylabel(’ correction coefficient’)
set(get(gca,’YLabel’),’Fontsize’,12)
set(get(gca,’XLabel’),’Fontsize’,12)
niu=20*10^6;
theta1=1/180*pi;c=3*10^8;theta2=5/180*pi;theta3=15/180*2;
omega=[0:20];
h=0.0051.*omega.^2;
g1=0.5*(4.*pi.*h.*niu.*sin(theta1)./c);
g2=0.5*(4.*pi.*h.*niu.*sin(theta2)./c);
g3=0.5*(4.*pi.*h.*niu.*sin(theta3)./c);
rou1=1./(sqrt(3.2.*g1-2+sqrt((3.2.*g1).^2-7.*g1+9)));
rou2=1./(sqrt(3.2.*g2-2+sqrt((3.2.*g2).^2-7.*g2+9)));
rou3=1./(sqrt(3.2.*g3-2+sqrt((3.2.*g3).^2-7.*g3+9)));
subplot(1,2,2);
plot(omega,rou1,’r’,omega,rou2,’b’,omega,rou3,’g’,’LineWidth’,1.5);axis([0 20 0.84 1]);
legend(’1a˛’,’5a˛’,’15a˛’)
xlabel(’wind speed(m/s)’)
ylabel(’ correction coefficient’)
set(get(gca,’YLabel’),’Fontsize’,12)
set(get(gca,’XLabel’),’Fontsize’,12)
%Figure9 Relation curve of reflection coefficient under different wind
%speed
clc;clear;
theta=87/180.*pi;
niu=(3:30);
lambda=1./niu;
epsilon=80-1i.*60.*lambda.*50;
RH1=sin(theta)-sqrt(epsilon-cos(theta).^2);
RH2=sin(theta)+sqrt(epsilon-cos(theta).^2);
RHh=abs(RH1./RH2);
RH1=epsilon.*sin(theta)-sqrt(epsilon-cos(theta).^2);
RH2=epsilon.*sin(theta)+sqrt(epsilon-cos(theta).^2);
RHv=abs(RH1./RH2);
RH=(power(RHh,2)+power(RHv,2))/2;
theta1=87/180*pi;
c=3*10^8;
nius=[3:30];
niu=nius.*10^6;
h1=0;h2=1.5;h3=3,h4=4.5;
g1=0.5*(4.*pi.*h1.*niu.*sin(theta1)./c);
g2=0.5*(4.*pi.*h2.*niu.*sin(theta1)./c);
g3=0.5*(4.*pi.*h3.*niu.*sin(theta1)./c);
g4=0.5*(4.*pi.*h4.*niu.*sin(theta1)./c);
rou1=1./(sqrt(3.2.*g1-2+sqrt((3.2.*g1).^2-7.*g1+9)));
rou2=1./(sqrt(3.2.*g2-2+sqrt((3.2.*g2).^2-7.*g2+9)));
rou3=1./(sqrt(3.2.*g3-2+sqrt((3.2.*g3).^2-7.*g3+9)));
rou4=1./(sqrt(3.2.*g4-2+sqrt((3.2.*g4).^2-7.*g4+9)));
RH_1=RH.*rou1;RH_2=RH.*rou2;RH_3=RH.*rou3;RH_4=RH.*rou4;
plot(nius,RH_1,’r’,nius,RH_2,’b’,nius,RH_3,’g’,nius,RH_4,’y’,’LineWidth’,1.5);
xlabel(’frequency(MHz)’)
ylabel(’reflection coefficient’)
set(get(gca,’YLabel’),’Fontsize’,12)
set(get(gca,’XLabel’),’Fontsize’,12)
legend(’calm’,’level 2’,’level 4’,’level 6’)


## 第 27 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#86103 Page24of25
%Figure11 Reflection coefficient relationship curves under different ground
%conditions
clc;clear;
theta=87/180.*pi;
niu=(3:30);
lambda=1./niu;
epsilon=80-1i.*60.*lambda.*50;
epsilon=8;
RH1=sin(theta)-sqrt(epsilon-cos(theta).^2);
RH2=sin(theta)+sqrt(epsilon-cos(theta).^2);
RHh=abs(RH1./RH2);
RH1=epsilon.*sin(theta)-sqrt(epsilon-cos(theta).^2);
RH2=epsilon.*sin(theta)+sqrt(epsilon-cos(theta).^2);
RHv=abs(RH1./RH2);
RH=(power(RHh,2)+power(RHv,2))/2;
theta1=87/180*pi;
c=3*10^8;
nius=[3:30];
niu=nius.*10^6;
h1=0;h2=1.5;h3=3,h4=4.5;
g1=0.5*(4.*pi.*h1.*niu.*sin(theta1)./c);
g2=0.5*(4.*pi.*h2.*niu.*sin(theta1)./c);
g3=0.5*(4.*pi.*h3.*niu.*sin(theta1)./c);
g4=0.5*(4.*pi.*h4.*niu.*sin(theta1)./c);
rou1=1./(sqrt(3.2.*g1-2+sqrt((3.2.*g1).^2-7.*g1+9)));
rou2=1./(sqrt(3.2.*g2-2+sqrt((3.2.*g2).^2-7.*g2+9)));
rou3=1./(sqrt(3.2.*g3-2+sqrt((3.2.*g3).^2-7.*g3+9)));
rou4=1./(sqrt(3.2.*g4-2+sqrt((3.2.*g4).^2-7.*g4+9)));
RH_1=RH.*rou1;RH_2=RH.*rou2;RH_3=RH.*rou3;RH_4=RH.*rou4;
subplot(1,2,1)
plot(nius,RH_1,’r’,nius,RH_2,’b’,nius,RH_3,’g’,nius,RH_4,’y’,’LineWidth’,1.5);
xlabel(’frequency(MHz)’)
ylabel(’reflection coefficient’)
set(get(gca,’YLabel’),’Fontsize’,12)
set(get(gca,’XLabel’),’Fontsize’,12)
RH_1=-10*log10(RH_1);RH_2=-10*log10(RH_2);RH_3=-10*log10(RH_3);RH_4=-10*log10(RH_4);
subplot(1,2,2)
plot(nius,RH_1,’r’,nius,RH_2,’b’,nius,RH_3,’g’,nius,RH_4,’y’,’LineWidth’,1.5);
xlabel(’frequency(MHz)’)
ylabel(’Sea surface reflection loss’);legend(’calm’,’hills’,’low mountains’,’middle mountains’
set(get(gca,’YLabel’),’Fontsize’,12)
set(get(gca,’XLabel’),’Fontsize’,12)
%figure 13 relationship among distances frequency and SNR
clear;clc;format ;
P=100;B=3000*10^-6;Yp=15;La=4;Fa=80;f=[3:30];
r=[4000:1000:20000];R=6371;h=300;c=3*10^8;flow=3;
n=1;thetas=(3:3:90);theta=thetas.*pi./180;
D=2*R*(acos(R/(R+h)*cos(theta))-theta);
lambda=1./f;
epsilon=80-1i.*60.*lambda.*50;
RH1=zeros(length(theta),length(epsilon));
RH2=zeros(length(theta),length(epsilon));
RHh=zeros(length(theta),length(epsilon));
RHv=zeros(length(theta),length(epsilon));
RH=zeros(length(theta),length(epsilon));
for i=1:length(theta)


## 第 28 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#86103 Page25of25
for j=1:length(f)
RH1(i,j)=sin(theta(i))-sqrt(epsilon(j)-cos(theta(i))^2);
RH2(i,j)=sin(theta(i))+sqrt(epsilon(j)-cos(theta(i))^2);
RHh(i,j)=abs(RH1(i,j)/RH2(i,j));
RH1(i,j)=epsilon(j)*sin(theta(i))-sqrt(epsilon(j)-cos(theta(i))^2);
RH2(i,j)=epsilon(j)*sin(theta(i))+sqrt(epsilon(j)-cos(theta(i))^2);
RHh(i,j)=abs(RH1(i,j)/RH2(i,j));
RH(i,j)=(power(RHh(i,j),2)+power(RHv(i,j),2));%¡ˇn
end
end
rou=zeros(length(theta),length(epsilon));
g=zeros(length(theta),length(epsilon));
niu=f.*10^6;
for i=1:length(theta)
for j=1:length(f)
g(i,j)=0.5*(4.*pi.*flow.*niu(j).*sin(theta(i))./c);
rou(i,j)=1./(sqrt(3.2.*g(i,j)-2+sqrt((3.2.*g(i,j)).^2-7.*g(i,j)+9)));
end
end
RH=RH.*rou;
Lg=-10*log10(RH);
for n=1:6
for j=1:30
thetax=3*j;
L(1,j)=n*D(1,j);
for i=1:28
fs=i+2;
SNR(j,i)=201.56+10*log10(P)-20*log10(fs)-20*log10(L(1,j))-10*log10(B)-n*La-(n-1)*
if i==13
dis(n)=L(1,1)
end
end
end
mesh(f,L,SNR);hold on;
max(n)=min(SNR(:,13))
end

# A76082-HF Radio Propagation under Different Terrains


## 第 1 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
TeamControlNumber
Forofficeuseonly 76082 Forofficeuseonly
T1 F1
T2 F2
T3 ProblemChosen F3
T4 A F4
2018
MCM/ICM
SummarySheet.
HF Radio Propagation under Different Terrains
Summary
Even in the satellite era, high-frequency (HF) signal communication still plays an important
role in everyday communications. In order to clearly understand the communication process of
HF waves and its influencing factors, we first design a mathematical model of signal reflection
off the ocean. Based on this model, we build the ground signal reflection model and compare the
two. Besides, westudy thecommunication process of vessel receivers onaturbulent sea.
Webegin with the establishment of a mathematical model of signal reflection at sea from
two aspects. On the one hand, we study the basic loss of the HF sky wave transmission process.
On the other hand, we investigate the surface properties of the sea. Weclassify the ocean surface
as a smooth and a rough sea. Based on the Fresnel reflection coefficient equation, we obtain the
reflection intensity of rough and smooth sea surface. And their ratio equals to the square of the
roughness correction factor. We select specific parameters for getting the specific value. Then
we get the first reflection power of rough sea surface is 0.4378mW, and the first reflection
power of smooth sea surface is 0.2832mW. The first reflection power of rough sea surface is
0.6469 times smooth sea surface. As a result, using this model, we can easily simulate the multi-
hop path of the signal. Taking the selected specific value as the parameter, we calculate the
maximumnumber ofhops to 8timesifthe signal-noise ratio threshold is notexceeded.
Next, based on the above models, we set up the mathematical model of ground signal
reflection. Similarly, we classify the terrain as a smooth terrain and a mountainous terrain. The
propagation loss of mountainous terrain is classified as diffraction loss of the mountain and
absorption loss of the vegetation. We use Epstein-Peterson method to study the typical double-
edged peak diffraction problem. Through comparison of the two models, we conclude that the
ocean surface ismore suitableforthe transmissionofshortwave skywaves than land surfaces.
What’s more, we introduce the ship sway model to further establish the communication
model of the ship receiver at sea. The ship can maintain communication while traveling in the
signal coverage. We get the longest communication time by calculating the maximum travel
timeof theshipin thesignal coveragearea.
Finally, we prepare a synopsis of the results that are suitable as a short note in IEEE
Communications Magazine.
Wefocus on the transmission process of shortwave skywaves off the ocean. The conclusion
can help inthe communications ofmaritimetransport and fishing industries.
Keywords:Fresnel reflection coefficient equation, Seasignal reflection model, Transmission
loss


## 第 2 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#76082 Page 1of24
Content
1.Introduction...................................................................................................................2
1.1 Restatement oftheproblem..................................................................................2
1.2 Notations..............................................................................................................3
2.Assumptions..................................................................................................................3
3. Skywavebasictransmissionloss................................................................................4
3.1 Loss model...........................................................................................................4
3.2 CalculationResultsAnalysis...............................................................................5
4.TheMathematical Model ofOceansignal’sReflection.............................................6
4.1Basicmodel...........................................................................................................6
4.1.1Seasurface’s plural dielectric constant.............................................................6
4.1.2FresnelreflectioncoefficientofSea......................................................................7
4.2Comparison ofReflection Intensity between Rough SeaandSmooth Sea.........11
4.3Calculation of themaximumnumberofhops.....................................................12
4.3.1Signaltonoiseratiocalculationofshortwaveskywavecommunication............12
4.3.2Calculationresults...............................................................................................12
5.ThecomparisonofGroundSignalTransmissionandSeaSignalTransmission...13
5.1 Themathematical model ofgroundsignalreflection.........................................13
5.1.1Shortwaveskywavepropagationlossinthesmoothterrain...............................13
5.1.2Shortwaveskywaveinmountainousterraintransmissionloss..........................13
5.2 Comparingresults..............................................................................................14
6. Thecommunication model of marineshipreceiver................................................15
6.1 Themodel ofship rocks.....................................................................................15
6.2 Seasignal transmission model ofcombiningshipswaying...............................16
6.3The samemulti-hoppath tomaintaincommunication time................................18
7. SensitivityAnalysis-Time factor...............................................................................19
8 Conclusions..................................................................................................................20
8.1 Strengths.............................................................................................................20
8.2 Weaknesses.........................................................................................................20
References.......................................................................................................................24


## 第 3 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#76082 Page 2of24
1.Introduction
1.1 Restatement of the problem
Thehigh frequency（HF, defined tobe3-30MHz）istheportion ofthe radio frequency
spectrum .The HF band is amajorpart oftheshortwave frequency band, socommunication
at these frequency is often called shortwave radio. Shortwave propagation modes include
groundwave and skywaves. For frequencies below the maximum usable frequency (MUF),
HF radio waves can travel further through the multiple reflections of the ionosphere and the
earth's surface (even to the world). This method of communication is called "skip" or
"skywave".
Many factors affect the propagation of HF skywaves, of which the properties of the
reflecting surface are important. The properties of the reflecting surface determine the
strength of the reflected wave and how far the wave will propagate with the useful signal
integrity. The most important issue is the reflections on the sea. Wedefine the raging sea as
arough sea, and relatively speaking, we define acalm seaas asmoothsea.
Theproblems that we need tosolve in thispaper are:
 Establisha mathematical model ofocean signalreflection.
 Determine a first reflection intensity of a 100-watt HF constant carrier signal
transmitted from a land-based source at the turbulent ocean level. In this paper, we
usethesizeofpower onbehalf ofthestrength ofthesize.
 Compare the above result with the first reflected intensity of the same signal on a
calm ocean surface
 Based on the first issue, the remaining reflections of the radio signals occur on a
calm sea surface. Determining the maximum number of hops the signal can reach
before its strength falls below a usable signal-to- noise ratio (SNR) threshold of 10
dB
 Using the results obtained above compared with the results of high-frequency radio-
wave reflections onrugged versus smoothterrain.
 There is a marine vessel that uses high frequencies to communicate and receive
weather and traffic reports. Transforming the model to accommodate radio
transmissions from the ship's receiver on a raging surface. Calculate the time that
theboat keeps thesignal commutatinginthesame multi-hoppath.


## 第 4 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#76082 Page 3of24
1.2 Notations
Let's first define thelistof notationsused inthis article:
Symbols Definition
 Seawater relative dielectric constant
r
 Seawater conductivity
 Wavelength
f Thebest available radio frequency
R Smooth seareflection coefficient
R Rough sea reflection coefficient

Rough correction factor

 Seasurface dielectric constant
R Horizontal polarized wave Fresnel reflection
H
coefficient
R Vertical polarization Fresnel reflection coefficient
v
SNR Signal to noiseratio
L Skywave basictransmission loss
b
L Transmissionloss offree space
bf
L Ionosphericabsorption loss
i
Y Extrasystem loss
p
2. Assumptions
 Calm sea is equivalent to a smooth sea, so calm sea is thereflection of radio waves is
specularreflection.
 The object of our study is the high frequency band of 3-30 MHz. If the wave
frequency exceeds MUF, the electric wave will enter the space through the
ionosphere and the ionosphere will change frequently. Therefore, the best available
frequency isusually 0.8-0.9times, we conservatively assumethat thebest available
frequency is f  20MHz .
 When the wavelength and the wave height are comparable or even far less than the
wave height, the influence of the shadow effect on the radio wave propagation needs
to be considered. However, this dissertation is not applicable. Therefore, the
influence oftheshadow effect ontheradio wave propagation isignored.
 Assumethat thedirectionalfactorof the emissionand receptionantennas is1.
 Supposetheemitted electromagneticwave is acircularly polarizedwave.
 Assumethat multipathinterferenceisignored


## 第 5 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#76082 Page 4of24
3. Skywave basic transmission loss
3.1 Loss model
In order to clearly describe the spread of the electric wave, we give the figure 1 about a
simplerepresentation ofits jumpingprocess:
Figure1 Signal transmissiondiagram
A radio wave emitted by the terrestrial source first reaches the ionosphere and reaches
the sea level through the reflection of the ionosphere. It is its first hopping process. After
being reflected by the sea, it returns to the ionosphere and returns to the sea for the second
jumpand soon.
We know that, in practice, radio waves produce loss of energy when transmitting.
According to the reason of transmission loss, the basic transmission loss of skywave is
expressed as[1]
L  L  L  L  Y (1)
b bf i g p
Where: L is the transmission loss in free space; L is the ionospheric absorption loss;
bf i
L is reflection loss on the ground; Y is the additional system loss. We mainly discuss the
g p
ionosphericabsorption loss andspace transmissionloss.
 Basictransmission loss infreespace L
bf
Thebasic transmissionloss in free space is theenergy loss. thegeometric diffusion
causes energy lossafter theradio wave leaves thetransmittingantenna. Theformulais [2]:
L 32.4420lg f 20lgr (2)
bf
Where: The unitof L isdB; fis theworking frequency, theunitis MHz;r is effective
bf


## 第 6 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#76082 Page 5of24
path for thepropagation of radio waves, theunit is km.
 Ionosphericabsorption loss L
i
In the ionosphere, there is a region of significant ionization in the atmosphere. In
accordance with the electronic density changes with height, the ionosphere can be divided
into D layer, E layer, F1 layer and F2 layer. The F layer is the reflective layer, because it is
highest and allows the radio waves to travel the furthest distance[3]. Therefore, we consider
thehigh-frequency signalsmainly reflect ontheF1layer (150km-200km) in thispaper.
Since the degree of ionospheric absorption relates to many factors, it is difficult to make
theoretical calculations. So we choosesemi-empirical formula[3-4]:
677.2Iseci
L  100 (3)
bf (f  f )1.9810.2
H
I (1 0.0037R)(cos(0.881))1.3 (4)
i  arcsin(0.985 cos ) (5)
100
Where: f is thefrequency of themagneticswing at aheight of100km; Iis the
H
absorption coefficient, and represents therelationship of theionosphericabsorption and solar
zenithangle  andsunspots R ; i isthe100km-height of theincident angle,  isthe ray
100
elevation.
Under certain circumstances, these parameters can access data to get aspecific value.
 Extra system loss Y
p
Theextrasystem loss is thesum ofthelosses calculated for otherreasons, and accurate
calculation is difficult. Sincetheadditional system loss isbasically afunction ofthe local
time[1],we canestimatethe additionalsystem loss bylookingat thedatasheet.
 Reflection loss ontheground L
g
Ground lossoccurs from theradio wave through the ground reflection. In this model, the
electric wave isreflected onthesea surface, sowe donot consider theground reflection loss.
3.2 Calculation Results Analysis
In order to makethecalculation easily, we choose thetypical numerical valueto
simulate.
Theparameters wechoose are as follows:
Ray elevation = ,Ionospheric height h 200km ,so it iseasy to obtain theffective
path ofradio wave propagation r  2002km.Reflection point(123E,26N ) is located in
theEast ChinaSea； f = 1.24MHz;timepointis 12:00 onJuly1,check thenumberof
H
sunspotsR  110.
Thesun zenithangle can becalculated bythe following formula[4]:


## 第 7 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#76082 Page 6of22
cossinasinS cosacosS cos
x x
S  23.44sin[0.9856(Y 80.7)]
x n
18015(24t8) 0t 8 (6)
S 
y  18015(t8) 8t 24
Where: S isthesun’spoint oflatitude, S isthe sun’spoint oflongitude, Y is the
x y n
numberofdays from January 1each year; tis Beijing time, aisthestudy point’s latitude; 
is thedifference between study point’slongitudeand S .
y
After simulationwe get thetransmission lossL is97.4597dB.
f
Welearn from theformula
P
L  10lg r
(7)
b
P
t
Calculatethe power P ofahigh-frequency constant carrier signal transmitted bya
t
terrestrial source is100W,incident power P reaching theseasurface after transmissionloss
r
is 0.43248mW.
4.The Mathematical Model of Ocean signal’s Reflection
4.1Basic model
The reflection coefficient of sea waves mainly represents the reflection characteristics of
sea waves on the surface of the sea. The reflection coefficient is related to the incident angle
of the sea waves, the size of the waves, the electromagnetic parameters of the sea surface and
otherfactors.
Before studying thereflection characteristics, we first studytheelectromagnetic
properties ofthesea surface. Theelectromagneticcharacteristics of seasurface affect the
sea surface reflection intensity of radio waves, and it is related to the seawater temperature,
salinity, electromagnetic wave frequency and other factors. The complex permittivity of the
seais a parameterdescribing theelectromagneticproperties of theseasurface.
4.1.1 Sea surface’s plural dielectric constant
The plural dielectric constant of sea surface is determined by the relative dielectric
constant ofseawater,sea water conductivityand thewave length,theexpressionis
r
[1]:

= i60 (8)
r
Wecan calculateconstantsand ratiobased onthepolynomial fit function given by
r
ConsultantsCommitteeof theInternational Radio (CCIR).
 Relative dielectric constantofthe seawater


## 第 8 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#76082 Page 7of24

Theexpression ofsea water’s relative dielectric constant is[5]
 70
 f 2253.5895
  1
r  a bf  cf2  df3  ef4 f 2253.5895
Where:
f istheradio frequency, and its unitsis MHz;
a 1.4114535102； b 5.2122497108； c 5.85478291011
d 7.67174231016； e 2.98563181021
 Conductivityof theSeawater
Theexpression ofsea water’s conductivity is[5]
 5.0
 f  1106.207
 rsf tf 2 (10)
 1 uf  uf2  wf3 f  1106.207
Where:
f istheradio frequency, itsunits is MHz;
r  3.8586749； s  9.1253873104； t  1.5309921108
u 2.1179295105； v 6.57275041010； w  1.96476641015
Because we assume f is 20MHz, we can get seawater relative permittivity = 70;
r
seawater conductivity 5.0;Sea surface dielectricconstant    70 4500i 。
4.1.2 Fresnel reflection coefficient of Sea
 Fresnel reflection coefficientof smoothsea
According to snell's law, theFresnel reflection coefficient ofhorizontal and vertical
polarized waves onasmoothsea surface is[5]

sin  cos2
R  (11)
H  
sin  cos2

 
sin cos2
R  (12)
V  
sin cos2
Where:is grazing angleof incidence.
Thecurve in Figure 2reflects therelationship between thepower reflection coefficient
and thegrazing incidence angle


## 第 9 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#76082 Page 8of24
.
Figure 2powerreflection coefficientand thegrazing incidenceangle.
Thegrazing incidence angle is 4590 byobserving, thechange ofthepower
reflection coefficient is not obvious. For convenience ofcalculation, weset the grazing
incidenceangle as 45.
 Fresnel reflection coefficientof roughsea
We can easily get a smooth sea reflection coefficient, in fact, the sea is choppy, so we
continue to study the reflection coefficient of the rough sea. Wave phenomenon is random
and non-linear, so it is difficult to establish an accurate model of waves. According to the
wave spectrum and the theory of stochastic ocean waves, we can regard the actual ocean
waves as the result of the superposition of sine waves of different frequencies, different initial
phases, different directions ofpropagation, and different waveheights..
Figure 3isour simulationofthe waves.
Figure3oceanwavediagram
In theraging sea,wave height, shape, and frequency change rapidly and wave


## 第 10 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#76082 Page 9of24
propagationdirection may change.Tosimplify themodel, we onlyconsider theeffect
offrequency and wave height ontheroughness oftheseasurface.
At present, Pierson-Moscowitz spectrum (Neutron spectrum), NTC spectrum (ITTC)
and two-parameter ITTC spectrum are the most widely used marine spectra. Among them,
PM spectrum is the most widely used, so we use PM spectrum to describe the frequency of
oceanwaves. Theexpression ofPM spectrumis
8.1103g2 g
4
S () exp[0.74( ) ] (13)
 i 5 v
Where: vis theaverage wind speed near the heightof thesea surface.
Figure 4describes thespectrum with thewind speed changes:
Figure4 Wavespectrum
From figure4 we conclude that wind speed is a majorfactor affecting thefrequency of
waves.
Nextwe studythe influence ofwave height onthereflection coefficient. According to
Phillips(1996) wave model asfollows[6-7]:
h 0.0051v2 (14)
Where: h is the root mean square height of the sea surface, v is the wind speed near the
height ofthesea surface.
It is obvious that the high wind speed near the sea surface directly affects the root mean
square of the sea surface. Therefore, we believe wind speed is a common major factor
affecting frequency and waveheight.
It is obvious that the high wind speed near the sea surface directly affects the root mean
square of the sea surface. Therefore, we believe wind speed is a common major factor
affecting frequency and waveheight.
Then we can get rough correction factor expression based on Miller-Brown rough
surfaceapproximation model[8-9]
 exp[2(2g)2]I[2(2g)2] (15)
0


## 第 11 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#76082 Page 10of24
Where: I is thefirst kindof modified Bessel function of order0;
0
gis theseasurface roughness which is used todescribe themagnitudeofsea surface
fluctuations. Theformulais ghsin/。
Figure 5shows theeffect ofwind speed ontheroughness correction factor.
Figure 5Relationshipbetween windspeed andpower reflection coefficient
Figure 5 shows that when the wind speed exceeds a certain level, the roughness
correction factordecreases rapidly withincreasing wind speed.
Because communication at sea is a communication distance, the influence of earth
curvature on the correction factor can not be ignored. D represents the Earth's curvaturefactor,
which is calculation formula16[10]
1

 2GG  2
D 1 1 2  (16)
   
 R G G sin 
e 1 2
Where, G is thedistancefrom theRF transmitting end to thespecular reflection point,
1
and is thedistance from thespecular reflection point to theRFreceiving end, which is
theradius of theearth (theeffective earth radius is 6400km).
Therefore, therough correction factor for earth curvature is taken into account
D.
Weusetheroughness correction factorto approximatethe Fresnel reflection coefficient
ofthehorizontal and vertical polarized waves ofa rough seasurface
R' R
H H (17)
R' R
V V
Depending on therelationship of thewavelength andfrequency cv.Whenwe can
get thefrequency f  20MHz ,wave length 15m. Inthis case, thewavelength is
comparable to theheight ofthewaves, as a result, shadowing may occur,in this article, to
simplify themodel, weassume noimpact.
In order tomeet thecomputing needs,we take sixwind speed v 15m/ s ,then
h 1.1475.Because45 ,Wecan get according to formula (15)The valueof  is


## 第 12 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#76082 Page 11of24
0.8043.
4.2Comparison of Reflection Intensity between Rough Sea and
Smooth Sea
In order to facilitate thestudy,wereplace theintensity withthepower,so thepower
ratio is equal to theratio oftheintensity.
Weset P as outgoing radio wave power for smooth sea surface. Based on the
1
concept ofcircularly polarized waves can bethe formula
Where:R is Fresnel reflection coefficient ofhorizontalpolarized wave on asmooth
H
sea surface;R istheFresnel reflection coefficient of averticallypolarized wave on a
V
smoothsea surface.
Again, weset P as Rough surfaceof theoutgoing radio power.
2
Wecan get
When the electric waves emitted by the terrestrial sources are reflected for the first time,
the incident electric wave power is the same both in the rough sea and in the smooth sea, so
thesea surface reflection coefficient determines the difference between therough seasurface
reflected power and thesmoothsea surface reflected power.
Using equations (17) and(18) wecan easily derive equation 19
Wecan conclude that theratio oftherough seasurface reflected power to thesmooth
seasurface reflected power is equal tothe square oftheroughness correction factorvalue.
Wehave calculated that thevalue oftheincident wave power P is 0.43248mW,
r
according to theformula(18) ,we can get thesmoothsurface ofthefirst reflected wave


## 第 13 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#76082 Page 12of24
power P = 0.4378mW. According to equation (19), wecan calculatethefirst reflected
1
wave power ofrough sea surface P =0.2832mW.
2
We conclude that the radio waves of the frequency 20MHz and the grazing angle 45
propagating under six winds, the first reflection intensity through the rough sea is 0.64689849
timesthe first reflection intensityofthesmooth sea.
4.3Calculation of the maximum number of hops
4.3.1Signal to noise ratio calculation of shortwave sky wavecommunication
 Theelectricfieldstrength ofshortwaveskywavepropagation
Thefield strength oftheHF radio reception can be calculated using Equation21[11]
E  137.2+20lg f 10lg P G  L (21)
t t b
Where: E isthe signal strength ofthereceiving point in theskywave propagation, its
t
unitis dB (v /m );P isthetransmitter transmitpower ,its unitis kW;G is thetransmitter
t
antenna radiation gain,its unitis dB; L is theday-wave transmissionloss.
b
 Atmospheric noisefieldstrength
The maritime shortwave communication under natural conditions is mainly disturbed by
atmospheric noise. The industrial and cosmic interferences are relatively small and will not
beconsidered here.
Atmosphericradio noisefield strength RMS calculation formula[11]
E  F +10lg B 20lg f 96.8 (22)
n a
Where: E is theatmospheric radio noise field strength in dB; F is the effective
n a
noisefigure oftheatmospheric radio in dB; Bis the effectivenoisebandwidth of the
receiver, wecheck thedatatoset its valueto6dB.
 Shortwavesky wavesignal to noiseratio

According to theformula21of signal-to-noise ratio ofsky wavecommunication and
formula22of rms valueof atmosphericnoisefield, we can get theformula ofSNR
SNR 201.5610lgP20lg f 20lgr10lgBL Y F (23)
t t i p a
4.3.2 Calculation results
The 100-watt high-frequency constant-carrier signal transmitted by the land-based
source experienced a power of 0.2832mW after the first reflection at the turbulent ocean
surface.
Becausethe threshold ofsignal available noiseratio (SNR)is 10dB, SNR  10dB .
t
Using thepreviously set parameters and theresulting data, wecalculatethe maximum
numberof hopswe get by8and thehorizontaldistance foreach jump is 400km.


## 第 14 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#76082 Page 12of22
5.The comparison of Ground Signal Transmission and Sea
Signal Transmission
5.1 The mathematical model of ground signal reflection
We have learned from the above analysis that the loss of signal on different reflective
surfaces is different. Next, we continue to discuss the comparison of the signals from
different ground reflections. For ease of analysis, we classify the ground into smooth terrain
and rough terrain.
5.1.1 Shortwave sky wave propagation loss in the smoothterrain
We assume that dry terrain is a smooth terrain that has the least surface obstructions
compared to other terrain. We think that mainly on the smooth terrains produce ground

reflection loss. According to the data[12], we get the relative complex permittivity  of dry
earth equal to 4.According to thefirst question ofFresnel reflection coefficient formula and
transmissionloss formula, we can find asmooth terrain reflection lossof 9.1133dB.
5.1.2 Shortwave sky wave in mountainous terrain transmissionloss
In addition to the reflection loss, shortwave sky wave in the mountainous terrain has the
jungle mountain diffraction loss and sky wave through the jungle leaf loss in the transmission
process [13]
 Thediffraction lossof shortwaveskywavethroughthe junglemountain
In fact, the terrain of the jungle mountains is complex with many obstacles and it is
difficult to accurately predict the diffraction loss of radio waves. In order to simplify the
model, we study double-edged peak diffraction in this paper. According to literature[14], the
Epstein-Peterson method using the equivalent method is an effective way to solve this
problem. Figure 6is aschematic oftheEpstein-Peterson method.


## 第 15 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#76082 Page 14of24
Figure6 Double-edged peakdiffration
a、b、h and b、c、h constitutea single-edged peak. Wecan usesingle-edged peak
1 2
diffraction lossformula respectively calculate a、b、h diffraction lossL1, and then find
1
thediffraction loss between L2
L 20lg(h 2 ( 1  1 )) (24)
1 1  d d
1 2
L 20lg(h 2 ( 1  1 )) (25)
2 2  d d
3 4
Themeaning ofthe parameters in theformula refer to Figure VI.
Afterfinding L1 and L2, acorrection factor L needs to beadded
c
(a b)(b c)
L 10lg[ ]
(26)
c b(abc)
Then thetotal diffraction loss is calculated as Equation 27
L  L  L  L (27)
a 1 2 c
 theloss ofshortwaveskywavethrough theforestleaves
According to theliterature[13],Ls is thelossofradio waves passing through thejungle
leaves, which isexpressed as
L  a s (28)
S L
Where: a isthe jungle attenuation coefficient (dB/m) and s isthethickness (m) of
L
theelectricwave passing through thebushes. The usual skywave modeband (3 <f
<30MHz), a is 0.01-0.1dB/m.
L
5.2 Comparing results
In order to compare themodels, we taketheparameters h h 60m ,a c 100m ,
1 2
b=200m, s=10m, a  0.8.Substituting intotheabove formula, themaximumnumber of
L
hops ofahigh-frequency radio wave transmitted onasmoothterrain is 3and themaximum


## 第 16 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#76082 Page 16of24
numberof hopspropagating inamountainous area is two.
At the same time, we can get smooth or rough sea and smooth or mountainous terrain
wavereflection loss comparison chart, as shown inFigure 7
Figure 7 Losscomparison chart
Analyzethe data, we get thefollowing result:
1. The same radio transmission distance in the smooth ground is greater than the
transmissiondistance in themountainousterrain.
2. The same radio wave transmission loss in the smooth terrain is less than the
transmissionloss in themountainousterrain.
3. The maximum number of hops transmitted by the same radio waves at sea is much
larger than themaximum numberof hopstransmitted onland.
4. The same radio wave transmission loss in the sea is much smaller than the
transmissionloss ofland.
As a result of the analysis, it is easy to obtain that the ocean surface is more suitable for
the transmission of shortwave skywaves than land surfaces. This conclusion is consistent
withexperience.
6. The communication model of marine ship receiver
Due to the fluctuation of the sea, the ship swaying and causing the antenna to change to
radio wave angle will affect the radio loss of the receiving end. We apply the method of
adding the sloshing loss of the ship to the ocean signal reflection model to improve the signal
propagationmodel at sea.
Under normal conditions, theshipborneantenna and theshipare relatively stationary.
Weassumethat themovement oftheship is themovement of theshipborneantenna.
6.1 The model of ship rocks
There are many factors that affect sea surface fluctuation. In thispaper, only the


## 第 17 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#76082 Page 16of24
influence ofwind-induced seawaves is considered.
There are three types of ship shaking, including floating up and down, left and right roll,
pitch before and after. This abstracts the ship's six-degree-of-freedom motion model[15]. As
shown in Figure 8,wecreate a spherical reference frame that is thecenter of theEarth.
Figure8Boatand antennaschematic
Sotheboat's movement can be expressed as:
a.Altitudechanges upand down theZaxis;
b.Swaying around the Xaxis as thecenter ofrotation;
c. tiltaround the Yaxis as thecenter ofrotation;
Because there is nomeasured data ofthe movement ofthevessel, weget themaximum
valueof thesway angle ofthevessel  according to literature[15].
max
 H 
 arcsin max  (29)
max  2 2H 2 
 
sea max
Where: H isthe maximumheight ofthewaves,  is Wavelength of thewaves.
max sea
6.2 Sea signal transmission model of combining ship swaying
Radio waves at seaenvironment propagation modelshown in Figure 8[15].


## 第 18 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#76082 Page 17of24
Figure 9Radiowaves environmentpropagationmodel
Radio waves at seaenvironment propagation modelshown in Figure 8[15].
According to thereceiving and dispatching enddistance, thepropagation distanceis
dividedinto three areas [15]:
Segment A: means from thetransmitting antenna base stationTto thebase station
visiblepoint R ,thedistance is d ;
A 1
Segment B: refers to thevisual pointfrom the basestation R to thelineofsight from
A
thevisual pointR ,the distanceis d ;
B 2
SegmentC: Refers to theshadow area oftheearth beyond the visiblerange ofline-of-
sight R ,the distanceis d .
B 3
In the segment A, a dual-path model considering ship sway is described, and in the
segment B, a single-path model considering ship sway is described, ie a direct path is
considered. Theformula is
L 147.558220lg f 20lg C C (30)
a DP RP
L  147.5582 20lg f 20lg C (31)
b DP
The data[13] shows that in section A, the up-and-down fluctuation has the greatest effect
on sea surface propagation loss compared to the other two types of rocking. In section B, the
influence ofship swaying onreceived power lossis negligible.
With the increase of transmitting and receiving distance, the impact of ship swaying on
radio wave propagation loss is getting smaller and smaller. We assume that the signal will
onlyfloat upand down when thesignal is transmitted in sectionAonly.
Through calculation, we get 1.5dB of ship sway loss in one sending and receiving
process.


## 第 19 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#76082 Page 18of24
6.3The same multi-hop path to maintain communication time
It is assumed that the ionosphere consists of many parallel thin sheets of very thin
thickness with uniform electron density in each sheet. Assuming that the refractive index in
airis 1,thecorresponding refractiveindex of each parallel sheet is
n  n  n  n   n .
0 1 2 3 n
The frequency of the waves, with a certain angle of incidence by the air into the
ionosphere, willoccur continuous refraction. According to therefraction theorem, we get
n sin n sin n sin nsin (32)
0 0 1 1 2 2 n
The ability of the ionosphere to reflect radio waves is related to the frequency of the
waves. At a certain angle of incidence, the lower the frequency of the radio wave, the easier it
is to reflect. When a bunch of high frequency electromagnetic wave with the frequency of 3-
30MHz is injected into the ionosphere from the air at a certain angle of incidence, the waves
of different frequencies will be reflected at different heights of the ionosphere. Its schematic
diagram is shown inFigure10.
Figure10Ionospheric reflection waveschematic
Due to the refraction, the higher frequency electric waves return to the sea after the
ionosphere has been subjected to a horizontal gliding pass. Although the radio waves of
different frequencies spread at different distances, the grazing angles incident on the sea
surfaceare thesame.
Thelocus of thewave propagation is Equation 33.
D=2rb rdr  2rt r 0 2cosdr (33)
r0 r2 rc2os2 rbr r2n2 r c2os 2
0 0
Where:isinitial incident elevation; r is earth radius (6370km); the subscript ofr
0


## 第 20 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#76082 Page 19of24
is ray fixed position.
When HF waves return to the sea, a relatively uniform electromagnetic radiation field is
formed between A and B. We call this area the signal coverage area. In this area, the ship's
antenna can always be in communication. We get the longest communication time by
calculating themaximum travel timeof theshipin thesignal coverage area.
The difference between the propagation distance of the highest-frequency electric wave
and the propagation distance of the lowest-frequency electric wave is calculated by the
formula 33. This difference is the maximum of the signal coverage area. Wetake the speed of
the ship is 30kont, calculate the longest communication time is 15.12 hour. The total
transmissiondistanceis 840km.
7. Sensitivity Analysis-Time factor
Change the time, observe the influence of the changes of each changes on ionospheric
loss.The sensitivity oftimebycalculation isobtained, as shown in thefollowing figures.
Figure11Sensitivityof time(forsignal-noise)


## 第 21 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#76082 Page 20of24
Figure12Sensitivityof time(forionospheric loss)
We can see that the grazing incidence is very sensitive to the parameters of time. It
proves that themodel we established issuitablefor anytime.
On theother hand, theionospheric lossis not very sensitivetotheparameters oftime.
That is tosay, theionospheric losscannot change toomuch.
8 Conclusions
8.1 Strengths
1. This model includes a large number of parameters. These parameters include the loss
of radio transmission, the complex permittivity of the sea surface, and the rough correction
factorand so on.theyhave great practical value and a widerange ofapplication
2. The model is fit for the complex problem of HF waves on different surfaces of the
loss and reflection. These fitting and approximation greatly reduce the difficulty of solving
themodel, and can get the resultsagree well with therealsituation.
3. For the error analysis and sensitivity of the model, we discuss each parameter.
Sensitivityanalysis results showthat ourmodel parameters havea widerange ofapplication.
8.2 Weaknesses
1. This model takes into account too much factors, causing the solving process is
tedious.
2. The solution of the model is limited to the capacity of the computer, and it can't
achievehigheraccuracy。


## 第 22 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#76082 Page 21of24
3.Alargenumber of assumptionsreduce theaccuracy ofthemodel’scalculationresults.


## 第 23 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#76082 Page 22of24
HF Radio Propagation under Different Terrains
Summary Weset updifferent models ofHF radio propagation under different terrains.
KeywordsFresnel reflection coefficient equation, Sea signal reflection model,
Transmission loss
1 Introduction Using this model, we can easily simulate the
Even in the satellite era, high-frequency multi-hop path of the signal. Taking the
（HF）signal communication still plays an selected specific value as the parameter, we
important role in everyday communications. calculate the maximum number of hops to 8
In order to clearly times if the signal-noise ratio threshold is
understand the communication process of notexceeded.
HF waves and its influencing factors, we Next, based on the above models, we
first design a mathematical model of signal set up the mathematical model of ground
reflection off the ocean. Based on this signal reflection. Depending on the surface
model, we build the ground signal reflection characteristics of the ground, we simply
model and compare the two. Besides, we divide the terrain into a smooth terrain and a
study the communication process of vessel mountainous terrain. The propagation loss
receivers onaturbulent sea. of mountainous terrain is classified as
2 Model diffraction loss of the mountain and
We begin with the establishment of a absorption loss of the vegetation. We use
mathematical model of signal reflection at Epstein-Peterson method to study the typical
sea from two aspects. On the one hand, due double-edged peak diffraction problem. In
to the energy loss in the transmission of order to compare the two models, we still
electric waves in the atmosphere, we study use the above-mentioned specific
the basic loss of the HF sky wave parameters to calculate the maximum
transmission process. On the other hand, we number of hops and transmission loss of the
investigate the surface properties of the sea. same radio wave propagating on different
We classify the ocean surface as a smooth ground. The results of the comparison are
and a rough sea. Then, based on the Fresnel shown in Figure 7. We conclude that the
reflection coefficient for both sea types and ocean surface is more suitable for the
the Phillips (1996) wave model, we obtain transmission of shortwave skywaves than
the reflection intensity of rough and smooth land surfaces, which is consistent with
sea surface. And their ratio equals to the experience.
square of the roughness correction factor. What’s more, we introduce the ship
Taking the high-frequency carrier signal sway model to further establish the
with the power of 100 watts as an example, communication model of the ship receiver at
we select specific parameters and calculate sea. The ship can maintain communication
the specific values. The roughness while traveling in the signal coverage are.
correction factor is 0.8043, the first We get the longest communication time by
reflection power of rough sea surface is calculating the maximum travel time of the
0.4378mW, and the first reflection power of shipinthesignal coverage area.
smooth sea surface is 0.2832mW. The ratio 3 Conclusion
of the two is exactly equal to the square of We focus on the transmission process
the value of the roughness correction factor, of shortwave skywaves off the ocean. The
which is consistent with the conclusion. conclusion can help inthecommunications


## 第 24 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#76082 Page 23of24
ofmaritimetransport and fishing
industries.


## 第 25 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team#76082 Page 24of24
References
[1] Ren Z, Xu C, et al. Modeling and Simulation of SNR and SIR in HF Communication
System [J]. CommunicationCountermeasures, 2010, 111(3):29-33.
[2] Zhao X.L, Huang J.Y, et al. Analysis of rader detection ability in evaporation duct
environment [J]. ChineseJournal ofRadio science, 2006,21(6):891-920.
[3]Luo N, WuW,et al. Simulation of Link Budget and Ionophere Characteristic [J]. Ship
Electronic Engineering, 2007,27(1): 132-134.
[4]Jia J, Sheng W,Chen H. Simulation and Analysis of Path Propagation Loss for Sky
WaveOver the HorizonRadar [J]. Morden Defence Technology,2013,41(3): 138-143.
[5]Wang Y,Gu J. Research and Simulation Analysis of Radio Reflection Characteristic
overthe Ocean [J].Electronic Design Engineering, 2016,24(5):113-119.
[6] Jiang Z.H, Huang L.P,et al. One-cycle controller for parallel-connected interleaving
critical continous conductionmode PFC converter[J]. Journal of TsingHua University,2007,
47(7):1197-1200.
[7] LuB，DongW，ZhaoQ．Performance evaluation ofCoolMOSTMand SiCdiode
forsingle--phase power factorcorrection applieations[C].APEC’03，2003,2：651-657．
[8] Miller A.R, Brown R.M, Vegh E. New derivation for the rough surface reflection
coefficient and forthedistribution ofsea-wave elevations [C].IEEE Proc..1984:131,114-116.
[9] Rui G.S, Guo Y, Tian W.B. Roughness Attenuation Factor in the Use of
Electromagnetic Wave Propagation in Evaporation Duct Environment [J]. Journal of Naval
Aeronautical and Astronautical University, 2012,27(5):545-548.
[10] Huang F.Research on Characteristics of Maritime Wireless Radio Propagation and
Channel Modeling [D]. Hai Nan, Hai Nan University, 2015:24.
[11] Xiong H. Radio wave propagation. Bei jing: Electronic Industry
Press,2000.2002:652-663
[12] Zhuang Q.P, Sui F.G. Influence on Different Forms of Ground on Shortwave
Communication[J]. ChinaNewTelecommunications, 2014,9:92.
[13] Jiang C.Y, Jiao P.N. Experimental Research of the Propagation Loss in the Forest
Environment [J].Journal ofChinaInstituteofCommunications,1992,13(2):73-78.
[14] Cheng R.T.The Radio propagation model of ITU-R P.526and diffraction of multi-
edged peak [J]. TheWindowof Industry:51-53.
[15] Huang F.Research on Characteristics of Maritime Wireless Radio Propagation and
Channel Modeling [D]. Hai Nan, Hai Nan University, 2015:24.

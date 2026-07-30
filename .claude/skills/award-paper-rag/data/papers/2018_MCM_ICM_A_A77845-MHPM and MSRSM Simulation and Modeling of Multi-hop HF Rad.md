# A77845-MHPM and MSRSM Simulation and Modeling of Multi-hop HF Radio Propagation


## 第 1 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
Team Control Number
For office use only For office use only
77845
T1 F1
T2 F2
T3 Problem Chosen F3
A
T4 F4
2018
MCM/ICM
Summary Sheet
MHPM and MSRSM: Simulation and Modeling of
Multi-hop HF Radio Propagation
Summary
Based on the properties of the ionosphere and some laws of physics, we
have established a complete mathematical model named MHPM that can well
simulate the refraction and reflection in the propagation of multi-hop high-
frequency radio waves. MHPM can also simulate the distribution of electron
density and refractive index in the ionosphere along altitude. The attenuation of
energy in the D layer ionosphere, the "free-space path loss" and the "energy
loss while reflecting off the ground or sea surface" determine the energy loss
during radio wave propagation, based on which, our model can successfully
simulate the loss of energy during the propagation of radio wave.
Using MHPM, we compare the different effects of the calm and turbulent
sea surface on the energy dissipation of radio waves, and calculate the max-
imum propagation distance and the maximum hop number of several cases
(different frequencies and different grazing angles). We also analyze the in-
fluence of grazing angle, frequency and the wind speed near the sea surface
on the refraction effect of rough sea surface. The MHPM can also be applied
to ground-reflection situations very well, and we find the energy dissipation of
radio waves in ground-reflection case increases rapidly with the increase of
elevation standard deviation.
We propose a radio-wave-emission scheme and establish the Moving-
Ship-Receiving-Signal Model (MSRSM) in order to make the ship receive
sig-nals continuously while sailing on the sea with the same multi-hop path.
Ap-plying MSRSM, we simulate the signal receiving process of the moving
ship, and get the total duration of 46.20 hours to receive the signal
continuously, for a case with the speed of wind near the sea is 20m=s, the
ship speed is 41:67km=h, and the frequency range is 21M Hz 21:45M Hz.
In the sensitivity analysis, we study three factors, which are the electron
concentration in the ionosphere, the altitude of the ionosphere and the wind
speed near the sea. And we analyze influence of their change on the
propaga-tion of multi-hop high-frequency radio waves.
Keywords: multi-hop, MHPM, MSRSM, free-space path loss


## 第 2 页

精品数模资料，T各ea类m比#赛7优78秀45论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店P铺a：ge闵1大of荒3工0科男的杂货铺！
Contents
1 Introduction 3
1.1 Background . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 3
1.2 Problem Restatement . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 3
2 Assumption and Symbols 4
2.1 Assumption . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 4
2.2 Symbols . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 5
3 Multi-Hop Propagation Model 5
3.1 Model Description . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 5
3.2 The Ionosphere . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 6
3.2.1 D-Layer Energy Loss . . . . . . . . . . . . . . . . . . . . . . . . . . . 6
3.2.2 The Refractive Index vs. Altitude and Frequency . . . . . . . . . . 6
3.2.3 E-Layer Refraction . . . . . . . . . . . . . . . . . . . . . . . . . . . . 7
3.2.4 F-Layer Refraction and Reflection . . . . . . . . . . . . . . . . . . . 8
3.2.5 MUF . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 9
3.3 Propagation on The Sea . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 10
3.4 Propagation on The Ground . . . . . . . . . . . . . . . . . . . . . . . . . . . 11
3.5 Free-Space Path Loss . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 13
3.6 Background Noise . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 14
4 Result of Part I and Part II 14
4.1 The Comparison of Strength of Single-Hop Radio Wave Between Calm and
Turbulent Ocean Surface . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 14
4.2 The Multi-Hop Radio Propagation Process on Ocean Surface . . . . . . . . 15
4.3 The Comparison of Strength of Single-Hop Radio Wave Between Rugged
and Smooth Ground Terrains . . . . . . . . . . . . . . . . . . . . . . . . . . 16
5 Moving-Ship-Receiving-Signal Model 17
6 Result of Part III 17
7 Sensitivity Analysis 18
7.1 Electron Density of The E Layer and F Layer . . . . . . . . . . . . . . . . . 18
Team #77845 Page2of 30


## 第 3 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
7.2 The Height of The F Layer . . . . . . . . . . . . . . . . . . . . . . . . . . . . 18
7.3 The Wind Speed Near The Sea . . . . . . . . . . . . . . . . . . . . . . . . . . 19
8 Strengths and weaknesses 19
8.1 Strengths . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 19
8.2 Weaknesses . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 20
Appendices 23
Appendix A A Short Synopsis 23
Appendix B The Code 25
Team#77845 Page3of 30
1 Introduction
1.1 Background
HF radio waves can be transmitted in the following three modes: skywave, ground
wave, direct wave [1]. The "Multi-hop HF Radio propagation" referred in the MCM’s
problem A is an application of sky wave.
Skywave which we use in our model is propagated relying the ionosphere which is
the high-level (80 to 1000 kilometers above the ground) atmosphere ionized by solar
radiation [6]. Because of the multiple reflections off the ionosphere and off the earth, its
propagation distance can be very far, generally more than 9600 kilometers [2]. The
disad-vantage is that it is affected by the climate and the transmission signal is very
unstable. The short-wave frequency band is the best of the skywave propagation.
Figure 1 displays the propagation mode.
Figure 1: Schematic diagram of Skywave reflection[3]
1.2 Problem Restatement


## 第 4 页

精品数模资料，各类T比h赛e 优p秀ro论bl文em、 学d习es教cr程ip、tio写n作 h模a板s 与al经re验ad技y巧 m、amdatel aab 程v序ivi代d 码a资nd料 b等a，si尽c 在ex淘p宝la店na铺ti：on闵 o大f 荒th工e科 男的杂货铺！
trans-mission patterns of high-frequency skywave bouncing between the ionosphere
and the surface of the Earth. After induction and arrangement we distilled the following
ques-tions that we need to consider and decide:
What’s factors about ionosphere need to mainly discuss? Solar activity, seasonal
change and day or night all have impact on the nature of ionosphere just like den-
sity of electrons and the height of the layers.
What’s assuming can not only guarantee the reliability of our model but also sim-
plify it usefully?
How to quantify the influence of different layers in ionosphere on radio waves?
Just like the determination of the reflection, refraction and absorbtion.
How to quantify the influence of different terrains on radio waves? What’s the effects
of obstacles on ground? What’s the differences between quiet sea and rough


## 第 5 页

精品数模资料，T各ea类m比#赛7优78秀45论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店P铺a：ge闵4大of荒3工0科男的杂货铺！
sea? Whether the reflection, angle and attenuation of radio waves will be affected
by different surface of earth?
What’s the main factors affecting the signal transmission’s distance and the hop-
count? And how to calculate the limit distance and the hop-count?
How can we ensure that our model has a range of coverage? In real navigation,
the receiving state changes randomly, and what’s method can we take to make
radio waves arrive at anywhere in an area whose range can be given accurately?
2 Assumption and Symbols
2.1 Assumption
The energy loss of radio waves during the "multi-hop" process contains the
attenua-tion of energy in the D layer ionosphere, the "free-space path loss[4]" and
"reflection off the ground or sea surface" .
In solving the problem, if there is no specific description, the wind speed near the
sea is 8 m/s ( for rough ocean surface), the grazing angle of the electromagnetic
wave is 15 and the radio frequency is 20MHz. According to literature [5], the
average wind speed on the earth is distributed between 4m=s and 12m=s, so we
choose 8m=s as a default case.
The radio wave is simplified as a straight line, like a laser, ignoring the divergence
of electromagnetic waves.
The D layer ionosphere does not affect the propagation path of electromagnetic
waves, but will cause the electromagnetic wave energy attenuation, acting as an
"attenuation layer" . And the energy loss of electromagnetic waves in the D layer
can be calculated by a formula given by Marc C. [1].
The E layer ionosphere is assumed to cause the refraction of electromagnetic
wave only once, does not affect the energy of electromagnetic wave, acting as a
"single-refraction layer" .
The F1 layer ionosphere and F2 layer ionosphere [6] are considered as one layer,
that is F layer, acting as a "refraction and reflection layer" . The radio wave with
appropriate grazing angle and frequency will continuously refract after entering
the F layer and then be reflected back to the Earth’s surface again.
We assume that the electron concentration of the E layer is uniform, that is, the
refractive index n of E layer is constant. We take the refractive index of the middle
height of E layer as its overall refractive index, and assume refraction occurs in
the plane at the middle height of the E layer, that is to say, the refraction occurs
only once when the electromagnetic wave propagates in the E layer.
D layer will disappear at night and the density of E layer will decrease by 90%
after sunset [1]. In our model, to contain more cases, we only consider the case of
daytime, that is D layer is existing, the density of E layer keep constant.


## 第 6 页

精品数模资料，T各ea类m比#赛7优78秀45论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店P铺a：ge闵5大of荒3工0科男的杂货铺！
Only electromagnetic waves with the same frequency can interfere with each other.
The electromagnetic wave transmitting device and the electromagnetic wave re-
ceiving device are reliable and accurate.
Radio-wave transmitters emit radio waves in a precise way that can emit the radio
with the frequency of the target.
Without a specific description, in our model, the default scenario is daylight during
the summer. The wavelength selection of daytime in summer is 20m, 17m or 15m,
which means that the frequency selection 15 Mhz, 17.65 MHz or 20 MHz.
2.2 Symbols
Some symbols used in this paper are listed in Table 1
3 Multi-Hop Propagation Model
3.1 Model Description
In the skywave mode, the refraction and reflection of radio waves in the ionosphere
are influenced by the properties of the ionosphere, and the different ionosphere (i.e. D,
E, F1, F2) are at different altitudes [6] . What’s more, their refractive index, thickness,
position will change with the alternation of day, night and seasons [1]. MHPM takes


## 第 7 页

精品数模资料，T各ea类m比#赛7优78秀45论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店P铺a：ge闵6大of荒3工0科男的杂货铺！
into account the ionospheric effects based on the assumptions presented in the section
Assumption and Symbols.
According to assumptions, in addition to the attenuation of energy in the D layer, the
energy of electromagnetic waves are affected by "free-space path loss[4]" and "reflection
off the ground or sea surface" during the "multi-hop" process. And our model contains
these factors well. The energy loss caused by the reflection of electromagnetic waves on
the surface of the sea or the ground surface is reflected in the reflection coefficient, and
the reflection coefficients of the calm sea and rough sea surface are discussed in litera-ture
[10], what’s more, the reflection on the ground from different terrain is discussed in the
literature [11]. Our MHPM realizes the simulation and analysis of "single-reflection" process
and "multi-hop HF radio propagation" based on the characteristics of electro-magnetic
waves in the process of propagation and reflection and refraction.
3.2 The Ionosphere
3.2.1 D-Layer Energy Loss
According to literature [1], the energy loss of the radio wave whose frequency is f
M Hz in D layer is represented as:
3
where, is the energy loss (dB=km), N is the electron density (m ), v is the collision rate
1
(sec ), and f is the frequency (M Hz). In literature [1], the electron of D layer is very
10 3 6 1
small, so N = 10 m , and the collision rate is 10 sec .
3.2.2 The Refractive Index vs. Altitude and Frequency
Yu Chao et al. analyzed the variation of electron density in ionosphere as well as
the refractive index of the ionosphere with altitude and carried out numerical simulation,
and the comparison between simulation and real ionospheric data in Sanya City and
Wuhan City confirmed the accuracy of their numerical simulation method [12]. So, the
refractive index of the ionosphere can be determined by [12]:
where f is the frequency of the radio wave, and Ne is the electron density, which can be
determined by:


## 第 8 页

精品数模资料，T各ea类m比#赛7优78秀45论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店P铺a：ge闵7大of荒3工0科男的杂货铺！
12 3
The unit of the electron density is 10 m , and the unit of the frequency is M Hz.
Some ionospheric parameters in the Sanya region are given in the literature [12], and
according to B. Zolesi and L. R. Cander, we can get the approximate value of an E-layer
maximum electron density [13]. In order to determine the distribution of the refractive index
and the electron density along the height, we put these parameters of ionosphere into the
Equation 4, Equation 3, and Equation 2 and can get the graphs of the distribution of
the refractive index and the electron density along the height, which is shown in
Figure 2. All these parameters of ionosphere are shown in Table 2.
Figure 2: The distribution of refractive index and electron density with altitude
3.2.3 E-Layer Refraction
We assume the refractive index of the area below the middle height of the the E layer
is the same as that of the D layer. Because we assume that the D layer only acts as
"energy attenuation layer", the refractive index of the D layer is the sameas that of the


## 第 9 页

精品数模资料，T各ea类m比#赛7优78秀45论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店P铺a：ge闵8大o荒f3工0科男的杂货铺！
Table 2: Ionospheric parameters used to determine the distribution of refractive index
and electron density
air. In order to simplify the calculation, we think that the refractive index of air is 1. The
refractive index of the region above the middle height in the E layer is constant, whose
value is the refractive index at the middle height. The refraction process in E layer is a
simple single refraction, as shown in the Figure 3.
Figure 3: A schematic of the refraction of radio waves in the E layer
3.2.4 F-Layer Refraction and Reflection
The propagation of radio waves in the F layer is complex compared to the E layer because
of the reflection of electromagnetic waves in the F layer. We believe that the refractive index of
the electromagnetic wave in F layer varies with the altitude, as de-scribed in the Equation 2.
According to the Figure 2 and Equation 2, the refractive index is gradually reduced with
the increase of the elevation in F layer, which indicates that the electromagnetic wave
will gradually refracted after entering the F layer, and its propaga-tion trajectory will
bend. If the electromagnetic wave path is sufficiently curved before reaching the top
level of the F layer, it can be reflected back to the ground, otherwise the electromagnetic
waves willpenetratetheF layer and goout.
Radio waves cannot return to the ground after passing through the F layer. It is because
the refractive index is increasing when the altitude is higher than the F layer, as shown in the
Figure 2, which leads to a decrease in the bending trend of the propagation path of the
electromagnetic wave. Thus, it is not possible to bend backwards, that is, to bend back
totheground. This phenomenonisshownintheFigure1.
To show more clearly the propagation of radio waves in the F layer, a schematic
diagram Figure 4 based on the "micro-element method" is shown below:


## 第 10 页

精品数模资料，各类比赛优秀论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店铺：闵大荒工科男的杂货铺！
We take a rather small height as the step hstep, dividing the F layer into many parts,
each being considered as a micro-element. According to Snell’s law [14], we can have:


## 第 11 页

精品数模资料，T各ea类m比#赛7优78秀45论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店P铺a：ge闵9大of荒3工0科男的杂货铺！
Figure 4: A schematic of the refraction and reflection of radio waves in the F layer
where, ni, i = 1; 2; ::: can be determined by Equation 3 and Equation 2. So, for each
micro-element, i, through Equation 5 and recursive method, we can get the angle
i and i, then the transverse distance of the radio waves in this micro-element i is:
If the radio waves reflect at the mth micro-element, then the overall transverse dis-
tance traveled by the radio waves from just entering F layer to the mth micro-elements
is:
where, m can be determined by Snell’s law, that is, when m = 90 , it is critical to reflect,
and then, the radio waves begin to reflect.
3.2.5 MUF
To achieve the reflection off the ionosphere, the frequency of radio waves must
sat-isfy the limit of critical frequency and MUF. The literature [1] shows a calculation
formula of the critical frequency and MUF (maximum usable frequency):


## 第 12 页

精品数模资料，T各ea类m比#赛7优78秀45论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店Pa铺g：e1闵0大of荒3工0科男的杂货铺！
where h is the height of the ionosphere, and the unit of the frequency is M Hz. And the
typical MUF is 15 40M hz for daytime, 3 14M Hz for nighttime [1].
3.3 Propagation on The Sea
WANG Ying analyzed the characteristics of the ocean’s reflection on the electromag-
netic wave, and according to WANG Ying, the reflection coefficient of the surface to the
electromagnetic wave can be determined as follows[10]. For smooth ocean surface:
where, "e is the complex permittivity of sea surface, which can be determined as: "e =
70 + i300 , where is the radio wave length.
The reflection coefficient of horizontal polarization wave and the reflection coeffi-cient
of vertical polarization wave are shown in the Figure 5 with the change of grazing angle.
And the frequencies of the subjects are: 15M Hz, 17:65M Hz and 20M Hz.
Figure 5: The reflection coefficient varies with the grazing angle, the left one is the hori-
zontal polarization wave, and the right one is the vertical polarization wave
For the reflection of rough sea surface, literature [10] uses the reflection coefficient
of smooth sea surface multiplying the rough correction factor to approximate, that is:


## 第 13 页

精品数模资料，T各ea类m比#赛7优78秀45论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店Pa铺g：e1闵1大of荒3工0科男的杂货铺！
’
R = ρR (10)
0
where, R is the reflectance coefficient of rough sea surface, R is the reflectance coefficient
of smooth sea surface, and is the rough correction factor, which can be determined by:
The changes of rough correction factor over the grazing angle and the wind speed near
the sea surface are shown in Figure 6. The Figure 6 shows that with the increase of
grazing angle and the increase of wind speed near the sea surface, the rough correction
factor of sea surface decreases gradually. This means that sea-surface-reflected sky-
wave communication will have better effects when the sea is calmer, and reducing the
grazinganglewillalsoenhancethepropagationabilityof radiowaves.
(a)varyingwiththegrazingangle, v=(b)varyingwiththewindspeed, =15
8m=s
Figure 6: Rough correction factor varies with the grazing angle and the wind speed
near the sea surface
3.4 Propagation on The Ground
According to literature [11], the reflection coefficient of electromagnetic wave on flat
terrain can still be described by Equation 9, which is the equation for calculating the
reflectance of sea surface, and the difference is the complex permittivity "e, which
can be determined by "e= "r(f) + i60 (f), where "r(f) is the relative permittivity of the
surface at frequency f and (f) is the conductivity(S=m) of the surface at frequency f.


## 第 14 页

精品数模资料，T各ea类m比#赛7优78秀45论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店Pa铺g：e1闵2大of荒3工0科男的杂货铺！
We take the relative permittivity of the wet concrete as the approximate relative
per-mittivity of the ground surface. According to the literature [15], one can get a
approxi-mate range of relative permittivity of wet concrete, 12-18, and we take 15.
Literature [16] shows that the electrical resistivity of concrete mainly concentrated in 10-
100 m, which means that the conductivity is in 0.01-0.1 S=m, because the conductivity
is the reciprocal of electrical resistivity [17], and we take 0.05. So the reflection
coefficient of horizontal po-larization wave and the reflection coefficient of vertical
polarization wave varying over grazing angle can be drawn as Figure 7.
Figure 7: The reflection coefficient of the plane ground surface varies with the grazing
angle, the left one is the horizontal polarization wave, and the right one is the vertical
polarization wave
For rugged terrain, similar to the situation on the surface of the sea, the refraction
coefficient of the plane ground is also multiplied by the topographic reduction factor s to
approximate the real reflection coefficient [11].
So we can have the changes of the topographic reduction factor s over frequency, ', Sh,
which are shown in Figure 8 and Figure 9.
In literature [18], the standard deviation of the elevation, Sh is divided into four
categories:
Ascanbe seenfromFigure9(b), theroughcorrectionfactordecreasesrapidlywiththe
increaseof elevationstandarddeviation. WhenSh is15m,thetopographicreduction


## 第 15 页

精品数模资料，T各ea类m比#赛7优78秀45论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店Pa铺g：e1闵3大of荒3工0科男的杂货铺！
Figure 8: The change of s over grazing angle
(a)varyingwiththefrequency (b)varyingwiththeSh
Figure 9: The change of s over frequency and Sh
factor is almost 0, which means that when the electromagnetic wave is reflected on the ground
with large elevation standard deviation, the energy will be greatly lost. Figure 9(a) shows that s
decreases as frequency increasing, which means that high-frequency radio waves are more
likely to lose energy when reflected on the ground. And Figure 8 shows that s can also
decrease withthe increase of grazing angle, electromagnetic waves with a small incident
angle are more likely to lose energy when reflected on the ground. Thus, when using
skywave to signal transmission on the ground, people should try to choose
electromagnetic waves with low frequency, and use smaller grazing angle. At the same
time,ground-reflectedskywave communicationismoresuitablefor flat terrain.
3.5 Free-Space Path Loss
We assume that the energy loss of electromagnetic waves caused by the influence
of free-space path loss is always exists as long as the electromagnetic wave is
spreading. According to [4], the free-space path loss can be described as:
F SP L(dB) = 20log10(d) + 20log10(f) + 32:45 (13)
where d id the propagation distance (km) and f is the frequency (M Hz).


## 第 16 页

精品数模资料，T各ea类m比#赛7优78秀45论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店Pa铺g：e1闵4大of荒3工0科男的杂货铺！
3.6 Background Noise
We assume that only the background electromagnetic noise which has the same fre-
quency as the target electromagnetic wave can interfere with the radio signal. And ac-
cording to [19], we get the background noise corresponding to each frequency, whose unit
P
is Fa, which means “dB above KT0b", that is 10log10 KT 0b , where P is the power (Watt)
of radio waves, as shown in Figure 10.
Figure 10: The background noise corresponding to each frequency[19]
4 Result of Part I and Part II
As can be seen from Figure 7 and Figure 5, the reflectance coefficient of
horizontal polarization waves are less affected by the change of grazing angle
than that of vertical polarization waves, both on the surface of ground and ocean.
So, in the model solution, we use the horizontal polarization wave to analyze.
4.1 The Comparison of Strength of Single-Hop Radio Wave
Between Calm and Turbulent Ocean Surface
We simulate a single-hop radio wave, and get the strength (in dBw [20]) of the
wave after the first reflection from the turbulent ocean surface and the calm ocean
surface. Several cases of radio waves with different frequencies, wind speeds and
grazing angles are shown in Table 3. In addition, we draw the changes of the power
ratio between the waves on turbulent and calm ocean surfaces with grazing
angle and the wind speed near the sea surface, as shown in Figure 11.


## 第 17 页

精品数模资料，T各ea类m比#赛7优78秀45论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店P铺ag：e闵15大o荒f3工0科男的杂货铺！
Table 3: A show of some cases of the comparison of the wave strength between calm
and turbulent surfaces, where P owerc means the power( in dBw) of the calm-surface
case, and P owert means the power( in dBw) of the turbulent-surface case, Diff. means
the difference between P owerc and P owert
(a)varyingwiththegrazingangle (b)varyingwiththewindspeed
Figure 11: The changes of the power ratio between the waves on turbulent and calm
ocean surfaces with grazing angle and the wind speed near the sea surface
4.2 The Multi-Hop Radio Propagation Process on Ocean Surface
According to the model, we simulate the multi-hop radio propagation process on
the sea surface, and draw the pictures of the propagation process with varying grazing
angle and varying frequency, as shown in Figure 12.
(a)varyingwiththegrazingangle (b)varyingwiththefrequency
Figure 12: A show of the propagation process with varying grazing angle and varying
frequency, in 12(a) the frequency is 20M Hz, and in 12(b) , the grazing angle is 15
We call the electromagnetic wave up and down as a hop. As shown in the Figure
12, we get the number of hops and the maximum propagation distance of each case,
as shown in Table 4.


## 第 18 页

精品数模资料，T各ea类m比#赛7优78秀45论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店P铺ag：e闵16大o荒f3工0科男的杂货铺！
20M Hz No. of hop D(km) 15 No. of hop D(km)
5 2 6300 15M Hz 2 5682
15 4 14650 17:65M Hz 3 9714
25 8 10970 20M Hz 4 14650
Table 4: A shown of the number of hops and the maximum propagation distance of
each case shown in Figure 12, D means the maximum propagation distance
4.3 The Comparison of Strength of Single-Hop Radio Wave
Between Rugged and Smooth Ground Terrains
Similar to the sea-surface-reflected case, we do the comparison of the strength of the
waves that are reflected from ground surface between rugged and smooth ground ter-rains.
Because the ground surface has a great effect on the dissipation of electromagnetic energy,
which can be seen from Figure 9, we only analyze the single-hop case. Table 5 shows
the radio-wave power ratio of rugged surface to smooth surface in several cases.
And Figure 13 indicates the change of the power ratio of rugged surface to smooth
sur-face with the standard deviation of the elevation, Sh.
Cases P owers (dBw) P owerr(dBw) Diff.(dBw) Power ratio
20M Hz; 15 ; Sh = 5 47.186 42.081 5.105 0.309
20M Hz; 15 ; Sh = 10 47.186 26.768 20.418 0.009
20M Hz; 15 ; Sh = 15 47.186 1.245 45.941 2.547E-5
20M Hz; 15 ; Sh = 20 47.186 -34.486 81.672 6.804E-9
Table 5: A show of some cases of the comparison of the wave strength between
rugged and smooth ground terrains, where P owers means the power( in dBw) of the
smooth-surface case, and P owerr means the power( in dBw) of the rugged-surface
case, Diff. means the difference between P owers and P owerr, Power ratio is ratio of
rugged-surface power to smooth-surface power
Figure 13: A show of the change of the ratio of rugged-surface power to smooth-
surface power with Sh


## 第 19 页

精品数模资料，T各ea类m比#赛7优78秀45论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店Pa铺g：e1闵7大of荒3工0科男的杂货铺！
5 Moving-Ship-Receiving-Signal Model
In order to ensure that the ship can continue to receive signals at sea, we assume
that radio waves are not a single frequency at launch, but have a certain bandwidth.
For example, the frequency of the emitted waves consists of all frequencies between
21M Hz and 21.45M Hz.
Because the frequency of electromagnetic waves in a given frequency range is con-
tinuous, and electromagnetic waves with different frequencies will have different prop-
agation path, the intersection of electromagnetic waves and the sea is no longer a point,
but becomes a range. We take the length of this range as L, and take the speed of the ship
as vship, then, the ship can remain in communication using the samemulti-hop path for
time= L .
v
ship
6 Result of Part III
Based on the Moving-Ship-Receiving-Signal Model (MSRSM), we analyze the length
of time the ship can remain receiving signal with the same path, and for the speed of ship,
the wind speed near the sea surface, the frequency range, we take 41:67km=h, 20m=s,
21M Hz 21:45M Hz, respectively. The grazing angle is 15 . A show of the multi-hop
propagation process of the continue-frequency radio waves is given in Figure 14.
Figure 14: A show of the multi-hop propagation of the continue-frequency radio waves,
with speed of wind near the sea is 20m=s, and the ship speed is 41:67km=h, and the
frequency range is 21M Hz 21:45MHz
Then we analyze the length of each intersection zone ( km ), and get the length of
time ( hour ) the ship can remain receiving signal in each intersection area, as shown in
Table 6.
Intersection zone Left(km) Right(km) Length(km) Time(hour)
1 2828 3031 203 4.87
2 5656 6049 393 9.43
3 8484 9055 571 13.70
4 11312 12070 758 18.19
total 1925 46.20
Table 6: A show of the length of time a ship can remain getting signal in each
intersection area


## 第 20 页

精品数模资料，T各ea类m比#赛7优78秀45论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店Pa铺g：e1闵8大of荒3工0科男的杂货铺！
7 Sensitivity Analysis
Solar activity, seasonal change, day and night will affect the nature of the
ionosphere around the earth, such as the altitude of the ionosphere, the density of
electrons, and so on [6]. We analyze the effects of these factors on the propagation of
the multi-hop HP radio waves.
7.1 Electron Density of The E Layer and F Layer
According to Equation 3, we change the electron density distribution of E and F lay-
ers by changing the maximum electron density of E and F layers. Figure 15 indicates the
effect of the change of the maximum electron density of E Layer and that of F layer. As
can be seen from it, the increase in E-layer electron density makes the radio waves
spread farther, because the increase in E-layer electron density makes the refractive
index of the E layer decrease, which means that the bending trend of electromagnetic
waves in the E layer will become larger, and the radio waves will spread farther in the
horizontal direc-tion. In addition, the loss of energy in the process of transmission has
hardly changed. However, the change of the maximum electron density of the F layer
hardly affects the propagation process of radio waves, because the change of the
maximum electron den-sity of the F layer has no effect on the electron concentration in
the lower layer of F layer, only affects the electron concentration in the upper part of F
layer, that can be got by ana-lyzing the Equation 3. And in the examples analyzed in this
section,no electromagneticwaves reachtheupper part of Flayer.
(a)changetheelectrondensityoftheElayer (b)changetheelectrondensityoftheFlayer
Figure 15: A show of the radio-wave propagation process with the change of electron
density distribution of the E and F layers
7.2 The Height of The F Layer
We analyze the propagation of the multi-hop HP radio waves with the height of the
F layer is 289.8m, or 339.3m, or 418.6m. As shown in Figure 16, as the altitude of the
F-layer ionosphere increases, radio waves can travel higher and the maximum
propagation distance is increased. However, the maximum number of hops does
not change, and the propagation paths looks similar in geometry.


## 第 21 页

精品数模资料，T各ea类m比#赛7优78秀45论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店Pa铺g：e1闵9大of荒3工0科男的杂货铺！
Figure 16: A show of the radio-wave propagation process with the change of the
altitude of F layer
7.3 The Wind Speed Near The Sea
Figure 17: A show of the changes of radio wave energy during propagation with
different wind speed
The change of wind speed only affects the sea surface reflectance and does not
af-fect the propagation path of radio waves. Figure 17 shows the changes in radio
wave energy during propagation with different wind speed near the ocean
surface. As can be seen from this figure, the increase in wind speed will cause
the electromagnetic wave to lose more energy in reflection, and will affect the
maximum number of the hops of electromagnetic waves.
8 Strengths and weaknesses
8.1 Strengths
Our model achieves a good simulation of the process of single-hop and multi-hop
propagation for high-frequency radio waves.


## 第 22 页

精品数模资料，T各ea类m比#赛7优78秀45论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店Pa铺g：e2闵0大of荒3工0科男的杂货铺！
Our model takes into account the effects of calm seas and turbulent seas as well
as different terrains.
The model gives a scheme for the ship to be able to receive the signal continuously,
and analyzes the length of the time the ship can remain receiving the signal.
The model can be widely applied to the design of radio wave propagation path
and the decision of frequency.
8.2 Weaknesses
The parameters that determine the ionospheric properties are taken from Wuhan
City and Sanya City and are not representative enough of the rest regions of the
Earth.
The relative permittivity and conductivity of the land surface are approximate with
these of the wet concrete, and it may be less accurate to calculate the reflection
coefficient of the ground using these data.


## 第 23 页

精品数模资料，T各ea类m比 #赛 7优78秀45论 文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店Pa铺g：e 2闵1大 of荒 3工0科男的杂货铺！
References
[1] Marc C. Tarplee. Hf radio wave propagation. http://arrlsc.org/wordpress/
Tech%20Presentations/HF%20Radio%20Wave%20Propagation.ppt. [On-line;
accessed 10-February-2018].
[2] Wikipedia. Skywave. https://en.wikipedia.org/wiki/Skywave. [Online; accessed 11-
February-2018].
[3] RF Cafe. Typical daytime ionosphere layer diagram. http://
www.rfcafe.com/references/electronics-world/images2/
ionospheric-propagation-prediction-electronics-world-april-1969-3. jpg. [Online; accessed
11-February-2018].
[4] Wikipedia. Free-space path loss. https://en.wikipedia.org/wiki/ Free-
space_path_loss. [Online; accessed 11-February-2018].
[5] A. H Monahan. The probability distribution of sea surface wind speeds. part i:
Theory and seawinds observations. Journal of Climate, 19(4):502, Feb. 2006.
[6] Wikipedia. Ionosphere. https://en.wikipedia.org/wiki/Ionosphere. [Online; accessed
11-February-2018].
[7] George Simpson. What is a grazing angle? https://www.quora.com/ What-is-a-
grazing-angle. [Quora; Online; accessed 12-February-2018].
[8] Wikipedia. Boltzmann constant. https://en.wikipedia.org/wiki/ Boltzmann_constant.
[Online; accessed 12-February-2018].
[9] Wikipedia. Kelvin. https://en.wikipedia.org/wiki/Kelvin. [Online; ac-cessed 12-
February-2018].
[10] WANG Ying and GU Jian. Research and simulation analysis of radio reflection char-
acteristic over the ocean. Electronic Design Engineering, 24(5):113–119, Mar. 2016.
[11] Reflection from the surface of the earth. https://www.itu.int/pub/R-REP-P. 1008.
[12] Yu Chao, Guozhu Shen, Gu Bin, and Guosheng Cheng. Characteristics of electro-
magnetic wave propagating through ionosphere. Journal of nanjing information
engi-neering university (natural science edition), 5(04):379–384, Aug. 2013.
[13] B. Zolesi and L. R. Cander. Chapter 2: The general structure of the iono-sphere,
ionospheric prediction and forecasting, springer geophysics. http:
//www.springer.com/cda/content/document/cda_downloaddocument/
9783642384295-c2.pdf?SGWID=0-0-45-1432953-p175163711, Chapter
2:38,2014. [Online; accessed 11-February-2018].
[14] Wikipedia. Snell’s law. https://en.wikipedia.org/wiki/Snell%27s_law. [Online;
accessed 11-February-2018].
[15] Bertrand Daout, Marc Sallin, and Heinz Wipf. Measurement of complex permittivity
of large concrete samples with an open-ended coaxial line. Measurement Notes,
10, 2014.


## 第 24 页

精品数模资料，T各ea类m比#赛7优78秀45论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店Pa铺g：e2闵2大of荒3工0科男的杂货铺！
[16] Hamed Layssi, Pouria Ghods, Aali R Alizadeh, and Mustafa Salehi. Electrical
resis-tivity of concrete. Concrete International, 37(5):41–46, 2015.
[17] Wikipedia. Electrical resistivity and conductivity. https://en.wikipedia.org/
wiki/Electrical_resistivity_and_conductivity. [Online; accessed 12-February-2018].
[18] SUI Gang, HAO Bingyuan, and PENG Lin. Data analysis of topographic relief
using standard deviation of elevation (in chinese). Journal of taiyuan university of
technology, 41(4):383, Jul. 2010.
[19] International Telecommunication Union. Radio noise. https://www.itu.int/
dms_pubrec/itu-r/rec/p/R-REC-P.372-13-201609-I!!PDF-C.pdf, 9 2016. P.372-13.
[20] Wikipedia. Decibel watt. https://en.wikipedia.org/wiki/Decibel_watt. [Online;
accessed 12-February-2018].


## 第 25 页

精品数模资料，T各ea类m比#赛7优78秀45论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店Pa铺g：e2闵3大of荒3工0科男的杂货铺！
Appendices
Appendix A A Short Synopsis
As an important means of communication, skywave communication is an applica-
tion of high-frequency radio waves. It uses the reflection of electromagnetic waves be-
tween the ionosphere and the surface of Earth to achieve long-distance communication.
Multi-hop propagation of high-frequency radio waves is a manifestation of the skywave
communication, and can spread farther than single-hop propagation.
In order to simulate the multi-hop propagation process of high-frequency radio
waves, a complete mathematical model is established. This model can simulate the
reflection be-tween the ionosphere and the surface of Earth, as well as the multi-hop
process very well. The ionosphere contains D layer, E layer, F1 layer and F2 layer. In the
model, we make a reasonable assumption of the daytime ionosphere, combining the
actual nature of the ionosphere. We consider the D layer to be a "energy attenuation
layer", the E layer as a "single-refraction layer", and the F1 layer and the F2 layer are
merged into one layer, F layer, which is considered as a "refraction and reflection layer" .
In order to simulate the attenuation of radio-wave energy during the propagation, we
considered three parts, which are the attenuation of energy in the D layer ionosphere, the
"free-space path loss" and "energy loss while reflecting off the ground or sea surface"
. We also simulate the distribution of electron density and refractive index in the iono-
sphere along altitude.
Using the Multi-Hop Propagation Model (MHPM), we compare the strength of radio
waves after the first reflection off the calm and the turbulent ocean surfaces. And we find
that the turbulent sea surface can enhance the attenuation of electromagnetic waves in
reflection. We also analyze the maximum number of hops and the maximum propagation
distance of several cases with different natural and frequency conditions. In addition, we
analyze the change of the ratio of the power in calm-sea case to the power in turbulent-sea
case with the grazing angle and the wind speed near ocean surface. Then we find that the
power ratio decreases with the increase of the grazing angle and the wind speed
.
The MHPM can also be applied to ground-reflection situations very well. We refer to
the relevant literature and divide the ground into four categories according to the elevation
standard deviation. By studying the change of the ratio of the power in rugged-surface case
to smooth-surface case with the standard deviation of elevation, we find that the power
decreases rapidly as the elevation standard deviation increasing. What’s more, rough
ground has a much greater impact on the energy loss of electromagnetic waves than the
sea surface. And when the elevation standard deviation is 15, the ground almost loses the
ability to reflect electromagnetic waves effectively.
Inorder tomaketheship beable toreceive signalscontinuouslywhile sailing on thesea,
we proposeasolution andestablishtheMoving-Ship-Receiving-SignalModel (MSRSM). The
solutionis toemitelectromagneticwaves witha certainbandwidth. Wesimulatethecasewith
thespeed of windnear theseais 20m=s, theshipspeedis 41:67km=h,and thefrequency range
is21M Hz 21:45M Hz, thatmeansthat thebandwidthis


## 第 26 页

精品数模资料，T各ea类m比#赛7优78秀45论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店Pa铺g：e2闵4大of荒3工0科男的杂货铺！
0:45M Hz. The simulation is shown in the following figure. And the length of time the
ship can remain receiving signals for each intersection of electromagnetic waves and
the sea is shown in the following table.
Intersection zone Left(km) Right(km) Length(km) Time(hour)
1 2828 3031 203 4.87
2 5656 6049 393 9.43
3 8484 9055 571 13.70
4 11312 12070 758 18.19
total 1925 46.20
The MHPM and MSRSM have good application prospects. They can be used to
de-termine the path, frequency, and grazing angle for the propagation of multi-hop
radio waves. Our model can determine the propagation path of radio waves and the
change of energy in the course of transmission, for a particular ionosphere with given
param-eters, the ground or the sea with special physical parameters. Thus, our models
are practical. We believe that our model can well simulate the propagation of multi-hop
high-frequency radio waves and play a certain role in the field of radio communication.


## 第 27 页

精品数模资料，T各ea类m比#赛7优78秀45论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店P铺ag：e闵25大o荒f3工0科男的杂货铺！
Appendix B The Code
main.m:
clc
clear
%Themainprogramof"multi-hop";i=1;
D_min=61.2;
D_max=88.6;
E_mid=95.65;
E_max=101;
F_max=271.5;
n1=1;
v=8; %oceanwindspeed,m/s
totalf=[1517.6520];%Defineoutputfrequency, MHzf=totalf(3);
totalAngled=[51525];%grazingangle,degreefor
l=1:length(totalf)
f=totalf(l);
%angled=totalAngled(l);angled=15;
angle=angled/180*pi;
x=zeros(1,1);y=zeros(1,1);
Srn=zeros(1,1);
parameterOcean=seareflection(f,angled,v);
lossOcean=parameterOcean(1);
Ploss=lossOcean^2;
NeN_E=calnAndNe(E_mid,f);
n_E=NeN_E(2);
angle_E=acos(cos(angle)*n1/n_E);
p0=100;%transmittingpower
%watttodBW
dp0=10*log10(p0);%dBW
K_boltzmann=1.38064852e-23;%Boltzmannconstant
T0=290;%Kelvintemperature
b=200;%Bandwidth
KT0b=10*log10(K_boltzmann*T0*b);
%Differentfrequenciescorrespondtonoiselevels.iff==15
p0=27;
end
iff==17.65
p0=22;
end
iff==20
p0=19;
end
pw=10^((p0+KT0b)/10);
dpnoise=10*log10(pw);
Srn(1)=dp0-dpnoise;
SrnLoop(1)=Srn(1);
%Belowtheionosphere.
NumLoop=1;
x(1)=0;
y(1)=0;


## 第 28 页

精品数模资料，T各ea类m比#赛7优78秀45论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店Pa铺g：e2闵6大of荒3工0科男的杂货铺！
dist(1)=0;
k=1;alpha_D=1.16*10^(-15)*10^10*10^6/f/f;
XofLoop(1)=0;
DISTofLoop(1)=1;while(SrnLoop(NumLoop)>=10&&
NumLoop<=10)
stepy_D=1;
while(y(k)<D_min)
y(k+1)=y(k)+stepy_D;x(k+1)=y(k+1)/tan(angle)+XofLoop(NumLoop);
dist(k+1)=y(k+1)/sin(angle)+DISTofLoop(NumLoop);Srn(k+1)=Srn(1)-
20*log10(dist(k+1))-20*log10(f)-32.45...
-alpha_D*(D_max-D_min)/sin(angle)*2*(NumLoop-1)+10*log10(Ploss)...
*(NumLoop-1);
k=k+1;
end
dist_beforD(NumLoop)=dist(k);
while(y(k)>D_min&&y(k)<=D_max)
y(k+1)=y(k)+stepy_D;
x(k+1)=y(k+1)/tan(angle)+XofLoop(NumLoop);
dist(k+1)=y(k+1)/sin(angle)+DISTofLoop(NumLoop);
Srn(k+1)=Srn(1)-20*log10(dist(k+1))-20*log10(f)-32.45-alpha_D*(y(k+1)-D_min)...
/sin(angle)-alpha_D*2*(D_max-D_min)/sin(angle)*(NumLoop-1)+10*log10(Ploss)...
*(NumLoop-1);
k=k+1;
end
while(y(k)>D_max&&y(k)<=E_mid)y(k+1)=y(k)+stepy_D;
x(k+1)=y(k+1)/tan(angle)+XofLoop(NumLoop);
dist(k+1)=y(k+1)/sin(angle)+DISTofLoop(NumLoop);
Srn(k+1)=Srn(1)-20*log10(dist(k+1))-20*log10(f)-32.45-alpha_D*(D_max-D_min)...
/sin(angle)-alpha_D*(D_max-D_min)/sin(angle)*2*(NumLoop-1)+10*log10(Ploss)...
*(NumLoop-1);
k=k+1;
end
x_beforeE_mid(NumLoop)=x(k);
y_beforeE_mid(NumLoop)=y(k);
dist_beforeE(NumLoop)=dist(k);
while(y(k)>=E_mid&&y(k)<=E_max)
y(k+1)=y(k)+stepy_D;x(k+1)=x_beforeE_mid(NumLoop)+(y(k+1)-y_beforeE_mid(NumLoop))/tan(angle_E);
dist(k+1)=dist_beforeE(NumLoop)+(y(k+1)-y_beforeE_mid(NumLoop))/sin(angle_E);Srn(k+1)=Srn(1)-
20*log10(dist(k+1))-20*log10(f)-32.45-alpha_D*(D_max-D_min)...
/sin(angle)-alpha_D*(D_max-D_min)/sin(angle)*2*(NumLoop-1)+10*log10(Ploss)...
*(NumLoop-1);
k=k+1;
end
stepy_F=0.01;
t=1;
NeN_F=calnAndNe(y(k),f);
n_F(1)=NeN_F(2);
cosAngleF=cos(angle_E);
COSF(1)=cosAngleF;
while(y(k)>=E_max&&y(k)<=F_max&&cosAngleF<1&&(1-cosAngleF)>0.0001)
y(k+1)=y(k)+stepy_F;
NeN_F=calnAndNe(y(k+1),f);
n_F(t+1)=NeN_F(2);
cosAngleF=COSF(t)*n_F(t)/n_F(t+1);


## 第 29 页

精品数模资料，T各ea类m比#赛7优78秀45论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店Pa铺g：e2闵7大of荒3工0科男的杂货铺！
COSF(t+1)=cosAngleF;angle_F=acos(cosAngleF);
AF(t)=angle_F;x(k+1)=x(k)+stepy_F/tan(angle_F);
dist(k+1)=dist(k)+stepy_F/sin(angle_F);
Srn(k+1)=Srn(1)-20*log10(dist(k+1))-20*log10(f)-32.45-alpha_D*(D_max-D_min)...
/sin(angle)-alpha_D*(D_max-D_min)/sin(angle)*2*(NumLoop-1)+10*log10(Ploss)...
*(NumLoop-1);
k=k+1;
t=t+1;
end
[dimx,rdimy]=size(x);
dimy=(rdimy)/(2*NumLoop-1);for
j=1:dimy
x(rdimy+j)=-x(rdimy-j+1)+2*x(rdimy);
y(rdimy+j)=y(rdimy-j+1);
end
forj=rdimy+1:rdimy+dimy
dist(k+1)=dist(k)+sqrt((x(j)-x(j-1))^2+(y(j)-y(j-1))^2);Srn(k+1)=Srn(1)-20*log10(dist(k+1))-20*log10(f)-32.45-alpha_D*(D_max-
D_min)...
/sin(angle)-alpha_D*(D_max-D_min)/sin(angle)*2*(NumLoop-1)+10*log10(Ploss)...
*(NumLoop-1);
if(y(k)>D_max&&y(k+1)<=D_max)
distD=dist(k+1);
end
if(y(k+1)<=D_max&&y(k+1)>=D_min)Srn(k+1)=Srn(k+1)-
alpha_D*(dist(k+1)-distD);
end
if(y(k+1)<=D_min)Srn(k+1)=Srn(k+1)-alpha_D*(D_max-D_min)/sin(angle);
end
k=k+1;
end
DISTofLoop(NumLoop+1)=dist(k);
XofLoop(NumLoop+1)=x(k);
SrnLoop(NumLoop+1)=Srn(k);
x(k+1)=x(k);
y(k+1)=y(k);
y(k+1)=0;
dist(k+1)=dist(k);
Srn(k)=Srn(k)+10*log10(Ploss);
Srn(k+1)=Srn(k);
k=k+1;
NumLoop=NumLoop+1;
endsubplot(2,1,1)
colormap(’Hot’)
patch([xNaN],[yNaN],[SrnSrn(end)],’edgecolor’,’flat’,’facecolor’,’none’)
plot(x,y,’linewidth’,1.5);xlabel(’Propagation
distance(km)’)ylabel(’Altitude(km)’)
holdon
colorbar
subplot(2,1,2)
patch([xNaN],[SrnNaN],[SrnSrn(end)],’edgecolor’,’flat’,’facecolor’,’none’)
plot(x,Srn,’linewidth’,1.5);
xlabel(’Propagationdistance(km)’)


## 第 30 页

精品数模资料，T各ea类m比#赛7优78秀45论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店Pa铺g：e2闵8大of荒3工0科男的杂货铺！
ylabel(’signal-to-noiseratio(dB)’)
holdon
end
colormap(’hsv’)
subplot(2,1,1)
legend(’15MHz’,’17.65MHz’,’20MHz’);
legend(’5^o’,’15^o’,’25^o’);
subplot(2,1,2)
legend(’15MHz’,’17.65MHz’,’20MHz’);
legend(’5^o’,’15^o’,’25^o’);
calnAndNe.m:
functionNeN=calnAndNe(h,f)
˘ ´
%thisfunctionisasimulatationofthenandNeã A C%Andthe’h’
shouldabovetheionosphere’E’.f_0E=3.21;%MHz
h_mE=101;%km
y_mE=10.7;%km
f_0F2=14.20;%MHz
h_mF2=339.3;%km
y_mF2=78;%km
f_j=1.7*f_0E;
N_j=1.24/100*f_j^2;%10^12*m^(-3)h_j=h_mF2-
y_mF2*sqrt(1-(f_j/f_0F2)^2);N_mE=3.16/100;%10^12*
m^(-3)N_mF2=2.5;%10^12*m^(-3)
H=1.66*(30+0.075*(h_mF2-200));NeN=zeros(1,2);
ifh<(h_mE-y_mE)||h>1000
n=100;%meansthe"h"isnotintheeffectiverangeNe=0;%means
the"h"isnotintheeffectiverange
end
ifh>=(h_mE-y_mE)&&h<=h_mE
Ne=N_mE*(1-((h-h_mE)/y_mE)^2);
n=sqrt(1-80.8*Ne/f/f);
end
ifh>h_mE&&h<=h_jNe=(N_j-N_mE)/(h_j-h_mE)*h+(N_mE*h_j-
N_j*h_mE)/(h_j-h_mE);n=sqrt(1-80.8*Ne/f/f);
end
ifh>h_j&&h<=h_mF2Ne=N_mF2*(1-((h-
h_mF2)/y_mF2).^2);
n=sqrt(1-80.8*Ne/f/f);
end
ifh>h_mF2&&h<=1000Ne=N_mF2*exp(0.5*(1-(h-h_mF2)/H-exp(-1.0*(h-
h_mF2)/H)));n=sqrt(1-80.8*Ne/f/f);
end
NeN(1)=Ne;
NeN(2)=n;
fcandMUF.m:
functionfrequency=fcandMUF(Ne,h)
R=6371;%Theradiusoftheearth,km
fcr=(Ne/1.24/10^10).^(0.5);%Criticalfrequency; MUF=fcr/(1-
(R/(R+h)).^2).^0.5;


## 第 31 页

精品数模资料，T各ea类m比#赛7优78秀45论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店Pa铺g：e2闵9大of荒3工0科男的杂货铺！
frequency=[fcr,MUF];
end
groundreflection.m:
functionf=groundreflection(fre,angle,Sh)theta=15;
thgema=0.05;
lamda=3*10^2/fre;
retheta=theta+lamda*thgema*60i;Rh=(sind(angle)-(retheta-
(cosd(angle)).^2).^0.5)/(sind(angle)+...
(retheta-(cosd(angle)).^2).^0.5);Rv=(retheta*sind(angle)-(retheta-
(cosd(angle)).^2).^0.5)/...
(retheta*sind(angle)+(retheta-(cosd(angle)).^2).^0.5); Rh=abs(Rh);
Rv=abs(Rv);
g=4*pi*Sh/lamda*sind(angle);
thou=exp(-1/(2*g.^2));
Rhrough=Rh*thou;Rvrough=Rv*thou;
f=[Rh,Rv,Rhrough,Rvrough];
end
seareflection.m:
functionf=seareflection(fre,angle,v)
a=1.411*10^-2;
b=-5.212*10^-8;
c=5.854*10^-11;
d=-7.671*10^-16;
e=2.985*10^-21;
theta(i,1)=1/(a+b*fre+c*fre.^2+d*fre.^3+e*fre.^4);
r=3.858;
s=9.125*10^-4;
t=1.530*10^-8;
u=-2.117*10^-5;
v=6.572*10^-10;
w=-1.964*10^-15;
thgema(i,1)=(r+s*fre+t*fre.^2)/(1+u*fre+v*fre.^2+w*fre.^3);theta=70;
thgema=5;
lamda=3*10^2/fre;
retheta=theta+lamda*thgema*60i;Rh=(sind(angle)-(retheta-
(cosd(angle)).^2).^0.5)/(sind(angle)+...
(retheta-(cosd(angle)).^2).^0.5);Rv=(retheta*sind(angle)-(retheta-
(cosd(angle)).^2).^0.5)/...
(retheta*sind(angle)+(retheta-(cosd(angle)).^2).^0.5); Rh=abs(Rh);
Rv=abs(Rv);
h=0.0051*v.^2;
g=0.5*(4*pi*h*fre*10^6*sind(angle)/3/10^8)^2;thou=1/(3.2*g-
2+((3.2*g)^2-7*g+9).^0.5)^0.5;Rhrough=Rh*thou;
Rvrough=Rv*thou;
f=[Rh,Rv,Rhrough,Rvrough];end
tryfcandMUF.m:


## 第 32 页

精品数模资料，T各ea类m比#赛7优78秀45论文、学习教程、写作模板与经验技巧、matlab程序代码资料等，尽在淘宝店Pa铺g：e3闵0大of荒3工0科男的杂货铺！
clc
clear
try fcandMUF.m
h_f=339-30:339;
f=10;
[dimx,dimy]=size(h_f); for
i=1:dimy
NeN(i,:)=calnAndNe(h_f(i),f);
fre(i,:)=fcandMUF(NeN(i,1)*10^12,h_f(i));
end
plot(fre(:,1),h_f);
xlabel(’fc’)
ylabel(’h(km)’)
figure(2)
plot(fre(:,2),h_f);
xlabel(’MUF(MHz)’)
ylabel(’h(km)’)
tryforCalnAndNe.m:
clc
clear
%trycalnAndNe.m
f=15;
h=91:1:600;
[dimx,dimy]=size(h);
NeN=zeros(dimy,2);for
i=1:dimy
NeN(i,:)=calnAndNe(h(i),f);
end
figure(1)
plot(NeN(:,1),h);
xlabel(’10^1^2m^-^3’)
ylabel(’h(km)’)
figure(2)
plot(NeN(:,2),h);
[22]

# Bayesian Compressive Sensing via Belief Propagation


## 第 1 页

This article has been accepted for publication in a future issue of this journal, but has not been fully edited. Content may change prior to final publication.
1
Bayesian Compressive Sensing
via Belief Propagation
DrorBaron,1ShriramSarvotham,2andRichardG.Baraniuk3
Copyright(c) 2008IEEE.Personal useofthismaterialis permitted. However,
permissiontousethismaterialforanyotherpurposesmustbeobtainedfrom
theIEEE bysendingarequest topubs-permissions@ieee.org.
1DepartmentofElectricalEngineering,Technion–IsraelInstituteofTechnology;Haifa,Israel
2Halliburton;Houston,TX
3DepartmentofElectricalandComputerEngineering,RiceUniversity;Houston,TX
June23,2009 DRAFT
Copyright (c) 2009 IEEE. Personal use is permitted. For any other purposes, Permission must be obtained from the IEEE by emailing pubs-permissions@ieee.org.
Authorized licensed use limited to: BEIJING UNIVERSITY OF POST AND TELECOM. Downloaded on December 9, 2009 at 20:44 from IEEE Xplore. Restrictions apply.


## 第 2 页

This article has been accepted for publication in a future issue of this journal, but has not been fully edited. Content may change prior to final publication.
Abstract
Compressivesensing (CS) is an emergingfield based on the revelationthat a smallcollection of lin-
ear projectionsof a sparse signalcontainsenoughinformationfor stable, sub-Nyquistsignalacquisition.
Whenastatisticalcharacterizationofthesignalisavailable,Bayesianinferencecancomplementconven-
tionalCSmethodsbasedonlinearprogrammingorgreedyalgorithms. WeperformapproximateBayesian
inferenceusingbeliefpropagation(BP)decoding,whichrepresentstheCSencodingmatrixasagraphical
model. Fast computation is obtained by reducing the size of the graphical model with sparse encoding
matrices.Todecodealength-N signalcontainingKlargecoefficients,ourCS-BPdecodingalgorithmuses
2
O(Klog(N)) measurementsandO(Nlog (N)) computation. Finally, althoughwe focuson a two-state
mixtureGaussianmodel,CS-BPiseasilyadaptedtoothersignalmodels.
I. INTRODUCTION
Manysignalprocessingapplicationsrequiretheidentificationandestimationofafewsignificantcoeffi-
cientsfromahigh-dimensional vector. Thewisdombehindthisistheubiquitous compressibility ofsignals:
in an appropriate basis, most of the information contained in a signal often resides in just a few large co-
efficients. Traditional sensing and processing first acquires the entire data, only to later throw away most
coefficients andretain thefewsignificant ones[2]. Interestingly, theinformation contained inthefewlarge
coefficients can be captured (encoded) by a small number of random linear projections [3]. The ground-
breakingworkincompressivesensing(CS)[4–6]hasprovedforavarietyofsettingsthatthesignalcanthen
bedecodedinacomputationally feasible mannerfromtheserandom projections.
A. Compressivesensing
Sparsityandrandomencoding:Inatypicalcompressive sensing (CS)setup, asignalvector x RN
∈
has theform x = Ψθ,where Ψ RN N is anorthonormal basis, and θ RN satisfies θ = K N.1
× 0
∈ ∈ k k (cid:28)
Owingtothesparsity ofxrelativetothebasisΨ,thereisnoneedtosampleallN values ofx. Instead, the
CS theory establishes that x can be decoded from a small number of projections onto an incoherent set of
measurement vectors [4,5]. To measure (encode) x, we compute M N linear projections of x via the
(cid:28)
matrix-vector multiplication y = ΦxwhereΦ RM N istheencoding matrix.
×
∈
Inadditiontostrictlysparsesignalswhere θ K,othersignalmodelsarepossible. Approximately
0
k k ≤
sparsesignalshaveK N largecoefficients,whiletheremainingcoefficientsaresmallbutnotnecessarily
(cid:28)
zero. Compressible signals have coefficients that, when sorted, decay quickly according to a power law.
1Weusek·k0todenotethe` 0“norm”thatcountsthenumberofnon-zeroelements.
Copyright (c) 2009 IEEE. Personal use is permitted. For any other purposes, Permission must be obtained from the IEEE by emailing pubs-permissions@ieee.org.
Authorized licensed use limited to: BEIJING UNIVERSITY OF POST AND TELECOM. Downloaded on December 9, 2009 at 20:44 from IEEE Xplore. Restrictions apply.


## 第 3 页

This article has been accepted for publication in a future issue of this journal, but has not been fully edited. Content may change prior to final publication.
Similarly, both noiseless and noisy signals and measurements may be considered. Weemphasize noiseless
measurementofapproximately sparsesignalsinthepaper.
Decoding via sparsity: Our goal is to decode x given y and Φ. Although decoding x from y =
Φx appears to be an ill-posed inverse problem, the prior knowledge of sparsity in x enables to decode x
from M N measurements. Decoding often relies on an optimization, which searches for the sparsest
(cid:28)
coefficients θ that agree with the measurements y. IfM is sufficiently large and θ is strictly sparse, then θ
isthesolution tothe` minimization:
0
θ =argmin θ s.t. y = ΦΨθ.
0
k k
b
Unfortunately, solvingthis` optimization isNP-complete[7].
0
The revelation that supports the CS theory is that a computationally tractable optimization problem
yields an equivalent solution. We need only solve for the ` -sparsest coefficients that agree with the mea-
1
surementsy [4,5]:
θ =argmin θ s.t. y = ΦΨθ, (1)
1
k k
aslongasΦΨsatisfiessometechnicabl conditions, whicharesatisfiedwithoverwhelming probability when
theentriesofΦareindependent andidenticallydistributed (iid)sub-Gaussianrandomvariables[4]. This`
1
optimizationproblem(1),alsoknownasBasisPursuit[8],canbesolvedwithlinearprogrammingmethods.
The ` decoder requires only M = O(Klog(N/K)) projections [9,10]. However, encoding by a dense
1
GaussianΦisslow,and` decoding requirescubiccomputation ingeneral[11].
1
B. FastCSdecoding
While ` decoders figure prominently in the CS literature, their cubic complexity still renders them
1
impractical for many applications. For example, current digital cameras acquire images with N = 106
pixelsormore,andfastdecoding iscritical. Theslownessof` decoding hasmotivatedaflurryofresearch
1
intofasteralgorithms.
One line of research involves iterative greedy algorithms. TheMatching Pursuit (MP)[12] algorithm,
for example, iteratively selects the vectors from thematrix ΦΨthat contain mostof theenergy of themea-
surement vector y. MP has been proven to successfully decode the acquired signal with high probabil-
ity[12,13]. AlgorithmsinspiredbyMPincludeOMP[12],treematchingpursuit[14],stagewiseOMP[15],
CoSaMP[16],IHT[17],andSubspacePursuit[18]havebeenshowntoattainsimilarguaranteestothoseof
theiroptimization-based counterparts [19–21].
3
Copyright (c) 2009 IEEE. Personal use is permitted. For any other purposes, Permission must be obtained from the IEEE by emailing pubs-permissions@ieee.org.
Authorized licensed use limited to: BEIJING UNIVERSITY OF POST AND TELECOM. Downloaded on December 9, 2009 at 20:44 from IEEE Xplore. Restrictions apply.


## 第 4 页

This article has been accepted for publication in a future issue of this journal, but has not been fully edited. Content may change prior to final publication.
While the CS algorithms discussed above typically use a dense Φ matrix, a class of methods has
emerged that employ structured Φ. For example, subsampling an orthogonal basis that admits a fast im-
plicit algorithm also leads to fast decoding [4]. Encoding matrices that are themselves sparse can also be
used. Cormode and Muthukrishnan proposed fast streaming algorithms based on group testing [22,23],
which considers subsets of signal coefficients in which we expect at most one “heavy hitter” coefficient
to lie. Gilbert et al. [24] propose the Chaining Pursuit algorithm, which works best for extremely sparse
signals.
C. BayesianCS
CSdecodingalgorithmsrelyonthesparsityofthesignalx. Insomeapplications, astatisticalcharacter-
ization ofthe signal isavailable, and Bayesian inference offers the potential formore precise estimation of
xorareduction inthenumberofCSmeasurements. Jietal.[25]haveproposed aBayesian CSframework
where relevance vector machines are used for signal estimation. For certain types of hierarchical priors,
their method can approximate the posterior density of x and is somewhat faster than ` decoding. Seeger
1
andNickisch[26]extendtheseideastoexperimentaldesign,wheretheencodingmatrixisdesignedsequen-
tially based on previous measurements. Another Bayesian approach by Schniter et al. [27] approximates
conditional expectation by extending the maximal likelihood approach to a weighted mixture of the most
likely models. There are also many related results on application of Bayesian methods to sparse inverse
problems(c.f.[28]andreferences therein).
Bayesianapproacheshavealsobeenusedformultiuserdecoding(MUD)incommunications. InMUD,
usersmodulatetheirsymbolswithdifferentspreadingsequences,andthereceivedsignalsaresuperpositions
of sequences. Because most users are inactive, MUD algorithms extract information from a sparse super-
position inamanneranalogous toCSdecoding. GuoandWang[29]perform MUDusing sparse spreading
sequences and decode via belief propagation (BP) [30–35]; our paper also uses sparse encoding matrices
andBPdecoding. Arelatedalgorithmfordecodinglowdensitylatticecodes(LDLC)bySommeretal.[36]
uses BP on a factor graph whose self and edge potentials are Gaussian mixtures. Convergence results for
theLDLCdecoding algorithm havebeenderivedforGaussiannoise[36].
D. Contributions
Inthispaper,wedevelopasparseencodermatrixΦandabeliefpropagation(BP)decodertoaccelerate
CS encoding and decoding under the Bayesian framework. We call our algorithm CS-BP. Although we
emphasize atwo-state mixture Gaussian model asaprior forsparse signals, CS-BPisflexible tovariations
4
Copyright (c) 2009 IEEE. Personal use is permitted. For any other purposes, Permission must be obtained from the IEEE by emailing pubs-permissions@ieee.org.
Authorized licensed use limited to: BEIJING UNIVERSITY OF POST AND TELECOM. Downloaded on December 9, 2009 at 20:44 from IEEE Xplore. Restrictions apply.


## 第 5 页

This article has been accepted for publication in a future issue of this journal, but has not been fully edited. Content may change prior to final publication.
inthesignalandmeasurement models.
EncodingbysparseCSmatrix:Thedensesub-Gaussian CSencoding matrices[4,5]arereminiscent
ofShannon’srandomcodeconstructions. However,althoughdensematricescapturetheinformationcontent
ofsparsesignals,theymaynotbeamenabletofastencodinganddecoding. Lowdensityparitycheck(LDPC)
codes[37,38]offeranimportantinsight: encodinganddecodingarefast,becausemultiplicationbyasparse
matrix is fast; nonetheless, LDPC codes achieve rates close to the Shannon limit. Indeed, in a previous
paper [39], weusedanLDPC-likesparseΦforthespecial caseofnoiseless measurement ofstrictly sparse
signals; similar matrices werealso proposed forCSby Berinde and Indyk [40]. Although LDPCdecoding
algorithms may not have provable convergence, the recent extension of LDPC to LDLC codes [36] offers
provableconvergence, whichmayleadtosimilarfutureresultsforCSdecoding.
Weencode(measure)thesignalusingsparseRademacher( 0,1, 1 )LDPC-likeΦmatrices. Because
{ − }
entries of Φ are restricted to 0,1, 1 , encoding only requires sums and differences of small subsets of
{ − }
coefficientvaluesofx. ThedesignofΦ,includingcharacteristics suchascolumnandrowweights,isbased
ontherelevantsignalandmeasurement models,aswellastheaccompanying decoding algorithm.
DecodingbyBP:Werepresent thesparseΦasasparsebipartite graph. Inaddition toaccelerating the
algorithm, the sparse structure reduces the number of loops in the graph and thus assists the convergence
of a message passing method that solves a Bayesian inference problem. Our estimate for x explains the
measurements while offering the best match to the prior. We employ BP in a manner similar to LDPC
channel decoding [34,37,38]. To decode a length-N signal containing K large coefficients, our CS-BP
decoding algorithm uses M = O(Klog(N)) measurements and O(Nlog2(N)) computation. Although
CS-BPisnotguaranteed toconverge, numericalresultsarequitefavorable.
Theremainderofthepaperisorganizedasfollows. SectionIIdefinesoursignalmodel,andSectionIII
describesoursparseCS-LDPCencodingmatrix. TheCS-BPdecodingalgorithmisdescribedinSectionIV,
anditsperformance isdemonstrated numerically inSectionV. Variations andapplications arediscussed in
SectionVI,andSectionVIIconcludes.
II. MIXTURE GAUSSIAN SIGNAL MODEL
We focus on a two-state mixture Gaussian model [41–43] as a prior that succinctly captures our prior
knowledgeaboutapproximatesparsityofthesignal. Bayesianinferenceusingatwo-statemixturemodelhas
been studied well before the advent of CS, for example by George and McCulloch [44] and Geweke [45];
the model was proposed for CS in [1] and also used by He and Carin [46]. More formally, let X =
[X(1),...,X(N)]bearandomvectorinRN,andconsiderthesignalx = [x(1),...,x(N)]asanoutcome
5
Copyright (c) 2009 IEEE. Personal use is permitted. For any other purposes, Permission must be obtained from the IEEE by emailing pubs-permissions@ieee.org.
Authorized licensed use limited to: BEIJING UNIVERSITY OF POST AND TELECOM. Downloaded on December 9, 2009 at 20:44 from IEEE Xplore. Restrictions apply.


## 第 6 页

This article has been accepted for publication in a future issue of this journal, but has not been fully edited. Content may change prior to final publication.
Pr(Q = 0) Pr(Q = 1)
f(X Q = 0) f(X Q = 1) f(X)
| |
⇒
Fig.1. MixtureGaussianmodelforsignalcoefficients.ThedistributionofX conditionedonthetwostatevariables,
Q=0andQ=1,isdepicted.AlsoshownistheoveralldistributionforX.
ofX. Because our approximately sparse signal consists ofasmallnumber oflarge coefficients andalarge
number of small coefficients, we associate each probability density function (pdf) f(X(i)) with a state
variable Q(i) that can take on two values. Large and small magnitudes correspond to zero mean Gaussian
distributions withhighandlowvariances, whichareimpliedbyQ(i) = 1andQ(i) = 0,respectively,
f(X(i)Q(i) = 1) (0,σ2) and f(X(i)Q(i) = 0) (0,σ2),
| ∼ N 1 | ∼ N 0
withσ2 > σ2. LetQ = [Q(1),...,Q(N)]bethestaterandom vectorassociated withthesignal; theactual
1 0
configuration q = [q(1),...,q(N)] 0,1 N isone of 2N possible outcomes. Weassume that theQ(i)’s
∈ { }
areiid.2 ToensurethatwehaveapproximatelyK largecoefficients,wechoosetheprobabilitymassfunction
(pmf)ofthestatevariableQ(i)tobeBernoulliwithPr(Q(i) = 1) = S andPr(Q(i) = 0) = 1 S,where
−
S = K/N isthesparsity rate.
Theresultingmodelforsignalcoefficientsisatwo-statemixtureGaussiandistribution, asillustratedin
Figure 1. This mixture model is completely characterized by three parameters: the sparsity rate S and the
variances σ2 andσ2 oftheGaussianpdf’scorresponding toeachstate.
0 1
Mixture Gaussian models have been successfully employed in image processing and inference prob-
lems,becausetheyaresimpleyeteffectiveinmodelingreal-worldsignals[41–43]. Theoreticalconnections
havealsobeenmadebetweenwaveletcoefficientmixturemodelsandthefundamental parametersofBesov
spaces, which have proved invaluable for characterizing real-world images. Moreover, arbitrary densities
withafinitenumber ofdiscontinuities canbeapproximated arbitrarily closely byincreasing thenumber of
statesandallowingnon-zeromeans[47]. Weleavetheseextensionsforfuturework,andfocusontwo-state
mixtureGaussiandistributions formodelingthesignalcoefficients.
2Themodelcanbeextendedtocapturedependenciesbetweencoefficients,assuggestedbyJietal.[25].
6
Copyright (c) 2009 IEEE. Personal use is permitted. For any other purposes, Permission must be obtained from the IEEE by emailing pubs-permissions@ieee.org.
Authorized licensed use limited to: BEIJING UNIVERSITY OF POST AND TELECOM. Downloaded on December 9, 2009 at 20:44 from IEEE Xplore. Restrictions apply.


## 第 7 页

This article has been accepted for publication in a future issue of this journal, but has not been fully edited. Content may change prior to final publication.
Prior Mixing
Encoding
Measurements
Y
States Coefficients
Q X
Fig.2. Factorgraphdepictingtherelationshipbetweenvariablenodes(black)andconstraintnodes(white)inCS-BP.
III. SPARSE ENCODING
SparseCSencodingmatrix: Weuseasparse Φmatrix toaccelerate both CSencoding anddecoding.
Our CS encoding matrices are dominated by zero entries, with a small number of non-zeros in each row
andeachcolumn. WefocusonCS-LDPCmatriceswhosenon-zeroentriesare 1,1 ;3 eachmeasurement
{− }
involves only sumsand differences ofasmall subset of coefficients of x. Although the coherence between
a sparse Φ and Ψ, which is the maximal inner product between rows of Φ and Ψ, may be higher than
the coherence using a dense Φ matrix [48], as long as Φ is not too sparse (see Theorem 1 below) the
measurements captureenoughinformation aboutxtodecodethesignal. ACS-LDPCΦcanberepresented
asabipartitegraphG,whichisalsosparse. EachedgeofGconnectsacoefficientnodex(i)toanencoding
nodey(j)andcorresponds toanon-zero entryofΦ(Figure2).
In addition to the core structure of Φ, we can introduce other constraints to tailor the measurement
process to the signal model. The constant row weight constraint makes sure that each row of Φ contains
exactly L non-zero entries. The row weight L can be chosen based on signal properties such as sparsity,
possiblemeasurementnoise,anddetailsofthedecodingprocess. Anotheroptionistouseaconstantcolumn
weightconstraint, whichfixesthenumberofnon-zero entriesineachcolumnofΦtobeaconstant R.
Althoughouremphasisisonnoiselessmeasurementofapproximatelysparsesignals,webrieflydiscuss
noisy measurement of a strictly sparse signal, and show that a constant row weight L ensures that the
measurements are approximated by two-state mixture Gaussians. To see this, consider a strictly sparse x
3CS-LDPCmatricesareslightlydifferentfromLDPCparitycheckmatrices,whichonlycontainthebinaryentries0and1. We
haveobservednumericallythatallowingnegativeentriesoffersimprovedperformance. Attheexpenseofadditionalcomputation,
furtherminorimprovementcanbeattainedusingsparsematriceswithGaussiannon-zeroentries.
7
Copyright (c) 2009 IEEE. Personal use is permitted. For any other purposes, Permission must be obtained from the IEEE by emailing pubs-permissions@ieee.org.
Authorized licensed use limited to: BEIJING UNIVERSITY OF POST AND TELECOM. Downloaded on December 9, 2009 at 20:44 from IEEE Xplore. Restrictions apply.


## 第 8 页

This article has been accepted for publication in a future issue of this journal, but has not been fully edited. Content may change prior to final publication.
withsparsity rateS andGaussian variance σ2. Wenowhavey = Φx+z,wherez (0,σ2)isadditive
1 ∼ N Z
whiteGaussian noise(AWGN)withvariance σ2. Inourapproximately sparse setting, eachrowofΦpicks
Z
up L(1 S)small magnitude coefficients. IfL(1 S)σ2 σ2, then the few large coefficients willbe
≈ − − 0 ≈ Z
obscured bysimilarnoiseartifacts.
OurdefinitionofΦreliesontheimplicitassumption thatxissparseinthecanonical sparsifying basis,
i.e.,Ψ = I. Incontrast, ifxissparseinsomeotherbasisΨ,thenmorecomplicated encoding matricesmay
be necessary. We defer the discussion of these issues to Section VI, but emphasize that in many practical
situations our methods can be extended to support the sparsifying basis Ψ in a computationally tractable
manner.
Information contentofsparsely encodedmeasurements: Thesparsity ofourCS-LDPCmatrixmay
yieldmeasurementsythatcontainlessinformationaboutthesignalxthanadenseGaussianΦ. Thefollow-
ing theorem, whose proof appears in the Appendix, verifies that y retains enough information to decode x
2
well. AslongasS = K/N = Ω σ0 ,thenM = O(Klog(N))measurements aresufficient.
σ1
(cid:18) (cid:19)
(cid:16) (cid:17)
Theorem1: Let x be a two-state mixture Gaussian signal with sparsity rate S = K/N and variances
σ2 andσ2,andletΦbeaCS-LDPCmatrixwithconstant rowweightL = η
ln(SN1+γ),whereη,γ
> 0. If
0 1 S
(1+2η 1)(1+γ) σ 2
− 0
M = O 2K +(N K) log(N) , (2)
µ2 − σ
" (cid:18) 1(cid:19) # !
thenxcanbedecoded toxsuchthat x x <µσ withprobability 1 2N γ.
1 −
k − k∞ −
TheproofofTheorem1reliesonaresultbyWangetal.[49,Theorem1]. Theirproofpartitions Φinto
b b
M sub-matrices ofM rowseach, and estimates each x asamedian ofinner products withsub-matrices.
2 1 i
The ` performance guarantee relies on the union bound; a less stringent guarantee yields a reduction
∞ b
in M . Moreover, L can be reduced if we increase the number of measurements accordingly. Based on
2
numericalresults, weproposethefollowingmodifiedvaluesasrulesofthumb,
L S 1 = N/K, M = O(Klog(N)), and R = LM/N = O(log(N)). (3)
−
≈
NotingthateachmeasurementrequiresO(L)additionsandsubtractions, andusingourrulesofthumbforL
andM (3),thecomputationrequiredforencodingisO(LM) = O(Nlog(N)),whichissignificantlylower
thantheO(MN) = O(KN log(N))required fordenseGaussianΦ.
IV. CS-BP DECODING OF APPROXIMATELY SPARSE SIGNALS
Decoding approximately sparse random signals can be treated as a Bayesian inference problem. We
observe the measurements y = Φx, where x is a mixture Gaussian signal. Our goal is to estimate x given
8
Copyright (c) 2009 IEEE. Personal use is permitted. For any other purposes, Permission must be obtained from the IEEE by emailing pubs-permissions@ieee.org.
Authorized licensed use limited to: BEIJING UNIVERSITY OF POST AND TELECOM. Downloaded on December 9, 2009 at 20:44 from IEEE Xplore. Restrictions apply.


## 第 9 页

This article has been accepted for publication in a future issue of this journal, but has not been fully edited. Content may change prior to final publication.
Φandy. Because thesetofequations y = Φxisunder-determined, there areinfinitely manysolutions. All
solutions lie along a hyperplane of dimension N M. We locate the solution within this hyperplane that
−
best matches our prior signal model. Consider the minimum mean square error (MMSE) and maximum a
posteriori (MAP)estimates,
x = arg minE X x 2 s.t. y = Φx,
MMSE x0 k − 0 k2 0
x = arg maxf(X = x) s.t. y = Φx,
b MAP x0 0 0
where the expectation is takebn over the prior distribution for X. The MMSE estimate can be expressed as
the conditional mean, x = E[X Y = y], where Y RM is the random vector that corresponds to
MMSE
| ∈
the measurements. Although the precise computation of x may require the evaluation of 2N terms,
MMSE
b
a close approximation to the MMSE estimate can be obtained using the (usually small) set of state con-
b
figuration vectors q with dominant posterior probability [27]. Indeed, exact inference in graphical models
is NP-hard [50], because of loops in the graph induced by Φ. However, the sparse structure of Φ reduces
thenumberofloopsandenablesustouselow-complexity message-passing methodstoestimatexapproxi-
mately.
A. Decodingalgorithm
We now employ belief propagation (BP), an efficient method for solving inference problems by itera-
tively passing messages overgraphical models [30–35]. Although BPhasnot beenproved toconverge, for
graphs with few loops it often offers a good approximation to the solution to the MAP inference problem.
BPreliesonfactorgraphs,whichenablefastcomputationofglobalmultivariatefunctionsbyexploitingthe
way in which the global function factors into a product of simpler local functions, each of which depends
onasubsetofvariables [51].
Factor graph for CS-BP: The factor graph shown in Figure 2 captures the relationship between the
statesq,thesignalcoefficients x,andtheobservedCSmeasurements y. Thegraphisbipartite andcontains
twotypesofvertices;alledgesconnectvariablenodes(black)andconstraintnodes(white). Therearethree
types of variable nodes corresponding tostate variables Q(i), coefficient variables X(i), and measurement
variables Y(j). Thefactorgraph alsohasthree typesofconstraint nodes, whichencapsulate thedependen-
ciesthattheirneighbors inthegraph (variable nodes)aresubjected to. First,priorconstraint nodesimpose
the Bernoulli prior on state variables. Second, mixing constraint nodes impose the conditional distribution
on coefficient variables given the state variables. Third, encoding constraint nodes impose the encoding
matrixstructure onmeasurementvariables.
9
Copyright (c) 2009 IEEE. Personal use is permitted. For any other purposes, Permission must be obtained from the IEEE by emailing pubs-permissions@ieee.org.
Authorized licensed use limited to: BEIJING UNIVERSITY OF POST AND TELECOM. Downloaded on December 9, 2009 at 20:44 from IEEE Xplore. Restrictions apply.


## 第 10 页

This article has been accepted for publication in a future issue of this journal, but has not been fully edited. Content may change prior to final publication.
Message passing: CS-BPapproximates the marginal distributions ofallcoefficient and state variables
in the factor graph, conditioned on the observed measurements Y, by passing messages between variable
nodes and constraint nodes. Each message encodes themarginal distributions ofavariable associated with
one of the edges. Given the distributions Pr(Q(i)Y = y) and f(X(i)Y = y), one can extract MAP and
| |
MMSEestimates foreachcoefficient.
Denotethemessagesentfromavariablenodevtooneofitsneighborsinthebipartitegraph,aconstraint
nodec,byµ (v);amessagefromctov isdenoted byµ (v). Themessageµ (v)isupdatedby
v c c v v c
−→ −→ −→
takingtheproductofallmessagesreceivedbyvonallotheredges. Themessageµ (v)iscomputedina
c v
−→
similar manner, buttheconstraint associated withcisapplied totheproduct and theresult ismarginalized.
Moreformally,
µ (v) = µ (v), (4)
v c u v
−→ −→
u n(v) c
∈ Y\{ }
µ (v) = con(n(c)) µ (w) , (5)
c v w c
−→  −→ 
v w n(c) v
∼X{ } ∈ Y\{ }
where n(v) and n(c) are sets of neighborsof v and c, respectively, con(n(c)) is the constraint on the set
of variable nodes n(c), and v is the set of neighbors of c excluding v. We interpret these 2 types of
∼ { }
messageprocessingasmultiplicationofbeliefsatvariablenodes(4)andconvolutionatconstraintnodes(5).
Finally,themarginaldistribution f(v)foragivenvariablenodeisobtained fromtheproductofallthemost
recentincomingmessagesalongtheedgesconnecting tothatnode,
f(v)= µ (v). (6)
u v
−→
u n(v)
∈Y
Basedonthemarginaldistribution, variousstatistical characterizations canbecomputed,including MMSE,
MAP,errorbars,andsoon.
Wealsoneedamethodtoencodebeliefs. Onemethodistosampletherelevantpdf’suniformlyandthen
use the samples as messages. Another encoding method is to approximate the pdf by a mixture Gaussian
with a given number of components, where mixture parameters are used as messages. These two methods
offer different trade-offs between modeling flexibility and computational requirements; details appear in
Sections IV-B and IV-C. Weleave alternative methods such as particle filters and importance sampling for
futureresearch.
Protecting against loopy graphs and message quantization errors: BP converges to the exact con-
ditional distribution in the ideal situation where the following conditions are met: (i) the factor graph is
cycle-free; and(ii)messagesareprocessed andpropagated withouterrors. InCS-BPdecoding, bothcondi-
tionsareviolated. First,thefactorgraphisloopy—itcontains cycles. Second, messageencoding methods
10
Copyright (c) 2009 IEEE. Personal use is permitted. For any other purposes, Permission must be obtained from the IEEE by emailing pubs-permissions@ieee.org.
Authorized licensed use limited to: BEIJING UNIVERSITY OF POST AND TELECOM. Downloaded on December 9, 2009 at 20:44 from IEEE Xplore. Restrictions apply.


## 第 11 页

This article has been accepted for publication in a future issue of this journal, but has not been fully edited. Content may change prior to final publication.
introduce errors. These non-idealities may lead CS-BP to converge to imprecise conditional distributions,
or more critically, lead CS-BP to diverge [52–54]. To some extent these problems can be reduced by (i)
usingCS-LDPCmatrices, whichhavearelatively modestnumberofloops; and(ii)carefully designing our
messageencodingmethods(SectionsIV-BandIV-C). WestabilizeCS-BPagainstthesenon-idealitiesusing
messagedampedbeliefpropagation (MDBP)[55],wheremessagesareweightedaverages betweenoldand
newestimates. Despitethedamping, CS-BPisnotguaranteed toconverge, andyetthenumerical resultsof
Section V demonstrate that its performance is quite promising. We conclude with a prototype algorithm;
Matlabcodeisavailable athttp://dsp.rice.edu/CSBP.
CS-BPDecodingAlgorithm
1) Initialization: Initialize the iteration counter i = 1. Setup data structures for factor graph messages
µ (v) and µ (v). Initialize messages µ (v) from variable to constraint nodes with the
v c c v v c
−→ −→ −→
signalprior.
2) Convolution:Foreachmeasurementc= 1,...,M,whichcorrespondstoconstraintnodec,compute
µ (v)viaconvolution(5)forallneighboringvariablenodesn(c). Ifmeasurementnoiseispresent,
c v
−→
then convolve further with a noise prior. Apply damping methods such as MDBP[55] by weighting
thenewestimatesfromiteration iwithestimatesfromprevious iterations.
3) Multiplication:Foreachcoefficient v = 1,...,N,whichcorresponds toavariable nodev,compute
µ (v) via multiplication (4) for all neighboring constraint nodes n(v). Apply damping methods
v c
−→
asneeded. Iftheiteration counterhasyettoreachitsmaximalvalue, thengotoStep2.
4) Output:Foreachcoefficientv = 1,...,N,compute MMSEorMAPestimates(oralternative statis-
ticalcharacterizations) basedonthemarginaldistribution f(v)(6). Outputtherequisite statistics.
B. Samplesofthepdfasmessages
Having described main aspects of the CS-BP decoding algorithm, we now focus on the two message
encoding methods, starting with samples. In this method, we sample the pdf and send the samples as
messages. Multiplicationofpdf’s(4)correspondstopoint-wisemultiplication ofmessages;convolution (5)
iscomputed efficientlyinthefrequency domain.4
Themainadvantageofusingsamplesisflexibilitytodifferentpriordistributionsforthecoefficients;for
example,mixtureGaussianpriorsareeasilysupported. Additionally,bothmultiplicationandconvolutionare
computedefficiently. However,samplinghaslargememoryrequirementsandintroducesquantizationerrors
4FastconvolutionviaFFThasbeenusedinLDPCdecodingoverGF(2q)usingBP[34].
11
Copyright (c) 2009 IEEE. Personal use is permitted. For any other purposes, Permission must be obtained from the IEEE by emailing pubs-permissions@ieee.org.
Authorized licensed use limited to: BEIJING UNIVERSITY OF POST AND TELECOM. Downloaded on December 9, 2009 at 20:44 from IEEE Xplore. Restrictions apply.


## 第 12 页

This article has been accepted for publication in a future issue of this journal, but has not been fully edited. Content may change prior to final publication.
thatreduceprecisionandhampertheconvergence ofCS-BP[52]. Samplingalsorequiresfinersamplingfor
precisedecoding; wepropose tosamplethepdf’swithaspacing lessthanσ .
0
We analyze the computational requirements of this method. Let each message be a vector of p sam-
ples. Eachiterationperformsmultiplication atcoefficientnodes(4)andconvolution atconstraint nodes(5).
Outgoingmessagesaremodified,
µ (v) µ (w)
u n(v) u v w n(c) w c
µ v c (v) = ∈ −→ and µ c v (v) = con(n(c)) ∈ −→ , (7)
−→ Q µ c v (v) −→ Q µ v c (v) !
−→ ∼X{ v } −→
where the denominators are non-zero, because mixture Gaussian pdf’s are strictly positive. The modifica-
tions (7) reduce computation, because the numerators are computed once and then reused for all messages
leaving thenodebeingprocessed.
Assuming that the column weight R is fixed (Section III), the computation required for message pro-
cessingatavariablenodeisO(Rp)periteration,becausewemultiplyR+1vectorsoflengthp. WithO(N)
variablenodes,eachiterationrequiresO(NRp)computation. Forconstraintnodes,weperformconvolution
in the frequency domain, and so the computational cost per node is O(Lplog(p)). With O(M) constraint
nodes, each iteration is O(LMplog(p)). Accounting for both variable and constraint nodes, each iteration
is O(NRp+LMplog(p)) = O(plog(p)Nlog(N)), where we employ our rules of thumb for L, M, and
R (3). To complete the computational analysis, we note first that we use O(log(N)) CS-BP iterations,
whichisproportional tothediameterofthegraph[56]. Second,samplingthepdf’swithaspacinglessthan
σ , we choose p = O(σ /σ ) to support a maximal amplitude on the order of σ . Therefore, our overall
0 1 0 1
computation isO σ1 log σ1 Nlog2(N) ,whichscalesasO(Nlog2(N))whenσ andσ areconstant.
σ0 σ0 0 1
(cid:16) (cid:16) (cid:17) (cid:17)
C. MixtureGaussianparameters asmessages
Inthismethod,weapproximatethepdfbyamixtureGaussianwithamaximumnumberofcomponents,
and then send the mixture parameters as messages. For both multiplication (4) and convolution (5), the
resulting number of components in the mixture is multiplicative in the number of constituent components.
To keep the message representation tractable, we perform model reduction using the Iterative Pairwise
ReplacementAlgorithm (IPRA)[57],whereasequence ofmixturemodelsiscomputediteratively.
The advantage of using mixture Gaussians to encode pdf’s is that the messages are short and hence
consumelittlememory. ThismethodworkswellformixtureGaussianpriors,butcouldbedifficulttoadapt
to other priors. Model order reduction algorithms such as IPRA can be computationally expensive [57],
andintroduce errorsinthemessages, whichimpairthequalityofthesolution aswellastheconvergence of
CS-BP[52].
12
Copyright (c) 2009 IEEE. Personal use is permitted. For any other purposes, Permission must be obtained from the IEEE by emailing pubs-permissions@ieee.org.
Authorized licensed use limited to: BEIJING UNIVERSITY OF POST AND TELECOM. Downloaded on December 9, 2009 at 20:44 from IEEE Xplore. Restrictions apply.


## 第 13 页

This article has been accepted for publication in a future issue of this journal, but has not been fully edited. Content may change prior to final publication.
TABLEI
ComputationalandstoragerequirementsofCS-BPdecoding
Messages Parameter Computation Storage
Samplesofpdf p = O(σ /σ )samples O σ1 log σ1 Nlog2(N) O(pN log(N))
1 0 σ0 σ0
MixtureGaussians mcomponents O (cid:16) m2N lo (cid:16) g2( (cid:17) N) (cid:17) O(mNlog(N))
S
(cid:0) (cid:1)
Again, we analyze the computational requirements. Because it is impossible to undo the multiplica-
tion in (4) and (5), we cannot use the modified form (7). Let m be the maximum model order. Model
order reduction using IPRA [57] requires O(m2R2) computation per coefficient node per iteration. With
O(N) coefficient nodes, each iteration is O(m2R2N). Similarly, with O(M) constraint nodes, each iter-
ation is O(m2L2M). Accounting for O(log(N)) CS-BP iterations, overall computation is O(m2[L2M +
R2N]log(N)) = O m2N log2(N) .
S
(cid:0) (cid:1)
D. PropertiesofCS-BPdecoding
We briefly describe several properties of CS-BP decoding. The computational characteristics of the
twomethodsforencodingbeliefsaboutconditionaldistributions wereevaluatedinSectionsIV-BandIV-C.
The storage requirements are mainly for message representation of the LM = O(Nlog(N)) edges. For
encoding withpdf samples, the message length isp, andso thestorage requirement isO(pN log(N)). For
encoding with mixture Gaussian parameters, the message length is m, and so the storage requirement is
O(mNlog(N)). Computational andstoragerequirements aresummarizedinTableI.
Several additional properties are now featured. First, we have progressive decoding; more measure-
ments willimprove the precision ofthe estimated posterior probabilities. Second, ifweare only interested
inanestimateofthestateconfigurationvectorqbutnotinthecoefficientvalues,thenlessinformationmust
beextractedfromthemeasurements. Consequently, thenumberofmeasurementscanbereduced. Third,we
have robustness to noise, because noisy measurements can be incorporated into our model by convolving
thenoiseless versionoftheestimatedpdf(5)ateachencoding nodewiththepdfofthenoise.
V. NUMERICAL RESULTS
To demonstrate the efficacy of CS-BP, we simulated several different settings. In our first setting, we
considered decoding problems where N = 1000, S = 0.1, σ = 10, σ = 1, and the measurements are
1 0
noiseless. Weused samples of the pdfas messages, where each message consisted ofp = 525 = 3 52 7
· ·
samples; this choice of p provided fast FFT computation. Figure 3 plots the MMSE decoding error as a
13
Copyright (c) 2009 IEEE. Personal use is permitted. For any other purposes, Permission must be obtained from the IEEE by emailing pubs-permissions@ieee.org.
Authorized licensed use limited to: BEIJING UNIVERSITY OF POST AND TELECOM. Downloaded on December 9, 2009 at 20:44 from IEEE Xplore. Restrictions apply.


## 第 14 页

This article has been accepted for publication in a future issue of this journal, but has not been fully edited. Content may change prior to final publication.
100
80
60
40
20
100 200 300 400 500 600 700
M
Copyright (c) 2009 IEEE. Personal use is permitted. For any other purposes, Permission must be obtained from the IEEE by emailing pubs-permissions@ieee.org.
ESMM
L=5
L=10
L=20
Fig.3. MMSEasafunctionofthenumberofmeasurementsM usingdifferentmatrixrowweightsL.Thedashed
linesshowthe`2normsofx(top)andthesmallcoefficients(bottom).(N = 1000,S = 0.1,σ1 = 10,σ0 = 1,and
noiselessmeasurements.)
functionofM foravarietyofrowweightsL. Thefigureemphasizes withdashedlinestheaverage` norm
2
of x(top) and of the small coefficients (bottom); increasing M reduces the decoding error, until it reaches
the energy level of the small coefficients. A small row weight, e.g., L = 5, may miss some of the large
coefficients and is thus bad for decoding; as we increase L, fewer measurements are needed to obtain the
same precision. However, there is an optimal L 2/S = 20 beyond which any performance gains
opt
≈
are marginal. Furthermore, values of L > L give rise to divergence in CS-BP, even with damping. An
opt
exampleoftheoutputoftheCS-BPdecoderandhowitcomparestothesignalxappearsinFigure4,where
we used L = 20 and M = 400. Although N = 1000, we only plotted the first 100 signal values x(i) for
easeofvisualization.
To compare the performance of CS-BP with other CS decoding algorithms, we also simulated: (i) `
1
decoding(1)vialinearprogramming;(ii)GPSR[20],anoptimizationmethodthatminimizes θ +µ y
1
k k k −
ΦΨθ 2; (iii) CoSaMP [16], a fast greedy solver; and (iv) IHT [17], an iterative thresholding algorithm.
k2
We simulated all five methods where N = 1000, S = 0.1, L = 20, σ = 10, σ = 1, p = 525, and
1 0
the measurements are noiseless. Throughout the experiment we ran the different methods using the same
CS-LDPC encoding matrix Φ, the same signal x, and therefore same measurements y. Figure 5 plots the
MMSEdecoding error as afunction of M for the fivemethods. Forsmall to moderate M, CS-BPexploits
its knowledge about the approximately sparse structure of x, and has a smaller decoding error. CS-BP
requires 20–30% fewer measurements than the optimization methods LP and GPSR to obtain the same
MMSEdecoding error; the advantage over the greedy solvers IHT and CoSaMP is even greater. However,
asM increases, theadvantage ofCS-BPoverLPandGPSRbecomeslesspronounced.
14
Authorized licensed use limited to: BEIJING UNIVERSITY OF POST AND TELECOM. Downloaded on December 9, 2009 at 20:44 from IEEE Xplore. Restrictions apply.


## 第 15 页

This article has been accepted for publication in a future issue of this journal, but has not been fully edited. Content may change prior to final publication.
20
10
0
−10
−20
0 10 20 30 40 50 60 70 80 90 100
i
Copyright (c) 2009 IEEE. Personal use is permitted. For any other purposes, Permission must be obtained from the IEEE by emailing pubs-permissions@ieee.org.
)i(x
lanigirO
20
10
0
−10
−20
0 10 20 30 40 50 60 70 80 90 100
i
)i(x
fo
etamitse
PB−SC
Fig.4. OriginalsignalxandversiondecodedbyCS-BP.(N =1000,S =0.1,L=20,M =400,σ1 =10,σ0 =1,
andnoiselessmeasurements.)
To compare the speed of CS-BP to other methods, we ran the same five methods as before. In this
experiment, we varied the signal length N from 100 to 10000, where S = 0.1, L = 20, σ = 10, σ = 1,
1 0
p = 525,andthemeasurements arenoiseless. Wementioninpassing thatsomeofthealgorithms thatwere
evaluatedcanbeacceleratedusinglinearalgebraroutinesoptimizedforsparsematrices;theimprovementis
quitemodest,andtherun-timespresented heredonotreflectthisoptimization. Figure6plotstherun-times
ofthe fivemethods inseconds asafunction ofN. Itcan beseen that LPscales morepoorly than theother
algorithms, and so we did not simulate it for N > 3000.5 CoSaMP also seems to scale relatively poorly,
althoughitispossiblethatourconjugategradientimplementationcanbeimprovedusingthepseudo-inverse
approach instead [16]. The run-times of CS-BP seem to scale somewhat better than IHT and GPSR. Al-
though the asymptotic computational complexity of CS-BP is good, for signals of length N = 10000 it
is still slower than IHT and GPSR; whereas IHT and GPSR essentially perform matrix-vector multiplica-
tions, CS-BP is slowed by FFT computations performed in each iteration for all nodes in the factor graph.
Additionally, whereasthechoicep = O(σ /σ )yieldsO σ1 log σ1 Nlog2(N) complexity,FFTcom-
1 0 σ0 σ0
putation with p = 525 samples is somewhat slow. That(cid:16)said, ou(cid:16)r m(cid:17)ain contributi(cid:17)on is a computationally
feasible Bayesian approach, whichallows toreduce thenumber ofmeasurements (Figure 5); acomparison
betweenCS-BPandprevious Bayesianapproaches toCS[25,26]wouldbefavorable.
To demonstrate that CS-BP deals well with measurement noise, recall the noisy measurement setting
5OurLPsolverisbasedoninteriorpointmethods.
15
Authorized licensed use limited to: BEIJING UNIVERSITY OF POST AND TELECOM. Downloaded on December 9, 2009 at 20:44 from IEEE Xplore. Restrictions apply.


## 第 16 页

This article has been accepted for publication in a future issue of this journal, but has not been fully edited. Content may change prior to final publication.
100
80
60
40
20
100 200 300 400 500 600 700
M
Copyright (c) 2009 IEEE. Personal use is permitted. For any other purposes, Permission must be obtained from the IEEE by emailing pubs-permissions@ieee.org.
ESMM
IHT
CoSaMP
GPSR
LP
CS−BP
Fig. 5. MMSEasafunctionofthenumberofmeasurementsM usingCS-BP,linearprogramming(LP),GPSR,
CoSaMP,andIHT.Thedashedlinesshowthe`2 normsofx(top)andthesmallcoefficients(bottom).(N = 1000,
S =0.1,L=20,σ1 =10,σ0 =1,andnoiselessmeasurements.)
y = Φx+zofSectionIII,wherez (0,σ2)isAWGNwithvarianceσ2. Ouralgorithmdealswithnoise
∼ N Z Z
by convolving the noiseless version of the estimated pdf (5) with the noise pdf. We simulated decoding
problems where N = 1000, S = 0.1, L = 20, σ = 10, σ = 1, p = 525, and σ2 0,2,5,10 .
1 0 Z ∈ { }
Figure 7 plots the MMSE decoding error as a function of M and σ2. To put things in perspective, the
Z
average measurement picks up a Gaussian term of variance L(1 S)σ2 = 18 from the signal. Although
− 0
thedecoding errorincreases withσ2,aslongasσ2 18thenoisehaslittleimpactonthedecoding error;
Z Z (cid:28)
CS-BPoffersagracefuldegradation tomeasurement noise.
OurfinalexperimentconsidersmodelmismatchwhereCS-BPhasanimprecisestatisticalcharacteriza-
tion of the signal. Instead ofa two-state mixture Gaussian signal model as before, where large coefficients
have variance σ2 and occur with probability S, we defined a C-component mixture model. In our defini-
1
tion,σ2 isinterpreted asabackground signallevel,whichappearsinallcoefficients. Whereasthetwo-state
0
modeladdsa“truesignal” component ofvariance σ2 σ2 tothebackground signal, theC 1large com-
1 − 0 −
ponents each occur with probability S and the amplitudes of the true signals are σ ,2σ ,...,(C 1)σ ,
2 2 2
−
where σ is chosen to preserve the total signal energy. At the same time, we did not change the signal
2
priors in CS-BP, and used the same two-state mixture model as before. We simulated decoding problems
where N = 1000, S = 0.1, L = 20, σ = 10, σ = 1, p = 525, the measurements are noiseless, and
1 0
C 2,3,5 . Figure 8 plots the MMSE decoding error as a function of M and C. The figure also shows
∈ { }
howIHTandGPSRperform, inordertoevaluatewhethertheyaremorerobustthantheBayesianapproach
ofCS-BP.WedidnotsimulateCoSaMPand` decoding, sincetheirMMSEperformance iscomparable to
1
thatofIHTandGPSR.Asthenumberofmixturecomponents C increases, theMMSEprovided byCS-BP
16
Authorized licensed use limited to: BEIJING UNIVERSITY OF POST AND TELECOM. Downloaded on December 9, 2009 at 20:44 from IEEE Xplore. Restrictions apply.


## 第 17 页

This article has been accepted for publication in a future issue of this journal, but has not been fully edited. Content may change prior to final publication.
2 10
0
10
2 3 4
10 10 10
N
Copyright (c) 2009 IEEE. Personal use is permitted. For any other purposes, Permission must be obtained from the IEEE by emailing pubs-permissions@ieee.org.
]sdnoces[
emiT
LP
CS−BP
GPSR
CoSaMP
IHT
Fig.6. Run-timeinsecondsasafunctionofthesignallengthN usingCS-BP,linearprogramming(LP)`1decoding,
GPSR,CoSaMP,andIHT.(S =0.1,L=20,M =0.4N,σ1 =10,σ0 =1,andnoiselessmeasurements.)
increases. However, even for C = 3 the sparsity rate effectively doubles from S to 2S, and an increase in
the required number of measurements M is expected. Interestingly, the greedy IHT method also degrades
significantly, perhaps because it implicitly makes an assumption regarding the number of large mixture
components. GPSR,ontheotherhand,degrades moregracefully.
VI. VARIATIONS AND ENHANCEMENTS
SupportingarbitrarysparsifyingbasisΨ:Untilnow,wehaveassumedthatthecanonicalsparsifying
basis is used, i.e., Ψ = I. In this case, x itself is sparse. We now explain how CS-BP can be modified to
supportthecasewherexissparseinanarbitrarybasisΨ. Intheencoder, wemultiplytheCS-LDPCmatrix
Φ by ΨT and encode x as y = (ΦΨT)x = (ΦΨT)(Ψθ) = Φθ, where ()T denotes the transpose operator.
·
In the decoder, we use BP to form the approximation θ, and then transform via Ψ to x = Ψθ. In order
to construct the modified encoding matrix ΦΨT and later transform θ to x, extra computation is needed;
b b b
this extra cost is O(N2) in general. Fortunately, in many practical situations Ψ is structured (e.g., Fourier
b b
or wavelet bases) and amenable to fast computation. Therefore, extending our methods to such bases is
feasible.
Exploiting statistical dependencies: In many signal representations, the coefficients are not iid. For
example,waveletrepresentations ofnaturalimagesoftencontaincorrelationsbetweenmagnitudesofparent
and child coefficients [2,43]. Consequently, it is possible to decode signals from fewer measurements
using an algorithm that allocates different distributions to different coefficients [46,58]. By modifying the
dependencies imposed by the prior constraint nodes (Section IV-A), CS-BP decoding supports different
signalmodels.
17
Authorized licensed use limited to: BEIJING UNIVERSITY OF POST AND TELECOM. Downloaded on December 9, 2009 at 20:44 from IEEE Xplore. Restrictions apply.


## 第 18 页

This article has been accepted for publication in a future issue of this journal, but has not been fully edited. Content may change prior to final publication.
100
80
60
40
20
100 200 300 400 500 600 700
M
Copyright (c) 2009 IEEE. Personal use is permitted. For any other purposes, Permission must be obtained from the IEEE by emailing pubs-permissions@ieee.org.
ESMM
s 2 =10
Z
s 2 =5
Z
s 2 =2
Z
Noiseless
Fig.7. MMSEasafunctionofM usingdifferentnoiselevelsσ Z 2.Thedashedlinesshowthe`2normsofx(top)and
thesmallcoefficients(bottom).(N =1000,S =0.1,L=20,σ1 =10,andσ0 =1.)
Feedback:Feedbackfromthedecodertotheencodercanbeusedinapplications wheremeasurements
maybelostbecauseoftransmissionsoverfaultychannels. Inananalogousmannertoadigitalfountain[59],
the marginal distributions (6) enable us to identify when sufficient information for signal decoding has
been received. At that stage, the decoder notifies the encoder that decoding is complete, and the stream of
measurements isstopped.
Irregular CS-LDPCmatrices:Inchannelcoding, LDPCmatricesthathaveirregularrowandcolumn
weights come closer to the Shannon limit, because a small number of rows or columns with large weights
require only modest additional computation yet greatly reduce the block error rate [38]. In an analogous
manner,weexpectirregularCS-LDPCmatricestoenableafurtherreductioninthenumberofmeasurements
required.
VII. DISCUSSION
This paper has developed a sparse encoding matrix and belief propagation decoding algorithm to ac-
celerate CS encoding and decoding under the Bayesian framework. Although we focus on decoding ap-
proximately sparse signals, CS-BP can be extended to signals that are sparse in other bases, is flexible to
modifications inthesignalmodel,andcanaddressmeasurementnoise.
Despite the significant benefits, CS-BP is not universal in the sense that the encoding matrix and de-
coding methods must be modified in order to apply our framework to arbitrary bases. Nonetheless, the
necessary modifications onlyrequiremultiplication bythesparsifying basisΨoritstranspose ΨT.
Our method resembles low density parity check (LDPC) codes [37,38], which use a sparse Bernoulli
parity check matrix. Although any linear code can be represented as a bipartite graph, for LDPC codes
18
Authorized licensed use limited to: BEIJING UNIVERSITY OF POST AND TELECOM. Downloaded on December 9, 2009 at 20:44 from IEEE Xplore. Restrictions apply.


## 第 19 页

This article has been accepted for publication in a future issue of this journal, but has not been fully edited. Content may change prior to final publication.
100
90
80
70
60
50
40
30
20
100 200 300 400 500 600 700 800
M
Copyright (c) 2009 IEEE. Personal use is permitted. For any other purposes, Permission must be obtained from the IEEE by emailing pubs-permissions@ieee.org.
ESMM
IHT C=5
IHT C=3
CS−BP C=5
IHT C=2
GPSR C=5
GPSR C=3
CS−BP C=3
GPSR C=2
CS−BP C=2
Fig.8. MMSEasafunctionofthenumberofmeasurementsM andthenumberofcomponentsC inthemixture
Gaussiansignalmodel. PlotsforCS-BP(x),GPSR(circle),andIHT(asterisk)appearforC = 2(dotted),C = 3
(dashed),andC = 5(solid). Thehorizontaldashedlinesshowthe`2 normsofx (top)andthesmallcoefficients
(bottom).(N =1000,S =0.1,L=20,σ1 =10,σ0 =1,andnoiselessmeasurements.)
the sparsity of the graph accelerates the encoding and decoding processes. LDPCcodes are celebrated for
achievingratesclosetotheShannonlimit. AsimilarcomparisonoftheMMSEperformanceofCS-BPwith
information theoretic bounds on CS performance is left for future research. Additionally, although CS-BP
isnotguaranteed toconverge, therecent convergence proofsforLDLCcodes[36]suggest thatfuturework
onextensions ofCS-BPmayalsoyieldconvergence proofs.
IncomparisontopreviousworkonBayesianaspectsofCS[25,26],ourmethodismuchfaster,requiring
only O(Nlog2(N)) computation. Atthe sametime, CS-BPoffers significant flexibility, and should notbe
viewedasmerelyanother fastCSdecoding algorithm. However,CS-BPreliesonthesparsity ofCS-LDPC
matrices,andfutureresearch canconsidertheapplicability ofsuchmatricesindifferentapplications.
APPENDIX
Outline of proof of Theorem 1: The proof begins with a derivation of probabilistic bounds on x
2
k k
19
Authorized licensed use limited to: BEIJING UNIVERSITY OF POST AND TELECOM. Downloaded on December 9, 2009 at 20:44 from IEEE Xplore. Restrictions apply.


## 第 20 页

This article has been accepted for publication in a future issue of this journal, but has not been fully edited. Content may change prior to final publication.
and x . Next,wereviewaresult byWangetal.[49,Theorem 1]. Theproofiscompleted bycombining
k k∞
theboundswiththeresultbyWangetal.
Upperboundon x 2:Consider x 2 = N x2,wheretherandomvariable(RV)X hasamixture
k k2 k k2 i=1 i i
distribution P
χ2σ2 w.p. S
X2 1 .
i ∼  χ2σ2 w.p. 1 S
 0 −
Recall the moment generating function (MGF), M (t) = E[etx]. The MGF of a Chi-squared RV satisfies
 X
M
χ2
(t) = (1
−
2t)
−
1 2. ForthemixtureRVX
i
2,
S 1 S
M X i 2 (t) = 1 2tσ2 + 1 − 2tσ2 .
− 1 − 0
p Np
Additionally, because theX areiid,M (t) = M (t) . Invoking theChernoffbound,wehave
i x 2 X2
k k2 i
h i
N
S 1 S
Pr k x k 2 2 < SNσ 1 2 < e − tSNσ 1 2 " 1 2tσ2 + 1 − 2tσ2 #
− 1 − 0
(cid:0) (cid:1)
fort < 0. WeaimtoshowthatPr x 2 < SNσ2 decpaysfasterthanNp γ asN isincreased. Todoso,let
k k2 1 −
t = α ,whereα > 0. Itsuffices(cid:0)toprovethatthe(cid:1)reexistssomeαforwhich
−σ
1
2
S 1 S
f 1 (α) =eαS  + −  < 1.
√1+2α 2
1+2α σ0

 r
σ1 

 (cid:16) (cid:17) 
Let f (α) = 1 and f (α) = eα. It is easily seen via Taylor series that f (α) = 1 α+O(α2) and
2 √1+2α 3 2 −
f (α) = 1+α+O(α2),andso
3
2 4
σ σ
f (α) = eαS S 1 α+O(α2) +(1 S) 1 α 0 +O α2 0
1
− − − σ σ
" (cid:18) 1(cid:19) (cid:18) 1(cid:19) !!#
(cid:0) (cid:1)
2
σ
= 1+αS +O(α2S2) 1 α S +(1 S) 0 +O(α2) .
− − σ
" (cid:18) 1(cid:19) ! #
(cid:2) (cid:3)
2
Because of the negative term α(1 S) σ0 < 0, which dominates the higher order term O(α2) for
− − σ1
small α, there exists α > 0, which is indep(cid:16)end(cid:17)ent of N, for which f (α) < 1. Using this α, the Chernoff
1
boundprovidesanupperboundonPr x 2 < SNσ2 thatdecaysexponentially withN. Insummary,
k k2 1
(cid:0) (cid:1)
Pr x 2 < SNσ2 =o(N γ). (8)
k k2 1 −
(cid:0) (cid:1)
Lower bound on x 2: In a similar manner, MGF’s and the Chernoff bound can be used to offer a
k k2
probabilistic boundonthenumberoflargeGaussianmixturecomponents
N
3
Pr Q(i) > SN = o(N γ). (9)
−
2
!
i=1
X
20
Copyright (c) 2009 IEEE. Personal use is permitted. For any other purposes, Permission must be obtained from the IEEE by emailing pubs-permissions@ieee.org.
Authorized licensed use limited to: BEIJING UNIVERSITY OF POST AND TELECOM. Downloaded on December 9, 2009 at 20:44 from IEEE Xplore. Restrictions apply.


## 第 21 页

This article has been accepted for publication in a future issue of this journal, but has not been fully edited. Content may change prior to final publication.
Takingintoaccountthelimitednumberoflargecomponents andtheexpected squared ` norm,E[ x 2] =
2 k k2
N[Sσ2+(1 S)σ2],wehave
1 − 0
Pr x 2 > N[2Sσ2 +(1 S)σ2] =o(N γ). (10)
k k2 1 − 0 −
(cid:0) (cid:1)
Weomitthe(similar)detailsforbrevity.
Boundon x :Theupperboundon x isobtainedbyfirstconsidering largemixturecomponents
k k∞ k k∞
and then small components. First, we consider the large Gaussian mixture components, and denote x =
L
x(i) : Q(i) = 1 .
{ }
N 3 3SN
Pr x < 2ln(SN1+γ)σ Q(i) SN f 2ln(SN1+γ) 2 (11)
L 1 4
k k∞ (cid:12) ≤ 2 ! ≥
p (cid:12)X i=1 h (cid:16)p (cid:17)i
(cid:12) (cid:12) (cid:12) f 5 2ln(SN1+γ) 3 2 SN
> 1 (12)
 − (cid:16)p2ln(SN1+γ) (cid:17)
 p 
f 2ln(SN1+γ)
3 5
> 1 SN (13)
− 2 (cid:16)p2ln(SN1+γ) (cid:17)
3SpN e −2
12ln(SN1+γ)
= 1
− 2 2ln(SN1+γ) √2π
3N γ
p −
= 1 ,
− 4 ln(SN1+γ)
where f (α) = 1 α e u2/2du is the cumulative distribution funpction of the standard normal dis-
4 √2π −
−∞
tribution, the inequalitRy (11) relies on f () < 1 and the possibility that N Q(i) is strictly smaller
4 · i=1
than
2
3SN, f
5
(α) =
√
1
2π
e
−
α2/2 is the pdf of the standard normal distributPion, (12) relies on the bound
f (α) > 1 f (α)/α,andtheinequality (13)ismotivatedby(1 α)β > 1 αβ forα,β > 0. Notingthat
4 5
− − −
ln(SN1+γ)increases withN,forlargeN wehave
N 3 N γ
Pr x < 2ln(SN1+γ)σ Q(i) SN > 1 − . (14)
L 1
k k∞ (cid:12) ≤ 2 ! − 5
p (cid:12)X i=1
(cid:12)
Nowconsider thesmallGaussianmixturecomponents(cid:12), anddenotex = x(i) : Q(i) = 0 . Asbefore,
(cid:12) S { }
N
σ
Pr x < 2ln(SN1+γ)σ f 2ln(SN1+γ) 1 (15)
S 1 4
k k∞ ≥
(cid:20) (cid:18)
σ
0(cid:19)(cid:21)
(cid:16) p (cid:17) p 12ln(SN1+γ) σ1 2
N e−2 “σ0”
> 1 ,
− 2ln(SN1+γ)σ1 √2π
σ0
wherein(15)thenumberofsmallmixturecomponents ipsoftenlessthanN. Becauseσ > σ ,forlargeN
1 0
wehave
N γ
Pr x < 2ln(SN1+γ)σ > 1 − . (16)
S 1
k k∞ − 5
(cid:16) p (cid:17)
21
Copyright (c) 2009 IEEE. Personal use is permitted. For any other purposes, Permission must be obtained from the IEEE by emailing pubs-permissions@ieee.org.
Authorized licensed use limited to: BEIJING UNIVERSITY OF POST AND TELECOM. Downloaded on December 9, 2009 at 20:44 from IEEE Xplore. Restrictions apply.


## 第 22 页

This article has been accepted for publication in a future issue of this journal, but has not been fully edited. Content may change prior to final publication.
Combining(9),(14)and(16),forlargeN wehave
N γ
Pr x < 2ln(SN1+γ)σ > 1 − . (17)
1
k k∞ − 2
(cid:16) p (cid:17)
ResultbyWangetal.[49,Theorem1]:
Theorem2—[49]: Considerx RN thatsatisfiesthecondition
∈
x
k k∞ Q. (18)
x ≤
2
k k
Inaddition,letV beanysetofN vectors v ,...,v RN. SupposeasparserandommatrixΦ RM N
1 N ×
{ } ⊂ ∈
satisfies
E[Φ ]= 0,E[Φ2 ]= 1,E[Φ4 ]= s,
ij ij ij
where 1 = L isthefraction ofnon-zero entriesinΦ. Let
s N
O 1+γsQ2log(N) ifsQ2 Ω(1)
M = (cid:15)2 ≥ . (19)
 O (cid:16)1+γ log(N) (cid:17) ifsQ2 O(1)
 (cid:15)2 ≤
(cid:16) (cid:17)
Then with probability at least 1  N γ, the random projections 1 Φxand 1 Φv can produce an estimate
− − M M i
a forxTv satisfying
i i
a xTv (cid:15) x v , i 1,...,N .
i i 2 i 2
b | − | ≤ k k k k ∀ ∈ { }
Application of Theorem 2 to proof of Theorem 1: Combining (8), (10), and (17), the union bound
b
demonstrates that with probability lower bounded by 1 N γ we have x < 2ln(SN1+γ)σ and
− 1
− k k∞
x 2 (NSσ2,N[2Sσ2 +(1 S)σ2]).6 Whenthese` and` boundshold,wecapnapplyTheorem2.
k k2 ∈ 1 1 − 0 2 ∞
To apply Theorem 2, we must specify (i) Q (18); (ii) the test vectors (v )N ; (iii) the matrix sparsity
i i=1
s; and (iv) the (cid:15) parameter. First, the bounds on k x k 2 and k x k∞ indicate that k
k
x x k
k
∞ 2 ≤ Q = 2ln(S S N N 1+γ).
Second, we choose (v )N to be the N canonical vectors of the identity matrix I , providin q g xTv = x .
i i=1 N i i
Third,ourchoiceofLofferss = N = NS . Fourth,weset
L ηln(SN1+γ)
µσ
1
(cid:15) = .
N[2Sσ2+(1 S)σ2]
1 − 0
Usingtheseparameters, Theorem2demonpstrates thatallN approximations a satisfy
i
a x = a xTv (cid:15) x v < µσ b
i i i i 2 i 2 1
| − | | − |≤ k k k k
6Theo(·)terms(8)and(10)demonstratethatthereexistssomeN 0suchthatforallN >N 0theupperandlowerboundsonkxk2
2
b b
eachholdwithprobabilitylowerboundedby1−1Nγ,resultinginaprobabilitylowerboundedby1−N−γ viatheunionbound.
4
Becausetheexpression(2)forthenumberofmeasurementsM isanorderterm,thecasewhereN ≤N 0isinconsequential.
22
Copyright (c) 2009 IEEE. Personal use is permitted. For any other purposes, Permission must be obtained from the IEEE by emailing pubs-permissions@ieee.org.
Authorized licensed use limited to: BEIJING UNIVERSITY OF POST AND TELECOM. Downloaded on December 9, 2009 at 20:44 from IEEE Xplore. Restrictions apply.


## 第 23 页

This article has been accepted for publication in a future issue of this journal, but has not been fully edited. Content may change prior to final publication.
withprobabilitylowerboundedby1 N γ. Combiningtheprobabilitythatthe` and` boundsholdand
− 2
− ∞
thedecoding probability offeredbyTheorem2,wehave
a x < µσ (20)
1
k − k∞
withprobability lowerboundedby1 2N γ.b
−
−
We complete the proof by computing the number of measurements M required (19). Because sQ2 =
K
2ln(SN1+γ)
= 2,weneed
ηln(SN1+γ) SN η
2
1+γ (1+γ) σ
M = O (1+2η 1) log(N) = O N(1+2η 1) 2S +(1 S) 0 log(N)
− −
(cid:15)2 µ2 − σ
(cid:18) (cid:19) " (cid:18) 1(cid:19) # !
measurements. (cid:3)
ACKNOWLEDGMENTS
Thanks to DavidScott, DannySorensen, YinZhang, MarcoDuarte, Michael Wakin, Mark Davenport,
JasonLaska,MatthewMoravec,ElaineHale,ChristineKelley,andIngmarLandforinformativeandinspir-
ingconversations. ThankstoPhilSchniterforbringinghisrelatedwork[27]toourattention. Specialthanks
toRameshNeelamani,Alexandre deBaynast, andPredragRadosavljevic forproviding helpful suggestions
forimplementingBP;toDannyBicksonandHarelAvissarforimprovingourimplementation;andtoMarco
Duarte for wizardry withthe figures. Additionally, the firstauthor thanks the Department ofElectrical En-
gineering at the Technion for generous hospitality while parts of the work were being performed, and in
particular the support of Yitzhak Birk and Tsachy Weissman. Final thanks to the anonymous reviewers,
whosesuperbcommentshelpedtogreatlyimprovethequalityofthepaper.
REFERENCES
[1] S. Sarvotham, D. Baron, and R. G. Baraniuk, “Compressed sensing reconstruction via belief propagation,” Tech. Rep.
TREE0601,RiceUniversity,Houston,TX,July2006.
[2] R.A.DeVore,B.Jawerth,andB.J.Lucier,“Imagecompressionthroughwavelettransformcoding,”IEEETrans.Inf.Theory,
vol.38,no.2,pp.719–746,Mar.1992.
[3] I.F.GorodnitskyandB.D.Rao, “SparsesignalreconstructionfromlimiteddatausingFOCUSS:Are-weightedminimum
normalgorithm,” IEEETrans.SignalProcess.,vol.45,no.3,pp.600–616,March1997.
[4] E. Cande`s, J. Romberg, and T. Tao, “Robust uncertainty principles: Exact signal reconstruction from highly incomplete
frequencyinformation,” IEEETrans.Inf.Theory,vol.52,no.2,pp.489–509,Feb.2006.
[5] D.Donoho, “Compressedsensing,” IEEETrans.Inf.Theory,vol.52,no.4,pp.1289–1306,Apr.2006.
[6] R.G.Baraniuk, “Alectureoncompressivesensing,” IEEESignalProcessMag.,vol.24,no.4,pp.118–121,2007.
23
Copyright (c) 2009 IEEE. Personal use is permitted. For any other purposes, Permission must be obtained from the IEEE by emailing pubs-permissions@ieee.org.
Authorized licensed use limited to: BEIJING UNIVERSITY OF POST AND TELECOM. Downloaded on December 9, 2009 at 20:44 from IEEE Xplore. Restrictions apply.


## 第 24 页

This article has been accepted for publication in a future issue of this journal, but has not been fully edited. Content may change prior to final publication.
[7] E.Cande`s, M.Rudelson, T.Tao, andR.Vershynin, “Errorcorrectionvialinearprogramming,” Found. Comp.Math., pp.
295–308,2005.
[8] S.Chen, D.Donoho, andM.Saunders, “Atomicdecompositionbybasispursuit,” SIAMJ.Sci.Comp., vol.20, no.1, pp.
33–61,1998.
[9] D. Donoho and J. Tanner, “Neighborliness of randomly projected simplices in high dimensions,” Proc. Nat. Academy
Sciences,vol.102,no.27,pp.9452–457,2005.
[10] D. Donoho, “High-dimensional centrally symmetric polytopes with neighborliness proportional to dimension,” Discrete
Comput.Geometry,vol.35,no.4,pp.617–652,Mar.2006.
[11] P.M.Vaidya, “AnalgorithmforlinearprogrammingwhichrequiresO(((m+n)n2+(m+n)1.5n)L) arithmeticoperations,” in
STOC’87:Proc.19thACMSymp.Theoryofcomputing,NewYork,NY,USA,1987,pp.29–38,ACM.
[12] J.A.TroppandA.C.Gilbert, “Signalrecoveryfromrandommeasurementsviaorthogonalmatchingpursuit,” IEEETrans.
Inf.Theory,vol.53,no.12,pp.4655–4666,Dec.2007.
[13] A.Cohen, W.Dahmen,andR.A.DeVore, “Nearoptimalapproximationofarbitraryvectorsfromhighlyincompletemea-
surements,” 2007, Preprint.
[14] M.F.Duarte,M.B.Wakin,andR.G.Baraniuk, “Fastreconstructionofpiecewisesmoothsignalsfromrandomprojections,”
inProc.SPARS05,Rennes,France,Nov.2005.
[15] D.L.Donoho,Y.Tsaig,I.Drori,andJ-CStarck, “Sparsesolutionofunderdeterminedlinearequationsbystagewiseorthog-
onalmatchingpursuit,” Mar.2006, Preprint.
[16] D.NeedellandJ.A.Tropp, “CoSaMP:Iterativesignalrecoveryfromincompleteandinaccuratesamples,” Appl.Comput.
HarmonicAnalysis,vol.26,no.3,pp.301–321,2008.
[17] T.BlumensathandM.E.Davies,“Iterativehardthresholdingforcompressedsensing,”toappearinAppl.Comput.Harmonic
Analysis,2008.
[18] W.DaiandO.Milenkovic, “Subspacepursuitforcompressivesensing: Closingthegapbetweenperformanceandcomplex-
ity,” IEEETrans.Inf.Theory,vol.55,no.5,pp.2230–2249,May2009.
[19] E. Hale, W. Yin, and Y. Zhang, “Fixed-point continuation for ` 1-minimization: Methodology and convergence,” 2007,
Submitted.
[20] M.Figueiredo,R.Nowak,andS.J.Wright,“Gradientprojectionforsparsereconstruction:Applicationtocompressedsensing
andotherinverseproblems,”Dec.2007, IEEEJ.Sel.Top.Sign.Proces.
[21] E.vandenBergandM. P.Friedlander, “ProbingtheParetofrontierforbasispursuit solutions,” Tech.Rep.TR-2008-01,
DepartmentofComputerScience,UniversityofBritishColumbia,Jan.2008, ToappearinSIAMJ.Sci.Comp.
[22] G.CormodeandS.Muthukrishnan, “Towardsanalgorithmictheoryofcompressedsensing,” DIMACSTechnicalReportTR
2005-25,2005.
[23] G. Cormode and S. Muthukrishnan, “Combinatorial algorithms for compressed sensing,” DIMACS Technical Report TR
2005-40,2005.
[24] A.C.Gilbert,M.J.Strauss,J.Tropp,andR.Vershynin, “Algorithmiclineardimensionreductioninthe` 1normforsparse
vectors,” Apr.2006, Submitted.
[25] S.Ji,Y.Xue,andL.Carin, “Bayesiancompressivesensing,” IEEETrans.SignalProcess.,vol.56,no.6,pp.2346–2356,
June2008.
[26] M.W.SeegerandH.Nickisch, “CompressedsensingandBayesianexperimentaldesign,” inICML’08:Proc.25thInt.Conf.
Machinelearning,2008,pp.912–919.
24
Copyright (c) 2009 IEEE. Personal use is permitted. For any other purposes, Permission must be obtained from the IEEE by emailing pubs-permissions@ieee.org.
Authorized licensed use limited to: BEIJING UNIVERSITY OF POST AND TELECOM. Downloaded on December 9, 2009 at 20:44 from IEEE Xplore. Restrictions apply.


## 第 25 页

This article has been accepted for publication in a future issue of this journal, but has not been fully edited. Content may change prior to final publication.
[27] P.Schniter, L. C.Potter, and J. Ziniel, “Fast Bayesian matching pursuit: Model uncertainty and parameter estimation for
sparselinearmodels,” IEEETrans.SignalProcess.,March2009.
[28] T.Hastie,R.Tibshirani,andJ.H.Friedman, TheElementsofStatisticalLearning, Springer,August2001.
[29] G.GuoandC.-C.Wang, “MultiuserdetectionofsparselyspreadCDMA,” IEEEJ.Sel.AreasCommun.,vol.26,no.3,pp.
421–431,2008.
[30] J.Pearl, “Probablisticreasoninginintelligentsystems:Networksofplausibleinference,” Morgan-Kaufmann,1988.
[31] F.V.Jensen, “AnintroductiontoBayesiannetworks,” Springer-Verlag,1996.
[32] B.J.Frey, “Graphicalmodelsformachinelearninganddigitalcommunication,” MITpress,1998.
[33] J.S.Yedidia,W.T.Freeman,andY.Weiss,“Understandingbeliefpropagationanditsgeneralizations,”MitsubishiTech.Rep.
TR2001-022,Jan.2002.
[34] D.J.C.MacKay, “Informationtheory,inferenceandlearningalgorithms,” CambridgeUniversityPress,2002.
[35] R.G.Cowell,A.P.Dawid,S.L.Lauritzen,andD.J.Spiegelhalter, “Probabilisticnetworksandexpertsystems,” Springer-
Verlag,2003.
[36] N.Sommer,M.Feder,andO.Shalvi, “Low-densitylatticecodes,” IEEETrans.Inf.Theory,vol.54,no.4,pp.1561–1585,
2008.
[37] R.G.Gallager, “Low-densityparity-checkcodes,” IEEETrans.Inf.Theory,vol.8,pp.21–28,Jan.1962.
[38] T.J.Richardson,M.A.Shokrollahi,andR.L.Urbanke, “Designofcapacity-approachingirregularlow-densityparity-check
codes,” IEEETrans.Inf.Theory,vol.47,pp.619–637,Feb.2001.
[39] S.Sarvotham,D.Baron,andR.G.Baraniuk, “Sudocodes–Fastmeasurementandreconstructionofsparsesignals,” inProc.
Int.Symp.Inf.Theory(ISIT2006),Seattle,WA,July2006.
[40] R.BerindeandP.Indyk,“Sparserecoveryusingsparserandommatrices,”MIT-CSAIL-TR-2008-001,2008,TechnicalReport.
[41] J.-CPesquet,H.Krim,andE.Hamman,“Bayesianapproachtobestbasisselection,”IEEE1996Int.Conf.Acoustics,Speech,
SignalProcess.(ICASSP),pp.2634–2637,1996.
[42] H.Chipman,E.Kolaczyk,andR.McCulloch, “AdaptiveBayesianwaveletshrinkage,” J.Amer.Stat.Assoc.,vol.92,1997.
[43] M.S.Crouse, R.D.Nowak, andR.G.Baraniuk, “Wavelet-basedsignalprocessing usinghidden Markovmodels,” IEEE
Trans.SignalProcess.,vol.46,pp.886–902,April1998.
[44] E.I.GeorgeandR.E.McCulloch, “VariableselectionviaGibbssampling,” J.Am.Stat.Assoc.,vol.88,pp.881–889,1993.
[45] J.Geweke, “Variableselectionandmodelcomparisoninregression,” inBayesianStatistics5,1996,pp.609–620.
[46] L.HeandL.Carin, “Exploitingstructureinwavelet-basedBayesiancompressedsensing,” toappearinIEEETrans.Signal
Process.,2008.
[47] H.W.SorensonandD.L.Alspach, “RecursiveBayesianestimationusingGaussiansums,” Automatica,vol.7,pp.465–479,
1971.
[48] J.A.Tropp,“Greedisgood:Algorithmicresultsforsparseapproximation,” IEEETrans.Inf.Theory,vol.50,pp.2231–2242,
2004.
[49] W.Wang, M.Garofalakis, andK.Ramchandran, “Distributedsparse randomprojections for refinableapproximation,” in
Proc.Inf.Process.SensorNetworks(IPSN2007),2007,pp.331–339.
[50] G.Cooper, “ThecomputationalcomplexityofprobabilisticinferenceusingBayesianbeliefnetworks,”ArtificialIntelligence,
vol.42,pp.393–405,1990.
[51] F.R.Kschischang,B.J.Frey,andH-A.Loeliger, “Factorgraphsandthesum-productalgorithm,” IEEETrans.Inf.Theory,
vol.47,no.2,pp.498–519,Feb.2001.
25
Copyright (c) 2009 IEEE. Personal use is permitted. For any other purposes, Permission must be obtained from the IEEE by emailing pubs-permissions@ieee.org.
Authorized licensed use limited to: BEIJING UNIVERSITY OF POST AND TELECOM. Downloaded on December 9, 2009 at 20:44 from IEEE Xplore. Restrictions apply.


## 第 26 页

This article has been accepted for publication in a future issue of this journal, but has not been fully edited. Content may change prior to final publication.
[52] E.Sudderth,A.Ihler,W.Freeman,andA.S.Willsky, “Nonparametricbeliefpropagation,” MITLIDSTech.Rep.2551,Oct.
2002.
[53] B.J.FreyandD.J.C.MacKay, “Arevolution:Beliefpropagationingraphswithcycles,” Adv.NeuralInf.Process.Systems,
M.Jordan,M.S.KearnsandS.A.Solla(Eds.),vol.10,1998.
[54] A.Ihler,J.Fisher,andA.S.Willsky, “Loopybeliefpropagation: Convergenceandeffectsofmessageerrors,” J.Machine
LearningRes.,vol.6,pp.905–936,May2005.
[55] M.Pretti, “AMessage-PassingAlgorithmwithDamping,” J.Stat.Mech.,Nov.2005.
[56] D.J.C.MacKay,“Gooderror-correctingcodesbasedonverysparsematrices,”IEEETrans.Inf.Theory,vol.45,pp.399–431,
Mar.1999.
[57] D.W.ScottandW.F.Szewczyk, “Fromkernelstomixtures,” Technometrics,vol.43,pp.323–335,Aug.2001.
[58] R.G.Baraniuk,V.Cevher,M.F.Duarte,andC.Hegde, “Model-basedcompressivesensing,” 2008, Preprint.
[59] J.W.Byers,M.Luby,andM.Mitzenmacher, “Adigitalfountainapproachtoasynchronousreliablemulticast,” IEEEJ.Sel.
AreasCommun.,vol.20,no.8,pp.1528–1540,Oct.2002.
Dror Baron received the B.Sc. (summa cum laude) and M.Sc. degrees from the Technion - Israel
InstituteofTechnology,Haifa,Israel,in1997and1999,andthePh.D.degreefromtheUniversityofIllinois
atUrbana-Champaign in2003,allinelectrical engineering.
From1997to1999,heworkedatWitcomLtd. inmodemdesign. From1999to2003,hewasaresearch
assistantattheUniversityofIllinoisatUrbana-Champaign,wherehewasalsoaVisitingAssistantProfessor
in2003. From2003to2006,hewasaPostdoctoral ResearchAssociate intheDepartmentofElectrical and
ComputerEngineeringatRiceUniversity,Houston,TX.From2007to2008,hewasaquantitative financial
analystwithMentaCapital,SanFrancisco,CA.Since2008hehasbeenavisitingscientistintheDepartment
ofElectrical Engineering atTechnion-IsraelInstitute ofTechnology, Haifa.
Dr. Baron’s research interests include information theory and signal processing. Dr. Baron was a
recipient of the 2002 M. E. Van Valkenburg Graduate Research Award, and received honorable mention
at the Robert Bohrer Memorial Student Workshop in April 2002, both at the University of Illinois. He
also participated from 1994 to 1997 in the Program for Outstanding Students, comprising the top 0.5% of
undergraduates attheTechnion.
ShriramSarvothamreceivedhisB.TechdegreefromIndianInstituteofTechnology,Madras,Indiaand
M.SandPh.D.degreesfrom RiceUniversity, Texas,allinElectricalEngineering. Hisresearch interests lie
inthebroadareasofCompressedSensing,non-asymptotic InformationTheoryandInternetTrafficanalysis
andmodeling. Currently, heworksasaPrincipal Research Scientist atHalliburton Energy Services, where
heinvestigates optimaldataacquisition andprocessing ofNMRdatainoilandgasexploration.
Richard G. Baraniuk received the BSc degree in 1987 from the University of Manitoba (Canada),
the MSc degree in 1988 from the University of Wisconsin-Madison, and the PhD degree in 1992 from the
26
Copyright (c) 2009 IEEE. Personal use is permitted. For any other purposes, Permission must be obtained from the IEEE by emailing pubs-permissions@ieee.org.
Authorized licensed use limited to: BEIJING UNIVERSITY OF POST AND TELECOM. Downloaded on December 9, 2009 at 20:44 from IEEE Xplore. Restrictions apply.


## 第 27 页

This article has been accepted for publication in a future issue of this journal, but has not been fully edited. Content may change prior to final publication.
University of Illinois at Urbana-Champaign, all inElectrical Engineering. After spending 1992–1993 with
theSignalProcessing LaboratoryofEcoleNormaleSupe´rieure, inLyon,France,hejoinedRiceUniversity,
where he is currently the Victor E. Cameron Professor of Electrical and Computer Engineering. He spent
sabbaticalsatEcoleNationaleSupe´rieuredeTe´le´communicationsinParisin2001andEcoleFe´de´ralePoly-
technique de Lausanne in Switzerland in 2002. His research interests lie in the area of signal and image
processing.
He has been a Guest Editor of several special issues of the IEEESignalProcessingMagazine, IEEE
JournalofSpecialTopicsinSignalProcessing, andtheProceedingsoftheIEEEandhasservedastechnical
program chairoronthetechnical program committeeforseveralIEEEworkshops andconferences.
In 1999, Dr. Baraniuk founded Connexions (cnx.org), a non-profit publishing project that invites au-
thors,educators,andlearnersworldwideto“create,rip,mix,andburn”freetextbooks,courses,andlearning
materialsfromaglobalopen-access repository.
Dr. Baraniuk received a NATO postdoctoral fellowship from NSERC in 1992, the National Young
Investigator award from the National Science Foundation in 1994, a Young Investigator Award from the
OfficeofNavalResearchin1995,theRosenbaumFellowshipfromtheIsaacNewtonInstituteofCambridge
Universityin1998,theC.HolmesMacDonaldNationalOutstandingTeachingAwardfromEtaKappaNuin
1999, theCharles Duncan Junior Faculty Achievement Awardfrom Ricein2000, theUniversity ofIllinois
ECE Young Alumni Achievement Award in 2000, the George R. Brown Award for Superior Teaching at
Ricein2001,2003,and2006,theHershelM.RichInventionAwardfromRicein2007,theWaveletPioneer
AwardfromSPIEin2008,andtheInternetPioneerAwardfromtheBerkmanCenterforInternetandSociety
at Harvard Law School in 2008. He was selected as one of Edutopia Magazine’s Daring Dozen educators
in 2007. Connexions received the Tech Museum Laureate Award from the Tech Museum of Innovation
in 2006. His work with Kevin Kelly on the Rice single-pixel compressive camera was selected by MIT
Technology Review Magazine as a TR10 Top 10 Emerging Technology in 2007. He was co-author on a
paper with Matthew Crouse and Robert Nowak that won the IEEE Signal Processing Society Junior Paper
Awardin2001andanotherwithVinayRibeiroandRolfRiedithatwonthePassiveandActiveMeasurement
(PAM) Workshop Best Student Paper Award in 2003. He was elected a Fellow of the IEEE in 2001 and a
PlusMemberofAAAin1986.
27
Copyright (c) 2009 IEEE. Personal use is permitted. For any other purposes, Permission must be obtained from the IEEE by emailing pubs-permissions@ieee.org.
Authorized licensed use limited to: BEIJING UNIVERSITY OF POST AND TELECOM. Downloaded on December 9, 2009 at 20:44 from IEEE Xplore. Restrictions apply.

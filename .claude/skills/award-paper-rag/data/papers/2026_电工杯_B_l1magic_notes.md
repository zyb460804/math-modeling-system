# l1magic_notes


## 第 1 页

-magic
‘ : Recovery of Sparse Signals
1
via Convex Programming
Emmanuel Cand`es and Justin Romberg, Caltech
October 2005
1 Seven problems
A recent series of papers [3–8] develops a theory of signal recovery from highly incomplete
information. The central results state that a sparse vector x ∈ RN can be recovered from a
0
small number of linear measurements b = Ax ∈ RK, K (cid:28) N (or b = Ax +e when there is
0 0
measurement noise) by solving a convex program.
As a companion to these papers, this package includes MATLAB code that implements this
recovery procedure in the seven contexts described below. The code is not meant to be cutting-
edge, ratheritis a proof-of-concept showing that these recovery procedures are computationally
tractable, even for large scale problems where the number of data points is in the millions.
The problems fall into two classes: those which can be recast as linear programs (LPs), and
those which can be recast as second-order cone programs (SOCPs). The LPs are solved using
a generic path-following primal-dual method. The SOCPs are solved with a generic log-barrier
algorithm. The implementations follow Chapter 11 of [2].
For maximum computational efficiency, the solvers for each of the seven problems are imple-
mented separately. They all have the same basic structure, however, with the computational
bottleneckbeingthecalculationoftheNewtonstep(thisisdiscussedindetailbelow). Thecode
can be used in either “small scale” mode, where the system is constructed explicitly and solved
exactly, or in “large scale” mode, where an iterative matrix-free algorithm such as conjugate
gradients (CG) is used to approximately solve the system.
Our seven problems of interest are:
• Min-‘ with equality constraints. The program
1
(P ) min kxk subject to Ax=b,
1 1
also known as basis pursuit, finds the vector with smallest ‘ norm
1
X
kxk := |x |
1 i
i
that explains the observations b. As the results in [4,6] show, if a sufficiently sparse x
0
existssuchthatAx =b, then(P )willfindit. Whenx,A,bhavereal-valuedentries, (P )
0 1 1
can be recast as an LP (this is discussed in detail in [10]).
• Minimum ‘ error approximation. Let A be a M ×N matrix with full rank. Given
1
y ∈RM, the program
(P ) min ky−Axk
A 1
x
1


## 第 2 页

finds the vector x ∈ RN such that the error y −Ax has minimum ‘ norm (i.e. we are
1
askingthatthedifferencebetweenAxandy besparse). Thisprogramarisesinthecontext
of channel coding [8].
Suppose we have a channel code that produces a codeword c = Ax for a message x. The
message travels over the channel, and has an unknown number of its entries corrupted.
The decoder observes y =c+e, where e is the corruption. If e is sparse enough, then the
decoder can use (P ) to recover x exactly. Again, (P ) can be recast as an LP.
A A
• Min-‘ with quadratic constraints. This program finds the vector with minimum ‘
1 1
norm that comes close to explaining the observations:
(P ) min kxk subject to kAx−bk ≤(cid:15),
2 1 2
where(cid:15)isauserspecifiedparameter. Asshownin[5],ifasufficientlysparsex existssuch
0
that b=Ax +e, for some small error term kek ≤(cid:15), then the solution x? to (P ) will be
0 2 2 2
close to x . That is, kx?−x k ≤ C ·(cid:15), where C is a small constant. (P ) can be recast
0 2 0 2 2
as a SOCP.
• Min-‘ with bounded residual correlation. Also referred to as the Dantzig Selector,
1
the program
(P ) min kxk subject to kA∗(Ax−b)k ≤γ,
D 1 ∞
whereγ isauserspecifiedparameter, relaxestheequalityconstraintsof(P )inadifferent
1
way. (P ) requires that the residual Ax−b of a candidate vector x not be too correlated
D
withanyofthecolumnsofA(theproductA∗(Ax−b)measureseachofthesecorrelations).
Ifb=Ax +e,wheree ∼N(0,σ2),thenthesolutionx? to(P )hasnear-optimalminimax
0 i D D
risk:
X
Ekx? −x k2 ≤C(logN)· min(x (i)2,σ2),
D 0 2 0
i
(see [7] for details). For real-valued x,A,b, (P ) can again be recast as an LP; in the
D
complex case, there is an equivalent SOCP.
It is also true that when x,A,b are complex, the programs (P ),(P ),(P ) can be written as
1 A D
SOCPs, but we will not pursue this here.
If the underlying signal is a 2D image, an alternate recovery model is that the gradient is
sparse[18]. Letx denotethepixelintheithrowandj columnofann×nimagex, anddefine
ij
the operators
( (
x −x i<n x −x j <n
D x= i+1,j ij D x= i,j+1 ij ,
h;ij v;ij
0 i=n 0 j =n
and
(cid:18) (cid:19)
D x
D x= h;ij . (1)
ij D x
v;ij
The 2-vector D x can be interpreted as a kind of discrete gradient of the digital image x. The
ij
total variation of x is simply the sum of the magnitudes of this discrete gradient at every point:
Xq X
TV(x):= (D x)2+(D x)2 = kD xk .
h;ij v;ij ij 2
ij ij
With these definitions, we have three programs for image recovery, each of which can be recast
as a SOCP:
2


## 第 3 页

• Min-TV with equality constraints.
(TV ) min TV(x) subject to Ax=b
1
If there exists a piecewise constant x with sufficiently few edges (i.e. D x is nonzero for
0 ij 0
only a small number of indices ij), then (TV ) will recover x exactly — see [4].
1 0
• Min-TV with quadratic constraints.
(TV ) min TV(x) subject to kAx−bk ≤(cid:15)
2 2
Examples of recovering images from noisy observations using (TV ) were presented in [5].
2
Note that if A is the identity matrix, (TV ) reduces to the standard Rudin-Osher-Fatemi
2
image restoration problem [18]. See also [9,11–13] for SOCP solvers specifically designed
for the total-variational functional.
• Dantzig TV.
(TV ) min TV(x) subject to kA∗(Ax−b)k ≤γ
D ∞
This program was used in one of the numerical experiments in [7].
Inthenextsection,wedescribehowtosolvelinearandsecond-orderconeprogramsusingmodern
interior point methods.
2 Interior point methods
Advances in interior point methods for convex optimization over the past 15 years, led by the
seminalwork[14],havemadelarge-scalesolversforthesevenproblemsabovefeasible. Belowwe
overviewthegenericLPandSOCPsolversusedinthe‘ -magicpackagetosolvetheseproblems.
1
2.1 A primal-dual algorithm for linear programming
In Chapter 11 of [2], Boyd and Vandenberghe outline a relatively simple primal-dual algorithm
forlinearprogrammingwhichwehavefollowedverycloselyfortheimplementationof(P ),(P ),
1 A
and (P ). For the sake of completeness, and to set up the notation, we briefly review their
D
algorithm here.
The standard-form linear program is
min hc ,zi subject to A z =b,
0 0
z
f (z)≤0,
i
wherethesearchvectorz ∈RN, b∈RK, A isaK×N matrix, andeachofthef , i=1,...,m
0 i
is a linear functional:
f (z)=hc ,zi+d ,
i i i
for some c ∈ RN, d ∈ R. At the optimal point z?, there will exist dual vectors ν? ∈ RK,λ? ∈
i i
Rm,λ? ≥0 such that the Karush-Kuhn-Tucker conditions are satisfied:
X
(KKT) c +ATν?+ λ?c =0,
0 0 i i
i
λ?f (z?)=0, i=1,...,m,
i i
A z? =b,
0
f (z?)≤0, i=1,...,m.
i
3


## 第 4 页

In a nutshell, the primal dual algorithm finds the optimal z? (along with optimal dual vectors
ν? andλ?)bysolvingthissystemofnonlinearequations. Thesolutionprocedureistheclassical
Newton method: at an interior point (zk,νk,λk) (by which we mean f (zk) < 0, λk > 0), the
i
system is linearized and solved. However, the step to new point (zk+1,νk+1,λk+1) must be
modified so that we remain in the interior.
In practice, we relax the complementary slackness condition λ f =0 to
i i
λkf (zk)=−1/τk, (2)
i i
where we judiciously increase the parameter τk as we progress through the Newton iterations.
Thisbiasesthesolutionofthelinearizedequationstowardstheinterior,allowingasmooth,well-
defined “central path” from an interior point to the solution on the boundary (see [15,20] for an
extended discussion).
Theprimal,dual,andcentralresidualsquantifyhowcloseapoint(z,ν,λ)istosatisfying(KKT)
with (2) in place of the slackness condition:
X
r = c +ATν+ λ c
dual 0 0 i i
i
r = −Λf −(1/τ)1
cent
r = A z−b,
pri 0
(cid:0) (cid:1)T
where Λ is a diagonal matrix with (Λ) =λ , and f = f (z) ... f (z) .
ii i 1 m
From a point (z,ν,λ), we want to find a step (∆z,∆ν,∆λ) such that
r (z+∆z,ν+∆ν,λ+∆λ)=0. (3)
τ
Linearizing (3) with the Taylor expansion around (z,ν,λ),
 
∆z
r
τ
(z+∆z,ν+∆ν,λ+∆λ)≈r
τ
(z,ν,λ)+J
rτ
(z,νλ)∆ν,
∆λ
where J (z,νλ) is the Jacobian of r , we have the system
rτ τ
 0 AT CT ∆z   c +ATν+ P λ c 
0 0 0 i i i
−ΛC 0 −F∆v=− −Λf −(1/τ)1 ,
A 0 0 ∆λ A z−b
0 0
where m×N matrix C has the cT as rows, and F is diagonal with (F) = f (z). We can
i ii i
eliminate ∆λ using:
∆λ=−ΛF−1C∆z−λ−(1/τ)f−1 (4)
leaving us with the core system
(cid:18) −CTF−1ΛC AT(cid:19)(cid:18) ∆z (cid:19) (cid:18) −c +(1/τ)CTf−1−ATν (cid:19)
0 = 0 0 . (5)
A 0 ∆ν b−A z
0 0
With the (∆z,∆ν,∆λ) we have a step direction. To choose the step length 0 < s ≤ 1, we ask
that it satisfy two criteria:
1. z+s∆z and λ+s∆λ are in the interior, i.e. f (z+s∆z)<0, λ >0 for all i.
i i
2. The norm of the residuals has decreased sufficiently:
kr (z+s∆z,ν+s∆ν,λ+s∆λ)k ≤(1−αs)·kr (z,ν,λ)k ,
τ 2 τ 2
whereαisauser-sprecifiedparameter(inallofourimplementations,wehavesetα=0.01).
4


## 第 5 页

Since the f are linear functionals, item 1 is easily addressed. We choose the maximum step size
i
that just keeps us in the interior. Let
I+ ={i:hc ,∆zi>0}, I−{i:∆λ<0},
f i λ
and set
s =0.99·min{1, {−f (z)/hc ,∆zi, i∈I+}, {−λ /∆λ , i∈I−}}.
max i i f i i λ
Then starting with s = s , we check if item 2 above is satisfied; if not, we set s0 = β·s and
max
try again. We have taken β =1/2 in all of our implementations.
When r and r are small, the surrogate duality gap η =−fTλ is an approximation to how
dual pri
closeacertain(z,ν,λ)istobeingopitmal(i.e.hc ,zi−hc ,z?i≈η). Theprimal-dualalgorithm
0 0
repeats the Newton iterations described above until η has decreased below a given tolerance.
Almost all of the computational burden falls on solving (5). When the matrix −CTF−1ΛC is
easily invertible (as it is for (P )), or there are no equality constraints (as in (P ),(P )), (5)
1 A D
can be reduced to a symmetric positive definite set of equations.
When N and K are large, forming the matrix and then solving the linear system of equations
in (5) is infeasible. However, if fast algorithms exist for applying C,CT and A ,AT, we can use
0 0
a “matrix free” solver such as Conjugate Gradients. CG is iterative, requiring a few hundred
applications of the constraint matrices (roughly speaking) to get an accurate solution. A CG
solver (based on the very nice exposition in [19]) is included with the ‘ -magic package.
1
The implementations of (P ),(P ),(P ) are nearly identical, save for the calculation of the
1 A D
Newton step. In the Appendix, we derive the Newton step for each of these problems using
notation mirroring that used in the actual MATLAB code.
2.2 A log-barrier algorithm for SOCPs
Although primal-dual techniques exist for solving second-order cone programs (see [1,13]), their
implementationisnotquiteasstraightforwardas inthe LPcase. Instead, wehaveimplemented
each of the SOCP recovery problems using a log-barrier method. The log-barrier method, for
which we will again closely follow the generic (but effective) algorithm described in [2, Chap.
11], is conceptually more straightforward than the primal-dual method described above, but at
its core is again solving for a series of Newton steps.
Each of (P ),(TV ),(TV ),(TV ) can be written in the form
2 1 2 D
min hc ,zi subject to A z =b
0 0
z
f (z)≤0, i=1,...,m (6)
i
where each f describes either a constraint which is linear
i
f =hc ,zi+d
i i i
or second-order conic
f (z)= 1(cid:0) kA zk2−(hc ,zi+d )2(cid:1)
i 2 i 2 i i
(the A are matrices, the c are vectors, and the d are scalars).
i i i
The standard log-barrier method transforms (6) into a series of linearly constrained programs:
1 X
min hc ,zi+ −log(−f (z)) subject to A z =b, (7)
z 0 τk i 0
i
5


## 第 6 页

where τk > τk−1. The inequality constraints have been incorporated into the functional via a
penalty function1 which is infinite when the constraint is violated (or even met exactly), and
smooth elsewhere. As τk gets large, the solution zk to (7) approaches the solution z? to (6): it
can be shown that hc ,zki−hc ,z?i<m/τk, i.e. we are within m/τk of the optimal value after
0 0
iterationk(m/τk iscalledthedualitygap). Theideahereisthateachofthesmoothsubproblems
can be solved to fairly high accuracy with just a few iterations of Newton’s method, especially
since we can use the solution zk as a starting point for subproblem k+1.
Atlog-barrieriterationk,Newton’smethod(whichisagainiterative)proceedsbyformingaseries
ofquadraticapproximationsto(7),andminimizingeachbysolvingasystemofequations(again,
we might need to modify the step length to stay in the interior). The quadratic approximation
of the functional
1 X
f (z)=hc ,zi+ −log(−f (z))
0 0 τ i
i
in (7) around a point z is given by
1
f (z+∆z) ≈ z+hg ,∆zi+ hH ∆z,∆zi := q(z+∆z),
0 z 2 z
where g is the gradient
z
1 X 1
g =c + ∇f (z)
z 0 τ −f (z) i
i
i
and H is the Hessian matrix
z
1 X 1 1 X 1
H = ∇f (z)(∇f (z))T + ∇2f (z).
z τ f (z)2 i i τ −f (z) i
i i
i i
Given that z is feasible (that A z =b, in particular), the ∆z that minimizes q(z+∆z) subject
0
to A z =b is the solution to the set of linear equations
0
(cid:18)
H
AT(cid:19)(cid:18)
∆z
(cid:19)
τ z 0 =−τg . (8)
A 0 v z
0
(The vector v, which can be interpreted as the Lagrange multipliers for the quality constraints
in the quadratic minimization problem, is not directly used.)
In all of the recovery problems below with the exception of (TV ), there are no equality con-
1
straints (A =0). In these cases, the system (8) is symmetric positive definite, and thus can be
0
solvedusingCGwhentheproblemis“largescale”. Forthe(TV )problem,weusetheSYMMLQ
1
algorithm (which is similar to CG, and works on symmetric but indefinite systems, see [16]).
With ∆z in hand, we have the Newton step direction. The step length s≤1 is chosen so that
1. f (z+s∆z)<0 for all i=1,...,m,
i
2. The functional has decreased suffiently:
f (z+s∆z)<f (z)+αs∆zhg ,∆zi,
0 0 z
where α is a user-specified parameter (each of the implementations below uses α=0.01).
This requirement basically states that the decrease must be within a certain percentage of
that predicted by the linear model at z.
As before, we start with s = 1, and decrease by multiples of β until both these conditions are
satisfied (all implementations use β =1/2).
The complete log-barrier implementation for each problem follows the outline:
1Thechoiceof−log(−x)forthebarrierfunctionisnotarbitrary,ithasaproperty(termedself-concordance)
that is very important for quick convergence of (7) to (6) both in theory and in practice (see the very nice
expositionin[17]).
6


## 第 7 页

1. Inputs: a feasible starting point z0, a tolerance η, and parameters µ and an initial τ1. Set
k =1.
2. Solve (7) via Newton’s method (followed by the backtracking line search), using zk−1 as
an initial point. Call the solution zk.
3. If m/τk <η, terminate and return zk.
4. Else, set τk+1 =µτk, k =k+1 and go to step 2.
In fact, we can calculate in advance how many iterations the log-barrier algorithm will need:
(cid:24) logm−logη−logτ1(cid:25)
barrier iterations= .
logµ
The final issue is the selection of τ1. Our implementation chooses τ1 conservatively; it is set so
that the duality gap m/τ1 after the first iteration is equal to hc ,z0i.
0
InAppendix,weexplicitlyderivetheequationsfortheNewtonstepforeachof(P ),(TV ),(TV ),(TV ),
2 1 2 D
again using notation that mirrors the variable names in the code.
3 Examples
To illustrate how to use the code, the ‘ -magic package includes m-files for solving specific
1
instances of each of the above problems (these end in “ example.m” in the main directory).
3.1 ‘ with equality constraints
1
We will begin by going through l1eq example.m in detail. This m-file creates a sparse signal,
takesalimitednumberofmeasurementsofthatsignal,andrecoversthesignalexactlybysolving
(P ). The first part of the procedure is for the most part self-explainatory:
1
% put key subdirectories in path if not already there
path(path, ’./Optimization’);
path(path, ’./Data’);
% load random states for repeatable experiments
load RandomStates
rand(’state’, rand_state);
randn(’state’, randn_state);
% signal length
N = 512;
% number of spikes in the signal
T = 20;
% number of observations to make
K = 120;
% random +/- 1 signal
x = zeros(N,1);
q = randperm(N);
x(q(1:T)) = sign(randn(T,1));
7


## 第 8 页

We add the ’Optimization’ directory (where the interior point solvers reside) and the ’Data’
directories to the path. The file RandomStates.m contains two variables: rand state and
randn state, which we use to set the states of the random number generators on the next
two lines (we want this to be a “repeatable experiment”). The next few lines set up the prob-
lem: a length 512 signal that contains 20 spikes is created by choosing 20 locations at random
and then putting ±1 at these locations. The original signal is shown in Figure 1(a). The next
few lines:
% measurement matrix
disp(’Creating measurment matrix...’);
A = randn(K,N);
A = orth(A’)’;
disp(’Done.’);
% observations
y = A*x;
% initial guess = min energy
x0 = A’*y;
create a measurement ensemble by first creating a K ×N matrix with iid Gaussian entries,
and then orthogonalizing the rows. The measurements y are taken, and the “minimum energy”
solution x0 is calculated (x0, which is shown in Figure 1 is the vector in {x : Ax = y} that is
closest to the origin). Finally, we recover the signal with:
% solve the LP
tic
xp = l1eq_pd(x0, A, [], y, 1e-3);
toc
The function l1eq pd.m (found in the ’Optimization’ subdirectory) implements the primal-dual
algorithm presented in Section 2.1; we are sending it our initial guess x0 for the solution, the
measurementmatrix(thethirdargument,whichisusedtospecifythetransposeofthemeasure-
mentmatrix,isunnecessaryhere—andhenceleftempty—sinceweareprovidingAexplicitly),
the measurements, and the precision to which we want the problem solved (l1eq pd will termi-
nate when the surrogate duality gap is below 10−3). Running the example file at the MATLAB
prompt, we have the following output:
>>l1eq_example
Creatingmeasurmentmatrix...
Done.
Iteration=1,tau=1.921e+02,Primal=5.272e+01,PDGap=5.329e+01,Dualres=9.898e+00,Primalres=1.466e-14
H11pconditionnumber=1.122e-02
Iteration=2,tau=3.311e+02,Primal=4.383e+01,PDGap=3.093e+01,Dualres=5.009e+00,Primalres=7.432e-15
H11pconditionnumber=2.071e-02
Iteration=3,tau=5.271e+02,Primal=3.690e+01,PDGap=1.943e+01,Dualres=2.862e+00,Primalres=1.820e-14
H11pconditionnumber=2.574e-04
Iteration=4,tau=7.488e+02,Primal=3.272e+01,PDGap=1.368e+01,Dualres=1.902e+00,Primalres=1.524e-14
H11pconditionnumber=8.140e-05
Iteration=5,tau=9.731e+02,Primal=2.999e+01,PDGap=1.052e+01,Dualres=1.409e+00,Primalres=1.380e-14
H11pconditionnumber=5.671e-05
Iteration=6,tau=1.965e+03,Primal=2.509e+01,PDGap=5.210e+00,Dualres=6.020e-01,Primalres=4.071e-14
H11pconditionnumber=2.054e-05
Iteration=7,tau=1.583e+04,Primal=2.064e+01,PDGap=6.467e-01,Dualres=6.020e-03,Primalres=3.126e-13
H11pconditionnumber=1.333e-06
Iteration=8,tau=1.450e+05,Primal=2.007e+01,PDGap=7.062e-02,Dualres=6.020e-05,Primalres=4.711e-13
H11pconditionnumber=1.187e-07
Iteration=9,tau=1.330e+06,Primal=2.001e+01,PDGap=7.697e-03,Dualres=6.020e-07,Primalres=2.907e-12
H11pconditionnumber=3.130e-09
Iteration=10,tau=1.220e+07,Primal=2.000e+01,PDGap=8.390e-04,Dualres=6.020e-09,Primalres=1.947e-11
H11pconditionnumber=3.979e-11
Elapsedtimeis0.141270seconds.
The recovered signal xp is shown in Figure 1(c). The signal is recovered to fairly high accuracy:
>> norm(xp-x)
8


## 第 9 页

0.4
1 1
0.8 0.3 0.8
0.6 0.6
0.2
0.4 0.4
0.2 0.1 0.2
0 0 0
−0.2 −0.2
−0.1
−0.4 −0.4
−0.6 −0.2 −0.6
−0.8 −0.3 −0.8
−1 −1
0 50 100 150 200 250 300 350 400 450 500 −0.40 50 100 150 200 250 300 350 400 450 500 0 50 100 150 200 250 300 350 400 450 500
(a) Original (b) Minimum energy reconstruction (c) Recovered
Figure 1: 1D recovery experiment for ‘ minimization with equality constraints. (a) Original length
1
512 signal x consisting of 20 spikes. (b) Minimum energy (linear) reconstruction x0. (c) Minimum ‘
1
reconstruction xp.
ans =
8.9647e-05
3.2 Phantom reconstruction
A large scale example is given in tveq phantom example.m. This files recreates the phantom
reconstructionexperimentfirstpublishedin[4]. The256×256Shepp-Loganphantom, shownin
Figure 2(a), is measured at K =5481 locations in the 2D Fourier plane; the sampling pattern is
shown in Figure 2(b). The image is then reconstructed exactly using (TV ).
1
The star-shaped Fourier-domain sampling pattern is created with
% number of radial lines in the Fourier domain
L = 22;
% Fourier samples we are given
[M,Mh,mh,mhi] = LineMask(L,n);
OMEGA = mhi;
TheauxiliaryfunctionLineMask.m(foundinthe‘Measurements’subdirectory)createsthestar-
shapedpatternconsistingof22linesthroughtheorigin. ThevectorOMEGAcontainsthelocations
of the frequencies used in the sampling pattern.
This example differs from the previous one in that the code operates in large-scale mode. The
measurement matrix in this example is 5481×65536, making the system (8) far too large to
solve (or even store) explicitly. (In fact, the measurment matrix itself would require almost 3
gigabytes of memory if stored in double precision.) Instead of creating the measurement matrix
explicitly, we provide function handles that take a vector x, and return Ax. As discussed above,
the Newton steps are solved for using an implicit algorithm.
To create the implicit matrix, we use the function handles
A = @(z) A_fhp(z, OMEGA);
At = @(z) At_fhp(z, OMEGA, n);
9


## 第 10 页

(a) Phantom (b) Sampling pattern (c) Min energy (d) min-TV reconstruction
Figure 2: Phantom recovery experiment.
The function A fhp.m takes a length N vector (we treat n×n images as N :=n2 vectors), and
returns samples on the K frequencies. (Actually, since the underlying image is real, A fhp.m
returntherealandimaginarypartsofthe2DFFTontheupperhalf-planeofthedomainshown
in Figure 2(b).)
To solve (TV ), we call
1
xp = tveq_logbarrier(xbp, A, At, y, 1e-1, 2, 1e-8, 600);
The variable xbp is the initial guess (which is again the minimal energy reconstruction shown
in Figure 2(c)), y are the measurements, and1e-1 is the desired precision. The sixth input is
the value of µ (the amount by which to increase τk at each iteration; see Section 2.2). The last
two inputs are parameters for the large-scale solver used to find the Newton step. The solvers
are iterative, with each iteration requiring one application of A and one application of At. The
seventh and eighth arguments above state that we want the solver to iterate until the solution
has precision 10−8 (that is, it finds a z such that kHz−gk /kgk ≤10−8), or it has reached 600
2 2
iterations.
The recovered phantom is shown in Figure 2(d). We have kX −Xk /kXk ≈8·10−3.
TV 2 2
3.3 Optimization routines
Weincludeabriefdescriptionofeachofthemainoptimizationroutines(typehelp <function>
in MATLAB for details). Each of these m-files is found in the Optimization subdirectory.
10


## 第 11 页

Solves Ax = b, where A is symmetric positive definite, using the
cgsolve Conjugate Gradient method.
Solves (P ) (the Dantzig selector) using a primal-dual algorithm.
l1dantzig pd D
Solves the norm approximation problem (P ) (for decoding via
A
l1decode pd linear programming) using a primal-dual algorithm.
SolvesthestandardBasisPursuitproblem(P )usingaprimal-dual
1
l1eq pd algorithm.
Barrier (“outer”) iterations for solving quadratically constrained
l1qc logbarrier ‘ minimization (P ).
1 2
Newton (“inner”) iterations for solving quadratically constrained
l1qc newton ‘ minimization (P ).
1 2
Barrier iterations for solving the TV Dantzig selector (TV ).
tvdantzig logbarrier D
Newton iterations for (TV ).
tvdantzig newton D
BarrieriterationsforequalityconstrainedTVminimizaiton(TV ).
tveq logbarrier 1
Newton iterations for (TV ).
tveq newton 1
Barrier iterations for quadratically constrained TV minimization
tvqc logbarrier (TV ).
2
Newton iterations for (TV ).
tvqc newton 2
4 Error messages
Here we briefly discuss each of the error messages that the ‘ -magic may produce.
1
• Matrix ill-conditioned. Returning previous iterate. This error can occur when
the code is running in small-scale mode; that is, the matrix A is provided explicitly. The
errormessageisproducedwhentheconditionnumberofthelinearsystemweneedtosolve
to find the step direction (i.e. (5) for the linear programs, and (8) for the SOCPs) has an
estimated condition number of less than 10−14.
Thiserrormostcommonlyoccursduringthelastiterationsoftheprimal-dualorlog-barrier
algorithms. While it means that the solution is not within the tolerance specified (by the
primal-dual gap), in practice it is usually pretty close.
• Cannot solve system. Returning previous iterate. This error is the large-scale
analog to the above. The error message is produced when the residual produced by the
conjugategradientsalgorithmwasabove1/2;essentiallythismeansthatCGhasnotsolved
the system in any meaningful way. Again, this error typically occurs in the late stages of
the optimization algorithm, and is a symptom of the system being ill-conditioned.
• Stuck backtracking, returning last iterate. Thiserroroccurswhenthealgorithm,
aftercomputingthestepdirection, cannotfindastepsizesmallenoughthatdecreasesthe
objective. It is generally occurs in large-scale mode, and is a symptom of CG not solving
forthestepdirectiontosufficientprecision(ifthesystemissolvedperfectly,asmallenough
step size will always be found). Again, this will typically occur in the late stages of the
optimization algorithm.
• Starting point infeasible; using x0 = At*inv(AAt)*y. Each of the optimization
programs expects an initial guess which is feasible (obeys the constraints). If the x0
provided is not, this message is produced, and the algorithm proceeds using the least-
squares starting point x =AT(AAT)−1b.
0
11


## 第 12 页

Appendix
A ‘ minimization with equality constraints
1
When x, A and b are real, then (P ) can be recast as the linear program
1
X
min u subject to x −u ≤0
i i i
x,u
i −x −u ≤0,
i i
Ax=b
which can be solved using the standard primal-dual algorithm outlined in Section 2.1 (again,
see [2, Chap.11] for a full discussion). Set
f := x −u
u1;i i i
f := −x −u ,
u2;i i i
with λ ,λ the corresponding dual variables, and let f be the vector (f ... f )T
u1;i u2;i u1 u1;1 u1;N
(and likewise for f ,λ ,λ ). Note that
u2 u1 u2
(cid:18) (cid:19) (cid:18) (cid:19)
δ −δ
∇f = i , ∇f = i , ∇2f =0, ∇2f =0,
u1;i −δ u2;i −δ u1;i u2;i
i i
where δ is the standard basis vector for component i. Thus at a point (x,u;v,λ ,λ ), the
i u1 u2
central and dual residuals are
(cid:18) (cid:19)
−Λ f
r = u1 u1 −(1/τ)1,
cent −Λ f
u2 u2
(cid:18) λ −λ +ATv (cid:19)
r = u1 u2 ,
dual 1−λ −λ
u1 u2
and the Newton step (5) is given by:
 Σ Σ AT ∆x   w   (−1/τ)·(−f−1+f−1)−ATv 
1 2 1 u1 u2
Σ
2
Σ
1
0 ∆u=w 2:= −1−(1/τ)·(f
u
−
1
1+f
u
−
2
1) ,
A 0 0 ∆v w b−Ax
3
with
Σ =Λ F−1−Λ F−1, Σ =Λ F−1+Λ F−1,
1 u1 u1 u2 u2 2 u1 u1 u2 u2
(The F , for example, are diagonal matrices with (F ) =f , and f−1 =1/f .) Setting
• • ii •;i •;i •;i
Σ =Σ −Σ2Σ−1,
x 1 2 1
we can eliminate
∆x = Σ−1(w −Σ Σ−1w −AT∆v)
x 1 2 1 2
∆u = Σ−1(w −Σ ∆x),
1 2 2
and solve
−AΣ−1AT∆v =w −A(Σ−1w −Σ−1Σ Σ−1w ).
1 3 x 1 x 2 1 2
ThisisaK×K positivedefinitesystemofequations,andcanbesolvedusingconjugategradients.
Given ∆x,∆u,∆v, we calculate the change in the inequality dual variables as in (4):
∆λ = Λ F−1(−∆x+∆u)−λ −(1/τ)f−1
u1 u1 u1 u1 u1
∆λ = Λ F−1(∆x+∆u)−λ −(1/τ)f−1.
u2 u2 u2 u2 u2
12


## 第 13 页

B ‘ norm approximation
1
The ‘ norm approximation problem (P ) can also be recast as a linear program:
1 A
M
X
min u subject to Ax−u−y ≤0
m
x,u
m=1 −Ax−u+y ≤0,
(recallthatunliketheother6problems,heretheM×N matrixAhasmorerowsthancolumns).
For the primal-dual algorithm, we define
f =Ax−u−y, f =−Ax−u+y.
u1 u2
Given a vector of weights σ ∈RM,
X (cid:18) ATσ (cid:19) X (cid:18) −ATσ (cid:19)
σ ∇f = , σ ∇f = ,
m u1;m −σ m u2;m −σ
m m
X (cid:18) ATΣA −ATΣ (cid:19) X (cid:18) ATΣA ATΣ (cid:19)
σ ∇f ∇fT = , σ ∇f ∇fT = .
m u1;m u1;m −ΣA Σ m u2;m u2;m ΣA Σ
m m
At a point (x,u;λ ,λ ), the dual residual is
u1 u2
(cid:18) AT(λ −λ ) (cid:19)
r = u1 u2 ,
dual −λ −λ
u1 u2
and the Newton step is the solution to
(cid:18) ATΣ A ATΣ (cid:19)(cid:18) ∆x (cid:19) (cid:18) −(1/τ)·AT(−f−1+f−1) (cid:19) (cid:18) w (cid:19)
11 12 = u1 u2 := 1
Σ A Σ ∆u −1−(1/τ)·(f−1+f−1) w
12 11 u1 u2 2
where
Σ = −Λ F−1−Λ F−1
11 u1 u1 u2 u2
Σ = Λ F−1−Λ F−1.
12 u1 u1 u2 u2
Setting
Σ =Σ −Σ2 Σ−1,
x 11 12 11
we can eliminate ∆u=Σ−1(w −Σ A∆x), and solve
11 2 22
ATΣ A∆x=w −ATΣ Σ−1w
x 1 22 11 2
for ∆x. Again, ATΣ A is a N ×N symmetric positive definite matrix (it is straightforward to
x
verify that each element on the diagonal of Σ will be strictly positive), and so the Conjugate
x
Gradients algorithm can be used for large-scale problems.
Given ∆x,∆u, the step directions for the inequality dual variables are given by
∆λ = −Λ F−1(A∆x−∆u)−λ −(1/τ)f−1
u1 u1 u1 u1 u1
∆λ = Λ F−1(A∆x+∆u)−λ −(1/τ)f−1.
u2 u2 u2 u2 u2
C ‘ Dantzig selection
1
An equivalent linear program to (P ) in the real case is given by:
D
X
min u subject to x−u≤0,
i
x,u
i −x−u≤0,
ATr−(cid:15)≤0,
−ATr−(cid:15)≤0,
13


## 第 14 页

where r =Ax−b. Taking
f =x−u, f =−x−u, f =ATr−(cid:15), f =−ATr−(cid:15),
u1 u2 (cid:15)1 (cid:15)2
the residuals at a point (x,u;λ ,λ ,λ ,λ ), the dual residual is
u1 u2 (cid:15)1 (cid:15)2
(cid:18) λ −λ +ATA(λ −λ ) (cid:19)
r = u1 u2 (cid:15)1 (cid:15)2 ,
dual 1−λ −λ
u1 u2
and the Newton step is the solution to
(cid:18) ATAΣ ATA+Σ Σ (cid:19)(cid:18) ∆x (cid:19) (cid:18) −(1/τ)·(ATA(−f−1+f−1))−f−1+f−1(cid:19) (cid:18) w (cid:19)
a 11 12 = (cid:15)1 (cid:15)2 u1 u2 := 1
Σ Σ ∆u −1−(1/τ)·(f−1+f−1) w
12 11 u1 u2 2
where
Σ = −Λ F−1−Λ F−1
11 u1 u1 u2 u2
Σ = Λ F−1−Λ F−1
12 u1 u1 u2 u2
Σ = −Λ F−1−Λ F−1.
a (cid:15)1 (cid:15)1 (cid:15)2 (cid:15)2
Again setting
Σ =Σ −Σ2 Σ−1,
x 11 12 11
we can eliminate
∆u=Σ−1(w −Σ ∆x),
11 2 12
and solve
(ATAΣ ATA+Σ )∆x=w −Σ Σ−1w
a x 1 12 11 2
for ∆x. As before, the system is symmetric positive definite, and the CG algorithm can be used
to solve it.
Given ∆x,∆u, the step directions for the inequality dual variables are given by
∆λ = −Λ F−1(∆x−∆u)−λ −(1/τ)f−1
u1 u1 u1 u1 u1
∆λ = −Λ F−1(−∆x−∆u)−λ −(1/τ)f−1
u2 u2 u2 u2 u2
∆λ = −Λ F−1(ATA∆x)−λ −(1/τ)f−1
(cid:15)1 (cid:15)1 (cid:15)1 (cid:15)1 (cid:15)1
∆λ = −Λ F−1(−ATA∆x)−λ −(1/τ)f−1.
(cid:15)2 (cid:15)2 (cid:15)2 (cid:15)2 (cid:15)2
D ‘ minimization with quadratic constraints
1
The quadractically constrained ‘ minimization problem (P ) can be recast as the second-order
1 2
cone program
X
min u subject to x−u≤0,
i
x,u
i −x−u≤0,
1(cid:0) kAx−bk2−(cid:15)2(cid:1)
≤0.
2 2
Taking
f =x−u, f =−x−u, f =
1(cid:0) kAx−bk2−(cid:15)2(cid:1)
,
u1 u2 (cid:15) 2 2
we can write the Newton step (as in (8)) at a point (x,u) for a given τ as
(cid:18) Σ −f−1ATA+f−2ATrrTA Σ (cid:19)(cid:18) ∆x (cid:19) (cid:18) f−1−f−1+f−1ATr (cid:19) (cid:18) w (cid:19)
11 (cid:15) (cid:15) 12 = u1 u2 (cid:15) := 1
Σ Σ ∆u −τ1−f−1−f−1 w
12 11 u1 u2 2
14


## 第 15 页

where r =Ax−b, and
Σ = F−2+F−2
11 u1 u2
Σ = −F−2+F−2.
12 u1 u2
As before, we set
Σ =Σ −Σ2 Σ−1
x 11 12 11
and eliminate ∆u
∆u=Σ−1(w −Σ ∆x),
11 2 12
leaving us with the reduced system
(Σ −f−1ATA+f−2ATrrTA)∆x=w −Σ Σ−1w
x (cid:15) (cid:15) 1 12 11 2
which is symmetric positive definite and can be solved using CG.
E Total variation minimization with equality constraints
The equality constrained TV minimization problem
min TV(x) subject to Ax=b,
x
can be rewritten as the SOCP
X
min t s.t. kD xk ≤t
ij ij 2 ij
t,x
ij
Ax=b.
Defining the inequality functions
f = 1(cid:0) kD k2−t2 (cid:1) i,j =1,...,n (9)
tij 2 ij 2 ij
we have
(cid:18) DTD x (cid:19)
∇f = ij ij
tij −t δ
ij ij
(cid:18) DTD xxTDTD −t DTD xδT(cid:19) (cid:18) D∗D 0 (cid:19)
∇f ∇fT = ij ij ij ij ij ij ij ij , ∇2f = ij ij ,
tij tij −t
ij
δ
ij
xTD
i
T
j
D
ij
t2
ij
δ
ij
δ
i
T
j
tij 0 −δ
ij
δ
i
T
j
where δ is the Kronecker vector that is 1 in entry ij and zero elsewhere. For future reference:
ij
X (cid:18) DTΣD x+DTΣD x (cid:19)
σ ∇f = h h v v ,
ij tij −σt
ij
X (cid:18) BΣBT −BTΣ (cid:19)
σ ∇f ∇fT = ,
ij tij tij −ΣTBT ΣT2
ij
X (cid:18) DTΣD +DTΣD 0 (cid:19)
σ ∇2f = h h v v
ij tij 0 −Σ
ij
where Σ=diag({σ }), T =diag(t), D has the D as rows (and likewise for D ), and B is a
ij h h;ij v
matrix that depends on x:
B =DTΣ +DTΣ .
h ∂h v ∂v
with Σ =diag(D x), Σ =diag(D x).
∂h h ∂v v
15


## 第 16 页

The Newton system (8) for the log-barrier algorithm is then
 H BΣ AT ∆x   DTF−1D x+DTF−1D x   w 
11 12 h t h v t v 1
Σ 12 BT Σ 22 0 ∆t =  −τ1−F t −1t  := w 2,
A 0 0 ∆v 0 0
where
H =DT(−F−1)D + DT(−F−1)D + BF−2BT.
11 h t h v t v t
Eliminating ∆t
∆t = Σ−1(w −Σ BT∆x)
22 2 12
= Σ−1(w −Σ Σ D ∆x−Σ Σ D ∆x),
22 2 12 ∂h h 12 ∂v v
the reduced (N +K)×(N +K) system is
(cid:18) H0 AT(cid:19)(cid:18) ∆x (cid:19) (cid:18) w0(cid:19)
11 = 1 (10)
A 0 ∆v 0
with
H0 = H −BΣ2 Σ−1BT
11 11 12 22
= DT(Σ Σ2 −F−1)D + DT(Σ Σ2 −F−1)D +
h b ∂h t h v b ∂v t v
DT(Σ Σ Σ )D + DT(Σ Σ Σ )D
h b ∂h ∂v v v b ∂h ∂v h
w0 = w −BΣ Σ−1w
1 1 12 22 2
= w −(DTΣ +DTΣ )Σ Σ−1w
1 h ∂h v ∂v 12 22 2
Σ = F−2−Σ−1Σ2 .
b t 22 12
The system of equations (10) is symmetric, but not positive definite. Note that D and D are
h v
(very) sparse matrices, and hence can be stored and applied very efficiently. This allows us to
again solve the system above using an iterative method such as SYMMLQ [16].
F Total variation minimization with quadratic constraints
We can rewrite (TV ) as the SOCP
2
X
min t subject to kD xk ≤t , i,j =1,...,n
ij ij 2 ij
x,t
ij kAx−bk ≤(cid:15)
2
where D is as in (1). Taking f as in (9) and
ij tij
f =
1(cid:0) kAx−bk2−(cid:15)2(cid:1)
,
(cid:15) 2 2
with
(cid:18) ATr (cid:19) (cid:18) ATrrTA 0 (cid:19) (cid:18) A∗A 0 (cid:19)
∇f = , ∇f ∇fT = , ∇2f =
(cid:15) 0 (cid:15) (cid:15) 0 0 (cid:15) 0 0
where r =Ax−b.
Also,
(cid:18) D∗D 0 (cid:19) (cid:18) A∗A 0 (cid:19)
∇2f = ij ij ∇2f = .
tij 0 −δ δT (cid:15) 0 0
ij ij
16


## 第 17 页

The Newton system is similar to that in equality constraints case:
(cid:18) H BΣ (cid:19)(cid:18) ∆x (cid:19) (cid:18) DTF−1D x+DTF−1D x+f−1ATr (cid:19) (cid:18) w (cid:19)
11 12 = h t h v t v (cid:15) := 1 .
Σ BT Σ ∆t −τ1−tf−1 w
12 22 t 2
where (tf−1) =t /f , and
t ij ij tij
H = DT(−F−1)D + DT(−F−1)D + BF−2BT −
11 h t h v t v t
f−1ATA + f−2ATrrTA,
(cid:15) (cid:15)
Σ = −TF−2,
12 t
Σ = F−1+F−2T2,
22 t t
Again eliminating ∆t
∆t=Σ−1(w −Σ Σ D ∆x−Σ Σ D ∆x),
22 2 12 ∂h h 12 ∂v v
the key system is
H0 ∆x=w −(DTΣ +DTΣ )Σ Σ−1w
11 1 h ∂h v ∂v 12 22 2
where
H0 = H −BΣ2 Σ−1BT
11 11 12 22
= DT(Σ Σ2 −F−1)D + DT(Σ Σ2 −F−1)D +
h b ∂h t h v b ∂v t v
DT(Σ Σ Σ )D + DT(Σ Σ Σ )D −
h b ∂h ∂v v v b ∂h ∂v h
f−1ATA + f−2ATrrTA,
(cid:15) (cid:15)
Σ = F−2−Σ2 Σ−1.
b t 12 22
The system above is symmetric positive definite, and can be solved with CG.
G Total variation minimization with bounded residual cor-
relation
The TV Dantzig problem has an equivalent SOCP as well:
X
min t subject to kD xk ≤t , i,j =1,...,n
ij ij 2 ij
x,t
ij AT(Ax−b)−(cid:15)≤0
−AT(Ax−b)−(cid:15)≤0.
The inequality constraint functions are
f = 1(cid:0) kD xk2−t2 (cid:1) i,j =1,...,n
tij 2 ij 2 ij
f = AT(Ax−b)−(cid:15),
(cid:15)1
f = −AT(Ax−b)−(cid:15),
(cid:15)2
with
X (cid:18) ATAσ (cid:19) X (cid:18) −ATAσ (cid:19)
σ ∇f = , σ ∇f = ,
ij (cid:15)1;ij 0 ij (cid:15)2;ij 0
ij ij
and
X X (cid:18) ATAΣATA 0 (cid:19)
σ ∇f ∇fT = σ ∇f ∇fT = .
ij (cid:15)1;ij (cid:15)1;ij ij (cid:15)2;ij (cid:15)2;ij 0 0
ij ij
17


## 第 18 页

Thus the log barrier Newton system is nearly the same as in the quadratically constrained case:
(cid:18) H BΣ (cid:19)(cid:18) ∆x (cid:19) (cid:18) DTF−1D x+DTF−1D x+ATA(f−1−f−1) (cid:19) (cid:18) w (cid:19)
11 12 = h t h v t v (cid:15)1 (cid:15)2 := 1 .
Σ BT Σ ∆t −τ1−tf−1 w
12 22 t 2
where
H = DT(−F−1)D + DT(−F−1)D + BF−2BT + ATAΣ ATA,
11 h t h v t v t a
Σ = −TF−2,
12 t
Σ = F−1+F−2T2,
22 t t
Σ = F−2+F−2.
a (cid:15)1 (cid:15)2
Eliminating ∆t as before
∆t = Σ−1(w −Σ Σ D ∆x−Σ Σ D ∆x),
22 2 12 ∂h h 12 ∂v v
the key system is
H0 ∆x=w −(DTΣ +DTΣ )Σ Σ−1w
11 1 h ∂h v ∂v 12 22 2
where
H0 = DT(Σ Σ2 −F−1)D + DT(Σ Σ2 −F−1)D +
11 h b ∂h t h v b ∂v t v
DT(Σ Σ Σ )D + DT(Σ Σ Σ )D + ATAΣ ATA,
h b ∂h ∂v v v b ∂h ∂v h a
Σ = F−2−Σ2 Σ−1.
b t 12 22
References
[1] F. Alizadeh and D. Goldfarb. Second-order cone programming. Math. Program., Ser. B,
95:3–51, 2003.
[2] S. Boyd and L. Vandenberghe. Convex Optimization. Cambridge University Press, 2004.
[3] E.Cand`esandJ.Romberg. Quantitativerobustuncertaintyprinciplesandoptimallysparse
decompositions. To appear in Foundations of Comput. Math., 2005.
[4] E. Cand`es, J. Romberg, and T. Tao. Robust uncertainty principles: Exact signal recon-
structionfromhighlyincompletefrequencyinformation. Submitted to IEEE Trans. Inform.
Theory, June 2004. Available on theArXiV preprint server: math.GM/0409186.
[5] E.Cand`es, J.Romberg, andT.Tao. Stablesignalrecoveryfromincompleteandinaccurate
measurements. Submitted to Communications on Pure and Applied Mathematics, March
2005.
[6] E.Cand`esandT.Tao. Near-optimalsignalrecoveryfromrandomprojectionsanduniversal
encoding strategies. submitted to IEEE Trans. Inform. Theory, November 2004. Available
on the ArXiV preprint server: math.CA/0410542.
[7] E. Cand`es and T. Tao. The Dantzig selector: statistical estimation when p is much smaller
than n. Manuscript, May 2005.
[8] E. J. Cand`es and T. Tao. Decoding by linear programming. To appear in IEEE Trans.
Inform. Theory, December 2005.
18


## 第 19 页

[9] T.Chan,G.Golub,andP.Mulet. Anonlinearprimal-dualmethodfortotalvariation-based
image restoration. SIAM J. Sci. Comput., 20:1964–1977, 1999.
[10] S. S. Chen, D. L. Donoho, and M. A. Saunders. Atomic decomposition by basis pursuit.
SIAM J. Sci. Comput., 20:33–61, 1999.
[11] D.GoldfarbandW.Yin. Second-orderconeprogrammingmethodsfortotalvariation-based
image restoration. Technical report, Columbia University, 2004.
[12] H. Hintermu¨ller and G. Stadler. An infeasible primal-dual algorithm for TV-based inf-
convolution-type image restoration. To appear in SIAM J. Sci. Comput., 2005.
[13] M. Lobo, L. Vanderberghe, S. Boyd, and H. Lebret. Applications of second-order cone
programming. Linear Algebra and its Applications, 284:193–228, 1998.
[14] Y. E. Nesterov and A. S. Nemirovski. Interior Point Polynomial Methods in Convex Pro-
gramming. SIAM Publications, Philadelphia, 1994.
[15] J. Nocedal and S. J. Wright. Numerical Optimization. Springer, New York, 1999.
[16] C. C. Paige and M. Saunders. Solution of sparse indefinite systems of linear equations.
SIAM J. Numer. Anal., 12(4), September 1975.
[17] J. Renegar. A mathematical view of interior-point methods in convex optimization. MPS-
SIAM Series on Optimization. SIAM, 2001.
[18] L. I. Rudin, S. Osher, and E. Fatemi. Nonlinear total variation noise removal algorithm.
Physica D, 60:259–68, 1992.
[19] J. R. Shewchuk. An introduction to the conjugate gradient method without the agonizing
pain. Manuscript, August 1994.
[20] S. J. Wright. Primal-Dual Interior-Point Methods. SIAM Publications, 1997.
19

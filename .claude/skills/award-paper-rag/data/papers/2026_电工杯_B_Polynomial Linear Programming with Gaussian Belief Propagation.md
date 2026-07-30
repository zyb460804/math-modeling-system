# Polynomial Linear Programming with Gaussian Belief Propagation


## 第 1 页

8002
tcO
9
]TI.sc[
1v1361.0180:viXra
Polynomial Linear Programming
with Gaussian Belief Propagation
Danny Bickson, Yoav Tock Ori Shental Danny Dolev
IBM Haifa Research Lab Center for Magnetic School of Computer Science
Mount Carmel Recording Research and Engineering
Haifa 31905, Israel UCSD, San Diego Hebrew University of Jerusalem
Email: {dannybi,tock}@il.ibm.com 9500 Gilman Drive Jerusalem 91904, Israel
La Jolla, CA 92093, USA Email: dolev@cs.huji.ac.il
Email: oshental@ucsd.edu
Abstract—Interior-pointmethodsarestate-of-the-artal- of BP. Globerson etal. [3], [4] assume convexity
gorithms for solving linear programming (LP) problems of the problem and modify the BP update rules
with polynomial complexity. Specifically, the Karmarkar using dual-coordinate ascent algorithm. Hazan et
algorithm typically solves LP problems in time O(n3.5 ),
al. [5] describe an algorithm for solving a general
wherenisthenumberofunknownvariables.Karmarkar’s
convex free energy minimization. In both cases the
celebrated algorithm is known to be an instance of the
algorithm is guaranteed to converge to the global
log-barrier method using the Newton iteration. The main
computational overhead of this method is in inverting minimum as the problem is tailored to be convex.
the Hessian matrix of the Newton iteration. In this In the present work we take a different path. Un-
contribution, we propose the application of the Gaussian like most of the previous work which uses gradient-
beliefpropagation(GaBP)algorithmaspartofanefficient
descent methods, we show how to use interior-point
and distributed LP solver that exploits the sparse and
methodswhich are shownto havestrong advantages
symmetric structure of the Hessian matrix and avoids the
over gradient and steepest descent methods. (For a
need for direct matrix inversion. This approach shifts the
computationfromrealmoflinearalgebratothatofproba- comparative study see [6, §9.5,p. 496].) The main
bilisticinferenceongraphicalmodels,thusapplyingGaBP benefit of using interior point methods is their
asanefficientinferenceengine.Ourconstructionisgeneral rapid convergence, which is quadratic once we are
and can be used for any interior-point algorithm which
close enough to the optimal solution. Their main
uses the Newton method, including non-linear program
drawback is that they require heavier computational
solvers.
effort for forming and inverting the Hessian ma-
trix, needed for computing the Newton step. To
I. INTRODUCTION
overcome this, we propose the use of Gaussian BP
In recent years, considerable attention has been (GaBP) [7], [8], which is a variant of BP applicable
dedicated to the relation between belief propagation when the underlying distribution is Gaussian. Using
message passing and linear programming schemes. GaBP, we are able to reduce the time associated
This relation is natural since the maximum a- with the Hessian inversion task, from O(n2.5) to
posteriori (MAP) inference problem can be trans- O(nplog(ǫ)/log(γ)) at the worst case, where p < n
lated into integer linear programming (ILP) [1]. is the size of the constraint matrix A, ǫ is the
Weiss etal. [1] approximate the solution to the desired accuracy, and 1/2 < γ < 1 is a parameter
ILP problem by relaxing it to a LP problem using characterizing the matrix A. This computational
convex variational methods. In [2], tree-reweighted saving is accomplished by exploiting the sparsity
belief propagation (BP) is used to find the global of the Hessian matrix.
minimum of a convex approximation to the free An additional benefit of our GaBP-based ap-
energy. Both of these works apply discrete forms proach is that the polynomial-complexity LP solver


## 第 2 页

can be implemented in a distributed manner, en- ∆x = −f′′(x˜)−1f′(x˜). (5)
abling efficient solution of large-scale problems.
We also provide what we believe is the first Denoting the current point x˜ , (x,µ,y) and
theoretical analysis of the convergence speed of the the Newton step ∆x , (x,y,µ), we compute the
GaBP algorithm. gradient
The paper is organized as follows. In Section
II, we reduce standard linear programming to a f′(x,µ,y) ≡ (∂f(x,µ,y)/∂x,∂f(x,µ,y)/∂µ,
least-squares problem. Section III shows how to ,∂f(x,µ,y)/∂y)
solve the least-squares problem using the GaBP
algorithm.InSectionIV,weextendourconstruction The Lagrangian is
to theprimal-dualmethod.We giveourconvergence
results for the GaBP algorithm in Section V, and L(x,µ,y) = cTx−µΣ logx +yT(b−Ax), (7)
k k
demonstrate our construction in Section VI using
an elementary example. We present our conclusions
in Section VII.
∂L(x,µ,y)
= c−µX−11−yTA = 0, (8)
II. STANDARD LINEAR PROGRAMMING ∂x
Consider the standard linear program
∂2L(x,µ,y)
minimize cTx (1a) = µX−2, (9)
x ∂x
subject to Ax = b, x ≥ 0 (1b)
where X , diag(x) and 1 is the all-one column
where A ∈ Rn×p with rank{A} = p < n. We vector. Substituting (8)-(9) into (4), we get
assume the problem is solvable with an optimal
x∗ assignment. We also assume that the problem c−µX−11−yTA+µX−2x = 0, (10)
is strictly feasible, or in other words there exists
x ∈ Rn that satisfies Ax = b and x > 0.
c−µX−11+xµX−2 = yTA, (11)
Using the log-barrier method [6, §11.2], one gets
minimize cTx−µΣn logx (2a)
x,µ k=1 k
∂L(x,µ,y)
subject to Ax = b. (2b) = Ax = 0. (12)
∂y
This is an approximation to the original problem
(1a). The quality of the approximation improves as Now multiplying (11) by AX2, and using (12) to
the parameter µ → 0. eliminate x we get
Now we would like to use the Newton method
in for solving the log-barrier constrained objective AX2ATy = AX2c−µAX1. (13)
function (2a), described in Table I. Suppose that we
These normal equations can be recognized as gen-
have an initial feasible point x for the canonical
0
erated from the linear least-squares problem
linear program (1a). We approximate the objective
function (2a) around the current point x˜ using a
min||XATy−Xc−µAX1||2. (14)
second-order Taylor expansion 2
y
f(x˜+∆x) ≃ f(x˜)+f′(x˜)∆x+1/2∆xTf′′(x˜)∆x.
Solving for y we can compute the Newton direction
(3)
x, taking a step towards the boundary and compose
Finding the optimal search direction ∆x yields the
oneiterationoftheNewtonalgorithm.Next,wewill
computation of the gradient and compare it to zero
explain how to shift the deterministicLP problem to
∂f the probabilistic domain and solve it distributively
= f′(x˜)+f′′(x˜)∆x = 0, (4)
using GaBP.
∂∆x


## 第 3 页

TABLEI
THENEWTONALGORITHM[6,§9.5.2].
Given feasible starting point x and tolerance ǫ > 0, k = 1
0
Repeat 1 Compute the Newton step and decrement
∆x = f′′(x)−1f′(x), λ2 = f′(x)T∆x
2 Stopping criterion. quit if λ2/2 ≤ ǫ
3 Line search. Choose step size t by backtracking line search.
4 Update. x := x +t∆x, k = k +1
k k−1
III. FROM LP TO PROBABILISTIC INFERENCE ψ and self-potentials (‘evidence’) φ . These graph
ij i
potentials are determined according to the follow-
We start from the least-squares problem (14),
ing pairwise factorization of the Gaussian distribu-
changing notations to
tion p(x) ∝ n φ (x ) ψ (x ,x ), resulting
i=1 i i {i,j} ij i j
m y in||Fy−g||2 2 , (15) in ψ ij (x i ,x j Q) , exp(−Qx i C ij x j ), and φ i (x i ) ,
exp b x − C x2/2 . The set of edges {i,j} cor-
i i ii i
where F , XAT,g , Xc+µAX1. Now we define resp(cid:0)onds to the set(cid:1)of non-zero entries in C (18).
a multivariate Gaussian Hence, we would like to calculate the marginal
densities, which must also be Gaussian,
p(xˆ) , p(x,y) ∝ exp(−1/2(Fy−g)TI(Fy−g)).
(16) p(x ) ∼ N(µ = {C−1g} ,P−1 = {C−1} ),
i i i i ii
It is clear that yˆ, the minimizing solution of (15),
∀i > p,
is the MAP estimator of the conditional probability
where µ and P are the marginal mean and inverse
i i
yˆ = argmaxp(y|x) =
variance (a.k.a. precision), respectively. Recall that,
y
according to [9], the inferred mean µ is identical
i
= N((FTF)−1FTg,(FTF)−1). (17) to the desired solution yˆ of (17). The GaBP update
rules are summarized in Table II.
Recent results by Bickson and Shental etal. [7]–
It is known that if GaBP converges, it results in
[9] show that the pseudoinverse problem (17) can
exact inference [10]. However, in contrast to con-
be computed efficiently and distributively by using
ventional iterative methods for the solution of sys-
the GaBP algorithm.
tems of linear equations, for GaBP, determining the
The formulation (16) allows us to shift the least-
exact region of convergence and convergence rate
squares problem from an algebraic to a probabilistic
remain open research problems. All that is known is
domain. Instead of solving a deterministic vector-
a sufficient (but not necessary) condition [11], [12]
matrix linear equation, we now solve an inference
stating that GaBP converges when the spectral ra-
problem in a graphical model describing a certain
dius satisfies ρ(|I −A|) < 1. A stricter sufficient
K
Gaussian distribution function. Following [9] we
condition [10], determines that the matrix A must
define the joint covariance matrix
be diagonally dominant (i.e., |a | > |a |,∀i)
ii j6=i ij
−I F in order for GaBP to converge. ConvPergence speed
C , (18)
(cid:18) FT 0 (cid:19) is discussed in Section V.
and the shift vector b , {0T,gT}T ∈ R(p+n)×1. IV. EXTENDING THE CONSTRUCTION TO THE
Given the covariance matrix C and the shift
PRIMAL-DUAL METHOD
vector b, one can write explicitly the Gaussian In the previous section we have shown how to
density function, p(xˆ) , and its corresponding graph compute one iteration of the Newton method using
G with edge potentials (‘compatibility functions’) GaBP. In this section we extend the technique for


## 第 4 页

TABLE II
COMPUTING x=A−1b VIAGABP[7].
# Stage Operation
1. Initialize Compute P = A and µ = b /A .
ii ii ii i ii
Set P = 0 and µ = 0, ∀k 6= i.
ki ki
2. Iterate Propagate P and µ , ∀k 6= i such that A 6= 0.
ki ki ki
Compute P = P + P and µ = P−1(P µ + P µ ).
i\j ii k∈N(i)\j ki i\j i\j ii ii k∈N(i)\j ki ki
Compute P = −A PP−1A and µ = −P−1A µ . P
ij ij i\j ji ij ij ij i\j
3. Check If P and µ did not converge, return to #2. Else, continue to #4.
ij ij
4. Infer P = P + P , µ = P−1(P µ + P µ ).
i ii k∈N(i) ki i i ii ii k∈N(i) ki ki
5. Output x = µ P P
i i
computing the primal-dual method. This construc- The solution [x(µ),y(µ),z(µ)] of these equations
tion is attractive, since the extended technique has constitutes the central path of solutions to the log-
the same computation overhead. arithmic barrier method [6, 11.2.2]. Applying the
The dual problem ( [13]) conforming to (1a) can Newton method to this system of equations we get
be computed using the Lagrangian
0 AT I ∆x b−Ax
L(x,y,z) = cTx+yT(b−Ax)−zTx, z ≥ 0,  A 0 0  ∆y  =  c−ATy−z .
Z 0 X ∆z µ1−Xz
    
(24)
g(y,z) = infL(x,y,z), (19a) The solution can be computed explicitly by
x
subject to Ax = b,x ≥ 0. (19b)
∆y = (AZ−1XAT)−1·
while (AZ−1X(c−µX−11−ATy)+b−Ax),
∂L(x,y,z) ∆x = XZ−1(AT∆y+µX−11 = c+ATy),
= c−ATy−z = 0. (20)
∂x ∆z = −AT∆y+c−ATy−z.
Substituting (20) into (19a) we get
The main computational overhead in this method
maximize bTy is the computation of (AZ−1XAT)−1, which is
y
derived from the Newton step in (5).
subject to ATy+z = c, z ≥ 0.
Now we would like to use GaBP for computing
Primal optimality is obtained using (8) [13] the solution. We make the following simple change
to (24) to make it symmetric: since z > 0, we can
yTA = c−µX−11. (22)
multiply the third row by Z−1 and get a modified
Substituting (22) in (21a) we get the connection symmetric system
between the primal and dual
0 AT I ∆x b−Ax
µX−11 = z.  A 0 0  ∆y  =  c−ATy−z .
I 0 Z−1X ∆z µZ−11−X
In total, we have a primal-dual system (again we
    
assume that the solution is strictly feasible, namely 0 AT I
x > 0,z > 0) Defining A˜ ,  A 0 0 , and b˜ ,
I 0 Z−1X
Ax = b, x > 0,
 
b−Ax
ATy+z = c, z > 0,
 c−ATy−z . one can use GaBP iterative
Xz = µ1. µZ−11−X
 
algorithm shown in Table II.


## 第 5 页

In general, by looking at (4) we see that the dominant, we define ε to be the non negative gap
i
solution of each Newton step involves inverting the
ε , |A |−Σ |A | > 0.
Hessian matrix f′′(x). The state-of-the-art approach i ii j ij
in practical implementations of the Newton step and the following decomposition
is first computing the Hessian inverse f′′(x)−1 by ˜ b = A , c˜ = A +ε /|N(i)|,
ij ij ij ij i
using a (sparse) decomposition method like (sparse)
Cholesky decomposition, and then multiplying the where |N(i)| is the number of graph neighbors of
result by f′(x). In our approach, the GaBP al- node i. Following Weiss, we define γ to be
gorithm computes directly the result ∆x, without ˜
|b | |a |
ij ij
computing the full matrix inverse. Furthermore, if γ = max = =
the GaBP algorithm converges, the computation of i,j |c˜ ij | |a ij |+ε i /|N(i)|
∆x is guaranteed to be accurate. 1
= max < 1. (25)
i,j 1+(ε i )/(|a ij ||N(i)|)
V. NEW CONVERGENCE RESULTS
In total,wegetthat foradesired accuracy ofǫ||b||
∞
In this section we give an upper bound on the
we need to iterate for t = ⌈log(ǫ)/log(γ)⌉ rounds.
convergence rate of the GaBP algorithm. As far as
Note that this is an upper bound and in practice
we know this is the first theoretical result bounding
we indeed have observed a much faster convergence
the convergence speed of the GaBP algorithm.
rate.
Our upper bound is based on the work of Weiss The computation of the parameter γ can be easily
etal. [10, Claim 4], which proves the correctness
done in a distributed manner: Each node locally
of the mean computation. Weiss uses the pairwise computes ε , and γ = max 1/(1+|a |ε /N(i)).
i i j ij i
potentials form1, where
Finally, one maximum operation is performed glob-
ally, γ = max γ .
p(x) ∝ Π ψ (x ,x )Π ψ (x ), i i
i,j ij i j i i i
ψ (x ,x ) ≡ exp(−1/2(x x )TV (x x )), A. Applications to Interior-Point Methods
i,j i j i j ij i j
˜ We would like to compare the running time of
a˜ b
V ij ≡ ˜ ij ij . our proposed method to the Newton interior-point
(cid:18) b c˜ (cid:19)
ji ij
method, utilizing our new convergence results of
Assuming the optimal solution is x∗, for a desired the previous section. As a reference we take the
accuracy ǫ||b|| where ||b|| ≡ max |b |, and b is Karmarkar algorithm [14] which is known to be
∞ ∞ i i
the shift vector, we need to run the algorithm for at an instance of the Newton method [15]. Its running
most t = ⌈log(ǫ)/log(β)⌉ rounds to get an accuracy time is composed of n rounds, where on each round
of |x∗ −x | < ǫ||b|| where β = max | ˜ b /c˜ |. one Newton step is computed. The cost of comput-
t ∞ ij ij ij
The problem with applying Weiss’ result directly ing one Newton step on a dense Hessian matrix is
to our model is that we are working with different O(n2.5), so the total running time is O(n3.5).
parameterizations. We use the information form Using our approach, the total number of Newton
p(x) ∝ exp(−1/2xTAx+bTx).Thedecomposition iterations, n, remains the same as in the Karmarkar
of the matrix A into pairwise potentials is not algorithm. However, we exploit the special structure
unique. In order to use Weiss’ result, we propose of the Hessian matrix, which is both symmetric
such a decomposition. Any decomposition from and sparse. Assuming that the size of the constraint
the canonical form to the pairwise potentials form matrix A is n × p, p < n, each iteration of
should be subject to the following constraints [10] GaBP for computing a single Newton step takes
O(np), and based on our new convergence analysis
˜ b = A , Σ c˜ = A .
ij ij j ij ii for accuracy ǫ||b|| we need to iterate for r =
∞
We propose to initialize the pairwise potentials as ⌈log(ǫ)/log(γ)⌉ rounds, where γ is defined in (25).
The total computational burden for a single Newton
following. Assuming the matrix A is diagonally
step is O(nplog(ǫ)/log(γ)). There are at most n
1Weiss assumes scalar variables with zero means. rounds, hence in total we get O(n2plog(ǫ)/log(γ)).


## 第 6 页

1.2
1
0.8
0.6
0.4
0.2
0 0 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9
x1
2x
an iterative algorithm, the Gaussian belief propaga-
tion algorithm. Unlike previous approaches which
use discrete belief propagation and gradient descent
methods, we take a different path by using con-
tinuous belief propagation applied to interior-point
methods. By shifting the Hessian matrix inverse
computation required by the Newton method, from
linear algebra domain to the probabilistic domain,
we gain a significant speedup in performance of
the Newton method. We believe there are numerous
applicationsthatcan benefitfrom ournewapproach.
ACKNOWLEDGEMENT
Fig. 1. A simple example of using GaBP for solving linear O. Shental acknowledges the partial support of
programming with two variables and eleven constraints. Each red
the NSF (Grant CCF-0514859). D. Bickson would
circle shows one iteration of the Newton method.
liketothankNatiLinialfromtheHebrewUniversity
of Jerusalem for proposing this research direction.
The authors are grateful to Jack Wolf and Paul
VI. EXPERIMENTAL RESULTS
Siegel from UCSD for useful discussions and for
We demonstrate the applicability of the proposed constructive comments on the manuscript.
algorithmusingthefollowingsimplelinear program
borrowed from [16] REFERENCES
maximize x +x [1] C. Yanover, T. Meltzer, and Y. Weiss, “Linear programming
1 2
relaxations and belief propagation – an empirical study,” in
subject to 2px +x ≤ p2 +1,
1 2 Journal of Machine Learning Research, vol. 7. Cambridge,
MA, USA: MIT Press, 2006, pp. 1887–1907.
p = 0.0,0.1,··· ,1.0 .
[2] Y. Weiss, C. Yanover, and T. Meltzer, “Map estimation, linear
programmingandbeliefpropagationwithconvexfreeenergies,”
Fig. 1 shows execution of the affine-scaling al-
inThe23thConferenceonUncertaintyinArtificialIntelligence
gorithm [17], a variant of Karmarkar’s algorithm (UAI), 2007.
[14], on a small problem with two variables and [3] A. Globerson and T. Jaakkola, “Fixing max-product: Conver-
gent message passing algorithms for map lp-relaxations,” in
eleven constraints. Each circle is one Newton step.
Advances in Neural Information Processing Systems (NIPS),
The inverted Hessian is computed using the GaBP
no. 21, Vancouver, Canada, 2007.
algorithm, using two computing nodes. Matlab code [4] M. Collins,A.Globerson, T. Koo, X.Carreras,and P.Bartlett,
“Exponentiated gradient algorithms for conditional random
for this example can be downloaded from [18].
fields and max-margin markov networks,” in Journal of Ma-
Regarding larger scale problems, we have ob-
chine Learning Research. Accepted for publication, 2008.
served rapid convergence (of a single Newton step [5] T. Hazan and A. Shashua, “Convergent message-passing al-
gorithms for inference over general graphs with convex free
computation) on very large scale problems. For
energy,” in The 24th Conference on Uncertainty in Artificial
example, [19] demonstrates convergence of 5-10
Intelligence (UAI), Helsinki, July 2008.
rounds on sparse constraint matrices with several [6] S. Boyd and L. Vandenberghe, Convex Optimization. Cam-
millions of variables. [20] shows convergence of bridge University Press, March 2004.
[7] O.Shental,D.Bickson,P.H.Siegel,J.K.Wolf,andD.Dolev,
dense constraint matrices of size up to 150,000 ×
“Gaussianbeliefpropagationsolverforsystemsoflinearequa-
150,000 in 6 rounds, where the algorithm is run in tions,” in IEEE Int. Symp. on Inform. Theory (ISIT), Toronto,
parallel using 1,024 CPUs. Empirical comparison Canada, July 2008.
[8] D.Bickson,O.Shental,P.H.Siegel,J.K.Wolf,andD.Dolev,
with other iterative algorithms is given in [8].
“Lineardetectionviabeliefpropagation,”inProc.45thAllerton
Conf.onCommunications,ControlandComputing,Monticello,
VII. CONCLUSION
IL, USA, Sept. 2007.
[9] ——,“Gaussianbeliefpropagationbasedmultiuserdetection,”
In this paper we have shown how to efficiently
inIEEEInt.Symp.onInform.Theory(ISIT),Toronto,Canada,
and distributivelysolveinterior-pointmethods using July 2008.


## 第 7 页

[10] Y.WeissandW.T.Freeman,“Correctnessofbeliefpropagation
in Gaussian graphical models of arbitrary topology,” Neural
Computation, vol. 13, no. 10, pp. 2173–2200, 2001.
[11] J. K. Johnson, D. M. Malioutov, and A. S. Willsky, “Walk-
suminterpretationandanalysisofGaussianbeliefpropagation,”
in Advances in Neural Information Processing Systems 18,
Y. Weiss, B. Scho¨lkopf, and J. Platt, Eds. Cambridge, MA:
MIT Press, 2006, pp. 579–586.
[12] D.M.Malioutov,J.K.Johnson,andA.S.Willsky,“Walk-sums
and belief propagation in Gaussian graphical models,” Journal
of Machine Learning Research, vol. 7, Oct. 2006.
[13] S.PortnoyandR.Koenker,“Thegaussianhareandthelaplacian
tortoise: Computability of squared- error versus absolute-error
estimators,” in Statistical Science, vol. 12, no. 4. Institute of
Mathematical Statistics, 1997, pp. 279–296.
[14] N. Karmarkar, “A new polynomial-time algorithm for linear
programming,” in STOC ’84: Proceedings of the sixteenth
annual ACMsymposium onTheoryof computing. New York,
NY, USA: ACM, 1984, pp. 302–311.
[15] D. A. Bayer and J. C. Lagarias, “Karmarkar’s linear pro-
gramming algorithm and newton’s method,” in Mathematical
Programming, vol. 50, no. 1, March 1991, pp. 291–330.
[16] http://en.wikipedia.org/wiki/Karmarkar’s_algorithm.
[17] R. J. Vanderbei, M. S. Meketon, and B. A. Freedman, “A
modification of karmarkar’s linearprogramming algorithm,”in
Algorithmica, vol. 1, no. 1, March 1986, pp. 395–407.
[18] http://www.cs.huji.ac.il/labs/danss/p2p/gabp/.
[19] D. Bickson and D. Malkhi, “A unifying framework for rating
users and data items in peer-to-peer and social networks,”
in Peer-to-Peer Networking and Applications (PPNA) Journal,
Springer-Verlag, April 2008.
[20] D. Bickson, D. Dolev, and E. Yom-Tov, “A gaussian belief
propagation solver for large scale support vector machines,”
in 5th European Conference on Complex Systems, Jerusalem,
Sept. 2008.

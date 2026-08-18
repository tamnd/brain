---
title: "CF 102185G - \u0413\u0438\u0440\u043b\u044f\u043d\u0434\u0430"
description: "The garland is controlled by one positive integer (A). After it is switched on at an integer time (s), it stays on for (A) minutes, then off for (A) minutes, and repeats forever. The holiday occupies the interval ([0,T])."
date: "2026-08-19T06:37:14+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102185
codeforces_index: "G"
codeforces_contest_name: "Southern Russia Open Championship \u2013 ContestSFedU 2019, Team Final."
rating: 0
weight: 102185
solve_time_s: 336
verified: false
draft: false
---

[CF 102185G - \u0413\u0438\u0440\u043b\u044f\u043d\u0434\u0430](https://codeforces.com/problemset/problem/102185/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 5m 36s  
**Verified:** no  

## Solution
## Problem Understanding

The garland is controlled by one positive integer (A). After it is switched on at an integer time (s), it stays on for (A) minutes, then off for (A) minutes, and repeats forever. The holiday occupies the interval ([0,T]). During this interval at least half of the time must be lit.

The grandfather is at home during several disjoint intervals ([L_i,R_i]). We want to choose (A) and the switching time (s) so that the amount of lit time inside all grandfather intervals is as small as possible. Among solutions with the same minimum overlap, the smaller (A) wins, and if (A) is also equal, the later switching time wins.

Since every endpoint is an integer, every relevant boundary is an integer as well. We can regard each minute ([t,t+1)) as one unit. Let (g[t]) be 1 when the grandfather is home during that minute and 0 otherwise. The requirement becomes that the garland must be on during at least (\lceil T/2\rceil) unit intervals, while the objective is the sum of (g[t]) over the lit minutes.

The bound (T\le 5000) is the central constraint. A quadratic algorithm is realistic, while a cubic algorithm is far too large. There are at most (T) possible useful values of (A), so even a constant amount of work for every pair involving (A) and a switching time gives roughly (25) million operations. The solution should exploit this quadratic budget rather than repeatedly scanning all (T) minutes for every candidate.

There are several boundary cases that easily cause incorrect solutions.

For an odd holiday length, "at least half" means the ceiling. For example,

```
3 1
0 1
```

The garland has to be lit for at least 2 minutes. The optimal answer is `0 2 1`: switching on at time 1 with (A=2) lights exactly ([1,3]), completely avoiding the grandfather.

A switching time can be negative, and such starts are not equivalent to simply starting at time zero with another phase. For example,

```
8 2
1 3
5 7
```

has the answer `0 2 -1`. With (A=2) and (s=-1), the garland is lit during ([0,1]), ([3,5]), and ([7,8]), giving exactly four lit minutes and avoiding both grandfather intervals.

The latest-start tie breaker also matters when there is no grandfather at all. For

```
4 0
```

the answer is `0 1 1`, not `0 1 0`. Both starts satisfy the lighting condition with (A=1), but time 1 is later.

Finally, interval endpoints describe continuous half-open intervals. For example,

```
3 1
1 2
```

with (A=1,s=0) lights ([0,1]) and ([2,3]), so the grandfather interval ([1,2]) is avoided completely. The answer is `0 1 0`. Treating the endpoint 1 or 2 as an extra minute would incorrectly count an overlap.

## Approaches

The direct brute-force solution is conceptually simple. For every (A), enumerate every relevant switching time (s), simulate the garland for all (T) minutes, count how many minutes are lit, and count how many of those minutes intersect the grandfather intervals. The simulation makes the method correct because it directly evaluates exactly the schedule represented by each candidate.

The problem is the number of candidates and the repeated simulation. For a fixed (A), starts at most (2A-1) minutes before zero can represent all distinct periodic states before the holiday, while positive starts only need to be considered up to (T/2), since after that fewer than half the holiday remains. This gives (O(T+A)) starts for one (A). Across all (A), there are already (O(T^2)) candidates. Simulating (T) minutes for each one produces (O(T^3)) work, around (1.9\cdot10^{11}) minute checks when (T=5000).

The key observation is that shifting the switching time by one minute changes the overlap in a very structured way. Fix (A), and consider a positive switching time (s). The lit minutes are

[
[s,s+A),[s+2A,s+3A),[s+4A,s+5A),\ldots
]

as long as they intersect the holiday. If the start moves from (s) to (s+1), every lit block loses its first minute and gains its next minute. Across all cycles, the difference depends only on two arithmetic progressions whose step is (2A).

Define

[
D[s]=\sum_{k\ge0}\left(g[s+2Ak]-g[s+A+2Ak]\right),
]

where values outside ([0,T-1]) are treated as zero. Then, if (F[s]) is the grandfather overlap for a garland started at (s),

[
F[s]=F[s+1]+D[s].
]

Even better, (D) itself has a recurrence:

[
D[s]=g[s]-g[s+A]+D[s+2A].
]

So for one fixed (A), all positive starts can be evaluated in a single backwards scan.

Starts at or before zero are slightly different because the garland has already been running when the holiday begins. In that case only the phase modulo (2A) matters. The (2A) phases naturally split into two complementary groups of (A) phases. If phase (p) lights residues (p,p+1,\ldots,p+A-1), then phase (p+A) lights exactly the complementary residues. Consequently their grandfather overlaps sum to the total amount of grandfather time.

The same difference array (D) also lets us move between neighboring phases. For (0\le p<A), shifting phase (p) to (p+1) changes its overlap by (D[p]), while shifting phase (p+A) to (p+A+1) changes it in the opposite direction. Thus all negative starts can be checked in only (A) iterations, examining two phases at each iteration.

There is also no need to consider (A>T). Since (2A>2T), such a garland can intersect the holiday in at most one lit segment. If that segment is a prefix of the holiday, the same prefix can be produced with (A=T) by ending the first lit interval at the same point. If it is a suffix, (A=T) with the same start works. A complete holiday can also be produced with (A=T,s=0). Thus every feasible solution with (A>T) has an equally good solution with (A\le T), and the smaller (A) tie breaker makes the larger value irrelevant.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(T^3)) | (O(T)) | Too slow |
| Optimal | (O(T^2)) | (O(T)) | Accepted |

## Algorithm Walkthrough

1. Convert the grandfather intervals into an array `g`, where `g[t]` is 1 exactly when the grandfather is present during minute ([t,t+1)). The total grandfather time is also stored because complementary garland phases will be compared against it.
2. Set the required lit duration to ((T+1)//2). Only (A=1,2,\ldots,T) need to be examined because values larger than (T) can always be replaced by (T) without changing the useful lit segment inside the holiday.
3. For a fixed (A), let (P=2A). Construct the difference array (D) backwards using

[
D[s]=g[s]-g[s+A]+D[s+P].
]

The term (D[s+P]) represents all later pairs in the same residue classes modulo (2A). Computing the array backwards makes that value available immediately.
4. At the same time, maintain the overlap for a positive switching time. Start with zero overlap after time (T), and when processing (s) from (T-1) down to zero, add (D[s]). The resulting cumulative value is exactly the overlap for a garland whose first activation starts at (s). Positive starts larger than (\lfloor T/2\rfloor) cannot light half of the holiday, so only starts up to that point need to be considered.
5. For starts at or before zero, consider the periodic phase (p) modulo (P). Phase (p) corresponds to the latest non-positive start (s=p-P) when (p>0), and to (s=0) when (p=0). Phase (p+A) corresponds to start (p-A).
6. Compute the overlap of phase zero. For every residue (r), let (R_r) be the total grandfather time occurring at minutes congruent to (r\pmod P). Then (D[r]=R_r-R_{r+A}) for (0\le r<A). Summing these differences over (r=0,\ldots,A-1) gives the difference between the overlap of phase zero and phase (A). Since those two phases partition all minutes, their overlaps add up to the total grandfather time. Hence

[
H_0=\frac{G+\sum_{r=0}^{A-1}D[r]}{2}.
]
7. Compute the number of lit minutes for phase zero directly. A full period contributes (A) lit minutes, so

[
L_0=\left\lfloor\frac{T}{2A}\right\rfloor A+
\min(T\bmod 2A,A).
]

Phase (A) is complementary, so it has (T-L_0) lit minutes.
8. Iterate (p=0,\ldots,A-1). At every iteration, evaluate both phase (p) and phase (p+A). For the first phase, its overlap decreases by (D[p]) when the phase advances. The complementary phase increases by the same amount. The lit durations behave identically, with the corresponding residue-count difference instead of the grandfather-weighted difference.
9. Whenever a candidate has at least (\lceil T/2\rceil) lit minutes, compare it with the current answer using the required order: smaller grandfather overlap first, then smaller (A), then later switching time.

### Why it works

For every fixed (A), the array (D[s]) exactly measures the change in grandfather overlap when a positive switching time moves from (s) to (s+1). The recurrence computes every such difference without scanning the holiday again, so the backwards cumulative sum evaluates every positive start exactly.

For non-positive starts, the garland state is periodic modulo (2A). Every phase is represented exactly once by either (p) or (p+A) for (0\le p<A). The difference (D[p]) is precisely the change between neighboring phases, and the two co

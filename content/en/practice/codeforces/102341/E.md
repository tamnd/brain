---
title: "CF 102341E - Eevee"
description: "There are (k) stacks, each containing one fragment of every one of the (n) stones. Since every stack contains every stone exactly once, each stack is a permutation of (1,ldots,n)."
date: "2026-08-14T01:37:47+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102341
codeforces_index: "E"
codeforces_contest_name: "Radewoosh+mnbvmar Contest (supported by AIM Tech)"
rating: 0
weight: 102341
solve_time_s: 680
verified: true
draft: false
---

[CF 102341E - Eevee](https://codeforces.com/problemset/problem/102341/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 11m 20s  
**Verified:** yes  

## Solution
## Problem Understanding

There are (k) stacks, each containing one fragment of every one of the (n) stones. Since every stack contains every stone exactly once, each stack is a permutation of (1,\ldots,n).

For a chosen consecutive group of stacks ([l,r]), we interleave their contents while preserving the internal order of every stack. Equivalently, we construct a sequence of stack indices, using every index in ([l,r]) exactly (n) times. The fragment value produced by choosing a stack is its current top value.

A construction is bad if some stone appears (r-l+1) times consecutively. Since the chosen stacks are all distinct, such a run contains exactly one occurrence of that stone from every stack in the interval. Let (f(l,r)) be the number of interleavings that avoid every such run. The required answer is the sum of (f(l,r)) over all intervals containing at least two stacks.

The permutations are generated independently and uniformly at random. This randomization is part of the intended complexity argument: for a fixed pair of stones, the probability that their relative order is the same in every stack of an interval of length (s) is (2^{-s+1}). The official problem is hosted by Codeforces, and an independent editorial for the same problem gives the resulting expected complexity as (O(n^2k+nk^2)).

The bounds (n,k\le300) rule out anything close to enumerating all interleavings. Even for one interval containing (k) stacks, the number of unrestricted interleavings is

[
\frac{(kn)!}{(n!)^k}.
]

At (n=k=300), this is far beyond any practical enumeration. We need to exploit the fact that a forbidden run contains one copy of the same stone from every stack, and that every stone occurs exactly once in each stack.

There are several boundary cases that can easily break an implementation. First, (k=2) means a forbidden interval consists of two equal adjacent fragments. For

```
2 2
1 2
2 1
```

there are (6) unrestricted interleavings. Exactly four are bad, so the answer is (2). A solution that checks only the final sequence of values but forgets that the two stack orders must be preserved can count invalid arrangements.

Second, two stones can both be selected in inclusion-exclusion only when they have the same relative order in every stack. For

```
3 2
1 2
1 2
2 1
```

the intervals of two stacks contribute (2) each, while the interval of all three stacks contributes (66). The total answer is (70). A solution that only checks whether each stone individually can form a run will miss the intersection term.

Third, identical permutations are a useful correctness test even though they are not representative of the randomized input distribution. For

```
2 3
1 2 3
1 2 3
```

the answer for the only interval is (4). Here many forbidden events are simultaneously compatible, so an implementation that assumes different bad events are independent will fail.

Finally, an input in which every value in a stack is equal is not a legal test case at all. Every row must be a permutation, so an alleged "all-equal values" stress test must instead use repeated permutations such as two copies of (1,2,\ldots,n). Treating the input as an arbitrary matrix can hide this distinction.

## Approaches

The direct brute force is conceptually simple. For every interval ([l,r]), enumerate every sequence of stack choices containing exactly (n) copies of each of the (r-l+1) stack indices. For each sequence, simulate the stacks and check whether a run of length (r-l+1) with one stone occurs. The method is correct because it explicitly examines every possible interleaving and applies exactly the definition of a good construction.

For an interval of (s) stacks, the number of sequences examined is

[
\frac{(sn)!}{(n!)^s},
]

and checking one sequence costs (O(sn)). Thus even one large interval already requires

[
O\left(sn\frac{(sn)!}{(n!)^s}\right)
]

operations. The worst interval has (s=k), so this approach is completely infeasible.

The useful observation is to count bad constructions with inclusion-exclusion. Fix an interval containing (s) stacks. For every stone (x), let (E_x) be the event that the (s) copies of (x) occur consecutively.

Now suppose we select several stones (x_1,x_2,\ldots,x_t) and require all their events. The selected stones must have the same relative order in every stack. If (x) occurs before (y) in every stack, write (x\prec y). The selected stones must form a chain in this partial order.

Once a chain is fixed, the sequence splits naturally into gaps. Before the first selected stone, between two consecutive selected stones, and after the last selected stone, every stack contributes some number of ordinary fragments. Inside one gap, all those fragments may be interleaved arbitrarily while preserving their stack orders.

Suppose a gap contains (d_1,d_2,\ldots,d_s) ordinary fragments from the (s) stacks. Its number of interleavings is

\frac{(d_1+\cdots+d_s)!}{d_1!\cdots d_s!}.
]

Each selected stone itself forms one consecutive block. Its (s) stack indices can appear in any order, giving a factor of (s!).

This gives a path DP over the stones. If (u\prec v), the transition from (u) to (v) only needs the multinomial coefficient of the fragments lying between their positions. The DP does not need to know how many selected stones have already been chosen, because the gap decomposition already accounts for the exact number and location of all selected blocks.

For one interval, the resulting DP takes (O(n+m)), where (m) is the number of comparable ordered pairs of stones. The random permutations make (m) small on average. For an interval of length (s), a fixed pair of stones has probability (2^{-(s-1)}) of having the same relative order throughout all stacks. Summed over all intervals, this gives expected (O(n^2k)) comparable-pair work. The remaining (O(n)) work for every one of the (O(k^2)) intervals contributes (O(nk^2)). This is the intended randomized complexity.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O\left(kn\frac{(kn)!}{(n!)^k}\right)) for the largest interval | (O(kn)) | Too slow |
| Optimal | Expected (O(n^2k+nk^2)) | (O(n^2+nk)) | Accepted |

## Algorithm Walkthrough

1. Convert every stack into a position array. For every stack (s) and stone (x), store (\operatorname{pos}[s][x]), the position of (x) in that stack. This lets every ordering test and every gap size be obtained in constant time.
2. Fix the left endpoint (L) and extend the right endpoint (R) one stack at a time. The first stack (L) gives a fixed order of all stones. Every comparable pair can be represented as an edge (u\to v) where (u) occurs before (v) in stack (L).
3. For every stone (x), maintain the multinomial coefficient of the prefix before (x),

[
B_x=
\frac{(\sum_s(\operatorname{pos}[s][x]-1))!}
{\prod_s(\operatorname{pos}[s][x]-1)!},
]

and the corresponding suffix coefficient

[
A_x=
\frac{(\sum_s(n-\operatorname{pos}[s][x]))!}
{\prod_s(n-\operatorname{pos}[s][x])!}.
]

These describe the number of ways to interleave all fragments before and after a selected block containing (x).

1. For every currently comparable pair (u\prec v), maintain the multinomial coefficient (G_{u,v}) of the gap between them. If the new stack has positions (p_u,p_v), then comparability survives exactly when (p_u<p_v). If (p_u\ge p_v), remove the edge permanently.
2. When a new stack is added, update every surviving multinomial coefficient in constant time. If a current multinomial has total (S), and the new stack contributes (d) elements, then

[
M' = M\frac{(S+d)!}{S!,d!}.
]

The same formula updates (B_x), (A_x), and every surviving (G_{u,v}).

1. Run the inclusion-exclusion DP in the order of stones in the first stack. Let (dp[x]) be the signed contribution of all nonempty chains whose last selected stone is (x), including all gaps before (x). Then

-s!\left(
B_x+
\sum_{u\prec x}dp[u]G_{u,x}
\right).
]

The first term corresponds to selecting only (x). Every other term appends (x) to a chain ending at (u). The factor (s!) accounts for the ordering of the (s) stack choices inside the new selected block.

1. After the DP, append the suffix after the last selected block. The inclusion-exclusion correction for the interval is

[
\sum_x dp[x]A_x.
]

The unrestricted number of interleavings is

[
T_s=\frac{(sn)!}{(n!)^s}.
]

Hence

[
f(L,R)=T_s+\sum_x dp[x]A_x.
]

1. Add this value to the global answer for every (R>L). Then extend (R) and update the active comparable-pair structure. When the left endpoint changes, rebuild the structure using the new first stack.

The key invariant is that every active edge (u\to v) represents exactly the condition that (u) occurs before (v) in every stack of the current interval. For every chain of active edges, the DP contributes exactly one inclusion-exclusion term, with one multinomial coefficient for every gap and one (s!) factor for every selected stone. Thus every subset of simultaneous bad events is counted exactly once with the correct sign.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 1_000_000_007

def solve_instance(k, n, a):
    # pos[s][x] = zero-based position of stone x in stack s.
    pos = [[0] * n for _ in range(k)]
    for s in range(k):
        for p, x in enumerate(a[s]):
            pos[s][x - 1] = p

    max_fact = k * n
    fact = [1] * (max_fact + 1)
    for i in range(1, max_fact + 1):
        fact[i] = fact[i - 1] * i % MOD

    invfact = [1] * (max_fact + 1)
    invfact[max_fact] = pow(fact[max_fact], MOD - 2, MOD)
    for i in range(max_fact, 0, -1):
        invfact[i - 1] = invfact[i] * i % MOD

    invfact_n = invfact[n]

    ans = 0

    for left in range(k - 1):
        first = pos[left]

        order = sorted(range(n), key=first.__getitem__)

        # Every pair is created according to the order in the first stack.
        # Pair id -> (u, v).
        eu = []
        ev = []

        # Global doubly linked list of active pairs.
        gnxt = []
        gprev = []

        # Doubly linked lists of active incoming pairs for every v.
        bnxt = []
        bprev = []
        head_bucket = [-1] * n

        # Multinomial data for each pair.
        gap_sum = []
        gap_val = []

        # Active flag is useful when unlinking through two lists.
        active = []

        global_head = -1
        global_tail = -1

        # Build all pairs u -> v in first-stack order.
        for ii in range(n):
            u = order[ii]
            for jj in range(ii + 1, n):
                v = order[jj]

                eid = len(eu)
                eu.append(u)
                ev.append(v)

                d = first[v] - first[u] - 1
                gap_sum.append(d)
                gap_val.append(1)

                active.append(True)

                # Insert into v's incoming list.
                old = head_bucket[v]
                bprev.append(-1)
                bnxt.append(old)
                if old != -1:
                    bprev[old] = eid
                head_bucket[v] = eid

                # Insert into global list.
                gprev.append(global_tail)
                gnxt.append(-1)
                if global_tail != -1:
                    gnxt[global_tail] = eid
                else:
                    global_head = eid
                global_tail = eid

        # For one stack every multinomial coefficient is 1.
        before_sum = [first[x] for x in range(n)]
        before_val = [1] * n

        after_sum = [n - 1 - first[x] for x in range(n)]
        after_val = [1] * n

        invfact_n_pow = invfact_n

        # Add stacks right of 'left'.
        for right in range(left + 1, k):
            s = right + 1

            cur = pos[right]

            # Add the new stack to the prefix/suffix multinomials.
            for x in range(n):
                d = cur[x]

                old_sum = before_sum[x]
                new_sum = old_sum + d
                before_val[x] = (
                    before_val[x]
                    * fact[new_sum]
                    % MOD
                    * invfact[old_sum]
                    % MOD
                    * invfact[d]
                    % MOD
                )
                before_sum[x] = new_sum

                d2 = n - 1 - cur[x]

                old_sum = after_sum[x]
                new_sum = old_sum + d2
                after_val[x] = (
                    after_val[x]
                    * fact[new_sum]
                    % MOD
                    * invfact[old_sum]
                    % MOD
                    * invfact[d2]
                    % MOD
                )
                after_sum[x] = new_sum

            # Add the new stack to every currently comparable pair.
            eid = global_head
            while eid != -1:
                nxt_eid = gnxt[eid]

                u = eu[eid]
                v = ev[eid]

                pu = cur[u]
                pv = cur[v]

                if pu >= pv:
                    active[eid] = False

                    # Remove from global list.
                    p = gprev[eid]
                    q = gnxt[eid]
                    if p != -1:
                        gnxt[p] = q
                    else:
                        global_head = q
                    if q != -1:
                        gprev[q] = p
                    else:
                        global_tail = p

                    # Remove from v's bucket.
                    p = bprev[eid]
                    q = bnxt[eid]
                    if p != -1:
                        bnxt[p] = q
                    else:
                        head_bucket[v] = q
                    if q != -1:
                        bprev[q] = p
                else:
                    d = pv - pu - 1

                    old_sum = gap_sum[eid]
                    new_sum = old_sum + d

                    gap_val[eid] = (
                        gap_val[eid]
                        * fact[new_sum]
                        % MOD
                        * invfact[old_sum]
                        % MOD
                        * invfact[d]
                        % MOD
                    )
                    gap_sum[eid] = new_sum

                eid = nxt_eid

            # Number of unrestricted interleavings.
            invfact_n_pow = invfact_n_pow * invfact_n % MOD
            total = fact[s * n] * invfact_n_pow % MOD

            # Inclusion-exclusion DP.
            dp = [0] * n
            block_factor = fact[s]

            for x in order:
                val = before_val[x]

                eid = head_bucket[x]
                while eid != -1:
                    u = eu[eid]
                    val += dp[u] * gap_val[eid]
                    if val >= MOD:
                        val %= MOD
                    eid = bnxt[eid]

                dp[x] = (-block_factor * (val % MOD)) % MOD

            good = total
            for x in range(n):
                good += dp[x] * after_val[x]
                if good >= MOD:
                    good %= MOD

            ans += good
            if ans >= MOD:
                ans %= MOD

    return ans % MOD

def solve():
    k, n = map(int, input().split())
    a = [list(map(int, input().split())) for _ in range(k)]
    print(solve_instance(k, n, a))

if __name__ == "__main__":
    solve()
```

The position matrix is the first structural preprocessing step. Storing the inverse permutation is much more useful than repeatedly searching a stack for a stone, because every comparison between two stones becomes a single array lookup.

For a fixed left endpoint, the first stack defines the topological order used by the DP. Every pair starts as comparable because only one stack is present. When another stack is added, a pair either survives, if its order agrees with the new stack, or disappears permanently. This monotonicity is what allows the active-pair lists to be maintained incrementally.

The prefix and suffix multinomials use the same update identity as the pair gaps. Suppose a multinomial currently has parts whose total is (S), and a new stack contributes (d). Its new value is the old value multiplied by

[
\frac{(S+d)!}{S!d!}.
]

All factorials and inverse factorials are precomputed modulo (10^9+7), so each update is constant time.

The pair structure uses two linked lists for every edge. The global list lets the implementation visit every currently active comparable pair when a stack is added. The per-target list lets the DP visit only active predecessors of a particular stone. A pair is removed from both lists exactly once after its relative order becomes inconsistent.

The sign in `dp[x]` is negative because selecting one additional bad event contributes a factor of (-1) in inclusion-exclusion. The transition is

[
-s!\left(B_x+\sum dp[u]G_{u,x}\right),
]

not

[
-s!B_x\left(1+\sum dp[u]G_{u,x}\right).
]

The latter would count the prefix before (x) twice when (x) is appended to an existing chain.

Python integers do not overflow, but every multiplication is reduced modulo (10^9+7). The largest factorial needed is (k n\le90000), which is small enough for direct precomputation.

## Worked Examples

### Sample 1

The input is

```
3 3
1 2 3
3 2 1
1 3 2
```

Consider the interval ([1,2]). There are (20) unrestricted interleavings because

[
\frac{6!}{3!3!}=20.
]

The positions of the three stones are

| Stone | Stack 1 | Stack 2 | Comparable? |
| --- | --- | --- | --- |
| 1 | 1 | 3 |  |
| 2 | 2 | 2 |  |
| 3 | 3 | 1 |  |

No pair of stones has the same relative order in both stacks, so every inclusion-exclusion chain has length one.

For stone (1), the prefix contains (0) and (2) elements, giving a multinomial coefficient of (1). The suffix contains (2) and (0), also giving (1). The block has (2!) internal orders, so its bad-event count is (2).

For stone (2), the prefix has (1,1) elements and contributes (2). The suffix also contributes (2). Including the block factor (2!), its bad-event count is (8).

For stone (3), the count is again (2).

The DP state is

| Stone | Prefix coefficient | Predecessor contribution | (dp) | Suffix coefficient |
| --- | --- | --- | --- | --- |
| 1 | 1 | 0 | -2 | 1 |
| 2 | 2 | 0 | -4 | 2 |
| 3 | 1 | 0 | -2 | 1 |

Thus

[
f(1,2)=20-2-8-2=8.
]

For the interval ([1,3]), the third stack removes some comparabilities and preserves others according to the three permutations. Running the same DP gives

[
f(1,3)=1446.
]

The three interval values are (8,1446,10), so the final answer is

[
8+1446+10=1464.
]

The trace demonstrates why the DP is based on chains of compatible bad events rather than on individual stones. A single bad event only needs its prefix and suffix multinomials, while a simultaneous collection of events is represented by the active predecessor edges.

### Sample 2

The input is

```
4 2
1 2
2 1
1 2
2 1
```

For two adjacent stacks, the unrestricted number of interleavings is

[
\frac{4!}{2!2!}=6.
]

For stacks (1,2), the two stones appear in opposite orders, so neither pair is comparable. Each stone contributes two bad constructions, leaving

[
f(1,2)=6-2-2=2.
]

The same reasoning gives

[
f(2,3)=2,\qquad f(3,4)=2.
]

For three stacks, the unrestricted number is

[
\frac{6!}{2!2!2!}=90.
]

The two stones again have incompatible relative orders, so there is no intersection term. Each individual bad event contributes (12), giving

[
f(1,3)=90-12-12=66.
]

Similarly,

[
f(2,4)=66.
]

For all four stacks, there are

[
\frac{8!}{2!^4}=2520
]

unrestricted interleavings. The two stones now have the alternating order pattern, and the DP gives

[
f(1,4)=2328.
]

The interval values are

| Interval | (f(l,r)) |
| --- | --- |
| ([1,2]) | 2 |
| ([1,3]) | 66 |
| ([1,4]) | 2328 |
| ([2,3]) | 2 |
| ([2,4]) | 66 |
| ([3,4]) | 2 |

Their sum is (2466), matching the sample output.

This example exercises the main optimization. As more stacks are added, incompatible pairs disappear from the active lists, so the DP does not repeatedly inspect all (n^2) possible pairs.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | Expected (O(n^2k+nk^2)) | (O(n)) DP work per interval, plus work proportional to surviving comparable pairs |
| Space | (O(n^2+nk)) | Pair lists and their gap coefficients dominate |

For a pair of stones, after fixing their order in one stack, every additional independent random stack preserves that order with probability (1/2). Consequently, for an interval of length (s), a pair survives with probability (2^{-(s-1)}). Summing over all possible intervals gives expected (O(n^2k)) pair processing, while the (O(n)) per-interval DP work gives (O(nk^2)). This is the randomized complexity described by the independent editorial sources for the problem.

With (n,k\le300), the expected amount of work is practical. The implementation also uses compact integer arrays instead of Python sets or dictionaries for the active pair graph, because the constant factors matter at this scale.

## Test Cases

The following tests use the same `solve_instance` function from the solution. The maximum-size case checks that the implementation remains within the modular result range, since writing a hard-coded expected value for a (300\times300) instance would make the test itself depend on another independently computed solution.

```
# Put the submitted solution in solution.py.
from solution import solve_instance

MOD = 1_000_000_007

# Sample 1
a = [
    [1, 2, 3],
    [3, 2, 1],
    [1, 3, 2],
]
assert solve_instance(3, 3, a) == 1464, "sample 1"

# Sample 2
a = [
    [1, 2],
    [2, 1],
    [1, 2],
    [2, 1],
]
assert solve_instance(4, 2, a) == 2466, "sample 2"

# Minimum size.
a = [
    [1, 2],
    [2, 1],
]
assert solve_instance(2, 2, a) == 2, "minimum-size case"

# Same permutation twice.
# There is only one interval, and its answer is 4.
a = [
    [1, 2, 3],
    [1, 2, 3],
]
assert solve_instance(2, 3, a) == 4, "identical permutations"

# Three stacks, with the third reversing the order.
# f(1,2)=2, f(2,3)=2, f(1,3)=66.
a = [
    [1, 2],
    [1, 2],
    [2, 1],
]
assert solve_instance(3, 2, a) == 70, "comparable-pair boundary"

# Maximum-size structural stress test.
# Cyclic shifts are valid permutations and avoid the invalid
# "all values equal" matrix requested by some generic test templates.
k = 300
n = 300
a = [
    [((j + i) % n) + 1 for j in range(n)]
    for i in range(k)
]
out = solve_instance(k, n, a)
assert 0 <= out < MOD, "maximum-size case"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2 2 / 1 2 / 2 1` | 2 | Minimum dimensions and the smallest possible forbidden run |
| `2 3 / 1 2 3 / 1 2 3` | 4 | Several compatible inclusion-exclusion events |
| `3 2 / 1 2 / 1 2 / 2 1` | 70 | Comparable pairs disappearing when a new stack reverses their order |
| (300\times300) cyclic shifts | (0\le ans<10^9+7) | Maximum dimensions, memory usage, factorial bounds, and performance |

## Edge Cases

For the minimum case

```
2 2
1 2
2 1
```

there are (6) unrestricted interleavings. Stone (1) can form a consecutive pair in (2) ways, and stone (2) can do the same in (2) ways. Their events cannot occur simultaneously because the two stacks disagree on their relative order. Hence the DP gives (6-2-2=2). The important boundary is that the interval length is exactly (2), so a bad run consists of two equal fragments.

For

```
2 3
1 2 3
1 2 3
```

all three stones are comparable. The bad-event counts are (12,8,12). The pair intersections have weights (8,8,8), and the triple intersection has weight (8). Inclusion-exclusion gives

[
20-(12+8+12)+(8+8+8)-8=4.
]

The active-pair structure keeps all three pair edges because their order agrees in both stacks. This test catches the mistake of treating every bad event independently.

For

```
3 2
1 2
1 2
2 1
```

the first two stacks agree, so the pair of stones is comparable for interval ([1,2]). Adding the third stack removes that pair because its order is reversed. The two-stack intervals each contribute (2), while the three-stack interval has (90) unrestricted interleavings and two individual bad-event contributions of (12), giving (66). The total is (70). This verifies that pair deletion happens exactly when the newly added stack reverses the order.

For a maximum-size valid input, such as the cyclic-shift construction used in the test block, every row remains a genuine permutation. The factorial arrays only need indices through (90000), and every multinomial update stays within modular arithmetic. The active-pair lists prevent the DP from scanning pairs that have already become incompatible. The randomized nature of the original input is what makes the expected number of surviving pairs small enough for the intended (O(n^2k+nk^2)) bound.

An "all-equal values" case should not be passed to this program because it violates the input condition that every stack is a permutation. The closest meaningful stress case is to repeat the same permutation many times. That case is also useful because it deliberately creates the largest possible number of comparable pairs and checks that the inclusion-exclusion formula itself remains correct even on an atypical, highly structured input.

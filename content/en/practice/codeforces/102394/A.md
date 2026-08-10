---
title: "CF 102394A - Artful Paintings"
description: "We have a row of (N) cubes, and each cube is either painted or left untouched. A type 1 rule requires at least (K) painted cubes inside a particular interval ([L,R]). A type 2 rule requires at least (K) painted cubes outside that interval."
date: "2026-08-11T04:16:34+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102394
codeforces_index: "A"
codeforces_contest_name: "The 2019 China Collegiate Programming Contest Harbin Site"
rating: 0
weight: 102394
solve_time_s: 352
verified: true
draft: false
---

[CF 102394A - Artful Paintings](https://codeforces.com/problemset/problem/102394/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 5m 52s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a row of (N) cubes, and each cube is either painted or left untouched. A type 1 rule requires at least (K) painted cubes inside a particular interval ([L,R]). A type 2 rule requires at least (K) painted cubes outside that interval.

The goal is not to construct a painting explicitly. We only need the minimum possible number of painted cubes that satisfies every rule. The official problem has (N\le 3000), (M_1,M_2\le3000), and the sums of these quantities over all test cases are also at most (3000). The original problem has a 1 second time limit and 512 MB memory limit.

The natural representation is a prefix sum. Let (S_i) be the number of painted cubes among positions (1,\ldots,i). Then painting position (i) corresponds to increasing the prefix sum by either zero or one:

[
0\le S_i-S_{i-1}\le1.
]

For a type 1 rule, the number painted in ([L,R]) is (S_R-S_{L-1}), so the rule becomes

[
S_R-S_{L-1}\ge K.
]

For a type 2 rule, the number painted outside ([L,R]) is

[
S_N-(S_R-S_{L-1}),
]

so the rule becomes

[
S_N-(S_R-S_{L-1})\ge K.
]

The troublesome part is (S_N), because it is itself the quantity we want to minimize. Once (S_N) is fixed to some value (X), every constraint becomes a difference constraint involving only two prefix sums. That is the central observation.

The size (N=3000) rules out anything exponential in (N). Even enumerating all paintings would require (2^{3000}) candidates. At the other extreme, an (O(N^3)) method would already involve around (27) billion basic operations in the largest single case, so the intended solution needs to exploit the sparse interval structure. The accepted approach uses (O(\log N)) feasibility checks, each based on a sparse graph with (O(N+M_1+M_2)) edges.

There are several edge cases that are easy to mishandle. If there are no rules at all, the answer is zero, because painting nothing is valid. For example,

```
1
1 0 0
```

has answer

```
0
```

A careless implementation that always paints at least one cube would fail immediately.

A rule can have (K=0), which places no actual requirement on the painting. For example,

```
1
3 1 0
1 3 0
```

has answer

```
0
```

The prefix-sum inequalities must allow equality in this case.

The boundaries (L=1) and (R=N) also matter because they involve (S_0) or (S_N). For example,

```
1
1 1 0
1 1 1
```

requires cube 1 to be painted, so the answer is (1). Forgetting the prefix position (S_0) would make the interval formula awkward and often introduces an off-by-one error.

A type 2 rule on the whole array is another useful boundary case. Its outside set is empty, so its only valid requirement is (K=0). For example,

```
1
3 0 1
1 3 0
```

has answer (0). Treating the complement as another ordinary interval would be incorrect.

## Approaches

The brute-force approach is straightforward. Try every subset of the (N) cubes, count how many cubes it paints, and check every rule. Since there are (2^N) subsets and checking a subset directly against all rules costs (O(N+M_1+M_2)), the worst-case work is

[
O\left(2^N(N+M_1+M_2)\right).
]

For (N=3000), this is roughly (6000\cdot2^{3000}) basic checks in a large case, which is completely infeasible.

The brute force works because every possible painting is explicitly represented, so there is no question about correctness. The problem is that the interesting structure is hidden by the exponential enumeration.

The first useful observation is to replace the individual painted-cube decisions by prefix sums. Once (S_i) is known, the number of painted cubes in any interval is just a difference of two prefix sums. The binary nature of each cube is also captured by the simple inequalities

[
S_i-S_{i-1}\ge0
]

and

[
S_i-S_{i-1}\le1.
]

Now suppose the final number of painted cubes is fixed to (X=S_N). A type 1 rule becomes

[
S_{L-1}-S_R\le-K.
]

A type 2 rule becomes

[
S_R-S_{L-1}\le X-K.
]

The total number is fixed by

[
S_N-S_0=X,
]

which can be represented by the two inequalities

[
S_N-S_0\le X
]

and

[
S_0-S_N\le-X.
]

Every resulting constraint has the standard form

[
S_v\le S_u+w.
]

Such systems are called difference constraints. They can be represented by a directed edge (u\to v) with weight (w). A feasible system has no negative cycle, and conversely, if the constraint graph has no negative cycle, shortest-path distances provide a feasible assignment.

This leaves one question: how do we find the smallest feasible (X)? Feasibility is monotone. If a painting with (X) painted cubes satisfies every rule, paint one additional unpainted cube. A type 1 count can only increase. For a type 2 rule, the number of painted cubes outside its interval either stays unchanged, when the new cube is inside the interval, or increases, when the new cube is outside. Thus every larger number of painted cubes is also feasible.

We can consequently binary search (X) from (0) to (N). For each candidate (X), we build the corresponding difference-constraint graph and use SPFA to check whether it contains a negative cycle. The official editorial gives exactly this binary-search plus SPFA formulation, with (O(NM\log N)) complexity when (M) denotes the number of constraints.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(2^N(N+M_1+M_2))) | (O(N+M_1+M_2)) | Too slow |
| Binary Search + SPFA | (O(N(N+M_1+M_2)\log N)) worst case | (O(N+M_1+M_2)) | Accepted |

SPFA itself has the same (O(VE)) worst-case bound as Bellman-Ford, although the queue-based implementation is much faster on the sparse graphs arising here. The official editorial explicitly relies on SPFA's practical pruning for the accepted (O(NM\log N)) solution.

## Algorithm Walkthrough

1. Define (S_i) as the number of painted cubes among positions (1) through (i). The value (S_0) is zero, and (S_N) is exactly the number of painted cubes.
2. Fix a candidate answer (X). We temporarily require (S_N=X). The reason for doing this is that every rule containing (S_N) then becomes an ordinary difference constraint with a constant right-hand side.
3. Add the two constraints
[
S_{i-1}-S_i\le0
]
and
[
S_i-S_{i-1}\le1
]
for every position (i). These force each difference (S_i-S_{i-1}) to be either zero or one, exactly matching an unpainted or painted cube.
4. Convert every type 1 rule ((L,R,K)) into
[
S_{L-1}-S_R\le-K.
]
This is just the original condition (S_R-S_{L-1}\ge K) with the terms rearranged.
5. Convert every type 2 rule ((L,R,K)) into
[
S_R-S_{L-1}\le X-K.
]
Starting from (X-(S_R-S_{L-1})\ge K), this says that the number painted inside the interval cannot exceed (X-K).
6. Force the total to equal (X) by adding
[
S_N-S_0\le X
]
and
[
S_0-S_N\le-X.
]
Together these give (S_N-S_0=X), and (S_0=0).
7. Turn every inequality (S_v-S_u\le w) into a directed edge (u\to v) with weight (w). A path relaxation then has exactly the same form as the original inequality:
[
S_v\le S_u+w.
]
8. Run SPFA to search for a negative cycle. The graph contains all relevant vertices reachable from vertex (0) because the prefix-sum edges include a forward edge from (i-1) to (i). If a negative cycle exists, the candidate (X) is impossible. If there is no negative cycle, the difference-constraint system has a solution, so (X) is feasible.
9. Binary search the smallest feasible (X). Start with the range ([0,N]). The upper endpoint is always feasible because painting every cube satisfies every rule allowed by the input bounds. When the midpoint is feasible, search the lower half. Otherwise search the upper half.

### Why it works

For a fixed (X), the graph represents exactly the possible prefix sums of a painting with (X) painted cubes. Every valid painting satisfies every graph inequality, so it cannot create a negative cycle. Conversely, if the graph has no negative cycle, shortest-path distances satisfy every difference constraint, and the constraints (0\le S_i-S_{i-1}\le1) make each prefix difference an integer in ({0,1}). Hence those differences describe an actual painting. The two constraints involving (S_N) force its total number of painted cubes to be exactly (X). Since feasibility is monotone in (X), binary search returns the smallest possible number.

## Python Solution

```python
import sys
from collections import deque

input = sys.stdin.readline

def solve():
    input = sys.stdin.readline
    t = int(input())
    answers = []

    for _ in range(t):
        n, m1, m2 = map(int, input().split())

        type1 = [tuple(map(int, input().split())) for _ in range(m1)]
        type2 = [tuple(map(int, input().split())) for _ in range(m2)]

        def feasible(x):
            g = [[] for _ in range(n + 1)]

            # 0 <= S[i] - S[i-1] <= 1
            for i in range(1, n + 1):
                g[i].append((i - 1, 0))
                g[i - 1].append((i, 1))

            # S[L-1] - S[R] <= -K
            for l, r, k in type1:
                g[r].append((l - 1, -k))

            # S[R] - S[L-1] <= X - K
            for l, r, k in type2:
                g[l - 1].append((r, x - k))

            # S[N] - S[0] <= X
            # S[0] - S[N] <= -X
            g[0].append((n, x))
            g[n].append((0, -x))

            # SPFA, starting from 0.
            # The chain edges make every vertex reachable from 0.
            vcnt = n + 1
            dist = [0] * vcnt
            in_queue = [False] * vcnt
            relax_count = [0] * vcnt

            q = deque([0])
            in_queue[0] = True
            relax_count[0] = 1

            while q:
                u = q.popleft()
                in_queue[u] = False
                du = dist[u]

                for v, w in g[u]:
                    nd = du + w
                    if nd < dist[v]:
                        dist[v] = nd

                        if not in_queue[v]:
                            q.append(v)
                            in_queue[v] = True
                            relax_count[v] += 1

                            if relax_count[v] >= vcnt:
                                return False

            return True

        lo, hi = 0, n

        while lo < hi:
            mid = (lo + hi) // 2
            if feasible(mid):
                hi = mid
            else:
                lo = mid + 1

        answers.append(str(lo))

    return "\n".join(answers)

if __name__ == "__main__":
    sys.stdout.write(solve())
```

The input is read case by case, and the two kinds of constraints are stored separately because their graph edges have different dependence on the binary-search value (X).

Inside `feasible`, the graph has (N+1) vertices, numbered from (0) to (N), corresponding directly to (S_0,\ldots,S_N). For each position, the edge (i\to i-1) with weight zero represents (S_{i-1}\le S_i), while (i-1\to i) with weight one represents (S_i\le S_{i-1}+1). Together they enforce a binary increment.

The type 1 edge is `g[r].append((l - 1, -k))`. Its relaxation condition is (S_{L-1}\le S_R-K), which is exactly the required lower bound on the interval.

The type 2 edge is reversed compared with type 1. Its weight is `x - k`, because fixing (S_N=X) transforms the outside-count condition into (S_R\le S_{L-1}+X-K).

The final two edges are both necessary. Using only `0 -> n` would give (S_N\le X), while using only `n -> 0` would give (S_N\ge X). Their combination fixes the total exactly.

The SPFA distance array can start with all zeros if every vertex is considered reachable, but this implementation starts only from vertex zero. That is safe because the forward prefix edges give a path from zero to every vertex. A negative cycle reachable from any vertex is consequently reachable from zero as well.

The relaxation counter detects a negative cycle before SPFA can continue indefinitely. In a graph with (V) vertices and no negative cycle, shortest paths do not require a repeatedly improving path containing at least (V) edges. A vertex being relaxed that many times signals a negative cycle.

Python integers remove any overflow concern. The largest values involved are only on the order of (N), although the accumulated shortest-path distances can be negative.

The binary search uses `hi = n` because painting all (N) cubes always satisfies every rule. The input bounds guarantee that a type 1 requirement never asks for more than the interval length, and a type 2 requirement never asks for more than the size of its complement.

## Worked Examples

### Sample 1

The actual sample contains one test case:

```
1
3 1 1
1 2 1
2 2 1
```

The first rule requires at least one painted cube among positions 1 and 2. The second rule requires at least one painted cube outside position 2, so either position 1 or position 3 must be painted.

The binary search behaves as follows.

| `lo` | `hi` | `mid` | Candidate interpretation | Feasible? |
| --- | --- | --- | --- | --- |
| 0 | 3 | 1 | Paint exactly 1 cube | Yes |
| 0 | 1 | 0 | Paint exactly 0 cubes | No |

For (X=1), painting cube 1 works. It satisfies the first rule because cube 1 lies in ([1,2]), and it satisfies the second rule because cube 1 lies outside ([2,2]). Thus the answer is 1. The official statement gives this same sample and output.

### Sample 2

Consider the following case:

```
1
5 1 1
2 4 2
2 4 1
```

The type 1 rule requires at least two painted cubes in positions 2 through 4. The type 2 rule requires at least one painted cube outside positions 2 through 4, so at least one of positions 1 and 5 must also be painted.

The binary search is:

| `lo` | `hi` | `mid` | Candidate interpretation | Feasible? |
| --- | --- | --- | --- | --- |
| 0 | 5 | 2 | Exactly 2 painted cubes | No |
| 3 | 5 | 4 | Exactly 4 painted cubes | Yes |
| 3 | 4 | 3 | Exactly 3 painted cubes | Yes |

With only two painted cubes, both must lie in positions 2 through 4 to satisfy the first rule, leaving no painted cube outside that interval. Thus (X=2) is impossible. With three painted cubes, positions 1, 2, and 3 work, so the answer is 3.

This example demonstrates why simply taking the largest required interval count is not sufficient. The two rule types interact through the total number of painted cubes.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(N(N+M_1+M_2)\log N)) worst case | There are (O(\log N)) feasibility checks, each SPFA check has (O(VE)) worst-case complexity with (V=O(N)) and (E=O(N+M_1+M_2)). |
| Space | (O(N+M_1+M_2)) | The graph, distances, queue state, and constraint arrays all have linear size. |

The official editorial gives the same (O(NM\log N)) bound for the binary-search plus SPFA approach and observes that the SPFA pruning is sufficient for the contest limits. Since the sums of (N), (M_1), and (M_2) over all test cases are each bounded by 3000, the total input is substantially smaller than treating every test case as an independent worst-case instance.

## Test Cases

The statement excerpt in the question is missing the leading `1` from the actual sample input. The complete official sample is the one used below.

The following tests assume the submitted solution is saved as `solution.py`.

```python
from solution import solve
import sys
import io

def run(inp: str) -> str:
    old_stdin = sys.stdin
    sys.stdin = io.StringIO(inp)
    try:
        return solve().strip()
    finally:
        sys.stdin = old_stdin

# Official sample
assert run(
    """1
3 1 1
1 2 1
2 2 1
"""
) == "1", "official sample"

# Minimum-size input, no constraints.
assert run(
    """1
1 0 0
"""
) == "0", "empty constraint set"

# Boundary condition L = R = 1, type 1 forces the only cube to be painted.
assert run(
    """1
1 1 0
1 1 1
"""
) == "1", "single-cube type 1"

# Type 2 complement at the boundary.
# Outside [1, 1] are positions 2, 3, 4, so two of them must be painted.
assert run(
    """1
4 0 1
1 1 2
"""
) == "2", "left boundary complement"

# Several identical constraints.
assert run(
    """1
4 3 0
1 4 2
1 4 2
1 4 2
"""
) == "2", "duplicate constraints"

# Interaction between type 1 and type 2 constraints.
assert run(
    """1
5 1 1
2 4 2
2 4 1
"""
) == "3", "inside and outside requirements"

# Maximum-size case: N = 3000 and 3000 constraints.
# Every identical type 1 rule requires all 3000 cubes.
n = 3000
max_case = "1\n{} 3000 0\n".format(n)
max_case += ("1 3000 3000\n" * 3000)
assert run(max_case) == "3000", "maximum-size input"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 1 0 0` | `0` | Minimum-size case and zero constraints |
| `1 / 1 1 0 / 1 1 1` | `1` | (L=R=1) and (S_0) boundary handling |
| `1 / 4 0 1 / 1 1 2` | `2` | Complement interval at the left boundary |
| `1 / 4 3 0 / 1 4 2` repeated | `2` | Duplicate and identical constraints |
| `1 / 5 1 1 / 2 4 2 / 2 4 1` | `3` | Interaction between interval and complement requirements |
| `N=3000`, 3000 identical rules | `3000` | Maximum (N) and maximum constraint count |

## Edge Cases

When there are no rules, the graph contains only the prefix-difference constraints and the fixed-total constraints. For

```
1
1 0 0
```

the candidate (X=0) produces (S_0=S_1=0), so there is no negative cycle and the binary search returns zero. The algorithm never assumes that at least one cube must be painted.

When a rule has (K=0), its graph edge has weight zero and imposes no additional restriction beyond one already implied by the prefix structure. For

```
1
3 1 0
1 3 0
```

the candidate (X=0) is feasible, giving the correct answer zero.

For a single cube with a type 1 requirement,

```
1
1 1 0
1 1 1
```

the constraint becomes (S_0-S_1\le-1), while the binary prefix constraints give (S_1-S_0\le1) and (S_0-S_1\le0). The only possible value is (S_1=1), so the answer is one. This exercises the (L-1=0) boundary directly.

For a type 2 boundary case,

```
1
4 0 1
1 1 2
```

the outside of ([1,1]) consists of positions 2, 3, and 4. The rule asks for two painted cubes there, so two cubes are sufficient and necessary. In the graph, the rule becomes (S_1-S_0\le X-2), which is the correct conversion of the complement condition.

The most subtle case is when interval and complement requirements pull in opposite directions. In

```
1
5 1 1
2 4 2
2 4 1
```

two cubes must be painted inside positions 2 through 4, while another painted cube must be outside. The minimum is consequently three. Testing (X=2) creates an inconsistent difference-constraint system, so SPFA finds a negative cycle. Testing (X=3) removes that contradiction, and binary search stops there.

Finally, larger (X) values are always safe once some (X) is feasible. Adding another painted cube cannot hurt a type 1 condition, because its interval count can only increase. For a type 2 condition, its outside count either remains unchanged or increases. This monotonicity is exactly what makes binary search valid rather than merely heuristic.

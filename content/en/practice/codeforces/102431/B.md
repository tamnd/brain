---
title: "CF 102431B - Infimum of Paths"
description: "Each directed edge carries one decimal digit from 0 through 9. A path is interpreted as a decimal fraction from left to right, but each new digit is divided by another factor of 10. For example, a path with edge weights 3, 1, 3 has value [ frac{3+frac{1+frac{3}{10}}{10}}{10}=0."
date: "2026-08-08T23:47:23+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102431
codeforces_index: "B"
codeforces_contest_name: "2019 China Collegiate Programming Contest Final (CCPC-Final 2019)"
rating: 0
weight: 102431
solve_time_s: 552
verified: true
draft: false
---

[CF 102431B - Infimum of Paths](https://codeforces.com/problemset/problem/102431/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 9m 12s  
**Verified:** yes  

## Solution
## Problem Understanding

Each directed edge carries one decimal digit from 0 through 9. A path is interpreted as a decimal fraction from left to right, but each new digit is divided by another factor of 10. For example, a path with edge weights `3, 1, 3` has value

[
\frac{3+\frac{1+\frac{3}{10}}{10}}{10}=0.313.
]

The task is to find the greatest lower bound of the values of all paths from vertex `0` to vertex `1`. The distinction between minimum and infimum matters because repeatedly traversing a cycle can produce values approaching a limit that no finite path actually reaches. The answer is printed modulo (10^9+7). The official problem uses an 8 second time limit and 256 MB of memory.

The bounds are small enough to allow roughly quadratic work in the number of vertices. With (n\le 2000), an (O(n^2)) or (O(nm)) method is reasonable, especially because the total number of vertices over all test cases is at most 20000 and the total number of edges is at most 40000. An approach that enumerates paths is completely different: cycles mean there can be infinitely many paths, and even restricting attention to paths of some fixed length (L) can produce exponentially many walks.

There are several traps that make a straightforward shortest-path implementation incorrect. First, ordinary numeric edge-weight minimization is not the objective. For

```
2 1
0 1 9
```

the only path has value (0.9), so the answer is (9/10), which is `300000003` modulo (10^9+7). A Dijkstra-style sum of edge weights would report 9, which is a different problem.

Second, the infimum need not be attained. Consider

```
3 3
0 2 1
2 2 1
2 1 9
```

The finite paths have values (0.19), (0.119), (0.1119), and so on. Their infimum is

[
0.11111\ldots=\frac19,
]

whose modular value is `111111112`. A solution that only searches for a finite minimum path misses the actual answer.

Third, a zero-weight cycle that cannot reach vertex 1 must not influence the answer. For example,

```
4 4
0 2 3
2 1 4
0 3 0
3 3 0
```

has answer (0.34=17/50), which is `380000003` modulo (10^9+7). The zero cycle at vertex 3 looks attractive, but it can never be completed to vertex 1, so it is irrelevant.

Finally, several edges with the same smallest digit can require comparing their suffixes. For

```
4 4
0 2 1
0 3 1
2 1 9
3 1 2
```

both first digits are 1, so the decision must be made using the next digit. The optimal value is (0.12=3/25), giving `840000006` modulo (10^9+7).

## Approaches

A brute-force solution would enumerate paths from vertex 0, compute their decimal values, and keep the smallest one. This is not merely inefficient, it also has no natural stopping point because a useful cycle may be traversed arbitrarily many times. In a graph with branching factor (b), enumerating all walks of length (L) already takes (\Theta(b^L)) work. With as many as 4000 edges, even a bound such as (L=2000) gives an astronomical number of candidates. Restricting the search to simple paths does not solve the problem either, because the infimum may be approached by paths that repeat a cycle.

The key observation is that decimal comparison is lexicographic. The first digit where two paths differ completely determines which value is smaller. We can consequently think of the answer as an infinite sequence of digits. Once a finite path reaches vertex 1, we can imagine appending a zero-weight self-loop at vertex 1 forever. Its infinite digit sequence represents exactly the same finite decimal value. Conversely, every vertex that can reach 1 can serve as a prefix of some valid finite path. Thus the original infimum is equivalent to finding the lexicographically smallest infinite digit sequence that can be generated from vertex 0 after adding a zero self-loop at vertex 1. This is the central transformation used by the official solution.

Vertices that cannot reach vertex 1 can be discarded immediately. Among the remaining vertices, only minimum-weight outgoing edges matter. If a vertex has an outgoing edge of weight 2 and another of weight 5, no optimal infinite sequence starting there can use the 5-edge, because the first digit would already be larger.

There can still be several minimum-weight edges. At some position we may have several vertices capable of producing the same smallest digit, so we keep all of them as a candidate set. At the next position we again choose the smallest digit available from any candidate. Repeating this point-set process constructs the lexicographically smallest digit sequence without enumerating paths.

The sequence eventually becomes periodic. The relevant finite graph has only (n) vertices, so an optimal infinite walk consists conceptually of a finite prefix followed by a cycle. Two possible prefix-plus-cycle structures whose lengths are at most (n) can be distinguished within the sum of their lengths, which gives the standard (3n)-digit bound used by the official solution. We generate (3n) digits and search the substring beginning at position (n) for its smallest period. The official editorial describes exactly this point-set iteration and the (3n) bound.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential in path length | Exponential in path length | Too slow |
| Point-set iteration | (O(nm+n^2)) | (O(n+m)) | Accepted |

The (n^2) term comes from finding the period by testing candidate cycle lengths. Since (m\le 4000) and (n\le 2000), the bounds are suitable for the given limits.

## Algorithm Walkthrough

1. Build the reverse graph and run a graph search from vertex 1. Mark every vertex that can eventually reach 1. Any edge touching an unmarked vertex can be ignored, because no valid path can use it.
2. Add a conceptual edge (1\to1) with weight 0. This converts stopping at vertex 1 into continuing forever with zero digits. It lets us reason entirely about infinite sequences instead of having separate cases for finite paths and paths that approach an infimum through a cycle.
3. For every remaining vertex, find its minimum outgoing edge weight and retain all destinations reached by edges having exactly that weight. Larger outgoing weights can never be part of the lexicographically smallest continuation because they lose at the first digit where they are used.
4. Start with the candidate set (S={0}). For the next digit, inspect every vertex in (S) and find the smallest minimum outgoing weight among them. Call this digit (d). Append (d) to the answer string.
5. Replace (S) by all destinations of minimum-weight edges from vertices in the old (S) whose minimum weight was exactly (d). We keep every tied destination because two paths can share the current prefix while having different future suffixes.
6. Repeat the previous two steps (3n) times. The resulting string contains enough information to identify the ultimately periodic tail of the optimal infinite decimal sequence. The official solution uses this (3n)-step construction and searches the part from position (n) onward for the smallest cycle.
7. Let (p) be the smallest positive integer at most (n) such that the substring from position (n) through position (3n-1) repeats every (p) positions. We deliberately use position (n) as the start of the periodic representation even if the true prefix becomes periodic earlier. Extending the prefix into the periodic part does not change the represented number.
8. Let (P) be the integer represented by the first (n) digits and let (C) be the integer represented by the next (p) digits. The infinite decimal is

[
\frac{P}{10^n}
+
\frac{C}{10^n(10^p-1)}.
]

This formula is just the geometric series for repeatedly appending the (p)-digit block (C).

1. Compute the expression modulo (10^9+7). Since the modulus is prime and all required denominators are nonzero for the relevant lengths, modular inverses can be obtained with Fermat's little theorem.

### Why it works

After removing vertices that cannot reach 1, every candidate prefix can be completed into a valid path to 1. Appending the zero self-loop at 1 means finite paths and their infinite zero-padded versions have exactly the same numeric value. Comparing such decimal values is equivalent to lexicographically comparing their digit sequences.

At every position, the algorithm chooses the smallest digit that any currently optimal prefix can produce. Any sequence beginning with a larger digit is immediately worse, while all sequences beginning with the chosen digit remain represented in the new candidate set. This gives the invariant that after (i) iterations, the generated (i)-digit string is the lexicographically smallest possible prefix among all valid continuations.

Because the graph is finite, an optimal infinite continuation can be represented by a finite prefix followed by a cycle. The official (3n)-digit argument guarantees that the periodic part can be identified from the generated string. Once its period is known, the geometric-series formula gives exactly the infimum, including cases where no finite path attains it.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 10**9 + 7

def solve_case(n, m, edges):
    # Reverse graph for finding vertices that can reach 1.
    rev = [[] for _ in range(n)]
    for u, v, w in edges:
        rev[v].append(u)

    good = [False] * n
    good[1] = True
    stack = [1]

    while stack:
        v = stack.pop()
        for u in rev[v]:
            if not good[u]:
                good[u] = True
                stack.append(u)

    # For every useful vertex, keep only minimum-weight outgoing edges
    # whose destinations are also useful.
    min_w = [10] * n
    nxt = [[] for _ in range(n)]

    for u, v, w in edges:
        if not good[u] or not good[v]:
            continue

        if w < min_w[u]:
            min_w[u] = w
            nxt[u] = [v]
        elif w == min_w[u]:
            nxt[u].append(v)

    # The added 1 -> 1 edge of weight zero.
    if good[1]:
        if min_w[1] > 0:
            min_w[1] = 0
            nxt[1] = [1]
        elif min_w[1] == 0:
            nxt[1].append(1)

    # Point-set iteration.
    # cur contains all vertices that can realize the currently
    # smallest prefix.
    cur = {0}
    digits = []

    for _ in range(3 * n):
        d = 10

        for u in cur:
            if min_w[u] < d:
                d = min_w[u]

        digits.append(d)

        new_cur = set()
        for u in cur:
            if min_w[u] == d:
                new_cur.update(nxt[u])

        cur = new_cur

    # Find the smallest period of digits[n:3*n].
    period = None
    for p in range(1, n + 1):
        ok = True
        for i in range(n, 3 * n - p):
            if digits[i] != digits[i + p]:
                ok = False
                break
        if ok:
            period = p
            break

    # The first n digits are the prefix.
    prefix = 0
    for i in range(n):
        prefix = (prefix * 10 + digits[i]) % MOD

    # The next 'period' digits form the repeating block.
    cycle = 0
    for i in range(n, n + period):
        cycle = (cycle * 10 + digits[i]) % MOD

    inv_10_n = pow(pow(10, n, MOD), MOD - 2, MOD)

    ten_p = pow(10, period, MOD)
    cycle_den = (ten_p - 1) % MOD
    inv_cycle_den = pow(cycle_den, MOD - 2, MOD)

    value = (prefix + cycle * inv_cycle_den) % MOD
    value = value * inv_10_n % MOD

    return value

def solve():
    t = int(input())
    out = []

    for case_id in range(1, t + 1):
        n, m = map(int, input().split())
        edges = [tuple(map(int, input().split())) for _ in range(m)]

        ans = solve_case(n, m, edges)
        out.append(f"Case #{case_id}: {ans}")

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The reverse graph is used only for reachability. Starting from vertex 1, every vertex discovered in the reverse graph has some directed path to 1 in the original graph. This preprocessing also removes misleading zero-weight cycles that can never reach the target.

The `min_w` and `nxt` arrays implement the second reduction. For each useful vertex, `min_w[u]` is its smallest possible next digit, and `nxt[u]` contains every destination achieving that digit. The special self-loop at vertex 1 is inserted after reading the original edges so that reaching 1 always permits the continuation of zero digits.

The point-set loop is the heart of the algorithm. `cur` represents every vertex that can occur immediately after the already chosen optimal prefix. The first scan finds the smallest next digit among those vertices. The second scan keeps only transitions producing that digit. A Python `set` removes duplicate destinations, which is useful when the input contains parallel edges.

The period search deliberately starts at digit `n`, rather than trying to determine the exact beginning of the cycle. If the true sequence becomes periodic earlier, taking some periodic digits as part of the prefix is harmless. The formula remains exact because the same infinite periodic tail follows that longer prefix.

All arithmetic involving the decimal itself is done modulo (10^9+7). Python integers do not overflow, but modular reduction keeps the intermediate values small and makes the intended arithmetic explicit.

## Worked Examples

### Sample 1

The graph is

```
0 -> 2 (3)
2 -> 3 (4)
2 -> 4 (1)
3 -> 1 (2)
4 -> 1 (3)
```

The useful vertices are all five vertices. The minimum outgoing digit of vertex 0 is 3, of vertex 2 is 1, of vertex 3 is 2, of vertex 4 is 3, and vertex 1 has the added zero self-loop.

| Position | Candidate set before step | Chosen digit | Candidate set after step |
| --- | --- | --- | --- |
| 1 | `{0}` | 3 | `{2}` |
| 2 | `{2}` | 1 | `{4}` |
| 3 | `{4}` | 3 | `{1}` |
| 4 | `{1}` | 0 | `{1}` |
| 5 | `{1}` | 0 | `{1}` |

The generated sequence begins with `31300...`, and after reaching vertex 1 it remains zero forever. The actual value is therefore (0.313), or

[
\frac{313}{1000}.
]

Modulo (10^9+7), this gives `241000002`, matching the sample.

### Sample 2

The important edges are

```
0 -> 1 (9)
0 -> 3 (3)
3 -> 0 (1)
```

The other vertices can reach 1 but do not provide a better outgoing digit from the states that matter.

| Position | Candidate set before step | Chosen digit | Candidate set after step |
| --- | --- | --- | --- |
| 1 | `{0}` | 3 | `{3}` |
| 2 | `{3}` | 1 | `{0}` |
| 3 | `{0}` | 3 | `{3}` |
| 4 | `{3}` | 1 | `{0}` |
| 5 | `{0}` | 3 | `{3}` |
| 6 | `{3}` | 1 | `{0}` |

The optimal sequence is

[
0.31313131\ldots=\frac{31}{99}.
]

There is no finite path with exactly this value. Instead, paths that traverse the cycle (0\to3\to0) more and more times approach it from above. The modular value is `40404041`, which is the second sample output.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(nm+n^2)) | Reachability costs (O(n+m)), point-set iteration examines retained edges for (3n) positions, and period testing costs (O(n^2)). |
| Space | (O(n+m)) | The graph, reverse graph, useful-edge lists, candidate sets, and digit sequence are all linear in the input size. |

For the maximum individual test case, (n\le2000) and (m\le4000), so the graph processing remains comfortably polynomial. The sums of (n) and (m) across all test cases are also bounded, which prevents the input from containing many simultaneously large cases. The official solution gives the same point-set construction and uses (3n) generated digits.

## Test Cases

```python
import sys
import io

MOD = 10**9 + 7

def solve_case(n, m, edges):
    rev = [[] for _ in range(n)]
    for u, v, w in edges:
        rev[v].append(u)

    good = [False] * n
    good[1] = True
    stack = [1]

    while stack:
        v = stack.pop()
        for u in rev[v]:
            if not good[u]:
                good[u] = True
                stack.append(u)

    min_w = [10] * n
    nxt = [[] for _ in range(n)]

    for u, v, w in edges:
        if not good[u] or not good[v]:
            continue

        if w < min_w[u]:
            min_w[u] = w
            nxt[u] = [v]
        elif w == min_w[u]:
            nxt[u].append(v)

    if min_w[1] > 0:
        min_w[1] = 0
        nxt[1] = [1]
    elif min_w[1] == 0:
        nxt[1].append(1)

    cur = {0}
    digits = []

    for _ in range(3 * n):
        d = min(min_w[u] for u in cur)
        digits.append(d)

        new_cur = set()
        for u in cur:
            if min_w[u] == d:
                new_cur.update(nxt[u])
        cur = new_cur

    period = None
    for p in range(1, n + 1):
        if all(
            digits[i] == digits[i + p]
            for i in range(n, 3 * n - p)
        ):
            period = p
            break

    assert period is not None

    prefix = 0
    for d in digits[:n]:
        prefix = (prefix * 10 + d) % MOD

    cycle = 0
    for d in digits[n:n + period]:
        cycle = (cycle * 10 + d) % MOD

    inv_10_n = pow(pow(10, n, MOD), MOD - 2, MOD)
    inv_cycle_den = pow(
        (pow(10, period, MOD) - 1) % MOD,
        MOD - 2,
        MOD
    )

    return (
        (prefix + cycle * inv_cycle_den) % MOD
    ) * inv_10_n % MOD

def run(inp: str) -> str:
    data = iter(map(int, inp.split()))
    t = next(data)
    out = []

    for case_id in range(1, t + 1):
        n = next(data)
        m = next(data)
        edges = [
            (next(data), next(data), next(data))
            for _ in range(m)
        ]
        ans = solve_case(n, m, edges)
        out.append(f"Case #{case_id}: {ans}")

    return "\n".join(out)

sample = """\
2
5 5
0 2 3
2 3 4
2 4 1
3 1 2
4 1 3
5 6
0 1 9
2 0 6
3 0 1
0 3 3
4 0 3
4 2 7
"""

assert run(sample) == (
    "Case #1: 241000002\n"
    "Case #2: 40404041"
), "provided samples"

assert run("""\
1
2 1
0 1 0
""") == "Case #1: 0", "minimum-size zero path"

assert run("""\
1
2 1
0 1 9
""") == "Case #1: 300000003", "single boundary digit"

assert run("""\
1
3 3
0 2 1
2 2 1
2 1 9
""") == "Case #1: 111111112", "non-attained periodic infimum"

assert run("""\
1
4 4
0 2 1
0 3 1
2 1 9
3 1 2
""") == "Case #1: 840000006", "equal first digits"

max_case = "1\n2000 1\n0 1 9\n"
assert run(max_case) == "Case #1: 300000003", "maximum n"

| Test input | Expected output | What it validates |
|---|---|---|
| `2 1`, edge `0 -> 1` with weight 0 | `Case #1: 0` | Minimum graph size and zero value |
| `2 1`, edge `0 -> 1` with weight 9 | `Case #1: 300000003` | Digit 9 and modular division by 10 |
| `3 3`, `0 -> 2 -> 2`, then `2 -> 1` | `Case #1: 111111112` | Infimum produced by an endlessly repeated cycle |
| `4 4`, two weight-1 choices from 0 | `Case #1: 840000006` | Comparing tied first digits by their suffixes |
| `n=2000`, one edge `0 -> 1` with weight 9 | `Case #1: 300000003` | Maximum vertex count and boundary handling |
```

The first custom case confirms that the target self-loop does not accidentally introduce a nonzero contribution. The second confirms the modular representation of a one-digit decimal. The third catches the most fundamental mistake in this problem, treating the answer as the value of a finite path rather than an infimum. The fourth checks that the candidate-set logic handles several paths sharing the same current digit. The final case exercises the largest allowed vertex count without introducing unnecessary graph structure.

## Edge Cases

For a direct zero-weight path,

```
2 1
0 1 0
```

the candidate set starts at `{0}` and selects digit 0. It then reaches vertex 1, where the added self-loop produces only zero digits. The generated sequence is `000...`, so the answer is exactly 0.

For a direct edge of weight 9,

```
2 1
0 1 9
```

the first digit is forced to be 9, after which vertex 1 contributes zeros. The sequence is `9000...`, representing (9/10). The modular calculation uses (10^{-1}), producing `300000003`.

For the periodic case,

```
3 3
0 2 1
2 2 1
2 1 9
```

the first digit is 1. At vertex 2 the smallest outgoing digit is again 1, so the candidate remains at vertex 2. This repeats indefinitely in the generated sequence. The paths that eventually leave through the weight-9 edge approach (0.11111\ldots), giving (1/9). The period search finds a one-digit cycle containing `1`.

For an unreachable zero cycle,

```
4 4
0 2 3
2 1 4
0 3 0
3 3 0
```

the reverse search from vertex 1 marks vertices 1, 2, and 0, but not vertex 3. The zero cycle at vertex 3 is removed before the digit process begins. Vertex 0 consequently has only the useful edge of weight 3, followed by weight 4 from vertex 2, so the sequence begins `34` and then zeros. The value is (34/100=17/50), giving `380000003`.

For the second sample, the graph creates the cycle

[
0\xrightarrow{3}3\xrightarrow{1}0.
]

The candidate-set sequence alternates between `{0}` and `{3}`, producing `313131...`. Paths can leave this cycle and reach vertex 1 after any number of repetitions, so finite path values approach (31/99). The algorithm does not need to explicitly enumerate any of those paths. It detects the repeated two-digit block and evaluates the corresponding geometric series directly.

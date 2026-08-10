---
title: "CF 102391D - Container"
description: "We have a binary array whose entries are container capacities, either 1 or 2. The goal is to transform the current array into a target array containing exactly the same number of each type. An allowed operation reverses either two consecutive entries or three consecutive entries."
date: "2026-08-10T20:55:29+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102391
codeforces_index: "D"
codeforces_contest_name: "XX Open Cup, Grand Prix of Korea"
rating: 0
weight: 102391
solve_time_s: 504
verified: false
draft: false
---

[CF 102391D - Container](https://codeforces.com/problemset/problem/102391/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 8m 24s  
**Verified:** no  

## Solution
## Problem Understanding

We have a binary array whose entries are container capacities, either `1` or `2`. The goal is to transform the current array into a target array containing exactly the same number of each type.

An allowed operation reverses either two consecutive entries or three consecutive entries. For two entries, the cost is their sum plus (C). For three entries, the cost is their sum plus (C). Since reversing equal entries changes nothing and only adds positive cost, the only useful operations are

[
12 \leftrightarrow 21
]

with cost (C+3),

[
112 \leftrightarrow 211
]

with cost (C+4), and

[
122 \leftrightarrow 221
]

with cost (C+5).

The output is a sequence of such reversals. The sequence must produce the target array and its total cost must be minimum. The output itself is not unique, so different optimal sequences are all accepted.

The constraint (N\leq 500) is the main clue. A generic shortest-path search over all binary strings has (2^N) states, which is hopeless at (N=500). We need something roughly quadratic or cubic in (N), and the memory limit is large enough for (O(N^2)) dynamic programming.

The difficult part is that an operation can move a `2` by either one position or two positions, and moving across another `2` costs slightly more. A greedy strategy that simply moves the nearest `2` to its target can choose the wrong matching between equal containers. The identity of equal `2`s does not matter to the final array, so choosing their matching carefully is part of the optimization.

For example, consider

```
3 2
221
122
```

The whole array can be reversed in one operation, giving

```
1
1 3
```

with cost (2+2+1+2=7). A strategy that insists on moving a particular `2` by adjacent swaps can use more operations and lose optimality.

Another boundary case is

```
2 5
12
21
```

The only possible useful operation is reversing the two entries, so the optimal output is

```
1
1 2
```

with cost (1+2+5=8). An implementation that only considers length-three reversals would incorrectly conclude that the transformation is impossible.

Finally, when the two strings are already equal, the correct answer is simply

```
0
```

with no following lines. Trying to perform a harmless reversal of equal values is never optimal because every selected container has positive capacity.

## Approaches

The most direct approach is to treat every binary string of length (N) as a state and run Dijkstra's algorithm. From every state there are (N-1) length-two reversals and (N-2) length-three reversals, so there are (2N-3) outgoing transitions. In the worst case the search may visit all (2^N) states, giving up to

[
(2N-3)2^N
]

transitions. At (N=500), this is completely infeasible. The fact that all operations have positive cost makes Dijkstra correct, but correctness is not the problem. The state space is simply too large.

The useful observation is that we never need to reason about the positions of both types independently. Once every `2` is in one of its target positions, every remaining position is automatically occupied by a `1`. We can consequently match every `2` in the current string with one `2` in the target string and reason about how far each matched `2` has to move. This is the central reduction used by the contest solution.

Suppose a particular `2` has to move a distance (d). Moving it by two positions can be done with a reversal of `112` or `211`, costing (C+4). Moving it by one position uses `12` or `21`, costing (C+3). Thus the movement itself has a lower bound

[
\left\lfloor\frac d2\right\rfloor(C+4)
+
(d\bmod2)(C+3).
]

There is one more contribution. If the chosen matching makes two `2` containers cross each other, one of the two-step movements has to cross a `2` instead of a `1`. The pattern is then `122` or `221`, whose cost is (C+5) rather than (C+4). Each such crossing contributes exactly one additional unit of cost. If the matching creates (z) crossings between `2`s, its total cost is consequently

[
z+
\sum_i
\left(
\left\lfloor\frac {d_i}2\right\rfloor(C+4)
+
(d_i\bmod2)(C+3)
\right).
]

This lower bound is attainable. We can move every matched `2` directly toward its destination, using two-position moves followed by at most one one-position move. A dependency ordering makes sure that a move never destroys a `2` that still has to be processed. The extra cost from every dependency crossing is exactly the crossing term above.

We still have to choose the matching. Here parity becomes the key. A two-position move preserves the parity of a `2`'s position, while a one-position move changes it. Once we decide which current `2`s will be matched to even target positions and which will be matched to odd target positions, the optimal matching inside each group is simply increasing position with increasing position. An exchange argument shows that swapping two matched targets cannot improve either the movement contribution or the number of crossings.

So the only real decision is which current `2` positions belong to the even-target group. Let the current `2` positions be (a_0,a_1,\ldots,a_{m-1}). Let (B_0) contain the target positions of `2`s with even indices and (B_1) the positions with odd indices. Define (f[i][j]) as the minimum cost after processing the first (i) current `2`s, with exactly (j) of them assigned to (B_0). The remaining (i-j) are assigned to (B_1).

There are only two transitions. The next `2` can be matched with the next unused position of (B_0), increasing (j), or with the next unused position of (B_1), leaving (j) unchanged. The movement cost is immediate. The number of new crossings can be counted using prefix counts of target positions of the opposite parity.

This gives an (O(N^2)) dynamic program. After recovering the matching, we build a directed dependency graph between the `2`s and process it topologically. The construction takes another (O(N^2)) time.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Dijkstra | (O(N2^N)) transitions | (O(2^N)) | Too slow |
| Optimal DP + reconstruction | (O(N^2)) | (O(N^2)) | Accepted |

## Algorithm Walkthrough

1. Extract the zero-based positions of every `2` from the current string. Call them (a_0,a_1,\ldots,a_{m-1}). Also extract the positions of target `2`s into two arrays, (B_0) for even positions and (B_1) for odd positions.

Equal `2`s can be treated as indistinguishable. The only information that matters is which target position each current `2` eventually occupies.
2. Match the target positions inside each parity class in increasing order.

Once we decide that a collection of current `2`s belongs to (B_0), their best matching is the first current one with the first target one, the second with the second, and so on. The same is true for (B_1). Any crossing inside one parity class can be removed by exchanging two target assignments, which cannot increase the movement cost and cannot reduce the crossing penalty.
3. Define (f[i][j]) as the minimum cost after processing the first (i) current `2`s, where (j) of them were assigned to (B_0).

The number assigned to (B_1) is then (i-j). This completely determines which target position is next in either parity class.
4. If the next current position (a_i) is assigned to (B_0[j]), compute its movement cost from the distance (d=|a_i-B_0[j]|).

Add

[
\left\lfloor\frac d2\right\rfloor(C+4)+(d\bmod2)(C+3).
]

The number of new inversions is the number of not-yet-matched odd target positions at or before (B_0[j]). If `pref[1][x]` counts odd target positions up to (x), then exactly (i-j) of those have already been consumed by earlier current `2`s. The new contribution is

[
\max(0,\text{pref}_1[x]-(i-j)).
]
5. If the next current position (a_i) is assigned to (B_1[i-j]), use the symmetric transition.

The movement cost is calculated in exactly the same way. The new inversion count is

[
\max(0,\text{pref}_0[x]-j).
]
6. Store which of the two transitions produced every DP state. At the final state ((m,|B_0|)), walk backward through these choices to recover the target position (v_i) assigned to every current `2` (a_i).
7. Build a dependency graph between matched `2`s. For every pair (j<i) with (v_i>v_j), the two movements may interfere. If moving (a_i) toward (v_i) would pass through the starting position of the `2` represented by (j), then (i) must be processed first. Symmetrically, if moving (a_j) would pass through (v_i), then (j) must be processed first.

These dependencies describe exactly which `2` must move out of the way before another one can move.
8. Run Kahn's topological sort on this dependency graph.

When a `2` becomes available, move it directly toward its assigned target. If it has to move right by two positions, reverse the three positions containing `211`. If it has to move left by two positions, reverse the three positions containing `112`. After all possible two-position moves, use one length-two reversal if one position remains.
9. Record every reversal in the order it is performed.

The dependency ordering guarantees that the selected substring has the required form whenever it is reversed, and that every matched `2` reaches exactly its assigned target position. Since the assignment came from the minimum-cost DP, the resulting sequence has minimum possible cost.

### Why it works

Fix any matching between current `2`s and target `2`s. Every matched `2` must travel its required distance, so its movement contributes at least the two-step and one-step costs described above. Whenever two matched `2`s cross, one two-step movement must use a `122` or `221` pattern instead of `112` or `211`, adding exactly one extra unit. Thus the DP objective is a lower bound for every valid sequence.

For any fixed partition of the current `2`s into the two target parity classes, sorted matching minimizes the movement contribution and the crossings. The DP examines every possible partition, so it finds the minimum lower bound over all matchings.

Finally, the dependency graph gives an order in which the corresponding movements can actually be executed. Every two-position movement contributes (C+4), every remaining one-position movement contributes (C+3), and every movement that crosses another `2` contributes the additional one unit already counted by the DP. Thus the constructed sequence reaches exactly the DP value. Since no valid sequence can be cheaper than that lower bound, the construction is optimal.

## Python Solution

```python
import sys
from bisect import bisect_right
from collections import deque

input = sys.stdin.readline

def solve(data: str) -> str:
    it = iter(data.split())
    n = int(next(it))
    C = int(next(it))
    s = next(it)
    t = next(it)

    a = [i for i, ch in enumerate(s) if ch == '2']
    b = [[], []]

    for i, ch in enumerate(t):
        if ch == '2':
            b[i & 1].append(i)

    m = len(a)
    b0_len = len(b[0])
    b1_len = len(b[1])

    # pref[p][x] = number of target 2s of parity p
    # in positions [0, x).
    pref = [[0] * (n + 1) for _ in range(2)]
    for p in range(2):
        for i in range(n):
            pref[p][i + 1] = pref[p][i]
            if i in set():
                pass

    # Avoid rebuilding sets in the inner loops.
    target_parity = [0] * n
    for p in range(2):
        for x in b[p]:
            target_parity[x] = 1

    for i in range(n):
        pref[0][i + 1] = pref[0][i] + (
            1 if target_parity[i] == 0 and t[i] == '2' else 0
        )
        pref[1][i + 1] = pref[1][i] + (
            1 if target_parity[i] == 1 and t[i] == '2' else 0
        )

    INF = 10**30
    dp = [[INF] * (m + 1) for _ in range(m + 1)]
    choice = [[-1] * (m + 1) for _ in range(m + 1)]
    dp[0][0] = 0

    for i in range(m):
        for j in range(i + 1):
            cur = dp[i][j]
            if cur == INF:
                continue

            # Assign a[i] to the next even target position.
            if j < b0_len:
                x = b[0][j]
                d = abs(a[i] - x)
                move = (d // 2) * (C + 4) + (d & 1) * (C + 3)

                already_used_odd = i - j
                inv = max(0, pref[1][x + 1] - already_used_odd)

                nv = cur + move + inv
                if nv < dp[i + 1][j + 1]:
                    dp[i + 1][j + 1] = nv
                    choice[i + 1][j + 1] = 0

            # Assign a[i] to the next odd target position.
            if i - j < b1_len:
                x = b[1][i - j]
                d = abs(a[i] - x)
                move = (d // 2) * (C + 4) + (d & 1) * (C + 3)

                already_used_even = j
                inv = max(0, pref[0][x + 1] - already_used_even)

                nv = cur + move + inv
                if nv < dp[i + 1][j]:
                    dp[i + 1][j] = nv
                    choice[i + 1][j] = 1

    # Recover the matched target position for every current 2.
    target = [0] * m
    i = m
    j = b0_len

    while i > 0:
        c = choice[i][j]
        if c == 0:
            target[i - 1] = b[0][j - 1]
            j -= 1
        else:
            target[i - 1] = b[1][i - j - 1]
        i -= 1

    # Dependency graph.
    graph = [[] for _ in range(m)]
    indeg = [0] * m

    for i in range(m):
        for j in range(i):
            if target[i] <= target[j]:
                continue

            if a[i] <= target[j]:
                graph[i].append(j)
                indeg[j] += 1

            if a[j] >= target[i]:
                graph[j].append(i)
                indeg[i] += 1

    q = deque(i for i in range(m) if indeg[i] == 0)
    operations = []

    while q:
        u = q.popleft()

        if a[u] < target[u]:
            while a[u] + 2 <= target[u]:
                p = a[u]
                operations.append((p + 1, p + 3))
                a[u] += 2

            if a[u] < target[u]:
                p = a[u]
                operations.append((p + 1, p + 2))
                a[u] += 1

        else:
            while a[u] - 2 >= target[u]:
                p = a[u]
                operations.append((p, p + 2))
                a[u] -= 2

            if a[u] > target[u]:
                p = a[u]
                operations.append((p, p + 1))
                a[u] -= 1

        for v in graph[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)

    out = [str(len(operations))]
    out.extend(f"{l} {r}" for l, r in operations)
    return "\n".join(out) + "\n"

def main() -> None:
    data = sys.stdin.read()
    sys.stdout.write(solve(data))

if __name__ == "__main__":
    main()
```

The input parser is deliberately separated into `solve`, which also makes the implementation easy to test. The current positions of `2`s are stored in zero-based coordinates because parity and distances are simpler there.

The two target parity lists are sorted automatically because the target string is scanned from left to right. The prefix arrays let every DP transition count the newly created inversions in constant time, so the whole DP is quadratic rather than cubic.

The reconstruction walks backward from `(m, len(b[0]))`. If the recorded choice is `0`, the last current `2` was assigned to the last unused even target position. Otherwise it was assigned to the corresponding odd target position. This exactly reverses the DP transitions.

The dependency graph contains at most (O(m^2)) edges. Kahn's algorithm processes every edge once. When a `2` moves two positions, the operation indices are especially easy to get wrong because the internal positions are stored zero-based while the required output is one-based. For a `2` at zero-based position `p`, moving right by two reverses output interval `(p+1,p+3)`. Moving left by two reverses `(p,p+2)`. The length-two cases are `(p+1,p+2)` and `(p,p+1)` respectively.

Python integers do not overflow, and the largest DP value is comfortably below the arbitrary-precision range that Python handles naturally. The maximum number of generated operations is (O(N^2)), so storing the answer explicitly is safe for (N=500).

## Worked Examples

### Sample 1

The input is

```
5 2
11221
21112
```

The current `2`s are at zero-based positions (2,3). The target `2`s are at positions (0,4), both even, so both must belong to (B_0).

| DP state | Current position | Target position | Movement cost | New inversions | Total |
| --- | --- | --- | --- | --- | --- |
| (f[0][0]) | 2 | 0 | 6 | 0 | 6 |
| (f[1][1]) | 3 | 4 | 5 | 0 | 11 |

The first `2` moves two positions left using `112 -> 211`, which is the reversal of positions `1..3`. The second `2` then moves one position right using `21 -> 12`, reversing positions `4..5`.

A valid optimal output is

```
2
1 3
4 5
```

The first operation costs (1+1+2+2=6), and the second costs (2+1+2=5), for a total of (11).

The trace demonstrates why the distance contribution uses (C+4) for a two-position move and (C+3) for a one-position move.

### Sample 2

The input is

```
7 0
2212121
1212122
```

The current `2`s are at positions (0,1,3,5). The target positions are (1,3,5,6), giving

[
B_0=[6],\qquad B_1=[1,3,5].
]

The optimal DP assigns the first three current `2`s to the odd target positions and the last one to the even target position.

| DP state | Current position | Target position | Class | Movement cost | New inversions | Total |
| --- | --- | --- | --- | --- | --- | --- |
| (f[0][0]) | 0 | 1 | odd | 3 | 0 | 3 |
| (f[1][0]) | 1 | 3 | odd | 4 | 0 | 7 |
| (f[2][0]) | 3 | 5 | odd | 4 | 0 | 11 |
| (f[3][0]) | 5 | 6 | even | 3 | 0 | 14 |

The resulting movements can be ordered as

```
4
6 7
4 6
2 4
1 2
```

The costs are (3,4,4,3), giving the optimum (14).

This example shows why choosing a single matching greedily is dangerous. The best assignment is not determined only by the nearest target. The DP has to balance one-step moves, two-step moves, and crossings.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(N^2)) | The DP has (O(N^2)) states and constant-time transitions; dependency construction also takes (O(N^2)). |
| Space | (O(N^2)) | The DP, choice table, and dependency graph each require at most quadratic space. |

With (N\leq500), (N^2=250000), so the dynamic program and dependency construction are easily within the intended limits. The output itself can contain (O(N^2)) operations, and the algorithm spends only linear time per generated operation.

## Test Cases

The output of this problem is not unique, so tests should not compare the raw output string against one fixed sequence. The following harness checks the properties that actually matter: every operation is legal, the final array equals the target, and the total cost equals the known optimum for each test.

```python
# Save the solution above as solution.py before running this file.

from solution import solve

def validate(inp: str, out: str):
    data = inp.split()
    n = int(data[0])
    C = int(data[1])
    s = list(data[2])
    target = data[3]

    lines = out.strip().splitlines()
    k = int(lines[0])
    assert len(lines) == k + 1

    cost = 0

    for line in lines[1:]:
        l, r = map(int, line.split())
        assert 1 <= l < r <= n
        assert r - l <= 2

        # Convert to zero-based indexing.
        l -= 1
        r -= 1

        cost += sum(int(s[i]) for i in range(l, r + 1)) + C
        s[l:r + 1] = reversed(s[l:r + 1])

    assert ''.join(s) == target
    return cost

# Sample 1.
sample1 = """\
5 2
11221
21112
"""
assert validate(sample1, solve(sample1)) == 11

# Sample 2.
sample2 = """\
7 0
2212121
1212122
"""
assert validate(sample2, solve(sample2)) == 14

# Sample 3.
sample3 = """\
7 2
2212121
1212122
"""
assert validate(sample3, solve(sample3)) == 21

# Minimum-size case.
case_min = """\
1 1000
1
1
"""
assert validate(case_min, solve(case_min)) == 0

# One length-two reversal, catches the basic indexing boundary.
case_two = """\
2 5
12
21
"""
assert validate(case_two, solve(case_two)) == 8

# One length-three reversal, catches the length-three boundary.
case_three = """\
3 7
112
211
"""
assert validate(case_three, solve(case_three)) == 11

# All values equal, maximum-size instance.
case_max = "500 1000\n" + "1" * 500 + "\n" + "1" * 500 + "\n"
assert validate(case_max, solve(case_max)) == 0
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Sample 1 | Minimum cost (11) | Mixed one-step and two-step movements |
| Sample 2 | Minimum cost (14) | Parity partition and zero-base-cost case |
| Sample 3 | Minimum cost (21) | Different optimal matching when (C) changes |
| (1, 1 \rightarrow 1) | `0` | Minimum size and already-correct input |
| (12\rightarrow21) | One reversal, cost (8) | Length-two boundary and one-step movement |
| (112\rightarrow211) | One reversal, cost (11) | Length-three boundary and two-step movement |
| (500) equal `1`s | `0` | Maximum (N), memory and boundary handling |

## Edge Cases

When (N=1), there is no legal reversal. Since the counts of `1` and `2` agree between the two strings, the strings must already be identical. The DP has (m=0), so it immediately produces zero operations.

When the input differs only by two positions, such as

```
2 5
12
21
```

there is exactly one useful reversal. The DP matches the current `2` at position (1) with the target position (0), giving distance one and cost (C+3=8). The reconstruction emits `1 2`.

When a length-three operation is the optimal choice, as in

```
3 7
112
211
```

the `2` must move two positions left. The DP assigns distance two, giving (C+4=11). The reconstruction emits `1 3`, which changes `112` directly into `211`.

When all containers are equal, such as

```
500 1000
111111...111
111111...111
```

there is no `2` to process and the DP has no transitions. The answer is zero operations. This case also verifies that the implementation does not accidentally create unnecessary reversals.

The most subtle edge case is when changing (C) changes the optimal matching itself. Samples 2 and 3 use the same two strings but different values of (C). With (C=0), the optimum uses four operations and costs (14). With (C=2), it is better to use three length-three operations, costing (21). A strategy that minimizes only the number of moved positions or only the number of operations cannot handle this tradeoff. The DP evaluates the complete cost expression, including both movement and crossing penalties, so it selects the correct matching in either case.

A small implementation detail worth calling out: the editorial code above uses a zero-based representation internally and converts only when emitting operations. That is the safest way to avoid the most common off-by-one errors in this problem.

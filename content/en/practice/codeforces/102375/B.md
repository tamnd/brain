---
title: "CF 102375B - \u0411\u043e\u043b\u044c\u0448\u0438\u0435 \u043f\u0435\u0440\u0435\u043c\u0435\u043d\u044b"
description: "We have (N) labeled cities and must build exactly (N-1) undirected flight routes between distinct pairs of cities. The resulting network has to be connected, so it is precisely a tree on the (N) labeled vertices."
date: "2026-08-14T03:21:21+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102375
codeforces_index: "B"
codeforces_contest_name: "\u041a\u0432\u0430\u043b\u0438\u0444\u0438\u043a\u0430\u0446\u0438\u043e\u043d\u043d\u044b\u0439 \u0440\u0430\u0443\u043d\u0434 \u0427\u0435\u043c\u043f\u0438\u043e\u043d\u0430\u0442\u0430 \u0421\u0435\u0432\u0435\u0440\u043e-\u0417\u0430\u043f\u0430\u0434\u0430 \u0420\u043e\u0441\u0441\u0438\u0438 \u0438 \u041c\u043e\u0441\u043a\u0432\u044b ICPC 2019"
rating: 0
weight: 102375
solve_time_s: 91
verified: false
draft: false
---

[CF 102375B - \u0411\u043e\u043b\u044c\u0448\u0438\u0435 \u043f\u0435\u0440\u0435\u043c\u0435\u043d\u044b](https://codeforces.com/problemset/problem/102375/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 31s  
**Verified:** no  

## Solution
## Problem Understanding

We have (N) labeled cities and must build exactly (N-1) undirected flight routes between distinct pairs of cities. The resulting network has to be connected, so it is precisely a tree on the (N) labeled vertices.

The accessibility of a city is its degree, meaning the number of routes incident to that city. Among all valid trees, we first want to make the largest degree as large as mathematically possible. The task is then to count how many different labeled trees achieve that maximum.

The input contains one integer (N), with (2 \le N \le 10^9). The upper bound immediately rules out any algorithm that constructs the graph explicitly, since even writing down all (N-1) edges could require (10^9) operations. We need to derive a formula whose running time is independent of (N), ideally (O(1)).

There are two small cases worth checking explicitly. For (N=2), the only possible tree consists of the single edge ((1,2)), so the answer is (1). A careless argument that counts possible centers and assumes several choices could accidentally produce (2), but the two cities describe the same edge and both have degree (1=N-1).

For (N=3), the maximum degree is (2). A vertex of degree (2) can be chosen in three ways, and once that vertex is chosen, both other vertices must be connected to it. Thus the answer is (3), matching the sample. An approach that counts arbitrary pairs of edges can easily count the same tree multiple times if it does not identify its unique maximum-degree vertex.

## Approaches

A direct brute-force solution could enumerate every possible set of (N-1) edges, check whether it forms a connected graph, compute all vertex degrees, and keep the trees whose maximum degree is largest. There are (\binom{N(N-1)/2}{N-1}) candidate edge sets, so this is already hopeless for very small values of (N). An alternative brute-force enumeration of all labeled trees is better mathematically, because Cayley's formula says there are (N^{N-2}) of them, but that is still exponential in (\log N) and completely unusable for (N) as large as (10^9).

The brute-force works because checking every valid tree cannot miss an answer, but it fails because the number of trees grows enormously. The key observation is that we do not actually need to construct or enumerate any tree.

Every tree on (N) vertices has exactly (N-1) edges. A single vertex can be adjacent to at most the other (N-1) vertices, so the maximum possible accessibility is at most (N-1). This upper bound is achievable: choose one city and connect it directly to every other city. The resulting graph is a star and is connected, so its center has degree exactly (N-1).

Now suppose a tree achieves this maximum. Some vertex must have degree (N-1), meaning that it is connected to every other vertex. That already uses all (N-1) edges available in a tree. Consequently, no edges can exist among the remaining vertices, and the whole tree is forced to be a star.

Thus every optimal tree corresponds to exactly one choice of its center. There are (N) possible centers, so the answer is simply (N).

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over labeled trees | (O(N^{N-2})) or worse | (O(N)) | Too slow |
| Optimal formula | (O(1)) | (O(1)) | Accepted |

## Algorithm Walkthrough

1. Read (N), the number of labeled cities.
2. Observe that every tree has maximum possible vertex degree at most (N-1), because a city has only (N-1) other cities it could be directly connected to.
3. Construct the extremal shape conceptually by selecting one city and connecting it to every other city. Its degree is (N-1), so the upper bound is achievable.
4. Count the optimal trees by choosing their center. There are exactly (N) choices, and after choosing the center every one of the other (N-1) edges is forced.
5. Output (N).

Why it works: a tree reaches the largest possible degree only when some vertex is adjacent to all other (N-1) vertices. Once that vertex is fixed, all (N-1) edges are already determined. Hence there is a one-to-one correspondence between optimal trees and choices of the center vertex. Since there are (N) labeled vertices, exactly (N) optimal trees exist.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
print(n)
```

The program only needs to read the number of cities and print it. This directly implements the formula derived above.

There is no graph to construct, so no adjacency list, edge list, or visited array is necessary. This matters because (N) can be (10^9), making any (O(N))-sized data structure impractical.

Python integers can represent the required answer without overflow. In fact, the answer is at most (10^9), which is far below Python's integer limits.

The boundary (N=2) is handled naturally. The program prints (2), but the correct answer is indeed (2) because there are two labeled descriptions of the same star center: choosing city (1) or choosing city (2) gives the same single edge, so this deserves closer examination.

For (N=2), the two possible choices of a vertex do not produce different edge sets. This means the formula (N) would give (2), contradicting the direct counting of graphs. The general center-to-tree correspondence is not one-to-one in this special case, because both vertices have maximum degree (1=N-1).

Thus the actual formula must handle (N=2) separately:

[
\text{answer} =
\begin{cases}
1, & N=2,\
N, & N\ge3.
\end{cases}
]

The corrected implementation is:

```python
import sys
input = sys.stdin.readline

n = int(input())

if n == 2:
    print(1)
else:
    print(n)
```

The special case is essential because the optimal tree has two maximum-degree vertices when (N=2), while for every (N\ge3), the center of a star is unique.

## Worked Examples

For the provided sample (N=3), the optimal maximum degree is (2). The center can be any of the three labeled cities.

| (N) | Maximum possible degree | Number of center choices | Answer |
| --- | --- | --- | --- |
| 3 | 2 | 3 | 3 |

Choosing city (1) gives edges ((1,2)) and ((1,3)). Choosing city (2) gives ((1,2)) and ((2,3)). Choosing city (3) gives ((1,3)) and ((2,3)). These are exactly the three trees from the sample.

For (N=4), the maximum possible degree is (3). Once the center is chosen, it must connect to all three remaining cities.

| (N) | Maximum possible degree | Center choices | Forced edges after choosing center | Answer |
| --- | --- | --- | --- | --- |
| 4 | 3 | 4 | 3 | 4 |

For example, choosing city (2) forces the edges ((2,1)), ((2,3)), and ((2,4)). No additional edge is possible because a tree on four vertices must contain exactly three edges. The same reasoning applies independently to each of the four possible centers.

For the boundary case (N=2), there is only one possible graph.

| (N) | Maximum possible degree | Optimal edge set | Answer |
| --- | --- | --- | --- |
| 2 | 1 | ((1,2)) | 1 |

This trace demonstrates why (N=2) needs separate handling. Both vertices have the maximum degree, so counting maximum-degree vertices would count the same tree twice.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(1)) | Only one integer is read and a constant number of operations are performed. |
| Space | (O(1)) | No data structure depends on (N). |

The constraints allow (N) to reach (10^9), so an (O(N)) solution would already be too large in the worst case. The constant-time formula is independent of the number of cities, which makes the upper bound irrelevant to runtime and memory usage.

## Test Cases

```python
import sys
import io

def solve(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    n = int(input())

    if n == 2:
        return "1\n"
    return f"{n}\n"

# Provided sample
assert solve("3\n") == "3\n", "sample 1"

# Minimum-size input
assert solve("2\n") == "1\n", "minimum N"

# Small case where the general formula applies
assert solve("4\n") == "4\n", "four cities"

# Boundary case just above the special case
assert solve("3\n") == "3\n", "N=3"

# Maximum-size input
assert solve("1000000000\n") == "1000000000\n", "maximum N"

# Large value checks that the algorithm does not depend on constructing the graph
assert solve("999999999\n") == "999999999\n", "large N"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `3` | `3` | Provided sample and ordinary star counting |
| `2` | `1` | Minimum-size boundary and duplicate-center issue |
| `4` | `4` | General case with a unique center |
| `3` | `3` | Boundary immediately above the special case |
| `1000000000` | `1000000000` | Maximum constraint and constant-time behavior |
| `999999999` | `999999999` | Large input without graph construction |

## Edge Cases

For (N=2), the input is `2`. The only possible tree contains the edge ((1,2)). Both vertices have accessibility (1), which is the maximum possible value, but they are not two different trees. The algorithm detects (N=2) and prints `1`, avoiding the incorrect result `2` that would come from blindly counting possible centers.

For (N=3), the input is `3`. A tree has two edges, and the maximum possible degree is (2). Choosing city (1) forces edges ((1,2)) and ((1,3)), choosing city (2) forces ((1,2)) and ((2,3)), and choosing city (3) forces ((1,3)) and ((2,3)). The three choices produce three distinct trees, so the algorithm prints `3`.

For a very large value such as `1000000000`, explicitly constructing a star would require creating (999999999) edges and would be infeasible. The mathematical argument has already reduced the entire problem to counting the possible center labels, so the algorithm simply prints `1000000000`. No loop depends on (N), which is why the maximum constraint causes no performance issue.

The transition from (N=2) to (N=3) is the critical off-by-one boundary. At (N=2), every vertex is a maximum-degree vertex and the center is not unique. Starting at (N=3), a star has exactly one vertex of degree (N-1), so each optimal tree corresponds to exactly one center. The implementation reflects precisely this change with the condition `n == 2`.

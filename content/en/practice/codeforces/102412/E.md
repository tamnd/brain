---
title: "CF 102412E - Minimums on the Edges"
description: "We have an undirected multigraph with (n) vertices and (m) edges, together with exactly (s) tokens. We choose a nonnegative integer (av) for every vertex (v), where (av) is the number of tokens placed there and the total is exactly (s). An edge ((u,v)) has capacity (min(au,av))."
date: "2026-08-12T00:33:18+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102412
codeforces_index: "E"
codeforces_contest_name: "MEX Foundation Contest (supported by AIM Tech)"
rating: 0
weight: 102412
solve_time_s: 139
verified: true
draft: false
---

[CF 102412E - Minimums on the Edges](https://codeforces.com/problemset/problem/102412/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 19s  
**Verified:** yes  

## Solution
## Problem Understanding

We have an undirected multigraph with (n) vertices and (m) edges, together with exactly (s) tokens. We choose a nonnegative integer (a_v) for every vertex (v), where (a_v) is the number of tokens placed there and the total is exactly (s).

An edge ((u,v)) has capacity (\min(a_u,a_v)). The goal is to distribute all tokens so that the sum of the capacities of all edges is as large as possible. Parallel edges count separately, so if the same pair of vertices is connected by five edges, their contribution is five times the same minimum. The required output is any token distribution attaining the maximum.

The constraints are unusually small in the number of vertices but large in the number of edges. We have (n \le 18), (m \le 100000), and (s \le 100). The bound (n \le 18) is the signal that subsets of vertices can be enumerated, because (2^{18}=262144). The large value of (m) means we cannot repeatedly scan all edges for every subset. The official time limit is 4 seconds with 512 MiB of memory, so an (O(2^n n)) subset computation is reasonable, while algorithms with an extra factor of (m) or a large polynomial in (s) inside the subset enumeration are undesirable.

There are several edge cases that can make a careless implementation wrong. First, (s) can be zero. For example,

```
1 0 0
```

must produce

```
0
```

because there are no tokens and no edges. An implementation that assumes at least one token or starts its DP at one can fail here.

Second, parallel edges matter. For

```
2 5 3
1 2
1 2
1 2
1 2
1 2
```

an optimal answer is

```
2 1
```

because every one of the five edges has capacity (1), giving total capacity (5). A careless implementation that stores only whether an edge exists would treat these five edges as one edge and lose a factor of five.

Third, the optimal sets used during the subset DP do not have to be nested as they are discovered. For example, different optimal subsets of the same size can be different. It is incorrect to assume that the subset remembered for size (i) is automatically contained in the subset remembered for size (i+1). The solution works because non-nested sets can be uncrossed without decreasing the objective.

Finally, (s) can be much larger than (n). With two vertices joined by one edge and (s=100),

```
2 1 100
1 2
```

the answer is

```
50 50
```

rather than putting all tokens on one vertex. The relevant DP must allow a subset of the same size to be used repeatedly.

## Approaches

A direct brute-force approach would enumerate every possible token distribution ((a_1,\ldots,a_n)) with sum (s), then evaluate all (m) edges. The number of such distributions is

[
\binom{s+n-1}{n-1}.
]

At the maximum bounds this is (\binom{117}{17}), already far beyond anything feasible, even before multiplying by the (100000) edges used to evaluate one distribution.

A more informed brute-force approach enumerates every vertex subset and directly counts its induced edges by checking every pair of vertices. There are (2^n) subsets and (O(n^2)) possible vertex pairs, so this costs (O(2^n n^2)). At (n=18), this is roughly (262144 \cdot 324), about 85 million pair checks. That is usable in optimized C++, and it is the standard bitmask solution described by existing editorials, but it is unnecessarily expensive for Python.

The key observation is to stop thinking about the tokens individually. Given a final allocation (a_v), define

[
X_k={v\mid a_v\ge k}.
]

The sets form a nested sequence,

[
X_1 \supseteq X_2 \supseteq X_3 \supseteq \cdots.
]

An edge contributes one unit for every level (k) at which both endpoints belong to (X_k). If (f(X)) denotes the number of graph edges whose two endpoints are both in (X), then the total objective becomes

[
\sum_k f(X_k).
]

Also,

[
\sum_k |X_k|=\sum_v a_v=s.
]

So the original problem becomes choosing nested vertex subsets whose sizes sum to (s), maximizing the sum of their induced-edge counts. This reformulation is the central idea behind the known bitmask and knapsack solution.

For every size (k), let

[
F_k=\max_{|X|=k} f(X).
]

If we temporarily ignore the requirement that the chosen subsets must be nested, the problem becomes an unbounded knapsack. An item of size (k) has weight (k) and value (F_k), and we may use the same size several times because several token levels can have the same vertex set.

The surprising part is that dropping the nesting requirement does not change the optimum. The induced-edge function is supermodular:

[
f(A)+f(B)\le f(A\cup B)+f(A\cap B).
]

If two selected sets (A) and (B) are not nested, replace them by (A\cup B) and (A\cap B). Their total size is unchanged, while their total value does not decrease. Repeating this uncrossing process eventually produces a nested family. Thus the knapsack optimum can always be converted into a valid token distribution.

The remaining question is how to compute every (F_k) efficiently. For a subset represented by a bitmask, remove one selected vertex (v). The induced-edge count of the larger subset equals the induced-edge count of the smaller subset plus the number of edges from (v) to the smaller subset. Since (n) is only 18, this gives an (O(n2^n)) computation, which is fast enough in Python. Parallel edges are handled by storing their multiplicities in an (n\times n) matrix.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Enumerate token distributions | (O\left(m\binom{s+n-1}{n-1}\right)) | (O(n+m)) | Too slow |
| Subsets + all vertex pairs | (O(2^n n^2 + ns)) | (O(2^n)) | Accepted in optimized languages |
| Subsets with incremental edge counts | (O(n2^n + ns)) | (O(2^n+n^2)) | Accepted |

## Algorithm Walkthrough

1. Store the multiplicity of every undirected edge in a matrix `edges[u][v]`. If the input contains several copies of the same edge, its multiplicity is increased several times.
2. Enumerate every subset of vertices with a bitmask. For each nonempty mask, remove its lowest set bit, corresponding to vertex (v), and call the remaining subset `prev`.

The induced edges inside `mask` consist of all edges already present inside `prev`, plus every edge connecting (v) to a vertex of `prev`. Thus

[
f(mask)=f(prev)+\sum_{u\in prev}edges[v][u].
]

This computes every induced-edge count from a smaller already-computed subset.
3. For each subset, compute its number of vertices with `mask.bit_count()`. If its induced-edge count is better than the current value for that subset size, store both the value and the mask.

After this pass, `best[k]` is exactly the maximum number of edges induced by any (k)-vertex subset, and `best_mask[k]` remembers one subset attaining that value.
4. Run an unbounded knapsack over the total number of tokens. Let `dp[x]` be the maximum value obtainable using exactly (x) tokens.

For every total (x), try taking one more layer containing (k) vertices. Its cost is (k), and its value is `best[k]`. The transition is

[
dp[x]=\max_{1\le k\le \min(n,x)}
\left(dp[x-k]+best[k]\right).
]

Since (k) can be used repeatedly, this is an unbounded knapsack.
5. Store which subset size was chosen by each DP state. Starting from (s), repeatedly follow these choices backwards. For every selected size (k), increment the token count of every vertex contained in `best_mask[k]`.

The resulting collection of subsets need not be nested. That is fine because the uncrossing argument proves that its value is already the optimum achievable by some nested collection. The token counts produced by adding all selected subsets directly represent the same collection of layers after the corresponding sets are uncrossed.
6. If the DP were ever allowed to use fewer than (s) tokens, the unused tokens could be placed anywhere without decreasing any edge capacity. In this implementation the DP is performed for exactly (s), so no extra filling is normally needed.

Why it works: every valid token distribution corresponds exactly to a nested sequence of level sets (X_k), and its objective is (\sum f(X_k)). Replacing every (f(X_k)) by the maximum possible value for its size gives an upper bound represented by the knapsack. Conversely, every collection selected by the knapsack can be uncrossed pairwise using supermodularity, preserving the sum of set sizes and never decreasing the total induced-edge value. The uncrossed family is nested, so it corresponds to an actual token distribution. The knapsack value is consequently both an upper bound and achievable, which proves optimality.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m, s = map(int, input().split())

    # Multiplicity of the edge between every pair of vertices.
    edges = [[0] * n for _ in range(n)]

    for _ in range(m):
        u, v = map(int, input().split())
        u -= 1
        v -= 1
        edges[u][v] += 1
        edges[v][u] += 1

    limit = 1 << n

    # f[mask] = number of edges completely inside mask.
    f = [0] * limit

    # best[k] = maximum f(mask) over masks of size k.
    best = [0] * (n + 1)

    # best_mask[k] = one mask attaining best[k].
    best_mask = [0] * (n + 1)

    for mask in range(1, limit):
        bit = mask & -mask
        v = bit.bit_length() - 1
        prev = mask ^ bit

        value = f[prev]

        # Add all edges from v to vertices already in prev.
        x = prev
        row = edges[v]
        while x:
            b = x & -x
            u = b.bit_length() - 1
            value += row[u]
            x ^= b

        f[mask] = value

        size = mask.bit_count()
        if value > best[size]:
            best[size] = value
            best_mask[size] = mask

    # Unbounded knapsack.
    dp = [0] * (s + 1)
    choice = [0] * (s + 1)

    for total in range(1, s + 1):
        upper = min(n, total)
        best_value = -1

        for size in range(1, upper + 1):
            candidate = dp[total - size] + best[size]
            if candidate > best_value:
                best_value = candidate
                choice[total] = size

        dp[total] = best_value

    # Reconstruct the selected subsets.
    answer = [0] * n
    total = s

    while total > 0:
        size = choice[total]
        mask = best_mask[size]

        x = mask
        while x:
            b = x & -x
            v = b.bit_length() - 1
            answer[v] += 1
            x ^= b

        total -= size

    print(*answer)

if __name__ == "__main__":
    solve()
```

The first part of the implementation stores edge multiplicities rather than a Boolean adjacency relation. This is essential because parallel edges contribute independently to the objective.

The subset DP uses the lowest set bit to identify the newly added vertex. `prev = mask ^ bit` removes exactly that vertex, so `f[prev]` has already been computed. The loop over the bits of `prev` then adds the multiplicity of every edge from the new vertex to the old subset.

The `best` array compresses all (2^n) subsets into only (n) useful values. Once the maximum induced-edge count for each possible subset size is known, the graph-specific part of the problem is finished.

The knapsack uses increasing `total`, so `dp[total - size]` is already available. Because the same subset size can occur at many token levels, the item is intentionally reusable.

The reconstruction follows the stored subset size backwards. For each selected subset, every vertex in that subset receives one token. This is equivalent to adding that subset as one layer in the level-set representation.

Python integers do not overflow, but the objective can be as large as (100000 \cdot 100=10^7), so ordinary Python integers are more than sufficient. The only delicate indexing issue is converting the lowest set bit into a vertex index with `bit_length() - 1`.

## Worked Examples

### Sample 1

The graph has four vertices and four edges forming a triangle on vertices (1,2,3), plus an edge from vertex (1) to vertex (4). There are six tokens.

The best induced-edge counts by subset size are

[
F_1=0,\qquad F_2=1,\qquad F_3=3,\qquad F_4=4.
]

The knapsack prefers two layers of size three, giving value (3+3=6) and using exactly six tokens.

| DP total | Chosen layer size | DP value | Reconstructed token counts |
| --- | --- | --- | --- |
| 3 | 3 | 3 | (1,1,1,0) |
| 6 | 3 | 6 | (2,2,2,0) |

The final answer is

```
2 2 2 0
```

The three vertices of the triangle receive two tokens each, so each of the three triangle edges has capacity two and the fourth edge has capacity zero. The total is (6), matching the sample's optimal value.

### Sample 2

There are three vertices, seven edges, and seven tokens. The graph has five edges contributing to the two-token minimum in the supplied sample distribution, with the remaining two edges also receiving capacity two.

The important DP state is that the best three-vertex subset is the entire graph, whose induced-edge count is seven. Taking that subset twice uses six tokens and contributes fourteen. The remaining one token can be placed on a single vertex without increasing or decreasing the already obtained contribution.

| DP total | Chosen layer size | DP value | Token counts after reconstruction |
| --- | --- | --- | --- |
| 3 | 3 | 7 | (1,1,1) |
| 6 | 3 | 14 | (2,2,2) |
| 7 | 1 | 14 | (3,2,2) |

The resulting output is

```
3 2 2
```

Every edge has capacity two in the first two levels, and the final single token does not create an additional edge contribution. The resulting total is fourteen, as shown in the sample.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(n2^n+ns)) | Each subset processes at most (n) vertices, followed by an (O(ns)) knapsack |
| Space | (O(2^n+n^2+n+s)) | The subset values dominate the memory usage |

With (n=18), there are only (262144) subsets. The subset stage performs only a few million small integer operations rather than the roughly 85 million pair checks of the straightforward (O(n^2 2^n)) implementation. The knapsack has at most (18\cdot100=1800) transitions. This comfortably matches the intended small-(n), large-(m), small-(s) structure of the problem and stays well below the 512 MiB memory limit.

## Test Cases

The following test harness embeds the solution as a function and validates both the provided samples and several targeted cases. Because the problem accepts any optimal distribution, the sample checks verify the produced distribution's objective rather than requiring one particular valid output.

```python
import sys
import io

def solve_data(inp: str) -> str:
    data = list(map(int, inp.split()))
    it = iter(data)

    n = next(it)
    m = next(it)
    s = next(it)

    edges = [[0] * n for _ in range(n)]

    for _ in range(m):
        u = next(it) - 1
        v = next(it) - 1
        edges[u][v] += 1
        edges[v][u] += 1

    limit = 1 << n
    f = [0] * limit
    best = [0] * (n + 1)
    best_mask = [0] * (n + 1)

    for mask in range(1, limit):
        bit = mask & -mask
        v = bit.bit_length() - 1
        prev = mask ^ bit

        value = f[prev]
        x = prev
        row = edges[v]

        while x:
            b = x & -x
            u = b.bit_length() - 1
            value += row[u]
            x ^= b

        f[mask] = value
        size = mask.bit_count()

        if value > best[size]:
            best[size] = value
            best_mask[size] = mask

    dp = [0] * (s + 1)
    choice = [0] * (s + 1)

    for total in range(1, s + 1):
        for size in range(1, min(n, total) + 1):
            candidate = dp[total - size] + best[size]
            if candidate > dp[total]:
                dp[total] = candidate
                choice[total] = size

    ans = [0] * n
    total = s

    while total:
        size = choice[total]
        mask = best_mask[size]

        x = mask
        while x:
            b = x & -x
            v = b.bit_length() - 1
            ans[v] += 1
            x ^= b

        total -= size

    return " ".join(map(str, ans))

def objective(inp: str, output: str) -> int:
    data = list(map(int, inp.split()))
    it = iter(data)

    n = next(it)
    m = next(it)
    s = next(it)

    edges = []
    for _ in range(m):
        u = next(it) - 1
        v = next(it) - 1
        edges.append((u, v))

    ans = list(map(int, output.split()))

    assert len(ans) == n
    assert sum(ans) == s
    assert all(0 <= x <= s for x in ans)

    return sum(min(ans[u], ans[v]) for u, v in edges)

def brute_optimum(inp: str) -> int:
    data = list(map(int, inp.split()))
    it = iter(data)

    n = next(it)
    m = next(it)
    s = next(it)

    edges = []
    for _ in range(m):
        edges.append((next(it) - 1, next(it) - 1))

    best = -1

    def dfs(pos, remaining, a):
        nonlocal best

        if pos == n - 1:
            a[pos] = remaining
            value = sum(min(a[u], a[v]) for u, v in edges)
            best = max(best, value)
            return

        for x in range(remaining + 1):
            a[pos] = x
            dfs(pos + 1, remaining - x, a)

    dfs(0, s, [0] * n)
    return best

def run(inp: str) -> str:
    return solve_data(inp)

# Provided sample 1
sample1 = """\
4 4 6
1 2
2 3
3 1
1 4
"""

out = run(sample1)
assert objective(sample1, out) == 6, "sample 1"

# Provided sample 2
sample2 = """\
3 7 7
1 2
1 2
1 2
1 3
1 3
2 3
2 3
"""

out = run(sample2)
assert objective(sample2, out) == 14, "sample 2"

# Minimum-size input
case_min = """\
1 0 0
"""
assert run(case_min) == "0", "minimum-size case"

# All vertices form a triangle, with five tokens.
case_equal = """\
3 3 5
1 2
2 3
1 3
"""
out = run(case_equal)
assert out == "2 2 1", "all-equal complete graph case"
assert objective(case_equal, out) == 4

# Parallel edges, catching Boolean-adjacency mistakes.
case_parallel = """\
2 5 3
1 2
1 2
1 2
1 2
1 2
"""
out = run(case_parallel)
assert out == "2 1", "parallel-edge case"
assert objective(case_parallel, out) == 5

# Boundary case where s is much larger than n.
case_large_s = """\
2 1 100
1 2
"""
out = run(case_large_s)
assert out == "50 50", "large-s boundary case"
assert objective(case_large_s, out) == 50

# Maximum n and s, complete graph.
n = 18
edges = []
for u in range(1, n + 1):
    for v in range(u + 1, n + 1):
        edges.append((u, v))

max_case = f"{n} {len(edges)} 100\n" + "\n".join(
    f"{u} {v}" for u, v in edges
) + "\n"

out = run(max_case)
assert out == "6 6 6 6 6 6 6 6 6 6 5 5 5 5 5 5 5 5", \
    "maximum-size complete graph case"

print("all tests passed")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 0 0` | `0` | Minimum (n), zero tokens |
| Complete triangle with (s=5) | `2 2 1` | Repeated layers and all-equal graph structure |
| Two vertices with five parallel edges | `2 1` | Parallel-edge multiplicities |
| One edge with (s=100) | `50 50` | Large token count and balanced allocation |
| Complete graph on 18 vertices with (s=100) | `6 6 6 6 6 6 6 6 6 6 5 5 5 5 5 5 5 5` | Maximum (n), maximum (s), and large subset enumeration |

## Edge Cases

When (s=0), there are no level sets at all. The knapsack starts and ends at `dp[0]`, reconstruction performs no iterations, and every answer entry remains zero. For the exact input

```
1 0 0
```

the algorithm outputs

```
0
```

with total capacity zero.

When there are parallel edges, the matrix stores their multiplicity. For

```
2 5 3
1 2
1 2
1 2
1 2
1 2
```

the only useful subset is ({1,2}), whose induced-edge count is five. The knapsack chooses that two-vertex layer once and a one-vertex layer once, producing `2 1`. The five parallel edges all have capacity one, so the total is five. A Boolean adjacency matrix would incorrectly calculate the subset value as one.

When (s) is much larger than (n), the same subset can be selected many times. For

```
2 1 100
1 2
```

the best layer has size two and value one. The knapsack chooses fifty such layers, using all one hundred tokens. Both vertices consequently receive fifty tokens, and the single edge has capacity fifty.

For a complete graph on three vertices with five tokens,

```
3 3 5
1 2
2 3
1 3
```

the best size-three subset has three edges, while the best size-two subset has one edge. The optimal knapsack decomposition uses one size-three layer and one size-two layer. The reconstructed allocation is `2 2 1`, whose three edge capacities are (2,1,1), for a total of four. This case exercises repeated subset sizes and demonstrates why the level-set interpretation is more useful than reasoning directly about individual tokens.

The maximum-size case has (n=18), so there are (262144) subsets. The implementation still handles every subset because the induced-edge count is obtained from a previously computed subset instead of rescanning the entire graph. This is exactly where the (n\le18) constraint is exploited: the exponential part depends on the number of vertices, while the large number of input edges is absorbed into the (18\times18) multiplicity matrix.

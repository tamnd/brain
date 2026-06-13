---
title: "CF 1657E - Star MST"
description: "We have a complete graph on n labeled vertices. Every edge receives an integer weight between 1 and k. Vertex 1 plays a special role. Consider the star centered at vertex 1, consisting of all edges (1, v) for v 1."
date: "2026-06-10T03:29:55+07:00"
tags: ["codeforces", "competitive-programming", "combinatorics", "dp", "graph-matchings", "math"]
categories: ["algorithms"]
codeforces_contest: 1657
codeforces_index: "E"
codeforces_contest_name: "Educational Codeforces Round 125 (Rated for Div. 2)"
rating: 2200
weight: 1657
solve_time_s: 124
verified: true
draft: false
---

[CF 1657E - Star MST](https://codeforces.com/problemset/problem/1657/E)

**Rating:** 2200  
**Tags:** combinatorics, dp, graph matchings, math  
**Solve time:** 2m 4s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a complete graph on `n` labeled vertices. Every edge receives an integer weight between `1` and `k`.

Vertex `1` plays a special role. Consider the star centered at vertex `1`, consisting of all edges `(1, v)` for `v > 1`. The total weight of this star is simply the sum of those `n - 1` edge weights.

A graph is called beautiful when the weight of its minimum spanning tree is exactly equal to the weight of that star.

The task is to count how many complete weighted graphs satisfy this condition, modulo `998244353`.

The constraints are the first hint that the solution must be heavily combinatorial. A complete graph on 250 vertices contains more than 31,000 edges. Even writing down all edge assignments is impossible. The number of possible weighted graphs is

$$k^{\binom n2},$$

which is astronomically large.

Since both `n` and `k` are at most `250`, a dynamic programming solution with roughly `O(n^2 k)` or `O(n^3)` states is realistic. Anything that tries to reason about individual graphs or MST computations directly is completely out of reach.

The tricky part is understanding what the MST condition actually means.

Consider three vertices `1, u, v`. Suppose

$$w(u,v) < \max(w(1,u), w(1,v)).$$

Then in the star, the heavier of the two edges `(1,u)` and `(1,v)` can be replaced by `(u,v)`, producing a spanning tree with strictly smaller weight. That would make the star non-optimal.

For example, if

$$w(1,u)=5,\quad w(1,v)=3,\quad w(u,v)=2,$$

the star has contribution `5 + 3` from these two vertices, but replacing edge `(1,u)` by `(u,v)` decreases the total weight by `3`.

A careless approach might only check whether the star itself is an MST. The actual condition is stronger: the MST weight must equal the star weight. Since the star is already a spanning tree, equality means the star must be a minimum spanning tree.

A useful small example is `n = 3`, `k = 2`.

Let

$$a=w(1,2),\quad b=w(1,3),\quad c=w(2,3).$$

The star is an MST exactly when

$$c \ge \max(a,b).$$

The valid assignments are:

| a | b | valid c |
| --- | --- | --- |
| 1 | 1 | 1,2 |
| 1 | 2 | 2 |
| 2 | 1 | 2 |
| 2 | 2 | 2 |

Total = 5, matching the sample output.

## Approaches

The brute force idea is straightforward. Assign a weight to every edge, run an MST algorithm, compute the star weight, and compare the two values.

The problem is the number of assignments. A complete graph contains

$$\binom n2$$

edges, so the number of weighted graphs is

$$k^{\binom n2}.$$

For `n = 250`, this is completely impossible.

The key observation is that the MST condition can be rewritten as a local constraint on every non-star edge.

Let

$$a_i = w(1,i).$$

These are the star edge weights.

The star is an MST if and only if every edge between non-root vertices satisfies

$$w(i,j) \ge \max(a_i,a_j).$$

Why?

If some edge is smaller than that maximum, we can replace the heavier star edge and obtain a lighter spanning tree.

Conversely, if every non-star edge is at least that maximum, then for every edge `(i,j)` the unique path in the star contains weights `a_i` and `a_j`, and the largest weight on that path is exactly `max(a_i,a_j)`. The edge `(i,j)` is never cheaper than the largest edge on the path, which is precisely the MST characterization given by the cycle property. The star is then an MST.

Now the problem becomes counting assignments of the values `a_i`.

Once the star weights are fixed, every edge `(i,j)` has

$$k-\max(a_i,a_j)+1$$

valid choices.

Thus the answer equals

$$\sum_{a_2,\dots,a_n} \prod_{i<j} \bigl(k-\max(a_i,a_j)+1\bigr).$$

A direct evaluation is still impossible because there are `k^(n-1)` star assignments.

The remaining insight is that only the counts of vertices having each star weight matter.

We process weights from `1` to `k` and build the set of vertices whose star-edge weight has already been determined. This leads to a DP over weight levels and vertex counts.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(k^{\binom n2})$ | Huge | Too slow |
| Optimal DP | $O(k n^2)$ | $O(kn)$ | Accepted |

## Algorithm Walkthrough

Let `N = n - 1`. We only need to assign star weights for the vertices `2...n`.

Define:

$$dp[w][t]$$

as the number of ways after processing weight values `1...w`, where exactly `t` vertices have already received a star weight at most `w`.

Initially,

$$dp[0][0]=1.$$

Suppose we are processing weight `w`.

Assume `t` vertices have already been assigned smaller weights.

Choose `x` new vertices whose star weight becomes exactly `w`.

Then the new count becomes

$$t+x.$$

### Counting the edge contributions

Every newly added vertex has star weight exactly `w`.

Consider pairs whose maximum star weight equals `w`.

There are two kinds:

1. One endpoint among the old `t` vertices and one among the `x` new vertices.

Count:

$$t \cdot x.$$

1. Both endpoints among the `x` new vertices.

Count:

$$\frac{x(x-1)}2.$$

Total:

$$E=tx+\frac{x(x-1)}2.$$

For every such pair, the corresponding edge `(i,j)` may take any value in

$$[w,k].$$

Hence each pair contributes

$$k-w+1$$

choices.

The total contribution is

$$(k-w+1)^E.$$

### Counting which vertices receive weight `w`

Among the remaining `N-t` vertices, choose `x` of them:

$$\binom{N-t}{x}.$$

Thus the transition is

$$dp[w][t+x] += dp[w-1][t] \cdot \binom{N-t}{x} \cdot (k-w+1)^E.$$

After processing all weight values, every vertex must have been assigned:

$$\text{answer}=dp[k][N].$$

### Why it works

The DP constructs the multiset of star-edge weights level by level.

When weight `w` is processed, all vertex pairs whose larger endpoint weight is exactly `w` become fully determined. Every such pair contributes independently exactly `k-w+1` choices for its non-star edge.

Each pair is counted once, namely when its larger endpoint weight first appears. The exponent

$$tx+\frac{x(x-1)}2$$

is exactly the number of pairs whose maximum star weight equals `w`.

Multiplying all these independent contributions counts every beautiful graph exactly once, and every counted graph satisfies the MST characterization above.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 998244353

def main():
    n, k = map(int, input().split())

    N = n - 1

    C = [[0] * (N + 1) for _ in range(N + 1)]
    C[0][0] = 1
    for i in range(1, N + 1):
        C[i][0] = C[i][i] = 1
        for j in range(1, i):
            C[i][j] = (C[i - 1][j - 1] + C[i - 1][j]) % MOD

    max_pairs = N * (N - 1) // 2

    pw = [[1] * (max_pairs + 1) for _ in range(k + 1)]
    for w in range(1, k + 1):
        base = k - w + 1
        for e in range(1, max_pairs + 1):
            pw[w][e] = pw[w][e - 1] * base % MOD

    dp = [[0] * (N + 1) for _ in range(k + 1)]
    dp[0][0] = 1

    for w in range(1, k + 1):
        for t in range(N + 1):
            cur = dp[w - 1][t]
            if cur == 0:
                continue

            rem = N - t

            for x in range(rem + 1):
                nt = t + x

                pairs = t * x + x * (x - 1) // 2

                ways = cur
                ways = ways * C[rem][x] % MOD
                ways = ways * pw[w][pairs] % MOD

                dp[w][nt] = (dp[w][nt] + ways) % MOD

    print(dp[k][N])

if __name__ == "__main__":
    main()
```

The combination table counts which vertices receive a particular star weight. Since `N ≤ 249`, a simple Pascal triangle is sufficient.

The transition exponent

$$t x + \frac{x(x-1)}2$$

is the heart of the solution. It counts exactly the vertex pairs whose maximum assigned star weight becomes the current weight.

The power values are precomputed because the same bases appear many times. Without this preprocessing, repeated modular exponentiation inside the DP would be unnecessarily expensive.

The state uses `N = n - 1` because only vertices other than the root need a star-weight assignment. This small reduction keeps the formulas cleaner.

## Worked Examples

### Sample 1

Input:

```
3 2
```

Here `N = 2`.

| Weight w | t before | x chosen | nt | pairs | factor |
| --- | --- | --- | --- | --- | --- |
| 1 | 0 | 0 | 0 | 0 | 1 |
| 1 | 0 | 1 | 1 | 0 | 2 |
| 1 | 0 | 2 | 2 | 1 | 2 |
| 2 | continue DP |  |  |  |  |

After all transitions finish:

| State | Value |
| --- | --- |
| dp[2][2] | 5 |

Answer:

```
5
```

This example demonstrates that the DP is counting star-weight assignments and valid non-star edge assignments simultaneously.

### Example 2

Input:

```
2 3
```

There is only one star edge.

| Weight w | t before | x | nt |
| --- | --- | --- | --- |
| 1 | 0 | 1 | 1 |
| 2 | 0 | 1 | 1 |
| 3 | 0 | 1 | 1 |

No non-star edges exist, so every choice of the single edge weight is valid.

| Final state | Value |
| --- | --- |
| dp[3][1] | 3 |

Answer:

```
3
```

This confirms that the formula correctly handles the smallest graph.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(kn^2)$ | For each weight, iterate over current assigned count and newly added count |
| Space | $O(kn)$ | DP table plus combinatorial precomputations |

With `n, k ≤ 250`, the number of DP transitions is roughly

$$250 \times 250 \times 250 \approx 1.6\times10^7,$$

which comfortably fits within the 6-second limit in optimized Python.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    MOD = 998244353

    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    n, k = map(int, input().split())
    N = n - 1

    C = [[0] * (N + 1) for _ in range(N + 1)]
    C[0][0] = 1
    for i in range(1, N + 1):
        C[i][0] = C[i][i] = 1
        for j in range(1, i):
            C[i][j] = (C[i - 1][j - 1] + C[i - 1][j]) % MOD

    max_pairs = N * (N - 1) // 2

    pw = [[1] * (max_pairs + 1) for _ in range(k + 1)]
    for w in range(1, k + 1):
        base = k - w + 1
        for e in range(1, max_pairs + 1):
            pw[w][e] = pw[w][e - 1] * base % MOD

    dp = [[0] * (N + 1) for _ in range(k + 1)]
    dp[0][0] = 1

    for w in range(1, k + 1):
        for t in range(N + 1):
            cur = dp[w - 1][t]
            if cur == 0:
                continue

            rem = N - t
            for x in range(rem + 1):
                pairs = t * x + x * (x - 1) // 2
                dp[w][t + x] = (
                    dp[w][t + x]
                    + cur * C[rem][x] * pw[w][pairs]
                ) % MOD

    return str(dp[k][N])

# provided sample
assert run("3 2\n") == "5"

# minimum graph
assert run("2 1\n") == "1"

# one edge, three possible weights
assert run("2 3\n") == "3"

# official sample
assert run("4 4\n") == "571"

# larger official sample
assert run("6 9\n") == "310640163"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2 1` | `1` | Smallest possible graph |
| `2 3` | `3` | No non-star edges exist |
| `3 2` | `5` | Basic MST constraint counting |
| `4 4` | `571` | Official sample |
| `6 9` | `310640163` | Larger official sample |

## Edge Cases

Consider:

```
2 1
```

There is only one edge in the graph. The star is the entire graph and also the unique spanning tree. The DP has `N = 1`, assigns the only vertex to weight `1`, and returns `1`.

Consider:

```
2 5
```

Again there are no non-star edges. Any weight from `1` to `5` works. The transition simply chooses one of the five levels for the lone vertex, producing answer `5`.

Consider:

```
3 2
```

The dangerous configuration is

$$w(1,2)=2,\quad w(1,3)=1,\quad w(2,3)=1.$$

A naive counting method might accept it because all weights lie in range. Our characterization rejects it because

$$1 < \max(2,1).$$

The DP never counts this graph, since edges whose maximum star weight equals `2` are only allowed values from `[2,2]`.

Consider:

```
3 1
```

Every edge weight is forced to be `1`. The star has weight `2`, every spanning tree has weight `2`, and the answer is exactly `1`. The DP handles this naturally because every multiplicative factor becomes `1`.

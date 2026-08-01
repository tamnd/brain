---
title: "CF 102726J - Risk"
description: "The problem asks us to view a graph as a model of correlated random variables. Each vertex represents a zero-mean random variable. A variable's variance is equal to its vertex degree, adjacent variables have covariance -1, and non-adjacent variables have covariance 0."
date: "2026-08-01T22:11:19+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102726
codeforces_index: "J"
codeforces_contest_name: "UTPC Contest 9-11-20 Div. 1"
rating: 0
weight: 102726
solve_time_s: 88
verified: true
draft: false
---

[CF 102726J - Risk](https://codeforces.com/problemset/problem/102726/J)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 28s  
**Verified:** yes  

## Solution
# Problem Understanding

The problem asks us to view a graph as a model of correlated random variables. Each vertex represents a zero-mean random variable. A variable's variance is equal to its vertex degree, adjacent variables have covariance `-1`, and non-adjacent variables have covariance `0`. We must choose coefficients for a linear combination of these variables, with the sum of squared coefficients fixed to `1`, and maximize the standard deviation of that combination.

The input gives an undirected unweighted graph. The output is the largest possible standard deviation of any normalized linear combination of the variables associated with the vertices.

The graph has at most `100` vertices and `1600` edges. These bounds are small enough that we can afford algorithms involving repeated passes over all edges or all vertices. However, they are not large enough to justify heavy general-purpose matrix decomposition routines in a contest environment, so we need to exploit the structure of the matrix created by the graph.

The key observation is that the covariance matrix is exactly the graph Laplacian. For every vertex, the diagonal entry is its degree. For every edge, the two corresponding off-diagonal entries are `-1`. All other entries are zero. The largest variance of a normalized linear combination is the largest eigenvalue of this symmetric matrix, and the answer is its square root.

A common mistake is to search only among individual variables. For example, a graph with two connected vertices has each variable variance equal to `1`, but combining them with opposite signs gives variance `4`, producing standard deviation `2`? Actually, for the covariance matrix `[[1,-1],[-1,1]]`, the largest eigenvalue is `2`, so the answer is `sqrt(2)`. The maximizing combination uses both variables together, which is why checking vertices independently fails.

Another edge case is a disconnected graph. Consider:

```
3 1
0 1
```

The correct output is approximately:

```
1.4142135623730951
```

The isolated vertex contributes a zero eigenvalue. A careless implementation that assumes the graph must be connected or removes isolated vertices changes the matrix and can lose the correct spectrum.

A final subtle case is a graph where all degrees are equal. For example:

```
3 3
0 1
1 2
2 0
```

The covariance matrix is the triangle graph Laplacian. The largest eigenvalue is `3`, so the answer is approximately `1.7320508075688772`. Looking only at degrees would incorrectly suggest every direction has variance `2`.

## Approaches

The direct approach is to build the covariance matrix and run a general eigenvalue decomposition. This is mathematically straightforward because the answer is the square root of the largest eigenvalue. However, implementing a full eigensolver is unnecessary and error-prone, especially when we only need one eigenvalue.

A simpler brute force idea is to try to construct candidate coefficient vectors and search for the maximum variance. The variance of a coefficient vector `a` is `a^T L a`, where `L` is the Laplacian. Since the coefficient space has infinitely many possible directions, enumerating candidates is impossible. Even restricting coefficients to a grid would require an exponential number of possibilities.

The important structure is that `L` is symmetric. For symmetric matrices, repeatedly multiplying by the matrix pushes a vector toward the direction of the largest eigenvalue. This is the power iteration method. The graph Laplacian also allows multiplication without storing the full matrix. For every edge `(u, v)`, the Laplacian multiplication contributes `x[u] - x[v]` to vertex `u` and `x[v] - x[u]` to vertex `v`.

The brute force fails because the optimal direction is a continuous eigenvector hidden inside the coefficient space. The observation that the answer is an extreme eigenvalue of a symmetric matrix lets us replace the search with repeated sparse matrix-vector multiplication.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential or worse | Large | Too slow |
| Full Eigen Decomposition | Depends on implementation, usually O(n³) | O(n²) | Unnecessary |
| Power Iteration | O(iterations × (n + m)) | O(n + m) | Accepted |

## Algorithm Walkthrough

1. Build the graph representation. Store every edge because multiplying by the Laplacian only requires visiting edges, not storing all `n × n` matrix entries.
2. Start with a non-zero coefficient vector and normalize it. The vector must have some component in the direction of the largest eigenvector, otherwise power iteration would not discover it.
3. Repeatedly multiply the current vector by the Laplacian. For an edge connecting `u` and `v`, add `x[u] - x[v]` to the result at `u` and add `x[v] - x[u]` to the result at `v`.
4. Normalize the resulting vector after every multiplication. Without normalization, the values grow exponentially with the eigenvalue and eventually become numerically unstable.
5. Estimate the eigenvalue using the Rayleigh quotient:

$$\lambda = \frac{x^T Lx}{x^Tx}$$

For the normalized vector this becomes simply `x · (Lx)`.

1. Output the square root of the estimated largest eigenvalue because the problem asks for standard deviation rather than variance.

The reason this works is that the Laplacian is a real symmetric matrix, so it has an orthogonal eigenbasis. Repeated multiplication scales every eigenvector component by its eigenvalue. The component belonging to the largest eigenvalue grows fastest, causing the vector to converge toward that eigenvector. The Rayleigh quotient then converges to the largest eigenvalue itself.

## Python Solution

```python
import sys
import math

input = sys.stdin.readline

def solve():
    line = input().split()
    if not line:
        return
    n, m = map(int, line)

    edges = []
    for _ in range(m):
        u, v = map(int, input().split())
        edges.append((u, v))

    vec = [i + 1.0 for i in range(n)]
    norm = math.sqrt(sum(x * x for x in vec))
    vec = [x / norm for x in vec]

    for _ in range(10000):
        nxt = [0.0] * n
        for u, v in edges:
            d = vec[u] - vec[v]
            nxt[u] += d
            nxt[v] -= d

        norm = math.sqrt(sum(x * x for x in nxt))
        if norm == 0:
            print("0.0")
            return
        vec = [x / norm for x in nxt]

    lap_vec = [0.0] * n
    for u, v in edges:
        d = vec[u] - vec[v]
        lap_vec[u] += d
        lap_vec[v] -= d

    eigenvalue = sum(vec[i] * lap_vec[i] for i in range(n))
    print(math.sqrt(max(0.0, eigenvalue)))

if __name__ == "__main__":
    solve()
```

The input section reads the graph and stores only edges. The algorithm never creates the full covariance matrix because almost all entries are zero, and edge-based multiplication is faster and uses less memory.

The initial vector uses different values instead of all ones. The all-ones vector is always an eigenvector of a Laplacian with eigenvalue zero, so starting with it would immediately lose the useful direction.

The multiplication loop performs the power iteration. The subtraction for each edge is exactly the Laplacian operation: every vertex receives its degree contribution minus the values of its neighbors.

After convergence, the code computes the Rayleigh quotient. The `max` call protects against tiny negative floating-point errors before taking the square root.

## Worked Examples

For the sample:

```
2 1
0 1
```

The Laplacian is:

$$\begin{bmatrix}
1 & -1\\
-1 & 1
\end{bmatrix}$$

The largest eigenvalue is `2`.

| Iteration | Vector direction | Estimated eigenvalue |
| --- | --- | --- |
| Start | `(1, 2)` normalized | not measured |
| Multiply | direction approaches `(1, -1)` | close to `2` |
| Final | dominant eigenvector | `2` |

The output is:

```
1.4142135623730951
```

because the required value is the standard deviation, which is the square root of the variance.

A triangle graph:

```
3 3
0 1
1 2
2 0
```

has degree `2` at every vertex.

| Iteration | Vector property | Estimated eigenvalue |
| --- | --- | --- |
| Start | arbitrary non-zero vector | unstable |
| Repeated multiplication | removes the zero-eigenvalue component | approaches `3` |
| Final | largest eigendirection | `3` |

The answer is:

```
1.7320508075688772
```

This demonstrates that the solution depends on the whole graph structure, not only individual variances.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(k(n + m)) | `k` power iterations, each visiting all vertices and edges |
| Space | O(n + m) | Stores the edge list and a few vectors |

Here `k` is a fixed number of iterations. With only `100` vertices and `1600` edges, the repeated sparse matrix multiplications easily fit within the limits.

## Test Cases

```python
import sys
import io
import math

def run(inp: str) -> str:
    old = sys.stdin
    sys.stdin = io.StringIO(inp)

    data = sys.stdin.read().split()
    if not data:
        return ""

    it = iter(data)
    n = int(next(it))
    m = int(next(it))

    edges = []
    for _ in range(m):
        edges.append((int(next(it)), int(next(it))))

    vec = [i + 1.0 for i in range(n)]
    norm = math.sqrt(sum(x * x for x in vec))
    vec = [x / norm for x in vec]

    for _ in range(10000):
        nxt = [0.0] * n
        for u, v in edges:
            d = vec[u] - vec[v]
            nxt[u] += d
            nxt[v] -= d
        norm = math.sqrt(sum(x * x for x in nxt))
        if norm == 0:
            return "0.0"
        vec = [x / norm for x in nxt]

    lap = [0.0] * n
    for u, v in edges:
        d = vec[u] - vec[v]
        lap[u] += d
        lap[v] -= d

    ans = math.sqrt(max(0.0, sum(vec[i] * lap[i] for i in range(n))))
    sys.stdin = old
    return str(ans)

assert abs(float(run("""2 1
0 1
""")) - math.sqrt(2)) < 1e-4, "sample"

assert abs(float(run("""3 3
0 1
1 2
2 0
""")) - math.sqrt(3)) < 1e-4, "triangle"

assert abs(float(run("""1 0
""")) - 0.0) < 1e-4, "isolated vertex"

assert abs(float(run("""4 2
0 1
2 3
""")) - math.sqrt(2)) < 1e-4, "two components"

assert abs(float(run("""5 4
0 1
1 2
2 3
3 4
""")) - math.sqrt(3.6180339887)) < 1e-4, "path graph"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Two connected vertices | `sqrt(2)` | Basic Laplacian eigenvalue case |
| Triangle | `sqrt(3)` | Equal degree graph |
| Single vertex | `0` | Empty edge case |
| Two disconnected edges | `sqrt(2)` | Disconnected graphs |
| Five vertex path | Approximately `1.9021` | Non-uniform degrees |

## Edge Cases

For a graph with one isolated vertex:

```
1 0
```

the Laplacian is the one-by-one zero matrix. Power iteration detects that multiplication produces the zero vector and returns `0`. The standard deviation is correctly zero because there is no variance.

For disconnected components:

```
4 2
0 1
2 3
```

the algorithm does not need any special handling. The Laplacian multiplication works independently on each component. Power iteration finds the component containing the largest eigenvalue, which is exactly what the global maximum requires.

For a regular graph:

```
3 3
0 1
1 2
2 0
```

all vertices have the same variance, but the answer does not come from that common degree alone. The repeated multiplications capture the interaction between covariance terms, leading to the correct largest eigenvalue `3`.

For small graphs, floating-point precision is the main risk. The algorithm avoids division by nearly zero by checking the vector norm after multiplication, and it clamps tiny negative eigenvalue estimates before applying the square root.

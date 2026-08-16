---
title: "CF 102388E - Stables"
description: "We have an undirected graph with at most 50 cities. A road lets a horse move between its two endpoints in one step, and a road may also be a self-loop. For a fixed city v, we need to decide whether there exists a walk that starts at v, uses exactly k roads, and ends back at v."
date: "2026-08-16T08:50:32+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102388
codeforces_index: "E"
codeforces_contest_name: "SUFE ICPC Team Formation Test"
rating: 0
weight: 102388
solve_time_s: 360
verified: false
draft: false
---

[CF 102388E - Stables](https://codeforces.com/problemset/problem/102388/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 6m  
**Verified:** no  

## Solution
## Problem Understanding

We have an undirected graph with at most 50 cities. A road lets a horse move between its two endpoints in one step, and a road may also be a self-loop. For a fixed city v, we need to decide whether there exists a walk that starts at v, uses exactly k roads, and ends back at v. The answer is the number of cities for which such a closed walk exists.

The input contains up to 20 independent graphs. The graph is small in terms of vertices, with n≤50, but k can be as large as 10 9. That combination is the key difficulty. Any algorithm that performs one operation per day or one graph traversal per step cannot survive a billion steps. On the other hand, n=50 is small enough that we can afford algorithms involving roughly n 2 work per bit of k. Since 10 9 has only about 30 binary digits, logarithmic exponentiation is a natural target.

There are several edge cases that can easily break an implementation. When k=0, every city qualifies because the empty walk already starts and ends at the same city. For example,

```
13 0 0
```

has output

```
3
```

A solution that requires at least one road would incorrectly return zero.

Self-loops matter especially when k=1. For

```
12 1 10 0
```

the answer is `1`, because city 0 can take its self-loop once and return to itself, while city 1 is isolated. A solution that treats the graph as a simple graph without preserving diagonal entries would miss city 0.

Parallel roads do not need special treatment. If two roads connect the same pair of cities, they provide no additional possibility for existence of a walk. We only care whether at least one transition exists. For example,

```
12 3 20 10 10 1
```

has output `2`. Both cities can go to the other city and immediately return.

Finally, parity can be deceptive. In a bipartite graph, every closed walk has even length, but the existence of an odd cycle changes the situation. For example,

```
13 3 30 11 22 0
```

has output `3`, since every city lies on the triangle. Trying to solve the problem using only graph bipartiteness would also miss special cases such as a vertex attached to an odd cycle, where sufficiently long odd closed walks may exist but short ones may not. The matrix formulation avoids having to manually characterize all of these cases.

## Approaches

The most direct approach is to simulate possible positions after each step. Fix a starting city s, keep the set of cities reachable after exactly t steps, and repeatedly expand that set through the graph. After k rounds, check whether s is reachable. This is correct because the set after round t represents exactly the endpoints of walks of length t starting from s.

The problem is k. In the worst case, one round may inspect every road, so processing one starting city takes O(km). Repeating this for all n starting cities gives O(knm). At the maximum constraints this is roughly

10 9 ⋅50⋅2500=1.25×10 14

road examinations, which is far beyond the time limit.

The graph is small enough to replace step-by-step simulation with matrix exponentiation. Define a Boolean adjacency matrix A, where A[i][j] is true exactly when a road permits a move from i to j. Under Boolean matrix multiplication, the entry (A t )[i][j] tells us whether there exists a walk of exactly t steps from i to j. Consequently, city i is valid exactly when the diagonal entry (A k )[i][i] is true.

Binary exponentiation reduces the number of matrix multiplications from k to O(logk). A conventional matrix multiplication would cost O(n 3 ), which is already reasonable for n=50, but Python can do even better here by representing each matrix row as a single integer bitset. A row then contains the set of reachable vertices as bits, and multiplying two Boolean matrices becomes a sequence of bitwise OR operations.

For a row i of the left matrix, every set bit j means that i can reach j. The corresponding row B[j] of the right matrix contains all vertices reachable from j. Thus the resulting row is simply the OR of B[j] over all set bits j in row i. This reduces the practical multiplication to O(n 2 ) row operations, with each operation using Python's highly optimized arbitrary-precision integers.

The brute-force method works because it explicitly follows walks one step at a time, but fails because k is enormous. The observation that only the binary representation of k matters lets us jump through exponentially many steps at once.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(knm) | O(n) | Too slow |
| Boolean Matrix Exponentiation with Bitsets | O(n 2 logk) bitset operations | O(n) bitsets | Accepted |

## Algorithm Walkthrough

1. Build the adjacency relation as a bitset for every city. Bit j in row i is set when a road exists between i and j. Because the graph is undirected, an input edge (x,y) sets both x→y and y→x. For a self-loop, this naturally sets the diagonal bit.
2. Represent the identity matrix as bitsets. Its row i contains only bit i, because the identity matrix represents a walk of length zero that stays at the same city.
3. Maintain two Boolean matrices, `result` and `base`. Initially, `result` is the identity matrix and `base` is the adjacency matrix. The invariant is that `result` represents the product of the powers of the original adjacency matrix already selected from the processed bits of k, while `base` represents the current power A 2 p.
4. Inspect the binary representation of k from its least significant bit. If the current bit is one, multiply `result` by `base`. This incorporates the corresponding power A 2 p into the answer.
5. Square `base` to obtain the next power of two. Boolean matrix multiplication is used here because we care whether at least one walk exists, not how many walks exist.
6. Shift k right by one bit and continue until every bit has been processed. At most 30 bits are needed because k≤10 9.
7. After exponentiation, inspect the diagonal of `result`. If bit i is set in row i, then there is a walk of exactly k steps from city i back to city i. Count all such cities.

### Why it works

The central invariant is that after processing some prefix of the binary representation of k, `result` equals the Boolean product of exactly the powers corresponding to the processed one-bits. Since Boolean matrix multiplication composes the existence of walks, A t [i][j] is true exactly when some length-t walk connects i to j. Binary exponentiation eventually constructs A k, so its diagonal contains precisely the cities that admit a closed walk of length k. The bitset implementation changes only how the Boolean multiplication is computed, not what mathematical result it represents.

## Python Solution

```python
Pythonimport sysinput = sys.stdin.readline

def multiply(A, B, n):    """    Boolean matrix multiplication.
    Each row is a bitset. For every set bit j in A[i],    row B[j] contributes all vertices reachable after the    second part of the walk.    """    C = [0] * n
    for i in range(n):        mask = A[i]        row = 0
        while mask:            bit = mask & -mask            j = bit.bit_length() - 1            row |= B[j]            mask ^= bit
        C[i] = row
    return C

def solve():    T = int(input())    answers = []
    for _ in range(T):        n, m, k = map(int, input().split())
        adj = [0] * n
        for _ in range(m):            x, y = map(int, input().split())            adj[x] |= 1 << y            adj[y] |= 1 << x
        # A^0 = I.        result = [1 << i for i in range(n)]
        # A^(2^p), starting with A^1.        base = adj
        while k:            if k & 1:                result = multiply(result, base, n)
            k >>= 1
            if k:                base = multiply(base, base, n)
        answer = 0        for i in range(n):            if result[i] & (1 << i):                answer += 1
        answers.append(str(answer))
    sys.stdout.write("\n".join(answers))

if __name__ == "__main__":    solve()
```

The adjacency construction uses one integer per city. Bit `j` represents city `j`, so setting `1 << j` records the existence of a transition to that city. Setting both directions handles the undirected road, and doing the same operation twice for a parallel edge has no effect, which is exactly what we want.

`result = [1 << i for i in range(n)]` creates the identity matrix. This is necessary even when k=0, because A 0 =I, and the diagonal of the identity contains every city. The `while k` loop consequently handles k=0 without any special branch.

The multiplication routine deserves the most attention. Suppose bit j is set in `A[i]`. That means there is a first-step segment from i to j. Every bit set in `B[j]` represents a second segment from j to some destination. Taking the OR over all such `B[j]` therefore gives exactly the destinations reachable through the concatenated walk.

The expression `mask & -mask` extracts the lowest set bit. `bit.bit_length() - 1` converts that bit into its vertex index. Removing it with `mask ^= bit` guarantees that every reachable intermediate vertex is processed once.

There is no integer overflow issue. Python integers grow automatically, and the largest bitset has only 50 meaningful bits. The value of k is also handled directly as a Python integer, so the 10 9 bound requires no special arithmetic.

The order of the operations in the exponentiation loop is also deliberate. If the current bit of k is one, the current power must be multiplied into `result`. After that, the current power is squared to prepare the next binary digit. The `if k` guard avoids one unnecessary final squaring.

## Worked Examples

The first sample testcase is

```
3 2 30 10 2
```

The graph is a path of length two, with city 0 in the middle. We want a closed walk of length 3.

The adjacency rows are represented by bitsets. Bit positions 0, 1, and 2 correspond to the three cities.

| Stage | k | `result` rows | `base` represents |
| --- | --- | --- | --- |
| Initial | 3 | `001`, `010`, `100` | A 1 |
| Bit 0 = 1 | 3 | A | A 1 |
| Shift | 1 | A | A 2 |
| Bit 1 = 1 | 1 | A 3 | A 2 |
| Finish | 0 | A 3 | A 2 |

There is no odd cycle and no self-loop, so the graph is bipartite and every closed walk has even length. The diagonal of A 3 is entirely false, giving answer `0`.

The second sample testcase is

```
3 2 40 10 2
```

This is the same graph, but now k=4.

| Stage | k | `result` | `base` |
| --- | --- | --- | --- |
| Initial | 4 | I | A |
| Shift | 2 | I | A 2 |
| Shift | 1 | I | A 4 |
| Bit 2 = 1 | 1 | A 4 | A 4 |
| Finish | 0 | A 4 | A 4 |

Every city has a length-4 closed walk. From city 1, for example, we can use

1→0→1→0→1.

The same construction works for city 2, while city 0 can alternate with either neighbor. Thus every diagonal entry of A 4 is true and the answer is `3`.

These two traces also show why looking only at reachability without tracking the exact walk length would be insufficient. The graph is connected in both cases, but length 3 produces no closed walk while length 4 produces one at every city.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n 2 logk) bitset operations | There are O(logk) matrix products, and each product processes at most n 2 set bits |
| Space | O(n) Python integers | Two n-row Boolean matrices are stored, with each row containing only n relevant bits |

For n≤50 and k≤10 9, there are at most 30 exponentiation levels. Each Boolean matrix multiplication processes at most 50 2 =2500 row relationships, and each relationship is handled through native integer bit operations. This is comfortably within the 3 second time limit and far below the 256 MB memory limit.

The distinction between this implementation and ordinary O(n 3 logk) matrix multiplication is useful in Python. The bitset representation compresses an entire Boolean row into one integer, so the expensive inner operation is performed by optimized integer arithmetic rather than a Python-level loop over all possible destinations.

## Test Cases

```python
Pythonimport sysimport io

def solve_data(inp: str) -> str:    old_stdin = sys.stdin    old_stdout = sys.stdout
    sys.stdin = io.StringIO(inp)    out = io.StringIO()    sys.stdout = out
    try:        T = int(sys.stdin.readline())        answers = []
        def multiply(A, B, n):            C = [0] * n
            for i in range(n):                mask = A[i]                row = 0
                while mask:                    bit = mask & -mask                    j = bit.bit_length() - 1                    row |= B[j]                    mask ^= bit
                C[i] = row
            return C
        for _ in range(T):            n, m, k = map(int, sys.stdin.readline().split())            adj = [0] * n
            for _ in range(m):                x, y = map(int, sys.stdin.readline().split())                adj[x] |= 1 << y                adj[y] |= 1 << x
            result = [1 << i for i in range(n)]            base = adj
            while k:                if k & 1:                    result = multiply(result, base, n)
                k >>= 1
                if k:                    base = multiply(base, base, n)
            answer = sum(                1 for i in range(n)                if result[i] & (1 << i)            )            answers.append(str(answer))
        sys.stdout.write("\n".join(answers))        return out.getvalue()
    finally:        sys.stdin = old_stdin        sys.stdout = old_stdout

# Provided sampleassert solve_data("""\33 2 30 10 23 2 40 10 25 5 50 11 22 03 44 0""") == "0\n3\n4", "provided sample"

# Minimum-size graph, k = 0.# The empty walk is valid at the only city.assert solve_data("""\11 0 0""") == "1", "k = 0"

# One vertex with a self-loop.# The loop can be traversed any positive number of times.assert solve_data("""\11 1 10 0""") == "1", "self-loop and k = 1"

# Two isolated vertices, k > 0.# There is no road at all, so no positive-length walk exists.assert solve_data("""\12 0 7""") == "0", "isolated vertices"

# Parallel edges and an even walk.# Multiplicity does not matter because we only ask whether a walk exists.assert solve_data("""\12 3 20 10 10 1""") == "2", "parallel edges"

# A triangle, k = 3.# Every vertex can traverse the triangle once and return.assert solve_data("""\13 3 30 11 22 0""") == "3", "odd cycle"

# Maximum-size vertex count and a huge k.# Complete graph has a closed walk of every positive length at every vertex.edges = []n = 50for i in range(n):    for j in range(i + 1, n):        edges.append(f"{i} {j}")
max_case = "1\n50 1225 1000000000\n" + "\n".join(edges) + "\n"assert solve_data(max_case) == "50", "maximum n and huge k"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 0 0` | `1` | Minimum graph and the k=0 boundary |
| One vertex with one loop, k=1 | `1` | Self-loop and exact one-step return |
| Two isolated vertices, k=7 | `0` | No positive-length walk |
| Three parallel edges between two vertices, k=2 | `2` | Parallel edges do not affect existence |
| Triangle, k=3 | `3` | Odd closed walks |
| Complete graph on 50 vertices, k=10 9 | `50` | Maximum n, huge k, and binary exponentiation |

## Edge Cases

### Zero steps

Consider

```
13 0 0
```

The algorithm initializes `result` to the identity matrix and never enters the exponentiation loop because `k` is zero. The identity matrix has every diagonal entry set, so all three cities are counted. This matches the definition of a length-zero walk.

### Self-loop with one step

Consider

```
12 1 10 0
```

The adjacency row of city 0 contains bit 0, while city 1 has an empty row. Since k=1, `result` becomes the adjacency matrix itself. Its diagonal contains a true value only at city 0, so the answer is `1`.

This case catches implementations that accidentally ignore self-loops or only insert an edge when its endpoints are different.

### Isolated vertices

Consider

```
12 0 7
```

The adjacency matrix is all zeroes. Every positive power of the zero Boolean matrix remains zero, so no diagonal entry is set. The answer is `0`. The identity matrix does not cause a false positive because it is used only for exponent zero, and here the exponent is positive.

### Parallel roads

Consider

```
12 3 20 10 10 1
```

The three input roads all set the same two adjacency bits. After construction, the matrix is exactly the adjacency matrix of a single undirected edge. Squaring it gives a diagonal true at both vertices, corresponding to the walks 0→1→0 and 1→0→1. The answer is `2`.

Treating the input as a multigraph with counts would be unnecessary because the problem asks for existence rather than the number of possible walks.

### Odd cycle

Consider

```
13 3 30 11 22 0
```

The first power allows one edge, and cubing the Boolean adjacency matrix detects the triangle walk from every vertex back to itself. The diagonal of A 3 is entirely true, so the answer is `3`.

This is also why a solution based only on even or odd k is insufficient. The graph structure determines which exact lengths are possible, and Boolean matrix powers represent that structure directly.

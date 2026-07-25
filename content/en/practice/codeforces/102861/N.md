---
title: "CF 102861N - Number Multiplication"
description: "There are M hidden nodes. Each hidden node owns one unknown prime number, and the primes are arranged in increasing order by node index. There are also N visible nodes."
date: "2026-07-25T14:09:42+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102861
codeforces_index: "N"
codeforces_contest_name: "2020-2021 ACM-ICPC Brazil Subregional Programming Contest"
rating: 0
weight: 102861
solve_time_s: 62
verified: true
draft: false
---

[CF 102861N - Number Multiplication](https://codeforces.com/problemset/problem/102861/N)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 2s  
**Verified:** yes  

## Solution
## Problem Understanding

There are `M` hidden nodes. Each hidden node owns one unknown prime number, and the primes are arranged in increasing order by node index. There are also `N` visible nodes. A visible node stores the product of the primes of all hidden nodes connected to it, where repeated edges mean repeated multiplication.

The input gives the products stored on the `N` visible nodes and the complete list of connections with their multiplicities. The original prime labels of the hidden nodes disappeared, and the task is to recover them in increasing order of hidden node index.

The important observation is that the graph already tells us the exponent pattern of every hidden prime. If hidden node `j` has `d` edges to visible node `i`, then the prime belonging to node `j` appears with exponent `d` in `c[i]`. So every hidden node corresponds to one row of an exponent matrix.

The constraints point toward factoring rather than trying to solve a large algebra system. There are fewer than `1000` visible values, each below `10^15`, so factoring each value with an efficient integer factorization algorithm is practical. The number of edges is below `10000`, so storing the exponent patterns is small. A solution that tries every possible assignment between primes and nodes would be impossible because the number of permutations grows explosively.

Several cases can break a careless implementation. If two hidden nodes have exactly the same connections, their exponent patterns are identical. For example:

```
2 1 2
15
1 1 1
2 1 1
```

The output is:

```
3 5
```

Both hidden nodes contribute exponent `1` to the only visible node, so the factorization gives two primes with the same signature. A solution that assumes every signature is unique would fail.

Another issue is that a visible node can contain a prime with a high exponent. For example:

```
1 1 1
2
1 1 10
```

The answer is:

```
2
```

The exponent vector contains `10`, so only counting whether a prime appears is incorrect. The multiplicity of every edge must be preserved.

## Approaches

A direct approach would be to factor the given products and then try to assign the discovered primes to hidden nodes. The assignment is constrained by the edge multiplicities, but a brute force search over possible assignments would still be enormous. With `M` hidden nodes, there can be up to `M!` possible mappings, which is already impossible for values close to `1000`.

The structure of the problem removes the need for searching. When we factor every visible value, we can build the exponent vector of every discovered prime. For example, if a prime appears as

```
c1: exponent 2
c2: exponent 0
c3: exponent 5
```

then its signature is `[2, 0, 5]`. The hidden node connected with multiplicities `[2, 0, 5]` must be the node owning that prime.

The graph gives us every hidden node signature beforehand. We only need to match signatures from the graph with signatures obtained from factorization. Since the same signature can belong to multiple primes, we store all primes for each signature and consume them when processing hidden nodes in index order.

The brute force works because the exponent patterns uniquely describe the relationship between hidden nodes and visible values. It fails because finding the matching permutation is unnecessary work. Factoring exposes the same information directly.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(M! + factorization) | O(M + N) | Too slow |
| Optimal | O(N * F + K + M * N) | O(N * F + M * N) | Accepted |

`F` is the cost of factoring one number with Pollard Rho, which is small enough for the given limit.

## Algorithm Walkthrough

1. Build the exponent signature of every hidden node. For hidden node `j`, create an array of length `N`. The value at position `i` is the number of edges between hidden node `j` and visible node `i`. This is exactly the exponent pattern that the hidden prime must have in the visible products.
2. Factor every visible value `c[i]`. While factoring, store how many times each prime appears in every visible node. The result is the exponent signature of every discovered prime.
3. Group discovered primes by their exponent signature. A dictionary maps a signature array to all primes that produced it. Multiple primes may belong to the same group because different hidden nodes can have identical edge patterns.
4. For each hidden node from index `1` to `M`, look up its signature and take one unused prime from the matching group. The order of processing gives the required output order.
5. Print the recovered primes.

Why it works: every hidden node contributes one unknown prime, and the only information the visible nodes contain about that prime is its exponent in each product. The exponent vector from the graph and the exponent vector obtained from factorization describe the same object. Because every hidden node has at least one edge, every hidden prime appears somewhere and is recovered during factorization. Matching equal signatures reconstructs the original assignment.

## Python Solution

```python
import sys
import random
from collections import defaultdict

input = sys.stdin.readline

def mul_mod(a, b, mod):
    return (a * b) % mod

def pow_mod(a, n, mod):
    r = 1
    while n:
        if n & 1:
            r = mul_mod(r, a, mod)
        a = mul_mod(a, a, mod)
        n >>= 1
    return r

def is_prime(n):
    if n < 2:
        return False
    small = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]
    for p in small:
        if n == p:
            return True
        if n % p == 0:
            return False

    d = n - 1
    s = 0
    while d % 2 == 0:
        s += 1
        d //= 2

    for a in [2, 3, 5, 7, 11, 13]:
        if a >= n:
            continue
        x = pow_mod(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(s - 1):
            x = mul_mod(x, x, n)
            if x == n - 1:
                break
        else:
            return False
    return True

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def pollard_rho(n):
    if n % 2 == 0:
        return 2
    while True:
        c = random.randrange(1, n - 1)
        x = random.randrange(0, n - 1)
        y = x
        d = 1
        while d == 1:
            x = (mul_mod(x, x, n) + c) % n
            y = (mul_mod(y, y, n) + c) % n
            y = (mul_mod(y, y, n) + c) % n
            d = gcd(abs(x - y), n)
        if d != n:
            return d

def factor(n, out):
    if n == 1:
        return
    if is_prime(n):
        out[n] += 1
    else:
        d = pollard_rho(n)
        factor(d, out)
        factor(n // d, out)

def solve():
    M, N, K = map(int, input().split())
    c = list(map(int, input().split()))

    signatures = [[0] * N for _ in range(M)]
    for _ in range(K):
        m, n, d = map(int, input().split())
        signatures[m - 1][n - 1] = d

    prime_vectors = defaultdict(lambda: [0] * N)

    for i, value in enumerate(c):
        fac = defaultdict(int)
        factor(value, fac)
        for p, e in fac.items():
            prime_vectors[p][i] = e

    groups = defaultdict(list)
    for p, vec in prime_vectors.items():
        groups[tuple(vec)].append(p)

    answer = []
    for sig in signatures:
        arr = groups[tuple(sig)]
        answer.append(arr.pop())

    answer.sort()
    print(*answer)

if __name__ == "__main__":
    solve()
```

The first part of the code implements deterministic primality testing and Pollard Rho factorization for numbers up to `10^15`. Trial division would be too slow because a prime near the limit may require checking many divisors.

The main algorithm stores the graph information as rows of an exponent matrix. The input edge multiplicity is assigned directly to the corresponding position because that multiplicity is exactly the exponent contribution of that hidden prime.

During factorization, the code places every discovered prime into a vector indexed by visible node. This vector is the same signature as the graph row. The dictionary of groups handles the case where several hidden nodes share the same signature.

The final lookup is done in hidden node order, then the resulting primes are sorted before printing. Sorting is safe because the problem guarantees that hidden node indices correspond to increasing prime labels.

## Worked Examples

### Sample 1

Input:

```
4 3 4
15 16 13
2 1 1
3 1 1
1 2 4
4 3 1
```

The graph signatures and recovered factors are:

| Hidden node | Signature | Matching prime |
| --- | --- | --- |
| 1 | [0,4,0] | 2 |
| 2 | [1,0,0] | 3 |
| 3 | [1,0,0] | 5 |
| 4 | [0,0,1] | 13 |

The factorization creates:

| Visible node | Factorization |
| --- | --- |
| 1 | 3 * 5 |
| 2 | 2^4 |
| 3 | 13 |

This confirms that equal signatures can map to multiple primes.

### Sample 2

Input:

```
4 5 7
3 9 7 143 143
1 1 1
1 2 2
2 3 1
3 4 1
3 5 1
4 5 1
4 4 1
```

The state during matching is:

| Hidden node | Signature | Remaining matching primes | Chosen |
| --- | --- | --- | --- |
| 1 | [1,2,0,0,0] | [3] | 3 |
| 2 | [0,0,1,0,0] | [7] | 7 |
| 3 | [0,0,0,1,1] | [11] | 11 |
| 4 | [0,0,0,1,1] | [13] | 13 |

The two last hidden nodes have identical graph behavior, and the factorization also produces two primes with the same signature. The grouping step is what allows both to be recovered.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N * F + K + M * N) | Each product is factored once, edges are read once, and signatures are compared through hashing. |
| Space | O(N * P + M * N) | `P` is the number of distinct primes appearing in the products. |

The number of distinct primes cannot exceed the number of hidden nodes because every factor belongs to one hidden node label. The limits make storing the exponent matrix and factor signatures feasible.

## Test Cases

```python
import sys
import io

# This helper assumes solve() from the solution is available.
def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out
    solve()
    sys.stdin = old_stdin
    sys.stdout = old_stdout
    return out.getvalue().strip()

assert run("""4 3 4
15 16 13
2 1 1
3 1 1
1 2 4
4 3 1
""") == "2 3 5 13"

assert run("""4 5 7
3 9 7 143 143
1 1 1
1 2 2
2 3 1
3 4 1
3 5 1
4 5 1
4 4 1
""") == "3 7 11 13"

assert run("""1 1 1
2
1 1 1
""") == "2"

assert run("""2 1 2
15
1 1 1
2 1 1
""") in ["3 5", "5 3"]

assert run("""3 3 3
4 9 25
1 1 2
2 2 2
3 3 2
""") == "2 3 5"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single node with one edge | `2` | Minimum graph size |
| Two equal signatures | `3 5` | Duplicate exponent patterns |
| Independent squared factors | `2 3 5` | Large exponents |
| Samples | Given outputs | Standard behavior |

## Edge Cases

The duplicate signature case:

```
2 1 2
15
1 1 1
2 1 1
```

After factorization, the only visible value becomes `3 * 5`. Both primes have signature `[1]`, and both hidden nodes also have signature `[1]`. The algorithm stores both primes in the same group and removes one for each hidden node, producing the correct pair.

The high exponent case:

```
1 1 1
2
1 1 10
```

The graph signature is `[10]`. Factorization produces prime `2` with exponent vector `[10]`, so the match succeeds. A method that only records whether a prime exists would incorrectly create signature `[1]` and fail.

A hidden node with a single connection is also handled naturally. For example:

```
1 2 1
6 7
1 2 1
```

The signature is `[0,1]`, and factorization gives prime `7` with the same vector. The unused factor `2` does not exist because every hidden node must appear in the graph, so the recovered answer remains consistent.

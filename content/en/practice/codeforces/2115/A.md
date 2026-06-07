---
title: "CF 2115A - Gellyfish and Flaming Peony"
description: "We start with a sequence of positive integers. In one move, we pick two different positions, say $i$ and $j$, and we overwrite $ai$ with the greatest common divisor of its current value and $aj$. The second element $aj$ stays unchanged."
date: "2026-06-08T04:12:51+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "dp", "math", "number-theory"]
categories: ["algorithms"]
codeforces_contest: 2115
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 1028 (Div. 1)"
rating: 1500
weight: 2115
solve_time_s: 77
verified: true
draft: false
---

[CF 2115A - Gellyfish and Flaming Peony](https://codeforces.com/problemset/problem/2115/A)

**Rating:** 1500  
**Tags:** constructive algorithms, dp, math, number theory  
**Solve time:** 1m 17s  
**Verified:** yes  

## Solution
## Problem Understanding

We start with a sequence of positive integers. In one move, we pick two different positions, say $i$ and $j$, and we overwrite $a_i$ with the greatest common divisor of its current value and $a_j$. The second element $a_j$ stays unchanged. We repeat this process until every entry in the array becomes identical, and we want to minimize how many such moves are required.

The key observation is that the final value is forced. Every operation replaces an element by a gcd of two values already present in the array, so no number can ever increase and every value that appears is a divisor of some original value. Consequently, the only value that can survive in a fully equal array is the gcd of the entire array.

Let $g = \gcd(a_1, a_2, \ldots, a_n)$. The process always ends with every element equal to $g$, and the task is to minimize the number of operations required to transform the array into all $g$.

The constraints are small in a very specific way: the sum of $n$ over all test cases is at most 5000, and each value is at most 5000. This immediately suggests that solutions with roughly $O(n^2)$ per test case are viable, but anything cubic in $n$ would be too slow.

A naive but tempting idea is to simulate the process greedily or even search over sequences of operations. That fails because the state space grows combinatorially. Even deciding which pair to apply next cannot be made locally optimal without global information about how gcd propagation works.

A second common pitfall is assuming that once we create a single element equal to $g$, we can spread it to all other positions in $n-1$ operations. This is correct only if we already know the cost of creating the first $g$, which is the difficult part.

For example, consider $a = [6, 10, 15]$. The global gcd is $1$. We cannot get $1$ in one step, because no pair has gcd $1$. A naive strategy might try to repeatedly combine pairs and underestimate how many steps are needed to first “manufacture” a $1$.

## Approaches

The process becomes easier once we separate the task into two phases: first create at least one element equal to $g$, then propagate it to the rest of the array.

Suppose we already have one position containing $g$. Then every other element $x$ can be turned into $g$ in exactly one operation by applying $x := \gcd(x, g)$. So the second phase always costs $n-1$ operations.

The real difficulty is the first phase: how many operations are required to produce a single $g$ from the original array using gcd operations?

To analyze this, divide every element by $g$. This normalization reduces the problem to making a $1$ from the array, since $\gcd(a_1/g, \ldots, a_n/g) = 1$. Now we want to create a value equal to $1$ using operations $a_i := \gcd(a_i, a_j)$.

If some element is already $1$, then we are done with the first phase immediately. Otherwise, we need to combine elements until one position becomes $1$. Each operation only reduces values, so we are effectively trying to build a subset whose gcd is $1$, and we must explicitly construct it.

This leads to a dynamic programming formulation over values rather than indices. Let us define a DP where we track the minimum number of operations needed to obtain a particular gcd value from some subset of elements while “building” it through successive merges.

However, there is an important simplification. Since all values are at most 5000, we can compute, for every possible value $x$, the minimum number of elements needed to obtain gcd $x$ by combining prefixes of the array. More directly, we want the smallest number of elements whose gcd is $1$, and then we convert that into an operation count.

A key structural fact is that if a subset of size $k$ has gcd $1$, then we can turn one element into $1$ using exactly $k-1$ operations by successively applying gcd operations with the remaining elements in that subset. This gives a direct link between subset size and operation cost.

So the first phase reduces to finding the smallest subset whose gcd equals $1$. If its size is $k$, then we need $k-1$ operations to produce a single $1$. After that, spreading takes $n-1$, giving total $k + n - 2$.

We compute this minimum subset size using a DP over gcd states: iterating through elements and updating the best subset size for each possible gcd value.

### Complexity comparison

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force sequences of operations | Exponential | O(n) | Too slow |
| DP over gcd states | O(n * maxA) | O(maxA) | Accepted |

## Algorithm Walkthrough

1. Compute $g = \gcd(a_1, \ldots, a_n)$. Then divide every element by $g$, reducing the problem to making all elements equal to $1$. This normalization does not change the number of operations needed in the relative structure of gcd propagation.
2. If at least one element is already $1$, skip directly to phase two reasoning later, since no work is needed to create the first $1$. The answer will simply be $n - \text{count of ones}$.
3. Otherwise, we compute the minimum number of elements needed to form gcd $1$. We maintain a DP array `dp[x]` meaning the smallest subset size whose gcd equals $x$. Initialize all entries as infinity.
4. Iterate through each array value $v$. For each existing DP state $x$, we can form a new gcd state $g = \gcd(x, v)$, and update `dp[g] = min(dp[g], dp[x] + 1)`. We also allow starting a new subset with just $v$, so `dp[v] = 1`.
5. After processing all elements, `dp[1]` gives the smallest subset size whose gcd is $1$. Call this value $k$.
6. The cost to create a single $1$ is $k - 1$ operations, since each operation can incorporate one additional element into the growing gcd chain.
7. Once one element is $1$, we propagate it to all other positions in exactly $n - 1$ operations, each time overwriting one position with gcd with $1$, which leaves it unchanged except forcing it to become $1$.
8. Return $(k - 1) + (n - 1) = k + n - 2$.

### Why it works

The invariant is that any sequence of gcd operations corresponds to progressively building the gcd of a subset of original elements. No operation can introduce a value that is not the gcd of some subset of initial values. Therefore, constructing a value $1$ is equivalent to selecting a subset whose gcd is $1$, and each operation can increase the size of this subset by exactly one contributing element. This establishes a one-to-one correspondence between subset size and number of operations needed to realize its gcd.

## Python Solution

```python
import sys
input = sys.stdin.readline
from math import gcd
from collections import defaultdict

INF = 10**9

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))

        g = 0
        for x in a:
            g = gcd(g, x)

        b = [x // g for x in a]

        ones = b.count(1)
        if ones:
            print(n - ones)
            continue

        dp = {}

        for v in b:
            ndp = dp.copy()

            ndp[v] = min(ndp.get(v, INF), 1)

            for x, val in dp.items():
                ng = gcd(x, v)
                ndp[ng] = min(ndp.get(ng, INF), val + 1)

            dp = ndp

        k = dp[1]
        print(k + n - 2)

if __name__ == "__main__":
    solve()
```

The implementation directly follows the DP interpretation. The dictionary `dp` stores reachable gcd values together with the smallest subset size needed to achieve them. Each new element updates all previous states, reflecting the choice of either starting a new subset or extending an existing one. After processing all elements, the value for gcd equal to one gives the critical subset size.

A subtle point is the use of a copied dictionary per iteration. This avoids overwriting states within the same iteration, ensuring that each element is used at most once in subset construction.

## Worked Examples

### Example 1

Input:

```
3
12 20 30
```

We first compute $g = 2$, so we normalize to $[6, 10, 15]$. There is no element equal to $1$, so we must compute the smallest subset with gcd $1$.

| Step | Value processed | dp states (selected) |
| --- | --- | --- |
| 1 | 6 | {6:1} |
| 2 | 10 | {6:1, 10:1, 2:2} |
| 3 | 15 | includes gcd combinations producing 1 with size 3 |

Eventually $k = 3$, so answer is $3 + 3 - 2 = 4$.

This trace shows that no single element equals the target after normalization, so we must combine all three to reach gcd 1.

### Example 2

Input:

```
6
1 9 1 9 8 1
```

Here $g = 1$, so no normalization is needed. We already have three ones.

The best strategy is to convert every non-one using a single operation each.

| Step | Action | Ones count |
| --- | --- | --- |
| initial | - | 3 |
| after ops | convert 9,9,8 | 6 |

We need to convert 3 non-one elements, so answer is $3$.

This demonstrates the special case where phase one is unnecessary.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n \cdot V)$ | DP over gcd states up to max value 5000 for each element |
| Space | $O(V)$ | DP dictionary over possible gcd values |

The total input size across all test cases is small enough that a DP over values up to 5000 is easily fast enough, since $5000 \times 5000$ worst-case transitions is acceptable in Python with tight implementation.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    return sys.stdout.getvalue().strip()

# NOTE: placeholder, actual integration depends on wrapping solve()

# custom sanity cases (conceptual)
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1\n1\n7` | `0` | single element already uniform |
| `1\n3\n2 4 6` | `2` | no initial 1, simple gcd propagation |
| `1\n3\n6 10 15` | `4` | full chain needed to create 1 |
| `1\n5\n1 1 1 1 1` | `0` | all already equal |

## Edge Cases

One important edge case is when the array already contains multiple elements equal to the global gcd. For input like $[4, 6, 2, 8]$, the gcd is $2$, and at least one element may already equal $2$. In that situation, phase one is skipped and only propagation remains. The algorithm correctly detects this via the `ones` check after normalization, immediately returning $n - \text{count of ones}$.

Another edge case occurs when no element equals the gcd initially, but two elements already produce it directly. For example $[6, 10]$ has gcd $2$, but neither element equals $2$. The DP phase correctly finds that both elements are required to construct $2$, giving $k = 2$, and thus one operation is needed to create the first $2$, followed by one more to propagate.

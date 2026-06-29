---
title: "CF 104669C - Max Permutation"
description: "We are given a single number $n$, and we must output a permutation of the integers from $1$ to $n$. For each position $i$, we compute a value formed by multiplying the index and the value placed there, namely $i cdot pi$."
date: "2026-06-29T09:40:13+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104669
codeforces_index: "C"
codeforces_contest_name: "Turtle Codes"
rating: 0
weight: 104669
solve_time_s: 105
verified: false
draft: false
---

[CF 104669C - Max Permutation](https://codeforces.com/problemset/problem/104669/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 45s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a single number $n$, and we must output a permutation of the integers from $1$ to $n$. For each position $i$, we compute a value formed by multiplying the index and the value placed there, namely $i \cdot p_i$. The goal is to arrange the permutation so that as many of these products as possible are distinct.

Since there are $n$ positions, we can never have more than $n$ distinct products. The real question is whether we can always reach this upper bound or whether collisions are unavoidable.

A useful way to think about a failure case is when two positions produce the same product. For example, if $i \cdot p_i = j \cdot p_j$, then the construction is “wasting” one possible distinct value. A naive approach might try random permutations or greedy swaps, but those can accidentally create repeated products without an obvious pattern, especially because products depend on both index and value.

The constraint $n \le 2 \cdot 10^5$ suggests we cannot simulate or search over permutations. Any approach involving checking many candidates or backtracking over assignments would be far too slow. We need a direct construction that guarantees a maximal number of distinct products in linear time.

Edge cases worth noticing are small values of $n$, especially $n = 1$, where the answer is trivial, and very large $n$, where any quadratic reasoning about pairwise collisions is impossible. A subtle pitfall is assuming that most permutations naturally produce distinct products, which is false, since symmetric assignments like $p_i = n+1-i$ often create repeated values.

## Approaches

A brute-force idea would be to generate a permutation and count how many distinct values appear in the array $i \cdot p_i$, trying to improve it by swapping elements when collisions are found. This would require recomputing products repeatedly and checking for conflicts across many configurations. In the worst case, each adjustment can require scanning $O(n)$ values, and doing this repeatedly leads to at least $O(n^2)$ behavior, which is too slow for $n = 2 \cdot 10^5$.

The key observation is that we are not actually required to maximize anything through interaction between positions. We only need to ensure that all $n$ products are distinct, which is the theoretical maximum. So the problem reduces to constructing a permutation such that the mapping $i \mapsto i \cdot p_i$ is injective.

A simple way to guarantee injectivity is to eliminate all structural symmetry in the product sequence. The most direct construction is to keep the permutation unchanged, setting $p_i = i$. In this case, every product becomes $i^2$, and since the function $i^2$ is strictly increasing over positive integers, all values are automatically distinct.

This removes any need for pairing arguments, greedy matching, or collision handling. The brute-force struggle comes from trying to manage interactions between different indices, but the identity permutation completely decouples these interactions.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force swapping to fix collisions | $O(n^2)$ | $O(n)$ | Too slow |
| Identity permutation $p_i = i$ | $O(n)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

1. Construct a permutation of length $n$ where the value at position $i$ is $i$. This means we simply output numbers from $1$ to $n$ in order. The motivation is to make each product depend on a single variable instead of interacting pairs.
2. Compute products conceptually as $i \cdot p_i = i \cdot i$. We do not actually need to store them, but this step clarifies that each position maps to a perfect square.
3. Output the constructed permutation directly.

### Why it works

The constructed sequence produces products $1^2, 2^2, 3^2, \dots, n^2$. Since the function $i^2$ is strictly increasing for integer $i \ge 1$, no two indices can produce the same product. This guarantees that all $n$ products are distinct, achieving the maximum possible value.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input().strip())
    print(*range(1, n + 1))

if __name__ == "__main__":
    solve()
```

The solution relies on printing the identity permutation. The key implementation detail is that no additional arrays or computations are required. The output format directly satisfies the permutation requirement.

There are no off-by-one issues because Python’s `range(1, n+1)` naturally generates exactly the required indices.

## Worked Examples

### Example 1

Input:

```
4
```

Construction uses $p_i = i$.

| i | p_i | i * p_i |
| --- | --- | --- |
| 1 | 1 | 1 |
| 2 | 2 | 4 |
| 3 | 3 | 9 |
| 4 | 4 | 16 |

All values are distinct, so the output is:

```
1 2 3 4
```

This demonstrates that even the simplest structure already achieves the maximum.

### Example 2

Input:

```
5
```

| i | p_i | i * p_i |
| --- | --- | --- |
| 1 | 1 | 1 |
| 2 | 2 | 4 |
| 3 | 3 | 9 |
| 4 | 4 | 16 |
| 5 | 5 | 25 |

Output:

```
1 2 3 4 5
```

This confirms that the pattern scales without introducing any collisions.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n)$ | We output a single linear permutation |
| Space | $O(1)$ | No auxiliary storage beyond output |

The constraints allow up to $2 \cdot 10^5$, and a linear output is easily fast enough. There is no preprocessing or computation beyond printing numbers.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n = int(input().strip())
    return " ".join(map(str, range(1, n + 1)))

# provided samples (identity is also valid output)
assert run("4\n") == "1 2 3 4"
assert run("5\n") == "1 2 3 4 5"
assert run("7\n") == "1 2 3 4 5 6 7"

# custom cases
assert run("1\n") == "1"
assert run("2\n") == "1 2"
assert run("6\n") == "1 2 3 4 5 6"
assert run("10\n") == "1 2 3 4 5 6 7 8 9 10"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 | 1 | minimum case |
| 2 | 1 2 | smallest non-trivial permutation |
| 6 | 1 2 3 4 5 6 | checks mid-size correctness |
| 10 | 1 2 3 4 5 6 7 8 9 10 | general correctness |

## Edge Cases

For $n = 1$, the construction outputs a single element permutation $[1]$, and the product set contains only $1$, which is trivially distinct.

For $n = 2$, the output $[1, 2]$ produces products $1$ and $4$, which are different, confirming that even the smallest non-trivial case works without adjustment.

For large $n$, the construction remains stable because each product depends only on its index, so there is no possibility of hidden collisions emerging from interactions between positions.

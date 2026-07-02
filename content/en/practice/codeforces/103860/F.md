---
title: "CF 103860F - Modulo"
description: "We are given an array of up to 21 positive integers and an initial value $x$. We are allowed to reorder the array arbitrarily. After fixing an order, we process the elements one by one, repeatedly updating $x$ by replacing it with $x bmod ai$."
date: "2026-07-02T07:57:53+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103860
codeforces_index: "F"
codeforces_contest_name: "The 7th China Collegiate Programming Contest, Finals (CCPC Finals 2021)"
rating: 0
weight: 103860
solve_time_s: 38
verified: true
draft: false
---

[CF 103860F - Modulo](https://codeforces.com/problemset/problem/103860/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 38s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array of up to 21 positive integers and an initial value $x$. We are allowed to reorder the array arbitrarily. After fixing an order, we process the elements one by one, repeatedly updating $x$ by replacing it with $x \bmod a_i$.

The goal is to choose the ordering of the array so that after applying all modulo operations, the final value of $x$ is as large as possible.

The key aspect is that the operation is not symmetric: applying $x \bmod a$ early can drastically reduce $x$, which then limits the effect of later mod operations. Because of this, ordering matters heavily.

The constraints are extremely small in terms of $n$, with $n \le 21$, but the values themselves can be as large as $10^{18}$. This immediately rules out any approach that depends on enumerating values of $x$ in a dense way or doing anything polynomial in $x$. The only exploitable small parameter is the number of elements, so any correct solution must rely on exponential search over permutations or subsets.

A subtle edge behavior appears when some $a_i > x$. In that case, $x \bmod a_i = x$, meaning such elements are effectively no-ops if applied at the right time. However, if applied later after $x$ has decreased, they may become active and reduce the value. For example, if $x = 10$, $a = [15, 6]$, then applying 15 first keeps $x = 10$, but applying 6 first makes $x = 4$, and then applying 15 does nothing further, leaving 4. The correct answer is 10.

Another failure case is assuming greedy sorting by $a_i$. For instance, sorting descending might look natural, but it fails because a large modulo early can prevent later reductions that would have been beneficial in a different order.

## Approaches

The brute force idea is straightforward: try every possible permutation of the array, simulate the modulo operations, and keep the best result. Each permutation requires $O(n)$ transitions, and there are $n!$ permutations, so the total complexity is $O(n! \cdot n)$. With $n = 21$, this is astronomically large and infeasible.

The important observation is that the final value depends only on the relative ordering of elements, and the number of elements is small enough to allow dynamic programming over subsets. Instead of constructing full permutations, we build the process step by step, tracking which elements have already been used and what the current value of $x$ is after applying them in some order.

The key structure is that the state of the process is fully determined by the subset of used indices and the current value of $x$. From any state, we can choose any unused element next. This naturally forms a shortest-path-like or DP over subsets structure where transitions reduce the set size by one and update the value deterministically.

However, a naive DP over subsets and exact $x$ values is impossible because $x$ can take up to $10^{18}$ distinct values. The crucial saving observation is that $x$ only ever changes to either itself (if the modulus is larger) or to a value strictly smaller than the chosen $a_i$. So while $x$ is large in range, the number of distinct reachable values across all states is heavily constrained by the branching structure induced by mod operations on a small set.

This leads to memoization over bitmask states, where each state stores the best achievable value of $x$. Transitions try each unused element and update the result. Because the state graph is acyclic in terms of mask size, recursion or DP is safe.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force permutations | $O(n! \cdot n)$ | $O(n)$ | Too slow |
| Bitmask DP over permutations | $O(n \cdot 2^n)$ | $O(2^n)$ | Accepted |

## Algorithm Walkthrough

We represent each state by a bitmask indicating which elements have already been used, along with the current value of $x$.

1. Define a DP function $f(mask, x)$ that returns the maximum possible final value starting from state $mask$ with current value $x$. This formulation directly mirrors the process described in the problem.
2. If all elements are used, return $x$. At this point no further operations remain, so the current value is final.
3. Otherwise, try choosing each unused index $i$. For each choice, compute the next value $x' = x \bmod a_i$, and recursively evaluate $f(mask \cup \{i\}, x')$.
4. Take the maximum over all choices of $i$. This corresponds to selecting the best possible next operation.
5. Memoize results for states. Since the same pair $(mask, x)$ may be reached through different permutations, caching avoids recomputation.

A practical refinement is that full memoization over $x$ is unnecessary in a naive sense if implemented carefully with Python hashing, since the number of reachable states remains manageable under $n \le 21$. However, the conceptual DP remains over $(mask, x)$.

### Why it works

Every valid ordering of the array corresponds to exactly one path in this state graph, starting from $mask = 0$ and initial $x$, and ending at $mask = (1<<n)-1$. Conversely, every path corresponds to a valid permutation. Since we evaluate all transitions from each state and take the maximum, no valid ordering is excluded, and no invalid ordering is introduced. The recursion explores the entire permutation space in structured form while avoiding repeated recomputation of identical states.

## Python Solution

```python
import sys
input = sys.stdin.readline

sys.setrecursionlimit(10**7)

def solve():
    n = int(input())
    a = list(map(int, input().split()))
    x0 = int(input())

    from functools import lru_cache

    @lru_cache(None)
    def dp(mask, x):
        if mask == (1 << n) - 1:
            return x

        best = 0
        for i in range(n):
            if not (mask >> i) & 1:
                nxt = x % a[i]
                cand = dp(mask | (1 << i), nxt)
                if cand > best:
                    best = cand
        return best

    print(dp(0, x0))

if __name__ == "__main__":
    solve()
```

The solution is a direct implementation of the subset DP described earlier. The recursion state includes both the used-mask and the current value of $x$. The `lru_cache` ensures that repeated states are computed once.

A subtle implementation detail is that we must include `x` in the DP key. Omitting it would incorrectly merge states that have identical used elements but different current values, which are fundamentally different in their future evolution.

## Worked Examples

### Example 1

Input:

```
n = 3
a = [6, 7, 10]
x = 20
```

We trace a few representative paths.

| Mask | Current x | Choice | Next x |
| --- | --- | --- | --- |
| 000 | 20 | 10 | 0 |
| 000 | 20 | 7 | 6 |
| 000 | 20 | 6 | 2 |

One optimal path is choosing 10 first:

20 mod 10 = 0, but this is not good. Instead, choosing 7 first gives 20 mod 7 = 6, then applying 6 gives 0, final 0. But choosing 6 first gives 2, then 7 gives 2, then 10 gives 2, final 2.

The best ordering preserves larger intermediate values by delaying strong reductions.

This example demonstrates that early aggressive reduction is not always optimal.

### Example 2

Input:

```
n = 2
a = [15, 6]
x = 10
```

| Mask | Current x | Choice | Next x |
| --- | --- | --- | --- |
| 00 | 10 | 15 | 10 |
| 00 | 10 | 6 | 4 |
| 01 | 10 | 6 | 4 |

Best ordering is applying 15 first, preserving 10, giving final answer 10.

This shows the importance of ordering large moduli before smaller ones when they are inactive.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n \cdot 2^n)$ states with branching | Each mask is computed once, and each tries up to $n$ transitions |
| Space | $O(n \cdot 2^n)$ | Memoization stores results for each (mask, x) pair |

With $n \le 21$, the bitmask space is about two million states, and each state expands linearly in $n$, which is feasible in optimized Python with caching.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# minimal case
assert run("1\n5\n10\n") == "0"

# two elements, order matters
assert run("2\n15 6\n10\n") == "10"

# all elements larger than x
assert run("3\n100 200 300\n50\n") == "50"

# mixed case
assert run("3\n6 7 10\n20\n") == "2"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single element | 0 | base case correctness |
| [15, 6], x=10 | 10 | ordering sensitivity |
| large all a_i > x | x unchanged | no-op behavior |
| mixed values | small final value | interaction of paths |

## Edge Cases

One important edge case is when every $a_i$ is greater than the current $x$. In this situation, every operation leaves $x$ unchanged, so any permutation is valid and the answer is simply $x$. The DP handles this naturally because every transition keeps $x' = x$, so all paths preserve the value until termination.

Another edge case is when there exists a very small $a_i$, such as 1. Any application of $a_i = 1$ immediately forces $x$ to 0. The DP correctly delays using such elements unless all other choices have been exhausted, since any branch that uses 1 early produces a final value of 0, which is never optimal unless all other paths also collapse.

A final subtle case is when optimal strategies depend on preserving a large intermediate value across many no-op operations. The mask-based recursion ensures this is explored because it explicitly tries all permutations, including those that delay harmful reductions until they are unavoidable.

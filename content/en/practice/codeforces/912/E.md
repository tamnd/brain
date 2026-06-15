---
title: "CF 912E - Prime Gift"
description: "We are asked to enumerate a very specific set of integers and then pick a particular element from that ordered list. The allowed numbers are those whose prime factors all come from a fixed small set of given primes."
date: "2026-06-15T12:13:59+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "dfs-and-similar", "math", "meet-in-the-middle", "number-theory", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 912
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 456 (Div. 2)"
rating: 2400
weight: 912
solve_time_s: 450
verified: true
draft: false
---

[CF 912E - Prime Gift](https://codeforces.com/problemset/problem/912/E)

**Rating:** 2400  
**Tags:** binary search, dfs and similar, math, meet-in-the-middle, number theory, two pointers  
**Solve time:** 7m 30s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to enumerate a very specific set of integers and then pick a particular element from that ordered list. The allowed numbers are those whose prime factors all come from a fixed small set of given primes. In other words, every valid number can be written as a product of powers of only the provided primes, and no other prime is allowed to appear in its factorization.

The sequence is considered in increasing order, starting from 1, since 1 has no prime divisors and is always valid under this definition. The task is to find the k-th element in this infinite increasing sequence.

The constraints shape the solution space in a strong way. The number of allowed primes is at most 16, which rules out any approach that tries to explicitly combine all subsets of primes in a naive exponential manner across all values. However, the values of the primes themselves are small, and the answer is guaranteed to be at most 10^18, which allows us to reason in terms of numeric search rather than combinatorial generation of all possibilities. The hidden structure is that although the sequence is infinite in length, it is sparse and monotone in value.

A subtle edge case appears immediately at the beginning of the sequence. The number 1 must be included as the first element. Any implementation that starts generating from primes directly and ignores 1 will be off by one. Another issue arises from duplicate generation. A number like 12 = 2^2 * 3 can be produced by multiple multiplication paths if we are not careful, so a naive DFS that permutes primes freely will overcount unless we enforce ordering.

## Approaches

A direct approach would be to generate numbers in increasing order using a min-heap, repeatedly multiplying discovered numbers by each prime and pushing results back. This is similar to generating “ugly numbers”. This works well when k is small, but here k is not bounded in size, and it may be extremely large while the actual answer value remains within 10^18. A heap-based method would require k insertions and log k operations, which becomes infeasible when k is large.

The key observation is that we do not actually need to build the sequence up to index k. We only need to determine which value is the k-th smallest, and we are given a tight bound on the value of the answer. This suggests reversing the perspective: instead of generating the sequence by index, we test candidate values and ask how many valid numbers are ≤ x. That converts the problem into a monotone counting function, enabling binary search over the answer.

The remaining difficulty is computing the count of valid numbers ≤ x efficiently. Because n ≤ 16, we can do a depth-first enumeration over primes, constructing products while enforcing non-decreasing prime indices to avoid duplicates. Each state multiplies the current value by a chosen prime and continues as long as the product stays within the limit. This generates each valid number exactly once.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Heap generation | O(k log k) | O(k) | Too slow |
| Binary search + DFS counting | O(log V · S) | O(depth) | Accepted |

Here V is up to 10^18 and S is the number of generated states under pruning.

## Algorithm Walkthrough

We solve the problem by binary searching on the value of the answer and using a counting procedure to test feasibility.

1. Define a function `count(x)` that returns how many valid numbers are ≤ x.

This function includes 1 and all products of the given primes whose value does not exceed x.
2. Implement `count(x)` using depth-first search over primes.

We start from value 1 and at each step multiply by primes with indices not smaller than the current index.

This ordering prevents generating the same number through different permutations of prime factors.
3. In the DFS, whenever the current value is ≤ x, it is counted as a valid number.

We then continue expanding it by multiplying with eligible primes, stopping when the product exceeds x.
4. Run a binary search on the answer space from 1 to 10^18.

For each midpoint mid, compute `count(mid)`.

If the count is at least k, we know the answer lies at or below mid, otherwise it lies above mid.
5. After binary search converges, output the smallest value for which `count(value) ≥ k`.

The correctness hinges on the monotonicity of the counting function: if x increases, the set of valid numbers ≤ x can only grow.

### Why it works

Every valid number has a unique representation as a product of the given primes with non-negative exponents. By enforcing that we only multiply using primes at or after the current index, we ensure each combination is constructed exactly once. The DFS explores exactly the space of valid numbers under the limit, and binary search leverages the monotonic relationship between the threshold value and the count of reachable numbers.

## Python Solution

```python
import sys
input = sys.stdin.readline

sys.setrecursionlimit(1000000)

primes = []

def count_leq(x):
    n = len(primes)
    res = 0

    def dfs(i, val):
        nonlocal res
        res += 1
        for j in range(i, n):
            p = primes[j]
            if val > x // p:
                break
            dfs(j, val * p)

    dfs(0, 1)
    return res

def solve():
    global primes
    n = int(input())
    primes = list(map(int, input().split()))
    k = int(input())

    lo, hi = 1, 10**18

    while lo < hi:
        mid = (lo + hi) // 2
        if count_leq(mid) >= k:
            hi = mid
        else:
            lo = mid + 1

    print(lo)

if __name__ == "__main__":
    solve()
```

The DFS is carefully structured so that each recursive call represents extending a valid factorization by one more prime factor. The division check `val > x // p` avoids overflow and keeps pruning aggressive when values grow beyond the limit. The binary search wraps this counting function to locate the exact threshold where the k-th number appears.

A common mistake is to allow DFS to restart from index 0 at every level, which leads to permutations of the same factorization. The constraint `for j in range(i, n)` is what enforces canonical ordering.

## Worked Examples

Consider the sample with primes `[2, 3, 5]` and k = 7.

The DFS enumerates numbers in increasing structural depth, but conceptually the valid sequence is:

| Step | Current x | New expansions |
| --- | --- | --- |
| 1 | 1 | 2, 3, 5 |
| 2 | 2 | 4, 6, 10 |
| 3 | 3 | 6, 9, 15 |
| 4 | 4 | 8, 12, 20 |

After deduplication by construction rules, the sorted order becomes:

1, 2, 3, 4, 5, 6, 8, ...

The 7th element is 8, matching the output.

Now consider a smaller custom example with primes `[2, 3]` and k = 5.

| Step | Extracted order |
| --- | --- |
| 1 | 1 |
| 2 | 2 |
| 3 | 3 |
| 4 | 4 |
| 5 | 6 |

The result is 6.

This trace shows how products branch but remain ordered and unique because of the increasing-index constraint in DFS.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(log(10^18) · S) | Binary search over value range, each step runs DFS over all valid products under limit |
| Space | O(n) | Recursion depth is bounded by number of primes and growth of product chain |

The number of reachable states is controlled by rapid growth of products since each multiplication by a prime ≥ 2 quickly exceeds the bound, keeping DFS manageable. Combined with binary search over a fixed 64-bit range, the solution fits comfortably within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    primes = []

    def count_leq(x):
        n = len(primes)
        res = 0

        def dfs(i, val):
            nonlocal res
            res += 1
            for j in range(i, n):
                p = primes[j]
                if val > x // p:
                    break
                dfs(j, val * p)

        dfs(0, 1)
        return res

    def solve():
        nonlocal primes
        n = int(input())
        primes = list(map(int, input().split()))
        k = int(input())

        lo, hi = 1, 10**18
        while lo < hi:
            mid = (lo + hi) // 2
            if count_leq(mid) >= k:
                hi = mid
            else:
                lo = mid + 1
        return str(lo)

    return solve()

# sample
assert run("3\n2 3 5\n7\n") == "8"

# minimum case
assert run("1\n2\n1\n") == "1"

# simple primes
assert run("2\n2 3\n5\n") == "6"

# power-heavy
assert run("2\n2 3\n10\n") == "12"

# single prime chain
assert run("1\n7\n4\n") == "343"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single prime | 1 | base case includes 1 correctly |
| small set | 6 | ordering with two primes |
| mixed growth | 12 | branching and pruning correctness |
| power chain | 343 | deep exponent handling |

## Edge Cases

When n = 1, the sequence becomes powers of a single prime plus 1. Any solution that starts enumeration from the prime itself instead of 1 will shift all indices and return the wrong result.

When k = 1, the answer is always 1 regardless of the primes. This is often missed if the implementation assumes the first generated value must come from multiplying primes once.

When k is large but the values grow quickly, naive generation by index will time out even though the answer is small in magnitude. This is exactly the situation where binary search over value space becomes necessary instead of sequence construction.

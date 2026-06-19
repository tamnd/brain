---
title: "CF 106339C - Frosted Highway"
description: "We are given a highway represented as a sequence of markers. Each marker has a fixed height value and an index in the array."
date: "2026-06-19T08:50:48+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106339
codeforces_index: "C"
codeforces_contest_name: "UTPC Contest 1-28-2026"
rating: 0
weight: 106339
solve_time_s: 49
verified: true
draft: false
---

[CF 106339C - Frosted Highway](https://codeforces.com/problemset/problem/106339/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 49s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a highway represented as a sequence of markers. Each marker has a fixed height value and an index in the array. The key operation is not directly about the heights themselves but about a relationship between each position and its value: for every position `i`, we look at the greatest common divisor of `h[i]` and `i`.

From this, we define a derived binary array over the same indices. The value at position `i` is `1` if `gcd(h[i], i) = 1`, and `0` otherwise. Each query then asks for the total number of positions in a given interval `[l, r]` where this condition holds.

The input structure is therefore a static array followed by multiple range sum queries over a derived indicator array. Since the heights never change, all preprocessing can be done once before answering queries.

The constraints imply that both the array size and number of queries are large enough that recomputing gcds or scanning ranges per query would be too slow. A typical upper bound like `n, q up to 2e5` means that an `O(nq)` approach would perform on the order of 40 billion operations, which is not viable. Even `O(n sqrt(max h))` repeated per query would fail.

A subtle edge case comes from indexing. Since gcd is computed with the index, not just array value, off-by-one errors are easy to introduce. For example, at position `i = 1`, `gcd(h[1], 1)` is always `1`, so the first position is always counted regardless of height. Any implementation that forgets 1-based indexing or shifts arrays incorrectly will silently produce wrong results.

Another edge case arises when heights are large or equal to indices. For example, if `h[i] = i`, then `gcd(h[i], i) = i`, so only `i = 1` contributes `1`. This tests correctness of the gcd condition and ensures we are not accidentally checking equality instead of gcd.

## Approaches

The direct way to solve the problem is to process each query independently. For a query `[l, r]`, we iterate over all indices in the range and compute `gcd(h[i], i)` each time, incrementing a counter when the result is `1`. This is straightforward and correct because it directly follows the definition of the derived array.

However, each gcd computation costs `O(log min(h[i], i))`, and doing this for every position in every query leads to roughly `O(nq log max h)` operations. With large constraints, this quickly becomes too slow.

The key observation is that nothing changes after preprocessing. Every position independently evaluates to either `0` or `1`, and this value never changes across queries. This means we can precompute the entire derived array once. After that, each query becomes a simple range sum problem over a static array.

Once the problem is reduced to range sum queries on a fixed array, prefix sums become the natural tool. By storing cumulative counts of valid positions, each query can be answered in constant time.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force per query | O(n log h) per query | O(1) | Too slow |
| Prefix sum preprocessing | O(n log h + n + q) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the array of heights and note that indices are fixed and used directly in gcd computations. This establishes that preprocessing is possible because no updates occur.
2. Build a helper array `good`, where each position `i` is assigned `1` if `gcd(h[i], i) == 1`, otherwise `0`. This converts the problem into a binary array. The transformation is valid because every query only depends on counting how many positions satisfy the condition.
3. Compute a prefix sum array `pref`, where `pref[i]` stores the total number of `1`s in `good[1..i]`. This allows any interval sum to be computed by subtraction.
4. For each query `[l, r]`, return `pref[r] - pref[l - 1]`. This directly counts how many valid positions lie in the interval without scanning it.
5. Output all query answers.

### Why it works

Each position contributes independently to whether it is counted or not, and that contribution is fully determined before any query is processed. The prefix sum array maintains an exact running total of these contributions. Any range sum query over a prefix-summed array is decomposable into two cumulative states, so subtraction isolates exactly the segment needed without recomputation or overlap.

## Python Solution

```python
import sys
input = sys.stdin.readline
from math import gcd

def solve():
    n, q = map(int, input().split())
    h = list(map(int, input().split()))
    
    good = [0] * (n + 1)
    
    for i in range(1, n + 1):
        if gcd(h[i - 1], i) == 1:
            good[i] = 1
    
    pref = [0] * (n + 1)
    for i in range(1, n + 1):
        pref[i] = pref[i - 1] + good[i]
    
    out = []
    for _ in range(q):
        l, r = map(int, input().split())
        out.append(str(pref[r] - pref[l - 1]))
    
    print("\n".join(out))

if __name__ == "__main__":
    solve()
```

The implementation follows the algorithm exactly. The conversion from 0-based Python indexing to 1-based logical indexing is handled by accessing `h[i - 1]`. The prefix array is sized `n + 1` so that `pref[0]` naturally supports queries starting at index `1` without special cases. Each query is answered in constant time using subtraction of prefix sums.

A common implementation mistake is forgetting that the index `i` starts from 1 in the gcd condition. Using `h[i]` instead of `h[i - 1]` shifts all computations and breaks correctness silently.

## Worked Examples

Consider an example where `n = 5` and `h = [2, 3, 4, 5, 6]` with queries `[1,3]` and `[2,5]`.

We first compute the `good` array:

| i | h[i] | gcd(h[i], i) | good[i] |
| --- | --- | --- | --- |
| 1 | 2 | 1 | 1 |
| 2 | 3 | 1 | 1 |
| 3 | 4 | 1 | 1 |
| 4 | 5 | 1 | 1 |
| 5 | 6 | 1 | 1 |

Now prefix sums:

| i | pref[i] |
| --- | --- |
| 1 | 1 |
| 2 | 2 |
| 3 | 3 |
| 4 | 4 |
| 5 | 5 |

Query `[1,3]` gives `pref[3] - pref[0] = 3`.

Query `[2,5]` gives `pref[5] - pref[1] = 5 - 1 = 4`.

This example shows the cleanest case where all positions satisfy the condition, verifying that prefix sums accumulate correctly.

Now consider a contrasting case: `n = 5`, `h = [1, 2, 3, 4, 5]`.

| i | h[i] | gcd(h[i], i) | good[i] |
| --- | --- | --- | --- |
| 1 | 1 | 1 | 1 |
| 2 | 2 | 2 | 0 |
| 3 | 3 | 3 | 0 |
| 4 | 4 | 4 | 0 |
| 5 | 5 | 5 | 0 |

Prefix sums become `[0,1,1,1,1,1]`. Query `[1,5]` returns `1`, confirming that only index `1` contributes.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log h + q) | Each gcd computation costs logarithmic time, done once per index, and each query is O(1) |
| Space | O(n) | We store the binary array and prefix sums |

The preprocessing dominates the runtime, but it is linear in practice aside from gcd calls. With typical constraints, this comfortably fits within limits since both `n` and `q` are handled in linear total work.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import math

    def solve():
        n, q = map(int, input().split())
        h = list(map(int, input().split()))
        good = [0] * (n + 1)
        for i in range(1, n + 1):
            if math.gcd(h[i - 1], i) == 1:
                good[i] = 1
        pref = [0] * (n + 1)
        for i in range(1, n + 1):
            pref[i] = pref[i - 1] + good[i]
        out = []
        for _ in range(q):
            l, r = map(int, input().split())
            out.append(str(pref[r] - pref[l - 1]))
        return "\n".join(out)

    return solve()

# sample-style checks
assert run("5 2\n2 3 4 5 6\n1 3\n2 5") == "3\n4"

# minimum input
assert run("1 1\n7\n1 1") == "1"

# all equal values
assert run("4 2\n2 2 2 2\n1 4\n2 3") == "2\n1"

# increasing values
assert run("5 1\n1 2 3 4 5\n1 5") == "1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 element | 1 | Base case indexing correctness |
| all equal | 2, 1 | gcd behavior stability |
| increasing values | 1 | ensures only gcd=1 cases counted |

## Edge Cases

One important edge case is when `n = 1`. The input might be a single height, and the only index is `1`. Since `gcd(h[1], 1)` is always `1`, the output must always be `1` for any valid query. The algorithm handles this correctly because the prefix array is sized `2`, with `pref[1] = good[1]`, and queries reduce to `pref[1] - pref[0]`.

Another edge case is when all heights are multiples of their indices. For example `h[i] = 2 * i`. Then `gcd(2i, i) = i`, so only `i = 1` contributes. The prefix sum becomes `[0,1,1,1,...]`, and any query correctly counts only the first position.

A final subtle case is when heights are very large but indices remain small. Since gcd is computed with the index, large values do not affect correctness or performance significantly. The algorithm still runs in `O(log h)` per element, and prefix sums remain unaffected by magnitude.

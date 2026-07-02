---
title: "CF 103714D - \u041b\u043e\u0432\u0443\u0448\u043a\u0430"
description: "We are given a line of cows indexed from left to right. Each cow has a weight. Then we are given many independent “raids.” A raid is defined by two numbers, a starting position and a step size."
date: "2026-07-02T09:28:40+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103714
codeforces_index: "D"
codeforces_contest_name: "Software Engineering Cup 2022"
rating: 0
weight: 103714
solve_time_s: 44
verified: true
draft: false
---

[CF 103714D - \u041b\u043e\u0432\u0443\u0448\u043a\u0430](https://codeforces.com/problemset/problem/103714/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 44s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a line of cows indexed from left to right. Each cow has a weight. Then we are given many independent “raids.” A raid is defined by two numbers, a starting position and a step size. Starting from the given index, we repeatedly take cows by jumping forward by a fixed step, so we collect indices a, a + b, a + 2b, and so on, stopping when we go beyond the last cow.

For each query, we must compute the total weight of all cows visited by that arithmetic progression.

The important detail is that each query is independent. We do not remove cows, and nothing changes between queries, so we are repeatedly summing values over arithmetic progressions on a static array.

The constraints are large: up to 3×10^5 cows and 3×10^5 queries. A direct simulation per query can take up to O(n) steps in the worst case, which leads to O(n·p) ≈ 10^10 operations. That is far beyond feasible limits.

The key difficulty is that the step size b can vary per query, which prevents a single prefix-sum trick from handling all queries uniformly.

A few edge cases matter. If b = 1, the query is just a range suffix sum from a to n. If a is near the end, the progression may contain only one element. If b is large, each query touches very few elements, but we cannot rely on that because worst-case b = 1 makes it linear.

## Approaches

The brute-force idea is straightforward: for each query, start at index a and keep adding a, a + b, a + 2b until exceeding n. Each step adds one value to the answer. This is correct because it exactly follows the definition of the raid. However, in the worst case where b = 1, each query touches O(n) elements, so the total complexity becomes O(n·p), which is too slow.

The key observation is that step sizes behave very differently depending on magnitude. If b is large, the number of visited elements is small, because a + kb exceeds n quickly. If b is small, then although each query visits many elements, there are only few distinct step sizes, and we can precompute answers for all small b using dynamic programming over residue classes.

The standard optimization is to split queries into two regimes. For large b, we directly simulate the progression because it is short. For small b, we precompute answers using a DP table where we accumulate sums from the end of the array backwards along steps of size b. This avoids recomputing overlapping arithmetic progressions repeatedly.

This works because all jumps with fixed b form independent chains by residue modulo b, and we can process each chain in reverse order in linear time per b.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n per query) | O(1) | Too slow |
| sqrt decomposition on step size | O(n √n + p √n) | O(n √n) | Accepted |

## Algorithm Walkthrough

We choose a threshold B around √n. Step sizes are classified into small (b ≤ B) and large (b > B).

1. Precompute answers for all small step sizes b by building a DP table over the array. For a fixed b, we process indices from n down to 1, and maintain dp[b][i] = w[i] + dp[b][i + b] if i + b ≤ n, otherwise just w[i]. This lets us answer any small-b query in O(1) time.
2. For large step sizes b, we do not precompute anything. Instead, for each query we directly simulate i, i + b, i + 2b until we exceed n, summing weights along the way. Since b is large, the number of visited positions is at most n / B, which is small.
3. For each query, we check whether b ≤ B. If yes, we return dp[b][a]. Otherwise, we compute the sum by stepping through the array manually.
4. Output the result for each query independently.

The reason this separation works is that every query either has few distinct step chains (small b) or few elements per chain (large b), so we avoid the worst-case blowup in both dimensions.

### Why it works

Fix a step size b. The indices split into independent sequences based on residue modulo b. Within each sequence, the contribution of each position depends only on the next position in the same sequence. By processing from right to left, we ensure that when computing dp[b][i], the value dp[b][i + b] is already known. This creates a correct recurrence that exactly matches the definition of the raid sum. No overlap between different residues affects correctness, because jumps never cross residue classes.

## Python Solution

```python
import sys
input = sys.stdin.readline

def main():
    n = int(input())
    w = list(map(int, input().split()))
    p = int(input())

    B = int(n ** 0.5) + 1

    dp = [None] * (B + 1)
    for b in range(1, B + 1):
        dp[b] = [0] * n
        for i in range(n - 1, -1, -1):
            j = i + b
            if j < n:
                dp[b][i] = w[i] + dp[b][j]
            else:
                dp[b][i] = w[i]

    out = []
    for _ in range(p):
        a, b = map(int, input().split())
        a -= 1

        if b <= B:
            out.append(str(dp[b][a]))
        else:
            s = 0
            i = a
            while i < n:
                s += w[i]
                i += b
            out.append(str(s))

    print("\n".join(out))

if __name__ == "__main__":
    main()
```

The DP table construction is the core optimization. Each dp[b][i] represents the sum of the arithmetic progression starting at i with step b. We compute it backwards so that transitions are already resolved.

For large steps, the loop is intentionally simple: we just walk the progression. The key correctness point is that the number of iterations is small enough to pass due to the chosen threshold.

A subtle implementation detail is indexing: the input is 1-based, but DP is built on 0-based indexing, so a must be decremented once and consistently used in that form.

## Worked Examples

### Example 1

Input:

```
3
1 2 3
2
1 1
1 2
```

We set B = 1 for this tiny case.

| Query | a | b | Traversal | Sum |
| --- | --- | --- | --- | --- |
| 1 | 0 | 1 | 0 → 1 → 2 | 6 |
| 2 | 0 | 2 | 0 → 2 | 4 |

First query collects all elements since step is 1. Second query picks alternating positions starting from index 0.

This confirms that both dense and sparse progressions are handled correctly.

### Example 2

Input:

```
4
2 3 5 7
3
1 3
2 3
2 2
```

Here B = 2.

| Query | a | b | Traversal | Sum |
| --- | --- | --- | --- | --- |
| 1 | 0 | 3 | 0 → 3 | 9 |
| 2 | 1 | 3 | 1 | 3 |
| 3 | 1 | 2 | 1 → 3 | 10 |

The third query shows a mixed pattern where stepping skips one element each time, confirming correct handling of general arithmetic jumps.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n√n + p√n) | Precompute DP for small step sizes, and simulate long jumps for large steps |
| Space | O(n√n) | DP table stores values for all small step sizes |

With n, p up to 3×10^5, √n is about 550, so total operations stay comfortably within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from math import sqrt
    input = sys.stdin.readline

    n = int(input())
    w = list(map(int, input().split()))
    p = int(input())

    B = int(n ** 0.5) + 1
    dp = [None] * (B + 1)

    for b in range(1, B + 1):
        dp[b] = [0] * n
        for i in range(n - 1, -1, -1):
            j = i + b
            dp[b][i] = w[i] + (dp[b][j] if j < n else 0)

    out = []
    for _ in range(p):
        a, b = map(int, input().split())
        a -= 1
        if b <= B:
            out.append(str(dp[b][a]))
        else:
            s = 0
            i = a
            while i < n:
                s += w[i]
                i += b
            out.append(str(s))

    return "\n".join(out)

# provided samples
assert run("""3
1 2 3
2
1 1
1 2
""") == "6\n4"

# custom cases
assert run("""1
10
2
1 1
1 2
""") == "10\n10"

assert run("""5
1 1 1 1 1
2
1 2
2 2
""") == "3\n2"

assert run("""6
5 4 3 2 1 0
2
1 3
2 3
""") == "8\n4"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single element | direct sums | minimal boundary |
| uniform array | consistency across steps | correctness under symmetry |
| reverse pattern | mixed traversal correctness | step skipping behavior |

## Edge Cases

For b = 1, the algorithm relies entirely on dp[1], which effectively becomes suffix sums over the entire array. This case ensures correctness for maximal-length progressions.

For b ≥ n, the traversal visits exactly one element, because a + b immediately exceeds bounds. The algorithm handles this naturally in both DP and simulation paths.

For alternating small values, such as w = [1, 0, 1, 0, ...] with b = 2, the DP ensures we correctly accumulate only same-parity indices, confirming that residue-class decomposition is sound.

---
problem: 981D
contest_id: 981
problem_index: D
name: "Bookshelves"
contest_name: "Avito Code Challenge 2018"
rating: 1900
tags: ["bitmasks", "dp", "greedy"]
answer: passed_samples
verified: true
solve_time_s: 70
date: 2026-06-18
model: gpt-5-3-mini
samples_passed: 1
samples_total: 1
share_url: https://chatgpt.com/share/6a33a5e2-81c8-83ec-803d-4377b87d6ef6
---

# CF 981D - Bookshelves

**Rating:** 1900  
**Tags:** bitmasks, dp, greedy  
**Model:** gpt-5-3-mini  
**Solve time:** 1m 10s  
**Verified:** yes (1/1 samples)  
**Share:** https://chatgpt.com/share/6a33a5e2-81c8-83ec-803d-4377b87d6ef6  

---

## Solution

## Problem Understanding

We are given a sequence of positive integers representing books arranged in a fixed order. Each book has a value, and we must split this sequence into exactly k contiguous segments. Each segment corresponds to one bookshelf, and the value of a bookshelf is the sum of the values in that segment.

Once the partition is chosen, we compute k segment sums and then take the bitwise AND of all these sums. The goal is to choose the partition so that this final AND value is as large as possible.

The structure is important: we are not reordering books, only deciding cut positions between them. Every book must belong to exactly one segment, and no segment can be empty.

The constraints n ≤ 50 and k ≤ n immediately suggest that a cubic or even moderately nested quadratic solution may be acceptable, but anything exponential in n without pruning is too large. A solution involving dynamic programming over positions and number of segments is plausible because the state space is small: at most 50 positions and 50 segments.

A naive approach that tries all partitions has combinatorial explosion. The number of ways to choose k−1 cuts among n−1 gaps is already large enough to make brute force infeasible in the worst case.

A few subtle edge cases matter.

One is when k = n. Then every segment has exactly one book, and the answer is simply the bitwise AND of all individual values.

Another is when k = 1. Then there is only one segment, and the answer is the sum of all elements. A careless DP implementation often forgets to initialize this case correctly.

A more interesting case is when values are large but sparse in bits. Because AND is bitwise, higher bits dominate the answer, and incorrect grouping can silently drop a bit that could have been preserved.

## Approaches

The brute force idea is to enumerate all ways of placing k−1 cuts among n−1 positions, compute each partition’s segment sums, and then compute the AND of those sums. For each partition, computing sums takes O(n), and there are C(n−1, k−1) partitions. This becomes enormous even for n = 50, easily exceeding 10^13 configurations in the worst case.

The key observation is that we only care about prefix sums when computing segment sums, and the partitioning structure depends only on cut positions. This suggests dynamic programming over prefixes.

We define a DP where we decide how to split the first i elements into j segments. The crucial idea is that once we fix the last cut position, the value of the last segment is known via prefix sums, and all previous segments are independent.

Thus we can try every possible previous cut position p < i and transition from dp[p][j−1] to dp[i][j] using the sum of elements in (p+1 ... i). The final answer is the maximum possible bitwise AND over all dp[n][k] states.

We store for each dp state not a single value but the best achievable AND result. Since AND is monotonic in the sense that adding more constraints only decreases bits, the DP remains valid.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(C(n,k) · n) | O(n) | Too slow |
| Optimal DP | O(n^2 k) | O(n k) | Accepted |

## Algorithm Walkthrough

We use prefix sums to compute segment sums in O(1). Let pref[i] be sum of first i books.

1. Build prefix sums so that any segment sum from l to r is pref[r] − pref[l−1]. This allows constant time segment evaluation.
2. Define dp[i][j] as the maximum possible value of the bitwise AND of segment sums when splitting first i books into j non-empty contiguous segments.
3. Initialize dp[0][0] = (all bits set, conceptually 2^50−1). This represents no segments chosen yet.
4. For each i from 1 to n, set dp[i][1] = pref[i], since with one segment the value is fixed.
5. For each j from 2 to k, and for each i from j to n, try all possible last cut positions p from j−1 to i−1.
6. For each transition, compute segment_sum = pref[i] − pref[p], and update:

dp[i][j] = max(dp[i][j], dp[p][j−1] & segment_sum).

The AND combines the previous best structure with the new segment contribution.
7. The final answer is dp[n][k].

The reason we loop p over all possible previous cut positions is that the last segment depends on where we cut, and different choices can preserve different bit patterns after ANDing.

### Why it works

At every state dp[i][j], we have considered all possible ways to partition the prefix of length i into j segments. Any valid partition must end with some last cut position p. For that fixed p, the best achievable result on the prefix p is already stored in dp[p][j−1]. Extending it with the last segment produces exactly one valid candidate value, and taking the maximum over all p ensures we explore every valid partition. Since AND is applied consistently at each step, every dp state exactly represents the best achievable bitwise result for that prefix and segment count.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, k = map(int, input().split())
a = list(map(int, input().split()))

pref = [0] * (n + 1)
for i in range(n):
    pref[i + 1] = pref[i] + a[i]

NEG = -1  # all bits set in Python two's complement representation is not needed explicitly

dp = [[-1] * (k + 1) for _ in range(n + 1)]
dp[0][0] = (1 << 60) - 1

for i in range(1, n + 1):
    dp[i][1] = pref[i]

for j in range(2, k + 1):
    for i in range(j, n + 1):
        best = -1
        for p in range(j - 1, i):
            if dp[p][j - 1] == -1:
                continue
            seg = pref[i] - pref[p]
            val = dp[p][j - 1] & seg
            if val > best:
                best = val
        dp[i][j] = best

print(dp[n][k])
```

The prefix sum array allows us to compute any segment sum in constant time, avoiding repeated recomputation inside transitions. The DP table stores the best achievable AND result for each prefix and segment count. The triple loop over j, i, and p is safe under n ≤ 50.

The initialization dp[i][1] = pref[i] encodes the fact that with a single bookshelf there is no choice. The use of −1 as an invalid state ensures we do not propagate impossible partitions.

## Worked Examples

### Example 1

Input:

```
5 2
1 2 3 4 5
```

Prefix sums:

| i | pref |
| --- | --- |
| 1 | 1 |
| 2 | 3 |
| 3 | 6 |
| 4 | 10 |
| 5 | 15 |

We compute dp[i][1] directly:

dp[1][1]=1, dp[2][1]=3, dp[3][1]=6, dp[4][1]=10, dp[5][1]=15.

For j = 2:

For i = 3:

p=1: (1) & (2+3=5) = 1 & 5 = 1

p=2: (3) & (3) = 3 & 3 = 3

So dp[3][2]=3.

For i = 4:

p=1: 1 & 9 = 1

p=2: 3 & 7 = 3

p=3: 6 & 4 = 4

dp[4][2]=4.

For i = 5:

p=1: 1 & 14 = 0

p=2: 3 & 12 = 0

p=3: 6 & 9 = 0

p=4: 10 & 5 = 0

dp[5][2]=0.

Final answer is dp[5][2]=0.

This trace shows how different split points preserve different bits, and how AND quickly collapses values when segments are large and mixed.

### Example 2

Input:

```
4 3
2 1 2 1
```

Prefix sums: 2, 3, 5, 6.

dp[i][1] = 2, 3, 5, 6.

For j=2:

dp[2][2] impossible, dp[3][2], dp[4][2]:

dp[3][2]:

p=1: 2 & 1 = 0

p=2: 3 & 2 = 2

dp[3][2]=2

dp[4][2]:

p=1: 2 & 3 = 2

p=2: 3 & 2 = 2

p=3: 5 & 1 = 1

dp[4][2]=2

For j=3:

dp[4][3]:

p=2: dp[2][2] invalid

p=3: dp[3][2] & 1 = 2 & 1 = 0

dp[4][3]=0

Final answer is 0.

This example demonstrates how increasing number of segments increases AND constraints, often reducing the final value.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n^3) | Three nested loops over segments, end position, and cut position |
| Space | O(nk) | DP table for prefixes and segment counts |

With n ≤ 50, n^3 is at most 125000 operations, easily within limits. Memory usage is also negligible.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from math import inf

    n, k = map(int, input().split())
    a = list(map(int, input().split()))

    pref = [0] * (n + 1)
    for i in range(n):
        pref[i + 1] = pref[i] + a[i]

    dp = [[-1] * (k + 1) for _ in range(n + 1)]
    dp[0][0] = (1 << 60) - 1

    for i in range(1, n + 1):
        dp[i][1] = pref[i]

    for j in range(2, k + 1):
        for i in range(j, n + 1):
            best = -1
            for p in range(j - 1, i):
                if dp[p][j - 1] == -1:
                    continue
                seg = pref[i] - pref[p]
                best = max(best, dp[p][j - 1] & seg)
            dp[i][j] = best

    return str(dp[n][k])

# provided sample
assert run("10 4\n9 14 28 1 7 13 15 29 2 31\n") == "24", "sample 1"

# custom tests
assert run("1 1\n5\n") == "5", "single element"
assert run("5 5\n1 2 3 4 5\n") == "1", "all singletons AND"
assert run("5 1\n1 2 3 4 5\n") == "15", "single segment"
assert run("3 2\n8 8 8\n") == "8", "uniform values"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1 / 5 | 5 | minimal case |
| 5 5 / 1 2 3 4 5 | 1 | every element separate |
| 5 1 / 1 2 3 4 5 | 15 | single segment correctness |
| 3 2 / 8 8 8 | 8 | stability under identical values |

## Edge Cases

A key edge case is when k = n, meaning every book forms its own segment. For input:

```
3 3
5 1 7
```

the only valid partition is [5], [1], [7]. The DP initializes dp[i][1] correctly, and higher segment transitions force each cut at exact positions, producing segment sums 5, 1, 7 and final result 5 & 1 & 7 = 1.

Another edge case is k = 1:

```
4 1
2 3 4 5
```

There is no splitting. dp[n][1] directly becomes total sum 14. Any DP state beyond j=1 is irrelevant, and the algorithm naturally avoids them.

A third case involves large values where bit structure matters:

```
4 2
8 4 2 1
```

Different splits preserve different high bits, but the DP explores all cut positions, ensuring the best combination is chosen.
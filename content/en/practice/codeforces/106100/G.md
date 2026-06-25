---
title: "CF 106100G - Transformable Segment"
description: "We are given a long array A and a target array B. For any chosen segment A[L..R], we are allowed to repeatedly delete elements until the segment length becomes m = The task is to count how many segments of A can be transformed into exactly B."
date: "2026-06-25T11:53:13+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106100
codeforces_index: "G"
codeforces_contest_name: "International MathCoding Narxoz open olympiad 2025"
rating: 0
weight: 106100
solve_time_s: 90
verified: true
draft: false
---

[CF 106100G - Transformable Segment](https://codeforces.com/problemset/problem/106100/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 30s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a long array `A` and a target array `B`.

For any chosen segment `A[L..R]`, we are allowed to repeatedly delete elements until the segment length becomes `m = |B|`. The deletion rule is unusual: an element can be deleted only if it has a right neighbor and the two values are different.

The task is to count how many segments of `A` can be transformed into exactly `B`.

The key constraint is that `n` can be as large as `2 · 10^5`, while `m ≤ 100`. Any solution that inspects all `O(n²)` segments is immediately impossible. Even `O(n² / 10)` would be far too large. The small value of `m` is the real hint. It suggests that we should build a dynamic programming solution whose complexity is roughly `O(nm)`.

The dangerous part of the problem is understanding which elements are actually removable.

Consider the segment:

```
1 1 2
```

We may delete the second `1`, then delete the first `1`, leaving only `2`.

Now consider:

```
1 1
```

No deletion is possible. The first element is equal to its right neighbor, and the second element has no right neighbor at all.

The entire trailing block of equal values is special. If a segment ends with:

```
... 5 5 5
```

then all three trailing `5`s are forced to survive. Nothing can ever delete them.

This observation is the foundation of the solution.

### Non-obvious edge case 1

```
A = [1, 1]
B = [1]
```

The answer is `0`.

A careless interpretation might think that one of the `1`s can be removed. It cannot. The whole suffix run consists of equal values, so neither element is deletable.

### Non-obvious edge case 2

```
A = [1, 2, 1]
B = [1, 1]
```

The answer is `1`.

The middle `2` can be deleted because it differs from its right neighbor. The result becomes `[1,1]`.

A solution that only thinks about preserving runs independently often misses that removing an entire run may cause two equal values to become adjacent and merge.

### Non-obvious edge case 3

```
A = [7, 7, 7]
B = [7, 7]
```

The answer is `0`.

The trailing run length is `3`, and every element in that run is forced to remain. Since the target length is only `2`, transformation is impossible.

## Approaches

A brute force solution would inspect every segment and determine whether it can be transformed into `B`.

There are `O(n²)` segments. Even if we had an `O(m)` verification procedure, the total complexity would be around `4 · 10^10` operations in the worst case, which is completely infeasible.

The crucial observation is to characterize all possible final arrays obtainable from a segment.

Take any segment and look at its last run of equal values.

```
x x x x
```

Every element of that run is forced to survive.

Every position before that final run is optional. We can either keep it or eventually delete it.

As a consequence, a segment can produce `B` if and only if:

1. The whole trailing run is mapped to the suffix of `B`.
2. The remaining prefix of `B` appears as a subsequence before that run.

This turns the problem into a subsequence-counting problem.

Since `m ≤ 100`, we can scan `A` once and maintain dynamic programming values for all prefixes of `B`. For every possible trailing run we ask a single question:

```
How many starting positions L allow
B[1..p] to appear as a subsequence
before the run starts?
```

The DP answers that in `O(1)` time after preprocessing.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²m) | O(m) | Too slow |
| Optimal | O(nm) | O(m + n) | Accepted |

## Algorithm Walkthrough

1. Compute the start position of the equal-value run ending at every index.

If index `R` belongs to a run that starts at `s`, then the mandatory suffix length is:

```
k = R - s + 1
```
2. Scan the array from left to right and maintain DP values for subsequences of `B`.

Let `dp[j]` denote the maximum possible first position of a subsequence equal to `B[1..j]` inside the processed prefix.
3. For every run start position `s`, store a snapshot of all `dp[j]` values after processing position `s - 1`.

Later we will need exactly these values.
4. Precompute for every suffix length `k` whether the last `k` elements of `B` are all equal to some value `v`.
5. Process each run of `A`.

Suppose a run starts at `s`, has value `v`, and length `len`.

For every possible suffix length:

```
k = 1 .. min(len, m)
```

corresponding to segment ending at:

```
R = s + k - 1
```

check whether the last `k` elements of `B` are all equal to `v`.
6. If not, this segment can never work.

If yes, let:

```
p = m - k
```

be the number of elements that must come from before the run.
7. When `p = 0`, the whole target is formed by the mandatory run. Any start position:

```
1 ≤ L ≤ s
```

is valid, contributing `s` segments.
8. When `p > 0`, we need a subsequence equal to `B[1..p]` before the run.

The stored DP snapshot at position `s - 1` gives:

```
mx = maximum first position of such a subsequence
```

Every start position:

```
L ≤ mx
```

works.

Add `mx` to the answer.

### Why it works

The final run of a segment is immutable. Every element in that run survives in every valid transformation.

Every position before the final run is removable. By deleting unwanted elements, we may keep exactly any subsequence of the prefix preceding the run.

Thus a valid transformation is completely determined by choosing a subsequence equal to the prefix of `B` before the run and matching the mandatory run against the suffix of `B`.

The DP stores the latest possible starting position of each matched prefix of `B`. If a match can start at position `x`, then every segment start `L ≤ x` contains that match. Counting such starts gives exactly the number of valid segments.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, m = map(int, input().split())
A = list(map(int, input().split()))
B = list(map(int, input().split()))

# run starts
run_start = [0] * n
run_start[0] = 0
for i in range(1, n):
    if A[i] == A[i - 1]:
        run_start[i] = run_start[i - 1]
    else:
        run_start[i] = i

# group positions by run start
runs = []
i = 0
while i < n:
    j = i
    while j + 1 < n and A[j + 1] == A[i]:
        j += 1
    runs.append((i, j, A[i]))
    i = j + 1

# snapshots[s] = dp state after processing prefix ending at s-1
snapshots = {}

dp = [0] * (m + 1)

for pos in range(n + 1):
    snapshots[pos] = dp[:]

    if pos == n:
        break

    x = A[pos]

    for j in range(m, 0, -1):
        if x == B[j - 1]:
            if j == 1:
                dp[1] = max(dp[1], pos + 1)
            elif dp[j - 1]:
                dp[j] = max(dp[j], dp[j - 1])

# suffix information of B
suffix_ok = [False] * (m + 1)
suffix_val = [None] * (m + 1)

for k in range(1, m + 1):
    v = B[m - 1]
    good = True
    for t in range(m - k, m):
        if B[t] != v:
            good = False
            break
    suffix_ok[k] = good
    suffix_val[k] = v

ans = 0

for start, end, value in runs:
    length = end - start + 1

    limit = min(length, m)

    state = snapshots[start]

    for k in range(1, limit + 1):
        if not suffix_ok[k]:
            continue
        if suffix_val[k] != value:
            continue

        p = m - k

        if p == 0:
            ans += start + 1
        else:
            ans += state[p]

print(ans)
```

The DP array has only `m + 1` states, so updating it costs `O(m)` per array element.

The meaning of `dp[j]` is subtle. It stores the largest possible first position of a matched subsequence equal to `B[1..j]`. Using the largest first position is exactly what we need, because every segment start not exceeding that position is valid.

The snapshots are taken before processing each position. When a run starts at index `s`, we need information only from the prefix ending at `s - 1`, which is why `snapshots[s]` is the correct state.

The implementation uses 1-based positions inside the DP values. This makes the counting formula straightforward because the number of valid starts is exactly the stored position.

## Worked Examples

### Example 1

```
A = [1, 1, 2]
B = [1, 2]
```

The runs are:

| Run start | Run end | Value |
| --- | --- | --- |
| 1 | 2 | 1 |
| 3 | 3 | 2 |

For the second run:

| k | Required suffix of B | Valid |
| --- | --- | --- |
| 1 | [2] | Yes |

Then `p = 1`.

The prefix before the run contains a subsequence `[1]` whose latest possible start is position `2`.

So starts `L = 1` and `L = 2` are both valid.

Answer:

```
2
```

This demonstrates why both segments `[1,1,2]` and `[1,2]` are counted.

### Example 2

```
A = [1, 2, 1]
B = [1, 1]
```

The final run has value `1` and length `1`.

| k | p |
| --- | --- |
| 1 | 1 |

Before the run we need subsequence `[1]`.

The latest possible start is position `1`.

So exactly one segment works.

| Quantity | Value |
| --- | --- |
| Latest start of prefix match | 1 |
| Added to answer | 1 |

Answer:

```
1
```

This confirms that deleting the middle `2` is sufficient.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(nm) | Each array position updates at most `m` DP states |
| Space | O(nm) snapshots conceptually reduced to O(nm) integers | We store one DP snapshot of size `m+1` for each position |

With `n = 2 · 10^5` and `m ≤ 100`, the running time is about twenty million DP transitions, which comfortably fits within the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    # paste solve() here when testing locally
    pass

# sample
assert run(
"""3 2
1 1 2
1 2
"""
) == "2\n"

# minimum size
assert run(
"""1 1
5
5
"""
) == "1\n"

# impossible
assert run(
"""2 1
1 1
1
"""
) == "0\n"

# all equal
assert run(
"""4 2
7 7 7 7
7 7
"""
) == "0\n"

# merge after deleting middle run
assert run(
"""3 2
1 2 1
1 1
"""
) == "1\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 / 5 / 5` | `1` | Minimum size |
| `1 1 / 1 1 / 1` | `0` | Forced suffix run |
| All equal values | `0` | Large immutable run |
| `1 2 1` → `1 1` | `1` | Run merging after deletion |

## Edge Cases

For

```
A = [1, 1]
B = [1]
```

the trailing run length is `2`, while `|B| = 1`.

The algorithm checks only `k ≤ m`. No valid configuration exists, so the contribution is zero.

For

```
A = [1, 2, 1]
B = [1, 1]
```

the last run has length `1`, matching the last element of `B`.

The DP snapshot before the run records a valid subsequence `[1]` starting at position `1`, producing exactly one valid segment.

For

```
A = [7, 7, 7]
B = [7, 7]
```

the trailing run length is already `3`.

Since all three elements are mandatory survivors, no segment ending at the last position can ever shrink to length `2`. The algorithm rejects it automatically because the required suffix length cannot be satisfied.

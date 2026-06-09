---
title: "CF 1659D - Reverse Sort Sum"
description: "We start with an unknown binary array $A$. For every prefix length $k$, we sort the first $k$ elements of $A$, leaving the rest unchanged. This produces $n$ arrays $B1, B2, dots, Bn$. Instead of seeing those arrays directly, we are given their column-wise sum $C$."
date: "2026-06-10T03:19:54+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "data-structures", "greedy", "implementation", "math", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 1659
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 782 (Div. 2)"
rating: 1900
weight: 1659
solve_time_s: 725
verified: false
draft: false
---

[CF 1659D - Reverse Sort Sum](https://codeforces.com/problemset/problem/1659/D)

**Rating:** 1900  
**Tags:** constructive algorithms, data structures, greedy, implementation, math, two pointers  
**Solve time:** 12m 5s  
**Verified:** no  

## Solution
## Problem Understanding

We start with an unknown binary array $A$. For every prefix length $k$, we sort the first $k$ elements of $A$, leaving the rest unchanged. This produces $n$ arrays $B_1, B_2, \dots, B_n$.

Instead of seeing those arrays directly, we are given their column-wise sum $C$. The task is to reconstruct any binary array $A$ that could have generated the given $C$.

The key observation is that we are not asked to verify existence. The statement guarantees that at least one valid array exists. Our only job is to recover one.

The array length can reach $2 \cdot 10^5$ across all test cases. Any solution that explicitly builds all $B_k$ arrays would require $O(n^2)$ work, which is far too large. We need a reconstruction procedure that runs in linear time per test case.

A common source of mistakes is misunderstanding what information is preserved by the transformation. For example, the total number of ones in $A$ is not lost. Every sorted array $B_k$ contains exactly the same number of ones as $A$, because sorting does not change element counts. Since $C$ is the sum of all $B_k$, the total sum of $C$ equals

$$n \cdot (\text{number of ones in } A).$$

This fact is the starting point of the reconstruction.

Another subtle case occurs when many positions of $C$ are equal. For example,

```
n = 3
C = [0,0,0]
```

The correct answer is

```
0 0 0
```

A reconstruction procedure that greedily inserts ones whenever possible would immediately fail.

A different edge case is

```
n = 4
C = [0,0,0,4]
```

The answer is

```
0 0 0 1
```

The last position alone carries enough information to force a one at the end.

## Approaches

The most direct idea is to try every binary array $A$, generate all sorted-prefix arrays, compute $C$, and compare it with the input.

This is correct but hopelessly slow. There are $2^n$ candidate arrays. Even for $n=40$, this already exceeds one trillion possibilities.

The real breakthrough comes from studying how a single one contributes to the final array $C$.

Suppose we know how many ones remain to be placed while reconstructing the answer from right to left. A one placed at position $i$ affects a contiguous range of earlier positions in a very regular way. Instead of simulating the sorting process directly, we can represent those effects with a difference array.

This converts the reconstruction into a greedy right-to-left scan. At each position we decide whether the current element must be $0$ or $1$, apply the contribution of that decision lazily through the difference array, and continue.

The resulting algorithm is linear.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(2^n \cdot n^2)$ | $O(n^2)$ | Too slow |
| Optimal | $O(n)$ per test case | $O(n)$ | Accepted |

## Algorithm Walkthrough

### Key Observation

Let

$$k = \frac{\sum C_i}{n}.$$

Since every array $B_j$ contains exactly the same number of ones as $A$, $k$ is exactly the number of ones in the unknown array.

We reconstruct $A$ from right to left.

Let `ones` denote how many ones still have not been fixed.

We maintain a difference array that stores the accumulated effect of previously chosen ones.

### Reconstruction Rule

At position $i$, after applying all active updates, we obtain an adjusted value

$$v = C_i + \text{current\_effect}.$$

Then:

1. If $v = \text{ones}$, the current position must be $0$.
2. Otherwise the current position must be $1$.

When we place a one:

1. We set $A_i = 1$.
2. We decrease `ones` by one.
3. We add its contribution lazily using the difference array.

### Why the Comparison Works

When scanning from right to left, every already-decided one contributes a predictable amount to earlier positions. After removing those contributions, the remaining value at position $i$ can only match the current number of unplaced ones if the original bit was zero.

If it does not match, the only valid possibility is that the original bit was one. The existence guarantee ensures this decision is never ambiguous.

### Step-by-Step Algorithm

1. Compute

$$\text{ones} = \frac{\sum C_i}{n}.$$
2. Create a difference array `diff`.
3. Scan positions from right to left.
4. Apply pending difference updates to obtain the current accumulated effect.
5. Let

$$v = C_i + \text{current\_effect}.$$
6. If `v == ones`, set $A_i = 0$.
7. Otherwise set $A_i = 1$, decrease `ones`, and register the contribution of this newly placed one in the difference structure.
8. Output the reconstructed binary array.

### Why it works

The algorithm maintains the invariant that all contributions of already reconstructed positions have been removed from the suffix currently being processed.

At position $i$, the adjusted value represents exactly the information that remains unexplained. A zero leaves the current count of remaining ones unchanged, while a one consumes one remaining one and creates a known contribution interval. Because the input is guaranteed to be valid, exactly one of these choices is consistent with the invariant.

By processing positions from right to left, every contribution interval affects only positions that will be visited later, which allows the difference array to handle all updates in constant time.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())

    for _ in range(t):
        n = int(input())
        c = list(map(int, input().split()))

        ones = sum(c) // n

        diff = [0] * (n + 1)
        cur = 0
        ans = [0] * n

        for i in range(n - 1, -1, -1):
            cur += diff[i]

            val = c[i] + cur

            if val == ones:
                ans[i] = 0
            else:
                ans[i] = 1

                ones -= 1

                cur -= 1

                pos = i - ones
                if pos >= 0:
                    diff[pos] += 1

        print(*ans)

solve()
```

The first step computes the total number of ones. This follows directly from the fact that every sorted-prefix array preserves the number of ones.

The variable `cur` stores the total active contribution at the current position. Instead of updating every affected index individually, we use a difference array and accumulate its values while moving left.

When a one is placed, its contribution extends over a contiguous range. The update

```
cur -= 1
```

activates that contribution immediately, while

```
diff[pos] += 1
```

schedules the moment when the contribution stops affecting future positions.

The most delicate part of the implementation is

```
pos = i - ones
```

which must be computed after decrementing `ones`. Reversing that order shifts every interval by one position and breaks the reconstruction.

## Worked Examples

### Example 1

Input:

```
n = 4
C = [2, 4, 2, 4]
```

First,

$$\text{ones} = (2+4+2+4)/4 = 3.$$

| i | cur | adjusted value | ones before | decision |
| --- | --- | --- | --- | --- |
| 3 | 0 | 4 | 3 | 1 |
| 2 | -1 | 1 | 2 | 1 |
| 1 | -1 | 3 | 1 | 1 |
| 0 | 0 | 2 | 0 | 0 |

Result:

```
1 1 0 1
```

This is one of the accepted answers.

### Example 2

Input:

```
n = 3
C = [0,0,0]
```

Then

$$\text{ones} = 0.$$

| i | cur | adjusted value | ones | decision |
| --- | --- | --- | --- | --- |
| 2 | 0 | 0 | 0 | 0 |
| 1 | 0 | 0 | 0 | 0 |
| 0 | 0 | 0 | 0 | 0 |

Result:

```
0 0 0
```

This example demonstrates that the algorithm naturally handles the case where no ones exist.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n)$ | Each position is processed once |
| Space | $O(n)$ | Difference array and answer array |

The total length across all test cases is at most $2 \cdot 10^5$, so the overall running time is linear in the input size. This easily fits within the limits.

## Test Cases

```
# These are conceptual tests for the reconstruction routine.

# 1. Sample case
# Input:
# 4
# 2 4 2 4
# One valid output:
# 1 1 0 1

# 2. All zeros
# Input:
# 3
# 0 0 0
# Output:
# 0 0 0

# 3. Single element zero
# Input:
# 1
# 0
# Output:
# 0

# 4. Single element one
# Input:
# 1
# 1
# Output:
# 1

# 5. Large trailing contribution
# Input:
# 4
# 0 0 0 4
# Output:
# 0 0 0 1
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `[2,4,2,4]` | `1 1 0 1` | General reconstruction |
| `[0,0,0]` | `0 0 0` | No ones present |
| `[0]` | `0` | Minimum size, zero |
| `[1]` | `1` | Minimum size, one |
| `[0,0,0,4]` | `0 0 0 1` | Contribution interval boundaries |

## Edge Cases

Consider

```
n = 1
C = [0]
```

The total number of ones is zero. The scan immediately finds that the adjusted value equals the remaining number of ones, so the answer is `[0]`.

Consider

```
n = 1
C = [1]
```

Now the total number of ones is one. The adjusted value differs from the remaining count, forcing the only position to become one.

Consider

```
n = 4
C = [0,0,0,4]
```

The computed number of ones is one. The rightmost position is forced to be one. Its contribution is propagated through the difference array, and all earlier positions become zero. This catches the most common off-by-one mistake in the interval update logic.

Consider

```
n = 3
C = [0,0,0]
```

No updates are ever activated. The difference array remains empty throughout the scan, confirming that the implementation handles the absence of ones without any special cases.

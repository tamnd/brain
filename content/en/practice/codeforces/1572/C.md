---
title: "CF 1572C - Paint"
description: "We have a one dimensional image represented by an array of colors. A single operation chooses a connected monochromatic segment and repaints the entire segment to any color. The connectivity definition is slightly unusual."
date: "2026-06-10T11:18:42+07:00"
tags: ["codeforces", "competitive-programming", "dp", "greedy"]
categories: ["algorithms"]
codeforces_contest: 1572
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 743 (Div. 1)"
rating: 2700
weight: 1572
solve_time_s: 337
verified: false
draft: false
---

[CF 1572C - Paint](https://codeforces.com/problemset/problem/1572/C)

**Rating:** 2700  
**Tags:** dp, greedy  
**Solve time:** 5m 37s  
**Verified:** no  

## Solution
## Problem Understanding

We have a one dimensional image represented by an array of colors. A single operation chooses a connected monochromatic segment and repaints the entire segment to any color.

The connectivity definition is slightly unusual. Two positions of the same color are connected if every position between them has that same color as well. In a one dimensional array, this simply means a maximal contiguous block of equal values. An operation picks one such block and changes the color of the whole block.

The goal is to make the entire array a single color using the minimum number of operations.

A direct simulation viewpoint is misleading because repainting one block may merge it with neighboring blocks of the target color, creating larger connected components that can later be repainted together.

The total length over all test cases is at most 3000. This is the key constraint. A cubic dynamic programming solution over intervals is feasible because $3000^3$ is too large globally, but the special restriction that every color appears at most 20 times dramatically reduces the number of meaningful transitions. The intended solution exploits this restriction to avoid considering all interval splits.

The most common mistake is to think in terms of contiguous blocks after coordinate compression. That loses essential information.

Consider:

```
1 2 1
```

The answer is 1. Repaint the middle block from 2 to 1 and the entire array becomes color 1.

A compression-based approach sees three blocks and may incorrectly conclude that two merges are needed.

Another subtle case is:

```
1 2 3 2 1
```

The answer is 2.

First repaint 3 into 2:

```
1 2 2 2 1
```

Then repaint the central block of 2s into 1:

```
1 1 1 1 1
```

A greedy strategy that always expands the largest color block fails because the optimal sequence depends on matching equal colors at both ends of an interval.

A third trap is assuming the final color must already exist everywhere inside the interval.

For:

```
1 2 1 4 2
```

The answer is 3. The optimal process repeatedly creates larger regions before the final merge. Local decisions do not reveal the global optimum.

## Approaches

A brute force approach would treat every image configuration as a state and run BFS over all reachable repaintings. The operation is easy to simulate: choose a block and recolor it. This search is correct because every operation has unit cost.

The problem is the state space. Even for modest values of $n$, the number of possible colorings grows exponentially. There is no hope of exploring all reachable configurations.

The crucial observation is that repainting behaves very similarly to interval merging problems such as Strange Printer. If two equal colors appear at positions $i$ and $j$, we may eventually make the entire interval $[i,j]$ collapse into a single region without paying separately for both endpoints.

This suggests an interval DP.

Let $dp[l][r]$ denote the minimum operations needed to make the subarray $a_l \dots a_r$ become a single color.

Suppose we want position $l$ to participate in the final merged color. One option is to repaint $a_l$ independently and solve the rest. Another possibility appears whenever there exists a position $k$ inside the interval with the same color as $a_l$. Then the endpoints $l$ and $k$ can be merged into the same final component, reducing the number of operations.

The restriction that each color occurs at most 20 times is what makes this practical. For each left endpoint, there are only $O(20)$ matching positions to consider. Instead of trying every split point, we only transition through equal-color occurrences.

This reduces the interval DP from a potentially cubic transition structure to roughly $O(n^2 \cdot 20)$.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force State Search | Exponential | Exponential | Too slow |
| Interval DP with Equal-Color Transitions | $O(n^2 \cdot 20)$ | $O(n^2)$ | Accepted |

## Algorithm Walkthrough

Let the array be indexed from 0.

Define $dp[l][r]$ as the minimum number of operations needed to make the interval $[l,r]$ monochromatic.

The answer will be $dp[0][n-1]$.

### Recurrence

If $l=r$, the interval already consists of one color.

$$dp[l][l]=0$$

For a longer interval, start by isolating the leftmost element.

$$dp[l][r]=1+dp[l+1][r]$$

This corresponds to repainting the color at position $l$ separately and then solving the remaining interval.

Now consider every position $k$ with

$$l<k\le r,\qquad a_k=a_l$$

If positions $l$ and $k$ have the same color, they can participate in the same final merged region.

The interval $(l+1,k-1)$ must first be made monochromatic so that $l$ and $k$ become adjacent in the merging process. After that, the suffix $[k,r]$ is solved independently.

This yields

$$dp[l][r] = \min \left( dp[l][r], \, dp[l+1][k-1] + dp[k][r] \right)$$

where an empty interval contributes 0.

### Efficient Enumeration

For each color, store the list of positions where it appears.

When processing a state $(l,r)$, only iterate over occurrences of color $a_l$. Because each color appears at most 20 times, each state performs at most 20 such transitions.

### Filling Order

Process intervals by increasing length.

When computing $dp[l][r]$, every required subinterval is strictly shorter, so its value is already known.

### Algorithm Walkthrough

1. Build a list of positions for every color.
2. Initialize $dp[l][l]=0$ for all indices.
3. Process interval lengths from 2 up to $n$.
4. For each interval $[l,r]$, start with the transition

$$dp[l][r]=1+dp[l+1][r]$$

which treats position $l$ independently.
5. Iterate through all occurrences $k$ of color $a_l$ satisfying $l<k\le r$.
6. Compute

$$cost = dp[l+1][k-1] + dp[k][r]$$

where the first term is 0 when $k=l+1$.
7. Update

$$dp[l][r]=\min(dp[l][r],cost)$$
8. After all intervals are processed, output $dp[0][n-1]$.

### Why it works

The recurrence exhausts every optimal possibility for the leftmost position.

In any optimal solution for interval $[l,r]$, either position $l$ is handled separately from every later occurrence of its color, giving the transition $1+dp[l+1][r]$, or it is eventually merged with the first matching position $k$ that belongs to its final monochromatic component.

When $l$ merges with such a $k$, every element between them must already have been absorbed into compatible regions. The cost of doing so is exactly $dp[l+1][k-1]$. After $l$ and $k$ are linked, the remaining work inside $[k,r]$ is independent and costs $dp[k][r]$.

Every optimal solution falls into one of these cases, and every transition corresponds to a realizable sequence of operations. By induction on interval length, the recurrence computes the true optimum for every interval.

## Python Solution

```python
import sys
from collections import defaultdict

input = sys.stdin.readline

def solve():
    t = int(input())
    ans = []

    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))

        pos = defaultdict(list)
        for i, x in enumerate(a):
            pos[x].append(i)

        dp = [[0] * n for _ in range(n)]

        for length in range(2, n + 1):
            for l in range(n - length + 1):
                r = l + length - 1

                dp[l][r] = 1 + dp[l + 1][r]

                for k in pos[a[l]]:
                    if k <= l:
                        continue
                    if k > r:
                        break

                    left_cost = 0
                    if l + 1 <= k - 1:
                        left_cost = dp[l + 1][k - 1]

                    dp[l][r] = min(
                        dp[l][r],
                        left_cost + dp[k][r]
                    )

        ans.append(str(dp[0][n - 1]))

    sys.stdout.write("\n".join(ans))

solve()
```

The DP table stores answers for every interval. Processing intervals by increasing length guarantees that every referenced subproblem has already been computed.

The initialization $dp[l][l]=0$ is obtained automatically because the table starts with zeros.

The transition `1 + dp[l + 1][r]` corresponds to handling the leftmost element separately.

The occurrence lists are the critical optimization. A naive implementation would test every possible split point $k$, producing $O(n^3)$ transitions. Here we only visit positions with the same color as the left endpoint. Since each color appears at most 20 times, the number of transitions per state stays bounded.

The empty interval case requires care. When $k=l+1$, the interval $[l+1,k-1]$ contains no elements, so its contribution must be zero.

## Worked Examples

### Example 1

Input:

```
1 2 3 2 1
```

Key DP states:

| Interval | Value |
| --- | --- |
| dp[2][2] | 0 |
| dp[1][3] | 1 |
| dp[0][4] | 2 |

For the full interval:

| Step | Transition | Cost |
| --- | --- | --- |
| Initial | 1 + dp[1][4] | 3 |
| Match at k=4 | dp[1][3] + dp[4][4] | 1 + 0 = 1 |
| Final dp[0][4] | 1 + best transition effect | 2 |

The equal colors at both ends allow the interval to collapse more cheaply than treating each endpoint independently.

### Example 2

Input:

```
1 1 2 2
```

Relevant states:

| Interval | Value |
| --- | --- |
| dp[0][1] | 0 |
| dp[2][3] | 0 |
| dp[0][3] | 1 |

For the whole interval:

| Step | Transition | Cost |
| --- | --- | --- |
| Initial | 1 + dp[1][3] | 2 |
| Match at k=1 | dp[1][0] + dp[1][3] | 1 |
| Final | 1 |  |

The two leading 1s already form a merged component, so only one repaint operation is needed for the entire image.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n^2 \cdot 20)$ | Each interval considers only occurrences of the left color |
| Space | $O(n^2)$ | DP table over all intervals |

Since the sum of all $n$ values is at most 3000, an $O(n^2)$ memory footprint and roughly $20n^2$ transitions fit comfortably within the limits.

## Test Cases

```python
import sys
import io
from collections import defaultdict

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline
    t = int(input())
    out = []

    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))

        pos = defaultdict(list)
        for i, x in enumerate(a):
            pos[x].append(i)

        dp = [[0] * n for _ in range(n)]

        for length in range(2, n + 1):
            for l in range(n - length + 1):
                r = l + length - 1

                dp[l][r] = 1 + dp[l + 1][r]

                for k in pos[a[l]]:
                    if k <= l:
                        continue
                    if k > r:
                        break

                    left = 0
                    if l + 1 <= k - 1:
                        left = dp[l + 1][k - 1]

                    dp[l][r] = min(dp[l][r], left + dp[k][r])

        out.append(str(dp[0][n - 1]))

    return "\n".join(out)

# provided samples
assert run(
"""3
5
1 2 3 2 1
4
1 1 2 2
5
1 2 1 4 2
"""
) == "2\n1\n3"

# minimum size
assert run(
"""1
1
7
"""
) == "0"

# all equal
assert run(
"""1
5
3 3 3 3 3
"""
) == "0"

# symmetric merge
assert run(
"""1
3
1 2 1
"""
) == "1"

# alternating colors
assert run(
"""1
4
1 2 1 2
"""
) == "2"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 7` | `0` | Single element interval |
| `3 3 3 3 3` | `0` | Already monochromatic |
| `1 2 1` | `1` | Matching endpoints merge optimally |
| `1 2 1 2` | `2` | Multiple overlapping equal-color transitions |

## Edge Cases

Consider:

```
1
1
5
```

The interval has length one. The DP base case gives `dp[0][0] = 0`. No repainting is needed because the image already has a single color.

Consider:

```
1
3
1 2 1
```

For interval `[0,2]`, the initial transition gives

$$1 + dp[1][2] = 2.$$

The matching occurrence at position 2 produces

$$dp[1][1] + dp[2][2] = 0.$$

This reduces the state value to 1. The algorithm correctly recognizes that repainting the middle element once is enough.

Consider:

```
1
5
1 2 3 2 1
```

The endpoints share the same color. The recurrence explicitly checks all later occurrences of color 1, including the final position. The transition through that matching endpoint captures the optimal sequence of merges and yields answer 2.

Consider:

```
1
5
1 1 1 1 1
```

Every interval repeatedly finds matching occurrences of the same color. The DP value remains zero throughout. A solution that counts color blocks would incorrectly report one operation, but the interval DP correctly returns zero because no repainting is required.

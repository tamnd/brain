---
title: "CF 1533F - Binary String Partition"
description: "We are given a binary string. For a fixed value of $k$, a substring is considered valid if at least one of the two character counts is small: either it contains at most $k$ zeroes or at most $k$ ones."
date: "2026-06-10T16:23:48+07:00"
tags: ["codeforces", "competitive-programming", "*special", "binary-search", "greedy"]
categories: ["algorithms"]
codeforces_contest: 1533
codeforces_index: "F"
codeforces_contest_name: "Kotlin Heroes: Episode 7"
rating: 0
weight: 1533
solve_time_s: 243
verified: true
draft: false
---

[CF 1533F - Binary String Partition](https://codeforces.com/problemset/problem/1533/F)

**Rating:** -  
**Tags:** *special, binary search, greedy  
**Solve time:** 4m 3s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a binary string. For a fixed value of $k$, a substring is considered valid if at least one of the two character counts is small: either it contains at most $k$ zeroes or at most $k$ ones.

The task is to split the original string into the minimum number of contiguous valid pieces. We must compute that minimum for every $k$ from $1$ to $n$, where $n$ is the length of the string.

The length can reach $2 \cdot 10^5$. Any solution that processes every $k$ independently in $O(n)$ time already costs $O(n^2)$, which is far beyond the limit. The total work must stay close to $O(n \log n)$.

A subtle point is that validity is not based on length. A long segment can still be valid if one character is rare enough. For example, with $k=1$, the segment `0000001` is valid because it contains only one `1`.

Another easy mistake is to cut as soon as one count exceeds $k$. The segment becomes invalid only when both counts exceed $k$. For $k=2$, the string `00011` is still valid because it has only two ones.

A third trap appears when computing the maximum valid extension. Suppose $k=1$ and the current segment starts at the beginning of `00100010`. The longest valid prefix is not determined by the first symbol that exceeds the limit. One character type may already exceed $k$, while the other still remains within the limit, allowing the segment to continue.

## Approaches

A brute force solution fixes a value of $k$, computes all valid segment boundaries, and runs dynamic programming or greedy partitioning. Even if we manage this in $O(n)$ time for one $k$, repeating it for all $n$ values gives $O(n^2)$, roughly $4 \cdot 10^{10}$ operations in the worst case.

The key observation is that for a fixed starting position $i$, the longest valid segment can be described using occurrence positions of zeroes and ones.

Let:

- $p_0$ be the position of the $(k+1)$-st zero occurring at or after $i$.
- $p_1$ be the position of the $(k+1)$-st one occurring at or after $i$.

A segment remains valid as long as at least one count is still at most $k$.

If we stop before $p_0$, then the segment contains at most $k$ zeroes.

If we stop before $p_1$, then the segment contains at most $k$ ones.

So the longest valid segment ends immediately before both conditions fail. Its next starting position is

$$\text{next}(i)=\max(p_0,p_1).$$

Once this jump function is known, the optimal partition is greedy: always take the longest valid segment. Any shorter first segment can only reduce future options.

The remaining challenge is computing answers for all $k$.

For small $k$, there are only about $\sqrt n$ different values. We can explicitly build the jump function for every position and compute answers with dynamic programming.

For large $k$, each segment is long, so the answer contains few segments. We can simulate the greedy process directly. The total cost over all large $k$ becomes a harmonic series.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n^2)$ | $O(n)$ | Too slow |
| Optimal | $O(n\sqrt n + n\log n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

1. Store the positions of all zeroes and all ones.
2. For every index $i$, compute:

- how many zeroes appear before $i$,
- how many ones appear before $i$.

These ranks let us jump directly to the $(k+1)$-st occurrence of either character after $i$.
3. Choose a threshold $B \approx \sqrt n$.
4. For every $k \le B$:

Compute

$$\text{next}[i] = \max( \text{pos0}[r_0(i)+k], \text{pos1}[r_1(i)+k] ),$$

where nonexistent occurrences are treated as position $n+1$.
5. For the same $k$, compute

$$dp[i]=1+dp[\text{next}[i]]$$

from right to left.

Here $dp[i]$ is the minimum number of segments needed to cover the suffix starting at $i$.
6. Store $dp[1]$ as the answer for this $k$.
7. For every $k>B$, simulate the greedy partition directly.

Start at position $1$.

Repeatedly jump to

$$\max( \text{pos0}[r_0(i)+k], \text{pos1}[r_1(i)+k] )$$

until the position becomes $n+1$.
8. Count how many jumps were performed. That count is the answer for this $k$.

### Why it works

For a segment beginning at $i$, the only way it becomes invalid is when it contains more than $k$ zeroes and more than $k$ ones simultaneously.

The first moment when the zero count exceeds $k$ is the $(k+1)$-st zero after $i$. The first moment when the one count exceeds $k$ is the $(k+1)$-st one after $i$.

Before reaching both positions, at least one character count is still within the limit. After reaching the larger of the two positions, both limits have been exceeded. This uniquely determines the longest valid segment.

Taking the longest valid segment greedily is optimal because every valid partition must end its first segment no later than this point. Extending the first segment as far as possible never increases the number of future pieces.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    s = input().strip()
    n = len(s)

    pos0 = [0]
    pos1 = [0]

    for i, c in enumerate(s, 1):
        if c == '0':
            pos0.append(i)
        else:
            pos1.append(i)

    zcnt = len(pos0) - 1
    ocnt = len(pos1) - 1

    pos0.extend([n + 1] * (n + 2))
    pos1.extend([n + 1] * (n + 2))

    r0 = [0] * (n + 2)
    r1 = [0] * (n + 2)

    z = o = 0
    for i in range(1, n + 1):
        r0[i] = z
        r1[i] = o
        if s[i - 1] == '0':
            z += 1
        else:
            o += 1

    r0[n + 1] = z
    r1[n + 1] = o

    B = int(n ** 0.5) + 1
    ans = [0] * (n + 1)

    nxt = [0] * (n + 2)
    dp = [0] * (n + 2)

    for k in range(1, min(B, n) + 1):
        for i in range(1, n + 1):
            p0 = pos0[r0[i] + k + 1]
            p1 = pos1[r1[i] + k + 1]
            nxt[i] = max(p0, p1)

        dp[n + 1] = 0
        for i in range(n, 0, -1):
            dp[i] = 1 + dp[nxt[i]]

        ans[k] = dp[1]

    for k in range(B + 1, n + 1):
        cur = 1
        cnt = 0

        while cur <= n:
            p0 = pos0[r0[cur] + k + 1]
            p1 = pos1[r1[cur] + k + 1]
            cur = max(p0, p1)
            cnt += 1

        ans[k] = cnt

    print(*ans[1:])

solve()
```

The arrays `r0` and `r1` store occurrence ranks. If position `i` is the start of a segment, then `r0[i] + k + 1` points to the first zero that would make the zero count exceed `k`. The same idea applies to ones.

For small values of `k`, we explicitly build the jump graph and compute the minimum number of segments using a one-dimensional DP. Since every jump moves strictly to the right, the DP is evaluated from right to left.

For large values of `k`, the answer is small. Simulating the greedy jumps becomes cheaper than building a full DP table.

The most common off-by-one mistake is the occurrence lookup. We need the $(k+1)$-st occurrence after the start position, which corresponds to `rank + k + 1`.

## Worked Examples

### Example 1

Input:

```
00100010
```

For $k=1$:

| Step | Current Start | Next Start |
| --- | --- | --- |
| 1 | 1 | 7 |
| 2 | 7 | 9 |

Answer = 2.

For $k=2$:

| Step | Current Start | Next Start |
| --- | --- | --- |
| 1 | 1 | 9 |

Answer = 1.

This shows how increasing $k$ enlarges each valid segment and reduces the number of required pieces.

### Example 2

Input:

```
1001011100
```

For $k=1$:

| Step | Current Start | Next Start |
| --- | --- | --- |
| 1 | 1 | 4 |
| 2 | 4 | 8 |
| 3 | 8 | 11 |

Answer = 3.

For $k=2$:

| Step | Current Start | Next Start |
| --- | --- | --- |
| 1 | 1 | 6 |
| 2 | 6 | 11 |

Answer = 2.

This example demonstrates that the greedy longest-segment rule automatically produces the optimal partition.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n\sqrt n + n\log n)$ | Small $k$ handled by DP, large $k$ handled by harmonic-series simulation |
| Space | $O(n)$ | Position arrays, ranks, DP, and jump arrays |

With $n \le 2 \cdot 10^5$, this comfortably fits within the limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    s = input().strip()
    n = len(s)

    pos0 = [0]
    pos1 = [0]

    for i, c in enumerate(s, 1):
        if c == '0':
            pos0.append(i)
        else:
            pos1.append(i)

    pos0.extend([n + 1] * (n + 2))
    pos1.extend([n + 1] * (n + 2))

    r0 = [0] * (n + 2)
    r1 = [0] * (n + 2)

    z = o = 0
    for i in range(1, n + 1):
        r0[i] = z
        r1[i] = o
        if s[i - 1] == '0':
            z += 1
        else:
            o += 1

    B = int(n ** 0.5) + 1
    ans = [0] * (n + 1)

    nxt = [0] * (n + 2)
    dp = [0] * (n + 2)

    for k in range(1, min(B, n) + 1):
        for i in range(1, n + 1):
            p0 = pos0[r0[i] + k + 1]
            p1 = pos1[r1[i] + k + 1]
            nxt[i] = max(p0, p1)

        dp[n + 1] = 0
        for i in range(n, 0, -1):
            dp[i] = 1 + dp[nxt[i]]

        ans[k] = dp[1]

    for k in range(B + 1, n + 1):
        cur = 1
        cnt = 0
        while cur <= n:
            p0 = pos0[r0[cur] + k + 1]
            p1 = pos1[r1[cur] + k + 1]
            cur = max(p0, p1)
            cnt += 1
        ans[k] = cnt

    return " ".join(map(str, ans[1:]))

assert run("00100010\n") == "2 1 1 1 1 1 1 1"
assert run("1001011100\n") == "3 2 2 2 1 1 1 1 1 1"

assert run("0\n") == "1"
assert run("11111\n") == "1 1 1 1 1"
assert run("01\n") == "1 1"
assert run("0101\n") == "2 1 1 1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `0` | `1` | Minimum length |
| `11111` | `1 1 1 1 1` | All characters equal |
| `01` | `1 1` | Small boundary case |
| `0101` | `2 1 1 1` | Alternating pattern and off-by-one checks |

## Edge Cases

Consider `0101` with $k=1$. The whole string is not valid because it contains two zeroes and two ones. A careless implementation may incorrectly allow it. The algorithm finds the second zero and the second one, takes the larger position, and cuts before both counts exceed the limit. The answer becomes `2`.

Consider `11111`. Every substring contains zero zeroes, so every substring is valid regardless of $k$.

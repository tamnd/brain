---
title: "CF 104804C - \u041c\u043e\u0440\u044f\u043a\u0438"
description: "We are simulating a very simple earning process over a sequence of items called sailors. There are $n$ sailors available in total, and in each of $k$ rounds Igor takes exactly one sailor from what remains."
date: "2026-06-28T13:24:19+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104804
codeforces_index: "C"
codeforces_contest_name: "Central Russia Regional Contest, 2022, Qualification Contest"
rating: 0
weight: 104804
solve_time_s: 78
verified: true
draft: false
---

[CF 104804C - \u041c\u043e\u0440\u044f\u043a\u0438](https://codeforces.com/problemset/problem/104804/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 18s  
**Verified:** yes  

## Solution
## Problem Understanding

We are simulating a very simple earning process over a sequence of items called sailors. There are $n$ sailors available in total, and in each of $k$ rounds Igor takes exactly one sailor from what remains. Each sailor has a fixed value determined purely by its position in the global ordering of sailors: the first sailor is worth $m$ coins, the second is worth $m+1$, the third is worth $m+2$, and so on.

Because there is no interaction between sailors and no randomness, the only thing that matters is which indices among the first $n$ positions get selected during the first $k$ picks. Since Igor always takes one sailor per round and there is no restriction beyond availability, the process is equivalent to taking the first $\min(n, k)$ sailors in order.

The output is the total sum of values of all sailors taken during these rounds.

The constraints allow up to $10^5$ sailors and $10^5$ rounds. A solution that iterates over each sailor individually is already borderline acceptable, but anything involving nested loops or repeated recomputation would still be fine only if it is strictly linear overall. Any approach that attempts to simulate choices step by step without recognizing the arithmetic structure risks unnecessary overhead but still remains safe; the real simplification comes from recognizing that the picked values form a contiguous arithmetic progression.

A subtle edge case appears when $k = 0$. In that case, no sailors are taken and the answer must be zero. Another edge case is when $k > n$, where only $n$ sailors exist, so the process effectively stops early and only $n$ terms contribute. A naive implementation that always sums $k$ terms would incorrectly assume nonexistent sailors exist.

## Approaches

If we simulate the process directly, we take sailors one by one and accumulate their values. The value of the $i$-th taken sailor is $m + i - 1$, and we stop either after $k$ steps or after exhausting $n$ sailors. This direct method performs a constant amount of work per taken sailor, so it runs in $O(\min(n, k))$, which is already fast enough for the limits.

However, the structure is not arbitrary, it is a consecutive arithmetic progression starting at $m$ with difference $1$. Instead of iterating, we can compute the sum in closed form. If $t = \min(n, k)$, then the sequence is:

$$m, m+1, m+2, \dots, m+t-1$$

This is a standard arithmetic series whose sum can be computed as:

$$t \cdot m + \frac{t(t-1)}{2}$$

The key improvement is replacing iteration with direct evaluation of this formula, reducing the computation to constant time.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(min(n, k)) | O(1) | Accepted |
| Arithmetic Formula | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read integers $n$, $k$, and $m$. These define how many sailors exist, how many are taken, and the starting value of the first sailor.
2. Determine how many sailors are actually taken: set $t = \min(n, k)$. This is necessary because we cannot take more sailors than exist.
3. Compute the sum of the arithmetic progression starting at $m$ with length $t$. Instead of iterating, use the identity that the sum equals $t \cdot m + \frac{t(t-1)}{2}$.
4. Output the computed sum.

### Why it works

At every step $i$, the value added is exactly $m + i$, with consistent increment of 1 between consecutive sailors. This guarantees that the taken values form a perfect arithmetic progression without gaps or reordering. Since we take exactly the first $t$ sailors in order, no permutation or selection effect alters the sequence. The sum formula for arithmetic progressions therefore exactly matches the accumulated result of any valid execution of the process.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, k, m = map(int, input().split())
    
    t = min(n, k)
    
    # sum of m + (m+1) + ... + (m+t-1)
    # = t*m + (0 + 1 + ... + t-1)
    # = t*m + t*(t-1)//2
    ans = t * m + t * (t - 1) // 2
    
    print(ans)

if __name__ == "__main__":
    solve()
```

The code first reads the input values and immediately reduces the problem size to $t = \min(n, k)$, ensuring we only consider valid picks. It then applies the arithmetic series formula directly. The subtraction-free formulation avoids any floating-point operations and relies entirely on integer arithmetic, which is safe under Python’s unbounded integers.

A common pitfall is forgetting to clamp $k$ by $n$, which would incorrectly assume sailors beyond $n$ exist. Another is implementing the sum with division instead of integer division, which could introduce floating errors in other languages.

## Worked Examples

### Sample 1

Input: $n = 12$, $k = 18$, $m = 2$

Since only 12 sailors exist, $t = \min(12, 18) = 12$.

| i | Value added |
| --- | --- |
| 1 | 2 |
| 2 | 3 |
| 3 | 4 |
| ... | ... |
| 12 | 13 |

Sum = $2 + 3 + \dots + 13 = 90$

This confirms that even though $k$ is larger than $n$, only available sailors contribute.

### Sample 2

Input: $n = 5$, $k = 4$, $m = 10$

Here $t = 4$, since we take fewer sailors than available.

| i | Value added |
| --- | --- |
| 1 | 10 |
| 2 | 11 |
| 3 | 12 |
| 4 | 13 |

Sum = $10 + 11 + 12 + 13 = 46$

This shows the straightforward arithmetic progression over the first $k$ elements.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only constant-time arithmetic after reading input |
| Space | O(1) | No auxiliary structures are used |

The computation reduces the entire process to a single formula evaluation, which trivially satisfies the constraints even for the largest inputs.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    out = io.StringIO()
    sys.stdout = out
    solve()
    return out.getvalue().strip()

# provided samples
assert run("12 18 2\n") == "90", "sample 1"
assert run("5 4 10\n") == "46", "sample 2"
assert run("75 40 96\n") == "4620", "sample 3"

# custom cases
assert run("1 0 100\n") == "0", "no rounds"
assert run("1 10 1\n") == "1", "single sailor cap by n"
assert run("5 5 1\n") == "15", "small full range"
assert run("100000 100000 100000\n") == str(100000 * 100000 + 100000 * 99999 // 2), "max stress"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 0 100 | 0 | zero rounds edge case |
| 1 10 1 | 1 | k > n with single element |
| 5 5 1 | 15 | full exact progression |
| 100000 100000 100000 | large sum | performance and overflow safety |

## Edge Cases

For $k = 0$, the algorithm sets $t = 0$, which immediately produces sum $0$ because both terms in the formula vanish. For example, input $1\ 0\ 10$ leads to $t=0$, hence $0 \cdot 10 + 0 = 0$.

When $k > n$, the clamping step ensures we only sum existing sailors. For instance, $n=3, k=10, m=5$ yields $t=3$, producing $5+6+7=18$. Any naive loop over $k$ would attempt to access non-existent sailors and either crash or overcount.

When $n = 1$, the progression collapses to a single value regardless of $k$. For $n=1, k=100, m=42$, the result is always $42$, since $t=1$ and the formula reduces to $1 \cdot 42 + 0$.

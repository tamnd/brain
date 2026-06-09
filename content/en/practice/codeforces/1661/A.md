---
title: "CF 1661A - Array Balancing"
description: "At every position i, we have a pair of values (a[i], b[i]). The only operation allowed is swapping the two values inside the same pair. We may do this independently for any positions. After choosing which pairs to swap, we obtain final arrays a and b."
date: "2026-06-10T02:55:23+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "math"]
categories: ["algorithms"]
codeforces_contest: 1661
codeforces_index: "A"
codeforces_contest_name: "Educational Codeforces Round 126 (Rated for Div. 2)"
rating: 800
weight: 1661
solve_time_s: 125
verified: true
draft: false
---

[CF 1661A - Array Balancing](https://codeforces.com/problemset/problem/1661/A)

**Rating:** 800  
**Tags:** greedy, math  
**Solve time:** 2m 5s  
**Verified:** yes  

## Solution
## Problem Understanding

At every position `i`, we have a pair of values `(a[i], b[i])`. The only operation allowed is swapping the two values inside the same pair. We may do this independently for any positions.

After choosing which pairs to swap, we obtain final arrays `a` and `b`. The cost is the sum of absolute differences between adjacent elements in the first array plus the same quantity in the second array:

$$\sum_{i=1}^{n-1} \left(|a_i-a_{i+1}| + |b_i-b_{i+1}|\right)$$

The task is to minimize this cost.

The crucial observation is that a swap at position `i` affects only the pair `(a[i], b[i])`. It never changes values at other indices. Since the objective only contains adjacent pairs of indices, the contribution of positions `i` and `i+1` can be analyzed independently from the rest of the array.

The constraints are surprisingly small. The length of each array is at most 25, although there may be up to 4000 test cases. A brute-force search over all swap configurations would still be impossible because each position has two choices, producing `2^n` configurations. For `n = 25`, that is over 33 million possibilities per test case.

A common mistake is to think that decisions at different positions interact globally and require dynamic programming. They do interact, but the interaction is extremely local. Once we understand the structure of the cost function, each adjacent pair can be optimized independently.

Consider:

```
a = [1, 10]
b = [10, 1]
```

Without swaps, the cost is

$$|1-10|+|10-1|=18.$$

Swapping one position gives

```
a = [1,1]
b = [10,10]
```

with cost `0`.

A greedy rule such as "swap whenever `a[i] > b[i]`" would fail on many examples because the objective depends on neighboring positions, not on the individual pair itself.

Another subtle case occurs when values are already ordered:

```
a = [1,2,3]
b = [6,7,8]
```

Any swap only mixes small numbers with large numbers and increases adjacent differences. The optimal answer is obtained by doing nothing. An algorithm that always normalizes pairs without checking the actual contribution could produce a larger cost.

## Approaches

The most direct solution is to try every swap configuration. Each position may be left unchanged or swapped, giving `2^n` possibilities. For each configuration we can compute the resulting cost in `O(n)` time.

The brute-force method is correct because it explicitly checks every possible final state. The problem is the size of the search space. For `n = 25`, we would need roughly

$$2^{25} \approx 3.3 \times 10^7$$

configurations for a single test case, which is far beyond what the time limit allows.

To find something better, look at one term of the objective:

$$|a_i-a_{i+1}| + |b_i-b_{i+1}|.$$

Only positions `i` and `i+1` appear in this expression. Let the pair at position `i` be `(x,y)` and the pair at position `i+1` be `(u,v)`.

For these two positions, we may choose either orientation:

```
(x,y) or (y,x)
(u,v) or (v,u)
```

Suppose we always reorder each pair so that the smaller value is first:

$$l_i = \min(a_i,b_i), \qquad r_i = \max(a_i,b_i).$$

Now consider the contribution of adjacent positions:

$$|l_i-l_{i+1}| + |r_i-r_{i+1}|.$$

Could some other orientation be better?

For two pairs, the only possibilities are:

$$|x-u|+|y-v|$$

or

$$|x-v|+|y-u|.$$

A standard inequality on the line states that matching smaller values together and larger values together is never worse than crossing the connections:

$$|x-u|+|y-v|
\le
|x-v|+|y-u|$$

whenever $x \le y$ and $u \le v$.

After sorting each pair internally, every adjacent contribution is minimized independently. Since the total objective is simply the sum of all adjacent contributions, sorting every pair once is globally optimal.

The solution becomes extremely simple: replace every pair by `(min, max)`, then compute the final cost.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n·2^n) | O(n) | Too slow |
| Optimal | O(n) per test case | O(1) extra | Accepted |

## Algorithm Walkthrough

1. For every position `i`, replace the pair `(a[i], b[i])` with `(min(a[i], b[i]), max(a[i], b[i]))`.

This fixes the orientation that minimizes all future adjacent contributions involving this position.
2. Initialize the answer to `0`.
3. For every adjacent pair of indices `i` and `i+1`, add

$$|a_i-a_{i+1}| + |b_i-b_{i+1}|$$

to the answer.

After step 1, these arrays already represent the optimal orientation of every pair.
4. Output the accumulated sum.

### Why it works

For any adjacent indices, let

$$x=\min(a_i,b_i), \quad y=\max(a_i,b_i),$$

and

$$u=\min(a_{i+1},b_{i+1}), \quad v=\max(a_{i+1},b_{i+1}).$$

The contribution of these two positions is either

$$|x-u|+|y-v|$$

or

$$|x-v|+|y-u|.$$

Since $x \le y$ and $u \le v$, pairing the smaller values together and the larger values together is never larger than the crossed pairing. Thus the sorted orientation minimizes the contribution of this adjacent pair.

The total objective is a sum of such adjacent contributions. Each term is minimized by the same local choice, namely placing the smaller element of every pair into the first array and the larger element into the second array. Since every term is simultaneously minimized, the whole sum is minimized.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())

    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        b = list(map(int, input().split()))

        for i in range(n):
            if a[i] > b[i]:
                a[i], b[i] = b[i], a[i]

        ans = 0
        for i in range(n - 1):
            ans += abs(a[i] - a[i + 1])
            ans += abs(b[i] - b[i + 1])

        print(ans)

solve()
```

The first loop normalizes every pair so that `a[i] <= b[i]`. This is the key greedy step. After that transformation, every adjacent contribution is already in its optimal form.

The second loop computes the objective exactly as defined. Since the answer can be larger than 32-bit integer limits, using Python integers avoids overflow concerns automatically.

A common implementation mistake is to compute the answer before performing all swaps. The proof relies on every pair being normalized first. Another mistake is forgetting that the contribution contains both arrays, not just one of them.

## Worked Examples

### Example 1

Input:

```
4
3 3 10 10
10 10 3 3
```

After normalization:

```
a = [3, 3, 3, 3]
b = [10, 10, 10, 10]
```

| i | a[i] | b[i] | Contribution |
| --- | --- | --- | --- |
| 0 | 3 | 10 | 0 |
| 1 | 3 | 10 | 0 |
| 2 | 3 | 10 | 0 |

Total answer = `0`.

This example shows how swapping inside pairs can completely separate small values from large values, eliminating all adjacent differences.

### Example 2

Input:

```
5
1 2 3 4 5
6 7 8 9 10
```

Normalization changes nothing.

| i | Term from a | Term from b | Running Total |
| --- | --- | --- | --- |
| 0 | 1 | 1 | 2 |
| 1 | 1 | 1 | 4 |
| 2 | 1 | 1 | 6 |
| 3 | 1 | 1 | 8 |

Final answer = `8`.

This example demonstrates that the optimal strategy is not necessarily to perform swaps. When each pair is already ordered, the arrays remain unchanged.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | One pass to normalize pairs and one pass to compute the answer |
| Space | O(1) extra | Only a few variables besides the input arrays |

With `n ≤ 25`, the running time is tiny. Even with 4000 test cases, the solution performs only a few hundred thousand operations, comfortably within the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    def input():
        return sys.stdin.readline()

    t = int(input())
    out = []

    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        b = list(map(int, input().split()))

        for i in range(n):
            if a[i] > b[i]:
                a[i], b[i] = b[i], a[i]

        ans = 0
        for i in range(n - 1):
            ans += abs(a[i] - a[i + 1])
            ans += abs(b[i] - b[i + 1])

        out.append(str(ans))

    return "\n".join(out) + "\n"

# provided samples
assert run(
"""3
4
3 3 10 10
10 10 3 3
5
1 2 3 4 5
6 7 8 9 10
6
72 101 108 108 111 44
10 87 111 114 108 100
"""
) == "0\n8\n218\n"

# minimum size
assert run(
"""1
2
1 10
10 1
"""
) == "0\n"

# all equal values
assert run(
"""1
5
7 7 7 7 7
7 7 7 7 7
"""
) == "0\n"

# already ordered
assert run(
"""1
3
1 2 3
4 5 6
"""
) == "4\n"

# alternating pairs requiring swaps
assert run(
"""1
3
10 1 10
1 10 1
"""
) == "0\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `n=2`, crossed pair | `0` | Smallest valid size |
| All values equal | `0` | Zero-difference handling |
| Already ordered arrays | `4` | Swaps are not forced |
| Alternating large/small pairs | `0` | Greedy normalization is necessary |

## Edge Cases

Consider the smallest possible input:

```
1
2
1 10
10 1
```

After normalization:

```
a = [1,1]
b = [10,10]
```

The only adjacent contribution is

$$|1-1|+|10-10|=0.$$

The algorithm outputs `0`, which is optimal.

Consider an input where every value is identical:

```
1
4
5 5 5 5
5 5 5 5
```

Normalization changes nothing. Every adjacent difference is zero, so the answer is `0`. The algorithm correctly avoids introducing any artificial cost.

Consider a case where no swap helps:

```
1
3
1 2 3
6 7 8
```

All pairs already satisfy `a[i] <= b[i]`. The computed answer is

$$(1+1)+(1+1)=4.$$

Any swap would mix small and large values and increase at least one adjacent contribution. The algorithm leaves the arrays unchanged and returns the optimum.

Consider a highly alternating input:

```
1
3
10 1 10
1 10 1
```

Normalization produces

```
a = [1,1,1]
b = [10,10,10]
```

Every adjacent contribution becomes zero. This confirms the key invariant: placing the smaller element of each pair into the first array and the larger element into the second array simultaneously minimizes every adjacent term of the objective.

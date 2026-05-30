---
title: "CF 459B - Pashmak and Flowers"
description: "We are given the beauty values of n flowers. We must choose exactly two flowers. Among all possible pairs, we are interested only in pairs whose beauty difference is as large as possible."
date: "2026-05-30T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "combinatorics", "implementation", "sortings"]
categories: ["algorithms"]
codeforces_contest: 459
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 261 (Div. 2)"
rating: 1300
weight: 459
solve_time_s: 91
verified: true
draft: false
---

[CF 459B - Pashmak and Flowers](https://codeforces.com/problemset/problem/459/B)

**Rating:** 1300  
**Tags:** combinatorics, implementation, sortings  
**Solve time:** 1m 31s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given the beauty values of `n` flowers. We must choose exactly two flowers.

Among all possible pairs, we are interested only in pairs whose beauty difference is as large as possible. The task is to output two values:

First, the maximum possible difference between the beauties of two chosen flowers.

Second, the number of distinct flower pairs that achieve this maximum difference. Flowers are distinguished by their positions, so two flowers with the same beauty are still different choices if they come from different indices.

The constraints are large. There can be up to `2 * 10^5` flowers, and beauty values can be as large as `10^9`. A quadratic algorithm that examines every pair would require roughly

$$\frac{n(n-1)}{2}$$

comparisons. For `n = 200000`, that is about 20 billion pairs, which is completely infeasible within one second.

The beauty values themselves are large, but we only need comparisons and counting. No dynamic programming or complex data structures are necessary.

A subtle edge case appears when all flowers have the same beauty.

Input:

```
5
7 7 7 7 7
```

Every pair has difference `0`, which is automatically the maximum difference. The answer is:

```
0 10
```

because there are

$$\binom{5}{2}=10$$

different pairs. A careless solution that only counts minimum-beauty flowers multiplied by maximum-beauty flowers would incorrectly produce `25`.

Another important case is when the minimum and maximum values occur multiple times.

Input:

```
5
1 3 1 5 5
```

The maximum difference is `5 - 1 = 4`.

There are two flowers with beauty `1` and two flowers with beauty `5`, so the number of optimal pairs is:

$$2 \times 2 = 4$$

The correct output is:

```
4 4
```

A solution that only finds one minimum and one maximum occurrence would incorrectly return `1`.

A final corner case is the smallest possible input.

Input:

```
2
100 1
```

Only one pair exists, so the answer must be:

```
99 1
```

Regardless of the values, there is exactly one valid choice.

## Approaches

The most direct approach is to examine every pair of flowers. For each pair, compute the beauty difference, track the largest difference seen so far, and count how many pairs achieve it.

This brute-force method is correct because it explicitly checks every possible pair. The problem is its running time. With `n = 200000`, the number of pairs is roughly 20 billion, which is far beyond what can be processed within the limits.

The key observation is that the largest possible difference must come from the smallest beauty value and the largest beauty value.

Suppose the minimum beauty in the entire array is `mn` and the maximum beauty is `mx`.

No pair can have a difference larger than `mx - mn`, because every beauty lies between those two extremes. At the same time, choosing one flower with beauty `mn` and another with beauty `mx` achieves exactly that difference.

This immediately gives the maximum difference:

$$mx - mn$$

The remaining question is how many pairs achieve it.

If `mn != mx`, every optimal pair must contain one minimum-valued flower and one maximum-valued flower. Any other beauty value would reduce the difference.

If the minimum value appears `cnt_min` times and the maximum value appears `cnt_max` times, then every minimum flower can be paired with every maximum flower:

$$cnt\_min \times cnt\_max$$

optimal pairs.

If `mn == mx`, then all flowers have identical beauty. Every pair achieves difference `0`, so we must count all unordered pairs:

$$\binom{n}{2}
=
\frac{n(n-1)}{2}$$

This reduces the problem to finding the minimum value, maximum value, and their frequencies.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(1) | Too slow |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the number of flowers and their beauty values.
2. Find the minimum beauty value `mn`.
3. Find the maximum beauty value `mx`.
4. Compute the maximum difference as `mx - mn`.
5. If `mn == mx`, all flowers have identical beauty.

The maximum difference is `0`, and every unordered pair is optimal. Compute:

$$\frac{n(n-1)}{2}$$
6. Otherwise, count how many flowers have beauty `mn`. Call this `cnt_min`.
7. Count how many flowers have beauty `mx`. Call this `cnt_max`.
8. The number of optimal pairs is:

$$cnt\_min \times cnt\_max$$
9. Output the maximum difference and the number of optimal pairs.

### Why it works

The largest beauty difference obtainable from any pair cannot exceed the difference between the global maximum and global minimum values. Since choosing a minimum-valued flower and a maximum-valued flower achieves exactly that difference, the optimal difference is uniquely determined as `mx - mn`.

When `mn != mx`, every optimal pair must use one flower from each extreme. Replacing either flower with any intermediate beauty decreases the difference. Thus the total number of optimal pairs is exactly the number of ways to choose a minimum flower and a maximum flower.

When `mn == mx`, every flower has the same beauty, so every pair yields difference `0`. Counting all unordered pairs gives the correct answer.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))

    mn = min(a)
    mx = max(a)

    diff = mx - mn

    if mn == mx:
        ways = n * (n - 1) // 2
    else:
        cnt_min = a.count(mn)
        cnt_max = a.count(mx)
        ways = cnt_min * cnt_max

    print(diff, ways)

solve()
```

The first step is finding the smallest and largest beauty values. These two values completely determine the maximum achievable difference.

After computing the difference, the implementation splits into two cases.

If the minimum and maximum values are equal, every flower has identical beauty. The number of optimal pairs is the number of unordered pairs among `n` flowers, computed with the combinatorial formula `n * (n - 1) // 2`.

Otherwise, the only optimal pairs are those formed by one minimum-valued flower and one maximum-valued flower. The code counts the occurrences of both values and multiplies the counts.

One detail that is easy to overlook is the size of the answer. With `n = 200000`, the number of pairs can reach nearly 20 billion. Languages with fixed-size 32-bit integers would overflow. Python integers grow automatically, so no special handling is required.

## Worked Examples

### Example 1

Input:

```
2
1 2
```

| Step | mn | mx | diff | cnt_min | cnt_max | ways |
| --- | --- | --- | --- | --- | --- | --- |
| After scan | 1 | 2 | 1 | - | - | - |
| Count frequencies | 1 | 2 | 1 | 1 | 1 | 1 |

Output:

```
1 1
```

There is only one pair of flowers. Its difference is `1`, which is automatically the maximum possible difference.

### Example 2

Input:

```
5
1 3 1 5 5
```

| Step | mn | mx | diff | cnt_min | cnt_max | ways |
| --- | --- | --- | --- | --- | --- | --- |
| After scan | 1 | 5 | 4 | - | - | - |
| Count frequencies | 1 | 5 | 4 | 2 | 2 | 4 |

Output:

```
4 4
```

There are two flowers with beauty `1` and two flowers with beauty `5`. Every minimum flower can pair with every maximum flower, producing `2 × 2 = 4` optimal pairs.

This example demonstrates that counting occurrences is essential. Looking only at distinct values would miss multiple valid pairs.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Finding min, max, and frequencies requires linear scans |
| Space | O(1) | Only a few variables are used beyond the input array |

The algorithm processes the array a constant number of times. Even for `200000` flowers, the total work is tiny compared to the time limit. Memory usage is also comfortably within the limit.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve():
    n = int(input())
    a = list(map(int, input().split()))

    mn = min(a)
    mx = max(a)

    if mn == mx:
        ways = n * (n - 1) // 2
    else:
        ways = a.count(mn) * a.count(mx)

    print(mx - mn, ways)

def run(inp: str) -> str:
    backup_stdin = sys.stdin
    backup_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    global input
    input = sys.stdin.readline

    solve()

    out = sys.stdout.getvalue().strip()

    sys.stdin = backup_stdin
    sys.stdout = backup_stdout

    return out

# provided sample
assert run("2\n1 2\n") == "1 1", "sample 1"

# minimum size
assert run("2\n100 1\n") == "99 1", "minimum n"

# all equal
assert run("5\n7 7 7 7 7\n") == "0 10", "all pairs optimal"

# repeated minima and maxima
assert run("5\n1 3 1 5 5\n") == "4 4", "multiple optimal pairs"

# many middle values
assert run("6\n1 2 3 4 5 6\n") == "5 1", "single min and max"

# boundary counting
assert run("6\n1 1 1 10 10 10\n") == "9 9", "3 * 3 optimal pairs"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2 / 100 1` | `99 1` | Smallest allowed input |
| `5 / 7 7 7 7 7` | `0 10` | All values equal |
| `5 / 1 3 1 5 5` | `4 4` | Multiple minima and maxima |
| `6 / 1 2 3 4 5 6` | `5 1` | Unique minimum and maximum |
| `6 / 1 1 1 10 10 10` | `9 9` | Frequency multiplication logic |

## Edge Cases

Consider the case where all flowers have the same beauty:

```
5
7 7 7 7 7
```

The algorithm finds `mn = mx = 7`, so it enters the special branch. The difference is `0`, and the number of optimal pairs becomes:

$$\frac{5 \cdot 4}{2} = 10$$

Output:

```
0 10
```

This avoids the common mistake of computing `5 × 5 = 25`, which counts invalid self-pairings and double-counts pairs.

Consider a case with repeated extremes:

```
5
1 3 1 5 5
```

The algorithm finds `mn = 1`, `mx = 5`, `cnt_min = 2`, and `cnt_max = 2`.

The number of optimal pairs is:

$$2 \times 2 = 4$$

Output:

```
4 4
```

Every optimal pair contains one flower with beauty `1` and one flower with beauty `5`. No pair involving the flower with beauty `3` can reach the maximum difference.

Consider the smallest valid input:

```
2
100 1
```

The algorithm computes `mn = 1`, `mx = 100`, and counts one occurrence of each. The answer becomes:

```
99 1
```

Only one pair exists, and the counting formula naturally produces the correct result.

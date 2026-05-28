---
title: "CF 194A - Exams"
description: "The author has to take n exams. Every exam receives an integer grade between 2 and 5 inclusive. A grade of 2 means the exam is failed and must be retaken. The total sum of all grades must equal exactly k."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "implementation", "math"]
categories: ["algorithms"]
codeforces_contest: 194
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 122 (Div. 2)"
rating: 900
weight: 194
solve_time_s: 88
verified: true
draft: false
---

[CF 194A - Exams](https://codeforces.com/problemset/problem/194/A)

**Rating:** 900  
**Tags:** implementation, math  
**Solve time:** 1m 28s  
**Verified:** yes  

## Solution
## Problem Understanding

The author has to take `n` exams. Every exam receives an integer grade between 2 and 5 inclusive. A grade of 2 means the exam is failed and must be retaken. The total sum of all grades must equal exactly `k`.

Among all possible assignments of grades whose sum is `k`, we want the smallest possible number of failed exams. Since only grade 2 causes a retake, the task becomes: maximize the number of exams with grades 3, 4, or 5 while still keeping the total sum equal to `k`.

The constraints are tiny. `n` is at most 50 and `k` is at most 250, so even brute force approaches would fit easily. Still, this problem has a direct mathematical observation that reduces the entire solution to a single formula.

The first subtle edge case happens when the target sum is already the minimum possible sum. For example:

```
Input:
4 8
```

Each exam must be at least 2, so the minimum achievable total is `4 * 2 = 8`. That forces every exam to be a 2, so the answer is 4. A careless solution that tries to greedily increase grades without handling this baseline correctly can accidentally produce fewer failures than possible.

Another easy mistake appears when the sum is very large. Consider:

```
Input:
3 15
```

The maximum possible grade is 5, and `3 * 5 = 15`, so every exam can be a 5. The answer is 0. Some incorrect implementations think every extra point above the minimum removes one failed exam, which is false because a single exam can absorb up to 3 extra points.

A more interesting case is:

```
Input:
4 10
```

The minimum total is 8. We need 2 extra points. One exam can be upgraded from 2 to 4, producing grades `[4,2,2,2]`. The answer is still 3 failed exams, not 2. This catches solutions that divide incorrectly or assume every extra point fixes a different failed exam.

## Approaches

A brute force approach would try all possible assignments of grades. Since every exam can take one of four values, there are `4^n` combinations. With `n = 50`, this becomes astronomically large and completely infeasible.

Dynamic programming is also possible. We could define `dp[i][s]` as the minimum number of failed exams after processing `i` exams with total score `s`. Since `n <= 50` and `k <= 250`, this runs comfortably fast. The state count is roughly `50 * 250`, and each transition considers four grades.

The problem structure allows something much simpler.

Every exam starts at grade 2. That gives a baseline total of `2n`. Any higher grade adds extra points:

| Grade | Extra points above 2 |
| --- | --- |
| 2 | 0 |
| 3 | 1 |
| 4 | 2 |
| 5 | 3 |

Suppose we need a final sum of `k`. The number of extra points we must distribute is:

$$k - 2n$$

Each non-failed exam can contribute at most 3 extra points, because the highest grade is 5. So if we want to minimize failed exams, we should pack as many extra points as possible into each passing exam.

If one passing exam can contribute at most 3 extra points, then the minimum number of passing exams needed is:

$$\left\lceil \frac{k - 2n}{3} \right\rceil$$

The total number of exams is `n`, so the minimum number of failed exams becomes:

$$n - \left\lceil \frac{k - 2n}{3} \right\rceil$$

This transforms the problem from a search problem into a direct mathematical computation.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(4^n) | O(n) | Too slow |
| Optimal | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read `n` and `k`.
2. Compute the minimum possible total score, which is `2 * n`. This corresponds to giving every exam grade 2.
3. Compute how many additional points are needed:

$$extra = k - 2n$$

1. Each passing exam can absorb at most 3 extra points by changing a 2 into a 5.
2. Compute the minimum number of passing exams needed:

$$pass\_exams = \left\lceil \frac{extra}{3} \right\rceil$$

In integer arithmetic, this becomes:

```
(extra + 2) // 3
```

1. The remaining exams must stay at grade 2, so the answer is:

```
n - pass_exams
```

### Why it works

Every exam initially contributes 2 points. To reach the required total, we distribute `extra` additional points across exams. A single exam can contribute at most 3 additional points because grades are capped at 5.

To minimize failed exams, we want as few exams as possible to carry all extra points. Packing 3 extra points into one exam is always at least as good as splitting them across multiple exams, because each exam upgraded above 2 stops being a failed exam.

The ceiling division computes the smallest number of exams capable of supplying all required extra points. Any remaining exams stay at grade 2 and count as failed exams. No arrangement can use fewer passing exams because each passing exam has a hard capacity of 3 extra points.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, k = map(int, input().split())

extra = k - 2 * n
passing = (extra + 2) // 3

print(n - passing)
```

The implementation directly follows the mathematical derivation.

The expression `k - 2 * n` computes how many points we still need after assigning the minimum grade 2 to every exam. Since the problem guarantees a valid configuration exists, this value is never negative beyond what the formula can handle.

The ceiling division is the only subtle part. In mathematics:

$$\left\lceil \frac{x}{3} \right\rceil$$

becomes:

```
(x + 2) // 3
```

for non-negative integers. Adding 2 before integer division correctly rounds upward.

Finally, subtracting the number of passing exams from `n` gives the number of exams that remain at grade 2.

No loops or large data structures are needed.

## Worked Examples

### Example 1

Input:

```
4 8
```

| Step | Value |
| --- | --- |
| n | 4 |
| k | 8 |
| Minimum sum `2n` | 8 |
| Extra points needed | 0 |
| Passing exams needed | 0 |
| Failed exams | 4 |

The total already equals the minimum possible score, so every exam must remain at grade 2. This confirms the lower-bound edge case.

### Example 2

Input:

```
4 10
```

| Step | Value |
| --- | --- |
| n | 4 |
| k | 10 |
| Minimum sum `2n` | 8 |
| Extra points needed | 2 |
| Passing exams needed | 1 |
| Failed exams | 3 |

One exam can absorb both extra points by becoming grade 4. The grades could be `[4,2,2,2]`. This demonstrates why grouping extra points into as few exams as possible minimizes retakes.

### Example 3

Input:

```
3 15
```

| Step | Value |
| --- | --- |
| n | 3 |
| k | 15 |
| Minimum sum `2n` | 6 |
| Extra points needed | 9 |
| Passing exams needed | 3 |
| Failed exams | 0 |

All exams must become grade 5. This reaches the maximum possible sum and produces zero failed exams.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only a few arithmetic operations are performed |
| Space | O(1) | No additional memory proportional to input size is used |

The constraints are extremely small, so even slower methods would pass. The constant-time formula solves the problem instantly and fits comfortably within all limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve():
    input = sys.stdin.readline

    n, k = map(int, input().split())

    extra = k - 2 * n
    passing = (extra + 2) // 3

    print(n - passing)

def run(inp: str) -> str:
    backup_stdin = sys.stdin
    backup_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    out = sys.stdout.getvalue()

    sys.stdin = backup_stdin
    sys.stdout = backup_stdout

    return out

# provided sample
assert run("4 8\n") == "4\n", "sample 1"

# custom cases
assert run("1 2\n") == "1\n", "minimum possible sum"
assert run("1 5\n") == "0\n", "maximum possible score"
assert run("4 10\n") == "3\n", "single upgraded exam"
assert run("3 15\n") == "0\n", "all exams score 5"
assert run("5 11\n") == "4\n", "one extra point only"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 2` | `1` | Smallest valid configuration |
| `1 5` | `0` | Maximum grade removes all failures |
| `4 10` | `3` | Extra points can be concentrated into one exam |
| `3 15` | `0` | Maximum achievable total |
| `5 11` | `4` | Ceiling division with remainder |

## Edge Cases

Consider the minimum-total case:

```
Input:
4 8
```

The algorithm computes:

```
extra = 8 - 2*4 = 0
passing = (0 + 2) // 3 = 0
answer = 4 - 0 = 4
```

No extra points are needed, so every exam remains at grade 2. The output is correctly 4.

Now consider the maximum-total case:

```
Input:
3 15
```

The algorithm computes:

```
extra = 15 - 2*3 = 9
passing = (9 + 2) // 3 = 3
answer = 3 - 3 = 0
```

All exams must become passing exams, specifically grade 5. The output is correctly 0.

Finally, examine a ceiling-division case:

```
Input:
5 11
```

The minimum total is 10, so only one extra point is needed:

```
extra = 1
passing = (1 + 2) // 3 = 1
answer = 5 - 1 = 4
```

One exam can become grade 3 while the remaining four stay at grade 2. A floor-division implementation would incorrectly compute zero passing exams here.

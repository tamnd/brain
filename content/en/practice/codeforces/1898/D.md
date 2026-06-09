---
title: "CF 1898D - Absolute Beauty"
description: "For every position i, we have a pair of numbers (ai, bi). The current beauty is the sum of the distances between the paired values: $$sum We may choose at most one pair of indices and swap the corresponding values inside array b."
date: "2026-06-08T21:31:48+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "math"]
categories: ["algorithms"]
codeforces_contest: 1898
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 910 (Div. 2)"
rating: 1900
weight: 1898
solve_time_s: 133
verified: true
draft: false
---

[CF 1898D - Absolute Beauty](https://codeforces.com/problemset/problem/1898/D)

**Rating:** 1900  
**Tags:** greedy, math  
**Solve time:** 2m 13s  
**Verified:** yes  

## Solution
## Problem Understanding

For every position `i`, we have a pair of numbers `(a_i, b_i)`. The current beauty is the sum of the distances between the paired values:

$$\sum |a_i-b_i|$$

We may choose at most one pair of indices and swap the corresponding values inside array `b`. After that swap, every position still contributes an absolute difference with its own `a_i`, and we want the largest possible total beauty.

A useful way to think about the problem is that every index defines an interval between its two values. If `a_i = 3` and `b_i = 8`, the pair corresponds to the interval `[3,8]`. The contribution of that index is exactly the interval length.

The total length of all intervals is already known. The only thing a swap can change is the contribution of the two indices involved in that swap.

The constraints are the real challenge. The sum of all `n` across test cases is at most `2·10^5`, which means an `O(n log n)` or `O(n)` solution is expected. Any algorithm that tries all pairs of indices would require `O(n²)` work, roughly `2·10^10` operations in the worst case, which is far beyond what can run in two seconds.

Several edge cases are easy to mishandle.

Consider:

```
n = 2
a = [1, 2]
b = [2, 1]
```

The current beauty is `1 + 1 = 2`. Swapping the two elements of `b` produces `[1,2]`, whose beauty is `0`. The correct answer is `2`, because the operation is optional. Any solution that assumes a swap must be performed gives the wrong result.

Consider:

```
n = 2
a = [1, 2]
b = [1, 2]
```

The initial beauty is `0`. After swapping, the beauty becomes `2`. The answer is `2`. A solution that only checks whether intervals overlap would miss that a beneficial swap exists even though both original intervals have length zero.

Another subtle case is when intervals are already disjoint:

```
a = [1, 2]
b = [5, 6]
```

The beauty is `4 + 4 = 8`. Any swap leaves it unchanged. The answer remains `8`. A careless derivation may incorrectly assume that every pair of non-overlapping intervals allows a gain.

## Approaches

The brute-force idea is straightforward. Compute the current beauty. For every pair `(i,j)`, swap `b_i` and `b_j`, recompute the change in contribution of those two positions, and keep the best result.

This works because a swap affects only positions `i` and `j`. Instead of recomputing the whole sum, we can evaluate a pair in constant time. Even then, there are `O(n²)` candidate pairs. With `n = 2·10^5`, that means roughly twenty billion pairs, which is completely infeasible.

The key observation is that each position can be represented by the interval

$$[l_i,r_i]$$

where

$$l_i=\min(a_i,b_i),\qquad r_i=\max(a_i,b_i).$$

Let

$$S=\sum (r_i-l_i)$$

be the original beauty.

Suppose we swap values between positions `i` and `j`. The only thing that changes is the combined contribution of those two positions.

A very useful identity is:

$$|x-v|+|u-y|
-
(|x-y|+|u-v|)
=
2\cdot \max(0,\; \text{gap})$$

where the gap is the distance between the two intervals.

After working through the geometry of absolute values, the maximum gain obtainable from swapping two positions depends only on the intervals. If two intervals overlap, no swap can improve their total contribution. If they are disjoint, the best gain equals twice the distance between them.

For intervals

$$[l_i,r_i],\quad [l_j,r_j]$$

with `r_i < l_j`, the gain is

$$2(l_j-r_i).$$

So the entire problem becomes:

Find two intervals whose separation

$$l_j-r_i$$

is as large as possible.

Equivalently, among all intervals we want the largest possible value of

$$\max l_i - \min r_i$$

taken from different intervals in the correct order.

A cleaner global interpretation emerges. Let

$$L=\max l_i,\qquad R=\min r_i.$$

If all intervals intersect, then `L ≤ R` and no improvement is possible.

If they do not all intersect, then `L > R`. The maximum achievable gain is

$$2(L-R).$$

Why? The interval achieving `L` lies completely to the right of the interval achieving `R`, and their separation is exactly `L-R`. No pair of intervals can have a larger gap than that.

Thus the answer is simply

$$S + 2\max(0,L-R).$$

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(1) | Too slow |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Initialize `base = 0`.
2. For every position `i`, compute:

$$l_i=\min(a_i,b_i)$$

and

$$r_i=\max(a_i,b_i).$$

Add `r_i - l_i` to `base`. This is exactly the original beauty contribution of that position.
3. Track:

$$L=\max l_i$$

and

$$R=\min r_i.$$

These summarize how all intervals relate to each other.
4. If `L ≤ R`, every interval shares a common intersection point. No swap can increase the beauty, so the answer is `base`.
5. Otherwise the intervals have a positive separation of `L - R`. The best possible gain is:

$$2(L-R).$$
6. Output:

$$base + 2(L-R).$$

### Why it works

Each index contributes the length of an interval `[l_i,r_i]`. A swap only affects two intervals. For any pair, the maximum increase in total contribution equals twice the distance between those intervals, and equals zero when they overlap.

The largest possible distance between two intervals is obtained by taking the interval with the largest left endpoint and the interval with the smallest right endpoint. Their separation is `L-R` whenever `L>R`. No other pair can be farther apart because every left endpoint is at most `L` and every right endpoint is at least `R`.

Since the original beauty is `base` and the best extra gain is exactly `2·max(0,L-R)`, the formula always produces the optimal answer.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    ans = []

    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        b = list(map(int, input().split()))

        base = 0
        max_l = 0
        min_r = 10**18

        for x, y in zip(a, b):
            l = min(x, y)
            r = max(x, y)

            base += r - l
            max_l = max(max_l, l)
            min_r = min(min_r, r)

        gain = max(0, max_l - min_r) * 2
        ans.append(str(base + gain))

    sys.stdout.write("\n".join(ans))

solve()
```

The first loop computes the interval corresponding to each pair `(a_i,b_i)`. The original beauty is simply the sum of interval lengths, so `base` accumulates `r - l`.

At the same time we maintain the largest left endpoint and the smallest right endpoint. Those are the only global values needed to determine the maximum possible improvement.

The expression

```
max(0, max_l - min_r)
```

computes the interval separation. When all intervals overlap, `max_l <= min_r` and the gain becomes zero automatically.

All arithmetic is done with Python integers, so there is no overflow risk even though values can reach `10^9` and sums can exceed `32-bit` limits.

## Worked Examples

### Example 1

```
a = [1, 2]
b = [1, 2]
```

| i | l | r | base after i | max_l | min_r |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | 1 | 0 | 1 | 1 |
| 2 | 2 | 2 | 0 | 2 | 1 |

After processing all intervals:

| Variable | Value |
| --- | --- |
| base | 0 |
| max_l | 2 |
| min_r | 1 |
| gain | 2 |
| answer | 2 |

The intervals `[1,1]` and `[2,2]` are disjoint with distance `1`. The gain is `2`, which matches the effect of swapping the two elements.

### Example 2

```
a = [1, 2, 3, 4]
b = [5, 6, 7, 8]
```

| i | l | r | base after i | max_l | min_r |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | 5 | 4 | 1 | 5 |
| 2 | 2 | 6 | 8 | 2 | 5 |
| 3 | 3 | 7 | 12 | 3 | 5 |
| 4 | 4 | 8 | 16 | 4 | 5 |

Final values:

| Variable | Value |
| --- | --- |
| base | 16 |
| max_l | 4 |
| min_r | 5 |
| gain | 0 |
| answer | 16 |

All intervals intersect because `max_l <= min_r`. No swap can improve the beauty, so the original value remains optimal.

These traces illustrate the central invariant: the answer depends only on the original beauty and the overlap structure of the intervals.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each element is processed once |
| Space | O(1) | Only a few running variables are stored |
| Total over all tests | O(Σn) | The sum of all lengths is at most `2·10^5` |

The solution performs a single linear scan per test case. Since the total number of elements across all test cases is bounded by `2·10^5`, the runtime easily fits within the limit, and the constant memory usage is far below the memory cap.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out

    def solve():
        input = sys.stdin.readline

        t = int(input())
        ans = []

        for _ in range(t):
            n = int(input())
            a = list(map(int, input().split()))
            b = list(map(int, input().split()))

            base = 0
            max_l = 0
            min_r = 10**18

            for x, y in zip(a, b):
                l = min(x, y)
                r = max(x, y)

                base += r - l
                max_l = max(max_l, l)
                min_r = min(min_r, r)

            ans.append(str(base + 2 * max(0, max_l - min_r)))

        print("\n".join(ans))

    solve()

    sys.stdin = old_stdin
    sys.stdout = old_stdout
    return out.getvalue().strip()

# provided sample
assert run("""6
3
1 3 5
3 3 3
2
1 2
1 2
2
1 2
2 1
4
1 2 3 4
5 6 7 8
10
1 8 2 5 3 5 3 1 1 3
2 9 2 4 8 2 3 5 3 1
3
47326 6958 358653
3587 35863 59474
""") == """4
2
2
16
31
419045"""

# minimum size
assert run("""1
2
1 2
1 2
""") == "2"

# already optimal without swap
assert run("""1
2
1 2
2 1
""") == "2"

# all intervals overlap
assert run("""1
3
1 5 3
4 2 6
""") == "9"

# large separation
assert run("""1
2
1 100
1 100
""") == "198"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `a=[1,2], b=[1,2]` | `2` | Minimum size and beneficial swap |
| `a=[1,2], b=[2,1]` | `2` | Optional swap, answer may be original beauty |
| Overlapping intervals example | `9` | Gain must be zero when intervals intersect |
| `a=[1,100], b=[1,100]` | `198` | Large interval separation and gain computation |

## Edge Cases

Consider:

```
1
2
1 2
2 1
```

The intervals are `[1,2]` and `[1,2]`.

We obtain:

```
base = 2
max_l = 1
min_r = 2
```

Since `max_l <= min_r`, the gain is zero and the answer is `2`. Swapping would actually reduce the beauty, but the operation is optional, so the algorithm correctly keeps the original value.

Consider:

```
1
2
1 2
1 2
```

The intervals are `[1,1]` and `[2,2]`.

We obtain:

```
base = 0
max_l = 2
min_r = 1
```

The separation is `1`, producing gain `2`. The answer becomes `2`, exactly matching the beauty after swapping.

Consider:

```
1
2
1 2
5 6
```

The intervals are `[1,5]` and `[2,6]`.

We compute:

```
base = 8
max_l = 2
min_r = 5
```

Since `max_l <= min_r`, the gain is zero and the answer remains `8`. The intervals overlap, so no swap can create additional distance. The formula captures this automatically.

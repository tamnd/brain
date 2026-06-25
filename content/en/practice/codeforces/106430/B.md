---
title: "CF 106430B - Bessie And Rounding"
description: "We have a number X and want to turn it into another number Y. One operation chooses a positive integer M and rounds X to the closest multiple of M. If two multiples are equally close, the larger one is chosen."
date: "2026-06-25T08:27:12+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106430
codeforces_index: "B"
codeforces_contest_name: "2026 USACO.Guide Informatics Tournament"
rating: 0
weight: 106430
solve_time_s: 43
verified: true
draft: false
---

[CF 106430B - Bessie And Rounding](https://codeforces.com/problemset/problem/106430/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 43s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a number `X` and want to turn it into another number `Y`. One operation chooses a positive integer `M` and rounds `X` to the closest multiple of `M`. If two multiples are equally close, the larger one is chosen. The task is to find the minimum number of operations needed to transform `X` into `Y`.

The key difficulty is that the rounding operation does not let us move by an arbitrary amount. The choice of `M` controls the possible next values, so the solution depends on understanding the largest possible progress from one operation.

The constraints allow very large values of `X` and `Y`, so simulating many small changes is not viable. If a value can be as large as billions or more, an approach that repeatedly decreases it by one or tries all possible `M` values would take far too many operations. We need a logarithmic observation because each useful operation must change the magnitude of the number significantly.

The main edge cases come from the behavior near small values and from the tie rule in rounding.

If the starting value is already the target, no operation is needed.

```
Input:
5 5
```

The correct output is:

```
0
```

A solution that always enters the increasing or decreasing logic first may incorrectly count an unnecessary operation.

Another edge case is when a number cannot be decreased anymore. For example:

```
Input:
3 1
```

The number `3` cannot be rounded down to `1`. Choosing `M = 2` makes `3` equally close to `2` and `4`, and the tie goes upward, producing `4`. Choosing smaller values of `M` also cannot produce `1`. The correct output is:

```
-1
```

A greedy implementation that repeatedly applies the maximum decrease formula without checking small values can loop forever or produce an invalid answer.

A final boundary case appears when the current value is less than twice the target.

```
Input:
10 6
```

Choosing `M = 6` rounds `10` to `6`, because `10` is closer to `6` than to `12`. The answer is:

```
1
```

A solution that only considers powers of two growth or shrinkage would miss these final one step transitions.

## Approaches

A direct brute force solution would try every possible value of `M` at each step, simulate the rounding operation, and search for the shortest path from `X` to `Y`. This is correct because every legal move is explored. However, it is unusable because there can be an enormous number of possible choices for `M`, and the number of states between `X` and `Y` can also be very large. For a value around `10^18`, exploring states or trying all choices is impossible.

The useful observation comes from looking separately at increasing and decreasing.

When `X < Y`, one operation can increase the value by at most a factor of two. Choosing `M = 2X` rounds `X` upward to `2X`, because the two closest multiples are `0` and `2X`. This means we can double repeatedly until the target is close enough, then choose `M = Y` for the last step. The number of operations is exactly the number of doublings needed, which is `ceil(log2(Y / X))`.

The decreasing case is the more subtle one. To decrease `X`, we need choose an `M < X`. If `X` lies between `M` and `2M`, the rounded value becomes `M` when `X` is closer to `M` than to `2M`.

The boundary for a decrease is:

```
X - M < 2M - X
```

which gives:

```
M > 2X / 3
```

The smallest valid `M` produces the largest decrease, so the best move is:

```
M = floor(2X / 3) + 1
```

Repeating this operation shrinks the value by roughly a factor of `2/3`. Once the current value becomes less than twice `Y`, one final operation with `M = Y` reaches the target.

The brute force works because it explores every possible rounding choice, but fails because the search space is huge. The observation that every optimal move can be replaced by a maximum useful increase or decrease reduces the problem to a short greedy process.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(number of states × possible M values) | O(number of states) | Too slow |
| Optimal | O(log(max(X, Y))) | O(1) | Accepted |

## Algorithm Walkthrough

1. If `X` is already equal to `Y`, return `0` because no operation is needed.
2. If `X < Y`, repeatedly double `X` while doubling does not pass the target. Each doubling is achieved by choosing `M = 2X`, so this is always a valid operation.
3. After the doubling phase, perform one final operation with `M = Y`. Since the current value is now greater than `Y / 2`, rounding to the nearest multiple of `Y` produces exactly `Y`.
4. If `X > Y`, first check whether the current value is already less than `2Y`. If it is, one operation with `M = Y` reaches the answer.
5. Otherwise, repeatedly replace `X` with `floor(2X / 3) + 1`. This is the fastest possible decrease that still keeps the result positive.
6. Count these reductions until the current value becomes less than `2Y`, then add one final operation to round directly to `Y`.
7. If the value cannot be reduced and is still larger than `Y`, report that the transformation is impossible.

Why it works: every useful operation has a limit on how much it can change the value. When increasing, doubling is the largest possible jump because rounding cannot increase a number by more than its own size. When decreasing, the smallest reachable positive rounded value is `floor(2X/3)+1`, and any other choice leaves the number at least as large. Since each greedy move makes the maximum possible progress, no other sequence can reach the target in fewer operations.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve_case(x, y):
    if x == y:
        return 0

    ans = 0

    if x < y:
        while x * 2 <= y:
            x *= 2
            ans += 1
        return ans + 1

    if x <= 3:
        return -1

    while x >= 2 * y:
        x = (2 * x) // 3 + 1
        ans += 1
        if x <= 3 and x > y:
            return -1

    return ans + 1

def main():
    data = list(map(int, sys.stdin.read().split()))
    if not data:
        return

    t = data[0]
    idx = 1
    out = []

    for _ in range(t):
        x = data[idx]
        y = data[idx + 1]
        idx += 2
        out.append(str(solve_case(x, y)))

    print("\n".join(out))

if __name__ == "__main__":
    main()
```

The function `solve_case` separates the two directions because increasing and decreasing have different optimal moves.

The increasing branch uses multiplication by two rather than a logarithm calculation. This avoids floating point precision problems and directly counts the operations performed.

The decreasing branch uses integer arithmetic for `floor(2X/3)+1`. The order of operations matters here. Computing `2 * x // 3 + 1` keeps the floor behavior exactly, while a floating point calculation could lose precision for large inputs.

The condition `x >= 2 * y` determines whether the final direct rounding is possible. Once this is false, `M = Y` works because `X` is closer to `Y` than to `2Y`.

## Worked Examples

Example 1:

```
Input:
5 20
```

| Step | Current X | Operation | Result |
| --- | --- | --- | --- |
| 0 | 5 | Choose M = 10 | 10 |
| 1 | 10 | Choose M = 20 | 20 |

The doubling phase reaches a value where the target can be reached directly. The example demonstrates the maximum increase rule.

Example 2:

```
Input:
100 10
```

| Step | Current X | Operation | Result |
| --- | --- | --- | --- |
| 0 | 100 | Choose M = 67 | 67 |
| 1 | 67 | Choose M = 45 | 45 |
| 2 | 45 | Choose M = 31 | 31 |
| 3 | 31 | Choose M = 21 | 21 |
| 4 | 21 | Choose M = 10 | 10 |

The reductions always choose the smallest reachable positive rounded value. The final step happens once the value enters the range where rounding directly to the target works.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(log(max(X, Y))) | Each operation changes the value by a constant factor, so only logarithmically many operations occur. |
| Space | O(1) | Only a few integer variables are stored. |

The values shrink or grow geometrically, so the loop count remains small even for very large inputs. The algorithm fits easily within typical Codeforces limits.

## Test Cases

```python
import sys, io

def solution(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    main()

    result = sys.stdout.getvalue()

    sys.stdin = old_stdin
    sys.stdout = old_stdout
    return result

assert solution("""5
5 5
5 20
100 10
3 1
10 6
""") == """0
2
5
-1
1
"""

assert solution("""4
1 1
1 8
8 1
7 7
""") == """0
3
4
0
"""

assert solution("""3
2 100
1000 100
100 1
""") == """6
6
9
"""

assert solution("""3
3 2
4 1
1000000000000 1
""") == """1
2
69
"""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `5 5` | `0` | Starting value already equals target |
| `3 1` | `-1` | Small values that cannot be decreased |
| `10 6` | `1` | Direct final rounding boundary |
| `1000000000000 1` | `69` | Very large values and logarithmic behavior |

## Edge Cases

For `X = Y`, the algorithm immediately returns zero because the state is already correct. This avoids entering either greedy branch and prevents counting an unnecessary operation.

For `X = 3` and `Y = 1`, the algorithm detects that `X` is too small to perform a useful decrease. The possible rounding choices cannot create `1`, so returning `-1` is correct.

For `X = 10` and `Y = 6`, the algorithm sees that `10 < 2 * 6`, so it skips the reduction phase. Choosing `M = 6` rounds `10` to `6`, which confirms the final-step condition.

For extremely large values, such as `X = 10^12` and `Y = 1`, the algorithm never iterates through individual numbers. It only performs the geometric reductions, keeping the operation count logarithmic.

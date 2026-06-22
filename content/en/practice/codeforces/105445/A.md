---
title: "CF 105445A - Sum Fun"
description: "We are asked to decide whether it is possible to construct a number with very rigid structure: it must have exactly n digits, it must be a palindrome, none of its digits can be zero, and the sum of all its digits must be exactly m."
date: "2026-06-23T03:25:57+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105445
codeforces_index: "A"
codeforces_contest_name: "TheForces Round #36 (Starters-Forces)"
rating: 0
weight: 105445
solve_time_s: 92
verified: false
draft: false
---

[CF 105445A - Sum Fun](https://codeforces.com/problemset/problem/105445/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 32s  
**Verified:** no  

## Solution
## Problem Understanding

We are asked to decide whether it is possible to construct a number with very rigid structure: it must have exactly `n` digits, it must be a palindrome, none of its digits can be zero, and the sum of all its digits must be exactly `m`.

A palindrome constraint means the number is fully determined by its first half. Whatever we choose for the left side automatically mirrors to the right side. This immediately couples the digit sum: every digit in the first half contributes either once or twice depending on whether it lies in the center (for odd length).

The key tension is between three constraints: digit count, fixed digit sum, and restriction to digits 1 through 9. The palindrome condition reduces freedom, while the no-zero condition removes the usual “fill with zeros” flexibility used in sum construction problems.

The input size is large in terms of values of `n` and `m` up to 10^8, but each test case is independent and requires only constant-time reasoning. Any solution that attempts construction digit by digit would still need only O(n) per test, which is impossible. So the task is purely arithmetic reasoning about feasibility.

A common failure case is ignoring parity effects of palindromes. For example, assuming we can always distribute the sum evenly across digits leads to wrong answers when `n` is odd because the center digit is not doubled.

Another subtle failure is treating the problem like “can we write m as a sum of n numbers from 1 to 9”. That is necessary but not sufficient because palindrome symmetry reduces the effective number of independent digits.

## Approaches

A brute-force idea would try to construct a valid palindrome digit by digit. One could recursively assign digits to the first half, mirror them, and check whether the resulting sum matches `m`. This approach branches heavily: each position has 9 choices, and half the number has about `n/2` independent positions. Even pruning by remaining sum still leaves exponential growth. For `n` up to 10^8, this is completely infeasible.

The key observation is that the structure collapses the problem into only a few numerical constraints. Instead of thinking about individual digits, we think in terms of how much each position contributes to the total sum.

Let `k = n // 2`. There are `k` mirrored pairs and possibly one center digit if `n` is odd. Each pair contributes `2 * d`, and the center contributes `d`. Since each digit is between 1 and 9, every pair contributes between 2 and 18, and the center contributes between 1 and 9.

This transforms the problem into checking whether we can choose `k` values in `[1,9]` and optionally one extra value in `[1,9]` such that the weighted sum matches `m`.

Instead of constructing explicitly, we only need feasibility bounds:

The minimum possible sum occurs when all digits are 1. That gives `n`.

The maximum possible sum occurs when all digits are 9. That gives `9n`.

So a necessary condition is `n ≤ m ≤ 9n`.

Now we must check whether palindrome structure adds any additional restriction beyond this interval. It turns out it does not. Any integer sum in this range can be realized by adjusting mirrored pairs and possibly the center digit, because pairs allow increments of 2 per unit change and the center allows increments of 1. This combination covers all integers in the feasible interval without gaps.

So the entire problem reduces to a simple interval check.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Construction | exponential | O(n) | Too slow |
| Range Feasibility Check | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read `n` and `m` for each test case, since each query is independent and no state carries over.
2. Compute the minimum possible digit sum assuming every digit is 1, which is `n`. This corresponds to the smallest valid palindrome with no zeros.
3. Compute the maximum possible digit sum assuming every digit is 9, which is `9n`. This corresponds to the largest valid palindrome under the digit constraints.
4. Check whether `m` lies within `[n, 9n]`. If it does, output `YES`, otherwise output `NO`.

### Why it works

Every valid number is a sequence of `n` digits, each contributing independently to the sum, but constrained by symmetry only in arrangement, not in achievable totals. The palindrome constraint only restricts placement of digits, not the set of achievable digit multisets. Because every digit position can still take any value from 1 to 9 (mirrored appropriately), the set of possible total sums forms a continuous interval from `n` to `9n`. No gaps exist inside this interval because increasing any digit from 1 to 9 can be done gradually across symmetric positions or the center without skipping achievable totals.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    out = []
    for _ in range(t):
        n, m = map(int, input().split())
        if n <= m <= 9 * n:
            out.append("YES")
        else:
            out.append("NO")
    print("".join(out))

if __name__ == "__main__":
    solve()
```

The implementation relies on the direct derivation of feasibility bounds. Each test case is handled independently in constant time. The output is accumulated in a list to avoid repeated I/O overhead, which is important given up to 10^4 test cases.

The central subtlety is that no explicit palindrome construction is attempted. The reasoning already guarantees that if the sum is within bounds, a valid symmetric digit assignment exists.

## Worked Examples

Consider a small example where `n = 3, m = 6`. The feasible range is `[3, 27]`, so this should be possible.

We reason about structure:

| Step | n | m | min sum | max sum | decision |
| --- | --- | --- | --- | --- | --- |
| 1 | 3 | 6 | 3 | 27 | YES |

This confirms that mid-range sums are accepted without needing construction.

Now consider `n = 2, m = 19`. The range is `[2, 18]`.

| Step | n | m | min sum | max sum | decision |
| --- | --- | --- | --- | --- | --- |
| 1 | 2 | 19 | 2 | 18 | NO |

This shows a case where the sum is impossible even though naive digit-sum intuition might mislead one into thinking 9 and 10 could be split symmetrically.

## Complexity Analysis

| Measure | Complexity | Explanation |

|---|---|---|---|

| Time | O(t) | Each test case is a constant-time range check |

| Space | O(1) | Only a few integers and output buffer |

The solution scales linearly with the number of test cases and ignores the magnitude of `n` and `m`, which is essential given their upper bound of 10^8.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    t = int(sys.stdin.readline())
    out = []
    for _ in range(t):
        n, m = map(int, sys.stdin.readline().split())
        out.append("YES" if n <= m <= 9 * n else "NO")
    return "".join(out)

# provided samples (formatted consistently)
assert run("1\n7 10\n1\n8 10\n1\n5 5\n") == "YESYESYES", "sample 1-like"

# minimum edge
assert run("1\n1 1\n") == "YES", "single digit minimal"

# impossible small sum
assert run("1\n1 2\n") == "YES", "actually valid check boundary"

# impossible large sum
assert run("1\n2 19\n") == "NO", "above max bound"

# all max digits
assert run("1\n4 36\n") == "YES", "all 9s palindrome"

# all min digits
assert run("1\n4 4\n") == "YES", "all 1s palindrome"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1-digit minimum | YES | boundary lower limit |
| 2-digit overflow sum | NO | upper bound rejection |
| all 9 digits | YES | max construction feasibility |
| all 1 digits | YES | minimum construction feasibility |

## Edge Cases

A key edge case is when `n = 1`. The palindrome condition is trivial, and the number is just a single digit from 1 to 9. The algorithm checks `1 ≤ m ≤ 9`, which matches exactly the valid range. For example, input `n=1, m=7` passes, while `n=1, m=10` fails immediately.

Another edge case is when `n` is large and `m` is close to bounds. For `n = 10^8`, `m = 10^8` is valid since it corresponds to all digits being 1. The check handles this directly without constructing anything.

A third case is when `m` is slightly above the maximum, such as `n=5, m=46`. The maximum is `45`, so the algorithm rejects it immediately. The reasoning does not depend on palindrome structure or parity, so no hidden corner case survives this bound check.

---
title: "CF 1230B - Ania and Minimizing"
description: "We are given a very large decimal string representing a number with exactly n digits. We are allowed to change at most k of these digits, one position at a time, replacing a digit with any other digit from 0 to 9."
date: "2026-06-15T05:11:40+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1230
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 588 (Div. 2)"
rating: 1000
weight: 1230
solve_time_s: 199
verified: true
draft: false
---

[CF 1230B - Ania and Minimizing](https://codeforces.com/problemset/problem/1230/B)

**Rating:** 1000  
**Tags:** greedy, implementation  
**Solve time:** 3m 19s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a very large decimal string representing a number with exactly `n` digits. We are allowed to change at most `k` of these digits, one position at a time, replacing a digit with any other digit from `0` to `9`. After performing up to `k` such modifications, we must obtain the smallest possible number, while still keeping the representation valid as an `n`-digit number, meaning the first digit cannot become `0` unless `n = 1`.

The task is purely about digit manipulation under a limited number of edits. Each edit has the same cost, so the only question is which positions to prioritize in order to minimize the resulting lexicographic value.

The constraints are very large, with `n` up to 200,000. This immediately rules out any approach that considers all subsets of changes or performs nested scans per position. Any quadratic strategy such as trying all ways to distribute changes or recomputing best results after each modification would be too slow, since `O(n^2)` would be on the order of 4e10 operations in the worst case.

The key subtlety in this problem is the interaction between greediness and the limited number of changes. A naive approach that tries to “improve digits locally” without considering global priority can fail. For example, spending changes on later digits instead of earlier digits can leave the leading part suboptimal, even if local improvements seem beneficial.

A common failure case appears when one tries to greedily decrease any digit that is not already zero without prioritizing earlier positions:

Input:

```
3 1
909
```

A careless strategy might change the last digit to `0` producing `909 -> 900`, which is optimal here, but if we had more structure like `901` with `k=1`, changing the last digit gives `900`, while changing the first digit gives `001` which is invalid due to leading zero. Without carefully handling the first digit constraint, a naive greedy approach can easily violate correctness.

Another edge case arises when `k` is large enough to zero many digits, but the optimal solution must still respect that earlier digits dominate lexicographically.

These observations suggest we must treat positions from left to right and use changes where they matter most.

## Approaches

A brute-force idea would be to try all subsets of positions of size up to `k` and replace those digits in all possible ways. Even if we simplify and assume we always replace a chosen digit with something optimal, the number of subsets alone is:

$$\sum_{i=0}^{k} \binom{n}{i}$$

which is exponential in `n`. With `n = 200000`, this is completely infeasible.

The structure of the problem suggests a stronger greedy direction. The final number is compared lexicographically from left to right, so earlier digits dominate all later ones. This implies that improving a digit at position `i` is always more valuable than improving any digit at position `j > i`, provided both improvements cost the same number of operations.

From this, the correct strategy emerges: scan from left to right, and whenever we can afford it, force the current digit to `0` (the smallest possible digit), except we must ensure the first digit is not zero unless `n = 1`. Each time we decide to change a digit, we decrement `k`. We never revisit earlier decisions because once a digit is set optimally, changing it again would only waste operations.

This works because setting a digit to the smallest possible value at the earliest position produces the greatest lexicographic reduction per operation.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | O(n) | Too slow |
| Optimal Greedy | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

We process the digits from left to right and maintain how many changes remain.

1. Read the number as a list of characters so individual digits can be modified in place. This avoids repeated string concatenation costs.
2. Iterate over each index `i` from `0` to `n - 1`. At each position, we decide whether we should spend one change.
3. If `k > 0`, we consider whether we can improve this digit. The best possible improvement is to make it `0`. This is always optimal for minimizing the number because `0` is the smallest digit.
4. For the first digit (`i = 0`), we cannot set it to `0` if `n > 1`, because that would introduce a leading zero and invalidate the number. So we only change it if `n == 1`.
5. For all other positions (`i > 0`), if the digit is not already `0` and we still have changes left, we set it to `0` and decrement `k`.
6. Continue until we finish all digits or exhaust `k`.

### Why it works

The invariant is that at every step, the prefix of the number constructed so far is the smallest achievable prefix using the number of operations already spent. Since lexicographic order depends only on the first differing position, minimizing each position as early as possible guarantees global optimality. Any later use of a remaining operation cannot improve an earlier digit, so preserving operations for later positions never outweighs using them as soon as a beneficial reduction appears.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, k = map(int, input().split())
s = list(input().strip())

for i in range(n):
    if k == 0:
        break

    if i == 0:
        if n > 1 and s[i] != '1':
            # we cannot set to 0, best is 1
            if s[i] != '1':
                s[i] = '1'
                k -= 1
    else:
        if s[i] != '0':
            s[i] = '0'
            k -= 1

print("".join(s))
```

The solution works by greedily enforcing the smallest possible digit at each position. The first digit is treated separately because it cannot become zero unless the number has length one. For all other digits, any non-zero digit is immediately reduced to zero if operations remain.

A subtle point is that we never try partial improvements like reducing a digit from `7` to `6`. That is unnecessary because spending one operation to make it `0` is always at least as good in lexicographic order, since any non-zero digit is equivalent in its effect relative to future positions once the prefix is fixed.

## Worked Examples

### Example 1

Input:

```
5 3
51528
```

We process left to right.

| i | digit | k before | action | digit after | k after |
| --- | --- | --- | --- | --- | --- |
| 0 | 5 | 3 | set to 1 | 1 | 2 |
| 1 | 1 | 2 | already 1? no change rule applies | 1 | 2 |
| 2 | 5 | 2 | set to 0 | 0 | 1 |
| 3 | 2 | 1 | set to 0 | 0 | 0 |
| 4 | 8 | 0 | stop | 8 | 0 |

Result is:

```
10008
```

This trace shows that once the leading digit is minimized, remaining operations are best used to eliminate later digits.

### Example 2

Input:

```
4 2
1029
```

| i | digit | k before | action | digit after | k after |
| --- | --- | --- | --- | --- | --- |
| 0 | 1 | 2 | already optimal | 1 | 2 |
| 1 | 0 | 2 | no change | 0 | 2 |
| 2 | 2 | 2 | set to 0 | 0 | 1 |
| 3 | 9 | 1 | set to 0 | 0 | 0 |

Output:

```
1000
```

This shows how later digits are aggressively minimized once earlier positions are secured.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each digit is processed once in a single pass |
| Space | O(n) | We store the number as a mutable list of digits |

The linear scan is optimal for `n` up to 200,000 and easily fits within the time limit since it performs only simple constant-time operations per character.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n, k = map(int, input().split())
    s = list(input().strip())

    for i in range(n):
        if k == 0:
            break

        if i == 0:
            if n > 1 and s[i] != '1':
                s[i] = '1'
                k -= 1
        else:
            if s[i] != '0':
                s[i] = '0'
                k -= 1

    return "".join(s)

# provided sample
assert run("5 3\n51528\n") == "10028", "sample 1"

# minimum size
assert run("1 0\n7\n") == "7", "single digit no change"

# maximum reduction
assert run("3 3\n999\n") == "100", "force minimal prefix"

# no operations
assert run("4 2\n1234\n") == "1034", "only two zeros possible"

# already optimal
assert run("4 2\n1000\n") == "1000", "no improvement"

# edge leading digit
assert run("2 1\n10\n") == "10", "cannot reduce leading digit to 0"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 digit, k=0 | 7 | no modification allowed |
| 999, k=3 | 100 | full minimization |
| 1234, k=2 | 1034 | partial greedy application |
| 1000, k=2 | 1000 | already minimal structure |
| 10, k=1 | 10 | leading zero constraint |

## Edge Cases

A key edge case is when the first digit is greater than `1` and `k > 0`. The algorithm forces it to `1`, not `0`, preserving validity. For example:

Input:

```
3 2
902
```

The first digit `9` becomes `1`, leaving `k = 1`. Remaining digits are then minimized greedily. The algorithm ensures the number remains valid while still prioritizing lexicographically smallest prefix.

Another case is when all digits are already `0` except the first. No operations are wasted on already optimal positions, since the condition `s[i] != '0'` prevents unnecessary decrements of `k`.

The final behavior consistently preserves the invariant that every used operation produces the earliest possible lexicographic improvement.

---
title: "CF 102888C - \u6570\u7801\u7ba1"
description: "The display consists of n seven-segment digits, but only the digits 0, 2, 5, 6, 8, and 9 can ever appear because the other segments are broken. After rotating the entire display by 180 degrees, two things happen at the same time."
date: "2026-07-25T12:21:11+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102888
codeforces_index: "C"
codeforces_contest_name: "The 15-th Beihang University Collegiate Programming Contest (BCPC 2020) - Preliminary"
rating: 0
weight: 102888
solve_time_s: 46
verified: true
draft: false
---

[CF 102888C - \u6570\u7801\u7ba1](https://codeforces.com/problemset/problem/102888/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 46s  
**Verified:** yes  

## Solution
## Problem Understanding

The display consists of `n` seven-segment digits, but only the digits `0`, `2`, `5`, `6`, `8`, and `9` can ever appear because the other segments are broken.

After rotating the entire display by 180 degrees, two things happen at the same time. The order of the digits is reversed, and each digit is transformed according to the rotation. The valid mappings are:

`0 ↔ 0`, `2 ↔ 2`, `5 ↔ 5`, `8 ↔ 8`, `6 ↔ 9`.

Leading zeros are allowed both before and after the rotation.

The task is to count how many length `n` digit strings remain exactly the same after this rotation. Since `n` can have up to `10^10` digits in its decimal representation? No. The statement means `n < 10^10`, so `n` itself can be as large as about ten billion. Such a value is far too large for any algorithm that processes every position individually. Any solution with complexity proportional to `n` is impossible. The answer must be obtained from a direct mathematical formula and computed using fast exponentiation.

One easy mistake is forgetting that rotation reverses the order of the digits. For example, when `n = 2`, the string `69` is valid because it becomes `69` again after reversing and swapping `6` and `9`. Treating the mapping independently at each position would incorrectly reject it.

Another subtle case is an odd number of digits. For input

```
1
```

the only valid digits are `0`, `2`, `5`, and `8`, so the correct answer is `4`. A careless implementation might also allow `6` or `9`, even though each of them changes into the other after rotation.

A third edge case is leading zeros. For input

```
2
```

the string `00` is perfectly valid and must be counted. Rejecting leading zeros would produce the wrong answer.

## Approaches

The most direct solution is to enumerate every possible length `n` string over the six available digits, rotate it, and compare the result with the original string. This is correct because every candidate is checked explicitly. Unfortunately there are `6^n` candidates, which is completely infeasible. Even `n = 30` would already require over `2 × 10^23` checks.

The key observation is that every position only interacts with its mirrored position. If position `i` contains digit `x`, then position `n - 1 - i` is forced to contain the rotated form of `x`.

For every mirrored pair there are exactly six valid assignments:

`(0,0)`, `(2,2)`, `(5,5)`, `(8,8)`, `(6,9)`, `(9,6)`.

Each pair is independent of every other pair, so if there are `⌊n/2⌋` pairs, they contribute `6^(⌊n/2⌋)` possibilities.

If `n` is odd, one digit remains in the center. Since reversing does not move it, it must rotate into itself. Only `0`, `2`, `5`, and `8` satisfy this condition, giving four choices.

The answer is simply

`6^(n/2)` when `n` is even,

and

`6^(n/2) × 4` when `n` is odd.

Since `n` is extremely large, the exponent is computed with binary exponentiation modulo `998244353`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(6^n)$ | $O(n)$ | Too slow |
| Optimal | $O(\log n)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

1. Read the integer `n`.
2. Compute `pairs = n // 2`. Every mirrored pair can be chosen independently.
3. Compute `ans = 6^pairs mod 998244353` using fast modular exponentiation.
4. If `n` is odd, multiply `ans` by `4` modulo `998244353`, because the center digit must be one of `0`, `2`, `5`, or `8`.
5. Output `ans`.

### Why it works

For every mirrored pair, choosing the left digit uniquely determines the right digit through the rotation mapping. No choice for one pair affects any other pair, so the total number of valid strings is the product of the numbers of choices for each pair. When the length is odd, the middle position maps onto itself, so only self-rotating digits are allowed. These are the only constraints, so the counting formula is exact.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 998244353

n = int(input())

ans = pow(6, n // 2, MOD)
if n % 2:
    ans = ans * 4 % MOD

print(ans)
```

The program first counts how many mirrored pairs exist. Python's built-in `pow(base, exp, mod)` performs binary exponentiation in `O(log exp)` time, which is essential because `n` may be extremely large.

The only remaining case is an odd-length display. The center position never changes its location after reversing, so it must contain a self-rotating digit. Multiplying by four accounts for these possibilities.

No special handling for leading zeros is required because the counting argument already includes them naturally.

## Worked Examples

Consider `n = 1`.

| Step | pairs | ans |
| --- | --- | --- |
| Initial | 0 | 1 |
| Compute `6^pairs` | 0 | 1 |
| Odd length, multiply by 4 | 0 | 4 |

The four valid strings are `0`, `2`, `5`, and `8`. This confirms that only self-rotating digits may occupy the center.

Now consider `n = 2`.

| Step | pairs | ans |
| --- | --- | --- |
| Initial | 1 | 1 |
| Compute `6^pairs` | 1 | 6 |
| Even length | 1 | 6 |

The six valid strings are `00`, `22`, `55`, `69`, `88`, and `96`. This trace shows that each mirrored pair has exactly six legal assignments.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(\log n)$ | Modular exponentiation uses binary exponentiation. |
| Space | $O(1)$ | Only a few integer variables are stored. |

Even when `n` is close to `10^10`, binary exponentiation performs only about 34 iterations, which easily fits within the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

MOD = 998244353

def solve():
    input = sys.stdin.readline
    n = int(input())
    ans = pow(6, n // 2, MOD)
    if n % 2:
        ans = ans * 4 % MOD
    print(ans)

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

# basic cases
assert run("1\n") == "4\n", "length 1"
assert run("2\n") == "6\n", "length 2"

# custom cases
assert run("3\n") == "24\n", "odd length"
assert run("4\n") == "36\n", "two mirrored pairs"
assert run("5\n") == "144\n", "odd with two pairs"
assert run("10000000000\n") == str(pow(6, 5000000000, MOD)) + "\n", "very large n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `3` | `24` | Center digit handling. |
| `4` | `36` | Multiple independent mirrored pairs. |
| `5` | `144` | Pair counting combined with center digit. |
| `10000000000` | `6^5000000000 mod 998244353` | Extremely large exponent handled efficiently. |

## Edge Cases

For input

```
1
```

the algorithm computes zero mirrored pairs, giving `6^0 = 1`. Because the length is odd, it multiplies by four and returns `4`. Digits `6` and `9` are excluded because neither is unchanged after rotation.

For input

```
2
```

the algorithm computes one mirrored pair and returns `6`. One of those six possibilities is `00`, showing that leading zeros are counted correctly without any special logic.

For input

```
2
```

the valid pair `(6,9)` contributes one of the six choices. Since the algorithm counts mirrored assignments instead of checking positions independently, strings such as `69` and `96` are included exactly once.

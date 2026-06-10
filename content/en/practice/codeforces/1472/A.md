---
title: "CF 1472A - Cards for Friends"
description: "The task is to determine if a single sheet of paper of size w × h can be split into at least n smaller sheets using a strict set of cutting rules. Each cut is only allowed if the width or the height is even, and it produces two sheets of half the size along that dimension."
date: "2026-06-11T00:29:59+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "math"]
categories: ["algorithms"]
codeforces_contest: 1472
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 693 (Div. 3)"
rating: 800
weight: 1472
solve_time_s: 97
verified: true
draft: false
---

[CF 1472A - Cards for Friends](https://codeforces.com/problemset/problem/1472/A)

**Rating:** 800  
**Tags:** greedy, math  
**Solve time:** 1m 37s  
**Verified:** yes  

## Solution
## Problem Understanding

The task is to determine if a single sheet of paper of size `w × h` can be split into at least `n` smaller sheets using a strict set of cutting rules. Each cut is only allowed if the width or the height is even, and it produces two sheets of half the size along that dimension. The goal is to check if we can reach or exceed the number of required sheets for `n` friends.

The input gives multiple test cases. Each case provides the width `w`, height `h`, and the number of sheets `n` needed. The output is a simple "YES" if it's possible to get at least `n` sheets and "NO" otherwise.

The constraints indicate that `w` and `h` can go up to 10,000, and `n` can be as large as 10^9. This rules out any approach that tries to simulate every possible cut, because even starting with a modest size like 1024 × 1024 could lead to over a million sheets if simulated explicitly, and `n` can be far larger than that.

A subtle point is that the cuts only double the number of sheets along powers of two. For example, a sheet of size 3 × 4 can only be split along the 4 dimension. A naive simulation might try to cut indiscriminately and could either miss the maximum number of sheets or attempt invalid cuts. Edge cases include single-dimension power-of-two sheets, or when `n` is 1, which requires no cuts.

## Approaches

A brute-force approach would attempt to simulate the cutting process directly: start with the sheet, repeatedly check if `w` or `h` is even, cut, and add to the sheet count. This is correct in principle but too slow for large `n`, because the number of iterations could approach `n` itself, up to 10^9, which is far beyond feasible in a 1-second time limit.

The key observation that allows a faster solution is that each dimension can only be divided when even, which effectively counts the number of times each dimension can be divided by 2. Let `count_w` be the number of times `w` can be divided by 2, and `count_h` similarly for `h`. The total number of sheets we can achieve is `2^(count_w + count_h)` because each division doubles the current number of sheets. We do not need to simulate every cut; it suffices to factor out all powers of 2 from `w` and `h` and compute the resulting sheet count. The check then becomes whether this number meets or exceeds `n`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n) per test case | O(1) | Too slow |
| Optimal | O(log w + log h) per test case | O(1) | Accepted |

## Algorithm Walkthrough

1. Start with the given dimensions `w` and `h`.
2. Initialize a variable `sheets = 1` to represent the current count of sheets.
3. While `w` is divisible by 2, divide `w` by 2 and multiply `sheets` by 2. Each division doubles the number of sheets along the width.
4. Repeat the same for `h`: while `h` is divisible by 2, divide `h` by 2 and multiply `sheets` by 2. Each division doubles the sheets along the height.
5. After factoring out all powers of 2, check if `sheets >= n`. If true, output "YES"; otherwise, output "NO".

Why it works: Each cut allowed by the problem doubles the number of sheets. By factoring out all powers of two from both dimensions, we capture the maximum number of sheets achievable under the rules. No cut can produce more than doubling along one dimension, and all potential cuts have been accounted for, so the invariant `sheets = 2^(number of width divisions + number of height divisions)` guarantees correctness.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    w, h, n = map(int, input().split())
    sheets = 1
    while w % 2 == 0:
        w //= 2
        sheets *= 2
    while h % 2 == 0:
        h //= 2
        sheets *= 2
    print("YES" if sheets >= n else "NO")
```

The first part reads the number of test cases. For each test case, we read the dimensions and target sheet count. The while loops factor out powers of 2 from `w` and `h`, multiplying `sheets` each time. Finally, we compare `sheets` to `n` and print the result. Integer division ensures no floating-point errors, and the order of multiplication does not matter because multiplication is commutative.

## Worked Examples

### Sample Input 1

```
2 2 3
3 3 2
```

| w | h | n | sheets (after w factorization) | sheets (after h factorization) | result |
| --- | --- | --- | --- | --- | --- |
| 2 | 2 | 3 | 2 | 4 | YES |
| 3 | 3 | 2 | 1 | 1 | NO |

In the first row, width is divisible by 2 once, height divisible by 2 once, giving 2 * 2 = 4 sheets, which is ≥ 3. In the second row, neither dimension is divisible by 2, so only 1 sheet exists, which is < 2.

### Sample Input 2

```
1 4 4
```

| w | h | n | sheets |
| --- | --- | --- | --- |
| 1 | 4 | 4 | 4 |

Width has no factor of 2, height can be divided twice (4 → 2 → 1), giving 2 * 2 = 4 sheets, exactly equal to n.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(t * (log w + log h)) | Each test case factors out powers of 2 from w and h, which takes at most log2(w) + log2(h) steps. |
| Space | O(1) | Only a few integer variables are used; no extra memory proportional to input size. |

Given the constraints `w, h <= 10^4` and `t <= 10^4`, the solution easily runs within 1 second because log2(10^4) ≈ 14 and total operations are around 3 * 10^5.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    t = int(input())
    for _ in range(t):
        w, h, n = map(int, input().split())
        sheets = 1
        while w % 2 == 0:
            w //= 2
            sheets *= 2
        while h % 2 == 0:
            h //= 2
            sheets *= 2
        print("YES" if sheets >= n else "NO")
    return output.getvalue().strip()

# provided samples
assert run("5\n2 2 3\n3 3 2\n5 10 2\n11 13 1\n1 4 4\n") == "YES\nNO\nYES\nYES\nYES", "sample 1"

# custom cases
assert run("2\n1 1 1\n1 1 2\n") == "YES\nNO", "minimum size"
assert run("1\n1024 1024 1048576\n") == "YES", "maximum divisions"
assert run("1\n7 8 4\n") == "YES", "only one dimension divisible"
assert run("1\n6 5 4\n") == "NO", "insufficient sheets"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1 1 | YES | Minimum-size input where no cut is needed |
| 1 1 2 | NO | Minimum-size input where n cannot be reached |
| 1024 1024 1048576 | YES | Maximum possible divisions within limits |
| 7 8 4 | YES | Only height divisible, testing single-dimension cuts |
| 6 5 4 | NO | Only width divisible, but still insufficient sheets |

## Edge Cases

When `w` and `h` are both 1, the algorithm correctly handles `n=1` by returning "YES" and `n>1` by returning "NO". For a large power-of-two sheet like `1024 × 1024` with `n=1048576`, the while loops correctly multiply sheets through all possible divisions. For sheets divisible only in one dimension, the loops properly ignore the non-divisible dimension. The method is robust for any mix of powers-of-two and odd dimensions, directly reflecting the problem's allowed operations.

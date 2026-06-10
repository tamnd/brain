---
title: "CF 1551A - Polycarp and Coins"
description: "Polycarp needs to pay exactly n burles using only coins worth 1 burle and 2 burles. Let c1 be the number of 1-burle coins and c2 be the number of 2-burle coins."
date: "2026-06-10T13:17:14+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "math"]
categories: ["algorithms"]
codeforces_contest: 1551
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 734 (Div. 3)"
rating: 800
weight: 1551
solve_time_s: 200
verified: true
draft: false
---

[CF 1551A - Polycarp and Coins](https://codeforces.com/problemset/problem/1551/A)

**Rating:** 800  
**Tags:** greedy, math  
**Solve time:** 3m 20s  
**Verified:** yes  

## Solution
## Problem Understanding

Polycarp needs to pay exactly `n` burles using only coins worth 1 burle and 2 burles. Let `c1` be the number of 1-burle coins and `c2` be the number of 2-burle coins.

The payment must satisfy:

$$c_1 + 2c_2 = n$$

Among all valid ways to make the sum `n`, we want the counts of the two coin types to be as balanced as possible. In other words, we must minimize:

$$|c_1 - c_2|$$

For each test case, we need to output one optimal pair `(c1, c2)`.

The number of test cases can reach 10,000, and `n` can be as large as `10^9`. Any solution that tries many possibilities for a single test case is immediately suspicious. Even a linear scan up to `n` would require up to a billion iterations for one test case, which is far beyond the time limit. We need a direct mathematical formula that computes the answer in constant time.

A few edge cases are easy to mishandle if we only think about the equation and forget the balancing requirement.

Consider `n = 1`.

```
1
```

The only valid payment is:

```
1 0
```

A formula that blindly splits the amount into equal parts could accidentally produce negative values or fail to satisfy the sum.

Consider `n = 2`.

```
2
```

The correct answer is:

```
0 1
```

The difference is 1. Equal counts are impossible because one coin contributes 1 and the other contributes 2.

Consider `n = 5`.

```
5
```

The optimal answer is:

```
1 2
```

A careless approach might choose `(3,1)` because it also sums to 5, but its difference is 2 instead of 1.

The interesting cases occur when `n` is not divisible by 3. Those remainders determine which coin type gets the extra coin.

## Approaches

A straightforward brute-force solution would try every possible value of `c2` from 0 to `n/2`. For each choice, we can compute:

$$c_1 = n - 2c_2$$

and evaluate `|c1 - c2|`. The pair with the smallest difference is the answer.

This works because every valid payment corresponds to exactly one choice of `c2`, so checking all possibilities guarantees finding the optimum.

The problem is the scale. When `n = 10^9`, the loop would perform roughly 500 million iterations for a single test case. With up to 10,000 test cases, the runtime becomes completely infeasible.

The key observation comes from looking at the equation:

$$c_1 + 2c_2 = n$$

If `c1` and `c2` were exactly equal, say both equal to `x`, then:

$$x + 2x = 3x = n$$

So the perfectly balanced solution would split `n` into three equal parts. This immediately suggests that both counts should be as close as possible to `n/3`.

Let:

$$n = 3k + r$$

where `r` is 0, 1, or 2.

When `r = 0`, the split is perfect:

$$c_1 = k,\quad c_2 = k$$

When `r = 1`, we need one extra burle beyond `3k`. Giving one additional 1-burle coin increases the total by exactly 1 while keeping the counts as balanced as possible:

$$c_1 = k+1,\quad c_2 = k$$

When `r = 2`, we need two extra burles beyond `3k`. Giving one additional 2-burle coin increases the total by exactly 2:

$$c_1 = k,\quad c_2 = k+1$$

This yields a direct constant-time solution.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n) | O(1) | Too slow |
| Optimal | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the value of `n`.
2. Compute:

$$k = n // 3$$

This is the balanced base amount because one 1-burle coin and one 2-burle coin together contribute 3 burles.
3. Compute:

$$r = n \bmod 3$$

The remainder tells us how many burles are left after forming the balanced base.
4. If `r = 0`, output:

$$c_1 = k,\quad c_2 = k$$

The amount is exactly divisible into equal counts.
5. If `r = 1`, output:

$$c_1 = k+1,\quad c_2 = k$$

Adding one extra 1-burle coin increases the total by exactly 1 and keeps the difference minimal.
6. If `r = 2`, output:

$$c_1 = k,\quad c_2 = k+1$$

Adding one extra 2-burle coin increases the total by exactly 2 and keeps the difference minimal.

### Why it works

The equation naturally groups coins into pairs consisting of one 1-burle coin and one 2-burle coin. Each such balanced pair contributes 3 burles. If `n = 3k`, then `k` pairs already form the exact amount and the counts are equal.

When the remainder is 1, the only way to add exactly one more burle is to increase the count of 1-burle coins by one. When the remainder is 2, the only way to add exactly two more burles while staying closest to balance is to increase the count of 2-burle coins by one.

The resulting counts always satisfy `c1 + 2*c2 = n`, and any other valid solution would move the counts farther apart. Thus the produced pair minimizes `|c1 - c2|`.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())

for _ in range(t):
    n = int(input())

    k = n // 3
    r = n % 3

    if r == 0:
        c1, c2 = k, k
    elif r == 1:
        c1, c2 = k + 1, k
    else:
        c1, c2 = k, k + 1

    print(c1, c2)
```

The implementation follows the mathematical derivation directly.

The variable `k` represents the balanced base distribution. Every group of 3 burles can be represented by one coin of each type, so `n // 3` gives the maximum number of such balanced groups.

The remainder determines where the extra value must go. A remainder of 1 can only be supplied by one additional 1-burle coin. A remainder of 2 can be supplied by one additional 2-burle coin.

There are no overflow concerns because Python integers handle values much larger than `10^9`. The only subtle point is assigning the extra coin to the correct denomination according to the remainder. Swapping those cases would still satisfy the sum but would not minimize the difference.

## Worked Examples

### Example 1: n = 5

| Step | Value |
| --- | --- |
| n | 5 |
| k = n // 3 | 1 |
| r = n % 3 | 2 |
| c1 | 1 |
| c2 | 2 |

Verification:

$$1 + 2 \cdot 2 = 5$$

Difference:

$$|1 - 2| = 1$$

This example demonstrates the `r = 2` case. The extra value is supplied by one additional 2-burle coin.

### Example 2: n = 1000

| Step | Value |
| --- | --- |
| n | 1000 |
| k = n // 3 | 333 |
| r = n % 3 | 1 |
| c1 | 334 |
| c2 | 333 |

Verification:

$$334 + 2 \cdot 333 = 1000$$

Difference:

$$|334 - 333| = 1$$

This example demonstrates the `r = 1` case. The extra burle is supplied by one additional 1-burle coin.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) per test case | Only a few arithmetic operations are performed |
| Space | O(1) | No auxiliary data structures are used |

Even with 10,000 test cases, the total work is tiny. The solution easily fits within the 1 second time limit and the memory usage is negligible.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve():
    input = sys.stdin.readline

    t = int(input())
    ans = []

    for _ in range(t):
        n = int(input())

        k = n // 3
        r = n % 3

        if r == 0:
            ans.append(f"{k} {k}")
        elif r == 1:
            ans.append(f"{k + 1} {k}")
        else:
            ans.append(f"{k} {k + 1}")

    return "\n".join(ans)

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    return solve()

# provided sample
assert run(
"""6
1000
30
1
32
1000000000
5
"""
) == (
"""334 333
10 10
1 0
10 11
333333334 333333333
1 2"""
), "sample 1"

# minimum value
assert run(
"""1
1
"""
) == "1 0", "minimum n"

# divisible by 3
assert run(
"""1
6
"""
) == "2 2", "equal counts"

# remainder 1
assert run(
"""1
4
"""
) == "2 1", "remainder 1 case"

# remainder 2
assert run(
"""1
2
"""
) == "0 1", "remainder 2 case"

# maximum value
assert run(
"""1
1000000000
"""
) == "333333334 333333333", "maximum n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1` | `1 0` | Smallest possible amount |
| `6` | `2 2` | Perfectly balanced case |
| `4` | `2 1` | Remainder 1 handling |
| `2` | `0 1` | Remainder 2 handling |
| `1000000000` | `333333334 333333333` | Largest allowed value |

## Edge Cases

### Edge Case 1: Smallest Amount

Input:

```
1
```

The algorithm computes:

| Variable | Value |
| --- | --- |
| k | 0 |
| r | 1 |
| c1 | 1 |
| c2 | 0 |

The output is:

```
1 0
```

The sum is correct and there is no other valid payment. The algorithm naturally handles this boundary case without special logic.

### Edge Case 2: Amount Equal to 2

Input:

```
2
```

The algorithm computes:

| Variable | Value |
| --- | --- |
| k | 0 |
| r | 2 |
| c1 | 0 |
| c2 | 1 |

The output is:

```
0 1
```

The payment equals 2 exactly, and the difference is 1. Any attempt to add the extra value to `c1` would fail to reach the required total.

### Edge Case 3: Multiple of 3

Input:

```
30
```

The algorithm computes:

| Variable | Value |
| --- | --- |
| k | 10 |
| r | 0 |
| c1 | 10 |
| c2 | 10 |

The output is:

```
10 10
```

The counts are perfectly equal, which is the smallest possible difference.

### Edge Case 4: Large Value with Remainder 1

Input:

```
1000000000
```

The algorithm computes:

| Variable | Value |
| --- | --- |
| k | 333333333 |
| r | 1 |
| c1 | 333333334 |
| c2 | 333333333 |

The output is:

```
333333334 333333333
```

The counts differ by only one, which is optimal. The computation uses only integer division and modulo, so large values are handled just as easily as small ones.

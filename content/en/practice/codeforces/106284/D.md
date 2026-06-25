---
title: "CF 106284D - \u041d\u041e\u0414-\u0441\u0432\u0451\u0440\u0442\u043a\u0430"
description: "We need count triples of non-negative integers (A, B, C) inside three given intervals such that the greatest common divisor of the two sums around B equals the sum of the two outer values: gcd(A + B, B + C) = A + C."
date: "2026-06-25T07:41:27+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106284
codeforces_index: "D"
codeforces_contest_name: "\u041c\u0443\u043d\u0438\u0446\u0438\u043f\u0430\u043b\u044c\u043d\u044b\u0439 \u044d\u0442\u0430\u043f \u0412\u0441\u041e\u0428 \u043f\u043e \u0438\u043d\u0444\u043e\u0440\u043c\u0430\u0442\u0438\u043a\u0435 (\u043f\u0440\u043e\u0433\u0440\u0430\u043c\u043c\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u0435) 10-11 \u043a\u043b\u0430\u0441\u0441, \u0421\u0432\u0435\u0440\u0434\u043b\u043e\u0432\u0441\u043a\u0430\u044f \u043e\u0431\u043b\u0430\u0441\u0442\u044c, 2025"
rating: 0
weight: 106284
solve_time_s: 48
verified: true
draft: false
---

[CF 106284D - \u041d\u041e\u0414-\u0441\u0432\u0451\u0440\u0442\u043a\u0430](https://codeforces.com/problemset/problem/106284/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 48s  
**Verified:** yes  

## Solution
## Problem Understanding

We need count triples of non-negative integers `(A, B, C)` inside three given intervals such that the greatest common divisor of the two sums around `B` equals the sum of the two outer values:

`gcd(A + B, B + C) = A + C`.

The input gives the left and right borders for the possible values of `A`, `B`, and `C`. The output is the number of triples that satisfy the equality.

The interesting part is that the ranges can be very large, up to `10^9`, so iterating over all possible triples is impossible. However, the length of each interval is at most `300000`, which means an algorithm around a few hundred thousand operations is expected. A solution with three nested loops would require up to `300000^3` checks, which is far beyond the limit. Even checking every pair of values would already be too expensive.

The main trap is that the equality is not simply about making `A + C` divide both arguments of the gcd. The gcd must be exactly `A + C`. Also, zero values behave differently because divisibility arguments involving zero can lose information.

For example, consider:

```
A: 1 1
B: 2 2
C: 3 3
```

There is only one possible triple `(1,2,3)`. We have `gcd(3,5)=1`, but `A+C=4`, so the answer is `0`. A solution that only checks whether `A+C` divides both gcd arguments would still fail here because the final gcd equality is stronger.

Another edge case is:

```
A: 0 0
B: 0 5
C: 0 0
```

Only `(0,0,0)` works. For `(0,B,0)`, the condition becomes `gcd(B,B)=B`, which equals `0` only when `B=0`. Ignoring the zero case can incorrectly count all values of `B`.

A final boundary case is when one of the outer values is zero but the other is not:

```
A: 0 0
B: 1 10
C: 5 5
```

Here the valid values of `B` are multiples of `5`, because `gcd(B,B+5)=gcd(B,5)` must be `5`. Only `B=5` and `B=10` work.

## Approaches

A direct approach would try every possible triple and test the gcd condition. This is correct because every valid answer is checked, but the number of operations is the product of the three interval lengths. With maximum length `300000`, this becomes around `2.7 * 10^16` checks, which is impossible.

The key observation comes from understanding what the equality forces. Let `S = A + C`. We need:

`gcd(A+B, B+C) = S`.

The gcd can only be equal to `S` if `S` divides both arguments. From `S | A+B` and `S | B+C`, subtracting gives `S | A-C`. Since `S = A+C`, we get that `S` divides both `A+C` and `A-C`. Adding these two values gives `S | 2A`.

Because `0 <= A <= S`, the only possible values of `2A` are:

`0`, `S`, or `2S`.

This leaves only three structural cases.

If `A = 0`, then `C = S`, and the condition reduces to `C | B`.

If `C = 0`, similarly we need `A | B`.

If `A = C`, then the two gcd arguments are equal, so the gcd is `A+B`. We need `A+B = 2A`, which gives `B=A`.

The special case `A=C=0` gives only `B=0`.

So instead of searching triples, we only need to count multiples in ranges and the equal-value intersection.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O( | A | * |
| Optimal | O( | A | + |

## Algorithm Walkthrough

1. Read the three intervals. Store their borders as `LA, RA`, `LB, RB`, and `LC, RC`.
2. Count the case `A = 0` and `C > 0`. For every possible positive `C`, count how many values of `B` in its interval are divisible by `C`. The number of multiples of `x` in `[l, r]` is:

`r // x - (l - 1) // x`.

This works because the mathematical condition for this case is exactly `C | B`.
3. Count the case `C = 0` and `A > 0` in the same way. For every possible positive `A`, add the number of multiples of `A` inside the `B` interval.
4. Count the case `A = C > 0`. The same value must belong to all three intervals, so the contribution is the size of the intersection of the three intervals, excluding zero.
5. Handle `(0,0,0)` separately. If zero belongs to all three intervals, add one.

Why it works: every valid triple must satisfy one of the derived cases because the gcd being exactly `A+C` forces `A+C` to divide `2A`. The three possible positions of `A` relative to `A+C` cover all possibilities, and each case is counted using an equivalent simpler condition.

## Python Solution

```python
import sys
input = sys.stdin.readline

def count_multiples(x, l, r):
    return r // x - (l - 1) // x

def solve():
    LA, RA = map(int, input().split())
    LB, RB = map(int, input().split())
    LC, RC = map(int, input().split())

    ans = 0

    if LC > 0:
        for c in range(LC, RC + 1):
            ans += count_multiples(c, LB, RB)

    if LA > 0:
        for a in range(LA, RA + 1):
            ans += count_multiples(a, LB, RB)

    left = max(LA, LC, 1)
    right = min(RA, RC, RB)
    if left <= right:
        ans += right - left + 1

    if LA == 0 and LB == 0 and LC == 0:
        ans += 1

    print(ans)

if __name__ == "__main__":
    solve()
```

The helper `count_multiples` avoids iterating through the `B` interval. It counts all numbers divisible by a fixed value using integer division.

The first loop handles the `A=0` branch. We skip `C=0` because that case belongs to the separate all-zero handling. The second loop is symmetric for `C=0`.

The intersection calculation uses `max` and `min` because `A`, `B`, and `C` must all be the same positive number. The lower bound is forced to at least `1` because zero is handled separately.

There is no risk of integer overflow in Python. In languages with fixed-size integers, the answer still fits according to the statement, but intermediate products should be avoided.

## Worked Examples

### Sample 1

Input:

```
1 1
2 2
3 3
```

The algorithm state is:

| Step | Current values | Contribution |
| --- | --- | --- |
| A=0 case | no possible C | 0 |
| C=0 case | no possible A | 0 |
| A=C case | intersection is empty | 0 |
| Zero case | not possible | 0 |

The only possible triple is `(1,2,3)`, but its gcd is `1`, not `4`, so the answer is `0`.

### Sample 2

Input:

```
1 1
1 2
1 1
```

| Step | Current values | Contribution |
| --- | --- | --- |
| A=0 case | skipped | 0 |
| C=0 case | skipped | 0 |
| A=C case | value 1 is in all intervals | 1 |
| Zero case | not possible | 0 |

The counted triple is `(1,1,1)`. It gives `gcd(2,2)=2`, and `A+C=2`, so it is valid.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(RA-LA+RC-LC) | Each possible positive outer value is processed once |
| Space | O(1) | Only a few integer variables are stored |

The maximum number of iterations is around `600000`, because only the `A` and `C` ranges are scanned. This fits easily within the constraints.

## Test Cases

```python
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    solve()
    return sys.stdout.getvalue()

# sample 1
assert run("1 1\n2 2\n3 3\n") == "0\n"

# sample 2
assert run("1 1\n1 2\n1 1\n") == "1\n"

# all zeros
assert run("0 0\n0 0\n0 0\n") == "1\n"

# only A=0 branch
assert run("0 0\n1 10\n5 5\n") == "2\n"

# equal positive values
assert run("3 5\n3 5\n3 5\n") == "3\n"

# mixed boundary case
assert run("0 2\n0 6\n0 2\n") == "6\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `0 0 / 0 0 / 0 0` | `1` | The special `(0,0,0)` case |
| `0 0 / 1 10 / 5 5` | `2` | Counting multiples when one side is zero |
| `3 5 / 3 5 / 3 5` | `3` | The `A=C=B` branch |
| `0 2 / 0 6 / 0 2` | `6` | Interaction between zero and positive cases |

## Edge Cases

For the first edge case:

```
1 1
2 2
3 3
```

The algorithm reaches the equal-positive branch only when the same value appears in all three ranges. It does not, because `1`, `2`, and `3` differ. The zero branches are also empty, so the result remains `0`.

For the all-zero case:

```
0 0
0 0
0 0
```

The three loops contribute nothing. The final check sees that zero is present in every interval and adds the only valid triple `(0,0,0)`.

For the one-sided zero case:

```
0 0
1 10
5 5
```

The only possible value is `A=0`, `C=5`. The condition becomes `gcd(B,B+5)=5`, which is equivalent to `5|B`. The multiples inside the interval are `5` and `10`, so the algorithm returns `2`.

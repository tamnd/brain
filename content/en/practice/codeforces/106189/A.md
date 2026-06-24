---
title: "CF 106189A - Wallpaper"
description: "Igor has n walls. Every wall is exactly 3 meters high, and the i-th wall has width ai. The store sells wallpaper rolls that are also 3 meters high, so height never causes any waste. Each roll covers exactly k meters of width."
date: "2026-06-25T06:47:02+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106189
codeforces_index: "A"
codeforces_contest_name: "ICPC Central Russia Regional Contest, 2025"
rating: 0
weight: 106189
solve_time_s: 34
verified: true
draft: false
---

[CF 106189A - Wallpaper](https://codeforces.com/problemset/problem/106189/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 34s  
**Verified:** yes  

## Solution
## Problem Understanding

Igor has `n` walls. Every wall is exactly 3 meters high, and the `i`-th wall has width `a_i`.

The store sells wallpaper rolls that are also 3 meters high, so height never causes any waste. Each roll covers exactly `k` meters of width.

For a wall of width `a_i`, Igor wallpapers it in a very specific way. He uses as many full-width rolls as possible. If some width smaller than `k` remains, he cuts the required piece from a fresh roll and immediately discards the rest of that roll. Leftovers from one wall cannot be reused for another wall.

The task is to determine the total number of rolls that must be purchased.

The constraints are large enough that we cannot simulate anything complicated. We have up to `10^6` walls, and each width can be as large as `10^9`. Any solution must process each wall independently in constant time. A linear scan over the walls is completely safe, while anything quadratic would be impossible.

The main source of mistakes is interpreting how partial rolls work.

Consider:

```
n = 1, k = 5
a = [13]
```

The wall needs two full rolls for 10 meters and one additional roll for the remaining 3 meters. The answer is `3`, not `2`, because the leftover 2 meters from that last roll cannot be reused.

Another easy mistake appears when the wall width is already divisible by `k`.

```
n = 1, k = 5
a = [10]
```

The answer is `2`, not `3`. No extra roll is needed because there is no uncovered remainder.

A final edge case is `k = 1`.

```
n = 1, k = 1
a = [7]
```

Every roll covers exactly one meter, so the answer is `7`. Since every width is divisible by 1, there are never any partially used rolls.

The number of rolls needed for a wall is exactly the ceiling of `a_i / k`.

## Approaches

The most direct way to think about a single wall is to repeatedly subtract `k` from its width until nothing remains. Every subtraction corresponds to one roll. This is correct because each roll contributes at most `k` meters of width.

For a wall of width `a_i`, this requires roughly `a_i / k` iterations. Since `a_i` may be as large as `10^9`, a single wall could already require a billion operations. With up to `10^6` walls, this approach is completely infeasible.

The observation is that repeated subtraction is simply computing a ceiling division.

If a wall width is `a_i`, then:

```
rolls = ceil(a_i / k)
```

When `a_i` is divisible by `k`, every roll is used fully.

When `a_i` leaves a remainder, all complete blocks of width `k` use full rolls, and one extra roll is needed for the remaining part.

So the answer becomes:

```
sum(ceil(a_i / k))
```

Using integer arithmetic:

```
ceil(a_i / k) = (a_i + k - 1) // k
```

We evaluate this formula for every wall and accumulate the result.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(Σ(a_i / k)) | O(1) | Too slow |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read `n` and `k`.
2. Read all wall widths.
3. Initialize `answer = 0`.
4. For each wall width `a`:

Compute

```
rolls = (a + k - 1) // k
```

This is the integer form of `ceil(a / k)`.
5. Add `rolls` to `answer`.
6. After processing all walls, print `answer`.

### Why it works

For any wall width `a`, write:

```
a = qk + r
```

where `0 ≤ r < k`.

If `r = 0`, exactly `q` full rolls cover the wall.

If `r > 0`, `q` full rolls cover `qk` width, and one additional roll is required to cover the remaining `r` width.

So the number of rolls is:

```
q            if r = 0
q + 1        if r > 0
```

which is precisely `ceil(a / k)`.

Since walls are independent and leftovers cannot be reused between walls, the total answer is the sum of these values over all walls.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, k = map(int, input().split())
a = map(int, input().split())

ans = 0
for x in a:
    ans += (x + k - 1) // k

print(ans)
```

The program performs a single pass through the wall widths.

The expression `(x + k - 1) // k` implements ceiling division using only integers. This avoids floating-point arithmetic and works correctly even for very large values.

The answer can become larger than `10^9`, because there may be up to `10^6` walls. Python integers automatically handle such values safely.

No additional arrays or data structures are needed beyond the input itself, so memory usage remains constant.

## Worked Examples

### Example 1

Input:

```
4 5
10 13 20 21
```

| Wall Width | Calculation | Rolls | Running Total |
| --- | --- | --- | --- |
| 10 | (10 + 4) // 5 | 2 | 2 |
| 13 | (13 + 4) // 5 | 3 | 5 |
| 20 | (20 + 4) // 5 | 4 | 9 |
| 21 | (21 + 4) // 5 | 5 | 14 |

Output:

```
14
```

This example contains both divisible and non-divisible widths. The wall of width 21 demonstrates why a remainder requires one extra roll.

### Example 2

Input:

```
4 8
8 16 32 33
```

| Wall Width | Calculation | Rolls | Running Total |
| --- | --- | --- | --- |
| 8 | (8 + 7) // 8 | 1 | 1 |
| 16 | (16 + 7) // 8 | 2 | 3 |
| 32 | (32 + 7) // 8 | 4 | 7 |
| 33 | (33 + 7) // 8 | 5 | 12 |

Output:

```
12
```

The first three walls divide evenly by 8. The last wall has a remainder of 1, which still requires a full extra roll.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | One constant-time computation per wall |
| Space | O(1) | Only a few variables are maintained |

With up to `10^6` walls, a linear scan is exactly what the constraints require. The solution easily fits within typical contest limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    n, k = map(int, input().split())
    arr = map(int, input().split())

    ans = 0
    for x in arr:
        ans += (x + k - 1) // k

    return str(ans)

# provided samples
assert run("4 5\n10 13 20 21\n") == "14", "sample 1"
assert run("3 1\n5 6 3\n") == "14", "sample 2"
assert run("4 8\n8 16 32 33\n") == "12", "sample 3"

# custom cases
assert run("1 5\n1\n") == "1", "minimum wall"
assert run("1 5\n10\n") == "2", "exact multiple"
assert run("3 7\n7 7 7\n") == "3", "all equal"
assert run("2 1000000\n1000000000 999999999\n") == "2000", "large values"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 5 / 1` | `1` | Smallest non-zero wall |
| `1 5 / 10` | `2` | Exact divisibility |
| `3 7 / 7 7 7` | `3` | Repeated equal values |
| `2 1000000 / 1000000000 999999999` | `2000` | Large-number arithmetic |

## Edge Cases

Consider:

```
1 5
10
```

The algorithm computes:

```
(10 + 4) // 5 = 2
```

There is no remainder, so no extra roll is added. The output is:

```
2
```

which is correct.

Now consider:

```
1 5
13
```

The algorithm computes:

```
(13 + 4) // 5 = 3
```

Two rolls cover 10 meters, and a third roll supplies the remaining 3 meters. The output is:

```
3
```

which matches the statement's restriction that a partially used roll cannot be reused.

Finally:

```
1 1
7
```

The algorithm computes:

```
(7 + 0) // 1 = 7
```

Every roll covers exactly one meter, so seven rolls are required. The output is:

```
7
```

This confirms that the ceiling-division formula also handles the smallest possible roll width correctly.

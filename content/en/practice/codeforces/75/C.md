---
title: "CF 75C - Modified GCD"
description: "We are given two positive integers, and then many range queries. For each query [low, high], we must find the largest integer inside that interval that divides both numbers. The first observation is that we are not really working with a and b independently."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "number-theory"]
categories: ["algorithms"]
codeforces_contest: 75
codeforces_index: "C"
codeforces_contest_name: "Codeforces Beta Round 67 (Div. 2)"
rating: 1600
weight: 75
solve_time_s: 100
verified: true
draft: false
---

[CF 75C - Modified GCD](https://codeforces.com/problemset/problem/75/C)

**Rating:** 1600  
**Tags:** binary search, number theory  
**Solve time:** 1m 40s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given two positive integers, and then many range queries. For each query `[low, high]`, we must find the largest integer inside that interval that divides both numbers.

The first observation is that we are not really working with `a` and `b` independently. Any number that divides both must also divide `gcd(a, b)`. Once we compute the gcd of the two numbers, every valid answer becomes one of its divisors.

The input size strongly hints that queries must be answered quickly. The numbers themselves can reach `10^9`, which makes iterating through every integer in a query range impossible. A single query interval might contain a billion numbers. With up to `10^4` queries, even an `O(high - low)` approach per query would be catastrophic.

At the same time, `10^9` is small enough that enumerating divisors of a number is feasible. A number up to `10^9` has at most around a few thousand divisors. Finding all divisors by checking integers up to `sqrt(g)` is fast enough because `sqrt(10^9)` is roughly `31623`.

The tricky part is handling the range condition correctly. We do not want just any divisor of the gcd. We want the largest divisor that lies inside `[low, high]`.

There are several edge cases that can quietly break incorrect implementations.

Suppose:

```
a = 12
b = 18
query = [7, 11]
```

The gcd is `6`, whose divisors are `{1, 2, 3, 6}`. None lie inside the interval, so the answer is `-1`. A careless implementation that only searches downward from `high` without checking divisibility carefully may accidentally return `6`, even though it is outside the range.

Another subtle case appears when the answer equals the lower boundary:

```
a = 100
b = 50
query = [25, 30]
```

The common divisors are `{1, 2, 5, 10, 25, 50}`. The correct answer is `25`. If binary search boundaries are handled incorrectly, it is easy to skip exact matches and return `-1`.

Perfect squares also need attention while generating divisors.

```
gcd = 36
```

While iterating with `i = 6`, both `i` and `gcd // i` are the same divisor. Adding both blindly duplicates `6`. The algorithm still works if duplicates are later sorted, but unnecessary duplication complicates reasoning and wastes time.

Finally, consider when the gcd itself is inside the range:

```
a = 9
b = 27
query = [9, 11]
```

The answer is immediately `9`. Some incorrect solutions search for divisors strictly smaller than `high`, which misses this exact-boundary case.

## Approaches

The most direct approach is to process each query independently. For a query `[low, high]`, we could iterate downward from `high` to `low` and check whether each number divides both `a` and `b`.

That works because the first valid number encountered is automatically the largest valid divisor in the interval.

The problem is the running time. In the worst case, a query range may contain nearly `10^9` numbers. With `10^4` queries, this becomes completely impossible.

The key observation is that every common divisor of `a` and `b` must divide `g = gcd(a, b)`.

Instead of searching through the interval itself, we can precompute all divisors of `g`. This changes the problem from:

"Find an integer in the range that divides both numbers"

to:

"Find the largest divisor of `g` inside the range."

That is much smaller. A number up to `10^9` has very few divisors compared to its size. We can generate all divisors in `O(sqrt(g))`, sort them once, and then answer each query using binary search.

For a query `[low, high]`, we binary search for the largest divisor `<= high`. If that divisor is still at least `low`, it is the answer. Otherwise no valid divisor exists.

The brute-force works because checking divisibility is simple and correct, but it fails because it searches an enormous numeric range. The divisor-based solution succeeds because the set of possible answers is tiny and fixed across all queries.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n × range size) | O(1) | Too slow |
| Optimal | O(sqrt(g) + n log d) | O(d) | Accepted |

Here, `g = gcd(a, b)` and `d` is the number of divisors of `g`.

## Algorithm Walkthrough

1. Read the integers `a` and `b`.
2. Compute `g = gcd(a, b)`.

Every common divisor of `a` and `b` must divide `g`, so all valid answers come from the divisors of `g`.
3. Generate all divisors of `g`.

Iterate from `1` to `sqrt(g)`. Whenever `i` divides `g`, both `i` and `g // i` are divisors.
4. Avoid duplicate insertion when `i * i == g`.

Perfect squares produce the same divisor twice, so we only insert it once.
5. Sort the divisor list.

Binary search requires sorted order.
6. For each query `[low, high]`, binary search for the largest divisor `<= high`.

In Python, `bisect_right(divs, high) - 1` gives the index of the largest divisor not exceeding `high`.
7. Check whether this divisor is still at least `low`.

If yes, print it. Otherwise print `-1`.

### Why it works

The algorithm relies on one property:

A number divides both `a` and `b` if and only if it divides `gcd(a, b)`.

That means the complete set of possible answers is exactly the divisor set of `g`. By sorting those divisors, binary search can always locate the largest divisor not exceeding `high`. If that value is also at least `low`, it lies inside the required interval and is the largest possible valid answer. If it is smaller than `low`, then every earlier divisor is even smaller, so no valid divisor exists in the interval.

## Python Solution

```python
import sys
from math import gcd, isqrt
from bisect import bisect_right

input = sys.stdin.readline

def solve():
    a, b = map(int, input().split())

    g = gcd(a, b)

    divisors = []

    for i in range(1, isqrt(g) + 1):
        if g % i == 0:
            divisors.append(i)

            other = g // i
            if other != i:
                divisors.append(other)

    divisors.sort()

    q = int(input())

    for _ in range(q):
        low, high = map(int, input().split())

        idx = bisect_right(divisors, high) - 1

        if idx >= 0 and divisors[idx] >= low:
            print(divisors[idx])
        else:
            print(-1)

solve()
```

The solution begins by collapsing the original problem into a gcd problem. Once `g = gcd(a, b)` is computed, every valid answer must come from its divisors.

The divisor generation loop runs only up to `sqrt(g)`. Whenever `i` divides `g`, we immediately know that `g // i` is also a divisor. This pair-generation trick reduces the complexity from linear to square root time.

The condition:

```
if other != i:
```

handles perfect squares correctly. Without it, divisors like `6` in `36` would be inserted twice.

After sorting the divisor list, each query becomes a binary search problem. `bisect_right(divisors, high)` returns the insertion position after all values `<= high`. Subtracting one gives the index of the largest valid candidate.

The boundary check:

```
divisors[idx] >= low
```

is essential. The binary search only guarantees the divisor is at most `high`. We still must confirm it lies inside the interval.

The implementation uses `isqrt` instead of floating-point square roots. Integer square roots avoid precision issues and are cleaner for divisor enumeration.

## Worked Examples

### Example 1

Input:

```
9 27
3
1 5
10 11
9 11
```

The gcd is:

```
gcd(9, 27) = 9
```

Divisors of `9`:

```
[1, 3, 9]
```

| Query | Largest divisor ≤ high | Candidate | Valid? | Answer |
| --- | --- | --- | --- | --- |
| [1, 5] | 3 | 3 | 3 ≥ 1 | 3 |
| [10, 11] | 9 | 9 | 9 < 10 | -1 |
| [9, 11] | 9 | 9 | 9 ≥ 9 | 9 |

This example demonstrates the core binary-search logic. The second query shows why we must still compare against `low` after locating the largest divisor not exceeding `high`.

### Example 2

Input:

```
100 80
4
1 2
5 15
16 25
41 50
```

The gcd is:

```
gcd(100, 80) = 20
```

Divisors of `20`:

```
[1, 2, 4, 5, 10, 20]
```

| Query | Largest divisor ≤ high | Candidate | Valid? | Answer |
| --- | --- | --- | --- | --- |
| [1, 2] | 2 | 2 | 2 ≥ 1 | 2 |
| [5, 15] | 10 | 10 | 10 ≥ 5 | 10 |
| [16, 25] | 20 | 20 | 20 ≥ 16 | 20 |
| [41, 50] | 20 | 20 | 20 < 41 | -1 |

This trace shows that the algorithm never scans the interval itself. Even for large ranges, it only searches among the divisors of the gcd.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(sqrt(g) + n log d) | `sqrt(g)` to generate divisors, binary search per query |
| Space | O(d) | storing all divisors of the gcd |

Here `g = gcd(a, b)` and `d` is the number of divisors of `g`.

The maximum square root is about `31623`, which is tiny for a 2-second limit. The divisor count is also small, so each query finishes in logarithmic time over a very short array. The solution easily fits both time and memory constraints.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io
from math import gcd, isqrt
from bisect import bisect_right

def solve():
    input = sys.stdin.readline

    a, b = map(int, input().split())

    g = gcd(a, b)

    divisors = []

    for i in range(1, isqrt(g) + 1):
        if g % i == 0:
            divisors.append(i)

            other = g // i
            if other != i:
                divisors.append(other)

    divisors.sort()

    q = int(input())

    out = []

    for _ in range(q):
        low, high = map(int, input().split())

        idx = bisect_right(divisors, high) - 1

        if idx >= 0 and divisors[idx] >= low:
            out.append(str(divisors[idx]))
        else:
            out.append("-1")

    print("\n".join(out))

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    return sys.stdout.getvalue()

# provided sample
assert run(
"""9 27
3
1 5
10 11
9 11
"""
) == "3\n-1\n9\n", "sample 1"

# minimum-size input
assert run(
"""1 1
1
1 1
"""
) == "1\n", "minimum case"

# no divisor in range
assert run(
"""12 18
1
7 11
"""
) == "-1\n", "no valid divisor"

# exact lower-bound answer
assert run(
"""100 50
1
25 30
"""
) == "25\n", "boundary inclusion"

# perfect square gcd
assert run(
"""36 72
2
6 6
7 8
"""
) == "6\n-1\n", "perfect square divisor handling"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1` with query `[1,1]` | `1` | Minimum constraints |
| `12 18` with query `[7,11]` | `-1` | No divisor exists in range |
| `100 50` with query `[25,30]` | `25` | Inclusive lower boundary |
| `36 72` with queries `[6,6]` and `[7,8]` | `6`, `-1` | Perfect square handling and missing intervals |

## Edge Cases

Consider the case where no divisor lies inside the interval:

```
12 18
1
7 11
```

The gcd is `6`, whose divisors are `[1, 2, 3, 6]`.

Binary search for the largest divisor `<= 11` returns `6`. The algorithm then checks whether `6 >= 7`. That fails, so the output becomes `-1`.

This extra boundary check prevents returning divisors outside the requested interval.

Now consider an exact-boundary answer:

```
100 50
1
25 30
```

The gcd is `50`, whose divisors are `[1, 2, 5, 10, 25, 50]`.

Binary search for the largest divisor `<= 30` returns `25`. Since `25 >= 25`, the algorithm outputs `25`.

This confirms that intervals are inclusive on both ends.

Finally, consider a perfect square gcd:

```
36 72
1
6 6
```

The gcd is `36`.

During divisor generation, when `i = 6`, both `i` and `36 // 6` equal `6`. The implementation inserts it only once because of:

```
if other != i:
```

The divisor list remains correct:

```
[1, 2, 3, 4, 6, 9, 12, 18, 36]
```

Binary search then correctly finds `6` for the interval `[6, 6]`.

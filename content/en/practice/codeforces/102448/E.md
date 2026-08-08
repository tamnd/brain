---
title: "CF 102448E - Everybody loves acai"
description: "Each restaurant gives Gabriel an integer (k), representing the maximum amount of açaí he can put into his bowl. He wants the largest positive integer not exceeding (k) whose proper divisors add up exactly to the number itself. If no such number exists, the answer is (-1)."
date: "2026-08-09T02:06:20+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102448
codeforces_index: "E"
codeforces_contest_name: "UFPE Starters Final Try-Outs 2020"
rating: 0
weight: 102448
solve_time_s: 483
verified: true
draft: false
---

[CF 102448E - Everybody loves acai](https://codeforces.com/problemset/problem/102448/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 8m 3s  
**Verified:** yes  

## Solution
## Problem Understanding

Each restaurant gives Gabriel an integer (k), representing the maximum amount of açaí he can put into his bowl. He wants the largest positive integer not exceeding (k) whose proper divisors add up exactly to the number itself. If no such number exists, the answer is (-1).

For example, (6) is perfect because its proper divisors are (1,2,3), and (1+2+3=6). Thus a restaurant offering (8) can provide a perfect bowl of size (6), while a restaurant offering (5) cannot provide any perfect bowl.

The input can contain up to (2\cdot10^6) restaurants, and every amount is at most (2\cdot10^6). The number of queries is large enough that doing substantial number theory separately for every restaurant is not viable. Even an (O(\sqrt{k})) perfect-number test would already require around (1400) divisor checks for a single number near the upper bound, and searching through many candidates would multiply that cost dramatically.

The crucial fact is that the range is tiny compared with the scale on which perfect numbers occur. The first perfect numbers are (6,28,496,8128), while the next one is (33,550,336), already far above the problem's maximum of (2\cdot10^6).

There is also no hidden odd perfect number in this range. In fact, the existence of odd perfect numbers is still an open problem, but any such number has been proved to be greater than (10^{1500}). Consequently, the only perfect numbers relevant to this problem are exactly (6,28,496,8128).

Several small boundaries are easy to mishandle. For input `1`, the answer is `-1`, because (1) has no proper positive divisors, so its divisor sum is (0). For input `6`, the answer is `6`, because the upper bound itself may be perfect. For input `7`, the answer is still `6`, because we need the largest perfect number less than or equal to the restaurant's amount, not a perfect number strictly smaller than it. Finally, for input `2000000`, the answer is `8128`, because the next perfect number is already outside the allowed range.

For example, the input

```
1
1
```

must produce

```
-1
```

A careless implementation that treats (1) as perfect because every number is divisible by itself would be using the wrong divisor definition.

Similarly,

```
1
6
```

must produce

```
6
```

An implementation that searches only for a perfect number strictly below (k) would incorrectly return (-1).

## Approaches

A direct approach would process every restaurant independently. Starting from (k), we could test (k,k-1,k-2,\ldots) until finding a perfect number. To test a candidate (x), we can enumerate divisors up to (\sqrt{x}), adding both members of every divisor pair. This is correct because every proper divisor either appears directly in that range or is paired with a complementary divisor.

The problem is the amount of repeated work. For a query with (k=2\cdot10^6), the search stops only when it reaches (8128), so it tests roughly (2\cdot10^6-8128) candidates. Each candidate takes (O(\sqrt{x})) work, giving roughly

[
\sum_{x=8129}^{2\cdot10^6}\sqrt{x},
]

which is about (1.9\cdot10^9) divisor iterations for just one worst-case query. With (2\cdot10^6) restaurants, the worst-case work is on the order of (10^{15}), far beyond the time limit.

The brute force works because testing a candidate tells us exactly whether that candidate is perfect, but it fails because the same candidates are rediscovered for millions of queries. The observation that the entire input range contains only four perfect numbers changes the problem completely. Instead of searching downward for every restaurant, we store the sorted list

[
[6,28,496,8128].
]

For each (k), we only need the largest element of this list that is at most (k). Since the list contains four elements, this is effectively constant time.

A binary search is convenient because it directly expresses the query as "find the rightmost perfect number not exceeding (k)." With only four values, even a linear scan would be fast enough, but binary search makes the boundary condition explicit and keeps the approach general if the precomputed list were larger.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(nM^{3/2})) in the worst case | (O(1)) | Too slow |
| Optimal | (O(n\log 4)=O(n)) | (O(1)) | Accepted |

Here (M=2\cdot10^6). The optimal solution is effectively linear in the number of restaurants.

## Algorithm Walkthrough

1. Store the only perfect numbers that can occur within the allowed amount range: `6`, `28`, `496`, and `8128`. The next perfect number is (33,550,336), so there is nothing else to consider.
2. Read the amount (k) for the current restaurant. We need the greatest stored perfect number that satisfies (p\le k).
3. Use `bisect_right` on the sorted perfect-number list. It returns the position immediately after all values less than or equal to (k). Moving one position to the left gives exactly the largest valid perfect number.
4. If the resulting position is negative, then (k<6), so no perfect bowl exists and we output `-1`. Otherwise, output the perfect number at that position.
5. Repeat the same constant-size lookup for all restaurants and write the answers in their original order.

### Why it works

The invariant is that the stored list contains every perfect number that can possibly be an answer for an input value. For any restaurant amount (k), a valid answer must be one of those four numbers and must not exceed (k). `bisect_right` selects the greatest such number, so the returned value is both valid and maximal. If every stored perfect number exceeds (k), no valid answer exists, and `-1` is correct.

## Python Solution

```python
import sys
from bisect import bisect_right

input = sys.stdin.readline

# The only perfect numbers <= 2 * 10^6.
PERFECT = (6, 28, 496, 8128)

def solve():
    n = int(input())
    out = bytearray()

    for _ in range(n):
        k = int(input())
        pos = bisect_right(PERFECT, k) - 1

        if pos < 0:
            out.extend(b"-1\n")
        else:
            out.extend(str(PERFECT[pos]).encode())
            out.append(10)

    sys.stdout.write(out.decode())

if __name__ == "__main__":
    solve()
```

The tuple `PERFECT` is sorted, which is required by `bisect_right`. Since the tuple has only four elements, the binary search takes at most a few comparisons regardless of the size of (k).

The subtraction by one after `bisect_right` handles the upper boundary correctly. If (k=6), `bisect_right` returns the position after `6`, so the preceding position contains `6` itself. If (k=7), it returns the same insertion position, and the preceding element is still `6`. If (k=5), it returns zero, so subtracting one gives `-1`.

The output is accumulated in a `bytearray` instead of storing two million Python strings in a list. This keeps memory usage low and reduces the number of output operations. Python's arbitrary-size integers also remove any integer-overflow concern, although all values here are small enough that ordinary machine integers would already suffice.

The input is processed one line at a time rather than using `read().split()`. With two million queries, materializing every input token simultaneously would consume substantially more memory than necessary.

## Worked Examples

For Sample 1, the perfect-number list is `[6, 28, 496, 8128]`.

| Restaurant | (k) | `bisect_right(PERFECT, k)` | Position after `-1` | Answer |
| --- | --- | --- | --- | --- |
| 1 | 8 | 1 | 0 | 6 |
| 2 | 5 | 0 | -1 | -1 |

For (k=8), only `6` is at most the available amount, so the answer is `6`. For (k=5), even the smallest perfect number is too large, so the answer is `-1`. This demonstrates both the ordinary predecessor query and the "no valid value" boundary.

For Sample 2, the statement's second example is a single restaurant with (k=5).

| Restaurant | (k) | `bisect_right(PERFECT, k)` | Position after `-1` | Answer |
| --- | --- | --- | --- | --- |
| 1 | 5 | 0 | -1 | -1 |

The search does not accidentally consider `6`, because `bisect_right` only includes values that are at most (5). This is exactly the inequality required by the problem.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(n\log 4)=O(n)) | Each restaurant performs a binary search over four fixed values. |
| Space | (O(1)) auxiliary space | The perfect-number list is fixed, and output storage is proportional to the required output size. |

With (n\le2\cdot10^6), the algorithm performs only a few comparisons per restaurant. There is no divisor enumeration, factorization, sieve, or per-query search through the integer range. The fixed-size number-theory preprocessing makes the solution easily compatible with the 3 second time limit and 256 MB memory limit. The original problem limits are (2\cdot10^6) restaurants and (2\cdot10^6) as the maximum amount.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io
from bisect import bisect_right

PERFECT = (6, 28, 496, 8128)
input = sys.stdin.readline

def solve():
    n = int(input())
    out = bytearray()

    for _ in range(n):
        k = int(input())
        pos = bisect_right(PERFECT, k) - 1

        if pos < 0:
            out.extend(b"-1\n")
        else:
            out.extend(str(PERFECT[pos]).encode())
            out.append(10)

    sys.stdout.write(out.decode())

def run(inp: str) -> str:
    global input

    old_stdin = sys.stdin
    old_stdout = sys.stdout
    old_input = input

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()
    input = sys.stdin.readline

    try:
        solve()
        return sys.stdout.getvalue()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout
        input = old_input

# Provided sample 1
assert run("2\n8\n5\n") == "6\n-1\n", "sample 1"

# Provided sample 2
assert run("1\n5\n") == "-1\n", "sample 2"

# Minimum-size input
assert run("1\n1\n") == "-1\n", "minimum value"

# Exact perfect numbers and their immediate successors
assert run(
    "8\n"
    "6\n"
    "7\n"
    "28\n"
    "29\n"
    "496\n"
    "497\n"
    "8128\n"
    "8129\n"
) == (
    "6\n"
    "6\n"
    "28\n"
    "28\n"
    "496\n"
    "496\n"
    "8128\n"
    "8128\n"
), "perfect-number boundaries"

# All-equal values
assert run("5\n2000000\n2000000\n2000000\n2000000\n2000000\n") == (
    "8128\n8128\n8128\n8128\n8128\n"
), "all equal"

# Maximum number of restaurants
maximum_input = "2000000\n" + "2000000\n" * 2000000
maximum_output = "8128\n" * 2000000
assert run(maximum_input) == maximum_output, "maximum n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 1` | `-1` | Smallest possible amount and absence of a perfect number. |
| `6, 7, 28, 29, 496, 497, 8128, 8129` | `6, 6, 28, 28, 496, 496, 8128, 8128` | Exact matches and the predecessor immediately after every perfect number. |
| Five copies of `2000000` | Five copies of `8128` | Values above the largest relevant perfect number and repeated queries. |
| Two million copies of `2000000` | Two million copies of `8128` | Maximum input size, output handling, and all-equal values. |

## Edge Cases

For the smallest amount, consider

```
1
1
```

`bisect_right` returns `0` because every perfect number is larger than `1`. After subtracting one, the position is `-1`, so the algorithm outputs `-1`. This avoids incorrectly treating the number itself as a proper divisor.

For an exact perfect number, consider

```
1
28
```

The insertion position returned by `bisect_right` is the position after `28`. Subtracting one selects `28`, so the output is

```
28
```

The use of `bisect_right`, rather than `bisect_left`, is what makes equality work correctly.

For a value immediately above a perfect number, consider

```
1
29
```

The search still selects `28`, because `29` itself is not perfect and the required answer must not exceed the restaurant's amount. The output is

```
28
```

For the maximum possible amount,

```
1
2000000
```

the search reaches `8128`. The next perfect number is (33,550,336), so no larger perfect number is allowed by the input range. The output is

```
8128
```

Finally, for the maximum number of restaurants, every query is independent. Even if all two million restaurants contain exactly `2000000`, each query performs only a four-element binary search. The algorithm never scales with the numerical distance between `k` and the nearest perfect number, which is the property that makes the solution fast enough for the largest input.

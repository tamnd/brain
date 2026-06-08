---
title: "CF 2067B - Two Large Bags"
description: "We start with an array of n numbers in the first bag and an empty second bag. Since the final bags must be identical, each bag must end up containing exactly n/2 numbers. There are only two allowed operations."
date: "2026-06-09T03:38:01+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "dp", "greedy", "sortings"]
categories: ["algorithms"]
codeforces_contest: 2067
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 1004 (Div. 2)"
rating: 1200
weight: 2067
solve_time_s: 136
verified: true
draft: false
---

[CF 2067B - Two Large Bags](https://codeforces.com/problemset/problem/2067/B)

**Rating:** 1200  
**Tags:** brute force, dp, greedy, sortings  
**Solve time:** 2m 16s  
**Verified:** yes  

## Solution
## Problem Understanding

We start with an array of `n` numbers in the first bag and an empty second bag. Since the final bags must be identical, each bag must end up containing exactly `n/2` numbers.

There are only two allowed operations.

The first operation moves a number from the first bag into the second bag.

The second operation increases a number in the first bag by one, but only if the current value already exists in the second bag.

The question is whether we can perform any sequence of such operations so that, in the end, the two bags contain exactly the same multiset of numbers.

The values satisfy `1 ≤ a[i] ≤ n`, and `n ≤ 1000`. The sum of `n²` over all test cases is at most `10^6`, which is a strong hint that an `O(n²)` solution is completely acceptable. We do not need anything sophisticated such as logarithmic data structures or advanced dynamic programming.

The tricky part is understanding what the increment operation really allows.

Suppose the second bag contains the value `x`. Then any occurrence of `x` remaining in the first bag may be turned into `x+1`. If the second bag also contains `x+1`, that new value may later be increased again. This means a value can be pushed upward through a chain of consecutive values, but every step requires that the current value already exists in the second bag.

A common mistake is to think only about frequency parity. For example:

```
4
1 1 2 2
```

The answer is `YES`. Move one `1` and one `2` to the second bag. The bags are already identical.

But parity alone is not enough:

```
4
1 1 1 4
```

The answer is `NO`.

Even though some frequencies are even, there is no way to create another `4`. Incrementing requires intermediate values to exist in the second bag, and there is no chain connecting `1` to `4`.

Another easy pitfall is forgetting that increments only move upward. Consider:

```
4
2 2 3 4
```

The answer is `NO`.

We can create larger numbers from smaller ones, but we can never decrease `4` to `3` or `2`.

Understanding these constraints is the key to the solution.

## Approaches

A brute-force viewpoint is to think about every possible choice of which `n/2` elements are moved into the second bag, then simulate all legal increment operations. This is correct in principle because every valid final state corresponds to some sequence of moves and increments.

The problem is the number of possibilities. Choosing `n/2` elements out of `n` already gives

$$\binom{n}{n/2}$$

possibilities, which is enormous even for moderate `n`. For `n = 1000`, this is completely impossible.

To make progress, we need to understand the structure of legal transformations.

Sort the array and think only about frequencies of each value.

Suppose a value `x` appears only once. Eventually one copy must be placed in each bag, because the final bags are identical. With only one copy available, this is impossible. The only hope is to increase that lone copy into a larger value before the final split.

Now consider a value that appears at least twice. We may place one copy into the second bag and keep another in the first bag. This effectively "locks in" the value `x`, because once `x` exists in the second bag, remaining copies of `x` can be increased to `x+1`.

This suggests processing values from left to right. Whenever a value appears at least twice, we can reserve one pair and push all extra copies forward to the next value. The forwarded copies represent numbers that can be incremented.

The crucial observation is that a value with odd frequency cannot be fixed locally. One copy must be carried forward. A value with frequency one is fatal because there is no pair available to anchor that value in both bags.

This leads to a very simple greedy simulation on frequencies.

Let `cnt[x]` be the number of occurrences of value `x`.

Process values in increasing order.

If `cnt[x] == 1`, the answer is immediately `NO`.

Otherwise, after forming as many pairs of value `x` as possible, any excess copies can be pushed to value `x+1`. Operationally, this is equivalent to adding

$$cnt[x] - 2$$

to `cnt[x+1]` whenever `cnt[x] ≥ 2`.

This exactly matches the effect of keeping one pair of `x` and incrementing every remaining copy.

At the end, if no frequency one was encountered, the construction succeeds.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | Exponential | Too slow |
| Optimal Greedy Frequency Simulation | O(n²) | O(n) | Accepted |

## Algorithm Walkthrough

1. Count the frequency of every value.
2. Process values from `1` up to `n`.
3. If the current frequency is exactly `1`, return `"NO"`.

A single copy cannot be split between the two bags, and there is no pair available to anchor this value.
4. If the current frequency is at least `2`, keep one pair of that value.

These two copies represent the final occurrence of this value in both bags.
5. Any remaining copies are forwarded to the next value.

Add `cnt[x] - 2` to `cnt[x+1]`.

This models incrementing surplus copies of `x` into `x+1`.
6. Continue until all values have been processed.
7. If no frequency one was encountered, return `"YES"`.

### Why it works

When processing value `x`, the only way to make `x` appear in both final bags is to reserve at least two copies of `x`. One copy goes to each bag.

If only one copy exists, this is impossible. No future operation can create another `x`, because increments only increase values.

When at least two copies exist, keeping exactly two is always optimal. Any extra copies cannot help produce additional `x` values, so the only useful action is to increment them. Incrementing moves them into the frequency count of `x+1`, which is exactly what the simulation does.

Processing values in increasing order preserves all reachable states. Every surplus copy is pushed as far right as needed through consecutive values. If the algorithm never encounters a frequency of one, then every value can be anchored by a pair and all excess copies can be propagated forward. Hence a valid construction exists.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())

    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))

        cnt = [0] * (n + n + 5)

        for x in a:
            cnt[x] += 1

        ok = True

        for x in range(1, n + 1):
            if cnt[x] == 1:
                ok = False
                break

            if cnt[x] >= 2:
                cnt[x + 1] += cnt[x] - 2

        print("YES" if ok else "NO")

solve()
```

The first part builds a frequency table.

The main loop processes values from smallest to largest. A frequency of one immediately proves impossibility, because one copy cannot appear in both final bags.

When the frequency is at least two, two copies are reserved and every remaining copy is transferred to the next value. This corresponds exactly to incrementing surplus occurrences.

The frequency array is allocated larger than `n + 1` because surplus copies may be pushed beyond the original maximum value. Using a slightly oversized array avoids boundary issues.

One subtle point is that we never explicitly subtract two from `cnt[x]`. After processing value `x`, that frequency is never used again. Only the surplus amount `cnt[x] - 2` matters, so directly adding that quantity to `cnt[x+1]` is sufficient.

## Worked Examples

### Example 1

Input:

```
6
3 3 4 5 3 3
```

Initial frequencies:

| Value | Frequency |
| --- | --- |
| 3 | 4 |
| 4 | 1 |
| 5 | 1 |

Processing:

| x | cnt[x] before | Action | cnt[x+1] added |
| --- | --- | --- | --- |
| 1 | 0 | Skip | 0 |
| 2 | 0 | Skip | 0 |
| 3 | 4 | Keep two copies | 2 |
| 4 | 3 | Keep two copies | 1 |
| 5 | 2 | Keep two copies | 0 |

No frequency one appears during processing after propagation, so the answer is:

```
YES
```

This example shows how surplus copies of `3` create extra copies of `4`, which in turn create extra copies of `5`.

### Example 2

Input:

```
4
2 3 4 4
```

Initial frequencies:

| Value | Frequency |
| --- | --- |
| 2 | 1 |
| 3 | 1 |
| 4 | 2 |

Processing:

| x | cnt[x] before | Result |
| --- | --- | --- |
| 1 | 0 | Continue |
| 2 | 1 | Fail |

The moment we encounter a frequency of one, the answer becomes:

```
NO
```

This demonstrates the key obstruction. A lone value cannot be represented in both final bags.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | One frequency pass and one linear scan |
| Space | O(n) | Frequency array |

The total work is comfortably within the limits. Even across all test cases, the input guarantee that the sum of `n²` is at most `10^6` is far larger than what this linear solution requires.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    out = []

    t = int(input())

    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))

        cnt = [0] * (2 * n + 5)

        for x in a:
            cnt[x] += 1

        ok = True

        for x in range(1, n + 1):
            if cnt[x] == 1:
                ok = False
                break

            if cnt[x] >= 2:
                cnt[x + 1] += cnt[x] - 2

        out.append("YES" if ok else "NO")

    return "\n".join(out) + "\n"

# provided sample
assert run(
"""9
2
1 1
2
2 1
4
1 1 4 4
4
3 4 3 3
4
2 3 4 4
6
3 3 4 5 3 3
6
2 2 2 4 4 4
8
1 1 1 1 1 1 1 4
10
9 9 9 10 10 10 10 10 10 10
"""
) == """YES
NO
YES
YES
NO
YES
NO
YES
YES
"""

# minimum size, possible
assert run(
"""1
2
1 1
"""
) == """YES
"""

# minimum size, impossible
assert run(
"""1
2
1 2
"""
) == """NO
"""

# all values equal
assert run(
"""1
8
3 3 3 3 3 3 3 3
"""
) == """YES
"""

# frequency one appears after propagation
assert run(
"""1
4
1 1 1 4
"""
) == """NO
"""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2 / 1 1` | YES | Smallest successful instance |
| `2 / 1 2` | NO | Smallest failing instance |
| Eight equal values | YES | Large surplus propagation |
| `1 1 1 4` | NO | Frequency-one obstruction after transfers |

## Edge Cases

Consider:

```
2
1 2
```

The frequencies are `{1:1, 2:1}`. The algorithm immediately sees `cnt[1] = 1` and returns `NO`.

This is correct because one copy of `1` cannot be placed into both final bags.

Consider:

```
4
1 1 1 4
```

The frequencies start as `{1:3, 4:1}`.

Processing value `1` forwards one surplus copy, producing frequency `1` at value `2`.

The table becomes:

| Value | Frequency |
| --- | --- |
| 1 | 3 |
| 2 | 1 |
| 4 | 1 |

When value `2` is processed, the algorithm finds a frequency of one and returns `NO`.

This matches reality. Although there are many copies of `1`, there is no continuous chain of anchored values that would allow creation of another `4`.

Consider:

```
8
1 1 1 1 1 1 1 4
```

Processing proceeds as:

| x | cnt[x] |
| --- | --- |
| 1 | 7 |
| 2 | 5 |
| 3 | 3 |
| 4 | 2 |

Every frequency is at least two, so the algorithm returns `YES`.

The surplus copies of `1` create enough `2`s, those create enough `3`s, and those create enough `4`s. This is exactly the kind of chain that the increment operation enables.

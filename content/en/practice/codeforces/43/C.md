---
title: "CF 43C - Lucky Tickets"
description: "We are given a collection of ticket pieces. Each piece is a number, representing the fragment of a ticket that was origi"
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "greedy"]
categories: ["algorithms"]
codeforces_contest: 43
codeforces_index: "C"
codeforces_contest_name: "Codeforces Beta Round 42 (Div. 2)"
rating: 1300
weight: 43
solve_time_s: 72
verified: true
draft: false
---

[CF 43C - Lucky Tickets](https://codeforces.com/problemset/problem/43/C)

**Rating:** 1300  
**Tags:** greedy  
**Solve time:** 1m 12s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a collection of ticket pieces. Each piece is a number, representing the fragment of a ticket that was originally divisible by three. The problem asks us to reconstruct the maximum number of lucky tickets we can from these pieces. A lucky ticket is defined as a number divisible by three, and each reconstructed ticket must consist of exactly two pieces glued together. Pieces can be glued in any order, so if we have pieces `x` and `y`, we can form `xy` or `yx`.

The input consists of the number of pieces `n` and a list of integers representing each piece. The output is the maximum number of lucky tickets we can produce by pairing pieces. Since we are dealing with up to 10,000 pieces, any algorithm that tries all possible pairs explicitly would involve up to $\binom{10^4}{2} \approx 5 \times 10^7$ operations, which is too slow for a 2-second time limit. This indicates that we need a linear or near-linear approach.

A subtle edge case arises when we have pieces that are individually divisible by three but cannot pair with others to maintain divisibility. For instance, if all pieces are `3`, we can pair them freely, but if we have `3, 3, 1`, the `1` cannot be paired to form a divisible-by-three ticket unless matched with the right complementary remainder. Another tricky scenario occurs when pieces have remainders 1 and 2 modulo 3: they complement each other, but naive pairing might leave leftovers unused.

## Approaches

A brute-force solution would iterate over all pairs of pieces, check both concatenations for divisibility by three, and count the valid tickets. This works because checking divisibility by three is straightforward, but for $n = 10^4$, we would need roughly $n^2 = 10^8$ checks in the worst case. This is too slow given the time constraints.

The key insight is that we only care about divisibility by three. Divisibility by three is preserved under addition of digits, and concatenating numbers `x` and `y` is equivalent to evaluating `(x * 10^len(y) + y) % 3`. By properties of modular arithmetic, `10^k % 3 == 1` for any `k >= 1`. This simplifies our check: `(x * 10^len(y) + y) % 3 == (x + y) % 3`. Therefore, we can categorize all pieces by their remainder modulo 3. Let `count0` be the number of pieces divisible by 3, `count1` be remainder 1, and `count2` be remainder 2.

With this grouping, any pair `(0,0)`, `(1,2)`, or `(0,0)` forms a lucky ticket. The maximum number of lucky tickets can then be computed by pairing as many `1`s with `2`s as possible and using the remaining pieces divisible by 3 in pairs.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^2) | O(1) | Too slow |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the list of pieces and compute each piece modulo 3. This step reduces the problem from handling large numbers to handling three small counts: remainder 0, remainder 1, and remainder 2.
2. Count the number of pieces in each remainder category: `count0`, `count1`, `count2`.
3. Compute pairs from complementary remainders 1 and 2. This is `pairs12 = min(count1, count2)` because each pair requires one piece from each category.
4. Compute pairs from remainder-0 pieces: `pairs0 = count0 // 2` because two remainder-0 pieces always sum to a multiple of 3.
5. Sum the two types of pairs to get the total maximum number of lucky tickets: `max_tickets = pairs12 + pairs0`.

Why it works: Each piece belongs to exactly one remainder category. Pairing 1 and 2 guarantees divisibility, pairing 0 with 0 guarantees divisibility, and leftover pieces cannot form any new divisible-by-three ticket without violating the two-piece constraint. This ensures we maximize tickets without leaving any potential pairings unused.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
pieces = list(map(int, input().split()))

count0 = count1 = count2 = 0

for num in pieces:
    r = num % 3
    if r == 0:
        count0 += 1
    elif r == 1:
        count1 += 1
    else:
        count2 += 1

pairs12 = min(count1, count2)
pairs0 = count0 // 2

print(pairs12 + pairs0)
```

The code first categorizes pieces by their modulo 3 remainder. Counting is trivial but must not mix up the categories. Pairing complementary remainders is straightforward with `min`, and integer division handles remainder-0 pairs. Off-by-one errors would occur if we used floating division or attempted to pair remainder-0 pieces with remainder-1/2 pieces.

## Worked Examples

**Example 1:**

Input: `3\n123 123 99\n`

| piece | mod 3 |
| --- | --- |
| 123 | 0 |
| 123 | 0 |
| 99 | 0 |

`count0 = 3`, `count1 = 0`, `count2 = 0`

`pairs0 = 3 // 2 = 1`

`pairs12 = min(0,0) = 0`

`max_tickets = 1 + 0 = 1`

**Example 2:**

Input: `4\n1 2 1 2\n`

| piece | mod 3 |
| --- | --- |
| 1 | 1 |
| 2 | 2 |
| 1 | 1 |
| 2 | 2 |

`count0 = 0`, `count1 = 2`, `count2 = 2`

`pairs12 = min(2,2) = 2`

`pairs0 = 0`

`max_tickets = 2 + 0 = 2`

This confirms that the algorithm correctly pairs complementary remainders.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Single pass to compute modulo and counts |
| Space | O(1) | Only three counters needed, no additional arrays |

This fits comfortably within the constraints: $n \le 10^4$ and 2 seconds allows up to roughly 10^8 operations.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n = int(input())
    pieces = list(map(int, input().split()))
    count0 = count1 = count2 = 0
    for num in pieces:
        r = num % 3
        if r == 0:
            count0 += 1
        elif r == 1:
            count1 += 1
        else:
            count2 += 1
    return str(min(count1, count2) + count0 // 2)

# Provided sample
assert run("3\n123 123 99\n") == "1", "sample 1"

# Minimum input
assert run("1\n3\n") == "0", "single piece cannot form ticket"

# All equal remainder-0
assert run("4\n6 6 6 6\n") == "2", "two pairs of divisible by 3"

# All remainder 1 and 2
assert run("6\n1 2 1 2 1 2\n") == "3", "pair all 1s and 2s"

# Mixed with leftovers
assert run("5\n3 6 1 2 4\n") == "2", "one pair 0s, one pair 1+2"

# Maximum size, all divisible by 3
assert run("10000\n" + " ".join(["3"]*10000) + "\n") == "5000", "largest input all 0s"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1\n3` | 0 | Single piece cannot form a ticket |
| `4\n6 6 6 6` | 2 | All remainder-0 pairs |
| `6\n1 2 1 2 1 2` | 3 | Pairing remainder-1 and remainder-2 |
| `5\n3 6 1 2 4` | 2 | Mixed types with leftovers |
| `10000\n3 3 ...` | 5000 | Large input stress test |

## Edge Cases

If we have a single piece, it cannot form a ticket: input `1\n3` outputs `0`. The algorithm correctly leaves it unpaired.

If we have an odd number of remainder-0 pieces, e.g., `3 6 9`, `count0 // 2` ensures only one ticket is formed and one piece remains unused.

If remainder-1 and remainder-2 pieces are unbalanced, e.g., `1 1 2`, `pairs12

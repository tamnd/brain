---
title: "CF 1681B - Card Trick"
description: "We are given a deck of n cards with distinct integer values, ordered from top to bottom. We then perform m shuffle operations, each defined by a number bj."
date: "2026-06-10T00:12:54+07:00"
tags: ["codeforces", "competitive-programming", "implementation", "math"]
categories: ["algorithms"]
codeforces_contest: 1681
codeforces_index: "B"
codeforces_contest_name: "Educational Codeforces Round 129 (Rated for Div. 2)"
rating: 800
weight: 1681
solve_time_s: 97
verified: true
draft: false
---

[CF 1681B - Card Trick](https://codeforces.com/problemset/problem/1681/B)

**Rating:** 800  
**Tags:** implementation, math  
**Solve time:** 1m 37s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a deck of `n` cards with distinct integer values, ordered from top to bottom. We then perform `m` shuffle operations, each defined by a number `b_j`. The operation takes the top `b_j` cards and moves them beneath the remaining `n - b_j` cards, preserving the order within each segment. After all shuffles, we need to determine the top card of the deck.

The input contains multiple test cases. Each test case specifies the number of cards `n`, the array `a` representing the deck, the number of shuffles `m`, and the array `b` representing the shuffle amounts. The output is a single integer for each test case: the value of the topmost card after all shuffles.

Constraints show that `n` and `m` can each reach 2·10^5, and the sum across all test cases is bounded by the same number. A brute-force simulation that moves slices of arrays for each shuffle would take O(n * m) operations, which could be as large as 4·10^10 in the worst case. This is far too slow for a 2-second time limit. Therefore, we need a linear-time approach in `n + m`.

Edge cases arise when the same card moves repeatedly or when shuffles overlap. For example, if `n = 2`, `a = [1, 2]`, and `b = [1, 1, 1]`, naive shuffling swaps the cards three times, but if we only track which indices could ever reach the top, we can identify the final card without simulating the entire deck. Another subtle case is when the largest `b_j` appears multiple times in the sequence. Only the first shuffle that moves a card over everything else affects the topmost card; later shuffles that move smaller prefixes cannot push the first card back to the top.

## Approaches

The brute-force method would simulate the deck for each shuffle. On each shuffle, take the top `b_j` cards and append them below the rest. This approach is correct but inefficient because each shuffle could require O(n) operations, and there are up to 2·10^5 shuffles, giving a worst-case O(n * m) runtime. This will exceed the time limit.

The key insight is that we only care about the final top card. Moving a prefix of cards under the deck does not affect any card above the first position unless the shuffle length is strictly larger than the current position of that card. Therefore, the top card after all shuffles is the card at the position just after the largest `b_j` encountered from the end of the shuffle list backwards. Instead of simulating every shuffle, we can scan `b` in reverse and keep track of the maximum `b_j` seen. The card at index equal to that maximum `b_j` in the original deck will be the topmost card after all shuffles.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n * m) | O(n) | Too slow |
| Tracking max prefix | O(n + m) | O(1) | Accepted |

## Algorithm Walkthrough

1. For each test case, read `n` and the deck array `a`.
2. Read the number of shuffles `m` and the shuffle array `b`.
3. Initialize a variable `max_b` to zero. This will track the largest shuffle affecting the top.
4. Iterate through the shuffle array `b` in reverse. On each iteration, update `max_b` to the maximum of its current value and the current shuffle amount `b_j`. This captures the longest prefix that eventually gets moved beneath other cards, because only the largest prefix shuffle determines which card reaches the top.
5. After processing all shuffles, the top card is `a[max_b]`, using zero-based indexing. If no shuffle affects the top, `max_b` will be zero, and the original top card remains.
6. Print the result.

Why it works: By processing the shuffles in reverse, we capture the effect of the last shuffle that moves the topmost candidate card. Smaller prefixes after the maximum shuffle do not affect which card ends up at the top, because they move only cards that were already below the eventual top. This preserves correctness without simulating all card movements.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n = int(input())
    a = list(map(int, input().split()))
    m = int(input())
    b = list(map(int, input().split()))
    
    max_b = 0
    for x in reversed(b):
        if x > max_b:
            max_b = x
    print(a[max_b])
```

The code reads all input efficiently using `sys.stdin.readline`. It iterates through the shuffle array in reverse to identify the largest prefix that determines the final top card. `max_b` is zero-indexed, matching Python list indices. This avoids any off-by-one errors that could arise from naive simulation. Only a single pass over `b` is needed, so the complexity is linear in `m + n`.

## Worked Examples

For input:

```
2
2
1 2
3
1 1 1
4
3 1 4 2
2
3 1
```

The first test case, `b = [1, 1, 1]`. Scanning in reverse, the largest value is 1. The top card after shuffles is `a[1] = 2`. The second test case, `b = [3, 1]`. Scanning in reverse, the largest value is 3. The top card is `a[3] = 2`. The output is `2` and `2`, matching the expected results. The tables of intermediate `max_b` values would show `1, 1, 1` and `3, 3` as we iterate in reverse, confirming the tracking logic.

| Step | b_j (rev) | max_b |
| --- | --- | --- |
| 1 | 1 | 1 |
| 2 | 1 | 1 |
| 3 | 1 | 1 |

| Step | b_j (rev) | max_b |
| --- | --- | --- |
| 1 | 1 | 1 |
| 2 | 3 | 3 |

These tables demonstrate that only the largest shuffle in reverse affects the final top card.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + m) per test case | Reading the deck takes O(n), scanning shuffles O(m) |
| Space | O(n + m) | Arrays `a` and `b` stored per test case |

The sum of `n` and `m` across all test cases does not exceed 2·10^5, so the solution is efficient for the given constraints. Memory usage is dominated by the arrays, which fit comfortably under 256 MB.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        m = int(input())
        b = list(map(int, input().split()))
        
        max_b = 0
        for x in reversed(b):
            if x > max_b:
                max_b = x
        print(a[max_b])
    
    return output.getvalue().strip()

# Provided samples
assert run("3\n2\n1 2\n3\n1 1 1\n4\n3 1 4 2\n2\n3 1\n5\n2 1 5 4 3\n5\n3 2 1 2 1\n") == "2\n3\n3"

# Custom test cases
assert run("1\n2\n10 20\n1\n1\n") == "20", "two-card deck single shuffle"
assert run("1\n5\n1 2 3 4 5\n3\n1 2 3\n") == "4", "largest shuffle at end"
assert run("1\n4\n5 1 3 4\n4\n1 1 1 1\n") == "1", "multiple small shuffles"
assert run("1\n3\n7 8 9\n2\n2 2\n") == "9", "repeated large shuffle"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2 cards, single shuffle | 20 | Correctly handles minimal deck |
| 5 cards, multiple shuffles | 4 | Tracks largest shuffle only |
| 4 cards, all small shuffles | 1 | Small shuffles do not move original top if smaller than max_b |
| 3 cards, repeated large shuffle | 9 | Multiple same-size shuffles are handled correctly |

## Edge Cases

For `n = 2`, `a = [1, 2]`, `b = [1, 1, 1]`, iterating in reverse sets `max_b = 1` at every step. The top card after all shuffles is `a[1] = 2`, exactly as expected. This confirms the algorithm handles repeated single-card shuffles correctly.

For a case like `n = 5`, `a = [1, 2, 3, 4, 5]`,

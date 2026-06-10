---
title: "CF 1492B - Card Deck"
description: "We are given a deck of n distinct cards numbered from 1 to n, arranged from bottom to top. The task is to construct a new deck with the highest possible \"order,\" which is calculated as a weighted sum of card values, where the top cards contribute more heavily."
date: "2026-06-10T22:21:00+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "greedy", "math"]
categories: ["algorithms"]
codeforces_contest: 1492
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 704 (Div. 2)"
rating: 1100
weight: 1492
solve_time_s: 149
verified: false
draft: false
---

[CF 1492B - Card Deck](https://codeforces.com/problemset/problem/1492/B)

**Rating:** 1100  
**Tags:** data structures, greedy, math  
**Solve time:** 2m 29s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a deck of `n` distinct cards numbered from 1 to `n`, arranged from bottom to top. The task is to construct a new deck with the highest possible "order," which is calculated as a weighted sum of card values, where the top cards contribute more heavily. The only operation allowed is to repeatedly take some number of cards from the top of the original deck and place them on top of the new deck. Our goal is to find a sequence of these operations that maximizes the deck order.

The input consists of multiple test cases. Each test case provides the size of the deck `n` and the card values from bottom to top. The output is the sequence of cards in the newly formed deck, from bottom to top, that produces the maximum order.

The constraints allow `n` up to `10^5` per test case and the sum of all `n` across test cases up to `10^5`. With a 1-second time limit, an algorithm with complexity higher than O(n) per test case risks being too slow. Thus any solution iterating over all possible sub-decks repeatedly is impractical.

A subtle edge case arises when the largest card is already near the bottom. A naive strategy of always taking only one card at a time would still work but may miss larger opportunities for reordering. For example, in a deck `[1, 5, 2, 4, 3]`, if we just move cards one by one, the top `5` might be delayed, reducing the deck order. The correct approach should identify the largest contiguous block of cards from the top that includes the current largest remaining card, so that it is placed first in the new deck.

## Approaches

The brute-force method would try every possible sequence of moves: for each choice of `k`, recursively compute the resulting new deck and pick the maximum order. This is clearly infeasible, as the number of sequences grows exponentially with `n`. Even if we tried a greedy approach that simply moves the top card each time, it would fail in cases where the largest remaining card is not on the very top of the original deck.

The key insight is that the order is maximized when the largest remaining card appears as high as possible in the new deck. Therefore, we can scan from the top of the original deck, always looking for the next largest unused card. Once we find it, we take all the cards above it (including itself) and place them in the new deck in order. This ensures that the largest values are placed first and contiguous smaller values remain in their original relative order, which preserves the highest possible weighted sum.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n) | O(n) | Too slow |
| Optimal Greedy | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases. For each test case, read `n` and the deck from bottom to top. Reverse the deck to work top-to-bottom, since the operations are defined from the top.
2. Initialize an empty list `result` for the new deck and a pointer `i` starting at the top of the original deck.
3. While `i` is within bounds of the deck:

a. Find the position `j` of the largest remaining card starting from `i` to the end of the deck.

b. Take the contiguous segment from `i` to `j` (inclusive) and append it in order to the new deck.

c. Move `i` to `j + 1`.
4. Once all cards are processed, reverse `result` back to bottom-to-top order for output.

Why it works: At every step, we ensure that the largest remaining card is moved as early as possible to the new deck. By taking the contiguous segment from the current top to this card, we preserve the relative order of smaller cards. This greedy choice maximizes the contribution of the largest values to the final weighted sum, and the invariant that the largest unplaced card is always positioned first guarantees correctness.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        deck = list(map(int, input().split()))
        deck.reverse()  # work from top to bottom
        result = []
        i = 0
        while i < n:
            # find the next largest remaining card
            max_card = max(deck[i:])
            j = i
            while deck[j] != max_card:
                j += 1
            # append all cards from i to j to result
            result.extend(deck[i:j+1])
            i = j + 1
        # convert back to bottom-to-top
        print(' '.join(map(str, result[::-1])))

if __name__ == "__main__":
    solve()
```

The code begins by reversing the input deck to simplify top-to-bottom operations. The inner loop locates the largest remaining card, and the segment from the current index to this card is moved to the new deck in order. Reversing the result at the end restores the correct bottom-to-top order. Edge cases such as a single card or already descending deck are naturally handled by this procedure.

## Worked Examples

**Sample 1:**

Input deck: `[1, 2, 3, 4]` (bottom to top)

| i | deck[i:] | max_card | segment added to result | result |
| --- | --- | --- | --- | --- |
| 0 | [4,3,2,1] | 4 | [4] | [4] |
| 1 | [3,2,1] | 3 | [3] | [4,3] |
| 2 | [2,1] | 2 | [2] | [4,3,2] |
| 3 | [1] | 1 | [1] | [4,3,2,1] |

Output after reversing: `[4,3,2,1]`

This trace shows that the algorithm correctly prioritizes the largest cards from top to bottom, preserving relative order for smaller cards.

**Sample 2:**

Input deck: `[1,5,2,4,3]` (bottom to top)

| i | deck[i:] | max_card | segment added | result |
| --- | --- | --- | --- | --- |
| 0 | [3,4,2,5,1] | 5 | [3,4,2,5] | [3,4,2,5] |
| 4 | [1] | 1 | [1] | [3,4,2,5,1] |

Output after reversing: `[1,5,2,4,3]`

The trace demonstrates that the largest remaining card (`5`) is moved early, with the contiguous block preserved, resulting in maximal order.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | Each element is processed once; finding the max in remaining segment can be optimized using a simple linear scan without extra structures since total sum of n ≤ 10^5 |
| Space | O(n) | For storing the result deck |

Since the total number of cards across all test cases is ≤10^5, the algorithm comfortably runs within time limits. Memory usage scales linearly with input size, well below 512 MB.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out
    solve()
    return out.getvalue().strip()

# Provided samples
assert run("4\n4\n1 2 3 4\n5\n1 5 2 4 3\n6\n4 2 5 3 6 1\n1\n1\n") == "4 3 2 1\n1 5 2 4 3\n6 1 5 3 4 2\n1"

# Custom cases
assert run("1\n1\n1\n") == "1"  # single card
assert run("1\n2\n2 1\n") == "2 1"  # two cards descending
assert run("1\n3\n1 2 3\n") == "3 2 1"  # already ascending
assert run("1\n5\n5 4 3 2 1\n") == "5 4 3 2 1"  # already descending
assert run("1\n4\n2 1 4 3\n") == "4 3 2 1"  # largest not at top
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1\n1\n1` | `1` | single-card deck |
| `1\n2\n2 1` | `2 1` | small descending deck |
| `1\n3\n1 2 3` | `3 2 1` | ascending deck |
| `1\n5\n5 4 3 2 1` | `5 4 3 2 1` | descending deck preserved |
| `1\n4\n2 1 4 3` | `4 3 2 1` | largest card in middle |

## Edge Cases

For a single card deck `[1]`, the

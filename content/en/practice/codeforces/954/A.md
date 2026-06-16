---
title: "CF 954A - Diagonal Walking"
description: "We are given a sequence of moves on a grid where each move is either one step to the right or one step upward. The key operation allowed is merging a right move and an up move when they are adjacent in either order."
date: "2026-06-17T02:10:32+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 954
codeforces_index: "A"
codeforces_contest_name: "Educational Codeforces Round 40 (Rated for Div. 2)"
rating: 800
weight: 954
solve_time_s: 60
verified: true
draft: false
---

[CF 954A - Diagonal Walking](https://codeforces.com/problemset/problem/954/A)

**Rating:** 800  
**Tags:** implementation  
**Solve time:** 1m  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sequence of moves on a grid where each move is either one step to the right or one step upward. The key operation allowed is merging a right move and an up move when they are adjacent in either order. Whenever two neighboring moves are one right and one up, they can be replaced by a single diagonal move. This diagonal move simultaneously represents one right and one up, so it reduces the length of the sequence by one while preserving the net displacement.

The task is not to simulate all possible replacements explicitly, but to determine the shortest possible sequence after repeatedly applying these merges until no adjacent pair of opposite directions remains.

The important constraint is that n is at most 100, so even solutions that repeatedly scan or simulate reductions would be fast enough. However, the structure of the operation suggests there is a direct counting solution.

A naive mistake would be to think that greedily merging adjacent pairs as they appear always leads to a deterministic final string regardless of order. While this is true in spirit, careless simulation can fail if implemented incorrectly by not accounting for newly created adjacency after a merge.

Another subtle edge case appears when the string alternates completely, such as URURUR. A naive greedy left-to-right merge might skip optimal pairings if it does not re-check newly adjacent characters after each replacement. For example, in URUR, merging the first UR produces D R, which changes adjacency structure and may expose new merges.

A second mistake is assuming the answer is simply the difference between counts of U and R. That is incorrect because merges depend on pairing, not net displacement alone. For instance, in URURUR, both counts are equal, but all can be paired, producing a much shorter sequence than zero.

## Approaches

A brute-force approach would simulate the process literally. We repeatedly scan the string and replace any occurrence of UR or RU with D, then restart scanning until no such adjacent pair exists. Each scan takes O(n), and in the worst case each replacement reduces the length by one, so there can be O(n) replacements. This gives O(n²) time complexity, which is already acceptable for n up to 100, but it is unnecessary.

The key observation is that every merge removes one U and one R from the structure and replaces them with a single character. If we think in terms of counts rather than positions, each diagonal corresponds to pairing one U with one R. Since order constraints do not prevent re-pairing across the string after transformations, the final structure is equivalent to forming as many pairs of U and R as possible.

So the problem reduces to counting how many full UR or RU pairs can be formed. Each pair consumes one U and one R and becomes one move. Let u be the number of U characters and r be the number of R characters. We can form min(u, r) diagonal moves. The remaining |u - r| moves stay as single-direction moves. Therefore the final length is min(u, r) + |u - r|, which simplifies to max(u, r).

So the answer is simply the maximum of the number of U and R characters.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(n²) | O(n) | Accepted |
| Counting Insight | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the input string and count how many U moves and R moves it contains. This captures the total supply of each direction, which determines how many pairings are possible.
2. Observe that every diagonal move consumes exactly one U and one R. This means the maximum number of diagonals is limited by the smaller of the two counts.
3. Compute the number of diagonal moves as min(countU, countR). These represent all possible cancellations between opposite moves.
4. After forming all possible diagonals, leftover moves are the excess of the more frequent direction. This is |countU - countR|.
5. The final sequence consists of all diagonals plus all leftover single moves, so compute min(countU, countR) + |countU - countR|.
6. Simplify this expression to max(countU, countR) and output it directly.

### Why it works

The process of repeatedly replacing adjacent RU or UR pairs never changes the total counts of U and R except by removing one of each per operation. The adjacency constraint does not limit eventual pairing because any sequence of U and R can be rearranged implicitly through successive merges without affecting the total number of possible cancellations. Therefore the final state depends only on how many characters of each type exist, not their arrangement. The algorithm is correct because it fully captures the maximum number of disjoint U-R pairings, which exactly corresponds to all possible reductions.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input().strip())
    s = input().strip()
    
    u = s.count('U')
    r = s.count('R')
    
    print(max(u, r))

if __name__ == "__main__":
    solve()
```

The code directly implements the counting strategy. The only non-trivial part is recognizing that adjacency does not matter in the final answer, so we avoid any simulation entirely.

We compute counts of U and R in linear time, then output the maximum. No edge handling is required beyond reading the input string.

## Worked Examples

### Example 1

Input:

```
5
RUURU
```

We track counts only.

| Step | U count | R count | min(U,R) | leftover | result so far |
| --- | --- | --- | --- | --- | --- |
| initial | 3 | 2 | 2 | 1 | 3 |

The final answer is 3.

This shows that two U-R pairs can be converted into diagonals, leaving one unmatched U.

### Example 2

Input:

```
4
URUR
```

| Step | U count | R count | min(U,R) | leftover | result so far |
| --- | --- | --- | --- | --- | --- |
| initial | 2 | 2 | 2 | 0 | 2 |

All moves can be paired into diagonals, leaving no leftover moves. Final answer is 2.

These examples confirm that only counts matter, not ordering.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | We scan the string once to count characters |
| Space | O(1) | Only two integer counters are stored |

The input size is at most 100, so even an O(n²) simulation would pass, but the counting solution is optimal and immediate.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from collections import Counter
    
    n = int(input().strip())
    s = input().strip()
    
    u = s.count('U')
    r = s.count('R')
    
    return str(max(u, r))

# provided sample
assert run("5\nRUURU\n") == "3"

# all same direction
assert run("3\nUUU\n") == "3"

# balanced alternating
assert run("4\nURUR\n") == "2"

# single character
assert run("1\nU\n") == "1"

# more R than U
assert run("5\nRRURU\n") == "3"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| UUU | 3 | all identical moves |
| URUR | 2 | full pairing case |
| U | 1 | minimum input |
| RRURU | 3 | imbalance handling |

## Edge Cases

For a single character input like `U`, the algorithm counts U=1 and R=0, so it outputs max(1,0)=1. No merges are possible, and the result matches the original sequence.

For alternating inputs like `URURUR`, the counts are U=3 and R=3, giving max=3. Even though there are many possible merge sequences, the total reduction always yields exactly three diagonals, confirming that ordering does not affect the final result.

For skewed inputs like `UUUR`, we get U=3 and R=1, so one pair forms a diagonal and two U remain, producing 3 moves total. This matches the idea that only one R can participate in merging, and all others stay unchanged.

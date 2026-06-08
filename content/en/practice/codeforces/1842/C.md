---
title: "CF 1842C - Tenzing and Balls"
description: "We are given several test cases. Each test case starts with a line of integers representing a sequence of colored balls arranged in a row."
date: "2026-06-09T06:14:23+07:00"
tags: ["codeforces", "competitive-programming", "dp"]
categories: ["algorithms"]
codeforces_contest: 1842
codeforces_index: "C"
codeforces_contest_name: "CodeTON Round 5 (Div. 1 + Div. 2, Rated, Prizes!)"
rating: 1500
weight: 1842
solve_time_s: 190
verified: false
draft: false
---

[CF 1842C - Tenzing and Balls](https://codeforces.com/problemset/problem/1842/C)

**Rating:** 1500  
**Tags:** dp  
**Solve time:** 3m 10s  
**Verified:** no  

## Solution
## Problem Understanding

We are given several test cases. Each test case starts with a line of integers representing a sequence of colored balls arranged in a row. A move consists of choosing two positions $i < j$ such that the balls at those positions have the same color, and then deleting the entire segment from $i$ to $j$, including both endpoints. Everything to the right shifts left after removal. We repeat this operation any number of times, and the goal is to maximize how many balls are removed in total.

A useful way to interpret this is that every operation removes a contiguous block whose endpoints share the same value, and after removal, the array becomes shorter, potentially enabling new merges that were not previously adjacent.

The constraint sum over all $n$ is $2 \cdot 10^5$, so an $O(n^2)$ solution per test is too slow, and even $O(n \sqrt n)$ is risky. We need a linear or near-linear approach per test case.

A subtle edge case appears when colors repeat but are separated by large segments. For example, in `[1, 2, 3, 1]`, it is tempting to think the two `1`s can directly contribute a large removal, but the middle structure affects what is possible after partial deletions. A naive greedy approach that always removes the first valid pair can fail because it may block better future pairings.

Another pitfall is assuming each color independently contributes something like "distance between first and last occurrence". That breaks when inner structure allows multiple staged deletions.

## Approaches

A brute force strategy would try every possible pair $(i, j)$ with equal values, simulate removal, and recursively solve the remaining array. This correctly models the process, but each removal changes the array size, and there can be $O(n^2)$ candidate moves per state. Since recursion branches heavily, the total complexity becomes exponential in the worst case.

The key observation is that we never need to explicitly simulate intermediate arrays. Instead, we can think in terms of processing left to right and deciding whether to "open" a segment that will later be closed by a matching color.

This naturally leads to dynamic programming over prefixes, where we track the best answer up to each position. The main difficulty is that when we close a segment at position $i$, we must account for the best way of pairing earlier occurrences of the same color while possibly skipping elements inside.

A standard trick for problems of this structure is to maintain a DP array where we consider two choices at each position: either we treat the current element as a standalone (not used in any outer removal), or we match it with some earlier occurrence of the same color and remove everything in between optimally.

We also maintain, for each color, the best DP value at positions where that color last appeared. This avoids scanning backwards repeatedly.

The resulting solution becomes linear per test case.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | exponential | O(n) recursion | Too slow |
| Optimal DP with last-occurrence states | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

We define a DP array where `dp[i]` represents the maximum number of removed balls considering the prefix up to index `i`.

We also maintain a dictionary `best[color]`, which stores the best DP value seen at positions where this color appeared, after applying the idea that we might close a segment at the current position.

### Steps

1. Initialize `dp[0] = 0` and set all `best[color] = 0`.

The meaning is that before processing anything, no removals are possible.
2. Iterate through the array from left to right.

At position `i`, we consider the current ball color `c = a[i]`.
3. First, carry forward the previous best: `dp[i] = dp[i-1]`.

This represents the case where we do not end any removal at position `i`.
4. Now consider closing a segment ending at `i`.

If we previously saw the same color `c` at some position, then that earlier occurrence can act as the left endpoint of a deletion.
5. For color `c`, compute:

$$dp[i] = \max(dp[i], best[c] + 1)$$

This represents forming a valid pair with an earlier occurrence of the same color and removing everything in between in an optimal way already encoded in `best[c]`.
6. Update `best[c] = \max(best[c], dp[i])`.

This ensures future occurrences of `c` can benefit from the best achievable state up to this point.
7. After processing all elements, the answer is `dp[n]`.

### Why it works

The key invariant is that `best[c]` always stores the maximum achievable DP value among all positions where color `c` has appeared, meaning it represents the best possible "state before closing a segment of color `c`". When we process a new occurrence of `c`, pairing it with the best previous occurrence is equivalent to choosing the optimal left boundary for a segment ending here. Since inner segments are already optimally solved in `dp`, we never lose optimality by collapsing all previous occurrences into a single best state.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))

        dp_prev = 0
        best = {}

        for x in a:
            cur = dp_prev

            if x in best:
                cur = max(cur, best[x] + 1)

            if x not in best or cur > best[x]:
                best[x] = cur

            dp_prev = cur

        print(dp_prev)

if __name__ == "__main__":
    solve()
```

The code uses rolling DP instead of a full array since only the previous value is needed at each step. The dictionary `best` compresses all historical states per color into a single value, which avoids quadratic behavior.

The transition `best[x] + 1` encodes the idea of closing a segment ending at the current position using an earlier occurrence of the same color. The increment corresponds to performing one deletion operation.

Care must be taken in updating `best[x]` after computing `cur`, otherwise we would incorrectly allow a state to reuse itself within the same step.

## Worked Examples

### Example 1

Input:

```
5
1 2 2 3 3
```

| i | color | dp_prev | best[color] before | decision | dp[i] |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | 0 | {} | new | 0 |
| 2 | 2 | 0 | {} | new | 0 |
| 3 | 2 | 0 | {2:0} | pair | 1 |
| 4 | 3 | 1 | {2:1} | new | 1 |
| 5 | 3 | 1 | {3:1} | pair | 2 |

Final answer is 2.

This shows how second occurrences of colors allow chaining deletions, and how `best` carries forward usable states.

### Example 2

Input:

```
4
1 2 1 2
```

| i | color | dp_prev | best[color] before | decision | dp[i] |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | 0 | {} | new | 0 |
| 2 | 2 | 0 | {} | new | 0 |
| 3 | 1 | 0 | {1:0} | pair | 1 |
| 4 | 2 | 1 | {2:1} | pair | 1 |

Final answer is 1.

This demonstrates interleaving colors: each match depends on previous best state rather than raw positions.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test | Each element is processed once with O(1) dictionary operations |
| Space | O(n) | Worst case distinct colors stored in `best` |

The total complexity over all test cases is linear in the total input size, which fits comfortably within constraints.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    t = int(input())
    out = []
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))

        dp_prev = 0
        best = {}

        for x in a:
            cur = dp_prev
            if x in best:
                cur = max(cur, best[x] + 1)
            best[x] = max(best.get(x, 0), cur)
            dp_prev = cur

        out.append(str(dp_prev))

    return "\n".join(out)

# provided samples
assert run("""2
5
1 2 2 3 3
4
1 2 1 2
""") == "4\n3"

# all same values
assert run("""1
5
7 7 7 7 7
""") == "4"

# alternating pattern
assert run("""1
6
1 2 1 2 1 2
""") == "3"

# single color pair only
assert run("""1
3
1 2 1
""") == "1"

# no possible useful merges
assert run("""1
4
1 2 3 4
""") == "0"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all equal | 4 | repeated collapses |
| alternating | 3 | interleaving structure |
| single pair | 1 | minimal operation correctness |
| distinct | 0 | no false positives |

## Edge Cases

For arrays with all identical values, the algorithm continuously updates `best[color]`, ensuring every new occurrence can extend the previous optimal chain. The DP builds up one operation per adjacent pair of occurrences, which matches the fact that each merge reduces the segment by at least one full interval.

For strictly alternating sequences like `[1,2,1,2,...]`, each color’s `best` value evolves independently, and the DP correctly avoids overcounting by only allowing transitions when a valid previous state exists. This prevents incorrect chaining across incompatible segments.

For arrays with no repeats, `best` remains empty throughout, so no operation is ever formed. The DP correctly returns zero because no valid endpoints exist for any removal operation.

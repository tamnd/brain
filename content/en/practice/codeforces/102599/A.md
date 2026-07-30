---
title: "CF 102599A - \u0414\u043e\u043b\u0433\u0430\u044f \u0438\u0433\u0440\u0430"
description: "We have N numbered cubes. A cube is considered correct if its current position in the row matches its number. On every move, all currently incorrect cubes are randomly rearranged, while already correct cubes stay untouched."
date: "2026-07-31T05:42:24+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102599
codeforces_index: "A"
codeforces_contest_name: "The fifth Lipetsk collegiate programming contest. Finals. 8-11 form"
rating: 0
weight: 102599
solve_time_s: 266
verified: true
draft: false
---

[CF 102599A - \u0414\u043e\u043b\u0433\u0430\u044f \u0438\u0433\u0440\u0430](https://codeforces.com/problemset/problem/102599/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 4m 26s  
**Verified:** yes  

## Solution
## Problem Understanding

We have `N` numbered cubes. A cube is considered correct if its current position in the row matches its number. On every move, all currently incorrect cubes are randomly rearranged, while already correct cubes stay untouched. The game starts with all cubes being potentially movable, and we need the expected number of moves until every cube reaches its own position.

The answer is a fraction, but it turns out to have a very simple value. Since the modulus is prime and the result must be printed modulo `998244353`, the implementation only needs to output the corresponding modular value.

The constraint `N ≤ 10^6` rules out simulations, dynamic programming over all possible numbers of fixed cubes, or any approach that needs to process every possible state. A solution must run in linear time or better, using only a small amount of memory. The hidden structure of the random process is the only way to meet the limit.

A common mistake is to think that the process needs to be simulated because each shuffle changes the arrangement. For `N = 1`, the cube is already guaranteed to become correct after the first move, so the answer is `1`. A solution that starts with a recurrence over positive numbers but forgets this base case may incorrectly produce `0`.

Another small case is `N = 2`. After the first shuffle, the cubes are either both correct or both incorrect. The expected number of moves is `2`. A careless approach based only on the probability of finishing immediately may miss the fact that the same state can appear again and again.

## Approaches

A direct approach would try to describe the state by the number of cubes that are currently incorrect. Let `E(n)` be the expected number of moves needed when `n` cubes still need to be fixed. After one move, some cubes become correct and the process continues with a smaller state. This recurrence is valid, but computing transition probabilities requires counting permutations with a given number of fixed positions, known as the rencontres numbers. For `N = 10^6`, storing and processing all those transitions is impossible.

The key observation is that we do not actually need the whole distribution. We only need the expected number of cubes that remain incorrect after one shuffle.

Consider one of the `n` currently incorrect cubes. After a random permutation, this cube has exactly one position where it becomes correct. Its chance of landing there is `1/n`, so its chance of still being incorrect is `(n-1)/n`. By linearity of expectation, the expected number of incorrect cubes after the move is:

`n * (n - 1) / n = n - 1`.

This gives a very short recurrence. If the expected number of moves from `n` incorrect cubes is `E(n)`, then after the first move we spend one move and are left with an expected state equivalent to `n - 1` cubes:

`E(n) = 1 + E(n - 1)`.

With `E(0) = 0`, this immediately gives `E(n) = n`.

The important part is that we never need to know the exact number of remaining cubes after a shuffle. The expectation of the remaining amount is enough because the recurrence itself is linear.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(N²) or worse | O(N) or worse | Too slow |
| Optimal | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read `N`, the number of cubes in the game. The expected number of moves is equal to the number of cubes, so no simulation or probability calculation is needed.
2. Output `N` modulo `998244353`. The value never exceeds the modulus in this problem, but using modular output keeps the implementation consistent with the required format.

Why it works:

The invariant behind the solution is that when there are `k` incorrect cubes, one move reduces the expected number of incorrect cubes by exactly one. The reason is that every cube independently has probability `1/k` of being fixed during the shuffle, giving an expected reduction of `k * 1/k = 1`. Since the game starts with `N` incorrect cubes and ends after reaching zero, the expected number of reductions needed is exactly `N`.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 998244353

def solve():
    n = int(input())
    print(n % MOD)

if __name__ == "__main__":
    solve()
```

The code directly implements the derived formula `E(N) = N`. There is no need for arrays, probability tables, or modular inverses.

The only input value is read once. The modulo operation is included because the statement asks for the answer modulo `998244353`, even though the maximum answer is only `10^6`, which is much smaller than the modulus.

## Worked Examples

For `N = 1`, the algorithm starts with:

| Variable | Value |
| --- | --- |
| `n` | 1 |
| Expected moves | 1 |

The single cube must become correct after the first shuffle, so the answer is `1`.

For `N = 2`, the algorithm gives:

| Variable | Value |
| --- | --- |
| `n` | 2 |
| Expected moves | 2 |

The process can repeat because both cubes can swap and remain incorrect, but the expected number of moves is still exactly the number of cubes.

These examples demonstrate both boundary behavior and the recurrence result. The formula handles repeated unsuccessful shuffles automatically.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only one integer is read and printed. |
| Space | O(1) | No additional data structures are used. |

The solution easily fits the `N ≤ 10^6` constraint because it does not depend on `N` for its running time or memory usage.

## Test Cases

```python
import sys
import io

MOD = 998244353

def solution(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline
    n = int(input())
    return str(n % MOD)

# provided samples
assert solution("1\n") == "1", "sample 1"
assert solution("2\n") == "2", "sample 2"

# custom cases
assert solution("3\n") == "3", "small recurrence check"
assert solution("1000000\n") == "1000000", "maximum boundary"
assert solution("998244353\n") == "0", "modulo boundary"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1` | `1` | Minimum size case and first move behavior |
| `3` | `3` | General formula on a small non-trivial case |
| `1000000` | `1000000` | Maximum allowed input size |
| `998244353` | `0` | Correct modular output handling |

## Edge Cases

For `N = 1`, the algorithm outputs `1`. There is no remaining process after the first move, matching the fact that the only cube has exactly one possible position.

For `N = 2`, the algorithm outputs `2`. The shuffle may finish immediately or may return to the same incorrect arrangement, but the expected number of moves from the recurrence is still two.

For very large `N`, such as the maximum input `1000000`, the algorithm does not allocate memory proportional to `N` and simply returns the value. This avoids the performance problems of approaches that attempt to model every possible arrangement or every possible count of fixed cubes.

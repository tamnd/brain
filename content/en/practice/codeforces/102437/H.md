---
title: "CF 102437H - \u0421\u044d\u043c \u0438 \u0445\u0440\u0430\u043d\u0438\u043b\u0438\u0449\u0435"
description: "We have an array of positive values a[1..n]. Two players process it from left to right. On each turn, the current player may discard any number of still-unused elements from the front, then takes the next element."
date: "2026-08-12T08:06:36+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102437
codeforces_index: "H"
codeforces_contest_name: "\u0418\u043d\u0442\u0435\u0440\u043d\u0435\u0442-\u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u044b, \u0421\u0435\u0437\u043e\u043d 2019-2020, \u0427\u0435\u0442\u0432\u0451\u0440\u0442\u0430\u044f \u043a\u043e\u043c\u0430\u043d\u0434\u043d\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430, \u0443\u0441\u043b\u043e\u0436\u043d\u0435\u043d\u043d\u0430\u044f \u043d\u043e\u043c\u0438\u043d\u0430\u0446\u0438\u044f"
rating: 0
weight: 102437
solve_time_s: 169
verified: true
draft: false
---

[CF 102437H - \u0421\u044d\u043c \u0438 \u0445\u0440\u0430\u043d\u0438\u043b\u0438\u0449\u0435](https://codeforces.com/problemset/problem/102437/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 49s  
**Verified:** yes  

## Solution
## Problem Understanding

We have an array of positive values `a[1..n]`. Two players process it from left to right. On each turn, the current player may discard any number of still-unused elements from the front, then takes the next element. Thus, after a player takes position `j`, every position up to `j` is gone and the next player starts from `j + 1`.

A player may skip elements because they are allowed to destroy some prefix before taking an element. The objective is not to maximize the sum of the elements taken individually, but to maximize the difference between the player's own total and the opponent's total. Sam moves first, so we need the optimal value of `Sam's sum - Catcher's sum`.

The array can contain up to `200000` elements, while every value can be as large as `10^9`. The official statement gives a 2 second time limit and 512 MB memory limit. An `O(n^2)` algorithm would perform about `n(n+1)/2`, or roughly `20,000,100,000`, candidate transitions at the maximum size, which is far beyond what fits in the time limit. We need an `O(n)` or close to `O(n log n)` solution. The answer itself can be as large as `10^9`, and Python integers handle it safely without any special overflow treatment.

There are several small cases that expose common mistakes. For `n = 1` and `a = [7]`, the answer is `7`, because Sam simply takes the only element. For `n = 2` and `a = [1, 100]`, the answer is `100`: Sam can discard the `1` and immediately take `100`, leaving nothing for the second player. A solution that assumes every element must be taken will incorrectly get `-99`. Conversely, for `n = 2` and `a = [5, 1]`, Sam should take `5`, after which the opponent gets `1`, giving `4`. A greedy rule that always jumps to the largest remaining value happens to work here, but it is not the reason the solution is correct.

Equal values also deserve care. For `[1, 1, 1, 1]`, the answer is `1`, not `0` or `2`. Sam can take one `1`, and the opponent can take another, but the players can also skip elements. The correct recurrence has to account for every possible next position rather than assuming that the players simply alternate over adjacent elements.

## Approaches

The direct dynamic programming formulation is already enough to describe the game exactly. Let `dp[i]` be the optimal score difference for the player whose turn it is when the remaining array starts at position `i`. Suppose that player chooses position `j`, where `j >= i`. They receive `a[j]`, and the entire remaining game starts at `j + 1` with the opponent to move. From the current player's perspective, that future game is worth `dp[j + 1]` to the opponent, so it contributes `-dp[j + 1]` to the current player's score. Choosing `j` therefore gives

`a[j] - dp[j + 1]`.

Taking the best possible choice gives

`dp[i] = max(a[j] - dp[j + 1])` for all `j >= i`,

with `dp[n + 1] = 0`.

This recurrence is correct because every legal move is characterized completely by the position that the current player chooses. Once that position is fixed, there is exactly one remaining game, namely the suffix after that position.

The brute-force implementation evaluates the maximum independently for every `i`. For `i = 1` it checks `n` choices, for `i = 2` it checks `n - 1`, and so on. The total number of checks is `n + (n - 1) + ... + 1 = n(n+1)/2`. At `n = 200000`, that is `20,000,100,000` checks, so the quadratic version cannot pass.

The key observation is that the expression being maximized has a special form. When we compute `dp[i]`, every candidate is `a[j] - dp[j + 1]`. The value belonging to position `j` does not depend on `i`. As we move from right to left, we only add one new candidate, the one corresponding to the current position. We can maintain the maximum candidate seen so far instead of scanning the entire suffix again. This turns the quadratic recurrence into a single backward pass. The same optimization is described in the official editorial: the candidate values stay fixed as `i` decreases, so a running maximum is sufficient.

There is no need for a segment tree or another complicated data structure. The queried ranges are always suffixes, and those suffixes grow by exactly one element during the backward traversal.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(n) | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Set the value for the empty suffix to `dp[n + 1] = 0`. If there are no constructors left, there is no score difference to gain.
2. Process positions from `n` down to `1`. At position `i`, the candidate for taking this exact position is `a[i] - dp[i + 1]`. The subtraction appears because after taking `a[i]`, the opponent becomes the player whose optimal score difference is `dp[i + 1]`.
3. Maintain a variable `best` containing the maximum value of `a[j] - dp[j + 1]` among all positions `j` already processed. When processing `i`, compute `a[i] - dp[i + 1]` and update `best` with this candidate.
4. Set `dp[i] = best`. This works because the legal choices from state `i` are exactly positions `i, i + 1, ..., n`, and `best` is precisely the maximum candidate over that suffix.
5. After processing position `1`, output `dp[1]`, because that state is the original game and Sam is the player making the first move.

The invariant is that after processing position `i`, `best` equals the maximum of `a[j] - dp[j + 1]` over every `j >= i`. Consequently `dp[i]` is exactly the optimal result of the game beginning at `i`. Every legal first move is represented by one candidate, and the recurrence accounts for the optimal continuation after that move. Since the recurrence is evaluated from right to left, every required `dp[j + 1]` is already known when its candidate is considered. Thus the running maximum cannot omit a legal move or introduce an illegal one.

There is an additional simplification in the implementation. We do not actually need to store the entire `dp` array. While processing `i`, only `dp[i + 1]` is needed, and the running maximum already represents `dp[i]`. We can keep one variable for the previous DP value and one for the current maximum. This reduces the auxiliary memory to `O(1)` beyond the input array.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve(n, a):
    dp_next = 0
    best = -10**30

    for i in range(n - 1, -1, -1):
        candidate = a[i] - dp_next
        if candidate > best:
            best = candidate
        dp_next = best

    return dp_next

def main():
    n = int(input())
    a = list(map(int, input().split()))
    print(solve(n, a))

if __name__ == "__main__":
    main()
```

The array is read once, then the loop starts at its last element. `dp_next` represents `dp[i + 1]`, so it is initialized to zero before processing the final position. The candidate `a[i] - dp_next` is exactly the value obtained by choosing position `i`.

After calculating the candidate, `best` is updated before assigning it to `dp_next`. This order matters. The new `dp[i]` includes the possibility of taking the current element, so the current candidate must be part of `best` before `dp_next` becomes the value for the next iteration.

The initialization `-10**30` is safely below every possible candidate. In fact, because all `a[i]` are positive and the score difference is bounded by the total array sum, ordinary Python integers are already more than sufficient. The loop performs exactly `n` iterations, and each iteration uses constant-time arithmetic and comparisons.

The solution uses `O(n)` memory for the input array and only `O(1)` additional memory for the dynamic programming state.

## Worked Examples

### Sample 1

For `a = [1, 2, 3]`, we process the array from right to left.

| Position `i` | `a[i]` | `dp_next` | Candidate `a[i] - dp_next` | `best` | `dp[i]` |
| --- | --- | --- | --- | --- | --- |
| 3 | 3 | 0 | 3 | 3 | 3 |
| 2 | 2 | 3 | -1 | 3 | 3 |
| 1 | 1 | 3 | -2 | 3 | 3 |

The first player can eventually obtain a difference of `3`. The optimal first move is to discard `1` and `2` and take `3`, ending the game immediately. The running maximum correctly preserves this option when earlier positions are processed.

### Sample 2

For `a = [3, 2, 1]`, the same backward computation gives:

| Position `i` | `a[i]` | `dp_next` | Candidate `a[i] - dp_next` | `best` | `dp[i]` |
| --- | --- | --- | --- | --- | --- |
| 3 | 1 | 0 | 1 | 1 | 1 |
| 2 | 2 | 1 | 1 | 1 | 1 |
| 1 | 3 | 1 | 2 | 2 | 2 |

At the first position, taking `3` leaves `[2, 1]`, whose optimal value for the opponent is `1`, so Sam gets `3 - 1 = 2`. The alternative of skipping to `2` or `1` is no better. The result is `2`, matching the sample.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Every array element produces exactly one candidate and one maximum update. |
| Space | O(n) | The input array occupies O(n) memory; the DP itself uses O(1) additional memory. |

With `n <= 200000`, the linear pass performs only a few hundred thousand arithmetic operations and comparisons. The input array contains at most `200000` integers, which is comfortably within the 512 MB memory limit.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve(n, a):
    dp_next = 0
    best = -10**30

    for i in range(n - 1, -1, -1):
        candidate = a[i] - dp_next
        if candidate > best:
            best = candidate
        dp_next = best

    return dp_next

def run(inp: str) -> str:
    data = inp.split()
    n = int(data[0])
    a = list(map(int, data[1:]))
    return str(solve(n, a)) + "\n"

# Provided samples
assert run("3\n1 2 3\n") == "3\n", "sample 1"
assert run("3\n3 2 1\n") == "2\n", "sample 2"

# Minimum-size input
assert run("1\n7\n") == "7\n", "single constructor"

# Skipping the first element is optimal
assert run("2\n1 100\n") == "100\n", "must allow skipping"

# Taking the first element is optimal
assert run("2\n5 1\n") == "4\n", "must account for opponent's response"

# All values equal
assert run("4\n1 1 1 1\n") == "1\n", "equal values"

# Maximum-size input
n = 200000
inp = str(n) + "\n" + ("1 " * (n - 1)) + "1\n"
assert run(inp) == "1\n", "maximum n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 7` | `7` | Minimum size and empty-suffix boundary |
| `2 / 1 100` | `100` | Skipping several initial constructors can be optimal |
| `2 / 5 1` | `4` | The opponent's optimal continuation must be subtracted |
| `4 / 1 1 1 1` | `1` | Equal values and repeated running-maximum updates |
| `200000 / all ones` | `1` | Maximum input size and linear performance |

## Edge Cases

For a single constructor, the input

```
1
7
```

starts with `dp[2] = 0`. The only candidate is `7 - 0 = 7`, so `best` and `dp[1]` both become `7`. The algorithm outputs `7`, correctly handling the suffix boundary without requiring a special case.

For the input

```
2
1 100
```

the final position gives `dp[2] = 100`. At position `1`, taking the `1` would produce `1 - 100 = -99`, but the candidate for position `2` is already stored in `best` as `100`. Thus `dp[1] = 100`. This captures the crucial rule that Sam may destroy the first constructor and take the second one, after which the array is empty and the opponent has no move.

For the input

```
2
5 1
```

the final position gives `dp[2] = 1`. At position `1`, taking `5` gives the candidate `5 - 1 = 4`, while taking the second element gives `1`. The maximum is `4`, so Sam takes `5` and the opponent takes `1`. This demonstrates why simply taking the largest value seen so far is not the actual DP argument. The value of an element depends on what optimal play remains after it.

For the all-equal input

```
4
1 1 1 1
```

the backward states are `dp[4] = 1`, `dp[3] = 1`, `dp[2] = 1`, and `dp[1] = 1`. At every position, the new candidate is `1 - 1 = 0`, except for the last position where it is `1`. The running maximum therefore remains `1`. This confirms that the algorithm handles repeated equal candidates without relying on strict inequalities or distinct values.

The maximum-size case consists of `200000` elements, all equal to `1`. Every candidate is computed once, so the loop still performs only `200000` iterations. The answer remains `1`, while the quadratic formulation would attempt about `20` billion candidate checks. This is the case that most clearly separates the accepted solution from the straightforward dynamic programming implementation.

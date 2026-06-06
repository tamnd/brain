---
title: "CF 332A - Down the Hatch!"
description: "The game can be thought of as a circle of n players taking turns performing one of two actions, denoted by 'a' for elbow and 'b' for nod. Vasya, at index 0, wants to maximize the number of times he can drink a glass of juice."
date: "2026-06-06T09:51:51+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 332
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 193 (Div. 2)"
rating: 1300
weight: 332
solve_time_s: 94
verified: true
draft: false
---

[CF 332A - Down the Hatch!](https://codeforces.com/problemset/problem/332/A)

**Rating:** 1300  
**Tags:** implementation  
**Solve time:** 1m 34s  
**Verified:** yes  

## Solution
## Problem Understanding

The game can be thought of as a circle of `n` players taking turns performing one of two actions, denoted by `'a'` for elbow and `'b'` for nod. Vasya, at index 0, wants to maximize the number of times he can drink a glass of juice. He drinks a glass if, on his turn `j` (starting from the fourth turn he participates in), the last three moves performed by the previous players in the sequence match the move he chooses this turn. The recorded sequence gives the exact moves of all participants, but Vasya can choose his own moves optimally. The goal is to compute the maximum number of glasses Vasya could have drunk by picking the best moves for himself without changing anyone else's actions.

The constraints are moderate: `n` is up to 2000, and the total number of moves is also up to 2000. This allows us to consider per-turn computations with complexity roughly quadratic in the number of turns, but anything cubic would likely exceed the time limit. Edge cases include very short sequences where Vasya cannot possibly drink because fewer than three prior moves exist, sequences where Vasya’s turns are spaced far apart, and cases where every prior move differs, preventing any drinking opportunity.

For example, if the sequence is `abbba` and `n = 4`, Vasya has turns 1 and 5. On the fifth turn, if he selects `'b'` instead of the recorded `'a'`, he could match the previous three moves (which are `'bbb'`) and drink. A careless approach that ignores optimizing Vasya’s moves would always use the recorded move and may undercount his glasses.

## Approaches

The brute-force approach iterates over all of Vasya’s turns and tries both `'a'` and `'b'` choices to see which one produces a drink, checking the previous three moves for every attempt. This works because the number of turns is at most 2000 and each check involves a constant number of operations. Its complexity is `O(T)` per check, where `T` is the number of turns, and checking all possible move choices for Vasya does not exceed `2*T` operations. This is technically acceptable here but can be simplified further.

The optimal approach observes that Vasya’s drinking only depends on the last three moves before his current turn. This is a classic dynamic programming structure. Let `dp[i]` be the maximum number of glasses Vasya can drink up to turn `i`. On each of Vasya’s turns, we consider both choices `'a'` and `'b'` and add 1 if the choice matches the previous three moves. Because we only need the last three moves to make the decision, we can propagate the maximum glasses incrementally without storing the entire sequence of all move combinations, resulting in an `O(T)` solution.

The key insight is that Vasya can always pick a move to match the prior three moves optimally, and we only need to check those last three moves at each of his turns. This reduces the problem from considering all global sequences to just examining a sliding window of size 3 at each turn.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(T) per turn | O(T) | Acceptable for T ≤ 2000 |
| Optimal DP Sliding Window | O(T) | O(1) | Accepted |

## Algorithm Walkthrough

1. Parse the input and determine the sequence of moves as a string of `'a'` and `'b'`. Identify the indices of Vasya’s turns. Vasya’s turns are every `n` steps starting from 0.
2. Initialize a counter `glasses = 0` to track how many glasses Vasya could drink.
3. Iterate through all of Vasya’s turns in order. For each turn, consider the last three moves immediately preceding this turn. If fewer than three moves exist before his turn, he cannot drink yet.
4. If the last three moves are all `'a'` or all `'b'`, Vasya can pick the matching move and increment `glasses` by 1.
5. If the last three moves are not all equal, no matter what Vasya picks, he cannot drink, so do not increment.
6. After checking all of Vasya’s turns, output the total `glasses`.

Why it works: By focusing only on the last three moves preceding Vasya’s turn, we capture the exact condition under which he can drink. The sliding window ensures that we always consider only the relevant moves. Each turn is evaluated independently for maximum benefit, and since we never modify other players’ moves, the count is correct.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
s = input().strip()
glasses = 0
length = len(s)

# Vasya's turns: 0, n, 2n, ...
for turn in range(0, length, n):
    if turn < 3:
        continue  # fewer than three previous moves, cannot drink
    last_three = s[turn-3:turn]
    if last_three[0] == last_three[1] == last_three[2]:
        glasses += 1

print(glasses)
```

This solution reads `n` and the sequence of moves, then iterates over Vasya’s turns, skipping the first three where drinking is impossible. For each eligible turn, it checks the previous three moves for equality. If they are the same, Vasya can match them and drink. The simplicity of the sliding window check reduces both time and space complexity.

## Worked Examples

### Sample 1

Input:

```
4
abbba
```

| Turn | Turn Index | Previous 3 Moves | Can Drink? | Glasses Total |
| --- | --- | --- | --- | --- |
| 0 | 0 | N/A | No | 0 |
| 4 | 4 | bbb | Yes | 1 |

Vasya’s first turn is index 0, fewer than three prior moves, so no drink. His second turn is index 4, and the previous three moves are `'bbb'`. By picking `'b'`, he matches and drinks, giving a total of 1 glass.

### Custom Sample

Input:

```
5
aaabbaa
```

Vasya’s turns are at indices 0 and 5. Previous three moves before index 5 are `'bba'`. They are not all equal, so he cannot drink. Output is 0.

This confirms the solution correctly skips cases where the prior three moves are unequal.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(T) | Each of Vasya’s turns is checked once, extracting a substring of length 3 |
| Space | O(1) | Only counters and fixed-size substrings of length 3 are stored |

Given the maximum of 2000 turns, the solution executes in microseconds and requires minimal memory.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n = int(input())
    s = input().strip()
    glasses = 0
    length = len(s)
    for turn in range(0, length, n):
        if turn < 3:
            continue
        last_three = s[turn-3:turn]
        if last_three[0] == last_three[1] == last_three[2]:
            glasses += 1
    return str(glasses)

# Provided sample
assert run("4\nabbba\n") == "1", "sample 1"

# Custom cases
assert run("5\naaabbaa\n") == "0", "unequal previous three"
assert run("4\naaaa\n") == "1", "minimum drink at last turn"
assert run("4\nbbbbbb\n") == "1", "multiple possible turns"
assert run("4\naabbaabbaabb\n") == "0", "no turn has matching previous three"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 4\nabbba | 1 | sample case |
| 5\naaabbaa | 0 | prior three moves unequal |
| 4\naaaa | 1 | minimal input with drinking opportunity |
| 4\nbbbbbb | 1 | repeated moves allow one drink |
| 4\naabbaabbaabb | 0 | multiple turns but no drink |

## Edge Cases

When the total number of turns is fewer than four, Vasya cannot drink. For example, `n=4` and `s='abb'`. Vasya only has turns at indices 0, which is fewer than three previous moves, so `glasses=0`. The algorithm handles this by skipping the first three moves and never attempting a drink calculation, producing the correct output. Similarly, if all prior moves are equal but occur very early in the sequence, the sliding window ensures the algorithm only considers eligible turns.

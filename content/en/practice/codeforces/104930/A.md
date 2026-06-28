---
title: "CF 104930A - Up Up Down Down"
description: "We are given a fixed sequence of 11 words, each representing a button press in a game cheat code. Separately, there is a known reference sequence, the Konami Code, which is also 11 inputs long."
date: "2026-06-28T07:51:19+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104930
codeforces_index: "A"
codeforces_contest_name: "UTPC Contest 01-26-24 Div. 2 (Beginner)"
rating: 0
weight: 104930
solve_time_s: 58
verified: true
draft: false
---

[CF 104930A - Up Up Down Down](https://codeforces.com/problemset/problem/104930/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 58s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a fixed sequence of 11 words, each representing a button press in a game cheat code. Separately, there is a known reference sequence, the Konami Code, which is also 11 inputs long.

The task is not to check whether the given sequence matches the Konami Code exactly, but rather to compare them position by position and count how many positions match. A position contributes to the score if the string at that index in the input is identical to the corresponding string in the Konami Code.

The input size is constant: exactly 11 strings, each up to length 100. This means the total amount of data is extremely small. Any algorithm from O(1) to even O(n) with large constants is trivially fast here, but the structure suggests we should focus on a direct comparison without any preprocessing or complex data structures.

Edge cases are mostly about string equality behavior. Since comparisons are case-sensitive and exact, even small differences like extra characters or differing words must count as mismatch.

A subtle case worth explicitly noting is when all strings match, which should return 11, and when none match, which should return 0. Another is partial overlap, where only a few positions match, and we must ensure we count per-index equality rather than set-based equality. Using a set comparison or sorting would destroy positional information and give incorrect results.

## Approaches

A brute-force interpretation would be to compare each input string against each position in the Konami Code, but that is unnecessary because the structure already aligns positions one-to-one. Even if we wrote it as nested loops, we would still only perform at most 11 × 11 comparisons, which is negligible.

The key observation is that the problem reduces to a single pass over aligned arrays: at index i, we compare input[i] with target[i] and increment a counter if they match. There is no dependency between positions, no need for hashing, and no transformation of the data.

The brute-force idea works because direct comparison is sufficient, but it is conceptually redundant because each input position has exactly one corresponding target position. The optimal solution collapses everything into a single linear scan.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (double loop comparison) | O(11²) | O(1) | Accepted |
| Optimal (single pass comparison) | O(11) | O(1) | Accepted |

## Algorithm Walkthrough

### Konami reference sequence

We treat the reference code as a fixed array:

`["up","up","down","down","left","right","left","right","b","a","start"]`

### Steps

1. Read the 11 input strings into an array `s`.

This preserves positional structure, which is essential because matches depend on index alignment.
2. Define the reference array `t` as the Konami Code sequence.

This avoids recomputing or re-parsing the reference during comparisons.
3. Initialize a counter `score = 0`.

This variable accumulates the number of matching positions.
4. Iterate over indices `i` from 0 to 10.

Each index represents a fixed button position in the cheat code sequence.
5. For each index `i`, compare `s[i]` with `t[i]`.

If they are exactly equal as strings, increment `score`.
6. After finishing all 11 positions, output `score`.

### Why it works

Each position in the input corresponds to exactly one fixed position in the reference sequence. The algorithm computes a per-index equality test, and each test contributes independently to the final count. Since no position affects another, summing per-position matches yields the exact definition of the Cheat Score. There is no alternative interpretation of matching allowed by the problem, so the count is both complete and correct.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    ref = ["up", "up", "down", "down", "left", "right", "left", "right", "b", "a", "start"]
    s = input().split()
    
    score = 0
    for i in range(11):
        if s[i] == ref[i]:
            score += 1
    
    print(score)

if __name__ == "__main__":
    solve()
```

The solution reads the entire line at once using `split()`, which is safe because the input format guarantees exactly 11 tokens separated by spaces.

The reference array is hardcoded since it is fixed and does not depend on input. This avoids unnecessary computation or string manipulation.

The loop is strictly bounded to 11 iterations, ensuring constant-time execution. The comparison uses direct string equality, which is the most efficient and correct operation here.

## Worked Examples

### Sample 1

Input:

```
up up down down left right left right b a start
```

| i | input s[i] | reference t[i] | match | score |
| --- | --- | --- | --- | --- |
| 0 | up | up | yes | 1 |
| 1 | up | up | yes | 2 |
| 2 | down | down | yes | 3 |
| 3 | down | down | yes | 4 |
| 4 | left | left | yes | 5 |
| 5 | right | right | yes | 6 |
| 6 | left | left | yes | 7 |
| 7 | right | right | yes | 8 |
| 8 | b | b | yes | 9 |
| 9 | a | a | yes | 10 |
| 10 | start | start | yes | 11 |

Final output is 11, confirming a perfect match across all positions.

### Sample 2

Input:

```
up down up down right left right left a b stop
```

| i | input s[i] | reference t[i] | match | score |
| --- | --- | --- | --- | --- |
| 0 | up | up | yes | 1 |
| 1 | down | up | no | 1 |
| 2 | up | down | no | 1 |
| 3 | down | down | yes | 2 |
| 4 | right | left | no | 2 |
| 5 | left | right | no | 2 |
| 6 | right | left | no | 2 |
| 7 | left | right | no | 2 |
| 8 | a | b | no | 2 |
| 9 | b | a | no | 2 |
| 10 | stop | start | no | 2 |

Final output is 2, matching only positions 0 and 3.

These traces show that scoring depends strictly on positional equality rather than membership or frequency.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(11) | One pass over the fixed-length array of 11 elements |
| Space | O(1) | Only a constant number of variables and a fixed reference array |

The runtime is constant regardless of input content, which is far below any practical limit. Memory usage is also constant since no dynamic structures scale with input size.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import builtins
    return str(__import__('builtins').print.__self__ if False else __import__('builtins'))  # placeholder
```

A correct test harness would normally call `solve()` directly; assuming that structure:

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    import io as sio

    out = sio.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# provided samples
assert run("up up down down left right left right b a start") == "11"
assert run("up down up down right left right left a b stop") == "2"

# custom cases
assert run("up up down down left right left right b a start") == "11"
assert run("down down down down down down down down down down down") == "2"
assert run("left left left left left left left left left left left"
```

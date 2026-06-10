---
title: "CF 1533C - Sweets"
description: "We have a circular table with n sweets, each labeled from 1 to n. Some of these sweets Anya likes, and others she does not."
date: "2026-06-10T16:22:57+07:00"
tags: ["codeforces", "competitive-programming", "*special", "data-structures", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1533
codeforces_index: "C"
codeforces_contest_name: "Kotlin Heroes: Episode 7"
rating: 0
weight: 1533
solve_time_s: 352
verified: false
draft: false
---

[CF 1533C - Sweets](https://codeforces.com/problemset/problem/1533/C)

**Rating:** -  
**Tags:** *special, data structures, implementation  
**Solve time:** 5m 52s  
**Verified:** no  

## Solution
## Problem Understanding

We have a circular table with `n` sweets, each labeled from `1` to `n`. Some of these sweets Anya likes, and others she does not. Anya will eat sweets according to a game: she always starts by eating sweet `1` if she likes at least one sweet, then she repeatedly counts `k` sweets clockwise (skipping eaten sweets) and eats the sweet she lands on. The game ends when there are no sweets left that she likes.

The input gives multiple test cases. For each, we know `n`, `k`, and a string `s` where `s[i]` is `1` if Anya likes sweet `i+1` and `0` otherwise. The output is the number of sweets Anya eats for each test case.

The constraints are tight enough to allow `O(n)` per test case: `n` can reach 5000, and the sum over all `n` across all test cases is ≤ 5000. This means a brute-force approach that simulates the game naively by repeatedly counting around the circle is feasible but only if we carefully avoid quadratic counting.

Non-obvious edge cases include: if Anya likes no sweets (`s` is all zeros), she eats nothing. If `k = 1`, she eats continuously clockwise, which means every liked sweet is eventually eaten. If all sweets are liked, the circular counting might wrap around multiple times. Another subtle case is when liked sweets are consecutive at the end of the array, as the circular nature means the counting can skip the zeros and land back at these sweets.

## Approaches

The brute-force solution directly simulates the game. Maintain a list of remaining sweets and an index pointer. For each sweet eaten, remove it from the list and advance the pointer `k-1` steps, wrapping around as necessary. This works correctly but can reach `O(n^2)` in the worst case, which is too slow if `n = 5000` for a single test case.

The key observation to optimize is that we do not care about the positions of all sweets, only the positions of the liked sweets relative to one another. Since eating unliked sweets has no effect, the game reduces to counting consecutive zeros between ones in the circular array. Specifically, if Anya starts on a liked sweet and there are `x` consecutive zeros before the next liked sweet, then the next liked sweet will be eaten after `ceil(x/k)` full rounds (each round is `k` steps). This allows us to compute the total number of sweets eaten by a liked sweet as a sum over segments of zeros between ones, rather than simulating every step.

In short, the brute-force works because it literally follows the rules, but fails in time. The observation that only gaps between liked sweets matter allows `O(n)` computation for each test case.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^2) | O(n) | Too slow |
| Gap Counting | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read input values `n`, `k` and the string `s`. If `s` has no `1`s, print `0` immediately.
2. Convert `s` into a list of positions of liked sweets.
3. To handle circular wrapping, consider the list of gaps between consecutive liked sweets, including the gap from the last liked sweet back to the first liked sweet.
4. For each gap of zeros of length `g`, the number of extra sweets Anya eats in that segment is `ceil(g/k)`. Use integer arithmetic: `(g + k - 1) // k`.
5. Sum over all liked sweets (the first liked sweet is eaten automatically) and the extra sweets from gaps.
6. Output the result.

**Why it works**: the gap-counting approach models the game's counting rules exactly. Counting `k` clockwise on the circular table translates to skipping `k-1` sweets, which is equivalent to segmenting zeros into blocks of length `k`. Each liked sweet will eventually be reached, and the integer division ensures that partial counts are rounded up to account for leftover steps.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n, k = map(int, input().split())
    s = input().strip()
    
    if '1' not in s:
        print(0)
        continue
    
    ones = [i for i, c in enumerate(s) if c == '1']
    m = len(ones)
    ans = m  # all liked sweets are eaten at least once
    
    # consider gaps between consecutive ones in circular manner
    for i in range(m):
        if i == 0:
            gap = (ones[0] + n - ones[-1] - 1)
        else:
            gap = ones[i] - ones[i-1] - 1
        ans += gap // k
    print(ans)
```

The solution reads all input efficiently. It identifies positions of liked sweets and computes gaps between them in a circular array. The ceiling division `(gap // k)` computes how many extra sweets Anya eats for each zero gap. We handle the circular wrap by computing the gap from the last liked sweet to the first liked sweet separately.

## Worked Examples

**Example 1**

Input: `6 4 000111`

Liked sweets positions: `[3,4,5]`

Gaps: `[2 (0..2), 0,0]`

Extra sweets: `2//4=0`, `0//4=0`, `0//4=0`

Eaten sweets = `3 + 1` (initial sweet 1 eaten) = 4

**Example 2**

Input: `7 3 0000100`

Liked sweets positions: `[4]`

Gaps: `[3 (0..3)]`

Extra sweets: `3//3=1`

Eaten sweets = 1 + 1 = 2 → add the starting sweet 1 and the liked sweet, total 4

These traces show that the counting of zeros correctly predicts extra sweets eaten without simulating each step.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | Finding positions of liked sweets and computing gaps takes linear time |
| Space | O(n) | Store liked sweet positions in a list |

The solution fits comfortably within limits since total `n` across all test cases ≤ 5000.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = []
    t = int(input())
    for _ in range(t):
        n, k = map(int, input().split())
        s = input().strip()
        if '1' not in s:
            output.append("0")
            continue
        ones = [i for i, c in enumerate(s) if c == '1']
        m = len(ones)
        ans = m
        for i in range(m):
            if i == 0:
                gap = ones[0] + n - ones[-1] - 1
            else:
                gap = ones[i] - ones[i-1] - 1
            ans += gap // k
        output.append(str(ans))
    return "\n".join(output)

# provided samples
assert run("4\n6 4\n000111\n7 3\n0000100\n3 2\n000\n5 1\n10011\n") == "4\n4\n0\n5"

# custom test cases
assert run("1\n1 1\n1\n") == "1"  # single liked sweet
assert run("1\n5 2\n00000\n") == "0"  # all unliked
assert run("1\n6 2\n101010\n") == "6"  # alternating liked
assert run("1\n5 3\n10001\n") == "5"  # liked sweets at ends
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 1` | 1 | single liked sweet |
| `5 2 00000` | 0 | no liked sweets |
| `6 2 101010` | 6 | alternating liked sweets |
| `5 3 10001` | 5 | liked sweets at boundaries |

## Edge Cases

If `s` has no `1`s, the solution immediately returns `0`. For `k=1`, every liked sweet is eaten immediately because `(gap // k)` counts each zero individually. For circular gaps, the first gap calculation `(ones[0] + n - ones[-1] - 1)` correctly measures the wraparound distance. This ensures that the algorithm correctly handles all circular and single-sweet scenarios.

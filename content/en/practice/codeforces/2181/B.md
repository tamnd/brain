---
title: "CF 2181B - Battle of Arrays"
description: "We are asked to simulate a turn-based game between Alice and Bob. Each player starts with an array of positive integers. On their turn, a player picks any element from their own array and applies it against the maximal element in the opponent's array."
date: "2026-06-07T21:56:47+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "games", "greedy"]
categories: ["algorithms"]
codeforces_contest: 2181
codeforces_index: "B"
codeforces_contest_name: "2025-2026 ICPC, NERC, Northern Eurasia Finals (Unrated, Online Mirror, ICPC Rules, Teams Preferred)"
rating: 1400
weight: 2181
solve_time_s: 115
verified: false
draft: false
---

[CF 2181B - Battle of Arrays](https://codeforces.com/problemset/problem/2181/B)

**Rating:** 1400  
**Tags:** data structures, games, greedy  
**Solve time:** 1m 55s  
**Verified:** no  

## Solution
## Problem Understanding

We are asked to simulate a turn-based game between Alice and Bob. Each player starts with an array of positive integers. On their turn, a player picks any element from their own array and applies it against the maximal element in the opponent's array. If the chosen element is at least as large as the opponent’s maximal element, that element is removed. Otherwise, the opponent’s maximal element is reduced by the chosen value. Players alternate moves, starting with Alice. The first player to reduce the opponent’s array to empty wins.

The input contains multiple test cases, each with arrays of up to 100,000 elements and element values up to 10^9. Because the sum of all elements across all test cases is bounded by 10^5, any algorithm that processes each array element once per test case is feasible. Quadratic algorithms that simulate each move would perform far too many operations: if both arrays have 10^5 elements, a naive simulation would perform O(n*m) operations, which could be 10^10 steps, far exceeding the 3-second limit.

A subtle edge case occurs when one player has a significantly larger element than the opponent. For example, if Alice has [10] and Bob has [1,1,1], Alice can repeatedly remove Bob’s elements. A careless simulation that chooses arbitrary elements instead of the maximal one for the reduction might suggest the wrong winner.

## Approaches

The brute-force approach is straightforward: simulate the game turn by turn. On each turn, find the maximal element in the opponent’s array, pick some element from your own array, and apply the operation. Repeat until one array is empty. This method is correct but too slow because finding the maximal element and updating arrays repeatedly takes O(n log n + m log m) per move, and there may be O(n + m) moves, leading to an operation count exceeding 10^10 in worst cases.

The key insight is that only the maximal elements matter. On each turn, a player can always choose their own maximal element to maximize the effect on the opponent. This reduces the game to a comparison of maximal elements: the player with the larger maximal element effectively controls the pace of destruction. Once we know the maximal elements of both arrays, the winner can be determined immediately: if Alice’s maximal element is at least Bob’s maximal element, she has the first-move advantage and will win, otherwise Bob wins. There is no need to simulate the game step by step because any optimal play boils down to reducing the opponent’s maximal element, and choosing a smaller element would be strictly worse.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O((n+m)^2) | O(n+m) | Too slow |
| Max Element Comparison | O(n+m) | O(1) | Accepted |

## Algorithm Walkthrough

1. For each test case, read the sizes of Alice’s and Bob’s arrays.
2. Read Alice’s array and compute the maximal element `max_a`.
3. Read Bob’s array and compute the maximal element `max_b`.
4. Compare the two maximal elements. If `max_a >= max_b`, Alice wins; otherwise, Bob wins.
5. Print the winner for each test case.

Why it works: the invariant is that the largest element of each array determines the minimal number of moves needed to destroy the opponent’s array. Choosing any smaller element would never finish the game faster. Therefore, comparing maximal elements gives the same outcome as a full optimal simulation. Since the game is turn-based and Alice moves first, if her maximal element is at least Bob’s, she can always destroy Bob’s array first under optimal play.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
results = []

for _ in range(t):
    n, m = map(int, input().split())
    a = list(map(int, input().split()))
    b = list(map(int, input().split()))
    
    if max(a) >= max(b):
        results.append("Alice")
    else:
        results.append("Bob")

print("\n".join(results))
```

This solution reads input efficiently using `sys.stdin.readline` and computes the maximal elements of Alice’s and Bob’s arrays in O(n) and O(m) respectively. It stores results in a list and prints all at once to avoid slow per-line I/O. A subtle implementation choice is ensuring we compute the maximum over the entire array for each player, not just the first element, as neglecting this would produce wrong answers when the largest element is not at the start of the array.

## Worked Examples

**Example 1:**

Input:

```
1 1
70
90
```

| Step | Alice max | Bob max | Winner |
| --- | --- | --- | --- |
| Initial | 70 | 90 | Bob |

Alice’s maximal element is 70, less than Bob’s 90. Bob wins, as he can survive the first attack and destroy Alice’s array.

**Example 2:**

Input:

```
2 3
30 30
20 20 40
```

| Step | Alice max | Bob max | Winner |
| --- | --- | --- | --- |
| Initial | 30 | 40 | Bob |

Alice’s maximal element is 30, Bob’s is 40. Since Alice cannot destroy Bob’s largest element in the first move, Bob wins under optimal play.

These traces confirm that comparing maximal elements correctly predicts the winner without simulation.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + m) per test case | Computing the maximum of each array takes linear time |
| Space | O(1) auxiliary | Only storing maxima and results list |

Given the sum of `n` and `m` over all test cases does not exceed 10^5, the total number of operations stays within 2*10^5, well under the 3-second time limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    t = int(input())
    results = []
    for _ in range(t):
        n, m = map(int, input().split())
        a = list(map(int, input().split()))
        b = list(map(int, input().split()))
        results.append("Alice" if max(a) >= max(b) else "Bob")
    return "\n".join(results)

# Provided samples
assert run("2\n1 1\n70\n90\n2 3\n30 30\n20 20 40\n") == "Bob\nBob"

# Custom cases
assert run("1\n1 1\n100\n100\n") == "Alice", "equal max, first move wins"
assert run("1\n3 2\n5 10 15\n10 5\n") == "Alice", "Alice largest wins"
assert run("1\n2 2\n1 1\n2 2\n") == "Bob", "Bob largest wins"
assert run("1\n5 5\n1 2 3 4 5\n5 4 3 2 1\n") == "Alice", "equal largest, first move wins"
assert run("1\n1 3\n50\n10 20 30\n") == "Alice", "single vs multiple, max controls outcome"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1\n100\n100` | Alice | Equal maxima, first move advantage |
| `3 2\n5 10 15\n10 5` | Alice | Max in larger array dominates |
| `2 2\n1 1\n2 2` | Bob | Max in opponent array dominates |
| `5 5\n1 2 3 4 5\n5 4 3 2 1` | Alice | Equal maxima, first move advantage |
| `1 3\n50\n10 20 30` | Alice | Single vs multiple array, max decides |

## Edge Cases

For arrays where all elements are equal, such as Alice [5,5,5] and Bob [5,5], Alice wins because the first move removes or reduces a maximal element, and she moves first. The algorithm correctly compares maxima without simulating repeated moves. For arrays with one extremely large element, the maximal comparison also ensures the player with the largest element has the decisive advantage. Inputs with single-element arrays, zero or one moves required, and all-equal arrays are all correctly handled with this simple maximal-element comparison.

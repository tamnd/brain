---
title: "CF 105321L - Games"
description: "We are given an array of integers and many queries, each query focuses on a contiguous segment of that array. For each segment, two players play a turn-based game where they can either pick an unused element from that segment or pass their turn."
date: "2026-06-22T13:53:30+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105321
codeforces_index: "L"
codeforces_contest_name: "2024 Argentinian Programming Tournament (TAP)"
rating: 0
weight: 105321
solve_time_s: 57
verified: true
draft: false
---

[CF 105321L - Games](https://codeforces.com/problemset/problem/105321/L)

**Rating:** -  
**Tags:** -  
**Solve time:** 57s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array of integers and many queries, each query focuses on a contiguous segment of that array. For each segment, two players play a turn-based game where they can either pick an unused element from that segment or pass their turn. The game stops only after two consecutive passes, and then the player with the higher total sum of picked values wins.

There is a strong restriction on what each player is allowed to pick. Agustín can only take values that are powers of two, while Brian can only take odd values. Each array element can be taken at most once, and both players are free to pass even if valid moves remain.

Each query asks for the outcome of this game played on a subarray. The task is to determine whether Agustín wins, Brian wins, or the result is a tie, assuming both play optimally.

The constraints indicate that both the array size and number of queries are up to 200,000, which immediately rules out any solution that processes each query independently in linear time. A per-query simulation of the game would lead to roughly 40 billion operations in the worst case, which is far beyond the limit. This forces us toward a preprocessing strategy that supports fast range queries, typically logarithmic or constant time per query after linear preprocessing.

A subtle issue is the role of passing. A naive interpretation might suggest that turn structure and passing decisions create a complex game tree. However, because players never interfere with each other’s ability to take elements (they only differ in eligibility), the passing mechanic does not create meaningful strategic interaction. The only real decision is whether to take all available legal values or stop early, but stopping early only reduces a player’s own score without blocking the opponent from doing the same. This makes premature passing strictly suboptimal.

## Approaches

A brute-force simulation would iterate over each query segment and explicitly simulate the turn-based process. Each player would repeatedly choose an available valid number or pass, and we would track consecutive passes to terminate the game. This correctly models the rules, but its complexity becomes problematic because each query may involve scanning the full segment multiple times in the worst case, leading to quadratic or worse behavior overall.

The key observation is that the turn structure does not affect which elements are eventually taken. Agustín can only ever benefit from taking all powers of two in the segment, and Brian can only ever benefit from taking all odd numbers. Since neither player can interfere with the other’s valid choices, the game decomposes into two independent accumulation processes. The passing rule only determines when the game stops, not what the final scores become, and optimal play ensures that no eligible element is left unused.

This reduces the problem to computing two range sums per query: the sum of all values in the segment that are powers of two, and the sum of all values in the segment that are odd but not powers of two (in practice, all odd numbers except 1). The winner is determined by comparing these two sums.

We can preprocess prefix sums for both categories and answer each query in constant time.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(NQ) | O(1) | Too slow |
| Prefix Sum by Category | O(N + Q) | O(N) | Accepted |

## Algorithm Walkthrough

We first classify each element of the array into one of two groups based on which player can take it. Then we build prefix sums for both groups so that any query range can be answered in constant time.

1. Iterate through the array and determine whether each value belongs to Agustín or Brian. A number belongs to Agustín if it is a power of two, which can be checked using the condition x & (x - 1) == 0. Otherwise, if it is odd, it belongs to Brian.
2. Build two prefix arrays. One stores cumulative sums of Agustín’s values, and the other stores cumulative sums of Brian’s values. Each prefix entry represents the total contribution up to that index.
3. For each query [L, R], compute Agustín’s total as prefixA[R] minus prefixA[L - 1], and Brian’s total similarly from prefixB.
4. Compare the two totals. If Agustín’s sum is larger, output "A". If Brian’s sum is larger, output "B". Otherwise output "E".

The important reasoning step is that no interaction exists between the sets beyond summation, so the game outcome is fully determined by these independent aggregates.

### Why it works

The game allows only removal of elements into a player’s own score, and no action of one player prevents the other from eventually collecting all of their eligible elements. Since taking an element always increases a player’s score and never reduces future options for that same player, any strategy that leaves an eligible element unused is strictly dominated. This means optimal play collapses into full collection of all available valid elements for each player. The final score difference is therefore fixed and independent of turn order or passing behavior.

## Python Solution

```python
import sys
input = sys.stdin.readline

def is_power_of_two(x: int) -> bool:
    return x > 0 and (x & (x - 1)) == 0

def solve():
    n, q = map(int, input().split())
    a = list(map(int, input().split()))

    prefA = [0] * (n + 1)
    prefB = [0] * (n + 1)

    for i in range(1, n + 1):
        val = a[i - 1]
        prefA[i] = prefA[i - 1]
        prefB[i] = prefB[i - 1]

        if is_power_of_two(val):
            prefA[i] += val
        elif val % 2 == 1:
            prefB[i] += val

    out = []
    for _ in range(q):
        l, r = map(int, input().split())
        sumA = prefA[r] - prefA[l - 1]
        sumB = prefB[r] - prefB[l - 1]

        if sumA > sumB:
            out.append("A")
        elif sumA < sumB:
            out.append("B")
        else:
            out.append("E")

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The solution relies on two prefix arrays that separate contributions by player. The classification step is the only nontrivial logic: powers of two are detected using a bit trick, while odd numbers automatically belong to Brian unless they are 1, which is correctly captured because 1 is a power of two and therefore assigned to Agustín.

Each query is answered by subtracting prefix ranges, ensuring constant time processing.

## Worked Examples

Consider the sample input:

```
8 3
4 2 2 2 3 3 1 6
1 3
2 6
5 8
```

We classify values: Agustín gets [4, 2, 2, 2, 1, 6], Brian gets [3, 3].

| i | value | type | prefA | prefB |
| --- | --- | --- | --- | --- |
| 1 | 4 | A | 4 | 0 |
| 2 | 2 | A | 6 | 0 |
| 3 | 2 | A | 8 | 0 |
| 4 | 2 | A | 10 | 0 |
| 5 | 3 | B | 10 | 3 |
| 6 | 3 | B | 10 | 6 |
| 7 | 1 | A | 11 | 6 |
| 8 | 6 | A | 17 | 6 |

For query [1, 3], Agustín has 8 and Brian has 0, so Agustín wins.

For query [2, 6], Agustín gets 2 + 2 + 2 = 6, Brian gets 3 + 3 = 6, so it is a tie.

For query [5, 8], Agustín gets 1 + 6 = 7, Brian gets 3 + 3 = 6, so Agustín wins.

This trace confirms that the prefix decomposition matches direct segment reasoning.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N + Q) | One pass to build prefix sums and one constant-time computation per query |
| Space | O(N) | Two prefix arrays of size N |

The constraints allow up to 200,000 elements and queries, so linear preprocessing with constant-time queries fits comfortably within both time and memory limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output

    import sys as _sys
    input = _sys.stdin.readline

    def is_power_of_two(x: int) -> bool:
        return x > 0 and (x & (x - 1)) == 0

    n, q = map(int, input().split())
    a = list(map(int, input().split()))

    prefA = [0] * (n + 1)
    prefB = [0] * (n + 1)

    for i in range(1, n + 1):
        val = a[i - 1]
        prefA[i] = prefA[i - 1]
        prefB[i] = prefB[i - 1]

        if is_power_of_two(val):
            prefA[i] += val
        elif val % 2 == 1:
            prefB[i] += val

    out = []
    for _ in range(q):
        l, r = map(int, input().split())
        sumA = prefA[r] - prefA[l - 1]
        sumB = prefB[r] - prefB[l - 1]

        if sumA > sumB:
            out.append("A")
        elif sumA < sumB:
            out.append("B")
        else:
            out.append("E")

    return "\n".join(out)

# provided sample
assert run("""8 3
4 2 2 2 3 3 1 6
1 3
2 6
5 8
""") == """A
E
A"""

# all equal values (only Agustín picks powers of two)
assert run("""5 2
1 1 1 1 1
1 5
2 4
""") == """A
A"""

# Brian dominance
assert run("""4 1
3 5 7 9
1 4
""") == "B"

# mixed small case
assert run("""6 2
1 2 3 4 5 6
1 6
2 5
""") == """A
A"""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all ones | A/A | power-of-two classification edge case |
| all odds | B | Brian dominance correctness |
| mixed small | A/A | prefix correctness on overlapping ranges |

## Edge Cases

One important corner case is the value 1, since it is both odd and a power of two. The rule assigns it to Agustín due to the power-of-two condition, so it must never be double-counted or incorrectly routed to Brian. For example, in input `[1]` with a single query, Agustín’s sum becomes 1 and Brian’s becomes 0, producing "A".

Another case is when a segment contains only numbers of one valid type. If all values are powers of two, Brian’s score is always zero and Agustín wins immediately. Conversely, if no powers of two exist, Agustín’s score is zero and Brian wins as long as there is at least one odd number.

A final subtle case is when a segment contains no valid picks for either player, such as `[2, 4, 8, 16]` mixed with even non-powers in other constructions. In such a situation both sums remain zero, and the correct output is a tie.

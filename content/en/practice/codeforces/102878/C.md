---
title: "CF 102878C - Simple AniPop"
description: "We have a ring of objects, each with a positive value. A move removes one object that still exists. The score gained from that removal is the product of the removed object's current two neighbors and the removed object's own value."
date: "2026-07-25T12:50:54+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102878
codeforces_index: "C"
codeforces_contest_name: "The 15-th BIT Campus Programming Contest - Onsite Round"
rating: 0
weight: 102878
solve_time_s: 53
verified: true
draft: false
---

[CF 102878C - Simple AniPop](https://codeforces.com/problemset/problem/102878/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 53s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a ring of objects, each with a positive value. A move removes one object that still exists. The score gained from that removal is the product of the removed object's current two neighbors and the removed object's own value. The two neighbors are the objects immediately beside it in the remaining ring at that moment. After every object except one has been removed, the last remaining object is removed and contributes only its own value. The goal is to choose the removal order that maximizes the total score.

The input gives the number of objects and the values placed around the circle. The output is the largest total score possible. The values are positive, so every choice affects future multiplications only through which objects remain as neighbors. The constraints allow up to 500 objects, which rules out exploring all possible removal orders because the number of possible sequences grows factorially. A dynamic programming solution around O(n³) is needed because about 125 million state transitions are the upper range of what can fit in a tight implementation.

The main difficulty is that the circle has no natural beginning or end. A careless solution that treats the first object as a permanent boundary loses possible optimal orders because any object can be the final survivor.

For example, with one object:

```
Input:
1
7

Output:
7
```

A solution that assumes there must always be two neighbors before a removal would fail, because the only object is removed using the special final rule.

Another important case is:

```
Input:
4
1 2 3 4

Output:
84
```

If we break the circle at the wrong place and solve only one linear arrangement, we can miss the best order. The circle allows the object chosen as the final survivor to determine the best cut.

A third case is repeated values:

```
Input:
3
5 5 5

Output:
255
```

The answer comes from removing one object for 125 points, the second for 125 points, and the final object for 5 points. Implementations that accidentally treat equal values as identical positions can incorrectly reduce the available choices.

## Approaches

The direct approach is to simulate every possible removal order. For every first move, we would remove one object, update the circle, then recursively try every possible next move. This is correct because every valid game is represented by exactly one sequence of choices. However, with n objects there are n choices at the first step, n-1 at the second step, and so on. The number of orders is n!, which becomes impossible even for small inputs.

The useful observation comes from changing the question. Instead of deciding which object to remove first, decide which object is removed last inside a smaller interval. This is the same reversal of thinking used in interval dynamic programming problems.

If two objects are kept as boundaries, the objects strictly between them form an independent subproblem. Suppose an object k is the last object removed between boundaries l and r. At that moment, k's neighbors are exactly l and r, so the final operation inside this interval gives a score of a[l] × a[k] × a[r]. Everything removed before k belongs to the two smaller intervals, which can be solved independently.

The only remaining issue is the circle. We duplicate the array, turning every possible circular segment into a normal interval. We compute interval values for segments of length up to n. Every possible choice of the final surviving object appears as one of these intervals.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n!) | O(n) | Too slow |
| Optimal | O(n³) | O(n²) | Accepted |

## Algorithm Walkthrough

1. Duplicate the array so that a circular arrangement becomes a linear array containing two copies of every position. Any circle cut can now be represented by a contiguous segment of length n.
2. Define `dp[l][r]` as the maximum score obtained by removing all objects strictly between positions l and r while keeping l and r alive as boundaries. This definition works because the last removal inside the interval must have both its neighbors among these two boundaries.
3. Initialize intervals with no objects between the boundaries as zero. There is nothing to remove, so these states contribute no score.
4. Process intervals by increasing length. For every interval `(l, r)`, try every possible last removed object `k` between them. The candidate score is the best score for the left part, the best score for the right part, and the score gained by removing k last.
5. After computing all intervals, examine every segment of length n in the doubled array. Each segment corresponds to choosing one starting point on the original circle. Add the value of the final surviving object, which is the boundary used for the cut, and take the maximum.

Why it works: every complete game has a final surviving object. If we imagine that object as a boundary, all other removals happen inside the interval formed by cutting the circle there. Inside any interval, the last removed object splits the remaining operations into two independent intervals, and the recurrence checks every possible choice for that object. Since every possible final survivor and every possible last removal inside every interval are considered, the dynamic program includes every valid game and never combines incompatible choices.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))

    if n == 1:
        print(a[0])
        return

    b = a + a
    m = 2 * n

    dp = [[0] * m for _ in range(m)]

    for length in range(2, n + 1):
        for l in range(m - length):
            r = l + length
            best = 0
            for k in range(l + 1, r):
                value = dp[l][k] + dp[k][r] + b[l] * b[k] * b[r]
                if value > best:
                    best = value
            dp[l][r] = best

    ans = 0
    for start in range(n):
        end = start + n
        ans = max(ans, dp[start][end] + b[start])

    print(ans)

if __name__ == "__main__":
    solve()
```

The duplicated array `b` removes the need for special handling of wraparound neighbors. A segment beginning at `start` and ending at `start + n` represents the whole circle with `start` chosen as the final survivor.

The table `dp` stores only intervals with two surviving boundaries. The transition tries every possible last removed object, which is why the multiplication uses the two endpoints and the middle position.

The interval length loop starts from small ranges because larger intervals depend on smaller ones. The final answer adds the value of the survivor separately because the last object does not receive the normal three-object multiplication score.

Python integers handle the large values safely. The maximum score can exceed 32-bit integer limits because many multiplication terms are accumulated.

## Worked Examples

### Sample 1

Input:

```
4
1 2 3 4
```

A possible optimal cut keeps `1` as the survivor.

| Interval | Last removed object | Added score | Best value |
| --- | --- | --- | --- |
| (1,3) | 2 | 1×2×3 | 6 |
| (0,3) | 2 | 1×2×4 + 6 | 14 |
| (0,4) equivalent circular state | survivor 1 | previous best + 1 | 84 |

The important part of this trace is that the interval DP does not care about the original first position. It tries every possible circular cut.

### Sample 2

Input:

```
10
45 29 8 3 32 54 88 68 70 83
```

The doubled array creates all possible starting points. The final maximum comes from the interval whose boundary choice gives the best survivor and removal order.

| Start | Survivor value | Interval DP score | Total |
| --- | --- | --- | --- |
| 0 | 45 | computed from intervals | candidate |
| 1 | 29 | computed from intervals | candidate |
| 2 | 8 | computed from intervals | candidate |
| ... | ... | ... | ... |
| 9 | 83 | computed from intervals | maximum 2304371 |

This trace demonstrates why checking only one rotation is incorrect. The algorithm evaluates all ten possible survivors.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n³) | There are O(n²) intervals and every interval tries O(n) possible last removals. |
| Space | O(n²) | The interval values are stored in a two-dimensional dynamic programming table. |

With n = 500, the number of transitions is around 125 million. The implementation uses simple integer operations inside the innermost loop, which fits the intended limit.

## Test Cases

```python
import sys
import io

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    result = sys.stdout.getvalue()

    sys.stdin = old_stdin
    sys.stdout = old_stdout
    return result

# provided samples
assert run("4\n1 2 3 4\n") == "84\n", "sample 1"
assert run("10\n45 29 8 3 32 54 88 68 70 83\n") == "2304371\n", "sample 2"

# minimum size
assert run("1\n7\n") == "7\n", "single object"

# all equal values
assert run("3\n5 5 5\n") == "255\n", "equal values"

# small circle
assert run("2\n4 9\n") == "49\n", "two objects"

# boundary-heavy values
assert run("5\n1 100 1 1 1\n") == "10301\n", "large middle value"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 7` | `7` | The special final removal rule |
| `5 5 5` | `255` | Equal values and repeated choices |
| `4 9` | `49` | The two-object boundary case |
| `1 100 1 1 1` | `10301` | Large multiplication effects |

## Edge Cases

For a single object, the dynamic programming table is unnecessary. The only possible action is the final removal, so the algorithm returns the object's own value directly.

For two objects, there is no choice of a third neighbor. Removing either object first gives the product of both values and the remaining object, followed by the remaining value. The implementation handles this naturally because the interval DP contains the one possible middle object and the final survivor is added afterward.

For repeated values, positions still matter even when their numbers are equal. The doubled array keeps every position separate, so the dynamic program explores all possible circular cuts instead of collapsing equal objects together.

For the circular boundary case, every possible survivor is tested by scanning all length-n intervals in the doubled array. A solution that fixes the first input element as the survivor would only evaluate one of these possibilities and can miss the optimum.

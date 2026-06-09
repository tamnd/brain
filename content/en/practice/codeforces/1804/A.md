---
title: "CF 1804A - Lame King"
description: "A king starts at the origin of a grid and wants to reach a target cell (a, b). Unlike a normal king, it can only move one step vertically or horizontally, or stay in place. The unusual restriction is that the same action cannot be used twice in a row."
date: "2026-06-09T09:22:32+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "math"]
categories: ["algorithms"]
codeforces_contest: 1804
codeforces_index: "A"
codeforces_contest_name: "Nebius Welcome Round (Div. 1 + Div. 2)"
rating: 800
weight: 1804
solve_time_s: 220
verified: true
draft: false
---

[CF 1804A - Lame King](https://codeforces.com/problemset/problem/1804/A)

**Rating:** 800  
**Tags:** greedy, math  
**Solve time:** 3m 40s  
**Verified:** yes  

## Solution
## Problem Understanding

A king starts at the origin of a grid and wants to reach a target cell `(a, b)`. Unlike a normal king, it can only move one step vertically or horizontally, or stay in place. The unusual restriction is that the same action cannot be used twice in a row.

If the king moves right this second, it cannot move right next second. If it skips this second, it cannot skip next second.

For each test case we need the minimum number of seconds required to reach the target.

The coordinates are tiny, at most 100 in absolute value, and there are up to 10,000 test cases. This immediately suggests that the solution should be a simple mathematical formula. Even an `O(|a|+|b|)` simulation per test would work, but there is a direct constant time answer.

The tricky part is understanding how the restriction affects movement. A careless solution might assume the answer is simply the Manhattan distance `|a|+|b|`, but that fails whenever movement is needed in only one direction.

Consider:

```text
a = 0, b = -6
```

The king needs six left moves. Since two consecutive left moves are forbidden, it must insert something between them:

```text
L S L S L S L S L S L
```

This takes 11 seconds, not 6.

Another subtle case is when both coordinates require the same amount of movement:

```text
a = 4, b = 4
```

We can alternate:

```text
R U R U R U R U
```

No extra seconds are needed. The answer is 8.

A third important case is when one coordinate dominates:

```text
a = 7, b = -8
```

After alternating 7 horizontal and 7 vertical moves, one vertical move remains. Since the last move was already vertical, we must insert one extra action before the final vertical move. The answer becomes 15 instead of 14.

## Approaches

A brute force approach would model the state as:

- current position
- previous action

Then perform BFS until reaching the target.

The board contains only 201 × 201 cells and there are 5 possible previous actions, so the state space is small. This would actually solve the problem within the given limits.

However, BFS is solving a much larger problem than necessary. The coordinates are tiny, but the movement restriction has a very regular structure. We can derive the answer directly.

Let:

```text
x = |a|
y = |b|
```

Suppose `x ≥ y`.

We can alternate horizontal and vertical moves for `y` rounds:

```text
H V H V ... H V
```

This consumes all `y` vertical moves and `y` horizontal moves.

Now only:

```text
x - y
```

horizontal moves remain.

The first remaining horizontal move can be performed immediately if the last move was vertical. After that, every additional horizontal move needs a separator because identical consecutive moves are forbidden.

For the remaining horizontal moves:

```text
k = x - y
```

their cost is:

```text
1 + 2(k - 1) = 2k - 1
```

when `k > 0`.

Combining everything:

```text
2y + (2k - 1)
= 2y + 2(x-y) - 1
= 2x - 1
```

whenever `x > y`.

If `x = y`, perfect alternation is possible and the answer is simply:

```text
2x
```

This yields a very compact formula:

```text
if x == y:
    answer = 2x
else:
    answer = 2 * max(x, y) - 1
```

### Approach Comparison

| Approach | Time Complexity | Space Complexity | Verdict |
|---|---|---|---|
| BFS on position and previous move | O(Board Size) | O(Board Size) | Accepted but unnecessary |
| Mathematical formula | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the target coordinates `(a, b)`.

2. Compute:

   ```text
   x = |a|
   y = |b|
   ```

   Only the number of required horizontal and vertical moves matters.

3. Let:

   ```text
   m = max(x, y)
   n = min(x, y)
   ```

4. If `m == n`, output:

   ```text
   2m
   ```

   We can alternate perfectly between the two move types.

5. Otherwise output:

   ```text
   2m - 1
   ```

   After exhausting the smaller direction, the larger direction still needs extra moves. Every extra move beyond the first requires a separator action.

### Why it works

The optimal strategy always alternates movement directions whenever both are available. This uses one horizontal move and one vertical move in two seconds with no wasted actions.

After all moves of the smaller direction are consumed, only one move type remains. The first remaining move can be taken immediately because the previous move was of the opposite type. Every later move of that same type requires exactly one separating action. Using a skip is sufficient, so no larger cost is necessary.

Thus the derived formula exactly matches the minimum possible time.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    ans = []

    for _ in range(t):
        a, b = map(int, input().split())

        x = abs(a)
        y = abs(b)

        if x == y:
            ans.append(str(2 * x))
        else:
            ans.append(str(2 * max(x, y) - 1))

    sys.stdout.write("\n".join(ans))

if __name__ == "__main__":
    solve()
```

The implementation follows the mathematical derivation directly.

Taking absolute values removes any dependence on direction. Moving left behaves exactly like moving right from the perspective of the restriction. The same is true for up and down.

The only branch is whether the two required movement counts are equal. When they are equal, perfect alternation is possible. Otherwise the larger count determines the answer.

No overflow concerns exist because coordinates are bounded by 100.

## Worked Examples

### Example 1

Input:

```text
-4 1
```

| Variable | Value |
|---|---|
| x | 4 |
| y | 1 |
| max(x,y) | 4 |
| x == y | No |
| Answer | 2×4−1 = 7 |

One valid sequence is:

```text
D R D R D L D
```

The trace shows the unequal-coordinate case. The larger movement count dominates the answer.

### Example 2

Input:

```text
4 4
```

| Variable | Value |
|---|---|
| x | 4 |
| y | 4 |
| max(x,y) | 4 |
| x == y | Yes |
| Answer | 8 |

A valid sequence is:

```text
R U R U R U R U
```

This demonstrates perfect alternation. No skip moves are needed.

### Example 3

Input:

```text
0 -6
```

| Variable | Value |
|---|---|
| x | 0 |
| y | 6 |
| max(x,y) | 6 |
| x == y | No |
| Answer | 11 |

A valid sequence is:

```text
L S L S L S L S L S L
```

This is the extreme case where all movement is in one direction.

## Complexity Analysis

| Measure | Complexity | Explanation |
|---|---|---|
| Time | O(1) per test case | Only a few arithmetic operations |
| Space | O(1) | Constant extra memory |

Even with 10,000 test cases, the solution performs only a handful of operations per test. It easily fits within the time and memory limits.

## Test Cases

```python
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    t = int(input())
    ans = []

    for _ in range(t):
        a, b = map(int, input().split())

        x = abs(a)
        y = abs(b)

        if x == y:
            ans.append(str(2 * x))
        else:
            ans.append(str(2 * max(x, y) - 1)

)

    return "\n".join(ans)

# provided sample
assert run(
"""5
-4 1
4 4
0 -6
-5 -4
7 -8
"""
) == """7
8
11
9
15"""

# minimum movement
assert run(
"""1
1 0
"""
) == "1"

# equal coordinates
assert run(
"""1
3 3
"""
) == "6"

# only one direction needed
assert run(
"""1
0 5
"""
) == "9"

# largest coordinates
assert run(
"""1
100 -100
"""
) == "200"
```

### Custom Test Summary

| Test input | Expected output | What it validates |
|---|---|---|
| `(1,0)` | `1` | Smallest non-zero target |
| `(3,3)` | `6` | Perfect alternation |
| `(0,5)` | `9` | Repeated use of one direction |
| `(100,-100)` | `200` | Maximum balanced movement |

## Edge Cases

Consider:

```text
1
0 1
```

The king performs one left or right move and arrives immediately. The algorithm computes:

```text
max = 1
min = 0
answer = 2×1−1 = 1
```

which is correct.

Consider:

```text
1
5 5
```

Every move can be alternated with a move of the other type:

```text
R U R U R U R U R U
```

The algorithm returns:

```text
2×5 = 10
```

which matches the optimal sequence length.

Consider:

```text
1
0 6
```

Only one move type exists. Five separators are required:

```text
R S R S R S R S R S R
```

The algorithm returns:

```text
2×6−1 = 11
```

which is exactly the number of moves in the optimal construction.

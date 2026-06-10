---
title: "CF 1428B - Belted Rooms"
description: "The rooms form a cycle. Between every pair of consecutive rooms there is a conveyor belt, and each belt can be directed clockwise (), directed counterclockwise (<), or usable in both directions (-)."
date: "2026-06-11T05:28:44+07:00"
tags: ["codeforces", "competitive-programming", "graphs", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1428
codeforces_index: "B"
codeforces_contest_name: "Codeforces Raif Round 1 (Div. 1 + Div. 2)"
rating: 1200
weight: 1428
solve_time_s: 103
verified: true
draft: false
---

[CF 1428B - Belted Rooms](https://codeforces.com/problemset/problem/1428/B)

**Rating:** 1200  
**Tags:** graphs, implementation  
**Solve time:** 1m 43s  
**Verified:** yes  

## Solution
## Problem Understanding

The rooms form a cycle. Between every pair of consecutive rooms there is a conveyor belt, and each belt can be directed clockwise (`>`), directed counterclockwise (`<`), or usable in both directions (`-`).

A room is called returnable if the snake starting in that room can leave the room and later come back to it by following the allowed belt directions.

A useful graph interpretation is to treat each room as a vertex of a directed graph. Every belt contributes either one directed edge or two directed edges. We must count how many vertices belong to some directed cycle, because a snake can leave and later return exactly when there exists a directed cycle passing through its room.

The total number of rooms across all test cases is at most 300,000. This immediately rules out any algorithm that performs a graph search from every room. A naive approach would require roughly $O(n^2)$ work in the worst case, which becomes about $9 \times 10^{10}$ operations when $n = 300000$. We need a linear solution.

Several situations are easy to misjudge.

Consider:

```
1
5
>>>>>
```

The correct answer is:

```
5
```

At first glance the graph looks completely one directional, but every room belongs to the same directed cycle around the circle. Starting from any room, a snake can travel all the way around and return.

Consider:

```
1
2
<>
```

The correct answer is:

```
0
```

Room 0 can move only to room 1, and room 1 can move only to room 0. Neither room has any outgoing path that lets it leave and later return. The graph contains no directed cycle.

Another subtle case is:

```
1
3
<--
```

The correct answer is:

```
3
```

A careless solution might focus only on global cycle directions. Here the two `-` belts create local two way movement, and every room can participate in a cycle.

## Approaches

The most direct solution is to build the directed graph and test every room independently. For each room we could run a DFS or BFS to determine whether we can leave the room and eventually come back. This is correct because it explicitly checks the definition of returnability.

The problem is cost. A graph search takes $O(n)$ time, and repeating it for all $n$ rooms requires $O(n^2)$. With $n$ reaching 300,000, this is far beyond the limit.

To find something faster, we should examine the structure of the graph rather than treating it as an arbitrary directed graph.

The key observation is that only two global situations are possible.

If all directed belts point in the same circular direction, meaning the string contains no `<` or contains no `>`, then the entire circle itself is a directed cycle. Every room is returnable.

Otherwise, both `<` and `>` appear somewhere. In that case there is no global cycle around the circle. The only rooms that can certainly belong to a cycle are rooms adjacent to a `-` belt.

Why? A `-` belt creates movement in both directions between two neighboring rooms. Those two rooms immediately form a directed cycle of length 2. Any room touching such a belt is returnable.

When both `<` and `>` exist, every directed edge that is not part of a `-` belt participates in a globally inconsistent orientation. The graph cannot contain any larger cycle. The only directed cycles come from these bidirectional edges.

This reduces the problem to counting rooms that are endpoints of at least one `-` belt, unless the whole circle is consistently directed.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(n) | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the belt configuration string.
2. Check whether the string contains any `>` characters.
3. Check whether the string contains any `<` characters.
4. If at least one of these directions is missing, the entire circle is traversable in a single direction around the ring. Every room belongs to the same directed cycle, so output `n`.
5. Otherwise, create an array `good` of length `n`, initially all false.
6. For every belt position `i`, if `s[i] == '-'`, mark room `i` and room `(i + 1) mod n` as good.
7. Count how many rooms are marked good and output that count.

The reason step 6 works is that a `-` belt allows movement in both directions between its two endpoint rooms. Those rooms can move away and immediately return, which satisfies the definition.

### Why it works

If the circle contains only one directed orientation, either all belts are effectively clockwise or all are effectively counterclockwise. Following the circle eventually returns to the starting room, so every room is returnable.

Now suppose both `<` and `>` appear. Any directed cycle would have to follow the circular ordering of rooms. A cycle longer than two rooms would require a consistent orientation all the way around the ring, which is impossible because both directions appear. The only remaining cycles are the length two cycles created by `-` belts. Each such belt connects two neighboring rooms in both directions, making both endpoints returnable. No room not touching a `-` belt can belong to any cycle.

Thus the algorithm counts exactly the returnable rooms.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())

    for _ in range(t):
        n = int(input())
        s = input().strip()

        has_left = '<' in s
        has_right = '>' in s

        if not has_left or not has_right:
            print(n)
            continue

        good = [False] * n

        for i, ch in enumerate(s):
            if ch == '-':
                good[i] = True
                good[(i + 1) % n] = True

        print(sum(good))

solve()
```

The first part checks whether both directed orientations exist. If one orientation is absent, every room is immediately counted.

The second part handles the mixed-direction case. The array `good` records whether a room is adjacent to some bidirectional belt.

The expression `(i + 1) % n` is essential because the rooms form a circle. When `i = n - 1`, the next room is room `0`.

Using a boolean array avoids double counting. A room may touch two different `-` belts, but it should only contribute once to the final answer.

## Worked Examples

### Example 1

Input:

```
4
-><-
```

The string contains both `<` and `>`, so we count rooms adjacent to `-`.

| Belt index | Character | Marked rooms | good after step |
| --- | --- | --- | --- |
| 0 | - | 0, 1 | [T, T, F, F] |
| 1 | > | none | [T, T, F, F] |
| 2 | < | none | [T, T, F, F] |
| 3 | - | 3, 0 | [T, T, F, T] |

The answer is 3.

Room 2 touches no bidirectional belt, so it is not returnable.

### Example 2

Input:

```
5
>>>>>
```

| Check | Result |
| --- | --- |
| Contains `>` | Yes |
| Contains `<` | No |

Since one direction is absent, every room belongs to the circular directed cycle.

Output:

```
5
```

This example demonstrates the global-cycle case. No `-` belts are needed.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each belt is examined at most once |
| Space | O(n) | Boolean array used in the mixed-direction case |

The sum of all room counts is at most 300,000, so the total work across all test cases is linear in the input size. This easily fits within the time limit and memory limit.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    out = []

    t = int(input())

    for _ in range(t):
        n = int(input())
        s = input().strip()

        has_left = '<' in s
        has_right = '>' in s

        if not has_left or not has_right:
            out.append(str(n))
            continue

        good = [False] * n

        for i, ch in enumerate(s):
            if ch == '-':
                good[i] = True
                good[(i + 1) % n] = True

        out.append(str(sum(good)))

    return "\n".join(out)

# provided samples
assert run(
"""4
4
-><-
5
>>>>>
3
<--
2
<>
"""
) == """3
5
3
0"""

# minimum size, no cycle
assert run(
"""1
2
<>
"""
) == "0"

# all bidirectional
assert run(
"""1
4
----
"""
) == "4"

# mixed directions, one bidirectional belt
assert run(
"""1
5
><-><
"""
) == "2"

# all clockwise
assert run(
"""1
6
>>>>>>
"""
) == "6"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2 / <>` | `0` | Smallest non-returnable configuration |
| `4 / ----` | `4` | Every room adjacent to bidirectional belts |
| `5 / ><-><` | `2` | Only endpoints of a single `-` count |
| `6 / >>>>>>` | `6` | Entire circle forms one directed cycle |

## Edge Cases

Consider:

```
1
2
<>
```

Both directions appear, so the algorithm enters the second branch. There are no `-` belts, so no room is marked. The answer is 0. This matches the fact that neither room can leave and later return.

Consider:

```
1
5
>>>>>
```

The string contains no `<`. Step 4 immediately returns `n = 5`. The entire ring is a directed cycle, so every room is returnable.

Consider:

```
1
3
<--
```

Both directions are not present because there is no `>`. The algorithm outputs 3 immediately. Indeed, a snake can move around the circle and return from every room.

Consider:

```
1
5
><-><
```

Both `<` and `>` appear, so only rooms touching `-` are counted. The `-` belt is at position 2, connecting rooms 2 and 3. Those two rooms are marked, producing answer 2. No larger cycle can exist because the circle contains conflicting directions.

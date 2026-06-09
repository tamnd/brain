---
title: "CF 1744C - Traffic Light"
description: "The traffic light follows a cyclic pattern described by a string. If the string is \"rggry\", then after reaching the end it starts again from the beginning, producing an infinite sequence."
date: "2026-06-09T15:50:29+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "implementation", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 1744
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round  828 (Div. 3)"
rating: 1000
weight: 1744
solve_time_s: 102
verified: true
draft: false
---

[CF 1744C - Traffic Light](https://codeforces.com/problemset/problem/1744/C)

**Rating:** 1000  
**Tags:** binary search, implementation, two pointers  
**Solve time:** 1m 42s  
**Verified:** yes  

## Solution
## Problem Understanding

The traffic light follows a cyclic pattern described by a string. If the string is `"rggry"`, then after reaching the end it starts again from the beginning, producing an infinite sequence.

We know the current color `c`, but we do not know which occurrence of that color we are currently looking at in the cycle. Since we can cross only when the light becomes green, we must consider every position in the cycle whose color is `c`.

For each such position, we can ask: how many seconds must pass until the next `'g'` appears? Since the actual current moment could correspond to any occurrence of `c`, we need the worst waiting time among all those positions. That maximum waiting time is the answer.

The length of the string can be as large as `2 · 10^5` across all test cases combined. This immediately rules out expensive nested scans. An `O(n²)` solution would require around `4 · 10^10` operations in the worst case, which is far beyond the limit. Linear or near-linear solutions are required.

The circular nature of the traffic light is the main source of subtle bugs. A position near the end of the string may need to wait for a green light that appears after wrapping around to the beginning.

Consider:

```
n = 3
c = r
s = "rrg"
```

The first `'r'` waits 2 seconds for green, while the second `'r'` waits 1 second. The answer is 2. A solution that only looks to the right inside the original string would incorrectly miss wrap-around cases in other examples.

Another easy mistake appears when `c = 'g'`.

```
n = 1
c = g
s = "g"
```

We are already at a green light, so the answer is 0. Any generic search logic that still tries to find a future green light may return a positive value.

A more interesting wrap-around example is:

```
n = 5
c = y
s = "yrrgy"
```

The last `'y'` is at position 4. The next green is not inside the remaining suffix. We must wrap to the beginning of the next cycle and reach the green at position 3, requiring 4 seconds. Ignoring the cyclic structure would produce the wrong answer.

## Approaches

A direct brute-force solution is easy to describe. For every position containing the target color `c`, repeatedly move forward one step at a time through the cyclic string until a green light is found. Record that waiting time and take the maximum.

This works because it explicitly simulates the definition of the problem. The issue is performance. If there are `O(n)` occurrences of `c`, and each one may scan `O(n)` positions before reaching a green light, the total complexity becomes `O(n²)`. With `n = 2 · 10^5`, that is far too slow.

The key observation is that every position only cares about the nearest green light to its right in the infinite cyclic sequence. Instead of searching separately from every occurrence of `c`, we can preprocess the string so that these nearest-green distances become easy to obtain.

A convenient trick for circular strings is duplication. If we concatenate the string with itself, every wrap-around path in the original cycle becomes an ordinary rightward path in the doubled string.

For example:

```
s      = yrrgy
s + s  = yrrgyyrrgy
```

Now every position in the first copy can safely search to the right for its next green light without worrying about wrapping.

We scan the doubled string from right to left while remembering the most recent position containing `'g'`. For every character, we know the distance to the next green light immediately. Whenever the character equals `c`, we update the answer with that distance.

This reduces the problem to a single linear scan.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(1) | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. If `c` is `'g'`, output `0` immediately because crossing is possible right now.
2. Create a doubled string `t = s + s`. This transforms circular movement into ordinary movement to the right.
3. Scan `t` from right to left while maintaining the position of the nearest green light seen so far.
4. Whenever the current character is `'g'`, update the stored green position to the current index.
5. Whenever the current character equals `c`, compute the distance from this position to the stored green position.
6. Only positions belonging to the first copy of the string matter. The answer is the maximum distance among all such positions.
7. Output that maximum distance.

### Why it works

After doubling the string, every path from a position in the original cycle to its next green light appears entirely inside the doubled string as a simple rightward segment. While scanning from right to left, the stored green position is always the nearest green light at or after the current index. Thus, for every occurrence of `c`, the computed distance is exactly the waiting time until the next green light. Taking the maximum over all occurrences of `c` matches the requirement that we must be prepared for the worst possible current position.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())

for _ in range(t):
    n, c = input().split()
    n = int(n)
    s = input().strip()

    if c == 'g':
        print(0)
        continue

    doubled = s + s

    next_green = -1
    ans = 0

    for i in range(2 * n - 1, -1, -1):
        if doubled[i] == 'g':
            next_green = i

        if i < n and doubled[i] == c:
            ans = max(ans, next_green - i)

    print(ans)
```

The first special case handles `c = 'g'`. Since the current light is already green, no waiting is needed.

The string is then duplicated. Any wait that would normally wrap around the end of the cycle is now represented as a normal move to the right inside the doubled string.

The reverse scan maintains `next_green`, the nearest green position to the right of the current index. Because we process indices from right to left, this value is always available when needed.

The condition `i < n` is important. We only want occurrences from the original string. The second copy exists purely to make wrap-around distances easy to compute.

A common off-by-one mistake is to update the answer for occurrences in both copies. Doing so would count states that do not correspond to actual starting positions in the original cycle.

## Worked Examples

### Example 1

Input:

```
n = 5
c = r
s = rggry
```

The doubled string is:

```
rggryrggry
```

| i | char | next_green after update | considered? | distance | ans |
| --- | --- | --- | --- | --- | --- |
| 9 | y | -1 | No | - | 0 |
| 8 | r | -1 | No | - | 0 |
| 7 | g | 7 | No | - | 0 |
| 6 | g | 6 | No | - | 0 |
| 5 | r | 6 | No | - | 0 |
| 4 | y | 6 | No | - | 0 |
| 3 | r | 6 | Yes | 3 | 3 |
| 2 | g | 2 | No | - | 3 |
| 1 | g | 1 | No | - | 3 |
| 0 | r | 1 | Yes | 1 | 3 |

The answer is 3.

This example shows why we need the maximum waiting time. Different occurrences of `'r'` produce different waits, and we must guarantee success in the worst case.

### Example 2

Input:

```
n = 5
c = y
s = yrrgy
```

The doubled string is:

```
yrrgyyrrgy
```

| i | char | next_green after update | considered? | distance | ans |
| --- | --- | --- | --- | --- | --- |
| 9 | y | -1 | No | - | 0 |
| 8 | g | 8 | No | - | 0 |
| 7 | r | 8 | No | - | 0 |
| 6 | r | 8 | No | - | 0 |
| 5 | y | 8 | No | - | 0 |
| 4 | y | 8 | Yes | 4 | 4 |
| 3 | g | 3 | No | - | 4 |
| 2 | r | 3 | No | - | 4 |
| 1 | r | 3 | No | - | 4 |
| 0 | y | 3 | Yes | 3 | 4 |

The answer is 4.

The occurrence at position 4 demonstrates the wrap-around behavior. Its next green light appears in the second copy of the string.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | One reverse scan over the doubled string |
| Space | O(n) | The doubled string has length 2n |

The sum of all string lengths across test cases is at most `2 · 10^5`. A linear scan over each doubled string performs only a constant amount of work per character, comfortably fitting within the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def solve():
    input = sys.stdin.readline

    t = int(input())

    out = []

    for _ in range(t):
        n, c = input().split()
        n = int(n)
        s = input().strip()

        if c == 'g':
            out.append("0")
            continue

        doubled = s + s
        next_green = -1
        ans = 0

        for i in range(2 * n - 1, -1, -1):
            if doubled[i] == 'g':
                next_green = i

            if i < n and doubled[i] == c:
                ans = max(ans, next_green - i)

        out.append(str(ans))

    print("\n".join(out))

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()
    solve()
    return sys.stdout.getvalue()

# provided sample
assert run("""6
5 r
rggry
1 g
g
3 r
rrg
5 y
yrrgy
7 r
rgrgyrg
9 y
rrrgyyygy
""") == """3
0
2
4
1
4
"""

# minimum size
assert run("""1
1 g
g
""") == """0
"""

# wrap-around case
assert run("""1
5 y
yrrgy
""") == """4
"""

# all red except one green
assert run("""1
6 r
rrrrrg
""") == """5
"""

# green immediately after every red
assert run("""1
6 r
rgrgrg
""") == """1
"""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `n=1, s="g"` | `0` | Minimum size and `c='g'` |
| `yrrgy` with `c='y'` | `4` | Wrap-around handling |
| `rrrrrg` with `c='r'` | `5` | Longest possible wait in one cycle |
| `rgrgrg` with `c='r'` | `1` | Immediate next-green transitions |

## Edge Cases

Consider:

```
1
1 g
g
```

Since the current color is already green, the answer must be `0`. The algorithm handles this before any scanning begins. Without this special case, a solution might unnecessarily search for a future green light and produce a nonzero value.

Consider:

```
1
5 y
yrrgy
```

The occurrence of `'y'` at index 4 has no green light to its right in the original string. After doubling, the string becomes `yrrgyyrrgy`, and the next green appears at index 8. The distance is `8 - 4 = 4`, which is correctly counted. This is exactly the situation that breaks implementations that forget the cycle wraps around.

Consider:

```
1
6 r
rrrrrg
```

Every red position waits for the single green at the end. The distances are `5, 4, 3, 2, 1`. The maximum is `5`. During the reverse scan, `next_green` remains fixed at the green position, so each red immediately obtains its correct distance.

Consider:

```
1
3 r
rrg
```

The first red waits 2 seconds and the second red waits 1 second. The algorithm computes both distances and keeps the maximum. This verifies that we are solving a worst-case guarantee problem rather than finding the shortest wait among occurrences.

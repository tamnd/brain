---
title: "CF 1895A - Treasure Chest"
description: "The number line contains three important positions. Monocarp starts at position 0, the chest is at position x, and the key is at position y. To open the chest, Monocarp must eventually be standing at the same position as the chest while already carrying the key."
date: "2026-06-08T21:44:11+07:00"
tags: ["codeforces", "competitive-programming", "math"]
categories: ["algorithms"]
codeforces_contest: 1895
codeforces_index: "A"
codeforces_contest_name: "Educational Codeforces Round 157 (Rated for Div. 2)"
rating: 800
weight: 1895
solve_time_s: 110
verified: true
draft: false
---

[CF 1895A - Treasure Chest](https://codeforces.com/problemset/problem/1895/A)

**Rating:** 800  
**Tags:** math  
**Solve time:** 1m 50s  
**Verified:** yes  

## Solution
## Problem Understanding

The number line contains three important positions. Monocarp starts at position `0`, the chest is at position `x`, and the key is at position `y`.

To open the chest, Monocarp must eventually be standing at the same position as the chest while already carrying the key. Walking costs one second per unit distance. Picking up or putting down the chest and key costs nothing.

The complication is that the chest can be carried for at most `k` seconds in total. If the key is not already on the way to the chest, Monocarp may need to move the chest closer to the key, but the carrying distance cannot exceed `k`.

The input contains up to 100 test cases, and all coordinates are at most 100. The constraints are tiny, but the real goal is finding the mathematical observation that gives the answer immediately.

A common mistake is to assume that Monocarp must always reach the key before touching the chest. That is not true because he is allowed to carry the chest.

Consider:

```
x = 5, y = 7, k = 2
```

He reaches the chest at position 5, carries it for 2 units to position 7, picks up the key, and opens the chest. The answer is 7, not 12.

Another easy mistake is to always answer `max(x, y)` when the key lies beyond the chest.

Consider:

```
x = 5, y = 8, k = 2
```

The key is 3 units beyond the chest, but Monocarp can only carry the chest for 2 units. He carries it to position 7, walks to 8 for the key, then returns to 7. The answer is 9, not 8.

A third edge case appears when the key is before the chest.

```
x = 10, y = 5, k = 0
```

Monocarp simply picks up the key on the way to the chest. The answer is 10. Any logic that tries to involve carrying the chest here is unnecessary.

## Approaches

A brute-force view is to model every possible position of Monocarp, whether he has the key, where the chest currently is, and how much carrying stamina remains. Then we could run a shortest-path search over the resulting state space.

This works because all actions have nonnegative cost and the state space is finite. With coordinates bounded by 100, such a solution could even be implemented. The problem is that it completely ignores the structure of the number line and the very simple geometry involved.

The key observation is that only two relative orderings matter.

If the key is at or before the chest (`y < x`), Monocarp reaches the key while walking toward the chest. He picks it up for free and continues to `x`. The chest never needs to move. The answer is simply `x`.

The interesting case is when the key lies beyond the chest (`y > x`).

Monocarp must first reach the chest, spending `x` seconds.

The remaining gap between chest and key is:

```
d = y - x
```

If `d <= k`, he can carry the chest all the way to the key. Total time becomes `x + d = y`.

If `d > k`, he carries the chest as far as possible, exactly `k` units. The chest stops at position `x + k`.

There is still a remaining distance:

```
r = d - k
```

Monocarp walks `r` units to the key and then `r` units back to the chest. That costs `2r` extra seconds.

The total becomes:

```
x + k + 2(d - k)
= x + 2d - k
```

Since `y = x + d`, this can also be written as:

```
y + (d - k)
```

A compact formula is:

```
x,                     if y < x
y + max(0, y - x - k), otherwise
```

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(S) | O(S) | Unnecessary |
| Optimal | O(1) per test case | O(1) | Accepted |

## Algorithm Walkthrough

1. Read `x`, `y`, and `k`.
2. If `y < x`, the key is encountered before reaching the chest. Pick up the key on the way and continue to the chest. Output `x`.
3. Otherwise compute the gap `d = y - x`.
4. If `d <= k`, the chest can be carried all the way to the key. Output `y`.
5. Otherwise the chest can only be moved `k` units. The remaining distance is `d - k`.
6. Monocarp must walk that remaining distance to get the key and then walk the same distance back to the chest. Output `y + (d - k)`.

### Why it works

When `y < x`, every valid solution must eventually reach position `x`, and the key lies on that path. Reaching the chest at `x` is already sufficient, so `x` is optimal.

When `y > x`, Monocarp must first spend `x` seconds reaching the chest. Carrying the chest toward the key is always beneficial because it reduces the future separation between them. The best strategy is to use as much carrying distance as possible, up to `k` or until the chest reaches the key. Any remaining separation must be traversed twice, once to collect the key and once to return to the chest. The formula above accounts exactly for these unavoidable movements, so no shorter route exists.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())

for _ in range(t):
    x, y, k = map(int, input().split())

    if y < x:
        print(x)
    else:
        print(y + max(0, y - x - k))
```

The first branch handles the case where the key is encountered before the chest. No carrying is required, so the answer is simply the chest position.

In the second branch, the key lies beyond the chest. The value `y - x - k` represents the portion of the chest-to-key gap that cannot be covered by carrying the chest. If this quantity is negative, the chest reaches the key directly, so the extra cost is zero. Otherwise that remaining distance contributes exactly once to the answer beyond `y`, producing the formula `y + max(0, y - x - k)`.

All calculations fit comfortably inside standard integer types, and there are no tricky boundary conditions because the formula naturally handles `k = 0` and `d = k`.

## Worked Examples

### Example 1

Input:

```
x = 5, y = 7, k = 2
```

| Variable | Value |
| --- | --- |
| x | 5 |
| y | 7 |
| k | 2 |
| d = y - x | 2 |
| d <= k | Yes |
| Answer | 7 |

Monocarp reaches the chest in 5 seconds and carries it exactly 2 units to the key. The chest and key meet at position 7, so the total time is 7.

### Example 2

Input:

```
x = 5, y = 8, k = 2
```

| Variable | Value |
| --- | --- |
| x | 5 |
| y | 8 |
| k | 2 |
| d = y - x | 3 |
| d <= k | No |
| Remaining gap | 1 |
| Answer | 8 + 1 = 9 |

Monocarp carries the chest from 5 to 7. He then walks from 7 to 8 for the key and returns from 8 to 7 to open the chest. The total time is 9.

These traces illustrate the key invariant: after using all available carrying distance, any remaining chest-key separation must be traversed twice.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) per test case | Only a few arithmetic operations |
| Space | O(1) | No extra data structures |

Even with the maximum number of test cases, the program performs only a handful of operations per case. It easily fits within the time and memory limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline
    t = int(input())
    ans = []

    for _ in range(t):
        x, y, k = map(int, input().split())

        if y < x:
            ans.append(str(x))
        else:
            ans.append(str(y + max(0, y - x - k)))

    return "\n".join(ans)

# provided sample
assert run(
"""3
5 7 2
10 5 0
5 8 2
"""
) == "7\n10\n9"

# key before chest
assert run(
"""1
8 3 5
"""
) == "8"

# exactly enough carrying distance
assert run(
"""1
4 9 5
"""
) == "9"

# no carrying allowed
assert run(
"""1
4 9 0
"""
) == "14"

# maximum coordinate values
assert run(
"""1
100 99 100
"""
) == "100"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `8 3 5` | `8` | Key lies before chest |
| `4 9 5` | `9` | Carrying distance exactly matches gap |
| `4 9 0` | `14` | No carrying available |
| `100 99 100` | `100` | Large coordinates and key before chest |

## Edge Cases

Consider:

```
1
10 5 0
```

The algorithm sees that `y < x` and immediately returns `10`. Monocarp picks up the key while walking toward the chest. No carrying is needed. The output is correct.

Consider:

```
1
5 7 2
```

Here `y > x`, and the gap is `2`. Since `2 <= k`, the algorithm returns `y = 7`. The chest can be carried directly to the key. No extra backtracking occurs.

Consider:

```
1
5 8 2
```

The gap is `3`, larger than `k`. The uncovered portion is `3 - 2 = 1`. The algorithm returns `8 + 1 = 9`. That extra unit corresponds exactly to walking from the relocated chest to the key and back.

Consider:

```
1
4 9 0
```

The gap is `5`, and no carrying is possible. The formula gives `9 + 5 = 14`. Monocarp walks to the chest in 4 seconds, then must travel from 4 to 9 and back to 4, adding 10 more seconds. The total is 14, matching the formula exactly.

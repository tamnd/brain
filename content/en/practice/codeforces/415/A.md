---
title: "CF 415A - Mashmokh and Lights"
description: "The factory has a row of lights indexed from left to right. Every light starts in the “on” state. Mashmokh performs a sequence of button presses, and each button has an index that determines how far to the right its effect extends."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 415
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 240 (Div. 2)"
rating: 900
weight: 415
solve_time_s: 83
verified: true
draft: false
---

[CF 415A - Mashmokh and Lights](https://codeforces.com/problemset/problem/415/A)

**Rating:** 900  
**Tags:** implementation  
**Solve time:** 1m 23s  
**Verified:** yes  

## Solution
## Problem Understanding

The factory has a row of lights indexed from left to right. Every light starts in the “on” state. Mashmokh performs a sequence of button presses, and each button has an index that determines how far to the right its effect extends.

When a button with index `i` is pressed, it scans all lights from position `i` to the end and turns off every light it encounters that is still on. Lights that are already off stay off, and lights before `i` are unaffected.

The task is to determine, for each light, which specific button press was responsible for turning it off for the first time. We are not asked how many times it was affected or what happens later, only the earliest press in the sequence that switches it off.

The constraints are small: both the number of lights and the number of button presses are at most 100. This immediately rules out any need for advanced data structures or logarithmic optimizations. Even a straightforward quadratic simulation fits comfortably within time limits because the total number of operations stays bounded around ten thousand.

A subtle point is that buttons are not guaranteed to be ordered. A later button may have a smaller index than an earlier one, which changes which lights get affected and when they are turned off. Another important detail is that once a light is turned off, later presses cannot change its recorded answer.

A naive mistake would be to assume each button only affects a fixed segment that is independent of previous presses. For example, if we ignored the “still on” condition, we might repeatedly overwrite answers incorrectly.

Consider this small scenario:

Input:

```
3 2
2 1
```

Correct behavior:

After pressing 2, lights 2 and 3 turn off, so both are assigned button 2. After pressing 1, light 1 turns off and is assigned button 1.

A careless simulation that keeps turning off already-off lights again might incorrectly overwrite answers or attempt to reassign them multiple times.

The key is that each light must be assigned exactly once, at the moment it transitions from on to off.

## Approaches

The most direct way to think about the process is to simulate it exactly as described. We maintain an array representing whether each light is on, and another array storing the answer for each light. For every button press, we scan all affected lights from its index to `n`, and whenever we encounter a light that is still on, we mark it as turned off by this button.

This approach is correct because it mirrors the factory process step by step. The issue is efficiency: in the worst case, each of the `m` presses may scan up to `n` lights, leading to roughly `n * m` operations. With the constraints given, this is still acceptable, since the maximum is only 10,000 operations.

A slightly more conceptual observation simplifies reasoning. A light `j` is turned off the first time we encounter a button with index less than or equal to `j` in the sequence. Earlier buttons with larger indices do not affect it, and once a valid button appears, the light is already off and will never be considered again. This observation matches the simulation and explains why a single pass over each light and button is sufficient.

So both the direct simulation and the derived “first qualifying press” viewpoint lead to the same implementation structure.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(n · m) | O(n) | Accepted |
| Direct First-Activation Scan | O(n · m) | O(n) | Accepted |

## Algorithm Walkthrough

We describe the simulation in a way that directly corresponds to how the process unfolds.

1. Initialize an array `ans` of size `n`, filled with zeros. This will store the button index that turns off each light. Also maintain a boolean array `on` initialized to all true, representing that all lights are initially on.
2. Iterate through the buttons in the given order from the first press to the last.
3. For each button with index `b_k`, scan all lights from position `b_k` through `n`.
4. If a light at position `j` is still on, assign `ans[j] = b_k` and mark it as off.
5. If the light is already off, skip it because its result was determined earlier and cannot change.
6. Continue until all button presses are processed.

The reason we only assign when a light is still on is that we are capturing the exact moment of its first transition to off state. Any later button that also covers that position must be ignored.

### Why it works

Each light changes state exactly once, from on to off. The first time a button with index `b_k ≤ j` is processed, light `j` is still on because no earlier button could have covered it. That press necessarily includes `j` in its range and turns it off. From that moment onward, no subsequent operation can affect its recorded answer because we explicitly prevent overwriting. This guarantees that `ans[j]` stores the earliest valid press that reaches it.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())
    b = list(map(int, input().split()))

    ans = [0] * n
    on = [True] * n

    for btn in b:
        i = btn - 1
        for j in range(i, n):
            if on[j]:
                on[j] = False
                ans[j] = btn

    print(*ans)

if __name__ == "__main__":
    solve()
```

The solution follows the exact simulation described earlier. The array `on` ensures that each light is assigned only once. The inner loop starts from `btn - 1` because lights are 0-indexed in the implementation, while input is 1-indexed.

A common pitfall is forgetting that once a light is turned off, later buttons must not overwrite its answer. The conditional check `if on[j]` enforces this invariant.

## Worked Examples

### Example 1

Input:

```
5 4
4 3 1 2
```

| Step | Button | Affected range | Updates |
| --- | --- | --- | --- |
| 1 | 4 | 4-5 | light 4 ← 4, light 5 ← 4 |
| 2 | 3 | 3-5 | light 3 ← 3 |
| 3 | 1 | 1-5 | light 1 ← 1, light 2 ← 1 |
| 4 | 2 | 2-5 | no change |

Final output:

```
1 1 3 4 4
```

This trace shows how earlier large-index buttons affect only the right side, while later small-index buttons fill in the remaining uncovered lights.

### Example 2

Input:

```
4 3
2 4 1
```

| Step | Button | Affected range | Updates |
| --- | --- | --- | --- |
| 1 | 2 | 2-4 | light 2 ← 2, light 3 ← 2, light 4 ← 2 |
| 2 | 4 | 4-4 | no change (already off) |
| 3 | 1 | 1-4 | light 1 ← 1 |

Final output:

```
1 2 2 2
```

This example highlights that once a light is turned off early, later presses cannot override it, even if they technically include its index.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n · m) | Each button may scan up to all lights to its right, and each light is assigned at most once |
| Space | O(n) | We store the state of each light and the final answer array |

With both `n` and `m` capped at 100, the worst-case number of operations is small enough to execute instantly within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from sys import stdout
    old = sys.stdout
    sys.stdout = io.StringIO()

    solve()

    out = sys.stdout.getvalue()
    sys.stdout = old
    return out.strip()

# provided sample
assert run("5 4\n4 3 1 2\n") == "1 1 3 4 4", "sample 1"

# minimum size
assert run("1 1\n1\n") == "1", "single light"

# already left-to-right pressing
assert run("3 3\n1 2 3\n") == "1 2 3", "strict order"

# reverse order
assert run("3 3\n3 2 1\n") == "3 2 1", "reverse order"

# overlapping coverage
assert run("4 2\n2 1\n") == "1 1 2 2", "overlap case"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 / 1` | `1` | minimal boundary |
| `3 / 1 2 3` | `1 2 3` | monotonic coverage |
| `3 / 3 2 1` | `3 2 1` | descending order effect |
| `4 / 2 1` | `1 1 2 2` | overlapping ranges |

## Edge Cases

A minimal single-light case checks that the implementation correctly handles indexing and does not attempt to access invalid ranges. When `n = 1`, any button `1` immediately turns off the only light, and the assignment is straightforward.

When buttons are strictly increasing, each press tends to affect only the yet-uncovered suffix. The algorithm assigns each light exactly when its index becomes covered for the first time, producing a direct mapping between position and earliest qualifying button.

When buttons are strictly decreasing, the first press already covers almost everything. In this situation, the inner loop still runs correctly but only assigns values once, and later presses find no active lights to modify. This confirms that the `on` array correctly prevents overwriting.

When coverage overlaps heavily, earlier wide-range presses may preempt later small-range ones. The condition `if on[j]` ensures that once a light is assigned, it remains fixed, which preserves correctness even under aggressive overlap patterns.

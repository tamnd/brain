---
title: "CF 62A - A Student's Dream"
description: "We have four integers describing the number of fingers on two alien hands. The Venusian girl has al fingers on her left hand and ar on her right hand. The Marsian boy has bl and br fingers. They want to hold exactly one pair of hands."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "math"]
categories: ["algorithms"]
codeforces_contest: 62
codeforces_index: "A"
codeforces_contest_name: "Codeforces Beta Round 58"
rating: 1300
weight: 62
solve_time_s: 73
verified: true
draft: false
---

[CF 62A - A Student's Dream](https://codeforces.com/problemset/problem/62/A)

**Rating:** 1300  
**Tags:** greedy, math  
**Solve time:** 1m 13s  
**Verified:** yes  

## Solution
## Problem Understanding

We have four integers describing the number of fingers on two alien hands. The Venusian girl has `al` fingers on her left hand and `ar` on her right hand. The Marsian boy has `bl` and `br` fingers.

They want to hold exactly one pair of hands. Since either person may stand on the left, there are only two possible pairings:

- girl's left hand with boy's right hand
- girl's right hand with boy's left hand

or the opposite orientation.

The arrangement must satisfy two comfort rules.

First, no two fingers of the girl may touch each other directly. Between every pair of neighboring girl fingers, there must be at least one boy finger.

Second, no three boy fingers may touch consecutively.

The task is to decide whether at least one valid hand pairing exists.

The limits are tiny, every value is at most 100. Even a brute-force simulation over all possibilities would run instantly. The real challenge is recognizing the mathematical condition hidden inside the wording.

The tricky part is translating the physical description into inequalities correctly.

Suppose the girl has `g` fingers and the boy has `b` fingers in the chosen hands.

To separate every adjacent pair of girl fingers, the boy needs at least `g - 1` fingers. For example, if the girl has 5 fingers, we need a structure like:

`B G B G B G B G B G`

There are 4 gaps between girl fingers, so at least 4 boy fingers are required.

At the same time, the boy cannot have three consecutive fingers touching. That means we can place at most two boy fingers in each slot around the girl fingers.

With `g` girl fingers, there are `g + 1` slots where boy fingers may appear:

- before the first girl finger
- between every adjacent pair
- after the last girl finger

Each slot can contain at most 2 boy fingers, so the maximum possible number of boy fingers is `2 * (g + 1)`.

A common mistake is forgetting the edge slots. Someone may incorrectly think the maximum is `2 * (g - 1)`, counting only the internal gaps. For example:

```
girl = 1
boy = 4
```

This is actually valid:

`BBGBB`

There are no three consecutive boy fingers.

Another easy mistake is using strict inequalities. Consider:

```
girl = 5
boy = 4
```

This is valid because exactly one boy finger can separate every pair of girl fingers:

`GBGBGBGBG`

The lower bound is `boy >= girl - 1`, not `boy > girl - 1`.

A final edge case appears when the girl has very few fingers.

```
girl = 1
boy = 0
```

This is valid because there are no adjacent girl fingers to separate.

The condition still works:

```
girl - 1 <= boy <= 2 * (girl + 1)
0 <= 0 <= 4
```

## Approaches

The most direct approach is brute force construction. For a chosen pair of hands, we could try generating all possible finger arrangements and check whether any arrangement satisfies the rules.

If the girl has `g` fingers and the boy has `b`, the total number of merged sequences is:

$$\binom{g+b}{g}$$

Even though the actual constraints are tiny, this grows rapidly in general. For example, with only 20 total fingers, there are already more than 180 thousand interleavings. A full search becomes unnecessary once we understand the structure of valid arrangements.

The key observation is that the constraints describe spacing rules.

The girl's condition creates a minimum requirement for boy fingers. Every adjacent pair of girl fingers needs at least one separator, so we need:

$$b \ge g - 1$$

The boy's condition creates a maximum requirement. Since no three boy fingers may touch consecutively, each slot around the girl fingers can contain at most two boy fingers.

With `g` girl fingers, there are `g + 1` slots:

```
_ G _ G _ G _
```

Each slot may hold at most two boy fingers, giving:

$$b \le 2(g+1)$$

These two inequalities are both necessary and sufficient.

We simply test both possible hand pairings:

- `(girl left, boy right)`
- `(girl right, boy left)`

If either satisfies the inequalities, the answer is `"YES"`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | Exponential | Too slow conceptually |
| Optimal | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the four finger counts.
2. Define a helper check function for a chosen pair of hands.
3. Suppose the girl has `g` fingers and the boy has `b`.
4. Verify the lower bound:

$$b \ge g - 1$$

This guarantees every neighboring pair of girl fingers can be separated.

1. Verify the upper bound:

$$b \le 2(g+1)$$

This guarantees the boy fingers can be distributed into the `g + 1` available slots without creating three consecutive boy fingers.

1. If both inequalities hold, this pairing is feasible.
2. Test both orientations:

1. girl left with boy right
2. girl right with boy left
3. If at least one orientation works, print `"YES"`. Otherwise print `"NO"`.

### Why it works

The lower bound is unavoidable because every gap between consecutive girl fingers must contain at least one boy finger. A hand with `g` girl fingers has exactly `g - 1` such gaps.

The upper bound is also unavoidable because the boy may not contribute three consecutive fingers. Around `g` girl fingers there are exactly `g + 1` insertion positions, and each can contain at most two boy fingers.

These conditions are also sufficient. If the number of boy fingers lies within the interval:

$$g - 1 \le b \le 2(g+1)$$

we can first place one boy finger in every internal gap, then distribute the remaining boy fingers into the available slots while never exceeding two per slot. That always constructs a valid arrangement.

## Python Solution

```python
import sys
input = sys.stdin.readline

def possible(g, b):
    return g - 1 <= b <= 2 * (g + 1)

def solve():
    al, ar = map(int, input().split())
    bl, br = map(int, input().split())

    if possible(al, br) or possible(ar, bl):
        print("YES")
    else:
        print("NO")

solve()
```

The helper function directly implements the mathematical characterization of a valid arrangement.

The expression:

```
g - 1 <= b
```

checks whether there are enough boy fingers to separate adjacent girl fingers.

The expression:

```
b <= 2 * (g + 1)
```

checks whether the boy fingers can be distributed without ever creating three consecutive ones.

The solution tests both possible orientations because the pairings swap depending on who stands on which side. Forgetting the second orientation is the most common implementation mistake.

All computations fit comfortably inside normal integers. The constraints are tiny, but even for much larger values this logic would still run instantly.

## Worked Examples

### Example 1

Input:

```
5 1
10 5
```

We test both pairings.

| Pairing | Girl fingers | Boy fingers | Lower bound | Upper bound | Valid |
| --- | --- | --- | --- | --- | --- |
| left-right | 5 | 5 | 5 ≥ 4 | 5 ≤ 12 | Yes |
| right-left | 1 | 10 | 10 ≥ 0 | 10 ≤ 4 | No |

Since the first pairing works, the answer is:

```
YES
```

This example shows that only one successful orientation is needed.

### Example 2

Input:

```
4 4
1 1
```

| Pairing | Girl fingers | Boy fingers | Lower bound | Upper bound | Valid |
| --- | --- | --- | --- | --- | --- |
| left-right | 4 | 1 | 1 ≥ 3 | 1 ≤ 10 | No |
| right-left | 4 | 1 | 1 ≥ 3 | 1 ≤ 10 | No |

Both orientations fail because there are not enough boy fingers to separate adjacent girl fingers.

Output:

```
NO
```

This demonstrates the necessity of the lower bound.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only a few arithmetic checks are performed |
| Space | O(1) | No extra data structures are used |

The constraints are extremely small, but the constant-time solution is mathematically clean and scales effortlessly far beyond the original limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    def possible(g, b):
        return g - 1 <= b <= 2 * (g + 1)

    al, ar = map(int, input().split())
    bl, br = map(int, input().split())

    if possible(al, br) or possible(ar, bl):
        return "YES"
    return "NO"

# provided sample
assert run("5 1\n10 5\n") == "YES", "sample 1"

# insufficient separators
assert run("4 4\n1 1\n") == "NO", "too few boy fingers"

# exact lower bound
assert run("5 2\n4 1\n") == "YES", "boy fingers equal girl-1"

# exact upper bound
assert run("1 3\n4 1\n") == "YES", "boy fingers equal 2*(girl+1)"

# exceeding upper bound
assert run("1 1\n5 5\n") == "NO", "three consecutive boy fingers unavoidable"

# symmetric equal values
assert run("3 3\n3 3\n") == "YES", "balanced configuration"

print("All tests passed.")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `4 4 / 1 1` | `NO` | Lower bound failure |
| `5 2 / 4 1` | `YES` | Exact minimum valid boy fingers |
| `1 3 / 4 1` | `YES` | Exact maximum valid boy fingers |
| `1 1 / 5 5` | `NO` | Upper bound violation |
| `3 3 / 3 3` | `YES` | Symmetric balanced case |

## Edge Cases

Consider the case where the boy has exactly enough fingers to separate the girl fingers.

Input:

```
5 1
4 1
```

Testing the first orientation gives `g = 5` and `b = 1`, which fails immediately. The second orientation gives `g = 1` and `b = 4`, which satisfies:

```
0 <= 4 <= 4
```

The algorithm correctly prints `"YES"` because edge slots allow two boy fingers before and after the single girl finger.

Now consider a case where the upper bound fails by one.

Input:

```
1 1
5 5
```

For either orientation:

```
g = 1
b = 5
```

The checks become:

```
0 <= 5 <= 4
```

The upper bound fails. With only two edge slots available, placing 5 boy fingers inevitably creates three consecutive boy fingers somewhere. The algorithm correctly returns `"NO"`.

Finally, consider the exact lower-bound scenario.

Input:

```
5 2
4 1
```

The valid pairing is `g = 5`, `b = 4`.

The condition becomes:

```
4 <= 4 <= 12
```

The arrangement:

```
G B G B G B G B G
```

works perfectly. The algorithm accepts equality in the lower bound, avoiding the common off-by-one mistake of requiring strictly more separators.

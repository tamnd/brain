---
title: "CF 174A - Problem About Equation"
description: "We have several mugs that already contain different amounts of Ber-Cola. There is also some drink left in the bottle. We must pour the entire remaining amount into the mugs so that every mug ends up with exactly the same volume. If the initial amounts are a1, a2, ..."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "math"]
categories: ["algorithms"]
codeforces_contest: 174
codeforces_index: "A"
codeforces_contest_name: "VK Cup 2012 Round 3 (Unofficial Div. 2 Edition)"
rating: 1100
weight: 174
solve_time_s: 93
verified: true
draft: false
---

[CF 174A - Problem About Equation](https://codeforces.com/problemset/problem/174/A)

**Rating:** 1100  
**Tags:** math  
**Solve time:** 1m 33s  
**Verified:** yes  

## Solution
## Problem Understanding

We have several mugs that already contain different amounts of Ber-Cola. There is also some drink left in the bottle. We must pour the entire remaining amount into the mugs so that every mug ends up with exactly the same volume.

If the initial amounts are `a1, a2, ..., an` and the bottle contains `b`, we need to determine how much additional drink goes into each mug. The added amounts must satisfy two conditions simultaneously. First, the total added amount must equal `b`. Second, after pouring, all mugs must contain the same final volume.

The constraints are extremely small. There are at most 100 mugs and every value is at most 100. Even a quadratic or cubic algorithm would easily fit within the limits. The challenge is not performance, it is recognizing the mathematical condition that determines whether a solution exists.

The key observation is that every mug must end at some common value `x`. For mug `i`, the amount added is:

$$c_i = x - a_i$$

The total added amount must equal `b`, so:

$$\sum (x - a_i) = b$$

Expanding this gives:

$$n \cdot x - \sum a_i = b$$

which immediately determines the only possible final value:

$$x = \frac{\sum a_i + b}{n}$$

Once `x` is known, every `c_i` is fixed.

The dangerous edge case is when some mug already contains more than the target value. In that situation, the corresponding `c_i` becomes negative, which is impossible because we are only allowed to pour drink into mugs, not remove it.

Consider this example:

```
2 1
5 1
```

The total amount after pouring would be `7`, so the target becomes `3.5`. The first mug already contains `5`, which is larger than `3.5`. Reaching equal volumes would require removing `1.5` from that mug. The correct output is:

```
-1
```

A careless implementation might compute the formula mechanically and print negative values.

Another subtle case happens when all mugs are already equal.

```
3 6
2 2 2
```

The target becomes `4`, so every mug simply receives `2`. The output is:

```
2.000000
2.000000
2.000000
```

An implementation that incorrectly assumes unequal starting values could mishandle this situation.

A third edge case is when the target becomes fractional.

```
2 1
1 1
```

The final amount in each mug is `1.5`, so each mug receives `0.5`. Floating point output is required here.

## Approaches

A brute-force mindset would start by guessing the final common amount `x`. For every candidate `x`, we could compute how much each mug needs and check whether the total added amount equals `b`.

Since all values are small, we might even try many possible real values with some precision. The approach is logically correct because any valid solution must correspond to some common final volume. The problem is that searching over real numbers is awkward and unnecessary. Even discretizing the search introduces precision concerns and pointless extra work.

The structure of the equations gives something much stronger. Every mug must end at the same value, which means all added amounts are directly tied to one variable `x`. Summing the equations collapses the entire system into a single formula:

$$x = \frac{\sum a_i + b}{n}$$

There is no need to search. The target value is uniquely determined by conservation of total liquid.

Once we know `x`, each answer is simply:

$$c_i = x - a_i$$

The only remaining validity check is whether any `c_i` is negative. If even one is negative, the configuration is impossible.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Undefined for real-valued search | O(1) | Impractical |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read `n`, `b`, and the array of mug volumes.
2. Compute the total amount of liquid that will exist after pouring:

$$total = \sum a_i + b$$
3. Compute the final equal volume for every mug:

$$x = \frac{total}{n}$$

This value is forced by the conservation of liquid. No other target can satisfy the conditions.
4. For every mug, compute:

$$c_i = x - a_i$$

This is exactly how much must be added to reach the common final value.
5. If any `c_i` is negative, print `-1` and stop.

A negative value means the mug already contains more than the target amount, so equalization would require removing liquid.
6. Otherwise, print every `c_i` with at least six digits after the decimal point.

### Why it works

The algorithm relies on a conservation law. The total amount of liquid after pouring is fixed, so if all mugs end with the same amount `x`, then the total liquid must equal `n * x`. That uniquely determines `x`.

For each mug, the only possible added amount is `x - a_i`. No alternative assignment can exist because changing one mug's added amount would change its final volume away from `x`.

If every computed value is non-negative, then all mugs can indeed be increased to exactly `x`, and the total added amount automatically equals `b` because of how `x` was derived. If any value is negative, no valid solution exists because pouring cannot decrease liquid.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, b = map(int, input().split())
    a = list(map(int, input().split()))

    target = (sum(a) + b) / n

    ans = []

    for value in a:
        add = target - value

        if add < 0:
            print(-1)
            return

        ans.append(add)

    for x in ans:
        print(f"{x:.6f}")

solve()
```

The first part reads the input and computes the target final volume. This value is derived directly from the total amount of liquid available after the bottle is emptied.

The loop computes how much must be added to each mug. The condition `add < 0` is the entire feasibility test. If a mug already exceeds the target level, we cannot repair the situation because the operation only allows adding liquid.

The answers are stored and printed afterward. Printing with `:.6f` guarantees at least six digits after the decimal point, which satisfies the output requirements.

One subtle detail is using floating point division when computing the target. Using integer division would truncate fractional answers and produce incorrect results for cases like `2 1` with mugs `1 1`.

## Worked Examples

### Example 1

Input:

```
5 50
1 2 3 4 5
```

The total liquid after pouring is:

$$1 + 2 + 3 + 4 + 5 + 50 = 65$$

The target amount per mug is:

$$65 / 5 = 13$$

| Mug | Initial | Target | Added |
| --- | --- | --- | --- |
| 1 | 1 | 13 | 12 |
| 2 | 2 | 13 | 11 |
| 3 | 3 | 13 | 10 |
| 4 | 4 | 13 | 9 |
| 5 | 5 | 13 | 8 |

Output:

```
12.000000
11.000000
10.000000
9.000000
8.000000
```

This trace demonstrates that the added amounts automatically sum to exactly `50`, matching the bottle volume.

### Example 2

Input:

```
2 1
5 1
```

The total liquid after pouring is:

$$5 + 1 + 1 = 7$$

The target amount per mug is:

$$7 / 2 = 3.5$$

| Mug | Initial | Target | Added |
| --- | --- | --- | --- |
| 1 | 5 | 3.5 | -1.5 |
| 2 | 1 | 3.5 | 2.5 |

The first mug requires a negative added amount, which is impossible.

Output:

```
-1
```

This example confirms that feasibility depends entirely on whether all computed additions are non-negative.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | We scan the array once to compute the sum and once to build the answer |
| Space | O(1) | Aside from the output list, only a few variables are used |

With at most 100 mugs, the solution runs instantly. The memory usage is negligible compared to the 256 MB limit.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def solve():
    input = sys.stdin.readline

    n, b = map(int, input().split())
    a = list(map(int, input().split()))

    target = (sum(a) + b) / n

    ans = []

    for value in a:
        add = target - value

        if add < 0:
            print(-1)
            return

        ans.append(add)

    for x in ans:
        print(f"{x:.6f}")

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    out = io.StringIO()
    backup = sys.stdout
    sys.stdout = out

    solve()

    sys.stdout = backup
    return out.getvalue()

# provided sample
assert run(
    "5 50\n1 2 3 4 5\n"
) == (
    "12.000000\n"
    "11.000000\n"
    "10.000000\n"
    "9.000000\n"
    "8.000000\n"
), "sample 1"

# minimum size with fractional answer
assert run(
    "2 1\n1 1\n"
) == (
    "0.500000\n"
    "0.500000\n"
), "fractional target"

# impossible case
assert run(
    "2 1\n5 1\n"
) == "-1\n", "negative addition required"

# all equal initially
assert run(
    "3 6\n2 2 2\n"
) == (
    "2.000000\n"
    "2.000000\n"
    "2.000000\n"
), "all equal"

# boundary-style large values
assert run(
    "2 100\n0 100\n"
) == (
    "100.000000\n"
    "0.000000\n"
), "one mug already at target"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2 1 / 1 1` | `0.500000 0.500000` | Fractional targets |
| `2 1 / 5 1` | `-1` | Impossible configuration |
| `3 6 / 2 2 2` | Equal additions | Already balanced mugs |
| `2 100 / 0 100` | `100` and `0` | Boundary where one addition is exactly zero |

## Edge Cases

Consider the impossible configuration:

```
2 1
5 1
```

The algorithm computes:

$$target = (5 + 1 + 1) / 2 = 3.5$$

For the first mug:

$$3.5 - 5 = -1.5$$

The negative result immediately triggers `-1`. This is correct because equalization would require removing liquid from the first mug.

Now consider a fractional target:

```
2 1
1 1
```

The target becomes:

$$(1 + 1 + 1) / 2 = 1.5$$

Both mugs receive `0.5`. The algorithm uses floating point division, so no precision is lost through integer truncation.

Finally, consider a case where one mug already matches the target:

```
2 100
0 100
```

The target becomes:

$$(0 + 100 + 100) / 2 = 100$$

The additions are:

$$100 - 0 = 100$$

and

$$100 - 100 = 0$$

Zero is allowed because we are not required to pour into every mug, only to distribute the entire bottle while ending with equal volumes.

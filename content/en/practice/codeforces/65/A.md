---
title: "CF 65A - Harry Potter and Three Spells"
description: "We have three transformation spells that convert one material into another. The first spell turns a grams of sand into b grams of lead. The second spell turns c grams of lead into d grams of gold. The third spell turns e grams of gold into f grams of sand."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "implementation", "math"]
categories: ["algorithms"]
codeforces_contest: 65
codeforces_index: "A"
codeforces_contest_name: "Codeforces Beta Round 60"
rating: 1800
weight: 65
solve_time_s: 122
verified: true
draft: false
---

[CF 65A - Harry Potter and Three Spells](https://codeforces.com/problemset/problem/65/A)

**Rating:** 1800  
**Tags:** implementation, math  
**Solve time:** 2m 2s  
**Verified:** yes  

## Solution
## Problem Understanding

We have three transformation spells that convert one material into another.

The first spell turns `a` grams of sand into `b` grams of lead.

The second spell turns `c` grams of lead into `d` grams of gold.

The third spell turns `e` grams of gold into `f` grams of sand.

We may apply these spells any number of times, in any order, as long as we currently own enough material for the spell we want to cast. The question is whether there exists some finite starting amount of sand such that we can eventually produce arbitrarily large amounts of gold.

The key phrase is “greater than any preassigned number”. We are not asked for a specific maximum amount. We must determine whether gold production can grow without bound.

The constraints are tiny. Every number is between `0` and `1000`. That means we are free to use direct mathematical reasoning without worrying about performance. Even brute-force state exploration over moderate ranges would fit inside the time limit. The real challenge is not efficiency, but correctly handling all degenerate situations involving zeros.

The dangerous cases all come from spells that create matter “from nothing”.

Consider this input:

```
1 1 0 1 1 1
```

The second spell converts `0` lead into `1` gold. We can cast it infinitely many times immediately. The answer is `"Ron"`.

A careless implementation that only checks the full cycle multiplication ratio would miss this.

Another subtle case:

```
1 1 1 1 0 1
```

The third spell converts `0` gold into `1` sand. Starting from zero sand, we can generate infinite sand for free, then use the first and second spells to create infinite gold. The answer is `"Ron"`.

A solution that assumes we always need positive initial resources would fail here.

There are also cases where every spell preserves or destroys matter:

```
100 50 100 50 100 50
```

Every transformation loses half the material. Repeating the cycle only shrinks resources, so the answer is `"Hermione"`.

Another edge case:

```
0 0 0 0 0 0
```

All spells do nothing. Infinite gold is impossible.

The hardest part of the problem is correctly distinguishing between genuine amplification and harmless cycles.

## Approaches

A natural brute-force idea is to simulate reachable states. We could start from some bounded amount of sand and repeatedly apply all possible spells, marking every reachable triple `(sand, lead, gold)`.

This works conceptually because the system is deterministic and the state transitions are simple. If infinite growth exists, we would expect resource values to keep increasing.

The problem is that there is no obvious upper bound for the state space. If the answer is `"Ron"`, quantities can grow forever. Even if we cap all resources at some limit like `10^6`, we still cannot prove correctness. A profitable cycle might require temporarily accumulating a large amount before becoming sustainable.

The structure of the spells gives a much cleaner route.

Observe that the materials form a directed cycle:

```
sand -> lead -> gold -> sand
```

If we start with some amount of sand and go through the whole cycle once, the total sand changes by a multiplicative factor:

```
(b / a) * (d / c) * (f / e)
```

If this factor is greater than `1`, then one complete cycle increases sand. Repeating the cycle grows resources exponentially, and we can extract unlimited gold.

Rearranging avoids fractions:

```
b * d * f > a * c * e
```

That handles the ordinary case where all denominators are positive.

The remaining challenge is zero handling. A spell with zero input can create matter from nothing. Such spells completely bypass the multiplicative argument.

For example, if `c = 0` and `d > 0`, the second spell creates gold for free. Infinite gold becomes immediate.

Similarly, if `e = 0` and `f > 0`, we can generate infinite sand from nothing. If the first two spells can eventually turn sand into gold, infinite gold follows.

The entire solution becomes a small collection of logical checks.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Unbounded / impractical | Unbounded | Too slow |
| Optimal | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Check whether the second spell creates gold from nothing.

If `c == 0` and `d > 0`, then every cast produces gold without consuming lead. We can cast it infinitely many times immediately, so the answer is `"Ron"`.
2. Check whether the third spell creates sand from nothing.

If `e == 0` and `f > 0`, then we can generate unlimited sand for free. To turn that sand into gold, we also need the first spell to actually produce lead and the second spell to actually produce gold.

Concretely, we need:

`a > 0`, `b > 0`, `c > 0`, and `d > 0`.

If all hold, the answer is `"Ron"`.
3. Handle impossible cycles involving zero denominators.

If any denominator among `a`, `c`, or `e` is zero, the multiplicative cycle formula becomes invalid.

At this point, all free-production cases were already handled. Any remaining zero denominator cannot generate infinite gold, so the answer is `"Hermione"`.
4. Compare the full-cycle amplification ratio.

Compute whether:

```
b * d * f > a * c * e
```

If true, one full cycle strictly increases sand. Repeating the cycle infinitely many times gives unbounded resources and thus unbounded gold.
5. Otherwise, output `"Hermione"`.

### Why it works

The system only contains one resource cycle:

```
sand -> lead -> gold -> sand
```

Any sustainable infinite-growth strategy must repeatedly traverse this cycle. The net effect of one traversal is multiplying sand by:

```
(b/a) * (d/c) * (f/e)
```

If this product exceeds `1`, repeated cycling grows resources without bound. If it is at most `1`, every complete cycle preserves or decreases total usable material, so no infinite growth is possible.

The only exception is when a spell consumes zero input. In that situation, matter can appear from nothing, and we must explicitly handle those cases separately.

## Python Solution

```python
import sys
input = sys.stdin.readline

a, b, c, d, e, f = map(int, input().split())

# Free gold
if c == 0 and d > 0:
    print("Ron")
    sys.exit()

# Free sand
if e == 0 and f > 0:
    if a > 0 and b > 0 and c > 0 and d > 0:
        print("Ron")
    else:
        print("Hermione")
    sys.exit()

# Invalid cycle denominators
if a == 0 or c == 0 or e == 0:
    print("Hermione")
    sys.exit()

# Profitable cycle
if b * d * f > a * c * e:
    print("Ron")
else:
    print("Hermione")
```

The first two checks isolate the dangerous zero-input spells. These are special because they break the usual conservation-style reasoning. A spell that consumes zero material can be repeated forever.

The second condition needs extra care. Free sand alone is not enough. We must still be able to transform sand into gold using the first two spells. That is why the code verifies positive inputs and outputs for those transformations.

The denominator check prevents division-by-zero logic errors. Once all free-production cases are removed, any remaining zero denominator means the cycle cannot function profitably.

The final comparison uses integer arithmetic only. Multiplying both sides avoids floating-point precision issues entirely.

Python integers automatically handle large products safely, although here the maximum value is only:

```
1000 * 1000 * 1000 = 10^9
```

which already fits comfortably in standard integer ranges.

## Worked Examples

### Example 1

Input:

```
100 200 250 150 200 250
```

| Step | Condition | Result |
| --- | --- | --- |
| Free gold check | `c == 0` → `250 == 0` | False |
| Free sand check | `e == 0` → `200 == 0` | False |
| Denominator check | all positive | Continue |
| Profitability | `200 * 150 * 250 = 7,500,000` |  |
| Compare | `100 * 250 * 200 = 5,000,000` |  |
| Final | `7,500,000 > 5,000,000` | `"Ron"` |

The cycle increases resources by a factor greater than `1`. Every repetition leaves extra material behind, so gold production can continue forever.

### Example 2

Input:

```
100 50 100 50 100 50
```

| Step | Condition | Result |
| --- | --- | --- |
| Free gold check | `c == 0` | False |
| Free sand check | `e == 0` | False |
| Denominator check | all positive | Continue |
| Profitability | `50 * 50 * 50 = 125000` |  |
| Compare | `100 * 100 * 100 = 1000000` |  |
| Final | `125000 > 1000000` | False |

Each full cycle loses material. Repeating transformations only shrinks the available resources, so infinite gold is impossible.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only a fixed number of arithmetic operations and comparisons |
| Space | O(1) | No additional data structures are used |

The constraints are extremely small, so this solution runs instantly. The algorithm performs only a handful of integer checks and multiplications.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def solve():
    input = sys.stdin.readline

    a, b, c, d, e, f = map(int, input().split())

    if c == 0 and d > 0:
        print("Ron")
        return

    if e == 0 and f > 0:
        if a > 0 and b > 0 and c > 0 and d > 0:
            print("Ron")
        else:
            print("Hermione")
        return

    if a == 0 or c == 0 or e == 0:
        print("Hermione")
        return

    if b * d * f > a * c * e:
        print("Ron")
    else:
        print("Hermione")

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out
    solve()
    sys.stdout = sys.__stdout__
    return out.getvalue().strip()

# provided sample
assert run("100 200 250 150 200 250\n") == "Ron", "sample 1"

# all zero
assert run("0 0 0 0 0 0\n") == "Hermione", "all zero"

# free gold
assert run("1 1 0 1 5 5\n") == "Ron", "free gold creation"

# free sand but impossible conversion
assert run("0 0 1 1 0 10\n") == "Hermione", "cannot convert sand"

# profitable cycle
assert run("1 2 1 2 1 2\n") == "Ron", "growth factor > 1"

# non-profitable cycle
assert run("2 1 2 1 2 1\n") == "Hermione", "growth factor < 1"

# equality case
assert run("1 1 1 1 1 1\n") == "Hermione", "exact conservation"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `0 0 0 0 0 0` | `Hermione` | Completely inactive system |
| `1 1 0 1 5 5` | `Ron` | Free gold generation |
| `0 0 1 1 0 10` | `Hermione` | Free sand alone is insufficient |
| `1 2 1 2 1 2` | `Ron` | Profitable multiplicative cycle |
| `2 1 2 1 2 1` | `Hermione` | Resource loss each cycle |
| `1 1 1 1 1 1` | `Hermione` | Exact conservation does not allow infinite growth |

## Edge Cases

Consider the free-gold case:

```
1 1 0 5 1 1
```

The algorithm first checks:

```
c == 0 and d > 0
```

which becomes:

```
0 == 0 and 5 > 0
```

This is true, so the answer is immediately `"Ron"`.

That is correct because the second spell creates `5` grams of gold without consuming any lead. We can cast it infinitely many times.

Now consider free sand without usable conversion:

```
0 0 1 1 0 10
```

The third spell creates sand for free, but the first spell cannot convert sand into lead because both `a` and `b` are zero.

The algorithm enters the free-sand branch:

```
e == 0 and f > 0
```

Then it checks whether the first two spells form a valid pipeline into gold:

```
a > 0 and b > 0 and c > 0 and d > 0
```

This fails, so the answer becomes `"Hermione"`.

Finally, consider exact conservation:

```
1 1 1 1 1 1
```

The multiplicative comparison becomes:

```
1 * 1 * 1 > 1 * 1 * 1
```

which is false.

Every cycle returns exactly the same amount of sand. Resources never grow, so gold cannot become arbitrarily large. The algorithm correctly prints `"Hermione"`.

---
title: "CF 1114A - Got Any Grapes?"
description: "We have three people with different grape preferences and three piles of grapes. Andrew wants exactly the first type of grape, green grapes. If he needs x grapes, all of them must come from the green pile. Dmitry dislikes black grapes. He can eat green or purple grapes."
date: "2026-06-12T04:55:35+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "greedy", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1114
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 538 (Div. 2)"
rating: 800
weight: 1114
solve_time_s: 324
verified: false
draft: false
---

[CF 1114A - Got Any Grapes?](https://codeforces.com/problemset/problem/1114/A)

**Rating:** 800  
**Tags:** brute force, greedy, implementation  
**Solve time:** 5m 24s  
**Verified:** no  

## Solution
## Problem Understanding

We have three people with different grape preferences and three piles of grapes.

Andrew wants exactly the first type of grape, green grapes. If he needs `x` grapes, all of them must come from the green pile.

Dmitry dislikes black grapes. He can eat green or purple grapes. He needs at least `y` grapes in total from those two colors.

Michal has no restrictions. He can eat grapes of any color and needs at least `z` grapes.

The input gives the required amounts `x`, `y`, and `z`, followed by the available counts `a`, `b`, and `c` of green, purple, and black grapes. We must determine whether there exists some distribution that satisfies all three people.

The constraints are tiny. Every value is at most `10^5`, and there is only a single test case. Even a brute-force search over many possibilities would fit comfortably, but the structure of the problem allows an even simpler constant-time solution.

The tricky part is that the colors have different levels of flexibility. Green grapes are the most restricted resource because Andrew can only eat green grapes. Purple grapes are more flexible because Dmitry can use them. Black grapes are the most flexible only for Michal, since nobody else can use them. A careless implementation may check only the total number of grapes and miss these restrictions.

Consider this example:

```
3 1 1
2 100 100
```

The total number of grapes is more than enough, but Andrew needs three green grapes and only two exist. The correct answer is `NO`.

Another subtle case is when Andrew can be satisfied, but Dmitry cannot.

```
2 5 1
2 4 100
```

After giving Andrew his two green grapes, no green grapes remain. Dmitry can only use the four purple grapes, which is not enough to reach five. The correct answer is `NO`.

A third case is when both Andrew and Dmitry can be satisfied, but Michal cannot.

```
1 1 10
1 1 8
```

Andrew takes one green grape. Dmitry takes one purple grape. Nothing remains, so Michal receives zero grapes although he needs ten. The correct answer is `NO`.

These examples show that the order of allocation matters. The most restricted consumers should be checked first.

## Approaches

A brute-force idea is to try every possible way of assigning green grapes between Andrew and Dmitry, then check whether the remaining grapes can satisfy everyone else. Since each pile size can reach `10^5`, enumerating all distributions would require up to about `10^5` possibilities. That is still manageable here, but it is unnecessarily complicated.

The key observation is that the restrictions form a natural hierarchy.

Andrew is the most constrained because he can consume only green grapes. If there are fewer than `x` green grapes, no solution exists.

Once Andrew receives his grapes, any remaining green grapes become available to Dmitry. Dmitry can use both green and purple grapes. If the total amount of remaining green plus all purple grapes is less than `y`, no solution exists.

After satisfying Andrew and Dmitry, every grape that remains, regardless of color, can be given to Michal. If the total remaining grapes are at least `z`, a valid distribution exists.

Because each step greedily satisfies the most constrained person first, we never waste a resource that might be needed later.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(a) | O(1) | Accepted but unnecessary |
| Optimal | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Check whether there are at least `x` green grapes. If `a < x`, output `NO` because Andrew cannot be satisfied.
2. Give Andrew his required grapes by subtracting `x` from `a`. The remaining green grapes are now available for Dmitry.
3. Check whether the remaining green grapes plus all purple grapes can satisfy Dmitry. If `a + b < y`, output `NO`.
4. Give Dmitry his required grapes. Since Dmitry can use green grapes first and then purple grapes, compute how many grapes remain after consuming `y` grapes from the combined pool.
5. Let `remaining = a + b - y + c`. This is the total number of grapes left for Michal.
6. If `remaining >= z`, output `YES`. Otherwise output `NO`.

### Why it works

Andrew's requirements are the strictest. Any valid solution must reserve `x` green grapes for him. Checking this first is mandatory.

After Andrew is satisfied, Dmitry can use every remaining grape that is not black. If the combined amount of remaining green and purple grapes is less than `y`, no arrangement can help because those are the only colors Dmitry accepts.

Once Andrew and Dmitry are satisfied, Michal can consume any leftover grapes. At that point only the total number of remaining grapes matters. If at least `z` grapes remain, Michal can always take them regardless of color.

Each check corresponds exactly to a necessary condition, and after satisfying the more restricted people first, those conditions are also sufficient. Hence the algorithm is correct.

## Python Solution

```python
import sys
input = sys.stdin.readline

x, y, z = map(int, input().split())
a, b, c = map(int, input().split())

if a < x:
    print("NO")
    sys.exit()

a -= x

if a + b < y:
    print("NO")
    sys.exit()

remaining = a + b - y + c

if remaining >= z:
    print("YES")
else:
    print("NO")
```

The first condition handles Andrew. If there are not enough green grapes, the answer is immediately impossible.

After subtracting Andrew's grapes, the variable `a` represents the green grapes that remain available. Dmitry can use these together with all purple grapes, so the second condition checks `a + b`.

The expression `a + b - y` represents how many green and purple grapes remain after Dmitry receives exactly `y` grapes. Adding `c` includes all black grapes, which only Michal may need.

The implementation avoids explicitly constructing a distribution because only the counts matter. No loops are needed, and all arithmetic easily fits within normal integer ranges.

## Worked Examples

### Sample 1

Input:

```
1 6 2
4 3 3
```

| Step | a | b | c | Action |
| --- | --- | --- | --- | --- |
| Initial | 4 | 3 | 3 | Start |
| Andrew check | 4 | 3 | 3 | 4 ≥ 1, possible |
| After Andrew | 3 | 3 | 3 | Subtract 1 green |
| Dmitry check | 3 | 3 | 3 | 3 + 3 = 6 ≥ 6 |
| After Dmitry | 0 | 0 | 3 | Consume 6 grapes |
| Michal check | 0 | 0 | 3 | 3 ≥ 2 |

Result: `YES`

This example shows the intended flow. Andrew consumes his required green grapes first. Dmitry then uses all remaining green and purple grapes. The black grapes remain for Michal.

### Sample 2

```
3 1 1
2 5 5
```

| Step | a | b | c | Action |
| --- | --- | --- | --- | --- |
| Initial | 2 | 5 | 5 | Start |
| Andrew check | 2 | 5 | 5 | 2 < 3 |

Result: `NO`

This example demonstrates the most restrictive constraint. Even though there are many grapes overall, Andrew cannot receive enough green grapes.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only a few arithmetic operations and comparisons |
| Space | O(1) | Uses a constant number of variables |

The algorithm performs a fixed amount of work regardless of the input values. It easily fits within the one-second time limit and the memory usage is negligible.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    x, y, z = map(int, input().split())
    a, b, c = map(int, input().split())

    if a < x:
        return "NO"

    a -= x

    if a + b < y:
        return "NO"

    remaining = a + b - y + c

    return "YES" if remaining >= z else "NO"

# provided sample
assert run("1 6 2\n4 3 3\n") == "YES", "sample 1"

# custom cases
assert run("1 1 1\n1 1 1\n") == "YES", "minimum feasible"
assert run("3 1 1\n2 100 100\n") == "NO", "not enough green grapes"
assert run("2 5 1\n2 4 100\n") == "NO", "not enough green+purple for Dmitry"
assert run("100000 100000 100000\n100000 100000 100000\n") == "YES", "maximum values"
assert run("1 1 10\n1 1 8\n") == "NO", "not enough total remaining for Michal"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 1 / 1 1 1` | YES | Smallest feasible case |
| `3 1 1 / 2 100 100` | NO | Andrew's restriction |
| `2 5 1 / 2 4 100` | NO | Dmitry's restriction |
| `100000 100000 100000 / 100000 100000 100000` | YES | Maximum bounds |
| `1 1 10 / 1 1 8` | NO | Michal's remaining-grapes check |

## Edge Cases

### Not enough green grapes

Input:

```
3 1 1
2 100 100
```

The algorithm immediately checks `a < x`. Since `2 < 3`, it outputs `NO`.

A solution is impossible because Andrew accepts only green grapes. Extra purple or black grapes cannot compensate.

### Enough green grapes, but not enough grapes for Dmitry

Input:

```
2 5 1
2 4 100
```

Andrew consumes two green grapes, leaving:

```
a = 0
b = 4
```

The algorithm checks `a + b < y`:

```
0 + 4 < 5
```

This is true, so the answer is `NO`.

Dmitry cannot eat black grapes, so the large black pile is irrelevant.

### Enough for Andrew and Dmitry, but not enough for Michal

Input:

```
1 1 10
1 1 8
```

After Andrew:

```
a = 0
```

Dmitry consumes one grape:

```
a + b - y = 0
```

The remaining grapes equal:

```
0 + 8 = 8
```

Since `8 < 10`, Michal cannot be satisfied and the algorithm outputs `NO`.

This confirms that satisfying the first two people does not automatically imply enough grapes remain for the third.

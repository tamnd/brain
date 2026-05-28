---
title: "CF 120C - Winnie-the-Pooh and honey"
description: "We have several jars of honey, and each jar starts with some amount of honey. Winnie repeatedly chooses the jar that currently contains the most honey. When Winnie picks a jar, two things may happen."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "implementation", "math"]
categories: ["algorithms"]
codeforces_contest: 120
codeforces_index: "C"
codeforces_contest_name: "School Regional Team Contest, Saratov, 2011"
rating: 1100
weight: 120
solve_time_s: 99
verified: true
draft: false
---

[CF 120C - Winnie-the-Pooh and honey](https://codeforces.com/problemset/problem/120/C)

**Rating:** 1100  
**Tags:** implementation, math  
**Solve time:** 1m 39s  
**Verified:** yes  

## Solution
## Problem Understanding

We have several jars of honey, and each jar starts with some amount of honey. Winnie repeatedly chooses the jar that currently contains the most honey.

When Winnie picks a jar, two things may happen. If the jar contains less than `k` kilos of honey, or if Winnie has already eaten from that jar three times, he stops touching that jar forever and gives the remaining honey to Piglet. Otherwise, he eats exactly `k` kilos from it and the jar stays available for future turns.

The process continues until every jar has been handed to Piglet. We must compute the total amount of honey Piglet finally receives.

The constraints are tiny. Both `n` and every `a[i]` are at most `100`. Even a direct simulation is easily fast enough. The total amount of honey is at most `100 * 100 = 10000`, and every eating action removes at least one kilo. A straightforward loop with repeated maximum searches performs only a few thousand operations.

The tricky part is understanding when a jar is removed. A jar is not discarded immediately after the third eating action. Winnie may eat from a jar exactly three times. The jar is discarded only when it becomes selected again afterward.

Consider this example:

```
1 3
10
```

Winnie eats three times:

```
10 -> 7 -> 4 -> 1
```

Now the jar has already been eaten from three times. When selected again, it is given to Piglet with `1` kilo remaining. The correct answer is:

```
1
```

A careless implementation might stop immediately after the third eating action and incorrectly give `4` instead.

Another subtle case happens when a jar becomes smaller than `k` after several operations.

```
1 5
14
```

Sequence:

```
14 -> 9 -> 4
```

Now the jar has less than `k`, so Piglet receives `4`. The answer is not `0`, because Winnie never partially eats a jar.

One more edge case appears when multiple jars share the same maximum value.

```
2 3
6 6
```

Either jar may be chosen first. The final result is still deterministic because each jar behaves independently. Each jar becomes `0` after two full eats, so Piglet gets `0 + 0 = 0`.

This observation hints at a much simpler solution than simulation.

## Approaches

The most direct approach is to simulate Winnie exactly as described. We keep track of the current honey in every jar and how many times Winnie has eaten from each one. On every step, we scan all jars to find the current maximum. If the chosen jar has already been eaten from three times, or contains less than `k`, we add its remaining honey to the answer and remove it from consideration. Otherwise, we subtract `k` and increment its eat counter.

This simulation is correct because it follows the rules literally. With these constraints it is also fast enough. At most three successful eating actions happen per jar, so there are at most `3n` reductions plus at most `n` removals. Every step scans all jars, giving roughly `O(n^2)` operations.

The interesting observation is that jars are completely independent from one another. The order in which Winnie chooses equal or different jars does not affect the final remainder of any individual jar.

For a single jar with `a[i]` honey:

If Winnie can eat from it fewer than three times before the amount drops below `k`, Piglet receives `a[i] mod k`.

If Winnie can eat from it at least three times, Winnie removes exactly `3k` honey total and then the jar is discarded on the next selection. Piglet receives `a[i] - 3k`.

So the remaining honey for one jar is simply:

```
max(a[i] - 3k, a[i] % k)
```

An even cleaner expression is:

If `a[i] < 3k`, Piglet gets `a[i] % k`.

Otherwise, Piglet gets `a[i] - 3k`.

This reduces the problem to processing each jar once.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(n²) | O(n) | Accepted |
| Mathematical Observation | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read `n` and `k`, then read the array of jar sizes.
2. Initialize the answer to `0`.
3. Process every jar independently.
4. For a jar containing `x` kilos:

If `x < 3 * k`, Winnie cannot complete three full eating operations. He keeps subtracting `k` while possible, and Piglet finally gets the remainder `x % k`.
5. Otherwise, Winnie successfully eats exactly three times from this jar.

After three operations, the jar contains `x - 3k`. On the next time the jar becomes the maximum, it is immediately handed to Piglet because the three-eat limit has been reached.
6. Add the correct remaining amount for this jar to the total answer.
7. Print the answer.

### Why it works

Each jar evolves independently. The only actions possible on a jar are subtracting `k` or permanently removing it. Winnie can subtract `k` at most three times from any jar.

If a jar runs below `k` before three operations, no more honey can be eaten from it, so the final remainder is exactly `x % k`.

If a jar survives three operations, Winnie removes exactly `3k` honey total. The rules forbid any further eating from that jar, so the remaining amount `x - 3k` goes directly to Piglet.

Since the final contribution of every jar depends only on its own initial value, summing these independent results produces the correct total.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, k = map(int, input().split())
    a = list(map(int, input().split()))

    ans = 0

    for x in a:
        if x < 3 * k:
            ans += x % k
        else:
            ans += x - 3 * k

    print(ans)

solve()
```

The solution processes each jar separately because the final remaining honey depends only on how many times Winnie can eat from that jar.

The condition `x < 3 * k` is the key observation. If the jar contains less than `3k`, Winnie cannot remove `k` three full times. He eventually stops because the remaining honey becomes smaller than `k`, and Piglet receives the remainder `x % k`.

Otherwise, Winnie successfully performs exactly three eating actions. After that, the rules prevent further eating from the same jar, so the leftover amount is `x - 3 * k`.

A common mistake is using `<=` instead of `<`. For example:

```
x = 9, k = 3
```

Winnie can eat exactly three times:

```
9 -> 6 -> 3 -> 0
```

Piglet receives `0`, not `9 % 3` by accident. The strict inequality handles this correctly.

All arithmetic fits comfortably inside standard Python integers.

## Worked Examples

### Example 1

Input:

```
3 3
15 8 10
```

| Jar | Initial Honey | Condition | Piglet Gets |
| --- | --- | --- | --- |
| 1 | 15 | 15 ≥ 9 | 15 - 9 = 6 |
| 2 | 8 | 8 < 9 | 8 % 3 = 2 |
| 3 | 10 | 10 ≥ 9 | 10 - 9 = 1 |

Total:

```
6 + 2 + 1 = 9
```

Output:

```
9
```

This example shows both behaviors. The first and third jars survive three eating operations, while the second becomes too small before reaching the limit.

### Example 2

Input:

```
2 5
14 20
```

| Jar | Initial Honey | Condition | Piglet Gets |
| --- | --- | --- | --- |
| 1 | 14 | 14 < 15 | 14 % 5 = 4 |
| 2 | 20 | 20 ≥ 15 | 20 - 15 = 5 |

Total:

```
4 + 5 = 9
```

Output:

```
9
```

The first jar demonstrates the "less than `k`" stopping condition. The second jar demonstrates the "three times eaten" stopping condition.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each jar is processed once |
| Space | O(1) | Only a few variables are used |

With `n ≤ 100`, even simulation would pass comfortably. The mathematical approach is simpler and faster, requiring only one pass through the array.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve():
    input = sys.stdin.readline

    n, k = map(int, input().split())
    a = list(map(int, input().split()))

    ans = 0

    for x in a:
        if x < 3 * k:
            ans += x % k
        else:
            ans += x - 3 * k

    print(ans)

def run(inp: str) -> str:
    backup_stdin = sys.stdin
    backup_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    out = sys.stdout.getvalue()

    sys.stdin = backup_stdin
    sys.stdout = backup_stdout

    return out.strip()

# provided sample
assert run("3 3\n15 8 10\n") == "9", "sample 1"

# minimum size
assert run("1 1\n1\n") == "0", "minimum case"

# exactly three full eats
assert run("1 3\n9\n") == "0", "exactly 3 operations"

# becomes smaller than k
assert run("1 5\n14\n") == "4", "remainder case"

# all equal values
assert run("4 2\n7 7 7 7\n") == "4", "all equal"

# maximum style values
assert run("3 1\n100 100 100\n") == "291", "large values"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 / 1` | `0` | Smallest valid input |
| `1 3 / 9` | `0` | Exactly three successful eating operations |
| `1 5 / 14` | `4` | Jar becomes smaller than `k` |
| `4 2 / 7 7 7 7` | `4` | Repeated equal values |
| `3 1 / 100 100 100` | `291` | Large values and repeated subtraction |

## Edge Cases

Consider the case where a jar can be eaten from exactly three times.

Input:

```
1 3
10
```

Execution:

```
10 -> 7 -> 4 -> 1
```

At this point Winnie has already eaten three times, so the remaining `1` kilo goes to Piglet. The algorithm checks:

```
10 >= 3 * 3
```

so Piglet receives:

```
10 - 9 = 1
```

which matches the simulation exactly.

Now consider a jar that becomes too small before three operations.

Input:

```
1 5
14
```

Execution:

```
14 -> 9 -> 4
```

The remaining amount is below `k`, so Piglet gets `4`. The algorithm uses:

```
14 < 15
```

and computes:

```
14 % 5 = 4
```

which is correct.

Finally, consider multiple equal maximum jars.

Input:

```
2 3
6 6
```

Each jar evolves independently:

```
6 -> 3 -> 0
```

Piglet receives `0` from each jar, for a final answer of `0`.

The order in which Winnie chooses between equal jars never changes the final remaining amount, which is why the independent per-jar formula is valid.

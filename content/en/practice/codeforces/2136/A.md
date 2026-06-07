---
title: "CF 2136A - In the Dream"
description: "We know the score at halftime and the score at full time. If the halftime score is a:b, then during the first half the RiOI team scored exactly a goals and the KDOI team scored exactly b goals."
date: "2026-06-08T02:35:00+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "math"]
categories: ["algorithms"]
codeforces_contest: 2136
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 1046 (Div. 2)"
rating: 800
weight: 2136
solve_time_s: 88
verified: true
draft: false
---

[CF 2136A - In the Dream](https://codeforces.com/problemset/problem/2136/A)

**Rating:** 800  
**Tags:** greedy, math  
**Solve time:** 1m 28s  
**Verified:** yes  

## Solution
## Problem Understanding

We know the score at halftime and the score at full time.

If the halftime score is `a:b`, then during the first half the RiOI team scored exactly `a` goals and the KDOI team scored exactly `b` goals.

If the final score is `c:d`, then during the second half the RiOI team scored `c-a` goals and the KDOI team scored `d-b` goals.

The only restriction is that inside each half, no team may score three goals in a row. The two halves are independent. A streak at the end of the first half does not continue into the second half.

For each test case, we must determine whether it is possible to arrange the goals in the first half and in the second half so that neither half contains three consecutive goals by the same team.

The scores are at most 100, and there are at most 1000 test cases. These bounds are tiny. Even a solution that performs some computation for every possible score pair would easily fit within the limits. The real challenge is identifying the mathematical condition that characterizes when a valid goal sequence exists.

A common mistake is to think only about the total match score. The restriction applies separately to each half. For example:

```
a=1 b=4 c=2 d=5
```

The first half has score `1:4` and the second half contributes `1:1`. Both halves can be arranged validly, so the answer is `YES`.

Another easy mistake is forgetting that a half with no goals is always valid. For example:

```
a=4 b=1 c=4 d=1
```

The second half contains zero goals. An empty sequence cannot contain three consecutive goals, so the answer is `YES`.

The most important edge case occurs when one team scores far more goals than the other. For example:

```
a=0 b=100
```

Every goal belongs to KDOI. That inevitably creates a run of 100 consecutive KDOI goals, which violates the rule. The first half alone is impossible, so the answer is `NO`.

## Approaches

A brute-force viewpoint is useful for discovering the condition.

Suppose a half contains `x` RiOI goals and `y` KDOI goals. We could try all sequences containing exactly those counts and check whether any sequence avoids three identical consecutive goals. This is correct because it directly tests the definition of validity.

The problem is that the number of sequences is enormous. A half with 100 goals already has roughly `2^100` possible arrangements. Exhaustive search is hopeless.

The key observation is that a team's goals can appear only in blocks of length at most 2.

Assume one team scores more goals than the other. Let

```
big = max(x, y)
small = min(x, y)
```

The `small` goals can be used as separators. They create at most `small + 1` gaps:

```
_ S _ S _ S _ ...
```

Inside each gap, the larger-scoring team may contribute at most 2 goals, otherwise a run of length 3 appears.

Since there are `small + 1` gaps and each gap can hold at most 2 goals, the maximum number of goals for the larger team is

```
2 * (small + 1)
```

So a valid sequence exists exactly when

```
big <= 2 * (small + 1)
```

This condition is also sufficient. If it holds, we can distribute the larger team's goals among the available gaps without exceeding 2 per gap.

We simply need to check this condition for the first half and for the second half independently.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | Exponential | Too slow |
| Optimal | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

For each test case:

1. Compute the score counts for the first half:

```
(a, b)
```
2. Check whether a valid first-half sequence exists.

Let:

```
big = max(a, b)
small = min(a, b)
```

The half is valid if:

```
big <= 2 * (small + 1)
```
3. Compute the goals scored during the second half:

```
x = c - a
y = d - b
```
4. Check the same condition for `(x, y)`.

Again, the half is valid if:

```
max(x, y) <= 2 * (min(x, y) + 1)
```
5. Print `"YES"` if both halves are valid. Otherwise print `"NO"`.

### Why it works

Consider any half with counts `(x, y)`. Let the larger count be `big` and the smaller count be `small`.

The `small` goals divide the sequence into at most `small + 1` positions where goals of the larger team can be placed. Since three consecutive equal goals are forbidden, each position may contain at most 2 such goals. Hence every valid sequence satisfies

```
big <= 2 * (small + 1)
```

Conversely, if this inequality holds, we can distribute the `big` goals among the `small + 1` positions so that no position receives more than 2 goals. Placing the separator goals between those positions produces a valid sequence.

Thus the inequality is both necessary and sufficient. Since the two halves are independent, the dream is possible exactly when both halves satisfy the condition.

## Python Solution

```python
import sys
input = sys.stdin.readline

def valid(x, y):
    big = max(x, y)
    small = min(x, y)
    return big <= 2 * (small + 1)

t = int(input())

for _ in range(t):
    a, b, c, d = map(int, input().split())

    first_half = valid(a, b)
    second_half = valid(c - a, d - b)

    print("YES" if first_half and second_half else "NO")
```

The helper function implements the mathematical characterization of a valid half.

For each test case we evaluate two independent halves. The first half directly uses `(a, b)`. The second half uses the additional goals scored after halftime, namely `(c-a, d-b)`.

No construction of the actual goal sequence is required. The proof shows that the inequality completely determines whether a valid arrangement exists.

The implementation avoids all boundary issues automatically. Empty halves work because, for example, `(0, 0)` satisfies the inequality. Cases where only one team scores are handled correctly as well. For instance `(0, 2)` is valid, while `(0, 3)` is not.

## Worked Examples

### Example 1

Input:

```
1 4 2 5
```

First half: `(1, 4)`

Second half: `(1, 1)`

| Half | x | y | big | small | Condition |
| --- | --- | --- | --- | --- | --- |
| First | 1 | 4 | 4 | 1 | 4 ≤ 4 |
| Second | 1 | 1 | 1 | 1 | 1 ≤ 4 |

Both halves satisfy the condition, so the answer is:

```
YES
```

This example shows that a heavily unbalanced half can still be valid. A sequence such as `KKRKK` contains four K goals and one R goal without ever creating three consecutive K goals.

### Example 2

Input:

```
0 100 0 100
```

First half: `(0, 100)`

Second half: `(0, 0)`

| Half | x | y | big | small | Condition |
| --- | --- | --- | --- | --- | --- |
| First | 0 | 100 | 100 | 0 | 100 ≤ 2 |
| Second | 0 | 0 | 0 | 0 | 0 ≤ 2 |

The first-half condition fails, so the answer is:

```
NO
```

This demonstrates the separator argument. With zero goals from one team, there is only one gap available, which can hold at most two goals before creating a forbidden streak.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Constant work per test case |
| Space | O(1) | Only a few integer variables are used |

Even with 1000 test cases, the program performs only a handful of arithmetic operations per case. The solution easily fits within the time and memory limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    def valid(x, y):
        big = max(x, y)
        small = min(x, y)
        return big <= 2 * (small + 1)

    t = int(input())
    out = []

    for _ in range(t):
        a, b, c, d = map(int, input().split())
        ok = valid(a, b) and valid(c - a, d - b)
        out.append("YES" if ok else "NO")

    return "\n".join(out) + "\n"

# provided sample
assert run(
"""11
1 4 1 4
4 1 4 1
1 4 2 5
0 100 0 100
1 4 2 9
3 1 13 5
8 11 17 36
19 41 30 50
20 38 30 60
0 0 0 0
100 100 100 100
"""
) == """YES
YES
YES
NO
NO
YES
NO
NO
YES
YES
YES
"""

# minimum values
assert run(
"""1
0 0 0 0
"""
) == """YES
"""

# boundary between valid and invalid
assert run(
"""2
0 2 0 2
0 3 0 3
"""
) == """YES
NO
"""

# second half causes failure
assert run(
"""1
1 1 1 4
"""
) == """NO
"""

# maximum values, all equal
assert run(
"""1
100 100 100 100
"""
) == """YES
"""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `0 0 0 0` | `YES` | Empty match is valid |
| `0 2 0 2` | `YES` | Largest count exactly equals the limit |
| `0 3 0 3` | `NO` | First value beyond the limit |
| `1 1 1 4` | `NO` | First half valid, second half invalid |
| `100 100 100 100` | `YES` | Maximum balanced scores |

## Edge Cases

Consider:

```
1
0 2 0 2
```

For the first half, `big = 2` and `small = 0`. The condition becomes:

```
2 <= 2 * (0 + 1)
```

which is true. The sequence `KK` is allowed because the restriction forbids three consecutive goals, not two. The algorithm prints `YES`.

Now consider:

```
1
0 3 0 3
```

Here:

```
big = 3
small = 0
```

and

```
3 <= 2
```

is false. The only possible sequence is `KKK`, which contains three consecutive goals by the same team. The algorithm correctly prints `NO`.

Another subtle case is:

```
1
4 1 4 1
```

The second-half counts are:

```
(0, 0)
```

The condition holds immediately because both counts are zero. Since halves are independent, an empty second half is perfectly valid. The algorithm outputs `YES`.

Finally, consider:

```
1
1 1 1 4
```

The first half satisfies the condition. The second half contributes `(0, 3)`, which fails because `3 > 2`. Looking only at the final score would miss this issue, but checking each half separately correctly yields `NO`.

---
title: "CF 82A - Double Cola"
description: "Five people stand in a queue in a fixed order: Sheldon, Leonard, Penny, Rajesh, Howard. Whenever the person at the front buys a cola, that person immediately creates a copy of themselves, and both copies go to the back of the queue. The queue keeps growing forever."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "implementation", "math"]
categories: ["algorithms"]
codeforces_contest: 82
codeforces_index: "A"
codeforces_contest_name: "Yandex.Algorithm 2011: Qualification 2"
rating: 1100
weight: 82
solve_time_s: 90
verified: true
draft: false
---

[CF 82A - Double Cola](https://codeforces.com/problemset/problem/82/A)

**Rating:** 1100  
**Tags:** implementation, math  
**Solve time:** 1m 30s  
**Verified:** yes  

## Solution
## Problem Understanding

Five people stand in a queue in a fixed order: Sheldon, Leonard, Penny, Rajesh, Howard.

Whenever the person at the front buys a cola, that person immediately creates a copy of themselves, and both copies go to the back of the queue. The queue keeps growing forever.

We are given the number `n`, representing the `n`-th cola sold. The task is to determine which person drinks that cola.

The constraint `n ≤ 10^9` completely changes the nature of the problem. A direct simulation would repeatedly push and pop names from a queue, but after enough steps the queue becomes enormous. Even a linear algorithm with one operation per cola would require up to one billion operations, which is far beyond what fits into a 1 second time limit.

The key observation is that the process grows in layers. Initially each person appears once. After all five drink once, each appears twice. Then each appears four times, then eight times, and so on. The queue expands geometrically, which means we can skip entire blocks instead of simulating every drink individually.

There are a few easy places to make mistakes.

The first common error is mixing 0-based and 1-based indexing. The problem numbers colas starting from 1. For example:

Input:

```
1
```

Correct output:

```
Sheldon
```

If we accidentally treat `n` as 0-based, we would shift every answer by one position.

Another subtle case happens exactly at group boundaries. Consider the first 5 drinks:

| Drink number | Person |
| --- | --- |
| 1 | Sheldon |
| 2 | Leonard |
| 3 | Penny |
| 4 | Rajesh |
| 5 | Howard |

Then the next block starts with two Sheldons:

| Drink number | Person |
| --- | --- |
| 6 | Sheldon |
| 7 | Sheldon |

If the subtraction logic skips one extra group, values like `n = 6` or `n = 10` become wrong.

Large values are another danger. Since counts double every round, implementations using floating point logarithms can introduce precision issues near boundaries. Integer arithmetic is safer and simpler.

## Approaches

A straightforward simulation uses a queue.

We start with:

```
[Sheldon, Leonard, Penny, Rajesh, Howard]
```

At each step we remove the front person, record that they drank a cola, then append two copies of that same person to the back.

This works because it exactly matches the rules of the process. After enough operations we eventually reach the `n`-th drink.

The problem is growth rate. Every drink increases queue size by one. If `n = 10^9`, we would need roughly one billion queue operations and enormous memory. That is impossible within the limits.

The structure of the queue gives us something much better.

Think about how many times each name appears consecutively during a phase.

At the beginning:

```
Sheldon Leonard Penny Rajesh Howard
```

Each person appears once.

After everyone drinks once:

```
Sheldon Sheldon Leonard Leonard Penny Penny ...
```

Each person now appears twice.

Then:

```
Sheldon Sheldon Sheldon Sheldon ...
```

Each person appears four times.

So the process works in blocks:

| Phase | Copies per person | Total drinks in phase |
| --- | --- | --- |
| 0 | 1 | 5 |
| 1 | 2 | 10 |
| 2 | 4 | 20 |
| 3 | 8 | 40 |

Instead of simulating individual drinks, we can subtract whole phases.

Suppose `n = 52`.

The phases consume:

```
5 + 10 + 20 = 35
```

So drink 52 lies inside the next phase, where each person appears 8 times consecutively.

Inside that phase:

```
52 - 35 = 17
```

The first 8 positions belong to Sheldon, the next 8 to Leonard, and the next 8 to Penny.

Position 17 falls into Penny's segment.

This reduces the problem to repeatedly doubling a block size until we locate the correct phase.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n) | O(n) | Too slow |
| Optimal | O(log n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Store the five names in their original order.
2. Let `group = 1`. This means each person currently appears once consecutively.
3. Compute how many drinks belong to the current phase. Since there are 5 people and each appears `group` times, the phase size is `5 * group`.
4. While `n` is larger than the current phase size, subtract the whole phase from `n` and double `group`.

This works because every completed phase fully disappears before the next one starts.
5. After the loop finishes, `n` lies inside the current phase.
6. Inside this phase, every person occupies exactly `group` consecutive positions.
7. Convert the position into a person index using:

```
index = (n - 1) // group
```
8. Output the name at that index.

### Why it works

Each phase contains all drinks where every person appears the same number of consecutive times.

If `group = 2^k`, then the phase contains:

```
[Sheldon repeated group times]
[Leonard repeated group times]
[Penny repeated group times]
[Rajesh repeated group times]
[Howard repeated group times]
```

Subtracting earlier phases is safe because those drinks occur entirely before the current phase begins.

Once we locate the correct phase, dividing by `group` tells us which person's segment contains the desired drink. Since the names remain in the same order in every phase, the computed index always matches the correct answer.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())

    names = ["Sheldon", "Leonard", "Penny", "Rajesh", "Howard"]

    group = 1

    while n > 5 * group:
        n -= 5 * group
        group *= 2

    index = (n - 1) // group
    print(names[index])

solve()
```

The solution starts by storing the five names in order because that order never changes throughout the process.

The variable `group` represents how many consecutive copies each person has in the current phase. Initially every person appears once, so `group = 1`.

The loop removes entire phases at once. For example, when `group = 4`, the current phase contains `5 * 4 = 20` drinks. If `n` is larger than 20, we know the desired drink cannot belong to this phase, so we subtract all 20 drinks and move to the next phase where every count doubles.

The expression:

```
(n - 1) // group
```

is the most important boundary detail.

Suppose `group = 4`.

Then positions:

```
1 2 3 4
```

belong to Sheldon,

```
5 6 7 8
```

belong to Leonard, and so on.

Subtracting 1 before integer division correctly converts the 1-based position into a 0-based block index.

Without the `-1`, exact boundaries would fail. For example, position 4 would incorrectly map to Leonard instead of Sheldon.

The algorithm uses only integer arithmetic, so there are no floating point precision problems even for very large values of `n`.

## Worked Examples

### Example 1

Input:

```
1
```

| Step | n | group | Phase size | Action |
| --- | --- | --- | --- | --- |
| Start | 1 | 1 | 5 | `n <= 5`, stop |
| Final | 1 | 1 | 5 | index = (1 - 1) // 1 = 0 |

Output:

```
Sheldon
```

This example shows the smallest possible input. The answer lies in the very first phase, so no subtraction happens.

### Example 2

Input:

```
52
```

| Step | n | group | Phase size | Action |
| --- | --- | --- | --- | --- |
| Start | 52 | 1 | 5 | subtract phase |
| After 1st subtraction | 47 | 2 | 10 | subtract phase |
| After 2nd subtraction | 37 | 4 | 20 | subtract phase |
| After 3rd subtraction | 17 | 8 | 40 | stop |
| Final | 17 | 8 | 40 | index = (17 - 1) // 8 = 2 |

Index `2` corresponds to Penny.

Output:

```
Penny
```

This trace demonstrates how the algorithm skips entire sections of the queue instead of simulating every drink individually.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(log n) | `group` doubles every iteration |
| Space | O(1) | only a few variables are stored |

Since `group` grows exponentially, the loop runs only about 30 times even when `n = 10^9`. The solution easily fits within both the time and memory limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def solve():
    input = sys.stdin.readline

    n = int(input())

    names = ["Sheldon", "Leonard", "Penny", "Rajesh", "Howard"]

    group = 1

    while n > 5 * group:
        n -= 5 * group
        group *= 2

    index = (n - 1) // group
    print(names[index])

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out

    solve()

    sys.stdout = sys.__stdout__
    return out.getvalue()

# provided sample
assert run("1\n") == "Sheldon\n", "sample 1"

# boundary of first phase
assert run("5\n") == "Howard\n", "end of first phase"

# start of second phase
assert run("6\n") == "Sheldon\n", "start of doubled block"

# inside larger doubled group
assert run("52\n") == "Penny\n", "larger phase test"

# very large input
assert run("1000000000\n") == "Penny\n", "large input handling"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1` | `Sheldon` | minimum input |
| `5` | `Howard` | exact end of first phase |
| `6` | `Sheldon` | transition into next phase |
| `52` | `Penny` | skipping multiple phases |
| `1000000000` | `Penny` | large input performance and correctness |

## Edge Cases

Consider the boundary between phases.

Input:

```
5
```

The first phase has size 5 because each of the five people appears once.

The loop condition:

```
while n > 5 * group
```

does not execute because `5 > 5` is false.

Then:

```
index = (5 - 1) // 1 = 4
```

Index 4 corresponds to Howard.

Output:

```
Howard
```

Using `>=` instead of `>` would incorrectly subtract the whole phase and produce the wrong answer.

Now consider the first drink of the next phase.

Input:

```
6
```

Initially:

```
group = 1
phase size = 5
```

Since `6 > 5`, we subtract:

```
n = 1
group = 2
```

Now the current phase is:

```
Sheldon Sheldon Leonard Leonard ...
```

We compute:

```
index = (1 - 1) // 2 = 0
```

which correctly maps to Sheldon.

This case confirms that phase transitions are handled properly.

Finally, consider a very large value.

Input:

```
1000000000
```

The loop doubles `group` repeatedly:

```
1, 2, 4, 8, 16, ...
```

After only about 30 iterations, the correct phase is found.

No queue is ever built, so memory usage stays constant and execution remains fast even for the maximum constraint.

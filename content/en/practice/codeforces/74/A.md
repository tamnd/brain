---
title: "CF 74A - Room Leader"
description: "We are given the scoreboard data for every participant in a Codeforces room. Each contestant has a handle, a number of successful hacks, a number of unsuccessful hacks, and the points earned from problems A through E."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 74
codeforces_index: "A"
codeforces_contest_name: "Codeforces Beta Round 68"
rating: 1000
weight: 74
solve_time_s: 95
verified: true
draft: false
---

[CF 74A - Room Leader](https://codeforces.com/problemset/problem/74/A)

**Rating:** 1000  
**Tags:** implementation  
**Solve time:** 1m 35s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given the scoreboard data for every participant in a Codeforces room. Each contestant has a handle, a number of successful hacks, a number of unsuccessful hacks, and the points earned from problems A through E.

The total score for one participant is computed as:

- the sum of the five problem scores,
- plus `100 × successful_hacks`,
- minus `50 × unsuccessful_hacks`.

Our task is simply to determine which participant has the highest final score and print their handle.

The constraints are extremely small. There are at most 50 participants, and each participant only has a fixed amount of information. Even an inefficient solution would comfortably fit within the time limit. A single pass over the contestants is already enough.

The main implementation risk is not algorithmic complexity, it is computing the score correctly and handling negative totals properly.

One easy mistake is forgetting that unsuccessful hacks subtract points.

Example:

```
2
alice 0 0 500 500 500 500 500
bob 0 10 500 500 500 500 500
```

Alice has `2500` points.

Bob has `2500 - 10 × 50 = 2000`.

The correct output is:

```
alice
```

A careless implementation that ignores hack penalties would incorrectly choose Bob as tied or equal.

Another subtle case is when a contestant solves nothing but still has a negative score because of failed hacks.

Example:

```
2
x 0 5 0 0 0 0 0
y 0 0 0 0 0 0 0
```

Contestant `x` has `-250`, while `y` has `0`.

The correct output is:

```
y
```

If we initialize the best score to `0` instead of something safely small, then all-negative cases could fail.

A third common bug is reading the input incorrectly because the handle is a string while the remaining fields are integers.

Example:

```
1
tourist_123 1 0 500 1000 1500 2000 2500
```

The correct output is:

```
tourist_123
```

The parser must keep the handle separate from the numeric values.

## Approaches

The brute-force idea is straightforward. For every participant, compute their final score from the input fields, then compare it against every other participant to check whether it is the maximum.

This works because the number of contestants is tiny. If there are `n` participants, this approach performs roughly `n²` comparisons. With `n ≤ 50`, that is only `2500` comparisons in the worst case.

The problem with this method is not performance here, but unnecessary work. Once we compute a contestant's score, we do not actually need to compare it against everyone else individually. We only care about the current maximum.

That observation leads to the optimal approach. While reading participants one by one, we compute their score immediately and maintain two variables:

- the best score seen so far,
- the corresponding handle.

Whenever a new participant has a larger score, we update both values.

This reduces the work from repeated comparisons to a single linear scan. The structure of the problem makes this natural because the winner depends only on the maximum score, not on any pairwise relationship between contestants.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(1) | Accepted |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the integer `n`, the number of contestants.
2. Initialize two variables:

- `best_score` as a very small number,
- `best_handle` as an empty string.

We need these variables to track the current leader while processing the input.
3. For each contestant:

- read the handle,
- read the number of successful hacks,
- read the number of unsuccessful hacks,
- read the five problem scores.
4. Compute the contestant's total score using:

```
total = sum(problem_scores) + 100 × successful_hacks - 50 × unsuccessful_hacks
```
5. Compare this total score with `best_score`.
6. If the new score is larger:

- update `best_score`,
- update `best_handle`.

This keeps the leader information correct after every processed contestant.
7. After all contestants are processed, print `best_handle`.

### Why it works

After processing any prefix of contestants, `best_score` stores the maximum score among all processed participants, and `best_handle` stores the corresponding handle.

Initially this invariant is true because no contestants have been processed yet and `best_score` is smaller than any possible real score.

When processing a new contestant, there are only two possibilities:

- their score is not larger than the current maximum, so the leader does not change,
- their score is larger, so replacing the stored leader keeps the invariant true.

After the final contestant, the invariant guarantees that the stored handle belongs to the participant with the highest score in the entire room.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())

best_score = -10**18
best_handle = ""

for _ in range(n):
    parts = input().split()

    handle = parts[0]
    plus = int(parts[1])
    minus = int(parts[2])

    scores = list(map(int, parts[3:]))

    total = sum(scores) + plus * 100 - minus * 50

    if total > best_score:
        best_score = total
        best_handle = handle

print(best_handle)
```

The solution follows the algorithm directly.

The first important detail is how the input line is parsed. The handle is stored separately because it is a string, while the remaining fields are integers.

The score computation exactly matches the contest rules. Successful hacks add `100` points, unsuccessful hacks subtract `50`, and the five problem scores are summed normally.

The variable `best_score` is initialized to a very small value instead of `0`. This avoids bugs when every contestant has a negative score.

The solution updates the leader immediately after computing each participant's score, so no extra arrays or sorting are necessary.

## Worked Examples

### Example 1

Input:

```
5
Petr 3 1 490 920 1000 1200 0
tourist 2 0 490 950 1100 1400 0
Egor 7 0 480 900 950 0 1000
c00lH4x0R 0 10 150 0 0 0 0
some_participant 2 1 450 720 900 0 0
```

| Contestant | Problem Sum | Hack Bonus/Penalty | Total | Current Leader |
| --- | --- | --- | --- | --- |
| Petr | 3610 | +250 | 3860 | Petr |
| tourist | 3940 | +200 | 4140 | tourist |
| Egor | 3330 | +700 | 4030 | tourist |
| c00lH4x0R | 150 | -500 | -350 | tourist |
| some_participant | 2070 | +150 | 2220 | tourist |

Final output:

```
tourist
```

This trace shows how the running maximum changes only when a larger score appears.

### Example 2

Input:

```
3
alice 0 5 0 0 0 0 0
bob 0 0 0 0 0 0 0
charlie 1 0 0 0 0 0 0
```

| Contestant | Problem Sum | Hack Bonus/Penalty | Total | Current Leader |
| --- | --- | --- | --- | --- |
| alice | 0 | -250 | -250 | alice |
| bob | 0 | 0 | 0 | bob |
| charlie | 0 | +100 | 100 | charlie |

Final output:

```
charlie
```

This example demonstrates why negative scores must be handled correctly and why the leader can change multiple times during the scan.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each contestant is processed exactly once |
| Space | O(1) | Only a few variables are stored |

With at most 50 contestants, the solution is far below the time and memory limits. Even slower approaches would pass, but the linear scan is the cleanest and simplest implementation.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def solve():
    input = sys.stdin.readline

    n = int(input())

    best_score = -10**18
    best_handle = ""

    for _ in range(n):
        parts = input().split()

        handle = parts[0]
        plus = int(parts[1])
        minus = int(parts[2])

        scores = list(map(int, parts[3:]))

        total = sum(scores) + plus * 100 - minus * 50

        if total > best_score:
            best_score = total
            best_handle = handle

    print(best_handle)

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out

    solve()

    sys.stdout = sys.__stdout__
    return out.getvalue().strip()

# provided sample
assert run(
"""5
Petr 3 1 490 920 1000 1200 0
tourist 2 0 490 950 1100 1400 0
Egor 7 0 480 900 950 0 1000
c00lH4x0R 0 10 150 0 0 0 0
some_participant 2 1 450 720 900 0 0
"""
) == "tourist", "sample 1"

# minimum-size input
assert run(
"""1
solo 0 0 0 0 0 0 0
"""
) == "solo", "single contestant"

# negative scores
assert run(
"""2
x 0 5 0 0 0 0 0
y 0 0 0 0 0 0 0
"""
) == "y", "negative totals"

# hack bonus changes winner
assert run(
"""2
alice 0 0 500 500 500 500 500
bob 3 0 500 500 500 500 500
"""
) == "bob", "successful hacks matter"

# boundary-style large values
assert run(
"""2
maxer 50 0 500 1000 1500 2000 2500
other 0 0 500 1000 1500 2000 2500
"""
) == "maxer", "large bonuses"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single contestant | `solo` | Minimum-size input |
| Negative-score case | `y` | Correct handling of negative totals |
| Equal problem scores but different hacks | `bob` | Successful hacks are added properly |
| Large-value case | `maxer` | Upper-bound style arithmetic |

## Edge Cases

Consider the case where all scores are negative except one zero score.

Input:

```
2
x 0 5 0 0 0 0 0
y 0 0 0 0 0 0 0
```

The algorithm starts with a very small `best_score`.

Processing `x`:

- total = `-250`
- leader becomes `x`

Processing `y`:

- total = `0`
- since `0 > -250`, leader becomes `y`

The output is:

```
y
```

This works because the initial value of `best_score` is smaller than every possible contestant score.

Now consider a case where hack penalties decide the winner.

Input:

```
2
alice 0 0 500 500 500 500 500
bob 0 10 500 500 500 500 500
```

The algorithm computes:

- `alice = 2500`
- `bob = 2000`

The leader remains `alice`.

The output is:

```
alice
```

This confirms that unsuccessful hacks are correctly subtracted.

Finally, consider handles containing underscores and digits.

Input:

```
1
tourist_123 1 0 500 1000 1500 2000 2500
```

The parser stores:

- handle = `tourist_123`
- remaining values as integers

The total score is computed normally, and the output is:

```
tourist_123
```

This verifies that the implementation separates the string handle from the numeric fields correctly.

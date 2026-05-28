---
title: "CF 155A - I_love_\\%username\\%"
description: "We are given the chronological contest scores of one programmer. A performance is called \"amazing\" when the current score is strictly greater than every previous score, or strictly smaller than every previous score."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "brute-force"]
categories: ["algorithms"]
codeforces_contest: 155
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 109 (Div. 2)"
rating: 800
weight: 155
solve_time_s: 264
verified: false
draft: false
---

[CF 155A - I_love_\\%username\\%](https://codeforces.com/problemset/problem/155/A)

**Rating:** 800  
**Tags:** brute force  
**Solve time:** 4m 24s  
**Verified:** no  

## Solution
## Problem Understanding

We are given the chronological contest scores of one programmer. A performance is called "amazing" when the current score is strictly greater than every previous score, or strictly smaller than every previous score.

The first contest never counts, because there are no earlier contests to compare against.

The task is to process the sequence and count how many times the programmer sets a new personal best or a new personal worst.

For example, consider:

```
100 50 200 150 200
```

The first score initializes both the best and worst records.

The second score, `50`, is lower than every previous score, so it breaks the worst record.

The third score, `200`, is higher than every previous score, so it breaks the best record.

The remaining scores do not break either record.

The answer is `2`.

The constraints are very small. The number of contests is at most `1000`, so even an `O(n²)` solution would pass comfortably within the time limit. Still, this problem has a very clean linear solution that scans the array once while maintaining only two values.

The tricky part is handling equality correctly. A score only counts if it is strictly larger than the current maximum or strictly smaller than the current minimum.

Consider this input:

```
4
10 10 10 10
```

The correct answer is `0`.

A careless implementation using `>=` or `<=` would incorrectly count repeated values as record-breaking performances.

Another subtle case is when records alternate repeatedly:

```
5
100 50 200 25 300
```

The correct answer is `4`.

Each new score breaks either the current minimum or maximum, and both records must be updated immediately after counting the event.

## Approaches

A direct brute-force solution checks every contest against all previous contests.

For contest `i`, we can scan contests `0` through `i-1` and determine whether the current score is strictly greater than all previous scores or strictly smaller than all previous scores.

This works because the definition of an amazing performance depends only on earlier contests. The logic is straightforward, but each position may compare against up to `n-1` earlier elements, leading to `O(n²)` time complexity.

With `n = 1000`, this still runs easily within limits. In the worst case, we perform about one million comparisons, which is trivial for modern hardware.

The faster approach comes from observing that we do not actually need all previous scores. At any moment, only two values matter:

```
current maximum score
current minimum score
```

If the next score is larger than the current maximum, it breaks the best-performance record.

If it is smaller than the current minimum, it breaks the worst-performance record.

After processing the score, we update the corresponding record.

This reduces the problem to a single left-to-right scan with constant extra memory.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(1) | Accepted |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the number of contests and the list of scores.
2. Initialize both `best` and `worst` with the first score.

The first contest establishes the initial records and is never counted as amazing.
3. Initialize `answer = 0`.
4. Iterate through the scores starting from the second contest.
5. For each score:

If the score is strictly greater than `best`, increment `answer` and update `best`.

If the score is strictly smaller than `worst`, increment `answer` and update `worst`.
6. After processing all scores, print `answer`.

### Why it works

At every step, `best` stores the largest score seen so far, and `worst` stores the smallest score seen so far.

When we process a new score, there are only three possibilities:

```
score > best
score < worst
worst <= score <= best
```

The first case means the programmer achieved a new highest score. The second case means a new lowest score. The third case means no record was broken.

Because the algorithm updates the records immediately after counting a new one, the invariant remains correct throughout the scan.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    scores = list(map(int, input().split()))

    best = scores[0]
    worst = scores[0]
    answer = 0

    for score in scores[1:]:
        if score > best:
            answer += 1
            best = score
        elif score < worst:
            answer += 1
            worst = score

    print(answer)

solve()
```

The solution starts by reading the input and initializing both record values using the first contest score.

The loop begins from the second element because the first contest cannot break any earlier record.

The `if` statement checks whether the current score exceeds the best score seen so far. If it does, we count an amazing performance and update the maximum.

The `elif` handles the opposite direction. Using `elif` instead of a second independent `if` is logically cleaner because a number cannot simultaneously be greater than the current maximum and smaller than the current minimum.

Strict comparisons are essential. Equal scores do not count as record-breaking performances.

The solution uses only constant extra memory because it stores just three integers beyond the input array.

## Worked Examples

### Example 1

Input:

```
5
100 50 200 150 200
```

| Contest | Score | Best Before | Worst Before | Amazing? | Best After | Worst After | Count |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 100 | - | - | No | 100 | 100 | 0 |
| 2 | 50 | 100 | 100 | Yes | 100 | 50 | 1 |
| 3 | 200 | 100 | 50 | Yes | 200 | 50 | 2 |
| 4 | 150 | 200 | 50 | No | 200 | 50 | 2 |
| 5 | 200 | 200 | 50 | No | 200 | 50 | 2 |

This trace shows how the algorithm maintains the running minimum and maximum. Equal values, like the last `200`, do not count because the comparison is strict.

### Example 2

Input:

```
10
1 2 3 4 5 4 3 2 1 0
```

| Contest | Score | Best Before | Worst Before | Amazing? | Best After | Worst After | Count |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 1 | - | - | No | 1 | 1 | 0 |
| 2 | 2 | 1 | 1 | Yes | 2 | 1 | 1 |
| 3 | 3 | 2 | 1 | Yes | 3 | 1 | 2 |
| 4 | 4 | 3 | 1 | Yes | 4 | 1 | 3 |
| 5 | 5 | 4 | 1 | Yes | 5 | 1 | 4 |
| 6 | 4 | 5 | 1 | No | 5 | 1 | 4 |
| 7 | 3 | 5 | 1 | No | 5 | 1 | 4 |
| 8 | 2 | 5 | 1 | No | 5 | 1 | 4 |
| 9 | 1 | 5 | 1 | No | 5 | 1 | 4 |
| 10 | 0 | 5 | 1 | Yes | 5 | 0 | 5 |

This example demonstrates that the running records continue to matter across the entire history, not just adjacent contests.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each score is processed once |
| Space | O(1) | Only a few variables are stored |

With at most `1000` contests, the linear solution is easily fast enough. Memory usage is negligible because the algorithm tracks only the current best score, current worst score, and the answer counter.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve():
    input = sys.stdin.readline

    n = int(input())
    scores = list(map(int, input().split()))

    best = scores[0]
    worst = scores[0]
    answer = 0

    for score in scores[1:]:
        if score > best:
            answer += 1
            best = score
        elif score < worst:
            answer += 1
            worst = score

    print(answer)

def run(inp: str) -> str:
    backup_stdin = sys.stdin
    backup_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    output = sys.stdout.getvalue()

    sys.stdin = backup_stdin
    sys.stdout = backup_stdout

    return output

# provided samples
assert run("5\n100 50 200 150 200\n") == "2\n", "sample 1"

assert run("10\n1 2 3 4 5 4 3 2 1 0\n") == "5\n", "sample 2"

# minimum size
assert run("1\n100\n") == "0\n", "single contest"

# all equal values
assert run("4\n10 10 10 10\n") == "0\n", "equal scores are not amazing"

# alternating new records
assert run("5\n100 50 200 25 300\n") == "4\n", "multiple alternating records"

# decreasing sequence
assert run("5\n9 8 7 6 5\n") == "4\n", "every contest breaks worst record"

# off-by-one style check
assert run("3\n5 10 10\n") == "1\n", "equal maximum should not count twice"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 100` | `0` | First contest never counts |
| `10 10 10 10` | `0` | Equal scores are ignored |
| `100 50 200 25 300` | `4` | Records can alternate repeatedly |
| `9 8 7 6 5` | `4` | Every lower score breaks the minimum |
| `5 10 10` | `1` | Equal maximum is not counted again |

## Edge Cases

Consider the case where all scores are identical:

```
4
10 10 10 10
```

The algorithm starts with:

```
best = 10
worst = 10
answer = 0
```

Every remaining score equals both records, so neither condition triggers.

The final answer remains `0`, which is correct because no strict improvement or decline occurred.

Now consider repeated maximum values:

```
3
5 10 10
```

After processing the second score:

```
best = 10
answer = 1
```

The third score equals `best`, but does not exceed it. Since the comparison is `>` rather than `>=`, the algorithm correctly avoids counting it again.

Finally, consider alternating record changes:

```
5
100 50 200 25 300
```

The sequence of records becomes:

```
100 -> new minimum 50 -> new maximum 200 -> new minimum 25 -> new maximum 300
```

Each new score exceeds one of the current boundaries, so the answer increases every time. The algorithm handles this naturally because it updates the running records immediately after each amazing performance.

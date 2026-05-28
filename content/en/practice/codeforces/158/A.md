---
title: "CF 158A - Next Round"
description: "We are given the final standings of a programming contest. The scores are already sorted in non-increasing order, meaning each participant has a score greater than or equal to the next participant. A participant advances to the next round if two conditions are true."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "*special", "implementation"]
categories: ["algorithms"]
codeforces_contest: 158
codeforces_index: "A"
codeforces_contest_name: "VK Cup 2012 Qualification Round 1"
rating: 800
weight: 158
solve_time_s: 89
verified: true
draft: false
---

[CF 158A - Next Round](https://codeforces.com/problemset/problem/158/A)

**Rating:** 800  
**Tags:** *special, implementation  
**Solve time:** 1m 29s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given the final standings of a programming contest. The scores are already sorted in non-increasing order, meaning each participant has a score greater than or equal to the next participant.

A participant advances to the next round if two conditions are true. Their score must be at least as large as the score of the participant currently in the k-th position, and their score must be positive.

The task is to count how many participants satisfy both conditions.

The constraints are extremely small. At most 50 participants exist, so even a simple linear scan is more than enough. Any algorithm with time complexity up to O(n²) would comfortably fit inside the limit. This problem is mainly about careful implementation rather than optimization.

The tricky part is correctly handling zero scores and ties around the k-th position.

Consider this example:

```
5 3
10 5 0 0 0
```

The 3rd participant has score 0. A careless solution might count everyone with score greater than or equal to 0, producing 5. That is wrong because participants must also have a positive score. The correct answer is 2.

Another subtle case appears when many participants share the same score as the k-th participant.

```
8 5
10 9 8 7 7 7 5 5
```

The participant in 5th place has score 7. Everyone with score 7 or higher advances, including the 6th participant. The correct answer is 6. A wrong implementation might simply output k, which would miss tied participants.

One more edge case is the smallest possible input:

```
1 1
0
```

The only participant scored 0, so nobody advances. The answer is 0, not 1.

## Approaches

The most direct approach is to examine every participant and check whether they satisfy the contest rules. We first find the score of the k-th participant, then count how many scores are both positive and at least that threshold.

This brute-force method is already completely acceptable because n is at most 50. In the worst case, we perform around 50 comparisons, which is effectively instantaneous.

A more complicated approach is unnecessary because the input is already sorted. The only observation we need is that the k-th participant defines the minimum qualifying score. Once we know that value, every participant can be checked independently.

The brute-force works because the qualification rule depends only on one fixed threshold. There is no need for searching, sorting, or additional data structures. A single linear scan is enough.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n) | O(1) | Accepted |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the integers `n` and `k`.
2. Read the array of scores.
3. Find the score of the participant in the k-th position. Since Python uses 0-based indexing, this value is `scores[k - 1]`.
4. Initialize a counter to 0.
5. Iterate through every score in the array.
6. For each score, check two conditions:

1. The score is greater than or equal to the k-th score.
2. The score is strictly greater than 0.
7. If both conditions are true, increment the counter.
8. Print the final counter.

The second condition is necessary because participants with score 0 never advance, even if the k-th participant also scored 0.

### Why it works

The k-th participant establishes the minimum score needed to qualify. Any participant with a smaller score cannot advance. Any participant with the same score or a larger score does qualify, provided their score is positive.

The algorithm checks exactly these two rules for every participant. Since every qualifying participant is counted once and every non-qualifying participant is ignored, the final count is correct.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, k = map(int, input().split())
scores = list(map(int, input().split()))

threshold = scores[k - 1]

answer = 0

for score in scores:
    if score >= threshold and score > 0:
        answer += 1

print(answer)
```

The program begins by reading the number of participants and the qualifying position. The scores are stored in a list.

The variable `threshold` stores the score of the k-th participant. This is the minimum score required for advancement.

The loop processes each participant independently. The condition:

```
score >= threshold and score > 0
```

matches the contest rules exactly.

The first part handles ties correctly. If several participants share the same score as the k-th participant, all of them are counted.

The second part prevents zero-score participants from advancing. This is the detail most likely to cause mistakes.

The implementation uses `k - 1` because Python lists are indexed from 0 while contest positions start from 1.

## Worked Examples

### Example 1

Input:

```
8 5
10 9 8 7 7 7 5 5
```

The k-th participant is in position 5 with score 7.

| Index | Score | Threshold | Positive? | Qualifies? | Count |
| --- | --- | --- | --- | --- | --- |
| 1 | 10 | 7 | Yes | Yes | 1 |
| 2 | 9 | 7 | Yes | Yes | 2 |
| 3 | 8 | 7 | Yes | Yes | 3 |
| 4 | 7 | 7 | Yes | Yes | 4 |
| 5 | 7 | 7 | Yes | Yes | 5 |
| 6 | 7 | 7 | Yes | Yes | 6 |
| 7 | 5 | 7 | Yes | No | 6 |
| 8 | 5 | 7 | Yes | No | 6 |

Final answer:

```
6
```

This example demonstrates why ties matter. Even though k is 5, the 6th participant also advances because their score matches the threshold.

### Example 2

Input:

```
4 2
0 0 0 0
```

The k-th participant has score 0.

| Index | Score | Threshold | Positive? | Qualifies? | Count |
| --- | --- | --- | --- | --- | --- |
| 1 | 0 | 0 | No | No | 0 |
| 2 | 0 | 0 | No | No | 0 |
| 3 | 0 | 0 | No | No | 0 |
| 4 | 0 | 0 | No | No | 0 |

Final answer:

```
0
```

This trace highlights the importance of the positive-score requirement. Matching the threshold alone is not enough.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | We scan the scores array once |
| Space | O(1) | Only a few extra variables are used |

With at most 50 participants, the running time is tiny. The memory usage is also negligible. The solution easily fits within the contest limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def solve():
    input = sys.stdin.readline

    n, k = map(int, input().split())
    scores = list(map(int, input().split()))

    threshold = scores[k - 1]

    ans = 0

    for score in scores:
        if score >= threshold and score > 0:
            ans += 1

    print(ans)

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
assert run("8 5\n10 9 8 7 7 7 5 5\n") == "6\n", "sample 1"

# custom cases
assert run("1 1\n0\n") == "0\n", "minimum size with zero"
assert run("1 1\n100\n") == "1\n", "minimum size with positive score"
assert run("5 3\n10 5 0 0 0\n") == "2\n", "zero threshold handling"
assert run("6 4\n5 5 5 5 5 5\n") == "6\n", "all equal values"
assert run("5 5\n9 7 5 3 1\n") == "5\n", "k equals n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 / 0` | `0` | Single participant with zero score |
| `1 1 / 100` | `1` | Single participant qualifies |
| `5 3 / 10 5 0 0 0` | `2` | Zero-score participants must not advance |
| `6 4 / 5 5 5 5 5 5` | `6` | All tied participants qualify |
| `5 5 / 9 7 5 3 1` | `5` | Handling when k is the last participant |

## Edge Cases

Consider the case where the k-th participant has score 0.

Input:

```
5 3
10 5 0 0 0
```

The threshold becomes 0 because the participant in 3rd place scored 0.

The algorithm checks every participant:

```
10 >= 0 and 10 > 0  -> counted
5 >= 0 and 5 > 0    -> counted
0 >= 0 and 0 > 0    -> not counted
```

The final answer is 2. The extra `score > 0` condition prevents incorrect counting.

Now consider ties around the cutoff.

Input:

```
8 5
10 9 8 7 7 7 5 5
```

The threshold is 7. The algorithm counts every participant whose score is at least 7.

That includes the participant in 6th place because:

```
7 >= 7 and 7 > 0
```

is true.

The final answer becomes 6, which correctly handles tied scores.

Finally, examine the smallest possible input.

Input:

```
1 1
0
```

The threshold is 0. The only participant fails the positive-score condition, so the counter never increases. The output is 0, which matches the rules exactly.

---
title: "CF 1178A - Prime Minister"
description: "There are several political parties, and the first party belongs to Alice. She wants to form a coalition that always contains her own party and may contain some additional parties. The coalition must control more than half of all seats in parliament."
date: "2026-06-12T01:37:49+07:00"
tags: ["codeforces", "competitive-programming", "greedy"]
categories: ["algorithms"]
codeforces_contest: 1178
codeforces_index: "A"
codeforces_contest_name: "Codeforces Global Round 4"
rating: 800
weight: 1178
solve_time_s: 106
verified: true
draft: false
---

[CF 1178A - Prime Minister](https://codeforces.com/problemset/problem/1178/A)

**Rating:** 800  
**Tags:** greedy  
**Solve time:** 1m 46s  
**Verified:** yes  

## Solution
## Problem Understanding

There are several political parties, and the first party belongs to Alice. She wants to form a coalition that always contains her own party and may contain some additional parties. The coalition must control more than half of all seats in parliament. At the same time, every invited party must be small enough that Alice's party has at least twice as many seats as that party.

The input gives the number of parties and the number of seats won by each party. The task is to output any set of party indices that forms a valid coalition. If no such coalition exists, we must print `0`.

The limits are tiny. There are at most 100 parties, and every seat count is at most 100. Even exponential search over all subsets would technically be possible because $2^{100}$ is astronomically large and far beyond what a computer can enumerate. Since only 100 elements exist, linear or quadratic algorithms are trivial to fit inside the one second limit.

A subtle point is that adding a party can never hurt the majority condition, but adding a party that violates the "twice as many seats" rule immediately makes the coalition invalid.

Consider

```
3
10 6 5
```

Party 2 cannot be invited because Alice has only 10 seats, which is not at least twice 6. Party 3 can be invited because 10 ≥ 2×5. The coalition becomes {1,3} with 15 seats out of 21, which is a majority. A careless implementation that simply keeps adding parties until a majority is reached would incorrectly include party 2.

Another edge case appears when Alice already controls a majority.

```
3
10 1 1
```

The answer is just party 1. A solution that assumes at least one ally is necessary would produce the wrong result.

A third case occurs when every other party is too large.

```
3
5 4 4
```

Neither party can join because 5 < 2×4. Alice alone has only 5 of 13 seats, so no coalition exists. The correct output is `0`.

## Approaches

The brute force approach is to examine every subset of parties, force party 1 to be present, and check whether the coalition satisfies both conditions. This is correct because every possible coalition is tested. The problem is the number of subsets. With 100 parties there are roughly $2^{99}$ possible choices, which is completely infeasible.

The key observation is that the restriction on coalition partners depends only on Alice's seat count. Whether another party can join has nothing to do with the rest of the coalition. If party $i$ satisfies

$$a_1 \ge 2a_i,$$

then including it only increases the total number of coalition seats and never violates any condition. Since Alice does not need to minimize the number of parties, there is no reason to reject any eligible party.

Because of this, the problem becomes very simple. Gather every party whose size is at most half of Alice's size, add their seats together, and check whether the resulting coalition controls more than half of all seats. If yes, output those indices. Otherwise no solution exists.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n · n) | O(n) | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the seat counts and compute the total number of seats in parliament.
2. Start the coalition with party 1 because Alice must always be included.
3. Iterate through parties 2 through n.
4. If Alice has at least twice as many seats as the current party, include that party in the coalition and add its seats to the coalition total.

The condition depends only on Alice's seat count, so every eligible party can safely be accepted.
5. After processing all parties, compare the coalition's seat count with half of the total seats.
6. If the coalition has strictly more than half of all seats, output the number of selected parties and their indices.
7. Otherwise print `0`.

### Why it works

A party that satisfies the size restriction can always be added without breaking any requirement. Since adding seats only helps achieve a majority, the best possible coalition under the restriction is obtained by taking every eligible party. If even this largest valid coalition fails to obtain a majority, no smaller valid coalition can succeed. Hence the algorithm always produces a correct answer.

## Python Solution

```python
import sys
input = sys.stdin.readline

# solution
n = int(input())
a = list(map(int, input().split()))

total = sum(a)

coalition = [1]
coalition_sum = a[0]

for i in range(1, n):
    if a[0] >= 2 * a[i]:
        coalition.append(i + 1)
        coalition_sum += a[i]

if coalition_sum * 2 > total:
    print(len(coalition))
    print(*coalition)
else:
    print(0)
```

The variable `total` stores the total number of seats in parliament. The list `coalition` initially contains only party 1, and `coalition_sum` starts with Alice's seat count.

The loop examines every other party. When the condition `a[0] >= 2 * a[i]` holds, the party can safely join and its index is stored using one based numbering.

The majority test uses

```
coalition_sum * 2 > total
```

instead of floating point division. This avoids precision issues and correctly implements the requirement of a strict majority.

The indices stored in `coalition` are already one based, so there is no off by one problem when printing.

## Worked Examples

Consider the sample

```
3
100 50 50
```

| Party | Seats | Eligible? | Coalition Indices | Coalition Seats |
| --- | --- | --- | --- | --- |
| 1 | 100 | Always | [1] | 100 |
| 2 | 50 | Yes | [1,2] | 150 |
| 3 | 50 | Yes | [1,2,3] | 200 |

Total seats = 200.

Since 200 × 2 > 200, the coalition has a strict majority.

This example shows that taking every eligible party is harmless. Any subset containing party 1 and at least one other party would also work.

Now consider

```
3
5 4 4
```

| Party | Seats | Eligible? | Coalition Indices | Coalition Seats |
| --- | --- | --- | --- | --- |
| 1 | 5 | Always | [1] | 5 |
| 2 | 4 | No | [1] | 5 |
| 3 | 4 | No | [1] | 5 |

Total seats = 13.

Since 5 × 2 = 10 ≤ 13, the coalition does not have a majority, so the answer is `0`.

This example demonstrates that if the largest valid coalition fails, no solution exists.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each party is processed once |
| Space | O(n) | The answer list may contain all parties |

With at most 100 parties, linear time is tiny. The algorithm easily satisfies the one second time limit and uses negligible memory.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    n = int(input())
    a = list(map(int, input().split()))

    total = sum(a)
    coalition = [1]
    coalition_sum = a[0]

    for i in range(1, n):
        if a[0] >= 2 * a[i]:
            coalition.append(i + 1)
            coalition_sum += a[i]

    out = []
    if coalition_sum * 2 > total:
        out.append(str(len(coalition)))
        out.append(" ".join(map(str, coalition)))
    else:
        out.append("0")

    return "\n".join(out)

# provided sample
assert run("3\n100 50 50\n") == "3\n1 2 3"

# minimum size, no solution
assert run("2\n1 1\n") == "0"

# Alice already has majority
assert run("3\n10 1 1\n") == "3\n1 2 3"

# all equal values
assert run("4\n5 5 5 5\n") == "0"

# boundary case with equality
assert run("3\n10 5 5\n") == "3\n1 2 3"

# all parties eligible
assert run("5\n20 1 2 3 4\n") == "5\n1 2 3 4 5"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2 / 1 1 | 0 | Minimum size without majority |
| 3 / 10 1 1 | 1 2 3 | Alice already controls parliament |
| 4 / 5 5 5 5 | 0 | Equal values violate the ratio condition |
| 3 / 10 5 5 | 1 2 3 | Equality in the condition is allowed |
| 5 / 20 1 2 3 4 | 1 2 3 4 5 | Every party can join |

## Edge Cases

Consider

```
3
10 6 5
```

The algorithm starts with coalition `{1}`. Party 2 is rejected because `10 < 12`. Party 3 is accepted because `10 ≥ 10`. The coalition has 15 seats out of 21, which is a majority, so the output contains parties 1 and 3. This handles the situation where some parties are too large but others are acceptable.

Consider

```
3
10 1 1
```

The coalition begins with 10 seats. Both remaining parties satisfy the condition and are added. The coalition ends with all 12 seats. Even if no parties were added, Alice alone already had a majority. Starting with party 1 guarantees this case works correctly.

Consider

```
3
5 4 4
```

Neither extra party satisfies the condition because `5 < 8`. The coalition remains `{1}` with 5 seats. Since 5 is not more than half of 13, the algorithm prints `0`. Because every valid coalition is a subset of `{1}`, no solution exists.

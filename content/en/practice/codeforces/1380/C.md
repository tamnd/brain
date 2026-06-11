---
title: "CF 1380C - Create The Teams"
description: "We have a group of programmers, each with a skill value. We want to form as many teams as possible. A team is valid if: $$(text{team size}) times (text{minimum skill in the team}) ge x$$ Every programmer can belong to at most one team, and some programmers may remain unused."
date: "2026-06-11T10:55:31+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "dp", "greedy", "implementation", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1380
codeforces_index: "C"
codeforces_contest_name: "Educational Codeforces Round 91 (Rated for Div. 2)"
rating: 1400
weight: 1380
solve_time_s: 91
verified: true
draft: false
---

[CF 1380C - Create The Teams](https://codeforces.com/problemset/problem/1380/C)

**Rating:** 1400  
**Tags:** brute force, dp, greedy, implementation, sortings  
**Solve time:** 1m 31s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a group of programmers, each with a skill value. We want to form as many teams as possible. A team is valid if:

$$(\text{team size}) \times (\text{minimum skill in the team}) \ge x$$

Every programmer can belong to at most one team, and some programmers may remain unused.

The task is to determine the maximum number of valid teams that can be created.

The largest test case contains up to $10^5$ programmers, and the sum of all $n$ values across test cases is also at most $10^5$. With this input size, any algorithm that repeatedly tries different partitions of programmers is impossible. Even an $O(n^2)$ solution would require around $10^{10}$ operations in the worst case, which is far beyond the limit. We need something around $O(n \log n)$ or better.

The tricky part is that the team's quality depends only on its weakest member. Adding stronger programmers does not improve the minimum skill, but adding more programmers increases the team size. A naive grouping strategy can easily waste strong programmers and reduce the final answer.

Consider this example:

```
n = 4, x = 10
skills = [10, 10, 10, 10]
```

The correct answer is 4. Each programmer alone forms a valid team because $1 \times 10 = 10$. A careless approach that combines programmers into larger groups would produce fewer teams.

Another important case is:

```
n = 5, x = 10
skills = [5, 5, 5, 5, 5]
```

The correct answer is 2. Each valid team needs at least two programmers because $2 \times 5 = 10$. We can create two teams of size 2 and leave one programmer unused. An implementation that insists on using everyone would incorrectly return 1.

A third edge case is when no team can be formed:

```
n = 4, x = 11
skills = [1, 3, 3, 7]
```

Even using all four programmers gives $4 \times 1 = 4$, which is still below 11. The answer is 0.

These examples show that maximizing the number of teams is not the same as maximizing the number of used programmers.

## Approaches

A brute-force solution would try different ways to partition programmers into teams and check which partitions satisfy the condition. Such a method is correct because it examines all possibilities, but the number of partitions grows exponentially. Even for a few dozen programmers it becomes impossible.

To do better, we need to understand how a valid team is characterized.

Suppose the minimum skill inside a team is $m$. Then the team is valid exactly when:

$$(\text{team size}) \times m \ge x$$

If we sort skills in descending order and process programmers from strongest to weakest, then when we reach a programmer with skill $a_i$, every programmer collected so far has skill at least $a_i$. If we decide that $a_i$ will be the weakest member of a team, then $a_i$ becomes the team's minimum skill.

At that moment, we only need to know how many programmers have been gathered for the current team. If:

$$(\text{current size}) \times a_i \ge x$$

then a valid team can be completed immediately.

This observation leads to a greedy strategy. Sort skills from largest to smallest. Build a team by accumulating programmers. Whenever the current group becomes valid, finalize it immediately and start building the next team.

Why is it safe to close the team as soon as it becomes valid?

Because every additional programmer consumed by this team could otherwise help form another team later. Once a group is already valid, making it larger never increases the number of teams. The smallest valid team is always the best choice.

This transforms the problem into a simple sorting and scanning process.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | Exponential | Too slow |
| Optimal Greedy + Sorting | $O(n \log n)$ | $O(1)$ auxiliary (excluding sort) | Accepted |

## Algorithm Walkthrough

1. Sort all skills in descending order.
2. Initialize a counter `current_size = 0`.
3. Initialize `teams = 0`.
4. Process the sorted skills from left to right.
5. For each skill value `s`, add that programmer to the current unfinished team by increasing `current_size`.
6. Treat `s` as the minimum skill of the current group. Since we are processing in descending order, every previously collected programmer has skill at least `s`.
7. Check whether:

$$current\_size \times s \ge x$$

If this condition holds, the current group already forms a valid team.
8. Increase `teams` by one.
9. Reset `current_size` to zero and begin constructing the next team.
10. After all programmers are processed, output `teams`.

### Why it works

The key invariant is that while scanning the sorted array, the current skill value is always the minimum skill among all programmers currently gathered for the unfinished team.

Whenever the condition `current_size * skill >= x` becomes true, we have enough programmers to form a valid team whose minimum skill is exactly `skill`. Closing the team immediately uses the smallest possible number of programmers for that team.

Any solution that keeps adding programmers after the team is already valid only consumes resources that could potentially help create additional teams later. Since larger teams never increase the team count, greedily finalizing every valid team cannot reduce the optimal answer.

Thus every team formed by the algorithm is valid, and every valid team uses the minimum number of available programmers, which maximizes the total number of teams.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())

    answers = []

    for _ in range(t):
        n, x = map(int, input().split())
        skills = list(map(int, input().split()))

        skills.sort(reverse=True)

        teams = 0
        current_size = 0

        for s in skills:
            current_size += 1

            if current_size * s >= x:
                teams += 1
                current_size = 0

        answers.append(str(teams))

    sys.stdout.write("\n".join(answers))

if __name__ == "__main__":
    solve()
```

The first step sorts the skills in descending order. This guarantees that whenever we are examining a skill value `s`, every programmer already placed into the current unfinished group has skill at least `s`. That means `s` is exactly the minimum skill of that potential team.

`current_size` stores how many programmers have been collected for the current team candidate. After adding a programmer, we test whether the team condition is satisfied.

When `current_size * s >= x`, a valid team has been formed. The greedy choice is to finalize it immediately and reset `current_size` to zero. This is the critical implementation detail. Forgetting to reset would incorrectly merge multiple teams together.

All arithmetic fits comfortably inside Python integers. The largest possible product is:

$$10^5 \times 10^9 = 10^{14}$$

which is well within Python's range.

## Worked Examples

### Sample 1

Input:

```
n = 5, x = 10
skills = [7, 11, 2, 9, 5]
```

After sorting:

```
[11, 9, 7, 5, 2]
```

| Skill s | current_size before check | current_size × s | Team formed? | Teams |
| --- | --- | --- | --- | --- |
| 11 | 1 | 11 | Yes | 1 |
| 9 | 1 | 9 | No | 1 |
| 7 | 2 | 14 | Yes | 2 |
| 5 | 1 | 5 | No | 2 |
| 2 | 2 | 4 | No | 2 |

Final answer:

```
2
```

The first programmer alone forms a team. The next two programmers form another valid team. The remaining programmers are insufficient to create a third team.

### Sample 2

Input:

```
n = 4, x = 8
skills = [2, 4, 2, 3]
```

After sorting:

```
[4, 3, 2, 2]
```

| Skill s | current_size before check | current_size × s | Team formed? | Teams |
| --- | --- | --- | --- | --- |
| 4 | 1 | 4 | No | 0 |
| 3 | 2 | 6 | No | 0 |
| 2 | 3 | 6 | No | 0 |
| 2 | 4 | 8 | Yes | 1 |

Final answer:

```
1
```

This example shows that several strong programmers may need to be combined before the requirement is reached.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n \log n)$ | Sorting dominates the running time |
| Space | $O(1)$ auxiliary | Only a few variables are used besides the sorted array |

The total number of programmers across all test cases is at most $10^5$. Sorting that many values requires roughly $10^5 \log_2(10^5)$ operations, which easily fits within the time limit. Memory usage is also comfortably below the limit.

## Test Cases

```python
# helper: run solution on input string, return output string

import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    t = int(input())
    ans = []

    for _ in range(t):
        n, x = map(int, input().split())
        a = list(map(int, input().split()))

        a.sort(reverse=True)

        teams = 0
        cur = 0

        for s in a:
            cur += 1
            if cur * s >= x:
                teams += 1
                cur = 0

        ans.append(str(teams))

    return "\n".join(ans)

# provided sample
assert run(
"""3
5 10
7 11 2 9 5
4 8
2 4 2 3
4 11
1 3 3 7
"""
) == "2\n1\n0"

# minimum size
assert run(
"""1
1 1
1
"""
) == "1"

# single programmer cannot form team
assert run(
"""1
1 2
1
"""
) == "0"

# all equal values
assert run(
"""1
5 10
5 5 5 5 5
"""
) == "2"

# every programmer alone forms a team
assert run(
"""1
4 10
10 10 10 10
"""
) == "4"

# boundary style case
assert run(
"""1
6 12
6 6 6 6 6 6
"""
) == "3"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 / 1` | `1` | Smallest valid input |
| `1 2 / 1` | `0` | Smallest impossible case |
| Five programmers with skill 5, `x=10` | `2` | Leftover programmers may remain unused |
| Four programmers with skill 10, `x=10` | `4` | Single-member teams |
| Six programmers with skill 6, `x=12` | `3` | Exact threshold equality |

## Edge Cases

Consider:

```
1
5 10
5 5 5 5 5
```

After sorting, nothing changes. The scan proceeds as:

```
size=1 -> 1*5=5
size=2 -> 2*5=10 -> team
size=1 -> 1*5=5
size=2 -> 2*5=10 -> team
size=1 -> end
```

The answer is 2. One programmer remains unused. The algorithm never tries to force all programmers into teams.

Now consider:

```
1
4 10
10 10 10 10
```

Each step immediately satisfies the condition:

```
1*10 = 10
```

A team is formed after every programmer, producing 4 teams. The greedy strategy naturally discovers that singleton teams are optimal.

Finally, consider:

```
1
4 11
1 3 3 7
```

Sorted order:

```
7 3 3 1
```

The scan produces:

```
1*7 = 7
2*3 = 6
3*3 = 9
4*1 = 4
```

No check ever reaches 11, so no team is formed. The algorithm correctly returns 0, even after using all available programmers.

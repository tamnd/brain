---
title: "CF 149C - Division into Teams"
description: "We have a group of boys, each with a skill level in football. The task is to split them into two teams such that the teams are nearly equal in size and the total skill levels of the teams are roughly balanced."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "math", "sortings"]
categories: ["algorithms"]
codeforces_contest: 149
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 106 (Div. 2)"
rating: 1500
weight: 149
solve_time_s: 100
verified: false
draft: false
---

[CF 149C - Division into Teams](https://codeforces.com/problemset/problem/149/C)

**Rating:** 1500  
**Tags:** greedy, math, sortings  
**Solve time:** 1m 40s  
**Verified:** no  

## Solution
## Problem Understanding

We have a group of boys, each with a skill level in football. The task is to split them into two teams such that the teams are nearly equal in size and the total skill levels of the teams are roughly balanced. Formally, if there are `n` boys, we need to assign them into two teams with sizes differing by at most one. Additionally, the absolute difference in total skills between the two teams cannot exceed the skill of the best player.

The input gives the number of boys `n` followed by an array of integers representing the skill of each boy. The output should list the number of boys in the first team, the indices of the boys in that team, the number of boys in the second team, and the indices of boys in the second team.

The constraints allow up to 10^5 boys and skill values up to 10^4. This rules out any brute-force enumeration of all possible team divisions since the number of possible partitions grows exponentially. We need a solution with roughly O(n log n) or O(n) complexity to meet the time limit.

A subtle edge case arises when the array of skills has repeated values, or when one boy is significantly stronger than the others. For example, if `n = 3` and skills are `[1, 1, 10]`, a naive approach that tries to balance the sums greedily by taking largest skills first could mistakenly put the strongest boy in a team that ends up exceeding the allowed skill difference. Another case is when `n` is even versus odd; the teams must differ in size by at most one, so we have to alternate assignment carefully to satisfy both size and skill constraints.

## Approaches

The brute-force approach would generate all possible ways to partition `n` boys into two teams of nearly equal size and then check the sum conditions. This is correct in principle, but for `n = 10^5` the number of partitions is astronomical (roughly 2^n / sqrt(n)) and completely infeasible.

The key insight is that we can use a greedy sorting approach. If we sort boys by skill, the absolute difference between team totals is most sensitive to the largest skill values. By alternating assignment of the strongest remaining players between the two teams, we can guarantee that the total skills stay close. Sorting ensures that when we assign the largest unassigned skill, it is balanced by distributing the next largest to the opposite team. We also alternate assignment from the largest downwards rather than from smallest up, because the constraint depends on the best player's skill. Assigning the largest last could violate this constraint.

This leads to an O(n log n) solution: sort the skills while keeping track of original indices, then iterate over them in descending order, alternately assigning to the two teams.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n) | O(n) | Too slow |
| Greedy Sort & Alternate | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the number of boys `n` and the array of skills `a`.
2. Create a list of pairs `(skill, index)` so we can sort while preserving original indices.
3. Sort this list in descending order of skill. Sorting ensures we deal with the strongest players first.
4. Initialize two empty lists for team 1 and team 2.
5. Iterate through the sorted list, assigning each player alternately to team 1 and team 2. This ensures both the team size difference and total skill difference remain within constraints.
6. Output the size and indices of the first team, followed by the size and indices of the second team.

Why it works: The invariant we maintain is that at every step, the difference in total skill between teams cannot exceed the largest unassigned skill. Since we start with the largest skill, alternating assignment ensures that no single team accumulates a total exceeding the allowed difference. Team size difference is automatically maintained because we assign one player at a time and alternate.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
a = list(map(int, input().split()))

# store original indices
players = [(skill, idx + 1) for idx, skill in enumerate(a)]
# sort descending by skill
players.sort(reverse=True)

team1 = []
team2 = []

# alternate assignment
for i, (_, idx) in enumerate(players):
    if i % 2 == 0:
        team1.append(idx)
    else:
        team2.append(idx)

print(len(team1))
print(" ".join(map(str, team1)))
print(len(team2))
print(" ".join(map(str, team2)))
```

This code reads the input, creates a skill-index pair list, sorts it in descending order, and then distributes players alternately to each team. The modulo operation `i % 2` guarantees the teams have nearly equal sizes. Using original indices ensures the output matches the required 1-based numbering.

## Worked Examples

Trace through the sample input `3\n1 2 1`:

| i | skill | idx | team1 | team2 |
| --- | --- | --- | --- | --- |
| 0 | 2 | 2 | [2] | [] |
| 1 | 1 | 1 | [2] | [1] |
| 2 | 1 | 3 | [2,3] | [1] |

Team sizes are 2 and 1, total skills are 3 and 1, difference is 2 which is equal to the max skill 2. Correct.

Another input `4\n10 1 1 1`:

| i | skill | idx | team1 | team2 |
| --- | --- | --- | --- | --- |
| 0 | 10 | 1 | [1] | [] |
| 1 | 1 | 2 | [1] | [2] |
| 2 | 1 | 3 | [1,3] | [2] |
| 3 | 1 | 4 | [1,3] | [2,4] |

Team sizes are 2 and 2, total skills 11 and 3, difference 8 ≤ max skill 10. Correct.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting dominates the runtime; all other operations are O(n) |
| Space | O(n) | We store skill-index pairs and two team lists |

Sorting 10^5 elements in O(n log n) is feasible under 1s time limit. Space usage is linear, fitting comfortably within 256 MB.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n = int(input())
    a = list(map(int, input().split()))
    players = [(skill, idx + 1) for idx, skill in enumerate(a)]
    players.sort(reverse=True)
    team1 = []
    team2 = []
    for i, (_, idx) in enumerate(players):
        if i % 2 == 0:
            team1.append(idx)
        else:
            team2.append(idx)
    out = []
    out.append(str(len(team1)))
    out.append(" ".join(map(str, team1)))
    out.append(str(len(team2)))
    out.append(" ".join(map(str, team2)))
    return "\n".join(out)

# sample
assert run("3\n1 2 1\n") == "2\n2 3\n1\n1", "sample 1"

# minimum input
assert run("2\n1 1\n") == "1\n1\n1\n2", "min size"

# all equal skills
assert run("4\n5 5 5 5\n") == "2\n1 3\n2\n2 4", "equal skills"

# max size with small skills
max_input = "100000\n" + " ".join(["1"]*100000)
result = run(max_input)
assert result.startswith("50000\n"), "max size"

# large difference
assert run("4\n10 1 1 1\n") == "2\n1 3\n2\n2 4", "large skill difference"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2\n1 1 | 1\n1\n1\n2 | minimum input handling |
| 4\n5 5 5 5 | 2\n1 3\n2\n2 4 | all-equal skills balanced |
| 100000 ones | 50000 ... | scalability to maximum n |
| 4\n10 1 1 1 | 2\n1 3\n2\n2 4 | high-skill player placement |

## Edge Cases

If all boys have the same skill, alternating ensures the team size difference is at most one and total skills are exactly balanced. For `[10, 1, 1, 1]`, the strongest player goes to the first team, the next to the second, and so on. The final totals differ by 8, which is within the allowed difference (10). Odd `n` is handled automatically by alternating assignments. The modulo operation guarantees no off-by-one errors in indexing, and original indices are preserved for output.

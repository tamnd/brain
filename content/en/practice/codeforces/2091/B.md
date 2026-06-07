---
title: "CF 2091B - Team Training"
description: "We are given a group of students, each with a fixed skill value, and we must split them into teams so that every student belongs to exactly one team. For any team, its strength is defined as the number of students in the team multiplied by the smallest skill inside that team."
date: "2026-06-08T05:45:28+07:00"
tags: ["codeforces", "competitive-programming", "dp", "greedy", "sortings"]
categories: ["algorithms"]
codeforces_contest: 2091
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 1013 (Div. 3)"
rating: 800
weight: 2091
solve_time_s: 72
verified: true
draft: false
---

[CF 2091B - Team Training](https://codeforces.com/problemset/problem/2091/B)

**Rating:** 800  
**Tags:** dp, greedy, sortings  
**Solve time:** 1m 12s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a group of students, each with a fixed skill value, and we must split them into teams so that every student belongs to exactly one team. For any team, its strength is defined as the number of students in the team multiplied by the smallest skill inside that team. A team is considered valid only if this computed strength reaches at least a given threshold value.

The task is not to maximize total strength or balance teams, but simply to maximize how many teams satisfy the strength condition after partitioning everyone exactly once.

The key tension is that grouping more students increases the multiplier, but it can decrease the minimum skill inside the team. The structure of the grouping fully determines whether a team qualifies.

From constraints, the total number of students across all test cases is up to 200,000. This immediately rules out any solution that tries to consider all partitions or even all subsets, since those grow exponentially. Even O(n^2) per test case is unsafe in worst-case aggregation. We should expect a sorting-based linear or near-linear greedy approach.

A subtle edge case arises when a student has extremely high skill but is left alone. For example, if x is large and all skills are small except one large value, a naive greedy might isolate strong students incorrectly or merge too aggressively. Another failure case is when grouping is done without considering that adding a weak student can reduce the minimum and break an otherwise valid team.

## Approaches

A brute-force idea would try every possible way to partition the students into teams and check how many teams satisfy the condition. Even restricting ourselves to building teams greedily in different orders still leaves a combinatorial explosion in grouping choices. With n students, the number of partitions is exponential, and even deciding locally optimal merges is insufficient because early decisions affect later feasibility.

The key observation comes from rewriting the condition for a team. If a team has minimum skill m and size k, it is strong when k · m ≥ x, or equivalently k ≥ ceil(x / m). This means that once we fix the weakest member of a team, we know the minimum number of people required to support them.

This suggests sorting students by skill and trying to “assign support” to weaker students using stronger ones. A useful way to think about it is processing students from strongest to weakest, accumulating a candidate team. Once the accumulated size is enough to support the current minimum, we can finalize a team immediately. Since we are processing in descending order, the current student is always the minimum of the current group.

This greedy works because every time we decide to form a team, using the strongest available students first ensures we waste no potential strength on earlier weaker groupings.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | Exponential | Too slow |
| Greedy sorting | O(n log n) | O(1) extra | Accepted |

## Algorithm Walkthrough

1. Sort the skill array in descending order. This ensures that when we build a team progressively, the last added element is always the weakest in the current segment. This makes it easy to evaluate strength when we decide to close a team.
2. Maintain a counter `cnt` representing how many students are currently in the forming team. We also maintain how many valid teams we have already formed.
3. Iterate through the sorted skills. For each student, increment `cnt` because we are tentatively adding them to the current team.
4. After each addition, check whether `cnt * current_skill ≥ x`. Since `current_skill` is the smallest in the current group (because of sorting), this condition checks whether the current group can already form a valid team.
5. If the condition holds, we finalize this team: increment the answer and reset `cnt` to zero, starting a new team from the next student.

### Why it works

The algorithm maintains the invariant that the current group is always composed of the strongest remaining students in descending order, so the last added element is always the minimum skill in that group. Whenever we decide to form a team, we do so at the earliest possible point where the group becomes valid. Delaying would only include weaker elements in future teams or reduce the number of possible valid groups. Because we always finalize as soon as the condition is satisfied, we never miss a potential team formation, and we never waste strong students by pairing them in unnecessarily large groups.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n, x = map(int, input().split())
        a = list(map(int, input().split()))
        
        a.sort(reverse=True)
        
        cnt = 0
        ans = 0
        
        for v in a:
            cnt += 1
            if cnt * v >= x:
                ans += 1
                cnt = 0
        
        print(ans)

if __name__ == "__main__":
    solve()
```

The solution begins by sorting skills in descending order so that when we build a group sequentially, the current element is always the weakest in that partial group. The counter `cnt` tracks the size of the ongoing group. Each time we extend the group, we check if multiplying its size by the weakest element satisfies the threshold. If it does, we immediately close the group and reset.

A common mistake is trying to maintain multiple partially formed groups or attempting to greedily assign students into bins without sorting. The descending order is what guarantees that each check correctly represents the true minimum of the current group.

## Worked Examples

We trace the algorithm on two inputs.

First input:

```
n = 6, x = 4
a = [4, 5, 3, 3, 2, 6]
```

Sorted descending:

```
[6, 5, 4, 3, 3, 2]
```

| step | value | cnt | cnt * value | action | teams |
| --- | --- | --- | --- | --- | --- |
| 1 | 6 | 1 | 6 | form team | 1 |
| 2 | 5 | 1 | 5 | form team | 2 |
| 3 | 4 | 1 | 4 | form team | 3 |
| 4 | 3 | 1 | 3 | no | 3 |
| 5 | 3 | 2 | 6 | form team | 4 |
| 6 | 2 | 1 | 2 | no | 4 |

This shows how strong elements form single-person teams quickly, while weaker elements may need grouping.

Second input:

```
n = 5, x = 3
a = [5, 3, 2, 3, 2]
```

Sorted:

```
[5, 3, 3, 2, 2]
```

| step | value | cnt | cnt * value | action | teams |
| --- | --- | --- | --- | --- | --- |
| 1 | 5 | 1 | 5 | form team | 1 |
| 2 | 3 | 1 | 3 | form team | 2 |
| 3 | 3 | 1 | 3 | form team | 3 |
| 4 | 2 | 1 | 2 | no | 3 |
| 5 | 2 | 2 | 4 | form team | 4 |

The trace shows how weaker elements can still complete valid teams when accumulated.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | sorting dominates each test case |
| Space | O(1) extra | in-place sorting and constant counters |

The total n across test cases is at most 200,000, so an O(n log n) approach is efficient enough within 2 seconds. The algorithm only performs sorting and a single linear scan per test case.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline
    
    t = int(input())
    out = []
    for _ in range(t):
        n, x = map(int, input().split())
        a = list(map(int, input().split()))
        
        a.sort(reverse=True)
        cnt = 0
        ans = 0
        
        for v in a:
            cnt += 1
            if cnt * v >= x:
                ans += 1
                cnt = 0
        
        out.append(str(ans))
    return "\n".join(out)

# provided samples
assert run("""5
6 4
4 5 3 3 2 6
4 10
4 2 1 3
5 3
5 3 2 3 2
3 6
9 1 7
6 10
6 1 3 6 3 2
""") == """4
0
4
2
1"""

# all equal values
assert run("""1
5 10
2 2 2 2 2
""") == "1"

# single strong element
assert run("""1
3 5
1 1 10
""") == "1"

# no valid teams
assert run("""1
4 100
1 2 3 4
""") == "0"

# minimum size
assert run("""1
1 1
1
""") == "1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all equal values | 1 | grouping stability |
| single strong element | 1 | correct handling of isolated large values |
| no valid teams | 0 | failure case where nothing satisfies threshold |
| minimum size | 1 | base edge case |

## Edge Cases

One important edge case is when all values are equal but just below threshold when multiplied by full size. For example:

```
n = 5, x = 10, a = [2,2,2,2,2]
```

After sorting, we accumulate counts: 1 gives 2, 2 gives 4, 3 gives 6, 4 gives 8, 5 gives 10, so one full team is formed. The algorithm correctly delays formation until the group is large enough.

Another edge case is when a single large value dominates:

```
n = 3, x = 5, a = [10,1,1]
```

We form a team immediately with 10, since 1·10 ≥ 5 is already satisfied at size 1. The remaining weak elements may fail to form a second team, which is also correct.

A third case is when greedy temptation suggests pairing weak elements first. Sorting prevents this mistake because weak elements always appear later, ensuring they only contribute when necessary rather than consuming strong elements prematurely.

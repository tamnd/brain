---
title: "CF 899A - Splitting in Teams"
description: "We are given several groups of students. Each group has either one student or two students, and these groups are indivisible. The coach wants to form as many teams as possible, where each team must contain exactly three students."
date: "2026-06-17T03:27:07+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "greedy", "math"]
categories: ["algorithms"]
codeforces_contest: 899
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 452 (Div. 2)"
rating: 800
weight: 899
solve_time_s: 64
verified: true
draft: false
---

[CF 899A - Splitting in Teams](https://codeforces.com/problemset/problem/899/A)

**Rating:** 800  
**Tags:** constructive algorithms, greedy, math  
**Solve time:** 1m 4s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given several groups of students. Each group has either one student or two students, and these groups are indivisible. The coach wants to form as many teams as possible, where each team must contain exactly three students.

A group of size one contributes a single flexible student. A group of size two contributes a fixed pair that must either both be used in the same team or not used at all. We cannot split a pair across different teams or combine only one member of a pair with someone else.

The task is to choose some groups and assign their students into disjoint teams of size three, maximizing the number of complete teams.

The constraint n can be as large as 200,000, which rules out any approach that tries all combinations of groups or builds teams incrementally with backtracking. Any solution must be linear or near-linear in the number of groups.

A subtle failure case appears when greedy intuition is applied incorrectly. For example, if we always try to form a team immediately whenever we see enough single students, we might miss the opportunity to combine a pair with two singles later.

Input like:

```
5
1 1 1 2 2
```

A naive greedy might form one team from three ones and then get stuck with two pairs that cannot form a full team, giving 1. However, optimal reasoning yields 2 teams by using both pairs with single students appropriately.

This shows the problem is not about local grouping, but about counting resources globally.

## Approaches

A brute-force interpretation would try to pick subsets of groups and assign them into teams of three while respecting the constraint that each selected group of size two is either fully included or excluded. This becomes a partitioning problem over weighted items where each item is either 1 or 2, and we try all combinations of picking or skipping each group.

For each subset of chosen groups, we would attempt to pack their total size into groups of three, possibly using backtracking or dynamic assignment. The number of subsets alone is 2^n, and even checking feasibility per subset would cost at least linear time, making this completely infeasible at n = 200,000.

The key observation is that only counts matter, not identities of groups. Let x be the number of single groups and y be the number of double groups. We are effectively trying to partition a multiset consisting of x ones and y twos into triples, with the restriction that twos cannot be split.

The structure simplifies because any valid team is one of only two useful types: three singles, or one double plus one single. A team of three twos is impossible since it would require splitting pairs. This reduces the problem to distributing singles around fixed pairs.

The greedy strategy emerges from the fact that pairs are expensive resources: they consume two people at once and leave less flexibility. The optimal construction always uses pairs by matching them with singles whenever possible, because leaving a pair unused wastes two potential contributions that are hard to reuse elsewhere.

We therefore prioritize forming teams that use one pair and one single, until either runs out. After that, remaining singles form teams of three.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n · n) | O(n) | Too slow |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

We compress the input into two counts: the number of single-person groups and the number of two-person groups.

1. Count how many groups of size 1 exist and how many groups of size 2 exist. This reduces the problem to two integers instead of an array.
2. First, try to use each group of size 2 together with a group of size 1 to form a full team of three people. Each such pairing consumes one of each type and produces exactly one team.
3. The number of such teams is limited by the smaller of the two counts, since each team needs both a pair and a single.
4. After this step, update the remaining counts by subtracting the used singles and pairs.
5. Now only singles remain relevant. Each team requires exactly three singles, so divide the remaining number of singles by three to get additional teams.
6. Sum both contributions to obtain the final answer.

The reasoning behind prioritizing pair-single teams is that a pair cannot contribute to any other configuration except by being paired with exactly one single or being left unused. Since leaving a pair unused is strictly worse than combining it with a single whenever possible, this matching step is always safe.

Why it works: every valid solution can be transformed into one where all possible pair-plus-single teams are formed first without decreasing the total number of teams. Any deviation either wastes a pair or uses more singles than necessary in configurations that could be rearranged into the same or better number of triples. This establishes that greedy pairing followed by packing remaining singles is optimal.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
a = list(map(int, input().split()))

ones = 0
twos = 0

for x in a:
    if x == 1:
        ones += 1
    else:
        twos += 1

# pair each 2-group with a 1-group if possible
pair_teams = min(ones, twos)
ones -= pair_teams
twos -= pair_teams

# remaining ones form teams of 3
single_teams = ones // 3

print(pair_teams + single_teams)
```

The code starts by compressing the input into two counters, which is the central simplification. This avoids tracking individual groups and focuses only on available resources.

The first phase computes how many (2,1) combinations can be formed. Using `min(ones, twos)` ensures we never overuse either resource. After subtracting, we correctly reflect what remains available for further grouping.

Finally, the remaining ones are grouped greedily into triples, since there is no other structure left that could involve them.

A common mistake here is attempting to form triples of ones before pairing with twos. That leads to stranded twos that cannot participate in any team, reducing the total count.

## Worked Examples

### Example 1

Input:

```
4
1 1 2 1
```

Counts:

ones = 3, twos = 1

| Step | ones | twos | pair_teams | remaining ones | remaining twos |
| --- | --- | --- | --- | --- | --- |
| start | 3 | 1 | 0 | - | - |
| pair formation | 2 | 0 | 1 | 2 | 0 |
| triple formation | 2 | 0 | 1 | 0 | 0 |

Final result is 1 team.

This shows that even though three singles exist initially, one of them is better used to unlock the pair, since the pair alone cannot form a team.

### Example 2

Input:

```
6
1 1 1 1 2 2
```

Counts:

ones = 4, twos = 2

| Step | ones | twos | pair_teams | remaining ones | remaining twos |
| --- | --- | --- | --- | --- | --- |
| start | 4 | 2 | 0 | - | - |
| pair formation | 2 | 0 | 2 | 2 | 0 |
| triple formation | 2 | 0 | 2 | 0 | 0 |

Final result is 2 teams.

This demonstrates that all pairs are best utilized immediately with singles, maximizing utilization before forming remaining triples.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Single pass to count groups, constant-time arithmetic afterward |
| Space | O(1) | Only counters for ones and twos are stored |

The solution easily fits within constraints since even for 200,000 groups, we perform only a linear scan and constant-time computations.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    n = int(input())
    a = list(map(int, input().split()))

    ones = 0
    twos = 0

    for x in a:
        if x == 1:
            ones += 1
        else:
            twos += 1

    pair_teams = min(ones, twos)
    ones -= pair_teams
    twos -= pair_teams

    single_teams = ones // 3

    return str(pair_teams + single_teams)

# provided sample
assert run("4\n1 1 2 1\n") == "1"

# all ones, no pairs
assert run("3\n1 1 1\n") == "1"

# all twos, cannot form any team
assert run("2\n2 2\n") == "0"

# mixed, but singles insufficient
assert run("5\n2 2 1 1 1\n") == "2"

# large balanced case
assert run("6\n1 1 1 1 2 2\n") == "2"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all ones | 1 | basic triple formation |
| all twos | 0 | pairs alone cannot form teams |
| mixed small | 2 | greedy pairing correctness |
| balanced | 2 | full utilization of pairs |

## Edge Cases

One edge case is when there are no single-person groups at all.

Input:

```
4
2 2 2 2
```

Here ones = 0, twos = 4. The pairing step produces zero teams because no single groups exist. The remaining singles are still zero, so the answer is 0. The algorithm correctly avoids trying to force invalid pair usage.

Another edge case is when singles are abundant but pairs are absent.

Input:

```
6
1 1 1 1 1 1
```

Here ones = 6, twos = 0. The pairing step produces zero teams. The remaining singles form 2 teams via 6 // 3. This confirms the algorithm does not depend on the presence of pairs and gracefully reduces to simple grouping.

A third edge case is when singles and pairs are equal in number, which maximizes interaction between the two categories.

Input:

```
5
1 1 1 2 2
```

ones = 3, twos = 2. Pairing yields 2 teams, leaving one single unused. No further triples can be formed, and the algorithm correctly outputs 2. This demonstrates that leftover singles less than three are naturally discarded without special handling.

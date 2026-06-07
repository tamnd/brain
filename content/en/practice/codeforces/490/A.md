---
title: "CF 490A - Team Olympiad"
description: "We are given a list of children, each identified by a number indicating their skill: programming (1), maths (2), or physical education (3). The task is to form as many teams of three as possible, where each team has exactly one child from each skill."
date: "2026-06-07T17:40:01+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "implementation", "sortings"]
categories: ["algorithms"]
codeforces_contest: 490
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 279 (Div. 2)"
rating: 800
weight: 490
solve_time_s: 117
verified: false
draft: false
---

[CF 490A - Team Olympiad](https://codeforces.com/problemset/problem/490/A)

**Rating:** 800  
**Tags:** greedy, implementation, sortings  
**Solve time:** 1m 57s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a list of children, each identified by a number indicating their skill: programming (1), maths (2), or physical education (3). The task is to form as many teams of three as possible, where each team has exactly one child from each skill. The output should first state the number of teams and then list the indices of the children forming each team. Each child can only appear in one team.

The key constraint is that $n \le 5000$. This is small enough to allow a linear or near-linear scan of the data, and even simple operations over all children multiple times will work. The indices must be preserved according to the original input for output purposes, but we are free to rearrange or store them as needed internally.

A non-obvious edge case occurs when one skill is underrepresented. For example, with input `1 1 2 2 2 3`, we have three programmers, three mathematicians, and one sportsman. The maximum number of teams is clearly 1, because we cannot form more than one team with exactly one child of each skill. A naive approach that tries to just match children sequentially could mistakenly attempt to create two teams, which would fail to satisfy the skill requirements.

## Approaches

A brute-force approach would attempt to try all possible combinations of three children and check if they form a valid team. With up to 5000 children, the number of possible triplets is $\binom{5000}{3}$, roughly 20 billion, which is clearly infeasible. This works in theory because it checks every combination, but it fails when $n$ grows beyond a few dozen.

The key insight is to separate children by skill. Once we have three lists - one for programmers, one for mathematicians, and one for sportsmen - the maximum number of teams is limited by the smallest list, because we cannot form a team without at least one child from each skill. We can then take children from the front of each list and form teams sequentially. This guarantees that every team has distinct skills, and we naturally respect the one-team-per-child constraint.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n³) | O(n) | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Initialize three empty lists: `prog` for programmers, `maths` for mathematicians, and `pe` for sportsmen. These will store the indices of children with each skill.
2. Iterate through the list of children. For each child, append its 1-based index to the appropriate list depending on the skill.
3. Compute the minimum length among the three lists. This number, `w`, is the maximum number of teams that can be formed.
4. For each integer `i` from 0 to `w-1`, output a team consisting of the `i`-th element from `prog`, `maths`, and `pe`. This ensures that each team has exactly one child of each skill, and no child is repeated.
5. Print `w` first, then print each team on a separate line.

Why it works: At every step, we take exactly one child from each skill. By iterating up to the minimum count among the three skill groups, we guarantee that we never exceed the available number of children in any skill. This produces the maximal number of valid teams, and since we track indices directly, output correctness is preserved.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
skills = list(map(int, input().split()))

prog = []
maths = []
pe = []

for idx, s in enumerate(skills, 1):
    if s == 1:
        prog.append(idx)
    elif s == 2:
        maths.append(idx)
    else:
        pe.append(idx)

w = min(len(prog), len(maths), len(pe))
print(w)

for i in range(w):
    print(prog[i], maths[i], pe[i])
```

The solution reads the number of children and their skills. It separates indices into three lists based on skill. It then calculates the maximum number of teams as the minimum of the lengths of the three lists. Finally, it prints `w` and outputs each team by taking one index from each skill list in order. Using 1-based indexing is crucial because the problem requires it.

## Worked Examples

Sample Input 1:

```
7
1 3 1 3 2 1 2
```

| prog | maths | pe | w | Teams formed |
| --- | --- | --- | --- | --- |
| [1,3,6] | [5,7] | [2,4] | min(3,2,2)=2 | (1,5,2), (3,7,4) |

We take two teams, because the smallest skill group (`maths` and `pe`) has 2 children each. The table shows how indices are picked sequentially from each list.

Sample Input 2:

```
4
1 1 2 3
```

| prog | maths | pe | w | Teams formed |
| --- | --- | --- | --- | --- |
| [1,2] | [3] | [4] | min(2,1,1)=1 | (1,3,4) |

Only one team can be formed, limited by the number of mathematicians and sportsmen.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | We iterate through the list of children once to separate indices, then iterate up to `w` (≤ n) to form teams. |
| Space | O(n) | We store indices in three separate lists, each up to n elements in total. |

The solution easily fits within the 1-second time limit for n ≤ 5000 and memory limit of 256 MB.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    # solution
    n = int(input())
    skills = list(map(int, input().split()))
    prog, maths, pe = [], [], []
    for idx, s in enumerate(skills, 1):
        if s == 1:
            prog.append(idx)
        elif s == 2:
            maths.append(idx)
        else:
            pe.append(idx)
    w = min(len(prog), len(maths), len(pe))
    print(w)
    for i in range(w):
        print(prog[i], maths[i], pe[i])
    return output.getvalue().strip()

# provided sample
assert run("7\n1 3 1 3 2 1 2\n") == "2\n1 5 2\n3 7 4", "sample 1"

# custom cases
assert run("4\n1 1 2 3\n") == "1\n1 3 4", "minimum teams"
assert run("6\n1 1 1 2 2 3\n") == "1\n1 4 6", "one team only"
assert run("3\n1 2 3\n") == "1\n1 2 3", "exactly one team"
assert run("5\n1 2 3 1 2\n") == "1\n1 2 3", "extra children in skill groups"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 4\n1 1 2 3 | 1\n1 3 4 | Only one team can be formed |
| 6\n1 1 1 2 2 3 | 1\n1 4 6 | Minimal number determines teams |
| 3\n1 2 3 | 1\n1 2 3 | Single team edge case |
| 5\n1 2 3 1 2 | 1\n1 2 3 | Extra children do not create additional teams |

## Edge Cases

If one skill has no children, for example `3\n1 1 2`, then the lists become `prog=[1,2]`, `maths=[3]`, `pe=[]`. The minimum of the lengths is 0, so no team can be formed. The algorithm correctly prints 0. This handles the edge case without any extra checks because the min operation naturally enforces it.

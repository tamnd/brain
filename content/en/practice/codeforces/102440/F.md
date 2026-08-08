---
title: "CF 102440F - Football championship"
description: "We have friends numbered from (1) to (n), and friend (i) contributes exactly (i) strength to whichever of three teams receives them. Every friend must belong to exactly one team, and the three team sums must be equal."
date: "2026-08-09T01:01:14+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102440
codeforces_index: "F"
codeforces_contest_name: "2018-2019 9th BSUIR Open Programming Championship. Junior"
rating: 0
weight: 102440
solve_time_s: 593
verified: false
draft: false
---

[CF 102440F - Football championship](https://codeforces.com/problemset/problem/102440/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 9m 53s  
**Verified:** no  

## Solution
## Problem Understanding

We have friends numbered from (1) to (n), and friend (i) contributes exactly (i) strength to whichever of three teams receives them. Every friend must belong to exactly one team, and the three team sums must be equal. The task is to print such a partition, or report that none exists.

The total strength is

[
S = 1+2+\dots+n = \frac{n(n+1)}2.
]

If a valid partition exists, every team must have strength

[
T = \frac{S}{3} = \frac{n(n+1)}6.
]

So divisibility of (n(n+1)) by (6) is the first necessary condition. However, it is not sufficient for small (n). For example, (n=2) gives total strength (3), so the target is (1), but only friend (1) can form a team of strength (1). Likewise, (n=3) has target (2), but only the single friend numbered (2) has that strength.

The constraint (n\le 10^6) makes the constructive nature of the problem decisive. We can afford a pass over all (n) players, but anything exponential or quadratic is completely out of range. The official contest version gives this problem a one second limit and 256 MB of memory, so the intended solution must be close to linear in (n).

There are several small boundary cases that a solution based only on divisibility can mishandle. For (n=1), the total strength is (1), so three positive-strength teams are impossible. For (n=2), the total is divisible by three, but the target is (1) and there is only one player of strength (1), so the answer is still `Impossible`. For (n=3), the target is (2), and again only one subset has that sum, namely ({2}). The input (n=4) has total (10), which is not divisible by three, so it is immediately impossible. The first possible value is (n=5), where the teams can be ({5}), ({4,1}), and ({3,2}), all with strength (5).

## Approaches

A direct brute-force solution could assign every player independently to one of the three teams. There are (3^n) assignments. After choosing an assignment, we would calculate the three sums and check whether they are equal, taking (O(n)) work per assignment. The worst-case operation count is therefore on the order of (n3^n). Even for (n=30), this is already far too large, while the actual limit reaches (10^6).

A subset-search approach is only marginally better. We could choose one team as a subset with the required sum and then try to partition the remaining players, but enumerating subsets already costs (2^n). The fact that the player strengths are exactly the consecutive integers (1,2,\dots,n) gives us a much stronger structure than a general subset-sum instance.

The key observation is to look at six consecutive numbers. Consider the block

[
L,L+1,L+2,L+3,L+4,L+5.
]

It can always be split into the three pairs

[
{L+5,L},\qquad
{L+4,L+1},\qquad
{L+3,L+2}.
]

Every pair has sum

[
2L+5.
]

So every block of six consecutive players can be added to an already valid solution without changing the equality between the three team strengths. This means we only need to construct a few small starting configurations. After that, every additional six players are handled identically.

The useful base configurations are particularly small:

[
\begin{aligned}
n=5 &: {5},{4,1},{3,2},\
n=6 &: {6,1},{5,2},{4,3},\
n=8 &: {8,4},{7,5},{6,3,2,1},\
n=9 &: {9,6},{8,7},{5,4,3,2,1}.
\end{aligned}
]

Their team sums are respectively (5), (7), (12), and (15).

These four bases cover every possible residue class that can lead to a solution. If (n\equiv 0\pmod 6), start from (6). If (n\equiv2\pmod6), start from (8). If (n\equiv3\pmod6), start from (9). If (n\equiv5\pmod6), start from (5). The remaining values of (n) have residue (1) or (4), so their total strength is not divisible by three.

There are two exceptional small values, (n=2) and (n=3), where divisibility holds but no partition exists. Thus the complete condition is that (n\ge5) and

[
n\bmod6\in{0,2,3,5}.
]

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(n3^n)) | (O(n)) | Too slow |
| Optimal construction | (O(n)) | (O(n)) | Accepted |

## Algorithm Walkthrough

1. Compute (n\bmod6). If (n<5), the only candidates requiring special attention are (1,2,3,4), and all of them are impossible. If the residue is (1) or (4), the total strength is not divisible by three, so print `Impossible`.
2. Choose a small base according to the residue. For residue (5), use the partition of (1,\dots,5) into ({5}), ({4,1}), and ({3,2}). For residue (0), use (1,\dots,6) with ({6,1}), ({5,2}), and ({4,3}). For residue (2), use (1,\dots,8) with ({8,4}), ({7,5}), and ({6,3,2,1}). For residue (3), use (1,\dots,9) with ({9,6}), ({8,7}), and ({5,4,3,2,1}).
3. Let `left` be the first number not included in the base. Process the remaining players in blocks of six. For a block starting at (L), add (L+5) and (L) to the first team, (L+4) and (L+1) to the second team, and (L+3) and (L+2) to the third team. Each team receives exactly (2L+5) additional strength.
4. Increase (L) by six and continue until all players have been assigned. Because the base size has the same residue modulo six as (n), the remaining number of players is always a multiple of six.
5. Print `Possible` and the three constructed teams. Their sums are equal because the base sums are equal and every added six-player block contributes the same amount to every team.

### Why it works

The invariant is that after processing the base and any number of complete six-player blocks, all three teams have exactly the same total strength and every processed player belongs to exactly one team. The base satisfies this invariant directly. For every later block, the three added pairs have the same sum (2L+5), so adding the block preserves equality. Since the base plus all processed blocks eventually contains every player from (1) through (n), the final teams form a complete valid partition.

For impossibility, when (n\equiv1) or (4\pmod6), (n(n+1)/2) is not divisible by three, so equal team sums cannot exist. The remaining values below five are checked separately, and none admits three equal positive-strength teams.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())

    if n < 5 or n % 6 in (1, 4):
        print("Impossible")
        return

    r = n % 6

    if r == 5:
        teams = [
            [5],
            [4, 1],
            [3, 2],
        ]
        start = 6

    elif r == 0:
        teams = [
            [6, 1],
            [5, 2],
            [4, 3],
        ]
        start = 7

    elif r == 2:
        teams = [
            [8, 4],
            [7, 5],
            [6, 3, 2, 1],
        ]
        start = 9

    else:  # r == 3
        teams = [
            [9, 6],
            [8, 7],
            [5, 4, 3, 2, 1],
        ]
        start = 10

    left = start

    while left <= n:
        teams[0].extend([left + 5, left])
        teams[1].extend([left + 4, left + 1])
        teams[2].extend([left + 3, left + 2])
        left += 6

    out = ["Possible"]

    for team in teams:
        out.append(str(len(team)))
        out.append(" ".join(map(str, team)))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The first condition handles both divisibility failures and the small exceptional values. Checking `n < 5` before the residue is convenient because (n=2) and (n=3) would otherwise pass the divisibility test.

The four base cases are hard-coded because they are the only genuinely special part of the construction. Their sizes are (5,6,8,9), and each corresponding residue guarantees that `n - start + 1` is divisible by six.

The loop processes exactly six new players at a time. The first team receives `left + 5` and `left`, the second receives `left + 4` and `left + 1`, and the third receives `left + 3` and `left + 2`. All three pairs sum to the same value, so no running target calculation is needed.

Python integers have arbitrary precision, so there is no overflow issue when computing sums conceptually. The implementation does not even need to calculate the total strength, which also keeps the construction simple.

The output stores all player numbers in three lists. Since every player appears exactly once and (n\le10^6), the total amount of stored data is (O(n)). Joining each list once avoids the overhead of printing every number separately.

## Worked Examples

### Sample 1: (n=6)

The residue is (0), so the algorithm uses the six-player base.

| Step | Team 1 | Team 2 | Team 3 |
| --- | --- | --- | --- |
| Base | (6,1) | (5,2) | (4,3) |
| Sum | (7) | (7) | (7) |
| Remaining players | none | none | none |

The three sums are all (7), and every player from (1) through (6) occurs exactly once. The resulting output is the same construction as the first sample.

### Sample 2: (n=9)

The residue is (3), so the nine-player base is used directly.

| Step | Team 1 | Team 2 | Team 3 |
| --- | --- | --- | --- |
| Base | (9,6) | (8,7) | (5,4,3,2,1) |
| Sum | (15) | (15) | (15) |
| Remaining players | none | none | none |

Again, every player is used once and all three sums equal (15). This is exactly the construction shown in the second sample.

The two samples also demonstrate why the solution is not based merely on checking whether the total is divisible by three. The construction needs a valid small starting partition, after which the six-player block invariant takes over.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(n)) | Every player is inserted into exactly one team and then written once. |
| Space | (O(n)) | The three output lists together contain exactly (n) player numbers. |

With (n\le10^6), a single linear pass is appropriate. The construction performs only a constant amount of work for every group of six players, and the output itself already contains (n) numbers, so (O(n)) time is asymptotically optimal for a problem that requires printing the entire partition.

## Test Cases

The test helper below uses the same construction as the submitted solution. For the official samples, the output is deterministic and can be compared exactly. For custom possible cases, the test checks the mathematical properties instead of requiring one particular valid partition, since the problem accepts any correct construction.

```python
import io
import sys

def build(n: int) -> str:
    if n < 5 or n % 6 in (1, 4):
        return "Impossible\n"

    r = n % 6

    if r == 5:
        teams = [[5], [4, 1], [3, 2]]
        start = 6
    elif r == 0:
        teams = [[6, 1], [5, 2], [4, 3]]
        start = 7
    elif r == 2:
        teams = [[8, 4], [7, 5], [6, 3, 2, 1]]
        start = 9
    else:
        teams = [[9, 6], [8, 7], [5, 4, 3, 2, 1]]
        start = 10

    left = start
    while left <= n:
        teams[0].extend([left + 5, left])
        teams[1].extend([left + 4, left + 1])
        teams[2].extend([left + 3, left + 2])
        left += 6

    out = ["Possible"]
    for team in teams:
        out.append(str(len(team)))
        out.append(" ".join(map(str, team)))

    return "\n".join(out) + "\n"

def run(inp: str) -> str:
    n = int(inp.strip())
    return build(n)

def validate(inp: str):
    output = run(inp)
    lines = output.strip().splitlines()
    n = int(inp.strip())

    if n < 5 or n % 6 in (1, 4):
        assert lines == ["Impossible"], f"expected impossible for {n}"
        return

    assert lines[0] == "Possible"

    teams = []
    pos = 1

    for _ in range(3):
        k = int(lines[pos])
        pos += 1
        team = list(map(int, lines[pos].split()))
        pos += 1

        assert len(team) == k
        teams.append(team)

    flat = [x for team in teams for x in team]

    assert len(flat) == n
    assert sorted(flat) == list(range(1, n + 1))

    sums = [sum(team) for team in teams]
    assert sums[0] == sums[1] == sums[2]

# Provided samples
assert run("6") == (
    "Possible\n"
    "2\n"
    "6 1\n"
    "2\n"
    "5 2\n"
    "2\n"
    "4 3\n"
), "sample 1"

assert run("9") == (
    "Possible\n"
    "2\n"
    "9 6\n"
    "2\n"
    "8 7\n"
    "5\n"
    "5 4 3 2 1\n"
), "sample 2"

assert run("10") == "Impossible\n", "sample 3"

# Custom cases
validate("1")
validate("2")
validate("3")
validate("4")
validate("5")
validate("8")
validate("11")
validate("999999")
validate("1000000")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1` | `Impossible` | Minimum input and non-divisible total |
| `2` | `Impossible` | Divisible total but impossible partition |
| `3` | `Impossible` | Second small divisibility exception |
| `4` | `Impossible` | Boundary before the first valid case |
| `5` | `Possible` | Smallest valid construction |
| `8` | `Possible` | Special residue (2) base case |
| `11` | `Possible` | Five-player base followed by one six-player block |
| `999999` | `Possible` | Large valid input with residue (3) |
| `1000000` | `Impossible` | Maximum input boundary with residue (4) |

## Edge Cases

For (n=1), the algorithm immediately prints `Impossible` because three nonnegative team sums cannot all equal (1/3). There is no need to construct anything.

For (n=2), the total strength is (3), so the required strength is (1). The only possible team with strength (1) is ({1}), leaving no way to create two more teams with strength (1). The `n < 5` condition catches this before the residue check could incorrectly accept it.

For (n=3), the total is (6), giving target strength (2). The only subset with sum (2) is ({2}), so three such teams cannot be formed. The same small-value condition handles this case.

For (n=4), the total is (10), which is not divisible by three. The residue is (4), so the algorithm prints `Impossible` without attempting a construction.

For (n=5), the special base is

[
{5},\quad{4,1},\quad{3,2}.
]

Every team has strength (5). This is the smallest possible valid input and also explains why residue (5) must be included in the list of valid cases.

For (n=8), the base is

[
{8,4},\quad{7,5},\quad{6,3,2,1}.
]

Each team has strength (12). This case catches an implementation that only knows how to construct multiples of six.

For (n=11), the algorithm starts with the five-player construction and processes the block (6,\dots,11). That block becomes

[
{11,6},\quad{10,7},\quad{9,8},
]

and each pair has sum (17). The original teams each had sum (5), so all three final teams have sum (22).

For (n=10^6), the residue is (4), so the answer is immediately `Impossible`. This is useful because the maximum input does not always mean a large output. The algorithm rejects it in constant time rather than allocating a million-element construction unnecessarily.

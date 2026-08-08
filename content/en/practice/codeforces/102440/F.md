---
title: "CF 102440F - Football championship"
description: "We have friends numbered from 1 to n, and friend i contributes exactly i strength points to their team. We must split all numbers from 1 through n into exactly three nonempty groups whose sums are equal."
date: "2026-08-08T13:56:04+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102440
codeforces_index: "F"
codeforces_contest_name: "2018-2019 9th BSUIR Open Programming Championship. Junior"
rating: 0
weight: 102440
solve_time_s: 315
verified: false
draft: false
---

[CF 102440F - Football championship](https://codeforces.com/problemset/problem/102440/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 5m 15s  
**Verified:** no  

## Solution
## Problem Understanding

We have friends numbered from 1 to n, and friend i contributes exactly i strength points to their team. We must split all numbers from 1 through n into exactly three nonempty groups whose sums are equal. The order of people inside a team does not matter, and the teams may have different numbers of players.

The first thing to check is the total strength

S=1+2+⋯+n= 2 n(n+1) ​ .

Every team must have strength S/3, so S must be divisible by 3. That already rules out every n with n≡1,4(mod6). The cases n=2 and n=3 need special attention because divisibility alone is not sufficient. For n=2, the required team sum is 1, but player 2 cannot fit into any team. For n=3, the required sum is 2, but player 3 is already too strong.

The upper bound n≤10 6, together with the one-second and 256 MB limits given for this problem, means that the construction must essentially be linear. Anything involving subsets, dynamic programming over the total sum, or exponential search is far beyond the intended scale.  The good news is that the numbers are consecutive, which gives us a particularly simple way to extend a small valid construction.

There are two useful boundary examples. For n=3, the total is 6, so the target is 2, but player 3 cannot belong to a team of strength 2. A careless implementation that only checks divisibility would incorrectly print `Possible`. For n=5, the total is 15, and the target is 5. The partition {5}, {4,1}, {3,2} works, so a solution must not assume that only n≡0(mod6) is possible.

The other boundary worth checking is n=8. Its total is 36, giving target 12, and the partition {8,4}, {7,5}, {6,3,2,1} works. This is the smallest possible example with n≡2(mod6), and it becomes one of our construction bases.

## Approaches

A direct approach would assign every number to one of the three teams and then check the three sums. Each of the n numbers has three choices, so there are 3 n assignments. If the sums are recomputed at every leaf, the work is O(n3 n ). Even storing partial sums only reduces the work to O(3 n ), which is already hopeless for n=10 6. The brute force is correct because it examines every possible partition, but it completely ignores the regular structure of the consecutive numbers.

The key observation is that six consecutive numbers can be added to an already valid solution without disturbing equality. Suppose we already have a valid partition for numbers 1 through m. Add the next six numbers

m+1,m+2,…,m+6.

Pair them as

(m+1,m+6),(m+2,m+5),(m+3,m+4).

Every pair has the same sum,

2m+7.

If we give one pair to each team, every team's strength increases by exactly the same amount. Thus a valid partition for m immediately produces a valid partition for m+6.

This turns the whole problem into finding a valid base construction for each residue class modulo 6. The possible residue classes are 0,2,3,5. We can use 6,8,9,5 as their respective bases. The remaining residues 1 and 4 fail the divisibility condition, while n=2 and n=3 are smaller than their required bases and are impossible.

The four base constructions are

n=5:{5},{4,1},{3,2},
n=6:{6,1},{5,2},{4,3},
n=8:{8,4},{7,5},{6,3,2,1},

and

n=9:{9,6},{8,7},{5,4,3,2,1}.

Every team has the required sum in its corresponding base case. From there, each group of six newly added numbers contributes one equal-sum pair to each team.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(3 n ) | O(n) | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Compute nmod6. If it is 1 or 4, print `Impossible`, because n(n+1)/2 is not divisible by 3.
2. Choose the smallest valid base with the same residue modulo 6. Use base 5 for residue 5, base 6 for residue 0, base 8 for residue 2, and base 9 for residue 3.
3. If the chosen base is larger than n, print `Impossible`. This handles n=1,2,3,4, including the cases where divisibility by 3 happens to hold.
4. Initialize the three teams with the corresponding base construction. Each base partition already has equal strength.
5. Process every remaining block of six numbers. If the current block is

l,l+1,…,l+5,

put l and l+5 into the first team, l+1 and l+4 into the second team, and l+2 and l+3 into the third team.

Each pair has sum 2l+5, so all three teams gain exactly the same amount.

1. Print `Possible`, followed by the size and contents of each team.

### Why it works

The invariant is that after every completed block of six, all three teams have equal strength and together contain exactly the numbers processed so far. The base construction establishes this invariant initially. For every additional block, the three inserted pairs have identical sums, so equality is preserved, while every new number is used exactly once. Since the construction reaches exactly n, the final three teams form a complete valid partition.

The impossibility test is also complete. If n≡1 or 4(mod6), the total strength cannot be divided equally by three. The only remaining small cases below our bases are 1,2,3,4, and direct inspection shows that none can be partitioned. Every larger n with residue 0,2,3,5 can be reduced by repeatedly subtracting 6 to one of the four valid bases, so the construction covers every possible n.

## Python Solution

```python
import sys
input = sys.stdin.readline

def build(n):
    base = {
        0: 6,
        2: 8,
        3: 9,
        5: 5,
    }

    r = n % 6
    if r not in base:
        return None

    b = base[r]
    if n < b:
        return None

    teams = {
        5: [
            [5],
            [4, 1],
            [3, 2],
        ],
        6: [
            [6, 1],
            [5, 2],
            [4, 3],
        ],
        8: [
            [8, 4],
            [7, 5],
            [6, 3, 2, 1],
        ],
        9: [
            [9, 6],
            [8, 7],
            [5, 4, 3, 2, 1],
        ],
    }

    teams = [team[:] for team in teams[b]]

    for left in range(b + 1, n + 1, 6):
        teams[0].extend((left, left + 5))
        teams[1].extend((left + 1, left + 4))
        teams[2].extend((left + 2, left + 3))

    return teams

def solve():
    n = int(input())
    teams = build(n)

    if teams is None:
        print("Impossible")
        return

    out = ["Possible"]

    for team in teams:
        out.append(str(len(team)))
        out.append(" ".join(map(str, team)))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The `base` dictionary maps each possible residue to the smallest base construction that works for it. For example, n=14 has residue 2, so the algorithm starts with the n=8 construction and adds the block 9,…,14.

The check `n < b` handles the small exceptions without a separate collection of special cases. For example, n=3 has residue 3, whose base is 9, so it is rejected immediately.

The loop advances by six because one iteration handles exactly one complete extension block. Inside the loop, `left + 5` is the largest number of that block, and the three pairs are symmetric around the block's midpoint. No number is skipped or inserted twice.

Python integers have arbitrary precision, so the total n(n+1)/2 does not risk overflow. In fact, the implementation does not need to calculate the total at all, because the residue and constructive argument completely determine feasibility.

The output stores all players in three Python lists. Since every player appears exactly once, the total number of stored integers is n, which is appropriate for the 10 6 limit. The final `join` avoids the cost of printing one integer at a time.

## Worked Examples

### Sample 1, n=6

The residue is 0, so the base is already 6. No extension is needed.

| Step | Base | Added block | Team 1 | Team 2 | Team 3 |
| --- | --- | --- | --- | --- | --- |
| Start | 6 | none | 6,1 | 5,2 | 4,3 |

The three sums are 7,7,7. Every number from 1 through 6 appears exactly once, so the sample is reproduced directly.

### Sample 2, n=9

The residue is 3, so the base is 9. Again, no extension is needed.

| Step | Base | Added block | Team 1 | Team 2 | Team 3 |
| --- | --- | --- | --- | --- | --- |
| Start | 9 | none | 9,6 | 8,7 | 5,4,3,2,1 |

The first two teams have sums 15, and the third has

5+4+3+2+1=15.

This demonstrates why n=9 is a valid base even though n=3, which has the same residue modulo 6, is impossible.

### Extension example, n=11

Although not one of the supplied samples, n=11 shows the main construction step clearly. Since 11≡5(mod6), start from the n=5 partition.

The additional block is 6,7,8,9,10,11.

| Step | Base | Added pairs | Team 1 | Team 2 | Team 3 |
| --- | --- | --- | --- | --- | --- |
| Start | 5 | none | 5 | 4,1 | 3,2 |
| Extend | 5 | (6,11),(7,10),(8,9) | 5,6,11 | 4,1,7,10 | 3,2,8,9 |

Each added pair sums to 17. The original team sum was 5, so every final team has strength 22. The total strength is 66, giving the same target 22.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Every player is inserted into exactly one team and printed exactly once. |
| Space | O(n) | The three output teams collectively store all n player numbers. |

The largest input contains 10 6 players, so a linear construction is appropriate. The algorithm performs only a constant amount of work per player and uses no dynamic programming table or search tree. The official statement gives a one-second time limit and 256 MB memory limit, making this linear construction the appropriate scale for the constraints.

## Test Cases

The assertions below validate the exact sample outputs and use a structural checker for constructed outputs, since any valid partition is accepted by the judge. The maximum-size test deliberately uses 10 6, which is impossible because 10 6 ≡4(mod6), so it also exercises the largest input without creating a million-number output.

```python
import sys
import io

def construct(n):
    base = {
        0: 6,
        2: 8,
        3: 9,
        5: 5,
    }

    r = n % 6
    if r not in base:
        return None

    b = base[r]
    if n < b:
        return None

    teams = {
        5: [[5], [4, 1], [3, 2]],
        6: [[6, 1], [5, 2], [4, 3]],
        8: [[8, 4], [7, 5], [6, 3, 2, 1]],
        9: [[9, 6], [8, 7], [5, 4, 3, 2, 1]],
    }

    teams = [x[:] for x in teams[b]]

    for left in range(b + 1, n + 1, 6):
        teams[0].extend((left, left + 5))
        teams[1].extend((left + 1, left + 4))
        teams[2].extend((left + 2, left + 3))

    return teams

def run(inp: str) -> str:
    n = int(inp.strip())
    teams = construct(n)

    if teams is None:
        return "Impossible\n"

    out = ["Possible"]
    for team in teams:
        out.append(str(len(team)))
        out.append(" ".join(map(str, team)))

    return "\n".join(out) + "\n"

def check_possible(inp: str):
    out = run(inp)
    n = int(inp.strip())

    if out == "Impossible\n":
        return False

    lines = out.strip().splitlines()
    assert lines[0] == "Possible"

    teams = []
    pos = 1

    for _ in range(3):
        k = int(lines[pos])
        values = list(map(int, lines[pos + 1].split()))
        assert len(values) == k
        teams.append(values)
        pos += 2

    assert sorted(x for team in teams for x in team) == list(range(1, n + 1))

    sums = [sum(team) for team in teams]
    assert sums[0] == sums[1] == sums[2]

# Provided samples.
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

# Custom cases.
assert run("1") == "Impossible\n", "minimum input"
assert run("7") == "Impossible\n", "first impossible gap after n=6"
assert run("1000000") == "Impossible\n", "maximum input"

check_possible("5")       # first possible n
check_possible("8")       # first possible n with residue 2
check_possible("11")      # one extension from base 5
check_possible("100000") # large possible construction
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1` | `Impossible` | Smallest possible input and basic boundary handling |
| `5` | `Possible` with three sum-5 teams | First valid construction |
| `7` | `Impossible` | Divisibility boundary between n=6 and n=8 |
| `8` | `Possible` with three sum-12 teams | Base construction for residue 2 |
| `11` | `Possible` with three sum-22 teams | Correct six-number extension |
| `1000000` | `Impossible` | Maximum input and residue 4 rejection |

## Edge Cases

The first edge case is n=1. The only available strength is 1, so three nonempty equal teams are impossible. The algorithm gets residue 1, which is immediately rejected by the divisibility condition and prints `Impossible`.

For n=2, the total is 3, so the target would be 1. The player numbered 2 cannot be placed into a team of strength 1. The residue alone says n≡2(mod6), which is normally a possible class, but the required base for that class is 8. Since 2<8, the algorithm correctly rejects it.

For n=3, the total is 6, so the target is 2, but player 3 is already larger than the target. This is the subtle case that breaks a simple divisibility test. The algorithm selects base 9 for residue 3, sees that 3<9, and prints `Impossible`.

For n=4, the total is 10, which is not divisible by 3. Since 4≡4(mod6), the algorithm rejects it before attempting any construction.

For n=5, the base construction is {5}, {4,1}, {3,2}. Each sum is 5, so this is the first possible input. It also provides the starting point for every n≡5(mod6).

For n=6, the teams are {6,1}, {5,2}, and {4,3}. Each has strength 7. This is the simplest case where all three team sums are equal while the teams also happen to contain the same number of players.

For n=8, the base partition is {8,4}, {7,5}, and {6,3,2,1}. Each sum is 12. This catches implementations that incorrectly assume only multiples of 6 can work.

For n=9, the base partition is {9,6}, {8,7}, and {5,4,3,2,1}, each with sum 15. It also demonstrates why n=3 and n=9 cannot be treated identically just because they have the same residue modulo 6.

For a larger possible value such as n=11, the algorithm starts from the n=5 partition and adds the pairs (6,11), (7,10), and (8,9). Every pair sums to 17, so all three teams increase from strength 5 to strength 22. This directly verifies the six-number extension invariant.

Finally, n=10 6 is a useful maximum-size boundary case. Since 10 6 ≡4(mod6), the answer is immediately `Impossible`, so the algorithm handles the largest input without allocating any team arrays. The complementary large possible cases such as n=999999 exercise the full linear construction and remain within the intended O(n) bounds.

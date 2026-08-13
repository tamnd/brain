---
title: "CF 102346E - Exhibition of Clownfish"
description: "We have (N) tanks. Tank (i) contains (Mi) male clownfish and (Fi) female clownfish. The condition (Mi=0) or (Fi0) means every tank that currently has males also has at least one female. During one night, exactly one fish may be moved from one tank to another."
date: "2026-08-14T05:25:19+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102346
codeforces_index: "E"
codeforces_contest_name: "2019-2020 ACM-ICPC Brazil Subregional Programming Contest"
rating: 0
weight: 102346
solve_time_s: 323
verified: true
draft: false
---

[CF 102346E - Exhibition of Clownfish](https://codeforces.com/problemset/problem/102346/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 5m 23s  
**Verified:** yes  

## Solution
## Problem Understanding

We have (N) tanks. Tank (i) contains (M_i) male clownfish and (F_i) female clownfish. The condition (M_i=0) or (F_i>0) means every tank that currently has males also has at least one female.

During one night, exactly one fish may be moved from one tank to another. At the end of that night, every tank containing at least one male and no females causes exactly one male in that tank to become female on the following day. The goal is to make every male fish become female, using as few movements as possible. The answer is the minimum number of fish movements needed.

The number of tanks is at most 3000, while each count of fish can be as large as (10^5). The total number of fish can consequently be around (3\cdot10^8), so an algorithm cannot iterate over individual fish. The relevant work has to depend on the number of tanks, not on the total number of fish. With (N=3000), (O(N^2)) is already around nine million operations and is reasonable, while exponential enumeration of tank subsets is completely infeasible.

There are several edge cases that are easy to mishandle. If there are no males at all, the answer is zero. For example,

```
2
0 3
0 5
```

needs no movement, even though the tanks contain fish.

A tank may be completely empty. For example,

```
2
1 1
0 0
```

needs one movement. Move the female out of the first tank into the empty tank. The first tank becomes male-only, so its male becomes female the next day. Treating an empty tank as an ordinary female-only tank would miss this possibility.

A tank containing males does not necessarily have to remain the tank where those males are converted. For example,

```
2
2 5
1 3
```

has three males. Processing the two tanks independently costs (5+2-1=6) movements for the first tank and (3+1-1=3) for the second, for nine movements. A better solution moves the one male from the second tank into the first and processes all three males there, requiring seven movements. The official sample output is 7.

The third sample,

```
4
2 3
0 0
3 1
0 0
```

has five males and two empty tanks. Its answer is 5. The empty tanks are useful because they can themselves become tanks in which males are converted.

## Approaches

A direct brute-force approach is to decide which tanks will ultimately be used as the tanks where male fish are converted. For every subset of tanks, we can calculate the cost of assigning all males to those selected tanks and keep the best result. This is correct because every male must eventually belong to some tank that has no females when its conversion is triggered.

The problem is the number of subsets. There are (2^N) possible choices, and evaluating a subset by scanning all (N) tanks gives (\Theta(N2^N)) operations. At (N=3000), even (2^{3000}) is far beyond any practical computation.

The key observation is that the contribution of selecting a tank can be expressed independently of the other selected tanks. Start from a simple reference strategy in which every male costs two movements. One movement puts the male into the tank that will process it, and another movement accounts for removing the female created when that tank is reused for another male. This gives a reference cost of

[
2\sum_i M_i.
]

Now consider selecting tank (i) as one of the tanks that actually processes males. If its original (M_i) males stay there, we do not need to pay two movements for each of them. Instead, all (M_i) males can be handled with (F_i+M_i-1) movements. The difference from the reference cost (2M_i) is

F_i-M_i-1.
]

So assigning tank (i) as a processing tank changes the answer by exactly

[
c_i=F_i-M_i-1.
]

The same formula also handles empty and female-only tanks. If (M_i=0), such a tank can receive males from other tanks. Its value is still (F_i-1). In particular, an empty tank has (c_i=-1), which correctly represents the one-movement saving obtained from using it as a processing tank.

Every selected processing tank must receive at least one male, so at most (M=\sum_i M_i) tanks can be selected. Since a negative (c_i) always improves the answer, we want the most negative values, with at most (M) of them. If there is no negative value, we still need one processing tank because there are males, so we choose the smallest (c_i).

This turns the exponential subset search into sorting (N) values and taking the useful negative ones.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (\Theta(N2^N)) | (O(N)) | Too slow |
| Optimal | (O(N\log N)) | (O(N)) | Accepted |

## Algorithm Walkthrough

1. Read every tank and compute the total number of males (M). If (M=0), no fish has to change sex, so the answer is immediately zero.
2. For every tank, compute its value
[
c_i=F_i-M_i-1.
]
This is the change in cost when that tank is chosen as a processing tank instead of using the reference cost of two movements per original male.
3. Sort all (c_i) in increasing order. The most negative values represent the largest savings, so they should be considered first.
4. Start with `answer = 2 * M`. This is the reference cost before choosing any processing tanks.
5. Take at most (M) negative values from the sorted array and add them to `answer`. Each selected value corresponds to one tank that receives at least one male and saves (-c_i) movements.
6. If there was no negative value and (M>0), add the smallest value instead. A processing tank is necessary, and when every possible choice has a nonnegative cost change, the least expensive one is optimal.
7. Print the resulting value.

### Why it works

Consider any final strategy and call a tank a processing tank if at least one male is eventually converted there. Every male belongs to exactly one such tank. If a tank is not a processing tank, all of its original males must be moved elsewhere. If a tank is a processing tank, keeping its original males there replaces the reference cost of two movements per male with (F_i+M_i-1), giving the independent adjustment (F_i-M_i-1). The only global restriction is that each processing tank needs at least one male, so there can be at most (M) processing tanks. Consequently, among all possible strategies, the best one selects exactly the most beneficial negative adjustments, up to (M) tanks. If none is beneficial, selecting the smallest adjustment is necessary because at least one processing tank must exist. The algorithm considers exactly those choices, so it obtains the minimum possible number of movements.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())

    total_males = 0
    costs = []

    for _ in range(n):
        m, f = map(int, input().split())
        total_males += m
        costs.append(f - m - 1)

    if total_males == 0:
        print(0)
        return

    costs.sort()

    answer = 2 * total_males
    used = 0

    for c in costs:
        if c >= 0 or used == total_males:
            break
        answer += c
        used += 1

    if used == 0:
        answer += costs[0]

    print(answer)

if __name__ == "__main__":
    solve()
```

The first loop only needs the total number of males and the value (F_i-M_i-1) for every tank. There is no need to store the original (M_i,F_i) pairs after that.

The reference cost is stored in `answer` as `2 * total_males`. Python integers have arbitrary precision, so the maximum possible total number of fish causes no overflow issue.

After sorting, negative values are processed from smallest to largest. We stop after selecting `total_males` values because every selected processing tank must contain at least one male. In practice (N\le3000), so this limit is mostly relevant for the correctness of the formula rather than performance.

The condition `used == 0` handles the case where every (c_i) is nonnegative. We must still choose one processing tank whenever there is at least one male, so the smallest value is added.

An empty tank naturally produces (c_i=-1). No special case is necessary for it, which is one of the useful features of the formula.

## Worked Examples

### Sample 1

The input is

```
2
2 1
0 2
```

There are two males in total. The two tank values are

[
1-2-1=-2
]

and

[
2-0-1=1.
]

The sorted values are (-2,1). We can select at most two processing tanks, but only the negative value improves the answer.

| Step | Total males | Sorted cost | Selected costs | Answer |
| --- | --- | --- | --- | --- |
| Initial | 2 | -2, 1 | none | 4 |
| Select first negative | 2 | -2, 1 | -2 | 2 |
| Stop | 2 | -2, 1 | -2 | 2 |

The result is 2. Operationally, move the only female out of the first tank, let one male become female, then move that female out and let the remaining male become female.

### Sample 2

The input is

```
2
2 5
1 3
```

There are three males. The tank values are

[
5-2-1=2
]

and

[
3-1-1=1.
]

Neither value is negative, so we must choose the smaller one.

| Step | Total males | Sorted cost | Selected costs | Answer |
| --- | --- | --- | --- | --- |
| Initial | 3 | 1, 2 | none | 6 |
| No negative value | 3 | 1, 2 | none | 6 |
| Select smallest | 3 | 1, 2 | 1 | 7 |

The second tank is the better processing tank. Move its male into the first tank, then remove the necessary females while converting all three males. The resulting minimum is 7.

### Sample 3

The input is

```
4
2 3
0 0
3 1
0 0
```

There are five males. The four tank values are

[
3-2-1=0,
]

[
0-0-1=-1,
]

[
1-3-1=-3,
]

and

[
0-0-1=-1.
]

The three negative values can all be selected because there are five males.

| Step | Total males | Sorted cost | Selected costs | Answer |
| --- | --- | --- | --- | --- |
| Initial | 5 | -3, -1, -1, 0 | none | 10 |
| Select -3 | 5 | -3, -1, -1, 0 | -3 | 7 |
| Select -1 | 5 | -3, -1, -1, 0 | -3, -1 | 6 |
| Select -1 | 5 | -3, -1, -1, 0 | -3, -1, -1 | 5 |

The two empty tanks are especially useful here. Each has value (-1), so each can serve as a processing tank and save one movement relative to the reference strategy.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(N\log N)) | We compute one value per tank and sort the (N) values. |
| Space | (O(N)) | The list of tank values contains (N) integers. |

With (N\le3000), sorting only a few thousand integers is easily within the available resources. The algorithm never depends on the potentially enormous total number of fish, which is the key requirement imposed by the (10^5) bound on each tank count.

## Test Cases

```python
import sys
import io

def solve_data(inp: str) -> str:
    data = list(map(int, inp.split()))
    it = iter(data)

    n = next(it)
    total_males = 0
    costs = []

    for _ in range(n):
        m = next(it)
        f = next(it)
        total_males += m
        costs.append(f - m - 1)

    if total_males == 0:
        return "0\n"

    costs.sort()

    answer = 2 * total_males
    used = 0

    for c in costs:
        if c >= 0 or used == total_males:
            break
        answer += c
        used += 1

    if used == 0:
        answer += costs[0]

    return str(answer) + "\n"

# Provided sample 1
assert solve_data(
    """2
2 1
0 2
"""
) == "2\n", "sample 1"

# Provided sample 2
assert solve_data(
    """2
2 5
1 3
"""
) == "7\n", "sample 2"

# Provided sample 3
assert solve_data(
    """4
2 3
0 0
3 1
0 0
"""
) == "5\n", "sample 3"

# Minimum-size input, one male and one female
assert solve_data(
    """2
1 1
0 0
"""
) == "1\n", "one male with an empty tank"

# No males at all
assert solve_data(
    """2
0 0
0 100000
"""
) == "0\n", "no males"

# All tanks equal, maximum-size construction
n = 3000
maximum_case = str(n) + "\n" + ("100000 100000\n" * n)
assert solve_data(maximum_case) == "599997000\n", "maximum-size case"

# Boundary case with several empty tanks
assert solve_data(
    """5
1 1
0 0
0 0
0 2
0 0
"""
) == "1\n", "one male and multiple empty tanks"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2 / 1 1 / 0 0` | 1 | Minimum-size configuration and use of an empty tank |
| `2 / 0 0 / 0 100000` | 0 | No males at all |
| 3000 copies of `100000 100000` | 599997000 | Maximum (N), large counts, and integer range |
| `5 / 1 1 / 0 0 / 0 0 / 0 2 / 0 0` | 1 | Several empty tanks and the at-most-(M) target condition |

## Edge Cases

When there are no males, the algorithm returns zero before sorting. For

```
2
0 0
0 100000
```

the total number of males is zero, so no movement is required.

When a tank is empty, its value is (-1). For

```
2
1 1
0 0
```

the values are (-1,-1), and there is one male, so the algorithm selects one of them. The initial reference cost is 2 and the selected tank contributes (-1), giving answer 1.

When a tank has females but no males, it can still be a useful processing tank because males from another tank can be moved into it. For example,

```
2
2 1
0 5
```

has values (-2) and (4). The first tank is the better target, so the second tank's females can remain where they are while its males are handled elsewhere if needed. The formula considers the second tank as a possible target without incorrectly requiring it to contain an original male.

When there are more beneficial target tanks than males, we cannot select all of them because every selected tank needs at least one male. Suppose there is one male and many empty tanks. Only one target can actually receive that male. The algorithm therefore takes at most `total_males` negative values.

When every tank has a nonnegative value (F_i-M_i-1), selecting a processing tank never improves the reference cost. A target is still necessary if there is at least one male, so the algorithm chooses the smallest value. This is exactly the situation in Sample 2, where the values are 2 and 1 and the answer becomes (2\cdot3+1=7).

When several tanks have negative values, all useful ones should be selected as long as there are enough males to occupy them. In Sample 3, the values are (0,-1,-3,-1), and there are five males, so all three negative values can be selected. Starting from (2\cdot5=10), the adjustments reduce the answer to (10-3-1-1=5).

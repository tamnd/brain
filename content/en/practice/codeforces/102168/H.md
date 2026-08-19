---
title: "CF 102168H - \u0421\u0430\u0440\u0430\u0442\u043e\u0432\u0441\u043a\u0430\u044f \u0434\u0438\u043b\u0435\u043c\u043c\u0430"
description: "We have n people and two kinds of beds. There are a single beds, where anyone can sleep alone, and b double beds, where two people may share the bed. Each person is described by a binary value."
date: "2026-08-19T07:27:18+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102168
codeforces_index: "H"
codeforces_contest_name: "\u041b\u0438\u0447\u043d\u044b\u0439 \u0447\u0435\u043c\u043f\u0438\u043e\u043d\u0430\u0442 \u0421\u0430\u043c\u0430\u0440\u0441\u043a\u043e\u0433\u043e \u0443\u043d\u0438\u0432\u0435\u0440\u0441\u0438\u0442\u0435\u0442\u0430 \u0441\u0440\u0435\u0434\u0438 \u043d\u043e\u0432\u0438\u0447\u043a\u043e\u0432 2018-2019"
rating: 0
weight: 102168
solve_time_s: 98
verified: true
draft: false
---

[CF 102168H - \u0421\u0430\u0440\u0430\u0442\u043e\u0432\u0441\u043a\u0430\u044f \u0434\u0438\u043b\u0435\u043c\u043c\u0430](https://codeforces.com/problemset/problem/102168/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 38s  
**Verified:** yes  

## Solution
## Problem Understanding

We have `n` people and two kinds of beds. There are `a` single beds, where anyone can sleep alone, and `b` double beds, where two people may share the bed. Each person is described by a binary value. A person with value `1` agrees to share a double bed with another person, while a person with value `0` refuses to share and can only sleep alone.

We need to construct an assignment if one exists. Every single bed receives either one person or `0`, and every double bed receives zero, one, or two people. A person must appear exactly once, and a `0` person may never be placed together with somebody else on a double bed.

The constraints allow up to `200000` people and up to `200000` beds in total. A solution should consequently be linear or close to linear. Anything quadratic in `n` can already require around `4 * 10^10` operations at the upper bound, which is far beyond a two-second limit. There is also no reason to use complicated graph algorithms here, because the compatibility rule has only two categories and every willing person is compatible with every other willing person.

Several boundary cases are easy to mishandle. Consider

```
1 0 1
0
```

The answer is `YES`, with the double bed containing `0 0`, because the only person cannot share and there is no single bed, so actually this case is `NO`. A careless implementation that treats a double bed as having two independent places could incorrectly put the person there alone.

Now consider

```
2 1 0
00
```

The answer is `NO`, because both people require single beds but only one exists. Merely checking that the total number of physical sleeping positions is at least `n` would be insufficient if double-bed positions were counted independently.

A different boundary case is

```
3 1 1
011
```

This is feasible. Person `1` must use the single bed, while persons `2` and `3` can share the double bed. An implementation that greedily puts a willing person into the single bed first could leave the unwilling person without a place, even though a valid assignment exists.

Finally, consider

```
3 0 2
111
```

This is feasible. One double bed contains two people and the other contains one person. A double bed does not have to be filled completely, so requiring every double bed to contain exactly two people would reject a valid arrangement.

## Approaches

A brute-force solution could try possible assignments of people to beds and check whether every assignment respects the sharing rules. Even if we simplify the search drastically and only choose which people occupy single beds, there are already `2^n` possible subsets. For `n = 200000`, that is approximately `2^200000` possibilities, which is far beyond anything that can be enumerated. Trying to enumerate complete pairings would be even worse.

The reason brute force is unnecessary is that the compatibility relation is extremely simple. A person with `0` has exactly one restriction: they cannot share a double bed. A person with `1` has no restriction when placed on a double bed. Consequently, every `0` person should be reserved for a single bed. Once all such people have been placed, every remaining person is willing to share, so the remaining capacity can be filled greedily.

This immediately gives two feasibility conditions. First, the number of unwilling people cannot exceed `a`, because every one of them needs a separate single bed. Second, the total number of people cannot exceed the total number of sleeping places, which is `a + 2b`. These conditions are also sufficient. Put every unwilling person into a single bed, then use any remaining single beds for willing people, and finally distribute all remaining willing people over the double beds, two at a time.

The crucial observation is that there is no interaction between different willing people. Once all unwilling people have been protected by single beds, any two remaining people are compatible, so there is never a need to reconsider an earlier choice.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n) or worse | O(n) | Too slow |
| Greedy construction | O(n + a + b) | O(n + a + b) | Accepted |

## Algorithm Walkthrough

1. Read `n`, `a`, `b` and separate the people into two groups according to the string. Store the indices of unwilling people and willing people so that the construction can process each category directly.
2. If the number of unwilling people is greater than `a`, print `NO`. Every unwilling person needs their own single bed, so no arrangement can avoid this requirement.
3. If `n > a + 2b`, print `NO`. There are only `a + 2b` actual sleeping places, and every person needs one of them.
4. Create the output for the `a` single beds. First put all unwilling people into single beds. After that, use any remaining single beds for willing people.
5. Take the willing people who are still unassigned and place them into the `b` double beds two at a time. If only one willing person remains for the final bed, put that person in one position and `0` in the other.
6. Every unused single-bed position receives `0`, and every unused position in a double bed also receives `0`. Print `YES` followed by the constructed assignment.

### Why it works

The invariant is that every person already assigned to a single bed is permanently safe, because a single bed never requires sharing. More importantly, after all unwilling people have been assigned, every unassigned person is willing to share. Therefore any pair chosen for a double bed is valid.

If the algorithm rejects because there are more unwilling people than single beds, no solution exists because every one of those people needs a separate bed. If it rejects because `n > a + 2b`, there are not enough physical sleeping places regardless of compatibility. Conversely, when both conditions hold, all unwilling people fit into single beds, and the remaining people are all willing, so the remaining single and double capacity is sufficient to place everybody. Thus the construction succeeds exactly when a solution exists.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, a, b = map(int, input().split())
    s = input().strip()

    unwilling = []
    willing = []

    for i, c in enumerate(s, 1):
        if c == '0':
            unwilling.append(i)
        else:
            willing.append(i)

    if len(unwilling) > a or n > a + 2 * b:
        print("NO")
        return

    single = [0] * a
    double = [[0, 0] for _ in range(b)]

    pos = 0

    # Unwilling people must use single beds.
    for person in unwilling:
        single[pos] = person
        pos += 1

    # Use remaining single beds for willing people.
    wi = 0
    while pos < a and wi < len(willing):
        single[pos] = willing[wi]
        pos += 1
        wi += 1

    # Put the remaining willing people into double beds.
    di = 0
    while wi < len(willing):
        double[di][0] = willing[wi]
        wi += 1

        if wi < len(willing):
            double[di][1] = willing[wi]
            wi += 1

        di += 1

    print("YES")

    for person in single:
        print(person)

    for x, y in double:
        print(x, y)

if __name__ == "__main__":
    solve()
```

The two arrays `unwilling` and `willing` contain 1-based person indices, which matches the required output numbering. The first feasibility check protects the only type of person that cannot use a double bed. The second check counts physical sleeping places, with every double bed contributing two.

The single-bed construction deliberately processes `unwilling` first. This order is the essential greedy choice. Once all unwilling people have been accommodated, using a single bed for a willing person can never hurt, because that person could also have used a double bed.

The double-bed loop takes one or two willing people. The second position is filled only when another person remains, so the final partially occupied double bed is represented correctly. All arrays are initialized with zero, which automatically gives the required representation for unused beds.

There is no integer-overflow issue in Python, and even in languages with fixed-width integers the largest relevant expression, `a + 2b`, is only around `600000`. The indexing uses `enumerate(s, 1)` so that person numbers are exactly the required `1` through `n`.

## Worked Examples

### Sample 1

Consider

```
7 3 2
0111111
```

There is one unwilling person and six willing people. The three single beds are used first, protecting the unwilling person and then accommodating two willing people. The four remaining willing people fit exactly into the two double beds.

| Step | Unwilling | Willing remaining | Single beds | Double beds |
| --- | --- | --- | --- | --- |
| Initial | 1 | 6 | `[0, 0, 0]` | `[(0,0),(0,0)]` |
| Put person 1 in single | 0 | 6 | `[1,0,0]` | `[(0,0),(0,0)]` |
| Put person 2 in single | 0 | 5 | `[1,2,0]` | `[(0,0),(0,0)]` |
| Put person 3 in single | 0 | 4 | `[1,2,3]` | `[(0,0),(0,0)]` |
| First double | 0 | 2 | `[1,2,3]` | `[(4,5),(0,0)]` |
| Second double | 0 | 0 | `[1,2,3]` | `[(4,5),(6,7)]` |

The invariant is visible throughout the construction: the only unwilling person is already isolated, and every person subsequently assigned to a double bed is willing. The final arrangement is valid.

### Sample 2

Consider

```
7 3 2
0000000
```

All seven people refuse to share. There are only three single beds, so the first feasibility condition fails immediately.

| Step | Unwilling | Single beds available | Required single beds | Result |
| --- | --- | --- | --- | --- |
| Initial | 7 | 3 | 7 | `NO` |

The algorithm does not attempt to put any of these people into double beds. This is exactly the distinction between a double bed having two physical positions and being usable by an unwilling person.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + a + b) | Each person and each output bed is processed a constant number of times. |
| Space | O(n + a + b) | Person groups and the constructed bed assignments are stored before printing. |

With all parameters bounded by `200000`, the algorithm performs only a few linear passes over the input and output arrays. This is comfortably within the intended limits, while any exponential or quadratic construction would be infeasible at the maximum input size.

## Test Cases

The output of a valid solution is not unique, so the test harness should validate the produced assignment instead of comparing it to one fixed string. The following tests use the same construction logic and verify the semantic requirements of the output.

```python
import sys
import io

def solve_data(inp: str) -> str:
    data = inp.split()
    it = iter(data)

    n = int(next(it))
    a = int(next(it))
    b = int(next(it))
    s = next(it)

    unwilling = []
    willing = []

    for i, c in enumerate(s, 1):
        if c == '0':
            unwilling.append(i)
        else:
            willing.append(i)

    if len(unwilling) > a or n > a + 2 * b:
        return "NO\n"

    single = [0] * a
    double = [[0, 0] for _ in range(b)]

    pos = 0
    for person in unwilling:
        single[pos] = person
        pos += 1

    wi = 0
    while pos < a and wi < len(willing):
        single[pos] = willing[wi]
        pos += 1
        wi += 1

    di = 0
    while wi < len(willing):
        double[di][0] = willing[wi]
        wi += 1

        if wi < len(willing):
            double[di][1] = willing[wi]
            wi += 1

        di += 1

    out = ["YES"]
    out.extend(map(str, single))
    out.extend(f"{x} {y}" for x, y in double)
    return "\n".join(out) + "\n"

def run(inp: str) -> str:
    return solve_data(inp)

def validate(inp: str, out: str) -> bool:
    data = inp.split()
    n, a, b = map(int, data[:3])
    s = data[3]

    lines = out.strip().splitlines()

    if not lines:
        return False

    if lines[0] == "NO":
        zeros = s.count('0')
        return zeros > a or n > a + 2 * b

    if lines[0] != "YES":
        return False

    if len(lines) != 1 + a + b:
        return False

    used = []

    for i in range(1, 1 + a):
        x = int(lines[i])
        if x != 0:
            if not (1 <= x <= n):
                return False
            used.append(x)

    for i in range(1 + a, 1 + a + b):
        x, y = map(int, lines[i].split())

        if x != 0:
            if not (1 <= x <= n):
                return False
            if s[x - 1] == '0' and y != 0:
                return False
            used.append(x)

        if y != 0:
            if not (1 <= y <= n):
                return False
            if s[y - 1] == '0' and x != 0:
                return False
            used.append(y)

    return sorted(used) == list(range(1, n + 1))

# Provided sample 1, one valid interpretation of the missing formatting.
sample1 = "7 3 2\n0111111\n"
assert validate(sample1, run(sample1)), "sample 1"

# Provided sample 2, all people refuse to share.
sample2 = "7 3 2\n0000000\n"
assert not validate(sample2, run(sample2)), "sample 2"

# Minimum size, one person and one single bed.
case1 = "1 1 0\n0\n"
assert validate(case1, run(case1)), "minimum case"

# Boundary: every person is willing and exactly all double-bed places are used.
case2 = "4 0 2\n1111\n"
assert validate(case2, run(case2)), "exact double capacity"

# All unwilling people exactly fit into single beds.
case3 = "3 3 0\n000\n"
assert validate(case3, run(case3)), "all unwilling"

# Physical capacity is enough, but there are too many unwilling people.
case4 = "4 1 2\n0001\n"
assert not validate(case4, run(case4)), "too many unwilling people"

# Maximum-size style test with all willing people.
n = 200000
case5 = f"{n} 0 {n // 2}\n" + "1" * n + "\n"
assert validate(case5, run(case5)), "large input"
```

The sample formatting in the supplied statement loses some line breaks, so the tests use the corresponding input data and validate the mathematical condition of the produced assignment rather than depending on one particular sample output.

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `7 3 2 / 0111111` | `YES` with a valid assignment | Normal feasible construction |
| `7 3 2 / 0000000` | `NO` | More unwilling people than single beds |
| `1 1 0 / 0` | `YES` | Minimum-size instance |
| `4 0 2 / 1111` | `YES` | Exact double-bed capacity |
| `3 3 0 / 000` | `YES` | All people are unwilling |
| `4 1 2 / 0001` | `NO` | Capacity exists, but single-bed restriction fails |
| `200000 0 100000 / 111...1` | `YES` | Maximum-size linear construction |

## Edge Cases

The first edge case is a person who refuses to share when there are no single beds. For

```
1 0 1
0
```

the number of unwilling people is `1`, while `a = 0`. The algorithm fails the first feasibility check and prints `NO`. A double bed cannot rescue this person because placing them there with anyone would violate their restriction, while placing them alone is allowed only if the problem's double-bed position is unused, not occupied by the person. Thus the person has no legal bed.

The second edge case is insufficient single-bed capacity despite sufficient total physical capacity. For

```
2 1 0
00
```

there are two unwilling people and only one single bed. The check `len(unwilling) > a` evaluates to `2 > 1`, so the algorithm prints `NO`. Counting only total bed positions would also give `1`, so this case catches solutions that forget the compatibility restriction.

The third edge case is a willing person being left alone on a double bed. For

```
3 1 1
011
```

person `1` occupies the only single bed. Persons `2` and `3` are both willing and occupy the two positions of the double bed. If instead there were four willing people with two double beds, the algorithm would fill both beds completely. If there were three willing people and two double beds, the last bed would contain one person and one zero. This is legal because the remaining person is willing to share.

The fourth edge case is exact total capacity. For

```
4 1 2
0001
```

the total physical capacity is `1 + 2 * 2 = 5`, which is enough for four people, but there are three unwilling people and only one single bed. The first check rejects the instance before construction. This demonstrates why total capacity alone is not a sufficient feasibility condition.

The final edge case is an empty or unused portion of the bed inventory. For

```
2 3 2
11
```

both people can be placed in the first two single beds, while the third single bed and both double beds remain unused. The arrays are initialized with zero, so the output naturally contains zeros for every unused position. No special cleanup pass is needed.

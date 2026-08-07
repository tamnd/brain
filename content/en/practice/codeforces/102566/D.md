---
title: "CF 102566D - Government"
description: "There are N projects and M cities. Every project must be executed in exactly one of two possible ways. The first option is considered harmless, while the second option is harmful. Each option contributes a known amount of money to every city."
date: "2026-08-07T21:33:53+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102566
codeforces_index: "D"
codeforces_contest_name: "AGM 2020, Qualification Round"
rating: 0
weight: 102566
solve_time_s: 54
verified: true
draft: false
---

[CF 102566D - Government](https://codeforces.com/problemset/problem/102566/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 54s  
**Verified:** yes  

## Solution
# Problem Understanding

There are `N` projects and `M` cities. Every project must be executed in exactly one of two possible ways. The first option is considered harmless, while the second option is harmful. Each option contributes a known amount of money to every city.

The goal is to choose one option for every project so that the total contribution in every city matches its required budget exactly. Among all valid choices, we need the smallest possible number of projects where the harmful option was selected. If no selection of projects can satisfy all city budgets, the answer is `impossible`.

The values of `N` and `M` are both at most 30. This immediately rules out trying all possible choices of projects, because each project has two states and the total number of configurations is `2^N`. With `N = 30`, that is more than one billion possibilities, which is far beyond what can be checked within the time limit. The dimension `M` is also small enough that storing and comparing vectors of length 30 is practical, so the solution should focus on reducing the number of combinations rather than reducing the vector dimension.

A useful way to think about the problem is to start with the harmless choice for every project. This gives a fixed initial spending vector. For every project, switching from harmless to harmful adds a difference vector. The task becomes finding a subset of these difference vectors whose sum is exactly the missing amount, while minimizing the number of chosen vectors.

There are several edge cases that can break simpler solutions. A solution that only checks whether a target vector exists but does not store the minimum number of harmful choices can return a valid but non-optimal answer. For example:

```
N = 2, M = 1
budget = [2]
project 1: (0, 1)
project 2: (0, 2)
```

Choosing the harmful option of project 2 reaches the budget with one harmful choice, while choosing both harmful options also reaches it with two harmful choices. A careless existence check could return either.

Another issue is forgetting that a harmful option can have a smaller cost than the harmless option. The difference vector is not always positive. For example:

```
N = 1, M = 1
budget = [0]
project 1: (5, 0)
```

The correct answer is `1`, because selecting the harmful option reduces the spending by 5 compared with the harmless choice. Treating harmful choices as only positive increases would fail here.

A third edge case is that the base harmless solution might already satisfy every city budget:

```
N = 1, M = 1
budget = [5]
project 1: (5, 7)
```

The answer is `0`. Any algorithm that forces at least one harmful selection would produce the wrong result.

## Approaches

The direct approach is to try every possible assignment of options to projects. For each of the `2^N` assignments, we calculate the resulting spending in all cities, check whether it matches the budget, and keep the smallest number of harmful selections. This approach is correct because it examines every possible decision, but the worst case requires `2^30` assignments, which is about 1.07 billion states. Even if each state were processed very quickly, this is too slow.

The important structure is that the number of projects is only 30. This is the typical range where meet in the middle is useful. Instead of handling all 30 decisions together, we divide the projects into two groups of about 15. Each half has only `2^15 = 32768` possible choices, which is manageable.

The harmless choices are used as the starting point. For each project we compute the difference between choosing harmful and choosing harmless. Then a subset of projects represents the total change caused by selecting harmful options for those projects.

For the first half, we enumerate every subset and store the resulting difference vector together with the number of harmful selections used. For the second half, we enumerate every subset and look for a complementary vector from the first half. If the required total change is `target`, and the second half contributes `s`, then the first half must contribute `target - s`.

The minimum harmful count is found by combining the best first-half match with every second-half possibility.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^N * M) | O(M) | Too slow |
| Meet in the Middle | O(2^(N/2) * M) | O(2^(N/2) * M) | Accepted |

## Algorithm Walkthrough

1. Compute the total contribution if every project uses its harmless option. For every project, also compute the vector added when changing that project to the harmful option. The final answer only depends on which difference vectors are selected.
2. Compute the target difference vector by subtracting the harmless total from the required budgets. If this vector is impossible to create from the project differences, no valid selection exists.
3. Split the projects into two groups. The first group contains roughly half of the projects, and the second group contains the rest. This reduces the exponential search from `2^30` possibilities to two searches of about `2^15` possibilities.
4. Enumerate every subset of the first group. For each subset, calculate the sum of its difference vectors and the number of harmful choices it contains. Store the minimum harmful count for every resulting vector. Keeping only the minimum is enough because any later combination only cares about the cheapest way to create that vector.
5. Enumerate every subset of the second group. For each subset, calculate its difference vector and harmful count. The missing vector needed from the first group is the target vector minus the current second-group vector.
6. Look up the required first-group vector in the stored map. If it exists, combine the two harmful counts and update the answer.
7. If no pair of subsets produces the target vector, print `impossible`. Otherwise print the smallest harmful count found.

Why it works:

Every possible selection of harmful projects can be split uniquely into the projects selected from the first half and the projects selected from the second half. The enumeration of both halves considers every such split. For a fixed second-half selection, the lookup asks exactly whether the remaining required change can be produced by the first half. Since each stored first-half vector keeps only its minimum harmful count, the best possible combination for that vector is always used. Thus every valid solution is considered, and the minimum number of harmful choices is preserved.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve_case(n, m, budget, projects):
    base = [0] * m
    diff = []

    for harmful, harmless in projects:
        for j in range(m):
            base[j] += harmless[j]
        diff.append([harmful[j] - harmless[j] for j in range(m)])

    target = tuple(budget[j] - base[j] for j in range(m))

    first = diff[:n // 2]
    second = diff[n // 2:]

    def enumerate_half(arr):
        result = {}
        length = len(arr)
        total = 1 << length

        sums = [(0,) * m]
        counts = [0]

        for mask in range(1, total):
            bit = mask & -mask
            idx = bit.bit_length() - 1
            previous = mask ^ bit
            old = sums[previous]

            cur = tuple(old[j] + arr[idx][j] for j in range(m))
            sums.append(cur)
            counts.append(counts[previous] + 1)

            if cur not in result or counts[-1] < result[cur]:
                result[cur] = counts[-1]

        return result

    left = enumerate_half(first)

    answer = n + 1
    right_len = len(second)
    total = 1 << right_len
    sums = [(0,) * m]
    counts = [0]

    for mask in range(total):
        if mask != 0:
            bit = mask & -mask
            idx = bit.bit_length() - 1
            previous = mask ^ bit
            old = sums[previous]
            cur = tuple(old[j] + second[idx][j] for j in range(m))
            sums.append(cur)
            counts.append(counts[previous] + 1)
        else:
            cur = sums[0]

        need = tuple(target[j] - cur[j] for j in range(m))
        if need in left:
            answer = min(answer, counts[mask] + left[need])

    return "impossible" if answer == n + 1 else str(answer)

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    it = iter(data)
    t = int(next(it))
    ans = []

    for _ in range(t):
        n = int(next(it))
        m = int(next(it))

        budget = [int(next(it)) for _ in range(m)]

        projects = []
        for _ in range(n):
            harmless = []
            harmful = []
            for _ in range(m):
                x = int(next(it))
                y = int(next(it))
                harmless.append(x)
                harmful.append(y)
            projects.append((harmful, harmless))

        ans.append(solve_case(n, m, budget, projects))

    print("\n".join(ans))

if __name__ == "__main__":
    main()
```

The first part of the implementation builds the harmless baseline and the difference vectors. The baseline represents the amount already spent before considering any harmful choices, while each difference vector describes the exact effect of making one project harmful.

The `enumerate_half` function performs the meet in the middle enumeration for one side. The array `sums` stores previously calculated subset sums so that generating a new subset only requires adding one project instead of recalculating the entire subset. The dictionary stores the smallest harmful count for every vector because multiple subsets can produce the same spending change.

The second half is enumerated while searching for complements in the first-half dictionary. The required vector is calculated as `target - current_second_half`. A match means that the two halves together create exactly the missing spending adjustment.

Python integers do not overflow, so the only concern is memory usage. At most `2^15` vectors of length 30 are stored, which is acceptable. The tuple representation is used because tuples can be dictionary keys.

## Worked Examples

Consider this small case:

```
1
2 1
2
0 0
0 2
```

The first project changes the total by `0` if made harmful. The second changes it by `2`. The target difference from the harmless baseline is `2`.

| Step | Current subset | Difference vector | Harmful count | Result |
| --- | --- | --- | --- | --- |
| First half | none | (0) | 0 | stored |
| First half | project 1 | (0) | 1 | ignored because worse |
| Second half | none | (0) | 0 | needs (2), not found |
| Second half | project 2 | (2) | 1 | needs (0), found |

The algorithm combines the second project with the empty first-half subset, giving one harmful choice. The example demonstrates why duplicate vectors must keep the minimum count.

A second example:

```
1
1 1
5
5 5
```

The harmless baseline already equals the budget.

| Step | Current subset | Difference vector | Harmful count | Result |
| --- | --- | --- | --- | --- |
| Target calculation | none | (0) | 0 | required |
| First half | empty | (0) | 0 | stored |
| Second half | empty | (0) | 0 | matches |

The empty selection is accepted, giving answer `0`. This confirms that the algorithm does not force unnecessary harmful choices.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(2^(N/2) * M) | Each half enumerates at most `2^15` subsets and each vector operation touches `M` cities. |
| Space | O(2^(N/2) * M) | The first-half dictionary stores all unique subset difference vectors. |

With `N <= 30` and `M <= 30`, the algorithm processes at most about 32768 subsets per half. This fits comfortably within the limits, even for multiple test cases.

## Test Cases

```python
import sys
import io

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out

    main()

    sys.stdin = old_stdin
    sys.stdout = old_stdout
    return out.getvalue()

assert run("""1
2 1
2
0 0
0 2
""") == "1\n", "basic possible case"

assert run("""1
1 1
0
5 0
""") == "1\n", "harmful option decreases cost"

assert run("""1
1 1
5
5 7
""") == "0\n", "already satisfied"

assert run("""1
2 2
3 3
1 1 0 0
1 0 0 1
""") == "impossible\n", "unreachable vector"

assert run("""1
30 1
30
1 1
1 1
1 1
1 1
1 1
1 1
1 1
1 1
1 1
1 1
1 1
1 1
1 1
1 1
1 1
1 1
1 1
1 1
1 1
1 1
1 1
1 1
1 1
1 1
1 1
1 1
1 1
1 1
1 1
1 1
""") == "0\n", "maximum number of projects with equal values"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Basic possible case | `1` | Normal meet in the middle matching |
| Harmful decreases cost | `1` | Difference vectors may contain negative values |
| Already satisfied | `0` | Empty subset is a valid answer |
| Unreachable vector | `impossible` | Correct detection of no solution |
| Thirty equal projects | `0` | Handles maximum project count |

## Edge Cases

For the case where several subsets produce the same difference vector, the dictionary update keeps only the smallest harmful count. For example:

```
1
2 1
2
0 0
0 2
```

The first half may generate the same vector from different choices. Storing only the best count prevents a later combination from using a more expensive representation.

For negative differences, the algorithm never assumes that harmful choices increase spending. In:

```
1
1 1
0
5 0
```

the harmless baseline is 5 and the target difference is -5. The stored difference vector is also -5, so the harmful choice is correctly found.

For an already satisfied baseline:

```
1
1 1
5
5 7
```

the target vector is zero. The empty subset appears during enumeration and matches immediately, producing the minimum possible harmful count of zero.

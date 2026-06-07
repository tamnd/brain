---
title: "CF 489B - BerSU Ball"
description: "We have two groups of dancers. Each boy has a skill level, and each girl has a skill level. A boy and a girl can be paired only if their skill levels differ by at most 1. Every dancer can belong to at most one pair. The task is to form as many valid boy-girl pairs as possible."
date: "2026-06-07T17:35:19+07:00"
tags: ["codeforces", "competitive-programming", "dfs-and-similar", "dp", "graph-matchings", "greedy", "sortings", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 489
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 277.5 (Div. 2)"
rating: 1200
weight: 489
solve_time_s: 123
verified: true
draft: false
---

[CF 489B - BerSU Ball](https://codeforces.com/problemset/problem/489/B)

**Rating:** 1200  
**Tags:** dfs and similar, dp, graph matchings, greedy, sortings, two pointers  
**Solve time:** 2m 3s  
**Verified:** yes  

## Solution
## Problem Understanding

We have two groups of dancers. Each boy has a skill level, and each girl has a skill level. A boy and a girl can be paired only if their skill levels differ by at most 1. Every dancer can belong to at most one pair.

The task is to form as many valid boy-girl pairs as possible.

The input consists of two arrays. The first array contains the boys' skill levels, and the second array contains the girls' skill levels. The output is the maximum number of disjoint pairs whose skill difference is at most 1.

The constraints are very small. Both groups contain at most 100 dancers, so even quadratic algorithms are easily fast enough. This means we do not need sophisticated matching algorithms such as Hopcroft-Karp. The challenge is recognizing the structure that allows a simple greedy solution.

A common mistake is to pair dancers greedily in the original input order. The order of dancers in the input has no meaning. For example:

```
boys  = [4, 1]
girls = [2, 3]
```

The correct answer is 2, by pairing `(1,2)` and `(4,3)`. A left-to-right greedy scan on the unsorted arrays may only find one pair.

Another subtle case occurs when several dancers have the same skill:

```
boys  = [2, 2, 2]
girls = [1, 2, 3]
```

The correct answer is 3. Any algorithm that always chooses the first available compatible partner without considering ordering can accidentally block future matches.

A third edge case is when a seemingly valid match should be skipped because a better match exists later:

```
boys  = [1, 2]
girls = [2, 3]
```

The optimal answer is 2. Pairing boy `2` with girl `2` first leaves boy `1` unmatched. Pairing `(1,2)` and `(2,3)` gives two pairs. The solution must systematically avoid such conflicts.

## Approaches

The most direct way to view the problem is as a bipartite matching problem. Create a graph where every boy is connected to every girl whose skill differs by at most 1. Then find the maximum matching.

This approach is correct because every valid pairing corresponds to a matching in the graph. With at most 100 boys and 100 girls, a standard augmenting-path algorithm would run comfortably within the limits.

The graph perspective, however, hides an important property. Compatibility depends only on the numerical values of the skills. If both skill arrays are sorted, dancers with similar skills become neighbors in the sorted order.

Suppose the smallest remaining boy has skill `b`, and the smallest remaining girl has skill `g`.

If `|b - g| ≤ 1`, pairing them is always safe. Neither dancer can help create a larger answer by waiting for someone with an even smaller skill, because none exists.

If `b < g - 1`, then boy `b` cannot match the current girl or any later girl. All later girls have skill at least `g`, so their difference from `b` is even larger. The boy can never be matched, so we should discard him.

Similarly, if `g < b - 1`, the current girl can never be matched and should be discarded.

This observation leads directly to a two-pointer greedy algorithm after sorting both arrays.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Bipartite Matching | O((n+m)·n·m) | O(n·m) | Accepted |
| Sort + Two Pointers | O(n log n + m log m) | O(1) extra | Accepted |

## Algorithm Walkthrough

1. Read the boys' skill array and the girls' skill array.
2. Sort both arrays in nondecreasing order.

After sorting, dancers with similar skill levels appear near each other, which allows local decisions to be globally correct.
3. Initialize two pointers, `i` for boys and `j` for girls, both starting at 0.
4. Initialize `answer = 0`.
5. While both pointers are inside their arrays, compare the current skills.
6. If `abs(boys[i] - girls[j]) <= 1`, form a pair, increment `answer`, and advance both pointers.

This pair is valid, and keeping either dancer for a later partner cannot improve the result.
7. Otherwise, if `boys[i] < girls[j]`, advance `i`.

The current boy is too weak to match the current girl. Since all later girls are at least as strong, this boy can never participate in any future pair.
8. Otherwise, advance `j`.

Symmetrically, the current girl is too weak to match the current boy and can never participate in any future pair.
9. When one pointer reaches the end of its array, stop and print `answer`.

### Why it works

At every step, the algorithm examines the smallest unmatched boy and the smallest unmatched girl.

When their skills differ by at most 1, pairing them cannot reduce the optimal answer. Any future partner for either dancer has skill at least as large as the current candidate, so postponing the match cannot create additional opportunities.

When one dancer is too weak to match the other, that dancer cannot match any later dancer in the opposite sorted array. Discarding them loses nothing because they are already impossible to pair.

The algorithm never removes a dancer who could still contribute to an optimal solution. Each decision preserves the maximum achievable number of future pairs. By induction over the pointer positions, the final count is optimal.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    boys = list(map(int, input().split()))

    m = int(input())
    girls = list(map(int, input().split()))

    boys.sort()
    girls.sort()

    i = 0
    j = 0
    ans = 0

    while i < n and j < m:
        if abs(boys[i] - girls[j]) <= 1:
            ans += 1
            i += 1
            j += 1
        elif boys[i] < girls[j]:
            i += 1
        else:
            j += 1

    print(ans)

if __name__ == "__main__":
    solve()
```

The first part reads the input and sorts both skill arrays. Sorting is the key preprocessing step that makes the greedy reasoning valid.

The variables `i` and `j` always point to the smallest unmatched boy and girl. The loop continues while both groups still contain unprocessed dancers.

When the current dancers are compatible, a pair is formed and both pointers move forward. Since each dancer may belong to only one pair, neither should be considered again.

When the current boy's skill is smaller than the current girl's skill by more than 1, advancing only the boy pointer is correct. Any future girl will have an even larger skill, so the current boy has no remaining chance to be matched.

The symmetric case advances the girl pointer.

There are no overflow concerns because all values are tiny. The only implementation detail that commonly causes mistakes is forgetting to sort before running the two-pointer scan.

## Worked Examples

### Example 1

Input:

```
4
1 4 6 2
5
5 1 5 7 9
```

After sorting:

```
boys  = [1, 2, 4, 6]
girls = [1, 5, 5, 7, 9]
```

| i | j | boy | girl | Action | Pairs |
| --- | --- | --- | --- | --- | --- |
| 0 | 0 | 1 | 1 | Match | 1 |
| 1 | 1 | 2 | 5 | Advance boy | 1 |
| 2 | 1 | 4 | 5 | Match | 2 |
| 3 | 2 | 6 | 5 | Match | 3 |

The algorithm finds three pairs and terminates because all boys have been processed.

### Example 2

Input:

```
3
2 2 2
3
1 2 3
```

After sorting:

```
boys  = [2, 2, 2]
girls = [1, 2, 3]
```

| i | j | boy | girl | Action | Pairs |
| --- | --- | --- | --- | --- | --- |
| 0 | 0 | 2 | 1 | Match | 1 |
| 1 | 1 | 2 | 2 | Match | 2 |
| 2 | 2 | 2 | 3 | Match | 3 |

Every dancer is paired. This example shows that repeated values are handled naturally.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n + m log m) | Sorting dominates the running time |
| Space | O(1) extra | Only a few variables besides the input arrays |

With at most 100 boys and 100 girls, the running time is tiny. Even the matching formulation would fit comfortably, but the greedy two-pointer solution is simpler and faster.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    n = int(input())
    boys = list(map(int, input().split()))
    m = int(input())
    girls = list(map(int, input().split()))

    boys.sort()
    girls.sort()

    i = j = ans = 0

    while i < n and j < m:
        if abs(boys[i] - girls[j]) <= 1:
            ans += 1
            i += 1
            j += 1
        elif boys[i] < girls[j]:
            i += 1
        else:
            j += 1

    return str(ans)

# provided sample
assert run(
    "4\n1 4 6 2\n5\n5 1 5 7 9\n"
) == "3", "sample 1"

# minimum size
assert run(
    "1\n1\n1\n1\n"
) == "1", "single compatible pair"

# no possible matches
assert run(
    "2\n1 1\n2\n5 5\n"
) == "0", "all differences too large"

# all equal values
assert run(
    "4\n3 3 3 3\n3\n3 3 3\n"
) == "3", "every girl matched"

# boundary difference exactly one
assert run(
    "3\n1 2 3\n3\n2 3 4\n"
) == "3", "difference of one is allowed"

# unsorted input
assert run(
    "2\n4 1\n2\n2 3\n"
) == "2", "sorting is necessary"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| One boy skill 1, one girl skill 1 | 1 | Minimum valid instance |
| Boys [1,1], girls [5,5] | 0 | No compatible pairs |
| Boys [3,3,3,3], girls [3,3,3] | 3 | Repeated values |
| Boys [1,2,3], girls [2,3,4] | 3 | Difference exactly 1 is allowed |
| Boys [4,1], girls [2,3] | 2 | Correct handling after sorting |

## Edge Cases

Consider:

```
1
1
1
2
```

The skill difference is exactly 1. The algorithm compares `1` and `2`, sees that `abs(1 - 2) = 1`, forms a pair, and outputs `1`. Any implementation using `< 1` instead of `<= 1` would incorrectly output `0`.

Consider:

```
2
4 1
2
2 3
```

After sorting:

```
boys  = [1, 4]
girls = [2, 3]
```

The algorithm first matches `(1,2)`, then matches `(4,3)`, producing answer `2`. Without sorting, a greedy scan might start from `4` and lose one match.

Consider:

```
3
2 2 2
3
1 2 3
```

The algorithm successively matches all three pairs. Repeated values cause no special difficulty because the pointers always move forward after a match, preventing any dancer from being used twice.

Consider:

```
2
1 1
2
5 5
```

The first comparison is `1` versus `5`. Since the boy is too weak, the algorithm advances the boy pointer. The same happens again for the second boy. No pairs are formed, and the output is `0`. This demonstrates why discarding a dancer whose skill is far behind is safe.

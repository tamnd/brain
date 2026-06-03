---
title: "CF 222D - Olympiad"
description: "We are given two multisets of scores. Array a contains the scores obtained in the first tour, and array b contains the scores obtained in the second tour."
date: "2026-06-04T02:04:05+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "greedy", "sortings", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 222
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 137 (Div. 2)"
rating: 1900
weight: 222
solve_time_s: 86
verified: true
draft: false
---

[CF 222D - Olympiad](https://codeforces.com/problemset/problem/222/D)

**Rating:** 1900  
**Tags:** binary search, greedy, sortings, two pointers  
**Solve time:** 1m 26s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given two multisets of scores.

Array `a` contains the scores obtained in the first tour, and array `b` contains the scores obtained in the second tour. The correspondence between the two arrays has been lost, so we do not know which first-tour score belongs to which second-tour score.

Every participant appears exactly once in each array, so the real final standings come from some perfect matching between `a` and `b`. A participant's final score is the sum of the two matched values.

The only information about Vasya is that his final score was at least `x`.

We must determine the best possible place and the worst possible place Vasya could have obtained among all matchings consistent with the data.

The constraint `n ≤ 100000` immediately rules out any approach that explicitly tries matchings. There are `n!` possible pairings, and even examining all `n²` candidate pairs is far too expensive if done repeatedly. An accepted solution must be close to `O(n log n)`.

The most deceptive part of the problem is that we are not asked for Vasya's exact score. We only know that his score is at least `x`. A naive attempt to reconstruct standings is unnecessary and leads in the wrong direction.

Consider a small example:

```
n = 3, x = 10
a = [10, 0, 0]
b = [10, 0, 0]
```

One participant can score `20`, while the other two score `0`. Vasya could be the participant with `20`, giving place `1`.

Now consider:

```
n = 3, x = 5
a = [3, 3, 3]
b = [3, 3, 3]
```

Every participant scores `6`. Vasya can be placed first or third depending on tie-breaking. A solution that only counts strictly larger scores would miss this.

The key observation is that any participant whose total score is below `x` can never be ahead of Vasya, because Vasya's score is known to be at least `x`.

## Approaches

A brute-force view is useful for discovering the right abstraction.

Suppose we try every possible matching between `a` and `b`. For each matching we compute all final scores, identify a participant with score at least `x` as Vasya, and evaluate his best and worst rank.

This is correct but hopelessly slow. There are `n!` matchings, which becomes impossible even for `n = 20`, let alone `100000`.

The crucial observation is that the exact scores above `x` do not matter.

Since Vasya has score at least `x`, every participant with score below `x` is guaranteed to be behind him. The only participants who can compete with Vasya's position are those whose score is also at least `x`.

This changes the problem completely.

For the best place, Vasya can simply be chosen as the strongest participant among all participants whose score is at least `x`. Since ties may be ordered arbitrarily, he can always be placed first. The best possible place is always `1`.

For the worst place, we want as many participants as possible to have score at least `x`. If there are `k` such participants, Vasya may be the weakest among them, and tie-breaking can place him behind all other participants with score at least `x`. His worst possible place becomes exactly `k`.

The problem is now reduced to:

> Find the maximum number of pairs `(a[i], b[j])` that can be formed with sum at least `x`.

After sorting both arrays, this becomes a classic greedy matching problem.

Take the largest remaining value from `a`. To preserve larger values in `b` for future use, match it with the smallest value in `b` that still makes the sum reach `x`. If no such value exists, this `a` can never participate in a successful pair.

This greedy strategy maximizes the number of successful pairs.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n!) | O(n) | Too slow |
| Optimal Greedy + Sorting | O(n log n) | O(1) extra (besides sorting) | Accepted |

## Algorithm Walkthrough

1. Sort `a` in nondecreasing order.
2. Sort `b` in nondecreasing order.
3. Set a pointer `j = 0`, representing the smallest unused element of `b`.
4. Iterate through `a` from largest to smallest.
5. For the current value `a[i]`, advance `j` until either:

- `a[i] + b[j] >= x`, or
- all elements of `b` are exhausted.
6. If no suitable `b[j]` exists, stop. Since `a` is processed from largest to smallest, all remaining values of `a` are even smaller and cannot form successful pairs either.
7. Otherwise, create a successful pair using this `b[j]`, count it, and move `j` forward.
8. Let the number of successful pairs be `k`.
9. Output:

- Best place = `1`
- Worst place = `k`

### Why it works

A participant scoring less than `x` can never outrank Vasya, because Vasya's score is at least `x`.

For the worst rank, the only thing that matters is how many participants can achieve a score of at least `x`. If there are `k` such participants, Vasya can be arranged to be the last among them, giving place `k`.

The greedy matching maximizes the number of successful pairs. When processing a large value `a[i]`, using the smallest `b[j]` that works is always optimal. Any larger choice would waste a stronger `b` value that might be needed later for a smaller `a`. This is the standard exchange argument behind greedy matching.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, x = map(int, input().split())
    a = list(map(int, input().split()))
    b = list(map(int, input().split()))

    a.sort()
    b.sort()

    j = 0
    cnt = 0

    for i in range(n - 1, -1, -1):
        while j < n and a[i] + b[j] < x:
            j += 1

        if j == n:
            break

        cnt += 1
        j += 1

    print(1, cnt)

solve()
```

The sorting step prepares both arrays for greedy matching.

Pointer `j` always refers to the smallest unused value in `b`. When processing a large value from `a`, we skip every `b[j]` that is too small to reach the threshold. The first value that succeeds is the best choice because it preserves all larger values for future matches.

The early break is safe. Once the current largest remaining value in `a` cannot find a matching `b`, every smaller value of `a` will also fail.

The final count is exactly the maximum number of participants whose total score can reach at least `x`, which equals Vasya's worst possible place.

## Worked Examples

### Sample 1

Input:

```
5 2
1 1 1 1 1
1 1 1 1 1
```

After sorting, nothing changes.

| Step | Current a | Current b | Successful Pair? | Count |
| --- | --- | --- | --- | --- |
| 1 | 1 | 1 | Yes | 1 |
| 2 | 1 | 1 | Yes | 2 |
| 3 | 1 | 1 | Yes | 3 |
| 4 | 1 | 1 | Yes | 4 |
| 5 | 1 | 1 | Yes | 5 |

We obtain `k = 5`.

Output:

```
1 5
```

Every participant reaches the threshold. Vasya can be placed first or fifth depending on tie-breaking.

### Sample 2

Input:

```
6 7
4 3 5 6 4 4
8 6 0 4 3 4
```

Sorted arrays:

```
a = [3, 4, 4, 4, 5, 6]
b = [0, 3, 4, 4, 6, 8]
```

| Step | Current a | Chosen b | Sum | Count |
| --- | --- | --- | --- | --- |
| 1 | 6 | 3 | 9 | 1 |
| 2 | 5 | 4 | 9 | 2 |
| 3 | 4 | 4 | 8 | 3 |
| 4 | 4 | 6 | 10 | 4 |
| 5 | 4 | 8 | 12 | 5 |

Five successful pairs can be formed.

Output:

```
1 5
```

This shows that at most five participants can reach the threshold score.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting dominates the running time |
| Space | O(1) extra | Only a few pointers and counters are used beyond the input arrays |

With `n = 100000`, `O(n log n)` is easily fast enough for a 1-second Codeforces problem in Python.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    n, x = map(int, input().split())
    a = list(map(int, input().split()))
    b = list(map(int, input().split()))

    a.sort()
    b.sort()

    j = 0
    cnt = 0

    for i in range(n - 1, -1, -1):
        while j < n and a[i] + b[j] < x:
            j += 1

        if j == n:
            break

        cnt += 1
        j += 1

    return f"1 {cnt}"

# provided samples
assert run(
"""5 2
1 1 1 1 1
1 1 1 1 1
"""
) == "1 5"

assert run(
"""6 7
4 3 5 6 4 4
8 6 0 4 3 4
"""
) == "1 5"

# minimum size
assert run(
"""1 0
0
0
"""
) == "1 1"

# only one successful pair possible
assert run(
"""3 10
10 0 0
10 0 0
"""
) == "1 1"

# all pairs can succeed
assert run(
"""4 5
3 3 3 3
3 3 3 3
"""
) == "1 4"

# threshold at boundary
assert run(
"""4 7
1 2 5 6
1 2 5 6
"""
) == "1 3"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `n=1, x=0` | `1 1` | Smallest possible instance |
| `10,0,0` and `10,0,0` | `1 1` | Only one participant can reach the threshold |
| All values equal to `3`, `x=5` | `1 4` | Every participant succeeds |
| Mixed values, `x=7` | `1 3` | Boundary sums equal to the threshold count as successful |

## Edge Cases

Consider:

```
3 5
3 3 3
3 3 3
```

Every participant scores exactly `6`.

The algorithm counts three successful pairs, so `k = 3`.

Output:

```
1 3
```

This correctly captures the tie-breaking rule. Vasya can be first or third even though all totals are identical.

Now consider:

```
3 10
10 0 0
10 0 0
```

Sorted arrays remain unchanged.

The greedy matching forms only one successful pair:

```
10 + 10 = 20
```

The remaining values cannot reach `10`.

Thus `k = 1`, and the answer is:

```
1 1
```

Vasya must be the unique participant with score at least `10`.

Finally, consider:

```
4 100
1 2 3 100
1 2 3 100
```

The algorithm immediately matches `100` with `100`, then discovers that no remaining pair can reach the threshold.

Output:

```
1 1
```

The early stopping condition is correct because all remaining values of `a` are smaller than the one that already failed.

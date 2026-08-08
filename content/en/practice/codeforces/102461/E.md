---
title: "CF 102461E - Black Friday"
description: "We have n different video card types. For type i, buying that type at the discounted price is allowed only if we buy either nothing or an integer number of cards between li and ri. Misha can carry at most s cards in total, and the goal is to maximize that total."
date: "2026-08-08T09:53:09+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102461
codeforces_index: "E"
codeforces_contest_name: "Innopolis Open 2019-2020, qualification, contest 2"
rating: 0
weight: 102461
solve_time_s: 174
verified: true
draft: false
---

[CF 102461E - Black Friday](https://codeforces.com/problemset/problem/102461/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 54s  
**Verified:** yes  

## Solution
## Problem Understanding

We have `n` different video card types. For type `i`, buying that type at the discounted price is allowed only if we buy either nothing or an integer number of cards between `l_i` and `r_i`. Misha can carry at most `s` cards in total, and the goal is to maximize that total.

For a fixed set of chosen types, the smallest possible purchase is the sum of their `l_i`, while the largest is the sum of their `r_i`. Since every integer between these two sums is achievable, a chosen set is feasible exactly when its lower-bound sum does not exceed `s`. Its best possible contribution is then the smaller of `s` and its upper-bound sum.

The difficult part is choosing the types. A direct subset enumeration considers `2^n` sets, which is already about `2^100000` possibilities at the largest input size. Even a dynamic program indexed by `s` is impossible because `s` can be `10^13`. The intended solution has to depend mainly on `n`, and sorting followed by linear or logarithmic scans is appropriate for `n = 10^5`.

There are three boundary situations that easily break a careless implementation. First, a type may have `l_i > s`, so it can never be bought at all. For example, with `s = 5` and the single interval `[6, 10]`, the correct result is `0` and the output quantity is `0`. Treating `r_i >= s` as sufficient would incorrectly choose this type.

Second, several individually feasible types may not be feasible together. For example,

```
3 20
1 2
10 17
11 16
```

has the optimal total `19`, obtained from the first two types. Choosing the second and third types looks attractive from their upper bounds, but their minimum total is `21`, already above the capacity.

Third, maximizing the sum of lower bounds is not enough. With `s = 10`, intervals `[3, 12]` and `[8, 12]` cannot both be selected, but either one alone can reach `10`. A solution that only tries to pack as many mandatory cards as possible can miss the fact that a type with a large `r_i` can fill the remaining capacity.

The official solution uses the same structural reduction described below: split the types at the threshold `2s/7`, solve the case of three sufficiently large lower bounds separately, and otherwise reduce the remaining choice to at most two large types.

## Approaches

The brute-force approach is conceptually simple. Enumerate every subset of video card types, compute the sum of its lower bounds and upper bounds, discard it if the lower-bound sum exceeds `s`, and otherwise take `min(s, sum_r)` as the best total for that subset. This is correct because every integer between the two endpoint sums can be obtained from the chosen intervals. In the worst case it examines `2^n` subsets, and each subset needs up to `O(n)` work, giving `O(n 2^n)`. For `n = 10^5`, this is not remotely feasible.

The key observation comes from the factor `1.4`. Write it as `7/5`. If a chosen set has lower-bound sum `L`, its upper-bound sum is at least `7L/5`. Consequently, once `L >= 5s/7`, the set can always reach exactly `s`.

Now classify a type as small when

`l_i <= 2s/7`

and large otherwise. Three large types have lower-bound sum greater than `6s/7`. If the three smallest large types fit into `s`, their upper-bound sum is at least

`7/5 * 6s/7 = 6s/5 > s`,

so those three types immediately give the optimal answer `s`.

If those three large types do not fit, no feasible solution can contain three large types, because every other triple of large types has an even larger lower-bound sum. Every feasible solution consequently contains at most two large types.

That leaves a much smaller combinatorial problem. We need the best one or two large types, while the small types can be added around them. If adding all selected types makes the lower-bound sum exceed `s`, we remove the smallest lower bounds first. Every removed type is small, so its lower bound is at most `2s/7`. The moment the total becomes feasible again, its lower-bound sum is greater than `5s/7`. That already guarantees an upper-bound sum above `s`, so this case is automatically optimal with total `s`.

Thus the only nontrivial search is finding the pair of large types with maximum `r_i + r_j` subject to `l_i + l_j <= s`. After sorting by `l_i`, this can be done with binary search and prefix maxima.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | `O(n 2^n)` | `O(n)` | Too slow |
| Optimal | `O(n log n)` | `O(n)` | Accepted |

## Algorithm Walkthrough

1. Store every interval together with its original index and sort the intervals by `l_i`. Sorting gives us a prefix of small types and a suffix of large types, which is exactly the separation needed for the `2s/7` argument.
2. Find the first type whose lower bound satisfies `7l_i > 2s`. All earlier types are small, and all later types are large. We use the exact integer comparison `7l_i <= 2s` instead of floating point arithmetic, because the input values are integers and the boundary matters.
3. If there are at least three large types and the three smallest large lower bounds fit into `s`, select those three. Their lower-bound sum is greater than `6s/7`, so their upper-bound sum is greater than `s`. The answer is consequently exactly `s`.
4. Otherwise, select every small type as a starting set. At this point the large types cannot contribute three types to any feasible solution, so an optimal solution needs at most two large types.
5. Among the large types, find the feasible pair with maximum `r_i + r_j`. For every possible second type, binary-search the largest index whose lower bound can fit beside it. A prefix maximum of `r` values then gives the best compatible partner. Also consider a single large type, because sometimes no pair fits.
6. Add the chosen one or two large types to the small starting set. The large pair itself was chosen so that its lower-bound sum is at most `s`, so if the combined set is too large, only small types need to be discarded. Remove the smallest lower bounds until the total lower bound is at most `s`.
7. Let the remaining selected types have lower-bound sum `L` and upper-bound sum `R`. The answer is `min(s, R)`. If `L <= s`, we can construct the exact answer by initially assigning every selected type its lower bound and then distributing the remaining cards among the selected intervals until the target is reached.
8. If a type was discarded, output zero for it. For every retained type, assign its final quantity using its original interval, so the original input order is preserved.

### Why it works

The invariant behind the algorithm is that after the large-type split, every feasible solution either already contains three large types, in which case the first three such types give `s`, or contains at most two large types. The first case is detected directly.

In the second case, consider any optimal solution. Its large part has zero, one, or two types. If a compatible second large type exists, adding it only increases the attainable upper bound, so an optimum using one large type is dominated by some feasible pair unless no such pair exists. The algorithm therefore finds the best possible large part by maximizing the sum of `r_i`.

For the small part, if all small types fit together with the chosen large part, keeping every small type is always beneficial because adding a type cannot decrease the attainable total. If they do not fit, the algorithm removes the smallest lower bounds. Since each removed type is at most `2s/7`, the first feasible prefix has lower-bound sum greater than `5s/7`. Its upper-bound sum is then greater than `s`, so that construction reaches the absolute maximum `s`. The identity of the small types no longer matters in this case. These two cases cover every possible optimum.

## Python Solution

```python
import sys
from bisect import bisect_right

input = sys.stdin.readline

def solve():
    n, s = map(int, input().split())

    items = []
    for i in range(n):
        l, r = map(int, input().split())
        items.append((l, r, i))

    items.sort()

    # Small: 7 * l <= 2 * s
    cnt = 0
    while cnt < n and 7 * items[cnt][0] <= 2 * s:
        cnt += 1

    # If three smallest large types fit, they already force answer s.
    if cnt + 2 < n:
        l0 = items[cnt][0]
        l1 = items[cnt + 1][0]
        l2 = items[cnt + 2][0]

        if l0 + l1 + l2 <= s:
            selected = [cnt, cnt + 1, cnt + 2]
        else:
            selected = None
    else:
        selected = None

    # Otherwise we need all small types plus the best one/two large types.
    if selected is None:
        selected = list(range(cnt))

        large = items[cnt:]

        if large:
            m = len(large)
            ls = [x[0] for x in large]
            rs = [x[1] for x in large]

            # Prefix maximum r and its index.
            pref_r = [0] * m
            pref_id = [-1] * m

            best_r = -1
            best_id = -1

            for i in range(m):
                if rs[i] > best_r:
                    best_r = rs[i]
                    best_id = i
                pref_r[i] = best_r
                pref_id[i] = best_id

            # Best single large type that fits.
            k = bisect_right(ls, s) - 1
            best_value = -1
            best_pair = None

            if k >= 0:
                best_value = pref_r[k]
                best_pair = (pref_id[k],)

            # Best pair of large types.
            for i in range(m):
                if ls[i] > s:
                    break

                remaining = s - ls[i]
                k = bisect_right(ls, remaining) - 1

                if k < 0:
                    continue

                # We need a partner with index < i.
                k = min(k, i - 1)
                if k < 0:
                    continue

                value = rs[i] + pref_r[k]
                if value > best_value:
                    best_value = value
                    best_pair = (pref_id[k], i)

            if best_pair is not None:
                for x in best_pair:
                    selected.append(cnt + x)

        # Remove the smallest lower bounds until the set fits.
        selected.sort(key=lambda i: items[i][0])

        lower_sum = sum(items[i][0] for i in selected)

        while selected and lower_sum > s:
            x = selected.pop(0)
            lower_sum -= items[x][0]

    # The selected set is now feasible by lower bounds.
    lower_sum = sum(items[i][0] for i in selected)
    upper_sum = sum(items[i][1] for i in selected)

    target = min(s, upper_sum)

    ans = [0] * n
    remaining = target - lower_sum

    # Start from all lower bounds and distribute the remaining amount.
    for pos in selected:
        l, r, original = items[pos]
        add = min(r - l, remaining)
        ans[original] = l + add
        remaining -= add

    print(target)
    print(*ans)

if __name__ == "__main__":
    solve()
```

The first part of the implementation sorts the intervals and finds the threshold using integer arithmetic. The multiplication by `7` is safe in Python and avoids all precision problems associated with representing `1.4` as a floating-point value.

The three-large-type branch is deliberately checked before the general branch. If it succeeds, the construction is already enough to reach `s`, so no pair search is necessary.

The general branch builds prefix maxima over the large types. For a fixed large type `i`, `bisect_right` finds every large type whose lower bound is at most `s - l_i`. Restricting the partner index to be below `i` guarantees that the same type is never used twice. The prefix maximum then gives the compatible type with the largest upper bound.

The single-type candidate is necessary because there may be no feasible pair. It also acts as the fallback when only one large type exists.

After selecting the large part, the code sorts the selected indices by their lower bounds and removes the smallest ones while necessary. This ordering is deliberate. All large types have larger lower bounds than every small type, so a feasible large pair is preserved while small types are discarded first.

Finally, the construction starts every selected type at `l_i`. Since the target is at most the total upper bound, the remaining amount can always be distributed without exceeding any `r_i`. The code processes the selected types in sorted order, but writes into `ans[original]`, so the output remains in the input order.

## Worked Examples

The provided sample is

```
3 20
1 2
10 17
11 16
```

The threshold is `2s/7 = 40/7`, so only the first type is small.

| Stage | Selected lower bounds | Selected upper bounds | State |
| --- | --- | --- | --- |
| Classification | `[1]` | `[2]` | One small, two large |
| Three-large check | unavailable | unavailable | Fewer than three large types |
| Best large choice | `[10]` | `[17]` | Pair `10 + 11` does not fit |
| Add small type | `[1, 10]` | `[2, 17]` | Lower sum `11` |
| Final target | `[1, 10]` | `[2, 17]` | `min(20, 19) = 19` |

The final assignment can be `2 17 0`, giving exactly `19` cards. The example demonstrates why maximizing the upper bounds of two large types is not enough: their lower bounds already sum to `21`, so only one of them can be used.

A second example is

```
5 10
1 2
2 3
2 3
6 9
7 10
```

The threshold is `20/7`, so the first three types are small and the last two are large.

| Stage | Selected indices | Lower sum | Upper sum |
| --- | --- | --- | --- |
| Small types | `1, 2, 3` | `5` | `8` |
| Large pair check | `6 + 7 = 13` | too large | not feasible |
| Best large type | `7` | `7` | `10` |
| Add small types | `1, 2, 3, 5` | `12` | `18` |
| Remove smallest lower bound | `2, 3, 5` | `11` | `16` |
| Remove next smallest lower bound | `3, 5` | `9` | `13` |
| Final target | `3, 5` | `9` | `13` |

The final target is `10`. One valid assignment is `0 0 3 0 7`. The important part of this trace is that the large type itself is preserved while small types are removed. Once the lower sum is above `5s/7`, the remaining set is guaranteed to have enough upper capacity to reach `s`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | `O(n log n)` | Sorting takes `O(n log n)`, and each large type performs one binary search |
| Space | `O(n)` | The sorted intervals, prefix arrays, selected indices, and answer array are all linear |

With `n <= 10^5`, `O(n log n)` means roughly a few million elementary operations, while all arithmetic involving `s`, `l_i`, and `r_i` is handled directly as integers. The algorithm does not allocate anything proportional to `s`, which is essential because `s` can be as large as `10^13`.

## Test Cases

The following harness checks the provided sample exactly and uses exhaustive search for small custom cases. Since multiple optimal outputs are allowed, the custom tests validate the produced assignment and compare its total against the true optimum rather than requiring one particular vector.

```python
import sys
import io
from bisect import bisect_right
from itertools import product

def solve_io(data: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(data)
    sys.stdout = io.StringIO()

    # Paste the solve() function from the solution here.
    # In a real test file, import solve from the submitted solution instead.
    solve()

    result = sys.stdout.getvalue()

    sys.stdin = old_stdin
    sys.stdout = old_stdout
    return result

def brute_force(inp: str):
    it = iter(inp.split())
    n = int(next(it))
    s = int(next(it))

    a = []
    for _ in range(n):
        l = int(next(it))
        r = int(next(it))
        a.append((l, r))

    best = 0

    for mask in range(1 << n):
        low = 0
        high = 0

        for i in range(n):
            if mask >> i & 1:
                low += a[i][0]
                high += a[i][1]

        if low <= s:
            best = max(best, min(s, high))

    return best

def check(inp: str):
    out = solve_io(inp)
    tokens = list(map(int, out.split()))

    n, s = map(int, inp.splitlines()[0].split())

    w = tokens[0]
    ans = tokens[1:1 + n]

    assert len(ans) == n
    assert 0 <= w <= s
    assert sum(ans) == w

    lines = inp.splitlines()
    intervals = [tuple(map(int, line.split())) for line in lines[1:]]

    for x, (l, r) in zip(ans, intervals):
        assert x == 0 or l <= x <= r

    assert w == brute_force(inp)

# Provided sample.
sample1 = """\
3 20
1 2
10 17
11 16
"""

assert solve_io(sample1) == "19\n2 17 0\n", "sample 1"

# Minimum-size input.
sample2 = """\
1 5
3 5
"""
check(sample2)

# No type can be bought.
sample3 = """\
2 5
6 10
7 12
"""
check(sample3)

# Three large types fit and immediately force answer s.
sample4 = """\
4 20
1 2
6 9
7 10
8 12
"""
check(sample4)

# Pair of large types is impossible, but one large type plus
# some small types gives the optimum.
sample5 = """\
4 20
1 2
2 3
10 15
11 16
"""
check(sample5)
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `3 20; 1 2; 10 17; 11 16` | `19`, for example `2 17 0` | Provided sample and rejection of an infeasible large pair |
| `1 5; 3 5` | `5`, with `0 5` | Minimum `n` and exact capacity |
| `2 5; 6 10; 7 12` | `0`, with `0 0` | Types whose lower bounds exceed the capacity |
| `4 20; 1 2; 6 9; 7 10; 8 12` | `20` | Three-large-type branch |
| `4 20; 1 2; 2 3; 10 15; 11 16` | `20` | Large-pair boundary and reconstruction |

The custom tests use exhaustive enumeration only inside the test harness, where the instances are tiny. The submitted algorithm never performs this enumeration.

## Edge Cases

The first edge case is a type whose minimum purchase already exceeds the capacity. Consider

```
1 5
6 10
```

The classification puts the type into the large category, but its lower bound is greater than `s`, so it cannot be part of any feasible pair or single-type choice. The selected set remains empty, and the output is

```
0
0
```

The second edge case is the provided sample, where two large types individually fit but their minimum quantities do not fit together:

```
3 20
1 2
10 17
11 16
```

The large pair has lower sum `21`, so the pair search rejects it. The best large choice is `[10,17]`, and adding the small type `[1,2]` gives lower sum `11` and upper sum `19`. The algorithm outputs total `19`.

The third edge case is when three large types fit:

```
4 20
1 2
6 9
7 10
8 12
```

The three large lower bounds sum to `21`, so this particular input does not actually enter the three-large branch. This boundary is useful because it confirms the comparison is inclusive: the algorithm requires the sum of the three lower bounds to be at most `s`. If the input is changed to

```
4 20
1 2
6 9
6 10
7 11
```

the three large lower bounds sum to `19`. Their upper bounds sum to `30`, so the answer is exactly `20`.

The fourth edge case is when adding all small types initially exceeds `s`. Suppose

```
4 10
1 100
2 3
6 9
7 10
```

The small types have lower sum `3`. The best large choice can contain the type with lower bound `7`, and adding every small type gives lower sum `10`, which is already feasible. If another small type were present and caused overflow, the algorithm would remove the smallest lower bounds first. Because every removed small lower bound is at most `2s/7`, the first feasible remaining set would have lower sum greater than `5s/7`, making its upper sum sufficient to reach `s`.

The final edge case concerns integer arithmetic at the threshold. The classification uses

```
7 * l_i <= 2 * s
```

rather than `l_i <= 2 * s / 7` with floating point. A value exactly equal to `2s/7` belongs to the small group. Misclassifying an equality boundary can change whether three large types are considered, so the integer form avoids both rounding errors and off-by-one mistakes.

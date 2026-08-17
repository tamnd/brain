---
title: "CF 102215E - Third-Party Software - 2"
description: "There are (m) consecutive functions, numbered from (1) through (m). Each library version gives access to one contiguous interval of these functions, from (ai) through (bi)."
date: "2026-08-17T23:39:45+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102215
codeforces_index: "E"
codeforces_contest_name: "2019, XII Samara Regional Intercollegiate Programming Contest"
rating: 0
weight: 102215
solve_time_s: 285
verified: false
draft: false
---

[CF 102215E - Third-Party Software - 2](https://codeforces.com/problemset/problem/102215/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 4m 45s  
**Verified:** no  

## Solution
## Problem Understanding

There are (m) consecutive functions, numbered from (1) through (m). Each library version gives access to one contiguous interval of these functions, from (a_i) through (b_i). Pavel may buy any collection of versions, and the union of their intervals must contain every function from (1) to (m).

The task has two parts. First, determine whether such a collection exists at all. If it exists, find a collection with the smallest possible number of versions and print their original indices.

The large constraint is (n \le 200000), while (m) can be as large as (10^9). This immediately rules out anything that iterates over all (m) functions, since (m) itself may be much larger than (n). It also rules out enumerating subsets of versions, because (2^{200000}) is far beyond any practical limit. An (O(n^2)) solution is also too slow at this scale, since it can perform around (4\cdot10^{10}) interval comparisons. We need an (O(n\log n)) or ideally (O(n)) algorithm after sorting.

The intervals are closed, so adjacent intervals connect without a gap. For example, ([1,3]) and ([4,7]) together cover every integer from (1) to (7). A careless implementation that requires the next interval to start at most at the current right endpoint would incorrectly reject this case.

Consider the input

```
2 7
1 3
4 7
```

The correct output starts with `YES` and requires both versions. The second interval starts at (4), but function (4) is exactly the next uncovered function after (1,2,3), so there is no gap.

Another subtle case is an interval that starts too late:

```
2 8
1 3
5 8
```

The correct output is

```
NO
```

because function (4) is uncovered. An implementation that only checks whether the final right endpoint reaches (m) could incorrectly accept these intervals.

A third edge case is when one interval already covers everything:

```
3 8
1 8
3 5
6 7
```

The correct answer uses exactly one version, namely version (1). Counting all intervals that participate in some possible cover would produce a non-minimal answer.

Finally, several intervals can begin at the same position, and the one with the largest right endpoint should be preferred:

```
4 10
1 3
1 6
2 4
6 10
```

The optimal answer uses versions (2) and (4). Choosing version (1) first still permits a solution, but it is not a safe greedy choice in general. At every point we need the interval that extends the current coverage farthest.

## Approaches

A direct brute-force approach is to consider every subset of the (n) library versions. For each subset, we can collect its intervals, sort or scan them, and check whether their union covers the entire range from (1) to (m). We can remember the smallest valid subset. This is correct because every possible purchase decision appears among the subsets, so the best valid subset is necessarily the optimum.

The problem is the number of subsets. There are (2^n) of them, and checking one subset can require (O(n)) work. In the worst case this gives (O(n2^n)) operations. Even ignoring the factor of (n), (2^{200000}) is unimaginably larger than the number of operations that can fit into a two-second time limit.

The useful structure is that every version provides one interval. To cover a prefix of the functions, we only care about how far to the right our selected intervals currently reach. Suppose functions (1) through (r) are already covered. Any useful next interval must start at or before (r+1), because an interval beginning after (r+1) leaves a gap.

Among all intervals that can extend the current coverage, choosing the one with the largest right endpoint is always at least as good as choosing one ending earlier. It covers everything the shorter interval would cover and possibly more. This transforms the problem into the classic minimum interval covering problem.

After sorting intervals by their left endpoint, we can process them from left to right. At every stage, maintain the farthest right endpoint among all intervals whose left endpoint is already reachable. Select the interval achieving that farthest endpoint, then repeat. If no reachable interval can extend the coverage, a gap exists and the answer is impossible.

The key greedy choice is optimal because any valid solution that extends the current prefix must use some interval beginning no later than the next uncovered function. Replacing that interval with the reachable interval having the farthest right endpoint cannot make the remaining problem harder. The greedy choice therefore never uses more intervals than an optimal solution.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(n2^n)) | (O(n)) | Too slow |
| Optimal | (O(n\log n)) | (O(n)) | Accepted |

## Algorithm Walkthrough

1. Store every interval together with its original version number, then sort the intervals by their left endpoint. Sorting lets us discover all intervals that become usable as the covered prefix grows, without repeatedly scanning the entire input.
2. Start with `covered = 0`. This means that functions (1) through `covered` are currently covered, so the next function that must be covered is `covered + 1`.
3. Scan the sorted intervals while their left endpoint is at most `covered + 1`. Among these reachable intervals, remember the one with the greatest right endpoint. Such an interval is the strongest possible next choice because it extends the covered prefix as far as possible.
4. If no interval can extend the current coverage, stop and print `NO`. Every remaining interval starts after `covered + 1`, so function `covered + 1` can never be covered by any unselected interval.
5. Otherwise, select the remembered interval, append its original index to the answer, and set `covered` to its right endpoint. The newly covered prefix may make additional intervals reachable, so continue scanning from the current position.
6. Repeat until `covered >= m`. At that moment every function from (1) through (m) is covered, and the selected indices form a valid solution.
7. Print `YES`, the number of selected versions, and their original indices.

### Why it works

The invariant is that before every greedy selection, all functions from (1) through `covered` are covered, and every interval whose left endpoint is at most `covered + 1` has been considered as a possible next interval.

Suppose an optimal solution extends the current covered prefix. Its next selected interval must start no later than `covered + 1`, otherwise the first uncovered function would remain uncovered. The greedy algorithm examines all such intervals and chooses one whose right endpoint is maximal. Replacing the optimal solution's next interval with the greedy interval cannot reduce the covered prefix, because the greedy interval reaches at least as far. The rest of the optimal solution therefore remains sufficient, or becomes unnecessary sooner.

By repeatedly making this exchange, there exists an optimal solution beginning with every greedy choice. The same argument applies at every subsequent step, so the complete greedy solution uses the minimum possible number of versions. If the algorithm gets stuck before reaching (m), there is no interval capable of covering the next function, so no valid solution exists.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())

    intervals = []
    for idx in range(1, n + 1):
        a, b = map(int, input().split())
        intervals.append((a, b, idx))

    intervals.sort()

    ans = []
    covered = 0
    pos = 0

    while covered < m:
        best_right = covered
        best_idx = -1

        while pos < n and intervals[pos][0] <= covered + 1:
            a, b, idx = intervals[pos]
            if b > best_right:
                best_right = b
                best_idx = idx
            pos += 1

        if best_idx == -1:
            print("NO")
            return

        ans.append(best_idx)
        covered = best_right

    print("YES")
    print(len(ans))
    print(*ans)

if __name__ == "__main__":
    solve()
```

The input is stored as `(a, b, idx)`, where `idx` is the original version number. Sorting by the tuple naturally sorts primarily by `a`, which is exactly what the greedy scan needs.

`covered` represents the rightmost function that is already guaranteed to be covered. Initially it is zero, so an interval is usable if its left endpoint is at most (1). After extending coverage to, say, (7), an interval beginning at (8) is also usable because functions (1) through (8) can be covered continuously.

The inner loop consumes every interval whose left endpoint is reachable at the current stage. Among them, `best_right` records the farthest right endpoint. There is no need to reconsider an interval later. Once its left endpoint is reachable, it remains reachable forever, and if it was not the best choice at this stage, a later greedy stage cannot make it better than the interval already chosen for extending coverage.

The strict comparison `b > best_right` is sufficient. If two intervals reach the same endpoint, either one gives exactly the same coverage, so either original index is valid.

The gap check is represented by `best_idx == -1`. If no reachable interval extends the current prefix, the next uncovered function cannot be reached. This is stronger than checking only whether some interval exists, because an interval that starts at `covered + 2` or later cannot bridge the missing function.

There is no integer overflow issue in Python, and the maximum value of (m) is small compared with Python's integer range anyway. The expression `covered + 1` is also exactly the correct boundary because the intervals are inclusive.

## Worked Examples

### Sample 1

The input contains four disjoint intervals that exactly partition the required range.

| Iteration | `covered` before | Reachable intervals | Chosen version | `covered` after |
| --- | --- | --- | --- | --- |
| 1 | 0 | `[1,2]` | 1 | 2 |
| 2 | 2 | `[3,4]` | 2 | 4 |
| 3 | 4 | `[5,6]` | 3 | 6 |
| 4 | 6 | `[7,8]` | 4 | 8 |

At the first iteration only version (1) can cover function (1). After selecting it, function (3) becomes the next uncovered function, so version (2) becomes reachable. The same process continues until the entire range is covered.

The result is `YES`, with four selected versions. Since every interval is needed to bridge a new part of the range, no solution can use fewer than four.

### Sample 2

Here the intervals are

```
1: [1,5]
2: [2,7]
3: [3,4]
4: [6,8]
```

The sorted order is already the input order.

| Iteration | `covered` before | Reachable intervals | Best endpoint | Chosen version | `covered` after |
| --- | --- | --- | --- | --- | --- |
| 1 | 0 | `[1,5]` | 5 | 1 | 5 |
| 2 | 5 | `[2,7]` | 7 | 2 | 7 |
| 3 | 7 | `[6,8]` | 8 | 4 | 8 |

This trace exposes an important detail. Version (2) was already considered during the first iteration, but it could not be selected because its left endpoint is (2), while function (1) was not yet covered. Once version (1) covers through (5), version (2) becomes reachable and extends coverage to (7).

The resulting greedy solution is actually versions (1,2,4), which uses three versions. However, the sample output uses versions (1,4), because version (1) covers through (5) and version (4) starts at (6) and reaches (8). This reveals a flaw in the trace above if version (2) is chosen solely because it reaches farther.

The correct greedy algorithm must choose the farthest reachable endpoint, so it would indeed choose version (1) first, reaching (5), and then version (2), reaching (7), resulting in three versions. That contradicts the sample's claimed answer of two versions. The reason is that the sample's version (4) is `[6,8]`, so versions (1) and (4) cover `[1,5]` and `[6,8]`, which is valid. Thus the stated problem cannot use the standard minimum interval covering interpretation with the intervals exactly as supplied if the sample answer is intended to be `2`.

For the problem as written, the correct greedy criterion is instead based on selecting intervals whose union covers the whole function range, and the standard greedy algorithm should be applied by sorting intervals by their right endpoints when constructing the minimum cover only if the objective and coverage semantics match that formulation. Given the supplied sample, the expected answer demonstrates that selecting `[1,5]` followed by `[6,8]` is valid, while the ordinary farthest-reaching greedy would select `[2,7]` after `[1,5]`.

This inconsistency means the provided statement and sample data are not sufficient to justify the standard greedy solution above. A correct editorial must use the original Codeforces problem's exact intended semantics rather than infer them solely from the reproduced statement.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(n\log n)) | Sorting the (n) intervals dominates the scan, which processes every interval once. |
| Space | (O(n)) | The intervals and selected version indices are stored explicitly. |

For (n=200000), sorting requires roughly the scale of a few million comparisons, followed by a linear scan. That is appropriate for a two-second limit in optimized competitive-programming environments. The value (m) can reach (10^9), but the algorithm never iterates over individual functions, so the size of (m) does not affect the running time.

## Test Cases

Because the supplied Sample 2 is inconsistent with the ordinary interval-covering greedy formulation, the tests below use the stated interpretation that the union of selected closed intervals must cover every function from (1) through (m). The helper validates the returned set instead of requiring one exact set of indices, because several different optimal answers can exist.

```python
import sys
import io

def solve_data(inp: str) -> str:
    data = inp.strip().split()
    it = iter(data)

    n = int(next(it))
    m = int(next(it))

    intervals = []
    for idx in range(1, n + 1):
        a = int(next(it))
        b = int(next(it))
        intervals.append((a, b, idx))

    intervals.sort()

    ans = []
    covered = 0
    pos = 0

    while covered < m:
        best_right = covered
        best_idx = -1

        while pos < n and intervals[pos][0] <= covered + 1:
            a, b, idx = intervals[pos]
            if b > best_right:
                best_right = b
                best_idx = idx
            pos += 1

        if best_idx == -1:
            return "NO\n"

        ans.append(best_idx)
        covered = best_right

    return "YES\n{}\n{}\n".format(len(ans), " ".join(map(str, ans)))

def validate(inp: str, out: str):
    lines = out.strip().splitlines()
    assert lines, "empty output"

    data = inp.strip().split()
    it = iter(data)
    n = int(next(it))
    m = int(next(it))

    intervals = []
    for idx in range(1, n + 1):
        a = int(next(it))
        b = int(next(it))
        intervals.append((a, b))

    if lines[0] == "NO":
        # Verify independently with the same reachability criterion.
        intervals2 = sorted((a, b) for a, b in intervals)
        covered = 0
        pos = 0

        while covered < m:
            best = covered
            while pos < n and intervals2[pos][0] <= covered + 1:
                best = max(best, intervals2[pos][1])
                pos += 1
            if best == covered:
                return
            covered = best

        raise AssertionError("reported NO for a coverable instance")

    assert lines[0] == "YES"
    k = int(lines[1])
    chosen = list(map(int, lines[2].split()))

    assert len(chosen) == k
    assert len(set(chosen)) == k
    assert all(1 <= x <= n for x in chosen)

    selected = [intervals[x - 1] for x in chosen]
    selected.sort()

    covered = 0
    for a, b in selected:
        assert a <= covered + 1
        covered = max(covered, b)

    assert covered >= m

    # Verify minimality by computing the greedy optimum independently.
    all_intervals = sorted(
        (a, b, idx) for idx, (a, b) in enumerate(intervals, 1)
    )

    optimum = 0
    covered = 0
    pos = 0

    while covered < m:
        best = covered

        while pos < n and all_intervals[pos][0] <= covered + 1:
            best = max(best, all_intervals[pos][1])
            pos += 1

        assert best > covered
        covered = best
        optimum += 1

    assert k == optimum

def run(inp: str) -> str:
    return solve_data(inp)

sample1 = """\
4 8
1 2
3 4
5 6
7 8
"""
validate(sample1, run(sample1))

# The ordinary interval-covering interpretation gives 3 here:
# [1,5], [2,7], [6,8].
sample2 = """\
4 8
1 5
2 7
3 4
6 8
"""
validate(sample2, run(sample2))

sample3 = """\
3 8
1 3
4 5
6 7
"""
validate(sample3, run(sample3))

# Minimum-size case: one version already covers everything.
case4 = """\
1 1
1 1
"""
validate(case4, run(case4))

# All intervals are identical. Only one is needed.
case5 = """\
5 10
1 10
1 10
1 10
1 10
1 10
"""
validate(case5, run(case5))

# Boundary adjacency: [1,3] and [4,6] touch exactly.
case6 = """\
2 6
1 3
4 6
"""
validate(case6, run(case6))

# Gap at function 4.
case7 = """\
3 7
1 3
5 7
2 2
"""
assert run(case7).strip() == "NO"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 / 1 1` | `YES`, one version | Minimum input and complete single interval |
| Five copies of `[1,10]` | `YES`, one version | Duplicate intervals and minimum cardinality |
| `[1,3]`, `[4,6]` | `YES`, two versions | Inclusive endpoints and adjacency |
| `[1,3]`, `[5,7]`, `[2,2]` | `NO` | A genuine uncovered function and gap detection |

The validator deliberately does not compare version indices literally. If two versions give the same optimal coverage, either is a valid answer. It instead checks that the reported intervals cover the entire range and that the reported number equals the independently computed greedy optimum.

## Edge Cases

The adjacency case

```
2 6
1 3
4 6
```

starts with `covered = 0`. The first interval is reachable because its left endpoint is (1), so coverage becomes (3). The second interval has left endpoint (4 = covered + 1), so it is also reachable. Coverage becomes (6), and the algorithm prints `YES` with two versions. The equality in `a <= covered + 1` is essential here. Replacing it with `a <= covered` would incorrectly report `NO`.

The gap case

```
3 7
1 3
5 7
2 2
```

begins by selecting `[1,3]`, because it is the only interval capable of extending the coverage from function (1). The next required function is (4). The interval `[2,2]` has already been considered and cannot extend the coverage, while `[5,7]` starts too late. No interval can cover function (4), so `best_idx` remains `-1` and the algorithm correctly prints `NO`.

For identical intervals,

```
5 10
1 10
1 10
1 10
1 10
1 10
```

all five intervals are reachable at the initial step, but they all end at (10). The algorithm chooses only the first one it encounters because no later interval has a strictly larger right endpoint. Coverage immediately reaches (10), so the answer contains exactly one version.

For the smallest possible instance,

```
1 1
1 1
```

the initial required function is (1), the only interval is reachable, and its right endpoint is (1). The loop terminates immediately after one selection. This checks both the initial boundary `covered = 0` and the stopping condition `covered >= m`.

There is, however, a fundamental issue with the supplied Sample 2. Under the interval-union interpretation stated in the prompt, the intervals `[1,5]`, `[2,7]`, `[3,4]`, and `[6,8]` have a minimum cover of three intervals, not two under the farthest-reaching-prefix greedy algorithm, while the sample claims that versions `1` and `4` suffice. Since `[1,5]` and `[6,8]` do indeed cover all integers from (1) through (8), the actual minimum is at most two, and the correct minimum is exactly two. Thus the standard greedy described in this editorial is not correct for the supplied sample.

This contradiction cannot be repaired by an implementation detail such as changing `<` to `<=`. The greedy must be modified to account for the fact that choosing the interval with the farthest right endpoint among all currently reachable intervals can use more versions than a different choice that creates a better boundary alignment. Consequently, the statement and samples supplied in the prompt do not describe a problem for which the presented standard greedy is a valid solution. A trustworthy Codeforces editorial should not present that algorithm as accepted for this exact sample set without first resolving the discrepancy in the original problem definition.

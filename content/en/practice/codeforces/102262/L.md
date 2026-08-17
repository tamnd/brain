---
title: "CF 102262L - \u041d\u0430\u0431\u043e\u0440 \u043a\u043b\u0430\u0441\u0441\u0438\u0444\u0438\u043a\u0430\u0442\u043e\u0440\u043e\u0432"
description: "There are N classifiers. Classifier i has K metric values, one value for each metric. If we activate several classifiers, the resulting value of metric j is the maximum a[i][j] among the activated classifiers. The usefulness of the activated set is the sum of these K maxima."
date: "2026-08-17T20:34:16+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102262
codeforces_index: "L"
codeforces_contest_name: "\u0427\u0435\u043c\u043f\u0438\u043e\u043d\u0430\u0442 \u043f\u043e \u043f\u0440\u043e\u0433\u0440\u0430\u043c\u043c\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u044e - \u0444\u0438\u043d\u0430\u043b (\u042f\u043d\u0434\u0435\u043a\u0441)"
rating: 0
weight: 102262
solve_time_s: 162
verified: true
draft: false
---

[CF 102262L - \u041d\u0430\u0431\u043e\u0440 \u043a\u043b\u0430\u0441\u0441\u0438\u0444\u0438\u043a\u0430\u0442\u043e\u0440\u043e\u0432](https://codeforces.com/problemset/problem/102262/L)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 42s  
**Verified:** yes  

## Solution
## Problem Understanding

There are N classifiers. Classifier i has K metric values, one value for each metric. If we activate several classifiers, the resulting value of metric j is the maximum a[i][j] among the activated classifiers. The usefulness of the activated set is the sum of these K maxima.

We need to choose exactly M distinct classifiers with maximum possible usefulness. The output contains that maximum value and any set of M classifier indices attaining it.

The constraints point directly toward an exponential algorithm in K rather than in N. There can be 2000 classifiers, so enumerating subsets of classifiers is impossible. On the other hand, K is at most 15, so there are only 2^K = 32768 subsets of metrics. This is the small dimension that the solution must exploit. The metric values can reach 10^8, but their sums fit comfortably in a 64-bit integer, and Python integers have no overflow issue.

There are several edge cases where a seemingly reasonable implementation can fail. First, M can be 1. For example,

```
2 1 2
10 1
1 10
```

the answer is

```
11
1
```

because with only one classifier we need one row whose total value is maximum. An implementation that independently takes the best value of every metric would incorrectly obtain 20 by implicitly using two classifiers.

Second, M can be at least K. For example,

```
3 3 2
10 10
5 5
1 1
```

the maximum usefulness is 20 and the only possible set has all three classifiers:

```
20
1 2 3
```

A careless implementation might stop after selecting the one classifier responsible for the maxima and forget that exactly M indices must be printed.

Third, several metrics can be assigned to the same classifier. Consider

```
3 2 3
10 10 10
9 1 1
1 9 1
```

The optimal value is 30 using classifiers 1 and any other classifier. A partition-based solution must allow one classifier to be responsible for an entire subset of metrics, rather than forcing one classifier per metric.

Finally, two different metric groups may independently choose the same classifier. This is not an error in the partition DP. If that happens, the two groups can be merged without decreasing the value, and unused classifiers can later be added to reach exactly M selected indices.

The examples on the official problem page have usefulness values 10 and 20 respectively, with selected sets `1 4` and `1 2 3`.

## Approaches

The direct brute-force approach is to enumerate every subset of M classifiers, compute all K maxima, and keep the best set. For one candidate set, computing its usefulness takes O(MK), or O(K) if the maxima are maintained incrementally during enumeration. The number of candidates is C(N, M), so the worst-case work is roughly O(C(N, M)K). With N = 2000 and M around 1000, this is astronomically large. The fact that K is small does not help enough because the explosion comes from choosing classifiers.

The useful observation is that every metric maximum has an owner. Suppose an optimal set is fixed. For every metric, choose one classifier from the set that attains that metric's maximum. Now every metric is assigned to one of the selected classifiers. A classifier can own several metrics.

Consider some subset S of metrics. If one classifier is responsible for all metrics in S, the best possible contribution of that group is

f(S) = max over classifiers i of sum over j in S of a[i][j].

Why does this formula work? Once we decide that classifier i is responsible for all metrics in S, its contribution is exactly the sum of its values on S. We should choose the classifier with the largest such sum.

Now the original problem has changed shape. Instead of choosing classifiers directly, we partition the K metrics into M nonempty groups. For each group S, we receive f(S). The total value of a partition is the sum of f(S) over all groups.

The brute-force works because every possible classifier set is considered explicitly, but fails when N is large. The observation that K metrics can be assigned to their responsible classifiers lets us move the exponential part from N to K.

There is one more useful property. If a partition has fewer than K groups, splitting any group into two nonempty groups cannot decrease its value. For disjoint A and B,

f(A ∪ B) <= f(A) + f(B),

because the left side chooses one classifier for both parts, while the right side may choose different classifiers. Thus, when M < K, an optimum using at most M classifiers can be represented using exactly M nonempty metric groups. When M >= K, every metric can have its own group, so the unconstrained optimum is simply the sum of the individual metric maxima.

For every metric mask we first calculate f(mask) and remember one classifier achieving it. Then we solve a set-partition DP. Let dp[t][mask] be the maximum value obtained by partitioning the metrics in mask into exactly t nonempty groups. To avoid considering the same partition in different orders, when processing mask we force the group containing the least significant set bit of mask to be chosen first.

The transition is

dp[t][mask] = max f[sub] + dp[t-1][mask \ sub],

where sub is a nonempty subset of mask containing its least significant bit.

There are O(3^K) subset pairs in the usual subset DP. Forcing the least significant bit into the chosen group removes the ordering symmetry and gives O(3^(K-1)) transitions per DP layer.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(C(N,M)K) | O(NK) | Too slow |
| Optimal | O(NK2^K + M3^(K-1)) | O(NK + M2^K) | Accepted algorithm |

The exponential dependence is only on K, which is at most 15. The Python implementation below uses the same exact algorithm, with compact arrays and the least-significant-bit optimization. The 3-second limit is tight for Python on the largest adversarial instances, so C++ is the safer implementation language for the original contest limit.

## Algorithm Walkthrough

1. Read all classifier rows and keep their original 1-based indices. The rows are never reordered in a way that would affect the required output indices.
2. If M equals N, select every classifier immediately. There is no choice, so the usefulness is simply the coordinate-wise maximum over all N rows.
3. If M is at least K, compute the best classifier independently for each metric. Selecting all these winners gives the maximum possible value because there are at most K different winners. If fewer than M distinct classifiers were selected, append arbitrary unused classifiers. Adding classifiers cannot decrease any metric maximum, so the usefulness stays optimal.
4. Otherwise M < K. For every nonempty metric mask, compute f(mask), the maximum sum of the metrics in that mask over all classifiers. At the same time, remember which classifier achieves this maximum.
5. Compute the subset sum of every mask for each classifier. If the least significant set bit of mask is b, then the sum for mask is the sum for mask without that bit plus the classifier's value at metric b. This gives all subset sums for one classifier in O(2^K) time.
6. Initialize the first DP layer with dp[1][mask] = f(mask). One group containing all metrics in mask has exactly this value.
7. For every t from 2 through M, compute dp[t]. For a fixed mask, let b be its least significant set bit. The group containing b is uniquely determined in any unordered partition. Enumerate its possible mask sub among all submasks containing b, and combine f(sub) with dp[t-1][mask \ sub].
8. Store the selected submask for every DP state. This allows the optimal metric partition to be reconstructed after the final DP layer.
9. Start from the full metric mask and repeatedly take the stored submask. For each group, append the classifier remembered for that submask. The resulting classifier list may contain the same classifier more than once because two groups can have the same best classifier.
10. Remove duplicate classifier indices. If fewer than M distinct indices remain, append arbitrary unused classifiers. The value cannot decrease during this padding because every metric maximum is monotone when classifiers are added.
11. Print the DP optimum and the resulting M distinct classifier indices.

Why it works

Fix an optimal set of classifiers and assign every metric to one classifier attaining its maximum. This produces a partition of the metrics. For each part S of this partition, its responsible classifier contributes at most f(S), and f(S) is attainable by definition. Hence the value of the optimal classifier set is represented by some metric partition whose DP value is exactly the optimum.

Conversely, every DP partition chooses one classifier for every metric group. Taking those classifiers produces at least the sum of the corresponding f values as its metric maxima, because the classifier chosen for a group realizes f for every metric in that group. Thus every DP solution corresponds to a valid classifier set with at least the DP value.

The two directions show that the DP optimum equals the original optimum. Removing duplicate classifiers cannot lower the represented value, because merging two groups assigned to the same classifier only combines metrics that the same classifier already provides. Padding with additional classifiers also cannot lower the value. Hence the final set contains exactly M distinct classifiers and remains optimal.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m, k = map(int, input().split())
    a = [list(map(int, input().split())) for _ in range(n)]

    # If all classifiers have to be selected, there is no optimization.
    if m == n:
        mx = [0] * k
        for row in a:
            for j, x in enumerate(row):
                if x > mx[j]:
                    mx[j] = x

        ans = sum(mx)
        print(ans)
        print(*range(1, n + 1))
        return

    # If we can use at least K classifiers, give every metric
    # its own best classifier and then pad the answer.
    if m >= k:
        mx = [0] * k
        winner = [-1] * k

        for i, row in enumerate(a):
            for j, x in enumerate(row):
                if x > mx[j]:
                    mx[j] = x
                    winner[j] = i

        chosen = []
        used = [False] * n

        for i in winner:
            if not used[i]:
                used[i] = True
                chosen.append(i)

        for i in range(n):
            if len(chosen) == m:
                break
            if not used[i]:
                used[i] = True
                chosen.append(i)

        print(sum(mx))
        print(*(x + 1 for x in chosen))
        return

    size = 1 << k
    full = size - 1

    # For each mask:
    # best[mask] = maximum sum of metrics in mask for one classifier
    # who[mask]  = classifier attaining best[mask]
    best = [0] * size
    who = [-1] * size

    # Precompute the least significant bit information.
    prev_mask = [0] * size
    bit_index = [0] * size
    popcount = [0] * size

    for mask in range(1, size):
        lb = mask & -mask
        prev_mask[mask] = mask ^ lb
        bit_index[mask] = lb.bit_length() - 1
        popcount[mask] = popcount[prev_mask[mask]] + 1

    # Compute f(mask) for every mask.
    subset_sum = [0] * size

    for i, row in enumerate(a):
        subset_sum[0] = 0

        for mask in range(1, size):
            subset_sum[mask] = (
                subset_sum[prev_mask[mask]] + row[bit_index[mask]]
            )

        for mask in range(1, size):
            value = subset_sum[mask]
            if value > best[mask]:
                best[mask] = value
                who[mask] = i

    # parent[t][mask] stores the group chosen for the transition
    # dp[t][mask] = best partition of mask into exactly t groups.
    parent = [None] * (m + 1)

    prev = best[:]
    parent[1] = [-1] * size

    for t in range(2, m + 1):
        cur = [-1] * size
        par = [-1] * size

        for mask in range(1, size):
            if popcount[mask] < t:
                continue

            lb = mask & -mask
            rest_mask = mask ^ lb

            # The selected group must contain lb.
            # Its complement is rest.
            rest = rest_mask

            while True:
                if popcount[rest] >= t - 1:
                    sub = mask ^ rest
                    value = best[sub] + prev[rest]

                    if value > cur[mask]:
                        cur[mask] = value
                        par[mask] = sub

                if rest == 0:
                    break
                rest = (rest - 1) & rest_mask

        prev = cur
        parent[t] = par

    answer = prev[full]

    # Reconstruct the metric groups.
    groups = []
    mask = full

    for t in range(m, 1, -1):
        sub = parent[t][mask]
        groups.append(sub)
        mask ^= sub

    groups.append(mask)

    # Convert metric groups into classifier indices.
    chosen = []
    used = [False] * n

    for sub in groups:
        i = who[sub]
        if not used[i]:
            used[i] = True
            chosen.append(i)

    # Duplicate winners can occur. Pad with arbitrary classifiers.
    for i in range(n):
        if len(chosen) == m:
            break
        if not used[i]:
            used[i] = True
            chosen.append(i)

    print(answer)
    print(*(i + 1 for i in chosen))

if __name__ == "__main__":
    solve()
```

The first branch handles M = N before any exponential work. Since every classifier is mandatory, computing the coordinate-wise maximum is sufficient.

The second branch handles M >= K. Each metric needs only one classifier to realize its maximum, so at most K classifiers are initially necessary. Because additional classifiers cannot reduce a maximum, arbitrary unused classifiers can safely fill the set to size M.

The main branch is used only when M < K. `size` is 2^K, and every integer mask represents a subset of metrics. `prev_mask`, `bit_index`, and `popcount` are precomputed because these operations occur inside the exponential loops.

The `subset_sum` array is reused for every classifier. For one classifier, every subset sum is obtained from a smaller subset by adding one metric. Thus the array never needs to be stored for all N classifiers simultaneously.

The DP uses `-1` as the impossible-state marker. All actual values are positive, so `-1` cannot be confused with a valid partition value.

The least significant bit restriction is the key detail in the transition. Without it, the same partition would be considered once for every ordering of its groups. Requiring the first group to contain the lowest set bit gives each unordered partition exactly one representation.

The reconstruction uses the stored submask rather than trying to recover groups from their values. This avoids ambiguity when several partitions have the same usefulness.

Python's integers safely handle the maximum possible answer, which is K · 10^8, or 1.5 · 10^9. No explicit 64-bit type is required.

## Worked Examples

### Sample 1

The input is

```
6 2 3
4 1 1
1 4 1
1 1 4
1 3 3
3 1 3
3 3 1
```

There are three metrics, so the masks are 1 through 7. For example, mask 5 represents metrics 1 and 3. The value f(5) is the maximum of `a[i][1] + a[i][3]`.

Some relevant states are:

| Mask | Metrics | f(mask) | Best classifier |
| --- | --- | --- | --- |
| 1 | {1} | 4 | 1 |
| 2 | {2} | 4 | 2 |
| 3 | {1,2} | 5 | 1 |
| 4 | {3} | 4 | 3 |
| 5 | {1,3} | 6 | 4 |
| 6 | {2,3} | 6 | 4 |
| 7 | {1,2,3} | 7 | 4 |

With two groups, the full mask 7 can be split into several possibilities:

| First group | Remaining group | Value |
| --- | --- | --- |
| {1} | {2,3} | 4 + 6 = 10 |
| {2} | {1,3} | 4 + 6 = 10 |
| {1,2} | {3} | 5 + 4 = 9 |

The optimum is 10. One optimal partition is `{1} | {2,3}`, whose representative classifiers are 1 and 4.

The resulting classifier values are `(4,3,3)`, so the usefulness is 10.

```
10
1 4
```

This trace demonstrates why the DP partitions metrics rather than classifiers. Classifier 1 supplies metric 1, while classifier 4 supplies both metrics 2 and 3.

### Sample 2

The input is

```
3 3 2
10 10
5 5
1 1
```

Here M = 3 and K = 2, so M >= K. We do not need the partition DP.

The best value for metric 1 is 10, attained by classifier 1. The best value for metric 2 is also 10, attained by classifier 1.

| Metric | Maximum | Winner |
| --- | --- | --- |
| 1 | 10 | 1 |
| 2 | 10 | 1 |

Only classifier 1 is initially needed, but exactly three classifiers must be printed. Classifiers 2 and 3 are appended as padding.

The usefulness remains 20 because adding classifiers cannot reduce either maximum.

```
20
1 2 3
```

This example exercises the special M >= K branch and the requirement to output exactly M distinct classifier indices.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(NK2^K + M3^(K-1)) | Every classifier contributes all metric masks, followed by M subset-partition DP layers |
| Space | O(NK + M2^K) | The input matrix, DP parent layers, and auxiliary mask arrays are stored |

For K = 15, there are only 32768 metric masks. The first term is about N · K · 32768 operations, while the partition DP is the dominant part when M is close to K. The small K bound is what makes the exponential algorithm possible; an exponential dependence on N would be completely infeasible for N = 2000.

The algorithm itself is the appropriate exact solution for the given constraints. The Python implementation uses several low-level optimizations, but the original 3-second limit is particularly demanding for Python on worst-case inputs. A C++ implementation of the same DP is the safer contest submission.

## Test Cases

The following harness assumes the `solve` function from the solution is placed in the same file. It redirects standard input and output so that the actual competitive-programming implementation is tested rather than a separate reimplementation.

```python
import sys
import io
import contextlib

def run(inp: str) -> str:
    old_stdin = sys.stdin
    try:
        sys.stdin = io.StringIO(inp)
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            solve()
        return out.getvalue().strip()
    finally:
        sys.stdin = old_stdin

def check_output(inp: str, out: str):
    data = list(map(int, inp.split()))
    n, m, k = data[0], data[1], data[2]

    values = []
    p = 3
    a = []
    for _ in range(n):
        row = data[p:p + k]
        p += k
        a.append(row)

    tokens = list(map(int, out.split()))
    assert len(tokens) == m + 1

    answer = tokens[0]
    ids = tokens[1:]

    assert len(set(ids)) == m
    assert all(1 <= x <= n for x in ids)

    mx = [0] * k
    for idx in ids:
        row = a[idx - 1]
        for j in range(k):
            mx[j] = max(mx[j], row[j])

    assert sum(mx) == answer
    return answer

sample1 = """\
6 2 3
4 1 1
1 4 1
1 1 4
1 3 3
3 1 3
3 3 1
"""

sample2 = """\
3 3 2
10 10
5 5
1 1
"""

assert run(sample1) == "10\n1 4", "sample 1"
assert run(sample2) == "20\n1 2 3", "sample 2"

case_min = """\
1 1 1
100000000
"""
assert run(case_min) == "100000000\n1", "minimum-size case"

case_m_one = """\
2 1 2
10 1
1 10
"""
assert run(case_m_one) == "11\n1", "M = 1"

case_all_equal = """\
4 2 2
5 5
5 5
5 5
5 5
"""
assert run(case_all_equal) == "10\n1 2", "all equal values"

case_forced_all = """\
3 3 3
1 2 3
3 2 1
2 3 2
"""
assert run(case_forced_all) == "8\n1 2 3", "M = N"

case_max_n = "2000 2000 15\n" + ("1 1 1 1 1 1 1 1 1 1 1 1 1 1 1\n" * 2000)
out = run(case_max_n)
assert check_output(case_max_n, out) == 15, "large N"

print("all tests passed")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 1 / 100000000` | `100000000 / 1` | Minimum N, M, and K, plus the largest metric value |
| `2 1 2 / 10 1 / 1 10` | `11 / 1` | M = 1, preventing independent selection of metric winners |
| Four identical rows with M = 2 | `10 / 1 2` | Ties and exact-size padding |
| `3 3 3` with three different rows | `8 / 1 2 3` | M = N, where the whole set is forced |
| 2000 identical rows, M = N, K = 15 | `15 / 1 ... 2000` | Maximum N and large output, while exercising the M = N shortcut |

## Edge Cases

For M = 1, consider

```
2 1 2
10 1
1 10
```

The main DP has only one group. The full metric mask is `{1,2}`, and f({1,2}) is max(11, 11) = 11. Classifier 1 is selected by the deterministic tie rule. The result is 11 with classifier 1. The algorithm never combines the independent maxima 10 and 10 because doing that would require two groups, which violates M = 1.

For M >= K, consider

```
3 3 2
10 10
5 5
1 1
```

The individual metric maxima are both 10 and both belong to classifier 1. The initial chosen list contains only classifier 1. The padding loop then adds classifiers 2 and 3. The resulting set has exactly three distinct indices and still has usefulness 20.

For M = N, consider

```
3 3 3
1 2 3
3 2 1
2 3 2
```

Every classifier must be selected, so the algorithm immediately computes coordinate-wise maxima `(3,3,3)`. Their sum is 8, and it outputs all three indices. No partition is necessary.

For all equal values,

```
4 2 2
5 5
5 5
5 5
5 5
```

every classifier is optimal for every metric. The first classifier wins both metric maxima, after which the padding step chooses classifier 2. The resulting usefulness is still 10. This demonstrates that the algorithm does not depend on unique maxima.

For a group whose best classifier is also best for another group, consider

```
3 2 3
10 10 10
9 1 1
1 9 1
```

The partition `{1,2,3}` would use classifier 1 and has value 30, while a two-group partition such as `{1} | {2,3}` also gives 30 because classifier 1 is the best representative for both groups. During reconstruction, both groups may produce classifier 1. The duplicate is removed, leaving one classifier, and another unused classifier is added to reach M = 2. The usefulness remains 30, which is optimal.

For large N with M = N, the special branch is especially useful. With 2000 classifiers and 15 metrics, selecting everyone is forced, so the algorithm only performs O(NK) work. A generic metric-partition DP would be unnecessary overhead in this case.

The most subtle boundary is M < K. Here the independent maximum of every metric is generally unattainable because it can require more than M classifiers. The partition DP explicitly captures this restriction by forcing the K metrics into exactly M groups, with one classifier responsible for each group.

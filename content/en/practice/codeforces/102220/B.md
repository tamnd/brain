---
title: "CF 102220B - Balanced Diet"
description: "We have (m) sweet types and (n) individual sweets. Each sweet has a positive value (ai) and belongs to a type (bi). For every type (j), there is a threshold (lj). If we buy any sweets of that type, we must buy at least (lj) of them. Buying zero is also allowed."
date: "2026-08-19T00:14:44+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102220
codeforces_index: "B"
codeforces_contest_name: "The 13th Chinese Northeast Collegiate Programming Contest"
rating: 0
weight: 102220
solve_time_s: 284
verified: true
draft: false
---

[CF 102220B - Balanced Diet](https://codeforces.com/problemset/problem/102220/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 4m 44s  
**Verified:** yes  

## Solution
## Problem Understanding

We have (m) sweet types and (n) individual sweets. Each sweet has a positive value (a_i) and belongs to a type (b_i). For every type (j), there is a threshold (l_j). If we buy any sweets of that type, we must buy at least (l_j) of them. Buying zero is also allowed.

For a chosen set, let (S) be the sum of all bought values, and let (C) be the largest number of bought sweets belonging to any one type. The score is (S/C). We need the maximum possible score, represented as a reduced fraction.

The constraints make the intended structure quite clear. A test case can contain (10^5) sweets, while the sums of (n) and (m) over all test cases are at most (10^6). An (O(n^2)) or exponential algorithm is immediately impossible. Even an (O(nm)) method can reach (10^{10}) operations in one large case. We need roughly (O(n\log n+m)), with the logarithmic factor coming from sorting.

There are several edge cases that can make a seemingly reasonable solution incorrect. First, a type whose threshold is larger than its number of available sweets cannot contribute at all. For example,

```
1
2 1
2
5 1
1 1
```

The only valid choice is both sweets, so the answer is (6/2=3/1). Taking only the value-5 sweet would give a larger numerical score, but that selection violates the threshold.

A second edge case is (l_j=1). In that situation, we may take any positive number of sweets from the type, including all of them. For example,

```
1
3 2
1 3
10 1
9 1
1 2
```

Taking the value-10 sweet alone gives (10/1), which is optimal. A solution that assumes every selected type must contribute exactly its threshold would miss this possibility.

A third subtlety is that a parameter (k) used during the optimization does not necessarily have to be the actual maximum count of the resulting set. For example,

```
1
2 2
1 1
10 1
1 2
```

For (k=2), we can take both sweets and obtain (11/2) when we divide by the imposed bound (k), even though the actual maximum count is only (1). The same set has score (11/1), which is considered when (k=1). Thus we are allowed to optimize under the condition that every type has at most (k) selected sweets, rather than insisting that some type has exactly (k).

## Approaches

The brute-force approach is straightforward. We could enumerate every subset of the (n) sweets, count how many sweets of each type it contains, reject subsets violating a threshold, compute (S), compute (C), and maximize (S/C). This is correct because every possible purchase is represented by exactly one subset. Unfortunately, there are (2^n) subsets, which is already about (10^{30103}) when (n=100000). Even before considering the work needed to evaluate each subset, this is completely infeasible.

The useful way to reorganize the problem is to stop choosing individual subsets and instead fix the denominator. Suppose we decide that no type may contribute more than (k) sweets. Consider one type containing (s) sweets, sorted by value from largest to smallest as (v_1,v_2,\ldots,v_s).

If (s<l), this type can never be selected, because selecting even one sweet would violate the minimum. If (s\ge l) but (k<l), the type also cannot be selected under the current bound (k). If (l\le k), the best choice is to take the largest (\min(k,s)) values. All values are positive, so there is never a reason to discard a permitted high-value sweet.

Let (F(k)) be the maximum total value obtainable when every type contributes at most (k) sweets. For a type with sorted values (v_1,\ldots,v_s), its contribution is

[
0 \quad\text{for } k<l,
]

and

[
v_1+\cdots+v_k
]

for (l\le k\le s, while it is the total sum of the type for (k>s).

The remaining problem is to calculate (F(k)) for every (k) without repeatedly summing prefixes. The key observation is that the contribution changes very simply as (k) increases. At (k=l), the type suddenly contributes the first (l) largest values. When (k) increases from (k-1) to (k), the contribution increases by exactly (v_k), until all sweets of the type have been included.

So for every type we can add its changes into an array. If its threshold is (l), we add the sum of its largest (l) values to `gain[l]`. For every later position (k), up to the size of the type, we add (v_k) to `gain[k]`. A prefix sum over `gain` then gives (F(k)) for every (k).

We only need to sort the sweets by type and then by decreasing value. The total number of per-sweet operations is linear after sorting.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(2^n n)) | (O(n)) | Too slow |
| Optimal | (O(n\log n+m+n)) | (O(n+m)) | Accepted |

## Algorithm Walkthrough

1. Read the threshold (l_j) for every type. Store the thresholds so that the threshold of a type can be obtained immediately while processing its sweets.
2. Sort all sweets by type, and inside each type sort by decreasing value. This puts every type into one contiguous segment, with its most valuable sweets first. We do not need to construct separate Python lists for all (m) types, which is useful because (m) can also be (10^5).
3. Create an array `gain`, where `gain[k]` represents the increase in (F(k)) when the allowed maximum count changes from (k-1) to (k).
4. Process one type at a time. Suppose its sorted values are (v_1,\ldots,v_s), and its threshold is (l). Maintain a running prefix sum.
5. When the number of processed sweets reaches (l), add the current prefix sum to `gain[l]`. This is the first point where the type becomes selectable, so its entire best valid contribution appears at once.
6. For every subsequent sweet (v_k), add (v_k) to `gain[k]` while (k\le s). Increasing the allowed count from (k-1) to (k) lets us take exactly this next-largest sweet from the type.
7. Ignore a type whose number of available sweets is smaller than its threshold. There is no valid positive selection from such a type, so it contributes nothing for every (k).
8. Convert `gain` into (F) by taking prefix sums. After this operation, `gain[k]` is effectively (F(k)), the best total value under a maximum-per-type count of (k).
9. Examine every (k) from (1) to (n). Compare (F(k)/k) with the best fraction found so far using cross multiplication, so no floating-point arithmetic is needed.
10. Reduce the best numerator and denominator by their greatest common divisor and print the resulting fraction.

### Why it works

Fix any positive integer (k). A valid selection whose every type appears at most (k) times can be optimized independently by type because there are no interactions between the values of different types except for the common upper bound (k). For a type with at least (l) available sweets, selecting fewer than (l) is forbidden, while selecting more than (k) is forbidden. Since every value is positive, the best permitted count is (\min(k,s)), and the best sweets are exactly the largest ones.

The `gain` construction represents precisely how this optimal contribution changes as (k) grows. Before (l), the contribution is zero. At (l), the first (l) values become available together. Each later increase of (k) adds the next-largest value. Thus the prefix sum of `gain` is exactly (F(k)).

Now consider an optimal purchase with actual maximum count (C). It is feasible under the bound (k=C), so (F(C)) is at least its total value. Hence (F(C)/C) is at least the optimal score. Conversely, a set constructed under bound (k) has actual maximum count at most (k), so its real score is at least (F(k)/k). Checking all (k) therefore cannot miss the optimum and cannot produce a value larger than the true optimum.

## Python Solution

```python
import sys
from math import gcd

input = sys.stdin.readline

MAX_A = 100_000_000
SHIFT = 27

def solve():
    t = int(input())
    out = []

    for _ in range(t):
        n, m = map(int, input().split())
        need = [0] + list(map(int, input().split()))

        # Encode (type, value) into one integer.
        # Higher bits contain the type.
        # Lower bits contain MAX_A - value, so sorting ascending
        # gives the values of each type in decreasing order.
        sweets = [0] * n
        for i in range(n):
            a, b = map(int, input().split())
            sweets[i] = (b << SHIFT) | (MAX_A - a)

        sweets.sort()

        gain = [0] * (n + 1)

        i = 0
        while i < n:
            type_id = sweets[i] >> SHIFT
            limit = need[type_id]

            j = i + 1
            while j < n and (sweets[j] >> SHIFT) == type_id:
                j += 1

            prefix = 0
            count = 0

            for p in range(i, j):
                value = MAX_A - (sweets[p] & ((1 << SHIFT) - 1))
                count += 1
                prefix += value

                if count == limit:
                    gain[count] += prefix
                elif count > limit:
                    gain[count] += value

            i = j

        # gain[k] is the increment when changing the bound
        # from k-1 to k. Convert it to F(k).
        for k in range(1, n + 1):
            gain[k] += gain[k - 1]

        best_num = gain[1]
        best_den = 1

        for k in range(2, n + 1):
            if gain[k] * best_den > best_num * k:
                best_num = gain[k]
                best_den = k

        d = gcd(best_num, best_den)
        out.append(f"{best_num // d}/{best_den // d}")

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The threshold array is indexed by type, so `need[type_id]` gives the minimum number of sweets that must be taken if that type is used. A type with too few sweets naturally never reaches its threshold during the inner loop, so it contributes nothing.

The integer encoding is used to avoid storing (n) Python tuples. The type occupies the high bits, while `MAX_A - value` occupies the low 27 bits. Since (10^8<2^{27}), the value fits safely in those low bits. Sorting the encoded integers consequently sorts first by type and then by decreasing value.

For each contiguous type segment, `prefix` is the sum of the currently largest sweets. At exactly `limit`, the type becomes selectable, so the whole prefix is added to `gain[limit]`. Every later sweet contributes only its own value because the previous prefix was already accounted for.

The second pass turns increments into actual values of (F(k)). Fraction comparison uses `gain[k] * best_den > best_num * k`, which is exact. The largest possible total value is at most (10^6\cdot10^8=10^{14}), so Python integers easily handle all arithmetic.

## Worked Examples

For Sample 1, there is one type with threshold (2), containing values (7) and (2). The type becomes usable at (k=2), where its contribution is (9).

| k | Processed values | gain[k] before prefix | F(k) | F(k)/k |
| --- | --- | --- | --- | --- |
| 1 | 7 | 0 | 0 | 0 |
| 2 | 7, 2 | 9 | 9 | 9/2 |

The maximum is (9/2). The transition at (k=2) demonstrates why the threshold contribution is added as the entire prefix rather than only the last value.

For Sample 2, type 1 has threshold (1) and value (2). Type 2 has threshold (2) and values (5,3,1). After sorting, type 2 is processed as (5,3,1).

| k | Type 1 gain | Type 2 gain | F(k) | F(k)/k |
| --- | --- | --- | --- | --- |
| 1 | 2 | 0 | 2 | 2 |
| 2 | 0 | 8 | 10 | 5 |
| 3 | 0 | 1 | 11 | 11/3 |

The best value is (5). The corresponding purchase contains the type-1 sweet worth (2) and the two best type-2 sweets worth (5) and (3), giving total value (10) and maximum type count (2).

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(n\log n+m+n)) | Sorting dominates, while grouping, gain construction, prefix sums, and fraction comparisons are linear |
| Space | (O(n+m)) | The encoded sweets, threshold array, and gain array each use linear space |

The largest test cases contain (10^5) sweets, and the total number of sweets over all test cases is at most (10^6). The algorithm performs one global sort per test case and then only linear scans. The memory usage stays within the stated 512 MB limit, while Python's arbitrary-precision integers safely handle totals around (10^{14}).

## Test Cases

```python
import sys
import io
from math import gcd

MAX_A = 100_000_000
SHIFT = 27

def solve():
    input = sys.stdin.readline
    t = int(input())
    out = []

    for _ in range(t):
        n, m = map(int, input().split())
        need = [0] + list(map(int, input().split()))

        sweets = [0] * n
        for i in range(n):
            a, b = map(int, input().split())
            sweets[i] = (b << SHIFT) | (MAX_A - a)

        sweets.sort()

        gain = [0] * (n + 1)
        mask = (1 << SHIFT) - 1

        i = 0
        while i < n:
            type_id = sweets[i] >> SHIFT
            limit = need[type_id]

            j = i + 1
            while j < n and (sweets[j] >> SHIFT) == type_id:
                j += 1

            prefix = 0
            count = 0

            for p in range(i, j):
                value = MAX_A - (sweets[p] & mask)
                count += 1
                prefix += value

                if count == limit:
                    gain[count] += prefix
                elif count > limit:
                    gain[count] += value

            i = j

        for k in range(1, n + 1):
            gain[k] += gain[k - 1]

        best_num = gain[1]
        best_den = 1

        for k in range(2, n + 1):
            if gain[k] * best_den > best_num * k:
                best_num = gain[k]
                best_den = k

        d = gcd(best_num, best_den)
        out.append(f"{best_num // d}/{best_den // d}")

    sys.stdout.write("\n".join(out))

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    try:
        solve()
        return sys.stdout.getvalue()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

# Provided samples
sample = """\
2
2 1
2
7 1
2 1
3 2
1 2
2 1
5 2
3 2
"""
assert run(sample) == "9/2\n5/1", "provided samples"

# Minimum-size input
assert run("""\
1
1 1
1
7 1
""") == "7/1", "minimum size"

# A type cannot be partially selected when its threshold is 2
assert run("""\
1
2 1
2
5 1
1 1
""") == "3/1", "threshold boundary"

# All values are equal and every type can be selected from one sweet upward
assert run("""\
1
4 2
1 1
7 1
7 1
7 2
7 2
""") == "14/1", "all equal values"

# The first valid k is exactly the threshold.
# Values are 10, 9, 1 and l = 2, so F(2) = 19.
assert run("""\
1
3 1
2
10 1
9 1
1 1
""") == "19/2", "off by one at threshold"

# Maximum n and m. Every type has exactly one sweet and l = 1.
# All sweets can be selected, while C = 1.
n = 100000
m = 100000
thresholds = " ".join(["1"] * m)
items = "\n".join(f"1 {i}" for i in range(1, m + 1))
maximum_case = f"1\n{n} {m}\n{thresholds}\n{items}\n"

assert run(maximum_case) == "100000/1", "maximum-size case"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 1 1 / 1 / 7 1` | `7/1` | Minimum-size input and denominator (1) |
| `2 1 / l=2 / values 5,1` | `3/1` | A type cannot be partially selected |
| Four equal values split across two types with (l=1) | `14/1` | All-equal values and taking every available sweet |
| One type, values (10,9,1), (l=2) | `19/2` | Exact threshold transition and off-by-one handling |
| (n=m=100000), one value per type, all (l=1) | `100000/1` | Maximum-size input and linear postprocessing |

## Edge Cases

When a type has fewer available sweets than its threshold, the algorithm never reaches `count == limit`, so its `gain` contribution remains zero. For

```
1
2 1
2
5 1
1 1
```

the only type has two sweets and threshold two. At `count=1`, nothing is added. At `count=2`, the prefix is (5+1=6), so `gain[2]=6`. The resulting (F(2)=6), giving (6/2=3/1). A single sweet is never considered valid.

When (l=1), the first sweet immediately creates a contribution at `gain[1]`, and every later sweet adds its own value to the corresponding larger (k). For

```
1
3 2
1 3
10 1
9 1
1 2
```

type 1 contributes (10) at (k=1), while type 2 cannot contribute until (k=3). Thus (F(1)=10), and the answer is (10/1). The algorithm correctly allows the first type to be selected without forcing any additional sweets.

When the chosen set has actual maximum count smaller than the current bound (k), the calculation still remains safe. Consider

```
1
2 2
1 1
10 1
1 2
```

For (k=2), both types can contribute one sweet, so (F(2)=11), producing the candidate (11/2). The actual selected set has maximum count (1), so its true score is (11/1). The algorithm also evaluates (k=1), where (F(1)=11), and consequently finds the correct answer (11/1). The bound (k) is only a device for enumerating possibilities, not a claim that some type must contain exactly (k) sweets.

Finally, the threshold transition itself must be handled without an off-by-one error. For

```
1
3 1
2
10 1
9 1
1 1
```

the sorted values are (10,9,1). At (k=1), the type is unavailable because its threshold is (2), so (F(1)=0). At (k=2), the prefix (10+9=19) is added at once, giving (F(2)=19). At (k=3), only the extra value (1) is added, giving (F(3)=20). The ratios are (0), (19/2), and (20/3), so the answer is (19/2). This is exactly the behavior encoded by adding the whole prefix at the threshold and only the next individual value afterward.

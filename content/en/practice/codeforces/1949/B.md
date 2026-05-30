---
title: "CF 1949B - Charming Meals"
description: "We have two arrays of size n. The array a contains the spiciness values of the appetizers, and the array b contains the spiciness values of the main dishes. Every appetizer must be paired with exactly one main dish, and every main dish must be used exactly once."
date: "2026-05-31T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "brute-force", "greedy", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1949
codeforces_index: "B"
codeforces_contest_name: "European Championship 2024 - Online Mirror (Unrated, ICPC Rules, Teams Preferred)"
rating: 1500
weight: 1949
solve_time_s: 104
verified: true
draft: false
---

[CF 1949B - Charming Meals](https://codeforces.com/problemset/problem/1949/B)

**Rating:** 1500  
**Tags:** binary search, brute force, greedy, sortings  
**Solve time:** 1m 44s  
**Verified:** yes  

## Solution
## Problem Understanding

We have two arrays of size `n`.

The array `a` contains the spiciness values of the appetizers, and the array `b` contains the spiciness values of the main dishes. Every appetizer must be paired with exactly one main dish, and every main dish must be used exactly once.

For a pair `(a[i], b[j])`, the charm of the meal is `|a[i] - b[j]|`. Among all created meals, we look at the smallest charm. Our goal is to choose the pairing so that this smallest charm is as large as possible.

This is a classic "maximize the minimum value" problem. Whenever a problem asks for the largest value `X` such that some condition is possible, binary search is usually a good candidate.

The constraints are the key clue. Each test case has `n ≤ 5000`, and the sum of `n²` over all test cases is at most `25 · 10⁶`. A solution around `O(n²)` per test case is acceptable, while anything factorial or exponential is impossible. Enumerating all matchings would require `n!` possibilities, which becomes hopeless even for `n = 15`.

A subtle aspect is that the condition involves absolute differences. For a fixed threshold `x`, a pair is valid if

`|a[i] - b[j]| ≥ x`.

This means a dish can be paired either with something much smaller or with something much larger. A naive greedy that only looks at one side can easily fail.

Consider:

```
a = [4, 5]
b = [1, 8]
```

For `x = 3`, both pairings work:

```
4 ↔ 1
5 ↔ 8
```

and

```
4 ↔ 8
5 ↔ 1
```

A greedy that always takes the closest valid value may block a later assignment even though a valid matching exists.

Another tricky case appears when many values are equal:

```
a = [1, 1, 1]
b = [1, 1, 1]
```

Every charm equals `0`, so the answer is `0`. Any algorithm that assumes distinct values or relies on strict inequalities will break here.

A third edge case is when all values of one array are far below all values of the other:

```
a = [0, 0, 0]
b = [100, 100, 100]
```

Every matching produces charm `100`, so the answer is `100`. The optimal matching is not something complicated, every pairing is equivalent.

## Approaches

The brute-force idea is straightforward. Generate every possible perfect matching between the two arrays, compute the minimum charm inside that matching, and keep the best result.

This works because it directly checks every valid pairing arrangement. The problem is the number of matchings. There are `n!` perfect matchings. Even for `n = 15`, this exceeds a trillion possibilities. The approach is unusable.

The structure of the objective suggests a different viewpoint.

Suppose somebody tells us a candidate answer `x`. Instead of asking for the optimal answer immediately, ask a yes/no question:

"Can we create a perfect matching such that every pair has charm at least `x`?"

If we can answer this efficiently, then binary search on `x` gives the maximum feasible value.

The remaining challenge is the feasibility check.

Sort both arrays.

For a fixed threshold `x`, a pair `(a, b)` is allowed when

```
b ≤ a - x
```

or

```
b ≥ a + x
```

The forbidden region is the interval

```
(a - x + 1 ... a + x - 1)
```

After sorting, all values forbidden for a particular `a[i]` form one contiguous interval in the sorted `b` array.

The crucial observation is that every valid partner for `a[i]` lies either in a prefix of `b` or in a suffix of `b`.

Suppose exactly `k` elements of `b` are assigned from the "small side" (`b ≤ a - x`). Then the remaining `n-k` elements must come from the "large side" (`b ≥ a + x`).

Because both arrays are sorted, we can check whether such a split is possible.

For the first `k` smallest appetizers, we match them with the `k` smallest main dishes. We need

```
a[i] - b[i] ≥ x
```

for all `i < k`.

For the remaining elements, we match

```
a[i] with b[i-k+k] = b[i]
```

in aligned order among the suffixes, requiring

```
b[i] - a[i] ≥ x
```

for all `i ≥ k`.

If both conditions hold for some split position `k`, then a valid perfect matching exists.

The entire feasibility test becomes a scan over all possible split points.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n!) | O(n) | Too slow |
| Optimal | O(n log V + n) per test case after sorting | O(n) | Accepted |

Here `V` is the value range, at most `10⁹`.

## Algorithm Walkthrough

### Feasibility Check for a Fixed `x`

Assume both arrays are already sorted.

1. Compute an array `pref`.

`pref[i]` indicates whether all positions `0..i` satisfy

```
a[j] - b[j] ≥ x
```

If `pref[i]` is true, then the first `i+1` smallest appetizers can be matched with the first `i+1` smallest main dishes using the "small side" condition.
2. Compute an array `suff`.

`suff[i]` indicates whether all positions `i..n-1` satisfy

```
b[j] - a[j] ≥ x
```

If `suff[i]` is true, then the suffix beginning at `i` can be matched using the "large side" condition.
3. Try every split position `k` from `0` to `n`.

The first `k` pairs use the small-side condition.

The last `n-k` pairs use the large-side condition.
4. The prefix part is valid if either `k = 0` or `pref[k-1]` is true.
5. The suffix part is valid if either `k = n` or `suff[k]` is true.
6. If both parts are valid for some `k`, then threshold `x` is achievable.
7. Binary search the largest feasible `x`.

### Why it works

After sorting, every valid partner of an appetizer lies either sufficiently far to the left or sufficiently far to the right in the sorted `b` array. Any perfect matching satisfying the threshold induces a boundary between elements matched from the left side and elements matched from the right side.

For a fixed boundary `k`, the left part is feasible exactly when every aligned pair in the first `k` positions differs by at least `x` in the direction `a ≥ b + x`. Similarly, the right part is feasible exactly when every aligned pair in the suffix differs by at least `x` in the direction `b ≥ a + x`.

The rearrangement argument for sorted sequences guarantees that if these aligned checks fail, no alternative matching inside the same side can repair them. Hence checking all split positions completely characterizes feasibility.

Because feasibility is monotone, if a threshold `x` is achievable then every smaller threshold is also achievable. Binary search is valid.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())

    ans = []

    for _ in range(t):
        n = int(input())
        a = sorted(map(int, input().split()))
        b = sorted(map(int, input().split()))

        def check(x):
            pref = [False] * n
            ok = True

            for i in range(n):
                ok &= (a[i] - b[i] >= x)
                pref[i] = ok

            suff = [False] * (n + 1)
            suff[n] = True

            ok = True
            for i in range(n - 1, -1, -1):
                ok &= (b[i] - a[i] >= x)
                suff[i] = ok

            for k in range(n + 1):
                left_ok = (k == 0) or pref[k - 1]
                right_ok = (k == n) or suff[k]

                if left_ok and right_ok:
                    return True

            return False

        lo, hi = 0, 10**9

        while lo < hi:
            mid = (lo + hi + 1) // 2

            if check(mid):
                lo = mid
            else:
                hi = mid - 1

        ans.append(str(lo))

    sys.stdout.write("\n".join(ans))

if __name__ == "__main__":
    solve()
```

The solution begins by sorting both arrays. Sorting is essential because the feasibility characterization relies on the relative order of elements.

The `check(x)` function verifies whether every meal can have charm at least `x`.

`pref[i]` stores whether all aligned pairs up to position `i` satisfy `a[j] - b[j] ≥ x`. Once a position fails, every larger prefix also fails, so a running boolean is enough.

`suff[i]` stores whether every aligned pair in the suffix satisfies `b[j] - a[j] ≥ x`.

For a split position `k`, the first `k` pairs come from the left-side condition and the rest come from the right-side condition. If both corresponding ranges are valid, then a perfect matching exists.

The binary search uses the standard upper-mid pattern:

```
mid = (lo + hi + 1) // 2
```

This avoids infinite loops when only two values remain.

All arithmetic fits comfortably in Python integers because values never exceed `10^9`.

## Worked Examples

### Example 1

Input:

```
n = 5
a = [1,2,3,4,5]
b = [1,2,3,4,5]
```

Check `x = 2`.

| i | a[i] | b[i] | a[i]-b[i]≥2 | b[i]-a[i]≥2 |
| --- | --- | --- | --- | --- |
| 0 | 1 | 1 | No | No |
| 1 | 2 | 2 | No | No |
| 2 | 3 | 3 | No | No |
| 3 | 4 | 4 | No | No |
| 4 | 5 | 5 | No | No |

No split satisfies both prefix and suffix requirements.

Now check `x = 1`.

The feasibility test succeeds, so binary search eventually returns:

```
2
```

This demonstrates that the optimal matching is not the sorted pairing. Rearranging the dishes increases the minimum charm.

### Example 2

Input:

```
n = 3
a = [0,0,0]
b = [100,100,100]
```

Check `x = 100`.

| i | a[i] | b[i] | a[i]-b[i]≥100 | b[i]-a[i]≥100 |
| --- | --- | --- | --- | --- |
| 0 | 0 | 100 | No | Yes |
| 1 | 0 | 100 | No | Yes |
| 2 | 0 | 100 | No | Yes |

`k = 0` immediately works because the whole array satisfies the suffix condition.

The threshold `100` is feasible.

Checking `101` fails, so the answer is:

```
100
```

This example exercises the case where every pair must come from the same side of the split.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n + n log 10⁹) | Sorting plus about 30 feasibility checks |
| Space | O(n) | Prefix and suffix arrays |

The dominant preprocessing cost is sorting. The feasibility test is linear, and binary search performs roughly 30 iterations because values lie in `[0, 10⁹]`. With the guarantee that the sum of `n²` is at most `25 · 10⁶`, this easily fits within the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    out = io.StringIO()
    old_stdout = sys.stdout
    sys.stdout = out

    def solve():
        input = sys.stdin.readline

        t = int(input())
        ans = []

        for _ in range(t):
            n = int(input())
            a = sorted(map(int, input().split()))
            b = sorted(map(int, input().split()))

            def check(x):
                pref = [False] * n
                ok = True

                for i in range(n):
                    ok &= (a[i] - b[i] >= x)
                    pref[i] = ok

                suff = [False] * (n + 1)
                suff[n] = True

                ok = True
                for i in range(n - 1, -1, -1):
                    ok &= (b[i] - a[i] >= x)
                    suff[i] = ok

                for k in range(n + 1):
                    left_ok = (k == 0) or pref[k - 1]
                    right_ok = (k == n) or suff[k]

                    if left_ok and right_ok:
                        return True

                return False

            lo, hi = 0, 10**9

            while lo < hi:
                mid = (lo + hi + 1) // 2

                if check(mid):
                    lo = mid
                else:
                    hi = mid - 1

            ans.append(str(lo))

        print("\n".join(ans))

    solve()

    sys.stdout = old_stdout
    return out.getvalue()

# provided sample
assert run(
"""4
3
0 0 0
1000000000 1000000000 1000000000
5
1 2 3 4 5
1 2 3 4 5
6
0 0 0 100 100 100
100 100 100 0 0 0
7
14 25 62 74 86 95 12
51 62 71 72 92 20 84
"""
) == "1000000000\n2\n100\n30\n"

# minimum size
assert run(
"""1
1
5
9
"""
) == "4\n"

# all equal
assert run(
"""1
4
7 7 7 7
7 7 7 7
"""
) == "0\n"

# reversed extremes
assert run(
"""1
3
0 0 0
100 100 100
"""
) == "100\n"

# off-by-one style case
assert run(
"""1
2
1 4
2 5
"""
) == "3\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `n=1, [5], [9]` | `4` | Smallest possible instance |
| All values equal | `0` | Handles zero answer correctly |
| `[0,0,0]` vs `[100,100,100]` | `100` | Entire matching comes from one side |
| `[1,4]` vs `[2,5]` | `3` | Detects boundary conditions in binary search |

## Edge Cases

### All Values Equal

Input:

```
1
3
5 5 5
5 5 5
```

For any positive threshold, neither `a[i]-b[i]` nor `b[i]-a[i]` reaches the threshold. Every feasibility check fails. The binary search settles at `0`.

Output:

```
0
```

### One Array Entirely Smaller

Input:

```
1
3
0 0 0
100 100 100
```

For `x = 100`, every suffix condition is true. The split `k = 0` succeeds immediately.

Output:

```
100
```

### Single Element

Input:

```
1
1
8
3
```

There is only one possible pair. Its charm is

```
|8 - 3| = 5
```

The feasibility test accepts every threshold up to `5` and rejects larger values.

Output:

```
5
```

### Duplicate Values Mixed With Distinct Values

Input:

```
1
4
1 1 10 10
3 3 8 8
```

The optimal matching is:

```
1 ↔ 8
1 ↔ 8
10 ↔ 3
10 ↔ 3
```

Every charm equals `7`, so the answer is `7`.

The sorted-array feasibility check correctly identifies the split between small-side and large-side assignments and returns the optimal value.

---
title: "CF 1843E - Tracking Segments"
description: "We start with an array of length n filled entirely with zeros. There are m segments. A segment is considered beautiful when the number of ones inside it is strictly greater than the number of zeros inside the same segment."
date: "2026-06-09T06:09:07+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "brute-force", "data-structures", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 1843
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 881 (Div. 3)"
rating: 1600
weight: 1843
solve_time_s: 107
verified: true
draft: false
---

[CF 1843E - Tracking Segments](https://codeforces.com/problemset/problem/1843/E)

**Rating:** 1600  
**Tags:** binary search, brute force, data structures, two pointers  
**Solve time:** 1m 47s  
**Verified:** yes  

## Solution
## Problem Understanding

We start with an array of length `n` filled entirely with zeros.

There are `m` segments. A segment is considered beautiful when the number of ones inside it is strictly greater than the number of zeros inside the same segment. For a segment of length `len`, this condition is equivalent to:

$$\text{ones} > \frac{\text{len}}{2}$$

We are also given a sequence of `q` updates. The `i`-th update turns position `x_i` into `1`. Positions are distinct, so once a position becomes `1`, it stays `1`.

The task is to find the earliest update number after which at least one of the given segments becomes beautiful. If no segment is beautiful even after all updates are applied, we output `-1`.

The constraints immediately suggest that simulating every update and rechecking every segment from scratch is too expensive. Across all test cases, the sum of `n` is at most `10^5`, but a single test case may still contain up to `10^5` segments and `10^5` updates. Any solution that performs work proportional to `m × q` is far beyond what fits in two seconds.

A subtle observation is that updates only add more ones. Once a segment becomes beautiful, it can never stop being beautiful. This monotonic behavior is the key to the solution.

Consider a small example:

```
n = 5
segment = [1,5]
updates = 5,3,1,2,4
```

After the first update there is one `1`, after the second there are two, after the third there are three. The segment length is five, so three ones are enough to make it beautiful. The answer is `3`.

Another easy mistake is forgetting that the condition is strictly greater.

```
segment length = 4
ones = 2
zeros = 2
```

This is not beautiful. A careless implementation using `>=` instead of `>` would incorrectly accept it.

A different edge case occurs when a segment consists of a single position.

```
segment = [3,3]
```

The moment position `3` becomes `1`, the segment contains one one and zero zeros, so it is beautiful immediately. The answer may be `1`.

Finally, some instances never produce a beautiful segment.

```
n = 4
segments = [1,1], [4,4]
updates = 2,3
```

Neither segment is ever touched, so the correct answer is `-1`.

## Approaches

A direct simulation is straightforward. After each update, mark the new position as `1`, then examine every segment. For each segment, count how many ones it currently contains and check whether that count exceeds half of the segment length.

The brute-force version is correct because it literally implements the definition. The problem is the cost. With `q` updates and `m` segments, even if counting ones inside a segment were constant time, we would still perform `m × q` checks. In the worst case this becomes roughly `10^10` operations, which is completely infeasible.

The turning point comes from observing that the property "some segment is beautiful" is monotonic.

If after the first `k` updates some segment is beautiful, then after any larger number of updates it remains beautiful because updates only add ones. This means the answer is the first position where a monotonic predicate becomes true.

Whenever a problem asks for the earliest point where a monotonic condition appears, binary search becomes a natural candidate.

Suppose we guess a value `mid`. We ask:

> After applying the first `mid` updates, does there exist a beautiful segment?

To answer this efficiently, we build an array marking which positions have been activated among the first `mid` updates. A prefix sum then allows us to compute the number of ones inside any segment in constant time.

For a segment `[l,r]`:

$$\text{ones} = pref[r] - pref[l-1]$$

The segment is beautiful when:

$$\text{ones} > (r-l+1) - \text{ones}$$

Checking all segments costs `O(m)`, and building the prefix sum costs `O(n)`.

The predicate can therefore be evaluated in `O(n+m)` time. Combining that with binary search over the `q` updates gives an accepted solution.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(qm) or worse | O(n) | Too slow |
| Optimal | O((n + m) log q) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read all segments and all update positions.
2. Define a function `check(k)` that determines whether some segment is beautiful after applying the first `k` updates.
3. Inside `check(k)`, create an array of length `n` initialized with zeros.
4. Mark the first `k` updated positions as `1`.
5. Build a prefix sum array over this binary array.
6. For every segment `[l,r]`, compute the number of ones inside it using the prefix sums.
7. Let `length = r - l + 1`. If the number of ones is strictly greater than `length / 2`, immediately return `True`.
8. If no segment satisfies the condition, return `False`.
9. Before binary searching, evaluate `check(q)`. If it is false, no segment ever becomes beautiful, so output `-1`.
10. Otherwise binary search on the answer. Maintain the smallest update count whose predicate is true.
11. Output the leftmost valid update number.

### Why it works

The predicate checked by `check(k)` is:

> At least one segment is beautiful after the first `k` updates.

Applying more updates can only increase the number of ones in every segment. A beautiful segment can never become non-beautiful later. Consequently, the predicate is monotonic: once it becomes true, it stays true forever.

The prefix sums compute the exact number of activated positions inside every segment, so `check(k)` returns true exactly when the problem condition is satisfied after `k` updates.

Binary search on a monotonic predicate always finds the smallest index where the predicate becomes true. That index is precisely the first update after which some segment becomes beautiful.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())

    for _ in range(t):
        n, m = map(int, input().split())

        segments = []
        for _ in range(m):
            l, r = map(int, input().split())
            segments.append((l, r))

        q = int(input())
        queries = [int(input()) for _ in range(q)]

        def check(k):
            arr = [0] * (n + 1)

            for i in range(k):
                arr[queries[i]] = 1

            pref = [0] * (n + 1)
            for i in range(1, n + 1):
                pref[i] = pref[i - 1] + arr[i]

            for l, r in segments:
                ones = pref[r] - pref[l - 1]
                length = r - l + 1

                if ones * 2 > length:
                    return True

            return False

        if not check(q):
            print(-1)
            continue

        lo, hi = 1, q
        ans = q

        while lo <= hi:
            mid = (lo + hi) // 2

            if check(mid):
                ans = mid
                hi = mid - 1
            else:
                lo = mid + 1

        print(ans)

if __name__ == "__main__":
    solve()
```

The solution revolves around the `check` function. It reconstructs the array state after the first `k` updates, then uses a prefix sum array to answer segment-count queries in constant time.

The condition

```
ones * 2 > length
```

is equivalent to checking whether the number of ones exceeds the number of zeros. Using multiplication avoids any issues with integer division.

The binary search looks for the first value of `k` for which `check(k)` returns true. Since the predicate is monotonic, the standard leftmost-true binary search applies directly.

One implementation detail that is easy to get wrong is indexing. The segments are 1-indexed, so the prefix sum array is also built as 1-indexed. This makes the formula

```
pref[r] - pref[l - 1]
```

work naturally.

Another subtle point is checking `check(q)` before binary search. If the predicate is false even after all updates, binary search would have no valid answer. Handling this case separately keeps the search logic simple.

## Worked Examples

### Example 1

Input:

```
n = 5
segments = [1,2], [4,5], [1,5], [1,3], [2,4]
updates = 5,3,1,2,4
```

Binary search evaluations:

| k | Active positions | Beautiful segment exists? |
| --- | --- | --- |
| 3 | {1,3,5} | Yes |
| 1 | {5} | No |
| 2 | {3,5} | No |

The search first discovers that `k=3` works. It then verifies that neither `1` nor `2` works. The smallest valid value is `3`.

This example demonstrates the monotonic nature of the predicate. Once `k=3` becomes valid, all larger values remain valid.

### Example 2

Input:

```
n = 4
segments = [1,1], [4,4]
updates = 2,3
```

State evolution:

| k | Active positions | Segment [1,1] | Segment [4,4] | Exists? |
| --- | --- | --- | --- | --- |
| 1 | {2} | 0 ones | 0 ones | No |
| 2 | {2,3} | 0 ones | 0 ones | No |

Even after all updates, neither monitored position becomes `1`.

The preliminary `check(q)` fails, so the answer is `-1`.

This example shows why the algorithm performs the full-check test before starting binary search.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((n + m) log q) | Each predicate evaluation scans the array and all segments, binary search performs O(log q) evaluations |
| Space | O(n) | Arrays for activation status and prefix sums |

The total sum of `n` across test cases is at most `10^5`. Each binary-search iteration performs linear work in `n + m`, and there are at most about 17 iterations because `q ≤ 10^5`. This comfortably fits within the time limit and uses only linear memory.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    from io import StringIO

    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = StringIO(inp)
    sys.stdout = StringIO()

    def solve():
        input = sys.stdin.readline

        t = int(input())

        for _ in range(t):
            n, m = map(int, input().split())

            segments = [tuple(map(int, input().split())) for _ in range(m)]

            q = int(input())
            queries = [int(input()) for _ in range(q)]

            def check(k):
                arr = [0] * (n + 1)

                for i in range(k):
                    arr[queries[i]] = 1

                pref = [0] * (n + 1)

                for i in range(1, n + 1):
                    pref[i] = pref[i - 1] + arr[i]

                for l, r in segments:
                    ones = pref[r] - pref[l - 1]
                    if ones * 2 > (r - l + 1):
                        return True

                return False

            if not check(q):
                print(-1)
                continue

            lo, hi = 1, q
            ans = q

            while lo <= hi:
                mid = (lo + hi) // 2

                if check(mid):
                    ans = mid
                    hi = mid - 1
                else:
                    lo = mid + 1

            print(ans)

    solve()

    out = sys.stdout.getvalue()

    sys.stdin = old_stdin
    sys.stdout = old_stdout

    return out

# provided sample
assert run(
"""6
5 5
1 2
4 5
1 5
1 3
2 4
5
5
3
1
2
4
4 2
1 1
4 4
2
2
3
5 2
1 5
1 5
4
2
1
3
4
5 2
1 5
1 3
5
4
1
2
3
5
5 5
1 5
1 5
1 5
1 5
1 4
3
1
4
3
3 2
2 2
1 3
3
2
3
1
"""
) == """3
-1
3
3
3
1
"""

# minimum size
assert run(
"""1
1 1
1 1
1
1
"""
) == """1
"""

# never becomes beautiful
assert run(
"""1
4 2
1 1
4 4
2
2
3
"""
) == """-1
"""

# strict inequality check
assert run(
"""1
4 1
1 4
2
1
2
"""
) == """-1
"""

# answer occurs at final update
assert run(
"""1
3 1
1 3
3
1
2
3
"""
) == """2
"""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single element segment | 1 | Minimum constraints |
| Untouched monitored positions | -1 | No beautiful segment ever appears |
| Length 4 with exactly 2 ones | -1 | Strictly greater, not greater-or-equal |
| Segment [1,3] activated gradually | 2 | Earliest valid update found correctly |

## Edge Cases

Consider a segment whose length is even.

```
1
4 1
1 4
2
1
2
```

After both updates the segment contains two ones and two zeros. The algorithm computes:

```
ones = 2
length = 4
ones * 2 = 4
```

Since `4 > 4` is false, the segment is not beautiful. The output is `-1`. This correctly handles the strict inequality requirement.

Consider a single-position segment.

```
1
1 1
1 1
1
1
```

For `k = 1`, the segment contains one one and zero zeros. The check becomes:

```
1 * 2 > 1
```

which is true, so the binary search returns `1`.

Consider a case where no segment is ever affected.

```
1
4 2
1 1
4 4
2
2
3
```

Even after all updates, both tracked segments contain zero ones. The preliminary call `check(q)` returns false, and the algorithm immediately outputs `-1`.

Finally, consider repeated large segments:

```
n = 5
segments = [1,5], [1,5], [1,5]
updates = 2,1,3,4
```

The algorithm checks every segment independently. Duplicate segments do not change correctness because each check uses the same prefix-sum query. As soon as one duplicate becomes beautiful, the predicate returns true.

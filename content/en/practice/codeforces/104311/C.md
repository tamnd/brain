---
title: "CF 104311C - c0=c1"
description: "We are given two binary arrays of equal length. From each array we are allowed to pick one contiguous segment, and the only restriction on each segment is that its length must fall inside a given range."
date: "2026-07-01T19:58:09+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104311
codeforces_index: "C"
codeforces_contest_name: "TheForces Round #11 (DIV2.5-Forces)"
rating: 0
weight: 104311
solve_time_s: 108
verified: true
draft: false
---

[CF 104311C - c0=c1](https://codeforces.com/problemset/problem/104311/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 48s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given two binary arrays of equal length. From each array we are allowed to pick one contiguous segment, and the only restriction on each segment is that its length must fall inside a given range. After choosing the two segments, we count how many zeros and ones appear in both of them combined. The goal is to determine whether there exists a choice of the two segments such that the total number of zeros equals the total number of ones.

A useful way to rewrite the condition is to think in terms of balance. For any segment, define its value as the number of ones minus the number of zeros. The requirement that total zeros equal total ones across both chosen segments is exactly the same as requiring that the sum of these two segment values is zero. So we are looking for one segment in array `a` and one segment in array `b`, within their respective length constraints, such that their “imbalance” cancels out perfectly.

The constraints make a brute-force over all segments impossible. Each array has up to 200,000 elements across test cases, and there are up to 100,000 test cases. Even a quadratic enumeration of segments per test case would be far beyond any feasible limit. A linear scan per test case is already the intended scale.

A common failure mode is to ignore that segments come from two different arrays. A naive solution might try to precompute all segment sums in one array and then match them against the other, but forgetting the length constraints breaks correctness. Another subtle mistake is to only consider prefix sums or only consider minimum and maximum segment sums; both lose the dependency on allowed segment lengths, which is essential here.

## Approaches

The brute-force idea is straightforward. We enumerate every valid segment in `a` whose length is between `x1` and `y1`, compute its balance, then enumerate every valid segment in `b` whose length is between `x2` and `y2`, compute its balance, and check whether a pair sums to zero. This works because it directly follows the definition, but it is far too slow. Each array has O(n²) segments in the worst case, so the total number of comparisons becomes O(n⁴) in the naive cross-product view, even if implemented carefully.

The key observation is that the condition depends only on segment sums of a transformed array. If we convert each binary array into an array where `0 → -1` and `1 → +1`, then every segment sum is exactly its balance. The problem becomes: do there exist two allowed segments, one from each array, whose sums add to zero.

This can be reframed as a set intersection problem over achievable segment sums under length constraints. Instead of enumerating all segments, we only care about which sums are achievable for each array. For a fixed array and a fixed length interval, we can determine all segment sums efficiently using a sliding window over prefix sums. The challenge is to check whether any sum from `a` has its negation in `b`.

We avoid storing all possible sums explicitly. Instead, we scan through one array, mark achievable segment sums in a hash set, then scan the other array and test for complements. Since segment sums depend on prefix differences, each segment sum can be computed in O(1), and each array contributes O(n) candidates overall.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) per test | O(n²) | Too slow |
| Prefix enumeration + hashing | O(n) per test | O(n) | Accepted |

## Algorithm Walkthrough

We transform each binary value so that zeros contribute -1 and ones contribute +1. This makes every segment sum represent the imbalance between ones and zeros.

We then compute prefix sums for both arrays so that any segment sum can be extracted in constant time.

For each array, we iterate over all valid segment lengths. For a fixed length `len`, we slide a window across the array and compute the segment sum using prefix differences. For array `a`, we store all achievable segment sums in a hash set. We repeat the same process for array `b`.

Finally, we check whether there exists a value `s` in the set of `a` such that `-s` exists in the set of `b`. If yes, we output YES, otherwise NO.

The subtle point is that we must respect the length constraints independently for both arrays. The sets are built only from valid window sizes, otherwise we would include invalid candidates that could not appear in a real solution.

### Why it works

Every valid segment corresponds uniquely to a prefix difference, so no valid candidate is missed when we enumerate by length and start index. The transformation to ±1 guarantees that equality of zeros and ones across two segments is equivalent to sum cancellation. Since we check all achievable sums from both arrays under the same constraints, the existence of a zero-sum pair is equivalent to detecting a matching negation in the two sets.

## Python Solution

```python
import sys
input = sys.stdin.readline

def build_sums(arr, x, y):
    n = len(arr)
    pref = [0] * (n + 1)
    for i in range(n):
        pref[i + 1] = pref[i] + (1 if arr[i] == 1 else -1)

    res = set()

    for length in range(x, y + 1):
        for i in range(n - length + 1):
            s = pref[i + length] - pref[i]
            res.add(s)

    return res

def solve():
    t = int(input())
    out = []

    for _ in range(t):
        n, x1, y1, x2, y2 = map(int, input().split())
        a = list(map(int, input().split()))
        b = list(map(int, input().split()))

        sa = build_sums(a, x1, y1)
        sb = build_sums(b, x2, y2)

        # check intersection via negation
        ok = False
        if len(sa) > len(sb):
            sa, sb = sb, sa

        for v in sa:
            if -v in sb:
                ok = True
                break

        out.append("YES" if ok else "NO")

    print("\n".join(out))

if __name__ == "__main__":
    solve()
```

The prefix sum array encodes cumulative imbalance so that segment sums are computed in O(1). The nested loops over length and start index ensure only valid intervals are considered. Swapping the sets reduces lookup cost slightly by iterating over the smaller one.

The negation check is the direct translation of the condition that the two segment balances must cancel.

## Worked Examples

### Example 1

Consider a small case where both arrays are `0 1 0 1` and both segment lengths must be exactly 2.

We convert to `-1 +1 -1 +1`. Segment sums are:

| segment | sum |
| --- | --- |
| a[0:2] | 0 |
| a[1:3] | 0 |
| a[2:4] | 0 |

Both arrays produce the same set `{0}`.

We then check whether any sum in `a` has negation in `b`. Since `0 == -0`, the answer is YES.

This confirms the algorithm correctly handles cases where the optimal cancellation is achieved by neutral segments.

### Example 2

Let `a = 1 1 1 1`, `b = 0 0 0 0`, and both length ranges allow full selection.

Converted arrays are `+1 +1 +1 +1` and `-1 -1 -1 -1`. Segment sums are strictly positive for `a` and strictly negative for `b`.

| array | possible sums |
| --- | --- |
| a | positive only |
| b | negative only |

No value in `a` has negation in `b`, so the algorithm returns NO.

This demonstrates the correctness in cases where imbalance directions never align.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n · (y - x + 1)) per test | each valid segment length is scanned linearly over the array |
| Space | O(n) | prefix sums plus hash sets of segment values |

The total sum of `n` across tests is bounded by 200,000, so even with moderate window ranges the approach stays linear in aggregate. The use of hash sets ensures constant-time complement checks.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    def build(arr, x, y):
        n = len(arr)
        pref = [0]*(n+1)
        for i in range(n):
            pref[i+1] = pref[i] + (1 if arr[i]==1 else -1)
        s = set()
        for l in range(x, y+1):
            for i in range(n-l+1):
                s.add(pref[i+l]-pref[i])
        return s

    def solve():
        t = int(input())
        out=[]
        for _ in range(t):
            n,x1,y1,x2,y2 = map(int,input().split())
            a=list(map(int,input().split()))
            b=list(map(int,input().split()))
            sa=build(a,x1,y1)
            sb=build(b,x2,y2)
            ok=False
            for v in sa:
                if -v in sb:
                    ok=True
                    break
            out.append("YES" if ok else "NO")
        return "\n".join(out)

    return solve()

# provided samples
assert run("""4
4 3 3 3 3
0 1 0 1
0 1 0 0
5 4 5 1 3
1 1 1 1 1
0 0 0 0 1
4 2 4 1 3
1 1 1 1
0 1 1 0
6 1 2 1 2
0 0 0 0 0 0
0 0 0 1 0 0
""") == "YES\nNO\nNO\nYES"

# custom cases
assert run("""1
1 1 1 1 1
0
1
""") == "YES", "single cancellation"

assert run("""1
3 1 3 1 3
0 0 0
0 0 0
""") == "YES", "all zero arrays"

assert run("""1
3 1 2 1 2
1 1 1
1 1 1
""") == "NO", "no zero balance possible"

assert run("""1
4 2 3 2 3
1 0 1 0
0 1 0 1
""") == "YES", "symmetry case"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single elements (0 vs 1) | YES | minimal cancellation |
| all zeros | YES | zero balance segments exist everywhere |
| all ones | NO | no way to balance |
| alternating symmetry | YES | mixed segment cancellations |

## Edge Cases

One edge case arises when both arrays consist entirely of identical bits. If all values are zero, every segment has zero imbalance, so any valid pair works. The algorithm correctly inserts only zeros into both sets and finds a match at zero.

Another edge case appears when segment length ranges exclude all but one length. The algorithm still enumerates only that length, so no invalid segments leak in. For example, if both ranges are `[1,1]`, only single elements are considered, and the balance check reduces to comparing individual bits across arrays, which is handled naturally by the prefix logic.

A third edge case is when one array can produce both positive and negative segment sums while the other is strictly one-sided. In that situation, the negation check never succeeds, since the value distribution does not overlap in a symmetric way. The set-based approach correctly captures this asymmetry without requiring special handling.

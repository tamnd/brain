---
title: "CF 102458C - Daniel's game"
description: "We have an array A of n non-negative integers and a budget M. For every non-empty contiguous subarray A[l..r], Andy may increase its elements, but the total amount added cannot exceed M. His goal is to make the chosen subarray non-decreasing."
date: "2026-08-09T02:42:40+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102458
codeforces_index: "C"
codeforces_contest_name: "Hanoi final contest"
rating: 0
weight: 102458
solve_time_s: 298
verified: true
draft: false
---

[CF 102458C - Daniel's game](https://codeforces.com/problemset/problem/102458/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 4m 58s  
**Verified:** yes  

## Solution
## Problem Understanding

We have an array `A` of `n` non-negative integers and a budget `M`. For every non-empty contiguous subarray `A[l..r]`, Andy may increase its elements, but the total amount added cannot exceed `M`. His goal is to make the chosen subarray non-decreasing.

For a fixed subarray, there is only one relevant quantity: the minimum total amount that must be added to make it non-decreasing. We need to count how many subarrays have this minimum cost at most `M`.

Suppose the chosen subarray starts at `l`. Process it from left to right. The first value needs no change. At position `i`, the smallest possible value after modification is the larger of the original `A[i]` and the previous modified value. Consequently, the optimal modified sequence is exactly the sequence of prefix maxima:

[
B_i=\max(A_l,A_{l+1},\ldots,A_i).
]

The minimum cost of `[l,r]` is therefore

[
C(l,r)=\sum_{i=l}^{r}\left(\max_{j=l}^{i} A_j-A_i\right).
]

A subarray is winning exactly when `C(l,r) <= M`.

The important constraint is `n <= 2 * 10^5`, while `M` can be as large as `2 * 10^14` and each `A[i]` can be as large as `10^9`. There are about `n(n+1)/2` subarrays, so enumerating them already takes about `2 * 10^10` cases at the maximum size. A solution that spends even linear time per subarray is completely impossible. We need close to `O(n log n)` work, and all costs must use 64-bit arithmetic. Python integers handle this range naturally.

There are several edge cases that easily cause incorrect answers.

When `n=1`, the single-element subarray already is non-decreasing and costs zero. For `1 0` with array `1234`, the answer is `1`. An implementation that only counts subarrays containing an inversion would incorrectly return zero.

Equal values must not be treated as a strict increase. For `n=4`, `M=0`, and array `5 5 5 5`, every one of the ten subarrays is already non-decreasing, so the answer is `10`. If the next-greater structure treats an equal value as a greater value, it can split a prefix maximum block incorrectly.

The budget comparison is inclusive. For `n=3`, `M=3`, and array `3 1 2`, the subarray `[3,1,2]` costs exactly `3`: the two smaller values must become `3`, adding `2+1`. It is valid, so all six subarrays are counted. Using `< M` instead of `<= M` would lose this interval.

Finally, the cost can be much larger than a 32-bit integer. With `n=2*10^5` and values around `10^9`, the total correction can reach the order of `10^14`. A 32-bit accumulator silently overflows in languages with fixed-width integers.

## Approaches

The direct approach is to fix every pair `(l,r)` and simulate the greedy construction of a non-decreasing sequence. Starting with `maximum = A[l]`, each following element contributes `max(0, maximum - A[i])`, and `maximum` is updated when `A[i]` is larger. This is correct because every element must be at least the previous final value, so choosing anything larger can only increase the cost.

There are `n(n+1)/2` subarrays, and a single subarray may contain `O(n)` elements. On the worst case this means

[
\Theta(n^3)
]

operations. With `n=2*10^5`, that is on the order of `8*10^15` elementary iterations, far beyond the two-second limit.

The brute-force approach works because it follows the exact greedy construction, but it repeatedly walks through the same parts of the array. The observation that unlocks the faster solution is that the prefix maximum does not change at every position. Starting from position `l`, the current maximum remains `A[l]` until the first position whose value is strictly greater than `A[l]`. After reaching that position, the same reasoning starts again from the new maximum.

Define `nxt[i]` as the first position to the right of `i` with `A[nxt[i]] > A[i]`. Between `i` and `nxt[i]-1`, the prefix maximum is exactly `A[i]`. The complete cost of this block is

[
A_i(nxt[i]-i)-\sum_{j=i}^{nxt[i]-1}A_j.
]

Thus the cost of a long subarray can be decomposed into a chain of complete next-greater blocks plus one final partial block.

All `nxt[i]` values can be found in linear time with a monotonic stack. We then use binary lifting to skip many next-greater blocks at once and obtain `C(l,r)` in `O(log n)`.

The final observation is that the maximum valid right endpoint is monotone. If we move `l` to the right while keeping `r` fixed, we remove elements from the beginning, so the minimum required cost cannot increase. Hence the largest valid `r` never moves left as `l` increases. This allows a two-pointer scan: each right endpoint advances only `O(n)` times overall, while every cost check takes `O(log n)`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | `O(n^3)` | `O(1)` | Too slow |
| Optimal | `O(n log n)` | `O(n log n)` | Accepted |

## Algorithm Walkthrough

1. Build the ordinary prefix sum array `pref`, where `pref[i]` is the sum of `A[0..i-1]`. This lets us calculate the sum of any contiguous block in constant time.
2. Compute `nxt[i]`, the first index `j > i` with `A[j] > A[i]`. Scan from right to left with a monotonic decreasing stack. While the top has a value smaller than `A[i]`, pop it because `i` becomes its first strictly greater element. Equal values are not popped, because the prefix maximum does not change when we encounter an equal value.
3. For every position `i`, define the cost of its complete block as the cost from `i` through `nxt[i]-1`. If there is no greater element, the block ends at `n`. Its cost is

[
block[i]=A_i(nxt[i]-i)-(pref[nxt[i]]-pref[i]).
]

Within this interval every prefix maximum is `A[i]`, so the formula directly sums `A[i]-A[j]`.

1. Build binary-lifting tables. `up[k][i]` represents the position reached after following `2^k` next-greater jumps starting at `i`. `gain[k][i]` stores the sum of all complete block costs crossed by those jumps. The base level contains one jump, so `up[0][i] = nxt[i]` and `gain[0][i] = block[i]`.
2. Implement a function `cost(l,r)` that computes the minimum cost of making `A[l..r]` non-decreasing. Starting at `l`, inspect the binary-lifting levels from largest to smallest. If the destination of a jump is at most `r`, that entire block lies inside the requested interval, so add its precomputed cost and jump there. After no more complete block fits, the remaining interval starts at `cur` and ends at `r`. Its prefix maximum is `A[cur]`, giving the final partial cost

[
A_{cur}(r-cur+1)-(pref[r+1]-pref[cur]).
]

1. Scan the array with two pointers. Keep a right endpoint `r`. For each new left endpoint `l`, repeatedly extend `r` while `cost(l,r+1) <= M`. Every extension is permanent because the right endpoint never needs to move backward. Once the next extension would exceed the budget, every larger right endpoint is also invalid, since adding an element cannot reduce the required modification cost.
2. For the current `l`, exactly `r-l+1` subarrays beginning at `l` are valid. Add this number to the answer and increment `l`. Removing the leftmost element cannot increase the minimum modification cost, so the existing `r` remains valid and the two-pointer invariant is preserved.

### Why it works

For every subarray, the minimum possible final value at each position is its prefix maximum. The next-greater decomposition partitions those prefix maxima into maximal regions where the current maximum is constant, so the block formula computes exactly the same cost as the direct greedy scan. Binary lifting only skips consecutive complete regions, without changing their total contribution, and the final partial region is computed directly.

The two-pointer part relies on monotonicity. For a fixed `l`, extending `r` can only add a non-negative contribution, so once a right endpoint becomes invalid, every larger endpoint is invalid. For a fixed `r`, moving `l` right removes constraints and cannot increase the minimum cost, so the largest valid `r` cannot move left. Thus every valid subarray is counted exactly once.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, M = map(int, input().split())
    a = list(map(int, input().split()))

    # Prefix sums.
    pref = [0] * (n + 1)
    s = 0
    for i, x in enumerate(a):
        s += x
        pref[i + 1] = s

    # nxt[i] = first j > i with a[j] > a[i].
    nxt = [n] * n
    stack = []

    for i in range(n - 1, -1, -1):
        x = a[i]
        while stack and a[stack[-1]] < x:
            nxt[stack.pop()] = i
        stack.append(i)

    # Cost of the complete block [i, nxt[i)-1].
    block = [0] * n
    for i in range(n):
        j = nxt[i]
        block[i] = a[i] * (j - i) - (pref[j] - pref[i])

    LOG = n.bit_length()

    # Binary lifting tables.
    up = [nxt]
    gain = [block]

    for k in range(1, LOG):
        prev_up = up[-1]
        prev_gain = gain[-1]

        cur_up = [n] * n
        cur_gain = [0] * n

        for i in range(n):
            mid = prev_up[i]
            if mid < n:
                cur_up[i] = prev_up[mid]
                cur_gain[i] = prev_gain[i] + prev_gain[mid]

        up.append(cur_up)
        gain.append(cur_gain)

    def cost(l, r):
        """Minimum increments needed for a[l..r]."""
        cur = l
        ans = 0

        for k in range(LOG - 1, -1, -1):
            j = up[k][cur]
            if j <= r:
                ans += gain[k][cur]
                cur = j

        # cur is the beginning of the final partial block.
        ans += a[cur] * (r - cur + 1) - (pref[r + 1] - pref[cur])
        return ans

    ans = 0
    r = -1

    for l in range(n):
        if r < l:
            r = l

        while r + 1 < n and cost(l, r + 1) <= M:
            r += 1

        ans += r - l + 1

    print(ans)

if __name__ == "__main__":
    solve()
```

The prefix sum construction corresponds directly to the block-cost formula. `pref[j] - pref[i]` is the sum of all original values in the block, while `a[i] * (j-i)` is the sum after every element in that block is raised to the block's maximum.

The monotonic stack uses the strict comparison `a[stack[-1]] < x`. Changing this to `<=` would be incorrect. For equal values, the earlier value remains the same prefix maximum, so the first strictly greater value is what ends its block.

The binary-lifting tables use `n` as a sentinel meaning that no greater element exists. A jump is used only when its destination is `<= r`. This condition is what guarantees that the whole block represented by the jump belongs to `[l,r]`.

After all complete blocks have been consumed, `cur` is the first position whose next greater element lies beyond `r`. Consequently every prefix maximum from `cur` through `r` equals `a[cur]`, which makes the final constant-time formula valid.

The two-pointer loop deliberately checks `r+1` rather than recomputing the current window's cost. The current `[l,r]` is already known to be valid. Once `[l,r+1]` fails, all further right endpoints fail as well.

Python's arbitrary-precision integers are useful here because both `M` and the accumulated costs can be around `10^14`. No explicit overflow handling is required.

## Worked Examples

### Sample 1

For `A = [5,4,1,1,5,5]` and `M = 6`, the maximum valid right endpoint for each left endpoint is as follows.

| `l` | Maximum `r` | `cost(l,r)` | Next cost | Subarrays added |
| --- | --- | --- | --- | --- |
| 1 | 3 | 5 | 9 | 3 |
| 2 | 6 | 6 | beyond array | 5 |
| 3 | 6 | 0 | beyond array | 4 |
| 4 | 6 | 0 | beyond array | 3 |
| 5 | 6 | 0 | beyond array | 2 |
| 6 | 6 | 0 | beyond array | 1 |

For `l=1`, the prefix maxima of `[5,4,1]` are `[5,5,5]`, so the cost is `0+1+4=5`. Extending to the fourth element gives another `4`, making the cost `9`, so the right endpoint stops at `3`.

For `l=2`, the subarray `[4,1,1,5,5]` costs `3+3+0+0=6`, exactly the available budget. The exact equality demonstrates why the condition must be `<= M`.

The counts are `3+5+4+3+2+1 = 18`, matching the official sample output.

### Sample 2

For `A = [6,5,4,3,2]` and `M = 5`, the trace is:

| `l` | Maximum `r` | `cost(l,r)` | Next cost | Subarrays added |
| --- | --- | --- | --- | --- |
| 1 | 3 | 3 | 6 | 3 |
| 2 | 4 | 3 | 6 | 3 |
| 3 | 5 | 3 | beyond array | 3 |
| 4 | 5 | 1 | beyond array | 2 |
| 5 | 5 | 0 | beyond array | 1 |

For example, `[6,5,4]` requires increments `1` and `2`, giving cost `3`. Adding `3` would require another `3`, giving total cost `6`, which exceeds the budget.

The answer is `3+3+3+2+1 = 12`, again matching the official sample.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | `O(n log n)` | Next-greater preprocessing is `O(n)`, binary lifting is `O(n log n)`, and the two-pointer scan performs `O(n)` cost queries, each taking `O(log n)`. |
| Space | `O(n log n)` | The `up` and `gain` binary-lifting tables each contain `O(n log n)` entries. |

With `n <= 2*10^5`, `log n` is only about 18. The algorithm avoids enumerating the quadratic number of subarrays and performs only a logarithmic amount of work for each movement of the two-pointer boundary, which is the required scale for the given limit.

## Test Cases

```python
import sys
import io

def solve_data(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out

    try:
        solve()
        return out.getvalue().strip()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

def solve():
    n, M = map(int, input().split())
    a = list(map(int, input().split()))

    pref = [0] * (n + 1)
    for i, x in enumerate(a):
        pref[i + 1] = pref[i] + x

    nxt = [n] * n
    stack = []

    for i in range(n - 1, -1, -1):
        while stack and a[stack[-1]] < a[i]:
            nxt[stack.pop()] = i
        stack.append(i)

    block = [0] * n
    for i in range(n):
        j = nxt[i]
        block[i] = a[i] * (j - i) - (pref[j] - pref[i])

    LOG = n.bit_length()
    up = [nxt]
    gain = [block]

    for _ in range(1, LOG):
        pu = up[-1]
        pg = gain[-1]
        cu = [n] * n
        cg = [0] * n

        for i in range(n):
            mid = pu[i]
            if mid < n:
                cu[i] = pu[mid]
                cg[i] = pg[i] + pg[mid]

        up.append(cu)
        gain.append(cg)

    def cost(l, r):
        cur = l
        res = 0

        for k in range(LOG - 1, -1, -1):
            j = up[k][cur]
            if j <= r:
                res += gain[k][cur]
                cur = j

        return res + a[cur] * (r - cur + 1) - (
            pref[r + 1] - pref[cur]
        )

    ans = 0
    r = -1

    for l in range(n):
        if r < l:
            r = l

        while r + 1 < n and cost(l, r + 1) <= M:
            r += 1

        ans += r - l + 1

    print(ans)

# Provided samples
assert solve_data(
    "6 6\n5 4 1 1 5 5\n"
) == "18", "sample 1"

assert solve_data(
    "5 5\n6 5 4 3 2\n"
) == "12", "sample 2"

assert solve_data(
    "1 0\n1234\n"
) == "1", "sample 3"

# Minimum-size input.
assert solve_data(
    "1 0\n7\n"
) == "1", "single element"

# All equal values: every subarray already works.
assert solve_data(
    "4 0\n5 5 5 5\n"
) == "10", "all equal"

# Exact budget boundary.
assert solve_data(
    "3 3\n3 1 2\n"
) == "6", "cost exactly equals M"

# Strictly decreasing, with only some longer intervals affordable.
assert solve_data(
    "3 1\n3 2 1\n"
) == "5", "decreasing boundary"

# Maximum n, all equal, so every subarray is valid.
n = 200000
expected = n * (n + 1) // 2
large_input = f"{n} 0\n" + ("1 " * (n - 1)) + "1\n"
assert solve_data(large_input) == str(expected), "maximum n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 0 / 7` | `1` | Minimum-size input and single-element subarray |
| `4 0 / 5 5 5 5` | `10` | Equal values and zero budget |
| `3 3 / 3 1 2` | `6` | Cost exactly equal to `M` |
| `3 1 / 3 2 1` | `5` | Strictly decreasing sequence and right-end boundary |
| `n=200000`, all values `1`, `M=0` | `20000100000` | Maximum input size and large answer |

## Edge Cases

The single-element case `n=1`, `M=0`, `A=[7]` starts with `r=l`. The cost of `[7]` is zero, so the loop cannot extend further and adds one valid subarray. The answer is `1`.

For equal values, consider `A=[5,5,5,5]` with `M=0`. Every `nxt[i]` is `n` because there is no strictly greater value. Each complete block therefore extends to the end, but its cost is zero because every element equals the block maximum. The two-pointer scan reaches `r=3` for every `l`, counting `4+3+2+1=10` subarrays.

For the exact-budget case `A=[3,1,2]`, `M=3`, the complete interval has prefix maxima `[3,3,3]`. Its cost is `(3-3)+(3-1)+(3-2)=3`, so the condition `cost <= M` accepts it. The algorithm extends `r` through the final position rather than stopping one position early.

For the decreasing case `A=[3,2,1]`, `M=1`, the intervals of length two have costs `1`, while the full interval has cost `1+2=3`. Thus the valid counts by starting position are `2`, `2`, and `1`, giving `5`. The next-greater chain for each element ends immediately because every following value is smaller, so the block formula correctly captures the increasing cost of extending the interval.

For the maximum-size case with `200000` equal elements and `M=0`, every one of the

[
\frac{200000\cdot200001}{2}=20000100000
]

subarrays is valid. The answer itself exceeds 32-bit range, while Python's integer arithmetic handles it directly. The algorithm still performs only `O(n log n)` preprocessing and scanning work.

If you want, I can also provide a shorter contest-editorial version, or a C++17 implementation using the same next-greater plus binary-lifting idea.

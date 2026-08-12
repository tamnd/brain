---
title: "CF 102426E - \u9f99\u8bed\u9b54\u6cd5"
description: "We have an array of n positive integers. Every pair of indices l <= r defines one contiguous subarray, and its value is the sum of all elements from l through r."
date: "2026-08-12T19:23:52+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102426
codeforces_index: "E"
codeforces_contest_name: "The 7-th BIT Campus Programming Contest for Junior Grade Group"
rating: 0
weight: 102426
solve_time_s: 91
verified: true
draft: false
---

[CF 102426E - \u9f99\u8bed\u9b54\u6cd5](https://codeforces.com/problemset/problem/102426/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 31s  
**Verified:** yes  

## Solution
## Problem Understanding

We have an array of `n` positive integers. Every pair of indices `l <= r` defines one contiguous subarray, and its value is the sum of all elements from `l` through `r`. There are exactly `n(n+1)/2` such subarrays, and equal sums are counted separately because different subarrays correspond to different results of the magic.

The task is to find the `k`-th smallest subarray sum after all these sums are sorted in nondecreasing order. For example, with `2 3 1 4`, the ten subarrays produce the sorted sequence `1, 2, 3, 4, 4, 5, 5, 6, 8, 10`, so `k = 6` gives `5`.

The array length can reach `10^5`. That means there can be about `5 * 10^9` subarrays. Even an algorithm that performs constant work per subarray is already too slow, and explicitly storing all subarray sums is impossible under the memory limit. The elements can be as large as `10^9`, so a subarray sum can reach about `10^14`, which also requires 64-bit integer arithmetic in languages with fixed-width integers.

The positivity of every `ai` is the key structural constraint. Prefix sums are consequently strictly increasing, which lets us count how many subarray sums are at most a given value in linear time. Without positivity, the two-pointer counting argument would not work.

There are several boundary cases that can silently break an implementation. For `n = 1`, the only possible result is the single element. For example, `1 1` followed by `7` has answer `7`; code that accidentally searches an empty range of subarrays can fail here.

Equal subarray sums must be counted with multiplicity. For `3 4` followed by `2 2 2`, the sorted sums are `2, 2, 2, 4, 4, 6`, so the answer is `4`. A solution that treats the results as distinct values would incorrectly think there are only three possible results.

The smallest and largest possible ranks are also meaningful. For `3 1` followed by `1 5 2`, the smallest subarray sum is `1`, while for `3 6` the answer is the sum of the entire array, `8`. A binary search that uses a strict inequality in the counting function can be off by one at either boundary.

## Approaches

The direct approach is to enumerate every contiguous subarray. For each left endpoint, extend the right endpoint one position at a time and maintain the current sum, giving the sum of every subarray in `O(1)` additional work. This is correct because every pair `(l, r)` appears exactly once. There are `n(n+1)/2` such pairs, which is `5,000,050,000` when `n = 100000`. Merely generating that many values is already far beyond the time limit, and sorting them would make the situation even worse.

The brute-force approach works because it explicitly constructs the collection whose `k`-th element we want. The problem is that the collection itself is quadratic in size. The useful change of viewpoint is to stop asking for every subarray sum and instead ask a counting question: given a number `x`, how many subarrays have sum at most `x`?

Once that counting operation is fast, the original selection problem becomes a binary search. If we can compute `count(x)`, the number of subarray sums no larger than `x`, then `count(x)` is monotonic. For small `x`, few sums fit; as `x` increases, the count can only increase. The answer is exactly the smallest `x` for which `count(x) >= k`.

To calculate `count(x)`, define prefix sums

`p[0] = 0` and `p[i] = a1 + a2 + ... + ai`.

The sum of subarray `l..r` is `p[r] - p[l-1]`. Because every array element is positive, `p` is strictly increasing. For a fixed right prefix index `r`, we need

`p[r] - p[i] <= x`

which is equivalent to

`p[i] >= p[r] - x`.

Since the prefix sums are already sorted, we could find the first suitable `i` by binary search for every `r`, giving `O(n log n)` counting. We can do better. As `r` moves to the right, `p[r]` increases, so the threshold `p[r] - x` also increases. The first valid `i` can never move backwards. A single moving pointer therefore counts all valid starts in `O(n)` time.

The outer binary search needs `O(log S)` iterations, where `S` is the total array sum. Since `S <= 10^14`, this is fewer than 50 iterations. The resulting complexity is `O(n log S)`, which is practical for `n = 10^5`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n² log n) | O(n²) | Too slow |
| Optimal | O(n log S) | O(n) | Accepted |

Here `S` denotes the sum of the entire array.

## Algorithm Walkthrough

1. Build the prefix sum array `p`. Set `p[0] = 0`, then `p[i] = p[i-1] + a[i]`. Because all `ai` are positive, the prefix sums are strictly increasing.
2. Define a function `count(x)` that returns the number of contiguous subarrays whose sum is at most `x`. For each right endpoint represented by prefix index `r`, we need to count all `i < r` satisfying `p[r] - p[i] <= x`.
3. Rewrite the condition as `p[i] >= p[r] - x`. Maintain a pointer `left` to the first prefix sum that satisfies this condition. While `left < r` and `p[left] < p[r] - x`, advance `left`.
4. After the pointer has stopped, every prefix index from `left` through `r-1` gives a valid subarray ending at `r-1`. There are `r - left` of them, so add that number to the count.

The pointer never needs to move backwards. When `r` increases, the threshold `p[r] - x` increases because the prefix sums are increasing. Thus a prefix sum that was already too small can never become valid later.
5. Binary search the answer between `1` and `p[n]`, the total array sum. For a midpoint `mid`, compute `count(mid)`. If the count is at least `k`, then `mid` is large enough to contain the `k`-th smallest sum, so search the left half. Otherwise, search the right half.
6. When the binary search finishes, the lower bound is the smallest value whose count reaches `k`. Print that value.

### Why it works

For every fixed `x`, the counting function considers every possible right endpoint. For that endpoint, the valid left prefix indices form one suffix of the earlier prefix indices because the prefix sums are increasing. The moving pointer identifies the first member of that suffix, so `r - left` counts exactly all valid subarrays ending there. Thus `count(x)` is exactly the number of subarray sums at most `x`.

The predicate `count(x) >= k` is monotonic because increasing `x` can only turn additional subarray sums from too large into valid ones. The binary search therefore finds the smallest value `x` containing at least `k` subarray sums. Since subarray sums are integers, that value is precisely the `k`-th smallest sum.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, k = map(int, input().split())
    a = list(map(int, input().split()))

    prefix = [0] * (n + 1)
    for i in range(1, n + 1):
        prefix[i] = prefix[i - 1] + a[i - 1]

    total = prefix[n]

    def count_at_most(x):
        left = 0
        count = 0

        for right in range(1, n + 1):
            threshold = prefix[right] - x

            while left < right and prefix[left] < threshold:
                left += 1

            count += right - left

            if count >= k:
                return count

        return count

    lo = 1
    hi = total

    while lo < hi:
        mid = (lo + hi) // 2

        if count_at_most(mid) >= k:
            hi = mid
        else:
            lo = mid + 1

    print(lo)

if __name__ == "__main__":
    solve()
```

The prefix construction stores the sum of the first `i` elements at position `i`. The extra zero at `prefix[0]` represents an empty prefix, which is necessary for subarrays beginning at index `1`.

Inside `count_at_most`, `right` is the ending prefix index. The corresponding subarray starts after some prefix index `left`. The inequality `prefix[left] >= prefix[right] - x` is exactly the condition that the resulting subarray sum does not exceed `x`.

The condition in the `while` loop uses `<`, not `<=`. If `prefix[left] == prefix[right] - x`, the resulting subarray has sum exactly `x` and must be counted. Excluding equality would turn the function into a count of sums strictly smaller than `x`, which would shift the binary search answer.

The `left < right` condition prevents using the same prefix index on both sides, which would represent an empty subarray. Every valid subarray has a distinct pair of prefix indices with `left < right`.

The early return when `count >= k` is not necessary for correctness, but it avoids scanning the remaining prefix sums once the binary search already knows that this `x` is large enough. Python integers automatically handle sums beyond 64-bit range, although the actual constraints only require values around `10^14`.

The binary search uses `lo = 1` because every array element is positive, so every nonempty subarray has a positive sum. `hi = total` is valid because the whole array itself has that sum, and it is the largest possible subarray sum.

## Worked Examples

### Sample 1

For the input `4 6` with array `2 3 1 4`, the prefix sums are `0, 2, 5, 6, 10`. The correct answer is `5`.

A useful part of the binary search can be traced as follows.

| `lo` | `hi` | `mid` | `count(mid)` | Decision |
| --- | --- | --- | --- | --- |
| 1 | 10 | 5 | 6 | `6 >= 6`, search left |
| 1 | 5 | 3 | 3 | `3 < 6`, search right |
| 4 | 5 | 4 | 5 | `5 < 6`, search right |
| 5 | 5 | 5 | 6 | stop |

For `x = 5`, the six qualifying subarrays are the sums `1, 2, 3, 4, 4, 5`. For `x = 4`, only five subarrays qualify. This proves that `5` is the first threshold containing at least six results.

### Custom Example 2

Consider:

```
3 4
2 2 2
```

The prefix sums are `0, 2, 4, 6`. The six subarray sums are `2, 2, 2, 4, 4, 6`, so the fourth answer is `4`.

For `x = 3`, each length-one subarray has sum `2`, while every length-two or length-three subarray is too large. Thus `count(3) = 3`.

For `x = 4`, the three length-one subarrays and the two length-two subarrays qualify, giving `count(4) = 5`.

| `lo` | `hi` | `mid` | `count(mid)` | Decision |
| --- | --- | --- | --- | --- |
| 1 | 6 | 3 | 3 | `3 < 4`, search right |
| 4 | 6 | 5 | 5 | `5 >= 4`, search left |
| 4 | 5 | 4 | 5 | `5 >= 4`, search left |
| 4 | 4 | 4 | 5 | stop |

The answer is `4`. This example demonstrates why duplicate sums must be counted separately. The value `2` occurs three times and the value `4` occurs twice.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log S) | Each `count_at_most` call moves `left` and `right` only forward, so it costs O(n), and binary search uses O(log S) calls. |
| Space | O(n) | The prefix sum array contains `n + 1` values. |

With `n <= 10^5` and `S <= 10^14`, the binary search performs fewer than 50 counting passes. Each pass is linear, so the algorithm performs only a few million pointer operations instead of billions of subarray operations. The prefix array also uses linear memory, which fits comfortably within the stated 64 MB limit in Python only with some care; the implementation stores just the input array and prefix array, and no quadratic collection of subarray sums.

## Test Cases

```python
import sys
import io

def solve_data(data: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(data)
    sys.stdout = io.StringIO()

    n, k = map(int, sys.stdin.readline().split())
    a = list(map(int, sys.stdin.readline().split()))

    prefix = [0] * (n + 1)
    for i in range(1, n + 1):
        prefix[i] = prefix[i - 1] + a[i - 1]

    def count_at_most(x):
        left = 0
        count = 0

        for right in range(1, n + 1):
            threshold = prefix[right] - x

            while left < right and prefix[left] < threshold:
                left += 1

            count += right - left

            if count >= k:
                return count

        return count

    lo, hi = 1, prefix[n]

    while lo < hi:
        mid = (lo + hi) // 2
        if count_at_most(mid) >= k:
            hi = mid
        else:
            lo = mid + 1

    result = str(lo)

    sys.stdin = old_stdin
    sys.stdout = old_stdout
    return result

# Provided sample
assert solve_data("4 6\n2 3 1 4\n") == "5", "sample 1"

# Minimum-size input
assert solve_data("1 1\n7\n") == "7", "single element"

# All values equal, with duplicate sums
assert solve_data("3 4\n2 2 2\n") == "4", "duplicate sums"

# Smallest possible rank
assert solve_data("4 1\n5 1 3 2\n") == "1", "k = 1"

# Largest possible rank, which must be the whole-array sum
assert solve_data("4 10\n5 1 3 2\n") == "11", "k = n(n+1)/2"

# Maximum-size structural test, all values equal.
# The expected value can be computed directly without enumerating subarrays.
n = 100000
a = "1 " * (n - 1) + "1"
k = n * (n + 1) // 2
expected = n
assert solve_data(f"{n} {k}\n{a}\n") == str(expected), "maximum n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 / 7` | `7` | Minimum size and the only possible subarray |
| `3 4 / 2 2 2` | `4` | Duplicate sums and multiplicity |
| `4 1 / 5 1 3 2` | `1` | Lower boundary `k = 1` |
| `4 10 / 5 1 3 2` | `11` | Upper boundary `k = n(n+1)/2` |
| `n = 100000`, all ones | `100000` | Maximum input size and large `k` |

## Edge Cases

For a single element, the input `1 1` followed by `7` gives only one prefix difference, `7 - 0 = 7`. During counting, `right = 1` and `left = 0`, so the count becomes `1`. The binary search has `lo = hi = 7`, and immediately returns `7`.

For duplicate sums, consider `3 4` followed by `2 2 2`. At `x = 3`, the pointer counts exactly the three length-one subarrays, giving `3`, which is below `k = 4`. At `x = 4`, the two length-two subarrays also become valid, so the count becomes `5`. The smallest threshold with at least four results is consequently `4`. The algorithm never deduplicates sums, so multiplicity is preserved naturally.

For the smallest possible rank, `4 1` followed by `5 1 3 2` has minimum subarray sum `1`. The predicate `count(x) >= 1` first becomes true at `x = 1`. Binary search keeps the lower half whenever the count reaches `k`, so it settles exactly on `1`.

For the largest possible rank, `4 10` followed by `5 1 3 2` asks for the tenth and final subarray sum. Since all elements are positive, the complete array has the largest sum, `5 + 1 + 3 + 2 = 11`. At `x = 10`, not all ten subarrays qualify, while at `x = 11`, all ten do. The binary search therefore returns `11`.

The maximum-size all-ones test has `100000` elements and `k = n(n+1)/2`, so the requested result is the largest subarray sum, which is `100000`. The counting function never constructs the roughly five billion subarrays. Its pointer simply advances through the prefix sums once per binary-search iteration, demonstrating why the quadratic number of possible results does not force a quadratic algorithm.

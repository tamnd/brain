---
title: "CF 102373F - \u041e\u043d\u0438"
description: "We have an array a[1..n], where a[i] is the number of children at position i. The old Pennywise takes a prefix, positions 1 through l, while the modern Pennywise takes a suffix, positions r through n. The two segments must not overlap, so l < r."
date: "2026-08-14T12:41:24+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102373
codeforces_index: "F"
codeforces_contest_name: "\u0426\u0438\u043a\u043b \u0418\u043d\u0442\u0435\u0440\u043d\u0435\u0442-\u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434 \u0434\u043b\u044f \u0448\u043a\u043e\u043b\u044c\u043d\u0438\u043a\u043e\u0432, \u0421\u0435\u0437\u043e\u043d 2019-2020, \u041f\u0435\u0440\u0432\u0430\u044f \u043a\u043e\u043c\u0430\u043d\u0434\u043d\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430"
rating: 0
weight: 102373
solve_time_s: 123
verified: false
draft: false
---

[CF 102373F - \u041e\u043d\u0438](https://codeforces.com/problemset/problem/102373/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 3s  
**Verified:** no  

## Solution
## Problem Understanding

We have an array `a[1..n]`, where `a[i]` is the number of children at position `i`. The old Pennywise takes a prefix, positions `1` through `l`, while the modern Pennywise takes a suffix, positions `r` through `n`. The two segments must not overlap, so `l < r`.

For a chosen pair `(l, r)`, the two scores are

`S1 = a[1] + ... + a[l]`

and

`S2 = a[r] + ... + a[n]`.

The task is to find any valid pair that minimizes `|S1 - S2|`, and print that minimum difference together with the corresponding `l` and `r`.

The constraint `n <= 10^6` is the main algorithmic signal. There can be roughly one million positions, so an `O(n^2)` search is completely infeasible. Even an `O(n log n)` approach is unnecessary here because the positive array values give us a monotonic structure that permits a linear scan. The values themselves can be as large as `10^9`, so a sum can reach `10^15`. C++ needs a 64 bit integer type for these sums, while Python integers already handle them safely.

There are several boundary cases where an implementation can silently fail. With `n = 2`, the only legal pair is `l = 1, r = 2`. For input

```
2
8 3
```

the correct result is

```
5 1 2
```

because the two scores are `8` and `3`. An implementation that moves one pointer before evaluating the initial pair can miss the only valid answer.

A second edge case occurs when the two initial segments already have equal sums. For

```
4
7 1 1 7
```

the pair `l = 1, r = 4` gives scores `7` and `7`, so the answer is

```
0 1 4
```

A careless implementation that always performs a pointer movement before checking the difference can miss the optimum of zero.

The opposite pointer boundary matters as well. Consider

```
3
1 2 3
```

Starting with the first and last elements gives scores `1` and `3`. The left score is smaller, so the left pointer moves to position `2`, giving `3` and `3`. The correct result is

```
0 2 3
```

If the condition is written incorrectly so that equality or the final valid position causes an extra movement, the pair `(2, 3)` can be skipped.

## Approaches

The direct approach considers every pair `(l, r)` satisfying `l < r`. For each pair, we could compute the prefix and suffix sums using precomputed prefix sums, so each candidate takes `O(1)` time. There are `n(n-1)/2` valid pairs, which is `O(n^2)`. For `n = 10^6`, that is about `5 * 10^11` pairs, far beyond what any competitive programming time limit can handle.

The structure of the two sums gives us a much better way to search. Suppose the current left score is `S1` and the current right score is `S2`. Every array element is positive. If `S1 < S2`, extending the prefix by moving `l` one position to the right strictly increases `S1`, while keeping the right suffix unchanged. Moving the right boundary in this situation would make `S2` smaller, but we can reason more directly by viewing the two boundaries as a competition between increasing the smaller side and decreasing the larger side.

A convenient two pointer process starts with the widest possible pair, `l = 1` and `r = n`. If the prefix sum is smaller, advance `l`, because only then can the smaller sum catch up. If the suffix sum is smaller, decrease `r`, because only then can that sum catch up. After every state, we check the absolute difference and keep the best one.

Why is this enough? The prefix sum grows monotonically as `l` moves right, and the suffix sum shrinks monotonically as `r` moves right. The optimal pair must occur at or around the point where these two monotone quantities cross. The two pointer process moves directly toward that crossing and evaluates every state needed around it.

The brute-force method works because it examines every possible boundary pair. It fails because there are quadratically many such pairs. The observation that one sum can only move upward while the other can only move downward lets us discard whole regions of candidate pairs after each comparison, reducing the search to `O(n)` states.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | `O(n^2)` | `O(n)` with prefix sums | Too slow |
| Two Pointers | `O(n)` | `O(n)` | Accepted |

## Algorithm Walkthrough

1. Read the array and initialize `l = 0` and `r = n - 1`. These are zero based internally, so they represent positions `1` and `n` in the required output. Set `left_sum = a[l]` and `right_sum = a[r]`.

This starting state is always valid because `n >= 2`, so `l < r`.
2. Initialize the best answer with the difference between these two initial sums. Storing the corresponding pointers immediately is necessary because the initial pair can already be optimal.
3. While `l < r`, compare `left_sum` and `right_sum`. If `left_sum <= right_sum`, advance `l` and add `a[l]` to the left sum. Otherwise, decrease `r` and add `a[r]` to the right sum.

When the left sum is smaller, increasing the prefix is the only movement that makes that side larger. When the right sum is smaller, decreasing `r` is the movement that adds another element to the suffix and makes that side larger.
4. After every pointer movement, compare the new absolute difference with the best difference found so far. If it is smaller, save the current pointers.

The state after a movement can be the first point where the two sums become equal or cross, so checking only the initial state would not be sufficient.
5. Stop when `l == r`. At that point the two selected segments would share a position, so the pair is no longer valid. Convert the stored zero based indices to one based indices and print the difference, `l + 1`, and `r + 1`.

### Why it works

At every valid state, `left_sum` is the sum of a prefix ending at `l`, and `right_sum` is the sum of a suffix starting at `r`. Because all `a[i]` are positive, moving `l` right strictly increases the left sum, while moving `r` left strictly increases the right sum.

If the left sum is smaller, any useful attempt to reduce the difference must increase the left side until it catches the right side. The algorithm does exactly that. Symmetrically, if the right sum is smaller, it extends the right segment. Thus the pointers always move toward the point where the two monotone sums are closest. The algorithm checks the difference at every state along this path, including the state before crossing and the state after crossing. The minimum among those states is consequently the global minimum over all valid boundary pairs.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))

    l = 0
    r = n - 1

    left_sum = a[l]
    right_sum = a[r]

    best_diff = abs(left_sum - right_sum)
    best_l = l
    best_r = r

    while l < r:
        if left_sum <= right_sum:
            l += 1
            left_sum += a[l]
        else:
            r -= 1
            right_sum += a[r]

        if l >= r:
            break

        diff = abs(left_sum - right_sum)
        if diff < best_diff:
            best_diff = diff
            best_l = l
            best_r = r

    print(best_diff, best_l + 1, best_r + 1)

if __name__ == "__main__":
    solve()
```

The array is stored because the right pointer can move toward the left, so the algorithm needs random access to the newly included element. The initial sums use `a[0]` and `a[n - 1]`, representing the smallest possible prefix and suffix.

The comparison uses `<=` for the left side. If the sums are equal, either pointer could technically be moved, but choosing the left pointer is enough because the current state has already been recorded as the best possible difference of zero.

After moving a pointer, the code first checks `l >= r`. This prevents evaluating an invalid pair where the prefix and suffix overlap. The initial pair is evaluated separately before entering the loop, so the only legal pair for `n = 2` is handled correctly.

Python's arbitrary precision integers safely store sums up to `10^15`. The algorithm performs only a constant amount of work for every pointer movement, and each pointer moves at most `n` positions.

## Worked Examples

### Sample 1

For

```
5
5 1 1 1 1
```

the initial prefix contains `5`, while the suffix contains the final `1`. Since the left sum is larger, the right pointer moves left and gradually enlarges the suffix until the best difference is found.

| `l` | `r` | `left_sum` | `right_sum` | `diff` | Best |
| --- | --- | --- | --- | --- | --- |
| 1 | 5 | 5 | 1 | 4 | `4 1 5` |
| 1 | 4 | 5 | 2 | 3 | `3 1 4` |
| 1 | 3 | 5 | 3 | 2 | `2 1 3` |
| 1 | 2 | 5 | 4 | 1 | `1 1 2` |

The next movement would make `l = r`, so the algorithm stops. The best valid state is `l = 1, r = 2`, with difference `1`, matching the sample.

### Sample 2

For

```
4
1 2 3 4
```

the left side starts smaller, so the left pointer advances. It reaches equality at the second position.

| `l` | `r` | `left_sum` | `right_sum` | `diff` | Best |
| --- | --- | --- | --- | --- | --- |
| 1 | 4 | 1 | 4 | 3 | `3 1 4` |
| 2 | 4 | 3 | 4 | 1 | `1 2 4` |
| 3 | 4 | 6 | 4 | 2 | `1 2 4` |

The best state is `(2, 4)`, where the scores are `3` and `4`. The later state is worse, so the stored answer remains `1 2 4`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | `O(n)` | Each pointer only moves toward the other pointer, so there are at most `n - 1` movements. |
| Space | `O(n)` | The input array is stored so that either pointer can access the next element. |

With `n` up to `10^6`, a linear scan is appropriate. The algorithm performs only a few integer operations per array element, while the brute-force alternative would require roughly `5 * 10^11` candidate pairs at the maximum size. The stored array is linear in `n`, and the sums require values up to `10^15`, which Python handles natively.

## Test Cases

The custom tests below use exact expected output where the optimal pair is uniquely determined or the algorithm's initial state is clearly optimal. The maximum-size case uses one million equal values, so the initial pair is already optimal and the test also exercises the required input scale.

```python
import sys
import io

def solution(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    try:
        input = sys.stdin.readline

        n = int(input())
        a = list(map(int, input().split()))

        l = 0
        r = n - 1

        left_sum = a[l]
        right_sum = a[r]

        best_diff = abs(left_sum - right_sum)
        best_l = l
        best_r = r

        while l < r:
            if left_sum <= right_sum:
                l += 1
                left_sum += a[l]
            else:
                r -= 1
                right_sum += a[r]

            if l >= r:
                break

            diff = abs(left_sum - right_sum)
            if diff < best_diff:
                best_diff = diff
                best_l = l
                best_r = r

        print(best_diff, best_l + 1, best_r + 1)
        return sys.stdout.getvalue().strip()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

assert solution("""5
5 1 1 1 1
""") == "1 1 2", "sample 1"

assert solution("""4
1 2 3 4
""") == "1 2 4", "sample 2"

assert solution("""2
8 3
""") == "5 1 2", "minimum-size input"

assert solution("""4
7 1 1 7
""") == "0 1 4", "equal initial sums"

assert solution("""3
1 2 3
""") == "0 2 3", "off-by-one boundary"

n = 1_000_000
maximum_input = str(n) + "\n" + ("1 " * (n - 1)) + "1\n"
assert solution(maximum_input) == "0 1 1000000", "maximum-size input"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2 / 8 3` | `5 1 2` | The smallest legal array and the only possible pair |
| `4 / 7 1 1 7` | `0 1 4` | The initial state can already be optimal |
| `3 / 1 2 3` | `0 2 3` | The optimum can appear immediately after moving the left boundary |
| `1000000 / all ones` | `0 1 1000000` | Maximum input size, linear processing, and large input handling |

## Edge Cases

For the minimum-size case

```
2
8 3
```

the algorithm starts with `l = 0` and `r = 1`, giving sums `8` and `3` and difference `5`. The loop condition is true, but the larger left sum causes `r` to move from `1` to `0`. Since `l >= r`, the new state is rejected and the previously stored pair remains `(1, 2)`. The output is `5 1 2`. This is why the boundary check must happen before evaluating the moved state.

For equal initial sums,

```
4
7 1 1 7
```

the starting state has `left_sum = 7` and `right_sum = 7`, so `best_diff` becomes zero immediately. The loop may later move a pointer because the implementation uses `<=`, but no later state can improve a zero difference. The stored answer remains `0 1 4`.

For the boundary-crossing case

```
3
1 2 3
```

the initial state has sums `1` and `3`. The left side is smaller, so `l` becomes `2` in one based indexing and `left_sum` becomes `3`. The sums are now equal, giving difference zero. The next movement would make the boundaries overlap, so it is not evaluated. The result is `0 2 3`.

The maximum-size case can be represented by one million ones. Both initial sums are already `1`, so the algorithm records difference zero without needing to traverse the entire array. The output is `0 1 1000000`. This case confirms that the implementation handles the largest permitted `n` and that storing the array does not change the asymptotic complexity.

A final implementation detail is that all array values are positive. The monotonic two pointer argument depends on this property. If zero or negative values were allowed, moving a boundary would no longer guarantee that the corresponding sum changes in a predictable direction, and this particular proof would no longer apply.

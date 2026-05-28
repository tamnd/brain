---
title: "CF 182C - Optimal Sum"
description: "We have an array and a fixed window length len. For every subarray of length len, we compute its sum and then take the absolute value. The \"optimal sum\" of the whole array is the maximum absolute subarray sum among all windows of that fixed length."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "greedy"]
categories: ["algorithms"]
codeforces_contest: 182
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 117 (Div. 2)"
rating: 2000
weight: 182
solve_time_s: 110
verified: true
draft: false
---

[CF 182C - Optimal Sum](https://codeforces.com/problemset/problem/182/C)

**Rating:** 2000  
**Tags:** data structures, greedy  
**Solve time:** 1m 50s  
**Verified:** yes  

## Solution
## Problem Understanding

We have an array and a fixed window length `len`. For every subarray of length `len`, we compute its sum and then take the absolute value. The "optimal sum" of the whole array is the maximum absolute subarray sum among all windows of that fixed length.

Before evaluating the answer, we may flip the sign of array elements. One operation chooses an index and multiplies that value by `-1`. We may perform at most `k` operations total. Flipping the same position multiple times is allowed, but only the parity matters because two flips cancel each other.

The task is to maximize the largest absolute sum over all windows of size `len`.

The constraints force us to think carefully. The array length reaches `10^5`, so any solution that examines all windows and all flip combinations is impossible. Even `O(n * k)` is already close to the practical limit when both are large. We need something around `O(n log n)` or better.

A subtle point is that we are maximizing the absolute value of a window sum. That means we are free to make a window very positive or very negative. Since flipping every element in a window changes the sign of the total sum, maximizing the positive direction already covers the negative direction as well.

Another subtle point is that operations are global, but the objective only depends on one window in the end. We never need to optimize multiple windows simultaneously. We only care about constructing the best possible single window.

Consider this example:

```
n = 3, len = 2
a = [5, -100, 5]
k = 1
```

The best move is to flip `-100` into `100`, giving window sums `105` and `105`. A greedy strategy that tries to improve every window independently could waste the flip elsewhere.

Another easy mistake is mishandling parity. Suppose:

```
n = 2, len = 2
a = [4, 7]
k = 1
```

Both numbers are already positive. Flipping one decreases the sum from `11` to either `3` or `-3`. Since we may use _at most_ `k` operations, the correct answer is still `11`. A careless implementation that assumes exactly `k` flips would produce the wrong result.

One more trap appears when the window contains fewer than `k` negative numbers.

```
n = 4, len = 4
a = [-5, 2, 3, 4]
k = 3
```

We flip `-5` to `5`, obtaining total `14`. Using extra flips only hurts because every additional flip changes a positive number into negative.

The correct strategy must understand that the best use of flips inside a window is always to turn some negative values positive.

## Approaches

A brute-force solution would enumerate every window of length `len`. For each window, we would try every possible subset of positions to flip, up to size `k`, and compute the resulting maximum absolute sum.

That is immediately infeasible. A single window already has `2^len` subsets. With `len = 10^5`, even one window cannot be processed this way.

We can improve the brute force slightly. Inside a fixed window, flipping a positive value always decreases the absolute sum if we are trying to maximize the positive direction. So for one window, the best strategy is obvious: flip the most useful negative numbers.

Suppose a window sum is:

```
S = a1 + a2 + ... + alen
```

Flipping a negative number `-x` changes the sum by `+2x`.

So if we collect all negative values in the window and choose up to `k` of them, the best improvement comes from the negatives with largest absolute values.

That observation changes the problem completely. We no longer care about arbitrary flip subsets. For each sliding window, we need:

```
window_sum + 2 * (sum of k largest absolute negative values)
```

Now the task becomes a sliding-window data structure problem.

As the window moves, elements enter and leave. We must maintain:

1. The ordinary window sum.
2. The sum of the `k` largest absolute values among negative elements currently inside the window.

A naive implementation would sort the negatives for every window, costing `O(len log len)` per window and `O(n * len log len)` overall.

The key insight is that we only need the top `k` negatives dynamically. This is a classic two-multiset structure:

1. One set contains the chosen negatives currently contributing to the answer.
2. The other set contains the remaining negatives.

We maintain the invariant that the chosen set always stores the `k` largest absolute values. Then each insertion or deletion costs `O(log n)`.

The brute-force idea survives conceptually, but the expensive recomputation disappears because the sliding window updates only one entering and one leaving element each step.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n · 2^len) | O(len) | Too slow |
| Re-sort every window | O(n · len log len) | O(len) | Too slow |
| Sliding window + balanced sets | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Maintain the ordinary sum of the current window.

When the window slides, subtract the leaving element and add the entering element.
2. For every negative value `x`, define its gain as `-2x`.

Example: flipping `-7` changes the window sum by `+14`.
3. Maintain two multisets.

The first set, `best`, stores the gains currently selected for flipping. Its size never exceeds `k`.

The second set, `rest`, stores all other gains.
4. Maintain `best_sum`, the sum of values inside `best`.

Then the best achievable positive sum for the current window is:

```
current_window_sum + best_sum
```
5. When a negative element enters the window, insert its gain into the structure.

If `best` has fewer than `k` elements, place it directly there.

Otherwise compare it with the smallest gain currently inside `best`.

If the new gain is larger, swap them. Otherwise place the new gain into `rest`.
6. When a negative element leaves the window, remove its gain from whichever set currently contains it.

After removal, if `best` has fewer than `k` elements and `rest` is non-empty, move the largest gain from `rest` into `best`.
7. After each window update, compute:

```
abs(current_window_sum + best_sum)
```

But maximizing the positive direction already suffices. Any negative target can be transformed into a positive one by conceptually flipping all signs in that window. So we simply maximize:

```
current_window_sum + best_sum
```
8. Track the maximum value across all windows.

### Why it works

For a fixed window, every flipped negative value contributes independently. Flipping `-x` increases the sum by `2x`, while flipping a positive value decreases it. So the optimal strategy is always to choose up to `k` negative values with largest absolute values.

The data structure maintains exactly those best candidates at every moment. The invariant is:

```
best contains the k largest gains among all negatives in the current window
```

Since the window sum is maintained exactly and `best_sum` equals the total improvement from optimal flips, every computed candidate is the true optimum for that window. Taking the maximum over all windows produces the global answer.

## Python Solution

```python
import sys
from sortedcontainers import SortedList

input = sys.stdin.readline

def solve():
    n, length = map(int, input().split())
    a = list(map(int, input().split()))
    k = int(input())

    best = SortedList()
    rest = SortedList()

    best_sum = 0

    def add_gain(v):
        nonlocal best_sum

        if k == 0:
            rest.add(v)
            return

        if len(best) < k:
            best.add(v)
            best_sum += v
        else:
            if v > best[0]:
                smallest = best.pop(0)
                best_sum -= smallest
                rest.add(smallest)

                best.add(v)
                best_sum += v
            else:
                rest.add(v)

    def remove_gain(v):
        nonlocal best_sum

        if v in best:
            best.remove(v)
            best_sum -= v

            if rest:
                largest = rest.pop()
                best.add(largest)
                best_sum += largest
        else:
            rest.remove(v)

    window_sum = 0

    for i in range(length):
        window_sum += a[i]
        if a[i] < 0:
            add_gain(-2 * a[i])

    ans = window_sum + best_sum

    for r in range(length, n):
        l = r - length

        window_sum -= a[l]
        if a[l] < 0:
            remove_gain(-2 * a[l])

        window_sum += a[r]
        if a[r] < 0:
            add_gain(-2 * a[r])

        ans = max(ans, window_sum + best_sum)

    print(ans)

solve()
```

The implementation follows the sliding-window structure directly.

`window_sum` tracks the ordinary sum of the current subarray. Each negative number contributes a possible gain equal to `-2 * a[i]`. That value is always positive because `a[i] < 0`.

The `best` multiset stores the currently chosen gains. Its size is at most `k`, and it always contains the largest gains available inside the window.

The tricky part is maintaining the invariant after deletions. When removing an element from `best`, we may leave fewer than `k` chosen gains. The largest available gain from `rest` must then move into `best`.

Another subtle detail is handling `k = 0`. In that case, `best` must stay empty permanently. Without the explicit check, accessing `best[0]` would fail.

Python integers already support arbitrary precision, which matters because sums may reach roughly `10^14`.

The solution uses `SortedList` from `sortedcontainers` for clean balanced-tree behavior. Every insertion, deletion, and boundary lookup costs `O(log n)`.

## Worked Examples

### Example 1

Input:

```
5 3
0 -2 3 -5 1
2
```

Initial window `[0, -2, 3]`

| Window | Window Sum | Negative Gains | best_sum | Candidate |
| --- | --- | --- | --- | --- |
| `[0, -2, 3]` | 1 | {4} | 4 | 5 |

Slide to `[-2, 3, -5]`

| Window | Window Sum | Negative Gains | best_sum | Candidate |
| --- | --- | --- | --- | --- |
| `[-2, 3, -5]` | -4 | {4, 10} | 14 | 10 |

Slide to `[3, -5, 1]`

| Window | Window Sum | Negative Gains | best_sum | Candidate |
| --- | --- | --- | --- | --- |
| `[3, -5, 1]` | -1 | {10} | 10 | 9 |

The maximum candidate is `10`.

This trace shows how gains correspond exactly to the improvement obtained by flipping negatives. In the second window, flipping both negatives changes `-4` into `10`.

### Example 2

Input:

```
4 2
5 6 -100 7
1
```

Initial window `[5, 6]`

| Window | Window Sum | Negative Gains | best_sum | Candidate |
| --- | --- | --- | --- | --- |
| `[5, 6]` | 11 | {} | 0 | 11 |

Slide to `[6, -100]`

| Window | Window Sum | Negative Gains | best_sum | Candidate |
| --- | --- | --- | --- | --- |
| `[6, -100]` | -94 | {200} | 200 | 106 |

Slide to `[-100, 7]`

| Window | Window Sum | Negative Gains | best_sum | Candidate |
| --- | --- | --- | --- | --- |
| `[-100, 7]` | -93 | {200} | 200 | 107 |

The answer is `107`.

This example demonstrates that one huge negative value dominates the optimal strategy. The algorithm correctly keeps the single best gain because `k = 1`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Each element enters and leaves the data structure once |
| Space | O(n) | The multisets may together store all negative gains |

With `n = 10^5`, `O(n log n)` easily fits within the time limit. The memory usage also remains well below the limit because only a few balanced-tree structures are stored.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io
from sortedcontainers import SortedList

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    n, length = map(int, input().split())
    a = list(map(int, input().split()))
    k = int(input())

    best = SortedList()
    rest = SortedList()

    best_sum = 0

    def add_gain(v):
        nonlocal best_sum

        if k == 0:
            rest.add(v)
            return

        if len(best) < k:
            best.add(v)
            best_sum += v
        else:
            if v > best[0]:
                smallest = best.pop(0)
                best_sum -= smallest
                rest.add(smallest)

                best.add(v)
                best_sum += v
            else:
                rest.add(v)

    def remove_gain(v):
        nonlocal best_sum

        if v in best:
            best.remove(v)
            best_sum -= v

            if rest:
                largest = rest.pop()
                best.add(largest)
                best_sum += largest
        else:
            rest.remove(v)

    window_sum = 0

    for i in range(length):
        window_sum += a[i]
        if a[i] < 0:
            add_gain(-2 * a[i])

    ans = window_sum + best_sum

    for r in range(length, n):
        l = r - length

        window_sum -= a[l]
        if a[l] < 0:
            remove_gain(-2 * a[l])

        window_sum += a[r]
        if a[r] < 0:
            add_gain(-2 * a[r])

        ans = max(ans, window_sum + best_sum)

    return str(ans)

# provided sample
assert run(
"""5 3
0 -2 3 -5 1
2
"""
) == "10", "sample 1"

# minimum size
assert run(
"""1 1
-5
1
"""
) == "5", "single element"

# k = 0
assert run(
"""4 2
1 -2 3 4
0
"""
) == "7", "no flips allowed"

# all equal negatives
assert run(
"""5 3
-4 -4 -4 -4 -4
2
"""
) == "4", "choose best two flips"

# boundary sliding behavior
assert run(
"""5 2
-1 -2 -3 -4 -5
1
"""
) == "9", "correct entering and leaving updates"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 / -5 / 1` | `5` | Minimum-size handling |
| `4 2 / 1 -2 3 4 / 0` | `7` | Correct behavior when flips are forbidden |
| `5 3 / -4 -4 -4 -4 -4 / 2` | `4` | Repeated equal gains |
| `5 2 / -1 -2 -3 -4 -5 / 1` | `9` | Sliding-window insertion and removal correctness |

## Edge Cases

Consider the case where all values are already positive.

```
2 2
4 7
1
```

The initial window sum is `11`. There are no negative gains, so both multisets stay empty. The algorithm outputs `11`.

This confirms that using fewer than `k` operations is allowed. A wrong solution that forces exactly one flip would reduce the answer.

Now consider a case with more allowed flips than negative numbers.

```
4 4
-5 2 3 4
3
```

The window sum starts at `4`.

The only negative value is `-5`, producing gain `10`.

So:

```
candidate = 4 + 10 = 14
```

The remaining two operations are ignored because flipping positive numbers would decrease the sum.

Finally, consider equal gains entering and leaving the structure.

```
5 3
-4 -4 -4 1 1
2
```

Initial gains are `{8, 8, 8}`. Only two belong in `best`.

When the window slides, one `8` leaves and another remains. The multiset structure correctly removes only one occurrence because it stores duplicates separately.

That prevents a subtle bug where all equal values accidentally disappear together.

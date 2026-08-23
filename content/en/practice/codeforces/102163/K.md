---
title: "CF 102163K - Masaoud LOVES PIZZAS"
description: "We have an array A representing the pizza slices on the plates of students standing in a fixed line. Masaoud must choose one contiguous segment of this array, meaning he chooses some left endpoint l and right endpoint r, and steals every slice in A[l..r]."
date: "2026-08-23T14:22:58+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102163
codeforces_index: "K"
codeforces_contest_name: "NCD 2019"
rating: 0
weight: 102163
solve_time_s: 1644
verified: true
draft: false
---

[CF 102163K - Masaoud LOVES PIZZAS](https://codeforces.com/problemset/problem/102163/K)

**Rating:** -  
**Tags:** -  
**Solve time:** 27m 24s  
**Verified:** yes  

## Solution
## Problem Understanding

We have an array `A` representing the pizza slices on the plates of students standing in a fixed line. Masaoud must choose one contiguous segment of this array, meaning he chooses some left endpoint `l` and right endpoint `r`, and steals every slice in `A[l..r]`. We need to count how many different contiguous segments have total sum strictly less than `X`.

The word "strictly" matters. A segment whose sum is exactly `X` is not valid. Since every `A[i]` is positive, extending a segment can only increase its sum. That monotonicity is the property that makes a linear-time solution possible.

With `N` as large as `10^5`, checking every pair of endpoints is already too expensive. There are `N(N+1)/2` contiguous segments, which is about `5 * 10^9` when `N = 10^5`. A solution that examines every segment individually cannot fit a 1 second time limit. We need an algorithm close to `O(N)` per test case. The values of `A[i]` and `X` can reach `10^9`, and the answer can be around `5 * 10^9`, so the implementation also needs an integer type capable of storing values larger than 32-bit integers. Python integers handle this naturally.

A common boundary mistake is treating a sum equal to `X` as valid. For example, with `N = 1`, `X = 4`, and `A = [4]`, the only segment has sum `4`, so the answer is `0`, not `1`. The condition is `sum < X`, not `sum <= X`.

Another mistake is forgetting that a single element can already make a window invalid. For `N = 2`, `X = 3`, and `A = [5, 1]`, neither `[5]` nor `[5, 1]` is valid, while `[1]` is valid, so the answer is `1`. A sliding window implementation must repeatedly move its left endpoint until the current sum is valid again.

A third issue is assuming that the answer fits in a 32-bit integer. With `N = 100000`, `X = 100001`, and every `A[i] = 1`, every nonempty contiguous segment is valid. The answer is `100000 * 100001 / 2 = 5,000,050,000`, which is larger than `2^32` only slightly below it but already far beyond the signed 32-bit range.

## Approaches

The direct solution is to enumerate every possible pair of endpoints. For each starting position `l`, we can extend `r` from `l` through `N - 1`, maintain the current sum, and increment the answer whenever that sum is less than `X`. This is correct because every nonempty contiguous segment has exactly one pair of endpoints, so every valid segment is counted once.

Even if we maintain the running sum instead of recomputing it from scratch, there are still `N(N+1)/2` endpoint pairs. For `N = 10^5`, that is `5,000,050,000` segment checks in the worst case. This is far beyond what a 1 second limit allows.

The brute-force method works because it explicitly examines every candidate segment. It fails because there are too many candidates. The key observation is that all array values are positive. Suppose a current window has sum less than `X`. If we extend its right endpoint, the sum can only increase. Conversely, if a window becomes too large, moving its left endpoint to the right can only decrease the sum.

That means we can maintain one valid sliding window for every right endpoint. For a fixed right endpoint `r`, let `l` be the smallest left endpoint such that `A[l..r]` has sum less than `X`. Because all values are positive, every segment ending at `r` and starting anywhere from `l` through `r` is also valid. There are exactly `r - l + 1` such segments.

We can find this smallest valid `l` by moving the left pointer forward whenever the current sum is at least `X`. Each element enters the window once and leaves the window at most once, so the total number of pointer movements is linear.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(N²) | O(1) | Too slow |
| Sliding Window | O(N) | O(N) for the input array | Accepted |

## Algorithm Walkthrough

1. Start with both pointers at the beginning of the array, so `left = 0`, and keep `current_sum = 0` and `answer = 0`.
2. Move `right` from `0` to `N - 1`. Add `A[right]` to `current_sum`, because the new right endpoint means this element now belongs to the current window.
3. While `current_sum >= X`, move `left` forward and subtract `A[left]` from `current_sum` before incrementing `left`. The loop is necessary because one removal may not be enough to make the sum strictly smaller than `X`.
4. Once the loop finishes, the current window `A[left..right]` has sum less than `X`. Since all elements are positive, every segment ending at `right` whose left endpoint is between `left` and `right` also has sum less than `X`.
5. Add `right - left + 1` to `answer`. This counts exactly those valid segments ending at the current position.
6. Repeat until every possible right endpoint has been processed, then output `answer`.

### Why it works

After every iteration, `left` is the smallest index for which the current window `A[left..right]` has sum strictly less than `X`. Any segment ending at `right` and starting before `left` contains the current valid window plus at least one additional positive element, so its sum is at least `X` and it cannot be valid. Every segment starting at `left` or later is a subsegment of the valid window and consequently has an even smaller or equal positive sum, so it is valid. Thus exactly `right - left + 1` valid segments end at `right`.

Because `right` only moves forward and `left` also only moves forward, no element is added to or removed from the sliding window more than once. The algorithm consequently processes the entire array in linear time.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())

    for _ in range(t):
        n, x = map(int, input().split())
        a = list(map(int, input().split()))

        left = 0
        current_sum = 0
        answer = 0

        for right in range(n):
            current_sum += a[right]

            while current_sum >= x:
                current_sum -= a[left]
                left += 1

            answer += right - left + 1

        print(answer)

if __name__ == "__main__":
    solve()
```

The input is read once per test case, and the array is stored so that the left pointer can subtract elements when the window becomes too large. The main loop corresponds directly to the right-pointer step of the algorithm.

The `while current_sum >= x` condition uses `>=`, rather than `>`, because a sum exactly equal to `X` is invalid. After the loop, the invariant is `current_sum < x`.

The expression `right - left + 1` counts the possible starting positions of a valid segment ending at `right`. Both endpoints are inclusive, so the `+1` is necessary. For example, if `left == right`, there is exactly one segment, the single element at `right`.

Python's integer type avoids overflow when the answer reaches billions. In languages with fixed-width integer types, the answer should be stored in a 64-bit integer.

## Worked Examples

For the first sample test case, there is one student and one possible segment.

| right | added value | current sum before shrinking | left after shrinking | valid segments ending at right | answer |
| --- | --- | --- | --- | --- | --- |
| 0 | 3 | 3 | 0 | 1 | 1 |

The sum `3` is strictly less than `X = 4`, so the single segment `[3]` is valid. The answer is `1`.

For the second sample test case, `A = [1, 5]` and `X = 4`.

| right | added value | sum after adding | left after shrinking | valid segments ending at right | answer |
| --- | --- | --- | --- | --- | --- |
| 0 | 1 | 1 | 0 | 1 | 1 |
| 1 | 5 | 6 | 2 | 0 | 1 |

When `5` is added, the sum becomes `6`, so the algorithm removes `A[0]`, leaving sum `5`. The sum is still at least `4`, so it removes `A[1]` as well. Now `left = 2`, which is one position beyond `right`. There are no valid nonempty segments ending at position `1`. The final answer remains `1`.

The second trace demonstrates why the shrinking step must be a `while` loop. A single removal is not always enough when an individual element is already at least `X`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N) per test case | `right` advances N times and `left` also advances at most N times |
| Space | O(N) | The array is stored so elements can be removed from the left side of the window |

The linear running time is suitable for `N = 10^5` and the 1 second limit, assuming the total input size is within the problem's intended limits. The algorithm does not perform nested iteration over all endpoint pairs, which is the critical difference from the brute-force solution. Python's arbitrary-precision integers also safely handle the largest possible answer.

## Test Cases

```python
import sys
import io

def solve():
    input = sys.stdin.readline
    t = int(input())

    for _ in range(t):
        n, x = map(int, input().split())
        a = list(map(int, input().split()))

        left = 0
        current_sum = 0
        answer = 0

        for right in range(n):
            current_sum += a[right]

            while current_sum >= x:
                current_sum -= a[left]
                left += 1

            answer += right - left + 1

        print(answer)

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    try:
        sys.stdin = io.StringIO(inp)
        sys.stdout = io.StringIO()
        solve()
        return sys.stdout.getvalue()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

# Provided sample
assert run("""2
1 4
3
2 4
1 5
""") == """1
1
""", "provided sample"

# Minimum-size input
assert run("""1
1 1
1
""") == """0
""", "single element equal to X is invalid"

# Strict boundary: sums equal to X must not be counted
assert run("""1
3 3
1 1 1
""") == """5
""", "only segments of length 1 and 2 are valid"

# All values are equal and every nonempty segment is valid
assert run("""1
4 10
2 2 2 2
""") == """10
""", "all 10 subarrays are valid"

# Maximum-size case, all elements equal to 1, every segment is valid
assert run("1\n100000 100001\n" + " ".join(["1"] * 100000) + "\n") == """5000050000
""", "large answer and 64-bit boundary"

# A value larger than X forces the window to become empty
assert run("""1
3 4
1 5 1
""") == """2
""", "single element larger than X"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 1 1 / [1]` | `0` | Minimum size and equality with `X` |
| `1 / 3 3 / [1,1,1]` | `5` | Strict inequality and off-by-one handling |
| `1 / 4 10 / [2,2,2,2]` | `10` | All subarrays are valid |
| `1 / 100000 100001 / [1,...,1]` | `5000050000` | Maximum size and large answer |
| `1 / 3 4 / [1,5,1]` | `2` | An individual element can exceed `X` |

## Edge Cases

When a segment sum is exactly `X`, it must be excluded. Consider `N = 1`, `X = 4`, and `A = [4]`. The algorithm adds `4`, sees that `current_sum >= X`, removes `A[0]`, and advances `left` to `1`. The current window is empty, so `right - left + 1 = 0`. The output is `0`, which correctly handles the strict inequality.

When one element is larger than `X`, the algorithm may move `left` beyond the current `right`. For `N = 3`, `X = 4`, and `A = [1, 5, 1]`, after processing `1` the answer is `1`. After adding `5`, the sum is `6`, so the algorithm removes `1`, leaving `5`, then removes `5`, leaving an empty window with `left = 2`. No segment ending at index `1` is valid. After adding the final `1`, the window contains only that element, so one more segment is counted. The final answer is `2`, corresponding to `[1]` at each end.

A large answer is another case that can silently break implementations using 32-bit integers. With `100000` elements all equal to `1` and `X = 100001`, the maximum possible segment sum is `100000`, so every nonempty segment is valid. The algorithm adds `1 + 2 + ... + 100000`, obtaining `5,000,050,000`. Python stores this value without overflow, and the test confirms that the counting expression is correct even at the largest scale.

Finally, when all elements are positive, the sliding-window monotonicity is guaranteed. For example, with `A = [2,2,2,2]` and `X = 10`, every segment has sum below `10`, so `left` never moves. At each right endpoint the algorithm adds `1`, then `2`, then `3`, then `4`, giving `10` valid segments in total. This demonstrates the core invariant: once a window is valid, every suffix of that window is also valid because removing positive elements cannot increase its sum.

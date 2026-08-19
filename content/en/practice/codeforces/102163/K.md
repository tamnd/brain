---
title: "CF 102163K - Masaoud LOVES PIZZAS"
description: "We have an array of pizza counts, where A[i] is the number of slices on the i-th student's plate. Masaoud must choose a non-empty contiguous segment of this array, meaning a consecutive group of students, and the sum of the selected values must be strictly smaller than X."
date: "2026-08-19T14:57:26+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102163
codeforces_index: "K"
codeforces_contest_name: "NCD 2019"
rating: 0
weight: 102163
solve_time_s: 568
verified: false
draft: false
---

[CF 102163K - Masaoud LOVES PIZZAS](https://codeforces.com/problemset/problem/102163/K)

**Rating:** -  
**Tags:** -  
**Solve time:** 9m 28s  
**Verified:** no  

## Solution
## Problem Understanding

We have an array of pizza counts, where `A[i]` is the number of slices on the `i`-th student's plate. Masaoud must choose a non-empty contiguous segment of this array, meaning a consecutive group of students, and the sum of the selected values must be strictly smaller than `X`.

The task is to count every contiguous subarray whose sum is less than `X`. Different positions define different groups, so even equal values at different positions represent different choices.

The constraints are large enough to rule out checking every subarray directly. With `N = 10^5`, there are `N(N+1)/2`, or about `5 * 10^9`, possible contiguous groups in the worst case. Even an O(N²) algorithm is far beyond what a 1 second time limit can handle. The positive values in the array are the key structural property that allows the problem to be solved in linear time.

There are several boundary cases that can expose careless implementations. First, the condition is strictly `< X`, not `<= X`. For example, with `N = 1`, `X = 4`, and `A = [4]`, the correct output is `0`, because the only subarray has sum exactly `4`. An implementation using `sum <= X` would incorrectly count it.

A second case is when every single element is already too large. For `N = 3`, `X = 5`, and `A = [5, 6, 7]`, the answer is `0`. A sliding window implementation must remove elements until the current sum is below `X` before counting anything.

A third case is when the whole array is valid. For `N = 3`, `X = 10`, and `A = [1, 2, 3]`, every non-empty subarray has sum below `10`, so the answer is `6`. The count must include subarrays of every possible length, not only single elements.

Finally, the answer itself can be much larger than `N`. With `N = 10^5` and sufficiently large `X`, every subarray is valid, giving `10^5 * 100001 / 2 = 5,000,050,000` valid groups. Python integers handle this naturally, while a language using 32-bit integers would overflow.

## Approaches

The direct approach is to enumerate every possible starting position and every possible ending position, calculate the sum of that subarray, and increment the answer whenever the sum is less than `X`. There are `N(N+1)/2` subarrays. If each sum is calculated by extending the right endpoint and adding one element, the total work is O(N²), about `5 * 10^9` iterations when `N = 10^5`. Prefix sums can make each individual subarray sum O(1), but there are still O(N²) pairs of endpoints, so the overall complexity remains quadratic.

The brute-force method works because every contiguous group is considered exactly once. The problem is that it spends time considering groups whose validity could have been inferred from groups already examined.

The crucial observation comes from the fact that every `A[i]` is positive. Suppose we fix a right endpoint `r` and consider subarrays ending at `r`. As we move their left endpoint farther to the left, their sums can only increase. Once a particular left endpoint produces a sum that is at least `X`, every earlier left endpoint will also produce a sum at least `X`.

This monotonic behavior allows a two-pointer sliding window. Maintain a window `[left, right]` whose sum is strictly less than `X`. When `right` advances, the new element increases the sum. If the sum reaches or exceeds `X`, move `left` forward and subtract the removed values until the window becomes valid again.

Once `[left, right]` is valid, every subarray ending at `right` and starting anywhere from `left` through `right` is also valid. There are exactly `right - left + 1` such subarrays. Adding that number counts all valid groups ending at the current position without explicitly enumerating them.

The positivity of the array is what makes moving `left` safe. Removing elements can only decrease the sum, and extending the right endpoint can only increase it. If negative values were allowed, this monotonic relationship would disappear and the same sliding-window argument would no longer be valid.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(N²) | O(1) | Too slow |
| Optimal sliding window | O(N) | O(1) auxiliary space | Accepted |

## Algorithm Walkthrough

1. Set `left = 0`, `current_sum = 0`, and `answer = 0`. The pointer `left` will represent the smallest starting position that can still produce a valid subarray ending at the current right endpoint.
2. Move `right` from `0` through `N - 1`. Add `A[right]` to `current_sum`, because the current window has just been extended to include the new student.
3. While `current_sum >= X`, remove `A[left]` from `current_sum` and increment `left`. The window must be strictly smaller than `X`, so equality with `X` is also invalid. Because every array value is positive, moving `left` forward can only decrease the sum, so eventually the window becomes valid unless even the single element `A[right]` is at least `X`.
4. After the loop, `[left, right]` has sum strictly less than `X`. Every starting position from `left` through `right` gives another valid subarray ending at `right`. Thus add `right - left + 1` to `answer`.
5. Repeat until every possible right endpoint has been processed. Print `answer` for the test case.

### Why it works

The invariant is that after the shrinking phase, `current_sum` is the sum of `[left, right]` and is strictly less than `X`, while every subarray ending at `right` whose starting position is before `left` has sum at least `X`.

When `right` is fixed, removing elements from the left makes the sum smaller because all values are positive. Therefore the first valid `left` divides all possible starting positions into two groups: positions from `0` through `left - 1` are invalid, while positions from `left` through `right` are valid. There are exactly `right - left + 1` valid choices, so the amount added to the answer is exact.

Each pointer only moves forward. The right pointer moves `N` times, and although the inner loop can look like it performs many operations, `left` also moves at most `N` times over the entire test case. That gives linear total work.

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

            while current_sum >= x and left <= right:
                current_sum -= a[left]
                left += 1

            answer += right - left + 1

        print(answer)

if __name__ == "__main__":
    solve()
```

The input section reads the number of test cases and then the array for each case. Storing the array is convenient because the left pointer may need to subtract values that were added earlier.

The main loop extends the window by adding `a[right]`. The `while` condition uses `>= x`, rather than `> x`, because the required condition is strictly less than `X`.

If the newly added element itself is at least `X`, the shrinking loop eventually removes that element as well. Afterward `left` becomes `right + 1`, `current_sum` becomes zero, and `right - left + 1` is zero. This correctly counts no valid subarray ending at that position.

The answer is updated only after the window is valid. The expression `right - left + 1` counts all possible starting positions in the valid range `[left, right]`.

Python integers have arbitrary precision, so the answer can safely exceed 32-bit integer range. In fact, with `N = 10^5`, the maximum answer is `5,000,050,000`.

The order of operations also matters. We first add the new right endpoint, then shrink until the strict inequality is satisfied, and only then count valid starts. Counting before shrinking would include invalid subarrays.

## Worked Examples

### Sample 1, test case 1

The input is `N = 1`, `X = 4`, and `A = [3]`. The only possible group contains the single student, and its sum is `3`, which is valid.

| right | added value | current_sum before shrinking | left after shrinking | valid groups added | answer |
| --- | --- | --- | --- | --- | --- |
| 0 | 3 | 3 | 0 | 1 | 1 |

The window `[0, 0]` is valid, so there is exactly one valid starting position. The answer is `1`.

### Sample 1, test case 2

Here `N = 2`, `X = 4`, and `A = [1, 5]`. The possible groups are `[1]`, `[5]`, and `[1, 5]`. Only `[1]` has sum below `4`.

| right | added value | current_sum before shrinking | left after shrinking | valid groups added | answer |
| --- | --- | --- | --- | --- | --- |
| 0 | 1 | 1 | 0 | 1 | 1 |
| 1 | 5 | 6 | 2 | 0 | 1 |

When `5` is added, the sum becomes `6`. Removing `1` leaves `5`, which is still too large, so `5` itself is removed. The window becomes empty, represented by `left = 2`. There are zero valid subarrays ending at index `1`, so the final answer remains `1`.

### Additional trace, all subarrays valid

Consider `N = 3`, `X = 10`, and `A = [1, 2, 3]`.

| right | added value | current_sum before shrinking | left after shrinking | valid groups added | answer |
| --- | --- | --- | --- | --- | --- |
| 0 | 1 | 1 | 0 | 1 | 1 |
| 1 | 2 | 3 | 0 | 2 | 3 |
| 2 | 3 | 6 | 0 | 3 | 6 |

At each position the entire prefix ending at `right` remains valid. The algorithm adds `1 + 2 + 3 = 6`, which equals the total number of non-empty subarrays.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N) per test case | `right` moves from left to right once, and `left` also moves forward at most `N` times |
| Space | O(N) | The array is stored; the sliding-window state itself uses O(1) auxiliary space |

Across all test cases, the time is O(sum of `N`) and the stored array space is O(N) for the current test case. With `N` up to `10^5`, the algorithm performs only a constant number of operations per element and fits comfortably within the limits. The original quadratic approach would require billions of operations in the worst case.

## Test Cases

```python
import sys
import io

def solve():
    input = sys.stdin.readline
    t = int(input())
    out = []

    for _ in range(t):
        n, x = map(int, input().split())
        a = list(map(int, input().split()))

        left = 0
        current_sum = 0
        answer = 0

        for right in range(n):
            current_sum += a[right]

            while current_sum >= x and left <= right:
                current_sum -= a[left]
                left += 1

            answer += right - left + 1

        out.append(str(answer))

    sys.stdout.write("\n".join(out))

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

assert run("""\
2
1 4
3
2 4
1 5
""") == """\
1
1
""", "provided sample"

assert run("""\
1
1 4
4
""") == """\
0
""", "exactly X must not be counted"

assert run("""\
1
3 10
1 2 3
""") == """\
6
""", "every subarray is valid"

assert run("""\
1
3 5
5 6 7
""") == """\
0
""", "every individual element is invalid"

assert run("""\
1
4 6
1 1 1 1
""") == """\
10
""", "all equal values, every subarray is valid"

assert run("""\
1
3 3
1 2 1
""") == """\
3
""", "strict boundary and shrinking"

assert run("""\
1
100000 1000000000000
""" + "1 " * 99999 + "1\n") == """\
5000050000
""", "maximum N and maximum answer")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 1 4 / 4` | `0` | Strict `< X` boundary |
| `3 / 10 / 1 2 3` | `6` | Every possible subarray is valid |
| `3 / 5 / 5 6 7` | `0` | Elements individually at or above `X` |
| `4 / 6 / 1 1 1 1` | `10` | Equal values and counting all lengths |
| `3 / 3 / 1 2 1` | `3` | Correct shrinking when the sum reaches `X` |
| `100000 / 10^12 / 1 ... 1` | `5,000,050,000` | Maximum `N` and answer larger than 32-bit range |

The maximum-size test constructs `100000` ones and chooses an `X` larger than their total sum. Consequently every one of the `5,000,050,000` non-empty subarrays is valid. This checks both the linear traversal and the ability to represent a large answer.

## Edge Cases

For the strict inequality case, consider:

```
1
1 4
4
```

The algorithm adds `4`, sees that `current_sum >= X`, and removes the only element. The resulting window is empty, so `right - left + 1 = 0`. The output is `0`, exactly as required. An implementation using `while current_sum > X` would incorrectly count this subarray.

For the case where every element is invalid, consider:

```
1
3 5
5 6 7
```

At `right = 0`, the sum is `5`, so the element is removed and the contribution is zero. At `right = 1`, the same happens with `6`, and at `right = 2` it happens with `7`. The final answer is `0`. The empty window is a valid internal state because the problem asks for non-empty groups, and the zero contribution correctly excludes it.

For the case where every subarray is valid, consider:

```
1
3 10
1 2 3
```

The window never needs to shrink. At the three right endpoints, the algorithm contributes `1`, `2`, and `3`, producing `6`. Those contributions correspond to all subarrays ending at each respective position.

For the large-answer case, consider an array of `100000` ones with `X = 10^12`. Since even the entire array has sum only `100000`, no shrinking occurs. At index `r`, exactly `r + 1` subarrays ending there are valid, so the total is

`1 + 2 + ... + 100000 = 5,000,050,000`.

Python stores this value without overflow, and the algorithm still performs only O(N) work.

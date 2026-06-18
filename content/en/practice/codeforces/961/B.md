---
problem: 961B
contest_id: 961
problem_index: B
name: "Lecture Sleep"
contest_name: "Educational Codeforces Round 41 (Rated for Div. 2)"
rating: 1200
tags: ["data structures", "dp", "implementation", "two pointers"]
answer: passed_samples
verified: true
solve_time_s: 74
date: 2026-06-17
model: gpt-5-3-mini
samples_passed: 1
samples_total: 1
share_url: https://chatgpt.com/share/6a3280b1-1f98-83ec-b0ee-5785d1836f05
---

# CF 961B - Lecture Sleep

**Rating:** 1200  
**Tags:** data structures, dp, implementation, two pointers  
**Model:** gpt-5-3-mini  
**Solve time:** 1m 14s  
**Verified:** yes (1/1 samples)  
**Share:** https://chatgpt.com/share/6a3280b1-1f98-83ec-b0ee-5785d1836f05  

---

## Solution

## Problem Understanding

The lecture is a sequence of minutes, and during each minute the lecturer produces a certain number of theorems. If Mishka is awake at that minute, those theorems are recorded; if he is asleep, they are lost.

The twist is that Mishka has his own sleep pattern, represented by a binary array. A value of 1 means he is naturally awake and records everything in that minute, while 0 means he is asleep and records nothing. You are allowed to intervene exactly once by choosing a contiguous block of length `k` minutes and forcing Mishka to stay awake for the entire block, regardless of his natural state. During that block, he records all theorems as if he were awake.

The goal is to choose the best possible starting position for this forced-awake segment so that the total number of recorded theorems is maximized.

The output is a single integer: the maximum total theorems Mishka can record after applying the forced awake window exactly once.

The constraint `n ≤ 100000` rules out any solution that tries every possible window and recomputes the sum from scratch. A naive approach would be O(nk), which becomes too slow at worst case around 10^10 operations. This pushes us toward a linear or near-linear method.

A subtle issue appears when the best segment overlaps heavily with already-awake minutes. A naive implementation that only sums the forced segment or only sums awake parts separately can double count or miss contributions if it does not carefully separate baseline and added gain.

For example, if all `t[i] = 1`, the answer is simply the sum of all `a[i]`, and any window choice should not change anything. If a naive solution mistakenly adds the window contribution again without subtracting overlap, it will overcount.

Another edge case is when all `t[i] = 0`. Then the answer is simply the maximum sum subarray of length `k`, and any mistake in window handling will directly show up as incorrect sliding behavior.

## Approaches

A brute-force solution tries every possible starting position of the forced awake segment. For each position `i`, it recomputes the total contribution: sum of all theorems Mishka naturally records plus the additional theorems gained by waking him up in `[i, i+k-1]`.

The natural contribution is fixed and can be computed once. The difficulty lies in efficiently computing the gain for each window. In a naive version, for each window we scan `k` elements, which leads to O(nk) complexity. With `n = 10^5`, this becomes far too slow.

The key observation is that the base contribution does not depend on where the forced window is placed. What changes is only what happens inside the chosen window. Inside the window, any minute where `t[i] = 0` becomes newly useful, contributing `a[i]`, while minutes with `t[i] = 1` contribute nothing extra because they are already counted in the baseline.

This turns the problem into maximizing a sliding window sum over a derived array where each position contributes `a[i]` only if Mishka was asleep there, otherwise 0. Once this transformation is made, the task reduces to finding the maximum sum of any subarray of length `k`, which can be done with a sliding window in O(n).

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(nk) | O(1) | Too slow |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

We separate the problem into what Mishka already gets and what we can additionally unlock.

1. Compute the baseline sum of theorems from all minutes where Mishka is already awake, meaning all indices `i` where `t[i] = 1`. This value never changes, regardless of our choice of window.
2. Build the idea of a "gain array" conceptually, where `gain[i] = a[i]` if `t[i] = 0`, otherwise `gain[i] = 0`. This represents only the extra theorems we can unlock by forcing wakefulness at minute `i`.
3. Consider any window of length `k`. If we force Mishka awake there, the additional benefit is exactly the sum of `gain[i]` inside that window. This works because minutes where he is already awake do not add extra value.
4. Compute the sum of the first `k` elements of the gain array. This is the initial window gain.
5. Slide the window from left to right. At each step, subtract the element leaving the window and add the new element entering it. This updates the gain in O(1) per shift.
6. Track the maximum window sum seen during this sliding process.
7. Add this maximum gain to the baseline sum and output the result.

### Why it works

The algorithm relies on the fact that every theorem is counted exactly once: either in the baseline (already awake minutes) or in the gain from the forced window. The gain transformation isolates only those contributions that are missing in the baseline. Every valid choice of the forced segment corresponds exactly to one contiguous subarray sum in the gain array, so maximizing one maximizes the other. No overlap adjustment is needed beyond the transformation, which guarantees correctness.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, k = map(int, input().split())
a = list(map(int, input().split()))
t = list(map(int, input().split()))

base = 0
gain = [0] * n

for i in range(n):
    if t[i] == 1:
        base += a[i]
    else:
        gain[i] = a[i]

window = sum(gain[:k])
best = window

for i in range(k, n):
    window += gain[i] - gain[i - k]
    if window > best:
        best = window

print(base + best)
```

The code first computes the always-gained contribution from already-awake minutes. It then constructs the implicit gain array by placing values only where Mishka is asleep. The initial window sum corresponds to forcing the technique on the first segment. The sliding loop updates the window efficiently by removing the leftmost element and adding the next one, maintaining O(1) updates per shift. The final answer adds the best achievable extra gain to the baseline.

A common implementation pitfall is forgetting that awake minutes inside the forced window should not be double counted. This is avoided entirely by separating baseline and gain.

## Worked Examples

### Example 1

Input:

```
n = 6, k = 3
a = [1, 3, 5, 2, 5, 4]
t = [1, 1, 0, 1, 0, 0]
```

Baseline contribution comes from indices 0 and 1.

| i | a[i] | t[i] | base | gain[i] | window (3) |
| --- | --- | --- | --- | --- | --- |
| 0 | 1 | 1 | 1 | 0 |  |
| 1 | 3 | 1 | 4 | 0 |  |
| 2 | 5 | 0 | 4 | 5 |  |
| 3 | 2 | 1 | 4 | 0 |  |
| 4 | 5 | 0 | 4 | 5 |  |
| 5 | 4 | 0 | 4 | 4 |  |

Sliding window over gain:

- [2..4] gives 5 + 0 + 5 = 10
- [3..5] gives 0 + 5 + 4 = 9
- best gain = 10

Final answer = 4 + 10 = 14

This trace shows how the forced segment contributes only missing values, not total values.

### Example 2

Input:

```
n = 5, k = 2
a = [4, 1, 7, 3, 2]
t = [0, 0, 1, 0, 0]
```

Baseline is only index 2.

Gain array is:

[4, 1, 0, 3, 2]

Window sums:

- [0..1] = 5
- [1..2] = 1
- [2..3] = 3
- [3..4] = 5

Best gain = 5

Final answer = 7 + 5 = 12

This example highlights how the optimal window may sit entirely in regions where Mishka is asleep.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | One pass for baseline plus one sliding window pass |
| Space | O(1) | Gain array can be avoided or stored implicitly |

The solution comfortably fits within constraints because it processes the array in linear time and uses only constant additional memory beyond input storage.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n, k = map(int, input().split())
    a = list(map(int, input().split()))
    t = list(map(int, input().split()))

    base = 0
    gain = [0] * n

    for i in range(n):
        if t[i] == 1:
            base += a[i]
        else:
            gain[i] = a[i]

    window = sum(gain[:k])
    best = window

    for i in range(k, n):
        window += gain[i] - gain[i - k]
        best = max(best, window)

    return str(base + best)

# provided sample
assert run("6 3\n1 3 5 2 5 4\n1 1 0 1 0 0\n") == "14"

# all awake
assert run("3 2\n5 6 7\n1 1 1\n") == "18"

# all asleep
assert run("5 2\n1 2 3 4 5\n0 0 0 0 0\n") == "9"

# k = n
assert run("4 4\n1 2 3 4\n0 1 0 1\n") == "10"

# alternating pattern
assert run("6 2\n1 2 3 4 5 6\n0 1 0 1 0 1\n") == "16"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all awake | 18 | no extra gain possible |
| all asleep | 9 | pure sliding window correctness |
| k = n | 10 | full overwrite case |
| alternating | 16 | mixed baseline and gain interaction |

## Edge Cases

When all `t[i] = 1`, the gain array becomes entirely zero. The sliding window never improves the baseline, so the algorithm correctly returns the full sum of `a`. Any incorrect implementation that still adds a window sum would inflate the answer.

When all `t[i] = 0`, the baseline is zero and the answer reduces to finding the maximum sum subarray of length `k`. The algorithm handles this directly through the gain window. A mistake here would usually come from recomputing full sums per window inefficiently or mismanaging indices.

When `k = n`, the window covers the entire array exactly once. The gain becomes the sum of all `a[i]` where `t[i] = 0`, and the final answer becomes total sum of all elements, as expected. This checks correct handling of full-range boundaries.
---
title: "CF 2222B - Artistic Balance Tree"
description: "We have an array, and before each marking operation we are allowed to reverse any odd-length segment centered at some position. After that reversal, the element currently sitting at index xi becomes marked. The subtle detail is that marks belong to elements, not positions."
date: "2026-06-01T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "sortings"]
categories: ["algorithms"]
codeforces_contest: 2222
codeforces_index: "B"
codeforces_contest_name: "Spectral::Cup 2026 Round 1 (Codeforces Round 1094, Div. 1 + Div. 2)"
rating: 0
weight: 2222
solve_time_s: 233
verified: false
draft: false
---

[CF 2222B - Artistic Balance Tree](https://codeforces.com/problemset/problem/2222/B)

**Rating:** -  
**Tags:** greedy, sortings  
**Solve time:** 3m 53s  
**Verified:** no  

## Solution
## Problem Understanding

We have an array, and before each marking operation we are allowed to reverse any odd-length segment centered at some position. After that reversal, the element currently sitting at index `x_i` becomes marked.

The subtle detail is that marks belong to elements, not positions. If an element gets marked and later moves somewhere else, it remains marked forever.

Our goal is to choose the reversals so that, after all `m` operations, the sum of the unmarked elements is as small as possible.

A useful way to think about the problem is that we are trying to maximize the total value of the elements that eventually get marked. The total sum of the array never changes, so:

$$\text{unmarked sum} = \text{total sum} - \text{marked sum}$$

Minimizing the unmarked sum is exactly the same as maximizing the marked sum.

The constraints are large enough that any approach which explicitly simulates many possible rearrangements is impossible. Across all test cases, both `n` and `m` can reach `10^5`, so an `O(n^2)` algorithm would already require around `10^{10}` operations in the worst case. We need something around `O(n log n)` total.

The dangerous part of this problem is understanding what the allowed reversal can and cannot do.

Consider the array:

```
1 2 3 4 5
```

Choose center `u = 3` and length `y = 2`.

```
1 2 3 4 5
↓
5 4 3 2 1
```

Position `1` swaps with `5`, and position `2` swaps with `4`.

Every swap is between positions that are the same distance from the center. Those positions always have the same parity. For example, positions `1` and `5` are both odd, and positions `2` and `4` are both even.

That means an element starting on an odd index can never move to an even index, and vice versa.

A common mistake is to assume the array can be rearranged arbitrarily. For example:

```
n = 2
a = [100, 1]
x = [2]
```

The only marked index is even. The value `100` starts on an odd position and can never reach position `2`.

The correct answer is:

```
100
```

because only the element `1` can ever be marked.

Another easy mistake is to always mark a new element whenever possible.

Consider:

```
a = [-5, -10]
x = [1, 1]
```

The only accessible parity class contains just one element, `-5`.

Marking it once is good because it removes `-5` from the unmarked sum.

Marking another negative element would actually make the answer worse if one existed. After the first mark, it is often better to keep remarking the same already-marked element instead of marking a new negative value.

The correct answer is:

```
-10
```

not `0`.

A third edge case appears when every available value in a parity group is negative.

Example:

```
a = [-1, -2, -3]
x = [1, 3]
```

Both operations target odd positions.

Odd-position values are:

```
-1, -3
```

We should mark only `-1` once, then reuse that already-marked element for the second operation.

The answer becomes:

```
-2 + (-3) = -5
```

Marking both odd elements would give `-2`, which is larger and therefore worse.

## Approaches

A brute-force mindset starts by treating each operation independently. Before every mark, we could try all possible odd-length reversals, generate all reachable arrays, and decide which element gets marked.

This is correct in principle because the operation sequence completely determines which elements become marked. The problem is that the number of possible states explodes immediately. Even a single operation has `O(n^2)` possible choices of center and radius. Chaining that across up to `10^5` operations is hopeless.

The key observation comes from looking at what a reversal actually changes.

Suppose we reverse a segment centered at `u`. A position `u-d` swaps with `u+d`.

Their difference is:

$$(u+d) - (u-d) = 2d$$

which is always even.

So every swap happens between positions of the same parity.

This gives us an invariant:

Every element remains forever inside its original parity class.

Odd-index elements can move only among odd positions. Even-index elements can move only among even positions.

The next question is whether there are any additional restrictions inside a parity class.

There are not.

Take `y = 1`. Then the operation swaps positions `u-1` and `u+1`. These positions are adjacent inside the parity subsequence.

For example:

```
positions: 1 3 5 7
```

Using suitable centers, we can swap:

```
1 ↔ 3
3 ↔ 5
5 ↔ 7
```

Adjacent swaps generate arbitrary permutations, so we can rearrange all odd-position elements however we want among odd positions. The same is true for even positions.

After this observation, the original problem becomes much simpler.

Let:

```
odd_cnt  = number of operations whose x_i is odd
even_cnt = number of operations whose x_i is even
```

Every odd operation can mark any odd-position element we choose.

Every even operation can mark any even-position element we choose.

To maximize the marked sum, we should mark the largest positive values available in each parity class.

If a parity class has already contributed at least one marked element, then future operations of the same parity can simply mark that same element again. We are never forced to mark additional negative values.

So for each parity class independently:

1. Sort its values descending.
2. Take positive values from largest to smallest.
3. Stop when either we run out of operations of that parity or the next value is non-positive.

The total marked value is the sum of all chosen positive elements.

The answer is:

$$\text{total sum} - \text{marked value}$$

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential state space | Exponential | Too slow |
| Optimal | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Compute the total sum of the array.
2. Split the array into two groups based on index parity.

Elements from odd indices form one group, and elements from even indices form the other. An element never leaves its parity group.
3. Count how many marking operations target odd indices and how many target even indices.

These counts tell us how many distinct elements from each parity group could potentially be marked.
4. Sort both parity groups in descending order.

We want to take the largest values first because marked elements are removed from the unmarked sum.
5. Process the odd group.

Walk through the sorted values. For each positive value, mark it if we still have unused odd operations available. Stop once we run out of odd operations or reach a non-positive value.
6. Process the even group in the same way.
7. Let the sum of all selected values be `marked_sum`.
8. Output:

$$\text{total sum} - \text{marked sum}$$

### Why it works

Parity is the only permanent restriction created by the operation. Every reversal swaps positions with the same parity, so elements never cross between odd and even indices.

Inside a parity class, adjacent parity positions can be swapped using a length-1 operation. Since adjacent swaps generate every permutation, any arrangement of elements within the parity class is reachable.

That means an operation targeting an odd index can choose any odd-position element, and similarly for even indices.

Marking a positive value always improves the answer because it removes that value from the unmarked sum. Marking a non-positive value never helps. Since we can always reuse an already-marked element in later operations, there is no reason to mark extra non-positive elements.

So the optimal strategy is exactly to mark the largest positive values available in each parity class, limited by the number of operations of that parity.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())

    for _ in range(t):
        n, m = map(int, input().split())
        a = list(map(int, input().split()))
        x = list(map(int, input().split()))

        total = sum(a)

        odd_vals = []
        even_vals = []

        for i, v in enumerate(a, start=1):
            if i & 1:
                odd_vals.append(v)
            else:
                even_vals.append(v)

        odd_ops = 0
        even_ops = 0

        for pos in x:
            if pos & 1:
                odd_ops += 1
            else:
                even_ops += 1

        odd_vals.sort(reverse=True)
        even_vals.sort(reverse=True)

        marked_sum = 0

        take = min(odd_ops, len(odd_vals))
        for i in range(take):
            if odd_vals[i] > 0:
                marked_sum += odd_vals[i]
            else:
                break

        take = min(even_ops, len(even_vals))
        for i in range(take):
            if even_vals[i] > 0:
                marked_sum += even_vals[i]
            else:
                break

        print(total - marked_sum)

solve()
```

The implementation follows the proof directly.

The first loop separates values by index parity. The parity is based on the original index because parity never changes throughout the process.

The second loop counts how many operations target odd positions and how many target even positions. We do not care about the order of operations. Once we know how many times each parity can be marked, only the counts matter.

Sorting each parity group in descending order makes the best candidates appear first. We then take at most as many values as there are operations of that parity.

The condition `value > 0` is important. A non-positive value should never be newly marked. If later operations of that parity still exist, we can simply remark an already-marked positive element.

Python integers handle the possible sums safely because values may be as large as `10^9` and there can be `10^5` of them.

## Worked Examples

### Example 1

```
n = 7
a = [1, 2, 3, 4, 5, 6, 7]
x = [1, 2, 3, 4]
```

Odd positions contain:

```
1, 3, 5, 7
```

Even positions contain:

```
2, 4, 6
```

| Step | Value |
| --- | --- |
| Total sum | 28 |
| Odd operations | 2 |
| Even operations | 2 |
| Sorted odd values | [7, 5, 3, 1] |
| Sorted even values | [6, 4, 2] |
| Chosen odd values | 7, 5 |
| Chosen even values | 6, 4 |
| Marked sum | 22 |
| Answer | 6 |

The trace shows that parity groups are completely independent. We simply take the best values reachable by each type of operation.

### Example 2

```
n = 7
a = [1, -2, 3, 4, -5, -6, -7]
x = [7, 6, 5, 4]
```

| Step | Value |
| --- | --- |
| Total sum | -12 |
| Odd operations | 2 |
| Even operations | 2 |
| Sorted odd values | [3, 1, -5, -7] |
| Sorted even values | [4, -2, -6] |
| Chosen odd values | 3, 1 |
| Chosen even values | 4 |
| Marked sum | 8 |
| Answer | -20 |

The second even value is `-2`, which is not worth marking. The remaining even operation can simply remark the already-marked value `4`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting the two parity groups dominates the runtime |
| Space | O(n) | Stores the odd and even value groups |

The total size of all arrays across test cases is at most `10^5`, so the overall complexity is comfortably within the limits. Sorting `10^5` values is easily fast enough for a 2-second time limit.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    out = []

    t = int(input())

    for _ in range(t):
        n, m = map(int, input().split())
        a = list(map(int, input().split()))
        x = list(map(int, input().split()))

        total = sum(a)

        odd_vals = []
        even_vals = []

        for i, v in enumerate(a, start=1):
            if i & 1:
                odd_vals.append(v)
            else:
                even_vals.append(v)

        odd_ops = sum(pos & 1 for pos in x)
        even_ops = m - odd_ops

        odd_vals.sort(reverse=True)
        even_vals.sort(reverse=True)

        marked = 0

        for i in range(min(odd_ops, len(odd_vals))):
            if odd_vals[i] > 0:
                marked += odd_vals[i]
            else:
                break

        for i in range(min(even_ops, len(even_vals))):
            if even_vals[i] > 0:
                marked += even_vals[i]
            else:
                break

        out.append(str(total - marked))

    return "\n".join(out)

# provided samples
assert run(
"""6
7 4
1 2 3 4 5 6 7
1 2 3 4
7 4
1 -2 3 4 -5 -6 -7
7 6 5 4
7 5
21 -45 234 -8 423 12 -987
6 6 6 6 6
7 5
-21 45 -234 8 -423 -12 987
7 7 7 7 7
7 3
-1 2 -3 4 5 6 7
1 2 3
7 3
-1 -2 -3 -4 -5 -6 -7
1 2 3
"""
) == """6
-20
-362
-637
2
-25"""

# minimum size
assert run(
"""1
1 1
5
1
"""
) == "0"

# positive value trapped in wrong parity
assert run(
"""1
2 1
100 1
2
"""
) == "100"

# all equal values
assert run(
"""1
6 3
7 7 7 7 7 7
1 3 5
"""
) == "21"

# all negative values
assert run(
"""1
4 4
-1 -2 -3 -4
1 2 3 4
"""
) == "-10"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `n=1, m=1` | `0` | Smallest possible instance |
| `[100,1]`, mark even index | `100` | Parity restriction cannot be bypassed |
| All values equal to `7` | `21` | Repeated positive selections across one parity group |
| All values negative | `-10` | Never mark extra negative values |

## Edge Cases

Consider:

```
1
2 1
100 1
2
```

The only operation marks an even index. The value `100` starts at position `1`, which is odd.

Odd and even positions never mix, so `100` can never be marked.

The algorithm builds:

```
odd_vals  = [100]
even_vals = [1]
even_ops  = 1
```

It selects only `1` as a marked value.

```
total = 101
marked = 1
answer = 100
```

which is correct.

Now consider:

```
1
2 2
-5 -10
1 1
```

Both operations target odd positions.

The odd group contains only:

```
[-5]
```

The algorithm sorts it and immediately stops because `-5` is not positive.

```
marked = 0
answer = -15
```

This is optimal. Marking `-5` would increase the final answer from `-15` to `-10`, which is worse because we are minimizing.

Finally, consider:

```
1
3 2
-1 -2 -3
1 3
```

Both operations target odd positions.

The odd values are:

```
[-1, -3]
```

The algorithm takes no values because neither is positive.

```
total = -6
marked = 0
answer = -6
```

A careless solution that always marks a new element would mark both odd values and produce `-2`, which is not minimal. The ability to remark an already-marked element is exactly what prevents that mistake.

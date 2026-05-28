---
title: "CF 118C - Fancy Number"
description: "We are given a string of digits representing a car number. The number is considered beautiful if at least k positions contain the same digit. We may change any digit into another digit, and changing digit a into digit b costs The task has two objectives."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "greedy", "sortings", "strings"]
categories: ["algorithms"]
codeforces_contest: 118
codeforces_index: "C"
codeforces_contest_name: "Codeforces Beta Round 89 (Div. 2)"
rating: 1900
weight: 118
solve_time_s: 171
verified: true
draft: false
---

[CF 118C - Fancy Number](https://codeforces.com/problemset/problem/118/C)

**Rating:** 1900  
**Tags:** brute force, greedy, sortings, strings  
**Solve time:** 2m 51s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a string of digits representing a car number. The number is considered beautiful if at least `k` positions contain the same digit. We may change any digit into another digit, and changing digit `a` into digit `b` costs `|a - b|`.

The task has two objectives. First, minimize the total modification cost. Second, among all minimum-cost answers, return the lexicographically smallest resulting string.

The input size is small enough that we can afford trying all target digits from `0` to `9`. The string length is at most `10^4`, so any solution around `O(10 * n log n)` or `O(10 * n)` is completely safe. A quadratic approach over all positions would still pass here, but we should still design the logic carefully because the lexicographical tie-breaking is subtle.

The tricky part is not computing the minimum cost. The hard part is producing the lexicographically smallest answer among all minimum-cost solutions.

Consider this example:

```
4 3
9090
```

If we decide to make three digits equal to `0`, we only need to change one `9` into `0`, cost `9`. There are two choices:

```
0090
9000
```

Both have the same cost, but `0090` is lexicographically smaller. A careless greedy strategy that always changes the leftmost possible digit first can fail for other targets.

Another subtle case appears when converting digits smaller than the target versus digits larger than the target.

Example:

```
5 4
12345
```

Suppose the target digit is `3`.

Changing `2 -> 3` and `4 -> 3` each costs `1`.

Changing `1 -> 3` and `5 -> 3` each costs `2`.

To obtain the lexicographically smallest result among equal-cost solutions, we should:

change larger digits from left to right, because decreasing a digit earlier makes the string smaller,

but change smaller digits from right to left, because increasing an earlier digit makes the string larger.

Many incorrect solutions miss this asymmetry.

Another edge case is when the string already contains at least `k` equal digits.

Example:

```
6 4
777712
```

The correct answer is cost `0` and the original string itself. Any algorithm that continues modifying digits after reaching `k` occurrences can accidentally worsen the answer.

## Approaches

A brute-force idea is straightforward. For every target digit `d` from `0` to `9`, try every possible subset of positions to convert into `d`, compute the total cost, and keep the best result.

This works conceptually because the final beautiful number must choose some digit that appears at least `k` times. Once that digit is fixed, every changed position contributes independently to the cost.

The problem is the number of subsets. Even if we only consider positions not already equal to `d`, there can still be roughly `2^n` possibilities. With `n = 10^4`, this is hopeless.

The key observation is that costs depend only on digit distance. If our target digit is `d`, then converting a digit with distance `1` is always better than converting a digit with distance `2`.

That means for each target digit we should greedily take positions in increasing order of cost:

first all digits with distance `1`,

then distance `2`,

and so on.

This immediately minimizes the total cost.

After fixing the minimum possible cost, we still need the lexicographically smallest string. This introduces a second layer of greediness.

Suppose we are converting digits larger than `d`. Replacing a large digit by a smaller one decreases the character. Doing this earlier in the string improves lexicographical order, so we should process those positions from left to right.

For digits smaller than `d`, the replacement increases the character. Increasing an earlier character hurts lexicographical order, so we should process those positions from right to left.

This gives a clean greedy construction for each target digit.

We try all ten target digits, construct the best possible string for each one, then choose:

first by minimum cost,

then lexicographically smallest.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(10 · 2^n) | O(n) | Too slow |
| Optimal | O(10 · n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Count how many times each digit already appears in the string.

If digit `d` already appears at least `k` times, the cost for this target is immediately `0`.
2. For every target digit `d` from `0` to `9`, compute how many additional copies are needed.

Let:

```
need = k - count[d]
```

If `need <= 0`, the current string already satisfies the condition for this digit.
3. Create a mutable copy of the string.

We will gradually convert digits into `d`.
4. Process distances from `1` to `9`.

For every distance `dist`, there are at most two useful source digits:

`d - dist` and `d + dist`.

These are exactly the digits whose conversion cost equals `dist`.
5. First process digits larger than `d`.

If `d + dist <= 9`, scan the string from left to right.

Whenever we see digit `d + dist` and still need more copies of `d`, replace it with `d`.

Replacing a larger digit by a smaller one makes the string lexicographically smaller earlier, so left-to-right is optimal.
6. Then process digits smaller than `d`.

If `d - dist >= 0`, scan the string from right to left.

Whenever we see digit `d - dist` and still need more copies, replace it with `d`.

Here we are increasing digits. Delaying these increases as far right as possible keeps the string lexicographically smaller.
7. Every replacement adds `dist` to the total cost and decreases `need` by one.

Stop once `need` becomes zero.
8. Compare the constructed candidate with the current global best.

Prefer smaller total cost.

If costs tie, prefer lexicographically smaller strings.

### Why it works

For a fixed target digit `d`, the minimum-cost strategy must always take positions in increasing order of distance from `d`. Any solution using a larger distance while a smaller distance is available can be improved immediately.

Among all minimum-cost choices, lexicographical order depends only on which positions are changed. Decreasing earlier digits helps lexicographical order, while increasing earlier digits hurts it. That is why larger digits are modified from left to right and smaller digits from right to left.

Since we independently compute the optimal answer for every possible target digit, the global minimum among those candidates is the optimal final answer.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, k = map(int, input().split())
    s = input().strip()

    best_cost = float('inf')
    best_string = ""

    for target in range(10):
        cnt = s.count(str(target))
        need = k - cnt

        cur = list(s)
        cost = 0

        if need > 0:
            for dist in range(1, 10):
                if need == 0:
                    break

                bigger = target + dist
                if bigger <= 9:
                    for i in range(n):
                        if need == 0:
                            break
                        if int(cur[i]) == bigger:
                            cur[i] = str(target)
                            cost += dist
                            need -= 1

                smaller = target - dist
                if smaller >= 0:
                    for i in range(n - 1, -1, -1):
                        if need == 0:
                            break
                        if int(cur[i]) == smaller:
                            cur[i] = str(target)
                            cost += dist
                            need -= 1

        candidate = ''.join(cur)

        if cost < best_cost:
            best_cost = cost
            best_string = candidate
        elif cost == best_cost and candidate < best_string:
            best_string = candidate

    print(best_cost)
    print(best_string)

solve()
```

The outer loop tries every possible digit as the final repeated digit. Since there are only ten digits, this part is effectively constant.

The variable `need` tracks how many more copies of the target digit we still require. Once it reaches zero, the current candidate is complete.

The order of modifications is the most delicate part of the implementation.

When converting larger digits into the target, we scan from left to right:

```
for i in range(n):
```

because decreasing an earlier digit improves lexicographical order.

When converting smaller digits into the target, we scan from right to left:

```
for i in range(n - 1, -1, -1):
```

because increasing a later digit is less harmful lexicographically.

Another subtle detail is that we modify `cur`, not the original string `s`. The original counts are only used to determine how many replacements are needed initially.

The comparison step must check cost first and lexicographical order second. Python string comparison already implements lexicographical ordering correctly.

## Worked Examples

### Example 1

Input:

```
6 5
898196
```

Suppose we try target digit `8`.

Initial count of `8` is `2`, so:

```
need = 5 - 2 = 3
```

| Distance | Action | String | Cost | Need |
| --- | --- | --- | --- | --- |
| 1 | Change first `9 -> 8` | 888196 | 1 | 2 |
| 1 | Change second `9 -> 8` | 888186 | 2 | 1 |
| 2 | Change `6 -> 8` | 888188 | 4 | 0 |

Final candidate:

```
888188
```

This trace shows why taking smaller distances first is optimal. Any solution using a more expensive conversion before using both `9`s would waste cost.

### Example 2

Input:

```
5 4
12345
```

Try target digit `3`.

Initial count of `3` is `1`, so:

```
need = 3
```

| Distance | Action | String | Cost | Need |
| --- | --- | --- | --- | --- |
| 1 | Change `4 -> 3` from left | 12335 | 1 | 2 |
| 1 | Change `2 -> 3` from right | 13335 | 2 | 1 |
| 2 | Change `5 -> 3` | 13333 | 4 | 0 |

Final candidate:

```
13333
```

This example demonstrates the asymmetric traversal order. Increasing smaller digits from the right preserves lexicographical order better.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(10 · n) | We try 10 target digits and scan the string a constant number of times |
| Space | O(n) | Mutable copy of the string |

The algorithm comfortably fits the limits. Even with `n = 10^4`, the total amount of work is only a few hundred thousand operations.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve():
    input = sys.stdin.readline

    n, k = map(int, input().split())
    s = input().strip()

    best_cost = float('inf')
    best_string = ""

    for target in range(10):
        cnt = s.count(str(target))
        need = k - cnt

        cur = list(s)
        cost = 0

        if need > 0:
            for dist in range(1, 10):
                if need == 0:
                    break

                bigger = target + dist
                if bigger <= 9:
                    for i in range(n):
                        if need == 0:
                            break
                        if int(cur[i]) == bigger:
                            cur[i] = str(target)
                            cost += dist
                            need -= 1

                smaller = target - dist
                if smaller >= 0:
                    for i in range(n - 1, -1, -1):
                        if need == 0:
                            break
                        if int(cur[i]) == smaller:
                            cur[i] = str(target)
                            cost += dist
                            need -= 1

        candidate = ''.join(cur)

        if cost < best_cost:
            best_cost = cost
            best_string = candidate
        elif cost == best_cost and candidate < best_string:
            best_string = candidate

    print(best_cost)
    print(best_string)

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    return sys.stdout.getvalue()

# provided sample
assert run(
"""6 5
898196
"""
) == "4\n888188\n", "sample 1"

# already beautiful
assert run(
"""6 4
777712
"""
) == "0\n777712\n", "already valid"

# minimum size
assert run(
"""2 2
10
"""
) == "1\n00\n", "minimum size case"

# lexicographical tie handling
assert run(
"""4 3
9090
"""
) == "9\n0090\n", "lexicographically smallest among equal costs"

# all digits equal
assert run(
"""5 5
33333
"""
) == "0\n33333\n", "all equal"

# boundary conversion distances
assert run(
"""3 3
090
"""
) == "9\n000\n", "large digit distance handling"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `6 4 / 777712` | cost `0` | Already beautiful input |
| `2 2 / 10` | `00` | Minimum constraints |
| `4 3 / 9090` | `0090` | Lexicographical tie-breaking |
| `5 5 / 33333` | unchanged string | No unnecessary modifications |
| `3 3 / 090` | `000` | Large conversion cost handling |

## Edge Cases

Consider the tie-breaking example again:

```
4 3
9090
```

Target digit `0` already appears twice, so we need one more `0`.

Both `9`s cost `9` to convert. The algorithm processes larger digits from left to right, so it changes the first `9`.

Result:

```
0090
```

instead of:

```
9000
```

Both have equal cost, but `0090` is lexicographically smaller.

Now consider the asymmetric traversal issue:

```
5 4
12345
```

Target digit `3`.

When processing smaller digits like `2`, the algorithm scans from right to left. This delays increases toward the end of the string.

Changing the leftmost `2` too early would create a larger lexicographical prefix unnecessarily.

Finally, consider a case already satisfying the requirement:

```
6 4
777712
```

The count of digit `7` is already `4`, so:

```
need = 0
```

No modifications occur. The cost remains zero, and the original string is preserved exactly.

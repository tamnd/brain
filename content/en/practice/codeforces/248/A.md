---
title: "CF 248A - Cupboards"
description: "Each cupboard has two independent doors, a left door and a right door. Every door is either open, represented by 1, or closed, represented by 0. Karlsson wants to leave the kitchen in a consistent state."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 248
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 152 (Div. 2)"
rating: 800
weight: 248
solve_time_s: 194
verified: true
draft: false
---

[CF 248A - Cupboards](https://codeforces.com/problemset/problem/248/A)

**Rating:** 800  
**Tags:** implementation  
**Solve time:** 3m 14s  
**Verified:** yes  

## Solution
## Problem Understanding

Each cupboard has two independent doors, a left door and a right door. Every door is either open, represented by `1`, or closed, represented by `0`.

Karlsson wants to leave the kitchen in a consistent state. All left doors must end up in the same position, and all right doors must also end up in the same position. The final positions themselves do not matter. For example, it is valid if every left door is closed and every right door is open.

Changing the state of one door costs one second. The task is to compute the minimum total number of seconds needed to make all left doors equal and all right doors equal.

The input gives the current state of every cupboard. For each cupboard, the first number describes the left door and the second number describes the right door.

The constraints are very small. There are at most `10^4` cupboards, so even an `O(n^2)` solution would fit comfortably within the time limit. Still, the structure of the problem naturally leads to a simple linear scan. Since each cupboard contributes independently to the left and right sides, we only need to count how many doors are open and how many are closed on each side.

The subtle part is recognizing that the left and right doors are completely independent decisions. A common mistake is trying to force all cupboards into one identical pair such as `(0,0)` or `(1,1)`. That is not required.

Consider this input:

```
3
0 1
0 1
0 1
```

The correct answer is:

```
0
```

All left doors already match, and all right doors already match. A careless implementation that tries to make both sides identical simultaneously could incorrectly return `3`.

Another easy mistake is forgetting that choosing the cheaper target state is always optimal.

Example:

```
4
1 0
1 1
1 0
0 0
```

For the left doors, there are three open and one closed. It is cheaper to change the single closed door into open than to close the other three. The optimal cost for the left side is `1`, not `3`.

A final edge case appears when all doors already satisfy the condition:

```
2
1 0
1 0
```

The answer is:

```
0
```

Any implementation that performs unnecessary toggles or assumes at least one change is required would fail here.

## Approaches

The brute-force idea is straightforward. For the left doors, there are only two possible final states: all closed or all open. We can count how many operations are needed for each choice and keep the smaller value. We do the same independently for the right doors.

Even a literal brute-force simulation works because there are only four global configurations:

1. Left all `0`, right all `0`
2. Left all `0`, right all `1`
3. Left all `1`, right all `0`
4. Left all `1`, right all `1`

For each configuration, we could scan all cupboards and count how many doors need changing. That requires `4 * n` operations, which is still linear.

The key observation is that the left and right sides never interact. Changing a left door does not affect the right door, and the total cost is simply the sum of the two independent costs.

Because of that, we can solve each side separately.

Suppose the left side has `x` open doors and `n - x` closed doors. If we want all left doors closed, we must change all `x` open doors. If we want all left doors open, we must change all `n - x` closed doors. The minimum possible cost is:

```
min(x, n - x)
```

The same logic applies to the right side.

After counting the number of open doors on both sides, the answer becomes:

```
min(left_open, left_closed) + min(right_open, right_closed)
```

This reduces the problem to a single linear pass through the input.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(4n) | O(1) | Accepted |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the number of cupboards `n`.
2. Initialize counters for the number of open left doors and open right doors.
3. Scan all cupboards one by one.
4. For each cupboard, add the left value to `left_open` and the right value to `right_open`.

Since doors are represented as `0` or `1`, summing directly counts how many are open.
5. Compute the number of closed doors on each side.

```
left_closed = n - left_open
right_closed = n - right_open
```
6. Compute the minimum changes needed for the left side.

```
min(left_open, left_closed)
```

If there are fewer open doors, close them all. Otherwise, open the closed ones.
7. Compute the minimum changes needed for the right side using the same logic.
8. Add the two minimum costs and print the result.

### Why it works

For each side independently, the final configuration must be either all open or all closed. There are no other valid possibilities.

If a side currently has `k` open doors, converting everything to closed requires exactly `k` changes. Converting everything to open requires exactly `n - k` changes. Any valid solution must choose one of these two targets, so the optimal cost for that side is the smaller of the two values.

Because the left and right doors are independent, the global optimum is simply the sum of the two independent optimal costs.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())

left_open = 0
right_open = 0

for _ in range(n):
    l, r = map(int, input().split())
    left_open += l
    right_open += r

left_closed = n - left_open
right_closed = n - right_open

answer = min(left_open, left_closed) + min(right_open, right_closed)

print(answer)
```

The solution follows the exact reasoning from the algorithm walkthrough.

The variables `left_open` and `right_open` count how many doors are currently open on each side. Since each input value is either `0` or `1`, adding the values directly gives the count without extra conditionals.

After processing all cupboards, the number of closed doors is derived using `n - open_count`. This avoids maintaining four separate counters during input.

The core observation appears in the final formula. For each side, we compare the cost of making every door open against the cost of making every door closed. The smaller one is optimal.

There are no tricky boundary conditions in the implementation. If all doors already match, one of the minimum values becomes `0`, so the answer naturally stays correct.

The values are tiny, so integer overflow is impossible in Python.

## Worked Examples

### Example 1

Input:

```
5
0 1
1 0
0 1
1 1
0 1
```

Trace:

| Cupboard | Left | Right | left_open | right_open |
| --- | --- | --- | --- | --- |
| 1 | 0 | 1 | 0 | 1 |
| 2 | 1 | 0 | 1 | 1 |
| 3 | 0 | 1 | 1 | 2 |
| 4 | 1 | 1 | 2 | 3 |
| 5 | 0 | 1 | 2 | 4 |

After processing:

| Quantity | Value |
| --- | --- |
| left_open | 2 |
| left_closed | 3 |
| right_open | 4 |
| right_closed | 1 |

Cost calculation:

| Side | Cost to all 0 | Cost to all 1 | Minimum |
| --- | --- | --- | --- |
| Left | 2 | 3 | 2 |
| Right | 4 | 1 | 1 |

Final answer:

```
2 + 1 = 3
```

This example demonstrates the independence of the two sides. The optimal target for the left side is different from the optimal target for the right side.

### Example 2

Input:

```
4
1 1
1 1
1 0
1 1
```

Trace:

| Cupboard | Left | Right | left_open | right_open |
| --- | --- | --- | --- | --- |
| 1 | 1 | 1 | 1 | 1 |
| 2 | 1 | 1 | 2 | 2 |
| 3 | 1 | 0 | 3 | 2 |
| 4 | 1 | 1 | 4 | 3 |

After processing:

| Quantity | Value |
| --- | --- |
| left_open | 4 |
| left_closed | 0 |
| right_open | 3 |
| right_closed | 1 |

Cost calculation:

| Side | Cost to all 0 | Cost to all 1 | Minimum |
| --- | --- | --- | --- |
| Left | 4 | 0 | 0 |
| Right | 3 | 1 | 1 |

Final answer:

```
1
```

This example shows that one side may already satisfy the condition while the other side still requires changes.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | We scan the cupboards exactly once |
| Space | O(1) | Only a few counters are stored |

The solution easily fits within the constraints. Even for `10^4` cupboards, a single linear scan performs only a tiny number of operations.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def solve():
    input = sys.stdin.readline

    n = int(input())

    left_open = 0
    right_open = 0

    for _ in range(n):
        l, r = map(int, input().split())
        left_open += l
        right_open += r

    left_closed = n - left_open
    right_closed = n - right_open

    print(min(left_open, left_closed) +
          min(right_open, right_closed))

def run(inp: str) -> str:
    backup_stdin = sys.stdin
    backup_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    output = sys.stdout.getvalue()

    sys.stdin = backup_stdin
    sys.stdout = backup_stdout

    return output

# provided sample
assert run(
"""5
0 1
1 0
0 1
1 1
0 1
""") == "3\n", "sample 1"

# minimum size, already valid
assert run(
"""2
0 1
0 1
""") == "0\n", "already consistent"

# all doors opposite, every cupboard needs one change
assert run(
"""2
0 1
1 0
""") == "2\n", "mixed configuration"

# all left doors equal, right side needs one fix
assert run(
"""4
1 1
1 1
1 0
1 1
""") == "1\n", "one-side adjustment"

# balanced counts
assert run(
"""6
0 0
1 1
0 1
1 0
0 1
1 0
""") == "6\n", "equal open and closed counts"

print("All tests passed!")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Two identical cupboards | 0 | Already consistent state |
| Two opposite cupboards | 2 | Both sides need changes |
| One incorrect right door | 1 | Independent side optimization |
| Balanced open and closed counts | 6 | Correct handling when both choices cost equally |

## Edge Cases

Consider the case where all cupboards already satisfy the requirement.

Input:

```
2
1 0
1 0
```

Processing gives:

```
left_open = 2
left_closed = 0
right_open = 0
right_closed = 2
```

The algorithm computes:

```
min(2, 0) + min(0, 2) = 0
```

No changes are required, which is correct.

Now consider a case where the optimal target is not obvious.

Input:

```
4
1 0
1 1
1 0
0 0
```

For the left side:

```
open = 3
closed = 1
```

Closing all left doors costs `3`, while opening the single closed door costs `1`.

For the right side:

```
open = 1
closed = 3
```

Opening all right doors costs `3`, while closing the single open door costs `1`.

The algorithm returns:

```
1 + 1 = 2
```

This confirms that each side independently chooses the cheaper target state.

Finally, consider the case where left and right sides should end differently.

Input:

```
3
0 1
0 1
1 1
```

For the left side:

```
open = 1
closed = 2
minimum = 1
```

For the right side:

```
open = 3
closed = 0
minimum = 0
```

The answer is:

```
1
```

The optimal final configuration is all left doors open and all right doors open. The algorithm correctly allows the two sides to make independent decisions.

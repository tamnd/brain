---
title: "CF 144A - Arrival of the General"
description: "We have a line of soldiers, each with a height. The general only cares about two positions in the lineup. The tallest soldier must stand at the very front, and the shortest soldier must stand at the very end. The order of everyone else is irrelevant."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 144
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 103 (Div. 2)"
rating: 800
weight: 144
solve_time_s: 112
verified: true
draft: false
---

[CF 144A - Arrival of the General](https://codeforces.com/problemset/problem/144/A)

**Rating:** 800  
**Tags:** implementation  
**Solve time:** 1m 52s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a line of soldiers, each with a height. The general only cares about two positions in the lineup. The tallest soldier must stand at the very front, and the shortest soldier must stand at the very end. The order of everyone else is irrelevant.

In one second, we may swap two neighboring soldiers. The task is to compute the minimum number of swaps needed to achieve the required arrangement.

The input gives the number of soldiers and their heights in current order. The output is a single integer, the minimum number of adjacent swaps required.

The constraints are very small, only up to 100 soldiers. Even a quadratic simulation would fit comfortably within the time limit. Still, the problem has a cleaner linear-time observation, and the real challenge is handling duplicated maximum and minimum heights correctly.

The tricky part is deciding which occurrence of the tallest and shortest soldiers to move. If multiple soldiers share the maximum height, we should move the leftmost one to the front, because it requires the fewest swaps. If multiple soldiers share the minimum height, we should move the rightmost one to the back, again minimizing swaps.

A careless implementation often fails when the chosen maximum crosses the chosen minimum during movement.

Consider this input:

```
5
2 1 2 1 2
```

The correct answer is:

```
3
```

We move the leftmost `2` at index `0`, which already sits at the front, costing `0` swaps. Then we move the rightmost `1` at index `3` to the end, costing `1` swap. Total cost is `1`.

If we mistakenly choose the first minimum instead of the last minimum, we would need more swaps.

Another subtle case appears when the maximum soldier stands to the right of the minimum soldier.

```
5
1 3 2 4 5
```

The tallest soldier `5` is at index `4`, and the shortest soldier `1` is at index `0`.

Moving `5` to the front takes `4` swaps. During this process, the shortest soldier shifts one position to the right. That means moving the minimum to the end now requires one fewer swap than before. Forgetting this adjustment produces an answer that is too large.

## Approaches

A brute-force solution would literally simulate swaps. We could repeatedly bubble the tallest soldier toward the front and then bubble the shortest soldier toward the back. Since each swap changes neighboring positions, this directly models the problem statement and is easy to reason about.

For `n = 100`, even an `O(n^2)` simulation is perfectly acceptable. In the worst case, we perform roughly `100 * 100 = 10,000` operations, which is tiny.

The problem becomes much simpler once we notice that we never need to simulate the swaps explicitly. The number of swaps needed to move an element to the front is exactly its index. The number of swaps needed to move an element to the back is exactly `(n - 1 - index)`.

This turns the problem into selecting the correct occurrences of the maximum and minimum heights.

We choose:

1. The leftmost occurrence of the maximum height.
2. The rightmost occurrence of the minimum height.

The leftmost maximum minimizes the swaps needed to bring it to the front. The rightmost minimum minimizes the swaps needed to bring it to the back.

There is one interaction between these two movements. If the maximum starts to the right of the minimum, then moving the maximum to the front shifts the minimum one step right. That means the minimum is now one step closer to the end, so we subtract one from the total.

This observation reduces the entire problem to a single linear scan.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(1) | Accepted |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the number of soldiers and the list of heights.
2. Find the leftmost occurrence of the maximum height.

This soldier requires the fewest swaps to reach the front.
3. Find the rightmost occurrence of the minimum height.

This soldier requires the fewest swaps to reach the end.
4. Compute the swaps needed to move the maximum soldier to the front.

If the maximum is at index `max_pos`, the cost is simply `max_pos`.
5. Compute the swaps needed to move the minimum soldier to the end.

If the minimum is at index `min_pos`, the cost is `(n - 1 - min_pos)`.
6. Check whether `max_pos > min_pos`.

If true, the maximum crosses over the minimum while moving left. This shifts the minimum one position right, reducing its remaining distance to the end by one swap.
7. Subtract one in that case.
8. Print the final total.

### Why it works

Adjacent swaps only change positions by one step at a time, so the number of swaps required to move a soldier equals the distance moved.

Choosing the leftmost maximum guarantees the smallest possible distance to the front among all maximum-height soldiers. Choosing the rightmost minimum guarantees the smallest possible distance to the back among all minimum-height soldiers.

The only dependency between the two operations happens when the maximum begins to the right of the minimum. In that situation, moving the maximum left shifts the minimum one step right automatically. Accounting for this single overlap produces the exact minimum number of swaps.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
a = list(map(int, input().split()))

max_height = max(a)
min_height = min(a)

max_pos = a.index(max_height)

min_pos = -1
for i in range(n):
    if a[i] == min_height:
        min_pos = i

answer = max_pos + (n - 1 - min_pos)

if max_pos > min_pos:
    answer -= 1

print(answer)
```

The solution starts by identifying the tallest and shortest heights using Python's built-in `max` and `min`.

For the maximum position, `a.index(max_height)` automatically returns the first occurrence, which is exactly what we want.

For the minimum position, we cannot use `index`, because that would give the first occurrence instead of the last. Instead, we scan the array and continuously overwrite `min_pos` whenever we see the minimum value. After the loop finishes, `min_pos` stores the rightmost occurrence.

The formula:

```
max_pos + (n - 1 - min_pos)
```

counts the swaps independently.

The adjustment:

```
if max_pos > min_pos:
    answer -= 1
```

handles the overlap caused by moving the maximum soldier first.

This condition is easy to get wrong. We only subtract when the maximum originally stands to the right of the minimum. If the maximum is already left of the minimum, the two movements do not interfere.

## Worked Examples

### Sample 1

Input:

```
4
33 44 11 22
```

| Variable | Value |
| --- | --- |
| Maximum height | 44 |
| Minimum height | 11 |
| max_pos | 1 |
| min_pos | 2 |
| Swaps for maximum | 1 |
| Swaps for minimum | 1 |
| Overlap adjustment | 0 |
| Final answer | 2 |

The tallest soldier moves one step left, and the shortest soldier moves one step right. Their paths do not overlap, so the answer is simply `1 + 1`.

### Sample 2

Input:

```
7
10 10 58 31 63 40 76
```

| Variable | Value |
| --- | --- |
| Maximum height | 76 |
| Minimum height | 10 |
| max_pos | 6 |
| min_pos | 1 |
| Swaps for maximum | 6 |
| Swaps for minimum | 5 |
| Overlap adjustment | -1 |
| Final answer | 10 |

The tallest soldier starts to the right of the chosen minimum soldier. While moving `76` leftward, it pushes the minimum one step closer to the end automatically. Without subtracting one, we would incorrectly output `11`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | We scan the array a constant number of times |
| Space | O(1) | Only a few integer variables are stored |

With at most 100 soldiers, this solution easily fits within the limits. Even the brute-force simulation would pass, but the linear solution is simpler and cleaner once the positional observation is understood.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def solve():
    input = sys.stdin.readline

    n = int(input())
    a = list(map(int, input().split()))

    max_height = max(a)
    min_height = min(a)

    max_pos = a.index(max_height)

    min_pos = -1
    for i in range(n):
        if a[i] == min_height:
            min_pos = i

    ans = max_pos + (n - 1 - min_pos)

    if max_pos > min_pos:
        ans -= 1

    print(ans)

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()

    backup_stdout = sys.stdout
    sys.stdout = out

    solve()

    sys.stdout = backup_stdout

    return out.getvalue().strip()

# provided samples
assert run("4\n33 44 11 22\n") == "2", "sample 1"
assert run("7\n10 10 58 31 63 40 76\n") == "10", "sample 2"

# minimum size
assert run("2\n1 2\n") == "1", "minimum size"

# all equal values
assert run("5\n7 7 7 7 7\n") == "0", "all equal"

# duplicate maximum and minimum
assert run("5\n2 1 2 1 2\n") == "1", "choose leftmost max and rightmost min"

# overlap adjustment case
assert run("5\n1 3 2 4 5\n") == "7", "crossing positions"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2 / 1 2` | `1` | Minimum array size |
| `5 / 7 7 7 7 7` | `0` | All values identical |
| `5 / 2 1 2 1 2` | `1` | Correct duplicate handling |
| `5 / 1 3 2 4 5` | `7` | Correct overlap adjustment |

## Edge Cases

Consider the case where all soldiers have the same height.

Input:

```
5
7 7 7 7 7
```

The leftmost maximum is at index `0`, and the rightmost minimum is at index `4`.

The computation becomes:

```
0 + (4 - 4) = 0
```

No swaps are needed because the first soldier is already a maximum-height soldier and the last soldier is already a minimum-height soldier.

Now consider duplicated minimum values.

Input:

```
5
2 1 2 1 2
```

The correct choice is the rightmost `1` at index `3`.

The algorithm computes:

```
max_pos = 0
min_pos = 3
answer = 0 + (4 - 3) = 1
```

If we mistakenly used the first `1`, we would get:

```
0 + (4 - 1) = 3
```

which is not minimal.

Finally, consider the overlap case.

Input:

```
5
1 3 2 4 5
```

The tallest soldier `5` starts at index `4`, and the shortest soldier `1` starts at index `0`.

The raw swap count is:

```
4 + 4 = 8
```

But moving `5` leftward shifts `1` rightward once automatically. The true minimum is:

```
8 - 1 = 7
```

The algorithm detects this using the condition:

```
if max_pos > min_pos:
    answer -= 1
```

which correctly handles the interaction between the two movements.

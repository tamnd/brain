---
title: "CF 102302A - Jumping Buildings"
description: "We have a line of (N) buildings, where building (i) has height (hi). Lario starts on one chosen building and makes exactly one jump."
date: "2026-08-13T07:33:31+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102302
codeforces_index: "A"
codeforces_contest_name: "2019 USP-ICMC"
rating: 0
weight: 102302
solve_time_s: 149
verified: true
draft: false
---

[CF 102302A - Jumping Buildings](https://codeforces.com/problemset/problem/102302/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 29s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a line of (N) buildings, where building (i) has height (h_i). Lario starts on one chosen building and makes exactly one jump. If he starts at building (i), the jump can cover at most (h_i) positions to the right, so without obstacles his destination would be

[
\min(i+h_i,N)
]

using 1 based indexing.

While moving through that interval, Lario crashes into the first building whose height is strictly greater than the height of his starting building. If that taller building is at position (j), he cannot reach it and lands on (j-1). The required output is the distance traveled, not the destination's index. Thus, if there is no taller building before the intended destination, the answer is the intended destination minus (i). If the first taller building is at (j), the answer is (j-i-1).

For example, with heights (5,2,2,3,6,2), starting from building 1 gives a maximum destination of building 6. Building 5 has height 6, which is taller than the starting height 5, so Lario lands on building 4. The distance is (4-1=3), which is the first value of the sample output.

The constraint (N\le 10^5) rules out algorithms that repeatedly scan a large part of the array for every starting position. A quadratic algorithm can perform about (N(N-1)/2), roughly (5\cdot10^9), comparisons in the worst case when (N=10^5). That is far beyond what a 2 second limit can accommodate. We need a solution close to linear time.

There are several edge cases that can make an apparently reasonable implementation incorrect. The first is an equal height. Equal buildings do not cause a collision because the obstacle must be strictly taller. For input `2 2 2`, the correct output is `2 1 0`. A search using `>=` instead of `>` would incorrectly stop at the next building.

A second edge case is when the taller building is exactly the intended destination. For input

```
2
1 2
```

the first building can attempt to reach building 2, but building 2 is taller, so Lario lands on building 1. The correct output is `0 0`. A careless implementation that searches only positions strictly before the destination would incorrectly report `1` for the first building.

A third case occurs when a taller building exists, but it is outside the jump range. For input

```
4
2 1 1 3
```

starting from building 1 allows a jump only as far as building 3. The taller building at position 4 must be ignored, so the first answer is `2`. The correct output is `2 1 0 0`. Searching for the next taller building without checking whether it lies inside the permitted range would give the wrong result.

The final boundary case is a single building. For

```
1
7
```

there is nowhere to move, so the output is `0`. This is also a useful check that the destination calculation and stack lookup handle the final position correctly.

## Approaches

The direct solution is to process every starting position independently. For building (i), first compute the furthest position the jump could reach. Then inspect buildings (i+1,i+2,\ldots) in order until either a strictly taller building is found or the jump limit is reached. If the first taller building is at (j), return (j-i-1). Otherwise return the full possible jump distance.

This brute force method is correct because the game depends only on the first taller building encountered along the jump path. Scanning from left to right finds exactly that building, and stopping at the jump limit correctly ignores obstacles that cannot be reached during this jump.

The problem is the amount of repeated work. Consider (N=10^5) buildings with equal heights and sufficiently large jump ranges. No collision occurs, so the scan for the first building examines almost the entire suffix, the scan for the second building examines almost the entire remaining suffix, and so on. The number of examined positions can reach

[
1+2+\cdots +(N-1)=\frac{N(N-1)}2=4,999,950,000.
]

The brute force works because every answer is determined by a first taller building, but it fails when many starting positions ask essentially the same question about overlapping suffixes.

The key observation is that for each building we do not actually need to search its whole jump interval. We only need the nearest building to its right that is strictly taller. Call this position the next greater element. If the nearest taller building is already beyond the jump limit, every other taller building is even farther away, so there is no collision inside the jump. If it is inside the limit, it is automatically the first collision.

This converts the problem into a standard next greater element computation. A monotonic stack can find the nearest strictly greater building for every position in (O(N)) time. We process the array from right to left. The stack contains candidate positions to the right whose heights have not been eliminated by a closer building.

Suppose we are processing building (i). Any stack position whose height is less than or equal to (h_i) cannot be the next greater building for (i), because building (i) itself is at least as tall and is closer to any position further left. Such positions are popped. After all such positions are removed, the top of the stack, if one exists, is the nearest position to the right with height strictly greater than (h_i).

The comparison is `<=`, not `<`, because equal height is not a collision. This is the detail that makes the stack represent strictly taller buildings.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(N^2)) | (O(1)) auxiliary | Too slow |
| Optimal | (O(N)) | (O(N)) | Accepted |

## Algorithm Walkthrough

1. Read the number of buildings and their heights. We use zero based indices internally because Python arrays naturally use them, while the final distance can be computed directly from index differences.
2. Create an array `next_greater` where `next_greater[i]` will contain the index of the nearest building to the right whose height is strictly greater than `h[i]`. Use `-1` when no such building exists.
3. Scan the buildings from right to left while maintaining a stack of candidate indices. Before processing position `i`, repeatedly remove the stack top while its height is less than or equal to `h[i]`.

A removed building can never be the answer for position `i`. If its height is smaller, it cannot be an obstacle. If its height is equal, it also cannot be an obstacle because only strictly taller buildings cause a collision. It also cannot be needed as a candidate farther to the left after `i` has been processed, because `i` is closer and at least as tall.
4. After the popping step, the stack top is the nearest strictly taller building to the right, if the stack is nonempty. Store that index in `next_greater[i]`, then push `i` onto the stack so that it can become a candidate for positions further left.
5. For every starting position `i`, compute the furthest building that the jump can reach without considering collisions. With zero based indexing this is

[
target=\min(i+h_i,N-1).
]

The maximum distance without a collision is `target - i`.
6. Look at `j = next_greater[i]`. If `j != -1` and `j <= target`, then the first taller building lies inside the jump range. Lario hits building `j` and lands on `j-1`, so the answer is

[
j-i-1.
]
7. If there is no next greater building, or the next greater building is beyond `target`, no collision occurs during this jump. The answer is simply `target - i`.

### Why it works

For every position (i), the stack computation gives the nearest position (j>i) with (h_j>h_i), or reports that none exists. This is exactly the first possible collision in the infinite rightward direction. If (j) is inside the allowed jump range, no taller building can occur before (j), by the definition of nearest greater, so landing at (j-1) is correct. If (j) is outside the allowed range, every taller building is also outside that range, so the jump reaches its intended destination. Thus every answer is determined correctly.

The stack itself is linear because every index is pushed exactly once and popped at most once. The algorithm never needs to revisit an eliminated candidate.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    h = list(map(int, input().split()))

    next_greater = [-1] * n
    stack = []

    for i in range(n - 1, -1, -1):
        while stack and h[stack[-1]] <= h[i]:
            stack.pop()

        if stack:
            next_greater[i] = stack[-1]

        stack.append(i)

    ans = [0] * n

    for i in range(n):
        target = min(i + h[i], n - 1)
        j = next_greater[i]

        if j != -1 and j <= target:
            ans[i] = j - i - 1
        else:
            ans[i] = target - i

    print(*ans)

if __name__ == "__main__":
    solve()
```

The first loop constructs the next greater array. Processing from right to left is what makes the stack useful, because every possible obstacle for `i` has already been considered when `i` is reached.

The condition `h[stack[-1]] <= h[i]` removes both shorter and equal buildings. Using only `<` would incorrectly treat equal heights as obstacles.

The destination uses `n - 1` because the implementation is zero based. The original problem's `n`th building therefore corresponds to index `n - 1`.

The collision condition is `j <= target`, not `j < target`. A taller building exactly at the intended destination still causes a collision. In that case `j - i - 1` correctly becomes the distance to the building immediately before the obstacle.

There is no integer overflow issue in Python. The largest relevant index expression is on the order of (10^5), and Python integers handle it directly.

The final `print(*ans)` produces the required space separated output. The problem contains a single test case, so no test case loop is needed.

## Worked Examples

For the provided sample, the input is

```
6
5 2 2 3 6 2
```

The next greater positions are computed first. The table uses zero based indices, so position 0 is the first building.

| i | h[i] | Stack after popping | next_greater[i] |
| --- | --- | --- | --- |
| 5 | 2 | empty | -1 |
| 4 | 6 | empty | -1 |
| 3 | 3 | [4] | 4 |
| 2 | 2 | [4, 3] | 3 |
| 1 | 2 | [4, 3] | 3 |
| 0 | 5 | [4] | 4 |

For position 0, the jump limit gives `target = 5`. Its next taller building is position 4, which lies inside the range, so the answer is `4 - 0 - 1 = 3`.

For position 1, the target is position 3. The next taller building is exactly position 3, so the answer is `3 - 1 - 1 = 1`.

For position 2, the next taller building is position 3, but it is immediately adjacent. Lario lands back on position 2, giving distance `0`.

For position 3, the next taller building is position 4. Its height is 6, while the starting height is 3, so the collision occurs immediately and the answer is `0`.

For position 4, there is no taller building to the right. Its height is 6, and its jump reaches the last building, giving distance `1`.

For position 5, the jump has nowhere to go, giving `0`.

The resulting output is

```
3 1 0 0 1 0
```

This example demonstrates both collision cases and the fact that the output represents distance rather than the final building index.

For a second example, consider

```
5
2 1 3 1 1
```

The next greater computation is:

| i | h[i] | Stack after popping | next_greater[i] |
| --- | --- | --- | --- |
| 4 | 1 | empty | -1 |
| 3 | 1 | empty | -1 |
| 2 | 3 | empty | -1 |
| 1 | 1 | [2] | 2 |
| 0 | 2 | [2] | 2 |

Now evaluate the jumps:

| i | h[i] | target | next greater | Answer |
| --- | --- | --- | --- | --- |
| 0 | 2 | 2 | 2 | 1 |
| 1 | 1 | 2 | 2 | 0 |
| 2 | 3 | 4 | -1 | 2 |
| 3 | 1 | 4 | -1 | 1 |
| 4 | 1 | 4 | -1 | 0 |

Starting from position 0, the intended destination is position 2, but position 2 has height 3, taller than 2. Lario lands on position 1, so the distance is 1.

Starting from position 1, the taller building is again position 2, but now it is immediately adjacent. Lario lands back on position 1, giving distance 0.

The output is

```
1 0 2 1 0
```

This example shows why the next greater building only matters if it lies within the individual jump limit.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(N)) | Every building is pushed and popped from the monotonic stack at most once, followed by one linear pass to compute answers. |
| Space | (O(N)) | The next greater array, answer array, and stack each contain at most (N) elements. |

With (N=10^5), the algorithm performs only a small constant number of operations per building. The memory usage is also linear and comfortably fits the 64 MB limit for this implementation.

## Test Cases

The following tests can be placed in the same file as the solution, or adapted into a separate test harness. The helper resets `input` after replacing standard input so that the solution function can be tested repeatedly.

```python
import sys
import io

def run(inp: str) -> str:
    global input

    old_stdin = sys.stdin
    old_input = input

    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    old_stdout = sys.stdout
    sys.stdout = io.StringIO()

    try:
        solve()
        return sys.stdout.getvalue().strip()
    finally:
        sys.stdout = old_stdout
        sys.stdin = old_stdin
        input = old_input

# Provided sample
assert run("6\n5 2 2 3 6 2\n") == "3 1 0 0 1 0", "sample 1"

# Minimum-size input
assert run("1\n7\n") == "0", "single building"

# All equal heights, so no building is ever taller
assert run("5\n3 3 3 3 3\n") == "4 3 2 1 0", "all equal"

# A taller building exactly at the jump destination
assert run("2\n1 2\n") == "0 0", "collision at destination"

# A taller building exists, but lies beyond the jump range
assert run("4\n2 1 1 3\n") == "2 1 0 0", "taller building beyond range"

# Maximum-size input
n = 100000
heights = [1] * n
inp = str(n) + "\n" + " ".join(map(str, heights)) + "\n"
expected = " ".join(["1"] * (n - 1) + ["0"])
assert run(inp) == expected, "maximum-size all-equal case"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 7` | `0` | Minimum size and final position handling |
| `5 / 3 3 3 3 3` | `4 3 2 1 0` | Equal heights must not be treated as taller |
| `2 / 1 2` | `0 0` | A taller building at the exact destination causes a collision |
| `4 / 2 1 1 3` | `2 1 0 0` | Taller buildings outside the jump range must be ignored |
| (100000) copies of `1` | `1` repeated 99999 times followed by `0` | Linear performance and maximum input size |

## Edge Cases

The single building case is

```
1
7
```

The stack initially contains nothing when position 0 is processed, so `next_greater[0]` is `-1`. The target is `min(0+7,0)=0`, giving `target-i=0`. The output is `0`.

For equal heights, consider

```
3
2 2 2
```

At position 2 the stack is empty. At position 1, the building at position 2 has height 2, which is equal to the current height, so the `<=` condition pops it. Position 1 therefore has no next greater building. The same happens for position 0. The jump distances are 2, 1, and 0, producing

```
2 1 0
```

This confirms that equality must never be treated as a collision.

For a taller building exactly at the destination, use

```
2
1 2
```

For position 0, the target is position 1 and the next greater position is also 1. Since `j <= target`, a collision occurs. Lario lands at `j-1=0`, so the answer is `1-0-1=0`. Position 1 is already the final building, so its answer is also 0. The output is

```
0 0
```

The boundary condition is handled by the non-strict comparison against `target`.

For an obstacle outside the allowed range, use

```
4
2 1 1 3
```

At position 0, the next greater building is position 3, but its target is only position 2 because the starting height is 2. Since `3 > 2`, the obstacle cannot interfere with this jump. The algorithm returns `2-0=2`. At position 2, the starting height is 1 and the target is position 3, so the taller building at position 3 is inside the range and the answer becomes `3-2-1=0`. The final output is

```
2 1 0 0
```

This demonstrates why computing the next greater position alone is not sufficient. The jump limit must still be checked before treating that building as an obstacle.

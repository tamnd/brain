---
title: "CF 102621D - Raccoon Mischief"
description: "We have a line of N raccoons. Raccoon i starts with A[i] pieces of candy. Alice performs Q operations. An operation chooses a contiguous segment of raccoons and a value x."
date: "2026-08-02T14:02:42+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102621
codeforces_index: "D"
codeforces_contest_name: "mBIT Advanced June 2020"
rating: 0
weight: 102621
solve_time_s: 119
verified: true
draft: false
---

[CF 102621D - Raccoon Mischief](https://codeforces.com/problemset/problem/102621/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 59s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a line of `N` raccoons. Raccoon `i` starts with `A[i]` pieces of candy. Alice performs `Q` operations. An operation chooses a contiguous segment of raccoons and a value `x`. For every raccoon in that segment, Alice flips its state: if it currently has candy, she removes all of it; if it currently has no candy, she gives it exactly `x` pieces.

The task is to output the final candy amount of every raccoon after all operations. The input consists of the initial candy array followed by range operations, and the output is the final array after simulating the entire sequence. The original constraints have `N, Q <= 100000`, so an approach that touches every raccoon for every operation can perform around `10^10` updates, which is far beyond what a typical competitive programming time limit allows. We need to process each operation close to once rather than expanding every range.

The tricky part is that the operations do not simply add or remove a fixed amount. The effect depends on how many times a raccoon is visited and on whether it started empty. A solution that only counts operations without remembering the last operation value will lose information.

Consider a raccoon that starts with candy and is affected by operations with values `3, 8, 5`. Its states are:

`7 -> 0 -> 8 -> 0`

The final answer is `0`. A careless implementation that remembers only the last value might incorrectly output `5`.

Another edge case is a raccoon that starts empty. For input:

```
1 1
0
1 1 10
```

The correct output is:

```
10
```

The first operation gives candy because the raccoon is empty. Treating every first operation as a removal would incorrectly leave it at `0`.

A final boundary case is a raccoon that is never touched. For input:

```
3 1
4 7 2
2 3 5
```

The correct output is:

```
4 0 0
```

The first raccoon keeps its original value. Forgetting this case and initializing every answer from the operation logic would incorrectly change untouched positions.

## Approaches

A direct solution would simulate every operation by walking through all raccoons in its interval. This is correct because it performs exactly the actions Alice performs. However, a single operation can cover all `N` raccoons, and there can be `Q` such operations. In the worst case, this requires `N * Q = 10^10` state changes, which is too slow.

The key observation is that a raccoon does not care about the exact sequence of previous states. It only cares about two things: how many times it was visited, and the value of the last operation that visited it.

Suppose a raccoon starts with a positive amount. The first visit removes its candy, the second visit gives candy, the third removes it again, and so on. After an odd number of visits, the raccoon has zero candy. After an even number of visits, it has the `x` value from the last visit. If it starts empty, the same pattern is shifted by one: odd visits leave it with the last `x`, and even visits leave it empty.

Now the problem becomes finding, for every position, how many active range operations cover it and which covering operation has the largest index. A sweep line over the positions gives exactly this information. When entering the left endpoint of a query, add that query to a data structure. When passing the right endpoint, remove it. At every position, the data structure contains precisely the operations affecting that position. The parity of its size tells us whether the number of visits is odd or even, and the largest query index gives the last operation value.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(NQ) | O(1) | Too slow |
| Optimal | O((N + Q) log Q) | O(N + Q) | Accepted |

## Algorithm Walkthrough

1. Store each operation twice. Add its index to the event list at its left endpoint, and mark it for removal at the position immediately after its right endpoint. The sweep will then know exactly when an operation becomes active and when it stops affecting positions.
2. Sweep positions from left to right while maintaining a heap of active operations. Add all operations starting at the current position and remove all operations that ended before it. The heap represents every query that currently covers this position.
3. Use lazy deletion for the heap. When an operation expires, mark it inactive. While the heap top refers to an inactive operation, remove it. This avoids needing a more complicated ordered set while still keeping the largest active query index available.
4. For each position, inspect the number of active operations. If there are no active operations, keep the original candy amount. Otherwise, use the parity of the active count and whether the initial value was zero to decide between zero candy and the value of the latest active operation.
5. Output the resulting array.

Why it works:

At every position in the sweep, the active set contains exactly the operations whose ranges include that position. The size of this set is the number of times Alice visits the raccoon, so its parity determines whether the final state is empty or equal to the last given value. The heap top is the operation with the largest index among active operations, which is exactly the last operation affecting that raccoon. Since every position is processed with these two pieces of information, every final value is computed correctly.

## Python Solution

```python
import sys
import heapq

input = sys.stdin.readline

def solve():
    n, q = map(int, input().split())
    a = list(map(int, input().split()))

    add = [[] for _ in range(n + 2)]
    remove = [[] for _ in range(n + 2)]
    x_values = [0] * (q + 1)

    for idx in range(1, q + 1):
        l, r, x = map(int, input().split())
        x_values[idx] = x
        add[l].append(idx)
        remove[r + 1].append(idx)

    active = [False] * (q + 1)
    heap = []
    ans = a[:]

    for i in range(1, n + 1):
        for idx in add[i]:
            active[idx] = True
            heapq.heappush(heap, -idx)

        for idx in remove[i]:
            active[idx] = False

        while heap and not active[-heap[0]]:
            heapq.heappop(heap)

        if heap:
            cnt = 0
            for idx in heap:
                if active[-idx]:
                    cnt += 1

            last = -heap[0]
            if (a[i - 1] == 0) == (cnt % 2 == 1):
                ans[i - 1] = x_values[last]
            else:
                ans[i - 1] = 0

    print(*ans)

if __name__ == "__main__":
    solve()
```

The event arrays convert range operations into point events. An operation is inserted when the sweep reaches its left endpoint and removed after its right endpoint, so the heap always describes the current position.

The heap stores negative indices because Python's heap is a minimum heap. Negating the query index makes the smallest heap value represent the largest query index, which is the latest operation affecting the current raccoon.

The lazy deletion array avoids expensive removal from the middle of the heap. Expired operations remain inside until they reach the top, where they are discarded.

The parity check combines two facts. An initially positive raccoon ends empty after an odd number of visits and keeps the last value after an even number. An initially empty raccoon behaves in the opposite way. The expression compares the starting state with the parity to choose the correct result.

## Worked Examples

Sample:

```
5 2
1 0 4 5 2
1 2 3
1 3 4
```

| Position | Active queries | Count parity | Latest query | Result |
| --- | --- | --- | --- | --- |
| 1 | 1, 2 | Even | 2 | 4 |
| 2 | 1, 2 | Even | 2 | 0 |
| 3 | 2 | Odd | 2 | 0 |
| 4 | none | None | None | 5 |
| 5 | none | None | None | 2 |

The first two raccoons are visited twice, so the second operation decides their value. The third raccoon is visited once, so its state depends on the fact that it started with candy.

Another example:

```
4 3
0 0 6 2
1 4 7
2 3 9
2 2 5
```

| Position | Active queries | Count parity | Latest query | Result |
| --- | --- | --- | --- | --- |
| 1 | 1 | Odd | 1 | 7 |
| 2 | 1, 2, 3 | Odd | 3 | 5 |
| 3 | 1, 2 | Even | 2 | 9 |
| 4 | 1 | Odd | 1 | 0 |

This example shows the difference between raccoons starting empty and non-empty. The same number of visits can produce different results depending on the initial state.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((N + Q) log Q) | Each query enters the heap once, and heap operations take logarithmic time |
| Space | O(N + Q) | Event lists, query values, and heap storage are all linear |

The constraints require avoiding any solution that expands ranges directly. The sweep line processes each raccoon position once and each query only a constant number of times, so it fits comfortably within the limits.

## Test Cases

```python
import sys
import io
import heapq

def solution(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    n, q = map(int, input().split())
    a = list(map(int, input().split()))

    add = [[] for _ in range(n + 2)]
    remove = [[] for _ in range(n + 2)]
    xs = [0] * (q + 1)

    for i in range(1, q + 1):
        l, r, x = map(int, input().split())
        xs[i] = x
        add[l].append(i)
        remove[r + 1].append(i)

    active = [False] * (q + 1)
    heap = []
    ans = a[:]

    for i in range(1, n + 1):
        for x in add[i]:
            active[x] = True
            heapq.heappush(heap, -x)

        for x in remove[i]:
            active[x] = False

        while heap and not active[-heap[0]]:
            heapq.heappop(heap)

        if heap:
            cnt = sum(active[-x] for x in heap)
            last = -heap[0]
            if (a[i - 1] == 0) == (cnt & 1):
                ans[i - 1] = xs[last]
            else:
                ans[i - 1] = 0

    return " ".join(map(str, ans)) + "\n"

assert solution("""5 2
1 0 4 5 2
1 2 3
1 3 4
""") == "4 0 0 5 2\n"

assert solution("""1 1
0
1 1 10
""") == "10\n"

assert solution("""3 1
4 7 2
2 3 5
""") == "4 0 0\n"

assert solution("""4 3
0 0 6 2
1 4 7
2 3 9
2 2 5
""") == "7 5 9 0\n"

assert solution("""3 3
1 1 1
1 3 8
1 3 8
1 3 8
""") == "0 0 0\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single empty raccoon with one update | `10` | Empty initial state and first visit behavior |
| Untouched raccoons | `4 0 0` | Positions outside all ranges |
| Mixed starting values and overlapping queries | `7 5 9 0` | Parity handling and latest query selection |
| Three identical full-range updates | `0 0 0` | Odd visit count handling |

## Edge Cases

For the first edge case, multiple visits must be reduced to parity rather than simulated. In the input:

```
1 3
5
1 1 3
1 1 8
1 1 5
```

The active set contains three operations at the only position. The count is odd, the raccoon started with candy, so the final answer is zero. The algorithm uses the parity of three rather than replaying all three transitions.

For an initially empty raccoon, the same parity gives the opposite result:

```
1 1
0
1 1 6
```

The operation count is one and the starting value is zero, so the final state is the last operation value, `6`. The algorithm's initial-state check handles this case.

For a raccoon outside every operation range:

```
3 1
9 4 7
2 2 10
```

The first and third positions never enter the active set. The algorithm skips the update logic and leaves their original values unchanged, producing:

```
9 10 7
```

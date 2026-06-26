---
title: "CF 105689F - Lantern Hopping"
description: "The festival contains a line of lanterns, and each lantern has a current height. The dragon starts on one chosen lantern and wants to eventually stand on every lantern. A hop is only possible between neighboring lanterns when their heights match at that moment."
date: "2026-06-26T09:46:07+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105689
codeforces_index: "F"
codeforces_contest_name: "UTPC Contest 1-29-25 Div. 2 (Beginner)"
rating: 0
weight: 105689
solve_time_s: 50
verified: true
draft: false
---

[CF 105689F - Lantern Hopping](https://codeforces.com/problemset/problem/105689/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 50s  
**Verified:** yes  

## Solution
## Problem Understanding

The festival contains a line of lanterns, and each lantern has a current height. The dragon starts on one chosen lantern and wants to eventually stand on every lantern. A hop is only possible between neighboring lanterns when their heights match at that moment.

The dragon can exchange height for energy at the lantern he is currently standing on. Lowering a lantern by one gives one energy, while increasing a lantern by one costs one energy. The task is to answer many queries: for a starting position, what is the smallest amount of initial energy needed, and after some queries the height of a lantern may change.

The input describes the number of lanterns and operations, followed by the initial heights. An update changes one lantern's height. A question asks for the minimum starting energy from a given lantern index.

The limits are large, with up to $2 \cdot 10^5$ lanterns and $2 \cdot 10^5$ operations. This rules out scanning all lanterns for every question because that would require around $4 \cdot 10^{10}$ operations in the worst case. We need a structure where updates and queries both take logarithmic or constant time.

The tricky part is realizing that the dragon cannot create free energy by repeatedly lowering and raising the same lantern. Lowering a lantern creates energy, but then returning that lantern to the height needed for the next hop consumes exactly the same amount. The only thing that matters is the relative heights of the lanterns visited.

A common mistake is to only consider the next lantern in one direction. The dragon may need to visit a very tall lantern on the opposite side, so every starting position must consider the tallest lantern in the entire row.

For example, with input:

```
3 1
5 1 2
1 2
```

the answer is:

```
0
```

Starting from the first lantern already has the maximum height, so no initial energy is needed.

Another edge case is when the starting lantern is not the tallest:

```
3 1
5 1 2
1 2
```

If the query were for lantern 2, the answer would be:

```
4
```

A solution that only checks adjacent lanterns could miss the height 5 at the other end and return a smaller value.

## Approaches

A direct approach would simulate the dragon's movement. Starting from the chosen lantern, we could try to move left and right, keeping track of the energy required at every hop. This works because the movement rule can be simulated exactly. However, for one query it may require looking at all $n$ lanterns. With $q$ queries, the worst case becomes $O(nq)$, which is far beyond the allowed range.

The key observation comes from looking at the energy change during a hop. Suppose the dragon moves from a lantern of height $x$ to a neighboring lantern of height $y$. If $y$ is higher, the dragon spends $y-x$ energy. If $y$ is lower, the dragon gains $x-y$ energy. In both cases, the energy changes by exactly:

$$x-y$$

After a sequence of hops, all intermediate heights cancel. Starting from lantern $p$ and reaching a lantern with height $h$, the energy becomes:

$$E + a_p - h$$

The lowest energy happens when the dragon reaches the highest lantern it ever visits. Since the goal is to visit every lantern, the highest lantern is simply the maximum height in the entire array.

Therefore, the required initial energy from position $p$ is:

$$\max(0, \text{maximum height} - a_p)$$

The only dynamic information we need is the current maximum height. Updates can change that maximum, so we maintain the multiset of heights and retrieve the largest value after every operation.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n) per query, O(nq) total | O(1) | Too slow |
| Optimal | O(log n) per update, O(1) per query | O(n) | Accepted |

## Algorithm Walkthrough

1. Store every lantern height in a data structure that can insert, delete, and retrieve the maximum value. A max heap with lazy deletion is enough for this problem.
2. For an update operation, replace the old height with the new one. The old value cannot be removed directly from a heap, so store the current height of every lantern separately and ignore outdated heap entries when checking the maximum.
3. For a question at lantern $p$, remove outdated heap entries first, then take the current maximum height. The answer is the difference between this maximum and the starting lantern's height if the difference is positive, otherwise it is zero.
4. Output the computed value.

Why it works: during any hop, the dragon's energy changes by the difference between the current lantern's height and the next lantern's height. Over a complete route, all visited intermediate heights cancel out. The only dangerous point is visiting the tallest lantern, because that is where the dragon has spent the most energy compared with the starting height. Having enough energy to reach that height means every other lantern can also be visited. The formula exactly measures the missing energy needed to make the starting lantern as high as the tallest lantern.

## Python Solution

```python
import sys
import heapq

input = sys.stdin.readline

def solve():
    n, q = map(int, input().split())
    a = list(map(int, input().split()))

    heap = []
    for i, x in enumerate(a):
        heapq.heappush(heap, (-x, i))

    out = []

    for _ in range(q):
        query = input().split()
        if query[0] == '1':
            p = int(query[1]) - 1
            while -heap[0][0] != a[heap[0][1]]:
                heapq.heappop(heap)
            out.append(str(max(0, -heap[0][0] - a[p])))
        else:
            p = int(query[1]) - 1
            x = int(query[2])
            a[p] = x
            heapq.heappush(heap, (-x, p))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The array `a` stores the current height of each lantern. It is needed because heap entries can become stale after updates.

The heap stores negative heights because Python's heap is a min heap. The largest height is therefore at the top as the smallest negative number.

Before answering a query, the code removes heap entries that no longer match the current height in `a`. This lazy deletion avoids the need for a more complicated data structure while keeping all operations fast.

The query answer uses the derived formula directly. The `max` call handles the case where the starting lantern already has the global maximum height, because the dragon does not need any initial energy.

## Worked Examples

### Sample 1

Input:

```
3 2
3 1 3
1 1
1 2
```

| Operation | Starting height | Maximum height | Answer |
| --- | --- | --- | --- |
| Query 1 | 3 | 3 | 0 |
| Query 2 | 1 | 3 | 2 |

The first lantern is already at the highest height, so the dragon can absorb energy from lower lanterns and move without any initial energy. The second lantern requires enough energy to reach height 3.

### Sample 2

Input:

```
2 5
1000000000 0
1 2
2 2 10
1 2
2 1 10
1 2
```

| Operation | Heights | Maximum height | Query answer |
| --- | --- | --- | --- |
| Query lantern 2 | [1000000000, 0] | 1000000000 | 1000000000 |
| Update lantern 2 | [1000000000, 10] | 1000000000 |  |
| Query lantern 2 | [1000000000, 10] | 1000000000 | 999999990 |
| Update lantern 1 | [10, 10] | 10 |  |
| Query lantern 2 | [10, 10] | 10 | 0 |

The trace shows that only the current maximum height matters. Changes to other lanterns matter only when they change the maximum.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(log n) per update, O(1) amortized per query | Each update inserts one heap entry, and stale entries are removed at most once |
| Space | O(n + q) | The heap may contain old entries from updates |

The constraints allow $2 \cdot 10^5$ operations, so a logarithmic update structure is required. The heap solution stays within the limits because each heap element is pushed once and removed once.

## Test Cases

```python
import sys
import io
import heapq

def solve(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    n, q = map(int, input().split())
    a = list(map(int, input().split()))

    heap = []
    for i, x in enumerate(a):
        heapq.heappush(heap, (-x, i))

    ans = []

    for _ in range(q):
        query = input().split()
        if query[0] == "1":
            p = int(query[1]) - 1
            while -heap[0][0] != a[heap[0][1]]:
                heapq.heappop(heap)
            ans.append(str(max(0, -heap[0][0] - a[p])))
        else:
            p = int(query[1]) - 1
            x = int(query[2])
            a[p] = x
            heapq.heappush(heap, (-x, p))

    return "\n".join(ans)

assert solve("""3 2
3 1 3
1 1
1 2
""") == """0
2""", "sample 1"

assert solve("""2 5
1000000000 0
1 2
2 2 10
1 2
2 1 10
1 2
""") == """1000000000
999999990
0""", "sample 2"

assert solve("""1 3
7
1 1
2 1 0
1 1
""") == """0
0""", "single lantern"

assert solve("""4 3
1 1 1 1
1 3
2 4 100
1 1
""") == """0
99""", "new maximum after update"

assert solve("""5 4
0 5 2 9 1
1 1
1 4
2 2 20
1 3
""") == """9
0
18""", "maximum movement and update"

assert solve("""3 2
5 5 5
1 2
1 3
""") == """0
0""", "all equal values"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single lantern | `0` | Minimum size case where no movement is needed |
| Updating to a new maximum | `0`, `99` | Correct handling of maximum changes |
| Mixed heights | `9`, `0`, `18` | Queries from low and high lanterns after updates |
| All equal values | `0`, `0` | The zero-energy case |

## Edge Cases

When there is only one lantern, the dragon has already visited every lantern. For input:

```
1 1
7
1 1
```

the maximum height and starting height are both 7, so the answer is:

```
0
```

The algorithm handles this because the required energy is the positive difference between the maximum and the starting height.

When the starting lantern is already the tallest, no initial energy is needed. For:

```
3 1
5 2 4
1 1
```

the maximum height is 5 and the starting height is also 5. The answer is:

```
0
```

The dragon can gain or spend energy while adjusting other lanterns.

When a height update removes the previous maximum, stale heap values must not affect answers. For:

```
2 3
100 0
2 1 10
1 2
1 1
```

after the update the heights are `[10, 0]`. The old value `100` remains inside the heap temporarily, but the lazy deletion step removes it before answering. The answers are:

```
10
0
```

because the current maximum is 10, not the outdated value 100.

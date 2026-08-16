---
title: "CF 102700I - Incredible photography"
description: "We have a line of (n) buildings, where building (i) has height (hi). Paula may start at any building and repeatedly move to a building that is strictly taller than her current building and visible from it."
date: "2026-08-16T17:54:24+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102700
codeforces_index: "I"
codeforces_contest_name: "2020 ICPC Universidad Nacional de Colombia Programming Contest"
rating: 0
weight: 102700
solve_time_s: 153
verified: true
draft: false
---

[CF 102700I - Incredible photography](https://codeforces.com/problemset/problem/102700/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 33s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a line of (n) buildings, where building (i) has height (h_i). Paula may start at any building and repeatedly move to a building that is strictly taller than her current building and visible from it. If she moves from (i) to (j), the distance added to her walk is (|i-j|).

Building (j) is visible from (i) when every building strictly between them has height at most (h_j). A building of the same height as (j) does not block the view, because only a strictly higher building blocks it.

For every starting building (i), we need the maximum total distance over any valid sequence of moves. Since every move goes to a strictly taller building, a valid route can never return to a previous height, so the movement graph is acyclic.

The important constraint is (n\le 10^5). An (O(n^2)) algorithm already performs around (5\cdot10^9) pair checks in the worst case, which is far beyond what a one-second limit can handle. We need an (O(n\log n)) solution, or better. The heights can be as large as (10^9), but they only participate in comparisons, so their magnitude does not affect the data structure.

There are several boundary cases where an implementation can silently go wrong. With a single building, for example, `1 / 15` has answer `0`, because there is nowhere to move. An implementation that assumes every building has a left or right candidate can access an invalid index.

Equal heights require more care. For `3 / 1 3 3`, the answer is `2 0 0`. The first building can see both buildings of height (3), including the farther one, because the nearer height-(3) building is not strictly higher than the farther one and therefore does not block it. An approach based only on the nearest strictly higher building would incorrectly consider only the first (3).

The two directions must also be handled independently. For `3 / 5 4 3`, the correct answer is `0 1 2`. Building (2) can move left to building (1), for distance (2), while there is no valid move to the right. An implementation that only searches to the right misses all of these routes.

## Approaches

A direct dynamic programming solution would consider every possible next building. For a fixed building (i), scan to the right while maintaining the maximum height encountered, and do the same to the left. Whenever a taller building (j) is visible, it gives a transition

[
dp[i] = \max(dp[i], |i-j|+dp[j]).
]

The buildings can be processed in decreasing height, so (dp[j]) is already known whenever (j) is taller than (i). This brute force is correct because it explicitly considers every legal first move.

The problem is the number of candidates. Consider strictly increasing heights. From every building, every building to its right is visible. The algorithm has to examine

[
\frac{n(n-1)}2
]

candidate pairs, which is (4,999,950,000) pairs when (n=100000). A direct visibility check for every pair can be even worse, reaching (O(n^3)) if the buildings between the pair are scanned each time.

The useful observation is that we can reverse the transition. Fix a taller building (j), and ask which lower buildings can see it.

Let (L_j) be the nearest building strictly taller than (j) on its left. Then every building (i) satisfying

[
L_j < i < j
]

and (h_i<h_j) can see (j). There cannot be a building taller than (h_j) between (i) and (j), because (L_j) is the nearest such building. Conversely, if (i\le L_j), building (L_j) blocks the view of (j).

The same argument applies on the right. If (R_j) is the nearest strictly taller building on the right, then every lower building (i) with

[
j<i<R_j
]

can see (j).

This converts one building (j) into two range updates. For a lower building (i<j), the transition through (j) has value

[
dp[j]+j-i=(dp[j]+j)-i.
]

The expression has the form constant minus (i), so we can store the constant (dp[j]+j) on an interval. For a lower building (i>j), the transition is

[
dp[j]+i-j=(dp[j]-j)+i,
]

so we store (dp[j]-j) on another interval.

A range maximum update followed by point queries is enough. We process buildings by decreasing height. All buildings of the same height are queried before any of them updates the data structures. This detail handles equal heights correctly, because Paula is not allowed to move between equal-height buildings.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(n^2)) | (O(n)) | Too slow |
| Optimal | (O(n\log n)) | (O(n)) | Accepted |

## Algorithm Walkthrough

1. Compute (L_i), the nearest index to the left whose height is strictly greater than (h_i). A decreasing monotonic stack finds all these positions in (O(n)). While the top of the stack has height at most (h_i), remove it, because it cannot be the nearest strictly greater building for (i).
2. Compute (R_i), the nearest index to the right whose height is strictly greater than (h_i), using the same monotonic-stack idea while scanning from right to left. If no such building exists, use (n) as a sentinel.
3. Sort the building indices by height in decreasing order. Buildings with equal height are kept in the same group. We need this grouping because a building of height (H) may move only to height strictly greater than (H), never to another building of height (H).
4. Maintain one range-chmax structure for moves from the right and another for moves from the left. The first structure stores values (dp[j]+j), and the second stores values (dp[j]-j). A point query at (i) gives the best stored constant applicable to (i).
5. For every building (i) in the current height group, query both structures before applying any updates from this group. If the left-looking structure returns (A), the corresponding route has value (A-i). If the right-looking structure returns (B), the corresponding route has value (B+i). Set (dp[i]) to the maximum of these values and zero.
6. After all buildings in the current height group have their (dp) values, update the structures for each building (j). The left interval is ([L_j+1,j)), because those are the positions to the left that can see (j). Store (dp[j]+j) there. The right interval is ([j+1,R_j)), and we store (dp[j]-j) there.
7. After all height groups have been processed, print the resulting (dp) array. Every transition used to calculate a value came from a strictly taller building whose answer was already finalized.

### Why it works

Consider any legal transition from a lower building (i) to a taller building (j) with (i<j). The transition is valid exactly when no building strictly taller than (h_j) lies between them. By definition, (L_j) is the nearest such building on the left, so this condition is equivalent to (L_j<i<j). Thus the update generated by (j) covers exactly the valid lower buildings on its left. The right side is symmetric.

For every such transition, the data structure stores (dp[j]+j), so a query at (i) reconstructs (dp[j]+j-i), exactly the distance (j-i) plus the best route starting at (j). Since all updates from taller height groups have already been applied, every possible first move is represented when (dp[i]) is computed. Equal-height buildings are not allowed as moves, and delaying all updates from an equal-height group prevents them from affecting one another. Hence the maximum produced for each building is exactly the maximum legal walking distance.

## Python Solution

```python
import sys
input = sys.stdin.readline

NEG = -10**30

class RangeChmaxPointQuery:
    def __init__(self, n):
        size = 1
        while size < n:
            size <<= 1
        self.size = size
        self.tree = [NEG] * (2 * size)

    def update(self, left, right, value):
        if left >= right:
            return

        size = self.size
        tree = self.tree

        left += size
        right += size

        while left < right:
            if left & 1:
                if value > tree[left]:
                    tree[left] = value
                left += 1

            if right & 1:
                right -= 1
                if value > tree[right]:
                    tree[right] = value

            left >>= 1
            right >>= 1

    def query(self, pos):
        tree = self.tree
        pos += self.size
        result = NEG

        while pos:
            if tree[pos] > result:
                result = tree[pos]
            pos >>= 1

        return result

def solve():
    n = int(input())
    h = list(map(int, input().split()))

    left_greater = [-1] * n
    right_greater = [n] * n

    stack = []

    for i in range(n):
        while stack and h[stack[-1]] <= h[i]:
            stack.pop()

        if stack:
            left_greater[i] = stack[-1]

        stack.append(i)

    stack = []

    for i in range(n - 1, -1, -1):
        while stack and h[stack[-1]] <= h[i]:
            stack.pop()

        if stack:
            right_greater[i] = stack[-1]

        stack.append(i)

    order = sorted(range(n), key=h.__getitem__, reverse=True)

    left_tree = RangeChmaxPointQuery(n)
    right_tree = RangeChmaxPointQuery(n)

    dp = [0] * n

    p = 0
    while p < n:
        q = p + 1
        height = h[order[p]]

        while q < n and h[order[q]] == height:
            q += 1

        for k in range(p, q):
            i = order[k]

            best = 0

            a = left_tree.query(i)
            if a != NEG:
                candidate = a - i
                if candidate > best:
                    best = candidate

            b = right_tree.query(i)
            if b != NEG:
                candidate = b + i
                if candidate > best:
                    best = candidate

            dp[i] = best

        for k in range(p, q):
            j = order[k]

            left_tree.update(
                left_greater[j] + 1,
                j,
                dp[j] + j
            )

            right_tree.update(
                j + 1,
                right_greater[j],
                dp[j] - j
            )

        p = q

    print(*dp)

if __name__ == "__main__":
    solve()
```

The first monotonic-stack pass computes the nearest strictly higher building on the left. The `<=` comparison is deliberate. An equal-height building does not count as strictly higher, so it must be removed from the stack before the nearest valid blocker is selected.

The second pass does the symmetric calculation for the right boundary. Using `n` as the missing right boundary makes the later range update naturally become `[j+1,n)` without special handling.

The `RangeChmaxPointQuery` structure uses an iterative segment tree. It does not need lazy propagation in the usual sense because updates are only range maximum assignments and queries are only points. A range is decomposed into (O(\log n)) canonical tree nodes, and a point query takes the maximum over the (O(\log n)) nodes on its root path.

The two trees represent the two signs of the distance. For a destination (j) to the right of (i), the expression is `dp[j] + j - i`, so the stored value is `dp[j] + j`. For a destination (j) to the left, it is `dp[j] - j + i`, so the stored value is `dp[j] - j`.

The order of querying and updating within an equal-height group is essential. If a height-(H) building updated the structure before another height-(H) building was processed, the second building could incorrectly use the first one as a destination. Processing the entire group first prevents that.

Python integers have arbitrary precision, so the potentially large accumulated walking distance does not overflow. In a fixed-width language, a 64-bit integer type should be used.

## Worked Examples

### Sample 1

For the input

```
4
3 1 2 4
```

the nearest strictly greater boundaries are

[
L=[-1,0,0,0]
]

and

[
R=[3,2,3,4].
]

The following table shows the important state while processing height groups. The `left query` represents a stored (dp[j]+j), while the `right query` represents a stored (dp[j]-j).

| Height group | Building | Left query | Right query | (dp) |
| --- | --- | --- | --- | --- |
| 4 | 3 | none | none | 0 |
| 3 | 0 | none | 3 | 3 |
| 2 | 2 | 3 | 3 | 5 |
| 1 | 1 | 7 | 3 | 6 |

After processing building (3) of height (4), its left update stores (dp[3]+3=3) on positions (0,1,2). Thus building (0) can already obtain distance (3).

When building (0) is processed, its answer becomes (3). Its right update stores (dp[0]-0=3) on positions (1,2). At building (2), this gives (3+2=5), corresponding to the route (2\to0\to3).

Finally, building (2) contributes (dp[2]+2=7) to its left interval, so building (1) obtains (7-1=6). The resulting output is `3 6 5 0`.

### Sample 2

For the input

```
5
3 3 1 5 5
```

the nearest strictly greater boundaries are

[
L=[-1,-1,1,-1,-1]
]

and

[
R=[3,3,3,5,5].
]

The two buildings of height (5) must be processed together. Their updates happen only after both have obtained (dp=0).

| Height group | Building | Left query | Right query | (dp) |
| --- | --- | --- | --- | --- |
| 5 | 3 | none | none | 0 |
| 5 | 4 | none | none | 0 |
| 3 | 0 | 4 | none | 4 |
| 3 | 1 | 4 | none | 3 |
| 1 | 2 | 4 | 4 | 6 |

Building (4) of height (5) updates every lower building to its left with the value (dp[4]+4=4). This is why building (1), for example, can directly see the farther height-(5) building and obtain distance (3), even though another height-(5) building lies between them.

After buildings (0) and (1) are processed, their right-side updates make the best route for building (2) equal to (6). One optimal route is (2\to0\to4), with distances (2) and (4).

The final output is `4 3 6 0 0`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(n\log n)) | Sorting takes (O(n\log n)), while every building performs a constant number of (O(\log n)) segment-tree operations. |
| Space | (O(n)) | The height array, boundary arrays, DP array, stacks, and two segment trees all use linear space. |

With (n\le10^5), the solution performs only a logarithmic number of operations per building after the sorting step. This is comfortably within the intended asymptotic bound, while the linear memory usage is far below the 512 MB limit.

## Test Cases

```python
import sys
import io

NEG = -10**30

class RangeChmaxPointQuery:
    def __init__(self, n):
        size = 1
        while size < n:
            size <<= 1
        self.size = size
        self.tree = [NEG] * (2 * size)

    def update(self, left, right, value):
        if left >= right:
            return

        left += self.size
        right += self.size

        while left < right:
            if left & 1:
                self.tree[left] = max(self.tree[left], value)
                left += 1

            if right & 1:
                right -= 1
                self.tree[right] = max(self.tree[right], value)

            left >>= 1
            right >>= 1

    def query(self, pos):
        pos += self.size
        result = NEG

        while pos:
            result = max(result, self.tree[pos])
            pos >>= 1

        return result

def solve_data(data: str) -> str:
    tokens = list(map(int, data.split()))
    n = tokens[0]
    h = tokens[1:n + 1]

    left_greater = [-1] * n
    right_greater = [n] * n

    stack = []

    for i in range(n):
        while stack and h[stack[-1]] <= h[i]:
            stack.pop()

        if stack:
            left_greater[i] = stack[-1]

        stack.append(i)

    stack = []

    for i in range(n - 1, -1, -1):
        while stack and h[stack[-1]] <= h[i]:
            stack.pop()

        if stack:
            right_greater[i] = stack[-1]

        stack.append(i)

    order = sorted(range(n), key=h.__getitem__, reverse=True)

    left_tree = RangeChmaxPointQuery(n)
    right_tree = RangeChmaxPointQuery(n)
    dp = [0] * n

    p = 0
    while p < n:
        q = p + 1

        while q < n and h[order[q]] == h[order[p]]:
            q += 1

        for k in range(p, q):
            i = order[k]
            best = 0

            a = left_tree.query(i)
            if a != NEG:
                best = max(best, a - i)

            b = right_tree.query(i)
            if b != NEG:
                best = max(best, b + i)

            dp[i] = best

        for k in range(p, q):
            j = order[k]

            left_tree.update(
                left_greater[j] + 1,
                j,
                dp[j] + j
            )

            right_tree.update(
                j + 1,
                right_greater[j],
                dp[j] - j
            )

        p = q

    return " ".join(map(str, dp))

def run(inp: str) -> str:
    return solve_data(inp).strip()

# Provided samples
assert run("4\n3 1 2 4\n") == "3 6 5 0", "sample 1"
assert run("1\n15\n") == "0", "sample 2"
assert run("5\n3 3 1 5 5\n") == "4 3 6 0 0", "sample 3"

# Minimum-size input
assert run("1\n7\n") == "0", "single building"

# Maximum-size input with all heights equal
n = 100000
inp = f"{n}\n" + " ".join(["42"] * n) + "\n"
expected = " ".join(["0"] * n)
assert run(inp) == expected, "maximum size and all equal"

# Boundary condition: every useful move is to the left
assert run("5\n5 4 3 2 1\n") == "0 1 2 3 4", "decreasing heights"

# Equal-height visibility and off-by-one boundary
assert run("3\n1 3 3\n") == "2 0 0", "equal-height farther building"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 7` | `0` | Minimum size and no valid transition |
| `100000 / 42 42 ... 42` | `0 0 ... 0` | Maximum size and equal-height batching |
| `5 / 5 4 3 2 1` | `0 1 2 3 4` | Left-side transitions and boundary at the first building |
| `3 / 1 3 3` | `2 0 0` | Equal heights remain visible and the farther equal maximum is not incorrectly blocked |

## Edge Cases

For a single building, the input `1 / 7` gives `0`. Both nearest-greater arrays contain only boundaries, so neither segment tree receives an update that can reach the building. Its DP value remains zero, exactly as required.

For equal heights, consider `3 / 1 3 3`. Both height-(3) buildings are processed together and receive `dp=0`. After that group is finished, the farther building at index (2) updates the lower building at index (0), storing (0+2=2). Building (0) consequently gets answer (2). The equal-height buildings never update each other because their updates are delayed until their entire group has been evaluated.

For a sequence whose useful moves all go left, `5 / 5 4 3 2 1`, the nearest strictly greater building for every position except the first lies to the left. Processing the tallest building first gives it answer zero, then each lower building receives the distance to the tallest building plus its already computed continuation. The answers become `0 1 2 3 4`.

The interval boundaries also matter when there is no strictly greater building on one side. For a building with no greater blocker on the left, `left_greater` is `-1`, so its update begins at position zero. When there is no greater blocker on the right, `right_greater` is `n`, so its update extends through the last position. Using inclusive endpoints here would incorrectly allow the destination building itself to receive its own update, which is why the implementation consistently uses half-open intervals `[left, right)`.

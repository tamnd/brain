---
title: "CF 102452H - Hold the Line"
description: "We have an array of (N) trenches. A trench is initially empty, and each trench can receive a soldier at most once. When a soldier is placed at position (x), that position permanently gets a height (h). A query gives a position interval ([L,R]) and an enemy height (H)."
date: "2026-08-10T06:22:48+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102452
codeforces_index: "H"
codeforces_contest_name: "2019-2020 ICPC Asia Hong Kong Regional Contest"
rating: 0
weight: 102452
solve_time_s: 388
verified: true
draft: false
---

[CF 102452H - Hold the Line](https://codeforces.com/problemset/problem/102452/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 6m 28s  
**Verified:** yes  

## Solution
## Problem Understanding

We have an array of (N) trenches. A trench is initially empty, and each trench can receive a soldier at most once. When a soldier is placed at position (x), that position permanently gets a height (h).

A query gives a position interval ([L,R]) and an enemy height (H). Among all soldiers currently present in that interval, we need the minimum value of (|h-H|). If the interval contains no currently usable soldier, the answer is (-1).

There are two different orders hidden in the problem. Position determines whether a soldier belongs to the requested interval, while event index determines whether the soldier has already been placed when the query occurs. A solution has to respect both conditions simultaneously.

The constraints make a direct scan impossible. There can be (5\cdot10^5) trenches and (10^6) events in total. In the worst case, about (5\cdot10^5) events can be queries after all (5\cdot10^5) trenches have received soldiers, so scanning the interval for every query can perform about (2.5\cdot10^{11}) position checks. Even an ordinary segment tree whose nodes contain balanced ordered sets gives (O((N+M)\log^2N)), but the official editorial specifically points out that this straightforward solution has too much constant overhead for the tight limits.

The current Codeforces problem page gives a 4.5 second time limit and 512 MB memory limit. This makes both the asymptotic complexity and the representation of the data structure relevant. The implementation below uses compact integer arrays for the large monotonic queues instead of millions of Python objects.

Several boundary cases are easy to mishandle. First, a query can occur before every soldier in its range is inserted.

```
1
1 1
1 1 1 5
```

The answer is

```
-1
```

There is no soldier yet. An offline algorithm that inserts every final soldier without checking its insertion time would incorrectly return a value.

A second issue is that a soldier can be inserted at the right endpoint only after an earlier query.

```
1
2 3
1 1 2 5
0 2 5
1 1 2 5
```

The output is

```
-1
0
```

The first query must not see the later insertion. The second query can see it.

A third boundary case is a single-position interval. The position test must be inclusive on both ends.

```
1
3 5
0 1 100
0 3 1
1 1 1 50
1 2 2 50
1 3 3 50
```

The output is

```
50
-1
49
```

The middle query examines only position 2, which is empty. A range implementation that accidentally treats ([L,R)) instead of ([L,R]) can silently fail on such cases.

Finally, equal heights must be handled normally. If several soldiers have height 7 and the enemy has height 7, the answer is exactly 0, not the distance to some other distinct height.

## Approaches

The brute-force solution keeps the current height at every trench. For a query ([L,R,H]), it scans every position from (L) through (R), ignores empty positions, and keeps the smallest absolute difference from (H). This is correct because every eligible soldier is examined and the minimum over all of them is exactly the required answer.

The problem is the number of scans. A query covering the entire array costs (O(N)), and there can be (O(M)) such queries. Under the given aggregate limits this reaches roughly (2.5\cdot10^{11}) position checks, far beyond what the time limit permits.

A natural improvement is a segment tree over positions, with an ordered set of heights in every node. A range query decomposes ([L,R]) into (O(\log N)) nodes, and each node can find the predecessor and successor of (H) in (O(\log N)). This gives (O((N+M)\log^2N)), but maintaining a separate balanced tree in every segment node is expensive in both memory and constant factors. The official editorial describes this straightforward approach and then replaces it with an offline structure.

The key observation is that queries can be processed in increasing order of their right endpoint (R). Suppose we are currently processing all queries whose right endpoint is (R). We can insert every soldier at position at most (R) into a data structure. This completely removes the right boundary from the query.

The remaining validity conditions for a soldier at position (j) are then

[
j\ge L
]

and

[
v_j < i,
]

where (v_j) is the event index at which the soldier was inserted and (i) is the event index of the current query. The first condition is positional, while the second is temporal.

Now build a segment tree over height values instead of positions. A node represents an interval of heights and stores the insertion events belonging to that height interval.

There is a useful dominance rule inside one node. Positions are inserted in increasing order because the outer sweep processes (R=1,2,\ldots,N). Suppose two stored soldiers have positions (j<k), but their insertion times satisfy (v_j>v_k). Soldier (j) is never useful. Whenever soldier (j) is old enough to be available, soldier (k) is also available, and (k) is farther to the right. Thus, for every lower-bound condition (j\ge L), soldier (k) is at least as good as (j).

We can consequently remove such dominated elements from the back of every node's queue. The surviving event indices increase from front to back, and their positions also increase from front to back. This is the monotonic queue described by the official editorial.

That monotonicity makes the validity test surprisingly small. Given a query with event index (i) and left endpoint (L), binary-search the node's queue for the first event index at least (i). The previous element is the largest insertion event strictly smaller than (i). Because both event indices and positions increase together, this one element also has the largest position among all soldiers that were inserted before the query. If its position is at least (L), the node contains a valid soldier. If its position is smaller than (L), no earlier element can satisfy the position condition.

Once a node can be tested this way, the height search becomes ordinary segment-tree navigation. We search for the largest valid height at most (H), and independently for the smallest valid height at least (H). Those two candidates are sufficient because every value below (H) is farther away than the largest value below it, and every value above (H) is farther away than the smallest value above it.

The resulting complexity is (O(N\log N+M\log^2N)), matching the official approach.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(NM)) | (O(N)) | Too slow |
| Segment tree with ordered sets | (O((N+M)\log^2N)) | (O(N\log N)) | Too much overhead |
| Offline segment tree with monotonic queues | (O(N\log N+M\log^2N)) | (O(N\log N+M)) | Accepted |

## Algorithm Walkthrough

1. Read all events and remember every soldier insertion by its trench position. For every query, remember its left endpoint, enemy height, event index, and right endpoint. We group queries by (R), because the offline sweep will process positions from left to right.
2. Compress the heights of all soldiers. Only soldier heights need to be leaves of the segment tree. For a query height (H), `bisect_left` and `bisect_right` locate the closest compressed height ranges on either side.
3. Build a segment tree over the compressed soldier heights. A soldier with height rank (p) belongs to the leaf for (p) and every ancestor of that leaf. Each node therefore represents all soldiers whose heights lie in that node's value interval.
4. Before processing the sweep, calculate how many soldier entries each segment-tree node could ever need. Every soldier contributes one potential entry to every node on its root-to-leaf path. The implementation uses this count to allocate one compact global integer array, avoiding a separate Python list for every node.
5. Sweep the trench positions from (1) through (N). When reaching position (R), insert the soldier at (R), if one exists. Its event index is appended to every segment-tree node on its height path.
6. While appending an event index (i) to a node, remove entries from the back while their event index is larger than (i). The current position is larger than every position previously inserted into that node, so a removed entry has an earlier position but a later insertion time. It can never be the best witness for a future validity check.
7. Process all queries whose right endpoint is the current (R). For each query, search the height segment tree twice. The first search finds the largest height at most (H) whose node contains a valid soldier. The second finds the smallest height at least (H) whose node contains a valid soldier.
8. For each node visited by a height search, test whether it contains a soldier with position at least (L) and insertion event index smaller than the current query index. Binary search gives the last event index smaller than the query. Because the queue's positions increase with its event indices, checking that single soldier is enough.
9. Convert the two height candidates into absolute differences from (H). If neither side exists, return (-1). Otherwise return the smaller difference. An exact height produces difference 0 and naturally wins over every other candidate.

### Why it works

Consider any segment-tree node and its surviving queue. Its event indices are strictly increasing, and its positions are also strictly increasing. For a query at event (i), every queue entry with event index at least (i) is too late. Among the entries with event index smaller than (i), the last one has the greatest position. Thus the node contains a valid soldier exactly when that last earlier event has position at least (L).

The removal rule never deletes a potentially useful soldier. If an earlier-position soldier has a later insertion time than a later-position soldier, the later-position soldier becomes available no later and satisfies every left-bound condition that the earlier soldier could satisfy. The removed soldier is consequently dominated.

The outer sweep has already inserted every position at most (R), so every soldier considered by a node lies on the correct side of the right endpoint. The event-index test removes soldiers that occur after the current query. Together, these two conditions leave exactly the soldiers in ([L,R]) that were already present at query time.

Finally, among valid heights, the closest one to (H) must be either the greatest height not exceeding (H) or the smallest height not less than (H). The two segment-tree searches find precisely those candidates, so the minimum of their distances is the required answer.

## Python Solution

```python
import sys
from bisect import bisect_left, bisect_right
from array import array

def solve():
    input = sys.stdin.readline
    T = int(input())
    output = []

    for _ in range(T):
        N, M = map(int, input().split())

        # For every position, store its unique insertion event and height.
        update_id_at_pos = array('i', [0]) * (N + 1)
        update_height_at_pos = array('i', [0]) * (N + 1)

        # Queries are linked by their right endpoint.
        query_head = array('i', [-1]) * (N + 1)
        query_next = array('i', [-1]) * (M + 1)
        query_left = array('i', [0]) * (M + 1)
        query_height = array('i', [0]) * (M + 1)
        is_query = bytearray(M + 1)

        # Position of every update event, indexed by event id.
        update_pos = array('i', [0]) * (M + 1)

        update_heights = []

        for event_id in range(1, M + 1):
            parts = input().split()
            typ = int(parts[0])

            if typ == 0:
                x = int(parts[1])
                h = int(parts[2])

                update_id_at_pos[x] = event_id
                update_height_at_pos[x] = h
                update_pos[event_id] = x
                update_heights.append(h)
            else:
                L = int(parts[1])
                R = int(parts[2])
                H = int(parts[3])

                is_query[event_id] = 1
                query_left[event_id] = L
                query_height[event_id] = H

                query_next[event_id] = query_head[R]
                query_head[R] = event_id

        answer = array('i', [-1]) * (M + 1)

        if not update_heights:
            for event_id in range(1, M + 1):
                if is_query[event_id]:
                    output.append("-1\n")
            continue

        # Coordinate compression only needs actual soldier heights.
        values = sorted(set(update_heights))
        K = len(values)

        # Rank of the soldier height at every position.
        rank_at_pos = array('i', [0]) * (N + 1)

        # Use an iterative segment tree with K leaves.
        S = 1
        while S < K:
            S <<= 1

        node_count = 2 * S

        # cnt[node] is the maximum number of queue entries needed by
        # that node. Every update contributes once to every ancestor.
        cnt = array('i', [0]) * node_count

        for x in range(1, N + 1):
            event_id = update_id_at_pos[x]
            if event_id:
                rank = bisect_left(values, update_height_at_pos[x]) + 1
                rank_at_pos[x] = rank

                node = S + rank - 1
                while node:
                    cnt[node] += 1
                    node >>= 1

        # Give every node a fixed slice of one global queue array.
        base = array('i', [0]) * node_count
        tail = array('i', [0]) * node_count

        total = 0
        for node in range(1, node_count):
            base[node] = total
            tail[node] = total
            total += cnt[node]

        # Each entry is an event id, so 32 bits are enough.
        queue = array('i', [0]) * total

        def check(node, qid, left):
            """Does this node contain a valid soldier?"""
            b = base[node]
            t = tail[node]

            if b == t:
                return False

            # queue[b:t] contains strictly increasing event ids.
            p = bisect_left(queue, qid, b, t)

            if p == b:
                return False

            candidate = queue[p - 1]
            return update_pos[candidate] >= left

        def find_left(rank, qid, left):
            """Largest valid height rank <= rank, or 0."""
            if rank <= 0:
                return 0

            node = S + rank - 1

            if check(node, qid, left):
                return rank

            while node > 1:
                # node is a right child, so its left sibling is
                # completely inside the prefix we are searching.
                if node & 1:
                    sibling = node - 1

                    if check(sibling, qid, left):
                        node = sibling

                        # Find the rightmost valid leaf in this subtree.
                        while node < S:
                            right = node * 2 + 1
                            if check(right, qid, left):
                                node = right
                            else:
                                node *= 2

                        return node - S + 1

                node >>= 1

            return 0

        def find_right(rank, qid, left):
            """Smallest valid height rank >= rank, or 0."""
            if rank > K:
                return 0

            node = S + rank - 1

            if check(node, qid, left):
                return rank

            while node > 1:
                # node is a left child, so its right sibling is
                # completely inside the suffix we are searching.
                if (node & 1) == 0:
                    sibling = node + 1

                    if check(sibling, qid, left):
                        node = sibling

                        # Find the leftmost valid leaf in this subtree.
                        while node < S:
                            left_child = node * 2
                            if check(left_child, qid, left):
                                node = left_child
                            else:
                                node = left_child + 1

                        return node - S + 1

                node >>= 1

            return 0

        # Sweep the right endpoint.
        for R in range(1, N + 1):
            event_id = update_id_at_pos[R]

            if event_id:
                rank = rank_at_pos[R]
                node = S + rank - 1

                # Add the event to every node on the root-to-leaf path.
                # The queue is monotone in event id.
                while node:
                    t = tail[node]
                    b = base[node]

                    while t > b and queue[t - 1] > event_id:
                        t -= 1

                    queue[t] = event_id
                    tail[node] = t + 1
                    node >>= 1

            # All these queries have exactly this R as their right endpoint.
            qid = query_head[R]

            while qid != -1:
                L = query_left[qid]
                H = query_height[qid]

                # Greatest compressed value <= H.
                right_rank = bisect_right(values, H)

                # Smallest compressed value >= H.
                left_rank = bisect_left(values, H) + 1

                best = -1

                if right_rank:
                    rank = find_left(right_rank, qid, L)
                    if rank:
                        best = H - values[rank - 1]

                if left_rank <= K:
                    rank = find_right(left_rank, qid, L)
                    if rank:
                        diff = values[rank - 1] - H
                        if best == -1 or diff < best:
                            best = diff

                answer[qid] = best
                qid = query_next[qid]

        # Restore the original event order.
        for event_id in range(1, M + 1):
            if is_query[event_id]:
                output.append(str(answer[event_id]) + "\n")

    sys.stdout.write("".join(output))

if __name__ == "__main__":
    solve()
```

The first part of the implementation stores updates by position and queries by right endpoint. The linked-list representation for queries avoids creating a Python tuple for every event, which matters when (M) reaches (10^6).

Height compression is done only on heights that actually occur in soldiers. A query height does not need its own segment-tree leaf. `bisect_right(values, H)` gives the last soldier-height rank that can be a predecessor, while `bisect_left(values, H) + 1` gives the first possible successor rank.

The segment tree uses a power-of-two leaf base `S`. A compressed rank from 1 through (K) maps to leaf `S + rank - 1`. The tree contains empty leaves when (K) is not a power of two, but the search functions never return those leaves because `check` is false there.

The queue storage deserves special attention in Python. A normal list for every segment-tree node can consume hundreds of megabytes because the number of queue entries is (O(N\log N)). Instead, the code first counts the maximum capacity needed by every node, assigns each node a contiguous slice of one `array('i')`, and stores event indices in that global buffer. The total queue storage is still (O(N\log N)), but each event index occupies four bytes.

When a soldier is inserted, the code pops larger event indices from the tail before appending the new event. The position is already increasing because the outer loop visits positions in increasing order. This is exactly the dominance rule behind the monotonic queue.

The `check` function uses `bisect_left` on the node's event-id interval. If the insertion event immediately before the query is at position at least (L), the node is valid. If it is not, no earlier event can work because the queue positions increase together with event ids.

The predecessor and successor searches use the path from the relevant leaf toward the root. Whenever the current path comes from a right child, its left sibling is a completely explored candidate subtree for the predecessor search. The successor search is symmetric. After finding a feasible sibling, the code descends toward the rightmost or leftmost feasible leaf respectively.

The event ordering is also subtle. An update at position (R) is inserted before processing queries whose right endpoint is (R), even if that update happened later in event order. This is intentional. The monotonic queue's event-id test rejects it whenever its event id is not smaller than the query id. Thus the sweep handles the position condition, while the queue handles the time condition.

All heights and differences fit in signed 32-bit integers because heights are at most (10^9). Event indices also fit in signed 32-bit integers. Python itself has arbitrary-precision integers, but the compact arrays deliberately use 32-bit storage.

## Worked Examples

The official sample has one test case. The event sequence is:

```
1
3 5
1 1 3 2
0 1 1
0 3 3
1 1 2 2
1 2 3 2
```

The first query occurs before either soldier is inserted. The later offline sweep does eventually insert both soldiers, but their event indices are larger than the first query's event index, so neither can pass `check`.

| Event | Action | Current R | Inserted soldiers | Query candidate heights | Answer |
| --- | --- | --- | --- | --- | --- |
| 1 | Query ([1,3],H=2) | 3 | none are valid by time | none | -1 |
| 2 | Insert position 1, height 1 | 1 | (1\mapsto1) |  |  |
| 3 | Insert position 3, height 3 | 3 | (1\mapsto1,\ 3\mapsto3) |  |  |
| 4 | Query ([1,2],H=2) | 2 | position 1 is valid | 1 | 1 |
| 5 | Query ([2,3],H=2) | 3 | position 3 is valid | 3 | 1 |

The output is

```
-1
1
1
```

The interesting part is that the first query is processed during the (R=3) sweep after both positions have been inserted. The event-id condition still rejects both soldiers. This is the central invariant of the offline transformation.

For a second example, consider:

```
1
5 8
1 1 5 10
0 2 7
0 5 13
1 2 5 10
0 1 10
1 1 2 10
1 3 4 10
0 4 9
```

The outputs are:

```
-1
3
0
-1
```

The first query occurs before any insertion. At the fourth event, positions 2 and 5 have been inserted, with heights 7 and 13. For enemy height 10, both are distance 3. The data structure may choose either one because only the difference is requested.

At event 6, position 1 has height 10 and was inserted earlier, so the exact match produces 0. At event 7, the requested interval is ([3,4]), but position 4 has not been inserted yet, while position 3 is empty, so the answer is (-1).

| Event | Action | Current R | Valid soldiers in queried range | Closest height | Answer |
| --- | --- | --- | --- | --- | --- |
| 1 | Query ([1,5],H=10) | 5 | none before event 1 | none | -1 |
| 2 | Insert position 2, height 7 | 2 |  |  |  |
| 3 | Insert position 5, height 13 | 5 |  |  |  |
| 4 | Query ([2,5],H=10) | 5 | (2\mapsto7,\ 5\mapsto13) | 7 or 13 | 3 |
| 5 | Insert position 1, height 10 | 1 |  |  |  |
| 6 | Query ([1,2],H=10) | 2 | (1\mapsto10,\ 2\mapsto7) | 10 | 0 |
| 7 | Query ([3,4],H=10) | 4 | none valid | none | -1 |
| 8 | Insert position 4, height 9 | 4 |  |  |  |

This example exercises both boundaries of the height search and the distinction between position order and event order.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(N\log N+M\log^2N)) | Each update touches (O(\log N)) tree nodes. Each query performs two height searches, each visiting (O(\log N)) nodes, with a binary search inside each node queue. |
| Space | (O(N\log N+M+N)) | The monotonic queues contain at most one potential slot per update per tree level, while event and query metadata use (O(M+N)) space. |

The aggregate constraint (\sum N\le5\cdot10^5) keeps the total queue capacity within (O(5\cdot10^5\log5\cdot10^5)), about ten million integer slots. The implementation stores those slots as four-byte integers, which is substantially more suitable for Python than a list of Python integer objects. The official editorial gives the same (O(n\log n+m\log^2n)) bound for the monotonic-queue approach.

The (M\le10^6) bound also explains why the code avoids object-heavy event tuples and processes queries through compact arrays and linked lists. The algorithm is designed around the fact that each trench receives at most one soldier, so there are at most (N) updates even though there can be many more queries.

## Test Cases

The following harness assumes the solution above is saved in the same file and that its entry point is the `solve()` function. It replaces standard input and output so the assertions exercise the actual implementation rather than a separate reference algorithm.

```python
# helper: run the solution on one input string
import sys
import io

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    try:
        solve()
        return sys.stdout.getvalue()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

# Official sample
assert run(
    """1
3 5
1 1 3 2
0 1 1
0 3 3
1 1 2 2
1 2 3 2
"""
) == "-1\n1\n1\n", "official sample"

# Minimum-size case
assert run(
    """1
1 3
1 1 1 7
0 1 7
1 1 1 7
"""
) == "-1\n0\n", "minimum size and future update"

# Boundary and singleton intervals
assert run(
    """1
3 5
0 1 100
0 3 1
1 1 1 50
1 2 2 50
1 3 3 50
"""
) == "50\n-1\n49\n", "singleton ranges"

# Equal heights and exact matches
assert run(
    """1
4 6
0 1 7
0 2 7
0 3 7
1 1 3 9
1 2 2 7
1 4 4 7
"""
) == "2\n0\n-1\n", "equal values"

# Queries before and after insertions, including a later right endpoint
assert run(
    """1
5 8
1 1 5 10
0 2 7
0 5 13
1 2 5 10
0 1 10
1 1 2 10
1 3 4 10
0 4 9
"""
) == "-1\n3\n0\n-1\n", "time and position boundaries"

# Maximum M stress shape: N = 1, M = 1,000,000.
# Only the first event inserts the soldier; every later query must answer 0.
M = 1_000_000
lines = ["1", f"1 {M}", "0 1 123456789"]
lines.extend("1 1 1 123456789" for _ in range(M - 1))
max_m_input = "\n".join(lines) + "\n"

expected = "0\n" * (M - 1)
assert run(max_m_input) == expected, "maximum M"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Official sample | `-1, 1, 1` | Future insertions and ordinary predecessor/successor searches |
| (N=1) minimum case | `-1, 0` | Empty query followed by an exact match |
| Singleton intervals | `50, -1, 49` | Inclusive (L,R) boundaries and empty positions |
| Equal heights | `2, 0, -1` | Duplicate heights and exact matches |
| Time and position boundaries | `-1, 3, 0, -1` | Event order versus position order |
| (M=10^6), (N=1) | (999999) zeroes | Maximum event count and repeated queries |

## Edge Cases

### Query before any insertion

For

```
1
1 1
1 1 1 5
```

the query is event 1. There is no soldier, so the answer is (-1). The height tree is empty, and the implementation directly outputs (-1) when there are no updates.

### Future insertion

For

```
1
2 3
1 1 2 5
0 2 5
1 1 2 5
```

the sweep reaches (R=2) and inserts the soldier from event 2 before processing the query from event 3. For event 1, the same soldier is also physically present in the offline structure, but its event index is 2, which fails the strict test `candidate < qid`. Thus event 1 returns (-1). Event 3 sees the soldier and returns 0.

### Singleton interval

For

```
1
3 5
0 1 100
0 3 1
1 1 1 50
1 2 2 50
1 3 3 50
```

the first query sees only position 1 and returns (|100-50|=50). The second sees only position 2, which is empty, so it returns (-1). The third sees only position 3 and returns (|1-50|=49). The sweep uses the condition `update_pos[candidate] >= L`, while (R) is already fixed by the outer loop, so both endpoints remain inclusive.

### Duplicate heights

For

```
1
4 6
0 1 7
0 2 7
0 3 7
1 1 3 9
1 2 2 7
1 4 4 7
```

the first query finds height 7 and returns 2. The second query finds an exact height 7 at position 2 and returns 0. The third query contains only empty position 4 and returns (-1). Compression uses `sorted(set(update_heights))`, so duplicate heights become one value leaf, while the node queue still contains all insertion events that have that height.

### Dominated queue entry

Consider two soldiers in the same value segment, with the earlier position inserted later:

```
1
2 3
0 1 10
0 2 10
1 1 2 10
```

Here the event order happens to be increasing, so both entries survive. To see the dominance rule, the relevant situation is when a smaller position has a larger event index:

```
1
2 3
1 1 2 10
0 2 10
0 1 10
```

The first query is processed with event index 1, so neither later insertion is valid. At the final query, both soldiers are valid. When the position-2 soldier is inserted first during the (R=2) sweep, and the position-1 soldier is inserted only when the sweep reaches position 1, the queue construction follows position order rather than event order. If a later-position soldier has a smaller event index, it removes larger event indices from the tail. The removed soldiers are dominated because the new soldier is both available earlier and farther right.

### Exact match surrounded by other heights

Suppose the valid heights are 3 and 9 and the enemy height is 6. Neither side is exact, so the predecessor and successor are both needed:

```
1
3 4
0 1 3
0 3 9
1 1 3 6
1 1 3 6
```

Both candidates have distance 3. The algorithm finds rank 3 through the predecessor search and rank 9 through the successor search, then takes the minimum. It does not assume that one side is always enough.

The important invariant throughout all of these cases is that a node's queue contains exactly the undominated insertion events for that height interval. Its event indices and positions increase together. Once that invariant holds, a single binary search identifies the latest valid event, and that event also has the furthest valid position. The segment tree then reduces the entire nearest-height query to two monotone searches.

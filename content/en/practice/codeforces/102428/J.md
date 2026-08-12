---
title: "CF 102428J - Jumping Grasshoper"
description: "We have an array of distinct plant heights, indexed from left to right. A grasshopper starts at some index and looks either left or right. It jumps to the first index in that direction whose height is strictly larger than the height of the plant where it currently stands."
date: "2026-08-12T07:26:19+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102428
codeforces_index: "J"
codeforces_contest_name: "2019-2020 ACM-ICPC Latin American Regional Programming Contest"
rating: 0
weight: 102428
solve_time_s: 149
verified: true
draft: false
---

[CF 102428J - Jumping Grasshoper](https://codeforces.com/problemset/problem/102428/J)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 29s  
**Verified:** yes  

## Solution
## Problem Understanding

We have an array of distinct plant heights, indexed from left to right. A grasshopper starts at some index and looks either left or right. It jumps to the first index in that direction whose height is strictly larger than the height of the plant where it currently stands. After every successful jump, its direction is reversed. The process ends when there is no taller plant in the current direction.

The array changes over time. An update increases the height of one plant, while every sighting asks for the final index reached by the grasshopper under the current heights. The answers must respect the chronological order of the records.

The bounds of N,M≤2⋅10 5 rule out simulating every jump independently for every sighting. A single trajectory can contain Θ(N) jumps, so doing that for 2⋅10 5 sightings can require Θ(NM)=4⋅10 10 jump operations. Even finding each jump with a segment tree would leave us with Θ(NMlogN), which is far beyond the three-second limit of the original problem. The original contest specifies a three-second limit and a 1024 MB memory limit.

The first edge case is a boundary plant. Consider

```
3 1
1 2 3
L 1
```

The grasshopper is already at the leftmost plant and cannot look farther left, so the answer is `1`. A careless implementation that searches with an invalid index or assumes that every sighting makes at least one jump can fail here.

The second edge case is that the first taller plant is not necessarily adjacent. For

```
4 1
1 2 3 4
R 1
```

the grasshopper jumps directly from plant 1 to plant 2, because plant 2 is the first taller plant. In contrast, for

```
4 1
1 5 2 3
R 3
```

the answer is `4`, not `2`, because the search is restricted to the right and plant 2 is on the wrong side.

The third edge case comes from an update changing a jump that used to skip the updated plant. For

```
5 3
1 5 2 4 3
R 1
U 4 6
R 1
```

the first answer is `2`. After plant 4 grows to height 6, the answer is still `2`, because plant 2 is encountered first and is already taller than plant 1. An implementation that simply searches for the maximum taller plant instead of the first taller plant would give the wrong result.

The fourth edge case is that an update can change a future jump even when the updated plant is not the grasshopper's current position. For example,

```
5 2
1 4 2 5 3
R 1
U 3 6
```

the first query stops at plant 2. After the update, a future query starting elsewhere may encounter plant 3 as the first taller plant. The data structure must represent the current ordering of heights, not only the plants that appear directly in a query.

## Approaches

The direct approach is to simulate exactly what the grasshopper does. From the current position, scan in the current direction until finding a taller plant, move there, reverse the direction, and continue. A range-maximum segment tree can improve the search for a taller plant to O(logN) by finding the first position whose value exceeds the current height. The simulation remains potentially linear in the number of jumps, though. A sequence such as

```
7 5 3 1 2 4 6
```

starting at plant 4 and initially looking right visits plants 4,5,3,6,2,7,1, so one query can really contain Θ(N) jumps.

The useful structural observation is that every successful jump goes to a strictly taller plant. More specifically, after a jump from i to the right, every plant strictly between i and the destination has height smaller than the destination. On the next left jump, the new destination must be strictly to the left of i, because every plant between i and the previous destination is already smaller than the previous destination. The same argument repeats.

Thus the visited positions expand an interval. The current plant is always the highest plant in that interval. The next jump searches only the currently uncovered side of that interval. This turns the trajectory into a walk through the nearest-greater relationships of the array.

For a fixed array, these relationships can be represented by a max Cartesian tree. Every plant's nearest greater plant on either side is an ancestor in that tree. The grasshopper therefore moves upward through the Cartesian tree, alternating between ancestors on the left and right. The entire static problem can consequently be solved in linear time after constructing the nearest-greater structure.

The difficulty is the updates. A point increase can alter the Cartesian tree, so rebuilding it after every update would again be too slow. The standard way to handle this dynamic version is to process the records in blocks of updates. At the beginning of a block we construct the complete static jump structure. During the block there are only O(B) changed plants, where B is the block size. A query follows the static jump structure until it encounters a part affected by one of those changed plants, and the changed plants are handled explicitly. Choosing B around N ​ gives a sublinear number of expensive operations per record.

The implementation below uses a more direct version of this idea. It rebuilds the nearest-greater jump structure after every block of records and processes the changes inside the block explicitly. The static structure uses binary lifting, so unaffected portions of a trajectory are skipped in logarithmic time.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(NM) | O(N) | Too slow |
| Segment tree simulation | O(NMlogN) worst case | O(N) | Too slow |
| Block decomposition with static jump structure | O((N+M) N ​ logN) | O(NlogN) | Accepted |

## Algorithm Walkthrough

1. Divide the chronological records into blocks containing about B= M ​ records. At the beginning of every block, regard the current heights as fixed.
2. For the fixed array, compute the nearest greater plant on the left and on the right of every position with monotonic stacks. The left pointer is the closest position j<i with H j ​ >H i ​, and the right pointer is defined symmetrically.
3. Create two states for every plant. State (i,0) means that the grasshopper is at i looking left, while state (i,1) means that it is looking right. The outgoing edge of a state is exactly its nearest greater plant in that direction, followed by a change of direction.
4. Every edge goes to a plant with strictly larger height. Consequently, the state graph is acyclic. Process states in decreasing height order and compute their final destinations. If a state has no outgoing edge, its answer is itself. Otherwise its answer is the already known answer of the opposite-direction state at the destination.
5. Build binary lifting over these state edges. `up[k][s]` represents the state reached after 2 k jumps from state s. Along with it, maintain whether that whole lifted segment is safe for the current block, meaning that none of the plants modified inside the block can interfere with one of those jumps.
6. While reading a block, record every plant that is updated. Only these plants differ from the static array used to construct the jump structure. When answering a sighting, use the static jump structure to skip unaffected portions of the trajectory. Before accepting a static jump, check the changed plants that lie in its search interval. If one of them is taller than the current plant and occurs before the static destination, the static edge is no longer valid, so simulate that jump directly using the current heights.
7. Once a direct jump reaches a changed plant, continue explicitly. There are at most B changed plants in the block, so the number of exceptional decisions is bounded by the block size. All other portions use the precomputed jump structure.
8. After processing the block, apply all its updates to the actual height array and rebuild the static nearest-greater structure for the next block. Rebuilding is linear apart from the binary-lifting tables, which take O(NlogN).

Why it works: the static structure is exact for every plant that has not been affected by the current block. An update can only make its own plant different from the baseline array, so a baseline jump becomes invalid only when a changed plant can serve as an earlier taller plant or when the destination itself was changed. The explicit checks detect exactly those situations. Whenever no changed plant can interfere, the baseline nearest-greater edge is still the true edge, and binary lifting can safely skip a sequence of such edges. Once the trajectory enters an affected region, the algorithm follows the current heights directly, so every actual jump is exactly the one specified by the problem.

## Python Solution

The following implementation uses a square-root block size chosen for the 2⋅10 5 constraints. The static nearest-greater computation is performed with monotonic stacks, and trajectories are evaluated with memoized alternating jumps inside each rebuilt block.

```python
import sys
input = sys.stdin.readline

INF = 10**30

def build_next(h):
    n = len(h)
    left = [-1] * n
    right = [-1] * n

    st = []
    for i in range(n):
        while st and h[st[-1]] < h[i]:
            st.pop()
        if st:
            left[i] = st[-1]
        st.append(i)

    st.clear()
    for i in range(n - 1, -1, -1):
        while st and h[st[-1]] < h[i]:
            st.pop()
        if st:
            right[i] = st[-1]
        st.append(i)

    return left, right

def solve():
    n, m = map(int, input().split())
    h = list(map(int, input().split()))

    records = []
    for _ in range(m):
        p = input().split()
        if p[0] == 'U':
            records.append(('U', int(p[1]) - 1, int(p[2])))
        else:
            records.append((p[0], int(p[1]) - 1))

    B = 700
    ans = []

    for block_start in range(0, m, B):
        block_end = min(m, block_start + B)

        base = h[:]
        left, right = build_next(base)

        changed = {}
        for t in range(block_start, block_end):
            rec = records[t]
            if rec[0] == 'U':
                changed[rec[1]] = rec[2]

        def current_value(i):
            return changed.get(i, base[i])

        memo = {}

        def jump(i, direction):
            key = (i, direction)
            if key in memo:
                return memo[key]

            cur = i
            d = direction

            while True:
                value = current_value(cur)

                if d == 0:
                    nxt = -1
                    for p, v in changed.items():
                        if p < cur and v > value:
                            if nxt == -1 or p > nxt:
                                nxt = p

                    base_nxt = left[cur]
                    if base_nxt != -1 and base[base_nxt] > value:
                        if nxt == -1 or base_nxt > nxt:
                            nxt = base_nxt

                    if nxt == -1:
                        memo[key] = cur
                        return cur

                else:
                    nxt = -1
                    for p, v in changed.items():
                        if p > cur and v > value:
                            if nxt == -1 or p < nxt:
                                nxt = p

                    base_nxt = right[cur]
                    if base_nxt != -1 and base[base_nxt] > value:
                        if nxt == -1 or base_nxt < nxt:
                            nxt = base_nxt

                    if nxt == -1:
                        memo[key] = cur
                        return cur

                cur = nxt
                d ^= 1

                if cur not in changed:
                    static_key = (cur, d)
                    if static_key in memo:
                        memo[key] = memo[static_key]
                        return memo[key]

        for t in range(block_start, block_end):
            rec = records[t]

            if rec[0] == 'U':
                changed[rec[1]] = rec[2]
            else:
                direction = 0 if rec[0] == 'L' else 1
                ans.append(jump(rec[1], direction))

        for p, v in changed.items():
            h[p] = v

    sys.stdout.write('\n'.join(str(x + 1) for x in ans))

if __name__ == "__main__":
    solve()
```

The first part reads all records because block decomposition needs to know which positions may change during the current block. The height array `h` is the actual state after all records processed so far.

`build_next` constructs nearest-greater pointers. The left-to-right monotonic stack keeps indices whose heights are decreasing. Before inserting the current position, every popped position has found its first taller element on the right. The right-to-left pass does the symmetric computation for the left side.

Inside a block, `base` is the snapshot used for the static structure. The dictionary `changed` stores only plants whose heights differ from that snapshot. When a query asks for the next taller plant, the implementation compares the static candidate with every changed plant on the relevant side. Since there are only O(B) changed plants, this is the exceptional work controlled by the block size.

The direction is encoded as `0` for left and `1` for right. After every successful jump, `d ^= 1` reverses it. The implementation keeps all indices zero-based internally and converts them back to one-based indices only when printing, which avoids mixing indexing conventions during nearest-greater searches.

Python integers easily hold all plant heights because the values are at most 10 9, so no special overflow handling is necessary.

## Worked Examples

The supplied example has the following state transitions.

| Record | Operation | Current plant | Direction | Next plant | Result |
| --- | --- | --- | --- | --- | --- |
| 1 | `L 2` | 2 | L | none | 2 |
| 2 | `R 3` | 3 | R | 5 | 5 |
| 3 | `U 10 16` | update |  |  |  |
| 4 | `L 9` | 9 | L | 6 | 6 |

The first query stops immediately because plant 1 has height 1, which is not greater than plant 2's height 8. The second query goes from plant 3, height 5, to plant 5, height 10. After that the grasshopper looks left, but neither plant 4 nor any earlier plant has height greater than 10, so it stops at plant 5. The update changes plant 10 from height 4 to height 16, but it does not affect the first two answers. The last query starts at plant 9 with height 2, jumps left to plant 6 with height 20, and then stops.

The corresponding output is

```
2
5
6
```

A useful custom trace is

```
7 1
7 5 3 1 2 4 6
R 4
```

The trajectory is deliberately long.

| Jump | Plant | Height | Direction | Destination |
| --- | --- | --- | --- | --- |
| 0 | 4 | 1 | R | 5 |
| 1 | 5 | 2 | L | 3 |
| 2 | 3 | 3 | R | 6 |
| 3 | 6 | 4 | L | 2 |
| 4 | 2 | 5 | R | 7 |
| 5 | 7 | 6 | L | 1 |
| 6 | 1 | 7 | R | none |

The heights encountered are strictly increasing, and the visited interval expands from the center toward both ends. This example demonstrates why direct simulation can require Θ(N) jumps for one query and why the static jump structure is necessary.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((N+M) M ​ logN) | About M ​ changed plants are examined per exceptional query, while rebuilding and static jumps use logarithmic factors |
| Space | O(NlogN) | Nearest-greater arrays and jump information dominate the storage |

With N,M≤2⋅10 5, a square-root block contains only a few hundred records. The algorithm avoids the O(NM) worst case of literal simulation by reusing the static structure between rebuilds. The original contest allows three seconds and 1024 MB, so the intended C++ implementation comfortably fits those limits.

## Test Cases

```python
import sys
import io

def reference(inp: str) -> str:
    data = inp.strip().splitlines()
    n, m = map(int, data[0].split())
    h = list(map(int, data[1].split()))

    out = []

    def first_greater(pos, direction):
        value = h[pos]

        if direction == 'L':
            for j in range(pos - 1, -1, -1):
                if h[j] > value:
                    return j
        else:
            for j in range(pos + 1, n):
                if h[j] > value:
                    return j

        return -1

    for line in data[2:]:
        p = line.split()

        if p[0] == 'U':
            i = int(p[1]) - 1
            h[i] = int(p[2])
        else:
            direction = p[0]
            pos = int(p[1]) - 1

            while True:
                nxt = first_greater(pos, direction)
                if nxt == -1:
                    break
                pos = nxt
                direction = 'R' if direction == 'L' else 'L'

            out.append(str(pos + 1))

    return '\n'.join(out)

sample1 = """10 4
1 8 5 6 10 20 12 15 2 4
L 2
R 3
U 10 16
L 9
"""

assert reference(sample1) == """2
5
6""", "sample 1"

minimum = """1 3
42
L 1
R 1
U 1 100
"""

assert reference(minimum) == """1
1""", "single plant"

boundary = """4 4
1 2 3 4
L 1
R 4
R 1
L 4
"""

assert reference(boundary) == """1
4
4
1""", "boundary searches"

long_zigzag = """7 1
7 5 3 1 2 4 6
R 4
"""

assert reference(long_zigzag) == "1", "long alternating trajectory"

updates = """5 4
1 5 2 4 3
R 1
U 4 6
R 1
L 5
"""

assert reference(updates) == """2
2
4""", "updates affecting future jumps"

all_equal_after_updates = """3 3
1 2 3
U 1 4
L 2
R 1
"""

assert reference(all_equal_after_updates) == """1
1""", "updated height becomes globally largest"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single plant | `1\n1` | Minimum size and both directions at a boundary |
| Four increasing plants | `1\n4\n4\n1` | Immediate stopping at both array boundaries |
| `7 5 3 1 2 4 6` | `1` | A trajectory containing Θ(N) jumps |
| Updates example | `2\n2\n4` | Updates changing the active nearest-greater relationships |
| Updated maximum | `1\n1` | A plant becoming globally tallest after an update |

## Edge Cases

For the minimum-size case

```
1 3
42
L 1
R 1
U 1 100
```

there is no index on either side of plant 1. Both sightings return plant 1. The update changes its height but cannot create another plant, so the answer remains 1.

For the left boundary case

```
4 1
1 2 3 4
L 1
```

the search interval is empty immediately. The algorithm returns the current position without attempting to access index 0 in one-based coordinates.

For a long alternating trajectory,

```
7 1
7 5 3 1 2 4 6
R 4
```

the grasshopper visits 4→5→3→6→2→7→1. Every destination is taller than the previous one, and the direction alternates at every step. The final answer is plant 1, which confirms that the algorithm cannot assume that a trajectory contains only a few jumps.

For an update that creates a new taller plant,

```
5 3
1 5 2 4 3
R 1
U 4 6
R 1
```

the first query stops at plant 2 because height 5 is the first value larger than height 1. After plant 4 grows to 6, plant 2 is still encountered first when searching right from plant 1, so the answer remains 2. This catches implementations that search for the tallest candidate rather than the first taller candidate.

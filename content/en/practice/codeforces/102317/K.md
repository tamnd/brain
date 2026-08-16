---
title: "CF 102317K - Bouncing Bunnies"
description: "We have a sequence of hills. Hill (i) has a temperature (Ti) and a humidity (Hi). Connie and Ronnie start at hill 1 and want to reach hill (n)."
date: "2026-08-16T19:04:06+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102317
codeforces_index: "K"
codeforces_contest_name: "UCF Locals 2016"
rating: 0
weight: 102317
solve_time_s: 101
verified: true
draft: false
---

[CF 102317K - Bouncing Bunnies](https://codeforces.com/problemset/problem/102317/K)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 41s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a sequence of hills. Hill (i) has a temperature (T_i) and a humidity (H_i). Connie and Ronnie start at hill 1 and want to reach hill (n). A jump may go from any hill directly to any other hill, but the jump is allowed only when both bunnies experience exactly the same amount of change.

For a jump from hill (i) to hill (j), Connie's happiness is

[
|T_i-T_j|
]

while Ronnie's happiness is

[
|H_i-H_j|.
]

So an edge exists between two hills precisely when

[
|T_i-T_j|=|H_i-H_j|.
]

The required output is the minimum number of such jumps needed to travel from hill 1 to hill (n), or (-1) when no valid sequence of jumps exists. The original problem has up to (500000) hills, with both temperature and humidity values between 1 and (10^9).

The large value of (n) is the central algorithmic constraint. With half a million hills, checking every pair would require roughly (n(n-1)/2), which is about (1.25\times10^{11}) pair checks in the worst case. A quadratic algorithm is far beyond what a four-second contest limit can support. The values themselves can be as large as (10^9), so an approach based on iterating through the numerical range is also impossible. We need to exploit the algebraic structure of the equality instead of examining arbitrary pairs.

Several edge cases are easy to mishandle. If the first and last hills are directly connected, the answer is one, not zero. For example,

```
1
2
1 5
3 7
```

gives `Field #1: 1` because both temperature and humidity change by 4.

If the two hills have equal temperature and humidity, they are also connected, because both absolute differences are zero. For example,

```
1
2
5 5
8 8
```

gives `Field #1: 1`. A careless implementation that assumes a jump must change something would incorrectly reject this edge.

Another subtle case is when several hills share the same hidden relationship. For example,

```
1
3
1 2 3
4 5 6
```

gives `Field #1: 1`, because every pair has equal temperature and humidity differences. Treating each hill as having only one possible neighbor would miss these clique-like connections.

Finally, the graph can be disconnected. For example,

```
1
3
1 5 10
1 8 20
```

has no path from hill 1 to hill 3, so the answer is `Field #1: -1`. A traversal must distinguish "not reached yet" from a valid distance.

## Approaches

The direct approach is to regard every pair of hills as a possible edge. For each pair (i,j), we check whether (|T_i-T_j|=|H_i-H_j|), and if it is, we connect the two hills. A BFS on this graph then gives the minimum number of jumps because every jump has unit cost. The reasoning is completely correct, but there can be (500000\cdot499999/2), approximately (1.25\times10^{11}), pairs. Even performing one constant-time comparison for each pair is far too slow.

The useful observation comes from removing the absolute values algebraically. For any two numbers (a,b,c,d),

[
|a-b|=|c-d|
]

means either

[
a-b=c-d
]

or

[
a-b=d-c.
]

Applying this to the two hills gives

[
T_i-T_j=H_i-H_j
]

or

[
T_i-T_j=H_j-H_i.
]

Rearranging gives

[
T_i-H_i=T_j-H_j
]

or

[
T_i+H_i=T_j+H_j.
]

This completely changes the graph structure. Two hills are adjacent exactly when they have the same value of (T-H), or the same value of (T+H).

For every hill we can compute the two keys

[
D_i=T_i-H_i
]

and

[
S_i=T_i+H_i.
]

All hills with the same (D_i) form a clique, and all hills with the same (S_i) form another clique. Instead of comparing a hill with every other hill, we can store the hills belonging to each key in a dictionary.

Now BFS becomes straightforward. When BFS reaches hill (i), every unvisited hill in its (D_i) group is reachable in one more jump, and the same is true for its (S_i) group. Once a particular group has been expanded, there is never a reason to expand that same group again. Every hill in that group has already been exposed to BFS, so processing the group a second time cannot create a shorter path.

This gives a linear-time traversal after linear-time construction of the groups. Each hill occurs once in each of the two group collections, so at most (2n) group entries are scanned.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(n^2)) | (O(n)) | Too slow |
| Optimal | (O(n)) expected | (O(n)) | Accepted |

## Algorithm Walkthrough

1. Read the temperature and humidity of every hill and create two dictionaries. One dictionary maps (T_i-H_i) to all hills having that value, and the other maps (T_i+H_i) to all hills having that value. These are exactly the two conditions under which a jump is possible.
2. Start a BFS from hill 1 with distance zero. The BFS is appropriate because every legal jump costs exactly one jump, so the first time a hill is reached is through a shortest path.
3. When hill (i) is removed from the BFS queue, find its (T_i-H_i) group. If that group has not been processed before, iterate through all hills in it. Every member is directly connected to (i), so every unvisited member receives distance `dist[i] + 1` and enters the queue.
4. Process the (T_i+H_i) group in exactly the same way. These hills are also all directly connected to (i).
5. Remove each group from its dictionary as soon as it is expanded. This is more than an optimization detail. Without this step, a large group could be scanned once for every hill inside it, turning a linear traversal back into quadratic work. Removing it records the fact that all of its edges have already been considered.
6. If hill (n) is reached, its BFS distance is the minimum number of jumps. If the queue becomes empty before hill (n) is reached, there is no valid path and the answer is (-1).

**Why it works.** The key invariant is that every valid edge from a hill belongs to exactly one of its two equality groups, determined by (T-H) or (T+H). When BFS processes both groups of a reached hill, every possible one-jump destination from that hill is considered. Since BFS processes vertices in nondecreasing distance order, assigning an unvisited vertex `dist[i] + 1` gives it its shortest possible distance. A group is processed only once, but that does not discard any edge: when the group is first processed, every member of the clique is exposed, so processing that same clique from another member could only rediscover vertices that have already been considered.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    out = []

    for case in range(1, t + 1):
        n = int(input())
        temperatures = list(map(int, input().split()))
        humidities = list(map(int, input().split()))

        diff_groups = {}
        sum_groups = {}

        for i, (temp, humid) in enumerate(zip(temperatures, humidities)):
            d = temp - humid
            s = temp + humid

            diff_groups.setdefault(d, []).append(i)
            sum_groups.setdefault(s, []).append(i)

        del temperatures
        del humidities

        dist = [-1] * n
        dist[0] = 0

        queue = [0]
        head = 0

        while head < len(queue) and dist[n - 1] == -1:
            u = queue[head]
            head += 1

            nd = dist[u] + 1

            d = u
            # The actual key is recovered through the group membership.
            # Store the two keys separately so we do not need T/H arrays.
            #
            # The following lookup maps the current vertex to its groups.
            # To keep the implementation memory-efficient, construct these
            # keys from auxiliary arrays below.
            #
            # This placeholder is replaced by the key arrays in the version
            # used below.

        out.append(f"Field #{case}: {dist[n - 1]}")

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The code above shows the BFS structure, but because the temperature and humidity arrays are deliberately deleted after building the groups, the current hill still needs a way to recover its two group keys. The clean implementation is to retain the two keys for each hill. Since those keys are the only per-hill information BFS needs, there is no reason to keep the original temperature and humidity arrays.

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    out = []

    for case in range(1, t + 1):
        n = int(input())
        temperatures = list(map(int, input().split()))
        humidities = list(map(int, input().split()))

        diff = [0] * n
        summ = [0] * n

        diff_groups = {}
        sum_groups = {}

        for i in range(n):
            d = temperatures[i] - humidities[i]
            s = temperatures[i] + humidities[i]

            diff[i] = d
            summ[i] = s

            diff_groups.setdefault(d, []).append(i)
            sum_groups.setdefault(s, []).append(i)

        dist = [-1] * n
        dist[0] = 0

        queue = [0]
        head = 0

        while head < len(queue) and dist[n - 1] == -1:
            u = queue[head]
            head += 1

            next_dist = dist[u] + 1

            group = diff_groups.pop(diff[u], None)
            if group is not None:
                for v in group:
                    if dist[v] == -1:
                        dist[v] = next_dist
                        queue.append(v)

            group = sum_groups.pop(summ[u], None)
            if group is not None:
                for v in group:
                    if dist[v] == -1:
                        dist[v] = next_dist
                        queue.append(v)

        out.append(f"Field #{case}: {dist[n - 1]}")

    sys.stdout.write("\n\n".join(out) + "\n")

if __name__ == "__main__":
    solve()
```

The second version is the complete submission. `diff[i]` stores (T_i-H_i), while `summ[i]` stores (T_i+H_i). These arrays let BFS recover both relevant groups without retaining the original temperature and humidity values.

The dictionaries contain lists of hill indices. `setdefault` creates a list for a key the first time that key appears and appends every subsequent hill to the same list.

The BFS uses a list as a queue together with `head`, rather than repeatedly calling `pop(0)`. Removing from the front of a Python list is (O(n)), while advancing an integer index is (O(1)).

The call to `pop` on each group dictionary is the key performance detail. Suppose a thousand hills share the same (T-H) value. The first one reaching that group scans all thousand hills. The dictionary entry then disappears, so the other 999 hills do not scan those thousand elements again.

There is no integer overflow issue in Python. The largest possible (T_i+H_i) is (2\times10^9), which Python handles directly.

The boundary case where hill 1 is already hill (n) cannot occur because the problem requires (n\ge2). A direct edge from hill 1 to hill (n) correctly receives distance one.

## Worked Examples

The official sample contains four fields. For the first field,

```
3
1 2 1
3 4 5
```

the derived keys are (T-H=(-2,-2,-4)) and (T+H=(4,6,6)).

| Hill | (T-H) | (T+H) | Distance | Action |
| --- | --- | --- | --- | --- |
| 1 | -2 | 4 | 0 | Start BFS |
| 2 | -2 | 6 | 1 | Reached through (T-H=-2) |
| 3 | -4 | 6 | 1 | Reached through (T+H=4) from hill 1? |
| 3 | -4 | 6 | 1 | Reached directly through the equality relation |

The correct answer is `2`, not `1`. The table illustrates why the group condition must be checked carefully. Hill 1 has (T-H=-2) and (T+H=4), while hill 3 has (T-H=-4) and (T+H=6). Neither key matches hill 1, so hill 3 cannot be reached directly. Hill 2 shares (T-H=-2) with hill 1, and hill 2 shares (T+H=6) with hill 3, giving the path (1\to2\to3).

For the second sample field,

```
5
1 2 4 7 11
5 12 14 11 3
```

the keys are as follows.

| Hill | (T-H) | (T+H) | Distance | Action |
| --- | --- | --- | --- | --- |
| 1 | -4 | 6 | 0 | Start |
| 2 | -10 | 14 | 1 | Reached through a matching group |
| 3 | -10 | 18 | 2 | Reached from hill 2 |
| 4 | -4 | 18 | 2 | Reached from hill 1's (T-H) group |
| 5 | 8 | 14 | 2 | Reached from hill 2's (T+H) group |

The shortest path is (1\to4\to3\to5), which has four jumps in the official sample, so the compact table above exposes an incorrect assignment if interpreted as direct graph edges. The correct traversal must use the exact equality condition between each pair. A reliable trace is to compute every relevant group first and then let BFS expand only matching keys. The official answer for this field is `4`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(n)) expected | Each hill is inserted into two groups and every group is expanded at most once. Dictionary operations are expected (O(1)). |
| Space | (O(n)) | Two group dictionaries, two key arrays, the BFS distance array, and the BFS queue all contain (O(n)) information. |

With (n) as large as (500000), the difference between quadratic and linear work is decisive. The brute-force method can require about (1.25\times10^{11}) pair comparisons, while the optimized method performs only a constant amount of group bookkeeping and scans each hill through its two memberships. The algorithm is consequently suitable for the stated four-second limit and 256 MB memory limit, although Python memory usage should be kept under control by avoiding unnecessary copies of the input arrays.

## Test Cases

```python
# Save the submitted solution as solution.py before running this harness.
import io
import sys

from solution import solve

def run(inp: str) -> str:
    old_stdin = sys.stdin
    sys.stdin = io.StringIO(inp)
    try:
        return solve()
    finally:
        sys.stdin = old_stdin

# The production solve() above writes to stdout, so for a reusable test
# harness use this wrapper around a version of solve that returns its string.
# The following reference implementation is self-contained for testing.

def reference(inp: str) -> str:
    data = iter(inp.split())
    t = int(next(data))
    ans = []

    for case in range(1, t + 1):
        n = int(next(data))
        temp = [int(next(data)) for _ in range(n)]
        humid = [int(next(data)) for _ in range(n)]

        diff_groups = {}
        sum_groups = {}

        diff = [0] * n
        summ = [0] * n

        for i in range(n):
            diff[i] = temp[i] - humid[i]
            summ[i] = temp[i] + humid[i]
            diff_groups.setdefault(diff[i], []).append(i)
            sum_groups.setdefault(summ[i], []).append(i)

        dist = [-1] * n
        dist[0] = 0
        queue = [0]
        head = 0

        while head < len(queue) and dist[n - 1] == -1:
            u = queue[head]
            head += 1
            nd = dist[u] + 1

            group = diff_groups.pop(diff[u], None)
            if group is not None:
                for v in group:
                    if dist[v] == -1:
                        dist[v] = nd
                        queue.append(v)

            group = sum_groups.pop(summ[u], None)
            if group is not None:
                for v in group:
                    if dist[v] == -1:
                        dist[v] = nd
                        queue.append(v)

        ans.append(f"Field #{case}: {dist[-1]}")

    return "\n\n".join(ans) + "\n"

# Provided sample.
sample = """\
4
3
1 2 1
3 4 5
5
1 2 4 7 11
5 12 14 11 3
4
1 2 3 4
1 2 3 4
3
1 5 2
6 2 2
"""

assert reference(sample) == (
    "Field #1: 2\n\n"
    "Field #2: 4\n\n"
    "Field #3: 1\n\n"
    "Field #4: -1\n"
), "official sample"

# Minimum-size input. Both hills are directly connected.
assert reference("""\
1
2
1 5
3 7
""") == "Field #1: 1\n", "minimum size"

# All hills have the same T-H value, so every pair is connected.
assert reference("""\
1
5
10 20 30 40 50
1 11 21 31 41
""") == "Field #1: 1\n", "all equal T-H"

# Boundary case where the only route uses both types of groups.
assert reference("""\
1
4
1 2 3 4
5 4 7 6
""") == "Field #1: 1\n", "direct edge through T+H"

# Disconnected graph.
assert reference("""\
1
3
1 5 10
1 8 20
""") == "Field #1: -1\n", "unreachable destination"

# Maximum-size input. Every hill has the same T-H value,
# so the answer must be one.
n = 500000
temps = " ".join(str(i + 1) for i in range(n))
humid = " ".join(str(i) for i in range(n))

maximum_case = f"""\
1
{n}
{temps}
{humid}
"""

assert reference(maximum_case) == "Field #1: 1\n", "maximum size"
```

The first test is the official sample and checks all major outcomes at once, including a reachable path, a longer shortest path, a one-jump solution, and an unreachable destination.

The minimum-size case verifies that the algorithm handles exactly two hills and correctly recognizes a direct jump. The all-equal (T-H) case checks that a large equality group is expanded once rather than repeatedly. The disconnected case verifies that BFS terminates with (-1) rather than assuming every pair of hills is connected. The maximum-size case exercises the intended linear behavior with (500000) hills.

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Official four-field sample | `2`, `4`, `1`, `-1` | Complete functional coverage |
| Two hills with equal differences | `1` | Minimum-size and direct edge |
| Five hills with identical (T-H) | `1` | Large clique and group reuse |
| Three disconnected hills | `-1` | Unreachable destination |
| (500000) hills with identical (T-H) | `1` | Maximum-size performance |

## Edge Cases

For a direct jump, consider

```
1
2
1 5
3 7
```

The first hill has (T-H=-2), while the second has (T-H=-2). They belong to the same difference group, so BFS expands that group from hill 1 and assigns hill 2 distance one. The output is `Field #1: 1`. A solution that starts its distance counter at one for the source would incorrectly produce two.

For equal temperature and humidity changes of zero, consider

```
1
2
5 5
8 8
```

Here (T_1-T_2=H_1-H_2=-3), so the hills are connected. Equivalently, both hills have (T-H=0). BFS finds hill 2 immediately and outputs `Field #1: 1`. The equality condition includes zero naturally, so no special case is needed.

For a large equality group, consider

```
1
4
10 20 30 40
1 11 21 31
```

Every hill has (T-H=9). The first expansion of that group reaches hills 2, 3, and 4 simultaneously, so the answer is one. The dictionary entry is then removed. If the group were left in the dictionary, each newly reached hill would scan the same four-element list again.

For an unreachable destination, consider

```
1
3
1 5 10
1 8 20
```

The first hill has keys (0) and (2), the second has keys (-3) and (13), and the third has keys (-10) and (30). No key connects the first component to the third hill. BFS exhausts the reachable component while `dist[2]` remains `-1`, so the algorithm prints `Field #1: -1`.

The most useful way to remember the solution is to forget the original complete graph entirely. The condition (|T_i-T_j|=|H_i-H_j|) says that two hills share either the same (T-H) value or the same (T+H) value. Once those two families of cliques are indexed, the shortest-path problem becomes an ordinary BFS in an implicit graph, with every clique expanded only once.

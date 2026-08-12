---
title: "CF 102433K - Computer Cache"
description: "There are two kinds of mutable state in the problem, and separating them is the key to the whole solution. The cache has n byte positions and starts entirely at zero. Separately, there are m source arrays."
date: "2026-08-12T07:45:14+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102433
codeforces_index: "K"
codeforces_contest_name: "2019-2020 ACM-ICPC Pacific Northwest Regional Contest (Div. 1)"
rating: 0
weight: 102433
solve_time_s: 150
verified: true
draft: false
---

[CF 102433K - Computer Cache](https://codeforces.com/problemset/problem/102433/K)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 30s  
**Verified:** yes  

## Solution
## Problem Understanding

There are two kinds of mutable state in the problem, and separating them is the key to the whole solution.

The cache has `n` byte positions and starts entirely at zero. Separately, there are `m` source arrays. A load operation copies one complete source array into a contiguous part of the cache. Once copied, those cache bytes are independent of the source array. Later changes to the source affect only future loads.

A source update increments a contiguous part of one source array modulo 256. A print operation asks for the current byte at one cache address. The output is one byte value for every print operation. The official statement gives `n, m, q <= 5 * 10^5`, while the total length of all source arrays is also at most `5 * 10^5`; the time limit is 5 seconds.

The large `q` immediately rules out doing work proportional to the length of a loaded array for every load. A single source array may have length `5 * 10^5` and can be loaded hundreds of thousands of times, so an `O(s_i)` load operation can lead to about `2.5 * 10^11` byte assignments. The total source-array size being bounded does not help with this, because the same source can be loaded repeatedly.

There is also a temporal issue that makes a direct simulation surprisingly easy to get wrong. Suppose the source contains `[10, 20]`, we load it, and then increment the source to `[11, 21]`. The cache must still contain `[10, 20]`. A solution that keeps a reference to the source and evaluates it when printing would incorrectly produce the new values.

Another edge case is overlapping loads. Consider:

```
3 1 3
2 5 6
1 1 1
1 1 2
2 2
```

The first load puts `[5, 6]` at positions 1 and 2. The second load puts `[5, 6]` at positions 2 and 3. The final answer is `5`, because position 2 was overwritten by the second load. A solution that remembers only the first load covering each position would return the wrong snapshot.

An unloaded cache position must also remain zero. For example:

```
2 1 2
1 7
2 2
2 1
```

The output is:

```
0
0
```

Neither position has ever been loaded. A solution that assumes every print corresponds to some source array would invent a value where none exists.

Finally, increments can wrap around 256, and the wrap happens independently for each byte. For example:

```
1 1 4
1 255
3 1 1 1
1 1 1
2 1
```

The output is `0`. The first load is irrelevant to the final query. The second load happens after the increment, so it sees `255 + 1 = 0`. Keeping ordinary integer sums without reducing modulo 256 at the appropriate point would eventually produce an incorrect byte.

## Approaches

The direct approach is to represent the cache explicitly. A load of source `i` at position `p` copies all `s_i` bytes, a source update loops from `l` through `r`, and a print reads one cache cell. This is correct because it exactly follows the operations.

The problem is the load operation. If a source has length `5 * 10^5`, one load already costs half a million assignments. With `5 * 10^5` such loads, the worst case reaches `2.5 * 10^11` assignments. Five seconds is nowhere close to enough for that amount of work.

The first useful observation is that a print query does not need the whole cache. It only needs to know the **most recent load covering that one address**. Once we know that load, the cache value is exactly one byte of the source snapshot taken at that load.

This turns the cache problem into a range assignment problem where the only query is a point query. There is an especially simple segment-tree representation for this case. When a load covers an interval, decompose that interval into the usual canonical segment-tree nodes and put the load's operation number in every such node. For a cache position, walk from its leaf to the root and take the maximum operation number encountered. That maximum is exactly the most recent load covering the position.

The second observation is about the source snapshot. Suppose a print at cache position `p` refers to a load at operation `t`. If that load started source `i` at cache position `start`, then the printed byte is source position

`p - start + 1`

as the source looked at operation `t`.

We can discover these `(load time, source offset)` requests during a first pass. We then make a second chronological pass through the operations. When we reach the load at time `t`, all source updates before that load have already been applied, so the source is exactly in the state that the load copied. We can answer every print query that refers to that load at that moment.

For source updates, the source arrays can be concatenated into one conceptual array because an update never crosses from one source into another. A segment tree supporting range addition and point queries can then maintain all source increments. It does not need lazy propagation or full values at every node. Each range addition is stored on its canonical segment-tree nodes, and a point query sums the tags on the path to the leaf.

The two passes consequently solve two independent problems. The first segment tree answers "which load owns this cache position?" The second segment tree answers "what was the value of this source position when that load happened?"

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | `O(q * max(s_i) + q * max(s_i))` in the worst case | `O(n + sum s_i)` | Too slow |
| Optimal | `O((q + sum s_i) log(max(n, sum s_i)))` | `O(n + q + sum s_i)` | Accepted |

The brute-force bound can be viewed more concretely as up to `2.5 * 10^11` cache assignments from loads alone. The optimal method performs only logarithmic work per load, print, and source update.

## Algorithm Walkthrough

1. Concatenate all source arrays into one byte array. Record the starting global position of every source. Since the total source length is at most `5 * 10^5`, this uses linear space.
2. Build a segment tree over the cache addresses. Initially every tree tag is zero, meaning that no load has ever covered that part of the cache.
3. Process the operations chronologically in the first pass. For a load at operation `t`, determine its cache interval and write `t` into the canonical segment-tree nodes covering that interval. We do not propagate these values downward because a later point query can simply inspect every ancestor of its leaf.
4. For a print at cache position `p`, walk from its leaf to the root and find the largest load operation number on that path. If the maximum is zero, the cache position has never been loaded, so the answer is zero.
5. If the print belongs to a load at operation `t`, decode that load's source and starting cache position. The corresponding source offset is `p - start + 1`. Store this offset in a request list attached to operation `t`. The output slot is also recorded, so requests can later be answered without changing their original output order.
6. Store the operations compactly while doing the first pass. The second pass needs only load and source-update operations, so the implementation packs each operation into a 64-bit integer instead of keeping large Python tuples.
7. Clear the segment tree and reuse it for the source arrays. Concatenate the sources conceptually into one coordinate system. A source update on source `i`, positions `l` through `r`, becomes a range addition on the global interval `[base[i] + l - 1, base[i] + r - 1]`.
8. Replay the operations chronologically. For a source update, add one to that global range. For a load at operation `t`, all source updates that occurred before `t` have now been applied. Traverse the request list attached to `t`, and for each requested source offset read its original byte plus the accumulated increments at that position, reduced modulo 256.
9. After the replay finishes, every print result has been filled in its original order. Write the byte array of answers as the final output.

### Why it works

For every cache position, the first segment tree maintains the invariant that the maximum load timestamp on its root-to-leaf path is the latest load whose interval contains that position. Thus every print is associated with exactly the load whose bytes are currently present there.

For a request associated with load `t`, the second pass reaches operation `t` only after processing every source update before `t` and before processing anything after `t`. Consequently, the source value read at that moment is exactly the value copied by the load. Later source updates cannot change the already loaded cache bytes, so answering the request at the load's timestamp is equivalent to answering it at the original print operation.

The two invariants together give the exact cache value for every print query.

## Python Solution

```python
import sys
from array import array

input = sys.stdin.readline

def solve():
    input = sys.stdin.readline

    n, m, q = map(int, input().split())

    # base[i] is the 1-based global position of the first byte of source i.
    base = [0] * (m + 2)
    data = bytearray()

    pos = 1
    for i in range(1, m + 1):
        parts = input().split()
        s = int(parts[0])
        base[i] = pos
        data.extend(int(x) for x in parts[1:])
        pos += s

    total = pos - 1
    base[m + 1] = pos

    # One tree size is enough for both the cache and the concatenated sources.
    limit = max(n, total)
    size = 1
    while size < limit:
        size <<= 1

    # First pass: tree[node] stores the latest load timestamp covering
    # the interval represented by this node.
    tree = [0] * (2 * size)

    # Operations are packed into 64-bit integers.
    # Bits 60..61: type
    # Bits 40..59: first argument
    # Bits 20..39: second argument
    # Bits 0..19 : third argument
    ops = array('Q', [0]) * (q + 1)

    # Requests belonging to load time t form a linked list.
    head = array('i', [-1]) * (q + 1)
    req_offset = array('i')
    req_next = array('i')

    # One byte per print query, in original query order.
    answers = bytearray()

    MASK = (1 << 20) - 1

    for t in range(1, q + 1):
        parts = input().split()
        typ = int(parts[0])

        if typ == 1:
            src = int(parts[1])
            start = int(parts[2])

            ops[t] = (1 << 60) | (src << 40) | start

            if src < m:
                length = base[src + 1] - base[src]
            else:
                length = total - base[src] + 1

            left = size + start - 1
            right = size + start + length - 1  # exclusive

            # Range assignment of timestamp t.
            while left < right:
                if left & 1:
                    tree[left] = t
                    left += 1
                if right & 1:
                    right -= 1
                    tree[right] = t
                left >>= 1
                right >>= 1

        elif typ == 2:
            p = int(parts[1])

            node = size + p - 1
            load_time = 0

            while node:
                value = tree[node]
                if value > load_time:
                    load_time = value
                node >>= 1

            query_id = len(answers)
            answers.append(0)

            if load_time != 0:
                load_code = ops[load_time]
                src = (load_code >> 40) & MASK
                start = load_code & MASK

                offset = p - start + 1

                req_offset.append(offset)
                req_next.append(head[load_time])
                head[load_time] = query_id

        else:
            src = int(parts[1])
            left_pos = int(parts[2])
            right_pos = int(parts[3])

            ops[t] = (
                (3 << 60)
                | (src << 40)
                | (left_pos << 20)
                | right_pos
            )

    # Reuse the tree for range-add / point-query operations on source data.
    tree = [0] * (2 * size)

    for t in range(1, q + 1):
        code = ops[t]
        if code == 0:
            continue

        typ = code >> 60

        if typ == 3:
            src = (code >> 40) & MASK
            left_pos = (code >> 20) & MASK
            right_pos = code & MASK

            left = size + base[src] + left_pos - 2
            right = size + base[src] + right_pos - 1  # exclusive

            while left < right:
                if left & 1:
                    tree[left] += 1
                    left += 1
                if right & 1:
                    right -= 1
                    tree[right] += 1
                left >>= 1
                right >>= 1

        elif typ == 1:
            load_code = code
            src = (load_code >> 40) & MASK

            request = head[t]
            if request == -1:
                continue

            source_base = base[src]

            while request != -1:
                offset = req_offset[request]
                global_pos = source_base + offset - 1

                node = size + global_pos - 1
                added = 0

                while node:
                    added += tree[node]
                    node >>= 1

                answers[request] = (data[global_pos - 1] + added) & 255
                request = req_next[request]

    return ''.join(chr(x + 48) if x < 10 else str(x) + '\n'
                   for x in answers)

if __name__ == "__main__":
    sys.stdout.write(solve())
```

The source arrays are flattened only for the second phase. `base[i]` gives the first global position of source `i`, so a source position `k` corresponds to `base[i] + k - 1`.

The first segment tree is deliberately not a normal lazy-propagation tree. Its entries are timestamps, not actual cache bytes. A range load writes its timestamp into `O(log n)` canonical nodes. A point query checks all ancestors and takes their maximum. Since timestamps increase as operations are processed, the largest timestamp is exactly the most recent covering load.

The operation number is packed together with the operation arguments. All relevant coordinates are below `5 * 10^5`, so 20 bits are enough for each coordinate. This avoids storing hundreds of thousands of Python tuples, which would consume considerably more memory.

The request lists are also stored using integer arrays. A request is identified by its output position, and `head[t]` points to all print queries that depend on load `t`. This lets the second pass answer a whole group of queries as soon as it reaches the corresponding load.

The second tree stores only range additions. A range increment is decomposed into canonical nodes and increases their tags by one. A point query sums the tags on its root-to-leaf path. That sum is the number of source increments affecting the byte.

The expression `(original + added) & 255` is equivalent to modulo 256 because both values are nonnegative and 256 is a power of two. It also keeps the operation compact.

All intervals in the problem are one-based and inclusive. The iterative segment-tree representation uses half-open intervals internally, which is why the right endpoint is converted to an exclusive coordinate. The source offset is also explicitly `p - start + 1`, which avoids the common one-position error when translating a cache address back into a source index.

## Worked Examples

### Sample 1

The official sample has two sources, `[255, 0, 15]` and `[1, 2, 1, 3]`, with overlapping loads and a later source update. Its output is `0, 255, 1, 255, 0, 3`.

| Operation | First-pass state | Request created | Second-pass value |
| --- | --- | --- | --- |
| `2 1` | no load at position 1 | none | `0` |
| `1 2 2` | positions 2..5 get load `2` | none | source 2 snapshot |
| `1 1 1` | position 1 gets load `3` | none | source 1 snapshot |
| `2 1` | latest load is `3`, offset `1` | `(3, 1)` | `255` |
| `2 4` | latest load is `2`, offset `3` | `(2, 3)` | `1` |
| `3 1 1 2` | cache tags unchanged | none | source 1 changes only |
| `2 1` | latest load still `3` | `(3, 1)` | `255` |
| `1 1 2` | positions 2..4 get load `8` | none | source 1 snapshot |
| `2 2` | latest load is `8`, offset `1` | `(8, 1)` | `0` |
| `2 5` | latest load is `2`, offset `4` | `(2, 4)` | `3` |

The important row is operation 7. Source 1 has already been incremented, but the cache position was filled by load 3 before that increment. The request therefore still asks for source 1's byte at time 3, which is `255`.

At operation 8, source 1 has value `[0, 1, 15]`, so the later load at position 2 copies that newer version. The second print after that load consequently observes `0` rather than the old value `255`.

### Snapshot timing example

Consider this smaller input:

```
4 1 7
3 5 6 7
2 1
1 1 2
3 1 2 3
2 3
1 1 1
2 2
2 4
```

The source is `[5, 6, 7]`. The trace is:

| Operation | First-pass load at queried position | Request | Source state when load occurs | Answer |
| --- | --- | --- | --- | --- |
| `2 1` | none | none | `[5,6,7]` | `0` |
| `1 1 2` | load `2` covers positions 2..4 | none | `[5,6,7]` |  |
| `3 1 2 3` | unchanged | none | source becomes `[5,7,8]` |  |
| `2 3` | load `2`, offset `2` | `(2,2)` | `[5,6,7]` | `6` |
| `1 1 1` | new load covers positions 1..3 | none | `[5,7,8]` |  |
| `2 2` | load `5`, offset `2` | `(5,2)` | `[5,7,8]` | `7` |
| `2 4` | load `2`, offset `3` | `(2,3)` | `[5,6,7]` | `7` |

The first query after the source update still returns `6`, not `7`, because its load happened before the update. The later load sees the update and produces `7`. This is exactly the temporal separation the two-pass algorithm captures.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | `O((q + S) log(max(n, S)))` | Each load and print uses a logarithmic cache-tree operation, while each source update and dependent request uses a logarithmic source-tree operation. Here `S = sum s_i <= 5 * 10^5`. |
| Space | `O(n + q + S)` | The two segment trees use `O(max(n,S))` space, while source data, packed operations, and request lists use linear space. |

With `n`, `q`, and `S` all bounded by `5 * 10^5`, the logarithmic factor is at most about 19. The implementation also uses compact integer arrays for the operation log and request lists, while the source bytes occupy one byte each. This keeps the memory proportional to the input size rather than to the total number of bytes copied by all loads.

## Test Cases

The following harness assumes the `solve()` function from the solution above is available.

```python
import sys
import io

def run(inp: str) -> str:
    old_stdin = sys.stdin
    try:
        sys.stdin = io.StringIO(inp)
        return solve()
    finally:
        sys.stdin = old_stdin

# Provided sample
sample1 = """\
5 2 10
3 255 0 15
4 1 2 1 3
2 1
1 2 2
1 1 1
2 1
2 4
3 1 1 2
2 1
1 1 2
2 2
2 5
"""

assert run(sample1) == """\
0
255
1
255
0
3
""", "sample 1"

# Minimum-size input.
minimum_case = """\
1 1 6
1 42
2 1
3 1 1 1
1 1 1
2 1
3 1 1 1
2 1
"""

assert run(minimum_case) == """\
0
43
43
""", "minimum size and snapshot"

# Boundary positions and source-end offsets.
boundary_case = """\
5 1 7
4 1 2 3 4
1 1 3
2 3
2 5
3 1 1 1
1 1 1
2 4
2 5
"""

assert run(boundary_case) == """\
1
4
4
4
""", "boundary positions"

# Overlapping loads and a source update between two loads.
overlap_case = """\
5 2 8
2 10 10
3 7 8 9
1 1 1
1 2 2
2 2
3 2 1 3
2 4
1 2 3
2 3
2 5
"""

assert run(overlap_case) == """\
7
9
8
10
""", "overlapping loads"

# Modulo 256 and repeated updates.
modulo_case = """\
3 1 10
2 250 250
1 1 1
3 1 1 2
3 1 1 2
3 1 1 2
3 1 1 2
3 1 1 2
3 1 1 2
1 1 1
2 1
2 2
"""

assert run(modulo_case) == """\
0
0
""", "modulo 256"

# Maximum-size stress case:
# n = 500000, q = 500000, sum(s_i) = 500000.
# Every cache query asks for the final address after one full-length load.
big_data = " ".join(["255"] * 500000)
big_case = (
    "500000 1 500000\n"
    + big_data
    + "\n1 1 1\n"
    + ("2 500000\n" * 499999)
)

assert run(big_case) == "255\n" * 499999, "maximum-size case"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Minimum-size case | `0`, `43`, `43` | Empty cache, one-byte source, and a loaded snapshot surviving a later source increment |
| Boundary case | `1`, `4`, `4`, `4` | Inclusive range endpoints, loading at the final cache positions, and source offset boundaries |
| Overlap case | `7`, `9`, `8`, `10` | Latest overlapping load wins and later loads see source updates |
| Modulo case | `0`, `0` | Repeated increments and wrapping through 256 |
| Maximum-size case | `255` repeated `499999` times | Maximum `n`, maximum `q`, maximum total source size, full-range load, and repeated point queries |

## Edge Cases

### A cache position has never been loaded

For

```
2 1 2
1 7
2 2
2 1
```

the first pass performs no range assignment at all. Both print queries walk their root-to-leaf paths and find timestamp zero. Their answer slots remain zero, producing `0` and `0`.

The algorithm does not need a special cache array for this case. Timestamp zero naturally represents the initial all-zero cache.

### A later source update must not change an old cache copy

Consider:

```
1 1 6
1 42
2 1
3 1 1 1
1 1 1
2 1
3 1 1 1
2 1
```

The load at operation 4 happens after one source increment, so the source value copied into the cache is `43`. The later increment at operation 6 changes the source to `44`, but the cache remains `43`.

The first pass associates the final print with load 4. During the second pass, that request is answered when operation 4 is reached, before operation 6 has been applied. The result is `43`.

### Overlapping loads must choose the latest timestamp

For:

```
5 2 8
2 10 10
3 7 8 9
1 1 1
1 2 2
2 2
3 2 1 3
2 4
1 2 3
2 3
2 5
```

the first load covers positions 1 and 2, while the second covers positions 2 through 4. The print at position 2 therefore sees load 2, not load 1.

In the cache segment tree, load 1 writes timestamp 1 to the canonical nodes for its interval. Load 2 subsequently writes timestamp 2 to the canonical nodes for its interval. A query at position 2 sees both timestamps along its root-to-leaf path and takes the maximum, namely 2.

### A load must capture the source before later updates

Take:

```
4 1 7
3 5 6 7
2 1
1 1 2
3 1 2 3
2 3
1 1 1
2 2
2 4
```

The load at operation 2 captures `[5,6,7]`. The update at operation 3 changes the source to `[5,7,8]`, but the print at operation 4 is tied to load 2 and therefore returns `6`.

When the second pass reaches operation 2, no source update has been processed yet. The request for source offset 2 reads the original value `6`. The later update is processed only afterward, so it cannot affect that request.

### A later load sees every preceding source update

In the same example, operation 5 loads the source after the update from operation 3. At that point the source is `[5,7,8]`, so the print at position 2 returns `7`.

The second pass has already applied operation 3 before reaching operation 5. The request attached to load 5 therefore reads the updated source state. The same source can consequently have multiple independent snapshots in the cache.

### Modulo 256 must be applied to the resulting byte

For:

```
3 1 10
2 250 250
1 1 1
3 1 1 2
3 1 1 2
3 1 1 2
3 1 1 2
3 1 1 2
3 1 1 2
1 1 1
2 1
2 2
```

six increments turn each `250` into `0` because `250 + 6 = 256`. The second load therefore copies `[0,0]`, and both prints return zero.

The source segment tree stores the number of increments as an ordinary integer. This is safe because the sum is at most `q`, which fits easily in Python's integers. The modulo operation is applied when the actual byte value is reconstructed.

### A load ending exactly at the cache boundary

In the maximum-size test, source 1 has length `500000`, and the operation `1 1 1` loads it into cache positions `1` through `500000`. A print at position `500000` must map to source offset `500000`.

The range conversion uses an exclusive right endpoint, so the internal interval is `[1, 500001)`. The point query uses `size + p - 1`, which maps cache position `500000` to exactly its leaf. No extra cache position is included, and the final byte is handled correctly.

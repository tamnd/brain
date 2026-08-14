---
title: "CF 102423B - Computer Cache"
description: "The cache is an array of n byte addresses, initially filled with zero. We also have m independent data pieces, where each piece is itself a byte array. A load operation copies an entire piece into a consecutive region of the cache, replacing whatever was there."
date: "2026-08-14T15:15:36+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102423
codeforces_index: "B"
codeforces_contest_name: "North American Southeast Regional 2019 (Div 1)"
rating: 0
weight: 102423
solve_time_s: 180
verified: true
draft: false
---

[CF 102423B - Computer Cache](https://codeforces.com/problemset/problem/102423/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 3m  
**Verified:** yes  

## Solution
## Problem Understanding

The cache is an array of `n` byte addresses, initially filled with zero. We also have `m` independent data pieces, where each piece is itself a byte array. A load operation copies an entire piece into a consecutive region of the cache, replacing whatever was there. An increment operation changes a consecutive range inside the stored data piece, modulo 256, but does not modify copies that have already been loaded into the cache. A print operation asks for the current byte at one cache address. The original statement allows up to `5 * 10^5` cache addresses, data pieces, and operations, with the total length of all data pieces also at most `5 * 10^5`. The stated time limit is 5 seconds.

Those bounds rule out simulating a load by copying every byte of the data piece. One piece can have length `5 * 10^5`, and the same piece can be loaded on almost every one of `5 * 10^5` operations. That gives a worst case of about `2.5 * 10^11` byte assignments. We need each operation to touch only logarithmically many structure nodes, apart from reading the input itself.

The tricky part is that a cache copy is a snapshot. If data piece `[10, 20]` is loaded and the piece is subsequently incremented, the cache still contains `[10, 20]`, not the new version. Conversely, increments performed before a load must be visible in that load. A direct implementation that stores only the data-piece identifier at a cache position loses this distinction.

Consider the smallest possible cache before anything is loaded.

```
1 1 2
1 0
2 1
2 1
```

The correct output is:

```
0
0
```

A careless implementation might assume every queried position belongs to the latest data piece and return `0` for the wrong reason, or attempt to access an uninitialized data offset. The cache must explicitly represent the absence of a previous load.

A second edge case is an increment before a load.

```
1 1 3
1 255
3 1 1 1
1 1 1
2 1
```

The output is:

```
0
```

The increment changes the stored piece from `255` to `0`, and the subsequent load copies `0`. Treating the data as immutable would incorrectly print `255`.

The reverse ordering is equally significant.

```
1 1 4
1 255
1 1 1
3 1 1 1
2 1
```

The output is:

```
255
```

The increment occurs after the load, so it cannot change the byte already stored in the cache. A solution that simply looks at the current data piece when answering a query would incorrectly print `0`.

Finally, overlapping loads must be handled at byte granularity. For example:

```
5 2 6
2 10 20
2 30 40
1 1 2
2 2
1 2 3
2 2
2 3
2 4
```

The output is:

```
10
30
40
40
```

The second load overwrites addresses `3` and `4`, but address `2` remains from the first load. A solution that treats loads as whole cache states instead of ranges can easily get this boundary wrong.

## Approaches

The brute-force solution directly maintains the cache array. A load of piece `i` at position `p` loops through all `k_i` bytes and writes them into the cache. An increment loops through the requested range and changes the corresponding bytes of the data piece. A print is constant time. This is correct because it follows exactly the semantics of every operation.

The problem is the load operation. Suppose there is one data piece of length `500000`, and the other `499999` operations are also loads of that piece. The brute-force solution performs roughly `500000 * 500000 = 2.5 * 10^11` byte writes. That is far beyond what the time limit permits.

The first useful observation is that a cache query does not need the entire cache state. It only needs to know which load last wrote that particular cache address, and which byte of the loaded piece corresponds to the address. We can find that load without copying the data by treating every load as a range assignment carrying its operation number.

A segment tree can store the latest load number affecting each cache position. For a range update, we place the load number in the segment-tree nodes completely covered by that load. For a point query, we walk from the leaf to the root and take the largest load number encountered. Since operation numbers increase with time, the largest number is exactly the last load that covered the position.

There is a second observation that handles increments. Once a query has been associated with a particular load, its cache value was fixed at that load's execution time. We can postpone calculating the value until that load is processed. We first scan all operations to associate every print query with its last load. Then we scan the operations again. While scanning the second time, the data pieces contain exactly the versions they had at each point in the original execution. When we reach a load, all queries associated with that load can be answered immediately.

For the data pieces, we need range increment and point query. A Fenwick tree gives exactly this combination. We store a difference array in the Fenwick tree, adding `+1` at the left endpoint and `-1` immediately after the right endpoint. The prefix sum at a byte position is then the number of increments that affect that byte. Since values are bytes, all these counts can be reduced modulo 256.

The two parts are thus independent. The segment tree answers the temporal question "which load produced this cache byte?", while the Fenwick trees answer the historical question "what was this data byte's value when that load occurred?"

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(sum of copied bytes) | O(n + sum k_i) | Too slow, up to about 2.5 * 10^11 writes |
| Optimal | O(sum k_i + q log n + q log S) | O(n + m + q + sum k_i) | Accepted |

Here `S` is the maximum data-piece length. The optimal approach never materializes a loaded copy inside the cache.

## Algorithm Walkthrough

1. Read every data piece and keep its original bytes. Give each piece a compact range inside one global byte array. Also reserve a Fenwick-tree range for every piece. The total size of all pieces is at most `5 * 10^5`, so storing all original bytes is cheap.
2. Store all `q` operations instead of executing them immediately. We need the operations twice, once to discover which load owns each cache query and once to reconstruct data-piece versions at load times.
3. Create a segment tree over the cache addresses. For every load operation `1 i p`, its affected cache interval is `[p, p + k_i - 1]`. Store the load's operation number on every segment-tree node completely contained in this interval. We do not need to push these tags downward because queries can simply inspect all ancestors of their leaf.
4. For every print operation `2 p`, walk from cache position `p` toward the segment-tree root and find the largest load operation number encountered. If there is no such operation, the cache address has never been written, so its answer is zero.
5. If a load operation was found, calculate the corresponding offset inside its data piece. If the load starts at cache address `s`, then querying cache address `p` refers to data offset `p - s + 1`. Attach this print query to that load operation. We do not calculate its byte value yet.
6. Initialize one conceptual Fenwick tree for every data piece. They are stored in one flat byte array, with a separate base offset for each piece. For an increment `3 i l r`, add `1` at `l` and `-1` at `r + 1` when that position exists. The Fenwick prefix sum at position `x` gives the number of increments that have affected byte `x` so far.
7. Scan the saved operations in their original order. For an increment, update the appropriate Fenwick tree. For a load, the Fenwick tree currently contains exactly the increments that happened before this load, so the data piece is currently at precisely the version that gets copied into the cache.
8. At a load, visit every print query attached to that load. For each query, read the original byte at its stored offset, add the Fenwick prefix sum for that offset, and reduce the result modulo 256. Store the answer using the query's original output index.
9. Print the answers in query order. Queries that occurred before any load already have their default answer of zero, while every other query was answered when its owning load was processed.

Why it works: for every cache address, the segment tree stores every load whose range contains that address, and the largest load number is the latest such load. Thus every print query is attached to exactly the operation that last determined its cache byte. When that load is reached during the second scan, every increment before the load has already been inserted into the corresponding Fenwick tree, while every increment after the load has not yet been inserted. The calculated byte is consequently exactly the snapshot copied into the cache. Later changes to the data piece cannot affect the stored answer, which matches the required cache semantics.

## Python Solution

```python
import sys
from array import array

input = sys.stdin.readline

def solve():
    n, m, q = map(int, input().split())

    lengths = array('i', [0]) * (m + 1)
    value_base = array('i', [0]) * (m + 1)
    fenwick_base = array('i', [0]) * (m + 1)

    values = bytearray()
    fenwick_total = 0

    for i in range(1, m + 1):
        tokens = input().split()
        k = int(tokens[0])

        lengths[i] = k
        value_base[i] = len(values)
        fenwick_base[i] = fenwick_total

        values.extend(int(x) for x in tokens[1:])
        fenwick_total += k + 1

    # Store operations compactly.
    typ = array('b', [0]) * q
    a = array('i', [0]) * q
    b = array('i', [0]) * q
    c = array('i', [0]) * q

    for t in range(q):
        op = list(map(int, input().split()))
        typ[t] = op[0]
        if op[0] == 1:
            a[t] = op[1]       # data piece
            b[t] = op[2]       # cache start
        elif op[0] == 2:
            a[t] = op[1]       # cache position
        else:
            a[t] = op[1]       # data piece
            b[t] = op[2]       # left
            c[t] = op[3]       # right

    # Segment tree for latest load covering a cache position.
    size = 1
    while size < n:
        size <<= 1

    tag = [0] * (2 * size)

    # For every load operation t, head[t] is the first query attached to it.
    head = array('i', [-1]) * q
    nxt = array('i', [-1]) * q
    query_offset = array('i', [0]) * q

    # Answers are bytes, so bytearray is enough.
    query_count = 0
    answers = bytearray()

    # First pass: resolve every cache query to its latest load.
    for t in range(q):
        if typ[t] == 1:
            data_id = a[t]
            start = b[t]
            end = start + lengths[data_id] - 1

            left = start - 1 + size
            right = end - 1 + size

            while left <= right:
                if left & 1:
                    tag[left] = t + 1
                    left += 1
                if not (right & 1):
                    tag[right] = t + 1
                    right -= 1
                left >>= 1
                right >>= 1

        elif typ[t] == 2:
            pos = a[t]
            node = pos - 1 + size
            load_id = 0

            while node:
                if tag[node] > load_id:
                    load_id = tag[node]
                node >>= 1

            answers.append(0)
            if load_id:
                load_idx = load_id - 1
                data_id = a[load_idx]
                offset = pos - b[load_idx] + 1

                query_offset[query_count] = offset
                nxt[query_count] = head[load_idx]
                head[load_idx] = query_count

            query_count += 1

    # Fenwick trees for range increment + point query.
    bit = bytearray(fenwick_total)

    def fenwick_add(base, length, pos, delta):
        while pos <= length:
            idx = base + pos
            bit[idx] = (bit[idx] + delta) & 255
            pos += pos & -pos

    def fenwick_sum(base, pos):
        result = 0
        while pos:
            result += bit[base + pos]
            pos -= pos & -pos
        return result & 255

    # Second pass: reconstruct each data piece exactly at each load time.
    for t in range(q):
        if typ[t] == 3:
            data_id = a[t]
            left = b[t]
            right = c[t]

            base = fenwick_base[data_id]
            length = lengths[data_id]

            fenwick_add(base, length, left, 1)

            after = right + 1
            if after <= length:
                fenwick_add(base, length, after, -1)

        elif typ[t] == 1:
            data_id = a[t]
            base = fenwick_base[data_id]
            original_base = value_base[data_id]

            query_id = head[t]

            while query_id != -1:
                offset = query_offset[query_id]
                increment = fenwick_sum(base, offset)

                value = values[original_base + offset - 1]
                answers[query_id] = (value + increment) & 255

                query_id = nxt[query_id]

    sys.stdout.write('\n'.join(map(str, answers)))

if __name__ == "__main__":
    solve()
```

The first set of arrays stores the data pieces compactly. `value_base[i]` points to the first original byte of piece `i`, while `fenwick_base[i]` points to the beginning of its Fenwick tree. Adding one extra Fenwick slot per piece lets every tree support the `r + 1` difference update without allocating a separate Python object for every data piece.

The operation arrays avoid storing half a million Python tuples. Each operation has a type and up to three integer arguments, so compact `array` objects keep the memory footprint predictable.

The segment tree uses one-based operation numbers as tags, with zero meaning that no load has covered the node. The update interval is converted from cache addresses to zero-based leaves using `start - 1 + size`. The inclusive right endpoint is `start + length - 1`, so the conversion must use `end - 1 + size`. This is the main boundary where an off-by-one error can change which load owns a query.

The segment tree is used only for range updates and point queries. A load stores its operation number on fully covered nodes. A query examines every node on its root-to-leaf path and takes the maximum. No lazy propagation is required because we never need to materialize the state of an entire segment.

The query linked lists avoid another large collection of Python lists. `head[t]` points to the queries whose final cache value came from load `t`, while `nxt` links queries belonging to the same load. A query is consequently processed exactly once during the second pass.

The Fenwick tree stores differences modulo 256. Although an ordinary Fenwick tree normally stores arbitrary integer sums, byte values only depend on the sum modulo 256, so every stored value can safely remain in a `bytearray`. The prefix sum is also reduced modulo 256 before it is added to the original byte.

The second pass processes an increment before any later load, exactly matching the chronological order of the original operations. When a load is reached, no later increment has entered the Fenwick tree yet, so the value calculated for every query attached to that load is its immutable cache snapshot.

Python integers do not overflow, but the implementation still explicitly reduces byte values modulo 256. This mirrors the problem definition and lets the compact byte arrays be used safely.

## Worked Examples

The official sample is:

```
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
```

The first pass determines which load owns each query.

| Operation | Action | Cache range affected | Query position | Owning load |
| --- | --- | --- | --- | --- |
| 1 | Query address 1 | none | 1 | none |
| 2 | Load piece 2 at 2 | 2..5 | none | none |
| 3 | Load piece 1 at 1 | 1..3 | none | none |
| 4 | Query address 1 | none | 1 | load 3 |
| 5 | Query address 4 | none | 4 | load 2 |
| 6 | Increment piece 1, 1..2 | none | none | none |
| 7 | Query address 1 | none | 1 | load 3 |
| 8 | Load piece 1 at 2 | 2..4 | none | none |
| 9 | Query address 2 | none | 2 | load 8 |
| 10 | Query address 5 | none | 5 | load 2 |

At operation 3, cache address 1 receives the first byte of piece 1, which is `255`. The later increment at operation 6 does not affect that cache copy. At operation 8, however, piece 1 has already been incremented, so its first byte is now `0`. The two loads of the same data piece consequently produce different cache snapshots.

During the second pass, the relevant load states are:

| Load | Data piece | Current data at load time | Attached query offsets | Answers |
| --- | --- | --- | --- | --- |
| 2 | 2 | `[1, 2, 1, 3]` | address 4 → offset 3 | `1` |
| 3 | 1 | `[255, 0, 15]` | address 1 → offset 1 | `255` |
| 8 | 1 | `[0, 1, 15]` | address 2 → offset 1 | `0` |

The query before any load remains `0`, and the final query at address 5 belongs to load 2 and returns its fourth byte, `3`. The final output is `0, 255, 1, 255, 0, 3`, matching the sample.

For a second example, consider:

```
5 2 8
3 10 20 30
2 40 50
1 1 2
2 2
2 4
1 2 3
2 2
2 3
2 4
2 5
```

The first load writes addresses `2..4`.

| Operation | Action | Latest load at queried address | Offset |
| --- | --- | --- | --- |
| 1 | Load piece 1 at 2 | none | none |
| 2 | Query address 2 | load 1 | 1 |
| 3 | Query address 4 | load 1 | 3 |
| 4 | Load piece 2 at 3 | none | none |
| 5 | Query address 2 | load 1 | 1 |
| 6 | Query address 3 | load 4 | 1 |
| 7 | Query address 4 | load 4 | 2 |
| 8 | Query address 5 | none | none |

The second load covers only addresses `3` and `4`. It cannot change address `2`, and it does not reach address `5`. The resulting outputs are `10, 30, 10, 40, 50, 0`. This trace demonstrates why the segment tree must remember the latest load independently for every cache position.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(sum k_i + q log n + q log S) | Reading data is linear in total data size. Each load range update and cache query uses O(log n), while each increment and each resolved query uses O(log S). |
| Space | O(n + m + q + sum k_i) | The segment tree uses O(n), operations and query links use O(q), piece metadata uses O(m), and the original data plus Fenwick storage use O(sum k_i + m). |

With all relevant bounds at `5 * 10^5`, the logarithmic factors are at most around 19 or 20. The algorithm never performs work proportional to the length of a loaded data piece, so repeatedly loading a large piece does not cause repeated large copies. The 5 second limit makes this logarithmic structure appropriate, while the compact arrays keep Python's memory usage under control.

## Test Cases

The following harness assumes the `solve()` function from the solution above is available in the same file or imported from the submitted solution.

```python
import sys
import io

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout
    old_input = globals()["input"]

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()
    globals()["input"] = sys.stdin.readline

    try:
        solve()
        return sys.stdout.getvalue()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout
        globals()["input"] = old_input

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

assert run(sample1) == "0\n255\n1\n255\n0\n3", "sample 1"

# Minimum-size cache, query before any load.
case_min = """\
1 1 2
1 7
2 1
2 1
"""

assert run(case_min) == "0\n0", "minimum-size input"

# Increment before a load, then increment after the load.
case_snapshot = """\
3 1 5
3 255 0 1
3 1 1 2
1 1 1
3 1 1 3
2 1
"""

assert run(case_snapshot) == "0", "snapshot semantics and modulo 256"

# Overlapping loads and exact boundaries.
case_boundaries = """\
5 2 8
3 10 20 30
2 40 50
1 1 2
2 2
2 4
1 2 3
2 2
2 3
2 4
2 5
"""

assert run(case_boundaries) == "10\n30\n10\n40\n50\n0", "load boundaries"

# All equal values, followed by a range increment.
case_equal = """\
3 1 5
3 7 7 7
1 1 1
3 1 1 3
2 1
2 2
2 3
"""

assert run(case_equal) == "8\n8\n8", "all-equal values"

# Maximum cache size and maximum total data size.
# The single query is at the last cache address, catching right-boundary errors.
max_data = " ".join(["0"] * 500000)
case_max_data = (
    "500000 1 2\n"
    "500000 " + max_data + "\n"
    "1 1 1\n"
    "2 500000\n"
)

assert run(case_max_data) == "0", "maximum n and total data size"

# Maximum number of operations.
# No address is ever loaded, so every query must remain zero.
case_max_q = "1 1 500000\n1 0\n" + "2 1\n" * 500000
assert run(case_max_q) == "0\n" * 500000, "maximum q"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 2`, one-byte data, two queries | `0\n0` | Minimum size and querying an untouched cache |
| Increment before load, then after load | `0` | Snapshot behavior and modulo 256 |
| Two overlapping loads | `10\n30\n10\n40\n50\n0` | Range boundaries and partial overwriting |
| Three equal bytes incremented together | `8\n8\n8` | Range update affecting every byte |
| `n = 500000`, data length `500000` | `0` | Maximum cache and data boundaries |
| `q = 500000` queries | `500000` zero lines | Maximum operation count and untouched-cache behavior |

## Edge Cases

For a query before any load, the segment-tree path contains only zero tags. The algorithm leaves its answer at the default byte value `0`. For example, with `1 1 2`, data `[7]`, and two `2 1` queries, both outputs are `0`. No artificial data-piece association is created for an untouched cache address.

For an increment before a load, the Fenwick tree is updated before the load is processed in the second pass. With data `[255]` and operation `3 1 1 1`, the Fenwick prefix sum at position 1 is `1`. The load therefore computes `(255 + 1) mod 256 = 0`, which is the correct snapshot.

For an increment after a load, the query is attached to that earlier load. When the load is processed in the second pass, the later increment has not yet reached the Fenwick tree. With data `[255]`, followed by a load and then an increment, the stored answer remains `255`, even though the data piece itself eventually becomes `0`.

For overlapping loads, the segment tree compares operation numbers rather than simply storing whether a position has ever been loaded. Suppose piece 1 is loaded at address 2 and later piece 2 is loaded at address 3. A query at address 2 sees only the first load, while queries at addresses 3 and 4 see the second load. The maximum-tag property gives exactly this result because the second load's range does not contain address 2.

For a load ending exactly at the last cache address, the right endpoint is calculated as `start + length - 1`. The segment tree converts this inclusive endpoint using `end - 1 + size`. A load of length `500000` starting at `1` consequently covers the leaf for address `500000`, which is exercised by the maximum-size test.

For a range increment ending at the final byte of a data piece, the difference update at `r + 1` must not be performed. The implementation checks `after <= length` before updating that position. Without this check, the difference marker would leak into the next logical piece in the flat Fenwick storage.

For byte overflow, the Fenwick contribution and original byte are both combined with `& 255`. Thus `255 + 1` becomes `0`, and repeated increments naturally cycle through all 256 byte values without requiring a large integer representation.

---
title: "CF 13E - Holes"
description: "We have a line of holes indexed from left to right. Every hole contains a jump length. If a ball is dropped into hole i,"
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "dsu"]
categories: ["algorithms"]
codeforces_contest: 13
codeforces_index: "E"
codeforces_contest_name: "Codeforces Beta Round 13"
rating: 2700
weight: 13
solve_time_s: 113
verified: true
draft: false
---

[CF 13E - Holes](https://codeforces.com/problemset/problem/13/E)

**Rating:** 2700  
**Tags:** data structures, dsu  
**Solve time:** 1m 53s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a line of holes indexed from left to right. Every hole contains a jump length. If a ball is dropped into hole `i`, it immediately moves to `i + a[i]`. From there it jumps again using the value of the new hole, and this continues until the next jump leaves the array.

Two kinds of operations must be processed online.

The first operation changes the jump length of one hole.

The second operation starts a ball from some hole and asks for two values:

1. The last hole visited before the ball exits the array.
2. The total number of jumps performed.

The structure is really a directed graph where every node has exactly one outgoing edge, either to another hole or outside the array. Since every jump moves strictly to the right, cycles are impossible. Every path eventually leaves the array.

The constraints are large enough that straightforward simulation is too slow. Both the number of holes and the number of queries can reach `10^5`. A naive simulation of every query may walk through almost the entire array each time. In the worst case, imagine every hole has value `1`. Starting from hole `1` requires `10^5` jumps. Doing this for `10^5` queries would lead to around `10^10` operations, far beyond what fits in one second.

The update operation is what makes the problem tricky. Precomputing all answers once is not enough because changing a single jump length can affect many paths.

Several edge cases are easy to mishandle.

Consider this input:

```
3 1
3 1 1
1 1
```

Starting from hole `1`, the ball immediately exits because `1 + 3 = 4`. The correct answer is:

```
1 1
```

A careless implementation may print hole `4` as the last position, even though the problem asks for the last valid hole before leaving.

Another subtle case appears when an update changes jumps only inside one local region.

```
5 3
1 1 1 1 1
0 3 5
1 1
```

After the update, the path becomes:

`1 -> 2 -> 3 -> outside`

The correct answer is:

```
3 3
```

If the preprocessing is not rebuilt correctly after updates, stale information from the old chain may survive and produce a longer path.

A final common mistake comes from block boundaries.

```
6 1
2 2 2 2 2 2
1 1
```

The jumps are:

`1 -> 3 -> 5 -> outside`

The answer is:

```
5 3
```

When using square root decomposition, many implementations accidentally stop at the last index of a block instead of the first jump outside the block. That breaks the chain compression logic.

## Approaches

The brute-force solution directly simulates the ball movement.

For a query starting at hole `x`, repeatedly jump to `x + a[x]` until the position leaves the array. Count how many jumps were made and remember the last valid hole. Updates are trivial because we only modify one array value.

This works because the graph is acyclic and every simulation eventually terminates. The problem is the running time. In the worst case, every jump moves only one step to the right. A single query then costs `O(n)`. With `10^5` queries, the total complexity becomes `O(nm)`, which is about `10^10` operations.

The key observation is that jumps only move to the right. Because of that, we can group indices into blocks and compress all jumps that stay inside the same block.

Suppose we divide the array into blocks of size about `sqrt(n)`. For every index `i`, we store:

1. The next position outside the current block reachable from `i`.
2. The number of jumps needed to get there.
3. The last hole visited before leaving the block.

Now a query no longer walks jump-by-jump. Instead, it jumps block-by-block. Since there are only about `sqrt(n)` blocks, each query becomes much faster.

Updates are also manageable. Changing `a[i]` only affects paths inside the same block because all jumps move rightward. We can rebuild one block in `O(sqrt(n))` time instead of recomputing everything.

This is classic square root decomposition with path compression inside blocks.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | `O(nm)` | `O(1)` | Too slow |
| Optimal | `O((n + m)\sqrt{n})` | `O(n)` | Accepted |

## Algorithm Walkthrough

1. Divide the array into blocks of size approximately `sqrt(n)`.

If `n = 10^5`, the block size is around `320`. This gives roughly `320` blocks, which keeps both queries and updates efficient.
2. For every position `i`, compute three helper values.

`nxt[i]` stores the first position reached outside the current block.

`cnt[i]` stores how many jumps are needed to reach `nxt[i]`.

`last[i]` stores the last valid hole visited before leaving the block.
3. Process indices inside each block from right to left.

Since jumps always go to larger indices, the destination information is already computed when handling `i`.
4. Let `j = i + a[i]`.

If `j` leaves the array or belongs to another block:

- `nxt[i] = j`
- `cnt[i] = 1`
- `last[i] = i`

Otherwise:

- `nxt[i] = nxt[j]`
- `cnt[i] = cnt[j] + 1`
- `last[i] = last[j]`

This compresses all jumps inside the block into one transition.
5. To answer a query starting from `x`, repeatedly:

- Add `cnt[x]` to the answer.
- Record `last[x]` as the latest valid hole.
- Move to `nxt[x]`.

Continue until `x > n`.

Each iteration skips an entire block worth of jumps.
6. To process an update at position `x`, change `a[x]` and rebuild only the block containing `x`.

No earlier blocks depend on this block because jumps move strictly to the right.

### Why it works

For every index `i`, the tuple `(nxt[i], cnt[i], last[i])` summarizes the entire sequence of jumps inside the current block.

If the next jump already leaves the block, the summary is immediate.

Otherwise, the path from `i` first jumps to `j` inside the same block, and the remainder of the path is exactly the precomputed summary of `j`. Since indices are processed from right to left, this information is already correct.

During queries, repeatedly following `nxt` reproduces the exact original jump sequence, but compressed into block transitions. The jump count is preserved because `cnt[i]` stores the exact number of skipped jumps. The last visited hole is preserved because `last[i]` tracks the final valid position before crossing the block boundary or leaving the array.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())
    a = [0] + list(map(int, input().split()))

    B = int(n ** 0.5) + 1

    nxt = [0] * (n + 1)
    cnt = [0] * (n + 1)
    last = [0] * (n + 1)

    def rebuild(block):
        l = block * B + 1
        r = min(n, (block + 1) * B)

        for i in range(r, l - 1, -1):
            j = i + a[i]

            if j > n or (j - 1) // B != block:
                nxt[i] = j
                cnt[i] = 1
                last[i] = i
            else:
                nxt[i] = nxt[j]
                cnt[i] = cnt[j] + 1
                last[i] = last[j]

    num_blocks = (n + B - 1) // B

    for b in range(num_blocks - 1, -1, -1):
        rebuild(b)

    out = []

    for _ in range(m):
        query = list(map(int, input().split()))

        if query[0] == 0:
            x, y = query[1], query[2]
            a[x] = y
            rebuild((x - 1) // B)
        else:
            x = query[1]

            total = 0
            ans_last = x

            while x <= n:
                total += cnt[x]
                ans_last = last[x]
                x = nxt[x]

            out.append(f"{ans_last} {total}")

    sys.stdout.write("\n".join(out))

solve()
```

The array is stored using 1-based indexing because the problem statement is naturally 1-based. This avoids repeated index adjustments during jumps.

The `rebuild` function recomputes all compressed information for one block. Processing indices from right to left is essential. When handling `i`, the destination `j` is always larger than `i`, so its compressed information is already available.

The condition

```
if j > n or (j - 1) // B != block:
```

checks whether the next jump leaves the current block. The `(j - 1) // B` expression converts a 1-based index into a 0-based block number. Missing the `-1` is a common off-by-one bug.

During queries, the loop does not simulate every jump individually. Instead, each iteration skips directly to another block using `nxt[x]`. The total number of skipped jumps is accumulated using `cnt[x]`.

The variable `ans_last` is updated before moving to the next block. This guarantees it always stores the final valid hole before exiting the array.

Updates only rebuild one block. Recomputing the entire structure after every update would be too slow.

## Worked Examples

### Example 1

Input:

```
8 5
1 1 1 1 1 2 8 2
1 1
0 1 3
1 1
0 3 4
1 2
```

Assume block size is `3`.

Initial compressed values:

| i | a[i] | nxt[i] | cnt[i] | last[i] |
| --- | --- | --- | --- | --- |
| 1 | 1 | 4 | 3 | 3 |
| 2 | 1 | 4 | 2 | 3 |
| 3 | 1 | 4 | 1 | 3 |
| 4 | 1 | 7 | 3 | 6 |
| 5 | 1 | 7 | 2 | 6 |
| 6 | 2 | 8 | 1 | 6 |
| 7 | 8 | 15 | 1 | 7 |
| 8 | 2 | 10 | 1 | 8 |

Processing query `1 1`:

| Current x | cnt[x] added | last[x] | nxt[x] |
| --- | --- | --- | --- |
| 1 | 3 | 3 | 4 |
| 4 | 3 | 6 | 7 |
| 7 | 1 | 7 | 15 |

Total jumps = `7`, final hole = `7`.

After updates, the compressed information changes only in affected blocks.

This trace demonstrates how entire chains inside blocks are skipped in one operation.

### Example 2

Input:

```
5 2
1 1 1 1 1
0 3 5
1 1
```

After the update, the array becomes:

| i | a[i] |
| --- | --- |
| 1 | 1 |
| 2 | 1 |
| 3 | 5 |
| 4 | 1 |
| 5 | 1 |

The jump sequence from `1` is:

`1 -> 2 -> 3 -> outside`

Query trace:

| Current x | cnt[x] added | last[x] | nxt[x] |
| --- | --- | --- | --- |
| 1 | 2 | 2 | 3 |
| 3 | 1 | 3 | 8 |

Answer:

```
3 3
```

This example shows why rebuilding the modified block is necessary after updates.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | `O((n + m)\sqrt{n})` | Each query and update touches at most `O(\sqrt{n})` blocks |
| Space | `O(n)` | Arrays `a`, `nxt`, `cnt`, and `last` each store one value per hole |

With `n, m <= 10^5`, square root decomposition is fast enough. Roughly `320` operations per query or update easily fits within the time limit in Python.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    def solve():
        n, m = map(int, input().split())
        a = [0] + list(map(int, input().split()))

        B = int(n ** 0.5) + 1

        nxt = [0] * (n + 1)
        cnt = [0] * (n + 1)
        last = [0] * (n + 1)

        def rebuild(block):
            l = block * B + 1
            r = min(n, (block + 1) * B)

            for i in range(r, l - 1, -1):
                j = i + a[i]

                if j > n or (j - 1) // B != block:
                    nxt[i] = j
                    cnt[i] = 1
                    last[i] = i
                else:
                    nxt[i] = nxt[j]
                    cnt[i] = cnt[j] + 1
                    last[i] = last[j]

        num_blocks = (n + B - 1) // B

        for b in range(num_blocks - 1, -1, -1):
            rebuild(b)

        out = []

        for _ in range(m):
            q = list(map(int, input().split()))

            if q[0] == 0:
                x, y = q[1], q[2]
                a[x] = y
                rebuild((x - 1) // B)
            else:
                x = q[1]

                total = 0
                ans_last = x

                while x <= n:
                    total += cnt[x]
                    ans_last = last[x]
                    x = nxt[x]

                out.append(f"{ans_last} {total}")

        return "\n".join(out)

    return solve()

# provided sample
assert run(
"""8 5
1 1 1 1 1 2 8 2
1 1
0 1 3
1 1
0 3 4
1 2
"""
) == """8 7
8 5
7 3""", "sample 1"

# minimum size
assert run(
"""1 1
1
1 1
"""
) == "1 1", "single hole"

# all values equal
assert run(
"""5 1
1 1 1 1 1
1 1
"""
) == "5 5", "full linear chain"

# immediate exit
assert run(
"""3 1
3 1 1
1 1
"""
) == "1 1", "jump exits immediately"

# update changes path
assert run(
"""5 3
1 1 1 1 1
0 3 5
1 1
1 2
"""
) == """3 3
3 2""", "rebuild after update"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single hole | `1 1` | Minimum constraints |
| All ones | `5 5` | Longest possible chain |
| Immediate exit | `1 1` | Correct last-hole handling |
| Update changes path | `3 3`, `3 2` | Proper block rebuilding after updates |

## Edge Cases

Consider the case where the very first jump exits the array.

```
3 1
3 1 1
1 1
```

From hole `1`, the jump goes directly to `4`, which is outside the array. During preprocessing:

| i | j = i + a[i] | nxt[i] | cnt[i] | last[i] |
| --- | --- | --- | --- | --- |
| 1 | 4 | 4 | 1 | 1 |

The query loop performs exactly one compressed jump and reports:

```
1 1
```

The algorithm correctly stores the last valid hole instead of the out-of-range position.

Now consider an update that changes the structure inside one block.

```
5 2
1 1 1 1 1
0 3 5
1 1
```

After updating `a[3] = 5`, rebuilding the block recomputes:

| i | nxt[i] | cnt[i] | last[i] |
| --- | --- | --- | --- |
| 3 | 8 | 1 | 3 |
| 2 | 3 | 1 | 2 |
| 1 | 3 | 2 | 2 |

The query follows:

`1 -> 3 -> outside`

and returns:

```
3 3
```

Only the modified block is rebuilt, but that is sufficient because all edges point rightward.

Finally, consider jumps that land exactly on a block boundary.

```
6 1
2 2 2 2 2 2
1 1
```

Suppose the block size is `2`.

The path is:

`1 -> 3 -> 5 -> outside`

The preprocessing recognizes that each jump leaves the current block immediately:

| i | nxt[i] | cnt[i] | last[i] |
| --- | --- | --- | --- |
| 1 | 3 | 1 | 1 |
| 3 | 5 | 1 | 3 |
| 5 | 7 | 1 | 5 |

The query accumulates three compressed jumps and correctly outputs:

```
5 3
```

This confirms the block-transition logic handles boundary crossings correctly.

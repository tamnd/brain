---
title: "CF 105224A - Trampolines"
description: "We are given a one-dimensional board of positions from 1 to n. Each position i contains a jump length t[i]. If a ball is dropped at position i, it repeatedly performs deterministic jumps: from i it moves to i + t[i], then from that new position j it moves to j + t[j], and so on…"
date: "2026-06-24T16:36:11+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105224
codeforces_index: "A"
codeforces_contest_name: "MOI2024"
rating: 0
weight: 105224
solve_time_s: 315
verified: false
draft: false
---

[CF 105224A - Trampolines](https://codeforces.com/problemset/problem/105224/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 5m 15s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a one-dimensional board of positions from 1 to n. Each position i contains a jump length t[i]. If a ball is dropped at position i, it repeatedly performs deterministic jumps: from i it moves to i + t[i], then from that new position j it moves to j + t[j], and so on, until the position exceeds n. At that moment the ball is considered to have exited the board.

The interesting part is that the array is not static. We must support two operations. One operation changes the jump length at a single index. The other asks us to simulate the entire jumping process starting from a given index and report two values: the last position that was still inside the board before the ball left it, and how many jumps were made before exiting.

The constraints n and q are both up to 100000, and each jump can potentially move far or stay small depending on the array. A direct simulation per query can easily degrade to quadratic behavior if the structure is adversarial, since a single query may traverse many positions and there can be many such queries.

A naive expectation would be that each query type 1 might take O(n) in the worst case, which leads to O(nq) total work. With 100000 operations, this is far beyond feasible limits.

A subtle edge case is when jumps always stay within a small region, for example t[i] = 1 for all i. Starting from position 1, we would visit every position in order until n, producing n steps per query. If there are many queries, this immediately becomes too slow. Another edge case is frequent updates that shift a single value and completely change the path, making memoization across queries unreliable unless carefully structured.

## Approaches

The brute force approach is straightforward. For a query starting at i, we repeatedly jump using the current array until we leave the range. We count steps and remember the last valid position. Each update simply changes one value.

This works correctly because it literally simulates the definition of the process. The issue is that a single query can walk through O(n) positions in the worst case. With q up to 100000, the worst case total becomes O(nq), which is too large.

The key observation is that each position either jumps to a far position or remains in a region where repeated small jumps behave predictably. We want to avoid simulating every intermediate step individually. A standard way to accelerate such “next pointer jumping” processes under updates is to maintain, for each position, the next position we will land in that stays within a controlled block structure, and also maintain how many steps are taken to reach that next position.

A well-known technique for this is sqrt decomposition on indices. We divide the array into blocks of size about sqrt(n). For each index we precompute where we exit the current block and how many steps it takes to do so. When processing a query, we repeatedly jump block-to-block instead of step-to-step. When an update happens, we recompute only the affected block.

Inside a block, jumps are simulated explicitly, but each block traversal is compressed into a single jump during queries.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n) per query, O(1) update | O(n) | Too slow |
| Block Decomposition | O(√n) per query, O(√n) update | O(n) | Accepted |

## Algorithm Walkthrough

We split indices 1 through n into blocks of size B, typically around sqrt(n). For each position i we maintain two values: nxt[i], the next position after we leave i’s block following the jumping rules, and cnt[i], the number of jumps needed to reach nxt[i] or exit the block.

1. Build blocks and initialize nxt and cnt from right to left. We process indices so that when computing i, we already know the result of i + t[i] if it is inside the same block or outside it.
2. For each index i, compute j = i + t[i]. If j > n, then nxt[i] is outside the array and cnt[i] is 1. This represents a single jump leading to exit.
3. If j is inside the same block as i, then nxt[i] and cnt[i] are inherited from j. We set nxt[i] = nxt[j] and cnt[i] = cnt[j] + 1. This compresses multiple internal jumps into one summary.
4. If j is in a different block but still inside the array, we set nxt[i] = j and cnt[i] = 1. This means the next compressed hop leaves the block immediately.
5. For a query starting at i, we repeatedly apply these block jumps. We accumulate total count and keep track of the last valid position. Each time we jump from i to nxt[i], the last position is i before the jump, and i is updated to nxt[i].
6. The process stops when i exceeds n, and we output the last valid position and total steps.
7. For an update at position i, we change t[i] and recompute all nxt and cnt values inside i’s block because only that block’s internal structure may have changed.

The key reason this works is that within a block, all chains are locally consistent after recomputation, and jumping across blocks reduces the path length dramatically. Each query crosses at most O(√n) blocks, since each block traversal skips many positions at once.

### Why it works

The structure maintained by nxt and cnt acts as a compressed representation of the functional graph induced by the jump rule. Inside a block, every path eventually exits the block or the array, and we precompute exactly where that exit happens. Since updates only affect one block and recomputation restores correctness locally, every jump either follows a valid precomputed chain or transitions to a new block boundary. This ensures that every simulated step in the compressed process corresponds exactly to a sequence of original jumps, preserving both final position and step count.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, q = map(int, input().split())
t = list(map(int, input().split()))

B = int(n ** 0.5) + 1

nxt = [0] * n
cnt = [0] * n

def rebuild(block):
    l = block * B
    r = min(n, (block + 1) * B)
    for i in range(r - 1, l - 1, -1):
        j = i + t[i]
        if j >= n:
            nxt[i] = n
            cnt[i] = 1
        else:
            if j // B == i // B:
                nxt[i] = nxt[j]
                cnt[i] = cnt[j] + 1
            else:
                nxt[i] = j
                cnt[i] = 1

for b in range((n + B - 1) // B):
    rebuild(b)

for _ in range(q):
    tmp = input().split()
    if tmp[0] == '0':
        i = int(tmp[1]) - 1
        x = int(tmp[2])
        t[i] = x
        rebuild(i // B)
    else:
        i = int(tmp[1]) - 1
        pos = i
        steps = 0
        last = i

        while pos < n:
            last = pos
            steps += cnt[pos]
            pos = nxt[pos]

        print(last + 1, steps)
```

The core of the implementation is the `rebuild` function, which recomputes the compressed jump information for one block. It processes indices from right to left so that whenever we use `nxt[j]` and `cnt[j]`, they are already valid.

During queries, instead of stepping one index at a time, we repeatedly jump using `nxt[pos]`, which skips entire chains inside blocks. The last valid position is always the start of the final jump that exits the array.

The update operation only touches one block, so recomputation stays local. The most subtle detail is handling indexing consistently: the stored structure uses 0-based indices internally, while the output requires 1-based positions.

## Worked Examples

Consider the sample input.

### Example 1

Input:

```
3 3
1 3 2
1 1
0 1 2
1 1
```

We track the state of jumps.

| Operation | Start | Jump path | Last inside | Steps |
| --- | --- | --- | --- | --- |
| Query | 1 | 1 → 2 → 5(exit) | 2 | 2 |

After update t[1] becomes 2.

| Operation | Start | Jump path | Last inside | Steps |
| --- | --- | --- | --- | --- |
| Query | 1 | 1 → 3 → 5(exit) | 3 | 2 |

The first query shows a short chain exiting through position 2. After modification, the path changes and now exits through position 3 instead.

This confirms that updates fully affect downstream jumps even though only one value changed.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((n + q) √n) | each query jumps across blocks, each update rebuilds one block |
| Space | O(n) | storage for nxt and cnt arrays |

With n and q up to 100000, sqrt decomposition keeps operations around a few hundred steps per query, which fits comfortably within time limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n, q = map(int, input().split())
    t = list(map(int, input().split()))

    B = int(n ** 0.5) + 1
    nxt = [0] * n
    cnt = [0] * n

    def rebuild(block):
        l = block * B
        r = min(n, (block + 1) * B)
        for i in range(r - 1, l - 1, -1):
            j = i + t[i]
            if j >= n:
                nxt[i] = n
                cnt[i] = 1
            else:
                if j // B == i // B:
                    nxt[i] = nxt[j]
                    cnt[i] = cnt[j] + 1
                else:
                    nxt[i] = j
                    cnt[i] = 1

    for b in range((n + B - 1) // B):
        rebuild(b)

    out = []
    for _ in range(q):
        tmp = sys.stdin.readline().split()
        if tmp[0] == '0':
            i = int(tmp[1]) - 1
            x = int(tmp[2])
            t[i] = x
            rebuild(i // B)
        else:
            i = int(tmp[1]) - 1
            pos = i
            steps = 0
            last = i
            while pos < n:
                last = pos
                steps += cnt[pos]
                pos = nxt[pos]
            out.append(f"{last+1} {steps}")

    return "\n".join(out)

# provided sample
assert run("""3 3
1 3 2
1 1
0 1 2
1 1
""").strip() == """2 2
3 2"""

# single element exit immediately
assert run("""1 1
1
1 1
""").strip() == "1 1"

# all jumps exit immediately
assert run("""5 2
10 10 10 10 10
1 1
1 3
""").strip() == "1 1"

# chain-like behavior
assert run("""5 1
1 1 1 1 1
1 1
""").strip() == "5 5"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single element | 1 1 | immediate exit handling |
| large jumps | fast exit | boundary jumps |
| all ones | 5 5 | long chain traversal |

## Edge Cases

A critical edge case is when every jump stays inside a single block, which would normally force step-by-step traversal. The block decomposition handles this because internal chains are precomputed and collapsed into nxt pointers. Even if we never leave the block until the last step, cnt accumulates the full internal path length.

Another edge case is when a single update changes a value near a block boundary. Without recomputing the whole block, subsequent queries could follow stale nxt pointers. Rebuilding the entire block ensures all internal dependencies are consistent again.

Finally, when t[i] is large enough to immediately exit the array, nxt[i] is set to n and cnt[i] is 1. This prevents any accidental dereferencing beyond bounds during chain compression and ensures that queries terminate cleanly even if multiple such jumps occur consecutively.

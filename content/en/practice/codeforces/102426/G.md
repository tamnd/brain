---
title: "CF 102426G - \u4f19\u4f34\u7cfb\u7edf"
description: "The system maintains free memory only through 11 counters. Counter i stores how many free blocks have size 2^i, where i ranges from 0 through 10."
date: "2026-08-14T15:18:20+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102426
codeforces_index: "G"
codeforces_contest_name: "The 7-th BIT Campus Programming Contest for Junior Grade Group"
rating: 0
weight: 102426
solve_time_s: 125
verified: true
draft: false
---

[CF 102426G - \u4f19\u4f34\u7cfb\u7edf](https://codeforces.com/problemset/problem/102426/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 5s  
**Verified:** yes  

## Solution
## Problem Understanding

The system maintains free memory only through 11 counters. Counter `i` stores how many free blocks have size `2^i`, where `i` ranges from 0 through 10. We never need to remember the physical positions of blocks, because the simplified model explicitly says that free blocks cannot be merged.

A `free n` operation introduces one new free block of size `n`. Since the system only stores powers of two, we represent `n` by its binary decomposition. For example, `13 = 8 + 4 + 1`, so freeing a block of size 13 increases the counters for sizes 8, 4, and 1.

An `allocate m` operation behaves differently. We must find the smallest power-of-two block whose size is at least `m` and whose counter is positive. If that block has size `s`, it is consumed and leaves a remainder of `s - m`. The remainder is treated exactly like a newly freed block, so its binary decomposition is inserted into the counters. If no suitable power-of-two block exists, the operation fails and the state remains unchanged.

The input starts with an integer `k`, followed by `k` operations. After every successful operation, we print all 11 counters from size 1 through size 1024. After a failed allocation, we print `ERROR!` and do not modify the counters.

The sequence can contain up to `10^5` operations. The number of possible block sizes is only 11, which is the key structural restriction. An algorithm that performs a constant amount of work over these 11 sizes per operation is easily fast enough. In contrast, an implementation that scans every possible integer size from 1 through 1024 for every allocation performs about `1024 * 10^5 = 10^8` checks in the worst case, which is unnecessarily expensive in Python and leaves little room for the cost of input and output.

There are several edge cases where a direct implementation can silently go wrong. The first is an allocation whose requested size is already a power of two. For example:

```
3
free 8
allocate 8
allocate 1
```

The correct output is:

```
0 0 0 0 0 0 0 0 0 0 0
ERROR!
```

The block of size 8 is used exactly, so its remainder is zero. A careless implementation that always inserts `s - m` without checking for zero could accidentally treat zero as a block.

A second edge case is an allocation that needs a larger block and leaves a remainder containing several binary components:

```
2
free 16
allocate 13
```

The correct output is:

```
1 1 0 0 0 0 0 0 0 0 0
```

The 16 block is consumed, leaving 3, which decomposes into 2 and 1. An implementation that only records the remainder as one integer would violate the system's representation.

A third edge case is failure even though smaller free blocks collectively have enough total memory:

```
2
free 1
allocate 2
```

The correct output is:

```
1 0 0 0 0 0 0 0 0 0 0
ERROR!
```

The system cannot combine the existing size-1 block into a size-2 block. The counters describe independent blocks, not an aggregate pool of memory.

A fourth edge case occurs when a suitable block exists at a larger power of two while smaller powers exist but are insufficient individually:

```
3
free 1
free 8
allocate 2
```

The correct output is:

```
1 0 1 0 0 0 0 0 0 0 0
```

The size-1 block cannot satisfy the request, so the size-8 block is selected. Its remainder is 6, which becomes 4 and 2. Together with the original size-1 block, the counters become `1 0 1`, corresponding to sizes 1, 2, and 4.

## Approaches

A straightforward implementation can store the 11 counters and, for `free n`, repeatedly find the largest power of two not exceeding the remaining value. Since `n < 2048`, this creates at most 11 pieces. For allocation, the simplest brute-force version can scan every integer size from `m` through 1024 and ask whether a free block of exactly that size exists. Since only powers of two are represented, most of those checks are immediately useless, but the implementation still performs up to 1024 checks for one allocation. With `10^5` operations, the worst case reaches roughly `1024 * 10^5 = 10^8` checks, which is too much for a 1 second contest limit, especially with Python.

The brute-force idea is still useful because it reveals the real state transition. Once a suitable block of size `s` is found, there are only two changes: decrement the counter for `s`, then insert the binary decomposition of `s - m`. Nothing about the history or physical position of a block matters.

The key observation is that the system has only 11 possible block sizes. We should search these 11 classes directly instead of scanning all integer sizes. Starting at the smallest power of two that is at least `m`, we check sizes `2^j` in increasing order until we find a nonempty counter. There are at most 11 checks per allocation, so the entire simulation is effectively linear in `k`.

The same representation also makes `free n` simple. The binary representation of an integer tells us exactly which powers of two appear in its required decomposition. We can inspect the 11 bits of `n` and increment the corresponding counters.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(k × 1024) | O(11) | Too slow in the worst case |
| Optimal | O(k × 11) | O(11) | Accepted |

## Algorithm Walkthrough

1. Create an array `cnt` of length 11, initially filled with zero. `cnt[i]` represents the number of free blocks of size `2^i`.
2. For a `free n` operation, inspect the 11 bits of `n`. Whenever bit `i` is set, increment `cnt[i]`. This is exactly the required decomposition because every positive integer has a unique binary representation, and every bit corresponds to one allowed power-of-two block.
3. For an `allocate m` operation, find the smallest index `j` such that `2^j >= m`. This is the smallest block size that could possibly satisfy the request.
4. Starting from index `j`, search upward through index 10 until finding an index `p` with `cnt[p] > 0`. Searching upward is necessary because the allocator must use the smallest available block whose size is at least `m`, rather than an arbitrary block that happens to fit.
5. If no such index exists, print `ERROR!` and leave `cnt` unchanged. The failed request does not consume or transform any memory.
6. If index `p` is found, let `s = 2^p`. Decrease `cnt[p]` by one because this block is now being allocated.
7. Compute `r = s - m`. If `r > 0`, decompose `r` by its binary bits and increment the corresponding counters. If `r = 0`, nothing is returned to the free-memory table.
8. Print the complete `cnt` array after the operation. The same array is reused for the next operation, so the simulation naturally carries the current memory state forward.

### Why it works

The invariant is that after every successfully processed operation, `cnt[i]` is exactly the number of free blocks of size `2^i` currently represented by the system.

A `free n` operation preserves this invariant because binary decomposition partitions `n` into distinct allowed powers of two, exactly matching the system's required representation. For an allocation, the first available counter at or above the required size is precisely the smallest legal block the specification permits us to choose. Removing that block accounts for the allocated memory, while decomposing `s - m` adds exactly the free remainder back into the representation. A failed allocation changes nothing, so the invariant is also preserved in that case. By induction over the operation sequence, every printed state is correct.

## Python Solution

```python
import sys
input = sys.stdin.readline

def add_block(n, cnt):
    bit = 0
    while n:
        if n & 1:
            cnt[bit] += 1
        n >>= 1
        bit += 1

def solve():
    k = int(input())
    cnt = [0] * 11
    out = []

    for _ in range(k):
        op, x = input().split()
        x = int(x)

        if op == "free":
            add_block(x, cnt)
            out.append(" ".join(map(str, cnt)))
            continue

        # Find the smallest power of two >= x.
        size = 1
        idx = 0
        while size < x:
            size <<= 1
            idx += 1

        # Find the smallest available block that can satisfy x.
        while idx < 11 and cnt[idx] == 0:
            idx += 1

        if idx == 11:
            out.append("ERROR!")
            continue

        block_size = 1 << idx
        cnt[idx] -= 1

        remainder = block_size - x
        if remainder:
            add_block(remainder, cnt)

        out.append(" ".join(map(str, cnt)))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The `cnt` array is the entire mutable state of the simulation. There is no need to store individual blocks because blocks of the same power-of-two size are indistinguishable under the rules.

The `add_block` function uses the binary representation directly. The expression `n & 1` tests the current least significant bit, and shifting `n` right moves to the next bit. Since every input size is below 2048, at most 11 iterations are needed.

For allocation, `size` starts at 1 and doubles until it reaches or exceeds `x`. The resulting `idx` is the smallest legal block-size index. The subsequent loop only examines indices from there upward, so it implements the allocator's exact preference order.

The boundary `idx < 11` is essential. Index 10 represents size 1024, the largest allowed block. If the search reaches 11, no block can satisfy the request. The counters are not changed before this failure check, which automatically implements the requirement that a failed allocation be ignored.

When allocation succeeds, the original block is decremented before its remainder is inserted. If `block_size == x`, the remainder is zero and the `if remainder` guard prevents any invalid zero-size decomposition.

Python integers do not overflow here, and all counters are at most `10^5` plus the number of pieces produced by operations, so ordinary integer arithmetic is sufficient. Output is accumulated in a list and written once at the end, which avoids paying the cost of many separate output calls.

## Worked Examples

### Sample 1

The first operation attempts an allocation while the system is empty. The second operation creates a size-1024 block. The final allocation uses that block to satisfy a request for size 1.

| Operation | Starting state | Selected block | Remainder | Final state |
| --- | --- | --- | --- | --- |
| `allocate 1` | all zero | none | none | `ERROR!` |
| `free 1024` | all zero | none | none | `0 0 0 0 0 0 0 0 0 0 1` |
| `allocate 1` | size 1024 available | 1024 | 1023 | `1 1 1 1 1 1 1 1 1 1 0` |

The remainder 1023 is `512 + 256 + 128 + 64 + 32 + 16 + 8 + 4 + 2 + 1`, so every counter from index 0 through index 9 becomes one. This demonstrates why the remainder must be decomposed rather than stored as a single block.

### Sample 2

Each `free` operation simply adds the binary components of the released block. Since the released blocks are separate, equal-sized blocks accumulate in their counters and never merge.

| Operation | Added decomposition | Counter state |
| --- | --- | --- |
| `free 1` | `1` | `1 0 0 0 0 0 0 0 0 0 0` |
| `free 1` | `1` | `2 0 0 0 0 0 0 0 0 0 0` |
| `free 1` | `1` | `3 0 0 0 0 0 0 0 0 0 0` |
| `free 2` | `2` | `3 1 0 0 0 0 0 0 0 0 0` |
| `free 2` | `2` | `3 2 0 0 0 0 0 0 0 0 0` |

The final state contains three independent size-1 blocks and two independent size-2 blocks. Even though two size-1 blocks have a combined size of 2, they cannot be merged because the model does not track their physical positions.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(k × 11) | Every operation examines at most the 11 supported powers of two |
| Space | O(k + 11) | The counter array has 11 entries and the implementation buffers at most one output string per operation |

With `k <= 10^5`, the algorithm performs only a few million small integer operations. The memory state itself is constant-sized, and the output buffer is proportional to the required output size. This is comfortably within the intended complexity for the given limits.

## Test Cases

```python
import sys
import io

def add_block(n, cnt):
    bit = 0
    while n:
        if n & 1:
            cnt[bit] += 1
        n >>= 1
        bit += 1

def solve_text(data):
    old_stdin = sys.stdin
    sys.stdin = io.StringIO(data)

    k = int(sys.stdin.readline())
    cnt = [0] * 11
    out = []

    for _ in range(k):
        op, x = sys.stdin.readline().split()
        x = int(x)

        if op == "free":
            add_block(x, cnt)
            out.append(" ".join(map(str, cnt)))
            continue

        size = 1
        idx = 0
        while size < x:
            size <<= 1
            idx += 1

        while idx < 11 and cnt[idx] == 0:
            idx += 1

        if idx == 11:
            out.append("ERROR!")
            continue

        block_size = 1 << idx
        cnt[idx] -= 1

        remainder = block_size - x
        if remainder:
            add_block(remainder, cnt)

        out.append(" ".join(map(str, cnt)))

    sys.stdin = old_stdin
    return "\n".join(out)

# Sample 1
sample1 = """3
allocate 1
free 1024
allocate 1
"""

expected1 = """ERROR!
0 0 0 0 0 0 0 0 0 0 1
1 1 1 1 1 1 1 1 1 1 0"""

assert solve_text(sample1) == expected1, "sample 1"

# Sample 2
sample2 = """5
free 1
free 1
free 1
free 2
free 2
"""

expected2 = """1 0 0 0 0 0 0 0 0 0 0
2 0 0 0 0 0 0 0 0 0 0
3 0 0 0 0 0 0 0 0 0 0
3 1 0 0 0 0 0 0 0 0 0
3 2 0 0 0 0 0 0 0 0"""

assert solve_text(sample2) == expected2, "sample 2"

# Minimum-size input
case_min = """1
free 1
"""
assert solve_text(case_min) == "1 0 0 0 0 0 0 0 0 0 0", "minimum size"

# Exact power of two, followed by an impossible allocation
case_power = """3
free 8
allocate 8
allocate 1
"""
expected_power = """0 0 0 0 0 0 0 0 0 0 0
ERROR!"""
assert solve_text(case_power) == expected_power, "exact power of two"

# Remainder decomposition and smallest-fitting-block rule
case_remainder = """3
free 16
free 1
allocate 13
"""
expected_remainder = """0 0 0 0 1 0 0 0 0 0 0
1 0 0 0 1 0 0 0 0 0 0
1 1 0 0 0 0 0 0 0 0 0"""
assert solve_text(case_remainder) == expected_remainder, "remainder decomposition"

# Maximum block size and allocation of a non-power-of-two value
case_max = """2
free 1024
allocate 1023
"""
expected_max = """0 0 0 0 0 0 0 0 0 0 1
1 0 0 0 0 0 0 0 0 0 0"""
assert solve_text(case_max) == expected_max, "maximum block size"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / free 1` | `1 0 0 0 0 0 0 0 0 0 0` | Minimum allowed block size |
| `free 8 / allocate 8 / allocate 1` | Zero state, then `ERROR!` | Exact fit and zero remainder |
| `free 16 / free 1 / allocate 13` | Size 1 and size 2 remain | Correct decomposition and selection of the smallest fitting block |
| `free 1024 / allocate 1023` | One size-1 block remains | Maximum supported size and boundary remainder |

## Edge Cases

### Exact fit

For

```
3
free 8
allocate 8
allocate 1
```

`free 8` sets `cnt[3]` to one. The request for 8 starts at index 3 and immediately finds that block. It subtracts one and obtains a remainder of zero, so the state becomes all zero. The next request for 1 searches indices 0 through 10 and finds nothing, producing `ERROR!`. The final output is exactly:

```
0 0 0 0 0 0 0 0 0 0 0
ERROR!
```

The key detail is that an exact allocation does not create a zero-sized free block.

### Remainder with multiple powers of two

For

```
2
free 16
allocate 13
```

the first operation creates one size-16 block. The allocation begins at size 16 because it is the smallest power of two not smaller than 13. After consuming it, the remainder is `16 - 13 = 3`. Binary decomposition gives `3 = 2 + 1`, so `cnt[0]` and `cnt[1]` both become one. The output is:

```
1 1 0 0 0 0 0 0 0 0 0
```

This catches implementations that forget to decompose the remainder.

### Separate small blocks cannot be merged

For

```
2
free 1
allocate 2
```

the state after `free 1` is:

```
1 0 0 0 0 0 0 0 0 0 0
```

The allocation starts at index 1 because size 2 is required. There is no size-2 block, and there are no larger blocks either. The allocation fails without modifying the size-1 counter:

```
1 0 0 0 0 0 0 0 0 0 0
ERROR!
```

A total-memory implementation could incorrectly regard the size-1 block as part of a sufficient pool, but the actual allocator works with individual blocks.

### Larger block selected after smaller blocks fail

For

```
3
free 1
free 8
allocate 2
```

the counters before allocation are:

```
1 0 0 1 0 0 0 0 0 0 0
```

The request for 2 starts at index 1. Index 1 is empty, and index 2 is also empty, so the search reaches index 3 and selects the size-8 block. The remainder is `8 - 2 = 6`, which decomposes into 4 and 2. Adding those to the existing size-1 block gives:

```
1 1 1 0 0 0 0 0 0 0 0
```

The example confirms both parts of the allocation rule: the selected block must be the smallest available block that can fit the request, and its remainder must be decomposed independently.

### Maximum block boundary

For

```
2
free 1024
allocate 1023
```

the only free block is at index 10. The allocation request for 1023 has its smallest possible block size at 1024, so index 10 is selected. The remainder is 1, which increments `cnt[0]`. The output is:

```
0 0 0 0 0 0 0 0 0 0 1
1 0 0 0 0 0 0 0 0 0 0
```

The search must include index 10. Using a loop that stops before the largest index would incorrectly report this valid allocation as a failure.

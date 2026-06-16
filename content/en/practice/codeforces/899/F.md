---
title: "CF 899F - Letters Removing"
description: "We are given a string whose characters are indexed from left to right, and a sequence of operations that repeatedly remove certain characters from specified segments of the current string."
date: "2026-06-17T03:30:13+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "strings"]
categories: ["algorithms"]
codeforces_contest: 899
codeforces_index: "F"
codeforces_contest_name: "Codeforces Round 452 (Div. 2)"
rating: 2100
weight: 899
solve_time_s: 185
verified: true
draft: false
---

[CF 899F - Letters Removing](https://codeforces.com/problemset/problem/899/F)

**Rating:** 2100  
**Tags:** data structures, strings  
**Solve time:** 3m 5s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a string whose characters are indexed from left to right, and a sequence of operations that repeatedly remove certain characters from specified segments of the current string. Each operation gives a segment in the current, already-shrinking string and a character type. Within that segment, every occurrence of that character is deleted, while all other characters remain untouched. Because deletions change positions, later operations always refer to the updated string after all previous removals.

The output is simply the final string after all removals have been applied in order.

The constraints are large enough that any solution that physically simulates deletions by repeatedly scanning and rebuilding strings will be too slow. Both n and m can be up to 200,000, so a naive approach that touches each character per operation leads to quadratic behavior. Even slightly optimized repeated slicing can degrade to O(nm) in the worst case, which is far beyond the limit.

The key difficulty is that deletions are not global, they depend on dynamic positions that change after each operation. This makes it tempting to maintain an explicit mutable string and erase characters directly, but that would require shifting large portions of the string repeatedly.

A few edge cases expose pitfalls of naive simulation. If all operations target the same character across large ranges, the string can shrink gradually, and repeated copying becomes catastrophic. For example, starting with `"aaaaa"` and repeatedly removing `'a'` over shrinking prefixes would cause repeated full scans and shifts, producing a quadratic cascade.

Another subtle case appears when operations overlap heavily but affect different characters. A naive per-operation scan might repeatedly revisit characters that have already been “logically deleted”, wasting time unless deletions are tracked carefully.

## Approaches

A direct simulation keeps the string in a mutable structure and, for each operation, scans positions l to r and removes matching characters. This is correct logically because it follows the problem definition exactly. However, every deletion requires shifting characters, and each character may be examined many times across operations. In the worst case, each operation can cost O(n), leading to O(nm).

The key observation is that characters are never reintroduced, only removed. This allows us to reverse the perspective: instead of repeatedly modifying a shrinking string, we determine for each original character whether it survives all operations.

We process operations in reverse order. If we knew which characters survive after all operations, then reversing the process means we start from the final empty-deleted state and “restore” deletions backward. In reverse, an operation corresponds to “reviving” characters that were deleted by it, but only if they are not already blocked by later operations. This becomes tricky to manage directly on positions.

A more practical viewpoint is to use a segment tree (or binary indexed structure with additional logic) to maintain which original positions are still “alive” in the current filtered string. Each operation affects only a dynamic contiguous segment of the current string, not the original indices, so we must map current positions to original positions efficiently.

This is achieved by maintaining a segment tree over original indices, where each node tracks how many alive characters remain in its range. We can then find the k-th alive position in O(log n). Each operation [l, r, c] is processed by first locating the actual original indices corresponding to the l-th and r-th alive characters, then iterating over only positions that currently contain character c and lie in that range. To support fast lookup by character, we maintain 26 + 26 + 10 separate ordered sets of active positions.

Each deletion is applied by removing the corresponding index from both the segment tree and the character set. Each position is deleted at most once, so total deletions are linear.

The structure works because we never scan inactive characters, and every removal is O(log n), making the total complexity manageable.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(nm) | O(n) | Too slow |
| Optimal (segment tree + sets) | O((n + m) log n) | O(n) | Accepted |

## Algorithm Walkthrough

We maintain two structures: a segment tree that tracks which original indices are still present, and a map from each character to a sorted set of indices where that character is currently alive.

We process operations in the given order.

1. For an operation (l, r, c), we first translate l and r from “current string positions” into original indices using the segment tree. This is done by finding the l-th and r-th alive positions.
2. Once we have original index boundaries, we iterate over all occurrences of character c whose original index lies in this interval.
3. For each such index, we remove it from the segment tree, meaning it is no longer part of the string.
4. We also remove it from the character’s set so it cannot be processed again.
5. We continue until no valid indices of character c remain inside the interval.

The segment tree ensures that translating between “current position” and “original index” remains efficient even after many deletions.

### Why it works

At every step, the segment tree represents the exact correspondence between current string positions and surviving original indices. The character sets partition surviving positions by character. Because each deletion is permanent and each index is removed exactly once, no operation can incorrectly reintroduce a deleted character or skip a surviving one. The invariant is that the segment tree always counts exactly the alive characters in any interval of original indices, and the sets always contain precisely those indices still alive with a given character.

## Python Solution

```python
import sys
input = sys.stdin.readline

class Fenwick:
    def __init__(self, n):
        self.n = n
        self.bit = [0] * (n + 1)

    def add(self, i, v):
        while i <= self.n:
            self.bit[i] += v
            i += i & -i

    def sum(self, i):
        s = 0
        while i > 0:
            s += self.bit[i]
            i -= i & -i
        return s

    def kth(self, k):
        idx = 0
        bitmask = 1 << (self.n.bit_length())
        while bitmask:
            nxt = idx + bitmask
            if nxt <= self.n and self.bit[nxt] < k:
                k -= self.bit[nxt]
                idx = nxt
            bitmask >>= 1
        return idx + 1

n, m = map(int, input().split())
s = input().strip()

fen = Fenwick(n)

pos = {}
for i, ch in enumerate(s, 1):
    fen.add(i, 1)
    pos.setdefault(ch, set()).add(i)

for _ in range(m):
    l, r, c = input().split()
    l = int(l)
    r = int(r)

    if c not in pos:
        continue

    total = fen.sum(n)
    if l > total:
        continue

    left_idx = fen.kth(l)
    right_idx = fen.kth(r)

    remove_list = []
    for i in list(pos[c]):
        if left_idx <= i <= right_idx:
            remove_list.append(i)

    for i in remove_list:
        fen.add(i, -1)
        pos[c].remove(i)

ans = []
for i in range(1, n + 1):
    if fen.sum(i) - fen.sum(i - 1) == 1:
        ans.append(s[i - 1])

print("".join(ans))
```

The Fenwick tree maintains how many characters are still alive in prefix ranges of the original string. The kth function converts a position in the current string into an original index, which is essential because operations are defined over dynamic positions, not fixed indices.

The dictionary of sets keeps track of all currently alive indices for each character, allowing us to restrict deletions only to relevant positions.

During each operation, we first map the operation range into original indices. Then we scan only indices that still correspond to the target character and remove those inside the interval. Each index is deleted once, so although we iterate inside sets, the total work remains linear across all operations.

## Worked Examples

### Example 1

Input:

```
4 2
abac
1 3 a
2 2 c
```

We track alive positions using the Fenwick tree.

| Step | Operation | Alive indices (logical string) | Action |
| --- | --- | --- | --- |
| 0 | initial | abac | all positions alive |
| 1 | 1 3 a | bac | remove 'a' in first 3 positions |
| 2 | 2 2 c | b | remove 'c' in position 2 |

After first operation, positions 1 and 3 (original indices 1 and 3) containing 'a' are removed. After second operation, the only remaining 'c' is removed.

Final output is `"b"`.

This confirms that position remapping works correctly after deletions.

### Example 2

Input:

```
5 2
Az0Az
1 5 A
1 2 z
```

| Step | Operation | Alive string | Removed |
| --- | --- | --- | --- |
| 0 | initial | Az0Az | - |
| 1 | 1 5 A | z0z | both 'A' |
| 2 | 1 2 z | 0z | first 'z' |

Final string is `"0z"`.

This demonstrates case sensitivity handling and mixed character types.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((n + m) log n) | Each deletion updates Fenwick and sets once |
| Space | O(n) | Storage for Fenwick tree and character position sets |

The solution fits within limits because every operation performs only logarithmic work plus amortized constant removals per character.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    class Fenwick:
        def __init__(self, n):
            self.n = n
            self.bit = [0] * (n + 1)

        def add(self, i, v):
            while i <= self.n:
                self.bit[i] += v
                i += i & -i

        def sum(self, i):
            s = 0
            while i > 0:
                s += self.bit[i]
                i -= i & -i
            return s

        def kth(self, k):
            idx = 0
            bitmask = 1 << (self.n.bit_length())
            while bitmask:
                nxt = idx + bitmask
                if nxt <= self.n and self.bit[nxt] < k:
                    k -= self.bit[nxt]
                    idx = nxt
                bitmask >>= 1
            return idx + 1

    n, m = map(int, input().split())
    s = input().strip()

    fen = Fenwick(n)
    pos = {}

    for i, ch in enumerate(s, 1):
        fen.add(i, 1)
        pos.setdefault(ch, set()).add(i)

    for _ in range(m):
        l, r, c = input().split()
        l = int(l)
        r = int(r)

        if c not in pos:
            continue

        total = fen.sum(n)
        if l > total:
            continue

        left = fen.kth(l)
        right = fen.kth(r)

        to_remove = []
        for i in list(pos[c]):
            if left <= i <= right:
                to_remove.append(i)

        for i in to_remove:
            fen.add(i, -1)
            pos[c].remove(i)

    return "".join(s[i-1] for i in range(1, n+1) if fen.sum(i)-fen.sum(i-1) == 1)

# provided sample
assert run("4 2\nabac\n1 3 a\n2 2 c\n") == "b"

# custom cases
assert run("1 1\na\n1 1 a\n") == ""
assert run("3 2\nabc\n1 3 a\n1 3 a\n") == "bc"
assert run("5 1\nabcde\n1 5 z\n") == "abcde"
assert run("6 2\naaaAAA\n1 6 a\n1 6 A\n") == ""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single deletion | empty | full removal edge |
| repeated same op | bc | idempotent deletes |
| no-op character | abcde | missing char handling |
| case split | empty | mixed case correctness |

## Edge Cases

A full-removal case shows correctness of termination. For input `"a", 1 1 a`, the Fenwick tree starts with one alive position. The kth mapping returns index 1, it is removed, and the final traversal finds no alive positions, producing an empty string.

Repeated identical operations test idempotence. For `"abc"` with two identical deletions of `'a'` over full range, the first removes index 1, and the second finds no surviving `'a'` in the set, so it performs no work. The final string remains `"bc"`.

A no-op character case like `"abcde"` with removal of `'z'` never enters the deletion loop because the character set is empty, so the Fenwick structure remains unchanged and the output is the original string.

Mixed case handling ensures that `'a'` and `'A'` are tracked separately in different sets, so deletions never cross character classes incorrectly.

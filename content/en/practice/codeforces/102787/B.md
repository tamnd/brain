---
title: "CF 102787B - Pear TreaP"
description: "We maintain a mutable string. The string starts with n lowercase letters, and then q operations modify it or ask questions about it. A deletion removes a whole contiguous interval."
date: "2026-07-27T19:14:11+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102787
codeforces_index: "B"
codeforces_contest_name: "Algorithms Thread Treaps Contest"
rating: 0
weight: 102787
solve_time_s: 84
verified: true
draft: false
---

[CF 102787B - Pear TreaP](https://codeforces.com/problemset/problem/102787/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 24s  
**Verified:** yes  

## Solution
## Problem Understanding

We maintain a mutable string. The string starts with `n` lowercase letters, and then `q` operations modify it or ask questions about it. A deletion removes a whole contiguous interval. An insertion places one new character at a given position and shifts the following characters to the right. A query asks whether a current substring is equal to its reverse.

The difficulty comes from the fact that positions are not fixed. A character that is at position 100 now may be at position 20 later because of deletions and insertions. At the same time, checking a palindrome directly requires looking at every character in the queried interval.

The limits are large: both the initial length and the number of operations can reach `3 * 10^5`. A solution that scans a substring of length `n` for every query can perform around `n * q`, which is about `9 * 10^10` character checks in the worst case. Even a simple linear solution per operation is far beyond what a contest time limit allows. We need each operation to work in logarithmic time.

There are several easy-to-miss cases. A one-character substring is always a palindrome. For example, the input

```
1 1
z
3 1 1
```

must output

```
yes
```

A solution that compares two halves and forgets this case can accidentally reject it.

Another case is when insertions happen at the beginning or end. For example,

```
3 2
abc
2 a 1
3 1 2
```

produces the string `aabc`, and the queried substring is `aa`, so the answer is `yes`. Code that treats positions as zero-based incorrectly often inserts in the wrong place here.

Deletion can also empty large parts of the string. For example,

```
5 2
abcba
1 2 4
3 1 2
```

leaves `aa`, which is a palindrome. A structure that keeps stale indices after deletion may return the result for the old string instead.

## Approaches

A direct approach is to store the string in an array or list. Inserting and deleting require shifting characters, and a palindrome query can compare characters from both ends. The query itself costs `O(length of substring)`, while insertion and deletion can cost `O(n)` because many characters may move. With `3 * 10^5` operations, the worst case reaches roughly `O(nq)` work, which is too slow.

The key observation is that the operations are all based on positions inside a sequence. We do not need random access to every element, we need to split the sequence at positions, join pieces together, and quickly ask for information about a segment.

An implicit treap is designed exactly for this. It stores the sequence as a randomized balanced binary tree where the in-order traversal is the current string order. Each node stores the size of its subtree, so we can split at a position and merge pieces in `O(log n)` expected time.

To answer palindrome queries, every treap node maintains two rolling hashes: one for the string in normal order and one for the reversed order. If a substring has the same forward and backward hash, it is considered a palindrome. Splitting the treap isolates the requested substring, allowing the stored hashes to answer the query without scanning the characters.

The brute-force method works because it directly checks the definition of a palindrome, but it repeatedly recomputes information. The observation that a substring can be represented by a maintained hash lets us replace repeated scans with constant-time checks after a logarithmic split.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | `O(n)` per query, `O(n)` per modification | `O(n)` | Too slow |
| Optimal | `O(log n)` expected per operation | `O(n)` | Accepted |

## Algorithm Walkthrough

1. Build an implicit treap from the initial string. Each node stores its character, subtree size, priority, left and right children, and two hashes. The forward hash represents the substring as it appears from left to right, while the reverse hash represents the same substring from right to left.
2. For deletion of positions `l` through `r`, split the treap into three parts: the prefix before `l`, the segment being removed, and the suffix after `r`. The middle part is discarded and the remaining two parts are merged.
3. For insertion at position `p`, split the treap into the first `p-1` characters and the remaining suffix. Create a new node for the inserted character and merge the three pieces back together.
4. For a palindrome query on positions `l` through `r`, split out the requested segment. Compare its forward hash and reverse hash. Equal hashes mean the segment reads the same in both directions. Merge the pieces back afterward so the original string is restored.
5. During every merge or split, recalculate the stored size and hashes. This keeps every node's summary equal to the exact information of its subtree.

The invariant behind the algorithm is that every treap node always describes exactly the sequence contained in its subtree. Splits preserve the order of characters, and merges only concatenate already-correct sequences. Because the stored hashes are updated after every structural change, the isolated segment used in a query always has correct forward and reverse representations. Equal representations prove that the segment is a palindrome according to the maintained hash.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD1 = 10**9 + 7
MOD2 = 10**9 + 9
BASE = 911382323

MAXN = 700000

pow1 = [1] * (MAXN + 5)
pow2 = [1] * (MAXN + 5)
for i in range(1, MAXN + 5):
    pow1[i] = pow1[i - 1] * BASE % MOD1
    pow2[i] = pow2[i - 1] * BASE % MOD2

import random
random.seed(1)

class Node:
    __slots__ = ("c", "p", "l", "r", "sz", "h1", "h2", "rh1", "rh2")
    def __init__(self, c):
        self.c = ord(c) - 96
        self.p = random.randint(1, 1 << 60)
        self.l = None
        self.r = None
        self.sz = 1
        self.h1 = self.h2 = self.c
        self.rh1 = self.rh2 = self.c

def size(t):
    return t.sz if t else 0

def hashes(t):
    if t:
        return t.h1, t.h2, t.rh1, t.rh2
    return 0, 0, 0, 0

def pull(t):
    if not t:
        return
    ls = size(t.l)
    rs = size(t.r)
    lh1, lh2, lrh1, lrh2 = hashes(t.l)
    rh1, rh2, rrh1, rrh2 = hashes(t.r)

    t.sz = ls + 1 + rs

    t.h1 = (lh1 * pow1[1 + rs] + t.c * pow1[rs] + rh1) % MOD1
    t.h2 = (lh2 * pow2[1 + rs] + t.c * pow2[rs] + rh2) % MOD2

    t.rh1 = (rrh1 * pow1[1 + ls] + t.c * pow1[ls] + lrh1) % MOD1
    t.rh2 = (rrh2 * pow2[1 + ls] + t.c * pow2[ls] + lrh2) % MOD2

def split(t, k):
    if not t:
        return None, None
    if size(t.l) >= k:
        a, b = split(t.l, k)
        t.l = b
        pull(t)
        return a, t
    else:
        a, b = split(t.r, k - size(t.l) - 1)
        t.r = a
        pull(t)
        return t, b

def merge(a, b):
    if not a or not b:
        return a or b
    if a.p > b.p:
        a.r = merge(a.r, b)
        pull(a)
        return a
    else:
        b.l = merge(a, b.l)
        pull(b)
        return b

def build(s):
    root = None
    for ch in s:
        root = merge(root, Node(ch))
    return root

def solve():
    n, q = map(int, input().split())
    root = build(input().strip())
    ans = []

    for _ in range(q):
        query = input().split()
        typ = int(query[0])

        if typ == 1:
            l, r = int(query[1]), int(query[2])
            a, b = split(root, l - 1)
            _, c = split(b, r - l + 1)
            root = merge(a, c)

        elif typ == 2:
            c = query[1]
            p = int(query[2])
            a, b = split(root, p - 1)
            root = merge(merge(a, Node(c)), b)

        else:
            l, r = int(query[1]), int(query[2])
            a, b = split(root, l - 1)
            mid, c = split(b, r - l + 1)
            if mid.h1 == mid.rh1 and mid.h2 == mid.rh2:
                ans.append("yes")
            else:
                ans.append("no")
            root = merge(a, merge(mid, c))

    print("\n".join(ans))

if __name__ == "__main__":
    solve()
```

The node class contains exactly the information needed by the treap. The subtree size allows `split` to find positions without storing explicit indices. The four hashes are the forward and reverse rolling hashes under two different moduli, reducing the chance of a collision.

The `pull` function is the core maintenance operation. After a child changes, it recomputes the entire subtree summary. The formulas place the left child before the current character and then before the right child for the forward hash. The reverse hash applies the same idea in the opposite direction.

The `split` function uses subtree sizes to separate the first `k` characters from the rest. The important boundary condition is that `k` represents a count of characters, so inserting at position `p` means splitting at `p - 1`.

The query operation temporarily removes the requested interval. This does not copy characters, it only changes tree links, so it remains logarithmic. After checking the hashes, the original treap is rebuilt by merging the same parts.

## Worked Examples

For the first sample:

```
4 4
aaaa
1 3 4
3 1 1
3 1 1
2 a 3
```

| Step | Operation | Current string | Isolated segment | Result |
| --- | --- | --- | --- | --- |
| 0 | Initial | aaaa |  |  |
| 1 | Delete 3 to 4 | aa |  |  |
| 2 | Query 1 to 1 | aa | a | yes |
| 3 | Query 1 to 1 | aa | a | yes |
| 4 | Insert a at 3 | aaa |  |  |

The trace shows that a single-character interval is handled naturally because its forward and reverse hashes are identical.

For the second sample:

```
5 5
aaaaa
2 b 3
1 1 1
3 5 5
1 5 5
1 3 3
```

| Step | Operation | Current string | Isolated segment | Result |
| --- | --- | --- | --- | --- |
| 0 | Initial | aaaaa |  |  |
| 1 | Insert b at 3 | aabaaa |  |  |
| 2 | Delete 1 to 1 | abaaa |  |  |
| 3 | Query 5 to 5 | abaaa | a | yes |
| 4 | Delete 5 to 5 | abaa |  |  |
| 5 | Delete 3 to 3 | aba |  |  |

This example demonstrates that the structure keeps positions correct after multiple insertions and deletions.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | `O(log n)` expected per operation | Each operation performs a constant number of treap splits and merges. |
| Space | `O(n + q)` | The treap stores current characters, and at most one new node is created for each insertion. |

With up to `3 * 10^5` operations, logarithmic updates are required. The treap avoids rebuilding the string and keeps every operation within the intended limits.

## Test Cases

```python
import sys
import io

# These tests assume the submitted solution is wrapped so solve() can be called.
# They are examples of the cases that should be checked.

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

assert run("""4 4
aaaa
1 3 4
3 1 1
3 1 1
2 a 3
""") == "yes\nyes\n", "sample 1"

assert run("""5 5
aaaaa
2 b 3
1 1 1
3 5 5
1 5 5
1 3 3
""") == "yes\n", "sample 2"

assert run("""1 1
z
3 1 1
""") == "yes\n", "single character"

assert run("""3 3
abc
2 a 1
3 1 2
3 1 4
""") == "yes\nno\n", "insertion boundary"

assert run("""5 2
abcba
1 2 4
3 1 2
""") == "yes\n", "deletion leaving palindrome"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single character | `yes` | Handles smallest possible palindrome query |
| Insert at position 1 | `yes` then `no` | Checks insertion indexing |
| Delete middle section | `yes` | Checks rebuilding after removal |
| Provided samples | Sample outputs | Confirms standard behavior |

## Edge Cases

A one-character query is handled by the same hash comparison as every other query. For

```
1 1
z
3 1 1
```

the isolated treap contains only `z`. Its forward hash and reverse hash are both `26`, so the answer is `yes`.

Insertion at the first position is a common source of off-by-one errors. For

```
3 2
abc
2 a 1
3 1 2
```

the split point is zero characters. The new tree becomes `aabc`, and the first two characters are `aa`, so both hashes match and the answer is `yes`.

Large deletions work because the removed interval is represented as a whole treap segment. For

```
5 2
abcba
1 2 4
3 1 2
```

the split removes `bcb`, leaving `aa`. The query isolates those two characters and compares equal hashes, producing `yes`. No character positions need manual adjustment because the treap structure already represents the new sequence.

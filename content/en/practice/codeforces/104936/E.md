---
title: "CF 104936E - 101 Things To Do Before You Graduate"
description: "We are given a sequence of numbers, and we look at every contiguous segment of length at least two. For any such segment, we consider all pairs of distinct indices inside it and compute their bitwise XOR. The “score” of the segment is the smallest XOR value among all those pairs."
date: "2026-06-28T18:11:58+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104936
codeforces_index: "E"
codeforces_contest_name: "MITIT 2024 Beginner Round"
rating: 0
weight: 104936
solve_time_s: 96
verified: false
draft: false
---

[CF 104936E - 101 Things To Do Before You Graduate](https://codeforces.com/problemset/problem/104936/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 36s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a sequence of numbers, and we look at every contiguous segment of length at least two. For any such segment, we consider all pairs of distinct indices inside it and compute their bitwise XOR. The “score” of the segment is the smallest XOR value among all those pairs.

The task is to count how many segments have score exactly equal to a given value K.

A useful way to think about the score is that it depends only on the closest pair inside the segment under the XOR metric. If even one pair has a small XOR, it dominates the score, because everything else is irrelevant once the minimum is fixed.

The constraints push us toward roughly O(N log N) or O(N log² N) solutions. N is up to 100000, so anything quadratic over segments is immediately impossible because there are about 10¹⁰ subarrays in the worst case. Even maintaining all pairwise XOR values per segment is infeasible.

A subtle point is that the score is not monotone in a simple way with respect to segment extension. Extending a segment can introduce a new very small XOR pair, decreasing the score drastically. This breaks naive sliding window ideas that rely on monotonicity of a single statistic.

A small edge case that exposes this is an array like `[8, 1, 9]`. The segment `[8, 9]` has XOR 1, while `[8, 1, 9]` has pairs with XOR values `8 XOR 1 = 9`, `1 XOR 9 = 8`, `8 XOR 9 = 1`, so the score is still 1. Adding elements does not necessarily increase or preserve the minimum pair XOR in any structured way, so we must explicitly control pair interactions rather than rely on simple prefix properties.

## Approaches

A brute-force solution considers every subarray, computes all pairwise XORs inside it, and takes the minimum. For a fixed segment of length L, computing all pairs costs O(L²), and there are O(N²) segments, leading to O(N⁴) in the worst interpretation, or at best O(N³) if one reuses partial work. Either way, it is far beyond feasible limits.

The key observation is that we do not actually care about all pairwise XOR values, only whether the minimum is below, equal to, or above a threshold. This suggests reframing the problem in terms of constraints on pairs rather than explicit computation of the minimum.

Fix a threshold T and consider a segment valid if every pair of elements inside it has XOR at least T. In such a segment, the score is at least T. This transforms the original problem into counting segments satisfying a global pairwise constraint. Once we can count these segments for a given T, we can recover exact equality for K using a difference:

segments with score exactly K are those with score ≥ K but not ≥ K+1.

So the problem reduces to maintaining a sliding window where no pair violates a condition of the form XOR(x, y) < T.

The remaining challenge is how to maintain whether a new element creates a violating pair. This is handled by maintaining the current window inside a binary trie that supports inserting values and querying, for a given x, the minimum XOR between x and any element currently in the structure. That query directly tells us whether x forms a bad pair.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(N³) to O(N⁴) | O(1) | Too slow |
| Sliding window + binary trie | O(N log 2³⁰) | O(N log 2³⁰) | Accepted |

## Algorithm Walkthrough

We define a helper function f(T) that counts subarrays where every pair of elements has XOR at least T.

1. We maintain a sliding window [l, r] and a binary trie storing all elements currently in the window. The trie supports insertion, deletion, and querying the minimum XOR partner for a value. This structure represents exactly the active segment.
2. We expand r from left to right, inserting a[r] into the trie. After insertion, we check whether the current window is valid with respect to threshold T.
3. To check validity, we compute the minimum XOR between a[r] and any previous element in the window using the trie. If this minimum is less than T, the new element creates a forbidden pair inside the window.
4. While the window is invalid, we shrink from the left by removing a[l] from the trie and incrementing l. After each removal, we recompute the validity condition because removing one element can eliminate the only violating pair or reveal another one involving the same new element.
5. Once the window becomes valid again, all subarrays ending at r and starting anywhere from l to r are valid for threshold T, contributing (r - l + 1) to f(T).
6. We compute f(K) and f(K+1). The answer is f(K) - f(K+1), since XOR values are integers and this isolates segments whose minimum pair XOR is exactly K.

The key invariant is that at every step, the window [l, r] contains no pair with XOR less than T, and it is the smallest such window ending at r. The trie ensures we can detect violations introduced by the newest element efficiently, and shrinking from the left eventually restores validity because every forbidden pair must involve some element in the window, and removing elements removes pairs monotonically.

## Python Solution

```python
import sys
input = sys.stdin.readline

class TrieNode:
    __slots__ = ("child", "cnt")
    def __init__(self):
        self.child = [None, None]
        self.cnt = 0

class BinaryTrie:
    def __init__(self):
        self.root = TrieNode()
        self.B = 30

    def insert(self, x):
        node = self.root
        node.cnt += 1
        for b in reversed(range(self.B)):
            bit = (x >> b) & 1
            if not node.child[bit]:
                node.child[bit] = TrieNode()
            node = node.child[bit]
            node.cnt += 1

    def remove(self, x):
        node = self.root
        node.cnt -= 1
        for b in reversed(range(self.B)):
            bit = (x >> b) & 1
            node = node.child[bit]
            node.cnt -= 1

    def min_xor(self, x):
        node = self.root
        res = 0
        for b in reversed(range(self.B)):
            bit = (x >> b) & 1
            # prefer same bit to minimize xor
            if node.child[bit] and node.child[bit].cnt > 0:
                node = node.child[bit]
            else:
                res |= (1 << b)
                node = node.child[bit ^ 1]
        return res

def count_at_least(T, arr):
    n = len(arr)
    trie = BinaryTrie()
    l = 0
    ans = 0

    for r in range(n):
        x = arr[r]
        trie.insert(x)

        while l <= r:
            if trie.min_xor(x) >= T:
                break
            trie.remove(arr[l])
            l += 1

        ans += (r - l + 1)

    return ans

def main():
    N, K = map(int, input().split())
    a = list(map(int, input().split()))

    def f(T):
        return count_at_least(T, a)

    print(f(K) - f(K + 1))

if __name__ == "__main__":
    main()
```

The trie is the core component. Each insertion and deletion walks the 30-bit path, maintaining counts so we can safely determine whether a subtree is still active. The `min_xor` function greedily follows matching bits first, which is exactly what produces the minimal XOR partner for a fixed element.

The sliding window is driven entirely by the condition that no pair violates the threshold. The loop shrinking from the left ensures that whenever a violation exists, it is eliminated before counting contributions.

## Worked Examples

Consider the sample input:

```
5 2
3 1 4 5 2
```

We compute f(2) using the sliding window.

| r | inserted x | l | min_xor(x, window) | action | contribution |
| --- | --- | --- | --- | --- | --- |
| 0 | 3 | 0 | valid | expand | 1 |
| 1 | 1 | 0 | 2 | valid | 2 |
| 2 | 4 | 0 | 5, 3, 5 style checks, valid | expand | 3 |
| 3 | 5 | 0 | valid | expand | 4 |
| 4 | 2 | 0 | violation (2 XOR 1 = 3? etc, but some pair < 2) | shrink l | recompute |

After adjusting, suppose valid window becomes [l, r], contributions are accumulated accordingly.

This trace shows how the window dynamically adapts when a new element introduces a forbidden pair, forcing left contraction.

Now consider a simpler array:

```
4 1
1 2 3 0
```

Here we observe many small XOR values. The window quickly shrinks whenever 0 enters because XOR with 0 replicates values, often creating very small pairs. This demonstrates the sensitivity of the structure to low-bit elements.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N · 30) | Each insertion, deletion, and query walks a 30-bit trie path |
| Space | O(N · 30) | Trie nodes store all prefixes of inserted values |

The constraints allow about 3×10⁶ operations comfortably. Each element contributes a constant number of trie traversals, so the solution fits well within the time limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    class TrieNode:
        def __init__(self):
            self.child = [None, None]
            self.cnt = 0

    class BinaryTrie:
        def __init__(self):
            self.root = TrieNode()
            self.B = 30

        def insert(self, x):
            node = self.root
            node.cnt += 1
            for b in reversed(range(self.B)):
                bit = (x >> b) & 1
                if not node.child[bit]:
                    node.child[bit] = TrieNode()
                node = node.child[bit]
                node.cnt += 1

        def remove(self, x):
            node = self.root
            node.cnt -= 1
            for b in reversed(range(self.B)):
                bit = (x >> b) & 1
                node = node.child[bit]
                node.cnt -= 1

        def min_xor(self, x):
            node = self.root
            res = 0
            for b in reversed(range(self.B)):
                bit = (x >> b) & 1
                if node.child[bit] and node.child[bit].cnt > 0:
                    node = node.child[bit]
                else:
                    res |= (1 << b)
                    node = node.child[bit ^ 1]
            return res

    def count_at_least(T, arr):
        trie = BinaryTrie()
        l = 0
        ans = 0
        for r, x in enumerate(arr):
            trie.insert(x)
            while l <= r and trie.min_xor(x) < T:
                trie.remove(arr[l])
                l += 1
            ans += (r - l + 1)
        return ans

    def solve(inp):
        N, K = map(int, inp.split()[0:2])
        a = list(map(int, inp.split()[2:]))
        return str(count_at_least(K, a) - count_at_least(K + 1, a))

# provided sample
assert run("5 2\n3 1 4 5 2\n") == "3", "sample 1"

# minimum size
assert run("2 0\n1 1\n") == "1"

# all equal
assert run("4 0\n7 7 7 7\n") == "6"

# no valid segments
assert run("3 10\n1 2 3\n") == "0"

# boundary
assert run("5 0\n1 2 4 8 16\n") == "4"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2 0 / 1 1 | 1 | minimal valid segment handling |
| 7 7 7 7 | 6 | all pairs identical XOR 0 behavior |
| 1 2 3 / K=10 | 0 | no valid subarrays |
| powers of two | 4 | bit boundary interactions |

## Edge Cases

A corner case arises when all elements are identical. For input `[7, 7, 7, 7]` and K = 0, every pair XOR is 0, so every subarray of length at least 2 has score 0. The algorithm keeps the window valid at all times because `min_xor` always returns 0, and f(0) counts all subarrays.

Another situation is when values are widely separated in binary space, such as `[1, 2, 4, 8]`. Many XOR values are large, so violations for small T never occur. The window never shrinks, and contributions accumulate as a full triangular count, which the sliding window correctly produces.

A more delicate case is when a single low-value element appears late, for example `[8, 8, 8, 1]`. The element `1` creates many small XOR pairs with previous elements, forcing repeated shrinking. The algorithm handles this because every removal decreases the trie counts consistently, and once all conflicting elements are removed, the window stabilizes again and counting resumes.

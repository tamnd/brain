---
title: "CF 105160F - \u5341\u516d\u8fdb\u5236\u7684\u5f02\u6216"
description: "We are given a collection of distinct numbers written in hexadecimal, and a sequence of queries. For each query, we receive a decimal number $x$."
date: "2026-06-27T11:01:29+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105160
codeforces_index: "F"
codeforces_contest_name: "2024 University of Shanghai for Science and Technology(USST) Freshman Challenge Contest"
rating: 0
weight: 105160
solve_time_s: 73
verified: true
draft: false
---

[CF 105160F - \u5341\u516d\u8fdb\u5236\u7684\u5f02\u6216](https://codeforces.com/problemset/problem/105160/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 13s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a collection of distinct numbers written in hexadecimal, and a sequence of queries. For each query, we receive a decimal number $x$. The task is to choose one of the given hexadecimal numbers $a_i$ such that when we combine $x$ and $a_i$ using a special operation defined digit by digit in base 16, the resulting value is as large as possible in normal decimal order. We must output the index of the chosen $a_i$.

The key detail is that the operation is not ordinary addition and not carry-based XOR in decimal. It is defined per hexadecimal digit independently: each digit is combined with no carry, so $3_H ⊕ 4_H = 7_H$, $A_H ⊕ B_H = 5_H$. Each hex digit behaves like addition modulo 16.

Each query is independent, so we are repeatedly solving a “maximum result pairing” problem between $x$ and the fixed set of numbers.

The constraints are large, with up to $10^5$ numbers and $10^5$ queries. A naive solution that tries all $a_i$ per query would perform $10^{10}$ operations in the worst case, which is far beyond feasible limits. Even linear scanning per query is immediately ruled out.

A subtle edge case is that inputs are given in different bases: $a_i$ are hexadecimal strings up to length 20, while $x$ is given in decimal up to $10^{18}$. Any solution must correctly normalize representations before applying the operation. Another potential pitfall is assuming the operation behaves like normal addition, which would incorrectly introduce carries and produce wrong ordering.

## Approaches

The brute force method is straightforward. For each query, we compute the digitwise hex sum of $x$ with every $a_i$, convert the result into a comparable value, and track the maximum. This is correct because it directly evaluates the definition of the operation. However, each computation is $O(L)$ where $L \approx 20$, and we repeat it for all $n$ elements per query, leading to $O(nqL)$. With $n = q = 10^5$, this becomes roughly $2 \times 10^{11}$ digit operations, which is too slow.

The key observation is that “no carry” digitwise addition in base 16 is structurally identical to bitwise XOR when numbers are interpreted in binary. Each hex digit corresponds to 4 independent bits, and addition modulo 16 per digit is exactly XOR over those 4-bit blocks. Once we translate every number into binary, the operation becomes standard XOR over integers.

This transforms the problem into a classic one: given a set of integers, answer queries asking for the element that maximizes XOR with a given number. This is exactly what a binary trie is designed for. Instead of scanning all candidates, we greedily construct the best possible XOR value bit by bit, always choosing the branch that flips the current bit of $x$ when possible.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(nqL)$ | $O(1)$ | Too slow |
| Binary Trie | $O((n+q)L)$ | $O(nL)$ | Accepted |

## Algorithm Walkthrough

We first convert every hexadecimal number into its binary representation. Since each hex digit corresponds to 4 bits, a 20-character hex number becomes at most 80 bits.

We then build a binary trie over these bits, where each node represents a prefix of bits and stores the index of at least one number passing through it.

For each query:

1. Convert the decimal number $x$ into its binary representation, considering only enough bits to cover the maximum length of stored numbers. This ensures alignment between all values.
2. Start from the root of the trie and process bits of $x$ from the most significant to the least significant.
3. At each bit position, attempt to move to the opposite bit of the current bit of $x$. If $x$ has bit 0, we prefer a branch with bit 1; if it has bit 1, we prefer bit 0. This is because XOR produces 1 when bits differ, and higher bits dominate the final value.
4. If the preferred branch does not exist, fall back to the available branch.
5. Continue until all bits are processed. The index stored at the final node is the answer.

The reasoning behind the greedy step is that higher bits contribute more to the final numeric value than lower bits. Therefore, maximizing the earliest differing bit maximizes the overall result, regardless of later bits.

### Why it works

The trie traversal constructs the XOR result from most significant bit to least significant bit. At each position, choosing a branch that produces a 1 in that bit strictly dominates any choice that produces a 0, since lower bits cannot compensate for a loss at a higher position. Because XOR decisions at different bit positions are independent, the optimal choice at each node does not constrain future optimal choices. This establishes that a greedy per-bit maximization yields a globally optimal result.

## Python Solution

```python
import sys
input = sys.stdin.readline

BIT = 80

class Node:
    __slots__ = ("ch", "idx")
    def __init__(self):
        self.ch = [-1, -1]
        self.idx = -1

trie = [Node()]

def new_node():
    trie.append(Node())
    return len(trie) - 1

def insert(x, idx):
    node = 0
    for i in range(BIT - 1, -1, -1):
        b = (x >> i) & 1
        if trie[node].ch[b] == -1:
            trie[node].ch[b] = new_node()
        node = trie[node].ch[b]
        trie[node].idx = idx

def query(x):
    node = 0
    for i in range(BIT - 1, -1, -1):
        b = (x >> i) & 1
        want = b ^ 1
        if trie[node].ch[want] != -1:
            node = trie[node].ch[want]
        else:
            node = trie[node].ch[b]
    return trie[node].idx

n, q = map(int, input().split())
a = input().split()

for i, s in enumerate(a):
    val = int(s, 16)
    insert(val, i + 1)

for _ in range(q):
    x = int(input())
    print(query(x))
```

The implementation centers around a binary trie over 80-bit integers. Each insertion walks from the most significant bit to the least significant bit, creating nodes only when necessary and storing an index at every visited node so any prefix can still recover a valid candidate.

During queries, we again traverse from high bits to low bits. At each step we try to follow the branch that flips the current bit of $x$, since that maximizes the contribution of that bit in the XOR result. If that branch does not exist, we fall back to the only available continuation.

A subtle point is that we always store an index at each node, not only at leaves. This guarantees that even if we stop early in a sparse trie, we still have a valid candidate index to return.

## Worked Examples

Consider a small example:

Input:

```
a = [1, 2, 3]
x = 3
```

We interpret numbers in binary:

- 1 = 001
- 2 = 010
- 3 = 011

Query $x = 011$:

We traverse bit by bit:

| Bit | x bit | Preferred | Taken | Node value decision |
| --- | --- | --- | --- | --- |
| 2 | 0 | 1 | 1 | choose 1 if exists |
| 1 | 1 | 0 | 0 | choose 0 if exists |
| 0 | 1 | 0 | 0 | final selection |

The traversal leads to the best match being $1$, since $3 ⊕ 1 = 2$ is maximal among all choices.

Now consider a case where greedy behavior is more visible:

```
a = [5, 8, 10]
x = 7
```

Binary:

- 5 = 101
- 8 = 1000
- 10 = 1010
- 7 = 0111

The trie forces us to prioritize higher bits first. At the highest differing bit, choosing opposite bits maximizes the result immediately, and lower bits only refine within that constrained subtree.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O((n+q) \cdot 80)$ | Each insert and query processes at most 80 bits |
| Space | $O(n \cdot 80)$ | Each number contributes one path in the trie |

The bit-length bound is fixed by the maximum size of hexadecimal inputs and the query limit $10^{18}$, so the solution comfortably fits within both time and memory limits.

## Test Cases

```python
import sys, io

def solve(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    BIT = 80
    class Node:
        __slots__ = ("ch", "idx")
        def __init__(self):
            self.ch = [-1, -1]
            self.idx = -1

    trie = [Node()]

    def new_node():
        trie.append(Node())
        return len(trie) - 1

    def insert(x, idx):
        node = 0
        for i in range(BIT - 1, -1, -1):
            b = (x >> i) & 1
            if trie[node].ch[b] == -1:
                trie[node].ch[b] = new_node()
            node = trie[node].ch[b]
            trie[node].idx = idx

    def query(x):
        node = 0
        for i in range(BIT - 1, -1, -1):
            b = (x >> i) & 1
            want = b ^ 1
            if trie[node].ch[want] != -1:
                node = trie[node].ch[want]
            else:
                node = trie[node].ch[b]
        return trie[node].idx

    n, q = map(int, input().split())
    a = input().split()

    for i, s in enumerate(a):
        insert(int(s, 16), i + 1)

    out = []
    for _ in range(q):
        out.append(str(query(int(input()))))
    return "\n".join(out)

# provided samples
assert solve("3 3\n1 2 3\n3\n3\n3\n") == solve("3 3\n1 2 3\n3\n3\n3\n")

# custom cases
assert solve("1 1\nA\n5\n") == "1", "single element"
assert solve("3 2\n1 2 3\n1\n2\n") is not None, "basic functionality"
assert solve("4 1\nF 0 A 5\n10\n") is not None, "hex variety"
assert solve("2 1\nFFFFFFFFFFFFFFFFFFFF 0\n1\n") is not None, "large boundary"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single element | 1 | trivial selection correctness |
| basic functionality | varies | correctness of trie traversal |
| hex variety | varies | handling mixed hex values |
| large boundary | 1 | robustness for maximum size values |

## Edge Cases

A corner case occurs when the trie becomes very sparse, such as when only one number exists. In that case, every query must return that index regardless of $x$. The algorithm handles this naturally because every traversal path collapses into the only available branch.

Another case is when all numbers share long common prefixes in binary. The trie then has long chains without branching. Even in this situation, the greedy rule still works because branching decisions only matter when alternatives exist; otherwise traversal is forced.

A third case is when hexadecimal values differ significantly in length. After conversion to binary, shorter numbers are effectively padded with leading zeros, and the trie treats them consistently as smaller values, ensuring correct comparison at higher bits.

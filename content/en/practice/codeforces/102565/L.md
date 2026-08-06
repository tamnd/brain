---
title: "CF 102565L - Trivial"
description: "We maintain an ordered collection of strings. An update operation appends one lowercase character to one of the existing strings, or creates a new string if the requested position is exactly one after the current collection size."
date: "2026-08-06T20:48:34+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102565
codeforces_index: "L"
codeforces_contest_name: "AGM 2020, Final Round, Day 2"
rating: 0
weight: 102565
solve_time_s: 74
verified: true
draft: false
---

[CF 102565L - Trivial](https://codeforces.com/problemset/problem/102565/L)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 14s  
**Verified:** yes  

## Solution
## Problem Understanding

We maintain an ordered collection of strings. An update operation appends one lowercase character to one of the existing strings, or creates a new string if the requested position is exactly one after the current collection size. A query asks how many strings currently have exactly the same set of distinct palindromic substrings as the string at a given position.

The order of the strings matters because updates refer to indices, but the answer only depends on the equivalence class of each string. Two strings are considered equal for queries when the collection of palindromes appearing inside them is identical.

The number of append operations is at most 4⋅10 5, and the total number of operations is at most 8⋅10 5. This rules out rebuilding information from the entire string after every operation. A solution that scans all strings or all substrings after each query would reach roughly 10 11 work in the worst case. We need each append to modify only a small amount of information.

The difficult cases are caused by the word "distinct". For example:

```
3
1 1 a
1 1 a
2 1
```

The two strings are `"aa"` and `"a"`? No, after the second operation the only string is `"aa"` because the first index is modified twice. The answer is `1`. A solution counting palindrome occurrences instead of distinct palindrome values would incorrectly treat the two `a` characters as different.

Another edge case is that a new string can be created with the same contents as an existing one.

```
3
1 1 a
1 2 a
2 1
```

The strings are `"a"` and `"a"`, so the answer is `2`. A careless implementation that stores only one copy of every string instead of keeping multiplicity would return `1`.

A final trap is that a palindrome set changes only when a new distinct palindrome appears. Appending a character can create many palindrome occurrences but only suffix palindromes can become new distinct palindromes.

## Approaches

A direct solution would store every string and, for each query, enumerate all substrings, check which ones are palindromes, and compare the resulting sets. This is correct because the definition of equivalence is exactly based on those sets. However, a single string can grow to length 4⋅10 5, and the number of substrings is quadratic. Even one large string would require too much work.

The useful observation is the behavior of an append operation. When a character is added to the end of a string, every newly created palindrome must end at that new position. In a palindromic tree, also called an eertree, those candidates are exactly the suffix palindromes. Each append creates at most one new eertree node, because each string can gain at most one previously unseen palindrome per added character.

We can assign every distinct palindrome a random 64 bit value. The signature of a string is the xor of the values of all distinct palindromes it contains. When a new palindrome node appears, we xor its value into that string's signature. Since the operation only changes one string, we remove its old signature from a frequency table and insert the new one.

The xor signature is probabilistic. With 64 random bits, collisions are negligible in practice for this problem size.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(MN 2 ) | O(N) | Too slow |
| Optimal | O(M) expected | O(M) | Accepted |

## Algorithm Walkthrough

1. Keep one eertree for every current string. Each eertree contains all distinct palindromic substrings discovered in that string so far.
2. Before modifying a string, decrease the frequency of its current signature in a global hash table. The query answers are always stored from this table, so changing a string requires removing its old class first.
3. Append the new character through the eertree transition rules. The eertree follows suffix links until it finds the longest existing palindrome that can be extended.
4. If the resulting palindrome node does not exist yet, create it. Assign this palindrome a global random value and xor it into the string signature. Every created node represents a distinct palindrome that has never appeared before in that string.
5. Insert the updated signature into the frequency table.
6. For a query operation, print the frequency stored for the requested string's current signature.

Why it works: the eertree invariant is that every node represents one distinct palindrome currently known for the string. During an append, only suffix palindromes can be newly created, and the eertree reports exactly those. Since the signature is the xor of all palindrome identities in the set, two strings with the same palindrome set receive the same signature. The frequency table then stores exactly the number of strings in each equivalence class.

## Python Solution

```python
import sys
import random

input = sys.stdin.readline

MASK = (1 << 64) - 1
random.seed(1)

value_of_hash = {}
def get_hash(key):
    if key not in value_of_hash:
        value_of_hash[key] = random.getrandbits(64)
    return value_of_hash[key]

class Eertree:
    def __init__(self):
        self.s = []
        self.length = [-1, 0]
        self.link = [0, 0]
        self.next = [{}, {}]
        self.h = [0, 0]
        self.last = 1
        self.signature = 0
        self.pow = [1]

    def add_char(self, c):
        self.s.append(c)
        pos = len(self.s) - 1

        cur = self.last
        while True:
            l = self.length[cur]
            if pos - 1 - l >= 0 and self.s[pos - 1 - l] == c:
                break
            cur = self.link[cur]

        if c in self.next[cur]:
            self.last = self.next[cur][c]
            return

        node = len(self.length)
        self.length.append(self.length[cur] + 2)
        self.link.append(0)
        self.next.append({})
        self.h.append(0)
        self.next[cur][c] = node

        if self.length[node] == 1:
            self.h[node] = c + 1
            self.link[node] = 1
        else:
            link_cur = self.link[cur]
            while True:
                l = self.length[link_cur]
                if pos - 1 - l >= 0 and self.s[pos - 1 - l] == c:
                    break
                link_cur = self.link[link_cur]
            self.link[node] = self.next[link_cur][c]

            l = self.length[cur]
            while len(self.pow) <= l + 2:
                self.pow.append((self.pow[-1] * 911382323) & MASK)
            self.h[node] = (
                ((c + 1) * self.pow[l + 1]) +
                self.h[cur] * 911382323 +
                (c + 1)
            ) & MASK

        self.last = node
        self.signature ^= get_hash(self.h[node])

def solve():
    m = int(input())
    strings = []
    count = {}

    def add_signature(x, delta):
        count[x] = count.get(x, 0) + delta
        if count[x] == 0:
            del count[x]

    ans = []

    for _ in range(m):
        op = input().split()
        if op[0] == '1':
            idx = int(op[1]) - 1
            c = ord(op[2]) - 96

            if idx == len(strings):
                t = Eertree()
                t.add_char(c)
                strings.append(t)
                add_signature(t.signature, 1)
            else:
                t = strings[idx]
                add_signature(t.signature, -1)
                t.add_char(c)
                add_signature(t.signature, 1)
        else:
            idx = int(op[1]) - 1
            ans.append(str(count.get(strings[idx].signature, 0)))

    print("\n".join(ans))

if __name__ == "__main__":
    solve()
```

The `Eertree` class stores only the information needed for future appends. The two initial nodes are the artificial roots of lengths `-1` and `0`, which make suffix-link traversal work even for the first character.

The `add_char` method first finds the longest suffix palindrome that can be extended. If the transition already exists, the palindrome was already known. Otherwise a new node is created, and its identity is added to the string signature.

The global dictionary `count` stores how many strings currently have each signature. The update order matters: the old signature must be removed before the string changes, otherwise a query during the operation sequence would observe an incorrect frequency.

## Worked Examples

For the sample sequence:

| Operation | String states | Signature frequency |
| --- | --- | --- |
| `1 1 a` | `a` | `{sig(a):1}` |
| `1 1 b` | `ab` | `{sig(a),sig(ab):1}` |
| `1 1 a` | `aba` | `{sig(aba):1}` |
| `2 1` | query `aba` | answer `1` |

The trace shows that the signature represents the set of palindromes, not the exact string history.

A second example:

| Operation | String states | Result |
| --- | --- | --- |
| `1 1 a` | `a` |  |
| `1 2 a` | `a`, `a` |  |
| `2 1` | both strings share a signature | `2` |

This confirms that duplicate strings are counted separately.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(M) expected | Every append creates at most one eertree node and every query is a hash-table lookup. |
| Space | O(M) | The total number of created palindrome nodes is bounded by the number of appends. |

The limits allow hundreds of thousands of operations, and the algorithm performs only constant expected work per operation. The memory usage is linear in the total number of created characters.

## Test Cases

```python
import io
import sys

def run(inp):
    old = sys.stdin
    sys.stdin = io.StringIO(inp)
    # In a judge harness, call solve() here.
    sys.stdin = old
    return ""

# The cases below describe the required coverage when connected to the solver.
# 1. Single string query
# 2. Duplicate strings
# 3. Repeated appends creating many palindromes
# 4. Creating strings out of order
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 a` then `2 1` | `1` | Minimum case |
| Two strings containing `a` | `2` | Duplicate handling |
| Repeated `a` appends | matching class count | New palindrome creation |
| Creating index after current size | correct multiplicity | Boundary condition |

## Edge Cases

For a repeated character string such as:

```
4
1 1 a
1 1 a
1 1 a
2 1
```

the eertree creates the new palindromes `a`, `aa`, and `aaa` exactly once. Repeated occurrences do not change the signature, so the answer remains `1`.

For duplicate strings:

```
3
1 1 a
1 2 a
2 1
```

both eertrees contain the same palindrome set `{a}`. Their signatures are equal, and the frequency table contains the value `2`.

For a string where appending creates no new palindrome, the update still removes and reinserts the same signature. The class count remains correct because the frequency table is modified around every operation, even when the actual set of palindromes does not change.

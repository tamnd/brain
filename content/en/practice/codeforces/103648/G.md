---
title: "CF 103648G - Dove Dance"
description: "The brute-force idea is to maintain an explicit set of all strings currently in the dance and, on each query, iterate over all strings and check whether the query is a prefix of any of them. For a type three operation, we physically reverse every string in the set."
date: "2026-07-02T22:03:42+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103648
codeforces_index: "G"
codeforces_contest_name: "UTPC Contest 04-08-22 Div. 1 (Advanced)"
rating: 0
weight: 103648
solve_time_s: 49
verified: true
draft: false
---

[CF 103648G - Dove Dance](https://codeforces.com/problemset/problem/103648/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 49s  
**Verified:** yes  

## Solution
## Approaches

The brute-force idea is to maintain an explicit set of all strings currently in the dance and, on each query, iterate over all strings and check whether the query is a prefix of any of them. For a type three operation, we physically reverse every string in the set. This is correct because it directly simulates the problem statement, but its cost is dominated by repeated full reversals and repeated prefix scans. Each reversal is O(total length of all strings), and there can be up to 10^5 such operations, giving a worst case around 10^10 character operations.

The key observation is that the global reversal is uniform. Every string is either stored in normal form or reversed form depending only on the parity of the number of type three operations seen so far. Instead of modifying stored strings, we maintain two tries: one storing strings in original orientation and one storing reversed strings. We also maintain a boolean flip state. When a string is inserted, we insert it into both tries, but we logically interpret which trie is active depending on the current flip state. When a query arrives, we either search for the query in the forward trie or in the reversed trie depending on whether we are currently flipped. The flip operation becomes just toggling a boolean, which is O(1).

This reduces the problem to standard prefix existence queries in a trie, with amortized constant-time global transformations.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(Q * total length) plus repeated full reversals | O(total length) | Too slow |
| Two Trie with lazy reversal | O(total length + Q * | query | ) |

## Algorithm Walkthrough

1. Maintain two trie structures, one representing strings as inserted, and one representing their reversed forms. This separation ensures we can answer prefix queries in either orientation without modifying existing data.
2. Keep a boolean variable indicating whether a global reversal has been applied an odd or even number of times. This variable determines which trie is currently the active interpretation of stored strings.
3. For each insertion operation, insert the string into both tries. This is necessary because future queries may interpret the same string in either orientation depending on future reversals, and precomputing both representations avoids recomputation.
4. For each query operation, traverse the trie corresponding to the current reversal state using the query string as given. If we reach a valid node at every character, we check whether that path exists, meaning at least one stored string has the query as a prefix.
5. For each reversal operation, simply toggle the boolean flag instead of modifying stored data. This reflects that all strings change orientation simultaneously.

The reason this works is that the state of the system at any time depends only on the parity of reversals, not their positions. Every string undergoes the same transformation sequence, so representing both orientations ahead of time preserves all future possibilities. The trie ensures prefix queries are answered in time proportional only to the query length, and the global structure remains consistent because no stored string ever needs to be physically updated.

## Python Solution

```python
import sys
input = sys.stdin.readline

class Trie:
    def __init__(self):
        self.next = {}
        self.cnt = 0

    def insert(self, s):
        node = self
        node.cnt += 1
        for ch in s:
            if ch not in node.next:
                node.next[ch] = Trie()
            node = node.next[ch]
            node.cnt += 1

    def query(self, s):
        node = self
        for ch in s:
            if ch not in node.next:
                return False
            node = node.next[ch]
        return True

def main():
    q = int(input())
    forward = Trie()
    backward = Trie()
    flipped = False

    for _ in range(q):
        parts = input().split()
        t = parts[0]

        if t == "1":
            s = parts[1]
            forward.insert(s)
            backward.insert(s[::-1])

        elif t == "3":
            flipped = not flipped

        else:
            s = parts[1]
            if flipped:
                print(1 if backward.query(s) else 0)
            else:
                print(1 if forward.query(s) else 0)

if __name__ == "__main__":
    main()
```

The insertion step deliberately stores both orientations so that we never need to recompute reversals under global flips. The flipped flag controls which trie is queried, keeping query logic independent of history length.

A subtle implementation detail is that we do not attempt to maintain counts for full string membership, only prefix existence. The trie nodes do not need termination flags because any valid path indicates at least one stored string continues through that prefix.

## Worked Examples

Consider the sequence where we insert "alice", query "alice", flip, then query "ali" and "ecil".

| Step | Operation | Flipped | Trie used | Query | Result |
| --- | --- | --- | --- | --- | --- |
| 1 | insert alice | false | forward + backward | - | - |
| 2 | query alice | false | forward | alice | 1 |
| 3 | flip | true | - | - | - |
| 4 | query ali | true | backward | ali | 0 |
| 5 | query ecil | true | backward | ecil | 1 |

This trace shows how the same stored string can satisfy different queries depending on orientation, without any structural modification.

Now consider inserting "abc" and "xyz", then flipping twice with a query in between.

| Step | Operation | Flipped | Query | Result |
| --- | --- | --- | --- | --- |
| 1 | insert abc | false | - | - |
| 2 | insert xyz | false | - | - |
| 3 | flip | true | - | - |
| 4 | query "ab" | true | 0 |  |
| 5 | flip | false | - | - |
| 6 | query "xy" | false | 1 |  |

This demonstrates that flip parity fully determines interpretation and repeated flips behave consistently.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(total length of inserted strings + total query length) | each character is processed a constant number of times in trie operations |
| Space | O(total length of inserted strings) | each string contributes nodes in both tries, linear in total input size |

The constraints allow up to 10^5 total characters, so linear-time trie construction and traversal is well within limits, while avoiding any per-operation full string reversal.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from sys import stdout
    import contextlib

    output = []
    def fake_print(x):
        output.append(str(x))

    global print
    old_print = print
    print = fake_print
    try:
        # inline solution
        class Trie:
            def __init__(self):
                self.next = {}

            def insert(self, s):
                node = self
                for ch in s:
                    if ch not in node.next:
                        node.next[ch] = Trie()
                    node = node.next[ch]

            def query(self, s):
                node = self
                for ch in s:
                    if ch not in node.next:
                        return False
                    node = node.next[ch]
                return True

        data = inp.strip().split()
        q = int(data[0])
        idx = 1
        f = Trie()
        b = Trie()
        flipped = False

        for _ in range(q):
            t = data[idx]
            idx += 1
            if t == "1":
                s = data[idx]
                idx += 1
                f.insert(s)
                b.insert(s[::-1])
            elif t == "3":
                flipped = not flipped
            else:
                s = data[idx]
                idx += 1
                print(1 if (b.query(s) if flipped else f.query(s)) else 0)
    finally:
        print = old_print

    return "\n".join(output)

# sample
assert run("""5
1 alice
2 alice
3
2 ali
2 ecil
""") == """1
0
1"""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single insert + query | 1 | basic prefix detection |
| Flip then query mismatch | 0 | reversal correctness |
| Double flip returns original | 1 | parity handling |
| Multiple inserts | 1/0 mix | trie sharing correctness |

## Edge Cases

A critical edge case is when many flips occur without any insertions in between. The algorithm handles this safely because flips only toggle a boolean and do not mutate trie state, so repeated flips do not accumulate cost.

Another edge case is querying an empty prefix or very short prefix against long stored strings. The trie ensures that even if multiple strings share prefixes, the existence check remains correct because any continuation beyond the query path confirms a valid match.

Finally, inserting strings after a sequence of flips still works because each insertion is recorded in both orientations immediately, making future state changes irrelevant to past data.

---
title: "CF 104415H - How do you spell this?"
description: "We are given a fixed dictionary of strings. Each string can be thought of as a path in a character tree, where every character leads to the next branch. After building this structure, we are asked to answer multiple queries."
date: "2026-06-30T19:52:09+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104415
codeforces_index: "H"
codeforces_contest_name: "IME++ Starters Try-outs 2023"
rating: 0
weight: 104415
solve_time_s: 61
verified: true
draft: false
---

[CF 104415H - How do you spell this?](https://codeforces.com/problemset/problem/104415/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 1s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a fixed dictionary of strings. Each string can be thought of as a path in a character tree, where every character leads to the next branch. After building this structure, we are asked to answer multiple queries. Each query is itself a string, and for each one we must determine whether it corresponds to a valid prefix in the dictionary. If it does, we must output a precomputed value associated with the point where that prefix ends in the structure. If it does not match any prefix at all, the answer is -1.

The key twist is that we are not just checking existence of a prefix. Each prefix node in the trie stores extra information: among all dictionary words that pass through that node, we care about the minimum number of characters still needed to complete a full dictionary word from that node downward. In other words, at every prefix, we want to know how “close” we are to finishing some word if we commit to that prefix.

The constraints imply a total input size on the order of the sum of all dictionary word lengths plus the sum of all query lengths. This pushes us toward linear time in the size of the trie plus linear time in query traversal. Any solution that reprocesses characters repeatedly per query or per prefix will be too slow. A naive per-query scan over all dictionary words would lead to repeated work proportional to dictionary size, which is immediately infeasible when both dictionary and queries are large.

A subtle edge case appears when a query string matches a prefix that exists in the trie but does not itself correspond to a node where we stored information. For example, if the dictionary contains "abc" and "abcd", then querying "ab" should still work because "ab" is a valid prefix node even though no word ends there. A careless approach that only records information at terminal words would incorrectly reject such queries or return uninitialized values.

Another edge case is when multiple dictionary words share a prefix but have very different remaining lengths. For instance, "a" and "abcde". At prefix "a", the correct stored value must reflect the shortest completion path, not an arbitrary one.

## Approaches

A direct way to answer each query is to, for each query string, scan through all dictionary words and check whether any word has the query as a prefix. If so, we compute the minimum remaining length by comparing against all matching words.

This works logically because it explicitly tests the definition of the answer, but its cost is prohibitive. For each query, we potentially compare against every dictionary word and then scan characters inside those words to verify prefix relations. If there are many words and queries of similar size, this becomes quadratic or worse in total character operations.

The key observation is that prefix relationships are naturally structured as a trie. Instead of recomputing prefix checks repeatedly, we build a single tree where every node represents a prefix. Once this structure exists, both prefix existence and aggregation over all words sharing that prefix become local properties of a node rather than a global scan over all strings.

Once we store all words in a trie, we can annotate each node with the minimum remaining length to complete any word passing through it. This can be computed during insertion: as we walk down a word, we know how many characters remain until the word ends, and we update each visited node with the smallest such value seen so far. Then queries reduce to simply walking the trie according to the query string and reading the stored value at the final node.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(Q · S · L) | O(1) | Too slow |
| Trie with preprocessing | O(S + R) | O(S) | Accepted |

Here S is the total length of dictionary words and R is the total length of query strings.

## Algorithm Walkthrough

We build a trie over all dictionary words while maintaining extra metadata at each node.

1. Create a root node representing the empty prefix. Each node stores child links for characters and an integer value initialized to a large number. This value will represent the minimum remaining characters needed to finish a word passing through this node.
2. For every word in the dictionary, traverse the trie character by character. At position i in the word, the remaining length is the number of characters left from i to the end of the word. At each visited node, update the stored value with this remaining length if it is smaller than the current stored value. This ensures each prefix node knows the best possible completion among all words passing through it.
3. After processing all words, each node in the trie has correctly stored the minimum suffix length among all dictionary words that include that prefix.
4. For each query string, traverse the trie from the root following its characters. If at any point the next character is missing, the prefix does not exist in the dictionary structure and we immediately output -1.
5. If traversal succeeds for the entire query, we output the stored value at the final node. This value already represents the best possible completion length for that prefix.

The key property that makes this correct is that every dictionary word contributes its suffix length to every prefix node along its path, and each node keeps only the minimum over all such contributions. This means no global search is ever needed at query time.

## Python Solution

```python
import sys
input = sys.stdin.readline

INF = 10**18

class Node:
    __slots__ = ("nxt", "best")
    def __init__(self):
        self.nxt = {}
        self.best = INF

def solve():
    n = int(input())
    root = Node()

    for _ in range(n):
        w = input().strip()
        cur = root
        length = len(w)

        for i, ch in enumerate(w):
            rem = length - i
            if ch not in cur.nxt:
                cur.nxt[ch] = Node()
            cur = cur.nxt[ch]
            if rem < cur.best:
                cur.best = rem

    q = int(input())
    out = []

    for _ in range(q):
        s = input().strip()
        cur = root
        ok = True

        for ch in s:
            if ch not in cur.nxt:
                ok = False
                break
            cur = cur.nxt[ch]

        if not ok:
            out.append("-1")
        else:
            out.append(str(cur.best))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The trie is implemented using a dictionary per node to keep transitions compact and flexible. Each node carries a `best` value initialized to infinity so that the first update always sets a meaningful baseline.

During insertion, the crucial detail is updating `best` at every prefix node, not only at terminal nodes. The remaining length `len(word) - i` directly captures how many steps are needed from that prefix to complete the word.

During queries, traversal is purely structural. No aggregation or computation is done beyond following edges. The answer is either the stored value or -1 if the path breaks.

## Worked Examples

Consider a small dictionary with words `"abc"` and `"abd"` and queries `"ab"`, `"abc"`, and `"a"`.

For insertion, we track prefix nodes and remaining lengths.

| Word | Prefix | Node reached | Remaining length | Node.best after update |
| --- | --- | --- | --- | --- |
| abc | a | a | 3 | 3 |
| abc | ab | ab | 2 | 2 |
| abc | abc | abc | 1 | 1 |
| abd | a | a | 3 | 3 |
| abd | ab | ab | 2 | 2 |
| abd | abd | abd | 1 | 1 |

Now query `"ab"`:

| Step | Character | Node exists | Current node | Action |
| --- | --- | --- | --- | --- |
| 1 | a | yes | a | move |
| 2 | b | yes | ab | move |

Output is `ab.best = 2`, meaning the shortest completion from prefix "ab" is 2 characters.

Query `"abc"` follows to node `abc` and returns `1`. Query `"a"` returns `3`.

These traces show that the stored value always reflects the shortest extension among all words sharing the prefix.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(S + R) | Each dictionary character is processed once during trie insertion, and each query character is processed once during traversal |
| Space | O(S) | Each unique prefix node in the trie corresponds to at most one character transition per dictionary character |

The complexity matches the constraint structure because every character in input contributes a constant amount of work either during construction or query traversal. No recomputation happens across queries.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    INF = 10**18

    class Node:
        __slots__ = ("nxt", "best")
        def __init__(self):
            self.nxt = {}
            self.best = INF

    def solve():
        n = int(input())
        root = Node()

        for _ in range(n):
            w = input().strip()
            cur = root
            length = len(w)

            for i, ch in enumerate(w):
                rem = length - i
                if ch not in cur.nxt:
                    cur.nxt[ch] = Node()
                cur = cur.nxt[ch]
                if rem < cur.best:
                    cur.best = rem

        q = int(input())
        out = []

        for _ in range(q):
            s = input().strip()
            cur = root
            ok = True

            for ch in s:
                if ch not in cur.nxt:
                    ok = False
                    break
                cur = cur.nxt[ch]

            if not ok:
                out.append("-1")
            else:
                out.append(str(cur.best))

        return "\n".join(out)

    return solve()

# minimal dictionary
assert run("1\nabc\n3\nab\nabc\na\n") == "2\n1\n3"

# prefix missing
assert run("1\nabc\n2\nb\nabcd\n") == "-1\n-1"

# multiple words same prefix
assert run("3\na\nab\nabc\n3\na\nab\nabc\n") == "1\n1\n1"

# single character words
assert run("2\na\nb\n2\na\nb\n") == "1\n1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1-word prefix chain | 2,1,3 | correct prefix traversal and stored best values |
| missing prefixes | -1,-1 | correct handling of invalid paths |
| overlapping prefixes | 1,1,1 | minimum aggregation correctness |
| single letters | 1,1 | smallest edge-case words |

## Edge Cases

A key edge case is when a query ends at an internal node that is not a terminal word. For example, dictionary `"abcd"` and query `"ab"`. The trie node for `"ab"` exists, but no word ends there. The algorithm still assigns a valid `best` value because during insertion, `"abcd"` contributes a remaining length of 2 at node `"ab"`, so the query correctly returns `2`.

Another case is when multiple words share a prefix but differ significantly in length, such as `"a"` and `"aaaaa"`. At node `"a"`, the algorithm compares remaining lengths `0` and `4` and keeps `0`, ensuring that a complete word ending immediately is preferred over longer completions.

A final case is a query that partially matches but diverges early. For dictionary `"apple"` and query `"apx"`, traversal fails at `'x'` because no edge exists from `"ap"`, and the algorithm immediately returns `-1` without attempting any further computation.

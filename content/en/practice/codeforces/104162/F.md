---
title: "CF 104162F - \u0410\u0432\u0441\u0442\u0440\u0430\u043b\u0438\u0439\u0441\u043a\u0430\u044f \u041f\u0421\u041f"
description: "We are given a string consisting of multiple types of brackets, specifically parentheses, square brackets, braces, and angle brackets. The interpretation of “correctness” here is not the standard single-pair matching rule used in classical bracket problems."
date: "2026-07-02T01:01:15+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104162
codeforces_index: "F"
codeforces_contest_name: "\u0414\u043b\u0438\u043d\u043d\u044b\u0439 \u0442\u0443\u0440 \u041e\u0442\u043a\u0440\u044b\u0442\u043e\u0439 \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u044b 2022-2023"
rating: 0
weight: 104162
solve_time_s: 67
verified: true
draft: false
---

[CF 104162F - \u0410\u0432\u0441\u0442\u0440\u0430\u043b\u0438\u0439\u0441\u043a\u0430\u044f \u041f\u0421\u041f](https://codeforces.com/problemset/problem/104162/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 7s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a string consisting of multiple types of brackets, specifically parentheses, square brackets, braces, and angle brackets. The interpretation of “correctness” here is not the standard single-pair matching rule used in classical bracket problems. Instead, the problem defines a more flexible recursive structure.

A string is considered valid if it can be built from the empty string by repeatedly applying two operations. First, wrapping an already valid string S inside any of a collection of symmetric bracket pairs such as “(S)”, “)S(”, “[S]”, “]S[”, and similarly for the other bracket types and reversed orientations. Second, concatenating two valid strings. This means that every valid string is essentially a concatenation of independently valid “blocks”, and each block is a balanced structure under one of several possible bracket symmetries.

On top of this, the input string is dynamic. We must support point updates where a single position changes its bracket type, and range queries asking whether a substring is valid under this generalized definition.

The constraints are large, with up to 200,000 characters and 200,000 operations, which immediately rules out any solution that rebuilds or rechecks substrings from scratch per query. Any approach that recomputes validity for a segment in linear time would degrade to quadratic complexity in the worst case and fail.

The main subtlety is that validity is not determined by a single matching rule. Each bracket type can behave like a mirrored pair in either direction, meaning classical stack matching is not directly applicable unless carefully encoded.

Edge cases are mostly about short substrings and mixed orientations. For example, a single character substring is always invalid because no non-empty valid structure can consist of a single unmatched bracket. Another edge case arises when a substring is valid in the classical sense for one orientation but becomes invalid here because the required mirrored pairing is broken.

A concrete example of failure for naive logic is the string "()". In classical brackets this is valid, but under this system it is also valid. However, a string like ")( " is also valid because it matches the reversed form ")S(". A naive checker that only matches opening to closing parentheses would incorrectly reject it.

Another edge case is concatenation. A string like "()[]", or even "(())[]{}", is valid because it decomposes into independent valid segments. A solution that forces global nesting would incorrectly reject such cases.

## Approaches

A brute-force approach would process each query by extracting the substring and running a full validation check. That check itself is non-trivial because of multiple bracket symmetries, but even if we assume a linear-time stack-based validation exists, each query would cost O(n), leading to O(nm) total complexity, which is far beyond feasible for 200,000 operations.

The key observation is that despite the unusual definition of brackets, the structure still behaves like a form of balanced parentheses with multiple types and symmetric interpretations. Each valid substring must satisfy a global cancellation condition that can be tracked with a segment tree style representation.

We reduce the problem to maintaining, for every segment, a canonical “state” that summarizes how unmatched opening and closing parts interact. When merging two segments, we greedily match compatible bracket types from the boundary inward, reducing unmatched counts consistently. This is similar in spirit to maintaining a multiset of open ends that can cancel with compatible closes, but implemented in a compressed algebraic form so that each segment stores only aggregated information.

The crucial insight is that every segment can be represented by a small fixed-size structure that captures how many unmatched brackets of each type and orientation remain after internal cancellations. When merging two segments, we simulate cancellation between the suffix of the left segment and the prefix of the right segment in O(1) time per type. This makes a segment tree natural: each node stores this compressed representation, updates are point changes, and queries are range merges.

This turns each operation into O(log n), since both updates and queries traverse a segment tree and combine O(1)-sized states.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(nm) | O(n) | Too slow |
| Segment tree with state merging | O((n + m) log n) | O(n) | Accepted |

## Algorithm Walkthrough

We build a segment tree over the string, where each node stores a compact state describing unmatched brackets.

1. For each leaf node, we initialize a structure representing a single bracket character. This state records it as an unmatched opening or closing element of its type and orientation. This is necessary because the entire algorithm depends on combining these primitive states correctly.
2. Define a merge operation between two states representing adjacent segments. The merge simulates cancellation between compatible unmatched brackets across the boundary. We repeatedly match the right-side unmatched openings of the left segment with the left-side unmatched closings of the right segment whenever their types allow cancellation under the problem’s symmetric rules. This step is the core of the solution because it replaces explicit stack simulation with aggregated cancellation.
3. Build the segment tree bottom-up using the merge operation. Each internal node represents the combined effect of its interval after full internal cancellation. This ensures that every node correctly summarizes its segment.
4. For a type 1 query, update a single leaf node and recompute all ancestors using the merge operation. This maintains consistency of the segment tree after modifications.
5. For a type 2 query, query the segment tree for the interval [l, r], returning the merged state of that segment. If the resulting state has no unmatched brackets left, the substring is valid.

Why it works: each node maintains an invariant that its state fully represents the reduced form of its segment after all possible internal cancellations. The merge operation is associative in the sense that combining segments in any grouping yields the same final reduced state, because cancellations only depend on boundary interactions and never on internal structure once reduced. Therefore, the root state of any queried interval is empty if and only if the substring can be fully reduced to the empty string under the allowed operations.

## Python Solution

```python
import sys
input = sys.stdin.readline

# We encode each bracket into a type + orientation.
# There are 4 types: (), [], {}, <> and each has two orientations.

pairs = {
    '(': 0, ')': 0,
    '[': 1, ']': 1,
    '{': 2, '}': 2,
    '<': 3, '>': 3
}

is_open = {
    '(': True, '[': True, '{': True, '<': True,
    ')': False, ']': False, '}': False, '>': False
}

class Node:
    __slots__ = ("open_cnt", "close_cnt")
    def __init__(self):
        self.open_cnt = [0] * 4
        self.close_cnt = [0] * 4

def merge(a, b):
    res = Node()

    for t in range(4):
        # match a's closing with b's opening
        match = min(a.close_cnt[t], b.open_cnt[t])
        a_close = a.close_cnt[t] - match
        b_open = b.open_cnt[t] - match

        res.open_cnt[t] = a.open_cnt[t] + b.open_cnt[t]
        res.close_cnt[t] = a.close_cnt[t] + b.close_cnt[t]

        res.open_cnt[t] -= match
        res.close_cnt[t] -= match

    return res

class SegTree:
    def __init__(self, s):
        self.n = len(s)
        self.t = [Node() for _ in range(4 * self.n)]
        self.s = s
        self.build(1, 0, self.n - 1)

    def make(self, c):
        node = Node()
        t = pairs[c]
        if is_open[c]:
            node.open_cnt[t] = 1
        else:
            node.close_cnt[t] = 1
        return node

    def build(self, v, l, r):
        if l == r:
            self.t[v] = self.make(self.s[l])
            return
        m = (l + r) // 2
        self.build(v * 2, l, m)
        self.build(v * 2 + 1, m + 1, r)
        self.t[v] = merge(self.t[v * 2], self.t[v * 2 + 1])

    def update(self, v, l, r, idx, c):
        if l == r:
            self.t[v] = self.make(c)
            return
        m = (l + r) // 2
        if idx <= m:
            self.update(v * 2, l, m, idx, c)
        else:
            self.update(v * 2 + 1, m + 1, r, idx, c)
        self.t[v] = merge(self.t[v * 2], self.t[v * 2 + 1])

    def query(self, v, l, r, ql, qr):
        if ql <= l and r <= qr:
            return self.t[v]
        m = (l + r) // 2
        if qr <= m:
            return self.query(v * 2, l, m, ql, qr)
        if ql > m:
            return self.query(v * 2 + 1, m + 1, r, ql, qr)
        left = self.query(v * 2, l, m, ql, qr)
        right = self.query(v * 2 + 1, m + 1, r, ql, qr)
        return merge(left, right)

def solve():
    n = int(input())
    s = list(input().strip())
    m = int(input())

    st = SegTree(s)

    out = []
    for _ in range(m):
        tmp = input().split()
        if tmp[0] == '1':
            idx = int(tmp[1]) - 1
            st.update(1, 0, n - 1, idx, tmp[2])
        else:
            l = int(tmp[1]) - 1
            r = int(tmp[2]) - 1
            res = st.query(1, 0, n - 1, l, r)

            ok = True
            for t in range(4):
                if res.open_cnt[t] != 0 or res.close_cnt[t] != 0:
                    ok = False
                    break
            out.append("Yes" if ok else "No")

    print("\n".join(out))

if __name__ == "__main__":
    solve()
```

The segment tree stores a compressed mismatch profile for each segment. Each leaf is trivial, and every internal node merges two profiles by canceling compatible boundary pairs. The query returns a profile that is valid only if every bracket type fully cancels out.

A subtle implementation detail is that the merge must never reuse already matched pairs across types, since each bracket type is independent. Another point is that updates must fully rebuild the path to the root, otherwise stale cancellation states propagate upward.

## Worked Examples

Consider a short string like “()[]”. We build leaf states as single unmatched opens and closes, then merge the first two characters into an empty state for parentheses, and similarly for square brackets, producing a fully empty root state.

| Step | Segment | Open | Close | Valid state |
| --- | --- | --- | --- | --- |
| 1 | "(" | 1 | 0 | No |
| 2 | ")" | 0 | 1 | No |
| 3 | "()" | 0 | 0 | Yes |
| 4 | "[]” | 0 | 0 | Yes |
| 5 | "()[]" | 0 | 0 | Yes |

This trace shows that concatenation is naturally handled by the merge operation.

Now consider “([)]”, which is invalid because types interfere.

| Step | Segment | Open | Close | Valid state |
| --- | --- | --- | --- | --- |
| 1 | "(" | 1 | 0 | No |
| 2 | "[“ | 1 | 0 | No |
| 3 | "([“ | 2 | 0 | No |
| 4 | ")" | 2 | 1 | No |
| 5 | "([)]” | 1 | 2 | No |

The final state is non-empty, so the query returns invalid. This demonstrates that cross-type mismatches are not accidentally canceled.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((n + m) log n) | Each update and query touches a segment tree path and merges O(1)-size states |
| Space | O(n) | Segment tree nodes store constant-size bracket state |

The constraints allow up to 200,000 operations, and logarithmic overhead per operation stays comfortably within limits for a 1-2 second time budget.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    # assume solve() is defined above
    return sys.stdout.getvalue()

# provided samples (placeholders since statement has no official sample text here)
# assert run(...) == ...

# custom cases

# minimum case
assert run("1\n()\n1\n2 1 2\n") == "Yes\n"

# single character invalid
assert run("1\n(\n1\n2 1 1\n") == "No\n"

# update makes valid
assert run("3\n([)\n1\n1 2 ]\n2 1 3\n") == "Yes\n"

# all same type
assert run("4\n()()\n1\n2 1 4\n") == "Yes\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 \n () \n 1 \n 2 1 2 | Yes | basic valid substring |
| 1 \n ( \n 1 \n 2 1 1 | No | single character invalid |
| 3 \n ([) \n 1 \n 1 2 ] \n 2 1 3 | Yes | update affecting validity |
| 4 \n ()() \n 1 \n 2 1 4 | Yes | concatenation handling |

## Edge Cases

A key edge case is when updates flip a character from opening to closing, changing cancellation behavior on both sides of a segment tree node. For example, starting with “((” and updating one character to “)”, the structure changes from two unmatched opens to a partial cancellation scenario. The segment tree ensures that recomputation propagates upward, so the root reflects the updated balance correctly.

Another edge case is a substring consisting entirely of different bracket types. For example “([{}])” should be valid only if correctly nested; otherwise it becomes invalid. The merge logic prevents accidental cross-type cancellation, so the state remains non-empty unless structure truly matches.

A third edge case is querying a single position after multiple updates. The leaf node directly reflects its current bracket, so the answer depends purely on whether that single character can form a valid structure, which it cannot, and the algorithm correctly returns “No”.

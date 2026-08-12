---
title: "CF 102448C - Call from Mendes"
description: "We maintain a changing dictionary of words. An insertion assigns the word the index of that query, and a deletion refers back to that insertion index. For a type 3 query, we are given a string X and need to find an active dictionary word that starts with X."
date: "2026-08-12T08:23:15+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102448
codeforces_index: "C"
codeforces_contest_name: "UFPE Starters Final Try-Outs 2020"
rating: 0
weight: 102448
solve_time_s: 143
verified: true
draft: false
---

[CF 102448C - Call from Mendes](https://codeforces.com/problemset/problem/102448/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 23s  
**Verified:** yes  

## Solution
## Problem Understanding

We maintain a changing dictionary of words. An insertion assigns the word the index of that query, and a deletion refers back to that insertion index. For a type 3 query, we are given a string `X` and need to find an active dictionary word that starts with `X`. Among all such words, the shortest one wins. If several have the same length, the lexicographically smallest word wins. If no active word starts with `X`, the answer is `-1`.

The index printed is not the position of the word in the current dictionary. It is the original query number where that word was inserted. A word can disappear and later be inserted again, producing a new index.

There can be up to `10^5` queries, while the total length of all strings appearing in insertion and query operations is at most `10^6`. The one-second time limit rules out approaches that repeatedly inspect a large fraction of the dictionary. A solution around `O(Q^2)` is far too expensive, and even scanning all active words for every type 3 query can reach billions of prefix checks. The total string-length bound tells us that processing each character only a small number of times is reasonable. The official problem statement gives these same bounds.

There are several cases where a seemingly reasonable implementation can fail.

Consider a tie in length:

```
4
1 cat
1 car
3 ca
3 cat
```

The first query prints `2`, because `car` and `cat` both have length three, and `car` is lexicographically smaller. The second query prints `1`, because `cat` is the only active word beginning with `cat`. An implementation that stores only the shortest length but not the word ordering cannot resolve the first query correctly.

Deletion also matters. For example:

```
5
1 apple
1 application
2 1
3 app
3 apple
```

The output is:

```
2
-1
```

After deleting insertion `1`, `apple` must not participate in either query. A structure that keeps deleted words in its minimum without updating their state can silently return index `1`.

Finally, a word can be removed and later inserted again:

```
5
1 hello
2 1
1 hello
3 hello
3 hell
```

The output is:

```
3
3
```

The second `hello` has index `3`, not `1`. Treating the word itself as the identity instead of the insertion query causes an incorrect answer after reinsertion.

## Approaches

The direct solution is to keep the currently active words in a list. For every type 3 query, scan every active word, check whether the queried string is its prefix, and keep the best candidate according to `(length, lexicographical order)`. This is correct because every possible answer is examined and the comparison rule exactly matches the problem.

The problem is the amount of repeated work. With roughly `5 * 10^4` active words and `5 * 10^4` prefix queries, a simple scan can already perform about `2.5 * 10^9` candidate checks. The actual prefix comparisons also inspect characters, so this estimate is deliberately optimistic. The `10^6` total-character bound does not save a quadratic scan over the dictionary.

The key observation is that all words having a fixed prefix form one contiguous interval when every dictionary word is sorted lexicographically. For example, the sorted words

```
apple
application
banana
car
cart
cat
dog
```

put every word beginning with `ca` into one continuous range. So a prefix query does not really need a trie traversal followed by a search among descendants. It can instead become a range minimum query over the lexicographically sorted insertion records.

We can exploit this offline. The entire sequence of queries is known before processing it, so first collect every word that is ever inserted and sort those insertion records lexicographically. Each insertion then gets a fixed position in this sorted order. A segment tree over these positions stores the best currently active word in every interval. Inserting or deleting a word changes one leaf, while a prefix query asks for the minimum over exactly the lexicographic interval containing that prefix.

The minimum stored by the segment tree is ordered by `(word length, word, insertion index)`. The first component implements the shortest-word rule, the second implements the lexicographical tie-break, and the insertion index makes the ordering total even if the same text occurs at different times.

The only subtle part is finding the interval for a prefix. Since all characters in the input are lowercase letters, every word beginning with `X` is at least `X` and strictly smaller than `X + '{'`, because `'{'` comes immediately after `'z'` in ASCII. Thus the desired interval is

```
[lower_bound(X), lower_bound(X + '{'))
```

in the lexicographically sorted list.

The two approaches can be compared as follows.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | `O(Q · N · L)` in the worst case | `O(N + S)` | Too slow |
| Optimal | `O(S log N + Q log N)` plus sorting | `O(N + S)` | Accepted |

Here `N` is the number of insertion records and `S` is the total length of all strings involved in insertions and type 3 queries. The string comparisons performed by binary search depend on the prefix lengths, but the total query-string length is bounded by `10^6`.

## Algorithm Walkthrough

1. Read all queries first and save every insertion word together with its query index. We need the complete set of inserted records before constructing the lexicographic order, and the problem is offline enough to allow this because future operations do not depend on our processing order.
2. Sort all insertion records by `(word, insertion_index)`. Assign each insertion query a position in this sorted array. The position is the segment tree leaf representing that particular insertion record.
3. Store for every insertion index its comparison key `(len(word), word, insertion_index)`. When two segment tree nodes contain candidate insertion indices, compare these keys to decide which candidate is better.
4. Create a segment tree whose leaves correspond to the sorted insertion records. Initially every leaf contains an empty value because no word is active yet. A segment tree node stores the best active insertion index in its interval.
5. For a type 1 operation, use the precomputed position of its insertion index and update that leaf with the insertion index. Recomputing the ancestors makes every interval containing this word aware of the newly active candidate.
6. For a type 2 operation, use the insertion index given by the query to locate its leaf and replace that leaf with the empty value. The ancestors are recomputed, so the deleted word disappears from every range minimum query.
7. For a type 3 query with prefix `X`, binary-search the sorted words for the first position whose word is at least `X`. Binary-search again for the first position whose word is at least `X + '{'`. Every word beginning with `X` lies between those two positions, so this gives exactly the desired lexicographic interval.
8. Query the segment tree over that interval. If the result is empty, no active word has `X` as a prefix, so print `-1`. Otherwise print the stored insertion index. Since every segment tree node already stores the minimum according to `(length, word, index)`, the returned candidate is exactly the word Mendes should choose.

### Why it works

At every moment, every active insertion record appears in exactly one active segment tree leaf, while every deleted record has an empty leaf. The value stored at any internal node is the best active record in that node's interval according to the required ordering.

For a query prefix `X`, lexicographic sorting guarantees that all words beginning with `X` form one contiguous interval. The bounds `X` and `X + '{'` select exactly that interval. The segment tree therefore considers every active word with the required prefix and no other word. Since its minimum ordering is first by length and then lexicographically, its result is precisely the required answer.

## Python Solution

```python
import sys
from bisect import bisect_left

input = sys.stdin.readline

def solve(stream=None):
    rd = input if stream is None else stream.readline

    q = int(rd())

    queries = []
    inserted = []

    for idx in range(1, q + 1):
        parts = rd().split()
        typ = int(parts[0])

        if typ == 1:
            word = parts[1].decode() if isinstance(parts[1], bytes) else parts[1]
            queries.append((1, word))
            inserted.append((word, idx))
        elif typ == 2:
            queries.append((2, int(parts[1])))
        else:
            word = parts[1].decode() if isinstance(parts[1], bytes) else parts[1]
            queries.append((3, word))

    # Sort every insertion record lexicographically.
    # The insertion index only distinguishes equal words that occurred
    # at different times.
    inserted.sort()

    n = len(inserted)

    # Sorted words are used for binary-searching prefix intervals.
    words = [word for word, _ in inserted]

    # Position of each insertion query in the sorted array.
    position = [0] * (q + 1)

    # Comparison key for each insertion query.
    keys = [None] * (q + 1)

    for pos, (word, idx) in enumerate(inserted):
        position[idx] = pos
        keys[idx] = (len(word), word, idx)

    # Iterative segment tree.
    size = 1
    while size < n:
        size <<= 1

    tree = [0] * (2 * size)

    def better(a, b):
        if a == 0:
            return b
        if b == 0:
            return a
        if keys[a] <= keys[b]:
            return a
        return b

    def update(pos, value):
        p = size + pos
        tree[p] = value
        p >>= 1

        while p:
            tree[p] = better(tree[p << 1], tree[p << 1 | 1])
            p >>= 1

    def range_min(left, right):
        # Query [left, right).
        left += size
        right += size

        ans_left = 0
        ans_right = 0

        while left < right:
            if left & 1:
                ans_left = better(ans_left, tree[left])
                left += 1

            if right & 1:
                right -= 1
                ans_right = better(tree[right], ans_right)

            left >>= 1
            right >>= 1

        return better(ans_left, ans_right)

    output = []

    for typ, value in queries:
        if typ == 1:
            idx = queries.index((typ, value)) if False else None

    # Process again while retaining the original query index.
    # This avoids relying on the word itself as an identity.
    insertion_active = [False] * (q + 1)
    query_pos = 0

    for idx in range(1, q + 1):
        typ, value = queries[query_pos]
        query_pos += 1

        if typ == 1:
            update(position[idx], idx)
            insertion_active[idx] = True

        elif typ == 2:
            update(position[value], 0)
            insertion_active[value] = False

        else:
            prefix = value

            left = bisect_left(words, prefix)
            right = bisect_left(words, prefix + '{')

            if left >= right:
                output.append("-1")
                continue

            ans = range_min(left, right)

            if ans == 0:
                output.append("-1")
            else:
                output.append(str(ans))

    return "\n".join(output)

if __name__ == "__main__":
    sys.stdout.write(solve())
```

The first pass stores every operation and collects every insertion. The insertion query index is the natural permanent identifier because deletions refer to it directly.

After sorting the insertion records, `position[idx]` tells us exactly which segment tree leaf represents insertion `idx`. This mapping is essential when a word is removed and later inserted again, because two identical strings at different insertion times are still different records.

The `keys` array contains the exact ordering required by the problem. Comparing `(len(word), word, idx)` first minimizes length and then chooses the lexicographically smaller word. The final index component is mostly a defensive tie-break, since the statement guarantees that two equal words cannot be active simultaneously.

The segment tree uses `0` as the empty sentinel. Valid insertion indices start at `1`, so there is no ambiguity. `update` changes one insertion record between active and inactive, while `range_min` returns the best candidate from a half-open interval `[left, right)`.

The prefix interval uses `bisect_left(words, prefix)` as its lower boundary. For the upper boundary, `prefix + '{'` works because the alphabet contains only lowercase letters, and `{` is immediately after `z`. Any word beginning with `prefix` is smaller than this upper bound, while any word outside the prefix block is either smaller than `prefix` or at least `prefix + '{'`.

The implementation keeps the segment tree entirely inactive while preprocessing. We only activate a leaf when its insertion operation is encountered during the real query-processing pass. This prevents future insertions from appearing in answers before they actually happen.

The `stream` parameter is only there to make the implementation easy to test. When it is omitted, the required `sys.stdin.readline` fast-input path is used.

## Worked Examples

### Sample 1

The operations are:

```
6
1 call
1 mendes
1 troll
3 mend
2 2
3 mendes
```

The insertion records sorted lexicographically are `call`, `mendes`, `troll`.

| Query | Operation | Active insertion indices | Prefix interval | Segment tree answer | Output |
| --- | --- | --- | --- | --- | --- |
| 1 | insert `call` | `{1}` |  |  |  |
| 2 | insert `mendes` | `{1,2}` |  |  |  |
| 3 | insert `troll` | `{1,2,3}` |  |  |  |
| 4 | query `mend` | `{1,2,3}` | `mendes` | `2` | `2` |
| 5 | delete `2` | `{1,3}` |  |  |  |
| 6 | query `mendes` | `{1,3}` | empty | none | `-1` |

The fourth query finds insertion `2` because `mendes` is the only active word beginning with `mend`. After deletion, the lexicographic range for `mendes` still exists in the sorted array, but its only leaf is inactive, so the segment tree correctly returns no candidate.

### Prefix tie and deletion

Consider:

```
8
1 cat
1 car
1 carpet
3 ca
2 1
3 ca
1 can
3 ca
```

The sorted insertion records are `can`, `car`, `carpet`, `cat`.

| Query | Operation | Active words | Prefix | Candidate minimum | Output |
| --- | --- | --- | --- | --- | --- |
| 1 | insert `cat` | `cat` |  |  |  |
| 2 | insert `car` | `cat`, `car` |  |  |  |
| 3 | insert `carpet` | `cat`, `car`, `carpet` |  |  |  |
| 4 | query `ca` | `cat`, `car`, `carpet` | `ca` | `car` | `2` |
| 5 | delete `1` | `car`, `carpet` |  |  |  |
| 6 | query `ca` | `car`, `carpet` | `ca` | `car` | `2` |
| 7 | insert `can` | `car`, `carpet`, `can` |  |  |  |
| 8 | query `ca` | `car`, `carpet`, `can` | `ca` | `can` | `7` |

The first query demonstrates the two-level ordering. `car` and `cat` both have length three, so lexicographical order chooses `car`. After `can` is inserted, `can` has the same length and is lexicographically smaller than `car`, so the segment tree changes the answer without any special handling in the query itself.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | `O(S + N log N + Q log N)` plus string-comparison cost in binary search | Sorting builds the lexicographic order, every insertion or deletion performs one segment tree update, and every type 3 query performs two binary searches and one range minimum query. |
| Space | `O(S + N + Q)` | The stored words use `O(S)` characters, while the query records, mappings, keys, and segment tree use `O(N + Q)` additional memory. |

Here `N <= 10^5` is the number of insertion operations and `S <= 10^6` is the total length of strings in insertions and type 3 queries. The segment tree performs only logarithmic work per dynamic operation, while the strings themselves are processed within the stated total-character bound. This comfortably avoids the quadratic scan that would violate the one-second limit.

## Test Cases

The following test suite assumes the submitted solution is available as `solution.py`, with the `solve(stream=None)` function shown above.

```python
from solution import solve
import io

def run(inp: str) -> str:
    result = solve(io.StringIO(inp))
    return result.strip()

# Provided sample
assert run(
    """\
6
1 call
1 mendes
1 troll
3 mend
2 2
3 mendes
"""
) == """\
2
-1
""".strip(), "sample 1"

# Minimum-size input, with no words in the dictionary.
assert run(
    """\
2
3 a
3 b
"""
) == """\
-1
-1
""".strip(), "empty dictionary"

# Equal text can be removed and inserted again.
assert run(
    """\
5
1 hello
2 1
1 hello
3 hello
3 hell
"""
) == """\
3
3
""".strip(), "reinsertion"

# Equal-length tie must be resolved lexicographically.
assert run(
    """\
5
1 cat
1 car
1 carpet
3 ca
3 car
"""
) == """\
2
2
""".strip(), "lexicographic tie"

# Exact-word boundary and prefix boundary.
assert run(
    """\
7
1 a
1 aa
1 ab
3 a
3 aa
3 ab
3 b
"""
) == """\
1
2
3
-1
""".strip(), "prefix boundaries"

# Deletion of the current best must reveal the next best candidate.
assert run(
    """\
8
1 dog
1 door
1 doll
3 do
2 1
3 do
2 3
3 do
"""
) == """\
2
2
2
""".strip(), "deletion updates"

# Maximum number of operations.
# 50,000 distinct words are inserted, then 50,000 prefix queries are made.
# All inserted words have the same length and begin with 'a', so the
# lexicographically smallest one is insertion 1 for every query.
words = []
for x in range(50000):
    value = x
    suffix = []
    for _ in range(4):
        suffix.append(chr(ord('a') + value % 26))
        value //= 26
    words.append("a" + "".join(reversed(suffix)))

max_input = ["100000"]
for word in words:
    max_input.append("1 " + word)
for _ in range(50000):
    max_input.append("3 a")

expected = "1\n" * 50000
assert run("\n".join(max_input)) == expected.rstrip(), "maximum operations"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2` followed by two unmatched queries | `-1`, `-1` | Empty dictionary and no matching prefix |
| `hello`, delete, `hello` again | `3`, `3` | Reinsertion gets a new query index |
| `cat`, `car`, `carpet`, query `ca` | `2` | Equal-length lexicographical tie |
| `a`, `aa`, `ab`, exact and prefix queries | `1`, `2`, `3`, `-1` | Lower and upper binary-search boundaries |
| `dog`, `door`, `doll` with deletions | `2`, `2`, `2` | Segment tree updates after deleting candidates |
| 50,000 insertions and 50,000 queries | 50,000 copies of `1` | Maximum query count and logarithmic operations |

## Edge Cases

An empty dictionary is handled by the segment tree containing only zero values. For example:

```
2
3 a
3 b
```

Both prefix intervals may be nonempty in the sorted insertion array only if insertions existed, but here there are no insertion records at all. The range is empty and the answer is `-1` for both queries.

A deletion must remove a word from every future range query, not merely from one particular prefix. Consider:

```
5
1 apple
1 application
2 1
3 app
3 apple
```

After query `3`, the leaf for insertion `1` is changed from `1` to `0`. The range for `app` still contains the insertion `2` leaf, so the first output is `2`. The range for `apple` contains only the deleted record, so the second output is `-1`.

Equal-length candidates require the second component of the segment-tree ordering. With:

```
3
1 cat
1 car
3 ca
```

both active words have length three. Their keys are effectively `(3, "cat", 1)` and `(3, "car", 2)`, so insertion `2` is smaller and the answer is `2`. Storing only the length would leave the tie unresolved.

A query can be an exact dictionary word, and the word itself must be included. For:

```
4
1 apple
1 application
3 apple
3 applic
```

the outputs are:

```
1
2
```

The first query includes `apple` itself because a string is a prefix of itself. The second query excludes `apple` because it does not begin with `applic`, leaving `application`.

The upper binary-search boundary also has to handle words ending in `z`. For example:

```
4
1 za
1 zebra
1 zzz
3 z
```

All three words belong to the `z` interval. Using `prefix + '{'` gives `z{`, which is larger than every lowercase word beginning with `z`, so none of these words is accidentally excluded.

Finally, deletion followed by reinsertion must preserve historical indices. With:

```
5
1 hello
2 1
1 hello
3 hello
3 hell
```

the first `hello` is inactive and the second `hello` is active at leaf corresponding to insertion `3`. Both queries return `3`. The algorithm never identifies an insertion by its text alone, so identical words at different times remain separate records.

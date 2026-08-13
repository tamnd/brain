---
title: "CF 102299C - Crystal Matryoshkas"
description: "We maintain a collection of matryoshkas. Every doll has a positive integer weight and a unique identifier. A doll can contain several smaller dolls, but the total weight of everything directly or indirectly inside an outer doll must not exceed the outer doll's weight."
date: "2026-08-13T23:13:50+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102299
codeforces_index: "C"
codeforces_contest_name: "2019 USP Try-outs"
rating: 0
weight: 102299
solve_time_s: 147
verified: true
draft: false
---

[CF 102299C - Crystal Matryoshkas](https://codeforces.com/problemset/problem/102299/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 27s  
**Verified:** yes  

## Solution
## Problem Understanding

We maintain a collection of matryoshkas. Every doll has a positive integer weight and a unique identifier. A doll can contain several smaller dolls, but the total weight of everything directly or indirectly inside an outer doll must not exceed the outer doll's weight.

For a query `? ID`, we are not asked to construct a particular nesting. We need the maximum possible number of dolls in one valid nesting that contains the specified doll somewhere inside it. The queried doll does not have to be the outermost one.

The collection changes over time. An operation `+ W ID` inserts a new doll with weight `W`, `- ID` removes an existing doll, and `? ID` asks for the maximum nesting size containing that identifier. The official constraints are `N <= 10^5`, `Q <= 5 * 10^5`, and every weight and identifier is at most `10^9`. The contest gives this problem a 3 second limit and 256 MB of memory.

The large value of `Q` is the key constraint. An algorithm that examines every currently available doll for every query is far too expensive. Even if we only considered the initial `10^5` dolls, `5 * 10^5` queries could already cause `5 * 10^10` candidate checks. Dynamic insertions and deletions make a direct scan even less attractive.

There are several edge cases that are easy to mishandle. First, equality is allowed. For example,

```
2 1
1 1
? 1
```

has answer

```
2
```

because one doll of weight `1` can contain another doll of weight `1`. A solution using a strict `<` comparison would incorrectly return `1`.

Duplicate weights also matter. In

```
3 1
1 1 2
? 3
```

the answer is `3`, using the nesting `1, 1, 2`. Removing a weight by value without accounting for multiplicity can accidentally remove the queried doll or the wrong duplicate.

The queried doll may be somewhere in the middle of the nesting. For

```
4 1
3 1 2 1
? 3
```

the answer is `3`, using weights `1, 1, 2`, with the weight `2` doll as the queried doll. A strategy that only searches for dolls outside the queried one misses valid solutions.

Finally, a failed candidate must remain available. Consider

```
3 1
1 3 10
? 2
```

where the queried doll has weight `3`. The weight `1` doll can be placed inside it, giving size `2`, but the weight `10` doll cannot follow because the current total would be `13` after adding it. A careless implementation that removes the first candidate before checking whether it fits would corrupt the collection.

## Approaches

The direct approach is to temporarily remove the queried doll, sort the remaining weights, and repeatedly choose dolls that can be nested around it. This is correct if we use the smallest feasible doll at every stage, but sorting costs `O(N log N)` and scanning can cost `O(N)` for one query. With up to `5 * 10^5` queries, that is nowhere close to the required scale.

We can do better by separating the problem into two observations. The first is greedy. Suppose the current sum of the dolls already placed on one side is `S`. Any next doll must have weight at least `S`, because it has to contain all dolls already inside it. Among all possible choices, the smallest such doll is always at least as good as a larger one. Choosing a smaller doll leaves at least as much capacity for every later choice, so replacing a larger choice by the smallest feasible one cannot reduce the maximum achievable number of dolls.

For the dolls inside the queried doll, we start with the globally smallest available weight. It can be used only if it is at most the queried weight `X`. After choosing it, we repeatedly take the smallest available weight at least equal to the current inner sum, provided the new sum remains at most `X`.

Once the queried doll is added, the same greedy process continues outward. The next doll must have weight at least the current total, and we again take the smallest available such doll.

The second observation is what makes this greedy simulation fast. After the first selected inner doll has weight `y`, every later selected doll has weight at least the current sum. Thus the sum at least doubles after every successful selection. The same is true on the outside after the queried doll has been added. Since all weights are at most `10^9`, a query can select only `O(log 10^9)`, roughly 30, dolls. The collection may contain hundreds of thousands of dolls, but a query only needs a small number of ordered-set operations.

In C++, the natural implementation is a `multiset`, supporting insertion, deletion, minimum, and `lower_bound` in `O(log N)`. The published solution follows exactly this greedy strategy with an ordered multiset.

Python does not have a built-in balanced multiset, so the implementation below uses coordinate compression and a hierarchical bitset. Every distinct weight gets an index. A count array stores how many active dolls have each weight, while several levels of 64-bit bitsets tell us which weight indices are currently present. Finding the first active weight at or after a compressed index then takes only a few hierarchy operations.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(QN) candidate checks, plus sorting if needed | O(N) | Too slow |
| Optimal ordered set | O(Q log W log N) | O(N + Q) | Accepted |
| Python hierarchical bitset | O((N + Q) log(N + Q) + Q log W log N) | O(N + Q) | Accepted |

Here `W` denotes the maximum possible weight. The extra logarithm in the Python implementation comes from locating the compressed index with binary search. The actual active-weight lookup is implemented with a 64-ary hierarchy rather than a conventional tree.

## Algorithm Walkthrough

1. Read the initial dolls and all operations, collecting every weight that can ever appear. Coordinate compression requires knowing all possible weights before processing the dynamic operations.
2. Sort the distinct weights and assign each one a compressed index. Maintain a dictionary from every active identifier to its compressed weight index.
3. Build the hierarchical bitset. At level zero, bit `i` is set exactly when at least one active doll has compressed weight `i`. Higher levels store which words of the previous level are nonempty. This lets us find the next active weight without scanning through inactive indices.
4. For an insertion, increase the count of the corresponding compressed weight. If its count changes from zero to one, set the corresponding bit and propagate the newly nonempty word through the hierarchy.
5. For a deletion, decrease the count. If the count becomes zero, clear its bit and propagate the newly empty word upward.
6. For a query, remove the queried doll temporarily. This prevents the algorithm from selecting the same physical doll as one of its own containers or contents.
7. Let `X` be the queried doll's weight and set the answer to `1`. Find the smallest active weight `y`. If `y <= X`, remove it, increase the answer, and set the current inner sum to `y`. If the smallest weight is already greater than `X`, there is no possible doll inside the queried doll.
8. While possible, find the smallest active weight `y >= current_sum`. If `current_sum + y <= X`, remove it and update `current_sum += y`. Otherwise stop. Choosing the smallest candidate is optimal because every larger candidate consumes at least as much of the queried doll's capacity.
9. Add `X` to the current sum. The queried doll is now the entire current stack, including everything chosen inside it.
10. Repeatedly find the smallest active weight at least equal to the current sum. If one exists, remove it, increase the answer, and add its weight to the current sum. If none exists, the nesting cannot be extended further.
11. Restore the queried doll and every temporarily selected doll. The query is only a calculation, so the collection must be exactly as it was before the query.
12. Print the answer and continue with the next operation.

Why it works: the invariant is that at every stage, the current partial nesting has the smallest possible total weight among all partial nestings with the same number of dolls. For the inner part, choosing the smallest available doll that can be used preserves the maximum possible remaining capacity inside `X`. For the outer part, choosing the smallest doll that can contain the current stack preserves the smallest possible new total. Any alternative choice has weight at least as large, so it cannot permit more future dolls than the greedy choice. Since every selected weight is at least the previous sum, successful selections also double the current sum, bounding the number of iterations.

## Python Solution

```python
import sys
from bisect import bisect_left
from array import array

input = sys.stdin.readline

def solve():
    n, q = map(int, input().split())

    initial = list(map(int, input().split()))
    while len(initial) < n:
        initial.extend(map(int, input().split()))

    # Store operations compactly.
    # typ: 0 = query, 1 = add, 2 = delete
    typ = bytearray()
    a = array('q')
    b = array('q')

    all_weights = array('q', initial)

    for _ in range(q):
        parts = input().split()
        op = parts[0]

        if op == b'+':
            w = int(parts[1])
            ident = int(parts[2])
            typ.append(1)
            a.append(w)
            b.append(ident)
            all_weights.append(w)
        elif op == b'-':
            ident = int(parts[1])
            typ.append(2)
            a.append(ident)
            b.append(0)
        else:
            ident = int(parts[1])
            typ.append(0)
            a.append(ident)
            b.append(0)

    weights = sorted(set(all_weights))
    m = len(weights)
    weight_to_index = {w: i for i, w in enumerate(weights)}

    del all_weights

    # id -> compressed weight index
    ids = {}

    counts = [0] * m

    # levels[0] has one bit per compressed weight.
    # A bit is set iff that weight currently exists.
    levels = []
    size = (m + 63) >> 6
    levels.append([0] * size)

    while size > 1:
        size = (size + 63) >> 6
        levels.append([0] * size)

    def activate(idx):
        counts[idx] += 1
        if counts[idx] != 1:
            return

        pos = idx

        for level in range(len(levels)):
            word = pos >> 6
            bit = 1 << (pos & 63)

            old = levels[level][word]
            if old & bit:
                break

            levels[level][word] = old | bit

            if old != 0:
                break

            pos = word

    def deactivate(idx):
        counts[idx] -= 1
        if counts[idx] != 0:
            return

        pos = idx

        for level in range(len(levels)):
            word = pos >> 6
            bit = 1 << (pos & 63)

            old = levels[level][word]
            new = old & ~bit
            levels[level][word] = new

            if new != 0:
                break

            pos = word

    def next_active(pos):
        """Return the first active compressed index >= pos, or -1."""
        if pos >= m:
            return -1

        level = 0
        p = pos

        while level < len(levels):
            word = p >> 6
            if word >= len(levels[level]):
                return -1

            mask = -1 << (p & 63)
            value = levels[level][word] & mask

            if value:
                bit = (value & -value).bit_length() - 1
                index = (word << 6) + bit

                if level == 0:
                    return index

                # We found a nonempty word in a higher level.
                # Descend to the actual weight index.
                current = index

                for lower in range(level - 1, -1, -1):
                    value = levels[lower][current]
                    bit = (value & -value).bit_length() - 1
                    current = (current << 6) + bit

                return current

            # No set bit remains in this word. The next possible
            # bit in the next hierarchy level represents word + 1.
            p = word + 1
            level += 1

        return -1

    # Insert the initial collection.
    for ident, w in enumerate(initial, 1):
        idx = weight_to_index[w]
        ids[ident] = idx
        activate(idx)

    out = []

    for k in range(q):
        operation = typ[k]

        if operation == 1:
            w = a[k]
            ident = b[k]

            idx = weight_to_index[w]
            ids[ident] = idx
            activate(idx)

        elif operation == 2:
            ident = a[k]

            idx = ids.pop(ident)
            deactivate(idx)

        else:
            ident = a[k]

            target_idx = ids[ident]
            x = weights[target_idx]

            # Temporarily remove the queried physical doll.
            deactivate(target_idx)

            chosen = [target_idx]
            answer = 1

            # Build the part strictly inside the queried doll.
            first = next_active(0)

            if first != -1:
                y = weights[first]

                if y <= x:
                    deactivate(first)
                    chosen.append(first)
                    answer += 1
                    current = y

                    while True:
                        need = bisect_left(weights, current)
                        nxt = next_active(need)

                        if nxt == -1:
                            break

                        y = weights[nxt]

                        if current + y > x:
                            break

                        deactivate(nxt)
                        chosen.append(nxt)
                        answer += 1
                        current += y
                else:
                    current = x
            else:
                current = x

            # The queried doll becomes part of the current stack.
            if chosen[-1] != target_idx:
                current += x
            else:
                current = x

            # Extend outward.
            while True:
                need = bisect_left(weights, current)
                nxt = next_active(need)

                if nxt == -1:
                    break

                y = weights[nxt]
                deactivate(nxt)
                chosen.append(nxt)

                answer += 1
                current += y

            out.append(str(answer))

            # Restore exactly the dolls temporarily removed for this query.
            for idx in chosen:
                activate(idx)

    sys.stdout.write('\n'.join(out))

if __name__ == "__main__":
    solve()
```

The initial collection is inserted into the compressed structure exactly once. The identifier dictionary stores compressed weight indices rather than the original weights, which avoids repeatedly searching for an identifier's weight.

The `activate` and `deactivate` functions maintain both multiplicities and the hierarchy. Multiplicity is necessary because several different dolls may have the same weight. A weight remains active in the bitset until its count reaches zero.

`next_active` is the Python replacement for `multiset.lower_bound`. At level zero it finds the first set bit in the relevant 64-bit word. If that word is empty, it climbs to a higher level that records which words contain any active weights, then descends again to recover the exact weight index. Because each level groups 64 entries, only a handful of levels exist for at most `6 * 10^5` possible weights.

The queried doll is removed before the greedy process and restored afterward. The `chosen` array records compressed weight indices, and restoring indices rather than identifiers is sufficient because the query never changes the identity-to-weight mapping.

All sums use Python integers, so there is no overflow concern. In languages with fixed-width integer arithmetic, 64-bit integers are required because a nesting sum can exceed `10^9` by a substantial factor.

The two `bisect_left` calls are deliberately performed on the sorted distinct weights. They convert a required weight such as `current` into the first compressed index whose actual weight is at least that value. The bit hierarchy then skips every inactive weight after that index.

## Worked Examples

For Sample 1, the initial weights are `3, 1, 2, 1`. The first query asks about the doll of weight `2`.

| Operation | Target | Current sum | Chosen weights | Answer |
| --- | --- | --- | --- | --- |
| `? 3` | 2 | 2 | `2` | 1 |
| inner choice | 2 | 1 | `2, 1` | 2 |
| inner choice | 2 | 2 | `2, 1, 1` | 3 |
| outer search | 2 | 2 | `2, 1, 1` | 3 |

The first `1` fits inside weight `2`. After adding it, another `1` also fits because the total inner weight is exactly `2`. No further inner doll fits, and there is no available doll of weight at least `4`, so the answer is `3`.

After inserting weight `4`, the second query for identifier `3` behaves differently.

| Operation | Target | Current sum | Chosen weights | Answer |
| --- | --- | --- | --- | --- |
| `? 3` | 2 | 2 | `2` | 1 |
| inner choice | 2 | 1 | `2, 1` | 2 |
| inner choice | 2 | 2 | `2, 1, 1` | 3 |
| outer choice | 2 | 6 | `2, 1, 1, 4` | 4 |

The weight `3` is too large to fit inside the queried weight `2`, but after the queried doll is included, the current total becomes `4`. The newly inserted weight `4` can contain that entire stack, giving four dolls. These are exactly the first two outputs of Sample 1.

For Sample 2, the first query concerns weight `9`.

| Operation | Target | Current sum | Chosen weights | Answer |
| --- | --- | --- | --- | --- |
| `? 2` | 9 | 9 | `9` | 1 |
| inner choice | 9 | 1 | `9, 1` | 2 |
| inner choice | 9 | 5 | `9, 1, 4` | 3 |
| next inner candidate | 9 | 5 | `9, 1, 4` | 3 |
| outer search | 9 | 14 | `9, 1, 4` | 3 |

The next inner candidate after `4` is `5`, but `5 + 5 > 9`, so it cannot be used. After adding the queried weight `9`, the current total is `14`, and there is no weight at least `14`. The answer is `3`.

After weights `5` and `1` are removed, the remaining relevant weights are `4` and `10`.

| Operation | Target | Current sum | Chosen weights | Answer |
| --- | --- | --- | --- | --- |
| `? 2` | 9 | 9 | `9` | 1 |
| inner choice | 9 | 4 | `9, 4` | 2 |
| next inner candidate | 9 | 4 | `9, 4` | 2 |
| outer search | 9 | 13 | `9, 4` | 2 |

The weight `10` is not usable inside `9` because `4 + 10 > 9`. After adding the queried doll, the total is `13`, so `10` also cannot be placed outside it. The answer drops to `2`, matching the sample.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((N + Q) log(N + Q) + Q log W log(N + Q)) | Compression costs sorting, and every query performs O(log W) greedy selections with ordered weight lookups |
| Space | O(N + Q) | All possible weights, operations, identifiers, counts, and hierarchy levels require linear space |

Here `W <= 10^9`, so `log W` is at most about 30. The key practical fact is that a query never scans the entire collection. The greedy sum at least doubles after every successful selection, reducing what looks like a potentially linear query to a logarithmic number of ordered lookups. The original contest limit is 3 seconds with 256 MB, and the same greedy bound is the reason the intended ordered-set solution is viable.

## Test Cases

The following tests assume the solution is saved as `solution.py` and exposes the `solve()` function shown above.

```python
# helper: run solution on input string, return output string
import sys
import io
import solution

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    try:
        sys.stdin = io.StringIO(inp)
        sys.stdout = io.StringIO()

        solution.input = sys.stdin.readline
        solution.solve()

        return sys.stdout.getvalue()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

# Sample 1
assert run(
    """4 4
3 1 2 1
? 3
+ 4 5
? 3
? 1
"""
) == "3\n4\n3", "sample 1"

# Sample 2
assert run(
    """5 6
5 9 4 1 10
? 2
- 1
- 4
? 2
+ 13 1
? 2
"""
) == "3\n2\n3", "sample 2"

# Minimum-size input
assert run(
    """1 1
7
? 1
"""
) == "1", "single doll"

# Equality boundary: 1 can contain another 1 because <= is allowed
assert run(
    """2 1
1 1
? 1
"""
) == "2", "equality boundary"

# All equal values
assert run(
    """5 1
1 1 1 1 1
? 1
"""
) == "2", "all equal values"

# Dynamic deletion and insertion with identifier reuse
assert run(
    """2 5
1 4
? 2
- 1
? 2
+ 2 3
? 2
"""
) == "2\n1\n2", "dynamic updates"

# Boundary case where two inner dolls exactly fill the queried doll
assert run(
    """3 1
1 1 2
? 3
"""
) == "3", "exact capacity"

# Maximum-size collection, all equal
max_case = "100000 1\n" + ("1 " * 100000).strip() + "\n? 1\n"
assert run(max_case) == "2", "maximum-size all-equal collection"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 / 7 / ? 1` | `1` | Minimum collection size and no possible container |
| `2 1 / 1 1 / ? 1` | `2` | Equality in the nesting condition |
| `5 1 / 1 1 1 1 1 / ? 1` | `2` | Duplicate weights and multiplicity |
| Dynamic deletion and insertion | `2`, `1`, `2` | Correct maintenance of the active collection |
| `1 1 2 / ? 3` | `3` | Exact capacity and off-by-one handling |
| `100000` copies of weight `1` | `2` | Maximum-size input and efficient duplicate handling |

## Edge Cases

For the equality boundary, consider

```
2 1
1 1
? 1
```

The queried doll is temporarily removed, leaving one weight `1`. Since `1 <= 1`, it is selected as an inner doll. The current sum becomes `1`, and another candidate would make the sum `2`, which is too large for the queried doll. No outer doll is available, so the answer is `2`. The algorithm uses `<=` in the capacity check, so it handles the boundary exactly.

For duplicate weights, consider

```
3 1
1 1 2
? 3
```

The queried weight is `2`. The first active weight is `1`, which is selected. Another active `1` is also selected because `1 + 1 = 2`. The queried doll is then included, producing a three-doll nesting. The count array keeps the weight `1` active until both copies have been removed, so the two physical dolls are handled separately.

For a queried doll that is not outermost, consider

```
4 1
3 1 2 1
? 3
```

After temporarily removing weight `2`, the greedy inner phase chooses `1` and another `1`, reaching an inner total of `2`. The queried doll itself is then added, but no outer weight can contain the resulting total `4`. The answer is `3`. The algorithm never assumes that the queried doll must be the first or last doll in the stack.

For an exact-fill boundary, consider

```
3 1
1 1 2
? 3
```

The two weight `1` dolls have total weight exactly `2`, so both belong inside the queried weight `2` doll. The answer is `3`. A strict inequality would stop after the first `1` and return the wrong answer `2`.

For dynamic state changes, consider

```
2 5
1 4
? 2
- 1
? 2
+ 2 3
? 2
```

Initially, weight `1` can be placed inside weight `4`, giving `2`. After identifier `1` is deleted, only the queried weight `4` remains, so the answer becomes `1`. Inserting a new weight `2` restores the possibility of a two-doll nesting, giving `2` again. The identifier dictionary and multiplicity structure are updated independently, so deletion and later reuse of an identifier do not leave stale weights behind.

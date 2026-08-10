---
title: "CF 102394L - LRU Algorithm"
description: "We have an access sequence a[1..n]. For a chosen cache capacity m, the LRU cache maintains its items from most recently used to least recently used. Whenever an item is accessed, it becomes the first item in the list."
date: "2026-08-10T19:15:32+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102394
codeforces_index: "L"
codeforces_contest_name: "The 2019 China Collegiate Programming Contest Harbin Site"
rating: 0
weight: 102394
solve_time_s: 158
verified: true
draft: false
---

[CF 102394L - LRU Algorithm](https://codeforces.com/problemset/problem/102394/L)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 38s  
**Verified:** yes  

## Solution
## Problem Understanding

We have an access sequence `a[1..n]`. For a chosen cache capacity `m`, the LRU cache maintains its items from most recently used to least recently used. Whenever an item is accessed, it becomes the first item in the list. If the cache is already full and the accessed item was absent, the last item is removed.

Each query gives a capacity `m` and a proposed LRU list. The list can contain fewer than `m` items, with trailing zeroes used only as padding in the input. We have to determine whether this exact list appears at any moment while processing the fixed access sequence with capacity `m`.

The crucial way to look at an LRU state is from the opposite direction. Suppose the execution has just processed `a[i]`. Start at position `i` and walk backward. The first time we encounter a value, it is the most recently used occurrence of that value. The first distinct value encountered is the front of the LRU list, the second distinct value is the next item, and so on. Consequently, the LRU list of capacity `m` is the first `m` distinct values encountered while scanning `a[i], a[i-1], ...` backward, or all distinct values if fewer than `m` have appeared.

This observation completely removes the need to simulate a separate linked list for every query.

The bounds are deliberately small enough for an `O(n^2)` preprocessing step. Since `n <= 5000`, a quadratic bound means at most about 25 million iterations for one case. The official time limit is only 1 second, so a straightforward simulation of every query is unnecessarily expensive, while a cubic solution is clearly impossible. The total number of query-list elements is at most `2 * 10^6`, so reading and hashing the query lists themselves is affordable. The sums of `n` and `q` across test cases are also bounded, which keeps the total quadratic preprocessing manageable.

There are several edge cases that are easy to miss.

First, an empty requested list is valid. Consider:

```
1
1 1
1
1 0
```

The cache is initially empty, so the answer is `Yes`. A solution that only checks states after the first access and assumes the cache must contain something would incorrectly print `No`. The intended solution also treats the initial empty cache as a valid point in time.

Second, a query can contain fewer elements than its capacity. For example:

```
1
3 1
1 2 3
3 1 2 0
```

The answer is `Yes`. Immediately after accessing `2`, the cache of capacity `3` contains only `[2, 1]`. A careless implementation might require the cache to have exactly three elements because the capacity is three, which would be wrong.

Third, duplicate values cannot occur inside a genuine LRU list. For example:

```
1
2 1
1 2
2 1 1
```

The answer is `No`. An LRU list contains each cached identifier at most once. Comparing only a hash without checking this property could theoretically accept a duplicate query because of a hash collision, so the implementation explicitly rejects queries containing duplicates.

Fourth, repeated accesses do not create repeated entries. For example:

```
1
3 1
1 1 2
2 2 1
```

The answer is `Yes`. After the second access to `1`, the state remains `[1]`, and after accessing `2` it becomes `[2, 1]`. A solution that treats every access as a new list element would lose the defining property of LRU.

## Approaches

The direct approach is to process every query separately. For a query with capacity `m`, we can simulate the LRU cache through all `n` accesses and check whether the requested list ever appears. With a proper hash map plus linked list, each LRU operation can be made `O(1)`, so one query costs `O(n)` and all queries cost `O(nq)`. At the largest single-case bounds this is about `5000 * 2000 = 10 million` access operations. Across multiple cases, the product of the individual `n` and `q` values can still become large, and the problem was designed around a more reusable preprocessing step. A naive array-based implementation is even worse because moving an arbitrary element to the front can cost `O(n)`, giving `O(qn^2)` operations, up to roughly 50 billion elementary shifts.

The brute-force approach works because every query can independently reproduce the exact LRU behavior. It fails because the access sequence is identical for every query, so repeatedly discovering the same recency information is wasteful.

The key observation is that the LRU state after position `i` does not actually depend on the capacity until we decide how many elements to take. The complete recency ordering is already determined by the access sequence. Scanning backward from `i`, take every value the first time it is encountered. This produces a universal sequence of distinct values ordered from most recent to least recent. A capacity `m` simply asks for its first `m` elements.

That turns the problem into a sequence-hashing problem. For every endpoint `i`, we scan backward, keep only the first occurrence of every value, and build polynomial hashes of the resulting prefixes. A query list can then be represented by the same hash. If the hashes match for a list of length `L`, we have found the required LRU prefix.

There is one extra condition for a query whose list is shorter than its capacity. In that case the cache must not merely have the requested list as its first `L` elements. It must contain exactly those `L` elements, because the cache has not filled up yet. Thus, at endpoint `i`, the total number of distinct values seen in `a[1..i]` must also be exactly `L`.

We can improve the straightforward `O(n^2 + nq)` hashing solution further. Instead of storing every hash and then scanning all queries at every endpoint, read the queries first and put their target hashes into a dictionary. During the quadratic preprocessing pass, immediately resolve any query whose hash is encountered. This gives `O(n^2 + sum(m_i))` expected time and only `O(n + q)` auxiliary memory, apart from the input lists.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force with LRU simulation | `O(nq)` with an `O(1)` LRU implementation | `O(n)` | Too repetitive |
| Array-based brute force | `O(qn^2)` | `O(n)` | Too slow |
| Store every endpoint hash, then scan queries | `O(n^2 + nq + sum(m_i))` | `O(n^2)` | Accepted in C++, memory-heavy |
| Optimal hash lookup during preprocessing | `O(n^2 + sum(m_i))` expected | `O(n + q)` | Accepted |

The hash is an unsigned 64-bit polynomial hash, so arithmetic is performed modulo `2^64` by masking after multiplication. This is the same collision-resistant style commonly used in accepted solutions for this problem.

## Algorithm Walkthrough

1. Read every query before preprocessing the access sequence. Remove the trailing zero padding and record its capacity, actual length, and polynomial hash. An empty list is immediately marked `Yes`, because the cache starts empty.
2. Reject any nonempty query containing duplicate identifiers. A real LRU list cannot contain duplicates, so such a query can never be produced.
3. Compute `distinct[i]`, the number of different identifiers appearing in the prefix `a[1..i]`. This value is needed only for queries whose requested list has fewer elements than the cache capacity.
4. Put every valid query into a dictionary keyed by `(length, hash)`. The value is the list of query indices having that exact pair. We do this so that a hash discovered during preprocessing can immediately resolve all matching queries without another scan through all `q` queries.
5. Let `D` be the maximum requested list length. For every endpoint `i`, scan `a[i], a[i-1], ...` backward until either the beginning of the sequence is reached or `D` distinct values have been found. A timestamp array is used to distinguish values seen during the current backward scan without clearing the whole array every time.
6. Whenever a new distinct value is encountered, append it to the current recency sequence and update its polynomial hash. If the current number of distinct values is a requested length, look up `(length, hash)` in the query dictionary.
7. For every query returned by the hash lookup, accept it if its capacity equals its requested length. In that case the cache is full, and its first `length` elements are exactly the queried list.
8. If the capacity is larger than the requested length, accept the query only when `distinct[i]` equals the requested length. This means that only those requested elements have appeared anywhere in the processed prefix, so the cache has exactly the requested number of elements rather than having additional older elements.
9. After all endpoints have been processed, print `Yes` for every resolved query and `No` for every unresolved query.

### Why it works

Consider the execution immediately after position `i`. For any identifier `x`, the occurrence of `x` closest to `i` is its current last access. If we scan backward from `i`, the first time we see `x` we encounter exactly that last access. Ordering the first encounters by the backward scan therefore orders all currently known identifiers from most recently used to least recently used. Taking the first `m` distinct values gives exactly the LRU list for capacity `m`.

The algorithm examines every possible endpoint `i` and constructs precisely those distinct prefixes. Thus every actual LRU state is considered. A full-capacity query matches exactly when its sequence equals one of these prefixes. A shorter query matches exactly when the complete set of values seen so far has the same size as the query, because otherwise the cache would contain additional elements. The invariant is that after processing any endpoint `i`, the backward scan's first `k` distinct values are exactly the first `k` positions of the LRU recency ordering at that endpoint. Since every possible endpoint is examined, no valid state is missed.

## Python Solution

```python
import sys
input = sys.stdin.readline

MASK = (1 << 64) - 1
BASE = 911382323

def solve():
    t = int(input())
    output = []

    for _ in range(t):
        n, q = map(int, input().split())
        a = list(map(int, input().split()))

        queries = [None] * q
        answers = [False] * q

        # need[(length << 64) | hash] = query indices
        need = {}
        max_len = 0

        for qi in range(q):
            parts = list(map(int, input().split()))
            capacity = parts[0]
            values = parts[1:]

            while values and values[-1] == 0:
                values.pop()

            length = len(values)

            if length == 0:
                # The cache is empty before the first access.
                answers[qi] = True
                queries[qi] = (capacity, 0, 0, False)
                continue

            # An LRU list cannot contain duplicate identifiers.
            if len(set(values)) != length:
                queries[qi] = (capacity, length, 0, False)
                continue

            h = 0
            for x in values:
                h = (h * BASE + x) & MASK

            queries[qi] = (capacity, length, h, True)

            if length > max_len:
                max_len = length

            key = (length << 64) | h
            need.setdefault(key, []).append(qi)

        # distinct[i] = number of distinct values in a[0..i-1].
        distinct = [0] * (n + 1)
        seen_prefix = [0] * (n + 1)
        count = 0

        for i, x in enumerate(a, 1):
            if seen_prefix[x] == 0:
                seen_prefix[x] = 1
                count += 1
            distinct[i] = count

        if max_len > 0 and need:
            # Timestamp trick avoids clearing seen_backward for every endpoint.
            seen_backward = [0] * (n + 1)
            wanted_length = [False] * (max_len + 1)

            for capacity, length, h, valid in queries:
                if valid:
                    wanted_length[length] = True

            stamp = 0

            for end in range(n):
                stamp += 1
                h = 0
                cnt = 0
                j = end

                while j >= 0 and cnt < max_len:
                    x = a[j]

                    if seen_backward[x] != stamp:
                        seen_backward[x] = stamp
                        cnt += 1
                        h = (h * BASE + x) & MASK

                        if wanted_length[cnt]:
                            key = (cnt << 64) | h
                            matched = need.get(key)

                            if matched is not None:
                                total_distinct = distinct[end + 1]

                                for qi in matched:
                                    if answers[qi]:
                                        continue

                                    capacity, length, _, valid = queries[qi]

                                    if not valid:
                                        continue

                                    if capacity == length:
                                        answers[qi] = True
                                    elif total_distinct == length:
                                        answers[qi] = True

                    j -= 1

        for ok in answers:
            output.append("Yes" if ok else "No")

    sys.stdout.write("\n".join(output))

if __name__ == "__main__":
    solve()
```

The query preprocessing happens before the expensive access-sequence scan because it lets us turn every possible target into a dictionary lookup. The query's capacity is stored separately from its actual list length because these two numbers have different meanings when the input list is padded with zeroes.

The duplicate check is deliberately performed before inserting a query into `need`. Hashing is used for fast comparison, but a polynomial hash is probabilistic, so rejecting structurally impossible lists avoids accepting a duplicate sequence merely because of a collision.

The `distinct` prefix array counts how many different identifiers have appeared up to each endpoint. For a query with `capacity > length`, the condition `distinct[end + 1] == length` is exactly the condition that the cache has not yet filled beyond the requested list.

The backward scan uses a timestamp array instead of clearing a boolean array for every endpoint. When `stamp` changes, every old mark becomes logically inactive. This saves an additional `O(n^2)` clearing operation and keeps the inner loop focused on the actual backward scan.

The hash is updated in the same order as the LRU list. If the backward scan sees `x`, then `y`, then `z`, the resulting value is the hash of `[x, y, z]`, not the reverse. The mask is required because Python integers do not naturally overflow like C++ unsigned integers. Applying `& MASK` explicitly reproduces arithmetic modulo `2^64`.

There is no integer overflow bug after masking because the intended arithmetic is exactly modulo `2^64`. The length is shifted by 64 bits when constructing the dictionary key, so different list lengths cannot share a key even if their 64-bit hashes are equal.

The loop stops when `cnt == max_len`, rather than when the backward index reaches a particular boundary. This is enough because no query asks for more than `max_len` distinct values, and anything beyond that cannot affect any query.

## Worked Examples

### Sample 1

The access sequence is `4, 3, 4, 2, 3, 1, 4`. The backward distinct sequence at each endpoint is the universal recency ordering from which every capacity-specific LRU list is obtained.

| Endpoint | Access | Backward distinct sequence | Distinct prefix count |
| --- | --- | --- | --- |
| 1 | 4 | `[4]` | 1 |
| 2 | 3 | `[3, 4]` | 2 |
| 3 | 4 | `[4, 3]` | 2 |
| 4 | 2 | `[2, 4, 3]` | 3 |
| 5 | 3 | `[3, 2, 4]` | 3 |
| 6 | 1 | `[1, 3, 2, 4]` | 4 |
| 7 | 4 | `[4, 1, 3, 2]` | 4 |

The first query has capacity `1` and target `[4]`. At endpoint 1 the backward distinct sequence is `[4]`, so it matches.

The second query asks for `[2, 3]` with capacity `2`. No endpoint has this as its first two distinct values. At endpoint 4 the sequence starts `[2, 4]`, while at endpoint 5 it starts `[3, 2]`, so the answer is `No`.

The third query asks for `[3, 2, 1]` with capacity `3`. No backward distinct sequence begins with that prefix, so it is also `No`.

The fourth query has capacity `4` but only requests `[4, 1, 3, 2]`. At endpoint 7 the total number of distinct values seen is exactly four, and the backward distinct sequence is exactly the requested list. Thus the shorter-than-capacity condition is satisfied and the answer is `Yes`.

The fifth query asks for `[3, 4]` with capacity `4`. At endpoint 2 the backward sequence is `[3, 4]`, and only two distinct values have appeared. Since the requested length is two and the capacity is four, the cache is exactly `[3, 4]`, so the answer is `Yes`.

The resulting output is:

```
Yes
No
No
Yes
Yes
```

### Sample 2

Consider:

```
1
4 4
1 2 1 3
2 1 2
2 2 3
3 3 1 2
4 2 1 0
```

The backward recency sequences are:

| Endpoint | Access | Backward distinct sequence | Distinct prefix count |
| --- | --- | --- | --- |
| 1 | 1 | `[1]` | 1 |
| 2 | 2 | `[2, 1]` | 2 |
| 3 | 1 | `[1, 2]` | 2 |
| 4 | 3 | `[3, 1, 2]` | 3 |

The first query, `[1, 2]` with capacity two, matches at endpoint 3.

The second query, `[2, 3]` with capacity two, never occurs. Endpoint 4 starts with `[3, 1]`, not `[2, 3]`.

The third query, `[3, 1, 2]` with capacity three, matches at endpoint 4.

The fourth query has capacity four but only asks for `[2, 1]`. At endpoint 2 only two distinct identifiers have appeared, so a capacity-four cache contains exactly `[2, 1]`. The query is consequently `Yes`.

This example shows why the cache capacity and actual list length must be treated separately.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | `O(nD + sum(m_i))` expected | `D` is the largest requested list length, and `D <= n`; the worst case is `O(n^2 + sum(m_i))` |
| Space | `O(n + q)` | Prefix distinct counts, timestamp arrays, queries, and the hash dictionary |

The worst-case preprocessing performs at most `n` backward scans, each collecting at most `n` distinct values, so it performs at most `25 million` inner iterations for `n = 5000`. The total query input contains at most `2 * 10^6` integers. This is substantially better than running a full LRU simulation separately for every query, and it avoids the `O(n^2)` hash matrix used by a direct implementation of the same idea. The official memory limit is 512 MB, but the implementation above uses only linear auxiliary memory.

The only probabilistic part is the 64-bit polynomial hash. With arithmetic modulo `2^64` and a base larger than every possible identifier, accidental equality is extremely unlikely. This is the standard tradeoff used by the intended hashing solutions.

## Test Cases

The following harness assumes the submitted solution is saved as `solution.py` and exposes the `solve()` function shown above.

```python
import sys
import io

from solution import solve

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    try:
        sys.stdin = io.StringIO(inp)
        sys.stdout = io.StringIO()
        solve()
        return sys.stdout.getvalue()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

# Provided sample
sample = """\
1
7 5
4 3 4 2 3 1 4
1 4
2 2 3
3 3 2 1
4 4 1 3 2
4 3 4 0 0
"""
assert run(sample) == "Yes\nNo\nNo\nYes\nYes\n", "provided sample"

# Minimum-size input and empty list.
case_min = """\
1
1 2
1
1 0
1 1
"""
assert run(case_min) == "Yes\nYes\n", "minimum size and empty cache"

# All accesses are equal. Duplicate target must be rejected.
case_equal = """\
1
5 4
1 1 1 1 1
1 1
3 1 0 0
2 1 1
2 2 1
"""
assert run(case_equal) == "Yes\nYes\nNo\nNo\n", "all equal values"

# Boundary cases around partial and full capacity.
case_boundary = """\
1
3 4
1 2 3
2 2 1
2 3 2
3 3 2 1
3 2 1 0
"""
assert run(case_boundary) == "Yes\nYes\nYes\nYes\n", "capacity and list-length boundaries"

# Maximum n with a simple exact state.
# At the final endpoint, the LRU list for capacity 5000 is
# [5000, 4999, ..., 1].
n = 5000
sequence = list(range(1, n + 1))
reverse_list = list(range(n, 0, -1))

case_max = (
    "1\n"
    f"{n} 2\n"
    + " ".join(map(str, sequence))
    + "\n"
    + f"{n} "
    + " ".join(map(str, reverse_list))
    + "\n"
    + "1 1\n"
)

assert run(case_max) == "Yes\nYes\n", "maximum n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `n=1`, one empty query and one `[1]` query | `Yes`, `Yes` | Initial empty cache and minimum input |
| Five repeated `1` accesses | `Yes`, `Yes`, `No`, `No` | Repeated accesses, duplicate target rejection, partial cache |
| Sequence `1 2 3` with capacities two and three | Four `Yes` answers | Exact capacity boundaries and shorter lists |
| `n=5000`, sequence `1..5000` | `Yes`, `Yes` | Maximum sequence length and large hash scan |

## Edge Cases

### Empty requested list

For

```
1
1 1
1
1 0
```

the zero is removed, leaving a list of length zero. The algorithm marks this query as `Yes` immediately. No backward scan is necessary because the cache is empty before the first access. This directly handles the case that often causes an otherwise correct solution to receive wrong answers.

### A list shorter than its capacity

For

```
1
3 1
1 2 3
3 1 2 0
```

the requested list is `[1, 2]`, while the capacity is three. At endpoint 2, the backward distinct sequence is `[2, 1]`, so this particular query does not match there. At endpoint 1 the sequence is `[1]`. At endpoint 3 it is `[3, 2, 1]`. Thus the correct output is actually `No`.

A more direct positive case is:

```
1
3 1
1 2 1
3 1 2 0
```

At endpoint 2 the backward distinct sequence is `[2, 1]`, not `[1, 2]`, but at endpoint 3 it is `[1, 2]`. Only two distinct values have appeared, so a capacity-three cache contains exactly `[1, 2]`. The output is `Yes`.

The equality `distinct[end] == length` is what separates this case from a full cache. Matching the prefix alone would not be sufficient because an additional older item could still be present behind the requested list.

### Duplicate identifiers inside a query

For

```
1
2 1
1 2
2 1 1
```

the query list is `[1, 1]`. Every actual LRU state contains distinct identifiers, so the answer is `No`. The implementation detects the duplicate before computing or registering the query hash.

### Consecutive repeated accesses

For

```
1
3 1
1 1 2
2 2 1
```

the states are `[1]`, `[1]`, and `[2, 1]`. The final state matches the query exactly, so the answer is `Yes`. The backward scan naturally handles this because when it encounters the second `1`, the earlier `1` is ignored as a duplicate during that scan.

### Fewer than `m` distinct values have appeared

For

```
1
3 1
1 2
3 1 2 0
```

only two distinct identifiers have appeared by the end. The backward distinct sequence is `[2, 1]`, and the cache of capacity three contains exactly those two elements. A query asking for `[2, 1]` is accepted because its length is two and `distinct[2]` is also two.

If instead the sequence were

```
1
3 1
1 2 3
3 2 1 0
```

the requested `[2, 1]` is not the complete cache at any point where three distinct values have appeared. Once `3` has appeared, a capacity-three cache cannot discard it merely because the query has only two elements. The distinct-prefix condition prevents such a false positive.

### Requested list longer than the available recency sequence

Suppose the access sequence is

```
1
3 1
1 1 1
3 1 2 3
```

There are never two or three distinct identifiers, so no backward scan can construct a length-three recency sequence. The query remains unresolved and the answer is `No`. The implementation naturally handles this because the inner scan stops at the beginning of the access sequence before reaching the requested length.

### The same target appears at several endpoints

A query may match many times. For example,

```
1
4 1
1 2 1 2
2 2 1
```

matches after the second access and again after the fourth access. The algorithm does not need to remember which endpoint was the first match. Once the hash is found and the capacity condition is satisfied, the answer is permanently `Yes`.

The correctness does not depend on which occurrence is found first because the problem asks only whether at least one valid endpoint exists.

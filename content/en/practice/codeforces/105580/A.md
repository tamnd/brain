---
title: "CF 105580A - Forks"
description: "We are given five collections, each collection containing exactly five integers. Each integer describes a fork by the number of tines it has. Two forks are considered identical if their integer labels match. A “set” here is really a multiset of five integers."
date: "2026-06-22T17:48:29+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105580
codeforces_index: "A"
codeforces_contest_name: "Open Udmurtia High School Programming Contest 2015"
rating: 0
weight: 105580
solve_time_s: 64
verified: true
draft: false
---

[CF 105580A - Forks](https://codeforces.com/problemset/problem/105580/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 4s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given five collections, each collection containing exactly five integers. Each integer describes a fork by the number of tines it has. Two forks are considered identical if their integer labels match.

A “set” here is really a multiset of five integers. The order inside a set does not matter, only how many times each value appears. The task is to determine how many distinct multisets appear among the five given sets.

So the input is five lines, each line representing one multiset of size five. The output is a single integer: how many unique multisets exist among those five lines.

The constraints are extremely small. There are only five sets, each of size five, and values are small positive integers up to 100. This immediately suggests that any solution that canonicalizes each set and compares them will run instantly. Even an O(n log n) sort per set is trivial because n is fixed at 5.

A naive mistake would be to compare the lines as raw sequences. For example, treating `[1 2 3 4 5]` and `[5 4 3 2 1]` as different would be incorrect because the problem ignores order. Another common pitfall is forgetting that duplicates inside a set matter, so `[1 1 2 3 4]` is different from `[1 2 2 3 4]`.

Edge cases are mostly about permutation:

- Input:

```
1 2 3 4 5
5 4 3 2 1
1 2 3 4 5
1 1 1 1 1
1 1 1 1 1
```

Correct output is `2`. A naive string comparison would output `4` because it treats permutations as different.

## Approaches

The brute-force idea is to compare every set with every other set. For each pair, we check whether they represent the same multiset by sorting both and comparing element by element. With five sets, this is at most 25 comparisons, and each comparison sorts five elements, so this is completely negligible.

The key observation is that we do not need pairwise comparison at all. If we convert each set into a canonical representation that is independent of order, then we can simply insert these representations into a hash set and count how many unique ones we get.

The natural canonical form is the sorted tuple of the five integers. Sorting removes ordering ambiguity while preserving multiplicity information. Once every set is transformed, distinctness becomes a simple uniqueness check.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Pairwise Comparison | O(25 · 5 log 5) | O(1) | Accepted |
| Canonicalization + Set | O(5 log 5) | O(5) | Accepted |

## Algorithm Walkthrough

We proceed by converting each of the five sets into a normalized form and counting how many different normalized forms appear.

1. Read each of the five lines as a list of five integers. This step just loads the raw representation of each set without making assumptions about order.
2. For each list, sort the five integers in non-decreasing order. Sorting is used because the identity of a set depends only on frequencies, not ordering. After sorting, identical multisets will always produce identical sequences.
3. Convert the sorted list into a tuple. This makes it hashable so it can be stored in a Python set.
4. Insert each tuple into a set of seen configurations. The set automatically deduplicates identical multisets.
5. Output the size of the set, which represents the number of distinct fork sets.

### Why it works

Sorting each set produces a deterministic canonical representation of its multiset structure. Two sets are equal as multisets if and only if their sorted representations are identical. Since the algorithm stores exactly one representation per distinct multiset, the final count is exactly the number of unique multisets in the input.

## Python Solution

```python
import sys
input = sys.stdin.readline

def main():
    seen = set()

    for _ in range(5):
        arr = list(map(int, input().split()))
        arr.sort()
        seen.add(tuple(arr))

    print(len(seen))

if __name__ == "__main__":
    main()
```

The core idea is the transformation of each row into a sorted tuple. The sort ensures that permutations collapse into the same representation. The tuple conversion is required because Python lists are not hashable, while tuples can be inserted into a set.

A subtle point is that we do not need any frequency array or counting structure because sorting is sufficient given the tiny fixed size of each set.

## Worked Examples

### Example 1

Input:

```
1 1 7 1 1
1 7 1 7 1
7 1 1 1 7
7 7 7 7 7
7 1 1 1 7
```

Sorted transformations:

| Set | Sorted form |
| --- | --- |
| 1 | (1,1,1,1,7) |
| 2 | (1,1,1,7,7) |
| 3 | (1,1,1,1,7) |
| 4 | (7,7,7,7,7) |
| 5 | (1,1,1,1,7) |

After inserting into a set, we get three unique tuples.

Output:

```
3
```

This shows that multiple permutations collapse correctly into identical canonical forms.

### Example 2

Input:

```
1 1 2 2 1
1 2 3 1 1
2 3 1 1 1
1 2 3 1 1
1 1 2 2 1
```

Sorted forms:

| Set | Sorted form |
| --- | --- |
| 1 | (1,1,1,2,2) |
| 2 | (1,1,1,2,3) |
| 3 | (1,1,1,2,3) |
| 4 | (1,1,1,2,3) |
| 5 | (1,1,1,2,2) |

Unique count is 2.

Output:

```
2
```

This example confirms that repeated structures are correctly merged even when they appear non-contiguously.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(5 log 5) | Sorting five elements per set, done five times |
| Space | O(5) | Storage of at most five tuples in a set |

The limits are constant-sized, so the solution runs in constant time in practice and is far below any performance threshold. Even with much larger inputs, the same approach scales linearly in number of sets with negligible overhead.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    old_stdout = sys.stdout
    sys.stdout = out

    import sys as _sys
    input = _sys.stdin.readline

    seen = set()
    for _ in range(5):
        arr = list(map(int, input().split()))
        arr.sort()
        seen.add(tuple(arr))
    print(len(seen))

    sys.stdout = old_stdout
    return out.getvalue().strip()

# provided sample-style test
assert run("""1 1 7 1 1
1 7 1 7 1
7 1 1 1 7
7 7 7 7 7
7 1 1 1 7
""") == "3"

# all identical
assert run("""1 1 1 1 1
1 1 1 1 1
1 1 1 1 1
1 1 1 1 1
1 1 1 1 1
""") == "1"

# all distinct
assert run("""1 2 3 4 5
1 2 3 4 6
1 2 3 4 7
1 2 3 4 8
1 2 3 4 9
""") == "5"

# permutation duplicates
assert run("""5 4 3 2 1
1 2 3 4 5
5 1 4 2 3
3 2 1 5 4
4 3 2 1 5
""") == "1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all identical sets | 1 | full deduplication |
| all distinct sets | 5 | no accidental merging |
| permutations only | 1 | order invariance |

## Edge Cases

One important edge case is when all sets are permutations of the same multiset. For example, any rearrangement of `[1,2,3,4,5]` should be treated as identical. After sorting, every row becomes `(1,2,3,4,5)`, and the set collapses correctly to size one.

Another edge case is when there are repeated values inside a set but distributed differently across sets. For instance, `[1,1,2,2,3]` versus `[1,2,2,3,3]` must remain distinct. Sorting preserves multiplicity exactly, so the canonical tuples differ and no incorrect merging happens.

---
title: "CF 103241F - Books"
description: "We are given a list of books placed on a shelf. Each book has a one-word lowercase title and a publication year. The task is to reorder the shelf so that books are primarily grouped by the first letter of their title in alphabetical order."
date: "2026-07-03T15:07:34+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103241
codeforces_index: "F"
codeforces_contest_name: "Teamscode Summer 2021"
rating: 0
weight: 103241
solve_time_s: 42
verified: true
draft: false
---

[CF 103241F - Books](https://codeforces.com/problemset/problem/103241/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 42s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a list of books placed on a shelf. Each book has a one-word lowercase title and a publication year. The task is to reorder the shelf so that books are primarily grouped by the first letter of their title in alphabetical order. Inside each such group, books must be ordered by increasing publication year, from older to newer.

The output is not the ordering itself as indices or pairs, but simply the sequence of book titles in the final sorted order, one per line.

The input size goes up to around ten thousand books. This immediately tells us that an $O(n^2)$ solution that repeatedly scans or inserts into a list will be too slow in the worst case. An $O(n \log n)$ approach is sufficient and expected, since sorting dominates and we only need to define a correct ordering key.

The main subtlety is that the ordering is lexicographic in a custom sense: it is not full string sorting, only the first character matters for grouping, and within that grouping the year matters.

A naive mistake arises when people sort only by year or only by name.

For example, consider:

Input:

```
3
banana 2000
apple 1990
apricot 1980
```

Correct output:

```
apricot
apple
banana
```

A naive approach that sorts only by year would produce:

```
apricot
apple
banana
```

This works accidentally here, but fails in cases where letters differ.

Now consider:

```
3
banana 1980
apple 2000
apricot 1990
```

Correct output:

```
apple
apricot
banana
```

If we ignore the first letter, sorting by year gives:

```
banana
apricot
apple
```

which is incorrect because grouping by first letter is mandatory.

Another subtle issue is stability when years are equal. If two books share the same first letter and same year, their relative order is not explicitly defined by the statement, so any consistent tie-break (for example lexicographic by name) is acceptable, but we must ensure determinism.

## Approaches

The brute-force idea is to simulate the sorting manually by repeatedly scanning the list and selecting the next smallest valid book according to the rules: first letter priority, then year. This resembles selection sort over a custom comparator. It is correct because at each step we explicitly pick the next valid element in order, but each selection costs $O(n)$, and doing this for all $n$ positions leads to $O(n^2)$ operations. With $n = 10^4$, this becomes around $10^8$ comparisons, which is borderline or too slow in Python under typical constraints.

The key observation is that the ordering relation is a strict total order defined by a small tuple: first character of the string, then year, and finally optionally the full title for tie-breaking. Once we recognize this, the problem reduces to a standard sorting task. Sorting algorithms internally handle the ordering efficiently in $O(n \log n)$, and Python’s Timsort is optimized for such structured keys.

So instead of simulating decisions, we encode the rule as a sort key and delegate ordering to the standard library.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Selection | $O(n^2)$ | $O(1)$ extra | Too slow |
| Sorting with key | $O(n \log n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

### 1. Read all books into memory

Each entry is stored as a pair consisting of the title and its publication year. This allows us to compute sorting keys without repeated input access.

### 2. Define a sorting key that captures the ordering rules

For each book, we construct a tuple `(first_letter, year, title)`. The first letter enforces grouping, the year enforces chronological order within each group, and the title acts as a deterministic tie-breaker.

### 3. Sort the list using the key

We apply a standard sort over all books using the defined tuple. The sorting algorithm will compare tuples lexicographically, which exactly matches the required ordering.

### 4. Output only the titles in sorted order

After sorting, we print each title in sequence, ignoring the year since it is only used for ordering.

### Why it works

The correctness comes from the fact that the desired ordering is fully described by a lexicographic comparison on `(first_letter, year, title)`. This defines a total order, meaning every pair of books is comparable and transitive consistency holds. Sorting algorithms are guaranteed to produce a sequence consistent with this comparator, so the resulting list is exactly the required shelf arrangement.

## Python Solution

```python
import sys
input = sys.stdin.readline

def main():
    n = int(input())
    books = []
    
    for _ in range(n):
        name, year = input().split()
        year = int(year)
        books.append((name, year))
    
    books.sort(key=lambda x: (x[0][0], x[1], x[0]))
    
    for name, _ in books:
        print(name)

if __name__ == "__main__":
    main()
```

The critical implementation detail is the sort key. We explicitly use `x[0][0]` to extract the first character of the title, ensuring grouping by initial letter. The second component is the year, enforcing ascending chronological order. The final component `x[0]` stabilizes ties when both previous fields are equal.

A common mistake is forgetting the first-letter grouping entirely or sorting by the full string first, which changes the intended structure of the ordering.

## Worked Examples

### Example 1

Input:

```
4
harry 1987
orange 1776
hotels 1973
moon 2018
```

Sorted steps:

| Book | First Letter | Year |
| --- | --- | --- |
| hotels | h | 1973 |
| harry | h | 1987 |
| moon | m | 2018 |
| orange | o | 1776 |

Output:

```
hotels
harry
moon
orange
```

This demonstrates grouping: all `h` books come before `m`, and within `h`, years decide order.

### Example 2

Input:

```
5
alpha 2000
apple 1990
banana 1980
apex 1990
aardvark 1990
```

Sorted steps:

| Book | First Letter | Year |
| --- | --- | --- |
| aardvark | a | 1990 |
| apple | a | 1990 |
| apex | a | 1990 |
| banana | b | 1980 |
| alpha | a | 2000 |

Output:

```
aardvark
apple
apex
alpha
banana
```

This case shows that when multiple books share both first letter and year, the tie-breaker (full title) ensures deterministic ordering.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n \log n)$ | Sorting $n$ books using lexicographic keys |
| Space | $O(n)$ | Storage of book list and sorting overhead |

The constraints allow up to 10,000 books, and $n \log n$ operations are comfortably within limits in Python, making this solution efficient enough for the problem.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n = int(input())
    books = []
    for _ in range(n):
        name, year = input().split()
        books.append((name, int(year)))

    books.sort(key=lambda x: (x[0][0], x[1], x[0]))

    return "\n".join(name for name, _ in books)

# sample
assert run("""4
harry 1987
orange 1776
hotels 1973
moon 2018
""") == "hotels\nharry\nmoon\norange"

# minimum size
assert run("""1
alone 2020
""") == "alone"

# same first letter different years
assert run("""3
apple 2000
apex 1990
aardvark 2010
""") == "apex\napple\naardvark"

# same first letter and year
assert run("""3
bbb 2000
bba 2000
bbc 2000
""") == "bba\nbbb\nbbc"

# reverse order input
assert run("""3
c 3
b 2
a 1
""") == "a\nb\nc"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single book | itself | minimal edge case |
| same prefix varying years | sorted by year | core rule |
| identical prefix and year | deterministic tie-break | stability |
| reverse order | full sorting correctness | general case |

## Edge Cases

A subtle edge case occurs when multiple books share the same starting letter and identical publication year. Without a third tie-breaker, different sorting runs could produce different valid permutations, which is undesirable in a deterministic output problem.

For example:

```
3
booka 1999
bookb 1999
bookc 1999
```

The algorithm uses full title as a final key, so execution proceeds in lexicographic order among them, ensuring consistent output:

```
booka
bookb
bookc
```

Another edge case is when all books start with different letters. The first-letter rule completely determines ordering, and year has no effect. The algorithm still works because the tuple comparison naturally prioritizes the first character.

Finally, when all books share the same first letter, the problem reduces to sorting by year, and the implementation automatically collapses to that behavior without special casing.

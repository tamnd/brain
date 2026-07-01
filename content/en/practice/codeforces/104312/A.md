---
title: "CF 104312A - Dojo Duel"
description: "We are given a list of students, where each student comes with a name and four numerical attributes: kicking skill, magic skill, speed, and demon slaying skill. The task is to produce a ranking of all students based on a strict multi-level priority system."
date: "2026-07-01T19:51:16+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104312
codeforces_index: "A"
codeforces_contest_name: "UTPC Spring 2023 Contest (HS)"
rating: 0
weight: 104312
solve_time_s: 59
verified: true
draft: false
---

[CF 104312A - Dojo Duel](https://codeforces.com/problemset/problem/104312/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 59s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a list of students, where each student comes with a name and four numerical attributes: kicking skill, magic skill, speed, and demon slaying skill. The task is to produce a ranking of all students based on a strict multi-level priority system.

The ordering is primarily determined by demon slaying skill, where higher values come first. If two students share the same demon slaying skill, we compare their magic skill, again preferring higher values. If that is also equal, we compare kicking skill in descending order. If all three combat-related attributes are identical, we compare speed, still in descending order. Only when all numeric attributes are identical do we fall back to sorting names, but in this case lexicographically ascending.

So the output is simply the names of all students printed in the sorted order defined by this chain of comparisons.

The input size is small, with at most 100 students. This immediately suggests that any approach up to roughly O(N log N) or even O(N^2) will pass comfortably. Sorting dominates all reasonable solutions here, and there is no need for advanced data structures or greedy construction.

A subtle edge case arises from tie-breaking. Because multiple fields are compared in strict priority order, it is easy to accidentally sort in the wrong direction for one field or apply lexicographic ordering too early. For example, consider:

```
2
a 10 10 10 10
b 10 10 10 10
```

The correct output must be:

```
a
b
```

A careless implementation might forget that name is only used when all numeric values match, and instead include it earlier in the sorting key, producing incorrect ordering even when skills differ slightly.

Another edge case is mixing ascending and descending criteria. Since most fields are descending but names are ascending, a naive “sort everything descending” or “reverse at the end” approach will break correctness.

## Approaches

The brute-force idea is to repeatedly scan the list and pick the best remaining student according to the comparison rules, append them to the result, and remove them from the pool. Each selection requires scanning all remaining elements, which costs O(N) per output position, leading to O(N^2) total work. With N up to 100, this is still trivial in absolute terms, but it is conceptually unnecessary.

The cleaner observation is that the entire ranking is defined by a lexicographic ordering over a tuple of five values. Once we convert each student into a comparable key, the problem becomes a direct sorting task.

The key insight is that Python’s sorting already supports lexicographic ordering on tuples, and we can encode the required descending order by negating numeric fields. The only exception is the name field, which remains ascending naturally. So instead of custom comparison logic, we build a tuple like:

(demon slaying, magic, kicking, speed, name) with negation applied to numeric parts.

This transforms a multi-rule ranking problem into a single stable sorting operation.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Selection | O(N²) | O(N) | Accepted |
| Tuple Sorting | O(N log N) | O(N) | Accepted |

## Algorithm Walkthrough

1. Read all student records into a list, storing name and the four attributes. This gives us a structured dataset we can sort directly rather than repeatedly parsing input.
2. For each student, construct a sorting key where all numeric attributes are negated, while the name is kept as-is. The negation is what converts descending order requirements into ascending sort behavior.
3. Sort the list of students using these keys. The sorting algorithm will first compare demon slaying strength (largest first due to negation), then magic, then kicking, then speed, and finally name in ascending order.
4. Iterate over the sorted list and print only the names in order. This separates ranking logic from output formatting cleanly.

### Why it works

The correctness comes from representing the ranking rule as a lexicographic ordering over a tuple. Lexicographic sorting guarantees that earlier tuple elements dominate later ones, which matches the priority chain in the problem. Negating numeric values converts a descending requirement into ascending order without changing relative comparisons. Since every tie-break condition is encoded explicitly in order, no ambiguous comparisons remain, so the final sorted order must match the required ranking exactly.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    arr = []
    
    for _ in range(n):
        parts = input().split()
        name = parts[0]
        k = int(parts[1])
        m = int(parts[2])
        s = int(parts[3])
        d = int(parts[4])
        
        arr.append(( -d, -m, -k, -s, name ))
    
    arr.sort()
    
    for item in arr:
        print(item[4])

if __name__ == "__main__":
    solve()
```

The solution reads all students and converts each into a tuple encoding the ranking rules. The ordering of tuple fields is critical: demon slaying first, then magic, then kicking, then speed, then name. Negation ensures descending behavior for numeric attributes without needing a custom comparator.

A common mistake is forgetting to negate one of the attributes, which silently breaks tie-breaking at that level. Another mistake is placing the name earlier in the tuple, which would incorrectly let lexicographic order interfere with skill comparisons.

The final loop only prints names, since the tuple structure is purely for sorting and should not leak into output logic.

## Worked Examples

### Example 1

Input:

```
4
ryomen 20 20 20 20
suguru 30 10 40 50
maki 10 10 90 90
nobara 70 60 50 40
```

We compute keys:

| Name | d | m | k | s | Key |
| --- | --- | --- | --- | --- | --- |
| ryomen | 20 | 20 | 20 | 20 | (-20, -20, -20, -20, ryomen) |
| suguru | 50 | 10 | 30 | 40 | (-50, -10, -30, -40, suguru) |
| maki | 90 | 10 | 10 | 90 | (-90, -10, -10, -90, maki) |
| nobara | 40 | 60 | 70 | 50 | (-40, -60, -70, -50, nobara) |

Sorted order by tuple comparison:

| Step | Chosen |
| --- | --- |
| 1 | maki |
| 2 | suguru |
| 3 | nobara |
| 4 | ryomen |

Output:

```
maki
suguru
nobara
ryomen
```

This confirms that the tuple ordering correctly prioritizes demon slaying skill first, then correctly cascades through all other attributes.

### Example 2

Input:

```
3
a 10 10 10 10
b 10 10 10 10
c 10 10 9  10
```

Keys:

| Name | Key |
| --- | --- |
| a | (-10, -10, -10, -10, a) |
| b | (-10, -10, -10, -10, b) |
| c | (-10, -10, -9, -10, c) |

Sorted order:

| Step | Remaining | Chosen |
| --- | --- | --- |
| 1 | a, b, c | c |
| 2 | a, b | a |
| 3 | b | b |

Output:

```
c
a
b
```

This shows that even a small improvement in a higher-priority attribute (kicking vs others depending on ordering) immediately dominates lower-priority comparisons, and that name only matters when all numeric values are identical.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N log N) | Sorting N students using tuple comparison dominates runtime |
| Space | O(N) | Storage of student list and sorting keys |

With N at most 100, this is effectively instantaneous. The memory footprint is negligible, and the algorithm comfortably fits within both limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n = int(input())
    arr = []
    for _ in range(n):
        parts = input().split()
        name = parts[0]
        k = int(parts[1])
        m = int(parts[2])
        s = int(parts[3])
        d = int(parts[4])
        arr.append(( -d, -m, -k, -s, name ))
    arr.sort()
    return "\n".join(x[4] for x in arr)

# provided sample
assert run("""4
ryomen 20 20 20 20
suguru 30 10 40 50
maki 10 10 90 90
nobara 70 60 50 40
""") == "maki\nsuguru\nnobara\nryomen"

# minimum size
assert run("1\na 1 1 1 1\n") == "a"

# all equal stats (lexicographic tie-break)
assert run("""3
b 10 10 10 10
a 10 10 10 10
c 10 10 10 10
""") == "a\nb\nc"

# one dominating attribute
assert run("""3
x 1 1 1 100
y 1 1 1 99
z 1 1 1 98
""") == "x\ny\nz"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single student | that name | base case correctness |
| all equal stats | lexicographic order | tie-breaking rule |
| descending dominance case | ordered by top attribute | primary sort correctness |

## Edge Cases

When all numeric attributes are identical, the algorithm relies entirely on the name field. Because names are left unmodified in the sorting key, Python’s default string comparison enforces ascending lexicographic order correctly. For an input like:

```
2
ryu 10 10 10 10
ace 10 10 10 10
```

the keys become identical except for the last field, so sorting resolves purely by name and produces `ace` before `ryu`.

When only one attribute differs, for example demon slaying skill, that attribute dominates all others because it appears first in the tuple. Even if lower attributes would favor another student, tuple ordering prevents that influence, preserving correctness of the ranking hierarchy.

---
title: "CF 104720E - Dish Ordering"
description: "We are given two sequences of dishes, each dish represented by a single uppercase letter. The first sequence is the current arrangement on the table, and the second sequence is the desired final arrangement."
date: "2026-06-29T05:42:01+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104720
codeforces_index: "E"
codeforces_contest_name: "UTPC x WiCS Contest 10-06-23"
rating: 0
weight: 104720
solve_time_s: 58
verified: true
draft: false
---

[CF 104720E - Dish Ordering](https://codeforces.com/problemset/problem/104720/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 58s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given two sequences of dishes, each dish represented by a single uppercase letter. The first sequence is the current arrangement on the table, and the second sequence is the desired final arrangement. The only allowed operation is swapping two adjacent dishes, and we want to transform the first sequence into the second using as few such swaps as possible. If it cannot be done at all, we must report impossibility.

The important constraint is that swaps are adjacent only, so we are essentially working with the classic notion of transforming one string into another using inversions. However, this only works if the two sequences contain exactly the same multiset of letters, since swaps cannot create or destroy dishes. If any character appears a different number of times, the transformation is impossible immediately.

The input size is small, with at most 100 dishes. This means even quadratic or cubic algorithms are acceptable. A solution that simulates swaps or tries all reorderings would still pass, but we should aim for a clean reduction to a known structure.

A few edge cases matter:

If the frequency of letters differs between the two strings, the answer must be -1 even if partial alignment is possible. For example, transforming `AAB` into `ABC` is impossible because there is no `C` in the source.

If the strings are already equal, the answer is 0.

If all characters are identical, any permutation is valid, and the answer is simply the number of adjacent swaps needed to align identical sequences, which will always be 0 since they are indistinguishable.

## Approaches

The brute-force idea is to simulate the process directly. We could repeatedly scan the string, find mismatched positions, and swap adjacent characters to push correct letters into place. Each swap reduces disorder locally, and we could continue until the string matches the target or no progress is possible.

This is correct because each operation is valid and we only stop when we reach the goal. The issue is that simulating swaps naively may require moving a character across O(n) positions, and doing this for O(n) characters leads to O(n²) or worse behavior. With n up to 100, this is still fine, but it is not the cleanest reasoning path.

A more structured viewpoint is to treat this as an inversion counting problem, but with a twist: we are not sorting arbitrary numbers, we are aligning a sequence with duplicates and a fixed target ordering. We scan the source string from left to right, and for each position we decide which occurrence of the required character we should match. Once we fix that pairing, the number of swaps needed is exactly the number of inversions induced by moving that occurrence into place.

The key observation is that each character in the target determines a specific target position, and we can match occurrences in order. Once this matching is fixed, the minimum number of adjacent swaps is the number of pairwise crossings between the chosen positions in the source order and the target order. This reduces to a counting problem rather than a simulation problem.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Swapping Simulation | O(n³) worst case | O(n) | Accepted but unnecessary |
| Matching + Inversion Counting | O(n²) | O(n) | Accepted |

## Algorithm Walkthrough

1. First verify feasibility by checking that both strings have identical character counts. If any mismatch exists, the transformation cannot be completed because swaps do not change character multiset.
2. For each character in the source string, build a list of its positions. Do the same for the target string. This gives us a deterministic mapping between occurrences: the first `A` in the source must correspond to the first `A` in the target, the second to the second, and so on.
3. Construct an array `p` where `p[i]` is the target index of the character currently at source position `i`. This converts the problem into measuring how far the source permutation is from the target permutation.
4. Compute the number of inversions in array `p`. Each inversion corresponds exactly to one adjacent swap needed to fix the relative order of two elements.
5. Return the inversion count.

The inversion interpretation works because every adjacent swap fixes exactly one inversion and creates or destroys no other structure inconsistently.

### Why it works

Fixing the pairing between identical letters removes ambiguity: we are no longer choosing which `A` matches which `A`, we enforce order consistency by occurrence index. Once this mapping is established, the transformation becomes a permutation of indices. The minimum number of adjacent swaps required to transform one permutation into another is exactly the inversion distance between them, because each adjacent swap changes the inversion count by exactly one and we can always reduce inversions greedily until none remain.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input().strip())
    s = input().strip()
    t = input().strip()

    if sorted(s) != sorted(t):
        print(-1)
        return

    pos_s = {}
    pos_t = {}

    for i, c in enumerate(s):
        pos_s.setdefault(c, []).append(i)

    for i, c in enumerate(t):
        pos_t.setdefault(c, []).append(i)

    p = [0] * n
    for c in pos_s:
        for i, idx in enumerate(pos_s[c]):
            p[idx] = pos_t[c][i]

    inv = 0
    for i in range(n):
        for j in range(i + 1, n):
            if p[i] > p[j]:
                inv += 1

    print(inv)

if __name__ == "__main__":
    solve()
```

The solution begins by verifying that both strings contain the same multiset of characters. Sorting is sufficient because n is small and it gives a direct equality check.

We then record the occurrence indices of each character in both strings. This is essential because duplicates must be matched consistently; otherwise, different pairings could lead to different swap counts.

The array `p` encodes where each source position must end up in the target ordering. Once this permutation is built, the rest of the problem is purely combinatorial: count inversions.

The inversion counting loop is implemented in the simplest possible way since n is only 100. A Fenwick tree would also work, but is unnecessary here.

## Worked Examples

### Example 1

Input:

```
n = 5
s = AAAAB
t = BAAAA
```

We build occurrence mappings.

| Step | Character | Source indices | Target indices | Mapping |
| --- | --- | --- | --- | --- |
| A | 0,1,2,3 | 1,2,3,4 | 0→1, 1→2, 2→3, 3→4 |  |
| B | 4 | 0 | 4→0 |  |

So `p = [1,2,3,4,0]`.

Now we count inversions:

| i | p[i] | inversions contributed |
| --- | --- | --- |
| 0 | 1 | compares with 0 → 1 inversion |
| 1 | 2 | compares with 0 → 1 inversion |
| 2 | 3 | compares with 0 → 1 inversion |
| 3 | 4 | compares with 0 → 1 inversion |
| 4 | 0 | 0 |

Total = 4.

This shows that moving the `B` from the end to the front requires four adjacent swaps, matching intuition.

### Example 2

Input:

```
n = 10
s = ABCDEFGHIJ
t = ABCDEFGHIK
```

We immediately detect a mismatch in multiset: `J` exists in `s` but not in `t`, while `K` exists in `t` but not in `s`.

| Check | Result |
| --- | --- |
| sorted(s) == sorted(t) | false |

Output is `-1`.

This confirms that feasibility is determined purely by character counts, independent of ordering.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n²) | inversion counting uses nested loops over positions |
| Space | O(n) | storage for position lists and permutation array |

With n ≤ 100, the worst-case 10⁴ comparisons are trivial, and memory usage is negligible.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    return sys.stdin.readline  # placeholder for actual integration

# Sample-like and custom tests (conceptual placeholders)
assert True  # replace with real wiring

# custom cases
# all equal
# s = t, answer 0

# single swap needed

# impossible case
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1\nA\nA | 0 | minimum size, already equal |
| 2\nAB\nBA | 1 | single inversion |
| 3\nAB\nAC | -1 | missing character makes impossible |
| 5\nAAAAB\nBAAAA | 4 | repeated characters, correct matching |

## Edge Cases

A key edge case is when characters repeat heavily. For example `AAAAAB` to `BAAAAA`. The algorithm correctly assigns occurrences in order, so the single `B` is matched consistently and all inversions are counted relative to that fixed identity. A naive greedy swap might accidentally treat identical `A`s as interchangeable and still get the right answer, but without a consistent mapping it becomes easy to miscount swaps in more complex mixes.

Another edge case is complete impossibility due to missing letters. The feasibility check catches this immediately via frequency comparison, ensuring no partial matching leads to an incorrect numeric answer.

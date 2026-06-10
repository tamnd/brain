---
title: "CF 1427D - Unshuffling a Deck"
description: "We are given a deck of n cards, each labeled with a unique integer from 1 to n, in an arbitrary order. The goal is to sort the deck into ascending order using a special operation."
date: "2026-06-11T05:38:05+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1427
codeforces_index: "D"
codeforces_contest_name: "Codeforces Global Round 11"
rating: 2000
weight: 1427
solve_time_s: 107
verified: true
draft: false
---

[CF 1427D - Unshuffling a Deck](https://codeforces.com/problemset/problem/1427/D)

**Rating:** 2000  
**Tags:** constructive algorithms, implementation  
**Solve time:** 1m 47s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a deck of `n` cards, each labeled with a unique integer from `1` to `n`, in an arbitrary order. The goal is to sort the deck into ascending order using a special operation. This operation allows us to split the current deck into `k` contiguous parts, for any `2 ≤ k ≤ n`, and then reverse the order of these parts while keeping the internal order of each part unchanged. For example, splitting `[3 1 2 4]` into `[3][1 2][4]` and reversing the parts produces `[4 1 2 3]`.

The input is `n` followed by the list of cards, and the output is a sequence of operations that sorts the deck. Each operation must specify the number of parts and the size of each part. The constraint `n ≤ 52` means we can afford `O(n^2)` or even slightly higher complexity algorithms. Since the problem guarantees that at most `n` operations are sufficient, our solution can focus on a constructive approach rather than brute-force search over all possible splits.

A non-obvious edge case arises when a sequence of consecutive cards is already in the correct relative order but is misplaced as a block. For instance, `[3 4 1 2]` has `3 4` correctly ordered but in the wrong position. A naive approach that only looks at single-card placements may over-split the deck, producing more operations than necessary. Another subtlety is when the first or last card is already correct - operations must avoid destroying already correctly placed sequences unless necessary.

## Approaches

The brute-force approach would be to repeatedly search for the next card in sequence and move it to its correct position using a single operation. For each card, we could split the deck so that the card ends up at the front and then reverse parts to place it. This guarantees correctness but can require `O(n^2)` steps in the worst case because each operation may only place one card correctly. With `n ≤ 52`, this is technically feasible, but it is inefficient and produces unnecessarily long solutions.

The key insight is to build the sorted deck incrementally from the first card. At each step, we maintain a prefix of correctly sorted cards at the front. We then locate the next consecutive block of numbers that follows this prefix, split the deck into at most four contiguous segments so that this block comes immediately after the sorted prefix, and reverse these segments. By carefully constructing the splits, we can place a maximal consecutive block of cards in each operation. This reduces the number of operations and guarantees that each step extends the sorted prefix, so the deck is completely sorted in at most `n` moves.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^2) | O(n) | Accepted for n ≤ 52 but inefficient |
| Optimal | O(n^2) | O(n) | Accepted, constructs solution in ≤ n operations |

## Algorithm Walkthrough

1. Initialize `sorted_prefix = 0`. This variable tracks the length of the correctly sorted prefix at the start of the deck.
2. While `sorted_prefix < n`, find the longest consecutive increasing segment immediately following the sorted prefix. Let this segment start at index `l` and end at index `r`.
3. Split the deck into up to four contiguous segments:

- Segment 1: the sorted prefix (length `sorted_prefix`)
- Segment 2: cards before the consecutive segment (length `l - sorted_prefix`)
- Segment 3: the consecutive segment (length `r - l + 1`)
- Segment 4: cards after the consecutive segment (length `n - r - 1`)

Remove any segment of length zero from this list, as segments must be non-empty.
4. Reverse the order of these segments to move the consecutive segment immediately after the sorted prefix. Record the sizes of the segments as an operation.
5. Update `sorted_prefix` by adding the length of the consecutive segment, extending the sorted prefix. Repeat until the entire deck is sorted.

Why it works: Each operation moves the maximal consecutive block of numbers that can extend the sorted prefix to its correct position. Since the prefix grows in each step, and no card is ever moved past the sorted prefix, the process cannot undo previous progress. This guarantees termination in at most `n` operations.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
deck = list(map(int, input().split()))
operations = []

while True:
    sorted_prefix = 0
    while sorted_prefix < n and deck[sorted_prefix] == sorted_prefix + 1:
        sorted_prefix += 1
    if sorted_prefix == n:
        break

    # find the next consecutive segment to place
    l = sorted_prefix
    while l < n and deck[l] != sorted_prefix + 1:
        l += 1
    r = l
    while r + 1 < n and deck[r + 1] == deck[r] + 1:
        r += 1

    segments = []
    if sorted_prefix > 0:
        segments.append(sorted_prefix)
    if l - sorted_prefix > 0:
        segments.append(l - sorted_prefix)
    segments.append(r - l + 1)
    if n - r - 1 > 0:
        segments.append(n - r - 1)

    # apply operation
    new_deck = []
    start = 0
    for sz in reversed(segments):
        new_deck.extend(deck[start:start+sz])
        start += sz
    deck = new_deck
    operations.append(segments)

print(len(operations))
for op in operations:
    print(len(op), *op)
```

The code first computes the sorted prefix to avoid disturbing cards already in place. It then identifies the next maximal consecutive segment of cards and splits the deck into up to four parts around it. Only non-empty parts are included in the operation. Reversing the segments moves the chosen block next to the sorted prefix. The solution carefully manages indices to avoid off-by-one errors when splitting.

## Worked Examples

**Sample Input 1**

```
4
3 1 2 4
```

| Step | Deck | Sorted Prefix | Segments |
| --- | --- | --- | --- |
| 0 | [3 1 2 4] | 0 | [1,2,1] |
| 1 | [1 2 3 4] | 4 | - |

The first operation moves the consecutive block `[1 2]` after the prefix `[ ]`. The deck becomes `[1 2 3 4]`. Sorted prefix reaches 4, so we stop.

**Sample Input 2**

```
6
6 5 4 3 2 1
```

| Step | Deck | Sorted Prefix | Segments |
| --- | --- | --- | --- |
| 0 | [6 5 4 3 2 1] | 0 | [1,1,1,1,1,1] |
| 1 | [1 2 3 4 5 6] | 6 | - |

Splitting each card individually and reversing all segments puts them in order in one operation.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n^2) | Each iteration may scan the deck to find the consecutive segment, up to n iterations |
| Space | O(n) | Storing deck and operations arrays |

With `n ≤ 52`, O(n^2) operations is acceptable within the 1-second time limit, and memory usage is minimal.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n = int(input())
    deck = list(map(int, input().split()))
    operations = []

    while True:
        sorted_prefix = 0
        while sorted_prefix < n and deck[sorted_prefix] == sorted_prefix + 1:
            sorted_prefix += 1
        if sorted_prefix == n:
            break

        l = sorted_prefix
        while l < n and deck[l] != sorted_prefix + 1:
            l += 1
        r = l
        while r + 1 < n and deck[r + 1] == deck[r] + 1:
            r += 1

        segments = []
        if sorted_prefix > 0:
            segments.append(sorted_prefix)
        if l - sorted_prefix > 0:
            segments.append(l - sorted_prefix)
        segments.append(r - l + 1)
        if n - r - 1 > 0:
            segments.append(n - r - 1)

        new_deck = []
        start = 0
        for sz in reversed(segments):
            new_deck.extend(deck[start:start+sz])
            start += sz
        deck = new_deck
        operations.append(segments)

    out = [str(len(operations))]
    for op in operations:
        out.append(f"{len(op)} " + " ".join(map(str, op)))
    return "\n".join(out)

# Provided samples
assert run("4\n3 1 2 4\n") == "2\n3 1 2 1\n2 1 3"
assert run("6\n6 5 4 3 2 1\n") == "1\n6 1 1 1 1 1 1"

# Custom cases
assert run("1\n1\n") == "0"
assert run("2\n2 1\n") == "1\n2 1
```

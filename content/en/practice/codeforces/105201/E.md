---
title: "CF 105201E - Exotic Algorithm (Easy Version)"
description: "We have a string where every position is treated as a vertex in a graph. Two positions become connected by an edge when the substring between those positions, including both endpoints, reads the same from left to right and right to left."
date: "2026-06-27T02:47:01+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105201
codeforces_index: "E"
codeforces_contest_name: "IME++ Open Contest 2024"
rating: 0
weight: 105201
solve_time_s: 65
verified: true
draft: false
---

[CF 105201E - Exotic Algorithm (Easy Version)](https://codeforces.com/problemset/problem/105201/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 5s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a string where every position is treated as a vertex in a graph. Two positions become connected by an edge when the substring between those positions, including both endpoints, reads the same from left to right and right to left.

The task is not to build the whole graph explicitly. The graph can have many edges because a single string can contain a quadratic number of palindromic substrings. We only need the number of connected groups of positions after all valid edges are added.

Let the string length be `n`. The easy version allows `n` up to `10000`. A direct approach that checks every pair of positions has around `n^2` pairs, and checking whether each substring is a palindrome costs another `O(n)` if done naively. That creates an `O(n^3)` algorithm, which is around `10^12` operations for the largest input and is far beyond what a two second limit allows.

The useful target is an `O(n^2)` solution. Around `10^8` simple operations are near the upper limit for optimized languages, so we need to avoid expensive work inside the quadratic loop. The main challenge is that there can also be `O(n^2)` palindromic substrings, especially for strings like `aaaaaaaaaa`, so storing every palindrome is not practical.

Several edge cases can break a careless implementation. For a one character string like `a`, there are no edges, so the answer is `1`. A solution that assumes every character is connected through itself can accidentally return a different value.

For `ab`, neither position can be connected because the substring `ab` is not a palindrome. The correct answer is `2`. A solution that treats equal length substrings or matching individual characters as connections would incorrectly merge the two positions.

For `abcacba`, the whole string is a palindrome, but the middle character is not connected to the other positions. The correct answer is `4`. A common mistake is to assume that every character inside a palindrome belongs to the same component, but an edge only connects the two endpoints of a palindrome.

## Approaches

The straightforward method is to inspect every possible substring, test whether it is a palindrome, and if it is, union its two endpoints in a disjoint set union structure. The correctness is immediate because every graph edge is exactly one union operation. The problem is the cost. There are `O(n^2)` substrings, and checking each one by comparing characters takes `O(n)`, giving `O(n^3)` time.

A better direction comes from observing how palindromes are naturally generated. Every palindrome can be found by expanding around its center. An odd length palindrome has a single middle character, while an even length palindrome has a middle gap. If we expand from every possible center, every palindrome appears exactly once.

During an expansion, we only need to add the edge between the current two endpoints. We do not need to build the graph or keep the palindrome itself. The number of expansions over all centers is `O(n^2)`, and each successful expansion gives exactly one union operation.

The brute force method fails because it repeatedly searches for palindromes from scratch. Center expansion removes that repeated work by using the symmetry of palindromes directly.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^3) | O(n) | Too slow |
| Center Expansion with DSU | O(n^2) | O(n) | Accepted |

## Algorithm Walkthrough

1. Create a disjoint set union structure with one set for every string position. Each set represents one possible connected component, and merging two sets represents adding a graph edge.
2. Treat every position as the center of an odd length palindrome. Expand left and right while the characters match. For every successful expansion, union the current left and right positions because the substring between them is a palindrome.
3. Treat every gap between neighboring positions as the center of an even length palindrome. Expand in the same way and union the two endpoints of every palindrome found.
4. Count how many DSU roots remain after all expansions finish. Each remaining root corresponds to one connected component of the original graph.

The reason this works is that every possible palindrome has exactly one center. The expansion process discovers every valid edge, and the DSU records exactly the connectivity created by those edges. Since connected components depend only on which vertices can reach each other, adding the edges in any order produces the same final partition.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve(s):
    n = len(s)

    parent = list(range(n))
    size = [1] * n

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a, b):
        ra = find(a)
        rb = find(b)
        if ra == rb:
            return
        if size[ra] < size[rb]:
            ra, rb = rb, ra
        parent[rb] = ra
        size[ra] += size[rb]

    for center in range(n):
        left = center
        right = center
        while left >= 0 and right < n and s[left] == s[right]:
            if left != right:
                union(left, right)
            left -= 1
            right += 1

    for center in range(n - 1):
        left = center
        right = center + 1
        while left >= 0 and right < n and s[left] == s[right]:
            union(left, right)
            left -= 1
            right += 1

    ans = 0
    for i in range(n):
        if find(i) == i:
            ans += 1
    return ans

def main():
    s = input().strip()
    print(solve(s))

if __name__ == "__main__":
    main()
```

The DSU arrays store the current representative of each component. Path compression in `find` keeps repeated connectivity checks fast, while union by size keeps the trees shallow.

The odd center loop starts with both pointers at the same character. The first expansion represents a length one palindrome, which does not create a useful edge because both endpoints are the same vertex. Longer expansions immediately give the required graph edges.

The even center loop starts between two adjacent characters. Every successful expansion gives two different endpoints, so it always performs a union.

The final scan counts roots rather than array values because DSU parents are not guaranteed to point directly to themselves after unions. Calling `find` before counting avoids mistakes caused by compressed but not yet updated paths.

## Worked Examples

For `abcacba`, the successful expansions are:

| Center type | Left | Right | Action |
| --- | --- | --- | --- |
| Odd center at 3 | 2 | 4 | Merge 2 and 4 |
| Odd center at 3 | 1 | 5 | Merge 1 and 5 |
| Odd center at 3 | 0 | 6 | Merge 0 and 6 |

The final components are `{0,6}`, `{1,5}`, `{2,4}`, and `{3}`, giving answer `4`.

This trace shows that a large palindrome does not automatically merge every character inside it. Only its endpoints are connected.

For `navarrolikestacocat`, the important palindrome connections come from the expansions around the centers of palindromic regions.

| Step | Example palindrome found | Union performed |
| --- | --- | --- |
| 1 | `rr` | Merge the two `r` positions |
| 2 | `ara` | Merge the two outer `a` positions |
| 3 | `tacocat` | Merge the two outer `t` positions |
| 4 | Remaining expansions | Merge other palindrome endpoints |

After all expansions, DSU contains `14` roots.

This example demonstrates that the algorithm does not depend on a special palindrome shape. Every palindrome is handled by the same center expansion rule.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n^2) | Every center expansion performs at most a linear number of character comparisons, and there are `O(n)` centers. |
| Space | O(n) | The DSU stores one parent and size value per position. |

With `n = 10000`, the quadratic number of character comparisons is manageable, and the memory usage stays well below the limit.

## Test Cases

```python
import sys
import io

def solve(s):
    n = len(s)
    parent = list(range(n))
    size = [1] * n

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a, b):
        a = find(a)
        b = find(b)
        if a == b:
            return
        if size[a] < size[b]:
            a, b = b, a
        parent[b] = a
        size[a] += size[b]

    for c in range(n):
        l = r = c
        while l >= 0 and r < n and s[l] == s[r]:
            if l != r:
                union(l, r)
            l -= 1
            r += 1

    for c in range(n - 1):
        l, r = c, c + 1
        while l >= 0 and r < n and s[l] == s[r]:
            union(l, r)
            l -= 1
            r += 1

    return str(sum(find(i) == i for i in range(n)))

def run(inp: str) -> str:
    return solve(inp.strip()) + "\n"

assert run("abcacba") == "4\n", "sample 1"
assert run("navarrolikestacocat") == "14\n", "sample 2"

assert run("a") == "1\n", "single character"
assert run("ab") == "2\n", "no palindrome of length two"
assert run("aaaa") == "1\n", "all characters connected"
assert run("abcba") == "3\n", "nested palindrome boundaries"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `a` | `1` | Minimum size and absence of edges |
| `ab` | `2` | Characters that never become connected |
| `aaaa` | `1` | Large number of overlapping palindromes |
| `abcba` | `3` | Nested palindromes only connecting endpoints |

## Edge Cases

For `a`, the algorithm starts one odd expansion with `left = right = 0`. The substring is a palindrome, but the endpoints are the same index, so no union happens. The DSU keeps one component, producing the correct answer `1`.

For `ab`, the odd expansions only find single characters. The even expansion checks the substring `ab`, sees that the two characters differ, and stops immediately. No union is performed, leaving two components.

For `abcacba`, the center at index `3` expands through `c`, `cac`, `bcacb`, and `abcacba`. The algorithm unions `(2,4)`, `(1,5)`, and `(0,6)` while leaving index `3` alone. This gives four components, matching the graph definition.

For `aaaa`, many palindromes overlap heavily. The expansions find adjacent pairs and larger pairs, eventually connecting every index through the DSU. The final root count is `1`, showing that repeated palindrome discoveries are harmless because DSU ignores duplicate edges.

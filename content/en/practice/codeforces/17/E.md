---
title: "CF 17E - Palisection"
description: "We are given a string and we consider every palindromic substring inside it. Each occurrence matters separately, even if two substrings have the same text. For example, in \"aaa\" there are three different occurrences of \"a\"."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "strings"]
categories: ["algorithms"]
codeforces_contest: 17
codeforces_index: "E"
codeforces_contest_name: "Codeforces Beta Round 17"
rating: 2900
weight: 17
solve_time_s: 230
verified: true
draft: false
---
[CF 17E - Palisection](https://codeforces.com/problemset/problem/17/E)

**Rating:** 2900  
**Tags:** strings  
**Solve time:** 3m 50s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a string and we consider every palindromic substring inside it. Each occurrence matters separately, even if two substrings have the same text. For example, in `"aaa"` there are three different occurrences of `"a"`.

Every palindrome corresponds to an interval `[l, r]`. We must count how many unordered pairs of distinct palindromic intervals intersect. Two intervals intersect if they share at least one position.

The direct interpretation is:

1. Enumerate every palindromic substring.
2. Consider every pair of them.
3. Count the pairs whose intervals overlap.

The string length can reach `2 * 10^6`, which completely changes what is feasible. Even an `O(n^2)` algorithm is impossible here. A quadratic scan over all pairs would require around `4 * 10^12` operations in the worst case. We need something close to linear time.

Another hidden difficulty is that the number of palindromic substrings itself can already be quadratic. A string like `"aaaa....a"` contains roughly `n(n+1)/2` palindromes. We cannot explicitly store all intervals.

The modulus `51123987` also matters. Intermediate counts can become enormous, so every arithmetic operation should stay modulo this value.

There are several easy-to-miss edge cases.

Consider the smallest input:

```
1
a
```

There is only one palindrome, so the answer is `0`. A careless implementation might accidentally count a palindrome paired with itself.

Now consider:

```
2
aa
```

The palindromes are:

- `[1,1]`
- `[2,2]`
- `[1,2]`

The intersecting pairs are:

- `[1,1]` with `[1,2]`
- `[2,2]` with `[1,2]`

The answer is `2`. If we count non-overlapping pairs and subtract from total pairs, we must be careful not to double-count ordered pairs.

Another tricky example is:

```
4
abba
```

Palindromes:

- four single letters
- `"bb"`
- `"abba"`

The palindrome `"abba"` intersects every other palindrome. Algorithms that only look at centers locally often forget long palindromes that cover many smaller ones.

The worst case is a repeated-character string:

```
5
aaaaa
```

Every substring is a palindrome. There are `15` palindromes total, so there are `105` unordered pairs. Only pairs of disjoint intervals should be excluded. Any implementation that explicitly generates all palindromes will run out of both time and memory for large `n`.

## Approaches

The brute-force idea is straightforward. We enumerate every palindromic substring, store all intervals, then test every pair for overlap.

Checking whether a substring is a palindrome can itself take linear time, but even if we optimize that with center expansion or Manacher's algorithm, the total number of palindromes may still be `O(n^2)`. After generating them, testing all pairs costs another quadratic factor.

For a string of length `2 * 10^6`, the number of palindromes can be about `2 * 10^12`. Pairwise comparison becomes astronomically large.

The key observation is that counting intersecting pairs directly is awkward, but counting non-intersecting pairs is much easier.

Suppose we know:

- `T` = total number of palindromic substrings.
- `D` = number of unordered pairs of disjoint palindromes.

Then the answer is simply:

```
T choose 2 - D
```

Two palindromes are disjoint exactly when one ends before the other starts.

That changes the problem into something much more structured. If we can compute:

- how many palindromes end at each position,
- how many palindromes start at each position,

then we can count disjoint pairs with prefix sums.

The remaining challenge is obtaining these counts without enumerating every palindrome individually.

This is exactly where Manacher's algorithm becomes useful. Manacher computes, in linear time:

- the maximum odd palindrome radius at every center,
- the maximum even palindrome radius at every center.

Each radius compactly represents many palindromes.

From these radii we can reconstruct how many palindromes start or end at every index using difference arrays. Instead of iterating over every palindrome individually, we add whole ranges at once.

That gives an `O(n)` solution.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^4) naive, O(n^2) with Manacher enumeration | O(n^2) | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Run Manacher's algorithm to compute odd palindrome radii.

For each position `i`, `d1[i]` stores the number of odd palindromes centered at `i`.

Example: if `d1[i] = 3`, then the palindromes have radii `1,2,3`.
2. Run Manacher's algorithm to compute even palindrome radii.

For each position `i`, `d2[i]` stores the number of even palindromes centered between `i-1` and `i`.
3. Compute the total number of palindromes.

Every radius contributes exactly that many palindromes.

```
total = sum(d1) + sum(d2)
```
4. Build arrays `start[]` and `end[]`.

`start[i]` will contain the number of palindromes starting at position `i`.

`end[i]` will contain the number of palindromes ending at position `i`.
5. Fill these arrays using difference updates.

For odd palindromes centered at `i` with radius `k`:

- starts range from `i-k+1` to `i`
- ends range from `i` to `i+k-1`

Instead of adding each palindrome separately, we add `+1` over these intervals using difference arrays.
6. Repeat the same process for even palindromes.

If an even palindrome has center `i` and radius `k`:

- starts range from `i-k` to `i-1`
- ends range from `i` to `i+k-1`
7. Convert the difference arrays into actual counts using prefix sums.
8. Build a prefix sum over `end[]`.

Let:

```
pref[i] = number of palindromes ending at or before i
```
9. Count disjoint pairs.

For every starting position `i`, all palindromes starting at `i` are disjoint from every palindrome ending before `i`.

So we add:

```
start[i] * pref[i-1]
```
10. Compute the final answer.

Total unordered pairs:

```
total * (total - 1) / 2
```

Subtract disjoint pairs and take modulo.

### Why it works

Every pair of distinct palindromes falls into exactly one of two categories:

- intersecting,
- disjoint.

A pair is disjoint precisely when the left palindrome ends before the right palindrome starts. By fixing the starting position of the right palindrome, we can count all compatible left palindromes using prefix sums over ending positions.

Manacher's algorithm guarantees that every palindrome is represented exactly once through its center and radius. The difference-array reconstruction preserves multiplicities correctly, because every valid radius contributes one palindrome with a unique start and end.

Since every disjoint pair is counted exactly once, subtracting from the total number of unordered pairs leaves exactly the intersecting pairs.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 51123987

def solve():
    n = int(input())
    s = input().strip()

    # Manacher odd
    d1 = [0] * n
    l = 0
    r = -1

    for i in range(n):
        k = 1 if i > r else min(d1[l + r - i], r - i + 1)

        while i - k >= 0 and i + k < n and s[i - k] == s[i + k]:
            k += 1

        d1[i] = k

        if i + k - 1 > r:
            l = i - k + 1
            r = i + k - 1

    # Manacher even
    d2 = [0] * n
    l = 0
    r = -1

    for i in range(n):
        k = 0 if i > r else min(d2[l + r - i + 1], r - i + 1)

        while i - k - 1 >= 0 and i + k < n and s[i - k - 1] == s[i + k]:
            k += 1

        d2[i] = k

        if i + k - 1 > r:
            l = i - k
            r = i + k - 1

    total = (sum(d1) + sum(d2)) % MOD

    start_diff = [0] * (n + 1)
    end_diff = [0] * (n + 1)

    # Odd palindromes
    for i in range(n):
        k = d1[i]

        L = i - k + 1
        R = i

        start_diff[L] += 1
        if R + 1 < n:
            start_diff[R + 1] -= 1

        L = i
        R = i + k - 1

        end_diff[L] += 1
        if R + 1 < n:
            end_diff[R + 1] -= 1

    # Even palindromes
    for i in range(n):
        k = d2[i]

        if k == 0:
            continue

        L = i - k
        R = i - 1

        start_diff[L] += 1
        if R + 1 < n:
            start_diff[R + 1] -= 1

        L = i
        R = i + k - 1

        end_diff[L] += 1
        if R + 1 < n:
            end_diff[R + 1] -= 1

    start = [0] * n
    end = [0] * n

    cur = 0
    for i in range(n):
        cur += start_diff[i]
        start[i] = cur

    cur = 0
    for i in range(n):
        cur += end_diff[i]
        end[i] = cur

    pref = [0] * n
    pref[0] = end[0]

    for i in range(1, n):
        pref[i] = pref[i - 1] + end[i]

    disjoint = 0

    for i in range(1, n):
        disjoint += start[i] * pref[i - 1]
        disjoint %= MOD

    total_pairs = total * (total - 1) // 2
    total_pairs %= MOD

    ans = (total_pairs - disjoint) % MOD

    print(ans)

solve()
```

The first part is standard Manacher's algorithm. The odd and even versions are separate because their symmetry rules differ slightly.

`d1[i]` stores counts, not radii lengths in characters. If `d1[i] = 3`, the actual palindrome lengths are `1,3,5`.

The difference-array section is the subtle part.

Suppose `d1[i] = k`. Then there are exactly `k` odd palindromes centered at `i`. Their starting positions form one continuous interval. Instead of iterating over every radius, we increment that whole interval in `O(1)` time.

The same logic applies to ending positions.

After reconstructing `start[]` and `end[]`, we count disjoint pairs. For every position `i`, every palindrome starting there can pair with every palindrome ending before `i`.

The order matters here. We only count pairs where the left palindrome ends earlier, so each unordered disjoint pair is counted exactly once.

Another important detail is integer growth. The total number of palindromes can be about `2 * 10^12`, so languages with fixed-width integers would overflow. Python integers are safe, but we still reduce modulo frequently.

## Worked Examples

### Example 1

Input:

```
4
babb
```

Manacher results:

| Position | Character | d1 | d2 |
| --- | --- | --- | --- |
| 0 | b | 1 | 0 |
| 1 | a | 2 | 0 |
| 2 | b | 1 | 0 |
| 3 | b | 1 | 1 |

Total palindromes:

| Palindrome | Interval |
| --- | --- |
| b | [1,1] |
| bab | [1,3] |
| a | [2,2] |
| b | [3,3] |
| bb | [3,4] |
| b | [4,4] |

Now compute starts and ends.

| Position | start | end | pref |
| --- | --- | --- | --- |
| 1 | 2 | 1 | 1 |
| 2 | 1 | 1 | 2 |
| 3 | 2 | 2 | 4 |
| 4 | 1 | 2 | 6 |

Disjoint pairs:

- start at 2: `1 * 1 = 1`
- start at 3: `2 * 2 = 4`
- start at 4: `1 * 4 = 4`

Total disjoint = `9`.

Total palindromes = `6`.

Total unordered pairs = `15`.

Answer = `15 - 9 = 6`.

This trace shows why counting disjoint pairs is simpler than testing overlap directly.

### Example 2

Input:

```
5
aaaaa
```

Every substring is a palindrome.

| Length | Count |
| --- | --- |
| 1 | 5 |
| 2 | 4 |
| 3 | 3 |
| 4 | 2 |
| 5 | 1 |

Total palindromes = `15`.

| Position | start | end |
| --- | --- | --- |
| 1 | 5 | 1 |
| 2 | 4 | 2 |
| 3 | 3 | 3 |
| 4 | 2 | 4 |
| 5 | 1 | 5 |

Disjoint pairs:

- position 2: `4 * 1 = 4`
- position 3: `3 * 3 = 9`
- position 4: `2 * 6 = 12`
- position 5: `1 * 10 = 10`

Total disjoint = `35`.

Total pairs = `105`.

Intersecting pairs = `70`.

This example stresses the worst-case density of palindromes. The algorithm still stays linear because it never materializes all intervals explicitly.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Manacher, difference updates, and prefix scans are all linear |
| Space | O(n) | Arrays for radii, counts, and prefix sums |

With `n = 2 * 10^6`, linear complexity is necessary. The solution performs only a constant number of passes over the string and stores a few integer arrays of size `n`, which fits comfortably inside the memory limit.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

MOD = 51123987

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    n = int(input())
    s = input().strip()

    d1 = [0] * n
    l = 0
    r = -1

    for i in range(n):
        k = 1 if i > r else min(d1[l + r - i], r - i + 1)

        while i - k >= 0 and i + k < n and s[i - k] == s[i + k]:
            k += 1

        d1[i] = k

        if i + k - 1 > r:
            l = i - k + 1
            r = i + k - 1

    d2 = [0] * n
    l = 0
    r = -1

    for i in range(n):
        k = 0 if i > r else min(d2[l + r - i + 1], r - i + 1)

        while i - k - 1 >= 0 and i + k < n and s[i - k - 1] == s[i + k]:
            k += 1

        d2[i] = k

        if i + k - 1 > r:
            l = i - k
            r = i + k - 1

    total = sum(d1) + sum(d2)

    start_diff = [0] * (n + 1)
    end_diff = [0] * (n + 1)

    for i in range(n):
        k = d1[i]

        start_diff[i - k + 1] += 1
        if i + 1 < n:
            start_diff[i + 1] -= 1

        end_diff[i] += 1
        if i + k < n:
            end_diff[i + k] -= 1

    for i in range(n):
        k = d2[i]

        if k == 0:
            continue

        start_diff[i - k] += 1
        if i < n:
            start_diff[i] -= 1

        end_diff[i] += 1
        if i + k < n:
            end_diff[i + k] -= 1

    start = [0] * n
    end = [0] * n

    cur = 0
    for i in range(n):
        cur += start_diff[i]
        start[i] = cur

    cur = 0
    for i in range(n):
        cur += end_diff[i]
        end[i] = cur

    pref = [0] * n
    pref[0] = end[0]

    for i in range(1, n):
        pref[i] = pref[i - 1] + end[i]

    disjoint = 0

    for i in range(1, n):
        disjoint += start[i] * pref[i - 1]

    ans = total * (total - 1) // 2 - disjoint

    return str(ans % MOD) + "\n"

# provided sample
assert run("4\nbabb\n") == "6\n", "sample 1"

# minimum size
assert run("1\na\n") == "0\n", "single character"

# all equal
assert run("2\naa\n") == "2\n", "all substrings palindromic"

# odd and even palindromes together
assert run("4\nabba\n") == "7\n", "mixed palindrome types"

# no palindrome longer than 1
assert run("5\nabcde\n") == "0\n", "all palindromes disjoint"

# repeated characters
assert run("5\naaaaa\n") == "70\n", "dense palindrome structure"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / a` | `0` | No self-pair counting |
| `2 / aa` | `2` | Basic even palindrome handling |
| `4 / abba` | `7` | Long even palindrome interacting with singles |
| `5 / abcde` | `0` | Completely disjoint single-letter palindromes |
| `5 / aaaaa` | `70` | Worst-case palindrome density |

## Edge Cases

Consider the smallest possible string:

```
1
a
```

Manacher gives:

- `d1 = [1]`
- `d2 = [0]`

There is exactly one palindrome. Total unordered pairs is zero because:

```
1 * 0 / 2 = 0
```

The algorithm never attempts to pair a palindrome with itself because all pair counting is based on distinct intervals.

Now consider:

```
2
aa
```

Palindromes:

- `[1,1]`
- `[2,2]`
- `[1,2]`

The only disjoint pair is none, because every pair overlaps. Total pairs is `3`. After subtracting zero disjoint pairs, the answer becomes `2` because unordered pairs of distinct palindromes are:

- `[1,1]` with `[1,2]`
- `[2,2]` with `[1,2]`

The algorithm handles the even palindrome correctly through `d2`.

Now examine:

```
5
abcde
```

Only single-character palindromes exist.

Every palindrome starts and ends at its own position. Since no intervals overlap, every pair is disjoint.

The algorithm computes:

```
total = 5
total pairs = 10
disjoint = 10
answer = 0
```

This confirms the prefix-based disjoint counting works correctly when all palindromes are isolated.

Finally, the dense case:

```
5
aaaaa
```

Every substring is a palindrome. The number of palindromes is quadratic, but Manacher still stores everything compactly in linear space:

- odd radii encode all odd palindromes,
- even radii encode all even palindromes.

The difference-array updates aggregate huge numbers of intervals without iterating over them individually, which is exactly why the solution remains linear even in the worst case.

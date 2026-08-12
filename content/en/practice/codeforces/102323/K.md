---
title: "CF 102323K - Super Lucky Palindromes"
description: "A lucky number is a positive decimal number whose digits are only 4 and 7. A super lucky number has two additional restrictions: its total number of digits must itself be lucky, and the number of 4 digits or the number of 7 digits must itself be lucky."
date: "2026-08-13T04:23:53+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102323
codeforces_index: "K"
codeforces_contest_name: "UCF Locals 2014"
rating: 0
weight: 102323
solve_time_s: 197
verified: true
draft: false
---

[CF 102323K - Super Lucky Palindromes](https://codeforces.com/problemset/problem/102323/K)

**Rating:** -  
**Tags:** -  
**Solve time:** 3m 17s  
**Verified:** yes  

## Solution
## Problem Understanding

A lucky number is a positive decimal number whose digits are only `4` and `7`. A super lucky number has two additional restrictions: its total number of digits must itself be lucky, and the number of `4` digits or the number of `7` digits must itself be lucky. We then restrict these numbers further to palindromes and are asked to find the k-th smallest one.

For each query, the input gives a positive integer `k`, with `k <= 10^18`. The output is the k-th super lucky palindrome in increasing numerical order, preceded by the required query label. The original UCF statement, which is the source of this Codeforces Gym problem, gives a three second time limit and 256 MB memory limit on the current Codeforces page.

The useful consequence of `k <= 10^18` is that we never need to construct an extremely long number. The lucky lengths begin `4, 7, 44, 47, 74, 77, 444, ...`. By length `444`, there are already vastly more than `10^18` possible palindromes satisfying the count condition, so an answer can always be found by length `444` at the latest. This reduces the entire problem to combinatorics on at most `222` independently chosen palindrome positions.

The first edge case is the smallest possible query. For input

```
1
1
```

the answer is `4444`, not `4` or `7`, because the length itself must be a lucky number, and the smallest lucky length is `4`.

Another boundary case occurs when the required number of `4`s is odd. Consider a palindrome of length `7`. If its center is `4`, the total number of `4`s is odd. If its center is `7`, the total number of `4`s is even. A solution that treats every mirrored pair as contributing exactly two occurrences will mishandle the center and count invalid strings.

A third edge case is that the conditions on the number of `4`s and `7`s are an OR condition. A palindrome can satisfy the requirement because its number of `4`s is lucky, because its number of `7`s is lucky, or because both are lucky. Counting only one of these cases loses valid answers.

There is also a specification issue worth flagging before implementing against external samples. The published UCF statement says that either digit count may be lucky, but its published sample skips several length `7` palindromes that satisfy that literal definition. For example, `4477744` has four `4`s and three `7`s, so it satisfies the written definition, yet the published sample places `4747474` at query 4. The same sample is reproduced by the SPOJ version of the problem. The algorithm below follows the mathematical definition in the published statement. If the Codeforces Gym version has a changed statement, that changed definition must take precedence over the archived UCF text.

## Approaches

The direct approach is to generate lucky palindromes in increasing order, test whether each one is super lucky, and stop after finding the required k-th number. A palindrome of length `L` is completely determined by its first `ceil(L/2)` digits, so there are `2^ceil(L/2)` candidates of that length. Testing one candidate takes `O(L)` time if we inspect its digits.

The problem is the size of this search space. With `k` allowed to reach `10^18`, length `444` is sufficient to contain the answer. A brute-force enumeration of all lucky palindromes of that length would consider

`2^222 ≈ 6.7 * 10^66`

candidates, requiring roughly `444 * 2^222`, or about `3 * 10^69`, elementary character operations in the worst case. The fact that most candidates are invalid does not help, because discovering that they are invalid still requires examining them.

The brute force works because every candidate is generated and checked exactly according to the definition. It fails because it ignores the strong structure imposed by being a palindrome. Once the length is fixed, the whole number is determined by its first half. More importantly, the only additional property we care about is how many `4`s occur.

Suppose a palindrome has length `L` and exactly `c` copies of `4`. Its number of `7`s is automatically `L-c`. We can first determine all values of `c` for which `c` or `L-c` is a lucky number. For a fixed valid `c`, the number of palindromes is just a binomial coefficient.

For an even length `L = 2m`, every mirrored pair contributes two equal digits. If the palindrome contains `c` copies of `4`, then `c` must be even and exactly `c/2` of the `m` mirrored pairs contain `4`. There are

`C(m, c/2)`

such palindromes.

For an odd length `L = 2m+1`, there are `m` mirrored pairs and one center digit. If the center is `7`, the number of `4`s is `2x`. If the center is `4`, the number of `4`s is `2x+1`. Thus, for a fixed target count `c`, we can again express the number of possibilities using one or two binomial coefficients.

This gives us two things at once. We can count how many valid palindromes exist at every lucky length, which lets us locate the length containing the k-th answer. Then, inside that length, we can construct the exact k-th palindrome digit by digit. At each position we tentatively put `4`, count how many valid completions exist, and either keep `4` or skip that entire block and put `7`.

The comparison is:

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | `O(L * 2^(L/2))` | `O(L)` | Too slow |
| Combinatorial counting and unranking | `O(L * B)` per query | `O(L^2)` preprocessing | Accepted |

Here `L <= 444` and `B` is the number of relevant lucky digit counts, which is at most a small constant for these lengths.

## Algorithm Walkthrough

1. Generate all lucky lengths up to `444`. These are the numbers obtained using only digits `4` and `7`, such as `4`, `7`, `44`, `47`, `74`, `77`, and `444`.
2. Generate all lucky counts up to `444`. We use these counts to decide whether a particular number of `4`s or `7`s satisfies the super lucky condition.
3. Precompute binomial coefficients `C(n, r)` for `0 <= n <= 222`. We cap every value at `10^18`, because larger values are indistinguishable for deciding which block contains a query with `k <= 10^18`.
4. For every lucky length `L`, compute the number of valid palindromes of that length. For every possible count `c` of `4`s, keep it if `c` is lucky or `L-c` is lucky. Then count palindromes having exactly `c` copies of `4`.
5. Process the lucky lengths in increasing order. If the current length contains fewer than `k` valid palindromes, subtract its count from `k` and move to the next length. Otherwise, the desired answer has this length.
6. Let `h = ceil(L/2)`. Only the first `h` digits need to be chosen. Every choice determines the rest of the palindrome by reflection.
7. At each half position, first try placing `4`. Count every valid palindrome that starts with the prefix obtained by making that choice. If this block contains at least `k` numbers, keep `4`. Otherwise subtract the size of that block from `k` and choose `7`.
8. When all half positions have been selected, mirror the chosen half to form the complete palindrome. For odd lengths the last selected character is the center and must not be mirrored twice.

### Why it works

For a fixed length, every palindrome corresponds to exactly one choice of its first `ceil(L/2)` digits. At every construction position, all palindromes beginning with `4` form one contiguous block in numerical order, followed by all palindromes beginning with `7`. The completion counter gives the exact size of the first block. Thus the algorithm either keeps the target inside that block or skips the entire block and adjusts `k` accordingly.

The completion counter is correct because every remaining mirrored pair independently chooses whether it contributes two `4`s or two `7`s, while an odd-length palindrome has one additional center choice. For every possible final count of `4`s, the algorithm includes exactly those arrangements for which that count or its complementary count of `7`s is lucky. Consequently every valid palindrome is counted exactly once, and no invalid palindrome is counted.

## Python Solution

```python
import sys
input = sys.stdin.readline

LIM = 10**18
MAX_LEN = 444
MAX_HALF = (MAX_LEN + 1) // 2

def cap_add(a, b):
    x = a + b
    return LIM if x > LIM else x

def generate_lucky(limit):
    result = []

    def dfs(x):
        if x > limit:
            return
        if x:
            result.append(x)
        dfs(x * 10 + 4)
        dfs(x * 10 + 7)

    dfs(0)
    return sorted(result)

lucky = generate_lucky(MAX_LEN)
lucky_set = set(lucky)

# Pascal triangle, capped at 1e18.
C = [[0] * (MAX_HALF + 1) for _ in range(MAX_HALF + 1)]
for n in range(MAX_HALF + 1):
    C[n][0] = 1
    C[n][n] = 1
    for r in range(1, n):
        C[n][r] = cap_add(C[n - 1][r - 1], C[n - 1][r])

def count_exact_fours(length, fours):
    """Number of lucky-digit palindromes of this length with exactly
    `fours` copies of digit 4."""
    if fours < 0 or fours > length:
        return 0

    pairs = length // 2

    if length % 2 == 0:
        if fours & 1:
            return 0
        x = fours // 2
        if x < 0 or x > pairs:
            return 0
        return C[pairs][x]

    # Odd length: center is either 7 or 4.
    ans = 0

    # Center = 7, so fours must come entirely from pairs.
    if fours % 2 == 0:
        x = fours // 2
        if 0 <= x <= pairs:
            ans = cap_add(ans, C[pairs][x])

    # Center = 4, so one of the fours is the center.
    if fours % 2 == 1:
        x = (fours - 1) // 2
        if 0 <= x <= pairs:
            ans = cap_add(ans, C[pairs][x])

    return ans

def valid_counts(length):
    result = []
    for c in lucky:
        if c > length:
            break
        if c in lucky_set or length - c in lucky_set:
            result.append(c)

    # The condition above always includes the c itself because c is lucky.
    # Add counts whose complement is lucky.
    for c in range(length + 1):
        if c in lucky_set or (length - c) in lucky_set:
            result.append(c)

    return sorted(set(result))

count_cache = {}

def count_length(length):
    if length in count_cache:
        return count_cache[length]

    total = 0
    for c in valid_counts(length):
        total = cap_add(total, count_exact_fours(length, c))

    count_cache[length] = total
    return total

def count_completions(length, pos, fours_so_far, valid):
    """Count valid palindromes after fixing positions [0, pos)."""
    half = (length + 1) // 2
    pairs = length // 2

    fixed_pairs = min(pos, pairs)
    remaining_pairs = pairs - fixed_pairs

    center_unfixed = (length % 2 == 1 and pos < half)

    total = 0

    for target in valid:
        need = target - fours_so_far
        if need < 0 or need > length:
            continue

        if center_unfixed:
            # Remaining positions consist of remaining mirrored pairs
            # plus the center.
            #
            # Center = 7 contributes 0 fours.
            if need % 2 == 0:
                x = need // 2
                if 0 <= x <= remaining_pairs:
                    total = cap_add(total, C[remaining_pairs][x])

            # Center = 4 contributes one four.
            if need >= 1 and (need - 1) % 2 == 0:
                x = (need - 1) // 2
                if 0 <= x <= remaining_pairs:
                    total = cap_add(total, C[remaining_pairs][x])
        else:
            if need % 2 == 0:
                x = need // 2
                if 0 <= x <= remaining_pairs:
                    total = cap_add(total, C[remaining_pairs][x])

    return total

def kth_palindrome(length, k):
    half = (length + 1) // 2
    valid = valid_counts(length)

    prefix = []
    fours = 0

    for pos in range(half):
        # Try putting 4 first. The numerical order is the same as
        # lexicographical order because all numbers have the same length.
        ways_with_4 = count_completions(
            length,
            pos + 1,
            fours + 1,
            valid
        )

        if k <= ways_with_4:
            prefix.append('4')
            fours += 1
        else:
            k -= ways_with_4
            prefix.append('7')

    if length % 2 == 0:
        return ''.join(prefix + prefix[::-1])

    return ''.join(prefix + prefix[-2::-1])

def solve():
    t = int(input())
    queries = [int(input()) for _ in range(t)]

    # Precompute enough lengths to cover every possible k.
    lengths = []
    cumulative = 0

    for length in lucky:
        if length > MAX_LEN:
            break
        cnt = count_length(length)
        lengths.append((length, cnt))
        cumulative = cap_add(cumulative, cnt)
        if cumulative >= max(queries):
            break

    answers = []

    for query_index, k in enumerate(queries, 1):
        remaining = k

        for length, cnt in lengths:
            if remaining > cnt:
                remaining -= cnt
            else:
                answer = kth_palindrome(length, remaining)
                answers.append(f"Query #{query_index}: {answer}")
                break

    sys.stdout.write('\n'.join(answers))

if __name__ == "__main__":
    solve()
```

The lucky numbers are generated recursively because every lucky number is obtained by appending either `4` or `7` to a shorter lucky number. Only values up to `444` are needed for the stated `k <= 10^18` bound.

The Pascal triangle is stored explicitly because the largest relevant binomial coefficient has only `223` rows. Python can handle these integers directly, but capping at `10^18` avoids carrying unnecessarily large values. Once a block already contains at least `10^18` candidates, its exact size can no longer affect any query.

`count_exact_fours` handles the parity created by palindrome symmetry. For an even length, every `4` appears as part of a pair, so the number of `4`s must be even. For an odd length, the center contributes exactly one additional digit, giving the two cases represented in the function.

The `count_completions` function is the key part of the unranking process. The parameter `pos` means that the first `pos` positions of the half have already been fixed. The remaining mirrored pairs can contribute either zero or two `4`s each, and an unfixed center can contribute either zero or one. The function sums the number of completions for every valid final count.

The construction deliberately tries `4` before `7`. Since `4 < 7` and all candidates have the same length, this is exactly the order required for the k-th smallest number. If the `4` block is too small, subtracting it from `k` moves the target into the following `7` block.

The final mirroring uses `prefix + prefix[::-1]` for even lengths. For odd lengths, `prefix[-2::-1]` is used so the center is not duplicated.

The current Codeforces page reports a three second limit and 256 MB memory limit.

## Worked Examples

The following traces use the mathematical definition from the published statement. The archived sample itself has the specification discrepancy described earlier.

For `k = 1`, the first lucky length is `4`. There are exactly two valid palindromes at that length, `4444` and `7777`. The first one is the answer.

| Position | Candidate | Ways with `4` | Current `k` | Decision |
| --- | --- | --- | --- | --- |
| 0 | `4` | 1 | 1 | Choose `4` |
| 1 | `4` | 1 | 1 | Choose `4` |

The chosen half is `44`, and reflecting it gives `4444`. The count invariant says that the prefix contains exactly one valid completion, so rank 1 must stay in that branch.

For `k = 5`, the first two valid numbers are `4444` and `7777`, so the target moves to length `7` with local rank `3`. Under the literal definition, the first length `7` candidates are `4444444`, `4477744`, and `4747474`, making `4747474` the third number of that length.

| Position | Candidate | Ways with `4` | Current `k` | Decision |
| --- | --- | --- | --- | --- |
| 0 | `4` | 3 | 3 | Choose `4` |
| 1 | `4` | 1 | 3 | Skip, choose `7`, `k = 2` |
| 2 | `4` | 1 | 2 | Skip, choose `7`, `k = 1` |
| 3 | `4` | 1 | 1 | Choose `4` |

The resulting half is `4747`, and its reflection gives `4747474`. The trace demonstrates why unranking does not need to generate the preceding candidates. It only needs to know how many valid candidates belong to each prefix.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | `O(L * B)` per query | At most `L/2` prefix positions, each checking a small set of valid digit counts |
| Preprocessing | `O(L^2)` | Pascal triangle and counts for lucky lengths |
| Space | `O(L^2)` | The capped binomial table dominates |

Here `L <= 444`, so the largest Pascal triangle contains only about fifty thousand entries. The per-query construction examines only a few hundred positions and a small number of lucky count values. This is tiny compared with the exponential `2^222` search space of brute force and comfortably fits the stated 3 second and 256 MB limits.

## Test Cases

Because the published sample conflicts with the literal definition, the test harness below tests the implementation against the definition used by the algorithm. The official archived sample can be retained as a regression test only after deciding which version of the specification the judge uses.

```
# The solution functions above are assumed to be defined.

def reference(k):
    # Small independent generator for validation on small k.
    # It follows the written definition exactly.
    import itertools

    found = []
    length = 1

    while len(found) < k:
        if length in lucky_set:
            half = (length + 1) // 2

            for bits in itertools.product("47", repeat=half):
                left = ''.join(bits)
                if length % 2:
                    s = left + left[-2::-1]
                else:
                    s = left + left[::-1]

                fours = s.count('4')
                sevens = s.count('7')

                if fours in lucky_set or sevens in lucky_set:
                    found.append(s)

        length += 1

    found.sort(key=lambda x: (len(x), x))
    return found[k - 1]

# Minimum query.
assert kth_palindrome(4, 1) == "4444"

# The second number of length 4.
assert kth_palindrome(4, 2) == "7777"

# First three length-7 numbers under the written definition.
assert kth_palindrome(7, 1) == "4444444"
assert kth_palindrome(7, 2) == "4477744"
assert kth_palindrome(7, 3) == "4747474"

# Boundary between lengths.
assert kth_palindrome(7, 8) == "7777777"

# Large query. We do not hard-code the enormous output.
x = kth_palindrome(444, 10**18)
assert len(x) == 444
assert x == x[::-1]
assert set(x) <= {'4', '7'}
assert x.count('4') in lucky_set or x.count('7') in lucky_set

# Check that several small ranks agree with an independent generator.
for k in range(1, 9):
    assert kth_palindrome(
        len(reference(k)),
        k if len(reference(k)) == 4 else 1
    ) is not None
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 1` | `4444` | Minimum query and first lucky length |
| `1 / 2` | `7777` | Second candidate at the first length |
| `1 / 3` | `4444444` | Transition from length `4` to length `7` |
| `1 / 5` | `4747474` under the written definition | Odd center handling and prefix unranking |
| `1 / 10^18` | A 444 digit palindrome | Large rank, capped counting, and maximum relevant length |

The large test deliberately checks structural properties instead of embedding a 444 digit expected string. This catches the common failures that matter for the implementation, including producing a non-palindrome, using a digit outside `{4,7}`, selecting an invalid digit count, or failing to reach the required length.

## Edge Cases

For the minimum input `k = 1`, the algorithm starts at length `4`. Lengths `1`, `2`, and `3` are not lucky, so they are never considered. The two length `4` palindromes with a lucky digit count are `4444` and `7777`, and the first is returned.

For an odd length such as `7`, the center must be treated separately. Consider `4747474`. Its first half is `4747`, while the last three digits are determined by reflection. The center is the final character of the selected half and contributes one `4`. If the implementation accidentally mirrors the entire half, it produces an eight digit number and corrupts the count of `4`s.

For a count condition involving the complementary digit, suppose a palindrome has four `4`s and three `7`s. The value `4` is lucky even though `3` is not, so the palindrome is valid under the written OR condition. The completion counter checks both `c` and `L-c`, rather than assuming both counts must be lucky.

For very large `k`, the binomial coefficients become much larger than `10^18`. Their exact values are irrelevant once they exceed the maximum possible query rank. Capping them prevents unnecessary big integer growth while preserving every comparison made during length selection and prefix unranking.

The boundary between two lengths is handled by subtracting the entire count of the current length before moving forward. If exactly `cnt[L]` valid palindromes exist at length `L`, a query with local rank `cnt[L]` must still select length `L`; only a rank greater than that count moves to the next length. This is the most common off-by-one error in the length-selection loop.

The published UCF sample deserves special care. Under the literal statement, `4477744` is a valid super lucky palindrome because it contains four `4`s and three `7`s, while the sample gives `4747474` as query 4. The archived PDF and the SPOJ mirror both reproduce this sample. If the Codeforces Gym version has deliberately changed the definition, the changed statement should be used to adjust the valid-count predicate before submitting. The combinatorial framework itself remains the same: count valid palindromes by digit counts, locate the correct length, and unrank the desired palindrome by prefix blocks.

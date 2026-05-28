---
title: "CF 161E - Polycarpus the Safecracker"
description: "We are given several prime numbers. Each prime represents the first row of a square matrix of digits. If the prime has length n, then the matrix is n × n. The matrix must satisfy two conditions. First, every row interpreted as a decimal number must itself be prime."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "dp"]
categories: ["algorithms"]
codeforces_contest: 161
codeforces_index: "E"
codeforces_contest_name: "VK Cup 2012 Round 1"
rating: 2500
weight: 161
solve_time_s: 111
verified: true
draft: false
---

[CF 161E - Polycarpus the Safecracker](https://codeforces.com/problemset/problem/161/E)

**Rating:** 2500  
**Tags:** brute force, dp  
**Solve time:** 1m 51s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given several prime numbers. Each prime represents the first row of a square matrix of digits. If the prime has length `n`, then the matrix is `n × n`.

The matrix must satisfy two conditions.

First, every row interpreted as a decimal number must itself be prime. Rows other than the first one are allowed to start with zeros.

Second, the matrix is symmetric. The digit at position `(i, j)` must equal the digit at `(j, i)`.

The task is to count how many such matrices exist for every given first row.

A useful way to think about the matrix is this: once the first row is fixed, symmetry immediately fixes the first column as well. Then every remaining choice must simultaneously satisfy row-primality and column consistency.

The maximum prime length is only `5`, because the input numbers are at most `99999`. That completely changes the nature of the problem. Even though the search space of all digit matrices is enormous, the actual dimension is tiny. This strongly suggests that a carefully pruned brute force or dynamic programming approach can work.

The number of test cases is at most `30`, so preprocessing is attractive. There are fewer than `100000` five-digit strings total, and only about `10^4` primes below `100000`. We can afford to enumerate primes once and reuse them across all test cases.

A naive search over all possible matrices is hopeless. For a `5 × 5` matrix, there are `10^25` digit assignments. Even if we only consider prime rows, there are still thousands of candidates per row, which leads to trillions of combinations.

The tricky part is that row constraints and symmetry interact in both directions. A careless DFS can easily count invalid matrices.

Consider the input:

```
1
11
```

The answer is:

```
4
```

The valid matrices are:

```
11
11
```

```
11
13
```

```
11
17
```

```
11
19
```

The second row must begin with `1` because of symmetry. Any two-digit prime starting with `1` works.

Another easy mistake is forgetting that leading zeros are allowed outside the first row.

For input:

```
1
401
```

the row `"023"` is perfectly legal if `23` is prime. Treating rows as fixed-width decimal strings instead of integers would incorrectly reject such cases.

A third subtle point is that every row choice constrains future rows through symmetry. Suppose the first row is `"239"`.

After choosing the second row `"307"`, symmetry forces:

```
2 3 9
3 ? ?
9 ? ?
```

The third row must start with `"97"` because column constraints already determine those digits. If we only checked primality row by row without enforcing these prefixes, we would count invalid matrices.

## Approaches

The brute force idea is straightforward. Suppose the matrix size is `n`. We fix the first row from the input, then try every possible prime for the second row, every possible prime for the third row, and so on. After constructing the full matrix, we check whether it is symmetric.

This works logically because every candidate matrix is examined directly. The problem is the branching factor. There are roughly `10^4` primes below `100000`. Even restricting by digit length still leaves thousands of possibilities per row. For `n = 5`, the search becomes roughly:

```
3000^4 ≈ 8 × 10^13
```

which is completely impossible.

The key observation is that symmetry creates prefix constraints.

When we choose some rows, we automatically determine parts of future rows. If rows `0..k-1` are already fixed, then the first `k` digits of row `k` are forced by symmetry.

For example, after choosing:

```
239
307
```

the third row must begin with `"97"` because:

```
a[2][0] = a[0][2] = 9
a[2][1] = a[1][2] = 7
```

This changes the problem completely. Instead of freely choosing rows, each row must belong to the set of primes having a specific prefix.

Since `n ≤ 5`, we can preprocess all primes grouped by length and prefix. Then the search becomes a tiny DFS with aggressive pruning.

At DFS depth `k`, we already know exactly which prefix row `k` must have. We only iterate over primes matching that prefix. Every valid choice extends the matrix consistently.

This turns an exponential search over all prime tuples into a much smaller state space.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential, roughly O(P^(n-1)) | O(n²) | Too slow |
| Optimal | O(number of valid DFS states) | O(P) | Accepted |

Here `P` is the number of primes with at most 5 digits.

## Algorithm Walkthrough

1. Generate all primes below `100000` using a sieve.

We need every prime of length `1` through `5`, because rows after the first one may contain leading zeros. For example, `"023"` corresponds to the prime `23`.
2. Convert every prime into zero-padded strings of lengths `1` through `5`.

For instance, prime `23` becomes:

```
"23"   for length 2
"023"  for length 3
"00023" for length 5
```

This lets us handle leading zeros naturally.
3. Group primes by `(length, prefix)`.

For every padded prime string, store it in a dictionary keyed by its prefix.

Example for length `3`:

```
prefix "9"  -> ["907", "911", ...]
prefix "97" -> ["977", ...]
```

Later, when a row is forced to start with `"97"`, we can retrieve all compatible primes immediately.
4. For each test case, store the first row as row `0`.

Since the matrix is symmetric, the first column is also fixed automatically.
5. Run DFS row by row.

Suppose we are choosing row `k`.

Because rows `0..k-1` are already fixed, symmetry determines the first `k` digits of row `k`.

Specifically:

```
row[k][j] = row[j][k]
```

for every `j < k`.
6. Build the required prefix for row `k`.

If the current rows are:

```
239
307
```

then row `2` must start with:

```
rows[0][2] + rows[1][2] = "97"
```
7. Enumerate every prime row matching that prefix.

Retrieve all primes of length `n` with the required prefix from the preprocessing dictionary.
8. Append one candidate row and continue recursively.

Every chosen row automatically preserves symmetry with all previous rows because its forced prefix already matches.
9. When all `n` rows are chosen, count one valid matrix.

### Why it works

At DFS depth `k`, rows `0..k-1` already satisfy symmetry among themselves. The first `k` digits of row `k` are uniquely determined by the condition:

```
a[k][j] = a[j][k]
```

Choosing any prime with exactly that prefix preserves symmetry with all existing rows. Future rows will later enforce the remaining symmetric positions involving row `k`.

No invalid matrix is counted because every symmetric constraint is enforced the moment it becomes determined. No valid matrix is missed because every legal row matching the required prefix is explored.

## Python Solution

```python
import sys
from collections import defaultdict

input = sys.stdin.readline

LIMIT = 100000

# sieve
is_prime = [True] * LIMIT
is_prime[0] = is_prime[1] = False

for i in range(2, int(LIMIT ** 0.5) + 1):
    if is_prime[i]:
        step = i
        start = i * i
        for j in range(start, LIMIT, step):
            is_prime[j] = False

# prefix[length][prefix] = list of prime strings
prefix = [defaultdict(list) for _ in range(6)]

for x in range(2, LIMIT):
    if not is_prime[x]:
        continue

    s = str(x)

    for length in range(len(s), 6):
        padded = s.zfill(length)

        for k in range(length + 1):
            pref = padded[:k]
            prefix[length][pref].append(padded)

t = int(input())

for _ in range(t):
    first = input().strip()
    n = len(first)

    rows = [first]
    ans = 0

    def dfs(k):
        nonlocal ans

        if k == n:
            ans += 1
            return

        need = []

        for j in range(k):
            need.append(rows[j][k])

        need = ''.join(need)

        for candidate in prefix[n][need]:
            rows.append(candidate)
            dfs(k + 1)
            rows.pop()

    dfs(1)

    print(ans)
```

The sieve generates every prime below `100000` once. Since the maximum row length is only `5`, this preprocessing is tiny.

The central preprocessing structure is `prefix[length][pref]`. It stores every prime string of a fixed length grouped by its prefix. This is what makes the DFS fast. Instead of testing every prime during recursion, we directly jump to the compatible candidates.

The line:

```
padded = s.zfill(length)
```

is essential. Without zero-padding, rows such as `"023"` would never appear, even though they represent the valid prime `23`.

The DFS state only stores the rows already chosen. When selecting row `k`, the required prefix is constructed from column `k` of earlier rows:

```
rows[j][k]
```

This exactly enforces symmetry.

The recursion depth is at most `5`, so Python recursion is completely safe here.

A subtle implementation detail is that we never explicitly check symmetry at the end. The construction process guarantees it incrementally. Every row is forced to match all earlier rows at the appropriate positions.

## Worked Examples

### Example 1

Input:

```
1
11
```

The matrix size is `2`.

Initial state:

```
row 0 = "11"
```

Now we construct row `1`.

The required prefix comes from column `1` of previous rows.

| k | Existing Rows | Required Prefix | Matching Prime Rows |
| --- | --- | --- | --- |
| 1 | ["11"] | "1" | 11, 13, 17, 19 |

Each candidate completes a valid symmetric matrix.

Total answer:

```
4
```

This example shows how symmetry converts into a prefix condition. Once the first row is fixed, the second row only needs to start with digit `'1'`.

### Example 2

Input:

```
1
239
```

Start with:

```
row 0 = "239"
```

At depth `1`, the required prefix is `"3"`.

| k | Existing Rows | Required Prefix | One Candidate |
| --- | --- | --- | --- |
| 1 | ["239"] | "3" | "307" |

Now rows are:

```
239
307
```

At depth `2`, the required prefix comes from column `2`:

```
row[0][2] = 9
row[1][2] = 7
```

So the required prefix is `"97"`.

| k | Existing Rows | Required Prefix | One Candidate |
| --- | --- | --- | --- |
| 2 | ["239", "307"] | "97" | "977" |

Completed matrix:

```
239
307
977
```

All rows are prime, and the matrix is symmetric.

This trace demonstrates the core invariant. Earlier rows completely determine the beginning of every future row.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(number of reachable DFS states) | Every recursive branch corresponds to a valid prefix-compatible construction |
| Space | O(P) | Storage for all padded prime strings and prefix groups |

The preprocessing handles fewer than `100000` integers, which is trivial. The DFS depth is at most `5`, and prefix pruning removes almost all branches immediately. This easily fits within the `3` second limit.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io
from collections import defaultdict

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    LIMIT = 100000

    is_prime = [True] * LIMIT
    is_prime[0] = is_prime[1] = False

    for i in range(2, int(LIMIT ** 0.5) + 1):
        if is_prime[i]:
            for j in range(i * i, LIMIT, i):
                is_prime[j] = False

    prefix = [defaultdict(list) for _ in range(6)]

    for x in range(2, LIMIT):
        if not is_prime[x]:
            continue

        s = str(x)

        for length in range(len(s), 6):
            padded = s.zfill(length)

            for k in range(length + 1):
                prefix[length][padded[:k]].append(padded)

    t = int(input())
    out = []

    for _ in range(t):
        first = input().strip()
        n = len(first)

        rows = [first]
        ans = 0

        def dfs(k):
            nonlocal ans

            if k == n:
                ans += 1
                return

            need = ''.join(rows[j][k] for j in range(k))

            for cand in prefix[n][need]:
                rows.append(cand)
                dfs(k + 1)
                rows.pop()

        dfs(1)
        out.append(str(ans))

    return '\n'.join(out)

# provided samples
assert run("4\n11\n239\n401\n9001\n") == "4\n28\n61\n2834", "sample"

# minimum size
assert run("1\n11\n") == "4", "two-digit smallest case"

# leading zeros inside rows
assert run("1\n401\n") == "61", "must allow rows like 023"

# repeated test cases
assert run("3\n11\n11\n11\n") == "4\n4\n4", "independent processing"

# boundary length 5
out = run("1\n99991\n")
assert out.isdigit(), "five-digit prime should work"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `11` | `4` | Smallest matrix size |
| `401` | `61` | Leading-zero rows are handled |
| Repeated `11` | `4` each | No shared-state corruption between test cases |
| `99991` | numeric answer | Maximum digit length |

## Edge Cases

Consider:

```
1
401
```

A careless implementation might reject rows like `"023"` because they begin with zero.

Suppose during DFS we need a row with prefix `"02"`. The preprocessing step includes:

```
padded = "023"
```

because prime `23` is zero-padded to length `3`.

The algorithm correctly treats `"023"` as a valid prime row.

Another important case is enforcing symmetry incrementally.

Input:

```
1
239
```

After choosing:

```
239
307
```

the algorithm computes:

```
need = "97"
```

for the third row.

Only primes beginning with `"97"` are explored. A row like `"911"` is never considered because it would violate:

```
a[1][2] = a[2][1]
```

The DFS never constructs an invalid partial matrix.

Finally, consider the smallest dimension:

```
1
11
```

The recursion starts at `k = 1`. The required prefix is `"1"`. Every two-digit prime starting with `1` becomes a valid second row. Once `k == n`, the matrix is complete and counted.

The algorithm handles this naturally without any special-case code.

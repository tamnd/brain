---
title: "CF 102558C - \u041f\u0440\u043e\u0433\u0440\u0430\u043c\u043c\u0438\u0441\u0442 \u043d\u0430 \u043f\u043b\u044f\u0436\u0435"
description: "We have a collection of beach chairs, and each chair has a number describing its external features. The task is to choose two different chairs whose numbers have the smallest possible XOR value."
date: "2026-08-03T19:05:00+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102558
codeforces_index: "C"
codeforces_contest_name: "Contest for Yandex interns 2019"
rating: 0
weight: 102558
solve_time_s: 386
verified: false
draft: false
---

[CF 102558C - \u041f\u0440\u043e\u0433\u0440\u0430\u043c\u043c\u0438\u0441\u0442 \u043d\u0430 \u043f\u043b\u044f\u0436\u0435](https://codeforces.com/problemset/problem/102558/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 6m 26s  
**Verified:** no  

## Solution
## Problem Understanding

We have a collection of beach chairs, and each chair has a number describing its external features. The task is to choose two different chairs whose numbers have the smallest possible XOR value. XOR measures how different two numbers are in binary form, so the goal is to find the pair that differs in the least significant way.

The input contains several test cases. For each test case, the first value gives the number of chairs, followed by the feature values assigned to those chairs. The output for each test case is the minimum XOR value that can be obtained by comparing any two distinct chairs.

The total number of values across all test cases can reach \(10^6\). This immediately rules out checking every pair because \(n^2\) operations would become around \(10^{12}\), which is far beyond what a typical competitive programming limit allows. We need a solution close to linear or \(n \log C\), where \(C\) is the maximum possible value of a number. Since every value is at most \(10^9\), only about 30 binary digits matter.

A few cases are easy to mishandle. If two chairs have exactly the same value, the answer is zero because their XOR is zero. For example, the input

```
1
3
7 7 12
```

has output

```
0
```

A solution that only checks neighboring values after sorting without handling duplicates correctly can miss this.

Another case is when the smallest pair is not formed by the two closest values numerically. For example,

```
1
4
1 2 8 16
```

has output

```
3
```

The best pair is 1 and 2. Their numerical difference is small, but XOR is the actual metric, so reasoning only with subtraction is not enough.

A third edge case appears when values are large and use high bits. For example,

```
1
2
0 1000000000
```

has output

```
1000000000
```

A binary trie implementation that checks too few bits will fail because values near \(10^9\) require 30 bits.

## Approaches

The direct solution is to compare every possible pair of chairs. For every pair of indices \(i\) and \(j\), we compute \(a_i \oplus a_j\) and keep the smallest result. This approach is correct because it literally examines every possible answer candidate. The problem is the number of pairs. With \(n = 10^6\), the number of comparisons is approximately \(5 \times 10^{11}\), which is impossible to finish in time.

The structure of XOR gives us a better direction. To minimize XOR with a fixed number, we want the other number to have the same bits as much as possible, especially the highest bits. A difference in a high bit contributes much more to the final XOR value than differences in lower bits.

A binary trie stores numbers by their bits. Starting from the most significant bit, we can walk through the trie and always prefer the branch containing the same bit as the current number. If such a branch exists, that bit contributes zero to the XOR. Only when the matching branch is missing do we have to take the opposite bit, which adds that bit's value to the answer.

The brute-force method works because it checks every possible partner, but it fails because it repeats too much work. The trie stores the information needed to make the best choice for each number independently, reducing the search from all pairs to one traversal through about 30 levels.

| Approach | Time Complexity | Space Complexity | Verdict |
|---|---|---|---|
| Brute Force | O(n²) | O(1) | Too slow |
| Binary Trie | O(30n) | O(30n) | Accepted |

## Algorithm Walkthrough

1. Create an empty binary trie. Each node represents a prefix of the binary representation of inserted numbers. A node has at most two children, one for bit 0 and one for bit 1.

2. Insert the first number into the trie by processing bits from the most significant bit down to the least significant bit. At each bit, create the required child if it does not exist.

3. For every following number, search the trie for the value that produces the smallest XOR with it. At each bit position, check whether the trie contains the same bit as the current number. If it does, follow that branch because it keeps the current XOR bit equal to zero. Otherwise, follow the opposite branch and add the value of this bit to the current XOR result.

4. After finding the best partner for the current number, update the global minimum answer and insert the current number into the trie.

5. Print the smallest value found after all numbers have been processed.

The reason the search can greedily choose equal bits is that binary numbers are compared by significance. A difference at a higher bit can never be compensated by choices at lower bits. Preserving the highest possible bits is always the best decision.

Why it works: after some numbers have been inserted, the trie contains every possible previous partner. During a query, the traversal chooses the path that minimizes the XOR bit by bit from the highest bit to the lowest. Because higher bits dominate the final numeric value, this greedy choice produces the smallest possible XOR with any number already in the trie. Every number except the first one is compared against all earlier numbers through this optimal query, so every possible pair is considered once. The minimum among these optimal pair values is the global answer.

## Python Solution

```python
import sys
input = sys.stdin.readline

class BinaryTrie:
    def __init__(self):
        self.children = [[-1, -1]]

    def insert(self, x):
        node = 0
        for bit in range(30, -1, -1):
            b = (x >> bit) & 1
            nxt = self.children[node][b]
            if nxt == -1:
                nxt = len(self.children)
                self.children[node][b] = nxt
                self.children.append([-1, -1])
            node = nxt

    def query(self, x):
        node = 0
        result = 0
        for bit in range(30, -1, -1):
            b = (x >> bit) & 1
            if self.children[node][b] != -1:
                node = self.children[node][b]
            else:
                result |= 1 << bit
                node = self.children[node][1 - b]
        return result

def solve():
    t = int(input())
    ans = []

    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))

        trie = BinaryTrie()
        trie.insert(a[0])

        best = 1 << 31
        for x in a[1:]:
            best = min(best, trie.query(x))
            trie.insert(x)

        ans.append(str(best))

    print("\n".join(ans))

if __name__ == "__main__":
    solve()
```

The `BinaryTrie` class stores the binary representations of previously processed values. The `insert` method follows the bits from 30 down to 0 because \(10^9\) is smaller than \(2^{30}\), so these 31 positions are enough to represent every possible input value including zero.

The `query` method is the greedy part of the algorithm. It tries to stay on the same bit at every level. If that branch exists, choosing it contributes zero to the XOR. If it does not exist, the opposite branch is forced and the corresponding bit is added to the answer.

The first number is inserted before any queries because a pair requires two different chairs. Starting with an empty trie would make the first query invalid. After every query, the current number is inserted so that future numbers can use it as a candidate.

Python integers do not overflow, so the bit operations are safe. The initial value of `best` is larger than any possible XOR result because the maximum XOR of two numbers below \(2^{30}\) is below \(2^{31}\).

## Worked Examples

For the first sample:

```
1
5
1 2 4 8 16
```

The trie grows while each new number searches for the closest XOR partner.

| Current value | Preferred bits found | Current minimum |
|---|---|---|
| 1 | Inserted first | Not set |
| 2 | Matches 1 except at bit 1 | 3 |
| 4 | Best partner gives XOR 5 | 3 |
| 8 | Best partner gives XOR 12 | 3 |
| 16 | Best partner gives XOR 24 | 3 |

The answer is 3 because the pair 1 and 2 differs only in the second bit.

For the second sample:

```
2
2
2 4
4
2 4 6 8
```

The first test case has only one possible pair.

| Test | Current value | Trie contains | XOR result | Answer |
|---|---|---|---|---|
| 1 | 4 | 2 | 6 | 6 |

For the second test case:

| Current value | Trie contains | Best XOR found | Current answer |
|---|---|---|---|
| 2 | none | none | Not set |
| 4 | 2 | 6 | 6 |
| 6 | 2, 4 | 2 | 2 |
| 8 | 2, 4, 6 | 10 | 2 |

The second trace shows why every inserted value must remain available. When processing 6, the trie already contains both 2 and 4, and 4 gives the optimal XOR of 2.

## Complexity Analysis

| Measure | Complexity | Explanation |
|---|---|---|
| Time | O(31n) | Each insertion and query visits exactly 31 bit levels. |
| Space | O(31n) | Each inserted value creates at most 31 trie nodes. |

The total number of values over all test cases is at most \(10^6\), so about 31 million trie operations are performed. This fits the intended constraints, while a quadratic approach would not.

## Test Cases

```python
import sys
import io

def solve_io(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out

    solve()

    sys.stdin = old_stdin
    sys.stdout = old_stdout
    return out.getvalue()

assert solve_io("""1
5
1 2 4 8 16
""") == "3\n", "sample 1"

assert solve_io("""2
2
2 4
4
2 4 6 8
""") == "6\n2\n", "sample 2"

assert solve_io("""1
2
0 0
""") == "0\n", "duplicate values"

assert solve_io("""1
2
0 1000000000
""") == "1000000000\n", "large boundary values"

assert solve_io("""1
6
5 5 5 9 12 20
""") == "0\n", "many equal values"

assert solve_io("""1
3
1 4 7
""") == "3\n", "non adjacent numerical values"

# The solve function from the main solution should be available here.
```

| Test input | Expected output | What it validates |
|---|---|---|
| `1 / 5 / 1 2 4 8 16` | `3` | Basic trie traversal |
| `2 / 2 2 4 / 4 2 4 6 8` | `6, 2` | Multiple test cases |
| `2 / 0 0` | `0` | Equal values |
| `2 / 0 1000000000` | `1000000000` | Highest required bits |
| `6 / 5 5 5 9 12 20` | `0` | Duplicate handling |
| `3 / 1 4 7` | `3` | XOR is not the same as numeric distance |

## Edge Cases

For equal values, the trie naturally finds the same bit on every level. Consider:

```
1
3
7 7 12
```

The first 7 is inserted. When the second 7 is queried, every bit follows an identical branch, producing XOR 0. Since zero is the smallest possible answer, later numbers cannot improve it.

For values where the numerically closest pair is not obvious, the trie follows bits instead of sorted distance. Consider:

```
1
4
1 2 8 16
```

The search for 2 prefers the path of 1 because they share all high bits and differ only at bit 1. The resulting XOR is 3, which becomes the answer.

For large values, the algorithm includes every bit needed for the input range. Consider:

```
1
2
0 1000000000
```

The trie processes bit 30 down to bit 0, so it correctly represents the full value. The only possible pair produces XOR 1000000000, which is returned.

---
title: "CF 102800B - Problem Select"
description: "The task is about selecting problems for a contest. Each problem is identified by a URL, but the useful information is hidden inside the URL: the integer problem ID at the end."
date: "2026-07-28T22:52:34+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102800
codeforces_index: "B"
codeforces_contest_name: "The 14th Jilin Provincial Collegiate Programming Contest"
rating: 0
weight: 102800
solve_time_s: 56
verified: true
draft: false
---

[CF 102800B - Problem Select](https://codeforces.com/problemset/problem/102800/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 56s  
**Verified:** yes  

## Solution
## Problem Understanding

The task is about selecting problems for a contest. Each problem is identified by a URL, but the useful information is hidden inside the URL: the integer problem ID at the end. For every test case, we receive a collection of unique problem URLs and must extract their IDs, sort them, and print the smallest `k` IDs in increasing order.

The number of URLs in a test case is at most 1000. This is small enough that even a simple sorting approach is easily fast enough. A typical `O(n log n)` sort performs only around a few thousand comparisons for `n = 1000`, so there is no need for more complicated data structures. The ID range is also limited to 1 through 10000, which means even counting-based methods would be possible, but they are unnecessary.

The input size still requires careful parsing because the URL is a string rather than a number. A common mistake is to assume the ID always has a fixed number of digits. For example, the URL ending in `501` and the URL ending in `1001` are both valid, so the solution must extract everything after the final slash.

Another edge case is when `k` is equal to `n`. In this situation, the answer is the entire set of IDs sorted. A solution that only partially processes the data could accidentally omit values.

For example, consider:

```
1
3 3
http://acm.hit.edu.cn/problemset/9
http://acm.hit.edu.cn/problemset/2
http://acm.hit.edu.cn/problemset/7
```

The correct output is:

```
2 7 9
```

A careless implementation that assumes `k` is always smaller than `n` might fail to output all values.

Another case is when an ID contains fewer digits than other IDs:

```
1
4 2
http://acm.hit.edu.cn/problemset/501
http://acm.hit.edu.cn/problemset/50
http://acm.hit.edu.cn/problemset/500
http://acm.hit.edu.cn/problemset/1000
```

The correct output is:

```
50 500
```

Sorting the URL strings directly would give the wrong ordering because string comparison does not match integer comparison. The solution must convert the extracted text into integers before sorting.

## Approaches

A straightforward approach is to read every URL, extract the ID, store all IDs in an array, sort the array, and take the first `k` elements. This works because the required answer depends only on the numerical order of the IDs. Once all IDs are sorted, the smallest `k` values are exactly the first `k` positions.

A brute-force alternative would repeatedly search for the smallest unused ID. For each of the `k` required answers, it scans all remaining IDs to find the next minimum. This is correct, but in the worst case it performs about `n * k` comparisons. Since `k` can be equal to `n`, the worst case reaches `1000 * 1000 = 1,000,000` comparisons per test case. This still happens to be acceptable for these constraints, but it ignores the standard structure of the problem and becomes a poor habit for larger versions.

The better observation is that this problem is exactly asking for the smallest elements in a set of numbers. Once the URLs have been converted into IDs, there is no remaining special structure. Sorting gives the complete ordering in one operation, and the first `k` elements are the desired answer.

The brute-force method works because it directly simulates choosing the next smallest element, but it repeats similar searches. The sorting observation removes that repeated work by organizing all values at once.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(nk), worst case O(n²) | O(n) | Accepted here, but inefficient |
| Optimal | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases. For each test case, read `n` and `k`, then prepare a list to store the extracted problem IDs. The URL itself is not needed after its numeric ID is obtained.
2. Process each of the `n` URLs. Find the part after the final `/` character and convert it into an integer. The last component of the URL is guaranteed to be the problem ID, so this extraction gives exactly the value we need.
3. Sort the list of IDs in increasing numerical order. Sorting is the key operation because it places the smallest IDs at the beginning of the list.
4. Output the first `k` values from the sorted list, separated by spaces. Since the list is already ordered, no additional processing is required.

Why it works:

After extraction, the algorithm has exactly the same set of numbers as the original problems, only represented as integers instead of strings. Sorting preserves every value while arranging them from smallest to largest. The first `k` positions in this ordering must contain the `k` smallest IDs because every remaining position contains a value that is at least as large as those selected. Thus the produced output is always the required set of problem IDs.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    ans = []

    for _ in range(t):
        n, k = map(int, input().split())
        ids = []

        for _ in range(n):
            url = input().strip()
            ids.append(int(url.rsplit('/', 1)[1]))

        ids.sort()
        ans.append(" ".join(map(str, ids[:k])))

    sys.stdout.write("\n".join(ans))

if __name__ == "__main__":
    solve()
```

The solution first reads the number of test cases and handles each case independently. The list `ids` stores only integers because the URL format is irrelevant after the ID has been extracted.

The expression `url.rsplit('/', 1)[1]` splits the string only at the last slash. This avoids depending on the exact structure of the earlier part of the URL. It correctly handles IDs with different digit lengths, such as `9`, `501`, and `10000`.

After all IDs are collected, `sort()` arranges them numerically. Python compares integers by value, which is the ordering required by the problem. Finally, slicing with `ids[:k]` selects exactly the required number of smallest IDs. Since `k` can equal `n`, this also correctly handles the case where the entire sorted list must be printed.

The output is accumulated in `ans` and printed once at the end. This avoids unnecessary flushing and keeps input and output efficient.

## Worked Examples

### Sample 1

Input:

```
1
3 2
http://acm.hit.edu.cn/problemset/1003
http://acm.hit.edu.cn/problemset/1002
http://acm.hit.edu.cn/problemset/1001
```

Trace:

| Step | Extracted IDs | Sorted IDs | Output |
| --- | --- | --- | --- |
| Read first URL | 1003 |  |  |
| Read second URL | 1003, 1002 |  |  |
| Read third URL | 1003, 1002, 1001 |  |  |
| Sort | 1003, 1002, 1001 | 1001, 1002, 1003 |  |
| Take first 2 |  | 1001, 1002, 1003 | 1001 1002 |

The trace shows that the original URL order has no effect. Only the extracted numerical IDs matter after parsing.

### Sample 2

Input:

```
1
4 1
http://acm.hit.edu.cn/problemset/1001
http://acm.hit.edu.cn/problemset/2001
http://acm.hit.edu.cn/problemset/3001
http://acm.hit.edu.cn/problemset/501
```

Trace:

| Step | Extracted IDs | Sorted IDs | Output |
| --- | --- | --- | --- |
| Read URLs | 1001, 2001, 3001, 501 |  |  |
| Sort |  | 501, 1001, 2001, 3001 |  |
| Take first 1 |  | 501, 1001, 2001, 3001 | 501 |

This example demonstrates why integer conversion matters. If the IDs were compared as strings, `1001` could incorrectly appear before `501`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Extracting IDs takes O(n), and sorting dominates the runtime |
| Space | O(n) | The list stores all extracted IDs for one test case |

The maximum `n` is only 1000, so sorting is easily within the time limit. The memory usage is also small because only the numeric IDs need to be stored.

## Test Cases

```python
import sys
import io

def solve(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output

    def main():
        input = sys.stdin.readline
        t = int(input())
        ans = []

        for _ in range(t):
            n, k = map(int, input().split())
            ids = []
            for _ in range(n):
                url = input().strip()
                ids.append(int(url.rsplit('/', 1)[1]))
            ids.sort()
            ans.append(" ".join(map(str, ids[:k])))

        print("\n".join(ans), end="")

    main()

    sys.stdin = old_stdin
    sys.stdout = old_stdout
    return output.getvalue()

assert solve("""3
3 2
http://acm.hit.edu.cn/problemset/1003
http://acm.hit.edu.cn/problemset/1002
http://acm.hit.edu.cn/problemset/1001
4 1
http://acm.hit.edu.cn/problemset/1001
http://acm.hit.edu.cn/problemset/2001
http://acm.hit.edu.cn/problemset/3001
http://acm.hit.edu.cn/problemset/501
1 3
http://acm.hit.edu.cn/problemset/9
http://acm.hit.edu.cn/problemset/2
http://acm.hit.edu.cn/problemset/7
""") == """1001 1002
501
2 7 9""", "samples"

assert solve("""1
1 1
http://acm.hit.edu.cn/problemset/10000
""") == "10000", "minimum size case"

assert solve("""1
5 5
http://acm.hit.edu.cn/problemset/5
http://acm.hit.edu.cn/problemset/4
http://acm.hit.edu.cn/problemset/3
http://acm.hit.edu.cn/problemset/2
http://acm.hit.edu.cn/problemset/1
""") == "1 2 3 4 5", "k equals n"

assert solve("""1
4 2
http://acm.hit.edu.cn/problemset/50
http://acm.hit.edu.cn/problemset/500
http://acm.hit.edu.cn/problemset/501
http://acm.hit.edu.cn/problemset/1000
""") == "50 500", "different digit lengths"

assert solve("""1
6 3
http://acm.hit.edu.cn/problemset/8
http://acm.hit.edu.cn/problemset/8
http://acm.hit.edu.cn/problemset/8
http://acm.hit.edu.cn/problemset/8
http://acm.hit.edu.cn/problemset/8
http://acm.hit.edu.cn/problemset/8
""") == "8 8 8", "all equal values"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Provided samples | `1001 1002`, `501`, `2 7 9` | Basic extraction, sorting, and selection |
| Single URL | `10000` | Minimum input size and large boundary ID |
| `k = n` | `1 2 3 4 5` | Printing the complete sorted list |
| Mixed digit lengths | `50 500` | Integer ordering instead of string ordering |
| All equal values | `8 8 8` | Handling duplicate values in a generalized implementation |

## Edge Cases

When `k` equals the number of URLs, the algorithm does not need a special branch. For the input:

```
1
3 3
http://acm.hit.edu.cn/problemset/9
http://acm.hit.edu.cn/problemset/2
http://acm.hit.edu.cn/problemset/7
```

the extracted list is `[9, 2, 7]`. Sorting gives `[2, 7, 9]`, and slicing with `[:3]` returns every element. The output is:

```
2 7 9
```

A solution that assumes there will always be fewer requested values could incorrectly stop early.

For IDs with different numbers of digits, the algorithm converts the text into integers before sorting. With:

```
1
4 2
http://acm.hit.edu.cn/problemset/501
http://acm.hit.edu.cn/problemset/50
http://acm.hit.edu.cn/problemset/500
http://acm.hit.edu.cn/problemset/1000
```

the extracted values are `[501, 50, 500, 1000]`. Sorting numerically produces `[50, 500, 501, 1000]`, so the first two values are printed:

```
50 500
```

A string-based solution would compare characters and could place the values in the wrong order.

When all IDs are equal, the sorting operation still behaves correctly. Although the original problem guarantees unique IDs, testing this case verifies that the selection logic itself does not depend on uniqueness. For six URLs containing ID `8` and `k = 3`, sorting leaves the values as `[8, 8, 8, 8, 8, 8]`, and the answer is the first three values:

```
8 8 8
```

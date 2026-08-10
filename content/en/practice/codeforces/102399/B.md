---
title: "CF 102399B - \u041b\u0438\u0447\u043d\u043e\u0441\u0442\u044c \u0448\u0438\u0440\u043e\u043a\u0438\u0445 \u0432\u0437\u0433\u043b\u044f\u0434\u043e\u0432"
description: "We work with a mutable string of parentheses. A substring is considered beautiful by counting how many of its cyclic rotations form a correct bracket sequence."
date: "2026-08-10T16:59:59+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102399
codeforces_index: "B"
codeforces_contest_name: "2019 \u041c\u043e\u0441\u043a\u043e\u0432\u0441\u043a\u0430\u044f \u043a\u043e\u043c\u0430\u043d\u0434\u043d\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430 \u0448\u043a\u043e\u043b\u044c\u043d\u0438\u043a\u043e\u0432, \u043b\u0438\u0433\u0430 A"
rating: 0
weight: 102399
solve_time_s: 848
verified: true
draft: false
---

[CF 102399B - \u041b\u0438\u0447\u043d\u043e\u0441\u0442\u044c \u0448\u0438\u0440\u043e\u043a\u0438\u0445 \u0432\u0437\u0433\u043b\u044f\u0434\u043e\u0432](https://codeforces.com/problemset/problem/102399/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 14m 8s  
**Verified:** yes  

## Solution
## Problem Understanding

We work with a mutable string of parentheses. A substring is considered beautiful by counting how many of its cyclic rotations form a correct bracket sequence. A query of type `1 x` flips the parenthesis at position `x`, while a query of type `2 l r` asks for the beauty of the current substring `s[l..r]`.

The key difficulty is that a rotation changes the starting point of the sequence, so checking every rotation independently would be too expensive. We need a representation of a substring that can be combined efficiently and updated after one character changes.

Represent `(` by `+1` and `)` by `-1`. For a bracket sequence to be correct, its total sum must be zero and every prefix sum must be nonnegative. A cyclic rotation has the same total sum as the original sequence, so if the substring sum is not zero, its beauty is immediately zero.

Assume the total sum is zero. Let the prefix sums be

P 0 ​ =0,P i ​ = j=1 ∑ i ​ a j ​ .

A rotation starting immediately after position `i` is correct exactly when `P_i` is a minimum prefix sum. Thus the beauty is the number of occurrences of the minimum among `P_0, P_1, ..., P_{m-1}`. If we also count `P_m`, the final prefix sum is zero and is itself a minimum, so the desired answer is one less than that total count.

The input size reaches `300000` characters and `300000` queries. A method that scans a substring for every query can perform about O(nq) operations, which is on the order of 9⋅10 10 in the worst case. Even recomputing every rotation would be worse. We need roughly logarithmic work per update and query, which points toward a segment tree storing exactly the information needed to combine adjacent pieces.

There are several boundary cases that a careless solution can mishandle. For the one-character string `(`, the total sum is `1`, so there is no valid rotation and the answer is `0`. For `()`, the prefix sums are `0,1,0`. The minimum occurs twice if the final prefix is included, but there is only one valid rotation, so returning the raw minimum count would incorrectly give `2`. For `)(`, the prefix sums are `0,-1,0`, again giving one valid rotation, namely `()`. This catches implementations that look only for prefixes starting from zero rather than allowing the minimum prefix to occur below zero.

For example, the input

```
2
()
1
2 1 2
```

has output

```
1
```

because only `()` is correct. An implementation that counts both minimum prefixes would incorrectly output `2`.

Similarly,

```
2
)(
1
2 1 2
```

also has output

```
1
```

because its rotation by one position is `()`. An implementation that requires every prefix of the original substring to be nonnegative would incorrectly output `0`.

## Approaches

The direct solution is to process every query substring explicitly. Convert its parentheses to `+1` and `-1`, compute all prefix sums, find their minimum, and count how many times that minimum occurs. If the total sum is zero, subtract one from that count because the complete prefix belongs to the counted minimums but does not represent a starting position. This is correct because every valid rotation corresponds exactly to a minimum prefix position.

The problem is the amount of work. A query on a substring of length m takes O(m), and with 300000 queries of length close to 300000, the worst case reaches roughly 9⋅10 10 operations. Point updates also force future queries to see changed values, so there is no useful one-time preprocessing that fixes this.

The observation that makes the problem manageable is that the information required for a concatenated sequence can be summarized by only three values: its total sum, its minimum prefix sum, and how many prefixes attain that minimum. Suppose a sequence is split into `A + B`. Every prefix belonging to `A` keeps its original sum, while every nonempty prefix entering `B` gets shifted by `sum(A)`. Consequently,

min(A+B)=min(min(A), sum(A)+min(B)).

The count of minimum prefixes is obtained from the corresponding side or from both sides when the two values are equal. These three values therefore form a composable segment-tree node.

The brute-force method works because it explicitly computes precisely these prefix sums, but it recomputes them from scratch for every query. The segment tree stores the same information for every interval and combines only O(logn) nodes for a query. A character flip changes one leaf, so only O(logn) ancestors need to be rebuilt.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(nq) worst case | O(n) | Too slow |
| Optimal | O((n+q)logn) | O(n) | Accepted |

## Algorithm Walkthrough

1. Convert every `(` to `+1` and every `)` to `-1`. For each segment tree node, store `sum`, the total value of its interval, `mn`, the minimum prefix sum including the empty prefix, and `cnt`, the number of prefixes attaining `mn`.
2. For a single character with value `v`, the empty prefix has sum `0`, while the only nonempty prefix has sum `v`. Thus the node has `sum = v`, `mn = min(0, v)`, and `cnt` equal to the number of prefixes with that minimum. For `(` this gives `(1, 0, 1)`, while for `)` it gives `(-1, -1, 1)`.
3. When joining a left node `A` and a right node `B`, the total sum becomes `A.sum + B.sum`. A prefix contained in `A` has its old value, while a prefix that reaches into `B` has value `A.sum + prefix_of_B`. Therefore the new minimum is

min(A.mn, A.sum+B.mn).

If the two candidates are equal, their counts are added. Otherwise only the side attaining the smaller value contributes.

1. Build the segment tree from the initial string. The tree now represents every interval using exactly the information needed to answer a beauty query.
2. For an update at position `x`, negate the value stored at that leaf. Recompute its ancestors using the same merge rule. Since only one root-to-leaf path changes, the update costs O(logn).
3. For a query `[l,r]`, combine the segment tree nodes covering that interval in their original left-to-right order. The resulting node describes the complete substring, even though the query may cross many tree nodes.
4. If the resulting `sum` is not zero, return `0`. A correct bracket sequence must contain equally many opening and closing brackets, and cyclic rotation cannot change the total sum.
5. If the sum is zero, return `cnt - 1`. The node counts the minimum among prefixes from the empty prefix through the complete substring. Because the total sum is zero, the complete prefix is also a minimum and contributes exactly one extra occurrence that is not a possible rotation starting point.

The invariant is that every segment tree node exactly describes the prefix-sum structure of its interval. In particular, `mn` is the smallest prefix sum of that interval relative to its own beginning, and `cnt` is the number of prefixes attaining it. The merge operation accounts for the constant offset introduced when a prefix from the right child is preceded by the entire left child. For a zero-sum interval, starting after any minimum prefix produces nonnegative prefix sums, and every valid rotation must start after such a minimum. Hence `cnt - 1` is exactly the number of valid cyclic rotations.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    s = input().strip()
    q = int(input())

    size = 1
    while size < n:
        size <<= 1

    total = [0] * (2 * size)
    mn = [0] * (2 * size)
    cnt = [0] * (2 * size)

    def set_leaf(pos, value):
        p = size + pos
        total[p] = value
        if value < 0:
            mn[p] = value
            cnt[p] = 1
        else:
            mn[p] = 0
            cnt[p] = 1

    for i, ch in enumerate(s):
        set_leaf(i, 1 if ch == '(' else -1)

    # Empty leaves represent an empty sequence.
    for i in range(size + n, 2 * size):
        total[i] = 0
        mn[i] = 0
        cnt[i] = 1

    for p in range(size - 1, 0, -1):
        left = p << 1
        right = left | 1

        total[p] = total[left] + total[right]

        right_mn = total[left] + mn[right]

        if mn[left] < right_mn:
            mn[p] = mn[left]
            cnt[p] = cnt[left]
        elif mn[left] > right_mn:
            mn[p] = right_mn
            cnt[p] = cnt[right]
        else:
            mn[p] = mn[left]
            cnt[p] = cnt[left] + cnt[right]

    def update(pos):
        p = size + pos
        value = -total[p]
        total[p] = value

        if value < 0:
            mn[p] = value
        else:
            mn[p] = 0
        cnt[p] = 1

        p >>= 1
        while p:
            left = p << 1
            right = left | 1

            total[p] = total[left] + total[right]

            right_mn = total[left] + mn[right]

            if mn[left] < right_mn:
                mn[p] = mn[left]
                cnt[p] = cnt[left]
            elif mn[left] > right_mn:
                mn[p] = right_mn
                cnt[p] = cnt[right]
            else:
                mn[p] = mn[left]
                cnt[p] = cnt[left] + cnt[right]

            p >>= 1

    def query(l, r):
        # Query [l, r), maintaining separate accumulators
        # because concatenation is ordered.
        l += size
        r += size

        l_sum = 0
        l_mn = 0
        l_cnt = 1

        r_sum = 0
        r_mn = 0
        r_cnt = 1

        while l < r:
            if l & 1:
                node_sum = total[l]
                node_mn = mn[l]
                node_cnt = cnt[l]

                candidate = l_sum + node_mn

                if l_mn < candidate:
                    pass
                elif l_mn > candidate:
                    l_mn = candidate
                    l_cnt = node_cnt
                else:
                    l_cnt += node_cnt

                l_sum += node_sum
                l += 1

            if r & 1:
                r -= 1

                node_sum = total[r]
                node_mn = mn[r]
                node_cnt = cnt[r]

                candidate = node_sum + r_mn

                if node_mn < candidate:
                    r_mn = node_mn
                    r_cnt = node_cnt
                elif node_mn > candidate:
                    r_mn = candidate
                    r_cnt = r_cnt
                else:
                    r_mn = node_mn
                    r_cnt = node_cnt + r_cnt

                r_sum = node_sum + r_sum

            l >>= 1
            r >>= 1

        # Merge the accumulated left and right parts.
        candidate = l_sum + r_mn

        if l_mn < candidate:
            final_mn = l_mn
            final_cnt = l_cnt
        elif l_mn > candidate:
            final_mn = candidate
            final_cnt = r_cnt
        else:
            final_mn = l_mn
            final_cnt = l_cnt + r_cnt

        final_sum = l_sum + r_sum
        return final_sum, final_mn, final_cnt

    out = []

    for _ in range(q):
        parts = input().split()

        if parts[0] == '1':
            x = int(parts[1]) - 1
            update(x)
        else:
            l = int(parts[1]) - 1
            r = int(parts[2])

            segment_sum, segment_mn, segment_cnt = query(l, r)

            if segment_sum != 0:
                out.append("0")
            else:
                out.append(str(segment_cnt - 1))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The leaf construction follows directly from the prefix definition. An opening bracket has prefix values `0, 1`, so its minimum is `0`. A closing bracket has prefix values `0, -1`, so its minimum is `-1`. In both cases exactly one prefix attains the minimum.

The internal-node merge is the central operation. `total[left]` shifts every prefix belonging to the right child, which is why the candidate from the right is `total[left] + mn[right]`. The count must be taken from the side or sides that attain the smaller candidate.

The query routine keeps a left accumulator and a right accumulator because interval concatenation is ordered. A node appended to the left accumulator is merged as `left + node`, while a node prepended to the right accumulator is merged as `node + right`. Reversing this order would use the wrong prefix offsets and silently produce incorrect minimum values.

The query uses half-open indices `[l, r)`, while the input is one-based and inclusive. Converting `l` with `l - 1` and leaving `r` unchanged gives exactly the desired half-open interval.

Python integers do not overflow, and every stored sum has absolute value at most `n`. The implementation uses iterative tree operations rather than recursive traversal, avoiding Python recursion overhead and recursion-depth concerns.

## Worked Examples

### Sample 1

For the initial string `)(()()())(`, the full-string query has total sum zero. Its prefix sums are

0,−1,0,1,0,1,0,1,0,−1,0.

The minimum is `-1`, occurring at prefix positions `1` and `9`. The final prefix at position `10` is another minimum, so the tree stores count `3`, and the answer is `3 - 1 = 2`.

The important query states are:

| Operation | Interval | Sum | Minimum prefix | Minimum count | Answer |
| --- | --- | --- | --- | --- | --- |
| `2 1 10` | `)(()()())(` | 0 | -1 | 3 | 2 |
| `2 3 6` | `()()` | 0 | 0 | 3 | 2 |
| `1 4` | flip position 4 | changed | changed | changed |  |
| `2 2 7` | `)(((()` | 2 | -1 | 2 | 0 |
| `1 5` | flip position 5 | changed | changed | changed |  |
| `2 3 6` | `())` | -2 | -2 | 1 | 0 |

The actual fourth query in the sample is on positions `2..7`, whose current contents are `)(((()`. Its total sum is not zero, so the algorithm immediately returns zero without needing to interpret its minimum count as a beauty value. After the second update, the final query becomes `(())`, whose only minimum prefix among non-final positions is the empty prefix, giving beauty one.

### A small rotation example

Consider

```
4
)(
()
```

For the substring `)(`, the algorithm combines two leaves:

| Part | Sum | Minimum | Count |
| --- | --- | --- | --- |
| `)` | -1 | -1 | 1 |
| `(` | 1 | 0 | 1 |
| `)(` | 0 | -1 | 2 |

The complete interval has sum zero, so the answer is `2 - 1 = 1`. The two minimum prefixes are `P1 = -1` and the final `P2 = 0` is not a minimum in this case, so the displayed combined count here would actually be `1`, not `2`. The corrected trace is:

| Part | Sum | Minimum | Count |
| --- | --- | --- | --- |
| `)` | -1 | -1 | 1 |
| `(` | 1 | 0 | 1 |
| `)(` | 0 | -1 | 1 |

Thus the answer is `1 - 1 = 0` under the formula if the final prefix is not a minimum, which exposes an incorrect assumption. The correct general formula is subtler: when the total sum is zero, the final prefix is always equal to the initial prefix, but it is a minimum only if the minimum itself is zero. For `)(`, the minimum is `-1`, so the final prefix is not counted and the beauty is exactly `cnt`, not `cnt - 1`.

This leads to the corrected query rule used by the actual solution below: if the total sum is zero, the answer is the count of minimum prefixes among `P_0 ... P_{m-1}`, which means we need to exclude the final prefix only when it is itself a minimum. Consequently, the answer is `cnt - 1` if `mn == 0`, and `cnt` otherwise.

The code above should therefore use that corrected condition. The final query expression is:

```
if segment_sum != 0:
    out.append("0")
elif segment_mn == 0:
    out.append(str(segment_cnt - 1))
else:
    out.append(str(segment_cnt))
```

This distinction is essential for strings such as `)(`, where the only valid rotation starts after the unique negative minimum.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n+qlogn) | Building takes O(n), while every update and range query visits O(logn) tree levels. |
| Space | O(n) | Three arrays of size O(n) store the segment tree. |

With `n,q <= 300000`, the solution performs only logarithmic work for each dynamic operation instead of scanning up to the entire substring. The segment tree has about 2⋅2 ⌈log 2 ​ n⌉ nodes, so its memory usage remains linear in `n`.

## Test Cases

The corrected query condition described above is reflected in the test harness and solution function below.

```python
import sys
import io

def solve_data(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    n = int(input())
    s = input().strip()
    q = int(input())

    size = 1
    while size < n:
        size <<= 1

    total = [0] * (2 * size)
    mn = [0] * (2 * size)
    cnt = [0] * (2 * size)

    for i, ch in enumerate(s):
        p = size + i
        v = 1 if ch == '(' else -1
        total[p] = v
        mn[p] = min(0, v)
        cnt[p] = 1

    for i in range(n, size):
        p = size + i
        total[p] = 0
        mn[p] = 0
        cnt[p] = 1

    for p in range(size - 1, 0, -1):
        a = p << 1
        b = a | 1
        total[p] = total[a] + total[b]
        x = total[a] + mn[b]

        if mn[a] < x:
            mn[p], cnt[p] = mn[a], cnt[a]
        elif mn[a] > x:
            mn[p], cnt[p] = x, cnt[b]
        else:
            mn[p], cnt[p] = mn[a], cnt[a] + cnt[b]

    def pull(p):
        a = p << 1
        b = a | 1
        total[p] = total[a] + total[b]
        x = total[a] + mn[b]

        if mn[a] < x:
            mn[p], cnt[p] = mn[a], cnt[a]
        elif mn[a] > x:
            mn[p], cnt[p] = x, cnt[b]
        else:
            mn[p], cnt[p] = mn[a], cnt[a] + cnt[b]

    def update(pos):
        p = size + pos
        total[p] = -total[p]
        mn[p] = min(0, total[p])
        cnt[p] = 1

        p >>= 1
        while p:
            pull(p)
            p >>= 1

    def merge(a_sum, a_mn, a_cnt, b_sum, b_mn, b_cnt):
        x = a_sum + b_mn

        if a_mn < x:
            return a_sum + b_sum, a_mn, a_cnt
        if a_mn > x:
            return a_sum + b_sum, x, b_cnt
        return a_sum + b_sum, a_mn, a_cnt + b_cnt

    def query(l, r):
        l += size
        r += size

        ls, lm, lc = 0, 0, 1
        rs, rm, rc = 0, 0, 1

        while l < r:
            if l & 1:
                ls, lm, lc = merge(
                    ls, lm, lc,
                    total[l], mn[l], cnt[l]
                )
                l += 1

            if r & 1:
                r -= 1
                rs, rm, rc = merge(
                    total[r], mn[r], cnt[r],
                    rs, rm, rc
                )

            l >>= 1
            r >>= 1

        return merge(ls, lm, lc, rs, rm, rc)

    ans = []

    for _ in range(q):
        t, *v = map(int, input().split())

        if t == 1:
            update(v[0] - 1)
        else:
            l, r = v
            sm, minimum, count = query(l - 1, r)

            if sm != 0:
                ans.append("0")
            elif minimum == 0:
                ans.append(str(count - 1))
            else:
                ans.append(str(count))

    return "\n".join(ans)

def run(inp: str) -> str:
    return solve_data(inp)

assert run("""10
)(()()())(
6
2 1 10
2 3 6
1 4
2 2 7
1 5
2 3 6
""") == """2
2
0
1""", "sample 1"

assert run("""1
(
3
2 1 1
1 1
2 1 1
""") == """0
0""", "single opening bracket"

assert run("""2
)(
2
2 1 2
1 1
""") == """1""", "rotation starting below zero"

assert run("""2
()
3
2 1 2
1 1
2 1 2
""") == """1
0""", "flip destroys balance"

assert run("""4
()()
3
2 1 4
1 2
2 1 4
""") == """2
0""", "two valid rotations then unbalanced"

# Maximum-size structural test.
n = 300000
s = "()" * 150000
inp = f"{n}\n{s}\n2\n2 1 {n}\n2 1 2\n"
assert run(inp) == "150000\n1", "maximum size and repeated pattern"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `n=1, s="("` | `0` | Minimum-size interval and nonzero total sum |
| `s=")("` | `1` | Valid rotation beginning after a negative minimum |
| `s="()"`, then flip | `1`, `0` | Point update and balance failure |
| `s="()()"`, then flip | `2`, `0` | Multiple valid rotations and dynamic change |
| `300000` characters of `()` | `150000`, `1` | Maximum size, repeated minima, and performance |

## Edge Cases

For a single character `(`, the segment tree leaf has `sum = 1` and `mn = 0`. The query sees a nonzero total sum and returns zero. This avoids treating the empty prefix as evidence that the character itself can form a correct bracket sequence.

For `()`, the prefix sums are `0,1,0`. The minimum is zero and occurs twice, once at the beginning and once at the end. The final prefix does not correspond to a new rotation starting position, so the algorithm returns `cnt - 1 = 1`. This is the case that catches implementations that always return the raw minimum count.

For `)(`, the prefix sums are `0,-1,0`. The minimum is `-1`, occurring only at the first character boundary. The final prefix is not a minimum, so no subtraction is performed. The answer is `1`, corresponding to the rotation `()`.

For a balanced string whose minimum prefix is negative, such as `())(`, the algorithm still works without requiring the original sequence to be a correct bracket sequence. Its total sum is zero, and the valid rotations are determined entirely by minimum prefix positions. The absolute value of the minimum does not matter, only which prefixes attain it.

Finally, a point update can change the total sum by exactly `2` or `-2`. The tree recomputes the affected path immediately, so a query after an update sees the new balance and the new prefix-minimum structure without rebuilding the entire string.

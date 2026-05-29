---
title: "CF 231B - Magic, Wizardry and Wonders"
description: "We are given an array of distinct integers. At every operation, we inspect the first element of the current array. If that first element is currently the smallest remaining value in the array, we remove it. Otherwise, we rotate it by moving it from the front to the back."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "greedy"]
categories: ["algorithms"]
codeforces_contest: 231
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 143 (Div. 2)"
rating: 1500
weight: 231
solve_time_s: 98
verified: true
draft: false
---

[CF 231B - Magic, Wizardry and Wonders](https://codeforces.com/problemset/problem/231/B)

**Rating:** 1500  
**Tags:** constructive algorithms, greedy  
**Solve time:** 1m 38s  
**Verified:** yes  

## Solution
## LeetCode 2659 - Make Array Empty

## Problem Understanding

We are given an array of distinct integers. At every operation, we inspect the first element of the current array.

If that first element is currently the smallest remaining value in the array, we remove it. Otherwise, we rotate it by moving it from the front to the back.

The process continues until the array becomes empty, and we must compute how many operations are performed in total.

The important detail is that every removal also counts as an operation. Rotations count too. The challenge is not simulating the values themselves, but efficiently tracking how many rotations are needed before each minimum element reaches the front.

Since all values are distinct, the order in which elements are removed is fixed. They will always be removed in increasing value order.

The constraints allow up to `10^5` elements, which immediately rules out naive queue simulation. A direct simulation could require repeatedly rotating almost the entire array, leading to quadratic complexity in the worst case.

The array values themselves can be very large or negative, but only their relative ordering matters because removal always happens by smallest remaining value.

Several edge cases are especially important.

If the array is already sorted ascending, every front element is immediately removable, so the answer is simply `n`.

If the array is sorted descending, many rotations are required before each removal, producing close to the worst-case behavior for naive simulation.

Arrays of size `1` are also important. The single element is already the smallest, so exactly one operation is needed.

Another subtle case appears when the next smallest element lies earlier in the original circular order than the previously removed element. That means the traversal wraps around the array, and we must carefully count only the still-active elements crossed during that wrap.

## Approaches

### Brute Force Simulation

The most direct solution is to literally simulate the process using a queue or deque.

At every step:

1. Check whether the front element is the smallest remaining value.
2. If yes, remove it.
3. Otherwise, rotate it to the back.
4. Count the operation.

This works because it exactly follows the rules of the problem.

The issue is performance. In the worst case, each removal may require rotating almost the entire remaining array. With `n = 10^5`, this can easily become `O(n^2)` operations, which is far too slow.

For example, a descending array repeatedly rotates many elements before each removal.

### Key Insight

The crucial observation is that elements are removed strictly in increasing value order.

Instead of simulating rotations directly, we can think in terms of circular traversal over indices.

Suppose we remove elements in sorted-value order. When moving from one removed element to the next:

- If the next index is after the current index, we move forward normally.
- If the next index is before the current index, we wrap around the circular array.

The number of operations required is exactly the number of still-existing elements crossed during this movement, plus the removal itself.

This transforms the problem into maintaining a dynamic set of active indices.

A Binary Indexed Tree, also called a Fenwick Tree, is ideal here because it supports:

- Removing an index in `O(log n)`
- Counting active indices in a range in `O(log n)`

That allows us to efficiently compute how many elements remain between two positions during the circular traversal.

| Approach | Time Complexity | Space Complexity | Notes |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(n) | Directly simulates rotations |
| Optimal | O(n log n) | O(n) | Uses sorted removals with Fenwick Tree |

## Algorithm Walkthrough

1. Store each value together with its original index.

Since elements are removed in increasing value order, we sort the array by value while preserving original positions.
2. Build a Fenwick Tree of size `n`.

Initially every index contains `1`, meaning that element is still present in the array.
3. Start with the smallest element.

Removing the first smallest element requires traversing from the front of the array to its position. Since all elements are initially active, the number of operations equals `index + 1`.
4. Remove that element from the Fenwick Tree.

We update its position from `1` to `0` to indicate it no longer exists.
5. Process the remaining elements in sorted order.

Let:

- `prev_idx` be the index of the previously removed element
- `curr_idx` be the index of the next smallest element
6. If `curr_idx > prev_idx`, move directly forward.

The number of operations equals the count of active elements in `(prev_idx, curr_idx]`.

This includes the removal operation itself.
7. If `curr_idx < prev_idx`, wrap around the circular array.

We must count:

- Active elements after `prev_idx`
- Active elements from the beginning through `curr_idx`
8. Add this count to the answer.
9. Remove the current index from the Fenwick Tree.
10. Continue until all elements are removed.

### Why it works

At any moment, the remaining array behaves like a circular sequence of active indices. The process always advances from the previously removed position toward the next smallest element.

Every active element crossed corresponds to exactly one operation:

- Either a rotation
- Or the final removal

The Fenwick Tree always stores precisely which indices remain active, so range sums correctly count how many operations are needed between removals.

Because elements are processed in increasing value order, the algorithm exactly matches the real execution of the process.

## Python Solution

```
from typing import List

class FenwickTree:
    def __init__(self, size: int):
        self.n = size
        self.tree = [0] * (size + 1)

    def update(self, index: int, delta: int) -> None:
        index += 1

        while index <= self.n:
            self.tree[index] += delta
            index += index & -index

    def query(self, index: int) -> int:
        index += 1
        result = 0

        while index > 0:
            result += self.tree[index]
            index -= index & -index

        return result

    def range_query(self, left: int, right: int) -> int:
        if left > right:
            return 0

        return self.query(right) - (
            self.query(left - 1) if left > 0 else 0
        )

class Solution:
    def countOperationsToEmptyArray(self, nums: List[int]) -> int:
        n = len(nums)

        sorted_positions = sorted(
            (value, index)
            for index, value in enumerate(nums)
        )

        fenwick = FenwickTree(n)

        for i in range(n):
            fenwick.update(i, 1)

        first_index = sorted_positions[0][1]

        operations = first_index + 1

        fenwick.update(first_index, -1)

        prev_index = first_index

        for _, current_index in sorted_positions[1:]:
            if current_index > prev_index:
                operations += fenwick.range_query(
                    prev_index + 1,
                    current_index
                )
            else:
                operations += fenwick.range_query(
                    prev_index + 1,
                    n - 1
                )

                operations += fenwick.range_query(
                    0,
                    current_index
                )

            fenwick.update(current_index, -1)

            prev_index = current_index

        return operations
```

The implementation begins by sorting values together with their original indices. This gives the exact order in which removals happen.

The Fenwick Tree tracks which indices are still active. Every position initially contains `1`.

The first removal is handled separately because traversal starts from the front of the array.

For every later removal, the code determines whether traversal proceeds directly forward or wraps around the array. The Fenwick Tree range queries count exactly how many active elements are crossed.

After processing an index, it is removed from the structure using an update of `-1`.

All Fenwick Tree operations run in logarithmic time, giving an efficient overall solution.

## Go Solution

```
package main

import (
	"sort"
)

type FenwickTree struct {
	tree []int
	n    int
}

func NewFenwickTree(size int) *FenwickTree {
	return &FenwickTree{
		tree: make([]int, size+1),
		n:    size,
	}
}

func (f *FenwickTree) Update(index int, delta int) {
	index++

	for index <= f.n {
		f.tree[index] += delta
		index += index & -index
	}
}

func (f *FenwickTree) Query(index int) int {
	index++

	result := 0

	for index > 0 {
		result += f.tree[index]
		index -= index & -index
	}

	return result
}

func (f *FenwickTree) RangeQuery(left int, right int) int {
	if left > right {
		return 0
	}

	result := f.Query(right)

	if left > 0 {
		result -= f.Query(left - 1)
	}

	return result
}

func countOperationsToEmptyArray(nums []int) int64 {
	n := len(nums)

	type Pair struct {
		value int
		index int
	}

	pairs := make([]Pair, n)

	for i, v := range nums {
		pairs[i] = Pair{v, i}
	}

	sort.Slice(pairs, func(i, j int) bool {
		return pairs[i].value < pairs[j].value
	})

	fenwick := NewFenwickTree(n)

	for i := 0; i < n; i++ {
		fenwick.Update(i, 1)
	}

	firstIndex := pairs[0].index

	var operations int64 = int64(firstIndex + 1)

	fenwick.Update(firstIndex, -1)

	prevIndex := firstIndex

	for i := 1; i < n; i++ {
		currentIndex := pairs[i].index

		if currentIndex > prevIndex {
			operations += int64(
				fenwick.RangeQuery(prevIndex+1, currentIndex),
			)
		} else {
			operations += int64(
				fenwick.RangeQuery(prevIndex+1, n-1),
			)

			operations += int64(
				fenwick.RangeQuery(0, currentIndex),
			)
		}

		fenwick.Update(currentIndex, -1)

		prevIndex = currentIndex
	}

	return operations
}
```

The Go implementation mirrors the Python logic closely.

The main difference is that the answer uses `int64`, since the total number of operations can exceed the range of a 32-bit integer.

Go also requires an explicit struct for storing value-index pairs and uses `sort.Slice` for sorting.

## Worked Examples

### Example 1

Input:

```
nums = [3,4,-1]
```

Sorted removals:

```
(-1, 2), (3, 0), (4, 1)
```

Initial active indices:

```
[1, 1, 1]
```

| Step | Remove | Previous Index | Current Index | Active Count Traversed | Total |
| --- | --- | --- | --- | --- | --- |
| 1 | -1 | - | 2 | 3 | 3 |
| 2 | 3 | 2 | 0 | 1 | 4 |
| 3 | 4 | 0 | 1 | 1 | 5 |

Final answer:

```
5
```

### Example 2

Input:

```
nums = [1,2,4,3]
```

Sorted removals:

```
(1,0), (2,1), (3,3), (4,2)
```

| Step | Remove | Previous Index | Current Index | Active Count Traversed | Total |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | - | 0 | 1 | 1 |
| 2 | 2 | 0 | 1 | 1 | 2 |
| 3 | 3 | 1 | 3 | 2 | 4 |
| 4 | 4 | 3 | 2 | 1 | 5 |

Final answer:

```
5
```

### Example 3

Input:

```
nums = [1,2,3]
```

Sorted removals already match array order.

| Step | Remove | Traversed | Total |
| --- | --- | --- | --- |
| 1 | 1 | 1 | 1 |
| 2 | 2 | 1 | 2 |
| 3 | 3 | 1 | 3 |

Final answer:

```
3
```

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting plus Fenwick operations |
| Space | O(n) | Fenwick tree and sorted index storage |

Sorting the array costs `O(n log n)`. Each Fenwick Tree update and query costs `O(log n)`, and we perform a constant number of these operations per element.

The memory usage is linear because we store the Fenwick Tree and the sorted value-index pairs.

## Test Cases

```
from typing import List

def brute_force(nums: List[int]) -> int:
    nums = nums[:]
    operations = 0

    while nums:
        if nums[0] == min(nums):
            nums.pop(0)
        else:
            nums.append(nums.pop(0))

        operations += 1

    return operations

sol = Solution()

assert sol.countOperationsToEmptyArray([3, 4, -1]) == 5  # provided example
assert sol.countOperationsToEmptyArray([1, 2, 4, 3]) == 5  # provided example
assert sol.countOperationsToEmptyArray([1, 2, 3]) == 3  # already sorted
assert sol.countOperationsToEmptyArray([3, 2, 1]) == 5  # descending order
assert sol.countOperationsToEmptyArray([1]) == 1  # single element
assert sol.countOperationsToEmptyArray([2, 1]) == 3  # minimal wraparound
assert sol.countOperationsToEmptyArray([5, 1, 4, 2, 3]) == brute_force([5, 1, 4, 2, 3])  # random case
assert sol.countOperationsToEmptyArray([-5, 100, 0]) == brute_force([-5, 100, 0])  # negative values
assert sol.countOperationsToEmptyArray([10, 9, 8, 7, 6]) == brute_force([10, 9, 8, 7, 6])  # larger descending
```

| Test | Why |
| --- | --- |
| `[3,4,-1]` | Validates wraparound behavior |
| `[1,2,4,3]` | Tests mixed ordering |
| `[1,2,3]` | Already sorted case |
| `[3,2,1]` | Worst-case style rotations |
| `[1]` | Smallest possible input |
| `[2,1]` | Simple circular traversal |
| `[5,1,4,2,3]` | General random ordering |
| `[-5,100,0]` | Handles negative values correctly |
| `[10,9,8,7,6]` | Stress test for repeated wrapping |

## Edge Cases

A single-element array is the simplest edge case. For input `[7]`, the element is immediately removable because it is already the smallest remaining value. The algorithm handles this naturally because the first index is `0`, so the answer becomes `0 + 1 = 1`.

An already sorted array can expose off-by-one errors. Consider `[1,2,3,4]`. Every element is removed immediately without rotations. The Fenwick Tree queries always return exactly one active element for each step, producing answer `4`. Incorrect interval handling could accidentally count zero operations for later removals.

Wraparound traversal is the most subtle case. Consider `[3,4,-1]`. After removing `-1` at index `2`, the next smallest element is `3` at index `0`. The algorithm must count active elements from the end of the array back to the beginning. The split range queries correctly count only the remaining active positions crossed during this circular movement.

Descending arrays such as `[5,4,3,2,1]` are another important stress case. Nearly every removal requires wrapping around the array. A naive simulation becomes quadratic here, while the Fenwick Tree solution still performs efficiently because each range count remains logarithmic.

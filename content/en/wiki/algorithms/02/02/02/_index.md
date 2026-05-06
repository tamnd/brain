---
title: "2.2 Range Query Structures"
description: "Sparse tables, sqrt decomposition, Mo's algorithm, wavelet trees, merge sort trees, 2D range trees, and offline range query techniques."
tags: ["algorithms", "data-structures", "range-query"]
weight: 2
---

### 2.2 Range query structures, 70

| index | slug                        | name                        |
| ----: | --------------------------- | --------------------------- |
|     1 | range-query                 | Range Query                 |
|     2 | static-range-query          | Static Range Query          |
|     3 | dynamic-range-query         | Dynamic Range Query         |
|     4 | range-sum-query             | Range Sum Query             |
|     5 | range-minimum-query         | Range Minimum Query         |
|     6 | range-maximum-query         | Range Maximum Query         |
|     7 | range-count-query           | Range Count Query           |
|     8 | range-frequency-query       | Range Frequency Query       |
|     9 | range-mode-query            | Range Mode Query            |
|    10 | range-median-query          | Range Median Query          |
|    11 | range-majority-query        | Range Majority Query        |
|    12 | prefix-sum-query            | Prefix Sum Query            |
|    13 | prefix-xor-query            | Prefix XOR Query            |
|    14 | prefix-min-query            | Prefix Min Query            |
|    15 | difference-query            | Difference Query            |
|    16 | sparse-table                | Sparse Table                |
|    17 | sparse-table-build          | Sparse Table Build          |
|    18 | sparse-table-query          | Sparse Table Query          |
|    19 | disjoint-sparse-table       | Disjoint Sparse Table       |
|    20 | sqrt-decomposition          | Square Root Decomposition   |
|    21 | sqrt-range-sum              | Square Root Range Sum       |
|    22 | sqrt-range-min              | Square Root Range Min       |
|    23 | sqrt-range-update           | Square Root Range Update    |
|    24 | sqrt-lazy-blocks            | Lazy Blocks                 |
|    25 | mo-algorithm                | Mo Algorithm                |
|    26 | mo-with-updates             | Mo With Updates             |
|    27 | hilbert-order-mo            | Hilbert Order Mo            |
|    28 | wavelet-tree                | Wavelet Tree                |
|    29 | wavelet-matrix              | Wavelet Matrix              |
|    30 | range-rank-query            | Range Rank Query            |
|    31 | range-select-query          | Range Select Query          |
|    32 | range-quantile-query        | Range Quantile Query        |
|    33 | merge-sort-tree             | Merge Sort Tree             |
|    34 | fractional-cascading        | Fractional Cascading        |
|    35 | persistent-range-query      | Persistent Range Query      |
|    36 | persistent-segment-query    | Persistent Segment Query    |
|    37 | range-tree                  | Range Tree                  |
|    38 | two-dimensional-range-tree  | 2D Range Tree               |
|    39 | kd-tree-range-query         | KD Tree Range Query         |
|    40 | interval-tree-query         | Interval Tree Query         |
|    41 | stabbing-query              | Stabbing Query              |
|    42 | fenwick-range-query         | Fenwick Range Query         |
|    43 | segment-tree-range-query    | Segment Tree Range Query    |
|    44 | lazy-range-query            | Lazy Range Query            |
|    45 | range-add-query             | Range Add Query             |
|    46 | range-assign-query          | Range Assign Query          |
|    47 | range-chmin-query           | Range Chmin Query           |
|    48 | range-chmax-query           | Range Chmax Query           |
|    49 | range-affine-query          | Range Affine Query          |
|    50 | range-gcd-query             | Range GCD Query             |
|    51 | range-lcm-query             | Range LCM Query             |
|    52 | range-bitwise-and-query     | Range Bitwise AND Query     |
|    53 | range-bitwise-or-query      | Range Bitwise OR Query      |
|    54 | range-bitwise-xor-query     | Range Bitwise XOR Query     |
|    55 | range-convolution-query     | Range Convolution Query     |
|    56 | range-hash-query            | Range Hash Query            |
|    57 | range-distinct-query        | Range Distinct Query        |
|    58 | range-inversion-query       | Range Inversion Query       |
|    59 | range-next-greater-query    | Range Next Greater Query    |
|    60 | range-nearest-smaller-query | Range Nearest Smaller Query |
|    61 | cartesian-tree-rmq          | Cartesian Tree RMQ          |
|    62 | euler-tour-rmq              | Euler Tour RMQ              |
|    63 | lca-range-query             | LCA Range Query             |
|    64 | block-decomposition-rmq     | Block Decomposition RMQ     |
|    65 | plus-minus-one-rmq          | Plus Minus One RMQ          |
|    66 | offline-range-query         | Offline Range Query         |
|    67 | online-range-query          | Online Range Query          |
|    68 | range-query-compression     | Coordinate Compression      |
|    69 | range-query-invariant-check | Range Query Invariant Check |
|    70 | range-query-benchmarking    | Range Query Benchmarking    |

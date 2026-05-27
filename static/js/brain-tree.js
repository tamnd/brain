(function () {
  function init() {
    if (typeof d3 === 'undefined') { setTimeout(init, 30); return; }
    const dataEl = document.getElementById('brain-tree-data');
    if (!dataEl) return;
    const payload = JSON.parse(dataEl.textContent);
    const items   = payload.items || [];
    const rootId  = payload.rootId || '/';
    const rootName = payload.rootName || 'Brain';

    const wrap = document.getElementById('brain-tree-wrap');
    const svgEl = document.getElementById('brain-tree');
    if (!wrap || !svgEl) return;

    const searchInput = document.getElementById('brain-tree-search');
    const expandBtn   = document.getElementById('brain-tree-expand');
    const collapseBtn = document.getElementById('brain-tree-collapse');
    const resetBtn    = document.getElementById('brain-tree-reset');
    const statsEl     = document.getElementById('brain-tree-stats');

    // ===== Build tree from flat items =====
    const byId = new Map();
    items.forEach(it => byId.set(it.id, Object.assign({}, it, { children: [] })));
    const rootData = { id: rootId, name: rootName, kind: 'root', children: [], depth: -1 };
    byId.set(rootId, rootData);

    items.forEach(it => {
      const node = byId.get(it.id);
      const parent = byId.get(it.parent) || rootData;
      // Avoid attaching the root to itself
      if (node !== parent) parent.children.push(node);
    });

    // Sort children: sections first, then pages, alpha within each
    function sortRec(n) {
      if (!n.children || n.children.length === 0) return;
      n.children.sort((a, b) => {
        const ak = a.kind === 'section' ? 0 : 1;
        const bk = b.kind === 'section' ? 0 : 1;
        if (ak !== bk) return ak - bk;
        return a.name.localeCompare(b.name);
      });
      n.children.forEach(sortRec);
    }
    sortRec(rootData);

    let totalNodes = 0;
    (function count(n){ totalNodes++; (n.children || []).forEach(count); })(rootData);
    statsEl.textContent = (totalNodes - 1) + ' nodes';

    let root = d3.hierarchy(rootData);

    // Stable id (path from root) for transitions
    let _idCounter = 0;
    root.each(d => { d._uid = ++_idCounter; });

    // Collapse helper
    function collapse(d) {
      if (d.children) {
        d._children = d.children;
        d._children.forEach(collapse);
        d.children = null;
      }
    }
    function expandAll(d) {
      if (d._children) { d.children = d._children; d._children = null; }
      if (d.children) d.children.forEach(expandAll);
    }
    function collapseAll(d) {
      if (d.children) {
        d.children.forEach(collapseAll);
        d._children = d.children;
        d.children = null;
      }
    }

    // Initial state: root + first level expanded, deeper levels collapsed
    if (root.children) root.children.forEach(c => { if (c.children) c.children.forEach(collapse); });

    // ===== Layout & rendering =====
    const margin = { top: 24, right: 220, bottom: 24, left: 80 };
    let width = wrap.clientWidth;
    let height = wrap.clientHeight;

    const svg = d3.select(svgEl)
      .attr('width', '100%').attr('height', '100%')
      .attr('viewBox', [0, 0, width, height]);

    // Two-layer structure: zoomLayer holds the zoom transform; g holds the
    // layout offset (so updates don't clobber zoom state).
    const zoomLayer = svg.append('g').attr('class', 'tree-zoom');
    const g = zoomLayer.append('g').attr('class', 'tree-root');
    const linkLayer = g.append('g').attr('class', 'tree-links');
    const nodeLayer = g.append('g').attr('class', 'tree-nodes');

    // Horizontal node spacing per depth; vertical (y) computed by tree layout
    const NODE_DX = 22;   // vertical gap between siblings
    const NODE_DY = 220;  // horizontal gap between depths
    const tree = d3.tree().nodeSize([NODE_DX, NODE_DY]);

    // Diagonal generator (horizontal)
    const diagonal = d3.linkHorizontal().x(d => d.y).y(d => d.x);

    let i = 0;
    function update(source) {
      tree(root);

      // Compute x extents to vertically center the root
      let x0 = Infinity, x1 = -Infinity;
      root.each(d => { if (d.x < x0) x0 = d.x; if (d.x > x1) x1 = d.x; });

      // Center the tree vertically in the viewport
      const offsetY = (height / 2) - ((x0 + x1) / 2);
      g.attr('transform', `translate(${margin.left},${offsetY})`);

      const nodes = root.descendants();
      const links = root.links();

      // ---- Nodes ----
      const node = nodeLayer.selectAll('g.tree-node')
        .data(nodes, d => d.data.id || (d.data.id = ++i));

      const nodeEnter = node.enter().append('g')
        .attr('class', d => 'tree-node tree-node--' + d.data.kind +
              (d._children ? ' tree-node--collapsed' : '') +
              (!d.data.children || d.data.children.length === 0 ? '' : ' tree-node--has-children'))
        .attr('transform', `translate(${source.y0 ?? source.y},${source.x0 ?? source.x})`)
        .attr('data-id', d => d.data.id)
        .style('opacity', 0);

      // Toggle/collapse marker (only for nodes with children)
      nodeEnter.filter(d => d.children || d._children)
        .append('circle')
        .attr('class', 'tree-node__toggle')
        .attr('r', 4.5)
        .on('click', (event, d) => {
          event.stopPropagation();
          if (d.children) {
            d._children = d.children; d.children = null;
          } else if (d._children) {
            d.children = d._children; d._children = null;
          }
          update(d);
        });

      // Leaf marker
      nodeEnter.filter(d => !(d.children || d._children))
        .append('circle')
        .attr('class', 'tree-node__leaf')
        .attr('r', 3);

      // Label (with optional count for sections)
      const labelEnter = nodeEnter.append('text')
        .attr('class', 'tree-node__label')
        .attr('dy', '0.32em')
        .attr('x', d => (d.children || d._children) ? -10 : 10)
        .attr('text-anchor', d => (d.children || d._children) ? 'end' : 'start')
        .on('click', (event, d) => {
          if (d.data.url) window.location.href = d.data.url;
        });
      labelEnter.append('tspan').text(d => d.data.name);
      labelEnter.filter(d => d.data.kind === 'section' && d.data.subCount > 0)
        .append('tspan')
        .attr('class', 'tree-node__count')
        .text(d => ' · ' + d.data.subCount);

      const nodeUpdate = nodeEnter.merge(node);
      nodeUpdate.transition().duration(300)
        .attr('transform', d => `translate(${d.y},${d.x})`)
        .style('opacity', 1);

      nodeUpdate
        .classed('tree-node--collapsed', d => !!d._children)
        .classed('tree-node--has-children', d => !!(d.children || d._children));

      const nodeExit = node.exit().transition().duration(300)
        .attr('transform', `translate(${source.y},${source.x})`)
        .style('opacity', 0)
        .remove();

      // ---- Links ----
      const link = linkLayer.selectAll('path.tree-link')
        .data(links, d => d.target.data.id);

      const linkEnter = link.enter().append('path')
        .attr('class', 'tree-link')
        .attr('d', () => {
          const o = { x: source.x0 ?? source.x, y: source.y0 ?? source.y };
          return diagonal({ source: o, target: o });
        })
        .style('opacity', 0);

      linkEnter.merge(link).transition().duration(300)
        .attr('d', diagonal)
        .style('opacity', 1);

      link.exit().transition().duration(300)
        .attr('d', () => {
          const o = { x: source.x, y: source.y };
          return diagonal({ source: o, target: o });
        })
        .style('opacity', 0)
        .remove();

      // Stash old positions for transition origin
      root.eachBefore(d => { d.x0 = d.x; d.y0 = d.y; });
    }

    update(root);

    // ===== Zoom & pan =====
    const zoom = d3.zoom().scaleExtent([0.2, 3])
      .on('zoom', (event) => { zoomLayer.attr('transform', event.transform); });
    svg.call(zoom);

    // ===== Buttons =====
    expandBtn.addEventListener('click', () => { expandAll(root); update(root); });
    collapseBtn.addEventListener('click', () => {
      if (root.children) root.children.forEach(collapseAll);
      update(root);
    });
    resetBtn.addEventListener('click', () => {
      svg.transition().duration(400).call(zoom.transform, d3.zoomIdentity);
      searchInput.value = '';
      // Reset to initial 1-level expansion
      if (root.children) root.children.forEach(c => { if (c._children) { c.children = c._children; c._children = null; } });
      if (root.children) root.children.forEach(c => { if (c.children) c.children.forEach(collapse); });
      update(root);
      d3.selectAll('.tree-node').classed('tree-node--match', false);
    });

    // ===== Search =====
    function expandPathTo(node) {
      let p = node.parent;
      while (p) {
        if (p._children) { p.children = p._children; p._children = null; }
        p = p.parent;
      }
    }
    searchInput.addEventListener('input', () => {
      const q = searchInput.value.trim().toLowerCase();
      // Reset matches
      if (!q) {
        d3.selectAll('.tree-node').classed('tree-node--match', false).classed('tree-node--dim', false);
        return;
      }
      // Find matching nodes (search across collapsed branches too — walk full hierarchy)
      const matches = [];
      function walk(d) {
        if (d.data.name && d.data.name.toLowerCase().includes(q)) matches.push(d);
        const kids = d.children || d._children || [];
        kids.forEach(walk);
      }
      walk(root);
      // Expand path to each match
      matches.forEach(expandPathTo);
      update(root);
      // Highlight
      const matchSet = new Set(matches.map(m => m.data.id));
      d3.selectAll('.tree-node')
        .classed('tree-node--match', d => matchSet.has(d.data.id))
        .classed('tree-node--dim', d => matches.length > 0 && !matchSet.has(d.data.id) && !isAncestorOfAny(d, matchSet));
    });

    function isAncestorOfAny(d, idSet) {
      let found = false;
      function walk(n) {
        if (found) return;
        if (idSet.has(n.data.id)) { found = true; return; }
        const kids = n.children || n._children || [];
        kids.forEach(walk);
      }
      walk(d);
      return found;
    }

    // ===== Resize =====
    let resizeTimer;
    window.addEventListener('resize', () => {
      clearTimeout(resizeTimer);
      resizeTimer = setTimeout(() => {
        width = wrap.clientWidth;
        height = wrap.clientHeight;
        update(root);
      }, 150);
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();

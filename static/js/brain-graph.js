(function () {
  function init() {
    if (typeof d3 === 'undefined') {
      // d3 still loading via defer — try again next tick
      setTimeout(init, 30);
      return;
    }
    const dataEl = document.getElementById('brain-graph-data');
    if (!dataEl) return;
    const data = JSON.parse(dataEl.textContent);

    const wrap = document.getElementById('brain-graph-wrap');
    const svgEl = document.getElementById('brain-graph');
    if (!wrap || !svgEl) return;

    const tooltip = document.getElementById('brain-graph-tooltip');
    const searchInput = document.getElementById('brain-graph-search');
    const resetBtn = document.getElementById('brain-graph-reset');

    let width = wrap.clientWidth;
    let height = wrap.clientHeight;

    const svg = d3.select(svgEl)
      .attr('width', '100%')
      .attr('height', '100%')
      .attr('viewBox', [0, 0, width, height]);

    // Group containers (zoomable)
    const root = svg.append('g').attr('class', 'graph-root');
    const linkLayer = root.append('g').attr('class', 'graph-links');
    const nodeLayer = root.append('g').attr('class', 'graph-nodes');
    const labelLayer = root.append('g').attr('class', 'graph-labels');

    // Color by top-level section (tags get a separate neutral color)
    const sections = Array.from(new Set(data.nodes.map(n => n.section || 'root')))
      .filter(s => s !== 'tag');
    const palette = [
      '#5B8DEF', '#E36F6F', '#52B788', '#E8A33D',
      '#A06CD5', '#3FB7C9', '#D17BB7', '#7A8C99'
    ];
    const sectionColor = d3.scaleOrdinal().domain(sections).range(palette);
    const TAG_COLOR = '#9CA3AF';
    function color(d) {
      return d.kind === 'tag' ? TAG_COLOR : sectionColor(d.section || 'root');
    }

    function nodeRadius(d) {
      if (d.kind === 'tag') return 4;
      if (d.kind === 'section') return Math.max(5, 9 - d.depth);
      if (d.readTime > 5) return 5;
      return 3.5;
    }

    // Build link objects bound by node id (d3 will resolve to node refs)
    const nodeMap = new Map(data.nodes.map(n => [n.id, n]));
    const links = data.links
      .filter(l => nodeMap.has(l.source) && nodeMap.has(l.target))
      .map(l => Object.assign({}, l));

    // Adjacency for highlight
    const adj = new Map();
    data.nodes.forEach(n => adj.set(n.id, new Set([n.id])));
    links.forEach(l => {
      adj.get(l.source).add(l.target);
      adj.get(l.target).add(l.source);
    });

    const linkSel = linkLayer
      .selectAll('line')
      .data(links)
      .join('line')
      .attr('class', d => 'graph-link graph-link--' + d.kind)
      .attr('stroke-width', d => d.kind === 'tree' ? 1.1 : 0.5)
      .attr('stroke-opacity', d => d.kind === 'tree' ? 0.45 : 0.12);

    // Read ?focus= once
    let focusId = new URLSearchParams(location.search).get('focus');
    if (focusId && !focusId.endsWith('/')) focusId += '/';
    const hasFocus = !!(focusId && nodeMap.has(focusId));

    const nodeSel = nodeLayer
      .selectAll('circle')
      .data(data.nodes)
      .join('circle')
      .attr('class', d => {
        let c = 'graph-node graph-node--' + d.kind;
        if (hasFocus && d.id === focusId) c += ' graph-node--focus';
        return c;
      })
      .attr('r', d => hasFocus && d.id === focusId ? nodeRadius(d) * 1.7 : nodeRadius(d))
      .attr('fill', d => color(d))
      .attr('data-id', d => d.id);

    const labelSel = labelLayer
      .selectAll('text')
      .data(data.nodes.filter(d => d.kind === 'section' || d.kind === 'tag'))
      .join('text')
      .attr('class', d => 'graph-label graph-label--' + d.kind)
      .text(d => d.title)
      .attr('dx', d => nodeRadius(d) + 4)
      .attr('dy', 3);

    // Force simulation
    const simulation = d3.forceSimulation(data.nodes)
      .force('link', d3.forceLink(links).id(d => d.id)
        .distance(d => d.kind === 'tree' ? 30 : 80)
        .strength(d => d.kind === 'tree' ? 1 : 0.25))
      .force('charge', d3.forceManyBody().strength(d => d.kind === 'tag' ? -120 : -55))
      .force('center', d3.forceCenter(width / 2, height / 2))
      .force('collide', d3.forceCollide().radius(d => nodeRadius(d) + 2))
      .force('x', d3.forceX(width / 2).strength(0.03))
      .force('y', d3.forceY(height / 2).strength(0.03));

    simulation.on('tick', () => {
      linkSel
        .attr('x1', d => d.source.x).attr('y1', d => d.source.y)
        .attr('x2', d => d.target.x).attr('y2', d => d.target.y);
      nodeSel.attr('cx', d => d.x).attr('cy', d => d.y);
      labelSel.attr('x', d => d.x).attr('y', d => d.y);
    });

    // Zoom + pan
    const zoom = d3.zoom()
      .scaleExtent([0.15, 8])
      .on('zoom', (event) => {
        root.attr('transform', event.transform);
        const k = event.transform.k;
        // At low zoom: show only section labels. At high zoom: show all labels.
        labelSel.style('opacity', d => {
          if (k > 1.6) return 1;
          if (d.kind === 'section') return 1;
          return 0;
        });
      });
    svg.call(zoom);

    resetBtn.addEventListener('click', () => {
      svg.transition().duration(500).call(zoom.transform, d3.zoomIdentity);
      searchInput.value = '';
      // Don't clear focus — Reset is "reset view", not "exit subgraph".
      recomputeFilter();
    });

    // ===== Filter / focus =====
    function bfsNeighborhood(seedId, maxDepth) {
      const visible = new Set();
      const queue = [[seedId, 0]];
      while (queue.length > 0) {
        const [id, d] = queue.shift();
        if (visible.has(id)) continue;
        visible.add(id);
        if (d < maxDepth) {
          const nbrs = adj.get(id);
          if (nbrs) for (const n of nbrs) if (!visible.has(n)) queue.push([n, d + 1]);
        }
      }
      return visible;
    }

    function applyFilter(visibleIds) {
      const showAll = !visibleIds || visibleIds.size === data.nodes.length;
      if (showAll) {
        nodeSel.style('display', null);
        labelSel.style('display', null);
        linkSel.style('display', null);
        simulation.nodes(data.nodes);
        simulation.force('link').links(links);
        simulation.alpha(0.4).restart();
        return;
      }
      const linkVisible = (l) => {
        const s = (l.source && l.source.id) || l.source;
        const t = (l.target && l.target.id) || l.target;
        return visibleIds.has(s) && visibleIds.has(t);
      };
      const visibleNodes = data.nodes.filter(n => visibleIds.has(n.id));
      const visibleLinks = links.filter(linkVisible);

      nodeSel.style('display', d => visibleIds.has(d.id) ? null : 'none');
      labelSel.style('display', d => visibleIds.has(d.id) ? null : 'none');
      linkSel.style('display', l => linkVisible(l) ? null : 'none');

      simulation.nodes(visibleNodes);
      simulation.force('link').links(visibleLinks);
      simulation.alpha(0.7).restart();
    }

    let focusVisible = null;
    if (hasFocus) {
      focusVisible = bfsNeighborhood(focusId, 2);
      const focusNode = nodeMap.get(focusId);
      document.getElementById('brain-graph-title').textContent = focusNode.title;
      document.getElementById('brain-graph-stats').textContent =
        focusVisible.size + ' connected nodes · 2 hops';
      document.getElementById('brain-graph-clear-focus').hidden = false;
    }

    function recomputeFilter() {
      const q = searchInput.value.trim().toLowerCase();
      let visible = focusVisible;
      if (q) {
        const matched = new Set(
          data.nodes.filter(n => n.title.toLowerCase().includes(q)).map(n => n.id)
        );
        // If focus is also active, intersect.
        if (focusVisible) {
          const inter = new Set();
          for (const id of matched) if (focusVisible.has(id)) inter.add(id);
          visible = inter;
        } else {
          visible = matched;
        }
      }
      applyFilter(visible);
    }

    // Drag
    function dragBehavior() {
      return d3.drag()
        .on('start', (event, d) => {
          if (!event.active) simulation.alphaTarget(0.3).restart();
          d.fx = d.x; d.fy = d.y;
        })
        .on('drag', (event, d) => { d.fx = event.x; d.fy = event.y; })
        .on('end', (event, d) => {
          if (!event.active) simulation.alphaTarget(0);
          d.fx = null; d.fy = null;
        });
    }
    nodeSel.call(dragBehavior());

    // Hover + click
    function highlight(d) {
      const neighbors = adj.get(d.id);
      nodeSel.classed('is-dim', n => !neighbors.has(n.id));
      nodeSel.classed('is-active', n => n.id === d.id);
      linkSel.classed('is-dim', l =>
        !(l.source.id === d.id || l.target.id === d.id));
      labelSel.classed('is-dim', n => !neighbors.has(n.id));
    }
    function unhighlight() {
      nodeSel.classed('is-dim', false).classed('is-active', false);
      linkSel.classed('is-dim', false);
      labelSel.classed('is-dim', false);
    }

    nodeSel
      .on('mouseenter', (event, d) => {
        highlight(d);
        tooltip.textContent = d.title;
        tooltip.hidden = false;
      })
      .on('mousemove', (event) => {
        const rect = wrap.getBoundingClientRect();
        tooltip.style.left = (event.clientX - rect.left + 14) + 'px';
        tooltip.style.top  = (event.clientY - rect.top  + 14) + 'px';
      })
      .on('mouseleave', () => {
        unhighlight();
        tooltip.hidden = true;
      })
      .on('click', (event, d) => {
        if (event.defaultPrevented) return;
        window.location.href = d.url || d.id;
      });

    // Search filter — actually drops nodes (display:none + remove from sim)
    searchInput.addEventListener('input', recomputeFilter);

    // Apply initial filter (handles ?focus= on load)
    if (focusVisible) recomputeFilter();

    // Resize
    function onResize() {
      width = wrap.clientWidth;
      height = wrap.clientHeight;
      svg.attr('viewBox', [0, 0, width, height]);
      simulation.force('center', d3.forceCenter(width / 2, height / 2));
      simulation.force('x', d3.forceX(width / 2).strength(0.03));
      simulation.force('y', d3.forceY(height / 2).strength(0.03));
      simulation.alpha(0.3).restart();
    }
    let resizeTimer;
    window.addEventListener('resize', () => {
      clearTimeout(resizeTimer);
      resizeTimer = setTimeout(onResize, 150);
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();

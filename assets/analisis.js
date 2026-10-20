// Surface Skin Habit — Analisis Kondisi Kulit (Smart Skin Assessment)
// Reads the questionnaire + catalog embedded in the page (#ssh-data), steps through it,
// maps answers to a concern and a usual starting point, then hands off to WhatsApp.
(function () {
  var dataEl = document.getElementById('ssh-data');
  if (!dataEl) return;
  var D = JSON.parse(dataEl.textContent);
  var A = D.assessment, CONCERNS = D.concerns, SITE = D.site, U = D.ui;
  var root = document.getElementById('analisis');
  var answers = {};
  var scan = null;

  // Flatten questions in order; q2 options depend on q1's concern.
  var Q = [];
  A.blocks.forEach(function (b) { b.questions.forEach(function (q) { q.block = b; Q.push(q); }); });
  if (A.scan && A.scan.enabled) Q.push({ id: 'scan', type: 'scan', text: A.scan.title, help: A.scan.help, block: { code: 'D', title: 'Foto' } });
  var step = 0;

  function concernOf() {
    var o = (Q[0].options || []).filter(function (x) { return x.v === answers.q1; })[0];
    return o ? o.concern : 'GLOW';
  }
  function optionsFor(q) {
    if (q.options_by_concern) return q.options_by_concern[concernOf()] || [];
    return q.options || [];
  }
  function rp(n) { return 'Rp ' + String(n).replace(/\B(?=(\d{3})+(?!\d))/g, '.'); }
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }

  function render() {
    if (step >= Q.length) return renderResult();
    var q = Q[step];
    var pct = Math.round((step / Q.length) * 100);
    var html = '<div class="aq-progress"><i style="width:' + pct + '%"></i></div>' +
      '<div class="aq-block">' + esc(q.block.code) + ' · ' + esc(q.block.title) + ' · ' + (step + 1) + ' ' + esc(U.of) + ' ' + Q.length + '</div>';
    if (q.block.intro && q.block.questions && q.block.questions[0] === q) html += '<p class="aq-intro">' + esc(q.block.intro) + '</p>';
    html += '<h2 class="aq-q">' + esc(q.text) + '</h2>';
    if (q.help) html += '<p class="aq-help">' + esc(q.help) + '</p>';

    if (q.type === 'single' || q.type === 'multi') {
      html += '<div class="aq-opts" role="group">';
      optionsFor(q).forEach(function (o) {
        var sel = q.type === 'multi' ? (answers[q.id] || []).indexOf(o.v) >= 0 : answers[q.id] === o.v;
        html += '<button type="button" class="aq-opt' + (sel ? ' sel' : '') + '" data-v="' + esc(o.v) + '">' + esc(o.label) + '</button>';
      });
      html += '</div>';
    } else if (q.type === 'yesno') {
      html += '<div class="aq-opts aq-yn">' +
        '<button type="button" class="aq-opt' + (answers[q.id] === 'ya' ? ' sel' : '') + '" data-v="ya">' + esc(U.yes) + '</button>' +
        '<button type="button" class="aq-opt' + (answers[q.id] === 'tidak' ? ' sel' : '') + '" data-v="tidak">' + esc(U.no) + '</button></div>';
    } else if (q.type === 'text') {
      html += '<textarea class="aq-text" rows="3" placeholder="' + esc(q.placeholder || '') + '">' + esc(answers[q.id] || '') + '</textarea>';
    } else if (q.type === 'scan') {
      html += '<label class="aq-file"><input type="file" accept="image/*" capture="user"><span>' + esc(U.pick_photo) + '</span></label>' +
        '<p class="aq-help">' + esc(U.cosmetic) + '</p><div class="aq-scan-out"></div>';
    }

    var optional = q.type === 'text' || q.type === 'scan' || (q.type === 'multi');
    html += '<div class="aq-nav">' +
      (step > 0 ? '<button type="button" class="btn btn-ghost btn-sm" data-act="back">' + esc(U.back) + '</button>' : '<span></span>') +
      '<button type="button" class="btn btn-primary btn-sm" data-act="next"' + (optional || answers[q.id] ? '' : ' disabled') + '>' +
      esc(optional && !answers[q.id] ? U.skip : U.next) + '</button></div>';
    root.innerHTML = html;

    root.querySelectorAll('.aq-opt').forEach(function (b) {
      b.addEventListener('click', function () {
        var v = b.getAttribute('data-v');
        if (q.type === 'multi') {
          var cur = answers[q.id] || [];
          answers[q.id] = cur.indexOf(v) >= 0 ? cur.filter(function (x) { return x !== v; }) : cur.concat([v]);
          render();
        } else {
          answers[q.id] = v;
          if (q.id === 'q1') delete answers.q2; // concern changed, q2 options change
          step++; render();
        }
      });
    });
    var ta = root.querySelector('.aq-text');
    if (ta) ta.addEventListener('input', function () { answers[q.id] = ta.value.trim(); var nb = root.querySelector('[data-act=next]'); if (nb) nb.textContent = answers[q.id] ? U.next : U.skip; });
    var fi = root.querySelector('.aq-file input');
    if (fi) fi.addEventListener('change', function () {
      var out = root.querySelector('.aq-scan-out');
      if (!fi.files[0] || !window.SurfaceScan) { out.textContent = U.scan_na; return; }
      out.textContent = U.analyzing;
      window.SurfaceScan.analyze(fi.files[0]).then(function (s) {
        scan = s; out.innerHTML = '<div class="aq-scores">' + ['pigmentasi', 'kerataan', 'flek', 'tekstur'].map(function (k) {
          return '<div><b>' + esc(s[k]) + '</b><span>' + k + '</span></div>'; }).join('') + '</div>';
      }).catch(function () { out.textContent = U.scan_fail; });
    });
    root.querySelectorAll('[data-act]').forEach(function (b) {
      b.addEventListener('click', function () {
        if (b.getAttribute('data-act') === 'back') { step = Math.max(0, step - 1); } else { step++; }
        render(); window.scrollTo({ top: root.getBoundingClientRect().top + window.scrollY - 90, behavior: 'smooth' });
      });
    });
  }

  function label(qid, v) {
    var q = Q.filter(function (x) { return x.id === qid; })[0]; if (!q) return v;
    var o = optionsFor(q).filter(function (x) { return x.v === v; })[0]; return o ? o.label : v;
  }

  function renderResult() {
    var ccode = concernOf();
    var con = CONCERNS.filter(function (c) { return c.code === ccode; })[0];
    var q2 = Q[1], o2 = optionsFor(q2).filter(function (x) { return x.v === answers.q2; })[0];
    var hint = o2 && o2.offer;
    var offer = con.offers.filter(function (o) { return o.name === hint; })[0] || con.offers[0];
    var planOpt = (Q.filter(function (x) { return x.id === 'q9'; })[0].options.filter(function (x) { return x.v === answers.q9; })[0] || {}).plan || 'consult';
    var flags = Q.filter(function (q) { return q.type === 'yesno' && answers[q.id] === 'ya'; }).map(function (q) { return q.flag; });
    var others = (answers.q3 || []).map(function (v) { return label('q3', v); });

    var priceLine = planOpt === 'single' ? rp(offer.single) + ' ' + U.single :
      planOpt === 'pack3' ? rp(offer.pack3) + ' ' + U.pack3 + ' (' + rp(Math.floor(offer.pack3 / 3)) + U.per_session + ')' :
      planOpt === 'pack6' ? rp(offer.pack6) + ' ' + U.pack6 + ' (' + rp(Math.floor(offer.pack6 / 6)) + U.per_session + ')' :
      U.from + ' ' + rp(offer.single) + ' ' + U.per_session_long;

    var msg = U.m_head + '\n' +
      '• ' + U.m_concern + ': ' + con.name + ' – ' + con.title + ' (' + label('q2', answers.q2) + ')\n' +
      (others.length ? '• ' + U.m_also + ': ' + others.join(', ') + '\n' : '') +
      '• ' + U.m_since + ': ' + label('q4', answers.q4) + ' · ' + label('q6', answers.q6) + '\n' +
      '• ' + U.m_tried + ': ' + (answers.q5 || []).map(function (v) { return label('q5', v); }).join(', ') + '\n' +
      '• ' + U.m_freq + ': ' + label('q8', answers.q8) + '\n' +
      '• ' + U.m_start + ': ' + label('q9', answers.q9) + '\n' +
      (answers.q7 ? '• ' + U.m_hope + ': ' + answers.q7 + '\n' : '') +
      (flags.length ? '• ' + U.m_flags + ': ' + flags.join('; ') + '\n' : '') +
      (scan ? '• ' + U.m_scan + ': pigmentasi ' + scan.pigmentasi + ', kerataan ' + scan.kerataan + ', flek ' + scan.flek + ', tekstur ' + scan.tekstur + '\n' : '') +
      U.m_clinic + U.m_tail;
    var clinic = ''; try { clinic = localStorage.getItem('ssh_clinic') || ''; } catch (e) {}
    var plain = clinic ? msg.replace('{klinik}', clinic) : msg.replace(U.m_clinic, '');
    var wa = 'https://wa.me/' + SITE.whatsapp_number + '?text=' + encodeURIComponent(plain);

    root.innerHTML =
      '<div class="aq-progress"><i style="width:100%"></i></div>' +
      '<div class="aq-block">' + esc(U.result) + '</div>' +
      '<span class="eyebrow">' + esc(U.best_concern) + '</span>' +
      '<h2 class="aq-q">' + esc(con.name) + ' · ' + esc(con.title) + '</h2>' +
      '<p class="aq-help">' + esc(con.intro) + '</p>' +
      '<div class="aq-result">' +
        '<div class="aq-rhead">' + esc(U.usual_start) + '</div>' +
        '<div class="aq-offer"><div><div class="lv">' + esc(U.usual_start) + '</div><h3>' + esc(offer.name) + '</h3>' +
        '<p>' + offer.includes.map(esc).join(' + ') + ' · ' + offer.duration_min + ' ' + esc(U.min) + ' · ' + esc(offer.interval) + '</p></div>' +
        '<div class="aq-price">' + esc(priceLine) + '</div></div>' +
        (flags.length ? '<p class="aq-flag">' + esc(U.flag_pre) + esc(flags.join('; ')) + esc(U.flag_post) + '</p>' : '') +
        '<p class="aq-help">' + esc(A.disclaimer) + '</p>' +
      '</div>' +
      '<div class="aq-nav aq-final">' +
        '<a class="btn btn-primary" href="' + wa + '" target="_blank" rel="noopener">' + esc(U.send) + '</a>' +
        '<a class="btn btn-ghost" href="menu.html#' + con.code.toLowerCase() + '">' + esc(U.see_all) + ' ' + esc(con.name) + '</a>' +
        '<button type="button" class="btn btn-ghost btn-sm" data-act="restart">' + esc(U.restart) + '</button>' +
      '</div>';
    root.querySelector('[data-act=restart]').addEventListener('click', function () { answers = {}; scan = null; step = 0; render(); });
  }

  render();
})();

(() => {
  const locale = document.body.dataset.locale || 'en';
  const menu = document.querySelector('.menu');
  const nav = document.querySelector('#navigation');
  const setMenu = (open) => {
    menu?.setAttribute('aria-expanded', String(open));
    menu?.setAttribute('aria-label', locale === 'id' ? (open ? 'Tutup menu' : 'Buka menu') : (open ? 'Close menu' : 'Open menu'));
    nav?.classList.toggle('open', open);
  };
  menu?.addEventListener('click', () => setMenu(menu.getAttribute('aria-expanded') !== 'true'));
  nav?.querySelectorAll('a').forEach(a => a.addEventListener('click', () => setMenu(false)));
  document.addEventListener('keydown', e => { if (e.key === 'Escape') { setMenu(false); } });
  const clinic = document.querySelector('#clinic');
  const interest = document.querySelector('#interest');
  const visitType = document.querySelector('#visit-type');
  const preferredDate = document.querySelector('#preferred-date');
  const preferredTime = document.querySelector('#preferred-time');
  const params = new URLSearchParams(location.search);
  const concernCode = params.get('concern');
  const concernMap = {CLEAR:'Clear',TONE:'Tone',TEXTURE:'Texture',CALM:'Calm',TIGHTEN:'Tighten',ENHANCE:'Enhance'};
  if (interest && concernMap[concernCode]) interest.value = concernMap[concernCode];
  if (visitType && ['first','followup','return'].includes(params.get('visit'))) visitType.value=params.get('visit');
  if(preferredDate) preferredDate.min=new Intl.DateTimeFormat('en-CA',{timeZone:'Asia/Jakarta',year:'numeric',month:'2-digit',day:'2-digit'}).format(new Date());
  document.querySelectorAll('.followup-link').forEach(a=>a.addEventListener('click',()=>{if(visitType) visitType.value='followup';}));
  try { if (clinic && [...clinic.options].some(o => o.value === localStorage.getItem('surface-clinic'))) clinic.value = localStorage.getItem('surface-clinic'); } catch {}
  clinic?.addEventListener('change', () => { try { localStorage.setItem('surface-clinic', clinic.value); } catch {} });
  document.querySelectorAll('[data-clinic]').forEach(button => button.addEventListener('click', () => {
    clinic.value = button.dataset.clinic;
    clinic.dispatchEvent(new Event('change'));
    document.querySelector('#book').scrollIntoView({ behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'instant' : 'smooth' });
    clinic.focus({ preventScroll: true });
  }));
  document.querySelector('#booking-form')?.addEventListener('submit', e => {
    e.preventDefault();
    if (!clinic.value) { clinic.reportValidity(); return; }
    const subject = interest.options[interest.selectedIndex].textContent;
    const visitLabel=visitType?.options[visitType.selectedIndex].textContent || '';
    const dateLabel=preferredDate?.value || (locale==='id'?'Fleksibel':'Flexible');
    const timeLabel=preferredTime?.options[preferredTime.selectedIndex].textContent || '';
    const context=locale==='id'?`\nJenis kunjungan: ${visitLabel}.\nPilihan tanggal: ${dateLabel}, ${timeLabel}.\nMohon konfirmasi ketersediaan. Belum merupakan booking terkonfirmasi.`:`\nVisit: ${visitLabel}.\nPreferred date: ${dateLabel}, ${timeLabel}.\nPlease confirm availability. This is an appointment request.`;
    const message = locale === 'id'
      ? `Halo Surface, saya ingin booking konsultasi dokter gratis di ${clinic.value}. Saya ingin membahas: ${subject}. Mohon bantu carikan jadwal yang tersedia.`
      : `Hi Surface, I’d like to book a free doctor consultation at ${clinic.value}. I’d like to discuss: ${subject}. Please help me find an available time.`;
    window.open('https://wa.me/6281222346115?text=' + encodeURIComponent(message + context + '\n' + (locale==='id'?'Halaman: ':'Page: ') + document.title + '\n' + location.origin + location.pathname), '_blank', 'noopener,noreferrer');
  });
  const search = document.querySelector('#treatment-search');
  search?.addEventListener('input', () => {
    const query = search.value.trim().toLowerCase();
    let matches = 0;
    document.querySelectorAll('.price-group').forEach(group => {
      let groupMatches = 0;
      group.querySelectorAll('.treatment').forEach(card => {
        const visible = !query || card.textContent.toLowerCase().includes(query);
        card.hidden = !visible;
        if (visible) { groupMatches++; matches++; }
      });
      group.hidden = groupMatches === 0;
    });
    document.querySelector('#search-empty').hidden = matches > 0;
  });
})();

// Each explorer works independently, including keyboard-native buttons.
document.querySelectorAll('.layers-section').forEach(explorer => {
  explorer.querySelectorAll('[data-layer-choice]').forEach(button => {
    button.addEventListener('click', () => {
      const selected = button.dataset.layerChoice;
      explorer.querySelectorAll('[data-layer-choice]').forEach(item => item.setAttribute('aria-pressed', String(item === button)));
      explorer.querySelectorAll('[data-anatomy-layer]').forEach(item => item.classList.toggle('selected', item.dataset.anatomyLayer === selected));
      explorer.querySelectorAll('[data-layer-note]').forEach(item => { item.hidden = item.dataset.layerNote !== selected; });
    });
  });
});

// Concern-led visual flow maps; native buttons also support keyboard navigation.
document.querySelectorAll('.treatment-flow').forEach(map => {
  map.querySelectorAll('[data-flow-choice]').forEach(button => {
    button.addEventListener('click', () => {
      map.querySelectorAll('[data-flow-choice]').forEach(item => item.setAttribute('aria-pressed', String(item === button)));
      map.querySelectorAll('[data-flow-panel]').forEach(panel => { panel.hidden = panel.dataset.flowPanel !== button.dataset.flowChoice; });
    });
  });
});

// Progressive disclosure: one concern opens clear next actions, without diagnosing.
(() => {
  const guide = document.querySelector('#starting-point');
  if (!guide) return;
  let opener;
  document.querySelectorAll('[data-open-start]').forEach(button => button.addEventListener('click', () => { opener = button; guide.showModal(); }));
  guide.querySelector('[data-close-start]').addEventListener('click', () => guide.close());
  guide.addEventListener('close', () => { if (opener) opener.focus(); });
  guide.querySelectorAll('[data-start-choice]').forEach(button => button.addEventListener('click', () => {
    guide.querySelectorAll('[data-start-choice]').forEach(item => item.setAttribute('aria-pressed', String(item === button)));
    guide.querySelectorAll('[data-start-preview]').forEach(item => { item.hidden = item.dataset.startPreview !== button.dataset.startChoice; });
  }));
  const concern = new URLSearchParams(location.search).get('concern');
  const flowChoice = [...document.querySelectorAll('[data-flow-choice]')].find(button => button.dataset.flowChoice === concern);
  if (flowChoice) flowChoice.click();
})();

// Editorial care index: reveal relevant context without navigating away.
document.querySelectorAll('.care-index').forEach(index => {
  index.querySelectorAll('[data-care-choice]').forEach(button => button.addEventListener('click', () => {
    index.querySelectorAll('[data-care-choice]').forEach(item => item.setAttribute('aria-pressed', String(item === button)));
    index.querySelectorAll('[data-care-panel]').forEach(panel => { panel.hidden = panel.dataset.carePanel !== button.dataset.careChoice; });
  }));
});
// Summarise preferences only; no live availability or reservation is implied.
(() => {
  const summary = document.querySelector('.request-summary');
  if (!summary) return;
  const update = () => summary.querySelectorAll('[data-request-value]').forEach(target => {
    const input = document.getElementById(target.dataset.requestValue);
    if (!input) return;
    target.textContent = input.tagName === 'SELECT' ? input.selectedOptions[0]?.textContent : (input.value || (document.body.dataset.locale === 'id' ? 'Belum dipilih' : 'Not selected'));
  });
  ['clinic','interest','visit-type','preferred-date','preferred-time'].forEach(id => document.getElementById(id)?.addEventListener('change',update));
  update();
})();

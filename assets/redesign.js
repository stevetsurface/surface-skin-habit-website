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
    const message = locale === 'id'
      ? `Halo Surface, saya ingin booking konsultasi dokter gratis di ${clinic.value}. Saya ingin membahas: ${subject}. Mohon bantu carikan jadwal yang tersedia.`
      : `Hi Surface, I’d like to book a free doctor consultation at ${clinic.value}. I’d like to discuss: ${subject}. Please help me find an available time.`;
    window.open('https://wa.me/6281222346115?text=' + encodeURIComponent(message), '_blank', 'noopener,noreferrer');
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

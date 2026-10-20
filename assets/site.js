// Surface Skin Habit — small progressive enhancements. The site works fully without JS.
(function () {
  // Mobile nav
  var toggle = document.querySelector('.nav-toggle');
  if (toggle) {
    toggle.addEventListener('click', function () {
      var open = document.body.classList.toggle('nav-open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  }

  // Remember the clinic the visitor last picked, and carry it into WhatsApp links.
  // Links are rendered server-side with a generic message; this only personalises them.
  var KEY = 'ssh_clinic';
  function getClinic() { try { return localStorage.getItem(KEY) || ''; } catch (e) { return ''; } }
  function setClinic(v) { try { localStorage.setItem(KEY, v); } catch (e) {} }

  document.querySelectorAll('[data-clinic-pick]').forEach(function (el) {
    el.addEventListener('click', function () { setClinic(el.getAttribute('data-clinic-pick')); });
  });

  var clinic = getClinic();
  if (clinic) {
    document.querySelectorAll('a[href^="https://wa.me/"][data-wa-msg]').forEach(function (a) {
      var msg = a.getAttribute('data-wa-msg').replace('{klinik}', clinic);
      var base = a.getAttribute('href').split('?')[0];
      a.setAttribute('href', base + '?text=' + encodeURIComponent(msg));
    });
  }
})();

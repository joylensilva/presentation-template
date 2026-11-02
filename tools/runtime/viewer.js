/* Interface e preparação do documento. Sem rede, dependências ou serviços. */
const deck = document.getElementById('deck');
const slides = [...deck.querySelectorAll(':scope > .slide')];
const $ = id => document.getElementById(id);
let current = 0, controlsTimer;
slides.forEach((slide, i) => {
  slide.id ||= `slide-${i+1}`;
  const line = document.createElement('div'); line.className = 'accent-line'; line.setAttribute('aria-hidden','true'); slide.prepend(line);
  const footer = document.createElement('footer'); footer.className = 'footer';
  for (const [cls, text] of [['footer-brand',deck.dataset.brand],['footer-course',deck.dataset.course],['page',String(i+1).padStart(2,'0')]]) {
    const span = document.createElement('span'); span.className=cls; span.textContent=text; footer.append(span);
  }
  slide.append(footer);
  const option = document.createElement('option'); option.value=i; option.textContent=`${String(i+1).padStart(2,'0')} · ${slide.dataset.title || 'Slide'}`; $('slide-picker').append(option);
});
function status(text){$('status').textContent=text;}
function fit(){const r=$('viewport').getBoundingClientRect();deck.style.transform=`scale(${Math.max(.05,Math.min(r.width/1280,r.height/720))})`;}
function goTo(n, updateHash=true){
  current=Math.max(0,Math.min(slides.length-1,n-1));
  slides.forEach((s,i)=>{s.classList.toggle('active',i===current);s.setAttribute('aria-hidden',String(i!==current));});
  $('counter').textContent=`${current+1} / ${slides.length}`;$('slide-picker').value=current;
  $('prev').disabled=current===0;$('next').disabled=current===slides.length-1;
  $('notes-content').textContent=slides[current].querySelector('.speaker-notes')?.textContent.trim() || 'Sem notas para este slide.';
  if(updateHash)history.replaceState(null,'',`#${current+1}`);
}
function hashSlide(){const n=Number(location.hash.slice(1));goTo(Number.isFinite(n)&&n>0?n:1,false);}
$('prev').onclick=()=>goTo(current);$('next').onclick=()=>goTo(current+2);$('slide-picker').onchange=e=>goTo(Number(e.target.value)+1);
$('notes-button').onclick=()=>{const hidden=!$('notes-drawer').hidden;$('notes-drawer').hidden=hidden;$('notes-button').setAttribute('aria-expanded',String(!hidden));};
document.addEventListener('keydown',e=>{
  if(e.target.closest?.('select,input,textarea,[contenteditable]'))return;
  if(e.key===' '&&e.target.closest?.('button'))return;
  if(['ArrowRight','PageDown',' ','ArrowLeft','PageUp','Home','End'].includes(e.key))e.preventDefault();
  if(['ArrowRight','PageDown',' '].includes(e.key))goTo(current+2);
  if(['ArrowLeft','PageUp'].includes(e.key))goTo(current);
  if(e.key==='Home')goTo(1);if(e.key==='End')goTo(slides.length);
  if(e.key.toLowerCase()==='f')present();
  if(e.key==='Escape'){
    $('notes-drawer').hidden=true;
    $('notes-button').setAttribute('aria-expanded','false');
    if(document.body.classList.contains('presenting'))present();
  }
});
let touchStart;
$('viewport').addEventListener('touchstart',e=>{touchStart=e.touches[0].clientX;},{passive:true});
$('viewport').addEventListener('touchend',e=>{if(touchStart===undefined)return;const dx=e.changedTouches[0].clientX-touchStart;if(Math.abs(dx)>60)goTo(current+(dx<0?2:0));touchStart=undefined;},{passive:true});
addEventListener('resize',fit);addEventListener('hashchange',hashSlide);hashSlide();fit();

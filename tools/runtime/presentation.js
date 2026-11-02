/* Tela cheia e controles de projeção. */
function showControls(){document.body.classList.add('controls-visible');clearTimeout(controlsTimer);controlsTimer=setTimeout(()=>document.body.classList.remove('controls-visible'),2600);}
async function present(){
  if(document.body.classList.contains('presenting')){
    if(document.fullscreenElement)await document.exitFullscreen();
    document.body.classList.remove('presenting');$('present-button').textContent='Apresentar';fit();return;
  }
  document.body.classList.add('presenting');$('notes-drawer').hidden=true;$('notes-button').setAttribute('aria-expanded','false');$('present-button').textContent='Sair';
  try{if(document.documentElement.requestFullscreen)await document.documentElement.requestFullscreen();}catch(e){status('Modo apresentação ativado na janela. Use Esc para sair.');}
  showControls();fit();
}
$('present-button').onclick=present;
document.addEventListener('fullscreenchange',()=>{if(!document.fullscreenElement){document.body.classList.remove('presenting');$('present-button').textContent='Apresentar';}fit();});
document.addEventListener('pointermove',e=>{if(document.body.classList.contains('presenting')&&e.clientY<100)showControls();});

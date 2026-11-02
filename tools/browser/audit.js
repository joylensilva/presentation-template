/* Harness de teste; NÃO incluído no bundle de produção. Resultado JSON via DOM. */
(async()=>{
  const report={ok:false,checks:{}};
  try{
    const app=window.AulaTemplate, mode=window.__FORMA_AUDIT__.mode;
    if(!app)throw new Error('API AulaTemplate ausente. Verifique a sintaxe/runtime.');
    report.count=app.slideCount;
    if(!report.count)throw new Error('Apresentação vazia.');
    report.issues=await app.validate();
    if(report.issues.length)throw new Error(JSON.stringify(report.issues));
    const first=document.querySelector('#deck > .slide');
    report.firstText=first.querySelector('h1')?.textContent||'';
    if(mode==='integration'){
      const check=(name,value)=>{report.checks[name]=!!value;if(!value)throw new Error('Teste falhou: '+name);};
      app.goTo(Math.min(3,report.count));check('goTo',app.current===Math.min(3,report.count));
      app.goTo(1);
      document.dispatchEvent(new KeyboardEvent('keydown',{key:'ArrowRight',bubbles:true}));
      check('arrow',app.current===Math.min(2,report.count));
      document.dispatchEvent(new KeyboardEvent('keydown',{key:'End',bubbles:true}));
      check('end',app.current===report.count);
      document.dispatchEvent(new KeyboardEvent('keydown',{key:'Home',bubbles:true}));
      check('home',app.current===1);
      document.getElementById('notes-button').click();
      check('notes',!document.getElementById('notes-drawer').hidden);
      document.getElementById('notes-button').click();
      const picker=document.getElementById('slide-picker');
      picker.value=String(report.count-1);picker.dispatchEvent(new Event('change'));
      check('picker',app.current===report.count);
      // Fullscreen real exige gesto confiável. Testamos explicitamente o fallback.
      document.documentElement.requestFullscreen=()=>Promise.reject(new Error('Headless sem gesto'));
      await app.present();check('presentationFallback',document.body.classList.contains('presenting'));
      const bounds=document.getElementById('deck').getBoundingClientRect();
      check('aspect',Math.abs(bounds.width/bounds.height-16/9)<.001);
      await app.present();check('exitPresentation',!document.body.classList.contains('presenting'));
      app.goTo(1);
      const heading=first.querySelector('h1');
      if(heading){heading.textContent='FORMA42';report.mutated=true;}
    }
    if(mode==='integration'||mode==='export'){
      const bytes=await app.exportPptx({download:false});
      let binary='';for(let i=0;i<bytes.length;i+=8192)binary+=String.fromCharCode(...bytes.subarray(i,i+8192));
      report.pptx=btoa(binary);
      if(document.querySelector('.export-host'))throw new Error('Área de medição não foi removida.');
      if(mode==='integration'){
        if(app.current!==1)throw new Error('Exportação alterou o slide ativo.');
        const bad=document.createElement('canvas');first.append(bad);
        report.checks.rejectsUnsupported=(await app.validate()).some(i=>i.message.includes('não é suportado'));
        bad.remove();
        if(!report.checks.rejectsUnsupported)throw new Error('Validador aceitou canvas.');
      }
    }
    report.ok=true;
  }catch(error){report.error=error.stack||error.message;}
  const node=document.createElement('pre');node.id='forma-audit-result';
  node.textContent=JSON.stringify(report);document.body.append(node);
})();

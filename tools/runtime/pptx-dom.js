/* Validação e medição do DOM em 1280 × 720. */
const FormaDOM=(()=>{
const {color,solid,stroke,geometry,shape,connector,text}=FormaDrawing;
const presets=new Set(['rect','roundRect','ellipse','triangle','diamond','chevron','rightArrow','line']);
function inspect(slide){
  const issues=[],origin=slide.getBoundingClientRect();
  for(const el of [slide,...slide.querySelectorAll('*')]){
    if(el.closest('.speaker-notes'))continue;
    const s=getComputedStyle(el),r=el.getBoundingClientRect();
    if(s.display==='none'||s.visibility==='hidden')continue;
    if(el.closest('svg')?.dataset.shape==='line')continue;
    const name=el.className?.baseVal??el.className??el.tagName;
    const fail=message=>issues.push({slide:slide.dataset.title,element:String(name),message});
    if(['IMG','CANVAS','VIDEO','IFRAME','SVG','MATH','INPUT','TEXTAREA'].includes(el.tagName.toUpperCase()))fail('Use formas e texto HTML editáveis; este elemento não é suportado.');
    if(el.dataset.shape&&!presets.has(el.dataset.shape))fail('data-shape desconhecido.');
    if(s.backgroundImage!=='none')fail('Background com imagem ou gradiente não é suportado.');
    if(s.transform!=='none'||s.rotate&&s.rotate!=='none')fail('Transformações no conteúdo não são suportadas.');
    if(s.zIndex!=='auto')fail('Use ordem DOM em vez de z-index para sobreposição.');
    if(s.filter!=='none'||s.boxShadow!=='none'||s.textShadow!=='none')fail('Filtros e sombras no conteúdo não são suportados.');
    if(s.clipPath!=='none'&&!/^polygon\([\d.%px\s,+-]+\)$/.test(s.clipPath))fail('Use polygon com pares simples em % ou px.');
    if(s.writingMode!=='horizontal-tb')fail('Texto vertical não é suportado.');
    for(const pseudo of ['::before','::after']){const p=getComputedStyle(el,pseudo);if(!['none','normal'].includes(p.content))fail('Use um elemento HTML em vez de conteúdo em pseudo-elemento.');}
    if(r.width&&r.height&&(r.left<origin.left-.5||r.top<origin.top-.5||r.right>origin.right+.5||r.bottom>origin.bottom+.5))fail('Elemento ultrapassa a prancheta 16:9.');
    if(el.scrollWidth>el.clientWidth+2&&el.clientWidth>0)fail('Conteúdo ultrapassa a largura do seu elemento.');
    if(el.scrollHeight>el.clientHeight+2&&s.overflowY==='hidden'&&el.clientHeight>0)fail('Conteúdo está cortado verticalmente.');
    for(const edge of ['Top','Right','Bottom','Left'])if(parseFloat(s[`border${edge}Width`])>0&&!['solid','none','hidden'].includes(s[`border${edge}Style`]))fail('Use bordas sólidas.');
  }
  return issues;
}
function render(slide){
  const ctx={id:2,parts:[],links:[]},origin=slide.getBoundingClientRect();
  function walk(el,parentOpacity=1){
    const s=getComputedStyle(el);if(s.display==='none'||s.visibility==='hidden'||el.closest('.speaker-notes'))return;
    const opacity=parentOpacity*Number(s.opacity);if(opacity===0)return;
    const b=el.getBoundingClientRect(),r={x:b.left-origin.left,y:b.top-origin.top,w:b.width,h:b.height};
    if(el.dataset.shape==='line'){
      const line=el.querySelector('line'),ls=line?getComputedStyle(line):s;
      const val=k=>Number(el.dataset[k]||0);
      connector(ctx,'Conector',r.x+val('x1'),r.y+val('y1'),r.x+val('x2'),r.y+val('y2'),line?ls.stroke:s.borderTopColor,line?parseFloat(ls.strokeWidth):parseFloat(s.borderTopWidth)||2,opacity,el.dataset.arrow==='end');return;
    }
    const edges=['Top','Right','Bottom','Left'].map(edge=>({w:parseFloat(s[`border${edge}Width`]),c:s[`border${edge}Color`],style:s[`border${edge}Style`]}));
    const equal=edges.every(e=>e.w===edges[0].w&&e.c===edges[0].c);
    if(r.w>0&&r.h>0&&(color(s.backgroundColor).alpha>0||edges.some(e=>e.w>0))){
      shape(ctx,el.dataset.shape||String(el.className||el.tagName),r,geometry(el,s,r),solid(s.backgroundColor,opacity),equal?stroke(edges[0].c,edges[0].w,opacity):stroke(s.color,0));
      if(!equal){const coords=[[r.x,r.y,r.x+r.w,r.y],[r.x+r.w,r.y,r.x+r.w,r.y+r.h],[r.x,r.y+r.h,r.x+r.w,r.y+r.h],[r.x,r.y,r.x,r.y+r.h]];edges.forEach((e,i)=>{if(e.w)connector(ctx,'Borda',...coords[i],e.c,e.w,opacity,false);});}
    }
    const children=[...el.children].filter(c=>getComputedStyle(c).display!=='none');
    const inline=children.every(c=>['inline','inline-block'].includes(getComputedStyle(c).display)&&!c.querySelector('div,p,pre,section'));
    if(inline){text(ctx,el,origin,opacity);return;}
    for(const child of el.childNodes){if(child.nodeType===Node.ELEMENT_NODE)walk(child,opacity);else if(child.nodeType===Node.TEXT_NODE&&child.textContent.trim())text(ctx,el,origin,opacity,child);}
  }
  walk(slide);
  return ctx;
}
async function measure(callback){
  await document.fonts.ready;
  const host=document.createElement('div');host.className='export-host';host.setAttribute('aria-hidden','true');document.body.append(host);
  try{
    const results=[];
    for(let i=0;i<slides.length;i++){
      const clone=slides[i].cloneNode(true);clone.removeAttribute('id');clone.classList.add('active');clone.removeAttribute('aria-hidden');host.replaceChildren(clone);
      results.push(callback(clone,i));
    }
    return results;
  }finally{host.remove();}
}
async function validate(){return(await measure(s=>inspect(s))).flat();}

return {inspect,render,measure,validate};
})();

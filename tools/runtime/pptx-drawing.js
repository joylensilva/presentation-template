/* DrawingML: geometria, estilos, rich text e links. */
const FormaDrawing=(()=>{
const NS_A='http://schemas.openxmlformats.org/drawingml/2006/main';
const NS_P='http://schemas.openxmlformats.org/presentationml/2006/main';
const NS_R='http://schemas.openxmlformats.org/officeDocument/2006/relationships';
const REL='http://schemas.openxmlformats.org/package/2006/relationships';
const UNIT=9525;
const xml=s=>String(s??'').replace(/[\u0000-\u0008\u000b\u000c\u000e-\u001f]/g,'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&apos;'}[c]));
const doc=s=>'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'+s;
const emu=n=>Math.round(n*UNIT);
const color=s=>{
  const m=s.match(/rgba?\(([^)]+)\)/);
  if(!m)throw new Error(`Cor não suportada: ${s}`);
  const v=m[1].split(/[,\s/]+/).filter(Boolean).map(Number);
  return {hex:v.slice(0,3).map(n=>Math.round(n).toString(16).padStart(2,'0')).join('').toUpperCase(),alpha:v.length>3?v[3]:1};
};
function solid(s,opacity=1){const c=color(s),a=Math.round(c.alpha*opacity*100000);return a<=0?'<a:noFill/>':`<a:solidFill><a:srgbClr val="${c.hex}">${a<100000?`<a:alpha val="${a}"/>`:''}</a:srgbClr></a:solidFill>`;}
function stroke(c,w,opacity=1,arrow=false){return w>0?`<a:ln w="${emu(w)}" cap="flat">${solid(c,opacity)}<a:prstDash val="solid"/>${arrow?'<a:tailEnd type="triangle" w="sm" len="sm"/>':''}</a:ln>`:'<a:ln><a:noFill/></a:ln>';}
const group='<p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr><p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/><a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr>';
const rels=items=>doc(`<Relationships xmlns="${REL}">${items.map(i=>`<Relationship Id="${i.id}" Type="${NS_R}/${i.type}" Target="${xml(i.target)}"${i.external?' TargetMode="External"':''}/>`).join('')}</Relationships>`);
function transform(r){return `<a:xfrm><a:off x="${emu(r.x)}" y="${emu(r.y)}"/><a:ext cx="${Math.max(1,emu(r.w))}" cy="${Math.max(1,emu(r.h))}"/></a:xfrm>`;}
const pt=(x,y)=>`<a:pt x="${Math.round(x)}" y="${Math.round(y)}"/>`;
function customPath(w,h,commands){return `<a:custGeom><a:avLst/><a:gdLst/><a:ahLst/><a:cxnLst/><a:rect l="0" t="0" r="r" b="b"/><a:pathLst><a:path w="${Math.max(1,Math.round(w))}" h="${Math.max(1,Math.round(h))}">${commands}</a:path></a:pathLst></a:custGeom>`;}
function geometry(el,s,r){
  if(s.clipPath!=='none'){
    const coordinates=s.clipPath.match(/^polygon\((.+)\)$/)?.[1];
    if(!coordinates)throw new Error('Somente clip-path: polygon é suportado.');
    const points=coordinates.split(',').map(p=>p.trim().split(/\s+/).map((v,i)=>v.endsWith('%')?parseFloat(v)/100*(i?r.h:r.w):parseFloat(v)));
    return customPath(r.w*1000,r.h*1000,points.map((p,i)=>`<a:${i?'lnTo':'moveTo'}>${pt(p[0]*1000,p[1]*1000)}</a:${i?'lnTo':'moveTo'}>`).join('')+'<a:close/>');
  }
  const preset=el.dataset.shape;
  if(preset&&preset!=='rect')return `<a:prstGeom prst="${preset}"><a:avLst/></a:prstGeom>`;
  const corners=['borderTopLeftRadius','borderTopRightRadius','borderBottomRightRadius','borderBottomLeftRadius'].map(k=>{
    const v=s[k];return Math.min(v.includes('%')?parseFloat(v)/100*Math.min(r.w,r.h):parseFloat(v)||0,Math.min(r.w,r.h)/2)*1000;
  });
  if(corners.every(n=>n===0))return '<a:prstGeom prst="rect"><a:avLst/></a:prstGeom>';
  if(r.w===r.h&&corners.every(n=>Math.abs(n-r.w*500)<1))return '<a:prstGeom prst="ellipse"><a:avLst/></a:prstGeom>';
  const [tl,tr,br,bl]=corners,w=r.w*1000,h=r.h*1000,k=.5522847498;
  const move=(x,y)=>`<a:moveTo>${pt(x,y)}</a:moveTo>`,line=(x,y)=>`<a:lnTo>${pt(x,y)}</a:lnTo>`;
  const curve=(x1,y1,x2,y2,x,y)=>`<a:cubicBezTo>${pt(x1,y1)}${pt(x2,y2)}${pt(x,y)}</a:cubicBezTo>`;
  return customPath(w,h,move(tl,0)+line(w-tr,0)+curve(w-tr+k*tr,0,w,tr-k*tr,w,tr)+line(w,h-br)+curve(w,h-br+k*br,w-br+k*br,h,w-br,h)+line(bl,h)+curve(bl-k*bl,h,0,h-bl+k*bl,0,h-bl)+line(0,tl)+curve(0,tl-k*tl,tl-k*tl,0,tl,0)+'<a:close/>');
}
function shape(ctx,name,r,geom,fill,line){const id=ctx.id++;ctx.parts.push(`<p:sp><p:nvSpPr><p:cNvPr id="${id}" name="${xml(name)}"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr><p:spPr>${transform(r)}${geom}${fill}${line}</p:spPr></p:sp>`);}
function connector(ctx,name,x1,y1,x2,y2,c,w,opacity,arrow){
  const id=ctx.id++,r={x:Math.min(x1,x2),y:Math.min(y1,y2),w:Math.abs(x2-x1),h:Math.abs(y2-y1)};
  ctx.parts.push(`<p:cxnSp><p:nvCxnSpPr><p:cNvPr id="${id}" name="${xml(name)}"/><p:cNvCxnSpPr/><p:nvPr/></p:nvCxnSpPr><p:spPr><a:xfrm${x2<x1?' flipH="1"':''}${y2<y1?' flipV="1"':''}><a:off x="${emu(r.x)}" y="${emu(r.y)}"/><a:ext cx="${emu(r.w)}" cy="${emu(r.h)}"/></a:xfrm><a:prstGeom prst="line"><a:avLst/></a:prstGeom>${stroke(c,w,opacity,arrow)}</p:spPr></p:cxnSp>`);
}
function hyperlink(ctx,el){
  const a=el.closest('a[href]');if(!a)return '';
  const raw=a.getAttribute('href');
  let target,type='hyperlink',external=true;
  if(/^https?:\/\//i.test(raw)||/^mailto:/i.test(raw)){target=raw;}
  else if(raw.startsWith('#')){
    const n=Number(raw.slice(1))||slides.findIndex(s=>s.id===raw.slice(1))+1;
    if(n<1||n>slides.length)return '';
    target=`slide${n}.xml`;type='slide';external=false;
  }else return '';
  let rel=ctx.links.find(i=>i.target===target&&i.type===type);
  if(!rel){rel={id:`rId${ctx.links.length+10}`,type,target,external};ctx.links.push(rel);}
  return `<a:hlinkClick r:id="${rel.id}"${external?'':' action="ppaction://hlinksldjump"'}/>`;
}
function textStyle(s,opacity,link){
  const size=Math.round(parseFloat(s.fontSize)*75),font=s.fontFamily.split(',')[0].replace(/["']/g,'');
  const spacing=parseFloat(s.letterSpacing)||0;
  return `<a:rPr lang="pt-BR" sz="${size}" b="${Number(parseInt(s.fontWeight)>=600)}" i="${Number(s.fontStyle==='italic')}" u="${s.textDecorationLine.includes('underline')?'sng':'none'}"${spacing?` spc="${Math.round(spacing*75)}"`:''}>${solid(s.color,opacity)}<a:latin typeface="${xml(font)}"/><a:ea typeface="${xml(font)}"/><a:cs typeface="${xml(font)}"/>${link}</a:rPr>`;
}
/* Caracteres são medidos com Range para preservar quebras, inline e alinhamento.
   Uma caixa por linha, com vários a:r para negrito/itálico/links sem duplicação. */
function text(ctx,root,origin,opacity,onlyNode=null){
  const nodes=[];
  if(onlyNode)nodes.push(onlyNode);
  else{const walker=document.createTreeWalker(root,NodeFilter.SHOW_TEXT);let n;while((n=walker.nextNode()))nodes.push(n);}
  const range=document.createRange(),lines=[];
  for(const node of nodes){
    const el=node.parentElement,s=getComputedStyle(el);
    if(s.display==='none'||s.visibility==='hidden'||el.closest('.speaker-notes'))continue;
    const isPre=s.whiteSpace.startsWith('pre');
    const link=hyperlink(ctx,el),pr=textStyle(s,opacity,link);
    for(let i=0;i<node.length;i++){
      let ch=node.data[i];
      if(ch==='\n'||ch==='\r'){if(isPre)continue;ch=' ';}
      range.setStart(node,i);range.setEnd(node,i+1);
      const b=range.getBoundingClientRect();
      if(b.width<.01||b.height<.01)continue;
      if(s.textTransform==='uppercase')ch=ch.toUpperCase();
      if(s.textTransform==='lowercase')ch=ch.toLowerCase();
      let line=lines.find(l=>Math.abs(l.top-b.top)<2);
      if(!line){line={top:b.top,left:b.left,right:b.right,h:b.height,font:parseFloat(s.fontSize),runs:[]};lines.push(line);}
      line.left=Math.min(line.left,b.left);line.right=Math.max(line.right,b.right);line.h=Math.max(line.h,b.height);line.font=Math.max(line.font,parseFloat(s.fontSize));
      const last=line.runs.at(-1);
      if(last?.pr===pr)last.value+=ch;else line.runs.push({pr,value:ch});
    }
  }
  for(const line of lines){
    if(!line.runs.some(r=>r.value.trim()))continue;
    const id=ctx.id++,r={x:line.left-origin.left,y:line.top-origin.top,w:line.right-line.left+3,h:Math.max(line.h,line.font*1.35)};
    const runs=line.runs.map(v=>`<a:r>${v.pr}<a:t xml:space="preserve">${xml(v.value)}</a:t></a:r>`).join('');
    ctx.parts.push(`<p:sp><p:nvSpPr><p:cNvPr id="${id}" name="${xml('Texto: '+line.runs.map(r=>r.value).join('').slice(0,60))}"/><p:cNvSpPr txBox="1"/><p:nvPr/></p:nvSpPr><p:spPr>${transform(r)}<a:prstGeom prst="rect"><a:avLst/></a:prstGeom><a:noFill/><a:ln><a:noFill/></a:ln></p:spPr><p:txBody><a:bodyPr wrap="none" lIns="0" tIns="0" rIns="0" bIns="0" anchor="t"><a:noAutofit/></a:bodyPr><a:lstStyle/><a:p><a:pPr marL="0" marR="0" indent="0" algn="l"><a:lnSpc><a:spcPct val="100000"/></a:lnSpc><a:spcBef><a:spcPts val="0"/></a:spcBef><a:spcAft><a:spcPts val="0"/></a:spcAft></a:pPr>${runs}<a:endParaRPr lang="pt-BR" sz="${Math.round(line.font*75)}"/></a:p></p:txBody></p:sp>`);
  }
}

return {NS_A,NS_P,NS_R,xml,doc,color,solid,stroke,group,rels,geometry,shape,connector,text};
})();

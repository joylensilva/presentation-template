/* Montagem OOXML: apresentação, mestres, slides, tema e notas. */
const FormaPackage=(()=>{
const {NS_A,NS_P,NS_R,xml,doc,group,rels}=FormaDrawing;
const {inspect,render,measure}=FormaDOM;
function theme(){
  const colors={dk1:'172B3A',lt1:'FCFCF9',dk2:'294652',lt2:'E5F3F0',accent1:'007E80',accent2:'F1B65C',accent3:'8FC6BC',accent4:'AA4146',accent5:'526674',accent6:'D4DFDF',hlink:'007E80',folHlink:'805210'};
  return doc(`<a:theme xmlns:a="${NS_A}" name="Forma"><a:themeElements><a:clrScheme name="Forma">${Object.entries(colors).map(([k,v])=>`<a:${k}><a:srgbClr val="${v}"/></a:${k}>`).join('')}</a:clrScheme><a:fontScheme name="Forma"><a:majorFont><a:latin typeface="Arial"/><a:ea typeface=""/><a:cs typeface=""/></a:majorFont><a:minorFont><a:latin typeface="Arial"/><a:ea typeface=""/><a:cs typeface=""/></a:minorFont></a:fontScheme><a:fmtScheme name="Forma"><a:fillStyleLst>${[0,1,2].map(()=>'<a:solidFill><a:schemeClr val="phClr"/></a:solidFill>').join('')}</a:fillStyleLst><a:lnStyleLst>${[6350,12700,19050].map(w=>`<a:ln w="${w}" cap="flat" cmpd="sng" algn="ctr"><a:solidFill><a:schemeClr val="phClr"/></a:solidFill><a:prstDash val="solid"/></a:ln>`).join('')}</a:lnStyleLst><a:effectStyleLst><a:effectStyle><a:effectLst/></a:effectStyle><a:effectStyle><a:effectLst/></a:effectStyle><a:effectStyle><a:effectLst/></a:effectStyle></a:effectStyleLst><a:bgFillStyleLst>${[0,1,2].map(()=>'<a:solidFill><a:schemeClr val="phClr"/></a:solidFill>').join('')}</a:bgFillStyleLst></a:fmtScheme></a:themeElements></a:theme>`);
}
const colorMap='<p:clrMap accent1="accent1" accent2="accent2" accent3="accent3" accent4="accent4" accent5="accent5" accent6="accent6" bg1="lt1" bg2="lt2" folHlink="folHlink" hlink="hlink" tx1="dk1" tx2="dk2"/>';
function notesXml(content){
  const paragraphs=content.split(/\n/).map(line=>`<a:p><a:r><a:rPr lang="pt-BR"/><a:t xml:space="preserve">${xml(line)}</a:t></a:r></a:p>`).join('');
  return doc(`<p:notes xmlns:a="${NS_A}" xmlns:r="${NS_R}" xmlns:p="${NS_P}"><p:cSld><p:spTree>${group}<p:sp><p:nvSpPr><p:cNvPr id="2" name="Notas do apresentador"/><p:cNvSpPr txBox="1"/><p:nvPr><p:ph type="body" idx="1"/></p:nvPr></p:nvSpPr><p:spPr/><p:txBody><a:bodyPr/><a:lstStyle/>${paragraphs}</p:txBody></p:sp></p:spTree></p:cSld><p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr></p:notes>`);
}
async function build(){
  const rendered=await measure((s,i)=>{const issues=inspect(s);if(issues.length)throw new Error(`Slide ${i+1}: ${issues[0].message} (${issues[0].element})`);return {ctx:render(s),title:s.dataset.title,notes:s.querySelector('.speaker-notes')?.textContent.trim()||''};});
  const files={},overrides=[];
  function add(path,content,type){files[path]=content;if(type)overrides.push([path,type]);}
  const mime='application/vnd.openxmlformats-officedocument.presentationml.';
  add('_rels/.rels',rels([{id:'rId1',type:'officeDocument',target:'ppt/presentation.xml'},{id:'rId2',type:'extended-properties',target:'docProps/app.xml'}]));
  // As propriedades core usam namespace de relacionamento próprio do pacote.
  files['_rels/.rels']=files['_rels/.rels'].replace('</Relationships>','<Relationship Id="rId3" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/></Relationships>');
  add('docProps/core.xml',doc(`<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"><dc:title>${xml(document.title)}</dc:title><dc:creator>${xml(deck.dataset.author)}</dc:creator><cp:lastModifiedBy>Forma — exportador nativo</cp:lastModifiedBy><dcterms:created xsi:type="dcterms:W3CDTF">${new Date().toISOString()}</dcterms:created></cp:coreProperties>`),'application/vnd.openxmlformats-package.core-properties+xml');
  add('docProps/app.xml',doc(`<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties" xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes"><Application>Forma — JavaScript nativo</Application><PresentationFormat>On-screen Show (16:9)</PresentationFormat><Slides>${rendered.length}</Slides><Notes>${rendered.length}</Notes></Properties>`),'application/vnd.openxmlformats-officedocument.extended-properties+xml');
  add('ppt/presentation.xml',doc(`<p:presentation xmlns:a="${NS_A}" xmlns:r="${NS_R}" xmlns:p="${NS_P}"><p:sldMasterIdLst><p:sldMasterId id="2147483648" r:id="rId1"/></p:sldMasterIdLst><p:notesMasterIdLst><p:notesMasterId r:id="rId2"/></p:notesMasterIdLst><p:sldIdLst>${rendered.map((s,i)=>`<p:sldId id="${256+i}" r:id="rId${i+3}"/>`).join('')}</p:sldIdLst><p:sldSz cx="12192000" cy="6858000" type="screen16x9"/><p:notesSz cx="6858000" cy="9144000"/><p:defaultTextStyle><a:defPPr><a:defRPr lang="pt-BR"/></a:defPPr></p:defaultTextStyle></p:presentation>`),mime+'presentation.main+xml');
  add('ppt/_rels/presentation.xml.rels',rels([{id:'rId1',type:'slideMaster',target:'slideMasters/slideMaster1.xml'},{id:'rId2',type:'notesMaster',target:'notesMasters/notesMaster1.xml'},...rendered.map((s,i)=>({id:`rId${i+3}`,type:'slide',target:`slides/slide${i+1}.xml`}))]));
  add('ppt/theme/theme1.xml',theme(),'application/vnd.openxmlformats-officedocument.theme+xml');
  add('ppt/slideMasters/slideMaster1.xml',doc(`<p:sldMaster xmlns:a="${NS_A}" xmlns:r="${NS_R}" xmlns:p="${NS_P}"><p:cSld name="Forma"><p:spTree>${group}</p:spTree></p:cSld>${colorMap}<p:sldLayoutIdLst><p:sldLayoutId id="2147483649" r:id="rId1"/></p:sldLayoutIdLst><p:txStyles><p:titleStyle/><p:bodyStyle/><p:otherStyle/></p:txStyles></p:sldMaster>`),mime+'slideMaster+xml');
  add('ppt/slideMasters/_rels/slideMaster1.xml.rels',rels([{id:'rId1',type:'slideLayout',target:'../slideLayouts/slideLayout1.xml'},{id:'rId2',type:'theme',target:'../theme/theme1.xml'}]));
  add('ppt/slideLayouts/slideLayout1.xml',doc(`<p:sldLayout xmlns:a="${NS_A}" xmlns:r="${NS_R}" xmlns:p="${NS_P}" type="blank" preserve="1"><p:cSld name="Em branco"><p:spTree>${group}</p:spTree></p:cSld><p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr></p:sldLayout>`),mime+'slideLayout+xml');
  add('ppt/slideLayouts/_rels/slideLayout1.xml.rels',rels([{id:'rId1',type:'slideMaster',target:'../slideMasters/slideMaster1.xml'}]));
  add('ppt/notesMasters/notesMaster1.xml',doc(`<p:notesMaster xmlns:a="${NS_A}" xmlns:r="${NS_R}" xmlns:p="${NS_P}"><p:cSld><p:spTree>${group}</p:spTree></p:cSld>${colorMap}<p:notesStyle><a:lvl1pPr><a:defRPr sz="1200"/></a:lvl1pPr></p:notesStyle></p:notesMaster>`),mime+'notesMaster+xml');
  add('ppt/notesMasters/_rels/notesMaster1.xml.rels',rels([{id:'rId1',type:'theme',target:'../theme/theme1.xml'}]));
  rendered.forEach(({ctx,title,notes},i)=>{
    const n=i+1;
    add(`ppt/slides/slide${n}.xml`,doc(`<p:sld xmlns:a="${NS_A}" xmlns:r="${NS_R}" xmlns:p="${NS_P}"><p:cSld name="${xml(title)}"><p:spTree>${group}${ctx.parts.join('')}</p:spTree></p:cSld><p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr></p:sld>`),mime+'slide+xml');
    add(`ppt/slides/_rels/slide${n}.xml.rels`,rels([{id:'rId1',type:'slideLayout',target:'../slideLayouts/slideLayout1.xml'},{id:'rId2',type:'notesSlide',target:`../notesSlides/notesSlide${n}.xml`},...ctx.links]));
    add(`ppt/notesSlides/notesSlide${n}.xml`,notesXml(notes),mime+'notesSlide+xml');
    add(`ppt/notesSlides/_rels/notesSlide${n}.xml.rels`,rels([{id:'rId1',type:'notesMaster',target:'../notesMasters/notesMaster1.xml'},{id:'rId2',type:'slide',target:`../slides/slide${n}.xml`}]));
  });
  files['[Content_Types].xml']=doc(`<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/>${overrides.map(([p,t])=>`<Override PartName="/${p}" ContentType="${t}"/>`).join('')}</Types>`);
  return FormaZip.zip(files);
}

return {build};
})();

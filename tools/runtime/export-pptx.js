/* API de download e feedback da exportação. */
const Pptx=(()=>{
let exporting=false;
  async function exportPptx({download=true}={}){
    if(exporting)throw new Error('Uma exportação já está em andamento.');
    exporting=true;$('export-button').disabled=true;status('Gerando formas e textos editáveis…');
    try{
      const bytes=await FormaPackage.build();
      if(download){const url=URL.createObjectURL(new Blob([bytes],{type:'application/vnd.openxmlformats-officedocument.presentationml.presentation'})),a=document.createElement('a');a.href=url;a.download=(document.title.replace(/[^\p{L}\p{N} _-]/gu,'').trim()||'aula')+'.pptx';a.click();setTimeout(()=>URL.revokeObjectURL(url),30000);}
      status(`PPTX gerado: ${slides.length} slides, com formas e textos editáveis.`);return bytes;
    }catch(error){status('Exportação interrompida: '+error.message);throw error;}
    finally{exporting=false;$('export-button').disabled=false;}
  }
  return {exportPptx,validate:FormaDOM.validate};
})();

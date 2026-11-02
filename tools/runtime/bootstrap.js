window.AulaTemplate=Object.freeze({...Pptx,goTo,present,get current(){return current+1;},slideCount:slides.length});
// Nome agnóstico; AulaTemplate é mantido como alias para apresentações existentes.
window.FormaPresentation=window.AulaTemplate;
$('export-button').onclick=()=>Pptx.exportPptx().catch(error=>console.error(error));

/* ZIP STORE nativo; sem dependências. */
const FormaZip=(()=>{
const ENC=new TextEncoder();
const crcTable=Uint32Array.from({length:256},(_,n)=>{for(let i=0;i<8;i++)n=n&1?0xedb88320^(n>>>1):n>>>1;return n>>>0;});
function crc32(data){let n=0xffffffff;for(const v of data)n=crcTable[(n^v)&255]^(n>>>8);return(n^0xffffffff)>>>0;}
function zip(files){
  const local=[],central=[];let offset=0;
  const header=n=>{const b=new Uint8Array(n);return[b,new DataView(b.buffer)];};
  for(const [name,source] of Object.entries(files)){
    const filename=ENC.encode(name),data=typeof source==='string'?ENC.encode(source):source,crc=crc32(data);
    const [l,lv]=header(30);lv.setUint32(0,0x04034b50,true);lv.setUint16(4,20,true);lv.setUint16(6,0x800,true);lv.setUint16(12,33,true);lv.setUint32(14,crc,true);lv.setUint32(18,data.length,true);lv.setUint32(22,data.length,true);lv.setUint16(26,filename.length,true);
    local.push(l,filename,data);
    const [c,cv]=header(46);cv.setUint32(0,0x02014b50,true);cv.setUint16(4,20,true);cv.setUint16(6,20,true);cv.setUint16(8,0x800,true);cv.setUint16(14,33,true);cv.setUint32(16,crc,true);cv.setUint32(20,data.length,true);cv.setUint32(24,data.length,true);cv.setUint16(28,filename.length,true);cv.setUint32(42,offset,true);central.push(c,filename);offset+=l.length+filename.length+data.length;
  }
  const size=central.reduce((n,b)=>n+b.length,0),[end,ev]=header(22),count=Object.keys(files).length;
  ev.setUint32(0,0x06054b50,true);ev.setUint16(8,count,true);ev.setUint16(10,count,true);ev.setUint32(12,size,true);ev.setUint32(16,offset,true);
  const out=new Uint8Array(offset+size+end.length);let at=0;for(const chunk of [...local,...central,end]){out.set(chunk,at);at+=chunk.length;}return out;
}

return {zip};
})();

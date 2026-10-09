const sharp=require('sharp');const fs=require('fs');
const svg=fs.readFileSync('icon-source.svg');
const jobs=[[192,'icon-192.png'],[512,'icon-512.png'],[180,'apple-touch-icon.png']];
Promise.all(jobs.map(([s,f])=>sharp(svg).resize(s,s).png().toFile(f).then(()=>console.log('ok',f))))
.then(()=>console.log('done')).catch(e=>{console.error(e);process.exit(1)});

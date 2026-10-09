const sharp=require('sharp');const fs=require('fs');
const full=fs.readFileSync('icon-source.svg');     // design completo (gradiente + sacola)
const fg=fs.readFileSync('icon-foreground.svg');    // sacola em fundo transparente (adaptive)
const res='android/app/src/main/res';
// legado: ic_launcher.png + ic_launcher_round.png
const legacy={ 'mdpi':48,'hdpi':72,'xhdpi':96,'xxhdpi':144,'xxxhdpi':192 };
// adaptive foreground (108dp): densidades maiores
const fgDp={ 'mdpi':108,'hdpi':162,'xhdpi':216,'xxhdpi':324,'xxxhdpi':432 };
const jobs=[];
for(const [d,s] of Object.entries(legacy)){
  jobs.push(sharp(full).resize(s,s).png().toFile(`${res}/mipmap-${d}/ic_launcher.png`));
  jobs.push(sharp(full).resize(s,s).png().toFile(`${res}/mipmap-${d}/ic_launcher_round.png`));
}
for(const [d,s] of Object.entries(fgDp)){
  jobs.push(sharp(fg).resize(s,s).png().toFile(`${res}/mipmap-${d}/ic_launcher_foreground.png`));
}
Promise.all(jobs).then(()=>console.log('Gerados',jobs.length,'PNGs de launcher')).catch(e=>{console.error(e);process.exit(1)});

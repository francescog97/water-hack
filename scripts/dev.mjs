import {spawn} from 'node:child_process';
import {existsSync} from 'node:fs';
import {resolve} from 'node:path';
const python=resolve(process.platform==='win32'?'.venv/Scripts/python.exe':'.venv/bin/python');
if(!existsSync(python)){console.error('Create .venv and install app/backend/requirements.txt first. See docs/RUN_LOCAL.md.');process.exit(1);}
const children=[spawn(python,['-m','uvicorn','app.backend.app.main:app','--host','127.0.0.1','--port','8000'],{stdio:'inherit'}),spawn(process.execPath,['node_modules/vite/bin/vite.js','app/frontend','--config','app/frontend/vite.config.ts'],{stdio:'inherit'})];
let stopping=false;
function stop(code=0){if(stopping)return;stopping=true;for(const child of children)child.kill();setTimeout(()=>process.exit(code),150);}
process.on('SIGINT',()=>stop());process.on('SIGTERM',()=>stop());
for(const child of children){child.on('error',err=>{console.error(err.message);stop(1)});child.on('exit',code=>{if(!stopping)stop(code??1)});}

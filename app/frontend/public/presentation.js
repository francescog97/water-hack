const slides=[...document.querySelectorAll('article')];
const previous=document.querySelector('#previous'),next=document.querySelector('#next');
let current=Math.max(0,Math.min(slides.length-1,Number.parseInt(location.hash.slice(1)||'1',10)-1||0));
function render(){slides.forEach((slide,index)=>slide.classList.toggle('active',index===current));document.querySelector('#counter').textContent=`${current+1} / ${slides.length}`;document.querySelector('#progress').value=current+1;previous.disabled=current===0;next.disabled=current===slides.length-1;history.replaceState(null,'',`#${current+1}`);}
function move(direction){current=Math.max(0,Math.min(slides.length-1,current+direction));render();window.scrollTo(0,0);}
previous.addEventListener('click',()=>move(-1));next.addEventListener('click',()=>move(1));
document.querySelector('#notes').addEventListener('click',()=>document.body.classList.toggle('show-notes'));
window.addEventListener('hashchange',()=>{current=Math.max(0,Math.min(slides.length-1,Number.parseInt(location.hash.slice(1)||'1',10)-1||0));render();});
document.addEventListener('keydown',event=>{if(event.key==='ArrowRight'){event.preventDefault();move(1);}if(event.key==='ArrowLeft'){event.preventDefault();move(-1);}});
render();

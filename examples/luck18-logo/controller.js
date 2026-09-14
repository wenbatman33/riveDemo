export function mount({player,container}) {
  const canvas=document.querySelector('#viewer canvas');
  let x=0,y=0,tx=0,ty=0,frame=0,disposed=false;
  const clamp=v=>Math.max(-1,Math.min(1,v));
  function update(){
    if(disposed)return;
    x+=(tx-x)*.1;y+=(ty-y)*.1;
    const vm=player.viewModelInstance;
    if(vm){vm.number('pointerX').value=x;vm.number('pointerY').value=y;vm.number('scaleX').value=1-Math.abs(x)*.07;vm.number('scaleY').value=1-Math.abs(y)*.04;}
    frame=requestAnimationFrame(update);
  }
  function move(e){const r=canvas.getBoundingClientRect();tx=clamp((e.clientX-r.left)/r.width*2-1);ty=clamp((e.clientY-r.top)/r.height*2-1);}
  function reset(){tx=ty=0;}
  canvas.addEventListener('pointermove',move);canvas.addEventListener('pointerleave',reset);canvas.addEventListener('pointercancel',reset);
  const b=document.createElement('button');b.textContent='回正';b.onclick=reset;container.append(b);container.hidden=false;
  frame=requestAnimationFrame(update);
  return ()=>{disposed=true;cancelAnimationFrame(frame);canvas.removeEventListener('pointermove',move);canvas.removeEventListener('pointerleave',reset);canvas.removeEventListener('pointercancel',reset);};
}

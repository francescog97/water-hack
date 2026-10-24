export async function api<T>(path:string, body?:unknown, signal?:AbortSignal):Promise<T>{
  const result=await fetch(`/api${path}`,{method:body===undefined?'GET':'POST',headers:body===undefined?undefined:{'Content-Type':'application/json'},body:body===undefined?undefined:JSON.stringify(body),signal});
  if(!result.ok){let detail=`Request failed (${result.status})`;try{const error=await result.json();if(typeof error.detail==='string')detail=error.detail;}catch{/* preserve bounded generic error */}throw new Error(detail);}
  return result.json();
}

(() => {
  "use strict";
  const $ = id => document.getElementById(id);
  const notice = $("notice"), list = $("list"), form = $("legacy-form"), token = $("token");
  const labels = {network:"網路工程", cctv:"監視器", access:"門禁系統"};
  function status(message,error=false) {
    notice.textContent=message;
    notice.className="notice "+(error?"error":"ok");
  }
  function row(tag,text) {
    const node=document.createElement(tag);
    node.textContent=String(text);
    return node;
  }
  async function api(url,method="GET",body=null) {
    if(!token.value.trim()) throw Error("需輸入本機測試權杖");
    const options={method,cache:"no-store",headers:{Authorization:"Bearer "+token.value.trim()}};
    if(body){options.headers["Content-Type"]="application/json";options.body=JSON.stringify(body);}
    const response=await fetch(url,options);
    const result=await response.json().catch(()=>({}));
    if(!response.ok) throw Error("HTTP "+response.status+"："+(typeof result.detail==="string"?result.detail:"驗證失敗"));
    return result;
  }
  async function refresh() {
    const jobs=await api("/my/requests");
    list.replaceChildren();
    if(!jobs.length){list.append(row("p","此測試身分尚無案件"));return;}
    for(const job of jobs) {
      const item=row("article","");
      item.className="item";
      item.append(row("strong",(labels[job.category]||"工程")+"｜"+job.region));
      item.append(row("p",job.description));
      item.append(row("p","案件 "+job.id.slice(0,8)+" · "+job.state));
      list.append(item);
    }
  }
  $("refresh").addEventListener("click",async()=>{
    try{await refresh();status("已從隔離後端讀回案件");}catch(error){status(error.message,true);}
  });
  form.addEventListener("submit",async event=>{
    event.preventDefault();
    const fields=new FormData(form);
    const payload={categoryId:fields.get("categoryId"),region:fields.get("region"),description:fields.get("description")};
    try{
      const saved=await api("/legacy/requests","POST",payload);
      await refresh();
      status("成功送至後端並待審核："+saved.id.slice(0,8));
    }catch(error){status(error.message,true);}
  });
})();

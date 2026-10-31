// Controlled local-only UI; no localStorage, no external APIs, no payment.
(() => {
  "use strict";
  const el = id => document.getElementById(id);
  const role = el("role"), token = el("token"), notice = el("notice");
  const panels = {customer: el("customer-panel"), reviewer: el("reviewer-panel"), contractor: el("contractor-panel")};
  const cat = {network:"商用網路／Wi-Fi", cctv:"監視器 CCTV",access:"門禁／弱電"};
  const temporaryTokens = {customer:"",reviewer:"",contractor:""};
  let activeRole = "customer";
  function element(tag, value, cls) {
    const n = document.createElement(tag);
    n.textContent = value == null ? "" : String(value);
    if (cls) n.className = cls;
    return n;
  }
  function status(message, error) {
    notice.textContent = message;
    notice.className = "notice " + (error ? "error" : "ok");
  }
  async function api(path, method, payload) {
    if (!token.value.trim()) throw Error("請輸入本機測試權杖");
    const options = {method:method || "GET", cache:"no-store",
      headers:{Authorization:"Bearer " + token.value.trim()}};
    if (payload) {
      options.headers["Content-Type"]="application/json";
      options.body=JSON.stringify(payload);
    }
    const result=await fetch(path,options);
    const data=await result.json().catch(()=>({}));
    if (!result.ok) throw Error("HTTP " + result.status + "：" +
      (typeof data.detail === "string" ? data.detail : "操作被拒絕"));
    return data;
  }
  async function run(message, action) {
    try { await action(); await refresh(); status(message); }
    catch (e) { status(e.message,true); }
  }
  function button(text,action,primary) {
    const b=element("button",text,"btn"+(primary?" primary":""));
    b.type="button";b.addEventListener("click",action);return b;
  }
  function shell(j) {
    const a=element("article","","item");
    a.append(element("strong",(cat[j.category]||"工程")+"｜"+(j.region||"測試")));
    a.append(element("div","案件："+j.id.slice(0,8)+" · "+j.state,"meta"));
    a.append(element("p",j.description));
    return a;
  }
  async function customers() {
    const box=el("customer-list");box.replaceChildren();
    const jobs=await api("/my/requests");
    if (!jobs.length){box.append(element("p","尚無示範發案。","empty"));return;}
    for (const job of jobs) {
      const row=shell(job);
      if (job.state==="APPROVED" || job.state==="SELECTED") {
        const quotes=await api("/requests/"+encodeURIComponent(job.id)+"/quotes");
        if (!quotes.length) row.append(element("p","尚未收到報價"));
        for (const q of quotes) {
          row.append(element("p","報價 NT$"+q.price_ntd.toLocaleString()+"｜"+q.scope));
          if (job.state==="APPROVED")
            row.append(button("選擇此報價",()=>run("已選擇示範報價（無付款）",
              ()=>api("/quotes/"+encodeURIComponent(q.id)+"/select","POST")),true));
          if (job.selected_quote===q.id) row.append(element("p","✓ 此報價已選擇（無付款）"));
        }
      }
      box.append(row);
    }
  }
  async function reviewers() {
    const box=el("review-list");box.replaceChildren();
    const jobs=await api("/review/requests");
    if (!jobs.length){box.append(element("p","目前沒有待審核案件。","empty"));return;}
    for(const j of jobs){
      const row=shell(j),buttons=element("div","","actions");
      buttons.append(button("核准公開",()=>run("審核通過",
        ()=>api("/requests/"+encodeURIComponent(j.id)+"/moderate","POST",{decision:"APPROVED"})),true));
      buttons.append(button("退回",()=>run("已退回",
        ()=>api("/requests/"+encodeURIComponent(j.id)+"/moderate","POST",{decision:"REJECTED"}))));
      row.append(buttons);box.append(row);
    }
  }
  async function contractors() {
    const box=el("contractor-list");box.replaceChildren();
    const jobs=await api("/requests");
    if (!jobs.length){box.append(element("p","尚無核准案件。","empty"));return;}
    for(const j of jobs){
      const row=shell(j),form=document.createElement("form");
      const pl=element("label","工程報價（NT$）"),price=document.createElement("input");
      price.type="number";price.min=1;price.max=10000000;price.required=true;price.value=28000;pl.append(price);
      const sl=element("label","交付範圍"),scope=document.createElement("textarea");
      scope.minLength=10;scope.maxLength=1000;scope.required=true;
      scope.value="含測試設備安裝與基本設定，不包含實際付款。";sl.append(scope);
      const submit=element("button","提交示範報價","btn primary");submit.type="submit";
      form.append(pl,sl,submit);
      form.addEventListener("submit",e=>{
        e.preventDefault();run("報價已保存（無付款）",
          ()=>api("/quotes","POST",{request_id:j.id,price_ntd:Number(price.value),scope:scope.value}));
      });
      row.append(form);box.append(row);
    }
  }
  async function refresh(){
    try {
      if(activeRole==="customer")await customers();
      if(activeRole==="reviewer")await reviewers();
      if(activeRole==="contractor")await contractors();
      status("角色："+role.selectedOptions[0].text+"；資料來自隔離 API。");
    }catch(e){status(e.message,true);}
  }
  role.addEventListener("change",()=>{
    temporaryTokens[activeRole]=token.value; activeRole=role.value;
    token.value=temporaryTokens[activeRole];
    for(const [name,panel] of Object.entries(panels))panel.hidden=(name!==activeRole);
    el("customer-list").replaceChildren();el("review-list").replaceChildren();el("contractor-list").replaceChildren();
    status("切換角色："+role.selectedOptions[0].text+"，請輸入本機測試權杖。");
  });
  el("load").addEventListener("click",refresh);
  el("request-form").addEventListener("submit",e=>{
    e.preventDefault();const f=new FormData(e.currentTarget);
    run("示範案件已建立（待審核）",()=>api("/requests","POST",{
      category:f.get("category"),region:f.get("region"),description:f.get("description")}));
  });
  for(const [name,panel] of Object.entries(panels))panel.hidden=(name!==activeRole);
})();

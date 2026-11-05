"use strict";
// Local synthetic click simulation: no cookies, network, storage, external URL or commission claims.
const offers = [
  {subid:"xy_art_ig_001",rate:0.04},
  {subid:"xy_nas_yt_001",rate:0.03},
  {subid:"xy_travel_blog_001",rate:0.05}
];
const state = Object.fromEntries(offers.map(item => [item.subid,{clicks:0,orders:0}]));
const tbody=document.getElementById("rows");
const summary=document.getElementById("summary");
const amount=document.getElementById("order-value");
const money=n=>new Intl.NumberFormat("zh-TW",{style:"currency",currency:"TWD",maximumFractionDigits:0}).format(n);
function render(){
  const price=Math.max(0,Math.min(1e6,Number(amount.value)||0));
  tbody.replaceChildren();
  let clicks=0,orders=0,estimated=0;
  for(const offer of offers){
    const item=state[offer.subid];
    clicks+=item.clicks;orders+=item.orders;
    const commission=item.orders*price*offer.rate;estimated+=commission;
    const tr=document.createElement("tr");
    for(const value of [offer.subid,String(item.clicks),String(item.orders),money(commission),money(0)]){
      const td=document.createElement("td");td.textContent=value;tr.appendChild(td);
    }
    tbody.appendChild(tr);
  }
  summary.textContent="合成點擊："+clicks+"；合成訂單："+orders+"；假設佣金："+money(estimated)+"；真實已結算：NT$0";
}
for(const button of document.querySelectorAll("[data-subid]")){
  button.addEventListener("click",()=>{state[button.dataset.subid].clicks+=1;render();});
}
document.getElementById("reset").addEventListener("click",()=>{for(const v of Object.values(state)){v.clicks=0;v.orders=0;}render();});
amount.addEventListener("input",render);
render();

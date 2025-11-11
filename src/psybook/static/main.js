async function loadSlots(){
  const day=document.getElementById("day").value;
  const r=await fetch(`/api/v1/slots?day=${day}`);
  const data=await r.json();
  const wrap=document.getElementById("slots");
  wrap.innerHTML="";
  data.forEach(s=>{
    const div=document.createElement("div");
    div.innerHTML=`<b>${s.slot_id}</b> — ${new Date(s.start_local).toLocaleString()} → ${new Date(s.end_local).toLocaleString()} — ${s.available?"✅ свободно":"❌ занято"} <button ${s.available?"":"disabled"} onclick="document.getElementById('slotId').value='${s.slot_id}'">Выбрать</button>`;
    wrap.appendChild(div);
  });
}
async function book(){
  const payload={slot_id:slotId.value,name:name.value,email:email.value};
  const r=await fetch("/api/v1/bookings",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(payload)});
  bookResult.textContent=await r.text();
  await loadSlots();
}
async function cancelBooking(){
  const payload={booking_id:bookingId.value,email:emailCancel.value};
  const r=await fetch("/api/v1/bookings/cancel",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(payload)});
  cancelResult.textContent=r.ok?"Отменено ✅":"Ошибка";
  await loadSlots();
}
document.addEventListener("DOMContentLoaded",()=>{
  const d=new Date(),m=String(d.getMonth()+1).padStart(2,"0"),day=String(d.getDate()).padStart(2,"0");
  document.getElementById("day").value=`${d.getFullYear()}-${m}-${day}`;
  loadSlots();
});

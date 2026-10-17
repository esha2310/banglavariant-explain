const form=$('authForm'),signup=document.body.dataset.mode==='signup';
if(form){if(!backend){document.querySelectorAll('#authForm input,#authForm button').forEach(e=>e.disabled=true)}else{$('previewNote').classList.add('hidden');accountInit()}
 form.onsubmit=async e=>{e.preventDefault();if(!backend)return;let d={username:$('username').value.trim(),password:$('password').value};if(signup){d.password_confirm=$('confirm').value;d.accepted_limits=$('accept').checked}if(!csrf){$('authError').textContent=tr('Wait for the secure session.','Secure session load হওয়া পর্যন্ত অপেক্ষা করুন।');return}$('submitButton').disabled=true;try{await api(signup?'signup':'login',d);location.href='dashboard.html'}catch(e){$('authError').textContent=e.message}finally{$('submitButton').disabled=false}};
}

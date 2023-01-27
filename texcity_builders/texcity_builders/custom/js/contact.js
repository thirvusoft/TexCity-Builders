frappe.ui.form.on('Contact',{
    refresh:function(frm){
        frm.remove_custom_button('Invite as User');
        if(!frm.doc.from_lead && !frm.doc.lead_created && !frm.is_new()){
            frm.add_custom_button(('Create Lead'), async ()=>{
                var doc = frappe.model.get_new_doc('Lead Management') ;
                doc.from_contact = 1;
                doc.contact = frm.doc.name;
                var phone = '', country_code='';
                if(frm.doc.phone_nos){
                    phone = frm.doc.phone_nos[0].phone || "";
                }
                if(phone.includes('+')){
                    country_code=phone.split('-')[0];
                    phone = phone.split('-')[1] || '';
                }
                doc.lead_name=frm.doc.first_name || "";
                doc.mobile_no = (country_code.trim() || '+91') + '- '+ phone.trim();
                doc.whatsapp_no = phone;
                frappe.ui.form.make_quick_entry('Lead Management',function after_insert(doc){
                    frappe.call({
                        method:'texcity_builders.texcity_builders.custom.py.contact.update_contact_for_lead',
                        args:{
                            cn_name:frm.doc.name,
                            value:1,
                            lead_doc:doc.name
                        },
                        callback(r){
                            frm.refresh_field('lead_created');
                            frm.reload_doc();
                        }
                    });
                }, undefined, doc)
                
            })
            let button = document.querySelectorAll('button[data-label="Create%20Lead"]')[0];
            button.style.color = '#262625';
            button.style['font-weight'] = 'bold';
            button.style['background-color'] = '#fcca03';
        }
    },
})



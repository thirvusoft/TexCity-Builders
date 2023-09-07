frappe.ui.form.on("Project",{
    setup: function(frm){
        frm.set_query("parent_project",function(){
            return {
                "filters": {
                    "is_group":1,
                   
                }
            }
        })
        
    }
})
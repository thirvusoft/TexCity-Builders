frappe.provide('frappe.ui.form');

frappe.ui.form.LeadManagementQuickEntryForm = class LeadManagementQuickEntryForm extends frappe.ui.form.QuickEntryForm {
	constructor(doctype, after_insert, init_callback, doc, force) {
		super(doctype, after_insert, init_callback, doc, force);
		this.skip_redirect_on_error = true;
	}
    render_dialog() {
		var me = this;
		var col_brk = 0
		var cur_col_brk = 0
		this.mandatory.forEach(d => {
			if(d.fieldtype == 'Column Break'){
				cur_col_brk += 1
			}
			if(d.fieldtype == 'Section Break'){
				if(cur_col_brk > col_brk){
					col_brk = cur_col_brk
				}
				cur_col_brk = 0
			}
			if(d.fieldname=='request_for_site'){
				d.onchange = function(){
					if(me.dialog.fields_dict.request_for_site.value){
					if(me.dialog.fields_dict.request_for_site.value.find(element => element.site=='Others')){
						me.dialog.fields_dict.site__others_checked.set_value(1)
					}
					else{
						me.dialog.fields_dict.site__others_checked.set_value(0)
					}
					me.dialog.refresh()
				}
				}
			}
			if(d.fieldname=='site__others_checked'){
				d.onchange = function(){
					me.dialog.refresh()
				}
			}
		})
		
		this.dialog = new frappe.ui.Dialog({
			title: __("New {0}", [__(this.doctype)]),
			fields: this.mandatory,
			doc: this.doc,
			size:col_brk>=2?'large':''
		});

		this.register_primary_action();
		!this.force && this.render_edit_in_full_page_link();
		// ctrl+enter to save
		this.dialog.wrapper.keydown(function (e) {
			if ((e.ctrlKey || e.metaKey) && e.which == 13) {
				if (!frappe.request.ajax_count) {
					// not already working -- double entry
					me.dialog.get_primary_btn().trigger("click");
					e.preventDefault();
					return false;
				}
			}
		});

		this.dialog.onhide = () => (frappe.quick_entry = null);
		this.dialog.show();

		this.dialog.refresh_dependency();
		this.set_defaults();

		if (this.init_callback) {
			this.init_callback(this.dialog);
		}
	}
    insert() {
		let me = this;
		return new Promise((resolve) => {
			me.update_doc();
			frappe.call({
				method: "frappe.client.save",
				args: {
					doc: me.dialog.doc,
				},
				callback: function (r) {
					if (frappe.model.is_submittable(me.doctype)) {
						frappe.run_serially([
							() => (me.dialog.working = true),
							() => {
								me.dialog.set_primary_action(__("Submit"), function () {
									me.submit(r.message);
								});
							},
						]);
					} else {
						me.dialog.hide();
						// delete the old doc
						frappe.model.clear_doc(me.dialog.doc.doctype, me.dialog.doc.name);
						me.dialog.doc = r.message;
						if (frappe._from_link) {
							frappe.ui.form.update_calling_link(me.dialog.doc);
						} else {
							if (me.after_insert) {
								me.after_insert(me.dialog.doc);
							} else {
								// me.open_form_if_not_list();
							}
						}
					}
				},
				error: function () {
					if (!me.skip_redirect_on_error) {
						me.open_doc(true);
					}
				},
				always: function () {
					me.dialog.working = false;
					resolve(me.dialog.doc);
				},
				freeze: true,
			});
		});
	}
}
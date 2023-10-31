frappe.listview_settings["Employee Checkin"] = {
    onload: function(list_view){
        list_view.page.add_inner_button(__("Checkin"), async function(){
            
        let cur_location = await get_location()   
        frappe.call({
            method:"texcity_builders.texcity_builders.custom.py.employee_checkin.create_checkin",
            args:{
                lat: cur_location["latitude"],
                long:cur_location["longitude"]
            },
            callback(r){
                if(r.message){
                    frappe.show_alert({"message":"Checkin Created Successfully", "indicator":"green"})
                }
                else{
                    frappe.show_alert({"message":"Unable to Create Checkin. Try Again", "indicator":"red"})
                }
                list_view.refresh()
            }
        })
            
        })

        list_view.page.add_inner_button(__("Checkout"), async function(){
            let cur_location = await get_location()       
            frappe.call({
                method:"texcity_builders.texcity_builders.custom.py.employee_checkin.create_checkout",
                args:{
                    lat: cur_location["latitude"],
                    long:cur_location["longitude"]
                },
                callback(r){
                    if(r.message){
                        frappe.show_alert({"message":"Checkout Created Successfully", "indicator":"green"})
                    }
                    else{
                        frappe.show_alert({"message":"Unable to Create Checkout. Try Again", "indicator":"red"})
                    }
                    list_view.refresh()
                }
            })
        })

    list_view.page.menu_btn_group.prevObject[0].style.marginTop="auto"
    $(list_view.page.menu_btn_group.prevObject.find(".custom-actions")).removeClass("hidden-xs")
    $(list_view.page.menu_btn_group.prevObject.find(".custom-actions")).removeClass("hidden-md")
    }
}
async function get_location() {
    check_location_permission()
    async function getLocation() {
        let latitude, longitude;
        try {
            let position = await new Promise((resolve, reject) => {
                navigator.geolocation.getCurrentPosition(resolve, reject);
            });

            latitude = position.coords.latitude;
            longitude = position.coords.longitude;
        } catch (error) {
            // Handle errors by displaying them as alerts
            switch (error.code) {
                case error.PERMISSION_DENIED:
                    window.alert("User denied the request for Geolocation.");
                    break;
                case error.POSITION_UNAVAILABLE:
                    window.alert("Location information is unavailable.");
                    break;
                case error.TIMEOUT:
                    window.alert("The request to get user location timed out.");
                    break;
                default:
                    window.alert("An unknown error occurred.");
            }
        }
        return {"latitude":latitude, "longitude":longitude}
    }
    return await getLocation();
}
function check_location_permission() {
    if ("geolocation" in navigator) {
        // Geolocation is available
    } else {
        // Geolocation is not available
        window.alert("Geolocation is not supported in this browser.");
    }
}
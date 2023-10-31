frappe.ui.form.on("Employee Checkin", {
    refresh: function(frm){
        if(frm.doc.checkin_latitude && frm.doc.checkin_longitude){
            var map = frm.get_field("custom_map").map;
            var latlng = L.latLng({'lat':frm.doc.checkin_latitude, 'lng': frm.doc.checkin_longitude});
            var marker = L.marker(latlng);
                        
            map.flyTo(latlng, 17);
            marker.addTo(map);
        }
        if(frm.doc.checkout_latitude && frm.doc.checkout_longitude){
            var map = frm.get_field("custom_map").map;
            var latlng = L.latLng({'lat':frm.doc.checkout_latitude, 'lng': frm.doc.checkout_longitude});
            var marker = L.marker(latlng);
                        
            map.flyTo(latlng, 17);
            marker.addTo(map);
        }
    }
})
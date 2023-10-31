frappe.ui.form.on("User", {
    refresh: function(frm){
        if(frm.doc.last_latitude && frm.doc.last_longitude){
            var map = frm.get_field("map").map;
            var latlng = L.latLng({'lat':frm.doc.last_latitude, 'lng': frm.doc.last_longitude});
            var marker = L.marker(latlng);
                        
            map.flyTo(latlng, 17);
            marker.addTo(map);
        }
    }
})
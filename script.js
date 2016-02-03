var Esri_WorldGrayCanvas = L.tileLayer('http://server.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Light_Gray_Base/MapServer/tile/{z}/{y}/{x}', {
    attribution: 'Tiles &copy; Esri &mdash; Esri, DeLorme, NAVTEQ',
    maxZoom: 16
});

var map = ""
var myLayer = ""
var teams={"All NHL Players":"All_NHL","Anaheim Ducks":"ANA","Boston Bruins":"BOS","Buffalo Sabres":"BUF","Carolina Hurricanes":"CAR","Columbus Blue Jackets":"CBJ","Calgary Flames":"CGY","Chicago Blackhawks":"CHI","Colorado Avalanche":"COL","Dallas Stars":"DAL","Detroit Red Wings":"DET","Edmonton Oilers":"EDM","Florida Panthers":"FLA","Los Angeles Kings":"LAK","Minnesota Wild":"MIN","Montreal Canadiens":"MTL","New Jersey Devils":"NJD","New York Rangers":"NYR","Ottawa Senators":"OTT","Philadelphia Flyers":"PHI","Phoenix Coyotes":"PHX","Pittsburgh Penguins":"PIT","San Jose Sharks":"SJS","St. Louis Blues":"STL","Tampa Bay Lightning":"TBL","Toronto Maple Leafs":"TOR","Vancouver Canucks":"VAN","Winnipeg Jets":"WPG","Washington Capitals":"WSH"};

function addTeam(teamName) {
    //$("#output").val(ui.item.label)
    $.getJSON("./outGeoJSON/" + teams[teamName] + '.geojson',
        function(data) {

            if (myLayer != "") {
                map.removeLayer(myLayer);
            }

            myLayer = L.geoJson(data, {

                // style: function(feature) {
                //    return feature.properties && feature.properties.style;
                //},

                onEachFeature: function(feature, layer) {
                    //popup = "<h5>" + feature.properties.placeName + "<\/h5><br><p>";
                    popup = "<strong>" + feature.properties.placeName + "</strong><br><hr/>";
                    //popup += "<hr>";
                    popup += feature.properties.players

                    layer.bindPopup(popup);
                },

                pointToLayer: function(feature, latlng) {
                    return L.circleMarker(latlng, {
                        radius: scaledRadius(feature.properties.playerCount),
                        fillColor: "#ff7800",
                        color: "#000",
                        weight: 1,
                        opacity: 1,
                        fillOpacity: 0.8

                    });
                }
            })
            map.addLayer(myLayer);
            map.fitBounds(myLayer);
        }


    )

}

function scaledRadius(value) {
    var scaledRadius = 0
    if (1 == value) {
        scaledRadius = 5;
    } else if (5 >= value && value >= 2) {
        scaledRadius = 8
    } else if (10 >= value && value >= 6) {
        scaledRadius = 11;
    } else if (20 >= value && value >= 10) {
        scaledRadius = 14
    } else if (value >= 20) {
        scaledRadius = 18
    }
    return scaledRadius
}

$(function() {
    $("#team").autocomplete({

        source: Object.keys(teams),
        select: function(event, ui) {

          addTeam(ui.item.label)
        }
    }).data("ui-autocomplete")._renderItem = function(ul, item) {
        return $("<li>")
            .data("ui-autocomplete-item", item)
            .append("<a>" + item.label + "</a>")
            .appendTo(ul);

    };

});

//Make sure that we wait for the page (and it to know about the map div) before we call leaflet
$(function() {

    addTeam("All NHL Players");

    map = new L.Map('map', {
        layers: [Esri_WorldGrayCanvas]
    });

  
});
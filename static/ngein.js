var extent = [-285401.92,22598.08,595401.9199999999,903401.9199999999];
var resolutions = [3440.640, 1720.320, 860.160, 430.080, 215.040, 107.520, 53.760, 26.880, 13.440, 6.720, 3.360, 1.680, 0.840, 0.420, 0.210, 0.105, 0.0525];
var projection = new ol.proj.Projection({code:'EPSG:28992', units:'m', extent: extent});

var url = 'http://geodata.nationaalgeoregister.nl/tms/1.0.0/brtachtergrondkaart/';
var url = 'http://' + location.hostname + '/mapproxy/tms/1.0.0/basisluchtfoto/EPSG28992/';
//var url = 'http://' + location.hostname + '/mapproxy/tms/1.0.0/basistopo/EPSG28992/';

var tileUrlFunction = function(tileCoord, pixelRatio, projection) {
  var zxy = tileCoord;
  if (zxy[1] < 0 || zxy[2] < 0) {
    return "";
  }
  return url +
    zxy[0].toString()+'/'+ zxy[1].toString() +'/'+
    zxy[2].toString() +'.png';
};


var source = new ol.source.Vector({
    url: 'static/foo.json',
    format: new ol.format.GeoJSON()
});

var draw = new ol.interaction.Draw({
    source: source,
    type: 'Polygon'
});
draw.on('drawend', function(evt){
  var feature = evt.feature;
  //var p = feature.getGeometry();
  //console.log(p.getCoordinates());
  var format = new ol.format.WKT();
  var wkt = format.writeFeature(feature)
  console.log(wkt)
  $('#coords').val(wkt);
});

var map = new ol.Map({
  interactions: ol.interaction.defaults().extend([draw]),
  target: 'map',
  layers:  [
    new ol.layer.Tile({
      source: new ol.source.TileImage({
        attributions: [
          new ol.Attribution({
            html: 'Kaartgegevens: © <a href="http://www.cbs.nl">CBS</a>, <a href="http://www.kadaster.nl">Kadaster</a>, <a href="http://openstreetmap.org">OpenStreetMap</a><span class="printhide">-auteurs (<a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>).</span>'
          })
        ],
        projection: projection,
        tileGrid: new ol.tilegrid.TileGrid({
          origin: [-285401.92,22598.08],
          resolutions: resolutions
        }),
        tileUrlFunction: tileUrlFunction
      })
    })
    
    ,
    new ol.layer.Vector({
        title: 'Draw',
        source: source,
        projection: projection,
        style: new ol.style.Style({
          image: new ol.style.Circle({
            radius: 5,
            fill: new ol.style.Fill({
              color: '#0000FF'
            }),
            stroke: new ol.style.Stroke({
              color: '#000000'
            })
          })
        })
    })
    
  ],
  view: new ol.View({
    minZoom: 3,
    maxZoom: 16,
    projection: projection,
    center: [135000, 450000],
    zoom: 9
  })
});


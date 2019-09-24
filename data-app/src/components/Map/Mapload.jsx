import React from 'react';
import MapboxGL from 'mapbox-gl';
import MapboxDraw from '@mapbox/mapbox-gl-draw';
import RulerControl from 'mapbox-gl-controls/lib/ruler';
import StylesControl from 'mapbox-gl-controls/lib/styles';
import CompassControl from 'mapbox-gl-controls/lib/compass';
import ZoomControl from 'mapbox-gl-controls/lib/zoom';
import Area from '@turf/area';
import Centroid from '@turf/centroid';
import MapboxGeocoder from "@mapbox/mapbox-gl-geocoder";
import { FormGroup, Label, Input } from "reactstrap";
import { polygons } from '@turf/helpers';

var map;
var draw;
var polygonList = '';
var mapLayer = 'main-layer';
var mapSource = 'main-source';
MapboxGL.accessToken = 'pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4M29iazA2Z2gycXA4N2pmbDZmangifQ.-g_vE53SD2WrJ6tFX7QHmA';

let geo_json;
var countCreate = "0";
let coordinates_value;

export default class Mapload extends React.Component {
  constructor(props) {
    super(props)
    this.state = {
      lng: 133.8920,
      lat: -25.0195,
      zoom: 3.4,
    }

    this.drawPolygon = this.drawPolygon.bind(this);
    this.createArea = this.createArea.bind(this);
    this.updateArea = this.updateArea.bind(this);
    this.polygonDataCalc = this.polygonDataCalc.bind(this);
  }

  componentDidMount() {
    // global variables
    let { lat, lng, zoom } = this.state;

    // trying to access clinet's coordinates. pop up will appear asking for permission 
    if ("geolocation" in navigator) {
      navigator.geolocation.getCurrentPosition(position => {
        lng = position.coords.longitude;
        lat = position.coords.latitude;
        zoom = 14
      });
    }

    // load the default map
    map = new MapboxGL.Map({
      container: this.mapDiv,
      style: 'mapbox://styles/mapbox/streets-v10?optimize=true',
      center: [lng, lat],
      zoom: zoom,
      attributionControl: false
    });

    map.on('draw.create', this.createArea);
    map.on('draw.delete', this.deleteArea);
    map.on('draw.update', this.updateArea);

    this.addControls();
    this.layeringMap("load");
    this.fixAlignments();
  }

  addControls() {
    // enable street view and satellite view
    map.addControl(new StylesControl(), 'top-left');
    // enbale mapbox draw controls (draw polygon, trash)
    draw = new MapboxDraw({
      displayControlsDefault: false,
      controls: {
        polygon: true,
        trash: true
      }
    });
    map.addControl(draw, 'top-left');
    // enbale map search box
    map.addControl(new MapboxGeocoder({
      accessToken: MapboxGL.accessToken,
      mapboxgl: map
    }));
    // enable get current location control
    map.addControl(new MapboxGL.GeolocateControl({
      positionOptions: {
        enableHighAccuracy: true
      },
      trackUserLocation: true
    }));
    // enable zoom control 
    map.addControl(new ZoomControl(), 'top-right');
    // enable compass control
    map.addControl(new CompassControl(), 'top-right');
  }

  layeringMap(e) {
    map.on(e, function () {
      map.addLayer({
        "id": "simple-tiles",
        "type": "raster",
        "source": {
          "type": "raster",
          "tiles": ["https://tile.openweathermap.org/map/temp_new/{z}/{x}/{y}.png?appid=874718354841f0e0250b4b06a05a971e"],
          "tileSize": 256
        },
        "minzoom": 0,
        "maxzoom": 22
      });
    });
  }

  // fix css issue with width when loading the map 
  fixAlignments() {
    map.on('load', function () {
      var mapCanvas = document.getElementsByClassName('mapboxgl-canvas')[0];
      mapCanvas.style.width = '100%';
    });
  }

  // add polygon layer  
  drawPolygon(points) {
    console.log("LOG: (points without stringify)", points[0]);
    console.log("LOG: (points)", JSON.stringify(points[0]));

    if (map.getLayer(mapLayer)) {
      // if layer exists remove map layer & source.
      map.removeLayer(mapLayer).removeSource(mapSource);
      // if this is not the first polygon add the new polygon with a comma
      polygonList += ',';
    }

    // create feature list with an unique id for GEOJSON
    polygonList = polygonList +
      '{' +
      '"type": "Feature",' +
      '"id": "feature' + countCreate + '",' +
      '"geometry": {' +
      '"type": "Point",' +
      '"coordinates":' + JSON.stringify(points) +
      '}' +
      '}';
    console.log("LOG: (polygonList)", polygonList);

    // create above feature list to feature collection for GEOJSON
    var polygonSource = '{' +
      '"type": "geojson",' +
      '"data": {' +
      '"type": "FeatureCollection",' +
      '"features": [' + polygonList + ']' +
      '}}';
    console.log("LOG: (polygonSource)", polygonSource);

    // GEOJSON structure/ layer
    var polygonLayer =
      '{"id": "' + mapLayer + '",' +
      '"type": "fill",' +
      '"source": "' + mapSource + '",' +
      '"paint": {' +
      '   "fill-color": "#088",' +
      '   "fill-opacity": 0.3' +
      '}}';
    console.log("LOG: (polygonLayer)", polygonLayer);

    // convert string to JSON
    var objPolygonSource = JSON.parse(polygonSource);
    var objPolygonLayer = JSON.parse(polygonLayer);
    console.log("LOG: (objPolygonSource)", objPolygonSource);
    console.log("LOG: (objPolygonLayer)", objPolygonLayer);

    // add source layer to map
    map.addSource(mapSource, objPolygonSource);
    // add main layer to map
    map.addLayer(objPolygonLayer);
  }

  // TODO
  deleteFeature(geoJSON, id) {
    var path = 'source,data,type,features,id';
    for (var i = 0; i < path.length - 1; i++) {
      geoJSON = geoJSON[path[i]];
      console.log("LOG: (geoJSON)", geoJSON);
      if (typeof geoJSON === 'undefined') {
        return;
      }
    }
    //delete geoJSON[path.pop()];
  }

  createArea(e) {
    let data = draw.getAll();
    console.log("LOG: (data)", data);
    const polygonCoordinates = data.features[countCreate].geometry.coordinates;
    this.drawPolygon(polygonCoordinates);
    this.polygonDataCalc(data);
    countCreate = (parseInt(countCreate) + 1).toString(10);
    console.log("LOG: (polygonCountCreate)", countCreate);
  }

  updateArea(e) {
    let data = draw.getAll();
    // map.removeLayer(mapLayer).removeSource(mapSource);
    countCreate = (parseInt(countCreate) - 1).toString(10);
    const polygonData = data.features[0].geometry.coordinates;
    this.drawPolygon(polygonData);
    this.polygonDataCalc(data);
    countCreate = (parseInt(countCreate) + 1).toString(10);
  }

  deleteArea(e) {

    // map.removeLayer(mapLayer).removeSource(mapSource);
    // console.log(document.getElementById(countCreate));
    // document.getElementById(countCreate).innerHTML = "";
    countCreate = (parseInt(countCreate) - 1).toString(10);
  }

  polygonDataCalc(data) {
    if (data.features.length > 0) {
      let area = Area(data);
      let centroid = Centroid(data);
      let rounded_area = Math.round(area * 100) / 100;
      console.log("Data Featres ", data.features["0"])
      console.log("Geometry ", data.features["0"].geometry);
      coordinates_value = data.features[countCreate].geometry.coordinates["0"];
      // console.log(data.features["0"].geometry.coordinates["0"]["0"]);
      // console.log(coordinates_value);
      // let coordinates_value_json = JSON.stringify(coordinates_value, undefined, 4);
      console.log(coordinates_value)
      geo_json = {
        Feature: data.features[countCreate].geometry.type,
        Coordinates: coordinates_value,
        Centroid: centroid.geometry.coordinates,
        Area: rounded_area + "sq.m"
        // coordinates:{coordinates1:coordinates_value[0],coordinates2:coordinates_value[1],coordinates3:coordinates_value[2]}
        // coordinates:coordinates_value[0],
        // coordinates2:coordinates_value[1],
        // coordinates3:coordinates_value[2]
      }
      console.log(JSON.stringify(geo_json))

      let geo_json_stringified = JSON.stringify(geo_json, undefined, 2)
      // this.polygonDiv.innerHTML = '<p><b><strong>Area: ' + rounded_area + ' square meter</strong></b></p><p><b><strong>Centroid: '+
      //     centroid.geometry.coordinates+' </strong></b></p>'+lat_val;
      let geo_json_readable = this.syntaxHighlight(geo_json_stringified);
      console.log(typeof (geo_json_readable));
      // this.polygonDiv.innerHTML =+ '<pre>'+geo_json_readable+'</pre>';
      var pre_tag = document.createElement("PRE");
      pre_tag.id = countCreate;
      var t = document.createTextNode(geo_json_stringified);
      pre_tag.appendChild(t);
      document.getElementById("calculated-area").appendChild(pre_tag);
      // this.polygonDiv.innerHTML = coordinates_value_json[2];
      // this.polygonDiv.innerHTML = '<JSONPretty id = "json-pretty"'
      // this.polygonDiv.innerHTML = '<JSONPretty data = { geo_json }></JSONPretty>'
      // console.log(trackUserLocation);
      // document.write(lat_val);
    }
    else {
      console.log("Drawn Area not fetched");
    }
  }

  syntaxHighlight(json) {
    json = json.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
    return json.replace(/("(\\u[a-zA-Z0-9]{4}|\\[^u]|[^\\"])*"(\s*:)?|\b(true|false|null)\b|-?\d+(?:\.\d*)?(?:[eE][+-]?\d+)?)/g, function (match) {
      var cls = 'number';
      if (/^"/.test(match)) {
        if (/:$/.test(match)) {
          cls = 'key';
        } else {
          cls = 'string';
        }
      } else if (/true|false/.test(match)) {
        cls = 'boolean';
      } else if (/null/.test(match)) {
        cls = 'null';
      }
      return '<span class="' + cls + '">' + match + '</span>';
    });
  }

  render() {
    return (
      <div>
        <div ref={e => this.mapDiv = e} className="map"></div>
        <div id='calculated-area' ref={el => this.polygonDiv = el}>
        </div>
      </div>
    )
  }
}

import React from 'react';
import MapboxGL from 'mapbox-gl';
import MapboxDraw from '@mapbox/mapbox-gl-draw';
import StylesControl from 'mapbox-gl-controls/lib/styles';
import CompassControl from 'mapbox-gl-controls/lib/compass';
import ZoomControl from 'mapbox-gl-controls/lib/zoom';
import Area from '@turf/area';
import Centroid from '@turf/centroid';
import MapboxGeocoder from "@mapbox/mapbox-gl-geocoder";

var map;
var draw;
var polygonList = '';
var mapLayer = 'main-layer';
var mapSource = 'main-source';
MapboxGL.accessToken = 'pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4M29iazA2Z2gycXA4N2pmbDZmangifQ.-g_vE53SD2WrJ6tFX7QHmA';

let geoJSON;
var countCreate = "0";

export default class Mapload extends React.Component {
  constructor(props) {
    super(props)
    this.state = {
      lng: 133.8920,
      lat: -25.7505,
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
    this.mapLayer("load");
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

  mapLayer(e) {
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

  // fix css issue of width when loading the map 
  fixAlignments() {
    map.on('load', function () {
      var mapCanvas = document.getElementsByClassName('mapboxgl-canvas')[0];
      mapCanvas.style.width = '100%';
    });
  }

  // add polygon layer  
  drawPolygon(points) {
    console.log("LOG: drawPolygon(points without stringify)", points[0]);
    console.log("LOG: drawPolygon(points)", JSON.stringify(points[0]));

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
    console.log("LOG: drawPolygon(polygonList)", polygonList);

    // create above feature list to feature collection for GEOJSON
    var polygonSource = '{' +
      '"type": "geojson",' +
      '"data": {' +
      '"type": "FeatureCollection",' +
      '"features": [' + polygonList + ']' +
      '}}';
    console.log("LOG: drawPolygon(polygonSource)", polygonSource);

    // GEOJSON structure/ layer
    var polygonLayer =
      '{"id": "' + mapLayer + '",' +
      '"type": "fill",' +
      '"source": "' + mapSource + '",' +
      '"paint": {' +
      '   "fill-color": "#088",' +
      '   "fill-opacity": 0.3' +
      '}}';
    console.log("LOG: drawPolygon(polygonLayer)", polygonLayer);

    // convert string to JSON
    var objPolygonSource = JSON.parse(polygonSource);
    var objPolygonLayer = JSON.parse(polygonLayer);
    console.log("LOG: drawPolygon(objPolygonSource)", objPolygonSource);
    console.log("LOG: drawPolygon(objPolygonLayer)", objPolygonLayer);

    // add source layer to map
    map.addSource(mapSource, objPolygonSource);
    // add main layer to map
    map.addLayer(objPolygonLayer);
  }

  polygonDataCalc(data) {
    if (data.features.length > 0) {
      let area = Area(data);
      let centroid = Centroid(data);
      let roundedArea = Math.round(area * 100) / 100;
      let featureType = data.features[countCreate].geometry.type;
      let coordinatesValue = data.features[countCreate].geometry.coordinates["0"];
      console.log("LOG: polygonDataCalc(data featres)", data.features["0"])
      console.log("LOG: polygonDataCalc(geometry)", data.features["0"].geometry);
      console.log("LOG: polygonDataCalc(coordinatesValue)", coordinatesValue)
      geoJSON = {
        feature: featureType,
        coordinates: coordinatesValue,
        centroid: centroid.geometry.coordinates,
        area: roundedArea + " sq.m"
      }
      console.log("LOG: polygonDataCalc(geoJSON)", JSON.stringify(geoJSON))
      let geoJSONStringified = JSON.stringify(geoJSON, undefined, 2)
      let geoJSONReadable = this.syntaxHighlight(geoJSONStringified);
      var preTag = document.createElement("pre");
      var geoJSONTag = document.createTextNode(geoJSONStringified);
      preTag.id = countCreate;
      preTag.appendChild(geoJSONTag);
      document.getElementById("geoJASON").appendChild(preTag);
    } else {
      console.log("LOG: error(drawn area not fetched)");
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

  // TODO
  deleteFeature(geoJSON, id) {
    var path = 'source,data,type,features,id';
    for (var i = 0; i < path.length - 1; i++) {
      geoJSON = geoJSON[path[i]];
      console.log("LOG: deleteFeature(geoJSON)", geoJSON);
      if (typeof geoJSON === 'undefined') {
        return;
      }
    }
    //delete geoJSON[path.pop()];
  }

  createArea(e) {
    let data = draw.getAll();
    console.log("LOG: createArea(data)", data);
    const polygonCoordinates = data.features[countCreate].geometry.coordinates;
    this.drawPolygon(polygonCoordinates);
    this.polygonDataCalc(data);
    countCreate = (parseInt(countCreate) + 1).toString(10);
    console.log("LOG: createArea(polygonCountCreate)", countCreate);
  }

  updateArea(e) {
    // TODO data.action 'change_coordinates', 'move'
    let data = draw.getAll();
    console.log("LOG: updateArea(data)", data);
    countCreate = (parseInt(countCreate) - 1).toString(10);
    const polygonData = data.features[0].geometry.coordinates;
    this.drawPolygon(polygonData);
    this.polygonDataCalc(data);
    countCreate = (parseInt(countCreate) + 1).toString(10);
  }

  deleteArea(e) {
    let data = draw.getAll();
    console.log("LOG: deleteArea(data)", data);
    const polygonData = data.features[0];
    countCreate = (parseInt(countCreate) - 1).toString(10);
  }

  render() {
    return (
      <div>
        <div ref={e => this.mapDiv = e} className="map"></div>
        <div id='geoJASON' ref={el => this.polygonDiv = el}>
        </div>
      </div>
    )
  }
}

import React from 'react';
import mapboxgl from 'mapbox-gl';
import MapboxDraw from '@mapbox/mapbox-gl-draw';
import turf from '@turf/turf';
import ReactDOM from 'react-dom';
import area_cal from '@turf/area';
import centroid_cal from '@turf/centroid';
import MapboxGeocoder from "@mapbox/mapbox-gl-geocoder";
import JSONPretty from 'react-json-pretty';

var map;
var draw;
let geo_json;
var count_create = "0";
mapboxgl.accessToken = 'pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4M29iazA2Z2gycXA4N2pmbDZmangifQ.-g_vE53SD2WrJ6tFX7QHmA';
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
    // this.showPolygonData = this.showPolygonData.bind(this);
    this.polygonDataCalc = this.polygonDataCalc.bind(this);
    this.syntaxHighlight = this.syntaxHighlight.bind(this);
}
  
    componentDidMount() {
        const { lat, lng, zoom } = this.state;
        map = new mapboxgl.Map({
            container: this.mapDiv,
            style: 'mapbox://styles/mapbox/streets-v9',
            center: [lng, lat],
            zoom: zoom
        });
        
        draw = new MapboxDraw({
            displayControlsDefault: true,
            // controls: {
            //     polygon: true,
            //     trash: true
            // }
        });
        
       map.addControl(draw);

       map.addControl(new MapboxGeocoder({
       accessToken: mapboxgl.accessToken,
       mapboxgl: map
       })); 


       map.addControl(new mapboxgl.GeolocateControl({
        positionOptions: {
        enableHighAccuracy: true
        },
        trackUserLocation: true
        }));
       
       map.on('draw.create', this.createArea);
       map.on('draw.delete', this.deleteArea);
       map.on('draw.update', this.updateArea);


       map.on('load', function(){
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
   
   drawPolygon(points) {
        map.addLayer({
            'id': 'maine',
            'type': 'fill',
            'source': {
                'type': 'geojson',
                'data': {
                    'type': 'Feature',
                    'geometry': {
                        'type': 'Polygon',
                        'coordinates': points
                    }
                }
            },
            'layout': {},
            'paint': {
                'fill-color': '#088',
                'fill-opacity': 0.3
            }
        });
    }
    
     createArea(e) {
          let data = draw.getAll();
          console.log(data);
           // if(count_create>0){
           //   map.removeLayer('maine').removeSource('maine');
           // }
           // console.log(toString(count_create));
            const polygonData = data.features[count_create].geometry.coordinates;
          console.log("polygonData"+data);
          this.drawPolygon(polygonData);
          // } 
          // else{
          //             const polygonData = data.features[0].geometry.coordinates;
          // console.log("polygonData"+polygonData);
          // this.drawPolygon(polygonData);
          // }  

          
          this.polygonDataCalc(data);
          count_create = (parseInt(count_create)+1).toString(10);
          console.log(count_create);

         
    }
    syntaxHighlight(json){
            json = json.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
            return json.replace(/("(\\u[a-zA-Z0-9]{4}|\\[^u]|[^\\"])*"(\s*:)?|\b(true|false|null)\b|-?\d+(?:\.\d*)?(?:[eE][+\-]?\d+)?)/g, function (match) {
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
    polygonDataCalc(data){
      if(data.features.length > 0){
        let area = area_cal(data);
        // console.log(data);
        let centroid = centroid_cal(data);
        let rounded_area = Math.round(area*100)/100;
        console.log(data.features["0"].geometry);
        let coordinates_value = data.features[count_create].geometry.coordinates["0"];
        // console.log(data.features["0"].geometry.coordinates["0"]["0"]);
        // console.log(coordinates_value);
        // let coordinates_value_json = JSON.stringify(coordinates_value, undefined, 4);
        console.log(coordinates_value)
        geo_json = {
          Feature: "Polygon",
          Coordinates: coordinates_value,
          Centroid: centroid.geometry.coordinates,
          Area: rounded_area+"sq.m"
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
        console.log(typeof(geo_json_readable));
        // this.polygonDiv.innerHTML =+ '<pre>'+geo_json_readable+'</pre>';
        var pre_tag = document.createElement("PRE");
        var t = document.createTextNode(geo_json_stringified);
        pre_tag.appendChild(t);
        document.getElementById("calculated-area").appendChild(pre_tag);  
        // this.polygonDiv.innerHTML = coordinates_value_json[2];
        // this.polygonDiv.innerHTML = '<JSONPretty id = "json-pretty"'
        // this.polygonDiv.innerHTML = '<JSONPretty data = { geo_json }></JSONPretty>'
        // console.log(trackUserLocation);
        // document.write(lat_val);
      }
      else{
        console.log("Drawn Area not fetched");
      }
    }
    
    deleteArea(e) {
         let data = draw.getAll();
         map.removeLayer('maine').removeSource('maine');
    }
updateArea(e) {
          let data = draw.getAll();
          map.removeLayer('maine').removeSource('maine');
          const polygonData = data.features[0].geometry.coordinates;
          this.drawPolygon(polygonData);
          this.polygonDataCalc(data);
    }
  
  render() {
    return (
      <div>
        <div ref={e => this.mapDiv = e} className="map"></div>
        <div className='calculation-box'>
          <div id='calculated-area' ref={el => this.polygonDiv = el}>
          </div>
        </div>
      </div>
    )
  }
}
ReactDOM.render(<Mapload />, document.querySelector("#root"))
// export default Mapload;

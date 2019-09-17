import React from 'react';
import mapboxgl from 'mapbox-gl';
import MapboxDraw from '@mapbox/mapbox-gl-draw';
import turf from '@turf/turf';
import ReactDOM from 'react-dom';
import area_cal from '@turf/area';
import centroid_cal from '@turf/centroid'
import MapboxGeocoder from "@mapbox/mapbox-gl-geocoder"


var map;
var draw;
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
            displayControlsDefault: false,
            controls: {
                polygon: true,
                trash: true
            }
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
          const polygonData = data.features[0].geometry.coordinates;
          this.drawPolygon(polygonData);
          this.polygonDataCalc(data);
    }
    
    polygonDataCalc(data){
      if(data.features.length > 0){
        let area = area_cal(data);
        // console.log(data);
        let centroid = centroid_cal(data);
        let rounded_area = Math.round(area*100)/100;
        let lat_val = data.features["0"].geometry.coordinates["0"];
        console.log(lat_val);
        this.polygonDiv.innerHTML = '<p><b><strong>Area: ' + rounded_area + ' square meter</strong></b></p><p><b><strong>Centroid: '+
            centroid.geometry.coordinates+' </strong></b></p>'+lat_val;
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
          <div id='calculated-area' ref={el => this.polygonDiv = el}></div>
        </div>
      </div>
    )
  }
}
ReactDOM.render(<Mapload />, document.querySelector("#root"))
// export default Mapload;

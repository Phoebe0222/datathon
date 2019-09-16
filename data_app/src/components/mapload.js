import React from 'react';
import mapboxgl from 'mapbox-gl';
import MapboxDraw from '@mapbox/mapbox-gl-draw';
import turf from '@turf/turf';
import ReactDOM from 'react-dom';
import area_cal from '@turf/area';
import centroid_cal from '@turf/centroid'
var map;
var draw;
mapboxgl.accessToken = 'pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4M29iazA2Z2gycXA4N2pmbDZmangifQ.-g_vE53SD2WrJ6tFX7QHmA';
export default class Mapload extends React.Component {
  constructor(props) {
    super(props)
    this.state = {
      lat: 27.85380233830591,
      lng: 78.37183893820759,
      zoom: 8.5,
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
        let centroid = centroid_cal(data);
        let rounded_area = Math.round(area*100)/100;
        this.polygonDiv.innerHTML = '<p><strong>Area: ' + rounded_area + ' square meter</strong></p><h4>Centroid: <br />'+
            centroid.geometry.coordinates+'</h4>';
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
document.addEventListener('DOMContentLoaded', function () {
    map_center = [14.273, 53.89]
    const map = new ol.Map({
        target: 'map',
        layers: [
            new ol.layer.Tile({
                source: new ol.source.XYZ({
                    minZoom: 0,
                    maxZoom: 22,
                    url: 'https://tile.openstreetmap.de/{z}/{x}/{y}.png',
                    attributions: '© <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
                    tileSize: [256, 256],
                }),
                name: 'base'
            })
        ],
        view: new ol.View({
            center: ol.proj.fromLonLat(map_center),
            zoom: 18,
        }),
        controls: [] // Empty array to remove default controls
    });

    openSeaMapLayer = new ol.layer.Tile({
        title: 'Open Sea Map',
        visible: true,
        source: new ol.source.XYZ({
            //attributions: '&copy;SeaTerra GmbH',
            minZoom: 0,
            maxZoom: 22,
            attributions: '© <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
            url: 'http://tiles.openseamap.org/seamark/{z}/{x}/{y}.png',
            tileSize: [256, 256],
        }),
        visible: true,
        name: 'osm'
    });
    map.addLayer(openSeaMapLayer);

    tmiLayer = new ol.layer.Tile({
        title: '20230710-MAG.tif',
        source: new ol.source.XYZ({
            attributions: '&copy;SeaTerra GmbH',
            minZoom: 0,
            maxZoom: 20,
            url: GEODATA_URL + PROJECT_NAME +'/geodata/tiles/tmi/{z}/{x}/{-y}.png',
            tileSize: [256, 256]
        }),
        visible: true,
        name: 'tmi'
    });
    map.addLayer(tmiLayer);

    mbesLayer = new ol.layer.Tile({
        title: '20230710-MBES.tif',
        source: new ol.source.XYZ({
            attributions: '&copy;SeaTerra GmbH',
            minZoom: 0,
            maxZoom: 18,
            url: GEODATA_URL + PROJECT_NAME +'/geodata/tiles/mbes/{z}/{x}/{-y}.png',
            tileSize: [256, 256]
        }),
        visible: false,
        name: 'mbes'
    });
    map.addLayer(mbesLayer);

    sssLayer = new ol.layer.Tile({
        title: '20230710-SSS.tif',
        visible: false,
        source: new ol.source.XYZ({
            attributions: '&copy;SeaTerra GmbH',
            minZoom: 0,
            maxZoom: 18,
            url: GEODATA_URL + PROJECT_NAME +'/geodata/tiles/sss/{z}/{x}/{-y}.png',
            tileSize: [256, 256]
        }),
        name: 'sss',
    });
    map.addLayer(sssLayer);

    /*const geotiffLayer = new ol.layer.Tile({
        title: 'GeoTIFF Layer',
        source: new ol.source.GeoTIFF({
            sources: [
                {
                  url: GEODATA_URL + PROJECT_NAME +'/geodata/tiff/projected_geotiff.tif',
                  //overviews: ['https://openlayers.org/data/raster/no-overviews.tif.ovr'],
                },
            ],
        }),
        minZoom: 0,
        maxZoom: 18,
        //projection: map.getView().getProjection(),
        imageExtent: [5451190, 5973197, 5452632, 5974009],
        visible: true,
        name: 'geotiff'
    });
    map.addLayer(geotiffLayer);
    console.log(geotiffLayer.getProperties());*/

    epsg_string = 'EPSG:'+EPSG
    utm_zone = '32'

    //proj4.defs(epsg_string, '+proj=utm +zone=' + utm_zone + '+ellps=GRS80 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs');
    //proj4.defs(epsg_string,"+proj=somerc +lat_0=46.95240555555556 +lon_0=7.439583333333333 +k_0=1 +x_0=600000 +y_0=200000 +ellps=bessel +towgs84=660.077,13.551,369.344,2.484,1.783,2.939,5.66 +units=m +no_defs");
    /*Polish projects with EPSG 2176: */proj4.defs(epsg_string,"+proj=tmerc +lat_0=0 +lon_0=15 +k_0=0.999923 +x_0=5500000 +y_0=0 +ellps=GRS +towgs84=0,0,0,0,0,0,0 +units=m +no_defs");
    /*Polish projects with EPSG 2180: *///proj4.defs(epsg_string,"+proj=tmerc +lat_0=0 +lon_0=19 +k_0=0.9993 +x_0=500000 +y_0=-5300000 +ellps=GRS +towgs84=0,0,0,0,0,0,0 +units=m +no_defs");
    
    ol.proj.proj4.register(proj4);

    var labelstyle = new ol.style.Style({
        stroke: new ol.style.Stroke({
            color: 'red',
            width: 3
        }),
        text: new ol.style.Text({
            font: '12px Calibri,sans-serif',
            fill: new ol.style.Fill({
                color: '#000'
            }),
        })
    });
    var labelstyle2 = new ol.style.Style({
        stroke: new ol.style.Stroke({
            color: 'red',
            width: 3
        }),
        text: new ol.style.Text({
            font: '12px Calibri,sans-serif',
            fill: new ol.style.Fill({
                color: '#000'
            }),
        })
    });
    var overlaystyle = new ol.style.Style({
        stroke: new ol.style.Stroke({color: 'black'}),
        fill: new ol.style.Fill({color: 'rgba(0, 0, 0, 0.2)'})
    });

    const overlayLayer = new ol.layer.Vector({
        source: new ol.source.Vector({
            url: GEODATA_URL + PROJECT_NAME +'/geodata/vector/overlay.geojson',
            //url: '/static/geodata/vector/overlay.geojson',
            format: new ol.format.GeoJSON(),
        }),
        title: 'Overlay.DXF',
        style: function(feature, resolution) {
            if(feature.get('Text')){
                labelstyle.getText().setText(feature.get('Text'));
                return labelstyle;
            }else{
                return overlaystyle;
            }
        },
        visible: true,
        name: 'overlay'
    });
    map.addLayer(overlayLayer);

    const textsLayer = new ol.layer.Vector({
        source: new ol.source.Vector({
            url: GEODATA_URL + PROJECT_NAME +'/geodata/vector/texts.geojson',
            format: new ol.format.GeoJSON(),
        }),
        title: 'Labels',
        style: function(feature) {
            labelstyle.getText().setText(feature.get('text'));
            return labelstyle;
        },
        visible: true,
        name: 'texts'
    });
    map.addLayer(textsLayer);

    const vectorSource = new ol.source.Vector();
    const vectorLayer = new ol.layer.Vector({
        source: vectorSource,
    });
    map.addLayer(vectorLayer);

    itpLayer = new ol.layer.Vector({
        source: new ol.source.Cluster({
            distance: 0,
            source: new ol.source.Vector({
                url: '/mtlitems',
                format: new ol.format.GeoJSON(),
            }),
        }),
        title: 'ItpLayer',
        style: itp_styleFunction,
        name: 'itp',
    });
    map.addLayer(itpLayer);

    vesselLayer = new ol.layer.Vector({
        source: new ol.source.Vector({
            url: '/vesselitems',
            format: new ol.format.GeoJSON(),
        }),
        title: 'Vessel Layer',
        name: 'vessel',
        style: vessel_styleFunction,
    });
    map.addLayer(vesselLayer);

    const popupContainer = document.getElementById('itp_overlay');
    /*const popupOverlay = new ol.Overlay({
        element: popupContainer,
        autoPan: true,
        autoPanAnimation: {
            duration: 250,
        },
    });
    map.addOverlay(popupOverlay);*/
    popupContainer.style.display = 'none';

    const closePopupButton = popupContainer.querySelector('.close-button');
    const currentImage = popupContainer.querySelector('.current-image');
    const leftArrow = popupContainer.querySelector('.left-arrow');
    const rightArrow = popupContainer.querySelector('.right-arrow');

    if (closePopupButton) {
        closePopupButton.addEventListener('click', closePopup);
    }

    let currentimgIndex = 0;

    // Function to update the current image
    function updateImage() {
        currentImage.src = imageSources[currentimgIndex];
    }

    // Event listener for left arrow click
    leftArrow.addEventListener('click', function () {
        //var img = new Image();
        //img.src = imageSources[(currentimgIndex - 1 + imageSources.length) % imageSources.length];
        //if(img.height!=0){
        currentimgIndex = (currentimgIndex - 1 + imageSources.length) % imageSources.length;
        updateImage();
        //}
    });

    // Event listener for right arrow click
    rightArrow.addEventListener('click', function () {
        //var img = new Image();
        //img.src = imageSources[(currentimgIndex + 1) % imageSources.length];
        //if(img.height!=0){
        currentimgIndex = (currentimgIndex + 1) % imageSources.length;
        updateImage();
        //}
    });

    function closePopup() {
        //popupOverlay.setPosition(undefined); // Hide the popup
        popupContainer.style.display = 'none';
        selectInteraction.getFeatures().clear();
    }

    const selectInteraction = new ol.interaction.Select({
        //style: itp_selected_styleFunction,
        layers: [itpLayer]
    });

    function fetchSecureURL(blobName) {
    return fetch(`/get-sas-token/?blob_name=${blobName}`)
        .then(response => response.json())
        .then(data => {
            if (data.url) {
                return fetch(data.url, { method: 'HEAD' })
                    .then(headResponse => {
                        if (headResponse.ok) {
                            return data.url;
                        } else {
                            throw new Error('Blob does not exist');
                        }
                    });
            } else {
                throw new Error('Failed to fetch image URL');
            }
        });
    }

    function selectFeature(feature) {
        currentimgIndex = 0;
        //const feature = e.selected[0];
        if (feature && feature.get('itp_no_mag')) {
            const coordinates = feature.getGeometry().getCoordinates();
            var img_pre = PROJECT_NAME +'/media/mtlimages/'+feature.get('itp_no_mag');
            
            fetch(`/get-image-sources/?itp_no_mag=${feature.get('itp_no_mag')}`)
            .then(response => response.json())
            .then(data => {
                if (data.image_sources) {
                    imageSources = data.image_sources;
                } else {
                    imageSources = ['/static/img/no_img.jpg'];
                }
                updateImage();
            });

            document.getElementById('popup_title').innerText = feature.get('itp_no_mag');
            //document.getElementById('info_coordinates').innerText = "Coordinates : "+feature.get('easting')+" E "+feature.get('northing')+" N";
            document.getElementById('info_easting').innerText = "Eastings : "+feature.get('easting')+" E";
            document.getElementById('info_northing').innerText = "Northings : "+feature.get('northing')+" N";
            document.getElementById('info_modelDepth').innerText = document.getElementById('info_modelDepth').title+" "+feature.get('model_depth_geoid');
            document.getElementById('info_waterDepth').innerText = document.getElementById('info_waterDepth').title+" "+feature.get('water_depth_geoid');
            document.getElementById('info_depthBelowGround').innerText = document.getElementById('info_depthBelowGround').title+" "+feature.get('model_depth_below_ground');
            document.getElementById('info_magMoment').innerText = "Mag moment : "+feature.get('mag_moment');
            document.getElementById('info_clearDate').innerText = "Clearance date : "+feature.get('cl_date');
            document.getElementById('info_ship').innerText = "Vessel : "+feature.get('vessel');
            document.getElementById('info_EOD').innerText = "EOD : "+feature.get('eod');

            document.getElementById('found-dropdown').value = feature.get('found');
            document.getElementById('recovered-dropdown').value = feature.get('salvaged');
            document.getElementById('uxo-dropdown').value = feature.get('uxo');
            document.getElementById('clear-dropdown').value = feature.get('clear');
            document.getElementById('qa-clear-dropdown').value = feature.get('qa_clear');
            document.getElementById('todo-dropdown').value = feature.get('todo_target');

            document.getElementById('weight').value = feature.get('cl_weight');
            document.getElementById('width').value = feature.get('cl_width');
            document.getElementById('length').value = feature.get('cl_length');

            document.getElementById('tr-comment').value = feature.get('tr_comment');
            document.getElementById('description-detail').value = feature.get('description_detail');

            document.getElementById('itp_no_mag').value = feature.get('itp_no_mag');

            // Set the offset property in the overlay configuration
            //popupOverlay.setPosition(coordinates);
            //const popupOffset = [-(popupContainer.offsetWidth / 2), -(popupContainer.offsetHeight / 2)];
            //popupOverlay.setOffset(popupOffset);

            pixel = map.getPixelFromCoordinate(coordinates);
            mapRect = map.getTargetElement().getBoundingClientRect();

            popupContainer.style.left = `${mapRect.left + pixel[0]}px`;
            popupContainer.style.top = `${mapRect.top + pixel[1]}px`;
            popupContainer.style.display = 'block';

            const mapSize = map.getSize();
            const popupRect = popupContainer.getBoundingClientRect();
            dx = popupRect.right - mapRect.right;
            dy = popupRect.bottom - mapRect.bottom;

            if (dx > 0 || dy > 0) {
                if (dx < 0) dx = 0;
                if (dy < 0) dy = 0;
                const view = map.getView();
                const resolution = view.getResolution();
                console.log(`Resolution: ${resolution}, dx: ${dx}, dy: ${dy}`);

                const center = view.getCenter();
                const offset = [(dx + 100) * resolution , (dy + 100) * resolution];

                const newCenter = [
                    center[0] + offset[0],
                    center[1] - offset[1],
                ];

                view.animate(
                    {
                        center: newCenter,
                        duration: 300,
                    },
                    function (complete) {
                        if (complete) {
                            pixel = map.getPixelFromCoordinate(coordinates);
                            mapRect = map.getTargetElement().getBoundingClientRect();

                            popupContainer.style.left = `${mapRect.left + pixel[0]}px`;
                            popupContainer.style.top = `${mapRect.top + pixel[1]}px`;
                            popupContainer.style.display = 'block';
                        }
                    }
                );
            }
        }
    }

    map.addInteraction(selectInteraction);  
    selectInteraction.on('select', function (e) {
        console.log(e);
        if(e.selected[0].get('features'))
            selectFeature(e.selected[0].get('features')[0]);
    });


    map.on('click', function (event) {
        map.forEachFeatureAtPixel(event.pixel, function (feature, layer) {
            if (layer.get('name') === 'dp') {
                const cluster_feature = feature.get('features')[0];
                showOverlay(cluster_feature, event.coordinate);
            }
        });
    });

    let draw;
    let measureActive = false;
    let measureTooltipElement;
    let measureTooltip;

    const formatLength = function (line) {
        const length = ol.sphere.getLength(line, { projection: map.getView().getProjection() });
        let output;
        if (length > 100) {
            output = (Math.round(length / 1000 * 100) / 100) + ' ' + 'km';
        } else {
            output = (Math.round(length * 100) / 100) + ' ' + 'm';
        }
        return output;
    };

    const toggleMeasurement = function () {
        measureActive = !measureActive;
        if (measureActive) {
            draw = new ol.interaction.Draw({
                source: vectorSource,
                type: 'LineString',
                style: new ol.style.Style({
                    fill: new ol.style.Fill({
                        color: 'rgba(255, 255, 255, 0.2)',
                    }),
                    stroke: new ol.style.Stroke({
                        color: 'rgba(0, 0, 0, 0.5)',
                        lineDash: [10, 10],
                        width: 2,
                    }),
                    image: new ol.style.Circle({
                        radius: 5,
                        stroke: new ol.style.Stroke({
                            color: 'rgba(0, 0, 0, 0.7)',
                        }),
                        fill: new ol.style.Fill({
                            color: 'rgba(255, 255, 255, 0.2)',
                        }),
                    }),
                }),
            });
            map.addInteraction(draw);

            measureTooltipElement = document.createElement('div');
            measureTooltipElement.className = 'tooltip';
            measureTooltip = new ol.Overlay({
                element: measureTooltipElement,
                offset: [0, -15],
                positioning: 'bottom-center'
            });
            map.addOverlay(measureTooltip);

            let listener;
            draw.on('drawstart', function (event) {
                const sketch = event.feature;
                listener = sketch.getGeometry().on('change', function (evt) {
                    const geom = evt.target;
                    const output = formatLength(geom);
                    measureTooltipElement.innerHTML = output;
                    const tooltipCoord = geom.getLastCoordinate();
                    measureTooltip.setPosition(tooltipCoord);
                });
            });

            draw.on('drawend', function () {
                measureTooltipElement.className = 'tooltip tooltip-static';
                measureTooltip.setOffset([0, -7]);
                draw.un('drawstart', function () {
                    sketch.getGeometry().un('change', listener);
                });
            });
        } else {
            map.removeInteraction(draw);
            map.removeOverlay(measureTooltip);
        }
    };

    document.addEventListener('keydown', function (event) {
        if (event.key === 'm') {
            toggleMeasurement();
        }
    });

    const searchInput = document.querySelector('#search-bar input');
    const searchResultsContainer = document.getElementById('search-results');

    // Event listener for search input
    searchInput.addEventListener('input', function () {
        const searchTerm = this.value.trim().toLowerCase();
        console.log('Searching');

        // Clear previous search results
        vectorSource.clear();
        searchResultsContainer.innerHTML = ''; // Clear previous search results in the container

        // Filter features based on search term
        clusters = itpLayer.getSource().getFeatures();
        clusters.forEach(cluster => {
            if (cluster.get('features')) {
                features = cluster.get('features');
                    features.forEach(feature => {
                        const featureValue = feature.get('itp_no_mag').toLowerCase();

                        if (featureValue.includes(searchTerm)) {
                            // Add matching features to vector source
                            //vectorSource.addFeature(feature.clone());

                            // Display matching feature in the results container
                            const resultItem = document.createElement('div');
                            resultItem.textContent = featureValue.toUpperCase();
                            searchResultsContainer.appendChild(resultItem);
                            resultItem.addEventListener('click', function () {
                                // Handle the click event for the selected result
                                selectInteraction.getFeatures().clear();

                                // Add the selected feature to the Select interaction
                                selectInteraction.getFeatures().push(feature);
                                selectFeature(feature);
                                searchResultsContainer.innerHTML = '';
                            });
                        }
                    });
                }
            });
        // Position the results container below the search bar
        const searchBarRect = searchInput.getBoundingClientRect();
        searchResultsContainer.style.left = searchBarRect.left + 'px';
        searchResultsContainer.style.top = (searchBarRect.bottom + window.scrollY) + 'px';
    });

    document.addEventListener('click', function (event) {
        if (!searchResultsContainer.contains(event.target) && event.target !== searchInput) {
            // Click occurred outside search results and search input
            searchResultsContainer.innerHTML = '';
        }
    });

    const mousePositionControlProjected = new ol.control.MousePosition({
        coordinateFormat: function (coordinate) {
            const lon = coordinate[0].toFixed(2);
            const lat = coordinate[1].toFixed(2);
            const latDir = lat >= 0 ? 'N' : 'S';
            const lonDir = lon >= 0 ? 'E' : 'W';

            return lat + latDir + ' ' + lon + lonDir;
            //return lat + '°' + latDir + ' ' + lon + '°' + lonDir;
        },
        projection: epsg_string,
        className: 'custom-mouse-position',
        target: document.getElementById('mouse-position-projected'),
        undefinedHTML: '&nbsp;'

    });

    map.addControl(mousePositionControlProjected);

    const mousePositionControl = new ol.control.MousePosition({
        coordinateFormat: function (coordinate) {
            const lon = coordinate[0].toFixed(2);
            const lat = coordinate[1].toFixed(2);
            const latDir = lat >= 0 ? 'N' : 'S';
            const lonDir = lon >= 0 ? 'E' : 'W';

            return lat + '°' + latDir + ' ' + lon + '°' + lonDir;
        },
        projection: 'EPSG:4326',
        className: 'custom-mouse-position',
        target: document.getElementById('mouse-position'),
        undefinedHTML: '&nbsp;'

    });

    map.addControl(mousePositionControl);

    let depthData = [];

    fetch(GEODATA_URL + PROJECT_NAME +'/geodata/xyz/depthsA.xyz')
        .then(response => response.text())
        .then(text => {
            const lines = text.split('\n');
            lines.forEach(line => {
                const [easting, northing, depth] = line.split(' ').map(Number);
                if (!isNaN(easting) && !isNaN(northing) && !isNaN(depth)) {
                    depthData.push({ easting, northing, depth });
                }
            });
        })
    .catch(error => console.error('Error loading XYZ file:', error));

    fetch(GEODATA_URL + PROJECT_NAME +'/geodata/xyz/depthsB.xyz')
        .then(response => response.text())
        .then(text => {
            const lines = text.split('\n');
            lines.forEach(line => {
                const [easting, northing, depth] = line.split(' ').map(Number);
                if (!isNaN(easting) && !isNaN(northing) && !isNaN(depth)) {
                    depthData.push({ easting, northing, depth });
                }
            });
        })
    .catch(error => console.error('Error loading XYZ file:', error));

    fetch(GEODATA_URL + PROJECT_NAME +'/geodata/xyz/depthsHA.xyz')
        .then(response => response.text())
        .then(text => {
            const lines = text.split('\n');
            lines.forEach(line => {
                const [easting, northing, depth] = line.split(',').map(Number);
                if (!isNaN(easting) && !isNaN(northing) && !isNaN(depth)) {
                    depthData.push({ easting, northing, depth });
                }
            });
        })
    .catch(error => console.error('Error loading XYZ file:', error));
    
    function getDepthAtCoordinate(coordinate) {
        const easting = coordinate[0];
        const northing = coordinate[1];
        
        let nearestPoint = null;
        let nearestDistance = Infinity;
        let minDist = 2;
        let acceptableDiff = 1;
        
        for (let i = 0; i < depthData.length; i++) {
            point = depthData[i];
            const dist = Math.pow(point.easting - easting, 2) + Math.pow(point.northing - northing, 2);
            if (dist < nearestDistance & dist < minDist) {
                nearestDistance = dist;
                nearestPoint = point;
                if (dist < acceptableDiff) {
                    break;
                }
            }
        }

        return nearestPoint ? nearestPoint.depth : 'N/A';
    }
    
    const depthControl = new ol.control.MousePosition({
        coordinateFormat: function (coordinate) {
            const lon = coordinate[0].toFixed(2);
            const lat = coordinate[1].toFixed(2);
            const depth = getDepthAtCoordinate(coordinate);
    
            return `Depth: ${depth} meters`;
        },
        projection: epsg_string,
        className: 'custom-depth-control',
        target: document.getElementById('mouse-depth'),
        undefinedHTML: 'Depth: N/A'
    });

    map.addControl(depthControl);

    const statisticsButton = document.getElementById('statistics-button');
    const statisticsPopup = document.getElementById('statistics-popup');
    const closeStatisticsPopupButton = document.getElementById('close-statistics-popup');

    /*statisticsButton.addEventListener('click', function () {
        // Show the popup
        statisticsPopup.style.display = 'block';

        // Create a simple pie chart
        const pieChartContainer = document.getElementById('pie-chart');
        createPieChart(pieChartContainer, 'clear');
        document.getElementById('clear-button').style.backgroundColor = 'green';

        // Handle checkbox events
        const statbutton1 = document.getElementById('clear-button');
        const statbutton2 = document.getElementById('todo-button');
        const statbutton3 = document.getElementById('uxo-button');
        const statbutton4 = document.getElementById('performance-button');
        const statbutton5 = document.getElementById('ship-button');

        statbutton1.addEventListener('click', handleStatToggle);
        statbutton2.addEventListener('click', handleStatToggle);
        statbutton3.addEventListener('click', handleStatToggle);
        statbutton4.addEventListener('click', handleStatToggle);
        statbutton5.addEventListener('click', handleStatToggle);
    });*/

    closeStatisticsPopupButton.addEventListener('click', function () {
        // Hide the popup
        statisticsPopup.style.display = 'none';
    });

    // Function to create a simple pie chart
    function createPieChart(container, type) {
        // Remove any existing canvas in the container
        container.innerHTML = '';
    
        // Create a new canvas element
        const canvas = document.createElement('canvas');
        canvas.style.width = 570;
        canvas.style.height = 360;
        container.appendChild(canvas);
    
        // Get the 2D context of the canvas
        const ctx = canvas.getContext('2d');
    
        // Set the new data and labels based on the type
        let data;
        if (type === 'clear') {
            data = {
                labels: ['Clear', 'Not clear', 'Waiting'],
                datasets: [{
                    data: [mtl_items_clear_count, mtl_items_not_clear_count, mtl_items_open_count],
                    backgroundColor: ['green', 'red', 'yellow'],
                    hoverBackgroundColor: ['green', 'red', 'yellow'],
                }],
            };
        } else if (type === 'todo') {
            data = {
                labels: ['To be cleared', 'Not to be cleared'],
                datasets: [{
                    data: [mtl_items_to_clear_count, mtl_items_count - mtl_items_to_clear_count],
                    backgroundColor: ['red', 'grey'],
                    hoverBackgroundColor: ['red', 'grey'],
                }],
            };
        } else if (type === 'uxo') {
            data = {
                labels: ['UXO', 'non-UXO'],
                datasets: [{
                    data: [mtl_items_uxo_count, mtl_items_clear_count - mtl_items_uxo_count],
                    backgroundColor: ['red', 'grey'],
                    hoverBackgroundColor: ['red', 'grey'],
                }],
            };
        } else if (type === 'ship') {
            data = {
                labels: ['Cleared by Kamara', 'Cleared by Sentinel', 'Unassigned'],
                datasets: [{
                    data: [mtl_items_kamara, mtl_items_sentinel, mtl_items_clear_count - (mtl_items_sentinel + mtl_items_kamara)],
                    backgroundColor: ['blue', 'purple', 'green'],
                    hoverBackgroundColor: ['blue', 'purple', 'green'],
                }],
            };
        } else if (type === 'performance'){
            data = {
                labels: clearance_dates.map(entry => entry.cl_date.slice(5)),
                datasets: [
                    {
                        label: 'Targets cleared',
                        data: clearance_dates.map(entry => entry.count),
                        backgroundColor: 'green',
                        borderColor: 'rgba(75, 192, 192, 1)',
                        borderWidth: 1,
                        //yAxisID: 'y-left'
                    },
                    {
                        label: 'Operational Hours',
                        data: clearance_dates.map(entry => entry.hours),
                        backgroundColor: 'blue',
                        borderColor: 'rgba(153, 102, 255, 1)',
                        borderWidth: 1,
                        //yAxisID: 'y-right'
                    }
                ]
            };
        }

        const pie_options = {
            responsive: true,
            maintainAspectRatio: false,
            tooltips: {
                callbacks: {
                    label: function (tooltipItem, data) {
                        // Calculate the percentage
                        const dataset = data.datasets[tooltipItem.datasetIndex];
                        const total = dataset.data.reduce((sum, value) => sum + value, 0);
                        const value = dataset.data[tooltipItem.index];
                        const percentage = ((value / total) * 100).toFixed(2) + '%';
    
                        // Display label with count and percentage
                            return /*data.labels[tooltipItem.index] + ': ' +*/ value + ' of '+ total +' (' + percentage + ')';
                    },
                },
                bodyFontSize: 18,
            },
            legend: {
                display: true,
                labels: {
                    generateLabels: function(chart) {
                        const labels = chart.data.labels.map(function(label, index) {
                            const dataset = chart.data.datasets[0];
                            const backgroundColor = dataset.backgroundColor[index];
                            const count = dataset.data[index];
                            return {
                                text: label + ': ' + count,
                                fillStyle: backgroundColor
                            };
                        });
                        return labels;
                    },
                    fontSize: 16,
                },
            }
        };

        const bar_options = {
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true
                    },
                }],
                xAxes: [{
                    ticks: {
                        autoSkip: true, // Ensure all labels are shown
                        maxRotation: 90,
                        minRotation: 0
                    },
                    /*afterBuildTicks: function(chartObj) {
                        // Limit the number of x-axis labels
                        const maxTicks = 10; // Set maximum number of ticks here
                        if (chartObj.ticks.length > maxTicks) {
                            chartObj.ticks = chartObj.ticks.slice(chartObj.ticks.length - maxTicks);
                        }
                    }*/
                }]
            },
            plugins: {
                zoom: {
                    pan: {
                        enabled: true,
                        drag: true,
                        mode: 'x',
                        speed: 0.1,
                        threshold: 2,
                        sensitivity: 3,
                    },
                    zoom: {
                        enabled: true,
                        drag: false,
                        mode: 'x',
                        rangeMin: {
                            x: null,
                            y: null
                        },
                        rangeMax: {
                            x: null,
                            y: null
                        },
                        speed: 0.1,
                        threshold: 2,
                        sensitivity: 3,
                    }
                }
                
            }
        }; 

        /*
        const bar_options = {
            scales: {
                yAxes: [
                    {
                        id: 'y-left',
                        position: 'left',
                        ticks: {
                            beginAtZero: true,
                            color: 'rgba(75, 192, 192, 1)'
                        },
                        scaleLabel: {
                            display: true,
                            labelString: 'Cleared MTLs'
                        }
                    },
                    {
                        id: 'y-right',
                        position: 'right',
                        ticks: {
                            beginAtZero: true,
                            color: 'rgba(153, 102, 255, 1)'
                        },
                        gridLines: {
                            drawOnChartArea: false // Prevents grid lines on the right y-axis
                        },
                        scaleLabel: {
                            display: true,
                            labelString: 'Operational Hours'
                        }
                    }
                ]
            }
        };
        */
    
        if(type === 'performance'){
            new Chart(ctx, {
                type: 'bar',
                data: data,
                options: bar_options,
            });
        }else{
            new Chart(ctx, {
                type: 'pie',
                data: data,
                options: pie_options,
            });
        }
    }
    

    // Function to handle checkbox change events
    function handleStatToggle(event) {
        const buttonId = event.target.id;
        if(buttonId=='clear-button'){
            const pieChartContainer = document.getElementById('pie-chart');
            createPieChart(pieChartContainer, 'clear');
            document.getElementById('clear-button').style.backgroundColor = 'green';
            document.getElementById('todo-button').style.backgroundColor = 'black';
            document.getElementById('uxo-button').style.backgroundColor = 'black';
            document.getElementById('performance-button').style.backgroundColor = 'black';
            document.getElementById('ship-button').style.backgroundColor = 'black';
        }else if(buttonId=='todo-button'){
            const pieChartContainer = document.getElementById('pie-chart');
            createPieChart(pieChartContainer, 'todo');
            document.getElementById('clear-button').style.backgroundColor = 'black';
            document.getElementById('todo-button').style.backgroundColor = 'green';
            document.getElementById('uxo-button').style.backgroundColor = 'black';
            document.getElementById('performance-button').style.backgroundColor = 'black';
            document.getElementById('ship-button').style.backgroundColor = 'black';
        }else if(buttonId=='uxo-button'){
            const pieChartContainer = document.getElementById('pie-chart');
            createPieChart(pieChartContainer, 'uxo');
            document.getElementById('clear-button').style.backgroundColor = 'black';
            document.getElementById('todo-button').style.backgroundColor = 'black';
            document.getElementById('uxo-button').style.backgroundColor = 'green';
            document.getElementById('performance-button').style.backgroundColor = 'black';
            document.getElementById('ship-button').style.backgroundColor = 'black';
        }else if(buttonId=='performance-button'){
            const pieChartContainer = document.getElementById('pie-chart');
            createPieChart(pieChartContainer, 'performance');
            document.getElementById('clear-button').style.backgroundColor = 'black';
            document.getElementById('todo-button').style.backgroundColor = 'black';
            document.getElementById('uxo-button').style.backgroundColor = 'black';
            document.getElementById('performance-button').style.backgroundColor = 'green';
            document.getElementById('ship-button').style.backgroundColor = 'black';
        }else if(buttonId=='ship-button'){
            const pieChartContainer = document.getElementById('pie-chart');
            createPieChart(pieChartContainer, 'ship');
            document.getElementById('clear-button').style.backgroundColor = 'black';
            document.getElementById('todo-button').style.backgroundColor = 'black';
            document.getElementById('uxo-button').style.backgroundColor = 'black';
            document.getElementById('performance-button').style.backgroundColor = 'black';
            document.getElementById('ship-button').style.backgroundColor = 'green';
        }
    }

    document.getElementById('filter-button').onclick=openFilterPopup;
    document.getElementById('close-filters-button').onclick=closeFilterPopup;
    document.getElementById('apply-filters-button').onclick=applyFilters;
    document.getElementById('reset-filters-button').onclick=resetFilters;

    function openFilterPopup() {
        document.getElementById('filter-popup').style.display = 'block';

        closeLanguagePopup();
        closeLayerPopup();
        closeLegendPopup();
        closeITPClusterPopup();
    }
    
    function closeFilterPopup() {
        document.getElementById('filter-popup').style.display = 'none';
    }
    
    function applyFilters() {

        target_filters.found = '';
        target_filters.recovered = '';        
        target_filters.uxo = '';        
        target_filters.clear = '';        
        target_filters.qa_clear = '';        
        target_filters.to_do = '';        

        if(document.getElementById('found-filter').checked)
            target_filters.found = 'y';
        if(document.getElementById('recovered-filter').checked)
            target_filters.recovered = 'y';
        if(document.getElementById('uxo-filter').checked)
            target_filters.uxo = 'y';
        if(document.getElementById('clear-filter').checked)
            target_filters.clear = 'y';
        if(document.getElementById('qa-clear-filter').checked)
            target_filters.qa_clear = 'y';
        if(document.getElementById('to-do-filter').checked)
            target_filters.to_do = 'y';

        if(document.getElementById('nfound-filter').checked)
            target_filters.found = 'n';
        if(document.getElementById('nrecovered-filter').checked)
            target_filters.recovered = 'n';
        if(document.getElementById('nuxo-filter').checked)
            target_filters.uxo = 'n';
        if(document.getElementById('nclear-filter').checked)
            target_filters.clear = 'n';
        if(document.getElementById('nqa-clear-filter').checked)
            target_filters.qa_clear = 'n';
        if(document.getElementById('nto-do-filter').checked)
            target_filters.to_do = 'n';


        if(document.getElementById('wclear-filter').checked)
            target_filters.clear = 'w';
        if(document.getElementById('wrecovered-filter').checked)
            target_filters.recovered = 'w';

        if(document.getElementById('prio1-filter').checked)
            target_filters.prio = '1';
        if(document.getElementById('prio2-filter').checked)
            target_filters.prio = '2';

        map.getLayers().forEach(layer => layer.getSource().refresh());

        closeFilterPopup();
    }

    //Making filter checkboxes mutually exclusive

    document.getElementById('found-filter').addEventListener('change', function () {
        if (document.getElementById('found-filter').checked) {
            document.getElementById('nfound-filter').checked = false;
        }
    });
    document.getElementById('recovered-filter').addEventListener('change', function () {
        if (document.getElementById('recovered-filter').checked) {
            document.getElementById('nrecovered-filter').checked = false;
            document.getElementById('wrecovered-filter').checked = false;
        }
    });
    document.getElementById('uxo-filter').addEventListener('change', function () {
        if (document.getElementById('uxo-filter').checked) {
            document.getElementById('nuxo-filter').checked = false;
        }
    });
    document.getElementById('clear-filter').addEventListener('change', function () {
        if (document.getElementById('clear-filter').checked) {
            document.getElementById('nclear-filter').checked = false;
            document.getElementById('wclear-filter').checked = false;
        }
    });
    document.getElementById('qa-clear-filter').addEventListener('change', function () {
        if (document.getElementById('qa-clear-filter').checked) {
            document.getElementById('nqa-clear-filter').checked = false;
        }
    });
    document.getElementById('to-do-filter').addEventListener('change', function () {
        if (document.getElementById('to-do-filter').checked) {
            document.getElementById('nto-do-filter').checked = false;
        }
    });

    document.getElementById('nfound-filter').addEventListener('change', function () {
        if (document.getElementById('nfound-filter').checked) {
            document.getElementById('found-filter').checked = false;
        }
    });
    document.getElementById('nrecovered-filter').addEventListener('change', function () {
        if (document.getElementById('nrecovered-filter').checked) {
            document.getElementById('recovered-filter').checked = false;
            document.getElementById('wrecovered-filter').checked = false;
        }
    });
    document.getElementById('nuxo-filter').addEventListener('change', function () {
        if (document.getElementById('nuxo-filter').checked) {
            document.getElementById('uxo-filter').checked = false;
        }
    });
    document.getElementById('nclear-filter').addEventListener('change', function () {
        if (document.getElementById('nclear-filter').checked) {
            document.getElementById('clear-filter').checked = false;
            document.getElementById('wclear-filter').checked = false;
        }
    });
    document.getElementById('nqa-clear-filter').addEventListener('change', function () {
        if (document.getElementById('nqa-clear-filter').checked) {
            document.getElementById('qa-clear-filter').checked = false;
        }
    });
    document.getElementById('nto-do-filter').addEventListener('change', function () {
        if (document.getElementById('nto-do-filter').checked) {
            document.getElementById('to-do-filter').checked = false;
        }
    });

    document.getElementById('wrecovered-filter').addEventListener('change', function () {
        if (document.getElementById('wrecovered-filter').checked) {
            document.getElementById('recovered-filter').checked = false;
            document.getElementById('nrecovered-filter').checked = false;
        }
    });
    document.getElementById('wclear-filter').addEventListener('change', function () {
        if (document.getElementById('wclear-filter').checked) {
            document.getElementById('clear-filter').checked = false;
            document.getElementById('nclear-filter').checked = false;
        }
    });

    function resetFilters() {
        target_filters.found = '';
        target_filters.recovered = '';        
        target_filters.uxo = '';        
        target_filters.clear = '';        
        target_filters.qa_clear = '';        
        target_filters.to_do = ''; 
        target_filters.prio = '';

        checkboxes = document.querySelector('.checkbox-container').querySelectorAll('input[type="checkbox"]');
        checkboxes.forEach(function (checkbox) {
            checkbox.checked = false;
        });

        map.getLayers().forEach(layer => layer.getSource().refresh());

    }

    function showLayerPopup() {
        document.getElementById("layer-popup").style.display = "block";
        closeLanguagePopup();
        closeLegendPopup();
        closeFilterPopup();
        closeITPClusterPopup();
    }
      
    function closeLayerPopup() {
        document.getElementById("layer-popup").style.display = "none";
    }
      
    document.getElementById("layer-button").addEventListener("click", showLayerPopup);
    document.getElementById("close-layers-button").addEventListener("click", closeLayerPopup);

    document.getElementById('layer-popup').getElementsByTagName("input").namedItem("base").checked = true;
    document.getElementById('layer-popup').getElementsByTagName("input").namedItem("osm").checked = true;
    document.getElementById('layer-popup').getElementsByTagName("input").namedItem("tmi").checked = true;
    document.getElementById('layer-popup').getElementsByTagName("input").namedItem("overlay").checked = true;
    document.getElementById('layer-popup').getElementsByTagName("input").namedItem("itp").checked = true;

    const layercheckboxes = document.querySelector('#layer-popup .checkbox-container').querySelectorAll('input[type="checkbox"]');;
    const layerSliders = document.querySelectorAll('#layer-popup .checkbox-container input[type="range"]');

    layercheckboxes.forEach(function (checkbox) {
        checkbox.addEventListener('change', function () {
            if(checkbox.checked){
                map.getLayers().getArray().find(layer => layer.get('name') === checkbox.name).setVisible(true);
                if(checkbox.name === 'overlay'){
                    map.getLayers().getArray().find(layer => layer.get('name') === 'texts').setVisible(true);
                }else if(checkbox.name === 'overlay2'){
                    map.getLayers().getArray().find(layer => layer.get('name') === 'texts2').setVisible(true);
                }
            } else{
                map.getLayers().getArray().find(layer => layer.get('name') === checkbox.name).setVisible(false);
                if(checkbox.name === 'overlay'){
                    map.getLayers().getArray().find(layer => layer.get('name') === 'texts').setVisible(false);
                }else if(checkbox.name === 'overlay2'){
                    map.getLayers().getArray().find(layer => layer.get('name') === 'texts2').setVisible(false);
                }
            }
        });
    });

    layerSliders.forEach(function (slider) {
        slider.addEventListener('input', function () {
            const layerName = slider.name.replace('-slider', '');
            const layer = map.getLayers().getArray().find(layer => layer.get('name') === layerName);
            layer.setOpacity(parseFloat(slider.value));
            if(layerName === 'overlay'){
                map.getLayers().getArray().find(layer => layer.get('name') === 'texts').setOpacity(parseFloat(slider.value));
            } else if(layerName === 'overlay2'){
                map.getLayers().getArray().find(layer => layer.get('name') === 'texts2').setOpacity(parseFloat(slider.value));
            }
        });
    });

    document.getElementById('cluster-button').addEventListener('click', function() {
        openITPClusterPopup();
    });
    
    document.getElementById('close-itp-cluster-popup').addEventListener('click', function() {
        closeITPClusterPopup();
    });

    function openITPClusterPopup() {
        document.getElementById('itp-cluster-popup').style.display = 'block';

        closeLanguagePopup();
        closeLayerPopup();
        closeFilterPopup();
        closeLegendPopup();
    }

    function closeITPClusterPopup() {
        document.getElementById('itp-cluster-popup').style.display = 'none';
    }

    document.getElementById('itp-cluster-slider').addEventListener('input', function() {
        var sliderValue = document.getElementById('itp-cluster-slider').value;
        itpLayer.getSource().setDistance(sliderValue);
        document.getElementById('itp-cluster-value').innerText = sliderValue + ' pixels';
    });

    document.getElementById('language-button').addEventListener('click', function() {
        openLanguagePopup();
    });

    document.getElementById('close-language-button').addEventListener('click', function() {
        closeLanguagePopup();
    });

    function openLanguagePopup() {
        document.getElementById('language-popup').style.display = 'block';
        closeLegendPopup();
        closeLayerPopup();
        closeFilterPopup();
        closeITPClusterPopup();
    }

    function closeLanguagePopup() {
        document.getElementById('language-popup').style.display = 'none';
    }

    //getCurrentWeather
    function getWeatherDetails(latitude, longitude) {
        const apiUrl = `https://api.open-meteo.com/v1/forecast?latitude=${latitude}&longitude=${longitude}&current=temperature_2m,relative_humidity_2m,weather_code,wind_speed_10m&timezone=Europe%2FBerlin`;
    
        return fetch(apiUrl)
            .then(response => response.json())
            .then(data => {
                // Weather data is available in 'data'
                return data;
            })
            .catch(error => {
                console.error('Error fetching weather data:', error);
                return null;
            });
    }

    function getWeatherForecast(latitude, longitude){
        const apiUrl = `https://api.open-meteo.com/v1/forecast?latitude=${latitude}&longitude=${longitude}&hourly=temperature_2m,relative_humidity_2m,weather_code,wind_speed_10m&timezone=Europe%2FBerlin&past_days=7`;
    
        return fetch(apiUrl)
            .then(response => response.json())
            .then(data => {
                return data;
            })
            .catch(error => {
                console.error('Error fetching weather data:', error);
                return null;
            });
    }
    //WMO codes
    const weatherCodeDescriptions = {
        0: "Clear sky",
        1: "Mainly clear",
        2: "Partly cloudy",
        3: "Overcast",
        45: "Fog and depositing rime fog",
        48: "Fog and depositing rime fog",
        51: "Drizzle: Light intensity",
        53: "Drizzle: Moderate intensity",
        55: "Drizzle: Dense intensity",
        56: "Freezing Drizzle: Light intensity",
        57: "Freezing Drizzle: Dense intensity",
        61: "Rain: Slight intensity",
        63: "Rain: Moderate intensity",
        65: "Rain: Heavy intensity",
        66: "Freezing Rain: Light intensity",
        67: "Freezing Rain: Heavy intensity",
        71: "Snowfall: Slight intensity",
        73: "Snowfall: Moderate intensity",
        75: "Snowfall: Heavy intensity",
        77: "Snow grains",
        80: "Rain showers: Slight intensity",
        81: "Rain showers: Moderate intensity",
        82: "Rain showers: Violent intensity",
        85: "Snow showers: Slight intensity",
        86: "Snow showers: Heavy intensity",
        95: "Thunderstorm: Slight",
        96: "Thunderstorm: Slight hail",
        99: "Thunderstorm: Heavy hail",
    };

    //Weather api provider: https://open-meteo.com/
    function openWeatherPopup() {
        getWeatherDetails(map_center[1], map_center[0])
            .then(weatherDetails => {
                if(weatherDetails.current.temperature_2m){
                    const temperature = weatherDetails.current.temperature_2m;
                    document.getElementById('weather-temp').innerText = temperature+" °C";
                }
                if(weatherDetails.current.relative_humidity_2m){
                    const humidity = weatherDetails.current.relative_humidity_2m;
                    document.getElementById('weather-humidity').innerText = humidity+" %";
                }
                if(weatherDetails.current.weather_code){
                    const weatherCode = weatherDetails.current.weather_code;
                    document.getElementById('weather-condition').innerText = weatherCodeDescriptions[weatherCode];
                }
                if(weatherDetails.current.wind_speed_10m){
                    const windSpeed = weatherDetails.current.wind_speed_10m;
                    document.getElementById('weather-wind').innerText = windSpeed+" km/h";
                }
            });
        currentDate = new Date();
        const weekdays = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
        document.getElementById('weather-date-label').innerText = "Today "+"("+weekdays[currentDate.getDay()]+") "+currentDate.getHours()+ ":"+currentDate.getMinutes();
    
        document.getElementById('weather-popup').style.display = 'block';
    }
    
    function closeWeatherPopup() {
        document.getElementById('weather-popup').style.display = 'none';
    }

    function getWeather(){
        date = document.getElementById('weather-date').value;
        time = document.getElementById('weather-time').value;
        time=time.slice(0,-2)+"00";

        getWeatherForecast(map_center[1], map_center[0])
            .then(weatherDetails => {
                var isoDateTime = date + "T" + time;
                var index = weatherDetails.hourly.time.findIndex(entry => entry.startsWith(isoDateTime));
                if (index !== -1) {
                    const temperature = weatherDetails.hourly.temperature_2m[index];
                    document.getElementById('weather-temp').innerText = temperature+" °C";
                    const humidity = weatherDetails.hourly.relative_humidity_2m[index];
                    document.getElementById('weather-humidity').innerText = humidity+" %";
                    const weatherCode = weatherDetails.hourly.weather_code[index];
                    document.getElementById('weather-condition').innerText = weatherCodeDescriptions[weatherCode];
                    const windSpeed = weatherDetails.hourly.wind_speed_10m[index];
                    document.getElementById('weather-wind').innerText = windSpeed+" km/h";
                }else{
                    alert('Weather data is only available for the past 7 and next 7 days. Please check the date/time entry and try again');
                }
            });
            
        dateobj = new Date(date)
        const weekdays = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
        document.getElementById('weather-date-label').innerText = date + " ("+weekdays[dateobj.getDay()]+") " + time;

        document.getElementById('weather-temp').innerText = "Loading...";
        document.getElementById('weather-humidity').innerText = "Loading...";
        document.getElementById('weather-condition').innerText = "Loading...";
        document.getElementById('weather-wind').innerText = "Loading...";
    }

    //document.getElementById('weather-button').addEventListener('click', openWeatherPopup);
    document.getElementById('close-weather-button').addEventListener('click', closeWeatherPopup);
    document.getElementById('new-weather-button').addEventListener('click', getWeather);

    document.getElementById("pullUpCalendarButton").addEventListener("click", function() {
        var calendarContent = document.getElementById("calendarContent");
        calendarContent.classList.toggle("active");

        pullUpCalendarButton = document.getElementById("pullUpCalendarButton");
        pullUpCalendarButton.classList.toggle("active");
        if(pullUpCalendarButton.classList.contains("active")){
            pullUpCalendarButton.innerText = 'Close calendar';
        }else{
            pullUpCalendarButton.innerText = 'Pull up calendar';
        }
    });

    function openLegendPopup(){
        document.getElementById('legend-popup').style.display = 'block';
        closeLanguagePopup();
        closeLayerPopup();
        closeFilterPopup();
        closeITPClusterPopup();
    }
    function closeLegendPopup(){
        document.getElementById('legend-popup').style.display = 'none';
    }
    document.getElementById('legend-button').addEventListener('click', openLegendPopup);
    document.getElementById('close-legend-button').addEventListener('click', closeLegendPopup);

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    function updateVesselPosition(vesselId) {
        fetch(`/vessels/${vesselId}/update-position/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': getCookie('csrftoken')
            },
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                vesselLayer.getSource().clear();
                vesselLayer.getSource().refresh(); 
                alert('Position aktualisiert');
            } else {
                alert('Error updating position: ' + data.message);
            }
        })
        .catch(error => console.error('Error:', error));
    }
    
    function displayVesselDetails(link) {
        var shipName = link.getAttribute('data-ship-name');
        var mmsi = link.getAttribute('data-mmsi');
        var imo = link.getAttribute('data-imo');
        var easting = link.getAttribute('data-easting');
        var northing = link.getAttribute('data-northing');
    
        var detailsHtml = `
            <h2>${shipName}</h2>
            <p><strong>MMSI:</strong> ${mmsi ? mmsi : 'N/A'}</p>
            <p><strong>IMO:</strong> ${imo ? imo : 'N/A'}</p>
            <p><strong>Easting:</strong> ${easting}</p>
            <p><strong>Northing:</strong> ${northing}</p>
            <button id="updatePositionBtn">Position aktualisieren</button>
        `;
    
        document.getElementById('vesselDetails').innerHTML = detailsHtml;
    
        document.getElementById('updatePositionBtn').addEventListener('click', function() {
            updateVesselPosition(link.getAttribute('data-vessel-id'));
        });
    }

    document.querySelectorAll('.vessel-link').forEach(function(link) {
        link.addEventListener('click', function(event) {
            event.preventDefault();
            document.querySelectorAll('.vessel-link').forEach(function(link) {
                link.classList.remove('selected');
            });

            this.classList.add('selected');
            displayVesselDetails(this);
        });
    });

    function openVesselPopup(){
        document.getElementById('vessel-popup').style.display = 'block';
    }
    function closeVesselPopup(){
        document.getElementById('vessel-popup').style.display = 'none';
    }
    document.getElementById('ships-button').addEventListener('click', openVesselPopup);
    document.getElementById('close-vessel-button').addEventListener('click', closeVesselPopup);

    const dragElement = document.getElementById("itp_overlay");
    const dragHandle = dragElement.querySelector(".popup-header");

    let dragOffsetX = 0, dragOffsetY = 0, isDragging = false;

    dragHandle.addEventListener("mousedown", function (e) {
        e.preventDefault();
        isDragging = true;
        const rect = dragElement.getBoundingClientRect();
        dragOffsetX = e.clientX - rect.left;
        dragOffsetY = e.clientY - rect.top;

        document.addEventListener("mousemove", onDragMouseMove);
        document.addEventListener("mouseup", onDragMouseUp);
    });

    function onDragMouseMove(e) {
        if (!isDragging) return;
        dragElement.style.position = "absolute";
        dragElement.style.left = `${e.clientX - dragOffsetX}px`;
        dragElement.style.top = `${e.clientY - dragOffsetY}px`;
    }

    function onDragMouseUp() {
        isDragging = false;
        document.removeEventListener("mousemove", onDragMouseMove);
        document.removeEventListener("mouseup", onDragMouseUp);
    }

});

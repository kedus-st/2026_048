const empty_circle_marker = new ol.style.Style({
    image: new ol.style.Circle({
        radius: 5,
        stroke: new ol.style.Stroke({
            color: 'rgb(0,0,0)',
            width: 1,
        }),
        fill: new ol.style.Fill({
            color: 'rgba(255,0,0,0.0)',
        }),
        points: 5,
    }),
    text: new ol.style.Text({
        font: 'bold 10px "Open Sans", "Arial Unicode MS", "sans-serif"',
        placement: 'point',
        offsetX: 10,
        offsetY: -10,
        //fill: new ol.style.Fill({color: '#fff'}),
        //stroke: new ol.style.Stroke({color: '#000', width: 2}),
        stroke: new ol.style.Stroke({color: '000', width: 0.4}),
    }),
});

const empty_star_marker = new ol.style.Style({
    image: new ol.style.RegularShape({
        radius: 8,
        radius2: 3,
        stroke: new ol.style.Stroke({
            color: 'rgb(0,0,0)',
            width: 1,
        }),
        fill: new ol.style.Fill({
            color: 'rgba(255,0,0,0.0)',
        }),
        points: 5,
    }),
    text: new ol.style.Text({
        font: 'bold 10px "Open Sans", "Arial Unicode MS", "sans-serif"',
        placement: 'point',
        offsetX: 10,
        offsetY: -10,
        //fill: new ol.style.Fill({color: '#fff'}),
        //stroke: new ol.style.Stroke({color: '#000', width: 2}),
        stroke: new ol.style.Stroke({color: '000', width: 0.4}),
    }),
});

const red_circle_marker = new ol.style.Style({
    image: new ol.style.Circle({
        radius: 5,
        stroke: new ol.style.Stroke({
            color: 'rgb(0,0,0)',
            width: 1,
        }),
        fill: new ol.style.Fill({
            color: 'rgba(255,0,0,1.0)',
        }),
        points: 5,
    }),
    text: new ol.style.Text({
        font: 'bold 10px "Open Sans", "Arial Unicode MS", "sans-serif"',
        placement: 'point',
        offsetX: 10,
        offsetY: -10,
        //fill: new ol.style.Fill({color: '#fff'}),
        //stroke: new ol.style.Stroke({color: '#000', width: 2}),
        stroke: new ol.style.Stroke({color: '000', width: 0.4}),
    }),
});

const blue_circle_marker = new ol.style.Style({
    image: new ol.style.Circle({
        radius: 5,
        stroke: new ol.style.Stroke({
            color: 'rgb(0,0,0)',
            width: 1,
        }),
        fill: new ol.style.Fill({
            color: 'rgba(0,0,255,1.0)',
        }),
        points: 5,
    }),
    text: new ol.style.Text({
        font: 'bold 10px "Open Sans", "Arial Unicode MS", "sans-serif"',
        placement: 'point',
        offsetX: 10,
        offsetY: -10,
        //fill: new ol.style.Fill({color: '#fff'}),
        //stroke: new ol.style.Stroke({color: '#000', width: 2}),
        stroke: new ol.style.Stroke({color: '000', width: 0.4}),
    }),
});

const green_circle_marker = new ol.style.Style({
    image: new ol.style.Circle({
        radius: 5,
        stroke: new ol.style.Stroke({
            color: 'rgb(0,0,0)',
            width: 1,
        }),
        fill: new ol.style.Fill({
            color: 'rgba(0,255,0,1.0)',
        }),
        points: 5,
    }),
    text: new ol.style.Text({
        font: 'bold 11px "Open Sans", "Arial Unicode MS", "sans-serif"',
        placement: 'point',
        offsetX: 10,
        offsetY: -10,
        //fill: new ol.style.Fill({color: '#fff'}),
        //stroke: new ol.style.Stroke({color: '#000', width: 2}),
        stroke: new ol.style.Stroke({color: '000', width: 0.4}),
    }),
});

const green_star_marker = new ol.style.Style({
    image: new ol.style.RegularShape({
        radius: 8,
        radius2: 3,
        stroke: new ol.style.Stroke({
            color: 'rgb(0,0,0)',
            width: 1,
        }),
        fill: new ol.style.Fill({
            color: 'rgba(0,255,0,1.0)',
        }),
        points: 5,
    }),
    text: new ol.style.Text({
        font: 'bold 10px "Open Sans", "Arial Unicode MS", "sans-serif"',
        placement: 'point',
        offsetX: 10,
        offsetY: -10,
        //fill: new ol.style.Fill({color: '#fff'}),
        //stroke: new ol.style.Stroke({color: '#000', width: 2}),
        stroke: new ol.style.Stroke({color: '000', width: 0.4}),
    }),
});

const red_star_marker = new ol.style.Style({
    image: new ol.style.RegularShape({
        radius: 8,
        radius2: 3,
        stroke: new ol.style.Stroke({
            color: 'rgb(0,0,0)',
            width: 1,
        }),
        fill: new ol.style.Fill({
            color: 'rgba(255,0,0,1.0)',
        }),
        points: 5,
    }),
    text: new ol.style.Text({
        font: 'bold 10px "Open Sans", "Arial Unicode MS", "sans-serif"',
        placement: 'point',
        offsetX: 10,
        offsetY: -10,
        //fill: new ol.style.Fill({color: '#fff'}),
        //stroke: new ol.style.Stroke({color: '#000', width: 2}),
        stroke: new ol.style.Stroke({color: '000', width: 0.4}),
    }),
});

const yellow_circle_marker = new ol.style.Style({
    image: new ol.style.Circle({
        radius: 5,
        stroke: new ol.style.Stroke({
            color: 'rgb(0,0,0)',
            width: 1,
        }),
        fill: new ol.style.Fill({
            color: 'rgba(255,255,0,1.0)',
        }),
        points: 5,
    }),
    text: new ol.style.Text({
        font: 'bold 10px "Open Sans", "Arial Unicode MS", "sans-serif"',
        placement: 'point',
        offsetX: 10,
        offsetY: -10,
        //fill: new ol.style.Fill({color: '#fff'}),
        //stroke: new ol.style.Stroke({color: '#000', width: 2}),
        stroke: new ol.style.Stroke({color: '000', width: 0.4}),
    }),
});

const yellow_star_marker = new ol.style.Style({
    image: new ol.style.RegularShape({
        radius: 8,
        radius2: 3,
        stroke: new ol.style.Stroke({
            color: 'rgb(0,0,0)',
            width: 1,
        }),
        fill: new ol.style.Fill({
            color: 'rgba(255,255,0,1.0)',
        }),
        points: 5,
    }),
    text: new ol.style.Text({
        font: 'bold 10px "Open Sans", "Arial Unicode MS", "sans-serif"',
        placement: 'point',
        offsetX: 10,
        offsetY: -10,
        //fill: new ol.style.Fill({color: '#fff'}),
        //stroke: new ol.style.Stroke({color: '#000', width: 2}),
        stroke: new ol.style.Stroke({color: '000', width: 0.4}),
    }),
});

const purple_circle_marker = new ol.style.Style({
    image: new ol.style.Circle({
        radius: 5,
        stroke: new ol.style.Stroke({
            color: 'rgb(0,0,0)',
            width: 1,
        }),
        fill: new ol.style.Fill({
            color: 'rgba(128,0,128,1.0)',
        }),
    }),
    text: new ol.style.Text({
        font: 'bold 10px "Open Sans", "Arial Unicode MS", "sans-serif"',
        placement: 'point',
        offsetX: 10,
        offsetY: -10,
        stroke: new ol.style.Stroke({color: '000', width: 0.4}),
    }),
});

const blue_star_marker = new ol.style.Style({
    image: new ol.style.RegularShape({
        radius: 8,
        radius2: 3,
        stroke: new ol.style.Stroke({
            color: 'rgb(0,0,0)',
            width: 1,
        }),
        fill: new ol.style.Fill({
            color: 'rgba(0,0,255,1.0)',
        }),
        points: 5,
    }),
    text: new ol.style.Text({
        font: 'bold 10px "Open Sans", "Arial Unicode MS", "sans-serif"',
        placement: 'point',
        offsetX: 10,
        offsetY: -10,
        stroke: new ol.style.Stroke({color: '000', width: 0.4}),
    }),
});

const purple_star_marker = new ol.style.Style({
    image: new ol.style.RegularShape({
        radius: 8,
        radius2: 3,
        stroke: new ol.style.Stroke({
            color: 'rgb(0,0,0)',
            width: 1,
        }),
        fill: new ol.style.Fill({
            color: 'rgba(128,0,128,1.0)',
        }),
        points: 5,
    }),
    text: new ol.style.Text({
        font: 'bold 10px "Open Sans", "Arial Unicode MS", "sans-serif"',
        placement: 'point',
        offsetX: 10,
        offsetY: -10,
        stroke: new ol.style.Stroke({color: '000', width: 0.4}),
    }),
});

const orange_square_marker = new ol.style.Style({
    image: new ol.style.RegularShape({
        radius: 6,
        points: 4,
        angle: Math.PI / 4,
        stroke: new ol.style.Stroke({
            color: 'rgb(0,0,0)',
            width: 1,
        }),
        fill: new ol.style.Fill({
            color: 'rgba(255,165,0,1.0)',
        }),
    }),
    text: new ol.style.Text({
        font: 'bold 10px "Open Sans", "Arial Unicode MS", "sans-serif"',
        placement: 'point',
        offsetX: 10,
        offsetY: -10,
        stroke: new ol.style.Stroke({color: '000', width: 0.4}),
    }),
});

const green_square_marker = new ol.style.Style({
    image: new ol.style.RegularShape({
        radius: 5,
        points: 4,
        angle: Math.PI / 4,
        stroke: new ol.style.Stroke({
            color: 'rgb(0,0,0)',
            width: 1,
        }),
        fill: new ol.style.Fill({
            color: 'rgba(0,128,0,1.0)',
        }),
    }),
    text: new ol.style.Text({
        font: 'bold 10px "Open Sans", "Arial Unicode MS", "sans-serif"',
        placement: 'point',
        offsetX: 10,
        offsetY: -10,
        stroke: new ol.style.Stroke({color: '000', width: 0.4}),
    }),
});

const orange_circle_marker = new ol.style.Style({
    image: new ol.style.Circle({
        radius: 5,
        stroke: new ol.style.Stroke({
            color: 'rgb(0,0,0)',
            width: 1,
        }),
        fill: new ol.style.Fill({
            color: 'rgb(255,165,0)',
        }),
        points: 5,
    }),
    text: new ol.style.Text({
        font: 'bold 10px "Open Sans", "Arial Unicode MS", "sans-serif"',
        placement: 'point',
        offsetX: 10,
        offsetY: -10,
        //fill: new ol.style.Fill({color: '#fff'}),
        //stroke: new ol.style.Stroke({color: '#000', width: 2}),
        stroke: new ol.style.Stroke({color: '000', width: 0.4}),
    }),
});

const itp_styleFunction = function (clusters, resolution) {
    const features = clusters.get('features');
    var size = 0;
    if (features) {
        size = features.length;
    }
    if (size > 1 /*&& resolution > 0.3*/) {
        style = new ol.style.Style({
            image: new ol.style.Circle({
                radius: 10,
                fill: new ol.style.Fill({
                    color: 'rgba(0, 255, 0, 0.5)',
                }),
            }),
            text: new ol.style.Text({
                text: size.toString(),
                fill: new ol.style.Fill({
                    color: 'black',
                }),
            }),
        });
        return style;
    } else {
        feature = features[0];
        style = new ol.style.Style({});
        if (feature.get('todo_target') === 'x') {
            if ((feature.get('clear') == 'y' && feature.get('uxo') != 'x') || (feature.get('clear') == 'y' && feature.get('uxo') == '')) {
                green_circle_marker.getText().setText(feature.get('itp_no_mag').replace('ITP-0000', '').replace('ITP-000', '').replace('ITP-00', '').replace('ITP-0', '').replace('ITP-', ''));
                style = green_circle_marker;
            }
            else if (feature.get('clear') == 'y' && feature.get('uxo') == 'x') {
                green_star_marker.getText().setText(feature.get('itp_no_mag').replace('ITP-0000', '').replace('ITP-000', '').replace('ITP-00', '').replace('ITP-0', '').replace('ITP-', ''));
                style = green_star_marker;
            }
            else if ((feature.get('clear') == 'w' && feature.get('uxo') != 'x') || (feature.get('clear') == 'w' && feature.get('uxo') == '')) {
                yellow_circle_marker.getText().setText(feature.get('itp_no_mag').replace('ITP-0000', '').replace('ITP-000', '').replace('ITP-00', '').replace('ITP-0', '').replace('ITP-', ''));
                style = yellow_circle_marker;
            }
            else if (feature.get('clear') == 'w' && feature.get('uxo') == 'x') {
                yellow_star_marker.getText().setText(feature.get('itp_no_mag').replace('ITP-0000', '').replace('ITP-000', '').replace('ITP-00', '').replace('ITP-0', '').replace('ITP-', ''));
                style = yellow_star_marker;
            }
            else if ((feature.get('clear') == 'n' && feature.get('uxo') != 'x') || (feature.get('clear') == 'n' && feature.get('uxo') == null)) {
                red_circle_marker.getText().setText(feature.get('itp_no_mag').replace('ITP-0000', '').replace('ITP-000', '').replace('ITP-00', '').replace('ITP-0', '').replace('ITP-', ''));
                style = red_circle_marker;
            }
            else if (feature.get('clear') == 'n' && feature.get('uxo') == 'x') {
                red_star_marker.getText().setText(feature.get('itp_no_mag').replace('ITP-0000', '').replace('ITP-000', '').replace('ITP-00', '').replace('ITP-0', '').replace('ITP-', ''));
                style = red_star_marker;
            }
            else {
                red_circle_marker.getText().setText(feature.get('itp_no_mag').replace('ITP-0000', '').replace('ITP-000', '').replace('ITP-00', '').replace('ITP-0', '').replace('ITP-', ''));
                style = red_circle_marker;
            }
        } else {
            if ((feature.get('clear') == 'y' && feature.get('uxo') != 'x') || (feature.get('clear') == 'y' && feature.get('uxo') == '')) {
                green_circle_marker.getText().setText(feature.get('itp_no_mag').replace('ITP-0000', '').replace('ITP-000', '').replace('ITP-00', '').replace('ITP-0', '').replace('ITP-', ''));
                style = green_circle_marker;
            }
            else if (feature.get('clear') == 'y' && feature.get('uxo') == 'x') {
                green_star_marker.getText().setText(feature.get('itp_no_mag').replace('ITP-0000', '').replace('ITP-000', '').replace('ITP-00', '').replace('ITP-0', '').replace('ITP-', ''));
                style = green_star_marker;
            }
            else if ((feature.get('clear') == 'w' && feature.get('uxo') != 'x') || (feature.get('clear') == 'w' && feature.get('uxo') == '')) {
                yellow_circle_marker.getText().setText(feature.get('itp_no_mag').replace('ITP-0000', '').replace('ITP-000', '').replace('ITP-00', '').replace('ITP-0', '').replace('ITP-', ''));
                style = yellow_circle_marker;
            }
            else if (feature.get('clear') == 'w' && feature.get('uxo') == 'x') {
                yellow_star_marker.getText().setText(feature.get('itp_no_mag').replace('ITP-0000', '').replace('ITP-000', '').replace('ITP-00', '').replace('ITP-0', '').replace('ITP-', ''));
                style = yellow_star_marker;
            }
            else if ((feature.get('clear') == 'n' && feature.get('uxo') != 'x') || (feature.get('clear') == 'n' && feature.get('uxo') == null)) {
                empty_circle_marker.getText().setText(feature.get('itp_no_mag').replace('ITP-0000', '').replace('ITP-000', '').replace('ITP-00', '').replace('ITP-0', '').replace('ITP-', ''));
                style = empty_circle_marker;
            }
            else if (feature.get('clear') == 'n' && feature.get('uxo') == 'x') {
                empty_star_marker.getText().setText(feature.get('itp_no_mag').replace('ITP-0000', '').replace('ITP-000', '').replace('ITP-00', '').replace('ITP-0', '').replace('ITP-', ''));
                style = empty_star_marker;
            }
            else {
                empty_circle_marker.getText().setText(feature.get('itp_no_mag').replace('ITP-0000', '').replace('ITP-000', '').replace('ITP-00', '').replace('ITP-0', '').replace('ITP-', ''));
                style = empty_circle_marker;
            }
        }

        /*if(feature.get('to_detonate') == 'y'){
            if(feature.get('detonated') == 'n' || feature.get('detonated') == '' || feature.get('detonated') == null){
                safety_dist = feature.get('safety_dist') || 0;
                console.log('Safety distance:', safety_dist);
                console.log('Resolution:', resolution);
                const safety_radius  = new ol.style.Style({
                    image: new ol.style.Circle({
                        radius: 1.75 * safety_dist / resolution,
                        stroke: new ol.style.Stroke({
                            color: 'rgba(255,165,0,1.0)',
                            width: 2,
                        }),
                        fill: new ol.style.Fill({
                            color: 'rgba(255,165,0,0.2)',
                        }),
                    }),
                });
                orange_circle_marker.getText().setText(feature.get('itp_no_mag').replace('ITP-0000', '').replace('ITP-000', '').replace('ITP-00', '').replace('ITP-0', '').replace('ITP-', ''));
                style = [orange_circle_marker, safety_radius];
            }
        }*/

        if(target_filters.found == 'y'){
            if(feature.get('found') == 'n' || feature.get('found') == '' || feature.get('found') == null)
                style = new ol.style.Style({});
        }
        else if(target_filters.found == 'n'){
            if(feature.get('found') != 'n')
                style = new ol.style.Style({});
        }

        if(target_filters.recovered == 'y'){
            if(feature.get('salvaged') == 'n' || feature.get('salvaged') == 'w' || feature.get('salvaged') == '' || feature.get('salvaged') == null)
                style = new ol.style.Style({});
        }
        else if(target_filters.recovered == 'w'){
            if(feature.get('salvaged') == 'n' || feature.get('salvaged') == 'y' || feature.get('salvaged') == '' || feature.get('salvaged') == null)
                style = new ol.style.Style({});
        }
        else if(target_filters.recovered == 'n'){
            if(feature.get('salvaged') == 'y' || feature.get('salvaged') == 'w')
                style = new ol.style.Style({});
        }

        if(target_filters.uxo == 'y'){
            if(feature.get('uxo') == '' || feature.get('uxo') == null)
                style = new ol.style.Style({});
        }
        else if(target_filters.uxo == 'n'){
            if(feature.get('uxo') == 'x')
                style = new ol.style.Style({});
        }

        if(target_filters.clear == 'y'){
            if(feature.get('clear') == 'n' || feature.get('clear') == 'w' || feature.get('clear') == '' || feature.get('clear') == null)
                style = new ol.style.Style({});
        }
        else if(target_filters.clear == 'w'){
            if(feature.get('clear') == 'n' || feature.get('clear') == 'y' || feature.get('clear') == '' || feature.get('clear') == null)
                style = new ol.style.Style({});
        }
        else if(target_filters.clear == 'n'){
            if(feature.get('clear') == 'y' || feature.get('clear') == 'w')
                style = new ol.style.Style({});
        }

        if(target_filters.qa_clear == 'y'){
            if(feature.get('qa_clear') == 'n' || feature.get('qa_clear') == '' || feature.get('qa_clear') == null)
                style = new ol.style.Style({});
        }
        else if(target_filters.qa_clear == 'n'){
            if(feature.get('qa_clear') == 'y')
                style = new ol.style.Style({});
        }
        
        if(target_filters.to_do == 'y'){
            if(feature.get('todo_target') == 'f' || feature.get('todo_target') == 'n' || feature.get('todo_target') == '' || feature.get('todo_target') == null)
                style = new ol.style.Style({});
        }
        else if(target_filters.to_do == 'n'){
            if(feature.get('todo_target') == 'x')
                style = new ol.style.Style({});
        }

        if(target_filters.prio == '1' && target_filters.prio == '2'){
            if(feature.get('prio') != '1' && feature.get('priority') != '2')
                style = new ol.style.Style({});
        }
        else if(target_filters.prio == '1'){
            if(feature.get('prio') != '1')
                style = new ol.style.Style({});
        }
        else if(target_filters.prio == '2'){
            if(feature.get('prio') != '2')
                style = new ol.style.Style({});
        }
        
        return style;
    }
}

const itp_styleFunctionVessels = function (clusters, resolution) {
    const features = clusters.get('features');
    var size = 0;
    if (features) {
        size = features.length;
    }
    if (size > 1 /*&& resolution > 0.3*/) {
        style = new ol.style.Style({
            image: new ol.style.Circle({
                radius: 10,
                fill: new ol.style.Fill({
                    color: 'rgba(0, 255, 0, 0.5)',
                }),
            }),
            text: new ol.style.Text({
                text: features.map(f => f.get('itp_no_mag').replace('ITP-0000', '').replace('ITP-000', '').replace('ITP-00', '').replace('ITP-0', '').replace('ITP-', '')).join(',\n'),
                fill: new ol.style.Fill({
                    color: 'black',
                }),
            }),
        });
        return style;
    } else {
        const feature = features[0];
        let style = new ol.style.Style({});
        const itp_no_mag = feature.get('itp_no_mag').replace('ITP-0000', '').replace('ITP-000', '').replace('ITP-00', '').replace('ITP-0', '').replace('ITP-', '');
        const clear = feature.get('clear');
        const uxo = feature.get('uxo');
        const vessel = feature.get('vessel');
        const todo_target = feature.get('todo_target');

        const setTextAndReturnStyle = (marker, text) => {
            marker.getText().setText(text);
            return marker;
        }

        let circle_marker, star_marker;

        if (feature.get('itp_no_mag').startsWith('SSS-')) {
            if (clear === 'y') {
                style = setTextAndReturnStyle(green_square_marker, itp_no_mag);
            } else {
                style = setTextAndReturnStyle(orange_square_marker, itp_no_mag);
            }
        } else {
            if (clear === 'y') {
                circle_marker = green_circle_marker;
                star_marker = green_star_marker;
            } else {
                if (vessel === 'Kamara') {
                    circle_marker = blue_circle_marker;
                    star_marker = blue_star_marker;
                } else if (vessel === 'RS Sentinel') {
                    circle_marker = purple_circle_marker;
                    star_marker = purple_star_marker;
                } else {
                    circle_marker = red_circle_marker;
                    star_marker = red_star_marker;
                }
            }

            if (todo_target === 'x') {
                if ((clear === 'y' && !uxo) || (clear === 'y' && uxo === '')) {
                    style = setTextAndReturnStyle(circle_marker, itp_no_mag);
                } else if (clear === 'y' && uxo === 'x') {
                    style = setTextAndReturnStyle(star_marker, itp_no_mag);
                } else if ((clear === 'w' && !uxo) || (clear === 'w' && uxo === '')) {
                    style = setTextAndReturnStyle(circle_marker, itp_no_mag);
                } else if (clear === 'w' && uxo === 'x') {
                    style = setTextAndReturnStyle(star_marker, itp_no_mag);
                } else if ((clear === 'n' && !uxo) || (clear === 'n' && uxo === '')) {
                    style = setTextAndReturnStyle(circle_marker, itp_no_mag);
                } else if (clear === 'n' && uxo === 'x') {
                    style = setTextAndReturnStyle(star_marker, itp_no_mag);
                } else {
                    style = setTextAndReturnStyle(circle_marker, itp_no_mag);
                }
            } else {
                if ((clear === 'y' && !uxo) || (clear === 'y' && uxo === '')) {
                    style = setTextAndReturnStyle(circle_marker, itp_no_mag);
                } else if (clear === 'y' && uxo === 'x') {
                    style = setTextAndReturnStyle(star_marker, itp_no_mag);
                } else if ((clear === 'w' && !uxo) || (clear === 'w' && uxo === '')) {
                    style = setTextAndReturnStyle(circle_marker, itp_no_mag);
                } else if (clear === 'w' && uxo === 'x') {
                    style = setTextAndReturnStyle(star_marker, itp_no_mag);
                } else if ((clear === 'n' && !uxo) || (clear === 'n' && uxo === '')) {
                    style = setTextAndReturnStyle(circle_marker, itp_no_mag);
                } else if (clear === 'n' && uxo === 'x') {
                    style = setTextAndReturnStyle(star_marker, itp_no_mag);
                } else {
                    style = setTextAndReturnStyle(circle_marker, itp_no_mag);
                }
            }
        }

        // Apply target_filters logic
        if (target_filters.found === 'y') {
            if (!feature.get('found') || feature.get('found') === 'n')
                style = new ol.style.Style({});
        } else if (target_filters.found === 'n') {
            if (feature.get('found') !== 'n')
                style = new ol.style.Style({});
        }

        if (target_filters.recovered === 'y') {
            if (!feature.get('salvaged') || feature.get('salvaged') === 'n' || feature.get('salvaged') === 'w')
                style = new ol.style.Style({});
        } else if (target_filters.recovered === 'w') {
            if (!feature.get('salvaged') || feature.get('salvaged') === 'n' || feature.get('salvaged') === 'y')
                style = new ol.style.Style({});
        } else if (target_filters.recovered === 'n') {
            if (feature.get('salvaged') === 'y' || feature.get('salvaged') === 'w')
                style = new ol.style.Style({});
        }

        if (target_filters.uxo === 'y') {
            if (!feature.get('uxo'))
                style = new ol.style.Style({});
        } else if (target_filters.uxo === 'n') {
            if (feature.get('uxo') === 'x')
                style = new ol.style.Style({});
        }

        if (target_filters.clear === 'y') {
            if (!feature.get('clear') || feature.get('clear') === 'n' || feature.get('clear') === 'w')
                style = new ol.style.Style({});
        } else if (target_filters.clear === 'w') {
            if (!feature.get('clear') || feature.get('clear') === 'n' || feature.get('clear') === 'y')
                style = new ol.style.Style({});
        } else if (target_filters.clear === 'n') {
            if (feature.get('clear') === 'y' || feature.get('clear') === 'w')
                style = new ol.style.Style({});
        }

        if (target_filters.qa_clear === 'y') {
            if (!feature.get('qa_clear') || feature.get('qa_clear') === 'n')
                style = new ol.style.Style({});
        } else if (target_filters.qa_clear === 'n') {
            if (feature.get('qa_clear') === 'y')
                style = new ol.style.Style({});
        }

        if (target_filters.to_do === 'y') {
            if (!feature.get('todo_target') || feature.get('todo_target') === 'f' || feature.get('todo_target') === 'n')
                style = new ol.style.Style({});
        } else if (target_filters.to_do === 'n') {
            if (feature.get('todo_target') === 'x')
                style = new ol.style.Style({});
        }

        return style;
    }
}

const vessel_styleFunction = function (feature){
    style = new ol.style.Style({
        image: new ol.style.RegularShape({
            radius: 6,
            points: 4,
            fill: new ol.style.Fill({
                color: 'rgba(0, 0, 255, 1)',
            }),
        }),
        text: 
            new ol.style.Text({
                text: feature.get('ship_name').toString(),
                font: 'bold 11px "Open Sans", "Arial Unicode MS", "sans-serif"',
                placement: 'point',
                offsetX: 0,
                offsetY: -15,
                stroke: new ol.style.Stroke({color: '000', width: 0.4}),
            }),
    });
    return style;
}
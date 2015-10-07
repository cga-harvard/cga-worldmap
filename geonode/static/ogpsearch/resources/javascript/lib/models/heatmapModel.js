
if (typeof OpenGeoportal === 'undefined')
{
    OpenGeoportal = {};
}
if (typeof OpenGeoportal.Models === 'undefined')
{
    OpenGeoportal.Models = {};
}



OpenGeoportal.Models.Heatmap = Backbone.Model.extend(
    {

        initialize: function()
        {
            that = this;
	    // add listener for seach events
	    //that.backgroundLayer = new OpenLayers.Layer.Stamen("toner-lite");
	    //OpenGeoportal.ogp.map.addLayer(that.backgroundLayer);
	    //var googleBasemap = OpenGeoportal.ogp.map.getLayersByName("Google Physical")[0];
	    //OpenGeoportal.ogp.map.removeLayer(googleBasemap);

	    OpenGeoportal.Models.Heatmap.radiusAdjust = 1.1;  // scales all heatmap circles
            jQuery(document).on("fireSearch", function()
                {
                    that.handleHeatmap(that);
                });
	    jQuery(document).trigger("fireSearch");
        },
        fetchOn: false,
        searcher: function() {return OpenGeoportal.ogp.search;},

	/*
	   return the url that supplies data for the model
	   url is the same as the last Solr query with an area filter added
	*/
        url: function()
            {
                searcher = OpenGeoportal.ogp.appState.get("queryTerms");
                solr = searcher.getSearchSolrObject();
                solr.enableHeatmap();
                solr.addFilter(solr.createNonGlobalAreaFilter());
                solr.addFilter(solr.createOriginFilter());
                url = solr.getURL();
		        return url;
	    },
	/*
	  called by listener on search change, uses backbone fetch
	*/
	handleHeatmap: function(that)
	{
	    this.deleteHeatmapLayer(this);  // delete quickly to get heatmap off of UI
	    this.fetch({dataType: "jsonp", jsonp: "json.wrf",
			reset: true,
			complete: function(dataObj, success)
			{
			    foo = dataObj;
			    var facetCounts = dataObj.responseJSON.facet_counts;
			    if (facetCounts != null)
				{
				    var facetHeatmaps = facetCounts.facet_heatmaps;
				    bbox_rpt = facetHeatmaps.bbox_rpt;
				    that.drawHeatmapOpenLayers(that, bbox_rpt);
				}
			}});
	},
	/*
	  a new OpenLayers layer object is created every time since its color bands change
	*/
	deleteHeatmapLayer: function(that)
	{
	    try
	    {
		if (that.heatmapLayer != null)
		{
		    OpenGeoportal.ogp.map.removeLayer(that.heatmapLayer);
		    that.heatmapLayer = null;
		}
	    }
	    catch (err)
	    {
		;
	    }
	},

	/*
	  we use a black and white stamen layer so heatmap colors aren't distorted
	  setting the background layer should not be done elsewhere
	*/
	initBackgroundLayer: function(that)
	{
	    if (that.backgroundLayer == null)
	    {
		// hack to set background layer for evaluation
		that.backgroundLayer = new OpenLayers.Layer.Stamen("toner-lite");
		OpenGeoportal.ogp.map.addLayer(that.backgroundLayer);
	    }

	},

	/**
	  create layer with move move listener to display number of documents in cell as a tool tip
	*/
	initHeatmapLayer: function(that)
	{
	    heatmapLayer = new Heatmap.Layer("Heatmap");
	    jQuery("#map").attr("title", "Number of layers =     ");
	    jQuery("#map").tooltip({track: true});
	    OpenGeoportal.ogp.map.events.register("mousemove", OpenGeoportal.ogp.map,
						  function(event) {that.processEvent(that, event);},
						  true);
	    return heatmapLayer;

	},

	// when the user moves the mouse we note how may documents are under the cursor
	processEvent: function(that, event)
	{
	    foo = event;
	    pixel = event.xy;
	    mercator = OpenGeoportal.ogp.map.getLonLatFromViewPortPx(pixel);
	    epsg4326 = new OpenLayers.Projection("EPSG:4326");
	    epsg900913 = new OpenLayers.Projection("EPSG:900913");
	    point = mercator.transform(epsg900913, epsg4326);
	    count = that.getCountGeodetic(that.lastHeatmapObject, point.lat, point.lon);
	    if (count < 0) count = 0;
	    message = "Number of layers = " + count;
	    jQuery("#map").tooltip( "option", "content", message );
	},

	getCountGeodetic: function(heatmapObject, latitude, longitude)
	{
	    var heatmap = heatmapObject[15];
	    if (heatmap == null)
		return;
	    var minimumLatitude = heatmapObject[11];
	    var maximumLatitude = heatmapObject[13];
	    var deltaLatitude = maximumLatitude - minimumLatitude;
	    var minimumLongitude = heatmapObject[7];
	    var maximumLongitude = heatmapObject[9];
	    var deltaLongitude = maximumLongitude - minimumLongitude;

	    var stepsLatitude = heatmap.length;
	    var stepsLongitude = heatmap[0].length;
	    var stepSizeLatitude = deltaLatitude / stepsLatitude;
	    var stepSizeLongitude = deltaLongitude / stepsLongitude;

	    var latitudeIndex = Math.floor((latitude - minimumLatitude) / stepSizeLatitude);
	    var longitudeIndex = Math.floor((longitude - minimumLongitude) / stepSizeLongitude);

	    if (latitudeIndex < 0) latitudeIndex = 0;
	    if (longitudeIndex < 0) longitudeIndex = 0;
	    try
	    {
		var heatmapValue = heatmap[heatmap.length - latitudeIndex - 1][longitudeIndex];
		return heatmapValue;
	    }
	    catch (err)
	    {
		console.log("error in getCount with lat = " + latitude + ", lon = " + longitude);
		console.log("  lat index = " + latitudeIndex + ", lon index = " + longitudeIndex);
		return heatmap[0][0];
	    }
	},

	flattenValues: function(heatmap)
	{
	    tmp = [];
	    for (i = 0 ; i < heatmap.length ; i++)
		tmp.push.apply(tmp, heatmap[i]);
	    return tmp;
	},

	/**
	  uses a Jenks algorithm with 5 classifications
	  the library supports many more options
	*/
	getClassifications: function(that, heatmap)
	{
	    flattenedValues = that.flattenValues(heatmap);
            series = new geostats(flattenedValues);

            jenksClassifications = series.getClassJenks(this.getColors().length);
	    for (var i = 0 ; i < jenksClassifications.length ; i++)
	    {
		if (jenksClassifications[i] < 0)
		    jenksClassifications[i] = 0;
	    }
      jenksClassifications = that.cleanupClassifications(jenksClassifications);
	    return jenksClassifications;
	},

  cleanupClassifications: function(classifications)
          {
              // classifications with multiple 0 can cause problems
              var lastZero = classifications.lastIndexOf(0);
              if (lastZero == -1)    // does the array have a zero
                  return classifications;    // if not, nothing to do
              var newClassifications = classifications.slice(lastZero, classifications.length);
              return newClassifications;
          },


	getColors: function()
	{
            //var colors = [0x00000000, 0xfef0d9ff, 0xfdcc8aff, 0xfc8d59ff, 0xe34a33ff, 0xb30000ff];
	    var colors = [0x00000000, 0x0000dfff, 0x00effeff, 0x00ff42ff, 0xfeec30ff, 0xff5f00ff, 0xff0000ff];
	    return colors;
	},

	/*
	  convert Jenks classifications to Brewer colors
	*/
	getColorGradient: function(that, classifications)
	{

	    colors = this.getColors();
            colorGradient = {};
            for (var i = 0 ; i < classifications.length ; i++)
	    {
		value = classifications[i];
		scaledValue = that.rescaleHeatmapValue(value, jenksClassifications[0], maxValue);
		if (scaledValue < 0)
		    scaledValue = 0;
		colorGradient[scaledValue] = colors[i];
	    }
	    return colorGradient;
	},

	/*
	  scale return value between 0 and 1
	 */
	rescaleHeatmapValue: function(value, min, max)
	{
	    if (value == null)
		return 0;
	    if (value == -1)
		return -1;
	    if (value == 0)
		return 0;
	    value = value * 1.0;
	    return value / max;
	},

	/**
	   radius of heatmap point depends on how many pixels are between adjacent points
	*/
	computeRadius: function(latitude, longitude, latitudeStepSize, longitudeStepSize)
	{
	    mercator1 = OpenGeoportal.ogp.map.WGS84ToMercator(longitude, latitude);
	    pixel1 = OpenGeoportal.ogp.map.getPixelFromLonLat(mercator1);
	    mercator2 = OpenGeoportal.ogp.map.WGS84ToMercator(longitude + longitudeStepSize, latitude + latitudeStepSize);
	    pixel2 = OpenGeoportal.ogp.map.getPixelFromLonLat(mercator2);
	    deltaLatitude = Math.abs(pixel1.x - pixel2.x);
	    deltaLongitude = Math.abs(pixel1.y - pixel2.y);
	    delta = Math.max(deltaLatitude, deltaLongitude);
	    return Math.ceil(delta / 2.);
	},

	/**
	   to improve the heatmap display we slightly adjust the radius of heatmap points based on zoom level.
	   these factos are computed by eyeballing the results and tweaking
	 */
	getRadiusFactor: function()
	{
	    var factor = [1.6, 1.5, 2.6, 2.4, 2.2, 1.8, 2., 2., 2.];
	    var zoomLevel = OpenGeoportal.ogp.map.getZoom();
	    if (zoomLevel <1)
		return 1;
	    var index = zoomLevel - 1;
	    if (index > factor.length - 1)
		return factor[factor.length - 1];
	    var value = factor[index];
	    return value;
	},
	/**
	   return the largest and smallest value in the heatmap so its values can be scaled
	   some elements in the heatmap can be null, this function replaces the nulls
	*/
	heatmapMinMax: function (heatmap, stepsLatitude, stepsLongitude)
	{
	    var max = -1;
	    var min = Number.MAX_VALUE;
	    for (i = 0 ; i < stepsLatitude ; i++)
	    {
		var currentRow = heatmap[i];
		if (currentRow == null)  heatmap[i] = currentRow = [];
		for (j = 0 ; j < stepsLongitude ; j++)
		{
		    if (currentRow[j] == null)
			currentRow[j] = -1;
		    if (currentRow[j] > max)
			max = currentRow[j];
		    if (currentRow[j] < min && currentRow[j] > -1)
			min = currentRow[j];
		}
	    }
	    return [min, max];
	},


	/**
	   the heatmap object is an array
	   it has fields for the count array as well as the extent and step sizes
	 */
	drawHeatmapOpenLayers: function(that, heatmapObject)
	{
	    that.lastHeatmapObject = heatmapObject;
	    that.deleteHeatmapLayer(that);
	    //that.initBackgroundLayer(that);
	    that.heatmapLayer = that.initHeatmapLayer(that);
	    that.heatmapLayer.points = [];  //delete any previously added points
	    // get components returned by Solr
	    heatmap = heatmapObject[15];
	    if (heatmap == null)
		return;
	    stepsLatitude = heatmapObject[5];  //heatmap.length;
	    stepsLongitude = heatmapObject[3];   //heatmap[0].length;

	    minMaxValue = that.heatmapMinMax(heatmap, stepsLatitude, stepsLongitude);
	    //ceilingValues = getCeilingValues(heatmap);
	    minValue = minMaxValue[0];
	    maxValue = minMaxValue[1];
	    if (maxValue == -1) return;  // something wrong

	    var minimumLatitude = heatmapObject[11];
	    var maximumLatitude = heatmapObject[13];
	    var deltaLatitude = maximumLatitude - minimumLatitude;
	    var minimumLongitude = heatmapObject[7];
	    var maximumLongitude = heatmapObject[9];
	    var deltaLongitude = maximumLongitude - minimumLongitude;

	    var stepSizeLatitude = deltaLatitude / stepsLatitude;
	    var stepSizeLongitude = deltaLongitude / stepsLongitude;

	    that.classifications = that.getClassifications(that, heatmap);
	    var colrGradient = that.getColorGradient(that, that.classifications);
	    that.heatmapLayer.setGradientStops(colorGradient);

	    for (var i = 0 ; i < stepsLatitude ; i++)
	    {
		for (var j = 0 ; j < stepsLongitude ; j++)
		{
		    try
		    {
			heatmapValue = heatmap[heatmap.length - i - 1][j];
			currentLongitude = minimumLongitude + (j * stepSizeLongitude) + (.5 * stepSizeLongitude);
			currentLatitude = minimumLatitude + (i * stepSizeLatitude) + (.5 * stepSizeLatitude)
			radius = that.computeRadius(currentLatitude, currentLongitude, stepSizeLatitude, stepSizeLongitude);;
			mercator = OpenGeoportal.ogp.map.WGS84ToMercator(currentLongitude, currentLatitude);
			scaledValue = that.rescaleHeatmapValue(heatmapValue, that.classifications[1], maxValue);
			radiusFactor = this.getRadiusFactor();
			if (heatmapValue > 0)
			{
			    heatmapLayer.addSource(new Heatmap.Source(mercator, radius*radiusFactor*OpenGeoportal.Models.Heatmap.radiusAdjust, scaledValue));
			}
		    }
		    catch (error)
		    {
			console.log("error making heatmap: " + error);
		    }
		}
	    }
	    that.heatmapLayer.setOpacity(0.50);
	    OpenGeoportal.ogp.map.addLayer(that.heatmapLayer);
	}
    }

);

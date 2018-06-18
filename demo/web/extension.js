(function ($) {
    if ($.QueryString)
        return;
    var reviewCount = 5;
    var chosenColor = "#FFBF80";
    var isClick = Array(reviewCount)
    for (var i = 0;i < reviewCount;i++)
    	isClick[i] = 0;
    var plzWait = "评论正在生成请稍后...";
	function init_container()
	{
		var controls = {
			panelBody: null, refresh: null, submit: null, textArea: null,
			clear: null, showImg: null,
	    };
	    var ansRequestId = "";

	    function requestReviews()
	    {
	    	let ws = new WebSocket ("ws://localhost:34567")
		    ws.onmessage = function(event) {
			  	var msg = event.data.split(/magic/g);
			  	for(var i = 0;i < reviewCount;i++)
	    		{
	    			reviews[i].text(msg[i]);
	    		}
			  	ws.close();
			};
		    ws.onopen = function () {
		        ws.send("reviews " + ansRequestId);
		    };
	    }

	    function showimage(filePath){  
            fileFormat = filePath.substring(filePath.lastIndexOf(".")).toLowerCase();
        	if (fileFormat.match(/.png|.jpg|.jpeg/)) {  
  				controls.showImg.attr('src',filePath);
        	}
		}

	    function requestId(itemName) {
		    let ws = new WebSocket ("ws://localhost:34567")
		    ws.onmessage = function(event) {
			  	ansRequestId = event.data;
			  	requestReviews();
			  	ws.close();
			};
		    ws.onopen = function () {
		    	showimage(itemName);
		        ws.send("id " + encodeURI(itemName));
		    };
		}

	    for (var i in controls)
	    {
	        controls[i] = $("#" + i);
	    }
	    ctrlBar = controls.panelBody;
	    controls.refresh.click(function() {
	    	for(var i = 0;i < reviewCount;i++)
	    	{
	    		reviews[i].text(plzWait);
	    	}
    		if (ansRequestId != "")
    			requestReviews();
    		for(var i = 0;i < reviewCount;i++)
    		{
    			isClick[i] = 0;
    			reviews[i].css("background-color", "#ffffff");
    		}
	    })
	    controls.submit.click(function() {
	    	for(var i = 0;i < reviewCount;i++)
	    	{
	    		reviews[i].text(plzWait);
	    	}
	    	if (controls.textArea.val() != "") requestId(controls.textArea.val());
    		for(var i = 0;i < reviewCount;i++)
    		{
    			isClick[i] = 0;
    			reviews[i].css("background-color", "#ffffff");
    		}
	    })
	    controls.clear.click(function() {
	    	controls.textArea.val("");
	    	controls.showImg.attr('src',"");
	    	ansRequestId = "";
	    	for(var i = 0;i < reviewCount;i++)
	    	{
	    		reviews[i].text(plzWait);
	    	}
	    })
	    var reviews = new Array(reviewCount);
	    for(var i = 0;i < reviewCount;i++)
	    {
	    	reviews[i] = $("#review" + i.toString(10));
	    }
	    for(var i = 0;i < reviewCount;i++)
	    {
	    	reviews[i].text(plzWait);
	    	reviews[i].attr("self", i);
	    	reviews[i].click(function()
		    {
		    	for(var i = 0;i < reviewCount;i++)
		    		if (isClick[i] == 1)
		    		{
		    			isClick[i] = 0;
		    			reviews[i].css("background-color", "#ffffff");
		    		}
		    	isClick[$(this).attr("self")] = 1;
		    	$(this).css("background-color", chosenColor);
		    });
		    reviews[i].hover(function()
		    {
		    	$(this).css("background-color", chosenColor);
		    },function()
		    {
		    	if (isClick[$(this).attr("self")] == 0)
		    		$(this).css("background-color", "#ffffff");
		    });
	    }
	}
	$(document).ready(function () {init_container()});
})(jQuery);
(function ($) {
    if ($.QueryString)
        return;
    var reviewCount = 5;
    var chosenColor = "#FFBF80";
    var isClick = Array(reviewCount)
    for (var i = 0;i < reviewCount;i++)
    	isClick[i] = 0;
    var plzWait = "评论正在生成请稍后...";
	function init_container(container)
	{
		var controls = {
			btnHide: null, panelBody: null, formBody: null, refresh: null
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

	    function requestId(itemName) {
		    let ws = new WebSocket ("ws://localhost:34567")
		    ws.onmessage = function(event) {
			  	ansRequestId = event.data;
			  	requestReviews();
			  	ws.close();
			};
		    ws.onopen = function () {
		        ws.send("id " + itemName);
		    };
		}

	    for (var i in controls)
	    {
	        controls[i] = container.find("#" + i);
	    }
	    ctrlBar = controls.panelBody;
	    controls.btnHide.click(function() {
	        if ($(this).data("hide")) {
	            $(this).text("隐藏好评机器人");
	            ctrlBar.slideDown();
	            $(this).data("hide", false);
	        }
	        else {
	            $(this).text("显示好评机器人");
	            ctrlBar.slideUp();
	            $(this).data("hide", true);
	        }
	    });
	    controls.refresh.click(function() {
    		requestReviews();
    		for(var i = 0;i < reviewCount;i++)
    		{
    			isClick[i] = 0;
    			reviews[i].css("background-color", "#ffffff");
    		}
	    })
	    var reviews = new Array(reviewCount);
	    for(var i = 0;i < reviewCount;i++)
	    	reviews[i] = container.find("#review" + i.toString(10));
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
		    	$('textarea').filter(function() {
			        return this.name.match(/RateContents/);
			    }).text($(this).text());
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
	    container.slideDown();
	    requestId("没准过");
	}

	$("body").append("<div id=\"extension\"></div>");
	$("#extension").load(chrome.extension.getURL('panel.html'), function(responseTxt,statusTxt,xhr){
	    if(statusTxt=="success")
	    {
	    	init_container($("#extension"))
	    }
	    if(statusTxt=="error")
	     	alert("Error: " + xhr.status + ": " + xhr.statusText);
  	});
    // 底部的空间
    $('body').css({ marginBottom: "250px" });
})(jQuery);
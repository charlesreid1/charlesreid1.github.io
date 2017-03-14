window.app = {  
  models: {},
  collections: {},
  views: {},
  routers: {},
  init: function() {    
    app.routers.main = new app.routers.MainRouter();
    // Enable pushState for compatible browsers
    var enablePushState = true;
    // Disable for older browsers
    var pushState = !!(enablePushState && window.history && window.history.pushState);
    // Start **Backbone History**
    Backbone.history = Backbone.history || new Backbone.History({});
    Backbone.history.start({
      pushState:pushState
    });
  }
};

// Define routes
app.routers.MainRouter = Backbone.Router.extend({

  routes: {
    'subway/': 'transitAdd',
    'subway/?*queryString': 'transitAdd'
  },
  
  home: function(){
    app.views.main = new app.views.HomeView({});
  },
  
  transitAdd: function(params){
    params = helper.parseQueryString(params);
    $.getJSON( "brian.json", function(data) {
      console.log('got json');
      params = $.extend({}, config, params, data);
      app.views.main = new app.views.TransitAddView(params);
    });   
  },
  
  transitEdit: function(id){
    var map = null;
    app.views.main = new app.views.TransitAddView({model: map});
  }, 
  
  transitShow: function(id){
    var map = null;
    app.views.main = new app.views.TransitShowView({model: map});
  }

});

// Init backbone app
$(document).ready(function(){
  app.init();
});

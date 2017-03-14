var ng;
dir = [];

// hipster jesus api
// for some hipster ipsum
var hipster_ipsum = function(N,tagname) {
    $.getJSON('http://hipsterjesus.com/api?paras='+N+'&html=true', function(data) {
        $(tagname).html( data.text );
    });
};

ng = a.directive('projectt', function() {

    function link(scope, element, attr) {
        var el = element[0];




        // Build a fucking sandcastle

        var div = $("<div />");

        var img = $("<img />", {
            "src" : "http://placehold.it/100x100",
            "class" : "image"
        }).appendTo(div);






        angular.element(el).append(div);
    }
    return {
        restrict: "E",
        link: link,
        scope: {}
    }
});
dir.push(ng);


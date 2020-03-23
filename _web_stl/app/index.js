import "./prepareJquery";
import "./prepareTabulator";
import "./prepareSprintf";
import "./prepareThree";
import "three/examples/js/controls/TrackballControls.js";
import "three/examples/js/loaders/STLLoader.js";
import "./prepareThreeAnnotator";

import "../css/construction.css"

$(() => {
    import("../js/init")
    // Prohibit file drag & drop.
    window.addEventListener('dragover', function(ev){
        ev.preventDefault();
    }, false);
    window.addEventListener('drop', function(ev){
        ev.preventDefault();
        ev.stopPropagation();
    }, false);

    $('.subMenu').hide();
    $('#menu .archive').click(function(e){
        $('+ul.subMenu',this).slideToggle();
    });

});


document.addEventListener('DOMContentLoaded', function() {
  setupTextAreaResize();
  setupSvgDrawing();
});

function autoresizeTextarea(textarea) {
    if (textarea == null) {
      return;
    }

    textarea.style.height = 'auto'; // Reset the height
    textarea.style.height = textarea.scrollHeight + 'px'; // Set the height
  }

function setupTextAreaResize() {
  const textarea = document.getElementById('content');

  if (textarea == null) {
    return;
  }

  autoresizeTextarea(textarea);

  // Adjust the textarea on input
  document.getElementById('content').addEventListener('input', function() {
    autoresizeTextarea(this);
  });
}

// Code for free drawing SVGs adapted from https://codepen.io/adrgautier/pen/VvPJbe
function setupSvgDrawing() {
  const strokeWidth = 2;
    const SVG = document.getElementById("SVG");
    
    function createPencil() {
        let pencilCoordinates;
        let pencilVelocity;
        let pencilInUse;
    
        window.addEventListener("mousemove", function(e) {
            const rect = SVG.getBoundingClientRect();
          
            nextPencilCoordinates = {
                x: e.pageX - rect.left,
                y: e.pageY - rect.top
            };
          
            if(!pencilCoordinates) {
              pencilCoordinates = nextPencilCoordinates;
            }
        
            const pencilXDelta = nextPencilCoordinates.x - pencilCoordinates.x;
            const pencilYDelta = nextPencilCoordinates.y - pencilCoordinates.y;
            pencilVelocity = Math.sqrt(Math.pow(pencilXDelta,2)+Math.pow(pencilYDelta,2));
            pencilCoordinates = nextPencilCoordinates;
        })
      
        window.addEventListener("touchmove", function(e) {
            const rect = SVG.getBoundingClientRect();
    
            nextPencilCoordinates = {
                x: e.clientX||e.touches[0].clientX - rect.left,
                y: e.clientY||e.touches[0].clientY - rect.top
            };
          
            if(!pencilCoordinates) {
                pencilCoordinates = nextPencilCoordinates;
            }
         
            const pencilXDelta = nextPencilCoordinates.x - pencilCoordinates.x;
            const pencilYDelta = nextPencilCoordinates.y - pencilCoordinates.y;
            pencilVelocity = Math.sqrt(Math.pow(pencilXDelta,2)+Math.pow(pencilYDelta,2));
            pencilCoordinates = nextPencilCoordinates;
        })
    
        return {
            getPencilCoordinates: function() {
                return pencilCoordinates;
            },
            getPencilVelocity: function() {
                return pencilVelocity;
            },
            getPencilRefreshRate: function() {
                const invVelocity = 1 / ((pencilVelocity > 1) ? pencilVelocity : 1);
                const refreshRate = invVelocity * 80 * (strokeWidth / 50);
                // above computation can definitely be improved
                return refreshRate;
            },
            isPencilUsed: function() {
                return pencilInUse;
            },
            usePencil: function() {
                pencilInUse = true;
            },
            leavePencil: function() {
                pencilInUse = false;
                pencilCoordinates = undefined;
            }
        }
    }
    
    function createPath() {
        const path = document.createElementNS('http://www.w3.org/2000/svg', 'path');
        const pencilCoordinates = pencil.getPencilCoordinates();
        path.setAttribute("fill","none");
        path.setAttribute("stroke","#000");
        path.setAttribute("stroke-width",strokeWidth);
        path.setAttribute("d","M"+pencilCoordinates.x+" "+pencilCoordinates.y);
        SVG.appendChild(path);
        return path;
    }
    
    function completePath(path) {
        const pencilCoordinates = pencil.getPencilCoordinates();
        let d = path.getAttribute("d");
        d += " L"+pencilCoordinates.x+" "+pencilCoordinates.y;
        path.setAttribute("d",d);
    
        const pencilRefreshRate = pencil.getPencilRefreshRate();
        if(pencil.isPencilUsed()) {
            setTimeout(completePath, pencilRefreshRate, path);
        }
    }
    
    const pencil = createPencil();
    
    SVG.addEventListener("mousedown", function(){
        const path = createPath();
    
        const pencilRefreshRate = pencil.getPencilRefreshRate();
    
        pencil.usePencil();
        pencilTimemout = setTimeout(completePath, pencilRefreshRate, path)
        
    });
    
    SVG.addEventListener("mouseup", function(){
        pencil.leavePencil();
    });
    
    SVG.addEventListener("touchstart", function(){
        setTimeout(function() {
          const path = createPath();
    
          const pencilRefreshRate = pencil.getPencilRefreshRate();
    
          pencil.usePencil();
          pencilTimemout = setTimeout(completePath, pencilRefreshRate, path)
        }, 100);    
    });
    
    SVG.addEventListener("touchend", function(){
        pencil.leavePencil();
    });
}


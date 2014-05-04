var myCodeMirror;

function GetQueryStringParams(sParam)
    {
    var sPageURL = window.location.search.substring(1);
    var sURLVariables = sPageURL.split('&');
    for (var i = 0; i < sURLVariables.length; i++)
      {
        var sParameterName = sURLVariables[i].split('=');
        if (sParameterName[0] == sParam)
        {
            return sParameterName[1];
        }
      }
    }

function s(e) {
    alert('toto');
}
function outf(text) {
   var mypre = document.getElementById("output");
   mypre.innerHTML = mypre.innerHTML + text;
}


function builtinRead(x)
{
    
	if (Sk.builtinFiles === undefined || Sk.builtinFiles["files"][x] === undefined){
        //alert('tentative de recuperer le code skulpt de debug du module '+x);
		$.ajax({
            url: "http://mrt2.no-ip.org/skulpt/plugins/"+x+"/__init__.js",
            context: document.body
        }).done(function(data) {
            alert(data);
		    Sk.builtinFiles["files"][x] = data;
            return Sk.builtinFiles["files"][x];
	    }).error(function(data) {
		throw "File not found: '" + x + "'";
		});
    }
    
}
function runit() {
     var prog = document.getElementById("code_edit").value;
     var mypre = document.getElementById("output");
     mypre.innerHTML = '';
     Sk.canvas = "mycanvas";
     Sk.pre = "output";
     Sk.configure({output:outf, read:builtinRead, error:s});
   try {
      Sk.importMainWithBody("<stdin>",false,prog);
   } catch (e) {
      alert(e);
   }
}





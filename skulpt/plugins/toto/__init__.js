var $builtinmodule = function(name)
{
    var mod = {};
    
    mod.Memory = Sk.misceval.buildClass(mod, function($gbl, $loc) {
        $loc.__init__ = new Sk.builtin.func(function(self, data) {
            document.cookie = data;
        });
		
		$loc.read = new Sk.builtin.func(function(self) {
            return document.cookie;
        });
       
    },
    'Memory', []);

    return mod;
}
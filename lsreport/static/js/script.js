$(function() {
    console.log('ready')

    function get(name){
        if(name=(new RegExp('[?&]'+encodeURIComponent(name)+'=([^&]*)')).exec(location.search))
            return decodeURIComponent(name[1]);
    }

    if($('body').is('.viewer')){
        image = 'static/image_data/nifti/' + get('image')
        mask = get('mask')
        console.log('loading papaya')
        papaya.Container.startPapaya();
        papayaContainers[0].viewer.resetViewer();
        papayaContainers[0].viewer.loadBaseImage([image], true)
    };
});
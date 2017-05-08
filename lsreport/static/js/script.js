$(function() {
    console.log('ready')

    function get(name){
        if(name=(new RegExp('[?&]'+encodeURIComponent(name)+'=([^&]*)')).exec(location.search))
            return decodeURIComponent(name[1]);
    }

    if($('body').is('.viewer')){
        console.log('loading papaya')
        papaya.Container.startPapaya();
        papayaContainers[0].viewer.resetViewer();

        image = 'static/image_data/nifti/' + get('image')
        papayaContainers[0].viewer.loadBaseImage([image], true)

        mask = 'static/image_data/nifti/' + get('mask')
        papayaContainers[0].viewer.loadOverlay([mask], true)
    };
});
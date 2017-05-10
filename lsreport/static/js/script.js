$(function() {
    console.log('ready')

    function get(name){
        if(name=(new RegExp('[?&]'+encodeURIComponent(name)+'=([^&]*)')).exec(location.search))
            return decodeURIComponent(name[1]);
    }

    if($('body').is('.nifti_viewer')){
        console.log('loading papaya for nifti')
        papaya.Container.startPapaya();
        papayaContainers[0].viewer.resetViewer();

        image = 'static/image_data/nifti/' + get('image')
        papayaContainers[0].viewer.loadBaseImage([image], true)

        mask = 'static/image_data/nifti/' + get('mask')
        papayaContainers[0].viewer.loadOverlay([mask], true)
    };

    if($('body').is('.npz_viewer')){
        console.log('loading papaya for npz')
        var dir = 'npz/' + get('dir')
        $.get(dir).done(function(data) {
            console.log('got', data)
        });
    };

});
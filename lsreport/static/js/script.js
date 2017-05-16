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
        papaya.Container.startPapaya();
        papayaContainers[0].viewer.resetViewer();

        acc_number = get('acc_number')
        ct_image = 'image_data?image_type=ct&acc_number=' + acc_number
        papayaContainers[0].viewer.loadBaseImage([ct_image], true)

        pet_image = 'image_data?image_type=pet&acc_number=' + acc_number
        papayaContainers[0].viewer.loadOverlay([pet_image], true)

        label_image = 'image_data?image_type=label&acc_number=' + acc_number
        // label image not working with papaya
        // papayaContainers[0].viewer.loadOverlay([label_image], true)
    };
});
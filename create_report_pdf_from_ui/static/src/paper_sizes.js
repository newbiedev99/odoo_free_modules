const PAPER_SIZES = {
    A0: {
        key: 'A0', 
        height: 1189.0, 
        width: 841.0
    }, 
    A1: {
        key: 'A1', 
        height: 841.0, 
        width: 594.0
    }, 
    A2: {
        key: 'A2', 
        height: 594.0, 
        width: 420.0
    }, 
    A3: {
        key: 'A3', 
        height: 420.0, 
        width: 297.0
    }, 
    A4: {
        key: 'A4', 
        height: 297.0, 
        width: 210.0
    }, 
    A5: {
        key: 'A5', 
        height: 210.0, 
        width: 148.0
    }, 
    A6: {
        key: 'A6', 
        height: 148.0, 
        width: 105.0
    }, 
    A7: {
        key: 'A7', 
        height: 105.0, 
        width: 74.0
    }, 
    A8: {
        key: 'A8', 
        height: 74.0, 
        width: 52.0
    }, 
    A9: {
        key: 'A9', 
        height: 52.0, 
        width: 37.0
    }, 
    B0: {
        key: 'B0', 
        height: 1414.0, 
        width: 1000.0
    }, 
    B1: {
        key: 'B1', 
        height: 1000.0, 
        width: 707.0
    }, 
    B2: {
        key: 'B2', 
        height: 707.0, 
        width: 500.0
    }, 
    B3: {
        key: 'B3', 
        height: 500.0, 
        width: 353.0
    }, 
    B4: {
        key: 'B4', 
        height: 353.0, 
        width: 250.0
    }, 
    B5: {
        key: 'B5', 
        height: 250.0, 
        width: 176.0
    }, 
    B6: {
        key: 'B6', 
        height: 176.0, 
        width: 125.0
    }, 
    B7: {
        key: 'B7', 
        height: 125.0, 
        width: 88.0
    }, 
    B8: {
        key: 'B8', 
        height: 88.0, 
        width: 62.0
    }, 
    B9: {
        key: 'B9', 
        height: 62.0, 
        width: 33.0
    }, 
    B10: {
        key: 'B10',
        height: 44.0, 
        width: 31.0
    }, 
    C5E: {
        key: 'C5E',
        height: 229.0, 
        width: 163.0
    }, 
    Comm10E: {
        key: 'Comm10E', 
        height: 241.0, 
        width: 105.0
    }, 
    DLE: {
        key: 'DLE',
        height: 220.0, 
        width: 110.0
    }, 
    Executive: {
        key: 'Executive', 
        height: 254.0, 
        width: 190.5
    }, 
    Folio: {
        key: 'Folio', 
        height: 330.0, 
        width: 210.0
    }, 
    Ledger: {
        key: 'Ledger', 
        height: 279.4, 
        width: 431.8
    }, 
    Legal: {
        key: 'Legal', 
        height: 355.6, 
        width: 215.9
    }, 
    Letter: {
        key: 'Letter', 
        height: 279.4, 
        width: 215.9
    }, 
    Tabloid: {
        key: 'Tabloid', 
        height: 431.8, 
        width: 279.4
    },
    custom: {
        key: 'custom', 
        height: 0.0, 
        width: 0.0
    }
}

tinymce.init({
    selector: '#editor__content',
    skins: 'material-classic',
    content_css: 'dark',
    icon: 'small',
    menubar: false,
    inline: true,
    plugins: 'quickbars table lists advlist image editimage link searchreplace preview',
    toolbar: false,
    quickbars_insert_toolbar: 'quicktable image | blocks fontfamily fontsize | link indent outdent',
    quickbars_selection_toolbar: 'blocks fontsize forecolor backcolor | bold italic underline | alignleft aligncenter alignright alignjustify | link superscript subscript indent outdent',
    quickbars_image_toolbar: 'alignleft aligncenter alignright | rotateleft rotateright | imageoptions',
    block_formats: 'Paragraph=p; Heading 1=h1; Heading 2=h2; Heading 3=h3; Heading 4=h4; Heading 5=h5; Heading 6=h6',
    color_map: [
        '#BFEDD2', 'Light Green',
        '#FBEEB8', 'Light Yellow',
        '#F8CAC6', 'Light Red',
        '#ECCAFA', 'Light Purple',
        '#C2E0F4', 'Light Blue',

        '#2DC26B', 'Green',
        '#F1C40F', 'Yellow',
        '#E03E2D', 'Red',
        '#B96AD9', 'Purple',
        '#3598DB', 'Blue',

        '#169179', 'Dark Turquoise',
        '#E67E23', 'Orange',
        '#BA372A', 'Dark Red',
        '#843FA1', 'Dark Purple',
        '#236FA1', 'Dark Blue',

        '#ECF0F1', 'Light Gray',
        '#CED4D9', 'Medium Gray',
        '#95A5A6', 'Gray',
        '#7E8C8D', 'Dark Gray',
        '#34495E', 'Navy Blue',

        '#000000', 'Black',
        '#ffffff', 'White'
    ],
    font_size_formats: '8pt 10pt 11pt 12pt 13pt 14pt 15pt 16pt 18pt 20pt 24pt 26pt 28pt 30pt 32pt 33pt 36pt 48pt',
    link_context_toolbar: true,
    image_title: true,
    automatic_uploads: true,
    file_picker_types: 'image',
    file_picker_callback: (cb, value, meta) => {
        const input = document.createElement('input');
        input.setAttribute('type', 'file');
        input.setAttribute('accept', 'image/*');

        input.addEventListener('change', (e) => {
            const file = e.target.files[0];
            const reader = new FileReader();
            reader.addEventListener('load', () => {
                const id = 'blobid' + (new Date()).getTime();
                const blobCache =  tinymce.activeEditor.editorUpload.blobCache;
                const base64 = reader.result.split(',')[1];
                const blobInfo = blobCache.create(id, file, base64);
                blobCache.add(blobInfo);
                cb(blobInfo.blobUri(), { title: file.name });
            });
            reader.readAsDataURL(file);
        });
        input.click();
    },
    setup: (editor) => {
        editor.ui.registry.addGroupToolbarButton('alignment', {
            icon: 'align-left',
            tooltip: 'Alignment',
            items: 'alignleft aligncenter alignright | alignjustify'
        });
    },
    content_style: '#editor__content { font-family:Helvetica,Arial,sans-serif; font-size:14px }'
})
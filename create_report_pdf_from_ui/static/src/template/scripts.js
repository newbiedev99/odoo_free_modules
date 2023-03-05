// DEFAULT VALUE
window.addEventListener('load', (e) => {
    const blockName = document.getElementById('block__name')
    const fontName = document.getElementById('font__name')
    const fontSize = document.getElementById('font__size')
    blockName.value = 'Paragraph'
    fontName.value = 'Arial'
    fontSize.value = '12 pt'

})

// PAPER SETTING
const paperPadding = {
    paddingTop: 0,
    paddingBottom: 0,
    paddingRight: 0,
    paddingLeft: 0,
}

const paperSettingsDialog =  {
    title: 'Paper Settings',
    body: {
        type: 'panel',
        items: [
            {
                type: 'input',
                name: 'paddingTop',
                label: 'Padding Top (mm)'
            },
            {
                type: 'input',
                name: 'paddingBottom',
                label: 'Padding Bottom (mm)'
            },
            {
                type: 'input',
                name: 'paddingRight',
                label: 'Padding Right (mm)'
            },
            {
                type: 'input',
                name: 'paddingLeft',
                label: 'Padding Left (mm)'
            },
        ]
    },
    buttons: [
        {
            type: 'cancel',
            name: 'closeButton',
            text: 'Cancel'
        },
        {
            type: 'submit',
            name: 'submitButton',
            text: 'Save',
            buttonType: 'primary'
        }
    ],
    initialData: {
        paddingTop: paperPadding.paddingTop.toString(),
        paddingBottom: paperPadding.paddingBottom.toString(),
        paddingRight: paperPadding.paddingRight.toString(),
        paddingLeft: paperPadding.paddingLeft.toString(),
    },
    onSubmit: (api) => {
        const data = api.getData();
        const paddingTop = parseInt(data.paddingTop.replace(/[^\d\.]/gm, ''))
        const paddingBottom = parseInt(data.paddingBottom.replace(/[^\d\.]/gm, ''))
        const paddingRight = parseInt(data.paddingRight.replace(/[^\d\.]/gm, ''))
        const paddingLeft = parseInt(data.paddingLeft.replace(/[^\d\.]/gm, ''))

        // CHANGE PAPER PADDING
        const padding = {
            paddingTop: paddingTop,
            paddingBottom: paddingBottom,
            paddingRight: paddingRight,
            paddingLeft: paddingLeft,
        }
        onchangePadding(padding)
        api.close();
    }
};

const papers = document.querySelectorAll('.paper')
const onchangePadding = (data) => {
    paperPadding.paddingTop = data.paddingTop
    paperPadding.paddingBottom = data.paddingBottom
    paperPadding.paddingRight = data.paddingRight
    paperPadding.paddingLeft = data.paddingLeft

    // CHANGE VALUE OF DIALOG
    paperSettingsDialog.initialData.paddingTop = data.paddingTop.toString()
    paperSettingsDialog.initialData.paddingBottom = data.paddingBottom.toString()
    paperSettingsDialog.initialData.paddingRight = data.paddingRight.toString()
    paperSettingsDialog.initialData.paddingLeft = data.paddingLeft.toString()

    papers.forEach(paper => {
        paper.style.paddingTop = paperPadding.paddingTop + 'mm'
        paper.style.paddingBottom = paperPadding.paddingBottom + 'mm'
        paper.style.paddingRight = paperPadding.paddingRight + 'mm'
        paper.style.paddingLeft = paperPadding.paddingLeft + 'mm'
    })
}


const paperSettingsButton = document.getElementById('papersettingsBTN')
paperSettingsButton.addEventListener('click', (e) => {
    tinymce.activeEditor.windowManager.open(paperSettingsDialog)
})

// SELECTION BUTTON
const selectionWrapper = document.querySelectorAll('.selection__wrapper')
selectionWrapper.forEach(selection => {
    const selectionInput = selection.querySelector('.toolbar__selection')
    const selectionButton = selection.querySelector('.button__selection')
    selectionButton.addEventListener('click', (e) => {
        if (!selectionButton.className.includes('active')){
            document.querySelectorAll('.button__selection').forEach(allButton => {
                allButton.classList.remove('active')
            })
        }
        selectionButton.classList.toggle('active')
    })
    const selectionItem = selection.querySelectorAll('.selection__item')
    selectionItem.forEach(item => {
        item.addEventListener('click', (e) => {
            let value = item.getAttribute('value')
            selectionInput.value = value
            selectionButton.classList.remove('active')
        })
    })
})

// FONT SIZE
const inputFontSize = document.getElementById('font__size')
const onchangeFontSize = (size) => {
    tinymce.activeEditor.execCommand('FontSize', false, size);
}
inputFontSize.addEventListener('change', (e) => {
    var value = e.target.value
    value = value.replace(/[^\d\.]/gm, '')
    if (value !== ''){
        value = value.split('.')
        var decimal = value.length > 1 ? '.' + value[1][0] : ''
        value = value[0] + decimal + ' pt'
    }else{
        value = '12 pt'
    }
    e.target.value = value
    var editorFontSize = value.replace('pt', 'px').split(' ').join('')
    onchangeFontSize(editorFontSize)
})


// tinymce.activeEditor.on('NodeChange', function(e) {
//     // Cek apakah posisi kursor berada pada elemen tertentu
//     if (e.element.nodeName === 'P') {
//       // Lakukan sesuatu ketika kursor diletakkan pada elemen <p>
//         console.log('Kursor berada pada elemen <p>');
//     }
// });

// TABLE
const tableButton = document.getElementById('tableBTN')
tableButton.addEventListener('click', (e) => {
    var table = `
        <table style="border-collapse: collapse; width: 100%; border-width: 1px;" border="1">
            <tbody>
                <tr>
                    <td style="width: 50%;"></td>
                    <td style="width: 50%;"></td>
                </tr>
            </tbody>
        </table>
    `
    tinymce.activeEditor.execCommand('insertHTML', false, table)
    // tinymce.activeEditor.execCommand('mceInsertTableDialog');
})

// CODE
const codeButton = document.getElementById('codeBTN')
codeButton.addEventListener('click', (e) => {
    console.log('DI SINII')
    tinymce.activeEditor.execCommand('mceCodeEditor');
})

// Cocok untuk menambahkan paper baru, karena langsung focus ke editor terakhir
// tinymce.activeEditor.execCommand('mceFocus'); 

// IMAGE
const imageButton = document.getElementById('imageBTN')
imageButton.addEventListener('click', (e) => {
    tinymce.activeEditor.execCommand('mceImage');
})

// FIND & REPLACE 
const findReplaceButton = document.getElementById('findreplaceBTN')
findReplaceButton.addEventListener('click', (e) => {
    tinymce.activeEditor.execCommand('SearchReplace');
    // tinymce.activeEditor.execCommand('mceEmoticons');
    // tinymce.activeEditor.execCommand('mceShowCharmap');
})

// LINK
const linkButton = document.getElementById('linkBTN')
linkButton.addEventListener('click', (e) => {
    tinymce.activeEditor.execCommand('mceLink');
})

// FORMAT BLOCK
const formatBlockButton = document.querySelectorAll('.format__block__button ')
formatBlockButton.forEach(formatBlock => {
    formatBlock.addEventListener('click', (e) => {
        var value = formatBlock.getAttribute('value')
        var block;
        switch (value) {
            case 'Paragraph':
                block = 'p'
                break;
            case 'Heading 1':
                block = 'h1'
                break;
            case 'Heading 2':
                block = 'h2'
                break;
            case 'Heading 3':
                block = 'h3'
                break;
            case 'Heading 4':
                block = 'h4'
                break;
            case 'Heading 5':
                block = 'h5'
                break;
            case 'Heading 6':
                block = 'h6'
                break;
            default:
                block = 'p'
                break;
        }
        tinymce.activeEditor.execCommand('FormatBlock', false, block);
    })
})

// FORMAT NAME
const formatNameButton = document.querySelectorAll('.format__name__button ')
formatNameButton.forEach(formatName => {
    formatName.addEventListener('click', (e) => {
        var p = formatName.querySelector('p')
        var fontFamily = p.style.fontFamily
        tinymce.activeEditor.execCommand('FontName', false, fontFamily);
    })
})

// BOLD
const boldBTN = document.getElementById('boldBTN')
boldBTN.addEventListener('click', (e) => {
    tinymce.activeEditor.execCommand('Bold');
})

// ITALIC
const italicButton = document.getElementById('italicBTN')
italicButton.addEventListener('click', (e) => {
    tinymce.activeEditor.execCommand('Italic');
})

// UNDERLINE
const underlineButton = document.getElementById('underlineBTN')
underlineButton.addEventListener('click', (e) => {
    tinymce.activeEditor.execCommand('Underline');
})

// STRIKETHROUGH
const strikethroughButton = document.getElementById('strikethroughBTN')
strikethroughButton.addEventListener('click', (e) => {
    tinymce.activeEditor.execCommand('Strikethrough');
})

// SUPERSCRIPT
const superscriptButton = document.getElementById('superscriptBTN')
superscriptButton.addEventListener('click', (e) => {
    tinymce.activeEditor.execCommand('Superscript');
})

// SUBSCRIPT
const subscriptButton = document.getElementById('subscriptBTN')
subscriptButton.addEventListener('click', (e) => {
    tinymce.activeEditor.execCommand('Subscript');
})

// CLEAR FORMAT
const clearFormatButton = document.getElementById('clearformatBTN')
clearFormatButton.addEventListener('click', (e) => {
    tinymce.activeEditor.execCommand('RemoveFormat');
})

// ALIGN LEFT
const alignLeftButton = document.getElementById('alignleftBTN')
alignLeftButton.addEventListener('click', (e) => {
    tinymce.activeEditor.execCommand('JustifyLeft');
})

// ALIGN CENTER
const alignCenterButton = document.getElementById('aligncenterBTN')
alignCenterButton.addEventListener('click', (e) => {
    tinymce.activeEditor.execCommand('JustifyCenter');
})

// ALIGN RIGHT
const alignRightButton = document.getElementById('alignrightBTN')
alignRightButton.addEventListener('click', (e) => {
    tinymce.activeEditor.execCommand('JustifyRight');
})

// ALIGN JUSTIFY
const alignJustifyButton = document.getElementById('alignjustifyBTN')
alignJustifyButton.addEventListener('click', (e) => {
    tinymce.activeEditor.execCommand('JustifyFull');
})


// elementEditor.forEach(editor => {
//     editor.addEventListener('input', (e) => {
//         if (tinymce.activeEditor) {
//             const editor = tinymce.activeEditor;
//             // Get the format of the current selection
//             const selectionFormat = editor.formatter.has('aligncenter');
//             console.log(selectionFormat)
//         }
//     })
// })


// SAVE
const buttonSave = document.getElementById('btn_save')
const elementEditor = document.querySelectorAll('.editor')
const editorWrapper = document.getElementById('papeWrapper')
buttonSave.addEventListener('click', (e) => {
    
    // REPLACE ATTRIBUTE style WITH data-mce-style
    const styleTinyMce = editorWrapper.querySelectorAll('[data-mce-style]')
    styleTinyMce.forEach(tinyMce => {
        var attrTinyMce = tinyMce.getAttribute('data-mce-style')
        tinyMce.setAttribute('style', attrTinyMce)
        tinyMce.removeAttribute('data-mce-style')
    })
    
    var elemHTML = editorWrapper.innerHTML
    elemHTML = elemHTML.replace(/<br( data-mce-bogus="1")?>/gm, '').replace(/<p><\/p>/gm, '')
    
    const url = "/get-report-data";
    const data = {
        report_layout: elemHTML
    }
    $.ajax({
        url: "/get-report-data",
        type: 'GET',
        contentType: "application/json",
        dataType: 'json',
        success: function(response) {
            console.log(response);
        },
        error: function(error) {
            console.log(error);
        }
    });
})


// const buttonSelection = document.querySelectorAll('.button__selection')

// buttonSelection.forEach(button => {
//     button.addEventListener('click', (e) => {
//         button.classList.toggle('active')
//     })
// })
const paperPadding = {
    paddingTop: 0,
    paddingBottom: 0,
    paddingRight: 0,
    paddingLeft: 0,
}
const papers = document.querySelectorAll('.paper')
const onchangePadding = (data) => {
    paperPadding.paddingTop = data.paddingTop
    paperPadding.paddingBottom = data.paddingBottom
    paperPadding.paddingRight = data.paddingRight
    paperPadding.paddingLeft = data.paddingLeft

    papers.forEach(paper => {
        paper.style.paddingTop = paperPadding.paddingTop + 'mm'
        paper.style.paddingBottom = paperPadding.paddingBottom + 'mm'
        paper.style.paddingRight = paperPadding.paddingRight + 'mm'
        paper.style.paddingLeft = paperPadding.paddingLeft + 'mm'
    })
}

const toggleBoldStyle = () => {
    tinymce.activeEditor.execCommand('Bold');
}

const changeFontSize = (size) => {
    tinymce.activeEditor.execCommand('FontSize', false, size);
}

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
        })
    })
})

// FONT SIZE
const inputFontSize = document.getElementById('font__size')
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
    changeFontSize(editorFontSize)
})


// SAVE
const buttonSave = document.getElementById('btn_save')
const elementEditor = document.querySelectorAll('.editor')
buttonSave.addEventListener('click', (e) => {
    elementEditor.forEach(editor => {
        console.log(editor.innerHTML)
    })
})

const cursor = document.getElementById('cursor')
cursor.addEventListener('click', (e) => {
    var myParagraph = document.getElementById("coba");
    myParagraph.focus();
    myParagraph.setSelectionRange(1, 3);
    console.log(myParagraph)
})

// TABLE
const tableButton = document.getElementById('tableBTN')
tableButton.addEventListener('click', (e) => {
    tinymce.activeEditor.execCommand('mceInsertTableDialog');
})

// IMAGE
const imageButton = document.getElementById('imageBTN')
imageButton.addEventListener('click', (e) => {
    tinymce.activeEditor.execCommand('mceImage');
})

// FIND & REPLACE 
const findReplaceButton = document.getElementById('findreplaceBTN')
findReplaceButton.addEventListener('click', (e) => {
    // tinymce.activeEditor.execCommand('SearchReplace');
    // tinymce.activeEditor.execCommand('mceEmoticons');
    tinymce.activeEditor.execCommand('mceShowCharmap');
})

// PAPER SETTING
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
        const paddingTop = data.paddingTop.replace(/[^\d\.]/gm, '')
        const paddingBottom = data.paddingBottom.replace(/[^\d\.]/gm, '')
        const paddingRight = data.paddingRight.replace(/[^\d\.]/gm, '')
        const paddingLeft = data.paddingLeft.replace(/[^\d\.]/gm, '')

        // CHANGE VALUE OF DIALOG
        paperSettingsDialog.initialData.paddingTop = paddingTop
        paperSettingsDialog.initialData.paddingBottom = paddingBottom
        paperSettingsDialog.initialData.paddingRight = paddingRight
        paperSettingsDialog.initialData.paddingLeft = paddingLeft


        // CHANGE PAPER PADDING
        const padding = {
            paddingTop: parseInt(paddingTop),
            paddingBottom: parseInt(paddingBottom),
            paddingRight: parseInt(paddingRight),
            paddingLeft: parseInt(paddingLeft),
        }
        onchangePadding(padding)

        // tinymce.activeEditor.execCommand('mceInsertContent', false, `<p>My ${pet}'s name is: <strong>${data.catdata}</strong></p>`);
        api.close();
    }
};
const paperSettingsButton = document.getElementById('papersettingsBTN')
paperSettingsButton.addEventListener('click', (e) => {
    tinymce.activeEditor.windowManager.open(paperSettingsDialog)
})
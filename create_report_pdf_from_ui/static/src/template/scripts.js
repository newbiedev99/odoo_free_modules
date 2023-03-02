// const buttonSelection = document.querySelectorAll('.button__selection')

// buttonSelection.forEach(button => {
//     button.addEventListener('click', (e) => {
//         button.classList.toggle('active')
//     })
// })

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
        var decimal = value.length > 1 ? value[1] : ''
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
const elementEditor = document.querySelectorAll('.editor__content')
buttonSave.addEventListener('click', (e) => {
    elementEditor.forEach(editor => {
        console.log(editor.innerHTML)
    })
})
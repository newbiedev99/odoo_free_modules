const paper_sizes = (paper_size, paper_height, paper_width, paper_orientation) => {
    var paper = {
        height: 0,
        width: 0
    }
    switch (paper_size) {
        case 'A0': 
            paper.height = 1189.0
            paper.width = 841.0
            break;
        case 'A1': 
            paper.height = 841.0
            paper.width = 594.0
            break;
        case 'A2': 
            paper.height = 594.0
            paper.width = 420.0
            break;
        case 'A3': 
            paper.height = 420.0
            paper.width = 297.0
            break;
        case 'A4': 
            paper.height = 297.0
            paper.width = 210.0
            break;
        case 'A5': 
            paper.height = 210.0
            paper.width = 148.0
            break;
        case 'A6': 
            paper.height = 148.0
            paper.width = 105.0
            break;
        case 'A7': 
            paper.height = 105.0
            paper.width = 74.0
            break;
        case 'A8': 
            paper.height = 74.0
            paper.width = 52.0
            break;
        case 'A9': 
            paper.height = 52.0
            paper.width = 37.0
            break;
        case 'B0': 
            paper.height = 1414.0
            paper.width = 1000.0
            break;
        case 'B1': 
            paper.height = 1000.0
            paper.width = 707.0
            break;
        case 'B2': 
            paper.height = 707.0
            paper.width = 500.0
            break;
        case 'B3': 
            paper.height = 500.0
            paper.width = 353.0
            break;
        case 'B4': 
            paper.height = 353.0
            paper.width = 250.0
            break;
        case 'B5': 
            paper.height = 250.0
            paper.width = 176.0
            break;
        case 'B6': 
            paper.height = 176.0
            paper.width = 125.0
            break;
        case 'B7': 
            paper.height = 125.0
            paper.width = 88.0
            break;
        case 'B8': 
            paper.height = 88.0
            paper.width = 62.0
            break;
        case 'B9': 
            paper.height = 62.0
            paper.width = 33.0
            break;
        case 'B10':
            paper.height = 44.0
            paper.width = 31.0
            break;
        case 'C5E':
            paper.height = 229.0
            paper.width = 163.0
            break;
        case 'Comm10E': 
            paper.height = 241.0
            paper.width = 105.0
            break;
        case 'DLE':
            paper.height = 220.0
            paper.width = 110.0
            break;
        case 'Executive': 
            paper.height = 254.0
            paper.width = 190.5
            break;
        case 'Folio': 
            paper.height = 330.0
            paper.width = 210.0
            break;
        case 'Ledger': 
            paper.height = 279.4
            paper.width = 431.8
            break;
        case 'Legal': 
            paper.height = 355.6
            paper.width = 215.9
            break;
        case 'Letter': 
            paper.height = 279.4
            paper.width = 215.9
            break;
        case 'Tabloid': 
            paper.height = 431.8, 
            paper.width = 279.4
            break;
        default:
            paper.height = paper_height
            paper.width = paper_width
            break;
    }
    if (paper_size.toLowerCase() !== 'custom' && paper_orientation.toLowerCase() === 'landscape'){
        default_height = paper.height
        default_width = paper.width
        paper.height = default_width
        paper.width = default_height
    }
    return paper
}

const compute_paper_size = (orientation, page_height, page_width, paper_size) => {
    var paper_utils = paper_sizes(paper_size,page_height,page_width,orientation)
    const paper_document = document.querySelectorAll('.paper')
    console.log(paper_document)
    paper_document.forEach(paper => {
        paper.style.width = paper_utils.width + 'mm'
        paper.style.height = paper_utils.height + 'mm'
    })
}
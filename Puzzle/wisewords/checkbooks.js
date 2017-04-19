const fs = require('fs')
const _ = require('lodash')

const data = fs.readFileSync('./bookData', 'utf8')
const books = JSON.parse(data)
const isbns = Object.keys(books)

const getTitle = (isbn) => {
    switch (isbn) {
        case '9781855732735': return 'Education and Training in Food Science'
        case '9781845696061': return 'A Complete Course in Canning and Related Processes, Thirteenth Edition: Processing Procedures for Canned Food Products'
        case '9781845696023': return 'Unit Operations for the Food Industries'
        case '9780953194995': return 'Lipids: Structure, Physical Properties and Functionality (Oily Press Lipid Library Series)'
        default:
    }
    let data = books[isbn].data[0]
    return data.title
}

let problemData = JSON.parse(fs.readFileSync('./output', 'utf8'))

let res = ''

_.flatMap(problemData).forEach(isbn => {
    const char = getTitle(isbn)[0]
    res = res + char
})

console.log(res);
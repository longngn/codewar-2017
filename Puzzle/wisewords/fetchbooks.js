require('isomorphic-fetch')
const _ = require('lodash')
const fs = require('fs')

const fetchBook = async (isbn) => {
    const response = await fetch(`http://isbndb.com/api/v2/json/M2AG85K5/book/${isbn}`)
    const data = await response.json()
    return data
}

const fetchAllBooks = async (isbns) => {
    for(let i = 0; i < isbns.length; i++) {
        const isbn = isbns[i]
        console.log(`Began ${i} (isbn: ${isbn})`);
        let data
        try { data = await fetchBook(isbn) } catch(e) { console.log(`Error: ${e}`);}
        books[isbn] = data
        console.log(`Finished ${i}`);
    }
}

const books = {}

const isbns = fs.readFileSync('./output', 'utf8').split('\n').filter(line => line)
const uniqIsbns = _.uniq(isbns)

fetchAllBooks(uniqIsbns).then(res => {
    fs.writeFileSync('./bookData', JSON.stringify(books), 'utf8')    
})

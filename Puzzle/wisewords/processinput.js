const fs = require('fs')
const _ = require('lodash')

const data = fs.readFileSync('./input', 'utf8')
const lines = data.split('\n')
const linesBlocks = _.chunk(lines, 14)

const isbnBlocks = linesBlocks.map(block => {
    const poses = [];
    [...block[0]].forEach((char, index) => char !== ' '? poses.push(index):0)
    const res = new Array(poses.length).fill('')
    block.forEach((line, idx) => {
        if (idx === 13) return
        poses.forEach((pos, index) => {
            res[index] += line[pos]
        })
    })
    return res
})

fs.writeFileSync('./output', JSON.stringify(isbnBlocks))
import React from 'react'
import './Block.css'

const Variable = ({ content, size = 8, bgColor = "#222", onDataUpdate = null }) => {
  let c = content.slice()
  if (c.length < size) {
    for (let i = c.length; i < size; i++) {
      c.push(null)
    }
  }

  onDataUpdate && onDataUpdate(c.map(x => x === null ? 0x0 : x))
  return (
    <div className="block-container">
      { c.map((val, index) => <Block content={val ? "0x" + val.toString(16) : ''} key={index} bgColor={bgColor} />) }
    </div>
  )
}

const Block = ({ content, bgColor }) => {
  return (
    <div className="block" style={{ backgroundColor: bgColor }}>
      <span className="block-content">{content}</span>
    </div>
  )
}

export {
  Block,
  Variable
};

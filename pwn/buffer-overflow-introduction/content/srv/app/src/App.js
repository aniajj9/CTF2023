import React, { Component } from 'react'
import bigInt from 'big-integer'
import './App.css'
import { instructions } from './instructions'
import { cProgram } from './ccode-live'
import { Variable } from './Block'

const FLAG = "CTF{basic_buffer_overflows_are_simple_and_powerfull}"

const byteToBit = (bytes) => [].concat.apply([], bytes.map(x => [7,6,5,4,3,2,1,0].map(i => (x >>> i) & 1)))
const byteToBitEndian = (bytes, littleEndian=true) => {
  const b = bytes.slice()
  if (littleEndian)
    b.reverse()
  return byteToBit(b)
}
const toInt = (bytes, signed=false, littleEndian=true) => {
  let bits = byteToBitEndian(bytes)
  let bitflip = false
  if (signed && bits[0] === 1) {
    bitflip = true
    // Negate the entire thing
    bits = bits.map(x => x === 1 ? 0 : 1)
  }
  let num = bigInt.fromArray(bits, 2)
  if (bitflip) {
    num = num.not()
  }
  return num
}

// C style string
const toStr = (data) => {
  const idx = data.indexOf(0x00)
  const d2 = data.slice(0, idx !== -1 ? idx : data.length)
  return d2.map(x => String.fromCharCode(x)).join("")
}

const Memory = ({ state, content }) => {
  let index = 0
  const newState = state.map((s) => {
    const ret = {
      ...s, 
      content: content.slice(index, index + s.size)
    }
    index += s.size
    return ret
  })
  return (
    <div className="block-wrapper" >
      { newState.map((s, index) => <Variable key={index} {...s} />) }
    </div>
  )
}

class App extends Component {
  constructor(props) {
    super(props)
    this.instructionStep = 0
    this.memoryState = [
      {
        size: 16,
        bgColor: "#f44d41",
        onDataUpdate: (data) => {
          const str = toStr(data)

          this.sendMessage({
            event: "code",
            code: `    char buf[16] = ${JSON.stringify(str)};`, 
            file: 'overflow.c', 
            index: 1
          })
          if (str === 'Hello World!') {
            this.setInstructionStep(1)
          }
        }
      },
      { 
        size: 4,
        bgColor: "#0b9116",
        onDataUpdate: (data) => {
          const int = toInt(data, true)
          const uint = toInt(data)

          this.sendMessage({
            event: "code",
            code: `    int secret = ${int.toString()}; // 0x${uint.toString(16)}`, 
            file: 'overflow.c', 
            index: 3
          })

          if (int.neq(0)) {
            this.setInstructionStep(2)
          }
          
          if (int.eq(0x61616161)) {
            this.setInstructionStep(3)
          } else if (int.eq(0x61626364)) {
            this.setInstructionStep(4)
          } else if (uint.eq(0xcafebabe)) {
            this.setInstructionStep(5)
            this.sendMessage({event: "flag", flag: FLAG})
          }
        }
      }
    ]
    this.totalMemorySize = this.memoryState.reduce((acc, val) => acc + val.size, 0)
    this.state = {
      error: '',
      buffer: "",
      memory: []
    }
    this.buildInstructionHTML();
    this.prepareCode();
  }

  buildInstructionHTML(){
    this.instructionHtml = "<ol>"

    for (let i = 0; i < instructions.length && i <= this.instructionStep; i++)
    {
      let classAttr = (i < this.instructionStep ? " class='completed'": "");
      this.instructionHtml += "<li " + classAttr + "><b>" + instructions[i].title + "</b><br />"
      this.instructionHtml += instructions[i].description

      if(instructions[i].hint){
        this.instructionHtml += "<div class='hint hidden'><button onclick='this.parentElement.className=\"hint\"'>Show hint</button> <span class='text'>"
        this.instructionHtml += instructions[i].hint.text
        this.instructionHtml += "</span></div>"
      }
      this.instructionHtml += "</li>"
    }

    this.instructionHtml += "</ol>"
  }

  sendMessage(json){

    switch(json.event)
    {
      case "code":
        if(this.ccode[json.index] !== json.code){
          this.ccode[json.index] = json.code;
          this.forceUpdate();
        }
        break;
      case "instruction_step":
        this.buildInstructionHTML();
        break;
      case "flag":
        if(instructions.length < 6){
          instructions[5] = {
            title: "Take flag",
            description: "FLAG: " + FLAG
          }
          this.buildInstructionHTML();
        }
        break;
    }
  }

  prepareCode(){
    this.ccode = cProgram.split("    /// LIVE CODE")
  }

  setInstructionStep(step) {
    if (this.instructionStep + 1 != step) return 

    this.instructionStep = step
    this.sendMessage({
      event: "instruction_step",
      step: step
    })

  }

  handleBufferUpdate = (event) => {
    const buffer = event.target.value
    // On error still set the state as the user might just be writing more data
    this.setState({ buffer })
    let val
    try {
      const json = `"${buffer.replace(/"/g, '\\"').replace(/\\x/g, "\\u00")}"`
      val = JSON.parse(json)
    } catch (e) {
      return
    }
    const memory = [...val].map(x => x.charCodeAt(0))
    if (memory.length > this.totalMemorySize)
      return this.setState({ error: 'Input is too long' })
    if (memory.filter(x => x <= 0xff).length !== memory.length)
      return this.setState({ error: 'Characters larger than 1 byte are not supported' })
    this.setState({ error: '', memory })
  }
  render() {
    return (
      <div className="app">
        <div className="instructions">
          <h2>Instructions</h2>
          <div dangerouslySetInnerHTML={{__html: this.instructionHtml}}></div>
         </div> 
        <div className="c-code"><pre>{this.ccode[0]}{this.ccode[1]}{this.ccode[2]}{this.ccode[3]}{this.ccode[4]}</pre></div>
        <header className="header">
          <div className="title">
            <h1>./overflow &lt;argument&gt;</h1>
          </div>
          <div className="input-container">
            <input 
              type="text"
              placeholder="&lt;argument&gt;" 
              className="buffer-input" 
              value={this.state.buffer}
              onChange={this.handleBufferUpdate} 
            />
          </div>
          <div className="error">{this.state.error}</div>
        </header>
        <Memory state={this.memoryState} content={this.state.memory} />
      </div>
    )
  }
}

export default App;

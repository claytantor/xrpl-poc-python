import React from "react"
import "./App.css"

function App() {
    return (<div className="p-4">
        <h2 className="text-2xl">Welcome to React App Foo</h2>
        <h3>Date : {new Date().toDateString()}</h3>
        <h1 class="bg-red-900 text-white">Hello world</h1>
    </div>)
}

export default App
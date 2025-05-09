
import { useState } from "react";
import { Tab } from "../types.ts"

import "./Tabs.css"

interface TabsProps {
    options : Tab[],
}

function Tabs({ options } : TabsProps) {
    const [selected, setSelected] = useState(0);

    return (
      <div className="tab-container">
        <ul className="tab-selector">
          {options.map((option, i) => (
            <li key={i} onClick={() => setSelected(i)} className={i===selected ? "tab selected" : "tab"}>{option.title}</li>
          ))}
        </ul>
        <div className="tab-content">{
          options.map((e, i) => (<div key={i} className={i === selected ? "content" : "content hidden"}>{e.element}</div>))
        }</div>
      </div>
    );
}


export default Tabs;
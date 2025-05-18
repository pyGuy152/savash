
import "./AssignmentList.css"

import { Assignment } from "../types.ts"

interface AssignmentListProps {
    list : Assignment[]
}

import "./potion.css"
import { useRef } from "react";


function AssignmentList({ list }:AssignmentListProps) {

  const bubs = useRef<HTMLDivElement>(null);
  const pot = useRef<HTMLImageElement>(null);


  function addBubbles() {

    document.body.style.filter = "hue-rotate(-90deg)";

    pot.current!.style.filter = "hue-rotate(90deg)";

    setTimeout(() => {
      document.body.style.filter = "none";
      pot.current!.style.filter = "none";
    }, 5000);

    bubs.current!.innerHTML = "";
    const text = document.createElement("h1");
    text.className = "bubble-title";
    text.innerText = "Procrastination Potion"
    text.style.animation = "bubble 5s 2s ease-in forwards"
    bubs.current!.appendChild(text);
    for(let x = 0; x < 100; x++){
      bubs.current!.innerHTML += `<div
        class="bubble"
        style="
          left: ${Math.random()*window.innerWidth + "px"};
          animation: bubble 2s ${x / 20.0}s forwards ease-in;"
      ></div>`;
    }
  }


    if(list.length == 0){
        return (
          <ul className="assignment-list">
            <h2 className="noAssignments">No assignments yet.</h2>
            <img
              id="potion"
              ref={pot}
              src="/potion.png"
              onClick={addBubbles}
            ></img>
            <div className="bubbles" ref={bubs}></div>
          </ul>
        );
    }
    

    return (
      <ul className="assignment-list">
        {list.map((row, i) => (
          <li key={i} className="row">
            <div className="left">
              <img src="/icons/paperclip.png"></img>
              <p>{row.title}</p>
            </div>
            <p>{row.due_date && row.due_date.toLocaleDateString()}</p>
          </li>
        ))}
        <img id="potion" src="/potion.png" onClick={addBubbles}></img>
        <div className="bubbles">
        </div>
      </ul>
    );
}

export default AssignmentList;

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
  const p1 = useRef<HTMLImageElement>(null);
  const p2 = useRef<HTMLImageElement>(null);
  const procras = useRef<HTMLHeadingElement>(null)


  function addBubbles() {

    bubs.current!.innerHTML = "";

    document.body.style.filter = "hue-rotate(-90deg)";
    document.body.style.overflowY = "hidden";

    p1.current!.classList.add("swing");
    p2.current!.classList.add("swing");

    pot.current!.style.filter = "hue-rotate(90deg)";

    setTimeout(() => {
      document.body.style.filter = "none";
      document.body.style.overflowY = "scroll";
      pot.current!.style.filter = "none";
    p1.current!.classList.remove("swing");
    p2.current!.classList.remove("swing");
    }, 6000);

    const text = document.createElement("h1");
    text.className = "bubble-title";
    text.innerText = "Lock In"
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
      <>
        <ul className="assignment-list">
          <h2>No Assignments Yet.</h2>
          <img
            id="potion"
            src="/potion.png"
            ref={pot}
            onClick={addBubbles}
            onMouseOver={() => procras.current!.classList.add("show")}
            onMouseLeave={() => procras.current!.classList.remove("show")}
          ></img>
          <h2 className="procras" ref={procras}>
            Procrastinating?
          </h2>
          <div className="bubbles" ref={bubs}></div>
        </ul>
        <img
          ref={p1}
          className="pendulum"
          src="/pendulum/pendulum.png"
          alt=""
        />
        <img
          ref={p2}
          className="pendulum-charm"
          src="/pendulum/pendulum-charm.png"
          alt=""
        />
      </>;
    }
    

    return (
      <>
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
          <img
            id="potion"
            src="/potion.png"
            ref={pot}
            onClick={addBubbles}
            onMouseOver={() => procras.current!.classList.add("show")}
            onMouseLeave={() => procras.current!.classList.remove("show")}
          ></img>
          <h2 className="procras" ref={procras}>
            Procrastinating?
          </h2>
          <div className="bubbles" ref={bubs}></div>
        </ul>
        <img
          ref={p1}
          className="pendulum"
          src="/pendulum/pendulum.png"
          alt=""
        />
        <img
          ref={p2}
          className="pendulum-charm"
          src="/pendulum/pendulum-charm.png"
          alt=""
        />
      </>
    );
}

export default AssignmentList;
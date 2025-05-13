
import "./Slider.css"
import { useState } from "react";

interface SliderProps {
    options : string[];
    setSelectedType : Function;
}

function Slider({ options, setSelectedType }: SliderProps) {

    const [left, setLeft] = useState(0);

  function selectOption(i: number) {
    let options = document.getElementsByClassName("option");
    setSelectedType(i);
    setLeft((options[i] as HTMLElement).offsetLeft-10);
  }

  return (
    <div className="slider">
      <ul>
        {options.map((option, i) => (
          <li key={i} onClick={() => selectOption(i)} className="option">
            {option}
          </li>
        ))}
      </ul>
      <div style={{left}} className="selected"></div>
    </div>
  );
}

export default Slider;
import { useEffect, useRef, useState } from "react";
import HomeNav from "./components/HomeNav";

import "./Theme.css";

import "./Classes.css"

function Theme() {
  const [themeColors, setThemeColors] = useState(
    localStorage.getItem("theme")
      ? JSON.parse(localStorage.getItem("theme")!)
      : {
          backgroundColor: "#D9D9D9",
          textColor: "#000000",
          navColor: "#F4EEEE",
          submitColor: "#5BB861",
          tint: "#dfdfa2",
          tabBackgroundColor: "#ccccb5",
          midColor: "#b9b9b9",
          warningColor: "#c70a0a",
        }
  );

  useEffect(() => {
    let str = "";
    for (const key in themeColors) {
      if (Object.prototype.hasOwnProperty.call(themeColors, key)) {
        str += `--${key}: ${themeColors[key as keyof typeof themeColors]};`;
      }
    }
    console.log(str);
    document.body.style = str;
    localStorage.setItem("theme", JSON.stringify(themeColors));
  }, [themeColors]);

  function selectPreset(preset: string) {
    switch (preset) {
      case "pink":
        setThemeColors({
          backgroundColor: "#F9D9D9",
          textColor: "#000000",
          navColor: "#F4EEEE",
          submitColor: "#FBB861",
          tint: "#Ffdfa2",
          tabBackgroundColor: "#Fcccb5",
          midColor: "#F9b9b9",
          warningColor: "#c70a0a",
        });
        break;
      case "bean":
        setThemeColors(
          JSON.parse(
            '{"backgroundColor":"#6e5e5e","textColor":"#3f3131","navColor":"#aa8d8d","submitColor":"#bfa982","tint":"#6f6f4d","tabBackgroundColor":"#ccccb5","midColor":"#a07979","warningColor":"#892f2f"}'
          )
        );
        break;
      default:
        setThemeColors({
          backgroundColor: "#D9D9D9",
          textColor: "#000000",
          navColor: "#F4EEEE",
          submitColor: "#5BB861",
          tint: "#dfdfa2",
          tabBackgroundColor: "#ccccb5",
          midColor: "#b9b9b9",
          warningColor: "#c70a0a",
        });
        break;
    }
  }

  const exportArea = useRef<HTMLParagraphElement>(null);

  return (
    <>
      <HomeNav />
      <h1>Theme Editor</h1>
      <div className="row">
        <label htmlFor="presets">Presets:</label>
        <select
          onChange={(e) => {
            selectPreset(e.target.value);
          }}
          name="Presets"
          id="presets"
        >
          <option value="default">Default</option>
          <option value="pink">Pink</option>
          <option value="bean">Bean</option>
        </select>
      </div>
      <hr></hr>
      <div id="color-selector">
        {Object.entries(themeColors).map(([key, value]) => (
          <div className="row" key={key}>
            <label htmlFor={key}>{key}</label>
            <input
              className="color-select"
              type="color"
              id={key}
              value={value as string}
              onChange={(e) =>
                setThemeColors({
                  ...themeColors,
                  [key]: e.target.value,
                })
              }
            />
          </div>
        ))}
      </div>
      <hr />
      <ul className="class-samples">
        <li className="class">
          <div className="header">
            <h2>Sample</h2>
            <hr />
            <p>5/29/2025</p>
          </div>
          <h2 className="code">1234567</h2>
        </li>
        <li className="class">
          <div className="header">
            <h2>Sample2</h2>
            <hr />
            <p>5/29/2025</p>
          </div>
          <h2 className="code">1234567</h2>
        </li>
      </ul>
      <hr />
      <p ref={exportArea} className="exportData"></p>
      <div className="custom">
        <button
          id="export"
          onClick={() => {
            exportArea.current!.innerText = JSON.stringify(themeColors);
          }}
        >
          Export
        </button>

        <button
          id="load"
          onClick={() => {
            const data = prompt("Paste your theme data:");
            if (data) {
              setThemeColors(JSON.parse(data));
            } else {
              alert("Invalid");
            }
          }}
        >
          Load
        </button>
      </div>
      <hr />
    </>
  );
}

export default Theme;

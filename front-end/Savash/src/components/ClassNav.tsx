import { Link } from "react-router-dom";
import { Class, loadTheme } from "../types";
import "./HomeNav.css"

interface ClassNavProps {
  classSelected: Class;
  inviteModalToggle: (event: React.MouseEvent<HTMLButtonElement, MouseEvent>) => void;
}

function ClassNav({ classSelected, inviteModalToggle }: ClassNavProps) {

  loadTheme();
  return (
    <nav className="HomeNav">
      <ul className="left">
        <li>
          <Link to="/classes">
            <img src="/icons/chevron.png" alt="Back" className="rotate-90deg" />{" "}
            Back
          </Link>
        </li>
      </ul>
      <ul className="center">
        <li>
          <p className="class-title">{classSelected.name}</p>
        </li>
      </ul>
      <ul className="right">
        {
          localStorage.getItem("role") === 'teacher' ? (<><li>
          <Link to="./add">
            <button className="register gray">Add Assignment</button>
          </Link>
        </li>
        <li>
          <button onClick={inviteModalToggle} className="register">
            Invite
          </button>
        </li></>) : 
        (<>
          
        </>)
        }
      </ul>
    </nav>
  );
}

export default ClassNav;
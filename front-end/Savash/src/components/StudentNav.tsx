


import "./HomeNav.css";

import { Link, useNavigate } from "react-router-dom";

import { LOGOUT } from "../types.ts"

function StudentNav() {
  const navigate = useNavigate();

  function handleLogout(){
    LOGOUT();
    navigate("/");
  }

  return (
    <nav className="HomeNav">
      <ul className="left">
        <li>
          <p onClick={handleLogout}>Logout</p>
        </li>
        <li>
          <Link to="/contact">Contact</Link>
        </li>
        <li>
          <Link to="/wiki">Wiki</Link>
        </li>
      </ul>
      <ul className="right">
        <li>
          <Link to="/inbox">
            <img className="icon" src="/icons/inbox.png"></img>
          </Link>
        </li>
        <li>
          <Link to="/dashboard">Dashboard</Link>
        </li>
        <li>
          <Link to="/join">
            <button className="register">Join</button>
          </Link>
        </li>
      </ul>
    </nav>
  );
}

export default StudentNav;
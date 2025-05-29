

import { useEffect, useRef } from "react";
import { apiUrl, getToken, loadTheme, LOGOUT } from "../types";
import "./HomeNav.css";

import { Link, useNavigate } from "react-router-dom";




function TeacherNav() {
  const navigate = useNavigate();
  const inboxIcon = useRef(null);

  loadTheme();

  function handleLogout(){
    LOGOUT();
    navigate("/");
  }

  function newMessage(){
      fetch(apiUrl + "/users/", {
          method: "GET",
          headers: {
            Authorization: "bearer " + getToken(document.cookie),
          },
        })
        .then((res) => res.json())
        .then((data) => {
            console.log(data);
            if (!data || data.join_req.length === 0) {
              (inboxIcon.current! as HTMLUListElement).className = "inbox";
            }
            else{
              (inboxIcon.current! as HTMLUListElement).className = "inbox new";
            }
        });
  }

  useEffect(newMessage, [])

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
            <Link to="/theme">Theme</Link>
          </li>
        </ul>
        <ul className="right">
        <li className="inbox" ref={inboxIcon}>
           <Link to="/inbox">
                <img className="icon" src="/icons/inbox.png"></img>
           </Link> 
        </li>
          <li>
            <Link to="/classes">Classes</Link>
          </li>
          <li>
            <Link to="/create">
                <button className="register">Create</button>
            </Link>
          </li>
        </ul>
      </nav>
    );
}

export default TeacherNav;

//wwwwwwwwwwwwdwwfwfwwwww